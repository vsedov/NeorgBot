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

PREFIX = Keys.prefix

# Mod roles
MODERATION_ROLES: list[str] = Guild.moderation_roles

# Keys
TOKEN: Optional[str] = os.getenv("TOKEN")
SENTRY: Optional[str] = os.getenv("SENTRY_DSN") if USE_SENTRY else ""

# paths
BOT_DIR: Optional[str] = os.path.dirname(__file__)
PROJECT_ROOT: Optional[str]
# bot negative replies
NEGATIVE_REPLIES: list[str] = []
# bot replies
POSITIVE_REPLIES: list[str] = []
# bot error replies
ERROR_REPLIES: list[str] = []
