# Shared Translator Spine

`trans-latin` should intentionally track the backbone of `Trans-heb` so the Hebrew and Latin translators remain structurally similar, object-oriented, and pipeline-compatible.

## Reference architecture

`Trans-heb` defines translation as a documented scholarly workflow rather than a single output. Its current spine includes corpus and witness registries, image linkage, diplomatic transcription, normalization, tokenization, morphology, lexical analysis, translation memory, apparatus, token alignment, exports, QA/CI, SQLite, local API, MkDocs, release workflow, and Vatican/BAV intake.

The equivalent Latin spine should preserve the same object boundaries wherever realistic.

## Shared evidence chain

```text
source image / witness
  -> diplomatic transcription
  -> normalized source text
  -> tokenization
  -> morphology
  -> lexical analysis
  -> literal translation
  -> interpretive translation
  -> apparatus / notes
  -> reviewer action
  -> publication export
```

For `Trans-heb`, the normalized source text is Hebrew. For `trans-latin`, the normalized source text is Latin. The pipeline shape should remain the same even when the language-specific rules differ.

## Shared repository layers

| Layer | Trans-heb object pattern | Trans-latin target pattern | Purpose |
|---|---|---|---|
| Corpus | `corpus/registry/`, `corpus/witnesses/`, `corpus/images/` | same | preserve witness provenance and image linkage |
| Text method | `docs/methodology/` | same | define transcription, normalization, OCR, Unicode, and review policy |
| Translation data | `translations/`, `data/translation_memory/` | same | preserve draft/reviewed translation units and consistency memory |
| Linguistic data | `data/tokens/`, `data/morphology/`, `data/lexicon/`, `data/alignment/` | same | support token, morphology, lexicon, and alignment analysis |
| Apparatus | `apparatus/`, `scripts/apparatus/` | same | track variants, uncertainty, and editorial decisions |
| Processing | `scripts/normalize/`, `scripts/tokenize/`, `scripts/transliterate/`, `scripts/morphology/` | `scripts/normalize/`, `scripts/tokenize/`, `scripts/morphology/` | execute reproducible language processing |
| Search/collation | `scripts/search/`, `scripts/collation/` | same | support corpus indexing and witness comparison |
| Export | `scripts/export/`, `outputs/latex/`, `outputs/releases/`, `outputs/review/` | same | generate interlinear, TEI/XML, LaTeX, reviewer packets, and release outputs |
| QA/CI | `scripts/qa/`, `.github/workflows/`, `Makefile` | same | validate structure and run automation |
| Platform | `db/`, `api/`, `mkdocs.yml`, `docs/architecture/` | same | define database/API/docs deployment path |

## Shared object model

### Base witness object

```text
Witness
  witness_id
  collection_id
  shelfmark
  repository
  rights_status
  source_link
  folio_or_page_range
  notes
```

### Base translation unit object

```text
TranslationUnit
  unit_id
  collection_id
  witness_id
  line_reference
  source_text
  normalized_source
  tokens
  morphology
  word_by_word_gloss
  literal_translation
  interpretive_translation
  uncertainty_flags
  apparatus_links
  notes
  translation_status
  reviewer
```

### Latin specialization

```text
LatinTranslationUnit extends TranslationUnit
  source_latin
  normalized_latin
  lemma_sequence
  morphology_sequence
  literal_translation
  interpretive_translation
```

### Hebrew specialization

```text
HebrewTranslationUnit extends TranslationUnit
  source_hebrew
  normalized_hebrew
  transliteration
  word_by_word_gloss
  literal_translation
  interpretive_translation
```

## Stable ID alignment

`Trans-heb` uses:

```text
THB-{collection}-{witness}-{folio_or_page}-{line_or_unit}
```

`trans-latin` should use the parallel form:

```text
TLA-{collection}-{witness}-{folio_or_page}-{line_or_unit}
```

Example:

```text
TLA-DEMO-W01-P001-L001
```

The earlier `TL-YYYY-NNNNNN` audit record pattern may remain useful for ledger-level records, but translation units should use the same witness-chain object pattern as `Trans-heb`.

## Shared Make targets

`trans-latin` should mirror the useful `Trans-heb` local command surface:

```bash
make qa
make vatican
make vatican-review
make sqlite
make sqlite-report
make release-check
```

Initial Latin targets may be lighter until the full scaffold exists, but the names should remain stable across repositories.

## Latin pipeline priority

```text
1. keep the current JSON audit validator live
2. add Latin translation-unit schema using TLA witness-chain IDs
3. move validators toward scripts/qa/ parity
4. add corpus/witness registry skeletons
5. add translations/ and data/translation_memory/ paths
6. add docs/methodology/latin_transcription_policy.md
7. add docs/methodology/latin_normalization_policy.md
8. add scripts/normalize/, scripts/tokenize/, scripts/morphology/
9. add apparatus/ and scripts/apparatus/
10. add outputs/review/, outputs/latex/, outputs/releases/
11. add SQLite loader and integrity check
12. add local API parity after data objects stabilize
```

## Design rule

Any new Latin object should first ask: does `Trans-heb` already have an equivalent object boundary? If yes, copy the boundary and only specialize the language-specific fields.
