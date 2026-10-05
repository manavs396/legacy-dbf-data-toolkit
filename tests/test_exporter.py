import json
from legacy_dbf_toolkit.exporter import export_csv, export_json

def test_json_export(tmp_path):
    output = tmp_path / "records.json"
    export_json([{"ID": 1, "NAME": "Test"}], output)
    assert json.loads(output.read_text()) == [{"ID": 1, "NAME": "Test"}]

def test_csv_export(tmp_path):
    output = tmp_path / "records.csv"
    export_csv([{"ID": 1, "NAME": "Test"}], output)
    assert "ID,NAME" in output.read_text()
