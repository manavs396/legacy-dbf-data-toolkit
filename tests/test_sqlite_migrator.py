import sqlite3

from legacy_dbf_toolkit.sqlite_migrator import _safe_identifier, _sqlite_type


def test_safe_identifier_normalizes_names():
    assert _safe_identifier("Customer Name") == "Customer_Name"
    assert _safe_identifier("123code") == "f_123code"


def test_sqlite_type_mapping():
    assert _sqlite_type(10) == "INTEGER"
    assert _sqlite_type(10.5) == "REAL"
    assert _sqlite_type("text") == "TEXT"
