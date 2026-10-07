import wave
import pyaudiowpatch as pyaudio


DEVICE = 21
SAMPLE_RATE = 48000
CHANNELS = 2
CHUNK = 1024


def record_system_audio(
    duration,
    output_file
):

    p = pyaudio.PyAudio()

    device = p.get_device_info_by_index(DEVICE)

    print("🎧 Audio device:")
    print(device["name"])

    stream = p.open(
        format=pyaudio.paInt16,
        channels=CHANNELS,
        rate=SAMPLE_RATE,
        input=True,
        input_device_index=DEVICE,
        frames_per_buffer=CHUNK
    )

    print()
    print("🎙️ Recording system audio...")
    print(f"Duration: {duration} seconds")

    frames = []

    for _ in range(
        int(SAMPLE_RATE / CHUNK * duration)
    ):

        data = stream.read(
            CHUNK,
            exception_on_overflow=False
        )

        frames.append(data)

    stream.stop_stream()
    stream.close()

    sample_width = p.get_sample_size(
        pyaudio.paInt16
    )

    p.terminate()

    with wave.open(
        output_file,
        "wb"
    ) as wf:

        wf.setnchannels(CHANNELS)
        wf.setsampwidth(sample_width)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(
            b"".join(frames)
        )

    print()
    print("✅ Audio saved:")
    print(output_file)