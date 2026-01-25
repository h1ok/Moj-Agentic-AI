import os
from typing import Optional

from playwright.sync_api import sync_playwright


def _pick_composer_file_input(page):
    loc = page.locator("input[type='file']")
    return loc.first


def _wait_media_uploaded(page, timeout_ms: int = 180_000):
    # Best-effort: wait for progress to settle
    page.wait_for_timeout(2500)


def post_to_x(storage_state_path: str, text: str, media_path: Optional[str], headless: bool):
    chrome_channel = os.getenv('XSUITE_CHROME_CHANNEL', '').strip() or None
    with sync_playwright() as p:
        if chrome_channel:
            browser = p.chromium.launch(channel=chrome_channel, headless=headless)
        else:
            browser = p.chromium.launch(headless=headless)

        context = browser.new_context(storage_state=storage_state_path)
        page = context.new_page()

        page.goto("https://x.com/home", wait_until="domcontentloaded")
        page.wait_for_timeout(2000)

        page.get_by_test_id("SideNav_NewTweet_Button").click()
        page.wait_for_timeout(1500)

        textbox = page.get_by_role("textbox", name="Post text")
        textbox.wait_for(state="visible", timeout=20_000)

        if media_path:
            file_input = _pick_composer_file_input(page)
            file_input.wait_for(state="attached", timeout=20_000)
            file_input.set_input_files(media_path)
            _wait_media_uploaded(page, timeout_ms=180_000)

        textbox.fill(text)
        page.get_by_test_id("tweetButton").click()
        page.wait_for_timeout(2500)

        context.close()
        browser.close()
