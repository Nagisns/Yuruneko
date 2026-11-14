# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

import asyncio
from time import monotonic
from pathlib import Path

import discord
from discord.ext import commands

from level.main import Level

class XpCog(commands.Cog):
    def __init__(self) -> None:
        self._last_xp_at: dict[int, float] = {}

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot or message.guild is None:
            return

        user_id = message.author.id
        now = monotonic()
        last_xp_at = self._last_xp_at.get(user_id)

        if last_xp_at is not None and now - last_xp_at < 5.0:
            return
        
        self._last_xp_at[user_id] = now

        await asyncio.to_thread(Level.add_xp, user_id=user_id, xp=10)

async def setup(bot: commands.Bot) -> None:
    Path("database").mkdir(exist_ok=True)
    Level.create()
    await bot.add_cog(XpCog())
