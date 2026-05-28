#!/usr/bin/env python3
"""Verify that the Trans-Latin repository spine exists.

This keeps Trans-Latin aligned with the shared translator-project backbone used
by Trans-heb while allowing Latin-specific implementation details to evolve.
"""

from __future__ import annotations

import sys
from pathlib import Path


class RequiredSpineChecker:
    """Checks required directories and anchor files for the translator spine."""

    REQUIRED_DIRECTORIES = [
        "schemas",
        "scripts/qa",
        "scripts/normalize",
        "scripts/tokenize",
        "scripts/morphology",
        "scripts/export",
        "translations",
        "records",
        "processing_handoffs",
        "audit/events",
        "audit/manifests",
        "metadata",
        "corpus/registry",
        "corpus/witnesses",
        "corpus/images",
        "apparatus",
        "outputs/review",
        "outputs/latex",
        "outputs/releases",
        "docs/architecture",
        "docs/governance",
        "docs/methodology",
        ".github/workflows",
    ]

    REQUIRED_FILES = [
        "Makefile",
        "requirements.txt",
        "schemas/translation_record.schema.json",
        "schemas/latin_translation_unit.schema.json",
        "schemas/processing_handoff.schema.json",
        "schemas/audit_event.schema.json",
        "schemas/audit_manifest.schema.json",
        "scripts/validate_translation_records.py",
        "scripts/qa/validate_latin_translation_units.py",
        "scripts/qa/validate_processing_handoffs.py",
        "scripts/qa/validate_audit_events.py",
        "scripts/qa/validate_audit_manifest.py",
        "scripts/qa/check_audit_chain.py",
        "scripts/export/generate_audit_manifest.py",
        "docs/architecture/shared-translator-spine.md",
        "docs/architecture/language-processing-repo-boundary.md",
        "docs/governance/auditability-standard.md",
        "docs/methodology/latin_transcription_policy.md",
        "docs/methodology/latin_normalization_policy.md",
    ]

    def __init__(self, root: Path) -> None:
        self.root = root

    def check(self) -> int:
        missing_dirs = [path for path in self.REQUIRED_DIRECTORIES if not (self.root / path).is_dir()]
        missing_files = [path for path in self.REQUIRED_FILES if not (self.root / path).is_file()]

        if missing_dirs or missing_files:
            print("Required translator spine check failed:", file=sys.stderr)
            for path in missing_dirs:
                print(f"- missing directory: {path}", file=sys.stderr)
            for path in missing_files:
                print(f"- missing file: {path}", file=sys.stderr)
            return 1

        print("Required translator spine is present.")
        return 0


def main() -> int:
    return RequiredSpineChecker(Path(".")).check()


if __name__ == "__main__":
    raise SystemExit(main())
