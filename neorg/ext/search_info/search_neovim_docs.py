import re
from neorg import constants as c
from typing import Union

import discord
from discord.ext.commands import Cog, Context, hybrid_command

from neorg.fetch_info.neovim_docs import NeovimDocs
from neorg.log import get_logger
from neorg.neorg import Neorg
from neorg import constants as c

log = get_logger(__name__)


class NeovimDocSearch(Cog):
    """Neovim Documentation extension."""

    def __init__(self, bot: Neorg):
        self.bot = bot
        self.neovim = NeovimDocs()

    @hybrid_command()
    async def doc(self, ctx: Context, *, query: str = "api highlights") -> None:
        """
        Neovim Documentation
        To search
        `n.doc <query>|<amount>(optional)<accuracy>(optional)`
        query : tag link
        amount : how many return links do you want.
        example:
            n.doc highlight-guifg | 10 | 50%  - 10 items will be returned and items no under 50 % will be resulted
            n.doc nvim-config | 100% - will return items with 100 % with default settings
            n.doc nvim-config | 10 - return 10 items of 70 %
            n.doc nvim-config | 1 - return 1 item
            n.doc nvim-config | 10% - return 1 item of 10 % [ not a great idea]
        """
        # `n.doc <query>|<amount>(optional)<accuracy>(optional)`
        #  TODO(vsedov) (05:04:22 - 03/07/22): Find a better way around this
        regex = re.compile(r"\|")
        query_list = query.split("|") if regex.search(query) else [query]
        def filter_check(query: str) -> Union[int, int]:
            """
            Filter check will return the limit and percent if they are within the query

            Returns
            -------
                limit : integer or None
                percent: integer or None
            """
            limit_filter = re.compile(r"\d+")
            percent_filter = re.compile(r"\d+%")
            query = query.strip()
            limit = None
            percent = None
            if limit_filter.search(query):
                limit = int(limit_filter.search(query).group())
            if percent_filter.search(query):
                percent = int(percent_filter.search(query).group().replace("%", ""))
            return limit, percent

        query_limit, query_percent = filter_check(query)
        query_limit = 1 if query_limit is None else query_limit
        query_percent = 70 if query_percent is None else query_percent

        log.info(f"Query: {query_list}, Limit: {query_limit}, Percent: {query_percent}")
        docs = self.neovim.get_link(
            self.neovim.fuzzy_search_tags(search_term=query_list[0], limit=query_limit, cut_off_limit=query_percent))
        if len(docs) == 0:
            await ctx.send("No results found")
            return
        log.info(len(docs))
        #  TODO(vsedov) (09:59:15 - 03/07/22): Something wrong here, to fix.
        table = discord.Embed(title="Neovim Documentation", color=c.NORG_BLUE)
        table.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
        for doc in docs:
            table.add_field(name=doc[1], value=doc[0])
        await ctx.send(embed=table)


async def setup(bot: Neorg) -> None:
    """
    setup for NeovimDocSearch
    """
    await bot.add_cog(NeovimDocSearch(bot))
