#!/usr/bin/env python3
"""Block rights-sensitive source image files by default.

The translator projects should store metadata, official links, transcription,
translation, apparatus, and notes. Restricted source images should remain
link-only unless explicit clearance is documented.
"""

from __future__ import annotations

import sys
from pathlib import Path


class RightsSensitiveFileChecker:
    """Checks for image/PDF files in source-evidence paths."""

    BLOCKED_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".tif",
        ".tiff",
        ".webp",
        ".gif",
        ".bmp",
        ".pdf",
    }

    SCANNED_DIRECTORIES = [
        Path("corpus/images"),
        Path("corpus/witnesses"),
        Path("metadata"),
    ]

    ALLOWLIST = Path("metadata/source_image_allowlist.txt")

    def __init__(self, root: Path) -> None:
        self.root = root
        self.allowed_paths = self._load_allowlist()

    def _load_allowlist(self) -> set[str]:
        allowlist_path = self.root / self.ALLOWLIST
        if not allowlist_path.exists():
            return set()
        return {
            line.strip()
            for line in allowlist_path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        }

    def find_blocked_files(self) -> list[Path]:
        blocked: list[Path] = []
        for directory in self.SCANNED_DIRECTORIES:
            full_dir = self.root / directory
            if not full_dir.exists():
                continue
            for path in full_dir.rglob("*"):
                if not path.is_file():
                    continue
                relative = path.relative_to(self.root).as_posix()
                if relative in self.allowed_paths:
                    continue
                if path.suffix.lower() in self.BLOCKED_EXTENSIONS:
                    blocked.append(path.relative_to(self.root))
        return blocked

    def check(self) -> int:
        blocked = self.find_blocked_files()
        if blocked:
            print("Rights-sensitive source files found without allowlist clearance:", file=sys.stderr)
            for path in blocked:
                print(f"- {path}", file=sys.stderr)
            return 1
        print("No rights-sensitive source image/PDF files found in scanned paths.")
        return 0


def main() -> int:
    return RightsSensitiveFileChecker(Path(".")).check()


if __name__ == "__main__":
    raise SystemExit(main())
