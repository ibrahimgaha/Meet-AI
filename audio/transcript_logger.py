from pathlib import Path


def save_transcript(
    audio_file,
    transcript,
    output_directory="audio/transcripts"
):

    audio_file = Path(audio_file)

    output_directory = Path(
        output_directory
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    transcript_file = (
        output_directory
        / f"{audio_file.stem}.txt"
    )

    with open(
        transcript_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            transcript.strip()
        )

    print(
        f"💾 Transcript saved: "
        f"{transcript_file}"
    )

    return transcript_file