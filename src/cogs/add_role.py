# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

import asyncio
import logging
import sqlite3

import discord
from discord import app_commands
from discord.ext import commands

from role import RoleRepository


class AddRoleCog(commands.Cog):
    @app_commands.command(name="add_role", description="レベル特典のロールを登録します")
    @app_commands.describe(role="レベル特典で付与するロールを選択してください")
    @app_commands.guild_only()
    @app_commands.checks.cooldown(rate=1, per=30.0)
    @app_commands.checks.has_permissions(manage_roles=True)
    async def add_role(self, interaction: discord.Interaction, role: discord.Role) -> None:
        await interaction.response.defer(ephemeral=True)

        if not isinstance(role, discord.Role):
            await interaction.edit_original_response(content="Error: 選択したロールを取得できませんでした。もう一度選択してください。")
            return

        guild_id: int | None = interaction.guild_id
        if guild_id is None:
            await interaction.edit_original_response(content="このコマンドはサーバー内で使ってください。")
            return

        role_id: int = role.id
        embed: discord.Embed = discord.Embed(
            title="✅ レベル特典ロールを登録しました", 
            description=discord.utils.escape_markdown(role.name),
            color=discord.Color.blue(),
        )

        try:
            await asyncio.to_thread(RoleRepository.registration_role, guild_id, role_id)
        except (OSError, sqlite3.Error):
            logging.exception(f"Failed to register role {role_id} for guild {guild_id}.")
            await interaction.edit_original_response(content="ロールの登録に失敗しました。")
            return

        await interaction.edit_original_response(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AddRoleCog())
