import asyncio
import json
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, PlainTextResponse

from backend.models.meeting import MeetingSummary, StartMeetingRequest
from backend.services.meeting_service import meeting_service

router = APIRouter(prefix="/api/meetings", tags=["meetings"])
BASE_MEETINGS_DIR = Path("meetings")


@router.post("/start")
def start_meeting(request: StartMeetingRequest):
    """
    Validates URL and triggers the background meeting service.
    Returns immediately with meeting_id and initial status.
    """
    url = request.meet_url.strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        raise HTTPException(status_code=400, detail="Invalid Google Meet URL format.")

    try:
        session_state = meeting_service.start_meeting(url)
        return {
            "meeting_id": session_state.meeting_id,
            "status": session_state.status.value,
            "message": session_state.message
        }
    except RuntimeError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start meeting: {str(e)}")


@router.get("", response_model=List[MeetingSummary])
def list_meetings():
    """Lists all past and active meetings."""
    return meeting_service.list_all_meetings()


@router.get("/active")
def get_active_meeting():
    """Returns the currently active meeting session if any."""
    active = meeting_service.get_active_meeting()
    if not active or not active.is_running:
        return {"active": False}
    return {"active": True, "meeting": active.to_dict()}


@router.get("/{meeting_id}/status")
def get_meeting_status(meeting_id: str):
    """Returns the status and metadata for a specific meeting."""
    active = meeting_service.get_active_meeting()
    if active and active.meeting_id == meeting_id:
        return active.to_dict()

    meeting_dir = BASE_MEETINGS_DIR / meeting_id
    if not meeting_dir.exists() or not meeting_dir.is_dir():
        raise HTTPException(status_code=404, detail="Meeting not found.")

    participants_file = meeting_dir / "participants.json"
    participants = []
    if participants_file.exists():
        try:
            data = json.loads(participants_file.read_text(encoding="utf-8"))
            participants = data.get("participants", [])
        except Exception:
            pass

    has_transcript = (meeting_dir / "transcripts" / "transcript.txt").exists()
    has_analysis = (meeting_dir / "analysis" / "analysis.txt").exists()
    has_report = (meeting_dir / "reports" / "meeting_report.pdf").exists()

    status = "completed" if (has_report or has_transcript) else "ended"

    return {
        "meeting_id": meeting_id,
        "status": status,
        "message": "Meeting archived",
        "participants": participants,
        "has_transcript": has_transcript,
        "has_analysis": has_analysis,
        "has_report": has_report,
    }


@router.post("/{meeting_id}/stop")
def stop_meeting(meeting_id: str):
    """Requests stopping the ongoing meeting call and triggers final processing."""
    stopped = meeting_service.stop_meeting(meeting_id)
    if not stopped:
        raise HTTPException(status_code=400, detail="Cannot stop meeting: meeting is not active or already stopping.")
    return {"status": "stopping", "message": "Stop signal sent to meeting service."}


@router.get("/{meeting_id}/participants")
def get_participants(meeting_id: str):
    """Returns the list of participants."""
    active = meeting_service.get_active_meeting()
    if active and active.meeting_id == meeting_id:
        return {"participants": active.participants}

    participants_file = BASE_MEETINGS_DIR / meeting_id / "participants.json"
    if not participants_file.exists():
        return {"participants": []}

    try:
        data = json.loads(participants_file.read_text(encoding="utf-8"))
        return {"participants": data.get("participants", [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading participants: {e}")


@router.get("/{meeting_id}/transcript")
def get_transcript(meeting_id: str):
    """Returns the full text transcript."""
    transcript_file = BASE_MEETINGS_DIR / meeting_id / "transcripts" / "transcript.txt"
    if not transcript_file.exists():
        # Fallback to direct directory
        alt_file = BASE_MEETINGS_DIR / meeting_id / "transcript.txt"
        if alt_file.exists():
            transcript_file = alt_file
        else:
            raise HTTPException(status_code=404, detail="Transcript not ready or not found.")

    return PlainTextResponse(transcript_file.read_text(encoding="utf-8"))


@router.get("/{meeting_id}/analysis")
def get_analysis(meeting_id: str):
    """Returns the AI analysis text."""
    analysis_file = BASE_MEETINGS_DIR / meeting_id / "analysis" / "analysis.txt"
    if not analysis_file.exists():
        alt_file = BASE_MEETINGS_DIR / meeting_id / "analysis.txt"
        if alt_file.exists():
            analysis_file = alt_file
        else:
            raise HTTPException(status_code=404, detail="Analysis not ready or not found.")

    return PlainTextResponse(analysis_file.read_text(encoding="utf-8"))


@router.get("/{meeting_id}/report")
def get_report(meeting_id: str):
    """Serves the generated PDF report."""
    report_file = BASE_MEETINGS_DIR / meeting_id / "reports" / "meeting_report.pdf"
    if not report_file.exists():
        alt_file = BASE_MEETINGS_DIR / meeting_id / "meeting_report.pdf"
        if alt_file.exists():
            report_file = alt_file
        else:
            raise HTTPException(status_code=404, detail="PDF report not ready or not found.")

    return FileResponse(
        path=report_file,
        media_type="application/pdf",
        filename=f"Meet-AI-Report-{meeting_id}.pdf"
    )


@router.delete("/{meeting_id}")
def delete_meeting(meeting_id: str):
    """Deletes a meeting from disk and from active sessions."""
    import shutil

    # Prevent deleting an active running meeting
    active = meeting_service.get_active_meeting()
    if active and active.meeting_id == meeting_id and active.is_running:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete a meeting that is currently in progress."
        )

    meeting_dir = BASE_MEETINGS_DIR / meeting_id
    if not meeting_dir.exists() or not meeting_dir.is_dir():
        raise HTTPException(status_code=404, detail="Meeting folder not found.")

    try:
        shutil.rmtree(meeting_dir)
        return {"status": "success", "message": f"Meeting {meeting_id} deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete meeting: {e}")

