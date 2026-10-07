from pathlib import Path

from audio.diarizer import diarize_audio
from audio.transcriber import transcribe_audio


def find_speaker(
    start,
    end,
    speaker_segments
):

    best_speaker = "UNKNOWN"
    best_overlap = 0

    for speaker_segment in speaker_segments:

        overlap_start = max(
            start,
            speaker_segment["start"]
        )

        overlap_end = min(
            end,
            speaker_segment["end"]
        )

        overlap = max(
            0,
            overlap_end - overlap_start
        )

        if overlap > best_overlap:

            best_overlap = overlap

            best_speaker = (
                speaker_segment["speaker"]
            )

    return best_speaker


def process_audio_with_speakers(
    audio_file
):

    print()
    print("================================")
    print(" SPEAKER + TRANSCRIPT PROCESSOR")
    print("================================")
    print()

    print("🎙️ Getting Whisper transcript...")

    whisper_segments = transcribe_audio(
        audio_file
    )

    print()
    print("👥 Getting speaker diarization...")

    diarization = diarize_audio(
        audio_file
    )

    speaker_segments = []

    for turn, speaker in (
        diarization.speaker_diarization
    ):

        speaker_segments.append({
            "start": turn.start,
            "end": turn.end,
            "speaker": speaker
        })

    final_segments = []

    for segment in whisper_segments:

        speaker = find_speaker(
            segment["start"],
            segment["end"],
            speaker_segments
        )

        final_segments.append({
            "start": segment["start"],
            "end": segment["end"],
            "speaker": speaker,
            "text": segment["text"]
        })

    return final_segments