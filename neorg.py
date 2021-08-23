import dotenv
dotenv.load_dotenv()

import discord
from discord.ext import commands
import os
import hosting

client = commands.Bot(command_prefix=['n.', 'N.'])

extensions = ['cogs.help', 'cogs.neorg_cmds', 'cogs.general']

if __name__ == '__main__':
    for e in extensions:
        client.load_extension(e)

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('the prefix n. | n.help'))
    print("Neorg bot initialized")

@client.command(aliases=['r'])
async def reload(ctx, cog):
    if not cog:
        await ctx.send('Specify the cog to reload!')
        return
    try:
        client.unload_extension(f'cogs.{cog}')
        client.load_extension(f'cogs.{cog}')
        await ctx.send(embed=discord.Embed(description=f"Cog **{cog}** reloaded", colour=discord.Color.red()))
    except Exception as ae:
        await ctx.send(ae)
        print(f'{cog} could not be loaded')

hosting.keep_running()
client.run(os.getenv('TOKEN'))
