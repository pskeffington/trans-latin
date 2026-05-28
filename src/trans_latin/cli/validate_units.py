"""CLI wrapper for Latin translation-unit validation."""

from __future__ import annotations

import subprocess
import sys


def main() -> int:
    return subprocess.call([sys.executable, "scripts/qa/validate_latin_translation_units.py"])


if __name__ == "__main__":
    raise SystemExit(main())
