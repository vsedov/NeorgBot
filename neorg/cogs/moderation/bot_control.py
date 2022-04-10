import logging

import discord
from discord.ext.commands import Cog, Context, command
from icecream import ic

from neorg.log import get_logger
from neorg.neorg import Neorg

log = get_logger(__name__)


class BotControl(Cog):
    """Moderation tools, to control the bot."""

    def __init__(self, bot: Neorg):
        self.bot = bot

    @command()
    async def shutdown(self, ctx: Context) -> None:
        """Shutdown the bot."""

        await ctx.send(embed=discord.Embed(description="Shutting down...", colour=discord.Color.red()))
        await self.bot.close()
        log.info("Bot shutdown.")

    @command()
    async def reload(self, ctx: Context, cog: str) -> None:  # noqa ignore
        """Reload a cog without restarting the bot."""
        if not cog:
            await ctx.send('Specify the cog to reload!')
            return
        try:
            #  TODO(vsedov) (18:32:18 - 10/04/22): Load modules using walk extension
            Neorg.unload_extension(cog)
            Neorg.load_extension(cog)
            await ctx.send(embed=discord.Embed(description=f"Cog **{cog}** reloaded", colour=discord.Color.red()))
        except Exception as ae:
            await ctx.send(ae)
            logging.warning(ic.format(f"{cog} could not be loaded"))


def setup(bot: Neorg) -> None:
    """Add Cog to Bot."""
    bot.add_cog(BotControl(bot))
