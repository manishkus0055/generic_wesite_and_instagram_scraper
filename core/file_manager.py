# core/file_manager.py

import os

class FileManager:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def profile_folder(self, site: str, identifier: str) -> str:
        folder = os.path.join(self.base_dir, site, identifier)
        os.makedirs(folder, exist_ok=True)
        for sub in ("text", "images", "videos", "stories", "highlights"):
            os.makedirs(os.path.join(folder, sub), exist_ok=True)
        return folder

    def generic_site_folder(self, site: str) -> str:
        folder = os.path.join(self.base_dir, site)
        os.makedirs(folder, exist_ok=True)
        for sub in ("text", "images", "links"):
            os.makedirs(os.path.join(folder, sub), exist_ok=True)
        return folder
