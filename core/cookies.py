# core/cookies.py

import json, os
from core.browser import BrowserManager

class CookieManager:
    def __init__(self, browser_mgr: BrowserManager, cookie_dir="cookies"):
        self.browser_mgr = browser_mgr
        self.cookie_dir = cookie_dir
        os.makedirs(self.cookie_dir, exist_ok=True)

    def save(self, name: str):
        cookies = self.browser_mgr.context.cookies()
        path = os.path.join(self.cookie_dir, f"{name}.json")
        with open(path, "w") as f:
            json.dump(cookies, f)

    def load(self, name: str):
        path = os.path.join(self.cookie_dir, f"{name}.json")
        if not os.path.exists(path):
            return False
        with open(path) as f:
            cookies = json.load(f)
        self.browser_mgr.context.add_cookies(cookies)
        return True
