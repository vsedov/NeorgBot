from neorg import log

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from neorg.neorg import Neorg

log.setup()
instance: "Neorg" = None  # Global Neorg instance.
