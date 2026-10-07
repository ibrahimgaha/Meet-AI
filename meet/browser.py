import os
import subprocess
import urllib.request
from playwright.sync_api import Page

from config import (
    CHROME_DEBUG_URL,
    JOIN_BUTTON_NAME,
    MEETING_STARTED_TEXT
)

CHROME_EXE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
CHROME_PROFILE_DIR = os.path.expandvars(r"%TEMP%\meet-chrome")


def is_chrome_debug_running() -> bool:
    """Checks whether Chrome CDP endpoint on port 9222 responds."""
    try:
        with urllib.request.urlopen(f"{CHROME_DEBUG_URL}/json/version", timeout=1.5) as response:
            return response.status == 200
    except Exception:
        return False


def launch_chrome_with_debug():
    """
    Terminates existing chrome.exe instances and automatically starts Chrome
    configured with remote debugging on port 9222 and user-data-dir in %TEMP%\meet-chrome.
    """
    print("🚀 Auto-launching Chrome with remote debugging on port 9222...")
    try:
        # 1. Kill any existing chrome instances
        subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"], capture_output=True)
        time.sleep(1)
    except Exception as e:
        print(f"Taskkill warning: {e}")

    # 2. Launch Chrome with required arguments
    cmd = [
        CHROME_EXE,
        "--remote-debugging-port=9222",
        f"--user-data-dir={CHROME_PROFILE_DIR}"
    ]

    try:
        subprocess.Popen(cmd)
        print("Waiting for Chrome CDP to be ready...")
        # Poll up to 10 seconds for CDP endpoint to respond
        for _ in range(20):
            time.sleep(0.5)
            if is_chrome_debug_running():
                print("Chrome CDP ready ✅")
                return True
    except Exception as e:
        print(f"Failed to launch Chrome: {e}")

    return is_chrome_debug_running()


def connect_to_chrome(playwright):

    # Automatically launch Chrome if not already running on port 9222
    if not is_chrome_debug_running():
        launch_chrome_with_debug()

    print("Connecting to Chrome...")

    browser = playwright.chromium.connect_over_cdp(
        CHROME_DEBUG_URL
    )

    context = browser.contexts[0]

    if context.pages:

        page = context.pages[0]

    else:

        page = context.new_page()

    print("Connected to Chrome ✅")

    return browser, context, page


def open_meeting(page: Page, meet_url: str):

    print("Opening Google Meet...")

    page.goto(
        meet_url,
        wait_until="domcontentloaded"
    )

    print("Meet loaded ✅")

    time.sleep(5)


def join_meeting(page: Page):

    try:

        join_button = page.get_by_role(
            "button",
            name=JOIN_BUTTON_NAME
        )

        if join_button.is_visible():

            print("Join button found ✅")

            print("Joining meeting...")

            join_button.click()

            print("Joined meeting ✅")

            time.sleep(8)

        else:

            print("Already inside the meeting.")

    except Exception as e:

        print("Join step:", e)


def verify_meeting(page: Page):

    time.sleep(3)

    try:

        leave_button = page.get_by_role(
            "button",
            name="Quitter l'appel"
        )

        if leave_button.is_visible():

            print()
            print("================================")
            print(" BOT IS INSIDE THE MEETING ✅")
            print("================================")

            return True

    except Exception:
        pass

    print()
    print("⚠️ Could not confirm meeting.")
    print(f"Current URL: {page.url}")

    return False

def leave_meeting(page: Page):


    print()
    print("🚪 Leaving Google Meet...")

    try:

        leave_button = page.get_by_role(
            "button",
            name="Quitter l'appel"
        )

        if leave_button.is_visible():

            leave_button.click()

            print("✅ Bot left the meeting.")

        else:

            print("⚠️ Leave button not visible.")

    except Exception as e:

        print(
            f"⚠️ Could not leave meeting: {e}"
        )  

def meeting_has_ended(page: Page):

    # Google Meet may keep the meeting URL
    # even after the call has ended.

    if page.url == "https://meet.google.com/home":
        return True

    try:
        body_text = page.locator("body").inner_text()

        if "Vous avez quitté la réunion" in body_text:
            return True

    except Exception:
        pass

    return False