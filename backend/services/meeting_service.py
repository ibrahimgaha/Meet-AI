import asyncio
from datetime import datetime
import json
from pathlib import Path
import threading
from typing import Dict, List, Optional, Set

from playwright.sync_api import sync_playwright

from audio.recorder import record_continuously
from backend.models.meeting import MeetingStatus, MeetingSummary
from backend.services.processing_service import process_meeting_with_progress
from meet.browser import (
    connect_to_chrome,
    join_meeting,
    leave_meeting,
    open_meeting,
    verify_meeting,
)
from meet.tracker import track_participants

BASE_MEETINGS_DIR = Path("meetings")


class MeetingSessionState:
    def __init__(self, meeting_id: str, meet_url: str):
        self.meeting_id = meeting_id
        self.meet_url = meet_url
        self.status = MeetingStatus.connecting
        self.message = "Initializing meeting session..."
        self.error: Optional[str] = None
        self.started_at: Optional[str] = None
        self.joined_at: Optional[str] = None
        self.ended_at: Optional[str] = None
        self.participants: List[str] = []
        self.progress_step: Optional[str] = None
        self.meeting_dir = BASE_MEETINGS_DIR / meeting_id
        self.stop_requested = threading.Event()
        self.is_running = True

    def to_dict(self):
        return {
            "meeting_id": self.meeting_id,
            "meet_url": self.meet_url,
            "status": self.status.value,
            "message": self.message,
            "error": self.error,
            "started_at": self.started_at,
            "joined_at": self.joined_at,
            "ended_at": self.ended_at,
            "participants": self.participants,
            "progress_step": self.progress_step,
        }


class MeetingService:
    def __init__(self):
        self.active_meeting: Optional[MeetingSessionState] = None
        self._lock = threading.Lock()
        self._subscribers: Dict[str, Set[asyncio.Queue]] = {}

    def get_active_meeting(self) -> Optional[MeetingSessionState]:
        return self.active_meeting

    def start_meeting(self, meet_url: str) -> MeetingSessionState:
        with self._lock:
            if self.active_meeting and self.active_meeting.is_running:
                raise RuntimeError("A meeting session is already in progress.")

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            meeting_state = MeetingSessionState(timestamp, meet_url)
            meeting_state.started_at = datetime.now().isoformat()
            self.active_meeting = meeting_state

            # Launch runner in background thread
            runner_thread = threading.Thread(
                target=self._run_meeting_lifecycle,
                args=(meeting_state,),
                daemon=True,
                name=f"MeetingRunner-{timestamp}"
            )
            runner_thread.start()
            return meeting_state

    def stop_meeting(self, meeting_id: str) -> bool:
        with self._lock:
            if not self.active_meeting or self.active_meeting.meeting_id != meeting_id:
                return False
            if not self.active_meeting.is_running:
                return False
            self.active_meeting.stop_requested.set()
            return True

    def update_state(self, state: MeetingSessionState, status: MeetingStatus, message: str, error: Optional[str] = None, progress_step: Optional[str] = None):
        state.status = status
        state.message = message
        if error:
            state.error = error
        if progress_step:
            state.progress_step = progress_step
        self.broadcast(state.meeting_id, state.to_dict())

    def subscribe(self, meeting_id: str) -> asyncio.Queue:
        queue = asyncio.Queue()
        if meeting_id not in self._subscribers:
            self._subscribers[meeting_id] = set()
        self._subscribers[meeting_id].add(queue)
        return queue

    def unsubscribe(self, meeting_id: str, queue: asyncio.Queue):
        if meeting_id in self._subscribers:
            self._subscribers[meeting_id].discard(queue)
            if not self._subscribers[meeting_id]:
                del self._subscribers[meeting_id]

    def broadcast(self, meeting_id: str, payload: dict):
        if meeting_id in self._subscribers:
            for queue in list(self._subscribers[meeting_id]):
                try:
                    queue.put_nowait(payload)
                except Exception:
                    pass

    def _run_meeting_lifecycle(self, state: MeetingSessionState):
        meeting_dir = state.meeting_dir
        recordings_dir = meeting_dir / "recordings"
        recordings_dir.mkdir(parents=True, exist_ok=True)

        stop_event = state.stop_requested
        recorder_thread: Optional[threading.Thread] = None
        playwright_instance = None
        page = None

        try:
            # 1. Connect to Chrome
            self.update_state(state, MeetingStatus.connecting, "Connecting to Chrome via remote debugging (port 9222)...")
            playwright_instance = sync_playwright().start()
            browser, context, page = connect_to_chrome(playwright_instance)

            # 2. Open Google Meet
            self.update_state(state, MeetingStatus.opening_meet, f"Opening Google Meet: {state.meet_url}...")
            open_meeting(page, state.meet_url)

            # 3. Join Meeting
            self.update_state(state, MeetingStatus.joining, "Clicking join button...")
            join_meeting(page)

            # 4. Verify Bot Joined
            if not verify_meeting(page):
                raise RuntimeError("Failed to verify bot inside Google Meet.")

            state.joined_at = datetime.now().isoformat()

            # 5. Start Audio Recorder Thread
            self.update_state(state, MeetingStatus.recording, "Bot joined call. Audio recording & participant tracking active.")
            recorder_thread = threading.Thread(
                target=record_continuously,
                kwargs={
                    "output_directory": str(recordings_dir),
                    "chunk_duration": 60,
                    "stop_event": stop_event,
                },
                daemon=True,
                name=f"AudioRecorder-{state.meeting_id}"
            )
            recorder_thread.start()

            # 6. Track participants loop (blocks until call ends or stop_event)
            def on_participants_change(participants_list):
                state.participants = participants_list
                self.broadcast(state.meeting_id, state.to_dict())

            track_participants(
                page=page,
                stop_event=stop_event,
                meeting_directory=meeting_dir,
                on_change=on_participants_change
            )

        except Exception as e:
            err_msg = str(e)
            print(f"❌ Meeting lifecycle error: {err_msg}")
            self.update_state(state, MeetingStatus.error, f"Meeting error: {err_msg}", error=err_msg)
        finally:
            state.ended_at = datetime.now().isoformat()
            self.update_state(state, MeetingStatus.ending, "Meeting ended. Finalizing audio recording...")

            # Leave meeting if page open
            if page:
                try:
                    leave_meeting(page)
                except Exception as e:
                    print(f"Error leaving meeting: {e}")

            # Stop audio recorder
            stop_event.set()
            if recorder_thread and recorder_thread.is_alive():
                recorder_thread.join(timeout=15)

            # Close Playwright context
            if playwright_instance:
                try:
                    playwright_instance.stop()
                except Exception:
                    pass

        # If there was an unrecoverable pre-recording error, we skip processing
        if state.status == MeetingStatus.error:
            state.is_running = False
            return

        # 7. Post-meeting audio & AI processing pipeline
        try:
            self.update_state(state, MeetingStatus.processing_audio, "Starting audio processing pipeline...")

            def on_processing_step(status: MeetingStatus, message: str):
                self.update_state(state, status, message, progress_step=status.value)

            process_meeting_with_progress(
                meeting_directory=meeting_dir,
                status_callback=on_processing_step,
                auto_map=True
            )
            self.update_state(state, MeetingStatus.completed, "Meeting processing successfully completed.")
        except Exception as e:
            err_msg = f"Post-processing failed: {e}"
            print(f"❌ {err_msg}")
            self.update_state(state, MeetingStatus.error, err_msg, error=err_msg)
        finally:
            state.is_running = False

    def list_all_meetings(self) -> List[MeetingSummary]:
        if not BASE_MEETINGS_DIR.exists():
            return []

        meetings: List[MeetingSummary] = []
        for folder in sorted(BASE_MEETINGS_DIR.iterdir(), reverse=True):
            if not folder.is_dir():
                continue

            meeting_id = folder.name
            participants_file = folder / "participants.json"
            transcript_file = folder / "transcripts" / "transcript.txt"
            analysis_file = folder / "analysis" / "analysis.txt"
            report_file = folder / "reports" / "meeting_report.pdf"

            participants: List[str] = []
            if participants_file.exists():
                try:
                    data = json.loads(participants_file.read_text(encoding="utf-8"))
                    participants = data.get("participants", [])
                except Exception:
                    pass

            is_active = self.active_meeting and self.active_meeting.meeting_id == meeting_id and self.active_meeting.is_running
            if is_active:
                status = self.active_meeting.status.value
            elif report_file.exists():
                status = "completed"
            elif transcript_file.exists():
                status = "completed"
            else:
                status = "ended"

            meetings.append(
                MeetingSummary(
                    meeting_id=meeting_id,
                    status=status,
                    participants=participants,
                    has_transcript=transcript_file.exists(),
                    has_analysis=analysis_file.exists(),
                    has_report=report_file.exists(),
                )
            )

        return meetings


# Global singleton service
meeting_service = MeetingService()
