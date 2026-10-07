from pathlib import Path

from audio.transcriber import transcribe_audio
from audio.transcript_logger import save_transcript


def process_audio_file(audio_file):

    audio_file = Path(audio_file)

    print()
    print("================================")
    print(" PROCESSING AUDIO")
    print("================================")
    print()
    print(f"🎧 File: {audio_file}")

    text = transcribe_audio(
        str(audio_file)
    )

    print()
    print("📝 Transcript:")
    print(text)

    save_transcript(
        audio_file,
        text
    )

    return text