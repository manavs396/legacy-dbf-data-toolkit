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
