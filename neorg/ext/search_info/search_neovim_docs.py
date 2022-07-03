from discord.ext.commands import Cog, Context, command

from neorg.fetch_info.neovim_docs import NeovimDocs
from neorg.log import get_logger
from neorg.neorg import Neorg

log = get_logger(__name__)


class NeovimDocSearch(Cog):
    """Neovim Documentation extension."""

    def __init__(self, bot: Neorg):
        self.bot = Neorg
        self.neovim = NeovimDocs

    @command()
    async def doc(self, ctx: Context, *, query: str = "api highlights") -> None:
        """
        Neovim Documentation
        To search
        `n.doc <query>|<amount>(optional)<accuracy>(optional)`
        query : tag link
        amount : how many return links do you want.
        example:
            n.doc highlight-guifg | 10 | 50%  - 10 items will be returned and items no under 50 % will be resulted
            n.doc nvim-config | 100% - will return items with 100 % with default settings
        """
        # `n.doc <query>|<amount>(optional)<accuracy>(optional)`
        #  TODO(vsedov) (05:04:22 - 03/07/22): Find a better way around this
        pass
