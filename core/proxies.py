# core/proxies.py

import random
from config.config import PLAYWRIGHT_PROXY

class ProxyRotator:
    def __init__(self, proxy_list=None):
        self.proxies = proxy_list or ([PLAYWRIGHT_PROXY] if PLAYWRIGHT_PROXY else [])

    def get_proxy(self):
        if not self.proxies:
            return None
        return random.choice(self.proxies)
