from audio.transcriber import transcribe_audio


audio_file = (
    "audio/recordings/chunk_0001.wav"
)


segments = transcribe_audio(
    audio_file
)

print()
print("================================")
print(" TIMESTAMPED TRANSCRIPT")
print("================================")
print()

for segment in segments:

    print(
        f"[{segment['start']:.2f}s → "
        f"{segment['end']:.2f}s] "
        f"{segment['text']}"
    )