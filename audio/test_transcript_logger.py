from audio.transcript_logger import save_transcript


audio_file = (
    "audio/recordings/chunk_0001.wav"
)

transcript = (
    "This is a test meeting transcript."
)


save_transcript(
    audio_file,
    transcript
)