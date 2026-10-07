from audio.full_meeting import (
    process_full_meeting
)


segments = process_full_meeting(
    recordings_directory="audio/recordings"
)


print()
print("================================")
print("     FINAL MEETING TRANSCRIPT")
print("================================")
print()

for segment in segments:

    print(
        f"[{segment['start']:.2f}s → "
        f"{segment['end']:.2f}s] "
        f"{segment['speaker']}: "
        f"{segment['text']}"
    )