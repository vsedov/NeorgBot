import discord
from discord.ext.commands import Cog, Context, command

from neorg.log import get_logger

log = get_logger(__name__)


class FunListen(Cog):
    """General Commansd and event inspection"""

    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot = bot
        self.reaction_id = {
            "sus": "<:sus:867395030988881921>",
            "neorg": "<:neorg:949327974442889277>",
            "are you dumb": "<:reee:948636504224329759>",
        }
        self.send_message_id = {
            "rtfm": "<:RTFM:945925360028090368>",
        }

    @Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        """
        If message is in reaction id then react with the corresponding reaction
        else if itse in message id then send it instead.
        """

        def generate_list(list_type: list[str]) -> list:
            """Generate_list, creats a list based on the filter of the content and list_type

            Parameters
            ----------
            list_type : list[str]
                list_type is either self.reaction_id or self.send_message_id

            Returns
            -------
            list
                new list that is filtered of the keys and values that are required for the output
            """
            return list(filter(lambda x: x in message.content.lower(), list_type))

        reaction_call = generate_list(self.reaction_id)
        send_call = generate_list(self.send_message_id)

        for emoji in reaction_call:
            await message.add_reaction(self.reaction_id[emoji])

        for emoji in send_call:
            await message.channel.send(self.send_message_id[emoji])

    @Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent) -> None:
        """on raw reaction add listens to events and checks payload. it checks if a message has a reaction.

        Parameters
        ----------
        payload : discord.RawReactionActionEvent
            The payload of the event.
        """
        if payload.emoji.name in "📑🔖":
            msg = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            author = msg.author

            if msg.content != "":
                bookmark = discord.Embed(description=msg.content, colour=0x4878BE)
                bookmark.set_author(name=author.name, icon_url=author.avatar_url)
                user = await self.bot.fetch_user(payload.user_id)
                await user.send(embed=bookmark)

    @command(name="ping", brief="Get the bot's ping")
    async def ping(self, ctx: Context) -> None:
        """Get the bot's ping"""
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    @command(name="sus", aliases=["susy"])
    async def sus(self, ctx: Context) -> None:
        """sus command"""
        await ctx.send(self.reaction_id["sus"])


def setup(bot: discord.ext.commands.Bot) -> None:
    """Add cog to bot."""
    bot.add_cog(FunListen(bot))
