#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# File Name: neorg.py
import asyncio
import warnings

import discord
from discord.ext import commands
from icecream import ic
from sentry_sdk import push_scope

from neorg import constants
from neorg.log import get_logger

log = get_logger("norg")


class StartupError(Exception):
    """Exception class for startup errors."""

    def __init__(self, base: Exception):
        super().__init__()
        self.exception = base


class Neorg(commands.Bot):
    """
    Neorg events, these are called when the bot is ready and initalisation class
    """

    def __init__(self, *args, **kwargs):
        if "connector" in kwargs:
            warnings.warn(
                "If login() is called (or the bot is started), the connector will be overwritten "
                "with an internal one")

        super().__init__(*args, **kwargs)

    @classmethod
    def create(cls) -> "Neorg":
        """Create and return an instance of a Bot."""
        loop = asyncio.get_event_loop()
        intents = discord.Intents.all()
        intents.dm_typing = False
        intents.dm_reactions = False
        intents.invites = False
        intents.webhooks = False
        intents.integrations = False
        return cls(
            loop=loop,
            command_prefix=commands.when_mentioned_or(constants.Bot.prefex),
            activity=discord.Game(name=f"Commands: {constants.Bot.prefex}help"),
            case_insensitive=True,
            max_messages=10_000,
            intents=intents,
        )

    def load_cogs(self) -> None:
        """Load all cogs."""
        from neorg.utils.extensions import EXTENSIONS
        log.info(ic.format(EXTENSIONS))
        for extension in EXTENSIONS:
            try:
                self.load_extension(extension)
            except Exception as e:
                log.error(f"Failed to load extension {extension}", exc_info=e)

    def add_cog(self, cog: commands.Cog) -> None:
        """Add cog to the bot"""
        super().add_cog(cog)
        log.info(f"Cog loaded: {cog.qualified_name}")

    async def wait_till_ready(self) -> None:
        """Wait until the bot is ready."""
        await super().wait_till_ready()
        log.info("Bot is ready")
        await self.change_presence(status=discord.Status.online, activity=discord.Game('the prefix n. | n.help'))
        log.info("Bot is ready")

    async def on_error(self, event: str, *args, **kwargs) -> None:
        """Log errors using sentry to listen in also avoids console clogging up with stderr"""
        with push_scope() as scope:
            scope.set_tag("event", event)
            scope.set_extra("args", args)
            scope.set_extra("kwargs", kwargs)

            log.exception(f"Unhandled exception in {event}.")
