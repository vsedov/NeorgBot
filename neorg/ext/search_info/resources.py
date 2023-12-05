from neorg import constants as c
import discord
from discord.ext.commands import Cog, Context, hybrid_command
from neorg.neorg import Neorg
from neorg import constants as c
from requests import get

class Resources(Cog):
    def __init__(self, bot: Neorg):
        self.bot = bot
        # self.titles = self.fetch_tuts()

    # def fetch_tuts(self):
        # sauce = get("https://raw.githubusercontent.com/pysan3/Norg-Tutorial/main/norg_tutorial.md").text
        # return [line.replace("#", "").strip() for line in sauce.split('\n') if line.startswith("#")]

    @hybrid_command()
    async def resource(self, ctx: Context, *, tutorial: str = "", pandoc: str = "", lsp: str = "") -> None:
        """
        List of resources. Currently only works for tutorial.
        Example: /resource tutorial: table-syntax
        """
        target_url = ""
        if tutorial:
            target_url = "https://github.com/pysan3/Norg-Tutorial/blob/main/norg_tutorial.md"
        elif pandoc:
            target_url = "https://github.com/boltlessengineer/norg-pandoc"
        else:
            target_url = "https://github.com/nvim-neorg/neorg"

        target_url = f"{target_url}#{'-'.join(tutorial.split())}" if tutorial else target_url
        em = discord.Embed(description=target_url, color=c.NORG_BLUE)
        em.set_footer(icon_url=ctx.author.avatar, text=ctx.author)
        await ctx.reply(embed=em)


        # if tutorial:
            # target_url = "https://github.com/pysan3/Norg-Tutorial/blob/main/norg_tutorial.md"
            # sections = [title for title in self.titles if "-".join(tutorial.split()) in title]
            # if len(sections) < 1:
                # await ctx.reply("Found no resources matching the query.")
                # return

            # items = [f"- [{section}]({target_url}#{section})" for section in sections]
            # em = discord.Embed(description="\n".join(items), color=c.NORG_BLUE)
            # # em.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
            # await ctx.reply(embed=em)

        # if pandoc:
            # await ctx.reply(embed=discord.Embed(description="https://github.com/boltlessengineer/norg-pandoc", color=c.NORG_BLUE))


async def setup(bot: Neorg) -> None:
    await bot.add_cog(Resources(bot))
