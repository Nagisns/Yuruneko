# Changelog

Release history for Yuruneko.

## v0.3.1 - 2026-11-14

### Added

- A five-second per-user cooldown for message XP rewards, shared across servers.
- Level-up notifications in the message channel, showing the user's mention, display name, avatar, previous and new levels, and cumulative XP.
- A unittest suite covering initial levels and key XP thresholds, XP persistence and user isolation, message reward conditions, cooldowns, and level-up notifications.
- A GitHub Actions workflow that runs tests on pushes and pull requests with uv and locked dependencies.

### Changed

- Separated pure level calculation in `Level.calculate_level` from SQLite XP storage in `XpRepository`, exposing both through the `level` package.
- Made XP updates return the saved total directly for level-up detection.
- Pinned the project's Python version to 3.15 through `.python-version`.
- Renamed the README title to Yuruneko and updated the XP behavior, project structure, and testing instructions.

### Fixed

- Moved `/level` XP lookups and XP event database initialization to worker threads to avoid blocking the event loop.
- Made `/level` calculate the level and display cumulative XP from a single database lookup.

## v0.3.0 - 2026-11-14

### Added

- A `/level` command that displays the invoking user's level and cumulative XP in an embed with their display name and avatar.
- An independent per-user cooldown of one use every 5 seconds for `/level`.
- Message XP rewards through `XpCog`: 10 XP per server message from a non-bot user, excluding direct messages.
- Persistent SQLite XP storage in `database/level.db`, keyed by Discord user ID and shared across servers.
- XP lookup and level calculation, starting at level 1 and reaching levels 2, 5, and 10 at 100, 3,000, and 15,000 cumulative XP.
- The `guild_messages` gateway intent to receive server message events for XP rewards.
- A `/level` entry in the `/help` command list.

### Changed

- Extended `MyBot` to load event Cogs from `src/events/` after command Cogs from `src/cogs/`.
- Moved successful-login logging into `ReadyCog` in `src/events/ready.py`.
- Centralized SQLite database operations and level calculation in `src/level/main.py`.
- Moved message XP updates to a worker thread to avoid blocking the bot's event loop.
- Excluded local database files from Git.
- Updated the README with the leveling system, `/level` command, database behavior, gateway intents, and project structure.

### Fixed

- Ensured the database directory and user table exist when loading `GetLevelCog` and `XpCog`, including on first startup.

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
