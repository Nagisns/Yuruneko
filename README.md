# Calm

**v0.2.0** — A minimal Discord bot with slash commands, built with discord.py.
The bot provides `/help` to list commands and `/ping` to respond with `Pong!`.
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

The bot enables the `guilds` gateway intent to maintain server state.
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

The bot automatically loads Cog extensions from `src/cogs/` and syncs global slash commands with Discord on startup.
Run `/ping` in Discord to check that the bot responds with `Pong!`.
Run `/help` to display the command list.
Commands may take some time to appear.

Press `Ctrl+C` in the terminal to stop the bot.

## Logging

The bot logs the number of synced commands and a successful login at `INFO` level.
Unexpected command errors and failures to send error messages are logged at `ERROR` level.
discord.py logs are limited to `WARNING` and above.
Log output uses discord.py's formatter, with colors when supported by the terminal.
Logging is configured once to avoid duplicate output.

## Commands

| Command | Description |
| --- | --- |
| `/help` | Displays the command list in an embed. |
| `/ping` | Responds with `Pong!`. |

Each command can be used once every 5 seconds per user. The cooldowns for `/help` and `/ping` are independent.

## Error Handling

Slash command errors are handled centrally by `ErrorHandler` in `src/error_handler.py`.
Permission errors, cooldowns, and unexpected errors produce Japanese messages visible only to the user who ran the command.
If the interaction has already been answered, the bot sends the error message as a follow-up.

## Project Structure

```text
Calm/
├── src/
│   ├── bot.py        # Bot entry point and error handler registration
│   ├── mybot.py      # MyBot, Cog loading, and command synchronization
│   ├── error_handler.py  # Shared slash command error handling
│   └── cogs/
│       ├── __init__.py
│       ├── help.py   # /help command
│       └── ping.py   # /ping command
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

`MyBot` automatically loads modules directly inside `src/cogs/` in name order, skipping names that start with `_`.

## Changelog and License

See [CHANGELOG.md](CHANGELOG.md) for the release history.
This project is licensed under the [MIT License](LICENSE).
