"""CLI wrapper for translation-record validation."""

from __future__ import annotations

import subprocess
import sys


def main() -> int:
    return subprocess.call([sys.executable, "scripts/validate_translation_records.py"])


if __name__ == "__main__":
    raise SystemExit(main())
