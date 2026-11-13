# Calm

**v0.1.0** — A minimal Discord bot with slash commands, built with discord.py.
The bot responds to `/ping` with `Pong!`. Dependencies are managed with uv, and python-dotenv loads the bot token from `.env`.

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

The bot syncs global slash commands with Discord on startup.
Run `/ping` in Discord to check that the bot responds with `Pong!`.
Commands may take some time to appear.

Press `Ctrl+C` in the terminal to stop the bot.

## Logging

The bot logs a successful login at `INFO` level. discord.py logs are limited to `WARNING` and above.
Log output uses discord.py's formatter, with colors when supported by the terminal.
Logging is configured once to avoid duplicate output.

## Commands

| Command | Description |
| --- | --- |
| `/ping` | Responds with `Pong!`. |

## Project Structure

```text
Calm/
├── src/
│   └── bot.py        # Bot entry point
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

Add an asynchronous function decorated with `@bot.tree.command(...)` in `src/bot.py`, alongside the existing `/ping` command and before the startup block.
Restart the bot to sync the new command with Discord.

## Changelog and License

See [CHANGELOG.md](CHANGELOG.md) for the release history.
This project is licensed under the [MIT License](LICENSE).
