# Yuruneko

**v0.3.0** — A Discord bot with slash commands and an XP-based leveling system, built with discord.py.
The bot provides `/help` to list commands, `/ping` to respond with `Pong!`, and `/level` to display your level and cumulative XP.
Server messages earn XP, which is stored locally in SQLite.
Commands are organized into automatically loaded Cogs, with per-user cooldowns and shared error handling.
Dependencies are managed with uv, and python-dotenv loads the bot token from `.env`.

## Requirements

- Python 3.15 or later, as specified in `pyproject.toml`
- [uv](https://docs.astral.sh/uv/)
- A Discord bot token and permission to add the bot to a server

## Setup

### 1. Create and Install the Discord Bot

1. Create an application in the [Discord Developer Portal](https://discord.com/developers/applications).
2. Get your bot token from the **Bot** page.
3. On the **Installation** page, add the `bot` and `applications.commands` scopes under **Guild Install**.
4. Use the **Install Link** to add the bot to your server.

The bot enables the `guilds` gateway intent to maintain server state and `guild_messages` to receive server message events for XP rewards.
No privileged gateway intents are required.

### 2. Install Dependencies

Run this command from the project root:

```powershell
uv sync
```

uv prepares the environment in `.venv` using `pyproject.toml` and `uv.lock`.
This installs `discord.py[voice]`, including the PyNaCl and davey voice dependencies.
No separate pip installation step is needed.

### 3. Configure the Token

Create a `.env` file in the project root and set your bot token:

```dotenv
TOKEN=your_bot_token
```

Keep your token private. `.env` is excluded from Git by `.gitignore`.
If the `TOKEN` environment variable is already set, it takes precedence over the value in `.env`.

## Run the Bot

Run this command from the project root. uv handles virtual environment activation automatically.

```powershell
uv run src/bot.py
```

The bot automatically loads Cog extensions from `src/cogs/` and `src/events/`, then syncs global slash commands with Discord on startup.
Run `/ping` in Discord to check that the bot responds with `Pong!`.
Run `/help` to display the command list.
Run `/level` to display your level and cumulative XP.
Commands may take some time to appear.

Press `Ctrl+C` in the terminal to stop the bot.

## Logging

The bot logs the number of synced commands and a successful login at `INFO` level. Login logging is handled by `ReadyCog` in `src/events/ready.py`.
Unexpected command errors and failures to send error messages are logged at `ERROR` level.
discord.py logs are limited to `WARNING` and above.
Log output uses discord.py's formatter, with colors when supported by the terminal.
Logging is configured once to avoid duplicate output.

## Commands

| Command | Description |
| --- | --- |
| `/help` | Displays the command list in an embed. |
| `/ping` | Responds with `Pong!`. |
| `/level` | Displays your level and cumulative XP in an embed with your display name and avatar. |

Each command can be used once every 5 seconds per user. The cooldowns for `/help`, `/ping`, and `/level` are independent.

## XP and Levels

Each server message from a non-bot user grants 10 XP. Bot messages and direct messages do not grant XP.
XP is tracked by Discord user ID and shared across servers where this bot runs.
Users start at level 1 with 0 XP, and levels are calculated from cumulative XP without spending it.

| Level | Cumulative XP required |
| --- | --- |
| 1 | 0 |
| 2 | 100 |
| 5 | 3,000 |
| 10 | 15,000 |

XP is stored in `database/level.db`, relative to the working directory. Run the bot from the project root as shown above.
The database directory and user table are created automatically when the Cogs load, and existing XP is retained across restarts.
XP updates run in a worker thread to avoid blocking the bot's event loop.
SQLite is included in Python, so no separate database server or additional dependency is required.
The `database/` directory is excluded from Git.

## Error Handling

Slash command errors are handled centrally by `ErrorHandler` in `src/error_handler.py`.
Permission errors, cooldowns, and unexpected errors produce Japanese messages visible only to the user who ran the command.
If the interaction has already been answered, the bot sends the error message as a follow-up.

## Project Structure

```text
Calm/
├── src/
│   ├── bot.py            # Bot entry point, intents, and error handler registration
│   ├── mybot.py          # MyBot, Cog loading, and command synchronization
│   ├── error_handler.py  # Shared slash command error handling
│   ├── cogs/
│   │   ├── __init__.py
│   │   ├── getlevel.py   # /level command
│   │   ├── help.py       # /help command
│   │   └── ping.py       # /ping command
│   ├── events/
│   │   ├── __init__.py
│   │   ├── ready.py      # Login logging
│   │   └── xp.py         # Message XP rewards
│   └── level/
│       ├── __init__.py
│       └── main.py       # SQLite XP storage and level calculation
├── database/             # Created automatically and excluded from Git
│   └── level.db          # Persistent user XP
├── .env              # Bot token (excluded from Git)
├── .gitignore
├── pyproject.toml    # Project settings and dependencies
├── uv.lock           # Locked dependency versions
├── requirements.txt  # Dependencies for pip
├── README.md
├── CHANGELOG.md
└── LICENSE
```

## Adding Commands

Create an extension module in `src/cogs/`, following `help.py` or `ping.py`:

1. Define a `commands.Cog` subclass and add asynchronous command methods decorated with `@app_commands.command(...)`.
2. Provide an `async def setup(bot)` function that registers the Cog with `await bot.add_cog(...)`.
3. Update the command list in `src/cogs/help.py` and this README.
4. Restart the bot to load the extension and sync the new command with Discord.

`MyBot` automatically loads modules directly inside `src/cogs/`, followed by `src/events/`, sorting each package's modules by name and skipping names that start with `_`.
Event listeners belong in `src/events/` and use `@commands.Cog.listener()` with the same `async def setup(bot)` registration pattern.

## Changelog and License

See [CHANGELOG.md](CHANGELOG.md) for the release history.
This project is licensed under the [MIT License](LICENSE).
