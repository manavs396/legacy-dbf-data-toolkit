from legacy_dbf_toolkit.validation import validate_records

def test_required_field_detection():
    records = [{"CUSTOMER_ID": "1001", "NAME": "Asha"}, {"CUSTOMER_ID": "1002", "NAME": ""}]
    issues = validate_records(records, required_fields=["CUSTOMER_ID", "NAME"])
    assert len(issues) == 1
    assert issues[0].row_number == 2
    assert issues[0].field == "NAME"

def test_max_length_detection():
    issues = validate_records([{"NAME": "Alexander"}], max_lengths={"NAME": 5})
    assert len(issues) == 1


def test_required_fields_match_case_insensitively():
    assert validate_records([{"Name": "Asha"}], required_fields=["NAME"]) == []


def test_max_length_matches_case_insensitively():
    issues = validate_records([{"Email": "long@example.com"}], max_lengths={"EMAIL": 5})
    assert len(issues) == 1
    assert issues[0].field == "EMAIL"


def test_blank_required_field_still_detected():
    issues = validate_records([{"name": "  "}], required_fields=["NAME"])
    assert len(issues) == 1
