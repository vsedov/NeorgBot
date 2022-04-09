#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# File Name: test_mock_bot.py
import unittest

import discord

from tests import MockBot


class NeorgDiscordTest(unittest.TestCase):

    def test_role_instance(self):
        """Check if instance replicates Role."""
        role = MockBot.MockRole()
        self.assertIsInstance(role, discord.Role)

    def test_member_instance(self):
        """Check if instance replicates discord.Members."""
        member = MockBot.MockMember()
        self.assertIsInstance(member, discord.Member)

    def test_guild_instance(self):
        """Check if instance replicates Guild."""
        guild = MockBot.MockGuild()
        self.assertIsInstance(guild, discord.Guild)
