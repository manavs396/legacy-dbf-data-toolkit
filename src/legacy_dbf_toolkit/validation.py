from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class ValidationIssue:
    row_number: int
    field: str
    message: str

def validate_records(records: list[dict[str, Any]], required_fields=None, max_lengths=None):
    required_fields = required_fields or []
    max_lengths = max_lengths or {}
    issues = []
    for row_number, record in enumerate(records, start=1):
        # FoxPro field names are case-insensitive; reject ambiguous transformed rows.
        values_by_field = {}
        for name, value in record.items():
            normalized = name.upper()
            if normalized in values_by_field:
                raise ValueError(f"Row {row_number} contains duplicate field name (ignoring case): {name}")
            values_by_field[normalized] = value
        for field in required_fields:
            value = values_by_field.get(field.upper())
            if value is None or (isinstance(value, str) and not value.strip()):
                issues.append(ValidationIssue(row_number, field, "Required value is missing"))
        for field, maximum in max_lengths.items():
            value = values_by_field.get(field.upper())
            if value is not None and len(str(value)) > maximum:
                issues.append(ValidationIssue(row_number, field, f"Value exceeds maximum length of {maximum}"))
    return issues
