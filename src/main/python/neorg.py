#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# File Name: neorg.py
import logging
import os

import discord
import hosting
import pyinspect as pi
from discord.ext import commands
from icecream import ic
from rich.logging import RichHandler

root = logging.getLogger()
if root.handlers:
    for h in root.handlers:
        root.removeHandler(h)()

FORMAT = "%(message)s"
logging.basicConfig(level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])

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
