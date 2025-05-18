# config/config.py

import os

# === PLAYWRIGHT SETTINGS ===
PLAYWRIGHT_HEADLESS = True
PLAYWRIGHT_PROXY = os.getenv("PROXY_URL", None)  # e.g. "http://user:pass@host:port"

# === INSTALOADER ===
INSTALOADER_SAVE_PATH = os.getenv("INSTALOADER_SAVE_PATH", "downloads/instagram")

# === FILE STRUCTURE ===
BASE_DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "downloads")
GENERIC_DIR = "generic"
INSTAGRAM_DIR = "instagram"

# === TIMEOUTS & RETRIES ===
REQUESTS_TIMEOUT = 15  # seconds
PLAYWRIGHT_TIMEOUT = 30000  # ms

# === CREDENTIALS (for private scraping) ===
IG_USERNAME = os.getenv("IG_USERNAME", "userid_for_log_in")
IG_PASSWORD = os.getenv("IG_PASSWORD", "user_pwd_for_login")

# === USER-AGENTS ===
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15"
]

# === New scroll settings ===
MAX_SCROLLS = 2           # Maximum scroll attempts
NO_CHANGE_LIMIT = 5        # Stop if no new content loads after this many attempts
SCROLL_PAUSE = 5         # Pause in seconds between scrolls to let content load
