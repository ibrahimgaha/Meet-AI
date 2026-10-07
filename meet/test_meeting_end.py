import time

from playwright.sync_api import sync_playwright

from config import MEET_URL

from meet.browser import (
    connect_to_chrome,
    open_meeting,
    join_meeting,
    verify_meeting,
    meeting_has_ended
)


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
        print("👀 Monitoring meeting...")
        print("End the meeting from the other participant.")
        print()

        while True:

            if meeting_has_ended(page):

                print()
                print("================================")
                print("   MEETING ENDED ✅")
                print("================================")
                print()

                break

            print(
                f"Current URL: {page.url}"
            )

            time.sleep(2)