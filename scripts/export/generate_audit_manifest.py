#!/usr/bin/env python3
"""Generate a Trans-Latin audit manifest.

The manifest inventories important repository artifacts and records their file
SHA-256 checksums. It is intended for release/review snapshots and should be
validated by scripts/qa/validate_audit_manifest.py.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class AuditManifestGenerator:
    """Builds a deterministic audit manifest from repository files."""

    INCLUDED_GLOBS = [
        ("records/*.json", "translation_record"),
        ("translations/*.json", "latin_translation_unit"),
        ("processing_handoffs/*.json", "processing_handoff"),
        ("audit/events/*.json", "audit_event"),
        ("schemas/*.json", "schema"),
        ("docs/governance/*.md", "policy_document"),
        ("docs/methodology/*.md", "policy_document"),
        ("docs/architecture/*.md", "policy_document"),
        ("scripts/qa/*.py", "qa_script"),
        (".github/workflows/*.yml", "workflow"),
        ("Makefile", "makefile"),
    ]

    def __init__(self, root: Path, output_path: Path, manifest_id: str, pipeline_version: str) -> None:
        self.root = root
        self.output_path = output_path
        self.manifest_id = manifest_id
        self.pipeline_version = pipeline_version

    @staticmethod
    def file_checksum(path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(65536), b""):
                digest.update(chunk)
        return digest.hexdigest()

    @staticmethod
    def infer_object_id(path: Path) -> str:
        if path.suffix in {".json", ".md", ".yml", ".yaml", ".py"}:
            return path.stem
        return path.name

    def collect_artifacts(self) -> list[dict[str, str]]:
        artifacts: list[dict[str, str]] = []
        seen: set[str] = set()
        for pattern, artifact_type in self.INCLUDED_GLOBS:
            for path in sorted(self.root.glob(pattern)):
                if not path.is_file():
                    continue
                relative_path = path.relative_to(self.root).as_posix()
                if relative_path == self.output_path.as_posix():
                    continue
                if relative_path in seen:
                    continue
                seen.add(relative_path)
                artifacts.append(
                    {
                        "path": relative_path,
                        "artifact_type": artifact_type,
                        "object_id": self.infer_object_id(path),
                        "checksum_sha256": self.file_checksum(path),
                    }
                )
        return sorted(artifacts, key=lambda artifact: artifact["path"])

    def build_manifest(self) -> dict[str, Any]:
        return {
            "manifest_id": self.manifest_id,
            "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
            "pipeline_version": self.pipeline_version,
            "description": "Generated Trans-Latin audit manifest for release/review verification.",
            "artifacts": self.collect_artifacts(),
        }

    def write(self) -> None:
        manifest = self.build_manifest()
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"Wrote audit manifest with {len(manifest['artifacts'])} artifact(s): {self.output_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a Trans-Latin audit manifest.")
    parser.add_argument("--output", default="audit/manifests/TLA-MANIFEST-2026-000001.json")
    parser.add_argument("--manifest-id", default="TLA-MANIFEST-2026-000001")
    parser.add_argument("--pipeline-version", default="0.1.0")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    generator = AuditManifestGenerator(
        root=Path("."),
        output_path=Path(args.output),
        manifest_id=args.manifest_id,
        pipeline_version=args.pipeline_version,
    )
    generator.write()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
