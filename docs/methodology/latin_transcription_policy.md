# Latin Diplomatic Transcription Policy

## Purpose

This policy defines the first-stage source capture rules for Latin materials in `trans-latin`. It should remain structurally parallel to the Hebrew diplomatic transcription policy in `Trans-heb`, while preserving Latin-specific paleographic and editorial needs.

## Core rule

Diplomatic transcription records what the witness presents before interpretive normalization. The project should not silently modernize spelling, punctuation, abbreviations, lineation, scribal marks, or uncertain readings.

## Required transcription fields

```text
unit_id
collection_id
witness_id
folio_or_page
line_reference
source_latin
transcription_notes
uncertainty_flags
source_reference
source_rights_status
transcriber
review_status
```

## Abbreviations

Expanded abbreviations must be marked in notes or apparatus. The diplomatic field should preserve the visible witness form when practical, while normalized fields may carry expanded forms.

## Damaged or uncertain text

Uncertain readings must be flagged. Do not present conjectural text as certain source text.

## Lineation

Line and folio/page references must remain stable enough to map back to the source witness. Translation-unit IDs should follow:

```text
TLA-{collection}-{witness}-{folio_or_page}-{line_or_unit}
```

## Source images

Rights-sensitive source images are link-only by default. The repository stores official links, metadata, transcription, translation, apparatus, and review outputs unless explicit image-storage clearance is documented.
