#!/usr/bin/env python3
"""Check Trans-Latin translation-unit ID integrity."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


class UnitIdChecker:
    """Validates Latin translation unit IDs and filename alignment."""

    UNIT_ID_PATTERN = re.compile(r"^TLA-[A-Z0-9]+-[A-Z0-9]+-[A-Z0-9]+-[A-Z0-9]+$")

    def __init__(self, translations_dir: Path) -> None:
        self.translations_dir = translations_dir

    @staticmethod
    def _load_json(path: Path) -> dict[str, Any]:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def check_file(self, path: Path) -> list[str]:
        errors: list[str] = []
        try:
            unit = self._load_json(path)
        except json.JSONDecodeError as exc:
            return [f"{path}: invalid JSON: {exc}"]

        unit_id = unit.get("unit_id")
        if not isinstance(unit_id, str):
            return [f"{path}: missing or non-string unit_id"]

        if not self.UNIT_ID_PATTERN.match(unit_id):
            errors.append(f"{path}: malformed unit_id {unit_id!r}")

        expected_name = f"{unit_id}.json"
        if path.name != expected_name:
            errors.append(f"{path}: filename must be {expected_name}")

        parts = unit_id.split("-")
        if len(parts) == 5:
            _, collection_id, witness_id, folio_or_page, line_or_unit = parts
            if unit.get("collection_id") != collection_id:
                errors.append(f"{path}: collection_id does not match unit_id")
            if unit.get("witness_id") != witness_id:
                errors.append(f"{path}: witness_id does not match unit_id")
            line_reference = unit.get("line_reference", "")
            if folio_or_page not in line_reference or line_or_unit not in line_reference:
                errors.append(f"{path}: line_reference should include {folio_or_page}-{line_or_unit}")

        return errors

    def check_all(self) -> int:
        paths = sorted(self.translations_dir.glob("*.json"))
        if not paths:
            print(f"No translation units found in {self.translations_dir}; nothing to validate.")
            return 0

        errors: list[str] = []
        seen: set[str] = set()
        for path in paths:
            file_errors = self.check_file(path)
            errors.extend(file_errors)
            if not file_errors:
                unit_id = self._load_json(path)["unit_id"]
                if unit_id in seen:
                    errors.append(f"{path}: duplicate unit_id {unit_id}")
                seen.add(unit_id)

        if errors:
            print("Unit ID validation failed:", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
            return 1

        print(f"Validated {len(paths)} unit ID(s).")
        return 0


def main() -> int:
    return UnitIdChecker(Path("translations")).check_all()


if __name__ == "__main__":
    raise SystemExit(main())
