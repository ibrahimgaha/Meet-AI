from audio.diarizer import (
    get_speaker_segments
)


audio_file = (
    "audio/recordings/full_meeting.wav"
)


segments = get_speaker_segments(
    audio_file
)


print()
print("================================")
print("   FULL MEETING DIARIZATION")
print("================================")
print()

for segment in segments:

    print(
        f"[{segment['start']:.2f}s → "
        f"{segment['end']:.2f}s] "
        f"{segment['speaker']}"
    )