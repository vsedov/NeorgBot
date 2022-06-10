import threading
from typing import NewType

import discord
from discord.ext.commands import Cog, Context, command
from disputils import BotEmbedPaginator
from icecream import ic

from neorg.ext.search_info.__database_loader import FetchDatabase
from neorg.log import get_logger
from neorg.neorg import Neorg

log = get_logger(__name__)


def set_interval(interval: int) -> threading.Event:
    """
    Decorator Function, with internal wrapper: Set_interval, ammount of seconds
    you want to loop over a function.
    Decorator function, is used to sepcify what function is being parsed down
    """

    def decorator(function: NewType("DatabaseSearch.update_database", None)) -> threading.Event:
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
        self.bot = Neorg
        self.database_search = FetchDatabase()
        self.database_search.run_async()
        self.loop = self.update_database()

    #  TODO(vsedov) (14:25:06 - 10/06/22): This can break : If it does, create a class instead of function.
    @set_interval(259200)
    def update_database(self) -> None:
        """ Update Database, refreshes json file. """
        log.info(ic.format('updating database.'))
        self.database_search = FetchDatabase()
        self.database_search.run_async()

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

    @command()
    async def recent_update_db(self, ctx: Context) -> None:
        """searches most recently updated plugins / within the database."""
        pass


def setup(bot: Neorg) -> None:
    """
    Setup the database search cog.
    """
    bot.add_cog(DatabaseSearch(bot))
