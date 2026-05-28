# Trans-Latin Ecosystem

## Purpose

`trans-latin` is the auditable Latin scholarly-translation layer in the wider translator ecosystem. It is intentionally aligned with `Trans-heb` so Latin and Hebrew projects share a near-matching system shape, command vocabulary, object model, and audit posture.

## Operating model

```text
source metadata + witness links
  -> witness records
  -> source text / diplomatic transcription
  -> normalized Latin
  -> token and morphology records
  -> processing handoff records
  -> accepted/rejected scholarly fields
  -> translation units
  -> audit event ledger
  -> review packets
  -> audit manifests
  -> release bundles
```

## Repository role

`trans-latin` owns durable scholarly truth:

```text
witness provenance
reviewed translation units
audit events
review packets
release manifests
rights posture
publication-facing outputs
```

A separate language-processing repository should own reusable mechanics:

```text
normalization engines
tokenizers
morphology parsers
lexicon providers
alignment helpers
batch runners
processor APIs
```

Processor output enters `trans-latin` only through processing handoff records.

## Shared translator-system vocabulary

| System concept | Trans-heb | Trans-latin |
|---|---|---|
| Translation unit ID | `THB-{collection}-{witness}-{folio_or_page}-{line_or_unit}` | `TLA-{collection}-{witness}-{folio_or_page}-{line_or_unit}` |
| Witness registry | `corpus/witnesses/` | `corpus/witnesses/` |
| Translation units | `translations/` | `translations/` |
| QA scripts | `scripts/qa/` | `scripts/qa/` |
| Export scripts | `scripts/export/` | `scripts/export/` |
| Review outputs | `outputs/review/` | `outputs/review/` |
| Release outputs | `outputs/releases/` | `outputs/releases/` |
| Workflows | `.github/workflows/` | `.github/workflows/` |
| Release command | `make release-check` target pattern | `make release-check` |

## Production artifacts

The production-facing artifact set is:

```text
outputs/review/trans_latin_review_packet.md
outputs/review/trans_latin_status_report.md
audit/manifests/TLA-MANIFEST-2026-000001.json
outputs/releases/trans-latin-audit-bundle/
```

## CI surface

```text
Full QA Spine
Package Smoke
Release Artifacts
Translation Audit Pipeline
Latin Translation Unit Audit
```

## Design rule

When adding a new object or pipeline to `trans-latin`, first check whether `Trans-heb` already has a corresponding object boundary. Prefer the same directory, command, and review concept unless Latin requires a specific specialization.
