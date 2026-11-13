# Changelog

Release history for Calm.

## v0.2.0 - 2026-11-14

### Added

- A `/help` command that displays the command list in an embed.
- Independent per-user cooldowns of one use every 5 seconds for `/help` and `/ping`.
- A shared `ErrorHandler` for slash command permission errors, cooldowns, and unexpected errors.
- Japanese error messages visible only to the invoking user, with follow-up responses when the interaction has already been answered.
- Error logging for unexpected command errors and failures to send error messages.
- Logging of the number of synced commands at startup.

### Changed

- Moved `/help` and `/ping` into separate Cogs under `src/cogs/`.
- Introduced `MyBot` to automatically load Cog extensions in name order, skip names starting with `_`, and sync global slash commands.
- Updated the README with the command list, cooldown behavior, error handling, project structure, and Cog-based command creation steps.

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
