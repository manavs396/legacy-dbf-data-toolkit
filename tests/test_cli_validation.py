"""Exercise the validation CLI contract without requiring real DBF files."""
import json
import sys

import pytest

from legacy_dbf_toolkit import cli


@pytest.mark.parametrize(
    "records, expected_issues, expected_status",
    [
        ([], [], 0),
        ([{"NAME": "Example"}], [], 0),
        ([{"NAME": ""}], [{"row_number": 1, "field": "NAME",
                          "message": "Required value is missing"}], 1),
    ],
)
@pytest.mark.parametrize("summary", [False, True])
def test_validate_cli_output(monkeypatch, capsys, records, expected_issues,
                             expected_status, summary):
    monkeypatch.setattr(cli, "read_dbf", lambda path: records)
    monkeypatch.setattr(cli, "load_rules", lambda path: {"required_fields": ["NAME"]})
    monkeypatch.setattr(cli, "configure_logging", lambda verbose: None)
    argv = ["toolkit", "validate", "synthetic.dbf", "--config", "rules.json"]
    if summary:
        argv.append("--summary")
    monkeypatch.setattr(sys, "argv", argv)

    assert cli.main() == expected_status
    captured = capsys.readouterr()
    assert json.loads(captured.out) == expected_issues
    if summary:
        assert json.loads(captured.err) == {
            "record_count": len(records),
            "issue_count": len(expected_issues),
            "issues_by_field": {"NAME": 1} if expected_issues else {},
        }
    else:
        assert captured.err == ""
