import time
import threading

from playwright.sync_api import sync_playwright

from config import MEET_URL

from meet.browser import (
    connect_to_chrome,
    open_meeting,
    join_meeting,
    verify_meeting
)

from meet.tracker import track_participants


stop_event = threading.Event()


with sync_playwright() as playwright:

    browser, context, page = connect_to_chrome(
        playwright
    )

    open_meeting(
        page,
        MEET_URL
    )

    join_meeting(page)

    if not verify_meeting(page):

        print("❌ Could not enter meeting.")

    else:

        print()
        print("================================")
        print("   STARTING TRACKER TEST")
        print("================================")
        print()

        track_participants(
            page,
            stop_event
        )

        print()
        print("✅ Tracker test finished.")