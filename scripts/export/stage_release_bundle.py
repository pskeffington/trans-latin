#!/usr/bin/env python3
"""Stage the Trans-Latin release audit bundle locally or in CI."""

from __future__ import annotations

import shutil
from pathlib import Path


class ReleaseBundleStager:
    """Copies review and audit artifacts into the release bundle directory."""

    REQUIRED_SOURCES = [
        Path("outputs/review/trans_latin_review_packet.md"),
        Path("outputs/review/trans_latin_status_report.md"),
        Path("audit/manifests/TLA-MANIFEST-2026-000001.json"),
        Path("docs/governance/auditability-standard.md"),
        Path("docs/architecture/shared-translator-spine.md"),
        Path("docs/architecture/language-processing-repo-boundary.md"),
    ]

    def __init__(self, bundle_dir: Path) -> None:
        self.bundle_dir = bundle_dir

    def stage(self) -> None:
        self.bundle_dir.mkdir(parents=True, exist_ok=True)
        for source in self.REQUIRED_SOURCES:
            if not source.is_file():
                raise FileNotFoundError(f"Required release source not found: {source}")
            shutil.copy2(source, self.bundle_dir / source.name)
        print(f"Staged release bundle: {self.bundle_dir}")


def main() -> int:
    ReleaseBundleStager(Path("outputs/releases/trans-latin-audit-bundle")).stage()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
