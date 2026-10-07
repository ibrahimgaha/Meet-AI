import wave
from pathlib import Path


def merge_audio_chunks(
    recordings_directory="audio/recordings",
    output_file="audio/recordings/full_meeting.wav"
):

    recordings_directory = Path(
        recordings_directory
    )

    output_file = Path(
        output_file
    )

    audio_files = sorted(
        recordings_directory.glob("chunk_*.wav")
    )

    if not audio_files:

        print("❌ No audio chunks found.")

        return None

    print()
    print("================================")
    print("      MERGING AUDIO CHUNKS")
    print("================================")
    print()

    first_file = audio_files[0]

    with wave.open(
        str(first_file),
        "rb"
    ) as first_wav:

        params = first_wav.getparams()

        with wave.open(
            str(output_file),
            "wb"
        ) as output_wav:

            output_wav.setparams(params)

            for audio_file in audio_files:

                print(
                    f"➕ Adding: "
                    f"{audio_file.name}"
                )

                with wave.open(
                    str(audio_file),
                    "rb"
                ) as wav:

                    output_wav.writeframes(
                        wav.readframes(
                            wav.getnframes()
                        )
                    )

    print()
    print(
        f"✅ Full meeting audio created:"
    )
    print(output_file)

    return output_file