# Security and Rights Posture

## Scope

This repository is a scholarly translation and audit repository. The main risks are provenance loss, malformed audit records, accidental storage of restricted source images, and unreviewed processing output being mistaken for approved translation.

## Reporting

For public-facing contact, use:

```text
paulskeffington@gmail.com
```

## Rights-sensitive materials

Rights-sensitive source images and PDFs are blocked by default in source-evidence paths. The preferred model is link-only source handling unless explicit storage clearance is documented.

## Processing outputs

External or future language-processing outputs must not be treated as final scholarly truth. They must enter through processing handoff records and be accepted, rejected, or superseded through the audit chain.

## Required checks

Run:

```bash
make qa
make release-check
```

These commands verify schemas, checksums, witness provenance, handoffs, audit events, audit chain links, rights-sensitive file exclusions, review packet generation, manifest generation, and release bundle contents.
