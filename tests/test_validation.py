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
