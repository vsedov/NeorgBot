from typing import TYPE_CHECKING

import log

if TYPE_CHECKING:
    from neorg.neorg import Neorg

log.setup()
instance: "Neorg" = None  # Global Bot instance.
