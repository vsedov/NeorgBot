#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# File Name: MockBot.py
import collections
import itertools
import logging
import unittest.mock
from collections import ChainMap, defaultdict
from typing import Optional

import discord
from discord.ext.commands import Context

from neorg.neorg import Neorg

GUILD_DATA = {
    "id": 1,
    "name": "guild",
    "region": "Europe",
    "verification_level": 1,
    "default_notications": 1,
    "afk_timeout": 100,
    "icon": "icon.png",
    "banner": "banner.png",
    "mfa_level": 1,
    "splash": "splash.png",
    "system_channel_id": 320923845093890044,
    "description": "mocking is fun",
    "max_presences": 10_000,
    "max_members": 100_000,
    "preferred_locale": "UTC",
    "owner_id": 1,
    "afk_channel_id": 320923845094090044,
}
ROLE_DATA = {"name": "role", "id": 1}

MEMBER_DATA = {
    "user": "aloof",
    "roles": [1],
}  # Mock Guild,, think of it as a basis for what data we will be testing
CHANNEL_DATA = {
    "id": 1,
    "type": "TextChannel",
    "name": "channel",
    "parent_id": 1234567890,
    "topic": "topic",
    "position": 1,
    "nsfw": False,
    "last_message_id": 1,
}
# Create a Message instance to get a realistic MagicMock of `discord.Message`
MESSAGE_DATA = {
    "id": 1,
    "webhook_id": 320923845094090044,
    "attachments": [],
    "embeds": [],
    "application": "Python Discord",
    "activity": "mocking",
    "channel": unittest.mock.MagicMock(),
    "edited_timestamp": "2019-10-14T15:33:48+00:00",
    "type": "message",
    "pinned": False,
    "mention_everyone": False,
    "tts": None,
    "content": "content",
    "nonce": None,
}

EMEMOJI_DATA = {"require_colons": True, "managed": True, "id": 1, "name": "hyperlemon"}
guild_instance = discord.Guild(data=GUILD_DATA, state=unittest.mock.MagicMock())

# test role set with our test guild data
role_instance = discord.Role(
    guild=guild_instance, state=unittest.mock.MagicMock(), data=ROLE_DATA
)
member_instance = discord.Member(
    data=MEMBER_DATA, guild=guild_instance, state=unittest.mock.MagicMock()
)

# time to make a fake user
user_instance = discord.User(
    data=unittest.mock.MagicMock(
        get=unittest.mock.Mock(
            side_effect=(
                defaultdict(
                    unittest.mock.MagicMock,
                    {
                        "id": 1,
                        "name": "user",
                        "discriminator": "0000",
                        "avatar": "avatar.png",
                        "bot": False,
                        "system": False,
                        "mfa_enabled": False,
                        "locale": "en-US",
                        "verified": False,
                    },
                )
            ).get
        )
    ),
    state=unittest.mock.MagicMock(),
)

state = unittest.mock.MagicMock()
guild = unittest.mock.MagicMock()
text_channel_instance = discord.TextChannel(state=state, guild=guild, data=CHANNEL_DATA)

state = unittest.mock.MagicMock()
channel = unittest.mock.MagicMock()
message_instance = discord.Message(state=state, channel=channel, data=MESSAGE_DATA)


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
    """This is an overidable value, based on different specs of the mock."""
    spec_set = None  # only defined for instances

    def __init__(self, **kwargs):
        name = kwargs.pop(
            "name", None
        )  # `name` has special meaning for Mock classes, so we need to set it manually.
        super().__init__(spec_set=self.spec_set, **kwargs)
        if name:
            self.name = name


class MockRole(CustomMock, unittest.mock.Mock):
    """Mock SubClass to mock discord.Role Class."""

    spec_set = role_instance

    def __init__(self, **kwargs) -> None:
        default_kwargs = {
            "id": next(self.discord_id),
            "name": "role",
            "position": 1,
            "colour": discord.Colour(0xDEADBF),
            "permissions": discord.Permissions(),
        }
        # update default_kwargs with kwargs
        super().__init__(**ChainMap(default_kwargs, kwargs))

        if isinstance(self.colour, int):
            self.colour = discord.Colour(self.colour)

        if isinstance(self.permissions, int):
            self.permissions = discord.Permissions(self.permissions)

        if "mention" not in kwargs:
            self.mention = f"&{self.name}"

    def __lt__(self, other):
        """Simplified position-based comparisons similar to those of `discord.Role`."""
        return self.position < other.position

    def __ge__(self, other):
        """Simplified position-based comparisons similar to those of `discord.Role`."""
        return self.position >= other.position


class MockMember(CustomMock, unittest.mock.Mock):
    """Mock Subclass for discord.member object."""

    spec_set = member_instance

    def __init__(self, roles: Optional[MockRole] = None, **kwargs) -> None:
        default_kwargs = {
            "id": next(self.discord_id),
            "name": "member",
            "roles": [],
            "joined_at": "2020-01-01T00:00:00.000000+00:00",
            "bot": False,
            "pending": False,
        }
        super().__init__(**ChainMap(kwargs, default_kwargs))
        self.roles = [MockRole(name="@everyone", position=1, id=0)]
        if roles:
            self.roles.extend(roles)

        if roles:
            self.roles.extend(roles)
        self.top_role = max(self.roles)

        if "mention" not in kwargs:
            self.mention = f"@{self.name}"


class MockGuild(CustomMock, unittest.mock.Mock):
    """
    Mock Subclass for discord.Guild objects
    Ideally we want to be sure that out guild is

    guild = MockGuild()
    isinstance(discord.guild, guild)
    to be true.
    """

    spec_set = guild_instance

    def __init__(self, roles: Optional[MockRole] = None, **kwargs) -> None:
        default_kwargs = {"id": next(self.discord_id), "members": []}
        super().__init__(**default_kwargs, **kwargs)
        self.roles = [MockRole(name="@everyone", position=1, id=1)]

        if roles:
            self.roles.extend(roles)


class MockUser(CustomMock, unittest.mock.Mock):
    """Mock Subclass for discord.User"""

    spect_set = user_instance

    def __init__(self, **kwargs) -> None:
        default_kwargs = {
            "id": next(self.discord_id),
            "name": "user",
            "discriminator": "0000",
            "avatar": "avatar.png",
            "bot": False,
            "system": False,
            "mfa_enabled": False,
            "locale": "en-US",
            "verified": False,
        }
        super().__init__(**ChainMap(default_kwargs, kwargs))
        if "mention" not in kwargs:
            self.mention = f"@{self.name}"


class MockBot(CustomMock, unittest.mock.MagicMock):
    """
    Magic mock subclass for our neorg bot.

    """

    spec_set = Neorg(
        command_prefix=unittest.mock.MagicMock(), loop=unittest.mock.MagicMock()
    )

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # replicate what we had before for the loop set
        self.loop = kwargs.get("loop", self.spec_set)


class MockTextChannel(CustomMock, unittest.mock.Mock):
    """
    A MagicMock subclass to mock TextChannel objects.
    Instances of this class will follow the specifications of `discord.TextChannel` instances.
    """

    spec_set = text_channel_instance

    def __init__(self, **kwargs) -> None:
        default_kwargs = {
            "id": next(self.discord_id),
            "name": "channel",
            "guild": MockGuild(),
        }
        super().__init__(**collections.ChainMap(kwargs, default_kwargs))

        if "mention" not in kwargs:
            self.mention = f"#{self.name}"


# Create a Context instance to get a realistic MagicMock of `discord.ext.commands.Context`
context_instance = Context(
    message=unittest.mock.MagicMock(), prefix="$", bot=MockBot(), view=None
)
context_instance.invoked_from_error_handler = None


class MockContext(CustomMock, unittest.mock.MagicMock):
    """
    A MagicMock subclass to mock Context objects.
    """

    spec_set = context_instance

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.me = kwargs.get("me", MockMember())
        self.bot = kwargs.get("bot", MockBot())
        self.guild = kwargs.get("guild", MockGuild())
        self.author = kwargs.get("author", MockMember())
        self.channel = kwargs.get("channel", MockTextChannel())
        self.message = kwargs.get("message", MockMessage())
        self.invoked_from_error_handler = kwargs.get(
            "invoked_from_error_handler", False
        )


class MockMessage(CustomMock, unittest.mock.MagicMock):
    """
    A MagicMock subclass to mock Message objects.
    """

    spec_set = message_instance

    def __init__(self, **kwargs) -> None:
        default_kwargs = {"attachments": []}
        super().__init__(**collections.ChainMap(kwargs, default_kwargs))
        self.author = kwargs.get("author", MockMember())
        self.channel = kwargs.get("channel", MockTextChannel())


emoji_instance = discord.Emoji(
    guild=MockGuild(), state=unittest.mock.MagicMock(), data=EMEMOJI_DATA
)


class MockEmoji(CustomMock, unittest.mock.MagicMock):
    """
    A MagicMock subclass to mock Emoji objects.
    """

    spec_set = emoji_instance

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.guild = kwargs.get("guild", MockGuild())


reaction_instance = discord.Reaction(
    message=MockMessage(), data={"me": True}, emoji=MockEmoji()
)


class MockReaction(CustomMock, unittest.mock.MagicMock):
    """
    A MagicMock subclass to mock Reaction objects.
    """

    spec_set = reaction_instance

    def __init__(self, **kwargs) -> None:
        _users = kwargs.pop("users", [])
        super().__init__(**kwargs)
        self.emoji = kwargs.get("emoji", MockEmoji())
        self.message = kwargs.get("message", MockMessage())

        user_iterator = unittest.mock.AsyncMock()
        """Pepe 525, async iteration protocol"""
        user_iterator.__aiter__.return_value = _users
        self.users.return_value = user_iterator
        self.__str__.return_value = str(self.emoji)
