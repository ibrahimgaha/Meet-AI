from pathlib import Path

from audio.transcriber import transcribe_audio
from audio.transcript_logger import save_transcript


def process_meeting(
    recordings_directory="audio/recordings",
    output_file="audio/transcripts/full_meeting.txt"
):

    recordings_directory = Path(
        recordings_directory
    )

    output_file = Path(
        output_file
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    audio_files = sorted(
        recordings_directory.glob("chunk_*.wav")
    )

    if not audio_files:

        print("❌ No audio chunks found.")

        return

    print()
    print("================================")
    print("      MEETING PROCESSOR")
    print("================================")
    print()

    print(
        f"🎧 Found {len(audio_files)} audio chunks."
    )

    transcripts = []

    for audio_file in audio_files:

        print()
        print(
            f"🎙️ Transcribing: "
            f"{audio_file.name}"
        )

        text = transcribe_audio(
            str(audio_file)
        )

        transcripts.append(
            text.strip()
        )

    full_transcript = "\n\n".join(
        transcripts
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            full_transcript
        )

    print()
    print("================================")
    print("   MEETING TRANSCRIPTION DONE ✅")
    print("================================")
    print()
    print(
        f"💾 Saved: {output_file}"
    )