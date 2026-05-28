# Synchronous Translation Audit

## Purpose

`trans-latin` should audit as translation happens, not only after translation is complete. The production pattern is a translation session ledger: every translation action emits both a scholarly object update and an audit event in the same workflow.

## Core rule

No translation step should be considered complete unless it produces an audit trace.

```text
translation action
  -> object draft/update
  -> checksum calculation
  -> audit event
  -> chain validation
```

## Session model

A translation session groups all actions performed while translating or reviewing a unit.

```text
TranslationSession
  session_id
  actor
  started_at_utc
  source_context
  target_units
  actions
  completed_at_utc
  session_checksum_sha256
```

## Action model

Each session action records one auditable step.

```text
TranslationAction
  action_id
  action_type
  object_type
  object_id
  before_checksum_sha256
  after_checksum_sha256
  input_summary
  output_summary
  created_at_utc
```

Typical action types:

```text
witness_selected
source_captured
source_normalized
tokens_generated
processing_handoff_created
field_accepted
field_rejected
literal_translation_created
interpretive_translation_created
note_added
review_status_changed
audit_event_created
review_packet_exported
```

## Synchronous audit flow

```text
1. Create session record.
2. Select witness and source unit.
3. Capture or confirm source text.
4. Normalize Latin.
5. Generate or import processor output.
6. Create processing handoff.
7. Accept/reject processor fields.
8. Create or update Latin translation unit.
9. Emit audit event for each action.
10. Recompute checksums.
11. Run audit-chain validation.
12. Export review packet/status report when requested.
```

## Transaction boundary

A production implementation should treat each step as an atomic transaction:

```text
write object
write audit event
verify checksum
verify link
```

If any part fails, the action is incomplete and should not be treated as accepted.

## Why this matters

Post-hoc auditing can prove that files are currently valid. Synchronous auditing also proves how the work got there.

This gives the project:

```text
provenance
non-repudiation
review traceability
processor-output separation
field-level acceptance history
release confidence
```

## Implementation path

```text
1. Add translation session schema.
2. Add bootstrap session record.
3. Add session validator.
4. Add session-to-event chain check.
5. Add TranslationSessionService under src/trans_latin/services/.
6. Make future translation commands write through the session service.
```

## Production rule

Future translator commands should not write directly to `translations/`. They should write through a session-aware service that creates or updates:

```text
translations/*.json
audit/events/*.json
audit/sessions/*.json
processing_handoffs/*.json when processor output is involved
```
