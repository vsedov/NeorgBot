from discord.ext import commands

class general(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message):
		if 'sus' in message.content.lower().split():
			await message.add_reaction("<:sus:867395030988881921>")

def setup(bot):
    bot.add_cog(general(bot))
