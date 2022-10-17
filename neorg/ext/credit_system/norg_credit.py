import asyncio
import json

import discord
from discord.ext.commands import Cog, Context, hybrid_command

from neorg import constants
from neorg.log import get_logger
from neorg.neorg import Neorg

log = get_logger(__name__)


class NorgCredit(Cog):
    """ Norg credit cog for public users."""

    def __init__(self, bot: Neorg):
        self.bot = bot

    @hybrid_command()
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
            "norg_credit": 1000,  # ammountj
            "norg_credit_level": 1,  # scalar value
            "norg_credit_xp": 10,  # xp
        }

        with open(constants.SOCIAL_CREDIT_FILE, 'w') as f:
            json.dump(data, f, indent=4)

        await ctx.send("You have been registered.")

    @hybrid_command()
    async def balance(self, ctx: Context, user: discord.Member = None) -> None:
        """Get your norg credit balance."""
        with open(constants.SOCIAL_CREDIT_FILE, 'r') as f:
            data = json.load(f)

        if user is None:
            user = ctx.author

        if data[str(user.id)] is None:
            log.info(f"{user.id} is not registered.")
            await ctx.send("You are not registered.")
            return

        # show all the information in a nice table
        em = discord.Embed(
            title="Norg Credit Balance",
            description=f"{user.mention}'s norg credit balance is {data[str(user.id)]['norg_credit']}",
            colour=discord.Colour.blue())
        for key, value in data[str(user.id)].items():
            em.add_field(name=key, value=value)
        await ctx.send(embed=em)

    @hybrid_command()
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

    @hybrid_command()
    async def leaderboard(self, ctx: Context) -> None:
        """
        Get the norg credit leaderboard.
        """
        with open(constants.SOCIAL_CREDIT_FILE, 'r') as f:
            data = json.load(f)

        data = sorted(data.items(), key=lambda x: x[1]['norg_credit'], reverse=True)
        reply = discord.Embed(title="Norg Credit Leaderboard", colour=discord.Colour.blue())
        for i in range(0, len(data)):
            reply.add_field(
                name=f"{i+1}. {self.bot.get_user(int(data[i][0])).name}", value=data[i][1]['norg_credit'], inline=False)
        await ctx.send(embed=reply)

    @hybrid_command()
    async def praise(self, ctx: Context, user: discord.Member) -> None:
        """Praise another user"""

        with open(constants.SOCIAL_CREDIT_FILE, 'r') as f:
            data = json.load(f)

        if data[str(ctx.author.id)] is None or data[str(user.id)] is None:
            log.info(f"{ctx.author.id} is not registered.")
            await ctx.send("You are not registered.")
            return

        if str(ctx.author.id) == str(user.id):
            await ctx.send("You cannot praise yourself.")
            return

        # ask how much credit to give
        await ctx.send(f"How much norg credit do you want to give to {user.name}?")

        def check(msg: discord.Message) -> bool:
            """Check if message is a valid number."""
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.isdigit()

        try:
            msg = await self.bot.wait_for('message', check=check, timeout=10)
        except asyncio.TimeoutError:
            return

        msg = int(msg.content)

        if msg <= 0:
            await ctx.send("Please enter a positive number.")
            return

        # check if user has enough credit
        if msg > data[str(ctx.author.id)]['norg_credit']:
            await ctx.send("You do not have enough norg credit.")
            return

        # give credit to user
        data[str(ctx.author.id)]['norg_credit'] -= msg
        data[str(user.id)]['norg_credit'] += msg

        with open(constants.SOCIAL_CREDIT_FILE, 'w') as f:
            json.dump(data, f, indent=4)

        await ctx.send(f"You have given {msg} norg credit to {user.name}.")

    @Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        """The longer a user is in the server the higher their credit xp will be. """

        with open(constants.SOCIAL_CREDIT_FILE, 'r') as f:
            data = json.load(f)

        if message.author.bot or str(message.author.id) not in data.keys():
            return

        # lol fuck it, if you talk about java even if you say its shit, it will reduce 1 :kekw:
        if any(word in message.content.lower() for word in constants.NEGATIVE_WORDS):
            data[str(message.author.id)]['norg_credit_xp'] -= 100

        # increase xp and level and credit based on how much the user tpes in the server
        data[str(message.author.id)]['norg_credit_xp'] += data[str(message.author.id)]['norg_credit_level']
        data[str(message.author.id)]['norg_credit'] += data[str(message.author.id)]['norg_credit_level']

        # you level up ever 10,000 xp
        # every time they level up, increase credit_level by 1 you level up when credit is divisable by 10,000
        if data[str(message.author.id)]['norg_credit'] % 10000 == 0:
            data[str(message.author.id)]['norg_credit_level'] += 1
            await message.channel.send(
                f"{message.author.mention} has leveled up to level {data[str(message.author.id)]['norg_credit_level']}!"
            )

        with open(constants.SOCIAL_CREDIT_FILE, 'w') as f:
            json.dump(data, f, indent=4)


async def setup(bot: Neorg) -> None:
    """Add Cog to Bot."""
    await bot.add_cog(NorgCredit(bot))
