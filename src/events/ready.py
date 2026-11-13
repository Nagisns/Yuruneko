# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

import logging

from discord.ext import commands

class ReadyCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logging.info(f"Logged in {self.bot.user}")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ReadyCog(bot))
