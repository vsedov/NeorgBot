import dotenv
dotenv.load_dotenv()

import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix=['n.', 'N.'])

extensions = ['cogs.help', 'cogs.neorg_cmds', 'cogs.general']

if __name__ == '__main__':
    for e in extensions:
        client.load_extension(e)

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('the prefix n. | n.help'))
    print("Neorg bot initialized")

client.run(os.getenv('TOKEN'))
