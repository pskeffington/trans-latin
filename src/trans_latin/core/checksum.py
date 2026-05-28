"""Checksum utilities for Trans-Latin audit objects."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


class ChecksumService:
    """Computes deterministic SHA-256 checksums for files and JSON objects."""

    @staticmethod
    def json_checksum(value: Any) -> str:
        canonical_payload = json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(canonical_payload.encode("utf-8")).hexdigest()

    @staticmethod
    def file_checksum(path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(65536), b""):
                digest.update(chunk)
        return digest.hexdigest()
