# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

import discord
from discord import app_commands
from discord.ext import commands

class PingCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="ping", description="Botが応答しているか確認します")
    @app_commands.checks.cooldown(rate=1.0, per=5.0)
    async def ping(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("Pong!")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(PingCog(bot))
    