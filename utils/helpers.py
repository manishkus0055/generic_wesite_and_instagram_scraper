# utils/helpers.py

import random
from config.config import USER_AGENTS

def random_user_agent() -> str:
    return random.choice(USER_AGENTS)
