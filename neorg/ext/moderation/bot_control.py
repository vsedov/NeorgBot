import discord

# yapf: disable
from discord.ext.commands import (
    BadArgument, CheckFailure, Cog, CommandNotFound, Context, MissingRequiredArgument, command, has_any_role
)
# yapf: enable
from icecream import ic

from neorg import constants
from neorg.log import get_logger
from neorg.neorg import Neorg
from neorg.utils import extensions

log = get_logger(__name__)


class BotControl(Cog):
    """Moderation tools, to control the bot."""

    def __init__(self, bot: Neorg):
        self.bot = bot

    @command()
    async def shutdown(self, ctx: Context) -> None:
        """Shutdown the bot."""

        await ctx.send(
            embed=discord.Embed(
                description="Shutting down...", colour=discord.Color.red()
            )
        )
        await self.bot.close()
        if self.bot.is_closed():
            log.info(ic.format(f"{ctx.author} has shut down the bot."))
        else:
            log.warning(
                ic.format(f"{ctx.author} tried to shut down the bot but it failed.")
            )

        log.info("Bot shutdown.")

    @command()
    async def reload(self, ctx: Context, *, cog: str) -> None:
        """Reload a cog."""
        try:
            if cog == "all":
                for extension in extensions.EXTENSIONS:
                    self.bot.reload_extension(extension)
                await ctx.send(
                    embed=discord.Embed(
                        description="Reloaded all extensions.",
                        colour=discord.Color.green(),
                    )
                )
                return

            ext_name = extensions.find_extension(cog)
            if ext_name is None:
                raise CommandNotFound(f"Extension {cog} not found.")
            self.bot.reload_extension(ext_name)
            await ctx.send(
                embed=discord.Embed(
                    description=f"Reloaded extension {cog}.",
                    colour=discord.Color.green(),
                )
            )
        except Exception as e:
            await ctx.send(
                embed=discord.Embed(
                    description=f"Failed to reload extension {cog}.",
                    colour=discord.Color.red(),
                )
            )
            log.error(ic.format(f"Failed to reload extension {cog}."))
            log.error(ic.format(e))

    async def cog_check(self, ctx: Context) -> bool:
        """Only allow moderators to invoke the commands in this cog."""
        return await has_any_role(*constants.MODERATION_ROLES).predicate(ctx)

    async def cog_command_error(self, ctx: Context, error: Exception) -> None:
        """Cog Role error, if not mod or admin, output will output and error."""
        error_dict = {
            CommandNotFound: "Command not found.",
            CheckFailure: "You do not have permission to run this command.",
            MissingRequiredArgument: "You are missing a required argument.",
            BadArgument: "You have provided an invalid argument.",
        }

        for error_type, error_message in error_dict.items():
            if isinstance(error, error_type):
                await ctx.send(
                    embed=discord.Embed(
                        description=error_message, colour=discord.Color.red()
                    )
                )

        log.warning(
            ic.format(f"{ctx.author} tried to run {ctx.command} but got {error}")
        )


def setup(bot: Neorg) -> None:
    """Add Cog to Bot."""
    bot.add_cog(BotControl(bot))
