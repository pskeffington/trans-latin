#!/usr/bin/env python3
"""Validate Trans-Latin audit event records."""

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


class AuditEventValidator:
    """Validates audit-event schema, filenames, checksums, and object links."""

    OBJECT_PATHS = {
        "translation_record": Path("records"),
        "latin_translation_unit": Path("translations"),
        "processing_handoff": Path("processing_handoffs"),
        "policy_document": Path("docs"),
        "export_artifact": Path("outputs"),
        "repository": Path("."),
    }

    def __init__(self, schema_path: Path, events_dir: Path, root: Path) -> None:
        self.schema_path = schema_path
        self.events_dir = events_dir
        self.root = root
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
    def compute_event_checksum(cls, event: dict[str, Any]) -> str:
        event_without_checksum = json.loads(json.dumps(event, ensure_ascii=False))
        event_without_checksum["audit"].pop("event_checksum_sha256", None)
        return cls._checksum(event_without_checksum)

    def _object_exists(self, event: dict[str, Any]) -> bool:
        object_type = event["object_type"]
        object_id = event["object_id"]
        if object_type == "repository":
            return True
        if object_type == "policy_document":
            return (self.root / object_id).exists()
        base = self.OBJECT_PATHS[object_type]
        return (self.root / base / f"{object_id}.json").exists()

    def validate_event(self, path: Path) -> list[str]:
        errors: list[str] = []
        try:
            event = self._load_json(path)
        except json.JSONDecodeError as exc:
            return [f"{path}: invalid JSON: {exc}"]

        for error in sorted(self.validator.iter_errors(event), key=str):
            location = ".".join(str(part) for part in error.absolute_path) or "<root>"
            errors.append(f"{path}: schema error at {location}: {error.message}")

        if errors:
            return errors

        expected_name = f"{event['event_id']}.json"
        if path.name != expected_name:
            errors.append(f"{path}: filename must be {expected_name}")

        if not self._object_exists(event):
            errors.append(
                f"{path}: linked object not found for {event['object_type']}:{event['object_id']}"
            )

        expected_checksum = self.compute_event_checksum(event)
        observed_checksum = event["audit"]["event_checksum_sha256"]
        if observed_checksum != expected_checksum:
            errors.append(
                f"{path}: event checksum mismatch: expected {expected_checksum}, observed {observed_checksum}"
            )

        return errors

    def validate_all(self) -> int:
        paths = sorted(self.events_dir.glob("*.json"))
        if not paths:
            print(f"No audit events found in {self.events_dir}; nothing to validate.")
            return 0

        all_errors: list[str] = []
        for path in paths:
            all_errors.extend(self.validate_event(path))

        if all_errors:
            print("Audit event validation failed:", file=sys.stderr)
            for error in all_errors:
                print(f"- {error}", file=sys.stderr)
            return 1

        print(f"Validated {len(paths)} audit event(s).")
        return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Trans-Latin audit event records.")
    parser.add_argument("--schema", default="schemas/audit_event.schema.json")
    parser.add_argument("--events", default="audit/events")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    validator = AuditEventValidator(Path(args.schema), Path(args.events), Path("."))
    return validator.validate_all()


if __name__ == "__main__":
    raise SystemExit(main())
