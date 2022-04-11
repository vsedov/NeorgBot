from discord.ext.commands import Cog
from youtubesearchpython import VideosSearch


class Youtube(Cog):
    """Youtube Extension, search for videos on youtube, and much more."""

    # def __init__(self, bot: discord.ext.commands.Bot):
    #     self.bot = bot

    def youtube(self, query: str = "star wars") -> None:
        """
        searches query from youtube, and fuzzy searches them using rapidfuzz.
        """
        # log.info(f"{ctx.author} searched for {query}")
        search = VideosSearch(query, limit=100)
        results = search.result()["result"]

        name_link = {i["title"]: i["link"]
                     for i in results}
        return name_link


# def setup(bot: commands.Bot) -> None:
#     """Add cog to bot."""
#     bot.add_cog(Youtube(bot))
