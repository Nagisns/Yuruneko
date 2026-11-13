# Changelog

Release history for Calm.

## v0.1.0 - 2026-11-13

Initial release.

### Added

- A minimal Discord bot with slash commands using discord.py.
- A `/ping` command that responds with `Pong!` to verify the bot is working.
- Global command synchronization on startup through `setup_hook`.
- The `guilds` gateway intent for maintaining server state without privileged gateway intents.
- Successful-login `INFO` logging with colors when supported by the terminal.
- discord.py logging at `WARNING` and above, configured once to avoid duplicate output.
- Loading `TOKEN` from `.env` with python-dotenv.
- An error message when `TOKEN` is not configured.
- Dependency management with uv and a `requirements.txt` file for pip.
- Voice dependencies through `discord.py[voice]`, including PyNaCl and davey.
- A `.gitignore` file excluding `.env`, the virtual environment, and Python caches.
- A README covering setup and usage, and an MIT license.
