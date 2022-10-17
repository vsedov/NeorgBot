import json

import discord
# yapf: disable
from discord.ext.commands import (
    BadArgument, CheckFailure, Cog, CommandNotFound, Context, MissingRequiredArgument, hybrid_command, has_any_role
)
# yapf: enable
from icecream import ic

from neorg import constants
from neorg.log import get_logger
from neorg.neorg import Neorg

log = get_logger(__name__)


class NeorgCreditMod(Cog):
    """Mod tools to manage the credit system."""

    def __init__(self, bot: Neorg):
        self.bot: Neorg = bot

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
                await ctx.send(embed=discord.Embed(description=error_message, colour=discord.Color.red()))

        log.warning(ic.format(f"{ctx.author} tried to run {ctx.command} but got {error}"))

    @hybrid_command()
    async def add_credit(self, ctx: Context, user: discord.Member, amount: int) -> None:
        """Add credits to a user."""
        await ctx.send(embed=discord.Embed(description=f"{user} has been given {amount} credits."))

        with open(constants.SOCIAL_CREDIT_FILE, "r") as f:
            social_credits = json.load(f)

        social_credits[str(user.id)]["norg_credit"] += amount

        with open(constants.SOCIAL_CREDIT_FILE, "w") as f:
            json.dump(social_credits, f)

    @hybrid_command()
    async def remove_credit(self, ctx: Context, user: discord.Member, amount: int) -> None:
        """Remove credits from a user."""

        with open(constants.SOCIAL_CREDIT_FILE, "r") as f:
            social_credits = json.load(f)

        social_credits[str(user.id)]["norg_credit"] -= amount

        with open(constants.SOCIAL_CREDIT_FILE, "w") as f:
            json.dump(social_credits, f)

        await ctx.send(embed=discord.Embed(description=f"{user} has been taken {amount} credits."))

    @hybrid_command()
    async def set_credit(self, ctx: Context, user: discord.Member, amount: int) -> None:
        """Set credits to a user."""

        with open(constants.SOCIAL_CREDIT_FILE, "r") as f:
            social_credits = json.load(f)

        social_credits[str(user.id)]["norg_credit"] = amount

        with open(constants.SOCIAL_CREDIT_FILE, "w") as f:
            json.dump(social_credits, f)

        await ctx.send(embed=discord.Embed(description=f"{user.display_name} has been given {amount} credits."))

    @hybrid_command()
    async def change_all(self, ctx: Context, user: discord.Member) -> None:
        """Changes norg_credit, norg_credit_level and norg_credit_xp."""

        with open(constants.SOCIAL_CREDIT_FILE, "r") as f:
            social_credits = json.load(f)

        await ctx.send(f"how much norg credit do you want to change, enter N to keep the same for {user.name}")
        norg_credit = await ctx.bot.wait_for("message", check=lambda m: m.author == ctx.author)
        if norg_credit.content == "N":
            norg_credit = social_credits[user.id]["norg_credit"]
        else:
            norg_credit = int(norg_credit.content)

        await ctx.send(f"How much do you want to change the xp to, enter N to keep the same for {user.name}")

        norg_credit_xp = await ctx.bot.wait_for("message", check=lambda m: m.author == ctx.author)
        if norg_credit_xp.content == "N":
            norg_credit_xp = social_credits[user.id]["norg_credit_xp"]
        else:
            norg_credit_xp = int(norg_credit_xp.content)

        await ctx.send(f"How much do you want to change the level to, enter N to keep the same for {user.name}")

        norg_credit_level = await ctx.bot.wait_for("message", check=lambda m: m.author == ctx.author)
        if norg_credit_level.content == "N":
            norg_credit_level = social_credits[user.id]["norg_credit_level"]
        else:
            norg_credit_level = int(norg_credit_level.content)

        social_credits[user.id]["norg_credit"] = norg_credit
        social_credits[user.id]["norg_credit_xp"] = norg_credit_xp
        social_credits[user.id]["norg_credit_level"] = norg_credit_level

        with open(constants.SOCIAL_CREDIT_FILE, "w") as f:
            json.dump(social_credits, f)

    @hybrid_command()
    async def set_xp(self, ctx: Context, user: discord.Member, amount: int) -> None:
        """Set xp to a user."""

        with open(constants.SOCIAL_CREDIT_FILE, "r") as f:
            social_credits = json.load(f)

        social_credits[str(user.id)]["norg_credit_xp"] = amount

        with open(constants.SOCIAL_CREDIT_FILE, "w") as f:
            json.dump(social_credits, f)

        await ctx.send(embed=discord.Embed(description=f"{user.display_name} has been given {amount} xp."))

    @hybrid_command()
    async def set_level(self, ctx: Context, user: discord.Member, amount: int) -> None:
        """Set level to a user."""

        with open(constants.SOCIAL_CREDIT_FILE, "r") as f:
            social_credits = json.load(f)

        social_credits[str(user.id)]["norg_credit_level"] = amount

        with open(constants.SOCIAL_CREDIT_FILE, "w") as f:
            json.dump(social_credits, f)

        await ctx.send(embed=discord.Embed(description=f"{user.display_name} has been given {amount} level."))


async def setup(bot: Neorg) -> None:
    """Load the cog."""
    await bot.add_cog(NeorgCreditMod(bot))
