#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# File Name: test_mock_bot.py
import unittest

import discord

from tests import MockBot


class NeorgDiscordTest(unittest.TestCase):
    """NeorgMock bot Test cases."""

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

    def test_bot_instance(self):
        """Check if MockBot is correct towards discord.ext.commands.Bot."""
        bot = MockBot.MockBot()
        self.assertIsInstance(bot, discord.ext.commands.Bot)

    def test_mock_context_instance(self):
        """Tests if MockContext initializes with the correct values."""
        context = MockBot.MockContext()

        # The `spec` argument makes sure `isistance` checks with `discord.ext.commands.Context` pass
        self.assertIsInstance(context, discord.ext.commands.Context)

        self.assertIsInstance(context.bot, MockBot.MockBot)
        self.assertIsInstance(context.guild, MockBot.MockGuild)
        self.assertIsInstance(context.author, MockBot.MockMember)
