import json

from legacy_dbf_toolkit import cli
from legacy_dbf_toolkit.reader import FieldInfo


def test_schema_diff_cli_prints_report_and_can_fail_on_changes(monkeypatch, capsys):
    def inspect(path):
        return [FieldInfo("ID", "N", 8, 0)] if path == "old.dbf" else [
            FieldInfo("ID", "N", 8, 0), FieldInfo("NAME", "C", 20, 0)
        ]

    monkeypatch.setattr(cli, "inspect_schema", inspect)
    monkeypatch.setattr("sys.argv", ["dbf-toolkit", "schema-diff", "old.dbf", "new.dbf"])
    assert cli.main() == 0
    assert json.loads(capsys.readouterr().out)["added"][0]["name"] == "NAME"

    monkeypatch.setattr("sys.argv", [
        "dbf-toolkit", "schema-diff", "old.dbf", "new.dbf", "--fail-on-change"
    ])
    assert cli.main() == 1
    capsys.readouterr()


def test_schema_diff_cli_no_changes_returns_success(monkeypatch, capsys):
    monkeypatch.setattr(cli, "inspect_schema", lambda _: [FieldInfo("ID", "N", 8, 0)])
    monkeypatch.setattr("sys.argv", [
        "dbf-toolkit", "schema-diff", "old.dbf", "new.dbf", "--fail-on-change"
    ])
    assert cli.main() == 0
    assert json.loads(capsys.readouterr().out) == {"added": [], "removed": [], "changed": []}
