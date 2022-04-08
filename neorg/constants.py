#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# File Name: constants.py
import os

__import__("dotenv").load_dotenv()


class Neorg:
    """Neorg Guild confgis"""
    #  TODO(vsedov) (05:09:25 - 07/04/22): Change this to load multiple prefixes
    prefex: list[str] = "n."


USE_SENTRY: bool = True

# Mod roles
MODERATION_ROLES: list[str] = ["mod", "admin"]

# Keys
TOKEN: "env" = os.getenv("TOKEN")
SENTRY: "env" = os.getenv("SENTRY_DSN") if USE_SENTRY else None

# paths
BOT_DIR: str = os.path.dirname(__file__)
PROJECT_ROOT: str = os.path.abspath(os.path.join(BOT_DIR, os.pardir))

# bot negative replies
NEGATIVE_REPLIES: list[str] = []
# bot replies
POSITIVE_REPLIES: list[str] = []
# bot error replies
ERROR_REPLIES: list[str] = []
