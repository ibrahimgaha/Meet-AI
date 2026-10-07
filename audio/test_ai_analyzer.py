from pathlib import Path

from ai_analyzer import analyze_transcript


# ============================================================
# ANALYZE A MEETING
# ============================================================

def analyze_meeting(meeting_dir):

    meeting_dir = Path(meeting_dir)

    transcript_file = (
        meeting_dir / "transcript.txt"
    )

    analysis_file = (
        meeting_dir / "analysis.txt"
    )

    print()
    print("================================")
    print("       AI MEETING ANALYZER")
    print("================================")
    print()

    print(
        f"📁 Meeting: {meeting_dir}"
    )

    # --------------------------------------------------------
    # CHECK TRANSCRIPT
    # --------------------------------------------------------

    if not transcript_file.exists():

        print(
            f"❌ Transcript not found:"
        )

        print(
            f"   {transcript_file}"
        )

        return None

    # --------------------------------------------------------
    # READ TRANSCRIPT
    # --------------------------------------------------------

    print(
        f"📄 Reading transcript:"
    )

    print(
        f"   {transcript_file}"
    )

    transcript = transcript_file.read_text(
        encoding="utf-8"
    )

    if not transcript.strip():

        print(
            "❌ Transcript is empty."
        )

        return None

    print(
        f"📝 Transcript loaded "
        f"({len(transcript)} characters)"
    )

    # --------------------------------------------------------
    # AI ANALYSIS
    # --------------------------------------------------------

    try:

        result = analyze_transcript(
            transcript
        )

    except Exception as e:

        print()
        print(
            "❌ AI analysis failed:"
        )

        print(e)

        return None

    # --------------------------------------------------------
    # SAVE ANALYSIS
    # --------------------------------------------------------

    analysis_file.write_text(
        result,
        encoding="utf-8"
    )

    print()
    print(
        "================================"
    )

    print(
        "          AI RESULT"
    )

    print(
        "================================"
    )

    print()

    print(result)

    print()

    print(
        f"💾 Analysis saved:"
    )

    print(
        f"   {analysis_file}"
    )

    return analysis_file


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    # Change this temporarily for testing.
    meeting_dir = Path(
        "meetings/2026-10-07_11-57-20"
    )

    analyze_meeting(
        meeting_dir
    )