# Latin Normalization Policy

## Purpose

This policy defines how `trans-latin` moves from diplomatic Latin source capture to normalized Latin suitable for tokenization, morphology, lexical analysis, and translation.

## Separation principle

Keep diplomatic transcription and normalized Latin separate. Normalization supports analysis; it must not erase source evidence.

## Initial normalization rules

For early pipeline work, normalized Latin may apply:

```text
lowercasing
terminal punctuation removal
consistent whitespace collapse
optional u/v and i/j policy only when explicitly declared
abbreviation expansion only when documented
```

## Non-silent changes

Do not silently normalize:

```text
proper names
divine names
abbreviations
scribal marks
damaged text
variant readings
orthographic forms relevant to dating or witness identity
```

## Required metadata

Every normalized unit should retain:

```text
normalization_policy
pipeline_version
source_latin
normalized_latin
normalization_notes
```

## Current bootstrap policy

The bootstrap unit uses:

```text
lowercase_and_strip_terminal_punctuation_for_bootstrap
```

This is intentionally minimal and should be replaced by named policies as the Latin corpus expands.
