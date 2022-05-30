import json

import discord
from discord.ext.commands import Cog, Context, command

from neorg import constants
from neorg.log import get_logger
from neorg.neorg import Neorg

log = get_logger(__name__)


class NorgCredit(Cog):
    """ Norg credit cog for public users."""

    def __init__(self, bot: Neorg):
        self.bot = bot

    @command()
    async def register(self, ctx: Context) -> None:
        """
        Register a user to the norg credit system.
        User can only register once and cannot deregister :kek:
        """
        with open(constants.SOCIAL_CREDIT_FILE, 'r') as f:
            data = json.load(f)

        keys = data.keys()
        log.info(keys)
        if str(ctx.author.id) in keys:
            await ctx.send("You are already registered.")
            return

        data[ctx.author.id] = {
            "norg_credit": 1000,
            "norg_credit_level": 1,
            "norg_credit_xp": 10,
        }

        with open(constants.SOCIAL_CREDIT_FILE, 'w') as f:
            json.dump(data, f, indent=4)

        await ctx.send("You have been registered.")

    @command()
    async def balance(self, ctx: Context) -> None:
        """Get your norg credit balance."""
        with open(constants.SOCIAL_CREDIT_FILE, 'r') as f:
            data = json.load(f)

        if data[str(ctx.author.id)] is None:
            log.info(f"{ctx.author.id} is not registered.")
            await ctx.send("You are not registered.")
            return

        # show all the information in a nice table
        em = discord.Embed(
            title="Norg Credit Balance",
            description=f"{ctx.author.mention}'s norg credit balance is {data[str(ctx.author.id)]['norg_credit']}",
            colour=discord.Colour.blue())
        for key, value in data[str(ctx.author.id)].items():
            em.add_field(name=key, value=value)
        await ctx.send(embed=em)

    @command()
    async def credit_help(self, ctx: Context) -> None:
        """
        Get information on how to get norg credit.
        """
        reply = "You can get credit by doing the following:\n"
        reply += "1. Register with `n.register`\n"
        reply += "2. Do `n.help` to get information on how to get norg credit\n"
        reply += "4. Just Keep talking in the server and you will get credit!\n"
        reply += "5. Your Credit Level is a multiplier, it will grow the longer you stay in the server\n"
        reply += "6. You can check your balance with `n.balance`\n"
        reply += "7. If you like java, you will get instant -10000 score :)\n"
        await ctx.send(embed=discord.Embed(title="Norg Credit Help", description=reply, colour=discord.Colour.purple()))

    @command(aliases=['lb', 'top'])
    async def leaderboard(self, ctx: Context) -> None:
        """
        Get the norg credit leaderboard.
        """
        with open(constants.SOCIAL_CREDIT_FILE, 'r') as f:
            data = json.load(f)

        data = sorted(data.items(), key=lambda x: x[1]['norg_credit'], reverse=True)
        reply = "```"
        for i in range(0, len(data)):
            reply += f"{i+1}. {self.bot.get_user(int(data[i][0])).name} - {data[i][1]['norg_credit']}\n"
        reply += "```"
        await ctx.send(reply)


def setup(bot: Neorg) -> None:
    """Add Cog to Bot."""
    bot.add_cog(NorgCredit(bot))
