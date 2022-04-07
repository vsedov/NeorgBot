import importlib
import inspect
import pkgutil
from typing import Iterator, NoReturn

from neorg import cogs

def unqualify(name: str) -> str:
    """Return an unqualified name given a qualified module/package `name`."""
    return name.rsplit(".", maxsplit=1)[-1]

def walk_extensions() -> Iterator[str]:
    """Yield extension names from the bot.exts subpackage."""

    def on_error(name: str) -> NoReturn:
        """An error handler for `pkgutil.walk_packages`."""
        raise ImportError(name=name)  # pragma: no cover

    for module in pkgutil.walk_packages(cogs.__path__, f"{cogs.__name__}.",
                                        onerror=on_error):
        if unqualify(module.name).startswith("_"):
            # Ignore module/package names starting with an underscore.
            continue

        if module.ispkg:
            imported = importlib.import_module(module.name)
            if not inspect.isfunction(getattr(imported, "setup", None)):
                # If it lacks a setup function, it's not an extension.
                continue

        yield module.name

EXTENSIONS = frozenset(walk_extensions())
