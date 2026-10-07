from audio.processor import process_audio_file


audio_file = (
    "audio/recordings/chunk_0001.wav"
)


text = process_audio_file(
    audio_file
)

print()
print("================================")
print(" PROCESSING COMPLETE ✅")
print("================================")