# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

import logging

import discord
from discord import app_commands

class ErrorHandler:
    async def _send_ephemeral_message(self, interaction: discord.Interaction, message: str) -> None:
        if interaction.response.is_done():
            await interaction.followup.send(message, ephemeral=True)
        else:
            await interaction.response.send_message(message, ephemeral=True)

    async def send_error_message(self, interaction: discord.Interaction, message: str) -> None:
        try:
            await self._send_ephemeral_message(interaction, message)
        except discord.HTTPException:
            logging.exception("Failed to send error message.")

    async def on_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
        message: str = "予期しないエラーが発生しました。"

        if isinstance(error, app_commands.MissingPermissions):
            message = "このコマンドを実行する権限がありません。"
        elif isinstance(error, app_commands.CommandOnCooldown):
            message = "このコマンドはクールダウン中です。"
        else:
            logging.error("Command error: %s", error, exc_info=error)

        await self.send_error_message(interaction, message)
