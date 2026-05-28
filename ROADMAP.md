# Trans-Latin Roadmap

## Current posture

`trans-latin` is in production-spine hardening. The repository now has auditable objects, QA validators, package smoke checks, release bundle generation, review artifacts, status reporting, and GitHub Actions workflows. The next major stage is interoperability with a dedicated language-processing repository.

## Phase status

| Phase | Status | Focus |
|---|---|---|
| Phase 0 | active scaffold complete | repository foundation, package metadata, schemas, QA, workflows |
| Phase 1 | active scaffold complete | witness provenance and source-rights posture |
| Phase 2 | active scaffold complete | Latin translation-unit schema and bootstrap unit |
| Phase 3 | active scaffold complete | processing handoff boundary and audit event ledger |
| Phase 4 | active scaffold complete | audit-chain validation, review packet, status report, audit manifest |
| Phase 5 | active scaffold complete | release bundle staging, release workflow, package smoke checks |
| Phase 6 | planned | dedicated language-processing repo integration |
| Phase 7 | planned | corpus-scale Latin sources, apparatus, collation, and exports |
| Phase 8 | planned | API/database layer and documentation site parity with `Trans-heb` |

## Immediate priorities

```text
1. keep `make qa` clean as the source of truth
2. keep `make release-check` clean before tags
3. create or connect the dedicated language-processing repository
4. define processor output schemas shared across Latin and Hebrew
5. add real Latin source/witness records beyond the bootstrap demo
6. add apparatus and variant-link records
7. add TEI/XML and LaTeX export parity
8. add database/API layer after object contracts stabilize
```

## Production milestone target

The first pre-release target is:

```text
v0.1.0-pre.0
```

A pre-release should include a passing release bundle with:

```text
review packet
status report
audit manifest
auditability standard
shared translator spine
language-processing boundary
```
