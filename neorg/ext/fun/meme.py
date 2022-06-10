from discord import Embed
from discord.ext import commands
from requests import get
from requests.models import Response


class Meme(commands.Cog):
    """Random Memes from reddit."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(aliases=["memes"])
    async def meme_test(self, ctx: commands.Context, *, sub: str = '') -> None:
        """
        Neorg: Reddit memes
        using: https://github.com/D3vd/Meme_Api
        Example :
            n.meme -> will get a meme from a random subreddit
            n.meme dankmemes -> will get a meme from the `dankmemes` subreddit
        """

        sauce: Response = get(f"https://meme-api.herokuapp.com/gimme/{sub}")
        if sauce.status_code != 200:
            await ctx.send(embed=Embed(description="Could not get the meme.", color=0x4878BE))
            return

        data = sauce.json()
        if data["nsfw"]:
            await ctx.send(embed=Embed(description="This meme is NSFW.", color=0x4878BE))
            return

        title: str = data["title"]
        sub = data["subreddit"]
        img = data["url"]
        ups = data["ups"]

        em = Embed(title=title, color=0x2f3136).set_image(url=img).set_footer(text=f" 👍{ups}  | r/{sub}")  # 0x4878BE
        await ctx.send(embed=em)


def setup(bot: commands.Bot) -> None:
    """Add cog to bot."""
    bot.add_cog(Meme(bot))
