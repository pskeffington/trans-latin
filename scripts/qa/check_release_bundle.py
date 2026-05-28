#!/usr/bin/env python3
"""Check that the Trans-Latin release bundle contains expected artifacts."""

from __future__ import annotations

import sys
from pathlib import Path


class ReleaseBundleChecker:
    """Verifies staged release-review bundle contents."""

    REQUIRED_FILES = [
        "trans_latin_review_packet.md",
        "trans_latin_status_report.md",
        "TLA-MANIFEST-2026-000001.json",
        "auditability-standard.md",
        "shared-translator-spine.md",
        "language-processing-repo-boundary.md",
    ]

    def __init__(self, bundle_dir: Path) -> None:
        self.bundle_dir = bundle_dir

    def check(self) -> int:
        missing = [name for name in self.REQUIRED_FILES if not (self.bundle_dir / name).is_file()]
        if missing:
            print("Release bundle check failed:", file=sys.stderr)
            for name in missing:
                print(f"- missing file: {self.bundle_dir / name}", file=sys.stderr)
            return 1
        print(f"Release bundle valid: {self.bundle_dir}")
        return 0


def main() -> int:
    return ReleaseBundleChecker(Path("outputs/releases/trans-latin-audit-bundle")).check()


if __name__ == "__main__":
    raise SystemExit(main())
