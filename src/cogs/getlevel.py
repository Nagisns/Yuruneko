# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

import asyncio 
from pathlib import Path

import discord
from discord import app_commands
from discord.ext import commands

from level import Level

class GetLevelCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="level", description="自分のレベルを表示します")
    @app_commands.checks.cooldown(rate=1.0, per=5.0)
    async def level(self, interaction: discord.Interaction) -> None:
        xp: int = await asyncio.to_thread(Level.get_user_xp, user_id=interaction.user.id)
        level: int = Level.calculate_level(xp)

        embed: discord.Embed = discord.Embed(
            title=f"🏆 レベル {level}",
            color=discord.Color.blue(),
        )
        embed.set_author(name=interaction.user.display_name)
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.add_field(name="累計XP", value=f"**{xp:,}** XP", inline=False)
        embed.set_footer(text="チャットに参加して、次のレベルを目指そう！")

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    Path("database").mkdir(exist_ok=True)
    await asyncio.to_thread(Level.create)
    await bot.add_cog(GetLevelCog(bot))
