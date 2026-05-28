#!/usr/bin/env python3
"""Validate Trans-Latin Latin translation units.

This validator checks every JSON file under translations/ against the Latin
translation-unit schema and verifies the deterministic audit checksum.
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


class LatinTranslationUnitValidator:
    """Validates Latin translation units against schema and checksum rules."""

    def __init__(self, schema_path: Path, translations_dir: Path) -> None:
        self.schema_path = schema_path
        self.translations_dir = translations_dir
        self.schema = self._load_json(schema_path)
        self.validator = jsonschema.Draft202012Validator(self.schema)

    @staticmethod
    def _load_json(path: Path) -> dict[str, Any]:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    @staticmethod
    def compute_checksum(
        source_text: str,
        literal_translation: str,
        interpretive_translation: str,
    ) -> str:
        canonical_payload = json.dumps(
            {
                "interpretive_translation": interpretive_translation,
                "literal_translation": literal_translation,
                "source_text": source_text,
            },
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(canonical_payload.encode("utf-8")).hexdigest()

    def validate_unit(self, path: Path) -> list[str]:
        errors: list[str] = []
        try:
            unit = self._load_json(path)
        except json.JSONDecodeError as exc:
            return [f"{path}: invalid JSON: {exc}"]

        for error in sorted(self.validator.iter_errors(unit), key=str):
            location = ".".join(str(part) for part in error.absolute_path) or "<root>"
            errors.append(f"{path}: schema error at {location}: {error.message}")

        if not errors:
            expected = self.compute_checksum(
                unit["source_latin"],
                unit["literal_translation"],
                unit["interpretive_translation"],
            )
            observed = unit["audit"]["checksum_sha256"]
            if observed != expected:
                errors.append(
                    f"{path}: checksum mismatch: expected {expected}, observed {observed}"
                )

        return errors

    def validate_all(self) -> int:
        unit_paths = sorted(self.translations_dir.glob("*.json"))
        if not unit_paths:
            print(f"No Latin translation units found in {self.translations_dir}; nothing to validate.")
            return 0

        all_errors: list[str] = []
        for path in unit_paths:
            all_errors.extend(self.validate_unit(path))

        if all_errors:
            print("Latin translation-unit validation failed:", file=sys.stderr)
            for error in all_errors:
                print(f"- {error}", file=sys.stderr)
            return 1

        print(f"Validated {len(unit_paths)} Latin translation unit(s).")
        return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Trans-Latin Latin translation units.")
    parser.add_argument("--schema", default="schemas/latin_translation_unit.schema.json")
    parser.add_argument("--translations", default="translations")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    validator = LatinTranslationUnitValidator(Path(args.schema), Path(args.translations))
    return validator.validate_all()


if __name__ == "__main__":
    raise SystemExit(main())
