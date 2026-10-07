from enum import Enum
from typing import Optional

from pydantic import BaseModel


# ============================================================
# MEETING STATUS
# ============================================================

class MeetingStatus(str, Enum):
    """All possible states of a meeting lifecycle."""

    connecting = "connecting"
    opening_meet = "opening_meet"
    joining = "joining"
    recording = "recording"
    ending = "ending"
    processing_audio = "processing_audio"
    merging_audio = "merging_audio"
    transcribing = "transcribing"
    diarizing = "diarizing"
    mapping_speakers = "mapping_speakers"
    analyzing = "analyzing"
    generating_report = "generating_report"
    completed = "completed"
    error = "error"


# ============================================================
# STATUS DISPLAY LABELS
# ============================================================

STATUS_LABELS = {
    "connecting": "Connecting to Chrome",
    "opening_meet": "Opening Google Meet",
    "joining": "Joining meeting",
    "recording": "Recording",
    "ending": "Meeting ended",
    "processing_audio": "Processing audio",
    "merging_audio": "Merging audio chunks",
    "transcribing": "Whisper transcription",
    "diarizing": "Speaker diarization",
    "mapping_speakers": "Speaker mapping",
    "analyzing": "AI analysis",
    "generating_report": "Generating PDF report",
    "completed": "Completed",
    "error": "Error",
}


# Processing steps in order — used by the frontend
# to render a progress timeline.

PROCESSING_STEPS = [
    "merging_audio",
    "transcribing",
    "diarizing",
    "mapping_speakers",
    "analyzing",
    "generating_report",
]


# ============================================================
# REQUEST / RESPONSE MODELS
# ============================================================

class StartMeetingRequest(BaseModel):
    """POST /api/meetings/start body."""

    meet_url: str


class MeetingSummary(BaseModel):
    """Lightweight summary for the meeting list."""

    meeting_id: str
    status: str
    started_at: Optional[str] = None
    ended_at: Optional[str] = None
    participants: list[str] = []
    duration_seconds: Optional[float] = None
    has_transcript: bool = False
    has_analysis: bool = False
    has_report: bool = False
