# Translator Project Auditability Standard

This standard applies to `trans-latin` and should remain aligned with the parallel translator projects, especially `Trans-heb`.

## Purpose

The translator projects must treat translation as an auditable scholarly workflow, not as a single generated text output. Every translation artifact should preserve provenance, method, review status, and reproducible validation evidence.

## Auditability requirements

A translation unit is not considered project-grade unless it preserves:

```text
source provenance
  -> source witness identity
  -> diplomatic transcription or source text capture
  -> normalization method
  -> tokenization method
  -> morphology / lexical analysis method
  -> literal translation
  -> interpretive translation
  -> uncertainty notes
  -> reviewer action
  -> export target
  -> validation status
```

## Required audit fields

Every translation record or translation unit should include the following audit fields directly or through linked objects:

```text
stable_id
collection_id
witness_id
source_reference
source_rights_status
source_capture_method
normalization_policy
translation_method
pipeline_version
created_at_utc
updated_at_utc
translator
reviewer
review_status
checksum_sha256
validation_status
notes
```

## Review states

Use a consistent review-state ladder across translator projects:

```text
draft
machine_checked
human_reviewed
approved
rejected
superseded
```

No public-facing export should be considered final unless the unit is `approved` or explicitly marked as a draft export.

## Checksum rule

Checksums must be deterministic and independently reproducible. At minimum, the checksum should cover:

```text
source_text
translation_text
```

For richer translation units, the checksum should eventually cover:

```text
source_text
normalized_source
literal_translation
interpretive_translation
apparatus_links
review_status
pipeline_version
```

## Source rights rule

Rights-sensitive source images should not be stored in the repository unless explicit permission is documented. The preferred default is link-only storage:

```text
repository stores metadata + official source link + transcription + notes
repository does not store restricted source image files by default
```

## Human review rule

A translation may be machine-assisted, but final scholarly status requires a named reviewer or a documented reason that review is pending.

## Supersession rule

Do not silently overwrite scholarly conclusions. If a translation is materially revised after review, preserve the older record in Git history and mark the current record with a supersession note where practical.

## CI rule

The CI pipeline must fail when:

```text
required audit fields are missing
record IDs are malformed
checksums do not match
review status is invalid
source language or target language is invalid
JSON or CSV records are malformed
rights-sensitive paths are introduced without clearance
```

## Cross-project alignment rule

Before creating a new object boundary in `trans-latin`, check whether `Trans-heb` already has a comparable object. Prefer shared names and shapes unless Latin requires a clear language-specific specialization.

## Minimum repository controls

The translator repositories should maintain:

```text
schemas/
scripts/qa/
scripts/normalize/
scripts/tokenize/
scripts/morphology/
scripts/export/
translations/
records/
metadata/
corpus/witnesses/
apparatus/
outputs/review/
outputs/latex/
outputs/releases/
.github/workflows/
Makefile
```

## Operational command surface

Use a shared command vocabulary across translator projects:

```bash
make qa
make audit
make vatican
make vatican-review
make sqlite
make sqlite-report
make release-check
```

`make qa` should remain the ordinary full local validation entry point.
