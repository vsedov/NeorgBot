#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# File Name: constants.py
import os
from dataclasses import dataclass
from typing import List, Optional

__import__("dotenv").load_dotenv()


@dataclass
class Keys:
    """Neorg Guild confgis"""

    prefix: str = "n."


class Guild:
    """Guid Configs settings"""

    section: str = "guild"
    moderation_channels: List[int] = [834857574850625586]
    moderation_roles: List[int] = [834325554131369995, 834325701892636672]


BOT_TRACE_LOGGERS: list[str] = [f"!{__name__}"]

USE_SENTRY: bool = True
TAG_SETUP: bool = False

PREFIX = Keys.prefix

# Mod roles
MODERATION_ROLES: list[str] = Guild.moderation_roles

# Keys
TOKEN: Optional[str] = os.getenv("TOKEN")
SENTRY: Optional[str] = os.getenv("SENTRY_DSN") if USE_SENTRY else ""

# paths
BOT_DIR: Optional[str] = os.path.dirname(__file__)
PROJECT_ROOT: Optional[str]
# bot error replies
ERROR_REPLIES: list[str] = []

# Social_credit file
SOCIAL_CREDIT_FILE = os.path.join(BOT_DIR, "utils/database/user.json")
PNP_DATABAS_FILE = os.path.join(BOT_DIR, "utils/database/database.json")

# If someone says something good about this, their score will be reduced .
NEGATIVE_WORDS = ["java", "prolog"]

DATABASE_PATH = os.path.join(BOT_DIR, "fetch_info/data/")
THIRD_PARTY_PATH = os.path.join(BOT_DIR, "fetch_info/third_party/")
FETCH_INFO_PATH = os.path.join(BOT_DIR, "fetch_info/")
