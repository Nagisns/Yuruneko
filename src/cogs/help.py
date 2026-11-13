# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

from textwrap import dedent

import discord
from discord import app_commands
from discord.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="help", description="コマンドの一覧を表示します")
    @app_commands.checks.cooldown(rate=1.0, per=5.0)
    async def help(self, interaction: discord.Interaction) -> None:
        embed: discord.Embed = discord.Embed(
            title="コマンド一覧",
            description=dedent(
                """
                `/help` - コマンドの一覧を表示します
                `/ping` - Botが応答しているか確認します
                """
            ).strip(),
            color=discord.Color.blue(),
        )

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(HelpCog(bot))
