from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from neorg.neorg import Neorg  # pass

from neorg import log

log.setup()
instance: "Neorg" = None  # Global Bot instance.
