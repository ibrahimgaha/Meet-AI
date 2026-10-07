from pathlib import Path
import json
import wave

from audio.diarizer import get_speaker_segments
from audio.merge_audio import merge_audio_chunks
from audio.transcriber import transcribe_audio

from audio.ai_analyzer import analyze_transcript
from audio.pdf_report import create_pdf_report


# ============================================================
# AUDIO DURATION
# ============================================================

def get_audio_duration(audio_file):

    with wave.open(str(audio_file), "rb") as wav:

        frames = wav.getnframes()
        rate = wav.getframerate()

        return frames / float(rate)


# ============================================================
# GET AUDIO CHUNKS
# ============================================================

def get_audio_files(recordings_directory):

    directory = Path(recordings_directory)

    return sorted(
        directory.glob("chunk_*.wav")
    )


# ============================================================
# LOAD PARTICIPANTS
# ============================================================

def load_participants(meeting_directory):

    participants_file = (
        Path(meeting_directory)
        / "participants.json"
    )

    if not participants_file.exists():

        print()
        print("⚠️ participants.json not found.")
        print(
            f"   Expected: {participants_file}"
        )
        print()

        return []

    try:

        data = json.loads(
            participants_file.read_text(
                encoding="utf-8"
            )
        )

        participants = data.get(
            "participants",
            []
        )

        participants = [
            participant
            for participant in participants
            if participant
        ]

        return sorted(
            set(participants)
        )

    except Exception as e:

        print()
        print(
            "⚠️ Failed to read participants.json:"
        )
        print(e)
        print()

        return []


# ============================================================
# GET SPEAKER IDS
# ============================================================

def get_speaker_ids(speaker_segments):

    speaker_ids = set()

    for segment in speaker_segments:

        speaker = segment.get(
            "speaker"
        )

        if speaker:

            speaker_ids.add(
                speaker
            )

    return sorted(
        speaker_ids
    )


# ============================================================
# MANUAL SPEAKER MAPPING
# ============================================================

def build_speaker_mapping(
    speaker_segments,
    participants,
    auto_map=False
):

    speaker_ids = get_speaker_ids(
        speaker_segments
    )

    if not speaker_ids:

        print()
        print(
            "⚠️ No speakers detected."
        )
        print()

        return {}

    if auto_map:
        mapping = {}
        for index, speaker in enumerate(speaker_ids):
            if index < len(participants):
                mapping[speaker] = participants[index]
            else:
                mapping[speaker] = speaker
        print()
        print("================================")
        print("  SPEAKER MAPPING (AUTOMATIC)")
        print("================================")
        for speaker in speaker_ids:
            print(f"   {speaker} → {mapping[speaker]}")
        print()
        return mapping

    print()
    print("================================")
    print("       SPEAKER MAPPING")
    print("================================")
    print()

    print(
        "Diarization detected:"
    )

    for speaker in speaker_ids:

        print(
            f"   🎤 {speaker}"
        )

    print()

    if not participants:

        print(
            "⚠️ No participant names available."
        )

        print(
            "Speaker names will remain as "
            "SPEAKER_XX."
        )

        print()

        return {
            speaker: speaker
            for speaker in speaker_ids
        }

    print(
        "Participants detected in Google Meet:"
    )

    print()

    for index, participant in enumerate(
        participants,
        start=1
    ):

        print(
            f"   {index}. {participant}"
        )

    print()

    print(
        "Map each detected speaker to a "
        "participant."
    )

    print(
        "Enter the participant number."
    )

    print(
        "Press ENTER to keep SPEAKER_XX."
    )

    print()

    mapping = {}

    used_participants = set()

    for speaker in speaker_ids:

        while True:

            choice = input(
                f"{speaker} = "
            ).strip()

            # --------------------------------------------
            # Keep original speaker name
            # --------------------------------------------

            if not choice:

                mapping[speaker] = speaker

                break

            # --------------------------------------------
            # Validate number
            # --------------------------------------------

            try:

                participant_index = int(
                    choice
                )

            except ValueError:

                print(
                    "❌ Please enter a number "
                    "or press ENTER."
                )

                continue

            # --------------------------------------------
            # Validate range
            # --------------------------------------------

            if not (
                1
                <= participant_index
                <= len(participants)
            ):

                print(
                    "❌ Invalid participant number."
                )

                continue

            participant = participants[
                participant_index - 1
            ]

            # --------------------------------------------
            # Avoid assigning same person twice
            # --------------------------------------------

            if participant in used_participants:

                print(
                    f"⚠️ {participant} is already "
                    "assigned to another speaker."
                )

                print(
                    "If this is intentional, "
                    "you can still choose it again "
                    "after confirming."
                )

                confirm = input(
                    "Use this participant anyway? "
                    "(y/n): "
                ).strip().lower()

                if confirm != "y":

                    continue

            mapping[speaker] = participant

            used_participants.add(
                participant
            )

            break

    print()
    print("================================")
    print("       SPEAKER MAPPING")
    print("================================")
    print()

    for speaker in speaker_ids:

        print(
            f"   {speaker} → "
            f"{mapping[speaker]}"
        )

    print()

    return mapping


# ============================================================
# APPLY SPEAKER NAMES
# ============================================================

def apply_speaker_mapping(
    segments,
    speaker_mapping
):

    named_segments = []

    for segment in segments:

        speaker = segment.get(
            "speaker",
            "UNKNOWN"
        )

        named_speaker = (
            speaker_mapping.get(
                speaker,
                speaker
            )
        )

        named_segments.append({

            "start": segment["start"],

            "end": segment["end"],

            "speaker": named_speaker,

            "text": segment["text"]
        })

    return named_segments


# ============================================================
# BUILD GLOBAL WHISPER SEGMENTS
# ============================================================

def build_global_whisper_segments(
    audio_files
):

    all_segments = []

    global_offset = 0

    for audio_file in audio_files:

        print()
        print(
            f"🎙️ Whisper: "
            f"{audio_file.name}"
        )

        segments = transcribe_audio(
            str(audio_file)
        )

        for segment in segments:

            all_segments.append({

                "start":
                    segment["start"]
                    + global_offset,

                "end":
                    segment["end"]
                    + global_offset,

                "text":
                    segment["text"]
            })

        duration = get_audio_duration(
            audio_file
        )

        global_offset += duration

    return (
        all_segments,
        global_offset
    )


# ============================================================
# MATCH SPEAKERS WITH TRANSCRIPT
# ============================================================

def match_speakers(
    whisper_segments,
    speaker_segments
):

    final_segments = []

    for transcript in whisper_segments:

        best_speaker = "UNKNOWN"

        best_overlap = 0

        for speaker in speaker_segments:

            overlap_start = max(
                transcript["start"],
                speaker["start"]
            )

            overlap_end = min(
                transcript["end"],
                speaker["end"]
            )

            overlap = max(
                0,
                overlap_end
                - overlap_start
            )

            if overlap > best_overlap:

                best_overlap = overlap

                best_speaker = (
                    speaker["speaker"]
                )

        final_segments.append({

            "start":
                transcript["start"],

            "end":
                transcript["end"],

            "speaker":
                best_speaker,

            "text":
                transcript["text"]
        })

    return final_segments


# ============================================================
# BUILD TRANSCRIPT TEXT
# ============================================================

def build_transcript(
    final_segments
):

    transcript_lines = []

    for segment in final_segments:

        start = segment["start"]

        end = segment["end"]

        speaker = segment["speaker"]

        text = segment["text"].strip()

        if not text:

            continue

        transcript_lines.append(
            f"[{start:.2f}s → {end:.2f}s] "
            f"{speaker}: {text}"
        )

    return "\n".join(
        transcript_lines
    )


# ============================================================
# FULL MEETING PROCESSOR
# ============================================================

def process_full_meeting(
    meeting_directory,
    auto_map=False
):

    meeting_directory = Path(
        meeting_directory
    )

    recordings_directory = (
        meeting_directory
        / "recordings"
    )

    transcripts_directory = (
        meeting_directory
        / "transcripts"
    )

    analysis_directory = (
        meeting_directory
        / "analysis"
    )

    reports_directory = (
        meeting_directory
        / "reports"
    )

    # --------------------------------------------------------
    # CREATE DIRECTORIES
    # --------------------------------------------------------

    transcripts_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    analysis_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    reports_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    print()
    print("================================")
    print("     FULL MEETING PROCESSOR")
    print("================================")
    print()

    print(
        f"📁 Meeting:"
    )

    print(
        f"   {meeting_directory}"
    )

    print()

    # --------------------------------------------------------
    # LOAD PARTICIPANTS
    # --------------------------------------------------------

    participants = load_participants(
        meeting_directory
    )

    print()

    if participants:

        print(
            "👥 Participants:"
        )

        for participant in participants:

            print(
                f"   - {participant}"
            )

    else:

        print(
            "⚠️ No participants found."
        )

    print()

    # --------------------------------------------------------
    # GET AUDIO FILES
    # --------------------------------------------------------

    audio_files = get_audio_files(
        recordings_directory
    )

    if not audio_files:

        print(
            "❌ No audio chunks found."
        )

        return []

    print(
        f"🎧 Found "
        f"{len(audio_files)} chunks."
    )

    # --------------------------------------------------------
    # MERGE AUDIO
    # --------------------------------------------------------

    print()
    print("================================")
    print("       MERGING AUDIO")
    print("================================")
    print()

    full_audio = (
        recordings_directory
        / "full_meeting.wav"
    )

    full_audio = merge_audio_chunks(

        recordings_directory=
            str(recordings_directory),

        output_file=
            str(full_audio)
    )

    # --------------------------------------------------------
    # WHISPER TRANSCRIPTION
    # --------------------------------------------------------

    print()
    print("================================")
    print("       WHISPER TRANSCRIPTION")
    print("================================")
    print()

    (
        whisper_segments,
        duration
    ) = build_global_whisper_segments(
        audio_files
    )

    print()
    print(
        f"⏱️ Meeting duration: "
        f"{duration:.2f}s"
    )

    # --------------------------------------------------------
    # SPEAKER DIARIZATION
    # --------------------------------------------------------

    print()
    print("================================")
    print("       SPEAKER DIARIZATION")
    print("================================")
    print()

    speaker_segments = (
        get_speaker_segments(
            str(full_audio)
        )
    )

    print()
    print(
        f"👥 Detected "
        f"{len(speaker_segments)} "
        f"speaker segments."
    )

    # --------------------------------------------------------
    # MATCH WHISPER + SPEAKERS
    # --------------------------------------------------------

    print()
    print(
        "🔗 Matching transcript "
        "with speakers..."
    )

    final_segments = match_speakers(

        whisper_segments,

        speaker_segments
    )

    # --------------------------------------------------------
    # BUILD SPEAKER MAPPING
    # --------------------------------------------------------

    speaker_mapping = (
        build_speaker_mapping(

            speaker_segments,

            participants,

            auto_map=auto_map
        )
    )

    # --------------------------------------------------------
    # REPLACE SPEAKER IDs
    # --------------------------------------------------------

    final_segments = (
        apply_speaker_mapping(

            final_segments,

            speaker_mapping
        )
    )

    # --------------------------------------------------------
    # BUILD FINAL TRANSCRIPT
    # --------------------------------------------------------

    transcript = build_transcript(
        final_segments
    )

    # --------------------------------------------------------
    # SAVE TRANSCRIPT
    # --------------------------------------------------------

    transcript_file = (
        transcripts_directory
        / "transcript.txt"
    )

    transcript_file.write_text(
        transcript,
        encoding="utf-8"
    )

    print()
    print("================================")
    print("    TRANSCRIPT SAVED ✅")
    print("================================")
    print()

    print(
        f"📝 {transcript_file}"
    )

    # --------------------------------------------------------
    # AI ANALYSIS
    # --------------------------------------------------------

    print()
    print("================================")
    print("       AI ANALYSIS")
    print("================================")
    print()

    try:

        analysis = analyze_transcript(
            transcript
        )

        analysis_file = (
            analysis_directory
            / "analysis.txt"
        )

        analysis_file.write_text(
            analysis,
            encoding="utf-8"
        )

        print()
        print(
            "🤖 AI analysis saved:"
        )

        print(
            f"   {analysis_file}"
        )

    except Exception as e:

        print()
        print(
            "❌ AI analysis failed:"
        )

        print(e)

        print()

        return final_segments

    # --------------------------------------------------------
    # PDF REPORT
    # --------------------------------------------------------

    print()
    print("================================")
    print("       PDF REPORT")
    print("================================")
    print()

    try:

        report_file = create_pdf_report(
            meeting_directory
        )

        print()
        print(
            "📄 PDF report generated:"
        )

        print(
            f"   {report_file}"
        )

    except Exception as e:

        print()
        print(
            "❌ PDF generation failed:"
        )

        print(e)

    # --------------------------------------------------------
    # COMPLETE
    # --------------------------------------------------------

    print()
    print("================================")
    print("   MEETING PROCESSING COMPLETE")
    print("================================")
    print()

    print(
        f"📁 Meeting folder:"
    )

    print(
        f"   {meeting_directory}"
    )

    print()

    return final_segments