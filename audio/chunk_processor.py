import time
from pathlib import Path

from audio.processor import process_audio_file


def process_chunks(
    recordings_directory="audio/recordings",
    check_interval=2
):

    recordings_directory = Path(
        recordings_directory
    )

    processed_files = set()

    print()
    print("================================")
    print(" AUTOMATIC CHUNK PROCESSOR")
    print("================================")
    print()
    print("Waiting for new audio chunks...")
    print("Press CTRL+C to stop.")
    print()

    try:

        while True:

            audio_files = sorted(
                recordings_directory.glob("chunk_*.wav")
            )

            for audio_file in audio_files:

                if audio_file in processed_files:
                    continue

                print()
                print(f"🆕 New chunk detected: {audio_file.name}")

                process_audio_file(
                    audio_file
                )

                processed_files.add(
                    audio_file
                )

            time.sleep(
                check_interval
            )

    except KeyboardInterrupt:

        print()
        print("🛑 Chunk processor stopped.")