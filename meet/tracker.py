import time
import json
from pathlib import Path
from threading import Event

from playwright.sync_api import Page

from config import POLL_INTERVAL

from meet.participants import get_participants
from meet.logger import log_event
from meet.session import MeetingSession
from meet.report import save_report
from meet.state import MeetingState
from meet.browser import meeting_has_ended


def track_participants(
    page: Page,
    stop_event=None,
    meeting_directory=None,
    on_change=None
):
    """
    Track participants entering and leaving the Google Meet.

    Also keeps a complete list of all participants who appeared
    during the meeting and saves it as participants.json.

    Parameters
    ----------
    page : Page
        Playwright Google Meet page.

    stop_event : Event, optional
        Event used to stop the tracker.

    meeting_directory : str or Path, optional
        Current meeting folder. If provided, participants.json
        will be saved there.
    """

    if stop_event is None:
        stop_event = Event()

    # ---------------------------------------------------------
    # INITIAL PARTICIPANTS
    # ---------------------------------------------------------

    initial_participants = get_participants(page)

    print()
    print("================================")
    print("   PARTICIPANT TRACKER STARTED")
    print("================================")
    print()

    for participant in sorted(initial_participants):
        print(
            f"🟢 Initial participant: "
            f"{participant}"
        )

    # ---------------------------------------------------------
    # SESSION / STATE
    # ---------------------------------------------------------

    session = MeetingSession(
        initial_participants
    )

    state = MeetingState(
        initial_participants
    )

    previous_participants = (
        initial_participants.copy()
    )

    # Complete list of everyone who appeared
    # during the meeting.
    all_participants = (
        initial_participants.copy()
    )

    if on_change:
        try:
            on_change(sorted(all_participants))
        except Exception:
            pass

    # ---------------------------------------------------------
    # TRACKING LOOP
    # ---------------------------------------------------------

    try:

        while not stop_event.is_set():

            # -------------------------------------------------
            # CHECK IF MEETING ENDED
            # -------------------------------------------------

            if meeting_has_ended(page):

                print()
                print("================================")
                print("   MEETING ENDED ✅")
                print("================================")
                print()

                stop_event.set()

                break

            # -------------------------------------------------
            # GET CURRENT PARTICIPANTS
            # -------------------------------------------------

            current_participants = (
                get_participants(page)
            )

            # -------------------------------------------------
            # DETECT PEOPLE WHO JOINED
            # -------------------------------------------------

            joined = (
                current_participants
                - previous_participants
            )

            for participant in sorted(joined):

                # Keep the participant permanently
                # in the meeting participant list.
                all_participants.add(
                    participant
                )

                print(
                    f"🟢 {participant} ENTERED"
                )

                log_event(
                    participant,
                    "ENTERED"
                )

                session.add_event(
                    participant,
                    "ENTERED"
                )

                state.participant_joined(
                    participant
                )

            # -------------------------------------------------
            # DETECT PEOPLE WHO LEFT
            # -------------------------------------------------

            left = (
                previous_participants
                - current_participants
            )

            for participant in sorted(left):

                print(
                    f"🔴 {participant} LEFT"
                )

                log_event(
                    participant,
                    "LEFT"
                )

                session.add_event(
                    participant,
                    "LEFT"
                )

                state.participant_left(
                    participant
                )

            # -------------------------------------------------
            # UPDATE PREVIOUS PARTICIPANTS
            # -------------------------------------------------

            if (joined or left) and on_change:
                try:
                    on_change(sorted(all_participants))
                except Exception:
                    pass

            previous_participants = (
                current_participants.copy()
            )

            # -------------------------------------------------
            # WAIT BEFORE NEXT CHECK
            # -------------------------------------------------

            time.sleep(
                POLL_INTERVAL
            )

    except KeyboardInterrupt:

        print()
        print("🛑 Tracker stopped manually.")

    finally:

        print()
        print("🛑 Stopping participant tracker...")

        # -----------------------------------------------------
        # SAVE PARTICIPANT LIST
        # -----------------------------------------------------

        if meeting_directory:

            participants_file = (
                Path(meeting_directory)
                / "participants.json"
            )

            participants_file.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            participants_data = {
                "participants": sorted(
                    all_participants
                )
            }

            participants_file.write_text(
                json.dumps(
                    participants_data,
                    indent=4,
                    ensure_ascii=False
                ),
                encoding="utf-8"
            )

            print()
            print("👥 Participants saved:")
            print(
                f"   {participants_file}"
            )

            print()
            print("👥 All participants:")

            for participant in sorted(
                all_participants
            ):
                print(
                    f"   - {participant}"
                )

        # -----------------------------------------------------
        # END SESSION
        # -----------------------------------------------------

        session.end()

        # -----------------------------------------------------
        # SAVE EXISTING PARTICIPANT REPORT
        # -----------------------------------------------------

        save_report(session)

        print(
            "👥 Participant tracker stopped."
        )

    return sorted(all_participants)