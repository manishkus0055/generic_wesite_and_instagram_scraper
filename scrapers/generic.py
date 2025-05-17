# scraper/generic.py

import os
import requests
from bs4 import BeautifulSoup
from config.config import REQUESTS_TIMEOUT
from core.file_manager import FileManager

class GenericScraper:
    def __init__(self):
        self.timeout = REQUESTS_TIMEOUT
        self.file_mgr = FileManager("downloads")

    def scrape(self, url: str):
        domain = url.split("//")[-1].split("/")[0]
        folder = self.file_mgr.generic_site_folder(domain)

        os.makedirs(os.path.join(folder, "text"), exist_ok=True)
        os.makedirs(os.path.join(folder, "links"), exist_ok=True)
        os.makedirs(os.path.join(folder, "images"), exist_ok=True)

        resp = requests.get(url, timeout=self.timeout, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")

        # Titles and headings
        title = soup.title.string if soup.title else ""
        headings = [h.get_text(strip=True) for h in soup.find_all(["h1", "h2", "h3"])]

        with open(f"{folder}/text/title.txt", "w", encoding="utf-8") as f:
            f.write(title + "\n")

        with open(f"{folder}/text/headings.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(headings))

        # All text
        with open(f"{folder}/text/all_text.txt", "w", encoding="utf-8") as f:
            f.write(soup.get_text(separator="\n"))

        # Links
        links = [a['href'] for a in soup.find_all('a', href=True)]
        with open(f"{folder}/links/links.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(links))

        # Images
        for idx, img in enumerate(soup.find_all('img', src=True), start=1):
            src = img['src']
            try:
                img_data = requests.get(src, timeout=self.timeout).content
                ext = src.split(".")[-1].split("?")[0]
                with open(f"{folder}/images/img_{idx}.{ext}", "wb") as img_f:
                    img_f.write(img_data)
            except Exception:
                continue
