import whisper
import torch


MODEL_SIZE = "base"

_model = None

DEVICE = (
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)


def get_model():

    global _model

    if _model is None:

        print(
            f"🧠 Loading Whisper model on: {DEVICE}"
        )

        _model = whisper.load_model(
            MODEL_SIZE,
            device=DEVICE
        )

        print("✅ Whisper model loaded.")

    return _model


def transcribe_audio(audio_file):

    model = get_model()

    print(
        f"🎙️ Transcribing: {audio_file}"
    )

    result = model.transcribe(
        audio_file,
        language=None,
        fp16=(DEVICE == "cuda")
    )

    segments = []

    for segment in result["segments"]:

        segments.append({
            "start": segment["start"],
            "end": segment["end"],
            "text": segment["text"].strip()
        })

    return segments