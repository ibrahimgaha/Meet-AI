import wave
import threading
from pathlib import Path

import pyaudiowpatch as pyaudio


DEVICE = 21
SAMPLE_RATE = 48000
CHANNELS = 2
CHUNK = 1024


def record_continuously(
    output_directory="audio/recordings",
    chunk_duration=10,
    stop_event=None
):

    if stop_event is None:
        stop_event = threading.Event()

    output_directory = Path(output_directory)

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    p = pyaudio.PyAudio()

    device = p.get_device_info_by_index(DEVICE)

    print(f"🎧 Audio device: {device['name']}")
    print()
    print("🎙️ Continuous recording started")
    print()

    stream = p.open(
        format=pyaudio.paInt16,
        channels=CHANNELS,
        rate=SAMPLE_RATE,
        input=True,
        input_device_index=DEVICE,
        frames_per_buffer=CHUNK
    )

    sample_width = p.get_sample_size(
        pyaudio.paInt16
    )

    chunk_number = 1

    try:

        while not stop_event.is_set():

            frames = []

            print(
                f"🔴 Recording chunk {chunk_number}..."
            )

            chunks_per_file = int(
                SAMPLE_RATE / CHUNK * chunk_duration
            )

            for _ in range(chunks_per_file):

                if stop_event.is_set():
                    break

                data = stream.read(
                    CHUNK,
                    exception_on_overflow=False
                )

                frames.append(data)

            # Save whatever was recorded.
            # This can be a partial final chunk.
            if frames:

                output_file = (
                    output_directory
                    / f"chunk_{chunk_number:04d}.wav"
                )

                with wave.open(
                    str(output_file),
                    "wb"
                ) as wf:

                    wf.setnchannels(CHANNELS)
                    wf.setsampwidth(sample_width)
                    wf.setframerate(SAMPLE_RATE)
                    wf.writeframes(
                        b"".join(frames)
                    )

                print(
                    f"✅ Saved: {output_file}"
                )

                chunk_number += 1

    except KeyboardInterrupt:

        print()
        print("🛑 Recording stopped manually.")

    finally:

        print()
        print("🛑 Stopping recorder...")

        stream.stop_stream()
        stream.close()

        p.terminate()

        print("🎧 Audio device released.")