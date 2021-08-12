from discord.ext import commands
import discord
import requests
from bs4 import BeautifulSoup

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
		neorg_wiki = {}
		wiki_url = "https://github.com/vhyrro/neorg/wiki"

		stuff = BeautifulSoup(requests.get(wiki_url).text, 'lxml')
		lis = stuff.find_all("div", {"class": "Box-body wiki-custom-sidebar markdown-body"})[0]

		for li in lis.find_all('li'):
			part = li.a['href']
			neorg_wiki[part[37:].lower()] = part

		wiki = [neorg_wiki[k] for k in neorg_wiki.keys() if query in k.lower()]

		if len(wiki) == 0:
			await ctx.send(embed=discord.Embed(description="No Results Found!", colour=0x4878BE))
			return
		
		for i in wiki:
			em = discord.Embed(description=i, colour=0x4878BE)
			await ctx.send(embed=em)

	@commands.command()
	async def spec(self, ctx, *, query):
		query = query.strip().lower().replace(' ', '-')
		spec = [spec_pages[k] for k in spec_pages.keys() if query in k]
		for i in spec:
			em = discord.Embed(description=i, colour=0x4878BE)
			await ctx.send(embed=em)

	@commands.command()
	async def neorg(self, ctx):
		"""Fetch the Neorg repository"""
		await ctx.send("Neorg - https://github.com/vhyrro/neorg")

def setup(bot):
    bot.add_cog(neorg_cmds(bot))
