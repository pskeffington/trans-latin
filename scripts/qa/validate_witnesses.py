#!/usr/bin/env python3
"""Validate Trans-Latin witness records."""

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
    raise SystemExit("Missing dependency: jsonschema. Install with `python -m pip install jsonschema`.") from exc


class WitnessValidator:
    """Validates witness records, checksums, and filename conventions."""

    def __init__(self, schema_path: Path, witnesses_dir: Path) -> None:
        self.schema_path = schema_path
        self.witnesses_dir = witnesses_dir
        self.schema = self._load_json(schema_path)
        self.validator = jsonschema.Draft202012Validator(self.schema)

    @staticmethod
    def _load_json(path: Path) -> dict[str, Any]:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    @staticmethod
    def checksum(witness: dict[str, Any]) -> str:
        value = json.loads(json.dumps(witness, ensure_ascii=False))
        value["audit"].pop("checksum_sha256", None)
        payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def validate_file(self, path: Path) -> list[str]:
        errors: list[str] = []
        try:
            witness = self._load_json(path)
        except json.JSONDecodeError as exc:
            return [f"{path}: invalid JSON: {exc}"]

        for error in sorted(self.validator.iter_errors(witness), key=str):
            location = ".".join(str(part) for part in error.absolute_path) or "<root>"
            errors.append(f"{path}: schema error at {location}: {error.message}")

        if errors:
            return errors

        expected_name = f"{witness['collection_id']}-{witness['witness_id']}.json"
        if path.name != expected_name:
            errors.append(f"{path}: filename must be {expected_name}")

        expected_checksum = self.checksum(witness)
        observed_checksum = witness["audit"]["checksum_sha256"]
        if expected_checksum != observed_checksum:
            errors.append(
                f"{path}: checksum mismatch: expected {expected_checksum}, observed {observed_checksum}"
            )

        return errors

    def validate_all(self) -> int:
        paths = sorted(self.witnesses_dir.glob("*.json"))
        if not paths:
            print(f"No witness records found in {self.witnesses_dir}; nothing to validate.")
            return 0

        errors: list[str] = []
        seen: set[tuple[str, str]] = set()
        for path in paths:
            file_errors = self.validate_file(path)
            errors.extend(file_errors)
            if not file_errors:
                witness = self._load_json(path)
                key = (witness["collection_id"], witness["witness_id"])
                if key in seen:
                    errors.append(f"{path}: duplicate witness key {key}")
                seen.add(key)

        if errors:
            print("Witness validation failed:", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
            return 1

        print(f"Validated {len(paths)} witness record(s).")
        return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Trans-Latin witness records.")
    parser.add_argument("--schema", default="schemas/witness.schema.json")
    parser.add_argument("--witnesses", default="corpus/witnesses")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return WitnessValidator(Path(args.schema), Path(args.witnesses)).validate_all()


if __name__ == "__main__":
    raise SystemExit(main())
