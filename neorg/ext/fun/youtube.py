import re

import discord
from discord.ext.commands import Cog, Context, hybrid_command
from icecream import ic

from neorg.ext.fun._youtube import Youtube
from neorg.log import get_logger

log = get_logger(__name__)


class YoutubeSearch(Cog):
    """Youtube Module for searching videos."""

    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot = bot
        self.youtube = Youtube()

    @hybrid_command()
    async def search(self, ctx: Context, *, query: str = "rick roll never going to give you up|1  ") -> None:
        """
        Neorg: Youtub Search
        To Search:
        `n.neorg search <query>|<ammont>`
        For example :
            n.neorg search rick roll -> will search 1 video by default
            n.neorg search rick roll|5 -> will provide a table of 5 videos
            n.neorg search star wars|3 -> will provide a table of 3 videos
            n.neorg search test -> will search 1 video by default
        """
        log.info(query)
        regex = re.compile(r"\|")

        if regex.search(query):
            query, limit = query.split("|")
            limit = int(limit)
        else:
            limit = 1

        log.info(ic.format(f"Searching {query} | {limit}"))

        search = self.youtube.get_video(query, limit)

        link = "https://www.youtube.com/watch?v="
        valid = list(search.values())[0]
        if len(valid) == 1:
            id = valid[0]["id"]
            title = valid[0]["title"]
            link += id
            embed = discord.Embed(title=title, url=link)
            embed.set_thumbnail(url=valid[0]["thumbnails"][0]["url"])
            embed.set_footer(text=f"Requested by {ctx.author.name}")
            await ctx.send(embed=embed)
        else:
            table = discord.Embed(title="Youtube Search")
            table.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            table.set_footer(text=f"Requested by {ctx.author.name}")

            for video in valid:
                id = video["id"]
                title = video["title"]
                link += id
                table.add_field(name=title, value=link)

                table.set_thumbnail(url=valid[0]["thumbnails"][0]["url"])
            await ctx.send(embed=table)


async def setup(bot: discord.ext.commands.Bot) -> None:
    """Add cog to bot."""
    await bot.add_cog(YoutubeSearch(bot))
