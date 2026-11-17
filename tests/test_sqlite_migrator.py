import sqlite3
import pytest

from legacy_dbf_toolkit.sqlite_migrator import _safe_identifier, _sqlite_type, _checked_columns


def test_safe_identifier_normalizes_names():
    assert _safe_identifier("Customer Name") == "Customer_Name"
    assert _safe_identifier("123code") == "f_123code"


def test_sqlite_type_mapping():
    assert _sqlite_type(10) == "INTEGER"
    assert _sqlite_type(10.5) == "REAL"
    assert _sqlite_type("text") == "TEXT"


def test_unique_sqlite_column_names_are_preserved():
    assert _checked_columns(["Customer ID", "Name"]) == ["Customer ID", "Name"]


@pytest.mark.parametrize("columns", [
    ["Customer Name", "Customer-Name"],
    ["Name", "NAME"],
    ["123code", "f_123code"],
])
def test_normalized_sqlite_column_collisions_are_rejected(columns):
    with pytest.raises(ValueError, match="map to the same SQLite identifier"):
        _checked_columns(columns)


def test_logical_fields_migrate_as_sqlite_integers(monkeypatch, tmp_path):
    from legacy_dbf_toolkit import sqlite_migrator

    monkeypatch.setattr(sqlite_migrator, "read_dbf", lambda _: [
        {"ACTIVE": True, "NAME": "Asha"},
        {"ACTIVE": False, "NAME": "Sam"},
        {"ACTIVE": None, "NAME": "Unknown"},
    ])
    database = tmp_path / "synthetic.sqlite"
    assert sqlite_migrator.migrate_dbf_to_sqlite("synthetic.dbf", database, "customers") == 3
    with sqlite3.connect(database) as connection:
        assert connection.execute(
            "SELECT ACTIVE, typeof(ACTIVE), NAME FROM customers ORDER BY rowid"
        ).fetchall() == [
            (1, "integer", "Asha"),
            (0, "integer", "Sam"),
            (None, "null", "Unknown"),
        ]
