import asyncio
import re

import discord
import requests
from discord.ext.commands import Cog, Context, command
from rapidfuzz import fuzz, process

from neorg.log import get_logger

log = get_logger(__name__)


class FunListen(Cog):
    """General Commansd and event inspection"""

    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        """on message listens to events and messages on server and puts sus as a reaction"""
        if 'sus' in message.content.lower():
            await message.add_reaction("<:sus:867395030988881921>")

    @Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent) -> None:
        """on raw reaction add listens to events and checks payload. it checks if a message has a reaction.

        Parameters
        ----------
        payload : discord.RawReactionActionEvent
            The payload of the event.
        """
        if payload.emoji.name in '📑🔖':
            msg = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            author = msg.author

            if msg.content != "":
                bookmark = discord.Embed(description=msg.content, colour=0x4878BE)
                bookmark.set_author(name=author.name, icon_url=author.avatar_url)
                user = await self.bot.fetch_user(payload.user_id)
                await user.send(embed=bookmark)

    @command(name="youtube", aliases=["yt"], brief="Search for a youtube video")
    async def youtube(self, ctx: Context, *, query: str) -> None:
        """Search for a youtube video and send list of results,
        user can choose one to play. by reacting to the message
        with the corresponding number. if no number is given, the first result is played. """

        url = "https://www.youtube.com/results?search_query="

        url_list = []
        with requests.get(url + query) as response:
            regex = '/watch\?v\=(.*?)\"'  # noqa: ignore
            match = re.findall(regex, response.text)[0]
            fuzzy_matches = process.extract(query, match, scorer=fuzz.token_set_ratio, limit=5, score_cutoff=20)

            option_list = {
                "https://www.youtube.com/watch?v=" + match: "Perfect Match"
            }
            for i in fuzzy_matches:
                option_list["https://www.youtube.com/watch?v=" + i[0]] = i[1]

        embed = discord.Embed(title="YouTube Search", description=query, colour=0xFF0000)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        if len(option_list) == 1:
            embed.add_field(name="Result", value=option_list.popitem()[0])
        else:
            for i, (url, score) in enumerate(option_list.items()):
                url_list.append(url)
                embed.add_field(name=f"Option {i+1}", value=f"{url}\n{score}% Match")
        if len(url_list) == 1:
            await ctx.send(embed=embed)
            return

        # need to add more server emojis for this to work .
        reaction_list = ["<:sus:867395030988881921>", "🔖", "📑", "🔙", "🔙"]

        # 5 total ractions based on max search results
        def check(reaction: discord.Reaction, user: discord.User) -> bool:
            """Check reaction to emoji, based if it within the reaction list. """
            return user == ctx.author and str(reaction.emoji) in reaction_list

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            return await ctx.send("Timed out.")

        url = url_list[reaction_list.index(str(reaction.emoji))]

        await ctx.send(embed=discord.Embed(title="Playing", description=url, colour=0x00FF00))

    @command(name='sus', aliases=['susy'])
    async def sus(self, ctx: Context) -> None:
        """sus command"""
        await ctx.send("<:sus:867395030988881921>")


def setup(bot: discord.ext.commands.Bot) -> None:
    """Add cog to bot."""
    bot.add_cog(FunListen(bot))
