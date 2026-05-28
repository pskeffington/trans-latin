#!/usr/bin/env python3
"""Validate Trans-Latin audit manifests.

The audit manifest is a release-style inventory of important artifacts and their
file checksums. This validator checks schema validity, path existence, duplicate
paths, and SHA-256 digest accuracy.
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


class AuditManifestValidator:
    """Validates audit manifests against schema and file checksums."""

    def __init__(self, schema_path: Path, manifest_path: Path, root: Path) -> None:
        self.schema_path = schema_path
        self.manifest_path = manifest_path
        self.root = root
        self.schema = self._load_json(schema_path)
        self.validator = jsonschema.Draft202012Validator(self.schema)

    @staticmethod
    def _load_json(path: Path) -> dict[str, Any]:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    @staticmethod
    def file_checksum(path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(65536), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def validate(self) -> int:
        errors: list[str] = []
        try:
            manifest = self._load_json(self.manifest_path)
        except json.JSONDecodeError as exc:
            print(f"{self.manifest_path}: invalid JSON: {exc}", file=sys.stderr)
            return 1

        for error in sorted(self.validator.iter_errors(manifest), key=str):
            location = ".".join(str(part) for part in error.absolute_path) or "<root>"
            errors.append(f"schema error at {location}: {error.message}")

        seen_paths: set[str] = set()
        for artifact in manifest.get("artifacts", []):
            relative_path = artifact.get("path")
            if not isinstance(relative_path, str):
                continue
            if relative_path in seen_paths:
                errors.append(f"duplicate manifest artifact path: {relative_path}")
            seen_paths.add(relative_path)

            artifact_path = self.root / relative_path
            if not artifact_path.is_file():
                errors.append(f"manifest artifact not found: {relative_path}")
                continue
            expected = self.file_checksum(artifact_path)
            observed = artifact.get("checksum_sha256")
            if observed != expected:
                errors.append(
                    f"manifest checksum mismatch for {relative_path}: expected {expected}, observed {observed}"
                )

        if errors:
            print("Audit manifest validation failed:", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
            return 1

        print(f"Audit manifest valid: {len(manifest['artifacts'])} artifact(s).")
        return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a Trans-Latin audit manifest.")
    parser.add_argument("--schema", default="schemas/audit_manifest.schema.json")
    parser.add_argument("--manifest", default="audit/manifests/TLA-MANIFEST-2026-000001.json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    validator = AuditManifestValidator(Path(args.schema), Path(args.manifest), Path("."))
    return validator.validate()


if __name__ == "__main__":
    raise SystemExit(main())
