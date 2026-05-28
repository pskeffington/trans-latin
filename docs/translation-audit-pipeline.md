# Translation Audit Pipeline

Trans-Latin now has a live, auditable translation pipeline using GitHub Actions.

## Workflow

```text
.github/workflows/translation-audit.yml
```

The workflow runs on:

- pushes to `main`
- pull requests into `main`
- manual `workflow_dispatch`

## Validation contract

Every translation record in `records/*.json` is validated against:

```text
schemas/translation_record.schema.json
```

The validator also verifies that the audit checksum is correct.

## Validator

```text
scripts/validate_translation_records.py
```

The validator is intentionally small and object-oriented:

- `TranslationRecordValidator` owns schema loading, record validation, checksum computation, and directory-wide validation.
- `compute_checksum()` creates a deterministic SHA-256 digest from canonical `source_text` and `translation_text`.
- `validate_record()` checks schema validity and checksum integrity.
- `validate_all()` scans the records directory and fails the build if any record is malformed.

## Local command

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python scripts/validate_translation_records.py
```

## Bootstrap proof record

```text
records/TL-2026-000001.json
```

This record proves that the pipeline can validate a translation artifact from source text through translated text and checksum audit.

## Audit rule

The checksum is computed from this canonical payload shape:

```json
{"source_text":"...","translation_text":"..."}
```

The payload uses sorted keys, UTF-8 encoding, and compact separators. This makes the record independently reproducible and reviewable from Git history.
