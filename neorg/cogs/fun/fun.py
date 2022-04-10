import discord
from discord.ext.commands import Cog

from neorg.log import get_logger

log = get_logger(__name__)


class FunListen(Cog):
    """General Commansd and event inspection"""

    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        """on message listens to events and messages on server and puts sus as a reaction"""
        if 'sus' in message.content.lower():
            await message.add_reaction("<:sus:867395030988881921>")

    @Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent) -> None:
        """on raw reaction add listens to events and checks payload. it checks if a message has a reaction.

        Parameters
        ----------
        payload : discord.RawReactionActionEvent
            The payload of the event.
        """
        if payload.emoji.name in '📑🔖':
            msg = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            author = msg.author

            if msg.content != "":
                bookmark = discord.Embed(description=msg.content, colour=0x4878BE)
                bookmark.set_author(name=author.name, icon_url=author.avatar_url)
                user = await self.bot.fetch_user(payload.user_id)
                await user.send(embed=bookmark)


def setup(bot: discord.ext.commands.Bot) -> None:
    """Add cog to bot."""
    bot.add_cog(FunListen(bot))
    log.info("Cog loaded: FunListen")
