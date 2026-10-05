from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from dbfread import DBF

@dataclass(frozen=True)
class FieldInfo:
    name: str
    type: str
    length: int
    decimal_count: int

def read_dbf(path: str | Path) -> list[dict[str, Any]]:
    table = DBF(str(path), load=True, char_decode_errors="replace")
    return [dict(record) for record in table]

def inspect_schema(path: str | Path) -> list[FieldInfo]:
    table = DBF(str(path), load=False, char_decode_errors="replace")
    return [
        FieldInfo(field.name, field.type, field.length, field.decimal_count)
        for field in table.fields
    ]
