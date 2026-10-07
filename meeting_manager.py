from pathlib import Path
from datetime import datetime


# ============================================================
# CONFIGURATION
# ============================================================

MEETINGS_DIR = Path("meetings")


# ============================================================
# CREATE NEW MEETING
# ============================================================

def create_meeting():

    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    meeting_dir = MEETINGS_DIR / timestamp

    meeting_dir.mkdir(
        parents=True,
        exist_ok=False
    )

    print()
    print("================================")
    print("       NEW MEETING CREATED")
    print("================================")
    print()

    print(
        f"📁 Meeting folder: {meeting_dir}"
    )

    print()

    return meeting_dir


# ============================================================
# SAVE TRANSCRIPT
# ============================================================

def save_transcript(
    meeting_dir,
    transcript
):

    transcript_file = (
        meeting_dir / "transcript.txt"
    )

    transcript_file.write_text(
        transcript,
        encoding="utf-8"
    )

    print(
        f"📝 Transcript saved: "
        f"{transcript_file}"
    )

    return transcript_file


# ============================================================
# SAVE ANALYSIS
# ============================================================

def save_analysis(
    meeting_dir,
    analysis
):

    analysis_file = (
        meeting_dir / "analysis.txt"
    )

    analysis_file.write_text(
        analysis,
        encoding="utf-8"
    )

    print(
        f"🤖 Analysis saved: "
        f"{analysis_file}"
    )

    return analysis_file


# ============================================================
# GET REPORT PATH
# ============================================================

def get_report_path(
    meeting_dir
):

    return (
        meeting_dir / "meeting_report.pdf"
    )


# ============================================================
# LIST MEETINGS
# ============================================================

def list_meetings():

    if not MEETINGS_DIR.exists():
        return []

    meetings = []

    for folder in MEETINGS_DIR.iterdir():

        if folder.is_dir():
            meetings.append(folder)

    return sorted(
        meetings,
        reverse=True
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    meeting = create_meeting()

    print()
    print(
        "Meeting ready for transcript/audio/analysis."
    )