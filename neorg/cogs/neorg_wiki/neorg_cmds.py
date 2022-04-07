import re

import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import commands
from icecream import ic

from neorg.log import get_logger

log = get_logger(__name__)


class NeorgCmd(commands.Cog):
    """
    NeorgCmd custom call to inspect neorg wiki, Using beautiful soup to webscrap
    Neorgs github wiki page to retreive links
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def wiki(self, ctx, *, query):
        """Neorg Wiki search handle to search neorg wiki for query
        n.wiki <query>

        Parameters
        ----------
        ctx : discord.ext.commands.Context
            discord context object allowing access to the message object
        query : Query taken from message after command
            a query to search the wiki to be search through

        """
        query = query.strip().lower().replace(' ', '-')
        neorg_wiki = {}
        wiki_url = "https://github.com/nvim-neorg/neorg/wiki"

        stuff = BeautifulSoup(requests.get(wiki_url).text, 'lxml')
        lis = stuff.find_all("div", {"class": "Box-body wiki-custom-sidebar markdown-body"})[0]

        for li in lis.find_all('li'):
            if li.a is None:
                continue

            part = li.a['href']
            #  TODO(vsedov) (13:39:53 - 06/04/22): remove hardcode
            neorg_wiki[part[37:].lower()] = part

        wiki = [neorg_wiki[k] for k in neorg_wiki.keys() if query in k.lower()]
        log.debug(ic.format(wiki))

        if len(wiki) == 0:
            await ctx.send(embed=discord.Embed(description="No Results Found!", colour=0x4878BE))
            return
        for i in wiki:
            em = discord.Embed(description=i, colour=0x4878BE)
            await ctx.send(embed=em)

    @commands.command()
    async def spec(self, ctx, *, query):
        """Spec search handle to search neorg spec for query
        n.spec <query>
        Similar to n.wiki but for spec files
        """
        query = query.strip().lower().replace(' ', '-')
        url = "https://raw.githubusercontent.com/nvim-neorg/neorg/main/docs/NFF-0.1-spec.md"
        og_url = "https://github.com/nvim-neorg/neorg/blob/main/docs/NFF-0.1-spec.md"

        soup = re.findall(r"\[(.+)\]\((.+)\)", requests.get(url).text[:1500])
        neorg_specs = {}

        for k, v in soup:
            neorg_specs[k.lower().replace(' ', '-')] = og_url + v

        spec = [neorg_specs[k] for k in neorg_specs.keys() if query in k.lower()]

        if len(spec) == 0:
            await ctx.send(embed=discord.Embed(description="No Results Found!", colour=0x4878BE))
            return

        for i in spec:
            em = discord.Embed(description=i, colour=0x4878BE)
            await ctx.send(embed=em)

    @commands.command(aliases=["norg"])
    async def neorg(self, ctx):
        """Fetch the Neorg repository"""
        await ctx.send("Neorg - https://github.com/nvim-neorg/neorg")


def setup(bot):
    bot.add_cog(NeorgCmd(bot))
