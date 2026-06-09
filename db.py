"""
Database layer — SQLite via aiosqlite.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional

import aiosqlite

from config import settings

logger = logging.getLogger(__name__)

_CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS flights (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL,
    date            TEXT    NOT NULL,
    destination     TEXT    NOT NULL,
    flight_minutes  INTEGER NOT NULL,
    night_minutes   INTEGER NOT NULL
);
"""

_CREATE_INDEX_SQL = """
CREATE INDEX IF NOT EXISTS idx_flights_user_date
    ON flights (user_id, date);
"""


@dataclass
class Flight:
    id: int
    user_id: int
    date: str
    destination: str
    flight_minutes: int
    night_minutes: int


def _row_to_flight(row: aiosqlite.Row) -> Flight:
    return Flight(
        id=row["id"],
        user_id=row["user_id"],
        date=row["date"],
        destination=row["destination"],
        flight_minutes=row["flight_minutes"],
        night_minutes=row["night_minutes"],
    )


async def init_db() -> None:
    async with aiosqlite.connect(settings.db_path) as db:
        await db.execute(_CREATE_TABLE_SQL)
        await db.execute(_CREATE_INDEX_SQL)
        await db.commit()
    logger.info("Database ready at '%s'.", settings.db_path)


async def add_flight(
    user_id: int,
    date: str,
    destination: str,
    flight_minutes: int,
    night_minutes: int,
) -> Flight:
    async with aiosqlite.connect(settings.db_path) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            """
            INSERT INTO flights (user_id, date, destination, flight_minutes, night_minutes)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, date, destination, flight_minutes, night_minutes),
        )
        await db.commit()
        row = await (
            await db.execute(
                "SELECT * FROM flights WHERE id = ?", (cursor.lastrowid,)
            )
        ).fetchone()
    return _row_to_flight(row)


async def get_flights_for_month(user_id: int, year: int, month: int) -> list[Flight]:
    month_prefix = f"{year:04d}-{month:02d}"
    async with aiosqlite.connect(settings.db_path) as db:
        db.row_factory = aiosqlite.Row
        rows = await (
            await db.execute(
                """
                SELECT * FROM flights
                WHERE user_id = ?
                  AND date LIKE ?
                ORDER BY date ASC, id ASC
                """,
                (user_id, f"{month_prefix}%"),
            )
        ).fetchall()
    return [_row_to_flight(r) for r in rows]


async def get_last_flight(user_id: int) -> Optional[Flight]:
    async with aiosqlite.connect(settings.db_path) as db:
        db.row_factory = aiosqlite.Row
        row = await (
            await db.execute(
                """
                SELECT * FROM flights
                WHERE user_id = ?
                ORDER BY id DESC
                LIMIT 1
                """,
                (user_id,),
            )
        ).fetchone()
    return _row_to_flight(row) if row else None


async def delete_flight(flight_id: int) -> bool:
    async with aiosqlite.connect(settings.db_path) as db:
        cursor = await db.execute(
            "DELETE FROM flights WHERE id = ?", (flight_id,)
        )
        await db.commit()
    return cursor.rowcount > 0
