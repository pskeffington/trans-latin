#!/usr/bin/env python3
"""Smoke-check the Trans-Latin Python package surface."""

from __future__ import annotations

import importlib
import sys


class PackageSmokeChecker:
    """Verifies that production package modules import cleanly."""

    REQUIRED_MODULES = [
        "trans_latin",
        "trans_latin.core.checksum",
        "trans_latin.cli.validate_records",
        "trans_latin.cli.validate_units",
    ]

    def check(self) -> int:
        errors: list[str] = []
        for module_name in self.REQUIRED_MODULES:
            try:
                importlib.import_module(module_name)
            except Exception as exc:  # pragma: no cover
                errors.append(f"{module_name}: import failed: {exc}")

        if errors:
            print("Package smoke check failed:", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
            return 1

        import trans_latin

        print(f"Package smoke check passed: trans_latin {trans_latin.__version__}")
        return 0


def main() -> int:
    return PackageSmokeChecker().check()


if __name__ == "__main__":
    raise SystemExit(main())
