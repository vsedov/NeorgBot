#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# File Name: MockBot.py
import itertools
import logging
import unittest.mock
from collections import ChainMap, defaultdict
from typing import Optional

import discord

from neorg.neorg import Neorg

GUILD_DATA = {
    'id': 1,
    'name': 'guild',
    'region': 'Europe',
    'verification_level': 1,
    'default_notications': 1,
    'afk_timeout': 100,
    'icon': "icon.png",
    'banner': 'banner.png',
    'mfa_level': 1,
    'splash': 'splash.png',
    'system_channel_id': 320923845093890044,
    'description': 'mocking is fun',
    'max_presences': 10_000,
    'max_members': 100_000,
    'preferred_locale': 'UTC',
    'owner_id': 1,
    'afk_channel_id': 320923845094090044,
}
ROLE_DATA = {
    'name': 'role',
    'id': 1
}

MEMBER_DATA = {
    'user': 'aloof',
    'roles': [1]
}  # Mock Guild,, think of it as a basis for what data we will be testing
guild_instance = discord.Guild(data=GUILD_DATA, state=unittest.mock.MagicMock())

# test role set with our test guild data
role_instance = discord.Role(guild=guild_instance, state=unittest.mock.MagicMock(), data=ROLE_DATA)
member_instance = discord.Member(data=MEMBER_DATA, guild=guild_instance, state=unittest.mock.MagicMock())

# time to make a fake user
user_instance = discord.User(
    data=unittest.mock.MagicMock(
        get=unittest.mock.Mock(
            side_effect=(
                defaultdict(
                    unittest.mock.MagicMock, {
                        'id': 1,
                        'name': 'user',
                        'discriminator': '0000',
                        'avatar': 'avatar.png',
                        'bot': False,
                        'system': False,
                        'mfa_enabled': False,
                        'locale': 'en-US',
                        'verified': False,
                    })).get)),
    state=unittest.mock.MagicMock())


def manage_loggers():
    """Reduce error rate as issues when tracing stuff, best to keep it quiet."""
    for logger in logging.Logger.manager.loggerDict.values():
        if not isinstance(logger, logging.Logger):
            continue
        logger.setLevel(logging.CRITICAL)


manage_loggers()


class CustomMock:
    """ChildMockType allows use to only define __init__ and __call__."""
    child_mock_type = unittest.mock.MagicMock
    discord_id = itertools.count(0)
    """This is an overidable value, based on different specs of the mock"""
    spec_set = None  # only defined for instances

    def __init__(self, custom_name: str, **kwargs):
        custom_name = custom_name or "None"
        super().__init__(name=custom_name, **kwargs)
        if custom_name:
            self.name = custom_name


class MockRole(CustomMock, unittest.mock.Mock):
    """Mock SubClass to mock discord.Role Class,"""

    spec_set = role_instance

    def __init__(self, **kwargs) -> None:
        default_kwargs = {
            'id': next(self.discord_id),
            'name': 'role',
            'pos': 1,
            'colour': discord.Color(0x4878BE),
            'permissions': discord.permissions()
        }
        # update default_kwargs with kwargs
        super().__init__(**ChainMap(default_kwargs, kwargs))
        if isinstance(self.colour, int):
            self.colour = discord.Colour(self.colour)

        if isinstance(self.permissions, int):
            self.permissions = discord.Permissions(self.permissions)


class MockMember(CustomMock, unittest.mock.Mock):
    """Mock Subclass for discord.member object."""
    spec_set = member_instance

    def __init__(self, roles: Optional[MockRole] = None, **kwargs) -> None:
        default_kwargs = {
            'id': next(self.discord_id),
            'name': 'member',
            'roles': [],
            'joined_at': '2020-01-01T00:00:00.000000+00:00',
            'bot': False,
            'pending': False,
            'self_deaf': False,
            'self_mute': False,
            'voice': None,
            'user': None
        }
        super().__init__(**ChainMap(default_kwargs, kwargs))
        self.roles = [MockRole(name="@everyone", pos=1, id=1)]
        if roles:
            self.roles.extend(roles)

        if 'mention' not in kwargs:
            self.mention = f"@{self.name}"

    def get_max_role(self) -> MockRole:
        if self.roles:
            return max(self.roles)
        return None


class MockGuild(CustomMock, unittest.mock.Mock):
    """
    Mock Subclass for discord.Guild objects
    Ideally we want to be sure that out guild is

    guild = MockGuild()
    isinstance(discord.guild, guild)
    to be true,
    """

    spec_set = guild_instance

    def __init__(self, roles: Optional[MockRole] = None, **kwargs) -> None:
        default_kwargs = {
            'id': next(self.discord_id),
            'members': []
        }
        super().__init__(**default_kwargs, **kwargs)
        self.roles = [MockRole(name="@everyone", pos=1, id=1)]

        if roles:
            self.roles.extend(roles)


class MockUser(CustomMock, unittest.mock.Mock):
    """Mock Subclass for discord.User"""
    spect_set = user_instance

    def __init__(self, **kwargs) -> None:
        default_kwargs = {
            'id': next(self.discord_id),
            'name': 'user',
            'discriminator': '0000',
            'avatar': 'avatar.png',
            'bot': False,
            'system': False,
            'mfa_enabled': False,
            'locale': 'en-US',
            'verified': False,
        }
        super().__init__(**ChainMap(default_kwargs, kwargs))


class MockBot(CustomMock, unittest.mock.MagicMock):
    """
    Magic mock subclass for our neorg bot

    """
    spec_set = Neorg(command_prefix=unittest.mock.MagickMock(), loop=unittest.mock.MagicMock())

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # replicate what we had before for the loop set
        self.loop = kwargs.get('loop', self.spec_set)
