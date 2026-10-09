from dataclasses import dataclass

from legacy_dbf_toolkit.schema_diff import compare_schemas


@dataclass(frozen=True)
class Field:
    name: str
    type: str
    length: int
    decimal_count: int = 0


def test_reports_added_removed_and_changed_fields():
    before = [Field("ID", "N", 8), Field("NAME", "C", 20), Field("OLD", "C", 5)]
    after = [Field("NAME", "C", 40), Field("NEW", "D", 8), Field("ID", "N", 8)]

    assert compare_schemas(before, after) == {
        "added": [{"name": "NEW", "type": "D", "length": 8, "decimal_count": 0}],
        "removed": [{"name": "OLD", "type": "C", "length": 5, "decimal_count": 0}],
        "changed": [{
            "before": {"name": "NAME", "type": "C", "length": 20, "decimal_count": 0},
            "after": {"name": "NAME", "type": "C", "length": 40, "decimal_count": 0},
        }],
    }


def test_ignores_order_and_field_name_case():
    before = [Field("customer_id", "N", 8), Field("Name", "C", 30)]
    after = [Field("NAME", "C", 30), Field("CUSTOMER_ID", "N", 8)]
    assert compare_schemas(before, after) == {"added": [], "removed": [], "changed": []}


def test_reports_decimal_precision_changes():
    result = compare_schemas([Field("PRICE", "N", 10, 2)], [Field("PRICE", "N", 10, 3)])
    assert len(result["changed"]) == 1


def test_empty_schemas_have_no_differences():
    assert compare_schemas([], []) == {"added": [], "removed": [], "changed": []}
