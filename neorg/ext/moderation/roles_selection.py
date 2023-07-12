import discord
from discord.ext.commands import Cog, hybrid_command, Context

from neorg import constants as c
from neorg.neorg import Neorg

class RolesSelection(Cog):
    """Add or remove roles based on reactions."""

    def __init__(self, bot: Neorg):
        self.bot = bot

    @Cog.listener()
    async def on_raw_reaction_add(self, p: discord.RawReactionActionEvent):
        if p.guild_id == c.GUILD_ID or p.channel_id == c.REACTION_CHANNEL or p.message_id == c.REACTION_MSG_ID:
            role_id = c.REACTION_ROLES.get(p.emoji.name, None)
            guild: discord.Guild = self.bot.get_guild(p.guild_id)

            if role_id:
                r = guild.get_role(role_id)
                user = (await guild.query_members(user_ids=[p.user_id]))[0]
                await user.add_roles(r)
                await user.send(f"Successfully added {p.emoji.name} role!")

    @Cog.listener()
    async def on_raw_reaction_remove(self, p: discord.RawReactionActionEvent):
        if p.guild_id == c.GUILD_ID or p.channel_id == c.REACTION_CHANNEL or p.message_id == c.REACTION_MSG_ID:
            role_id = c.REACTION_ROLES.get(p.emoji.name, None)
            guild: discord.Guild = self.bot.get_guild(p.guild_id)

            if role_id:
                r = guild.get_role(role_id)
                user = (await guild.query_members(user_ids=[p.user_id]))[0]
                await user.remove_roles(r)
                await user.send(f"Successfully removed {p.emoji.name} role!")

    @hybrid_command()
    async def egg(self, ctx: Context):
        """What, you egg? *He stabs him*"""
        await ctx.send(
            embed=discord.Embed(
                description="Ha! you've found it! Checkout the source code for more! (Hint: n.source)",
                color=c.NORG_BLUE,
            )
        )

async def setup(bot: Neorg) -> None:
    """Add Cog to Bot."""
    await bot.add_cog(RolesSelection(bot))
