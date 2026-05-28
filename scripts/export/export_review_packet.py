#!/usr/bin/env python3
"""Export a Markdown review packet for Trans-Latin translation units."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class ReviewPacketExporter:
    """Builds a human-readable review packet from translation units and witnesses."""

    def __init__(self, translations_dir: Path, witnesses_dir: Path, output_path: Path) -> None:
        self.translations_dir = translations_dir
        self.witnesses_dir = witnesses_dir
        self.output_path = output_path

    @staticmethod
    def _load_json(path: Path) -> dict[str, Any]:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def _load_witnesses(self) -> dict[tuple[str, str], dict[str, Any]]:
        witnesses: dict[tuple[str, str], dict[str, Any]] = {}
        for path in sorted(self.witnesses_dir.glob("*.json")):
            witness = self._load_json(path)
            witnesses[(witness["collection_id"], witness["witness_id"])] = witness
        return witnesses

    @staticmethod
    def _render_tokens(unit: dict[str, Any]) -> str:
        rows = ["| Surface | Lemma | POS | Morphology | Gloss |", "|---|---|---|---|---|"]
        for token in unit.get("tokens", []):
            rows.append(
                "| {surface} | {lemma} | {pos} | {morphology} | {gloss} |".format(
                    surface=token.get("surface", ""),
                    lemma=token.get("lemma", ""),
                    pos=token.get("pos", ""),
                    morphology=token.get("morphology", ""),
                    gloss=token.get("gloss", ""),
                )
            )
        return "\n".join(rows)

    def build(self) -> str:
        witnesses = self._load_witnesses()
        generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        sections = [
            "# Trans-Latin Review Packet",
            "",
            f"Generated at UTC: `{generated_at}`",
            "",
            "This packet is generated from repository JSON objects and is intended for human scholarly review.",
            "",
        ]

        for path in sorted(self.translations_dir.glob("*.json")):
            unit = self._load_json(path)
            witness = witnesses.get((unit["collection_id"], unit["witness_id"]), {})
            sections.extend(
                [
                    f"## {unit['unit_id']}",
                    "",
                    f"**Collection:** `{unit['collection_id']}`  ",
                    f"**Witness:** `{unit['witness_id']}`  ",
                    f"**Witness title:** {witness.get('title', 'UNKNOWN')}  ",
                    f"**Repository:** {witness.get('repository', 'UNKNOWN')}  ",
                    f"**Rights:** {witness.get('rights_status', 'UNKNOWN')}  ",
                    f"**Line reference:** `{unit['line_reference']}`  ",
                    f"**Status:** `{unit['translation_status']}`  ",
                    f"**Reviewer:** `{unit.get('reviewer')}`  ",
                    "",
                    "### Source Latin",
                    "",
                    unit["source_latin"],
                    "",
                    "### Normalized Latin",
                    "",
                    unit["normalized_latin"],
                    "",
                    "### Token analysis",
                    "",
                    self._render_tokens(unit),
                    "",
                    "### Literal translation",
                    "",
                    unit["literal_translation"],
                    "",
                    "### Interpretive translation",
                    "",
                    unit["interpretive_translation"],
                    "",
                    "### Notes",
                    "",
                    "\n".join(f"- {note}" for note in unit.get("notes", [])) or "- None",
                    "",
                    "---",
                    "",
                ]
            )
        return "\n".join(sections)

    def write(self) -> None:
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_path.write_text(self.build(), encoding="utf-8")
        print(f"Wrote review packet: {self.output_path}")


def main() -> int:
    ReviewPacketExporter(
        translations_dir=Path("translations"),
        witnesses_dir=Path("corpus/witnesses"),
        output_path=Path("outputs/review/trans_latin_review_packet.md"),
    ).write()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
