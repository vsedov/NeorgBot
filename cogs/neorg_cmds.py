from discord.ext import commands
import discord

page_types = {
	'neorg': 'https://github.com/vhyrro/neorg/wiki',
	'installation': 'https://github.com/vhyrro/neorg/wiki/Installation#installation',
	'configuring-modules': 'https://github.com/vhyrro/neorg/wiki/Configuring-Modules',
	'modules-concept': 'https://github.com/vhyrro/neorg/wiki/Installation#the-concept-of-modules',
	'enabling-modules': 'https://github.com/vhyrro/neorg/wiki/Installation#enabling-our-own-modules',
	'logger-config': 'https://github.com/vhyrro/neorg/wiki/Installation#configuring-the-logger',
	'user-callbacks': 'https://github.com/vhyrro/neorg/wiki/User-Callbacks',
	'user-keybinds': 'https://github.com/vhyrro/neorg/wiki/User-Keybinds',
	'custom-highlights': 'https://github.com/vhyrro/neorg/wiki/Custom-Highlights',
	'concealing': 'https://github.com/vhyrro/neorg/wiki/Concealing',
	'workspace-management': 'https://github.com/vhyrro/neorg/wiki/Workspace-Management',
	'creating-modules': 'https://github.com/vhyrro/neorg/wiki/Creating-Modules',
	'autocommands': 'https://github.com/vhyrro/neorg/wiki/Autocommands',
	'keybinds': 'https://github.com/vhyrro/neorg/wiki/Keybinds',
	'neorg-command': 'https://github.com/vhyrro/neorg/wiki/Neorg-Command',
	'concealing-api-functions': 'https://github.com/vhyrro/neorg/wiki/Concealing#api-functions',
	'dirman': 'https://github.com/vhyrro/neorg/wiki/Dirman',
	'api-calls-for-corehighlights': 'https://github.com/vhyrro/neorg/wiki/Custom-Highlights#api-calls-for-corehighlights',
	'hotswapping-modules': 'https://github.com/vhyrro/neorg/wiki/Hotswapping-Modules',
	'public-vs-public-config': 'https://github.com/vhyrro/neorg/wiki/Public-vs-Public-Config',
	'metamodules': 'https://github.com/vhyrro/neorg/wiki/Metamodules',
}

class neorg_cmds(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def wiki(self, ctx, *, query):
		query = query.strip().lower().replace(' ', '-')
		stuff = [page_types[k] for k in page_types.keys() if query in k]
		for i in stuff:
			em = discord.Embed(description=i, colour=0x4878BE)
			await ctx.send(embed=em)

	@commands.command()
	async def neorg(self, ctx):
		"""Fetch the Neorg repository"""
		await ctx.send("Neorg - https://github.com/vhyrro/neorg")

def setup(bot):
    bot.add_cog(neorg_cmds(bot))
