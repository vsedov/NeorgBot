#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# File Name: constants.py
import os
from typing import List

__import__("dotenv").load_dotenv()

class Neorg:
    """Neorg Guild confgis"""
    #  TODO(vsedov) (05:09:25 - 07/04/22): Change this to load multiple prefixes
    prefex: List[str] = "n."

# Mod roles
MODERATION_ROLES = ["mod", "admin"]

# Keys
TOKEN = os.getenv("TOKEN")
SENTRY = os.getenv("SENTRY_DSN")

# paths
BOT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(BOT_DIR, os.pardir))

# bot negative replies
NEGATIVE_REPLIES = []
# bot replies
POSITIVE_REPLIES = []
# bot error replies
ERROR_REPLIES = []
