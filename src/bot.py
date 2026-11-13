# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

import os
import logging

import discord
from discord.ext import commands
from dotenv import load_dotenv

from mybot import MyBot

discord.utils.setup_logging(level=logging.INFO, root=True)
logging.getLogger("discord").setLevel(logging.WARNING)

bot: MyBot = MyBot(
    command_prefix=commands.when_mentioned,
    intents=discord.Intents(guilds=True),
    help_command=None,
)

@bot.event
async def on_ready() -> None:
    logging.info(f"Logged in {bot.user}")

@bot.tree.command(name="ping", description="動作確認")
async def ping(interaction: discord.Interaction) -> None:
    await interaction.response.send_message("Pong!")

if __name__ == "__main__":
    load_dotenv()

    token: str | None = os.getenv("TOKEN")

    if not token:
        raise SystemExit(".env または環境変数 TOKEN を設定してください。")

    bot.run(token, log_handler=None)
