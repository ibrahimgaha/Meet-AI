from audio.speaker_transcript import (
    process_audio_with_speakers
)


audio_file = (
    "audio/recordings/chunk_0001.wav"
)


segments = process_audio_with_speakers(
    audio_file
)

print()
print("================================")
print(" FINAL SPEAKER TRANSCRIPT")
print("================================")
print()

for segment in segments:

    print(
        f"[{segment['start']:.2f}s → "
        f"{segment['end']:.2f}s] "
        f"{segment['speaker']}: "
        f"{segment['text']}"
    )