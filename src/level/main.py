# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

import sqlite3

class Level:
    @staticmethod
    def _execute(sql: str, params: tuple[int, ...] = ()) -> None:
        conn = sqlite3.connect("database/level.db")
        try:
            conn.execute(sql, params)
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def create() -> None:
        Level._execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                xp INTEGER NOT NULL DEFAULT 0
            )
            """
        )

    @staticmethod
    def add_xp(user_id: int, xp: int) -> None:
        Level._execute(
            """
            INSERT INTO users (user_id, xp) VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET xp = users.xp + excluded.xp
            """,
            (user_id, xp)
        )

    @staticmethod
    def get_user_xp(user_id: int) -> int:
        conn = sqlite3.connect("database/level.db")
        try:
            row = conn.execute(
                "SELECT xp FROM users WHERE user_id = ?",
                (user_id,)
            ).fetchone()
            return row[0] if row is not None else 0
        finally:
            conn.close()

    @staticmethod
    def get_user_level(user_id: int) -> int:
        """Reach levels 2, 5, and 10 at 100, 3000, and 15000 cumulative XP."""
        xp = Level.get_user_xp(user_id)
        level = 1
        required_xp = 100

        while xp >= required_xp:
            level += 1
            if level < 5:
                required_xp += 100 * level**2
            else:
                required_xp += 300 * (level + 1)

        return level
