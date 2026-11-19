# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

import sqlite3
from contextlib import closing
from pathlib import Path
from typing import Any


_DATABASE_PATH: Path = Path("database/role.db")


class RoleRepository:
    @classmethod
    def create_table(cls) -> None:
        _DATABASE_PATH.parent.mkdir(exist_ok=True)

        with closing(sqlite3.connect(_DATABASE_PATH)) as connection, connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS guild_roles (
                    guild_id INTEGER PRIMARY KEY,
                    role_id INTEGER NOT NULL
                )
                """
            )

    @classmethod
    def registration_role(cls, guild_id: int, role_id: int) -> None:
        cls.create_table()

        with closing(sqlite3.connect(_DATABASE_PATH)) as connection, connection:
            connection.execute(
                """
                INSERT INTO guild_roles (guild_id, role_id) VALUES (?, ?)
                ON CONFLICT(guild_id) DO UPDATE SET role_id = excluded.role_id
                """,
                (guild_id, role_id),
            )

    @classmethod
    def get_role(cls, guild_id: int) -> int | None:
        cls.create_table()

        with closing(sqlite3.connect(_DATABASE_PATH)) as connection:
            row: Any = connection.execute(
                "SELECT role_id FROM guild_roles WHERE guild_id = ?",
                (guild_id,),
            ).fetchone()
            return row[0] if row else None
