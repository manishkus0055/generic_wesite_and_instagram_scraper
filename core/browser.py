# core/browser.py

from playwright.sync_api import sync_playwright
from config.config import PLAYWRIGHT_HEADLESS, PLAYWRIGHT_PROXY, PLAYWRIGHT_TIMEOUT, USER_AGENTS
import random

class BrowserManager:
    def __init__(self):
        self.play = sync_playwright().start()
        self.browser = self.play.firefox.launch(headless=PLAYWRIGHT_HEADLESS,
                                                proxy={"server": PLAYWRIGHT_PROXY} if PLAYWRIGHT_PROXY else None)
        self.context = self.browser.new_context(
            user_agent=random.choice(USER_AGENTS),
            viewport={"width": 1280, "height": 800},
            ignore_https_errors=True
        )
        self.context.set_default_timeout(PLAYWRIGHT_TIMEOUT)
        self.page = self.context.new_page()

    def goto(self, url, timeout=30000, wait_until="load"):
        print(f"[Browser] Navigating to: {url}")
        try:
            self.page.goto(url, timeout=timeout, wait_until=wait_until)
        except Exception as e:
            print(f"Navigation to {url} failed: {e}")
            print("Retrying with fallback strategy...")
            try:
                self.page.goto(url, timeout=timeout, wait_until="domcontentloaded")
            except Exception as e2:
                print(f"Final navigation failure: {e2}")
                raise


    def close(self):
        self.context.close()
        self.browser.close()
        self.play.stop()
