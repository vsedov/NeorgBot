#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# File Name: test_mock_bot.py
import unittest

import discord

from tests import MockBot


class NeorgDiscordTest(unittest.TestCase):

    def default_role(self):
        role = MockBot.MockRole()
        # THIS WORKS
        self.assertIsInstance(role, discord.Role)


class NeorgObjectTest(unittest.TestCase):
    """Test objects, i.e creating user role and guild values"""
    pass
