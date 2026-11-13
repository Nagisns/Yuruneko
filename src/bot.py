# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

import os
import logging

import discord
from discord.ext import commands
from dotenv import load_dotenv

from error_handler import ErrorHandler
from mybot import MyBot

discord.utils.setup_logging(level=logging.INFO, root=True)
logging.getLogger("discord").setLevel(logging.WARNING)

bot: MyBot = MyBot(
    command_prefix=commands.when_mentioned,
    intents=discord.Intents(guilds=True, guild_messages=True),
    help_command=None,
)

error_handler: ErrorHandler = ErrorHandler()
bot.tree.error(error_handler.on_app_command_error)

if __name__ == "__main__":
    load_dotenv()

    token: str | None = os.getenv("TOKEN")

    if not token:
        raise SystemExit(".env または環境変数 TOKEN を設定してください。")

    bot.run(token, log_handler=None)
