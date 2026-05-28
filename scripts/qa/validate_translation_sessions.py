#!/usr/bin/env python3
"""Validate synchronous Trans-Latin translation sessions."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import jsonschema
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Missing dependency: jsonschema. Install with `python -m pip install jsonschema`.") from exc


class TranslationSessionValidator:
    """Validates session schema, checksums, object links, and action order."""

    def __init__(self, schema_path: Path, sessions_dir: Path, root: Path) -> None:
        self.schema_path = schema_path
        self.sessions_dir = sessions_dir
        self.root = root
        self.schema = self._load_json(schema_path)
        self.validator = jsonschema.Draft202012Validator(self.schema)

    @staticmethod
    def _load_json(path: Path) -> dict[str, Any]:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    @staticmethod
    def _parse_time(value: str) -> datetime:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))

    @staticmethod
    def _checksum(value: Any) -> str:
        payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    @classmethod
    def session_checksum(cls, session: dict[str, Any]) -> str:
        value = json.loads(json.dumps(session, ensure_ascii=False))
        value["audit"].pop("session_checksum_sha256", None)
        return cls._checksum(value)

    def _object_exists(self, object_type: str, object_id: str) -> bool:
        if object_type == "witness":
            return (self.root / "corpus/witnesses" / f"{object_id}.json").is_file()
        if object_type == "translation_record":
            return (self.root / "records" / f"{object_id}.json").is_file()
        if object_type == "latin_translation_unit":
            return (self.root / "translations" / f"{object_id}.json").is_file()
        if object_type == "processing_handoff":
            return (self.root / "processing_handoffs" / f"{object_id}.json").is_file()
        if object_type == "audit_event":
            return (self.root / "audit/events" / f"{object_id}.json").is_file()
        if object_type in {"review_packet", "status_report", "repository"}:
            return True
        return False

    def validate_session(self, path: Path) -> list[str]:
        errors: list[str] = []
        try:
            session = self._load_json(path)
        except json.JSONDecodeError as exc:
            return [f"{path}: invalid JSON: {exc}"]

        for error in sorted(self.validator.iter_errors(session), key=str):
            location = ".".join(str(part) for part in error.absolute_path) or "<root>"
            errors.append(f"{path}: schema error at {location}: {error.message}")

        if errors:
            return errors

        expected_name = f"{session['session_id']}.json"
        if path.name != expected_name:
            errors.append(f"{path}: filename must be {expected_name}")

        expected_checksum = self.session_checksum(session)
        observed_checksum = session["audit"]["session_checksum_sha256"]
        if observed_checksum != expected_checksum:
            errors.append(
                f"{path}: session checksum mismatch: expected {expected_checksum}, observed {observed_checksum}"
            )

        action_times = []
        action_ids = set()
        for action in session["actions"]:
            action_id = action["action_id"]
            if action_id in action_ids:
                errors.append(f"{path}: duplicate action_id {action_id}")
            action_ids.add(action_id)
            action_times.append(self._parse_time(action["created_at_utc"]))
            if not self._object_exists(action["object_type"], action["object_id"]):
                errors.append(
                    f"{path}: action {action_id} links missing object {action['object_type']}:{action['object_id']}"
                )

        if action_times != sorted(action_times):
            errors.append(f"{path}: actions are not in chronological order")

        target_units = set(session.get("target_units", []))
        action_unit_ids = {
            action["object_id"]
            for action in session["actions"]
            if action["object_type"] == "latin_translation_unit"
        }
        missing_target_actions = target_units - action_unit_ids
        for unit_id in sorted(missing_target_actions):
            errors.append(f"{path}: target unit has no session action: {unit_id}")

        return errors

    def validate_all(self) -> int:
        paths = sorted(self.sessions_dir.glob("*.json"))
        if not paths:
            print(f"No translation sessions found in {self.sessions_dir}; nothing to validate.")
            return 0

        errors: list[str] = []
        for path in paths:
            errors.extend(self.validate_session(path))

        if errors:
            print("Translation session validation failed:", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
            return 1

        print(f"Validated {len(paths)} translation session(s).")
        return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Trans-Latin translation sessions.")
    parser.add_argument("--schema", default="schemas/translation_session.schema.json")
    parser.add_argument("--sessions", default="audit/sessions")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return TranslationSessionValidator(Path(args.schema), Path(args.sessions), Path(".")).validate_all()


if __name__ == "__main__":
    raise SystemExit(main())
