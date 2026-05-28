# Language Processing Repository Boundary

## Purpose

`trans-latin` should not become the only place where language-processing machinery lives. The translator repository should remain the auditable scholarly layer: witnesses, transcription, translation units, review state, apparatus, exports, and validation.

A separate language-processing repository should handle the reusable processing engine, similar in spirit to an ingestion layer such as Eagle Eye.

## Repository split

```text
trans-latin
  scholarly translator layer
  audit ledger
  Latin translation units
  witness-chain IDs
  review workflow
  apparatus and notes
  export artifacts
  CI verification

trans-language-processing / trans-latin-processing / eagle-eye-latin
  reusable processing layer
  intake adapters
  normalization engines
  tokenization engines
  morphology parsers
  lexicon lookup
  alignment helpers
  batch processing
  processor APIs
```

## Boundary rule

`trans-latin` owns scholarly truth. The processing repo owns reproducible mechanical transformation.

A processor may propose normalized text, tokens, morphology, lemmas, glosses, and confidence scores, but `trans-latin` records what was accepted, reviewed, rejected, or superseded.

## Data flow

```text
source metadata / witness link
  -> processing repo intake adapter
  -> Latin normalization processor
  -> Latin tokenizer
  -> morphology / lemma parser
  -> optional lexical gloss engine
  -> processing output JSON
  -> trans-latin translation unit
  -> audit validation
  -> reviewer action
  -> export
```

## Processing repo responsibilities

The processing repository should provide:

```text
ProcessorBase
NormalizerBase
TokenizerBase
MorphologyParserBase
LexiconProviderBase
AlignmentProviderBase
ProcessingResult
ProcessingAudit
BatchRunner
CLI entrypoints
JSON schema outputs
unit tests
CI checks
```

## Latin processor modules

Suggested first package layout:

```text
src/trans_language_processing/
  __init__.py
  core/
    processor_base.py
    processing_result.py
    processing_audit.py
  latin/
    normalizer.py
    tokenizer.py
    morphology.py
    lexicon.py
    pipeline.py
  io/
    readers.py
    writers.py
    schemas.py
  cli/
    normalize_latin.py
    tokenize_latin.py
    parse_latin_morphology.py
    run_latin_pipeline.py
  qa/
    validators.py
```

## Contract with trans-latin

The processing repo should emit JSON compatible with `trans-latin` translation units, but it should not directly approve or overwrite scholarly records.

Minimum output contract:

```json
{
  "processor_name": "latin_pipeline",
  "processor_version": "0.1.0",
  "source_latin": "In principio erat Verbum.",
  "normalized_latin": "in principio erat verbum",
  "tokens": [
    {
      "surface": "In",
      "lemma": "in",
      "pos": "preposition",
      "morphology": "takes ablative here",
      "gloss": "in",
      "confidence": 1.0
    }
  ],
  "warnings": [],
  "checksum_sha256": "..."
}
```

## Audit handoff

When `trans-latin` imports a processing result, it should store:

```text
processor_repo
processor_commit
processor_version
processor_config
processing_checksum_sha256
accepted_fields
rejected_fields
reviewer
review_status
```

This preserves reproducibility and makes it possible to rerun a processor later without confusing processor output with reviewed scholarly translation.

## Naming options

Possible repo names:

```text
trans-language-processing
trans-latin-processing
eagle-eye-latin
eagle-eye-lang
trans-processing-core
```

Recommended default:

```text
trans-language-processing
```

This keeps the repo useful for Latin first while leaving room for Hebrew and other classical-language processors.

## Near-term implementation plan

```text
1. create dedicated processing repo
2. add Python package scaffold
3. add core processing result schema
4. add Latin normalizer
5. add Latin tokenizer
6. add bootstrap morphology parser
7. add CLI commands
8. add tests and GitHub Actions
9. emit trans-latin-compatible JSON
10. add trans-latin import validator for processing outputs
```
