import json
import sys
from pathlib import Path

import legacy_dbf_toolkit.cli as cli


def _changed_report():
    return {
        "added": [{"name": "NEW", "type": "C", "length": 10, "decimal_count": 0}],
        "removed": [],
        "changed": [],
    }


def test_schema_diff_writes_optional_output_file(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(cli, "inspect_schema", lambda _: [])
    monkeypatch.setattr(cli, "compare_schemas", lambda _before, _after: _changed_report())

    output = tmp_path / "reports" / "schema.json"
    monkeypatch.setattr(
        sys,
        "argv",
        ["legacy-dbf-toolkit", "schema-diff", "before.dbf", "after.dbf", "--output", str(output)],
    )

    assert cli.main() == 0
    assert json.loads(output.read_text(encoding="utf-8")) == _changed_report()
    assert json.loads(capsys.readouterr().out) == _changed_report()


def test_schema_diff_preserves_fail_on_change_with_output(monkeypatch, tmp_path):
    monkeypatch.setattr(cli, "inspect_schema", lambda _: [])
    monkeypatch.setattr(cli, "compare_schemas", lambda _before, _after: _changed_report())

    output = tmp_path / "schema.json"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "legacy-dbf-toolkit",
            "schema-diff",
            "before.dbf",
            "after.dbf",
            "--output",
            str(output),
            "--fail-on-change",
        ],
    )

    assert cli.main() == 1
    assert output.exists()


def test_schema_diff_returns_2_for_unwritable_output(monkeypatch, tmp_path):
    monkeypatch.setattr(cli, "inspect_schema", lambda _: [])
    monkeypatch.setattr(cli, "compare_schemas", lambda _before, _after: _changed_report())

    directory = tmp_path / "existing-directory"
    directory.mkdir()
    monkeypatch.setattr(
        sys,
        "argv",
        ["legacy-dbf-toolkit", "schema-diff", "before.dbf", "after.dbf", "--output", str(directory)],
    )

    assert cli.main() == 2
