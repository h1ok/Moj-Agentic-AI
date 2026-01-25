import os
import time
from typing import Optional

from playwright.sync_api import Page, sync_playwright


DEFAULT_TIMEOUT = 30_000


def _launch_browser(p, headless: bool):
    """Launch Chromium with optional Chrome channel (defaults to installed Chrome)."""
    chrome_channel = os.getenv("XSUITE_CHROME_CHANNEL", "").strip() or "chrome"
    try:
        return p.chromium.launch(channel=chrome_channel, headless=headless)
    except Exception:
        # Fallback if channel isn't available
        return p.chromium.launch(headless=headless)


def _norm_tweet_url(url: str) -> str:
    url = (url or "").strip()
    # Accept x.com or twitter.com
    if url.startswith("https://twitter.com/"):
        url = url.replace("https://twitter.com/", "https://x.com/", 1)
    return url


def _goto_tweet(page: Page, tweet_url: str):
    tweet_url = _norm_tweet_url(tweet_url)
    if not tweet_url:
        raise ValueError("tweet_url required")
    page.goto(tweet_url, wait_until="domcontentloaded")
    # Ensure tweet page is ready
    page.wait_for_timeout(1200)
    # Sometimes content loads after initial DOMContentLoaded
    page.locator("article").first.wait_for(state="visible", timeout=60_000)


def _click_first_visible(page: Page, selectors: list[str], timeout_ms: int = 30_000):
    deadline = time.time() + (timeout_ms / 1000.0)
    last_err: Optional[Exception] = None
    while time.time() < deadline:
        for sel in selectors:
            try:
                loc = page.locator(sel)
                if loc.count() and loc.first.is_visible():
                    loc.first.scroll_into_view_if_needed()
                    try:
                        loc.first.click(timeout=3_000)
                    except Exception:
                        loc.first.click(timeout=3_000, force=True)
                    return
            except Exception as e:
                last_err = e
        page.wait_for_timeout(250)
    if last_err:
        raise last_err
    raise TimeoutError("Could not find a clickable element")


def _wait_any(page: Page, selectors: list[str], timeout_ms: int = 30_000):
    deadline = time.time() + (timeout_ms / 1000.0)
    while time.time() < deadline:
        for sel in selectors:
            try:
                loc = page.locator(sel)
                if loc.count() and loc.first.is_visible():
                    return
            except Exception:
                pass
        page.wait_for_timeout(200)
    raise TimeoutError("Timeout waiting for expected UI")



def _wait_publish_button_enabled(page: Page, timeout_ms: int = 120_000):
    """انتظار زر إرسال الرد يصبح enabled بدون استخدام evaluate/wait_for_function (لتجنب CSP unsafe-eval)."""
    dialog = page.locator("div[role='dialog']")
    scope = dialog.first if dialog.count() else page
    deadline = time.time() + (timeout_ms / 1000.0)

    selectors = [
        "button[data-testid='tweetButtonInline']",
        "button[data-testid='tweetButton']",
        "button:has-text('Reply')",
        "button:has-text('رد')",
        "button:has-text('نشر')",
        "button:has-text('Post')",
    ]

    while time.time() < deadline:
        for sel in selectors:
            try:
                btn = scope.locator(sel)
                if btn.count() and btn.first.is_visible():
                    aria = btn.first.get_attribute("aria-disabled")
                    try:
                        enabled = btn.first.is_enabled()
                    except Exception:
                        enabled = (aria != "true")
                    if enabled and (aria != "true"):
                        return
            except Exception:
                pass
        page.wait_for_timeout(250)

    # لا نرمي خطأ هنا لأن X أحيانًا لا يبدّل حالة الزر بشكل واضح رغم أن الضغط ينجح
    return


def like_tweet(storage_state_path: str, tweet_url: str, headless: bool, wait_after_ms: int = 2_000):
    """Like a tweet by URL."""
    with sync_playwright() as p:
        browser = _launch_browser(p, headless=headless)
        context = browser.new_context(storage_state=storage_state_path)
        page = context.new_page()
        page.set_default_timeout(DEFAULT_TIMEOUT)
        try:
            _goto_tweet(page, tweet_url)

            # Prefer stable testids
            selectors = [
                "div[data-testid='like']",
                "button[data-testid='like']",
                "div[role='button'][data-testid='like']",
                # Fallback to aria-label (EN/AR)
                "[aria-label*='Like']",
                "[aria-label*='إعجاب']",
                "[aria-label*='أعجب']",
            ]
            _click_first_visible(page, selectors, timeout_ms=60_000)

            page.wait_for_timeout(wait_after_ms)
        finally:
            context.close()
            browser.close()


def repost_tweet(storage_state_path: str, tweet_url: str, headless: bool, wait_after_ms: int = 2_000):
    """Repost (retweet) a tweet by URL."""
    with sync_playwright() as p:
        browser = _launch_browser(p, headless=headless)
        context = browser.new_context(storage_state=storage_state_path)
        page = context.new_page()
        page.set_default_timeout(DEFAULT_TIMEOUT)
        try:
            _goto_tweet(page, tweet_url)

            # Step 1: open repost menu
            open_menu_selectors = [
                "div[data-testid='retweet']",
                "button[data-testid='retweet']",
                "div[role='button'][data-testid='retweet']",
                # recorded: aria label contains reposts. Repost
                "[aria-label*='reposts'][aria-label*='Repost']",
                "[aria-label*='Repost']",
                "[aria-label*='إعادة النشر']",
                "[aria-label*='إعاده النشر']",
                "[aria-label*='إعادة نشر']",
            ]
            _click_first_visible(page, open_menu_selectors, timeout_ms=60_000)

            # Step 2: choose "Repost" from menu
            menu_item_selectors = [
                "div[role='menuitem']:has-text('Repost')",
                "div[role='menuitem']:has-text('إعادة النشر')",
                "div[role='menuitem']:has-text('إعاده النشر')",
                "div[role='menuitem']:has-text('إعادة نشر')",
                "span:has-text('Repost')",
                "span:has-text('إعادة النشر')",
                "span:has-text('إعاده النشر')",
                "span:has-text('إعادة نشر')",
            ]
            # Wait for menu to appear then click
            _wait_any(page, ["div[role='menu']", "div[role='menuitem']"], timeout_ms=15_000)
            _click_first_visible(page, menu_item_selectors, timeout_ms=30_000)

            page.wait_for_timeout(wait_after_ms)
        finally:
            context.close()
            browser.close()


def reply_to_tweet(
    storage_state_path: str,
    tweet_url: str,
    reply_text: str,
    headless: bool,
    wait_after_ms: int = 5_000,
):
    """Reply to a tweet by URL."""
    reply_text = (reply_text or "").strip()
    if not reply_text:
        raise ValueError("reply_text required")

    with sync_playwright() as p:
        browser = _launch_browser(p, headless=headless)
        context = browser.new_context(storage_state=storage_state_path)
        page = context.new_page()
        page.set_default_timeout(DEFAULT_TIMEOUT)
        try:
            _goto_tweet(page, tweet_url)

            # Open reply composer (if needed)
            reply_btn_selectors = [
                "div[data-testid='reply']",
                "button[data-testid='reply']",
                "div[role='button'][data-testid='reply']",
                "[aria-label*='Reply']",
                "[aria-label*='رد']",
            ]
            # If textbox already visible, skip clicking reply
            textbox = page.locator("div[data-testid='tweetTextarea_0']")
            if not (textbox.count() and textbox.first.is_visible()):
                _click_first_visible(page, reply_btn_selectors, timeout_ms=30_000)

            # Textbox
            tb = page.locator("div[data-testid='tweetTextarea_0'][role='textbox']")
            if not tb.count():
                tb = page.locator("div[data-testid='tweetTextarea_0']")
            tb.first.wait_for(state="visible", timeout=60_000)
            tb.first.click()
            try:
                tb.first.fill(reply_text)
            except Exception:
                tb.first.press("Control+A")
                tb.first.type(reply_text, delay=10)

            # Publish reply: tweetButtonInline preferred
            publish_selectors = [
                "button[data-testid='tweetButtonInline']",
                "button[data-testid='tweetButton']",
                # fallback by visible text (EN/AR)
                "button:has-text('Reply')",
                "button:has-text('رد')",
                "button:has-text('نشر')",
                "button:has-text('Post')",
            ]

            # Wait until enabled (especially when video/media is processing)
            _wait_publish_button_enabled(page, timeout_ms=120_000)

            _click_first_visible(page, publish_selectors, timeout_ms=30_000)

            # Wait 5s as requested then exit
            page.wait_for_timeout(wait_after_ms)
        finally:
            context.close()
            browser.close()
