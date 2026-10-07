from datetime import datetime
from pathlib import Path


LOG_FILE = Path("logs/meeting.log")


def log_event(participant, event):

    LOG_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    timestamp = datetime.now().strftime("%H:%M:%S")

    message = (
        f"[{timestamp}] "
        f"{participant} {event}"
    )

    print(message)

    with open(
        LOG_FILE,
        "a",
        encoding="utf-8"
    ) as file:

        file.write(message + "\n")