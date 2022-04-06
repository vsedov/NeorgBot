import os
from typing import List

__import__("dotenv").load_dotenv()

class Neorg:
    prefex: List[str] = "n."

MODERATION_ROLES = ["mod", "admin"]
TOKEN = os.getenv("TOKEN")
SENTRY = os.getenv("SENTRY_DSN")

# Paths
BOT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(BOT_DIR, os.pardir))

NEGATIVE_REPLIES = []
# bot replies
POSITIVE_REPLIES = []

ERROR_REPLIES = []
