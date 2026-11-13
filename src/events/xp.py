# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

from pathlib import Path

import discord
from discord.ext import commands

from level.main import Level

class XpCog(commands.Cog):
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot or message.guild is None:
            return

        Level.add_xp(user_id=message.author.id, xp=10)

async def setup(bot: commands.Bot) -> None:
    Path("database").mkdir(exist_ok=True)
    Level.create()
    await bot.add_cog(XpCog())
