#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# File Name: neorg.py
import asyncio
import logging
import os

import discord
import pyinspect as pi
from discord.ext import commands
from icecream import ic

from .log import get_logger

log = get_logger("norg")
LOCALHOST = "127.0.0.1"


class StartupError(Exception):
    """Exception class for startup errors."""

    def __init__(self, base: Exception):
        super().__init__()
        self.exception = base

class Norg(commands.Bot):
    """A subclass of discord.ext.command.Bots where aiohttp session and api client will be called."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #  TODO(vsedov) (05:11:05 - 06/04/22): use aiohttp for client for http addr

    @classmethod
    def create(cls) -> "Neorg":
        "Create and return a instance of Neorg bot"
        loop = asyncio.get_event_loop()
        return cls(
            #  TODO(vsedov) (05:13:45 - 06/04/22): Call from global file called constants
            command_prefix=commands.when_mentioned_or("n!"),
            description="Neorg",
            loop=loop,
            intents=discord.Intents.all())


client = commands.Bot(command_prefix=['n.', 'N.'])

extensions = ['cogs.help', 'cogs.neorg_cmds', 'cogs.general']
def client_load_extensions():
    for e in extensions:
        logging.info(ic.format("loading extension: {}", e))
        client.load_extension(e)

@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.online, activity=discord.Game('the prefix n. | n.help'))
    logging.info(ic.format("logged in as: {}", client.user))

@client.command(aliases=['r'])
async def reload(ctx, cog):
    """ reload cogs

    Parameters
    ----------
    ctx : ctx : discord.ext.commands.Context
        The context of the command
    cog : Cog : discord.ext.commands.Cog
        external modules to reload

    Returns
    -------
    None
    """
    if not cog:
        await ctx.send('Specify the cog to reload!')
        return
    try:
        client.unload_extension(f'cogs.{cog}')
        client.load_extension(f'cogs.{cog}')
        await ctx.send(
            embed=discord.Embed(
                description=f"Cog **{cog}** reloaded", colour=discord.Color.red()))
        # this is a hack to reload the cog without restarting the bot
    except Exception as ae:
        await ctx.send(ae)
        logging.warning(ic.format(f"{cog} could not be loaded"))

if __name__ == "__main__":
    pi.install_traceback(enable_prompt=True)
    hosting.keep_running()
    __import__("dotenv").load_dotenv()
    client_load_extensions()
    client.run(os.environ['TOKEN'])
