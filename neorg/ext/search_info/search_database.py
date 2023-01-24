import asyncio
import threading
from typing import NewType

import discord
import requests
from discord import Interaction
from discord.ext.commands import Cog, Context, hybrid_command
from icecream import ic

from neorg import constants as c
from neorg.ext.search_info.__database_loader import FetchDatabase
from neorg.log import get_logger
from neorg.neorg import Neorg
from neorg.utils.paginator import BotEmbedPaginator

log = get_logger(__name__)


def set_interval(interval: int) -> threading.Event:
    """
    Decorator Function, with internal wrapper: Set_interval, amount of seconds
    you want to loop over a function.
    Decorator function, is used to sepcify what function is being parsed down
    """

    def decorator(
        function: NewType("DatabaseSearch.update_database", None)
    ) -> threading.Event:
        """
        This is a function of what you want to be looped over a period of time : based on
        Interval.
        """

        def wrapper(*args, **kwargs) -> threading.Event:
            """Initiates threading event."""
            stopped = threading.Event()

            def loop() -> DatabaseSearch:  # executed in another thread
                """Starts the loop on specific function."""
                while not stopped.wait(interval):  # until stopped
                    function(*args, **kwargs)

            t = threading.Thread(target=loop)
            t.daemon = True  # stop if the program exits
            t.start()
            return stopped

        return wrapper

    return decorator


class DatabaseSearch(Cog):
    """Cog to search pnp database for all neovim plugins."""

    def __init__(self, bot: Neorg):
        self.bot = bot
        self.loop = self.update_database()
        self.database_search = FetchDatabase()

    #  TODO(vsedov) (14:25:06 - 10/06/22): This can break : If it does, create a class instead of function.
    @set_interval(259200)
    def update_database(self) -> None:
        self.database_search = FetchDatabase()

    @hybrid_command()
    async def search_db(self, ctx: Context, *, query: str = "neorg") -> None:
        """
        Search for a package in the database.
        """
        query = query.strip().lower()
        search_results = self.database_search.search_fuzzy(query)

        if not search_results:
            await ctx.send("No results found.")

        embeds = []
        for i in range(len(search_results)):
            name = search_results[i]["full_name"]
            em = discord.Embed(title=name, color=0x00FF00)
            for name, value in search_results[i].items():
                if name == "full_name":
                    continue
                em.add_field(name=name, value=value)
            embeds.append(em)

        if len(embeds) == 0:
            await ctx.send("No results found.")

        paginator = BotEmbedPaginator(embeds)

        inter = ctx.interaction
        if inter:
            await inter.channel.send(embed=embeds[0], view=paginator)

    @hybrid_command()
    async def recent_update_db(self, ctx: Context) -> None:
        """searches most recently updated plugins / within the database."""
        search_results = self.database_search.open_database()

        sorted_result = sorted(
            search_results.keys(),
            key=lambda test: search_results[test]["updated_at"],
            reverse=True,
        )

        embeds = []
        for i in range(0, 10):
            data = search_results[sorted_result[i]]
            em = discord.Embed(title=data["full_name"], color=0x00FF00)
            for name, value in data.items():
                if name == "full_name":
                    continue
                em.add_field(name=name, value=value)
            embeds.append(em)

        paginator = BotEmbedPaginator(embeds)
        await ctx.send(embed=embeds[0], view=paginator)

    @hybrid_command()
    async def random_db(self, ctx: Context) -> None:
        """Fetches a random plugin within the database."""
        data = requests.get("https://api.nvimplugnplay.repl.co/random").json()
        filt_vals = [
            "created_at",
            "updated_at",
            "default_branch",
            "language",
            "open_issues_count",
            "stargazers_count",
            "description",
        ]

        name, d = list(data.items())[0]
        em = discord.Embed(title=name, url=d["clone_url"], color=c.NORG_BLUE)

        for f in filt_vals:
            em.add_field(name=f, value=d[f])

        await ctx.send(embed=em)


async def setup(bot: Neorg) -> None:
    """
    Setup the database search cog.
    """

    await bot.add_cog(DatabaseSearch(bot))
