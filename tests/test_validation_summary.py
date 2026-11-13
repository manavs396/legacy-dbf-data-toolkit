import json
import sys

from legacy_dbf_toolkit.validation import ValidationIssue, summarize_issues


def test_empty_summary():
    assert summarize_issues(0, []) == {
        "record_count": 0, "issue_count": 0, "issues_by_field": {}
    }


def test_summary_counts_multiple_issues_per_field():
    issues = [
        ValidationIssue(1, "NAME", "missing"),
        ValidationIssue(2, "EMAIL", "too long"),
        ValidationIssue(3, "NAME", "missing"),
    ]
    assert summarize_issues(3, issues) == {
        "record_count": 3,
        "issue_count": 3,
        "issues_by_field": {"EMAIL": 1, "NAME": 2},
    }


def test_cli_summary_preserves_stdout_and_exit_code(monkeypatch, capsys):
    from legacy_dbf_toolkit import cli

    monkeypatch.setattr(sys, "argv", [
        "dbf-toolkit", "validate", "dummy.dbf", "--config", "rules.json", "--summary"
    ])
    monkeypatch.setattr(cli, "load_rules", lambda _: {"required_fields": ["NAME"]})
    monkeypatch.setattr(cli, "read_dbf", lambda _: [{"NAME": ""}, {"NAME": "Asha"}])
    assert cli.main() == 1
    captured = capsys.readouterr()
    assert json.loads(captured.out) == [
        {"row_number": 1, "field": "NAME", "message": "Required value is missing"}
    ]
    assert json.loads(captured.err) == {
        "record_count": 2, "issue_count": 1, "issues_by_field": {"NAME": 1}
    }


def test_cli_summary_for_clean_records(monkeypatch, capsys):
    from legacy_dbf_toolkit import cli

    monkeypatch.setattr(sys, "argv", [
        "dbf-toolkit", "validate", "dummy.dbf", "--config", "rules.json", "--summary"
    ])
    monkeypatch.setattr(cli, "load_rules", lambda _: {"required_fields": ["NAME"]})
    monkeypatch.setattr(cli, "read_dbf", lambda _: [{"NAME": "Asha"}])
    assert cli.main() == 0
    captured = capsys.readouterr()
    assert json.loads(captured.out) == []
    assert json.loads(captured.err) == {
        "record_count": 1, "issue_count": 0, "issues_by_field": {}
    }
