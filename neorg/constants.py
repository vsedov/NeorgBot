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
    norg_blue: int = 0x4878BE


class Guild:
    """Guid Configs settings"""
    id: int = 834325286664929280

    section: str = "guild"
    moderation_channels: List[int] = [834857574850625586]
    moderation_roles: List[int] = [834325554131369995, 834325701892636672]

    reaction_channel: int = 1032633634798190644  # channel id for the message
    reaction_msg_id: int = 1032633967029014628  # message id which is active for reactions
    # map of reaction emoji: role id
    reaction_roles = {
        "📥": 1032634526033248266,
        "⚡": 1032634280985239662
    }


BOT_TRACE_LOGGERS: list[str] = [f"!{__name__}"]

USE_SENTRY: bool = False
TAG_SETUP: bool = False

PREFIX = Keys.prefix
NORG_BLUE = Keys.norg_blue

GUILD_ID = Guild.id

# Mod roles
MODERATION_ROLES: list[int] = Guild.moderation_roles

# Reaction Roles
REACTION_ROLES: dict[str, int] = Guild.reaction_roles
REACTION_MSG_ID: int = Guild.reaction_msg_id
REACTION_CHANNEL: int = Guild.reaction_channel

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
