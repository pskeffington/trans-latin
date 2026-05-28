# Contributing to Trans-Latin

## Purpose

`trans-latin` is an auditable scholarly translation repository. Contributions should preserve the chain from source witness to reviewed translation and export artifact.

## Required local check

Before opening a pull request or tagging a release, run:

```bash
make qa
```

For release work, run:

```bash
make release-check
```

## Object rules

- Do not add translation units without stable `TLA-...` IDs.
- Do not add undocumented witnesses.
- Do not bypass checksum fields.
- Do not silently overwrite reviewed scholarly content.
- Do not store rights-sensitive source images unless explicit clearance is documented.
- Processing outputs must enter through processing handoff records before acceptance into reviewed translation units.

## Review states

Use the shared review-state ladder:

```text
draft
machine_checked
human_reviewed
approved
rejected
superseded
```

## Pull request standard

A production-ready pull request should identify:

```text
changed object type
affected unit IDs
affected witnesses
review status changes
new or changed audit events
validation command run
```
