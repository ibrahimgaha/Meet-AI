from playwright.sync_api import Page


def get_participants(page: Page):

    participants = set()

    elements = page.locator("span.notranslate")

    count = elements.count()

    for i in range(count):

        try:

            element = elements.nth(i)

            if not element.is_visible():
                continue

            name = element.inner_text().strip()

            if name:

                participants.add(name)

        except Exception:

            pass

    return participants