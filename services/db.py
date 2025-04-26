# src/services/db.py

import sqlite3
from typing import Any
from src.config import config

class Database:
    """
    Класс для работы с таблицей connections в SQLite.
    """
    def __init__(self, db_path: str = config.DB_PATH):
        self.conn = sqlite3.connect(db_path)
        self._init_tables()

    def _init_tables(self) -> None:
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS connections (
                id INTEGER PRIMARY KEY,
                source_id TEXT NOT NULL,
                vk_api_key TEXT NOT NULL,
                vk_group_id TEXT NOT NULL,
                ok_access_token TEXT,
                ok_group_id TEXT,
                ok_app_key TEXT,
                ok_session_key TEXT,
                delay INTEGER DEFAULT 0
            )
        """
        )
        self.conn.commit()

    def add_connection(self, data: dict[str, Any]) -> int:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO connections (
                source_id, vk_api_key, vk_group_id,
                ok_access_token, ok_group_id,
                ok_app_key, ok_session_key, delay
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data['source_id'], data['vk_api_key'], data['vk_group_id'],
                data.get('ok_access_token'), data.get('ok_group_id'),
                data.get('ok_app_key'), data.get('ok_session_key'),
                data['delay']
            )
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_all(self) -> list[tuple]:
        cursor = self.conn.cursor()
        return cursor.execute(
            "SELECT * FROM connections"
        ).fetchall()

    def delete(self, conn_id: int) -> int:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM connections WHERE id = ?", (conn_id,))
        self.conn.commit()
        return cursor.rowcount

    def get_by_source(self, source_id: str) -> tuple[Any, ...] | None:
        cursor = self.conn.cursor()
        return cursor.execute(
            """
            SELECT vk_api_key, vk_group_id, ok_access_token,
                   ok_group_id, ok_app_key, ok_session_key, delay
            FROM connections WHERE source_id = ?
            """,
            (source_id,)
        ).fetchone()