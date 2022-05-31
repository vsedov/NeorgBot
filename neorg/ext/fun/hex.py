from discord import Embed
from discord.ext import commands
import re

class Hex(commands.Cog):
    """Show hex colors preview"""
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, mess) -> None:
        """
        Neorg: Hex color preview
        using: https://singlecolorimage.com/api.html
        Example :
            #986fec -> will get a color preview for this hex color.
            #000000 #ffffff -> will get color previews for both colors.
        NOTE: the message must start with the hex codes.
        """
        matched = re.search(r"^#[A-Fa-f0-9]{6}", mess.content)

        if matched:
            for hex in matched.string.split():
                em = Embed(description="", color=0x2f3136)
                url = f"https://singlecolorimage.com/get/{hex[1:]}/20x20"
                em.set_author(name=hex, icon_url=url)
                await mess.channel.send(embed=em)

def setup(bot):
    bot.add_cog(Hex(bot))

