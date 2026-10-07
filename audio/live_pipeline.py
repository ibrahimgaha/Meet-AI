import time
import threading
from pathlib import Path

from audio.processor import process_audio_file


def process_new_chunks(
    recordings_directory="audio/recordings",
    check_interval=2
):

    recordings_directory = Path(
        recordings_directory
    )

    processed_files = set()

    print("🧠 Chunk processor started.")

    while True:

        audio_files = sorted(
            recordings_directory.glob("chunk_*.wav")
        )

        for audio_file in audio_files:

            if audio_file in processed_files:
                continue

            processed_files.add(
                audio_file
            )

            print()
            print(
                f"🆕 Processing {audio_file.name}"
            )

            process_audio_file(
                audio_file
            )

        time.sleep(
            check_interval
        )


def start_processing_thread():

    thread = threading.Thread(
        target=process_new_chunks,
        daemon=True
    )

    thread.start()

    print("🧠 Background transcription started.")

    return thread