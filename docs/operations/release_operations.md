# Trans-Latin Release Operations

## Purpose

This document defines the production-facing release path for `trans-latin`. A release is not only a Git tag; it is a reproducible audit bundle containing review, governance, architecture, and manifest artifacts.

## Local release check

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
make release-check
```

`make release-check` runs the full audit path, generates the review packet, generates and validates the audit manifest, stages the release bundle, and checks that required bundle files exist.

## Core commands

```bash
make qa
make audit
make release-check
```

## Release bundle contents

The release bundle is staged at:

```text
outputs/releases/trans-latin-audit-bundle/
```

Required files:

```text
trans_latin_review_packet.md
TLA-MANIFEST-2026-000001.json
auditability-standard.md
shared-translator-spine.md
language-processing-repo-boundary.md
```

The CI workflow archives this directory as:

```text
outputs/releases/trans-latin-audit-bundle.tar.gz
```

## CI release workflow

The release workflow is:

```text
.github/workflows/release-artifacts.yml
```

It runs on manual dispatch and version tags matching:

```text
v*
```

## Recommended release sequence

```bash
make release-check
git status
git tag v0.1.0-pre.0
git push origin v0.1.0-pre.0
```

The tag triggers the release artifact workflow in GitHub Actions.

## Audit rule

Do not tag a release until local `make release-check` passes cleanly. If any generated artifact changes, commit the source object or script change that explains why.

## Boundary with processing repo

The release bundle represents accepted and reviewable `trans-latin` scholarly artifacts. It does not claim that external language-processing outputs are final scholarly truth. Processing outputs must enter through processing handoff records, be accepted or rejected, and be represented in the audit trail.
