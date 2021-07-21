import discord
from discord.ext import commands

class neorg_cmds(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def neorg(self, ctx):
        """Fetch the Neorg repository"""
        await ctx.send('Neorg - https://github.com/vhyrro/neorg')

    @commands.command()
    async def wiki(self, ctx):
        """Fetch Neorg's wiki"""
        await ctx.send('Neorg\'s wiki - https://github.com/vhyrro/neorg/wiki')

def setup(bot):
    bot.add_cog(neorg_cmds(bot))
