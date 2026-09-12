---
title: 'diffStix: MITRE''s own machine-readable ontology-drift ledger — and the errors
  it defends against'
id: diffstix-mitres-own-machine-readable-ontology-drift-ledger-and-the-errors-it-def
tags:
- attack-ontology-drift-cti-85bc51
- critique
- rebuttal
created: '2026-09-12T13:22:50.382478Z'
source: https://github.com/mitre-attack/mitreattack-python/tree/master/mitreattack/diffStix
status: draft
type: note
tier: institutional
content_type: docs
deprecated: false
summary: MITRE computes additions/major/minor/patch/revocation/deprecation/deletion
  buckets plus line-level description diffs per release pair; its code also logs 'unexpected
  version increase' and missing revoked-by edges.
---

## What it is
The `diffStix` module inside MITRE's officially maintained `mitreattack-python` library (read directly from a clone at `/home/user/ext/mitreattack-python`): `mitreattack/diffStix/README.md` and `changelog_helper.py` (~1700 lines). It is the tool MITRE itself uses to generate the per-release changelog pages on attack.mitre.org, and it is exposed as CLI commands `diff_stix` and `attack-changelog --old-version 17.1 --new-version 18.0`.

## The position it takes (second major rebuttal artefact)
Ontology drift between any two ATT&CK releases is **already a computed, typed, published, machine-readable diff**. The changelog JSON schema buckets every object of every type (techniques, software, groups, campaigns, assets, mitigations, datasources, datacomponents) into exactly the categories the thesis names:
`additions`, `major_version_changes`, `minor_version_changes`, `other_version_changes`, `patches`, `revocations`, `deprecations`, `deletions`.

Crucially for the thesis's "silent rewriting of technique descriptions" claim: **description rewrites are not silent**. `changelog_helper.py` diffs old vs. new `description` strings line-by-line and emits a rendered `description_change_table` (`difflib.HtmlDiff(...).make_table(old_lines, new_lines, "Old Description", "New Description")`) into the detailed HTML changelog. Semantic edits that leave the T-ID and version untouched are still caught as `patches`: *"ATT&CK objects that have been patched while keeping the version the same. (e.g., 1.0 → 1.0 but something like a typo, a URL, or some metadata was fixed)"*.

## Strength of evidence
Maximal — primary source code, read locally. Caveat: I inspected the source, not the generated per-release outputs, so I cannot state how many objects fall in each bucket per release.

## For or against the thesis
**Mostly against, with two exploitable admissions visible in the code itself.**

*Against the thesis:* "additions vs. bookkeeping" is not a research question needing a new methodology — `attack-changelog --old-version X --new-version Y` answers it for any release pair, free, today. A paper whose contribution is "we counted what fraction of ATT&CK growth is genuine" risks being a re-run of a MITRE-supplied tool. Similarly, "silent description rewriting" is factually the weakest leg of the thesis: the rewrites are diffed and published.

*Cracks for the thesis:*
1. `other_version_changes` is documented as *"ATT&CK objects that have a version change of any other kind. (e.g. 1.0 → 1.3). These are unintended, but can be found in previous releases."* The code logs a warning: `"Unexpected version increase {old} → {new}"`. **MITRE's own tooling admits its versioning discipline has been violated in historical releases** — so version numbers are not a reliable signal of semantic change magnitude.
2. The code contains `logger.error(f"[{stix_id}] revoked object has no revoked-by relationship")` and a check for `revoked_by_key not in new_attack_objects` → *"revoked by {X}, but {X} not found in new STIX bundle!!"*. **The revocation graph is defensive-coded against being broken**, which is direct evidence that dangling/missing revocation edges occur in real bundles. That is the single best empirical wedge against the "revoked-by makes drift a solved bookkeeping problem" rebuttal — and it is quantifiable: run diffStix over all consecutive release pairs and count the error lines.
3. Severity is un-typed. `major_version_changes` is purely a numeric bump (1.0 → 2.0); nothing distinguishes "scope narrowed, all prior labels now wrong" from "added two new platforms." A changelog is not a semantic-compatibility contract.

## Fidelity
High — README table and code logic read verbatim from the clone; quoted strings are literal from `changelog_helper.py` and `diffStix/README.md`. Source: https://github.com/mitre-attack/mitreattack-python/tree/master/mitreattack/diffStix
