---
title: MITRE attack-stix-data USAGE.md — the official versioning and revocation contract
  (primary rebuttal)
id: mitre-attack-stix-data-usagemd-the-official-versioning-and-revocation-contract-p
tags:
- attack-ontology-drift-cti-85bc51
- critique
- rebuttal
created: '2026-09-12T13:22:50.119030Z'
source: https://github.com/mitre-attack/attack-stix-data/blob/master/USAGE.md
status: draft
type: note
tier: institutional
content_type: docs
deprecated: false
summary: Every ATT&CK release since v1.0 is an immutable pinned bundle, revocations
  are typed revoked-by edges, and deprecated objects are retained so workflows do
  not break — drift as a documented, solved lookup problem.
---

## What it is
`USAGE.md` (867 lines) from MITRE's official `attack-stix-data` repository — the canonical distribution channel for ATT&CK content as STIX 2.1 bundles. I read this file directly from a sparse clone (`/home/user/ext/attack-stix-data`), so the quotations below are verbatim.

## The position it takes (this is the strongest institutional rebuttal to the thesis)
Drift is not silent, not lossy, and not un-navigable. Three documented guarantees:

1. **Every release is an immutable, separately addressable artefact.** `index.md` (generated from `index.json`) lists every Enterprise release from v1.0 (17 January 2018) through v19.2 (05 August 2026) — 40+ bundles — each at a stable raw URL of the form `enterprise-attack/enterprise-attack-{version}.json`. USAGE.md gives a five-line recipe (`get_attack_version(domain, version)`) to load any of them, and explicitly recommends the static-copy workflow because "Downloaded copy is static, so updates to the ATT&CK catalog won't cause bugs in automated workflows." **"Pin a version and move on" is literally the documented, first-class path.**
2. **Retirement is typed and machine-readable, and old identifiers are never deleted.** Verbatim: *"Objects that are deemed no longer beneficial to track as part of the knowledge base are marked as deprecated, and objects which are replaced by a different object are revoked. In both cases, the old object is marked with a field (either `x_mitre_deprecated` or `revoked`) noting their status. In the case of revoked objects, a relationship of type `revoked-by` is also created targeting the replacing object."*
3. **Backwards compatibility is an explicit design commitment.** Verbatim: *"Revoked and deprecated objects are kept in the knowledge base so that workflows relying on those objects are not broken."* USAGE.md ships a `getRevokedBy(stix_id, src)` helper and a `remove_revoked_deprecated()` filter.

## Strength of evidence
Maximal for what it establishes — this is the primary source, read in full where relevant. It establishes *capability*, not *practice*: it proves a correct normalization map exists and is free, not that anyone applies it.

## For or against the thesis
**Strongly against, and any SCI-level contribution must beat this rebuttal head-on.** The steel-manned counter-argument is: revocation is a typed edge (`revoked-by`) in a public graph; deprecation is a boolean; every historical version is pinned and downloadable; MITRE deliberately never deletes identifiers. Therefore cross-version normalization is a *solved lookup problem*, and any non-comparability in published CTI analytics is researcher negligence, not an ontology defect — a reporting-discipline paper, not a science paper.

**The cracks the thesis can exploit, all visible inside this same primary source:**
- `revoked-by` is 1:1 by construction. It cannot express the **1:N split** (one technique fractured into sub-techniques) or the **N:1 merge**, which is exactly what the 2020 sub-technique restructure and the v19 Defense Evasion split do. USAGE.md's `getRevokedBy` even hardcodes `revoked_by = revoked_by[0]` — it takes the first revoking object and discards any others.
- Nothing in the contract covers **description rewriting**: `x_mitre_version` bumps and the text changes, but the identifier is stable, so a naive "same T-ID = same label" join silently compares different concepts. There is no `semantics_changed` flag.
- USAGE.md itself concedes an identifier-integrity defect: *"technique ATT&CK IDs are not truly unique"* (legacy 1:1 mitigations shared their technique's ID) — the identifier system has already failed once.
- Note the framing of the deprecation guarantee: workflows *don't break*. Not producing an error is not the same as producing a comparable answer. Silent semantic change is worse for analytics than a hard failure.

## Fidelity
High — verbatim quotes read from the cloned file. Source of truth: https://github.com/mitre-attack/attack-stix-data/blob/master/USAGE.md
