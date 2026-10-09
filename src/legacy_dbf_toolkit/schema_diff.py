"""Compare DBF field metadata before a legacy-table migration."""

from dataclasses import asdict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .reader import FieldInfo


def compare_schemas(before: list["FieldInfo"], after: list["FieldInfo"]) -> dict:
    """Report added, removed, and changed fields (DBF names are case-insensitive).

    Field changes cover type, length, and decimal precision. Output is sorted by
    field name for stable reporting, regardless of the DBF column order.
    """
    old = {field.name.upper(): field for field in before}
    new = {field.name.upper(): field for field in after}

    added = [asdict(new[name]) for name in sorted(new.keys() - old.keys())]
    removed = [asdict(old[name]) for name in sorted(old.keys() - new.keys())]
    changed = [
        {"before": asdict(old[name]), "after": asdict(new[name])}
        for name in sorted(old.keys() & new.keys())
        if (old[name].type, old[name].length, old[name].decimal_count)
        != (new[name].type, new[name].length, new[name].decimal_count)
    ]
    return {"added": added, "removed": removed, "changed": changed}
