from pathlib import Path


REPORT_DIRECTORY = Path("logs")


def save_report(session):

    REPORT_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True
    )

    report_file = (
        REPORT_DIRECTORY / "meeting_report.txt"
    )

    summary = session.get_summary()

    with open(
        report_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write("================================\n")
        file.write("       MEETING SESSION REPORT\n")
        file.write("================================\n\n")

        file.write(
            f"Started: "
            f"{summary['start_time'].strftime('%Y-%m-%d %H:%M:%S')}\n"
        )

        if summary["end_time"]:

            file.write(
                f"Ended: "
                f"{summary['end_time'].strftime('%Y-%m-%d %H:%M:%S')}\n"
            )

        if summary["duration"]:

            file.write(
                f"Duration: "
                f"{summary['duration']}\n"
            )

        file.write("\n")

        file.write("INITIAL PARTICIPANTS\n")
        file.write("--------------------\n")

        for participant in sorted(
            summary["initial_participants"]
        ):

            file.write(
                f"- {participant}\n"
            )

        file.write("\n")

        file.write("EVENTS\n")
        file.write("------\n")

        for event in summary["events"]:

            timestamp = event["time"].strftime(
                "%H:%M:%S"
            )

            file.write(
                f"[{timestamp}] "
                f"{event['participant']} "
                f"{event['event']}\n"
            )
            file.write("\n")

        file.write("PARTICIPANT DURATIONS\n")
        file.write("---------------------\n")

        for participant, seconds in sorted(
            summary["participant_durations"].items()
        ):

            minutes = int(seconds // 60)

            remaining_seconds = int(
                seconds % 60
            )

            file.write(
                f"- {participant}: "
                f"{minutes}m "
                f"{remaining_seconds}s\n"
            )    

    print()
    print("================================")
    print(" MEETING REPORT SAVED ✅")
    print("================================")
    print()
    print(report_file)