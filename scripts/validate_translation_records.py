#!/usr/bin/env python3
"""Validate Trans-Latin translation records for auditability.

The validator checks every JSON file under records/ against the project schema
and verifies that audit.checksum_sha256 equals the SHA-256 digest of the
canonical source_text + translation_text payload.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

try:
    import jsonschema
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing dependency: jsonschema. Install with `python -m pip install jsonschema`."
    ) from exc


class TranslationRecordValidator:
    """Validates translation records against schema and checksum rules."""

    def __init__(self, schema_path: Path, records_dir: Path) -> None:
        self.schema_path = schema_path
        self.records_dir = records_dir
        self.schema = self._load_json(schema_path)
        self.validator = jsonschema.Draft202012Validator(self.schema)

    @staticmethod
    def _load_json(path: Path) -> dict[str, Any]:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    @staticmethod
    def compute_checksum(source_text: str, translation_text: str) -> str:
        canonical_payload = json.dumps(
            {
                "source_text": source_text,
                "translation_text": translation_text,
            },
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(canonical_payload.encode("utf-8")).hexdigest()

    def validate_record(self, path: Path) -> list[str]:
        errors: list[str] = []
        try:
            record = self._load_json(path)
        except json.JSONDecodeError as exc:
            return [f"{path}: invalid JSON: {exc}"]

        for error in sorted(self.validator.iter_errors(record), key=str):
            location = ".".join(str(part) for part in error.absolute_path) or "<root>"
            errors.append(f"{path}: schema error at {location}: {error.message}")

        if not errors:
            expected = self.compute_checksum(
                record["source_text"],
                record["translation_text"],
            )
            observed = record["audit"]["checksum_sha256"]
            if observed != expected:
                errors.append(
                    f"{path}: checksum mismatch: expected {expected}, observed {observed}"
                )

        return errors

    def validate_all(self) -> int:
        record_paths = sorted(self.records_dir.glob("*.json"))
        if not record_paths:
            print(f"No translation records found in {self.records_dir}; nothing to validate.")
            return 0

        all_errors: list[str] = []
        for path in record_paths:
            all_errors.extend(self.validate_record(path))

        if all_errors:
            print("Translation record validation failed:", file=sys.stderr)
            for error in all_errors:
                print(f"- {error}", file=sys.stderr)
            return 1

        print(f"Validated {len(record_paths)} translation record(s).")
        return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Trans-Latin translation records.")
    parser.add_argument("--schema", default="schemas/translation_record.schema.json")
    parser.add_argument("--records", default="records")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    validator = TranslationRecordValidator(Path(args.schema), Path(args.records))
    return validator.validate_all()


if __name__ == "__main__":
    raise SystemExit(main())
