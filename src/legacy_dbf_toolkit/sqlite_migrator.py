from __future__ import annotations

import re
import sqlite3
from pathlib import Path
from typing import Any

from .reader import read_dbf


def _safe_identifier(name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_]", "_", name.strip())
    if not cleaned:
        raise ValueError("Identifier cannot be empty")
    if cleaned[0].isdigit():
        cleaned = f"f_{cleaned}"
    return cleaned


def _sqlite_type(value: Any) -> str:
    if isinstance(value, bool):
        return "INTEGER"
    if isinstance(value, int):
        return "INTEGER"
    if isinstance(value, float):
        return "REAL"
    return "TEXT"


def migrate_dbf_to_sqlite(
    dbf_path: str | Path,
    sqlite_path: str | Path,
    table_name: str | None = None,
) -> int:
    records = read_dbf(dbf_path)
    if not records:
        return 0

    table = _safe_identifier(table_name or Path(dbf_path).stem)
    columns = list(records[0].keys())

    column_defs = []
    for column in columns:
        sample = next((row.get(column) for row in records if row.get(column) is not None), None)
        column_defs.append(f'"{_safe_identifier(column)}" {_sqlite_type(sample)}')

    db_path = Path(sqlite_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as connection:
        connection.execute(
            f'CREATE TABLE IF NOT EXISTS "{table}" ({", ".join(column_defs)})'
        )

        placeholders = ", ".join("?" for _ in columns)
        column_sql = ", ".join(f'"{_safe_identifier(c)}"' for c in columns)
        insert_sql = f'INSERT INTO "{table}" ({column_sql}) VALUES ({placeholders})'

        connection.executemany(
            insert_sql,
            [[str(row.get(column)) if row.get(column) is not None else None for column in columns]
             for row in records],
        )
        connection.commit()

    return len(records)
