import os
from typing import List

try:
    import dotenv
    dotenv.load_dotenv()
except ModuleNotFoundError:
    pass

class Neorg:
    prefex: List[str] = ["n.", "N."]

MODERATION_ROLES = ["mod", "admin"]
TOKEN = os.getenv("TOKEN")
# Paths
BOT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(BOT_DIR, os.pardir))

NEGATIVE_REPLIES = []
# bot replies
POSITIVE_REPLIES = []

ERROR_REPLIES = []
