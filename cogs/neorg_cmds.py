from discord.ext import commands
import discord

wiki_pages = {
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

spec_pages = {
	'spec': 'https://github.com/vhyrro/neorg/blob/main/docs/NFF-0.1-spec.md',
	'theory': 'https://github.com/vhyrro/neorg/blob/main/docs/NFF-0.1-spec.md#theory',
	'design-decisions': 'https://github.com/vhyrro/neorg/blob/main/docs/NFF-0.1-spec.md#design-decisions',
	'parsing-order': 'https://github.com/vhyrro/neorg/blob/main/docs/NFF-0.1-spec.md#parsing-order',
	'attached-modifiers-and-their-functions': 'https://github.com/vhyrro/neorg/blob/main/docs/NFF-0.1-spec.md#attached-modifiers-and-their-functions',
	'detached-modifiers-and-their-functions': 'https://github.com/vhyrro/neorg/blob/main/docs/NFF-0.1-spec.md#detached-modifiers-and-their-functions',
	'trailing-modifiers': 'https://github.com/vhyrro/neorg/blob/main/docs/NFF-0.1-spec.md#trailing-modifiers',
	'escaping-special-characters': 'https://github.com/vhyrro/neorg/blob/main/docs/NFF-0.1-spec.md#escaping-special-characters',
	'defining-data': 'https://github.com/vhyrro/neorg/blob/main/docs/NFF-0.1-spec.md#defining-data',
	'tag-parameters': 'https://github.com/vhyrro/neorg/blob/main/docs/NFF-0.1-spec.md#tag-parameters',
	'carryover-tags': 'https://github.com/vhyrro/neorg/blob/main/docs/NFF-0.1-spec.md#carryover-tags',
	'quirks': 'https://github.com/vhyrro/neorg/blob/main/docs/NFF-0.1-spec.md#quirks',
	'single-line-paragraphs': 'https://github.com/vhyrro/neorg/blob/main/docs/NFF-0.1-spec.md#single-line-paragraphs',
	'intersecting-modifiers': 'https://github.com/vhyrro/neorg/blob/main/docs/NFF-0.1-spec.md#intersecting-modifiers',
	'lists': 'https://github.com/vhyrro/neorg/blob/main/docs/NFF-0.1-spec.md#lists',
	'nesting': 'https://github.com/vhyrro/neorg/blob/main/docs/NFF-0.1-spec.md#nesting',
	'todo-lists': 'https://github.com/vhyrro/neorg/blob/main/docs/NFF-0.1-spec.md#todo-lists',
	'links': 'https://github.com/vhyrro/neorg/blob/main/docs/NFF-0.1-spec.md#links',
	'the-first-segment': 'https://github.com/vhyrro/neorg/blob/main/docs/NFF-0.1-spec.md#the-first-segment',
	'the-second-segment': 'https://github.com/vhyrro/neorg/blob/main/docs/NFF-0.1-spec.md#the-second-segment',
	'markers': 'https://github.com/vhyrro/neorg/blob/main/docs/NFF-0.1-spec.md#markers',
	'drawers': 'https://github.com/vhyrro/neorg/blob/main/docs/NFF-0.1-spec.md#drawers',
	'data-tags': 'https://github.com/vhyrro/neorg/blob/main/docs/NFF-0.1-spec.md#data-tags',
	'unsupported-tags': 'https://github.com/vhyrro/neorg/blob/main/docs/NFF-0.1-spec.md#unsupported-tags',
}

class neorg_cmds(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def wiki(self, ctx, *, query):
		query = query.strip().lower().replace(' ', '-')
		stuff = [wiki_pages[k] for k in wiki_pages.keys() if query in k]
		for i in stuff:
			em = discord.Embed(description=i, colour=0x4878BE)
			await ctx.send(embed=em)

	@commands.command()
	async def spec(self, ctx, *, query):
		query = query.strip().lower().replace(' ', '-')
		stuff = [spec_pages[k] for k in spec_pages.keys() if query in k]
		for i in stuff:
			em = discord.Embed(description=i, colour=0x4878BE)
			await ctx.send(embed=em)

	@commands.command()
	async def neorg(self, ctx):
		"""Fetch the Neorg repository"""
		await ctx.send("Neorg - https://github.com/vhyrro/neorg")

def setup(bot):
    bot.add_cog(neorg_cmds(bot))
