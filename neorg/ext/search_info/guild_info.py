import discord
from discord.ext.commands import Cog, Context, command

from neorg.log import get_logger
from neorg.neorg import Neorg

log = get_logger(__name__)


class GuildInfo(Cog):
    """A Extension to fetch information about the guild/server"""

    def __init__(self, bot: Neorg):
        self.bot = bot

    @command()
    async def count(self, ctx: Context) -> None:
        """Get the number of members in the server."""
        await ctx.send(embed=discord.Embed(description=f"There are {len(ctx.guild.members)} members in the server."))

    @command()
    async def invite(self, ctx: Context) -> None:
        """Invite me to your server."""
        await ctx.send(f"**{ctx.author.name}**, use this URL to invite others\nhttps://discord.gg/T6EgTAX7ht")

    @command()
    async def source(self, ctx: Context) -> None:
        """Check out my source code >.<"""
        await ctx.send(f"**{ctx.bot.user}** is powered by this source code:\nhttps://github.com/vsedov/NeorgBot")

    @command(name="about", aliases=["info", "stats"])
    async def about(self, ctx: Context) -> None:
        """About the bot, what can it do ?"""

        embed_colour = None
        if hasattr(ctx, "guild") and ctx.guild is not None:
            embed_colour = ctx.me.top_role.colour

        avgmembers = sum(g.member_count for g in self.bot.guilds) / len(self.bot.guilds)
        embed = discord.Embed(colour=embed_colour)
        embed.add_field(name="Library", value="discord.py")
        embed.add_field(name="Servers", value=f"{len(ctx.bot.guilds)} ( avg: {avgmembers:,.2f} users/server )",)
        embed.add_field(name="Commands loaded", value=len([x.name for x in self.bot.commands]))

        await ctx.send(content=f"ℹ About **{ctx.bot.user}**", embed=embed)


def setup(bot: Neorg) -> None:
    """Add Cog to Bot."""
    bot.add_cog(GuildInfo(bot))
