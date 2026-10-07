import threading

from pathlib import Path
from datetime import datetime

from playwright.sync_api import sync_playwright

from audio.full_meeting import process_full_meeting

from config import MEET_URL

from meet.browser import (
    connect_to_chrome,
    open_meeting,
    join_meeting,
    verify_meeting,
    leave_meeting
)

from meet.tracker import track_participants

from audio.recorder import record_continuously


# ============================================================
# CREATE MEETING FOLDER
# ============================================================

def create_meeting_folder():

    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    meeting_directory = Path(
        "meetings"
    ) / timestamp

    recordings_directory = (
        meeting_directory / "recordings"
    )

    recordings_directory.mkdir(
        parents=True,
        exist_ok=False
    )

    print()
    print("================================")
    print("       NEW MEETING")
    print("================================")
    print()

    print(
        f"📁 Meeting folder:"
    )

    print(
        f"   {meeting_directory}"
    )

    print()

    return meeting_directory, recordings_directory


# ============================================================
# MAIN
# ============================================================

def main():

    stop_event = threading.Event()

    # --------------------------------------------------------
    # CREATE UNIQUE MEETING FOLDER
    # --------------------------------------------------------

    meeting_directory, recordings_directory = (
        create_meeting_folder()
    )

    with sync_playwright() as playwright:

        # ----------------------------------------------------
        # CONNECT TO CHROME
        # ----------------------------------------------------

        browser, context, page = connect_to_chrome(
            playwright
        )

        # ----------------------------------------------------
        # OPEN MEETING
        # ----------------------------------------------------

        open_meeting(
            page,
            MEET_URL
        )

        # ----------------------------------------------------
        # JOIN MEETING
        # ----------------------------------------------------

        join_meeting(
            page
        )

        # ----------------------------------------------------
        # VERIFY
        # ----------------------------------------------------

        if not verify_meeting(page):

            print(
                "❌ Cannot continue."
            )

            return

        # ----------------------------------------------------
        # START AUDIO RECORDER
        # ----------------------------------------------------

        recorder_thread = threading.Thread(
            target=record_continuously,
            kwargs={
                "output_directory": str(
                    recordings_directory
                ),

                "chunk_duration": 60,

                "stop_event": stop_event
            }
        )

        recorder_thread.start()

        print()
        print("================================")
        print("   MEETING RECORDING STARTED")
        print("================================")
        print()

        print(
            f"🎙️ Audio chunks:"
        )

        print(
            f"   {recordings_directory}"
        )

        print()

        try:

            # ------------------------------------------------
            # TRACK PARTICIPANTS
            # ------------------------------------------------

            track_participants(
                page,
                stop_event,
                meeting_directory

            )

        except KeyboardInterrupt:

            print()
            print(
                "🛑 Meeting stopped manually."
            )

        finally:

            # ------------------------------------------------
            # LEAVE MEETING
            # ------------------------------------------------

            leave_meeting(
                page
            )

            # ------------------------------------------------
            # STOP RECORDER
            # ------------------------------------------------

            print()
            print(
                "🛑 Stopping audio recorder..."
            )

            stop_event.set()

            recorder_thread.join()

            print()
            print("================================")
            print("   MEETING RECORDING FINISHED")
            print("================================")
            print()

            # ------------------------------------------------
            # PROCESS AUDIO
            # ------------------------------------------------

            print()
            print("================================")
            print("   PROCESSING MEETING AUDIO")
            print("================================")
            print()

            print(
                f"📁 Processing:"
            )

            print(
                f"   {recordings_directory}"
            )

            print()

            try:

                final_segments = process_full_meeting(
                    str(meeting_directory)
                )

                print()
                print(
                    "✅ Meeting audio processing finished."
                )

                print()

            except Exception as e:

                print()
                print(
                    "❌ Meeting processing failed:"
                )

                print(
                    e
                )

                print()

            # ------------------------------------------------
            # FINAL LOCATION
            # ------------------------------------------------

            print()
            print("================================")
            print("       MEETING FILES")
            print("================================")
            print()

            print(
                f"📁 Meeting:"
            )

            print(
                f"   {meeting_directory}"
            )

            print()

            print(
                "Expected files:"
            )

            print(
                "   🎙️ recordings/"
            )

            print(
                "   📝 transcript.txt"
            )

            print(
                "   🤖 analysis.txt"
            )

            print(
                "   📄 meeting_report.pdf"
            )

            print()

            print(
                "================================"
            )
            print(
                "       MEETING COMPLETE"
            )
            print(
                "================================"
            )
            print()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()