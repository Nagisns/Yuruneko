# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

import os
import logging
from textwrap import dedent

import discord
from discord import app_commands
from dotenv import load_dotenv

discord.utils.setup_logging(level=logging.INFO, root=True)
logging.getLogger("discord").setLevel(logging.WARNING)

class MyBot(discord.Client):
    def __init__(self) -> None:
        super().__init__(intents=discord.Intents(guilds=True))
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        await self.tree.sync()

bot: MyBot = MyBot()

@bot.event
async def on_ready() -> None:
    logging.info(f"Logged in {bot.user}")

@bot.tree.command(name="help", description="コマンドの一覧を表示します")
async def help(interaction: discord.Interaction) -> None:
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

@bot.tree.command(name="ping", description="動作確認")
async def ping(interaction: discord.Interaction) -> None:
    await interaction.response.send_message("Pong!")

if __name__ == "__main__":
    load_dotenv()

    token: str | None = os.getenv("TOKEN")

    if not token:
        raise SystemExit(".env または環境変数 TOKEN を設定してください。")

    bot.run(token, log_handler=None)
