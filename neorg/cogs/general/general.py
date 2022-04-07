import discord
from discord.ext import commands

class General(commands.Cog):
    """General Commansd and event inspection"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        """on message listens to events and messages on server and puts sus as a reaction"""
        if 'sus' in message.content.lower():
            await message.add_reaction("<:sus:867395030988881921>")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """on raw reaction add listens to events and checks payload. it checks if a message has a reaction.

        Parameters
        ----------
        payload : discord.RawReactionActionEvent
            The payload of the event.
        """
        if payload.emoji.name in '📑🔖':
            msg = await self.bot.get_channel(payload.channel_id
                                            ).fetch_message(payload.message_id)
            author = msg.author

            if msg.content != "":
                bookmark = discord.Embed(description=msg.content, colour=0x4878BE)
                bookmark.set_author(name=author.name, icon_url=author.avatar_url)
                user = await self.bot.fetch_user(payload.user_id)
                await user.send(embed=bookmark)

def setup(bot):
    bot.add_cog(General(bot))
