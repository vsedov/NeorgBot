from discord import Embed
from discord.ext import commands
from requests import get
from requests.models import Response
from neorg import constants as c


# TODO: add support for non-github repos
class Loc(commands.Cog):
    """Number of lines for a github repo."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command()
    async def loc(self, ctx: commands.Context, *, repo=None) -> None:
        """
        Neorg: Lines of code for a repo
        using: codetabs.com api
        Example :
            n.loc -> will get loc info for neorg repo
            n.loc username/repo -> will get loc for github.com/username/repo
        """

        repo = repo or 'nvim-neorg/neorg'
        url = f"https://api.codetabs.com/v1/loc/?github={repo}"
        sauce: Response = get(url)

        if sauce.status_code == 200:
            res = "".join(
                f"***{lang['language']}***: {lang['linesOfCode']}\n"
                for lang in sauce.json()
            )
            await ctx.send(embed=Embed(title=f":man_mage: LOC for __***{repo}***__ :man_mage:", description=res, color=c.NORG_BLUE))
        elif 'Error' in sauce.json().keys():
            msg = sauce.json()['Error']
            await ctx.send(embed=Embed(description=msg, color=c.NORG_BLUE))
        else:
            await ctx.send(embed=Embed(description="Could not get repo details.", color=c.NORG_BLUE))

async def setup(bot: commands.Bot) -> None:
    """Add cog to bot."""
    await bot.add_cog(Loc(bot))
