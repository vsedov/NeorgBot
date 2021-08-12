from discord.ext import commands
import discord
import requests
from bs4 import BeautifulSoup
import re

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
		url = "https://raw.githubusercontent.com/vhyrro/neorg/main/docs/NFF-0.1-spec.md"
		og_url = "https://github.com/vhyrro/neorg/blob/main/docs/NFF-0.1-spec.md"

		soup = re.findall( r"\[(.+)\]\((.+)\)", requests.get(url).text[:1500])
		neorg_specs = {}

		for k,v in soup:
			neorg_specs[k.lower().replace(' ', '-')] = og_url + v

		spec = [neorg_specs[k] for k in neorg_specs.keys() if query in k.lower()]

		if len(spec) == 0:
			await ctx.send(embed=discord.Embed(description="No Results Found!", colour=0x4878BE))
			return

		for i in spec:
			em = discord.Embed(description=i, colour=0x4878BE)
			await ctx.send(embed=em)

	@commands.command()
	async def neorg(self, ctx):
		"""Fetch the Neorg repository"""
		await ctx.send("Neorg - https://github.com/vhyrro/neorg")

def setup(bot):
    bot.add_cog(neorg_cmds(bot))
