# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

import logging
from pkgutil import iter_modules
from types import ModuleType

from discord.ext import commands

import cogs

class MyBot(commands.Bot):
    async def setup_hook(self) -> None:
        def _get_extensions(package: ModuleType) -> list[str]:
            return sorted(
                module.name
                for module in iter_modules(
                    package.__path__, prefix=f"{package.__name__}."
                )
                if not module.name.rsplit(".", 1)[-1].startswith("_")
            )

        extensions_cogs: list[str] = _get_extensions(cogs)

        for extension in extensions_cogs:
            await self.load_extension(extension)

        synced = await self.tree.sync()
        logging.info(f"Synced {len(synced)} commands.")
