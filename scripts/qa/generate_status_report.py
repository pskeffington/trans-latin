#!/usr/bin/env python3
"""Generate a concise Trans-Latin repository status report."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class StatusReportGenerator:
    """Summarizes repository audit, corpus, translation, and release health."""

    def __init__(self, root: Path, output_path: Path) -> None:
        self.root = root
        self.output_path = output_path

    @staticmethod
    def _load_json(path: Path) -> dict[str, Any]:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def _count(self, pattern: str) -> int:
        return len([path for path in self.root.glob(pattern) if path.is_file()])

    def _translation_status_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for path in sorted((self.root / "translations").glob("*.json")):
            unit = self._load_json(path)
            status = str(unit.get("translation_status", "unknown"))
            counts[status] = counts.get(status, 0) + 1
        return counts

    def _handoff_status_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for path in sorted((self.root / "processing_handoffs").glob("*.json")):
            handoff = self._load_json(path)
            status = str(handoff.get("review_status", "unknown"))
            counts[status] = counts.get(status, 0) + 1
        return counts

    @staticmethod
    def _render_counts(counts: dict[str, int]) -> str:
        if not counts:
            return "- None"
        return "\n".join(f"- `{key}`: {value}" for key, value in sorted(counts.items()))

    def build(self) -> str:
        generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        sections = [
            "# Trans-Latin Status Report",
            "",
            f"Generated at UTC: `{generated_at}`",
            "",
            "## Object counts",
            "",
            f"- Witness records: {self._count('corpus/witnesses/*.json')}",
            f"- Translation records: {self._count('records/*.json')}",
            f"- Latin translation units: {self._count('translations/*.json')}",
            f"- Processing handoffs: {self._count('processing_handoffs/*.json')}",
            f"- Audit events: {self._count('audit/events/*.json')}",
            f"- Schemas: {self._count('schemas/*.json')}",
            f"- GitHub workflows: {self._count('.github/workflows/*.yml')}",
            "",
            "## Translation status counts",
            "",
            self._render_counts(self._translation_status_counts()),
            "",
            "## Processing handoff status counts",
            "",
            self._render_counts(self._handoff_status_counts()),
            "",
            "## Production commands",
            "",
            "```bash",
            "make qa",
            "make release-check",
            "```",
            "",
            "## Release artifacts",
            "",
            "- Review packet: `outputs/review/trans_latin_review_packet.md`",
            "- Audit manifest: `audit/manifests/TLA-MANIFEST-2026-000001.json`",
            "- Release bundle: `outputs/releases/trans-latin-audit-bundle/`",
            "",
        ]
        return "\n".join(sections)

    def write(self) -> None:
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_path.write_text(self.build(), encoding="utf-8")
        print(f"Wrote status report: {self.output_path}")


def main() -> int:
    StatusReportGenerator(Path("."), Path("outputs/review/trans_latin_status_report.md")).write()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
