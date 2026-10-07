import torch

from pyannote.audio import Pipeline


MODEL = "pyannote/speaker-diarization-community-1"

_pipeline = None


def get_pipeline():

    global _pipeline

    if _pipeline is None:

        device = (
            torch.device("cpu")
            if torch.cuda.is_available()
            else torch.device("cpu")
        )

        print(
            f"👥 Loading diarization model on: {device}"
        )

        _pipeline = Pipeline.from_pretrained(
            MODEL
        )

        _pipeline.to(device)

        print("✅ Diarization model loaded.")

    return _pipeline


def diarize_audio(audio_file):

    pipeline = get_pipeline()

    print(
        f"🎙️ Diarizing: {audio_file}"
    )

    output = pipeline(
        audio_file
    )

    return output


def get_speaker_segments(audio_file):

    diarization = diarize_audio(
        audio_file
    )

    segments = []

    for turn, speaker in (
        diarization.speaker_diarization
    ):

        segments.append({

            "start": turn.start,

            "end": turn.end,

            "speaker": speaker

        })

    return segments