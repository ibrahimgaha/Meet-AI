from pathlib import Path
from typing import Callable, Optional

from audio.ai_analyzer import analyze_transcript
from audio.diarizer import get_speaker_segments
from audio.full_meeting import (
    apply_speaker_mapping,
    build_global_whisper_segments,
    build_speaker_mapping,
    build_transcript,
    get_audio_files,
    load_participants,
    match_speakers,
)
from audio.merge_audio import merge_audio_chunks
from audio.pdf_report import create_pdf_report
from backend.models.meeting import MeetingStatus


def process_meeting_with_progress(
    meeting_directory: Path,
    status_callback: Optional[Callable[[MeetingStatus, str], None]] = None,
    auto_map: bool = True
):
    """
    Executes the full post-meeting processing pipeline step-by-step
    and calls status_callback(status, message) before each stage.
    """
    meeting_directory = Path(meeting_directory)
    recordings_dir = meeting_directory / "recordings"
    transcripts_dir = meeting_directory / "transcripts"
    analysis_dir = meeting_directory / "analysis"
    reports_dir = meeting_directory / "reports"

    transcripts_dir.mkdir(parents=True, exist_ok=True)
    analysis_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    def notify(status: MeetingStatus, msg: str):
        if status_callback:
            status_callback(status, msg)

    # 1. Load participants
    participants = load_participants(meeting_directory)

    # 2. Check audio files
    audio_files = get_audio_files(recordings_dir)
    if not audio_files:
        raise RuntimeError("No audio chunks found in recordings directory.")

    # 3. Merge audio chunks
    notify(MeetingStatus.merging_audio, f"Merging {len(audio_files)} audio chunks...")
    full_audio = recordings_dir / "full_meeting.wav"
    merge_audio_chunks(
        recordings_directory=str(recordings_dir),
        output_file=str(full_audio)
    )

    # 4. Whisper transcription
    notify(MeetingStatus.transcribing, "Running Whisper speech-to-text transcription...")
    whisper_segments, duration = build_global_whisper_segments(audio_files)

    # 5. Diarization
    notify(MeetingStatus.diarizing, "Running speaker diarization (pyannote)...")
    speaker_segments = get_speaker_segments(str(full_audio))

    # 6. Speaker matching & mapping
    notify(MeetingStatus.mapping_speakers, "Matching transcribed text with speakers...")
    final_segments = match_speakers(whisper_segments, speaker_segments)
    speaker_mapping = build_speaker_mapping(
        speaker_segments,
        participants,
        auto_map=auto_map
    )
    final_segments = apply_speaker_mapping(final_segments, speaker_mapping)

    transcript = build_transcript(final_segments)
    transcript_file = transcripts_dir / "transcript.txt"
    transcript_file.write_text(transcript, encoding="utf-8")

    # 7. AI Analysis
    notify(MeetingStatus.analyzing, "Generating AI meeting recap via OpenRouter...")
    try:
        analysis = analyze_transcript(transcript)
        analysis_file = analysis_dir / "analysis.txt"
        analysis_file.write_text(analysis, encoding="utf-8")
    except Exception as e:
        print(f"⚠️ AI analysis failed: {e}")

    # 8. PDF Report
    notify(MeetingStatus.generating_report, "Compiling PDF executive summary report...")
    try:
        create_pdf_report(meeting_directory)
    except Exception as e:
        print(f"⚠️ PDF generation failed: {e}")

    notify(MeetingStatus.completed, "Meeting processing successfully completed.")
    return final_segments
