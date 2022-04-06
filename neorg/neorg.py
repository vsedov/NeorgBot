#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# File Name: neorg.py
import asyncio
import logging
import warnings

import constants
import discord
from discord.ext import commands
from icecream import ic
from log import get_logger

log = get_logger("norg")
LOCALHOST = "127.0.0.1"

class StartupError(Exception):
    """Exception class for startup errors."""

    def __init__(self, base: Exception):
        super().__init__()
        self.exception = base

class Neorg(commands.Bot):

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
            command_prefix=commands.when_mentioned_or(constants.Neorg.prefex),
            activity=discord.Game(name=f"Commands: {constants.Neorg.prefex}help"),
            case_insensitive=True,
            max_messages=10_000,
            allowed_mentions=discord.AllowedMentions(
                everyone=False, roles=constants.MODERATION_ROLES),
            intents=intents,
        )

    def load_cogs(self) -> None:
        """Load all cogs."""
        from utils.extensions import EXTENSIONS
        print(EXTENSIONS)
        for extension in EXTENSIONS:
            try:
                self.load_extension(extension)
            except Exception as e:
                log.error(f"Failed to load extension {extension}", exc_info=e)

    def add_cog(self, cog: commands.Cog) -> None:
        super().add_cog(cog)
        log.info(f"Cog loaded: {cog.qualified_name}")

    async def wait_till_ready(self) -> None:
        """Wait until the bot is ready."""
        await super().wait_till_ready()
        log.info("Bot is ready")
        await self.change_presence(
            status=discord.Status.online, activity=discord.Game('the prefix n. | n.help'))
        log.info("Bot is ready")

    @commands.command(name="reload")
    async def reload(self, ctx, cog):
        if not cog:
            await ctx.send('Specify the cog to reload!')
            return
        try:
            self.unload_extension(f'cogs.{cog}')
            self.load_extension(f'cogs.{cog}')
            await ctx.send(
                embed=discord.Embed(
                    description=f"Cog **{cog}** reloaded", colour=discord.Color.red()))
            # this is a hack to reload the cog without restarting the bot
        except Exception as ae:
            await ctx.send(ae)
            logging.warning(ic.format(f"{cog} could not be loaded"))
