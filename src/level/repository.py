# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

import sqlite3

class XpRepository:
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
        XpRepository._execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                xp INTEGER NOT NULL DEFAULT 0
            )
            """
        )

    @staticmethod
    def add_xp(user_id: int, xp: int) -> int:
        conn = sqlite3.connect("database/level.db")
        try:
            row = conn.execute(
                """
                INSERT INTO users (user_id, xp) VALUES (?, ?)
                ON CONFLICT(user_id)
                DO UPDATE SET xp = users.xp + excluded.xp
                RETURNING xp
                """,
                (user_id, xp),
            ).fetchone()
            conn.commit()
            return row[0]
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

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
