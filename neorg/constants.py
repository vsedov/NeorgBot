#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# File Name: constants.py
import os
from dataclasses import dataclass
from typing import Optional

__import__("dotenv").load_dotenv()


@dataclass
class Bot:
    """Neorg Guild confgis"""
    prefex: list[str] = "n."


BOT_TRACE_LOGGERS: list[str] = [f"!{__name__}"]

USE_SENTRY: bool = True

# Mod roles
MODERATION_ROLES: list[str] = ["mod", "admin"]

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
