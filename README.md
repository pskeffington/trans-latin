# Trans-Latin

Auditable Latin translation, witness, review, and release infrastructure for the broader translator ecosystem.

`trans-latin` is the scholarly translator layer. It preserves source provenance, witness identity, reviewed Latin translation units, processing handoffs, audit events, review packets, audit manifests, and release bundles. Mechanical language processing should live in a separate processing repository and enter this repo through documented handoff records.

## Current ecosystem update — 2026-06-28

`trans-latin` remains the accepted scholarly-record and audit-truth layer for Latin work while the shared `trans` processing package has moved into a bounded handoff architecture. The current operating boundary is:

```text
processing engines and bounded handoffs
  -> trans-latin processing_handoffs/
  -> accepted or rejected scholarly fields
  -> audit event
  -> review packet
  -> release manifest
```

For the five-repo translator ecosystem, this means `trans-latin` should treat outputs from `pskeffington/trans` as processor evidence only. Processor output is not automatically accepted translation truth. It must enter through documented processing handoff records and then be accepted, rejected, or superseded through the Latin audit chain.

Current documentation posture:

- keep `trans-latin` as the scholarly Latin authority
- keep mechanical normalization, tokenization, morphology, lexicon lookup, and batch processing outside this repo unless recorded as handoff evidence
- preserve witness-chain IDs, audit events, review packets, release manifests, and rights-sensitive blocking
- do not import raw source images, OCR dumps, page screenshots, private source bodies, credentials, or unbounded processor payloads

## Status

Production-shaped scaffold: active audit, QA, release, and packaging spine.

The repository currently supports:

```text
witness provenance
translation records
Latin translation units
processing handoffs
audit event ledger
audit-chain validation
audit manifest generation
review packet export
status report generation
release bundle staging/checking
rights-sensitive file blocking
package smoke testing
GitHub Actions QA
```

## Core principle

Every accepted translation must preserve the chain:

```text
source witness
  -> source text / diplomatic transcription
  -> normalized Latin
  -> token analysis
  -> processing handoff
  -> accepted or rejected fields
  -> literal translation
  -> interpretive translation
  -> audit event
  -> review packet
  -> release manifest
```

## Local quickstart

```bash
git clone https://github.com/pskeffington/trans-latin.git
cd trans-latin

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

make qa
make release-check
```

## Main commands

```bash
make qa             # full validation and generated review/audit artifacts
make release-check  # full QA plus release bundle staging and validation
```

Package smoke entrypoints after editable install:

```bash
python -m pip install -e .
trans-latin-validate-records
trans-latin-validate-units
```

## Repository layers

```text
schemas/                 JSON schemas for auditable objects
records/                 ledger-style translation records
translations/            witness-chain Latin translation units
corpus/witnesses/        source witness records
processing_handoffs/     processor-to-scholarship handoff records
audit/events/            audit event ledger
audit/manifests/         generated audit manifests
scripts/qa/              validators and health checks
scripts/export/          review, manifest, and release exporters
docs/architecture/       system architecture and repo-boundary documents
docs/governance/         auditability standard
docs/methodology/        Latin transcription and normalization policies
docs/operations/         release operations
outputs/review/          generated review packets and status reports
outputs/releases/        staged release bundles
src/trans_latin/         installable Python package scaffold
.github/workflows/       CI and release workflows
```

## Review artifacts

`make qa` generates:

```text
outputs/review/trans_latin_review_packet.md
outputs/review/trans_latin_status_report.md
audit/manifests/TLA-MANIFEST-2026-000001.json
```

`make release-check` stages:

```text
outputs/releases/trans-latin-audit-bundle/
```

The release workflow archives the bundle as:

```text
outputs/releases/trans-latin-audit-bundle.tar.gz
```

## Object IDs

Latin translation units use the shared translator witness-chain pattern:

```text
TLA-{collection}-{witness}-{folio_or_page}-{line_or_unit}
```

Example:

```text
TLA-DEMO-W01-P001-L001
```

Processing handoff and event objects use:

```text
TLA-HANDOFF-YYYY-NNNNNN
TLA-EVENT-YYYY-NNNNNN
TLA-MANIFEST-YYYY-NNNNNN
```

## Rights posture

Rights-sensitive source images and PDFs are blocked by default in source-evidence paths. The preferred source model is link-only unless explicit storage clearance is documented.

## Relationship to language processing

`trans-latin` owns accepted scholarly records and audit truth. A separate processing repository should own normalization, tokenization, morphology, lexicon lookup, and batch language-processing engines. Processor output must enter `trans-latin` through processing handoff records and be accepted, rejected, or superseded through the audit chain.

## Maintainer

Paul Skeffington, MS, MPH  
Dartmouth College  
GitHub: `@pskeffington-github`  
Public contact: `paulskeffington@gmail.com`
