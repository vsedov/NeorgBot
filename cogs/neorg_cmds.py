import discord
from discord.ext import commands
import re

class neorg_cmds(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def get_wiki(self, ctx, key, obj):
        page_types = {
            'Neorg': 'https://github.com/vhyrro/neorg/wiki',
            'Installation': 'https://github.com/vhyrro/neorg/wiki/Installation#installation',
            'Configuring-Modules': 'https://github.com/vhyrro/neorg/wiki/Configuring-Modules',
            'Modules-Concept': 'https://github.com/vhyrro/neorg/wiki/Installation#the-concept-of-modules',
            'Enabling-Modules': 'https://github.com/vhyrro/neorg/wiki/Installation#enabling-our-own-modules',
            'Logger-Config': 'https://github.com/vhyrro/neorg/wiki/Installation#configuring-the-logger',
            'User-Callbacks': 'https://github.com/vhyrro/neorg/wiki/User-Callbacks',
            'User-Keybinds': 'https://github.com/vhyrro/neorg/wiki/User-Keybinds',
            'Custom-Highlights': 'https://github.com/vhyrro/neorg/wiki/Custom-Highlights',
            'Concealing': 'https://github.com/vhyrro/neorg/wiki/Concealing',
            'Workspace-Management': 'https://github.com/vhyrro/neorg/wiki/Workspace-Management',
            'Creating-Modules': 'https://github.com/vhyrro/neorg/wiki/Creating-Modules',
            'Autocommands': 'https://github.com/vhyrro/neorg/wiki/Autocommands',
            'Keybinds': 'https://github.com/vhyrro/neorg/wiki/Keybinds',
            'Neorg-Command': 'https://github.com/vhyrro/neorg/wiki/Neorg-Command',
            'Concealing-api-functions': 'https://github.com/vhyrro/neorg/wiki/Concealing#api-functions',
            'Dirman': 'https://github.com/vhyrro/neorg/wiki/Dirman',
            'api-calls-for-corehighlights': 'https://github.com/vhyrro/neorg/wiki/Custom-Highlights#api-calls-for-corehighlights',
            'Hotswapping-Modules': 'https://github.com/vhyrro/neorg/wiki/Hotswapping-Modules',
            'Public-vs-Public-Config': 'https://github.com/vhyrro/neorg/wiki/Public-vs-Public-Config',
            'Metamodules': 'https://github.com/vhyrro/neorg/wiki/Metamodules',
        }

        if obj is None:
            await ctx.send(page_types[key])
            return

        obj = re.sub(r'^(?:discord\.(?:ext\.)?)?(?:commands\.)?(.+)', r'\1', obj)

    @commands.group(invoke_without_command=True)
    async def wiki(self, ctx, *, obj: str = None):
        """The Neorg wiki"""
        if ctx.invoked_subcommand is None:
            await self.get_wiki(ctx, 'Neorg', obj)

    @wiki.command(name='Installation', aliases=['installation'])
    async def installation_wiki(self, ctx, *, obj: str = None):
        """Installing Neorg"""
        await self.get_wiki(ctx, 'Installation', obj)

    @wiki.command(name='Configuring-Modules', aliases=['configuring-modules'])
    async def configuring_modules_wiki(self, ctx, *, obj: str = None):
        """Configuring Modules in Neorg"""
        await self.get_wiki(ctx, 'Configuring-Modules', obj)

    @wiki.command(name='Modules-Concept', aliases=['modules-concept'])
    async def modules_concept_wiki(self, ctx, *, obj: str = None):
        """The Concept of Modules"""
        await self.get_wiki(ctx, 'Modules-Concept', obj)

    @wiki.command(name='Enabling-Modules', aliases=['enabling-modules'])
    async def enabling_modules_wiki(self, ctx, *, obj: str = None):
        """Enabling our own modules"""
        await self.get_wiki(ctx, 'Enabling-Modules', obj)

    @wiki.command(name='Logger-Config', aliases=['logger-config', 'logger'])
    async def logger_config_wiki(self, ctx, *, obj: str = None):
        """Configuring the Logger"""
        await self.get_wiki(ctx, 'Logger-Config', obj)

    @wiki.command(name='User-Callbacks', aliases=['user-callbacks'])
    async def user_callbacks_wiki(self, ctx, *, obj: str = None):
        """User Callbacks"""
        await self.get_wiki(ctx, 'User-Callbacks', obj)

    @wiki.command(name='User-Keybinds', aliases=['user-keybinds'])
    async def user_keybinds_wiki(self, ctx, *, obj: str = None):
        """User Keybinds"""
        await self.get_wiki(ctx, 'User-Keybinds', obj)

    @wiki.command(name='Custom-Highlights', aliases=['custom-highlights'])
    async def custom_highlights_wiki(self, ctx, *, obj: str = None):
        """Custom Highlights"""
        await self.get_wiki(ctx, 'Custom-Highlights', obj)

    @wiki.command(name='Concealing', aliases=['concealing'])
    async def concealing_wiki(self, ctx, *, obj: str = None):
        """Concealing"""
        await self.get_wiki(ctx, 'Concealing', obj)

    @wiki.command(name='Workspace-Management', aliases=['workspace-management'])
    async def workspace_management_wiki(self, ctx, *, obj: str = None):
        """Managing Workspaces in Neorg"""
        await self.get_wiki(ctx, 'Workspace-Management', obj)

    @wiki.command(name='Creating-Modules', aliases=['creating-modules'])
    async def creating_modules_wiki(self, ctx, *, obj: str = None):
        """Creating Modules for Neorg"""
        await self.get_wiki(ctx, 'Creating-Modules', obj)

    @wiki.command(name='Autocommands', aliases=['autocommands'])
    async def autocommands_wiki(self, ctx, *, obj: str = None):
        """The Autocommand Module"""
        await self.get_wiki(ctx, 'Autocommands', obj)

    @wiki.command(name='Keybinds', aliases=['keybinds'])
    async def keybinds_wiki(self, ctx, *, obj: str = None):
        """The Keybinds Module"""
        await self.get_wiki(ctx, 'Keybinds', obj)

    @wiki.command(name='Neorg-Command', aliases=['neorg-command'])
    async def neorg_command_wiki(self, ctx, *, obj: str = None):
        """The `:Neorg` Command"""
        await self.get_wiki(ctx, 'Neorg-Command', obj)

    @wiki.command(name='Concealing-api-functions', aliases=['concealing-api-functions'])
    async def concealing_api_functions_wiki(self, ctx, *, obj: str = None):
        """API Functions for `core.norg.concealer`"""
        await self.get_wiki(ctx, 'Concealing-api-functions', obj)

    @wiki.command(name='Dirman', aliases=['dirman'])
    async def dirman_wiki(self, ctx, *, obj: str = None):
        """Using `core.dirman`'s API"""
        await self.get_wiki(ctx, 'Dirman', obj)

    @wiki.command(name='api-calls-for-corehighlights', aliases=['api-calls-corehighlights', 'corehighlights-api-calls'])
    async def api_calls_for_corehighlights_wiki(self, ctx, *, obj: str = None):
        """API Calls for `core.highlights`"""
        await self.get_wiki(ctx, 'api-calls-for-corehighlights', obj)

    @wiki.command(name='Hotswapping-Modules', aliases=['hotswapping-modules'])
    async def hotswapping_modules_wiki(self, ctx, *, obj: str = None):
        """Hotswapping Modules in Neorg"""
        await self.get_wiki(ctx, 'Hotswapping-Modules', obj)

    @wiki.command(name='Public-vs-Public-Config', aliases=['public-vs-public-config'])
    async def public_vs_public_config_wiki(self, ctx, *, obj: str = None):
        """The Difference Between `module.public` and `module.config.public`"""
        await self.get_wiki(ctx, 'Public-vs-Public-Config', obj)

    @wiki.command(name='Metamodules', aliases=['metamodules'])
    async def metamodules_wiki(self, ctx, *, obj: str = None):
        """Metamodules - an Introduction"""
        await self.get_wiki(ctx, 'Metamodules', obj)


    @commands.command()
    async def neorg(self, ctx):
        """Fetch the Neorg repository"""
        await ctx.send('Neorg - https://github.com/vhyrro/neorg')

def setup(bot):
    bot.add_cog(neorg_cmds(bot))
