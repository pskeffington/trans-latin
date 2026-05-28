#!/usr/bin/env python3
"""Validate processing handoff records for Trans-Latin.

Processing handoffs preserve the boundary between a reusable language-processing
repo and the scholarly translation repository. This validator checks schema
validity, recomputes payload checksums, recomputes full handoff checksums, and
verifies that every handoff points to an existing translation unit.
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


class ProcessingHandoffValidator:
    """Validates processing handoff records and cross-links."""

    def __init__(self, schema_path: Path, handoffs_dir: Path, translations_dir: Path) -> None:
        self.schema_path = schema_path
        self.handoffs_dir = handoffs_dir
        self.translations_dir = translations_dir
        self.schema = self._load_json(schema_path)
        self.validator = jsonschema.Draft202012Validator(self.schema)

    @staticmethod
    def _load_json(path: Path) -> dict[str, Any]:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    @staticmethod
    def _checksum(value: Any) -> str:
        canonical_payload = json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(canonical_payload.encode("utf-8")).hexdigest()

    @classmethod
    def compute_payload_checksum(cls, handoff: dict[str, Any]) -> str:
        return cls._checksum(handoff["source_payload"])

    @classmethod
    def compute_handoff_checksum(cls, handoff: dict[str, Any]) -> str:
        handoff_without_checksum = json.loads(json.dumps(handoff, ensure_ascii=False))
        handoff_without_checksum["audit"].pop("handoff_checksum_sha256", None)
        return cls._checksum(handoff_without_checksum)

    def validate_handoff(self, path: Path) -> list[str]:
        errors: list[str] = []
        try:
            handoff = self._load_json(path)
        except json.JSONDecodeError as exc:
            return [f"{path}: invalid JSON: {exc}"]

        for error in sorted(self.validator.iter_errors(handoff), key=str):
            location = ".".join(str(part) for part in error.absolute_path) or "<root>"
            errors.append(f"{path}: schema error at {location}: {error.message}")

        if errors:
            return errors

        expected_name = f"{handoff['handoff_id']}.json"
        if path.name != expected_name:
            errors.append(f"{path}: filename must be {expected_name}")

        translation_path = self.translations_dir / f"{handoff['unit_id']}.json"
        if not translation_path.exists():
            errors.append(f"{path}: linked translation unit not found: {translation_path}")

        expected_payload_checksum = self.compute_payload_checksum(handoff)
        observed_payload_checksum = handoff["audit"]["payload_checksum_sha256"]
        if observed_payload_checksum != expected_payload_checksum:
            errors.append(
                f"{path}: payload checksum mismatch: expected {expected_payload_checksum}, observed {observed_payload_checksum}"
            )

        expected_handoff_checksum = self.compute_handoff_checksum(handoff)
        observed_handoff_checksum = handoff["audit"]["handoff_checksum_sha256"]
        if observed_handoff_checksum != expected_handoff_checksum:
            errors.append(
                f"{path}: handoff checksum mismatch: expected {expected_handoff_checksum}, observed {observed_handoff_checksum}"
            )

        return errors

    def validate_all(self) -> int:
        handoff_paths = sorted(self.handoffs_dir.glob("*.json"))
        if not handoff_paths:
            print(f"No processing handoffs found in {self.handoffs_dir}; nothing to validate.")
            return 0

        all_errors: list[str] = []
        for path in handoff_paths:
            all_errors.extend(self.validate_handoff(path))

        if all_errors:
            print("Processing handoff validation failed:", file=sys.stderr)
            for error in all_errors:
                print(f"- {error}", file=sys.stderr)
            return 1

        print(f"Validated {len(handoff_paths)} processing handoff record(s).")
        return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Trans-Latin processing handoffs.")
    parser.add_argument("--schema", default="schemas/processing_handoff.schema.json")
    parser.add_argument("--handoffs", default="processing_handoffs")
    parser.add_argument("--translations", default="translations")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    validator = ProcessingHandoffValidator(
        Path(args.schema),
        Path(args.handoffs),
        Path(args.translations),
    )
    return validator.validate_all()


if __name__ == "__main__":
    raise SystemExit(main())
