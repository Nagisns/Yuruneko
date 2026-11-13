# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

import sqlite3

class Level:
    @staticmethod
    def create():
        conn = sqlite3.connect("database/level.db")
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                xp INTEGER NOT NULL DEFAULT 0
            )
        """)

        conn.commit()
        conn.close()

    @staticmethod
    def add_xp(user_id: int, xp: int):
        conn = sqlite3.connect("database/level.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
            (user_id,)
        )

        cursor.execute(
            "UPDATE users SET xp = xp + ? WHERE user_id = ?",
            (xp, user_id)
        )

        conn.commit()
        conn.close()
