import discord
from discord.ext.commands import Cog, Context, command

from neorg.fetch_info.fetch_from_awesome import ReadAwesome
from neorg.log import get_logger
from neorg.neorg import Neorg

log = get_logger(__name__)


class AwesomeSearch(Cog):
    """Search for a plugin in awesome."""

    def __init__(self, bot: Neorg):
        self.bot = Neorg
        self.awesome = ReadAwesome()

    @command()
    async def awesome_search(self, ctx: Context, *, query: str = "neorg") -> None:
        """Active search for plugins on awesome-neorg."""
        query = query.strip().lower()
        search_result = self.awesome.fuzzy(query)
        em = discord.Embed(title="Search result", color=0x00ff00)

        for result in search_result.items():
            link = f"https://github.com/{result[1]}"
            em.add_field(name=result[0], value=f"{result[1]}, {link}", inline=False)
        await ctx.send(embed=em)

    @command()
    async def recent_plugin(self, ctx: Context) -> None:
        """Get most recent plugins added."""
        recent_plugins = self.awesome.get_most_recent_plugin()
        em = discord.Embed(title="Recent Plugins", color=0x00ff00)
        for i, plugin in enumerate(recent_plugins):
            link = f"https://github.com/{plugin}"
            em.add_field(name=plugin, value=link, inline=False)
            log.info(f"{i+1}: {plugin}")
        await ctx.send(embed=em)


def setup(bot: Neorg) -> None:
    """Set up the extension."""
    bot.add_cog(AwesomeSearch(bot))
