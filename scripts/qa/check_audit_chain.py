#!/usr/bin/env python3
"""Check end-to-end Trans-Latin audit-chain consistency.

This validator checks relationships across translation units, processing
handoffs, and audit events. It verifies that accepted processor output fields
match the current translation unit and that every handoff has an event entry.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


class AuditChainChecker:
    """Checks cross-object consistency for the audit chain."""

    def __init__(
        self,
        translations_dir: Path,
        handoffs_dir: Path,
        events_dir: Path,
    ) -> None:
        self.translations_dir = translations_dir
        self.handoffs_dir = handoffs_dir
        self.events_dir = events_dir

    @staticmethod
    def _load_json(path: Path) -> dict[str, Any]:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def _load_objects_by_id(self, directory: Path, id_field: str) -> dict[str, dict[str, Any]]:
        objects: dict[str, dict[str, Any]] = {}
        for path in sorted(directory.glob("*.json")):
            obj = self._load_json(path)
            object_id = obj.get(id_field)
            if isinstance(object_id, str):
                objects[object_id] = obj
        return objects

    @staticmethod
    def _values_match(left: Any, right: Any) -> bool:
        return left == right

    def _check_accepted_fields(
        self,
        handoff: dict[str, Any],
        unit: dict[str, Any],
        errors: list[str],
    ) -> None:
        handoff_id = handoff["handoff_id"]
        payload = handoff["source_payload"]

        field_map = {
            "source_latin": "source_latin",
            "normalized_latin": "normalized_latin",
            "tokens": "tokens",
        }

        for field in handoff.get("accepted_fields", []):
            if field not in field_map:
                errors.append(f"{handoff_id}: accepted field is not chain-checkable: {field}")
                continue
            unit_field = field_map[field]
            if field not in payload:
                errors.append(f"{handoff_id}: accepted field missing from source_payload: {field}")
                continue
            if unit_field not in unit:
                errors.append(f"{handoff_id}: linked unit missing accepted field: {unit_field}")
                continue
            if not self._values_match(payload[field], unit[unit_field]):
                errors.append(
                    f"{handoff_id}: accepted field {field} does not match linked unit field {unit_field}"
                )

        overlap = set(handoff.get("accepted_fields", [])) & set(handoff.get("rejected_fields", []))
        for field in sorted(overlap):
            errors.append(f"{handoff_id}: field cannot be both accepted and rejected: {field}")

    def check(self) -> int:
        errors: list[str] = []
        units = self._load_objects_by_id(self.translations_dir, "unit_id")
        handoffs = self._load_objects_by_id(self.handoffs_dir, "handoff_id")
        events = self._load_objects_by_id(self.events_dir, "event_id")

        handoffs_by_unit: dict[str, list[str]] = {}
        for handoff_id, handoff in handoffs.items():
            unit_id = handoff.get("unit_id")
            if unit_id not in units:
                errors.append(f"{handoff_id}: linked unit missing: {unit_id}")
                continue
            handoffs_by_unit.setdefault(unit_id, []).append(handoff_id)
            self._check_accepted_fields(handoff, units[unit_id], errors)

        for unit_id in sorted(units):
            if unit_id not in handoffs_by_unit:
                errors.append(f"{unit_id}: no processing handoff linked to translation unit")

        event_object_ids = {
            event.get("object_id")
            for event in events.values()
            if event.get("object_type") == "processing_handoff"
        }
        for handoff_id in sorted(handoffs):
            if handoff_id not in event_object_ids:
                errors.append(f"{handoff_id}: no audit event references this handoff")

        if errors:
            print("Audit chain validation failed:", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
            return 1

        print(
            f"Audit chain valid: {len(units)} unit(s), {len(handoffs)} handoff(s), {len(events)} event(s)."
        )
        return 0


def main() -> int:
    return AuditChainChecker(
        Path("translations"),
        Path("processing_handoffs"),
        Path("audit/events"),
    ).check()


if __name__ == "__main__":
    raise SystemExit(main())
