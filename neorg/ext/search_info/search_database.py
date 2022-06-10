import time

import discord
from discord.ext.commands import Cog, Context, command
from disputils import BotEmbedPaginator

from neorg.ext.search_info.__database_loader import FetchDatabase
from neorg.log import get_logger
from neorg.neorg import Neorg

log = get_logger(__name__)


class DatabaseSearch(Cog):
    """Cog to search pnp database for all neovim plugins."""

    def __init__(self, bot: Neorg):
        self.bot = Neorg
        self.database_search = FetchDatabase()

    # make a function that will call FetchDatabase()() to update the database every three days
    # maybe use a listner ?

    @Cog.listener()
    def on_ready(self) -> None:
        """Update the database every three days."""
        while True:
            time.sleep(259200)  # 259200 seconds = 3 days
            self.database = FetchDatabase()
            #  TODO(vsedov) (13:38:59 - 10/06/22): This is beyond scuffed find a better way of doing this.
            self.database.run_async()

    @command()
    async def db_search(self, ctx: Context, *, query: str = "neorg") -> None:
        """
        Search for a package in the database.
        """
        query = query.strip().lower()
        search_results = self.database_search.search_fuzzy(query)
        if not search_results:
            await ctx.send("No results found.")
            return
        embeds = []
        for i in range(len(search_results)):

            name = search_results[i]["full_name"]
            em = discord.Embed(title=name, color=0x00ff00)
            for name, value in search_results[i].items():
                if name == "full_name":
                    continue
                em.add_field(name=name, value=value)
            embeds.append(em)

        paginator = BotEmbedPaginator(ctx, embeds)
        await paginator.run()


def setup(bot: Neorg) -> None:
    """
    Setup the database search cog.
    """
    bot.add_cog(DatabaseSearch(bot))
