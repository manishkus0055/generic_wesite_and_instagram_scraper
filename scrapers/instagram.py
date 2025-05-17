# scraper/instagram.py

import os, time, csv, re, requests, instaloader
from instaloader import Instaloader, Profile, Post
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from core.browser import BrowserManager
from core.cookies import CookieManager
from core.file_manager import FileManager
from config.config import IG_USERNAME, IG_PASSWORD, INSTALOADER_SAVE_PATH, MAX_SCROLLS, NO_CHANGE_LIMIT, SCROLL_PAUSE
from urllib.parse import urlparse
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

class InstagramScraper:
    def __init__(self):
        self.browser_mgr = BrowserManager()
        self.cookies = CookieManager(self.browser_mgr)
        self.file_mgr = FileManager(INSTALOADER_SAVE_PATH)
        self.loader = Instaloader(
            dirname_pattern=INSTALOADER_SAVE_PATH,
            download_videos=True,
            download_video_thumbnails=False,
            save_metadata=False,
            download_comments=False,
        )

    def login(self):
        if IG_USERNAME and IG_PASSWORD:
            print("Logging in with credentials...")
            self.browser_mgr.goto("https://www.instagram.com/accounts/login/")
            page = self.browser_mgr.page

            page.wait_for_selector('input[name="username"]', timeout=15000)
            page.fill('input[name="username"]', IG_USERNAME)
            page.fill('input[name="password"]', IG_PASSWORD)
            page.click('button[type="submit"]')

            page.wait_for_timeout(5000)
            try:
                page.wait_for_selector('text=Save Info', timeout=10000)
                page.click('text=Save Info')
                print("Clicked 'Save Info' popup.")
            except:
                print("'Save Info' popup not found or skipped.")

            page.wait_for_timeout(3000)
            self.cookies.save("instagram_session")
        else:
            raise ValueError("IG_USERNAME and IG_PASSWORD must be set for Instagram scraping.")

    def _ensure_logged_in(self):
        if not self.cookies.load("instagram_session"):
            print("No session cookies found. Logging in.")
            self.login()

    def scrape_profile(self, username: str):
        self._ensure_logged_in()

        folder = self.file_mgr.profile_folder("instagram", username)
        text_path = os.path.join(folder, "text")
        os.makedirs(text_path, exist_ok=True)

        profile = Profile.from_username(self.loader.context, username)

        info_file = os.path.join(text_path, "profile_info.txt")
        with open(info_file, "w", encoding="utf-8") as f:
            f.write(f"Username: {profile.username}\n")
            f.write(f"User ID: {profile.userid}\n")
            f.write(f"Full Name: {profile.full_name}\n")
            f.write(f"Bio: {profile.biography}\n")
            f.write(f"External Link: {profile.external_url}\n")
            f.write(f"Followers: {profile.followers}\n")
            f.write(f"Following: {profile.followees}\n")
            f.write(f"Profile Pic URL: {profile.profile_pic_url}\n")

        self.loader.dirname_pattern = folder
        self.loader.download_profile(username, profile_pic_only=True)

    def _scroll_to_load_all(self, page, scroll_pause=1.0, max_scrolls=50, no_change_limit=5):
        prev_height = 0
        unchanged_scrolls = 0
        scroll_count = 0

        while scroll_count < max_scrolls and unchanged_scrolls < no_change_limit:
            page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause)
            new_height = page.evaluate("document.body.scrollHeight")

            if new_height == prev_height:
                unchanged_scrolls += 1
            else:
                unchanged_scrolls = 0

            prev_height = new_height
            scroll_count += 1

        print(f"Scrolling finished after {scroll_count} scrolls ({unchanged_scrolls} unchanged).")

    def scrape_media_links(self, username: str):
        self._ensure_logged_in()

        base_url = f"https://www.instagram.com/{username}/"
        folder = self.file_mgr.profile_folder("instagram", username)
        text_folder = os.path.join(folder, "text")
        os.makedirs(text_folder, exist_ok=True)

        output_path = os.path.join(text_folder, "all_links.csv")
        all_links_set = set()
        page = self.browser_mgr.page

        targets = {
            "post": {
                "url": base_url,
                "class": "x1lliihq x1n2onr6 xh8yej3 x4gyw5p x11i5rnm x1ntc13c x9i3mqj x2pgyrj"
            },
            "reel": {
                "url": base_url + "reels/",
                "class": "x1qjc9v5 x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x78zum5 xdt5ytf x2lah0s xln7xf2 xk390pu xdj266r xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x11njtxf xpzaatj xw3qccf"
            },
            "tagged": {
                "url": base_url + "tagged/",
                "class": "x1lliihq x1n2onr6 xh8yej3 x4gyw5p x11i5rnm x1ntc13c x9i3mqj x2pgyrj"
            }
        }

        for media_type, data in targets.items():
            print(f"Visiting {media_type} page: {data['url']}")
            try:
                self.browser_mgr.goto(data["url"])
                page.wait_for_selector("main", timeout=20000)
            except PlaywrightTimeoutError:
                print(f"Timeout loading {media_type} page. Skipping...")
                continue

            print("Scrolling and extracting...")
            self._scroll_to_load_all(
                page,
                scroll_pause=SCROLL_PAUSE,
                max_scrolls=MAX_SCROLLS,
                no_change_limit=NO_CHANGE_LIMIT
            )

            class_selector = "." + ".".join(data["class"].split())
            links = page.eval_on_selector_all(
                f'{class_selector} a[href]',
                'elements => elements.map(el => el.getAttribute("href"))'
            )

            print(f"Found {len(links)} raw links on {media_type} page.")

            for href in links:
                if href and ("/p/" in href or "/reel/" in href):
                    full_url = "https://www.instagram.com" + href
                    all_links_set.add((media_type, full_url))

        print(f"Total unique media links collected: {len(all_links_set)}")

        with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["type", "url"])
            for media_type, url in sorted(all_links_set, key=lambda x: x[1]):
                writer.writerow([media_type, url])

        print(f"Saved all media links to: {output_path}")

    def download_media_by_category_from_csv(self, username, csv_path, limits: dict):

        if not os.path.isfile(csv_path):
            print(f"CSV file not found: {csv_path}")
            return

        category_links = {"post": [], "reel": [], "tagged": []}

        # Read and categorize links from CSV
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader, None)
            for row in reader:
                if len(row) >= 2:
                    category, url = row[0].strip().lower(), row[1].strip()
                    if category in category_links:
                        category_links[category].append(url)

        print("\nAvailable media counts:")
        for cat in category_links:
            print(f"  {cat}: {len(category_links[cat])}")

        print("\n⬇Starting downloads...\n")

        # Map categories to folder names inside the user's folder
        folder_map = {
            "post": "post",
            "reel": "videos",    # reels go to videos folder
            "tagged": "tagged"
        }

        # Base folder for this user downloads (e.g., downloads/instagram/instagram/username/)
        base_folder = self.file_mgr.profile_folder("instagram", username)
        os.makedirs(base_folder, exist_ok=True)

        for cat, urls in category_links.items():
            count = limits.get(cat, 0)
            selected_links = urls[:count]

            for link in selected_links:
                try:
                    shortcode_match = re.search(r'/([A-Za-z0-9_-]{10,})/', link)
                    if not shortcode_match:
                        print(f"Invalid Instagram link format: {link}")
                        continue
                    shortcode = shortcode_match.group(1)

                    target_subfolder = folder_map.get(cat, "others")
                    target_folder = os.path.join(base_folder, target_subfolder)
                    os.makedirs(target_folder, exist_ok=True)

                    # Set dirname_pattern to the category folder (full path)
                    self.loader.dirname_pattern = target_folder

                    post = instaloader.Post.from_shortcode(self.loader.context, shortcode)

                    # Download post with empty target to use dirname_pattern directly
                    self.loader.download_post(post, target="")

                    print(f"Downloaded [{cat.upper()}]: {link}")

                except Exception as e:
                    print(f"Failed to download {link}: {e}")


    def close(self):
        self.browser_mgr.close()
