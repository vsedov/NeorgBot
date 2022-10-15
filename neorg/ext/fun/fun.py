import discord
from discord.ext.commands import Cog, Context, hybrid_command

from neorg.log import get_logger

log = get_logger(__name__)


class FunListen(Cog):
    """General Commands and event inspection"""

    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot = bot
        self.reaction_types = {
            "ree": "<:reee:948636504224329759>",
            "sus": "<:sus:867395030988881921>",
            "neorg": "<:neorg:949327974442889277>",
            "based": "<:based:946814517566930954>",
            "troll": "<:trollar:968455084604276816>",
        }
        self.reaction_id = {
            "sus": self.reaction_types["sus"],
            "neorg": self.reaction_types["neorg"],
            "based": self.reaction_types["based"],
            "troll": self.reaction_types["troll"]
        }

        self.reaction_id_normalizer(["dumb", "idiot", "stupid", "moron", "dumbass"], "ree")

        self.send_message_id = {
            "rtfm": "<:RTFM:945925360028090368>",
        }

    def reaction_id_normalizer(self, list_of_words: list[str], type: str) -> None:
        """reaction id normaliser allows reduce reptetion of code, we use this if a emoji is used more than once.
        this needs to be called within the init method.

        Parameters
        ----------
        list_of_words : list[str]
            list of words, this can be a hard coded list or something from the constants file.
        type : str
            str type needs to be a key from the reaction_types dictionary.
        """
        for word in list_of_words:
            self.reaction_id[word] = self.reaction_types[type]

    @Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        """
        If message is in reaction id then react with the corresponding reaction
        else if itse in message id then send it instead.
        """

        def generate_list(list_type: list[str]) -> list:
            """Generate_list, creates a list based on the filter of the content and list_type

            Parameters
            ----------
            list_type : list[str]
                list_type is either self.reaction_id or self.send_message_id

            Returns
            -------
            list
                new list that is filtered of the keys and values that are required for the output
            """
            message_container = str(message.content.lower())
            if message_container.startswith("<:"):
                return
            return list(filter(lambda x: x in message_container, list_type))

        reaction_call = generate_list(self.reaction_id)
        send_call = generate_list(self.send_message_id)

        if reaction_call:
            for emoji in reaction_call:
                await message.add_reaction(self.reaction_id[emoji])

        if send_call:
            for emoji in send_call:
                await message.channel.send(self.send_message_id[emoji])

    # @Cog.listener()
        # async def on_ready(self):
        # print("Bot ready to be served!")
            # try:
        # synced = await self.bot.tree.sync()
            # except:
    # print("Exception on syncing the tree!")

    # TODO: a way to delete a sent message in dm.
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

            if len(msg.attachments) > 0:
                for att in msg.attachments:
                    await author.send(att.url)

    @hybrid_command(name="ping", brief="Get the bot's ping")
    async def ping(self, ctx: Context) -> None:
        """Get the bot's ping"""
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    @hybrid_command(name="sus", aliases=["susy"])
    async def sus(self, ctx: Context) -> None:
        """sus command"""
        await ctx.send(self.reaction_id["sus"])


async def setup(bot: discord.ext.commands.Bot) -> None:
    """Add cog to bot."""
    await bot.add_cog(FunListen(bot))
