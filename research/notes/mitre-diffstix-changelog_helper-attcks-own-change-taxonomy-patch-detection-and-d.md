---
title: 'MITRE diffStix changelog_helper: ATT&CK''s own change taxonomy, patch detection,
  and dangling-revocation handling'
id: mitre-diffstix-changelog_helper-attcks-own-change-taxonomy-patch-detection-and-d
tags:
- attack-ontology-drift-cti-85bc51
- ontology-versioning
created: '2026-09-12T13:22:25.771513Z'
source: https://github.com/mitre-attack/mitreattack-python/blob/master/mitreattack/diffStix/changelog_helper.py
status: draft
type: note
tier: institutional
content_type: docs
deprecated: false
summary: 'Artefact read of MITRE''s changelog generator: additions/major/minor/other/patches/revocations/deprecations/unchanged,
  where ''patch'' means version-unchanged content edits detected only by the modified
  timestamp - silent rewriting is official, and dangling revocations are handled because
  they occur.'
---

## What it is

MITRE's own `diffStix` module in `mitreattack-python` (`mitreattack/diffStix/changelog_helper.py`), read as an **artefact** from a shallow clone of `github.com/mitre-attack/mitreattack-python`. This is the tool that generates the official ATT&CK release changelogs.

## Concept/mechanism it contributes

MITRE already operates a change taxonomy, defined in code. The category descriptions, read verbatim from the source:

> "additions": "ATT&CK objects which are only present in the new release."
> "major_version_changes": "ATT&CK objects that have a major version change. (e.g. 1.0 → 2.0)"
> "minor_version_changes": "ATT&CK objects that have a minor version change. (e.g. 1.0 → 1.1)"
> "other_version_changes": "ATT&CK objects that have a version change of any other kind. (e.g. 1.0 → 1.2)"
> "patches": "ATT&CK objects that have been patched while keeping the version the same. (e.g., 1.0 → 1.0 but something like a typo, a URL, or some metadata was fixed)"
> "revocations": "ATT&CK objects which are revoked by a different object."
> "deprecations": "ATT&CK objects which are deprecated and no longer in use, and not replaced."
> "unchanged": "ATT&CK objects which did not change between the two versions."

Three findings from reading the implementation matter for the manuscript:

1. **"Silent rewriting" is an officially recognised category, and its detection rule is a timestamp.** `is_patch_change()` returns True when the object's `x_mitre_version` is unchanged but the `modified` timestamp advanced. So a technique description can be rewritten with no version increment; the only signal is `modified`. Any CTI study that pins "ATT&CK v13" and assumes object-level stability is unprotected against this class of change.
2. **Deprecation and revocation are formally distinct, and MITRE's own definitions state the difference.** Revoked = replaced by a different object (an exact-successor relation, `revoked-by`); deprecated = "no longer in use, and not replaced". This is precisely the OBO `replaced_by` vs plain-obsoletion distinction, and it means ATT&CK's model has no slot for the *inexact/multiple* successor case that sub-technique splits produce.
3. **Dangling revocations occur in practice.** The code logs errors for two real conditions: `"revoked object has no revoked-by relationship"`, and the case where an object is revoked by a target that is not present in the new STIX bundle (`"revoked by {revoked_by_key}, but {revoked_by_key} not found in new STIX bundle!!"`). MITRE wrote defensive handling because these referential-integrity failures happen. That is a directly measurable drift-integrity metric for the manuscript: count, per release pair, the revocations whose successor is missing or unstated.

The module also computes a per-object description diff (old/new line comparison rendered as an HTML table) and separately tracks technique→mitigation and technique→detection relationship changes — meaning the raw material for measuring coverage-claim drift is already produced by MITRE's tooling.

## Mapping onto ATT&CK

This is the ATT&CK-side counterpart to COnto-Diff, and its existence constrains the manuscript's novelty claim in a useful way. MITRE already emits *basic* change operations with a partial type system. What the manuscript adds is the layer above: aggregating those categories into conceptual change types (split / merge / move / rename), separating genuine-intelligence additions from bookkeeping additions, and propagating the mapping to labelled CTI corpora. Positioning: "we build on MITRE's published change taxonomy rather than inventing one, and we show what it cannot express" — notably that a `split` appears as N additions plus one revocation with no relation tying them together, and that tactic reassignment (a change to `kill_chain_phases`) is not a distinct category at all but merely contributes to a version bump.

Practical benefit: diffStix is runnable offline against archived STIX bundles, so the manuscript's drift census can be built on MITRE's own instrument, which forecloses the "your change classification is idiosyncratic" reviewer objection.

## Fidelity

Ground truth. All quoted strings were read from `/home/user/ext/mitreattack-python/mitreattack/diffStix/changelog_helper.py` at HEAD of the default branch (shallow clone, 2026-09-12); the category descriptions are at lines ~205-213 and the patch-detection logic at `is_patch_change()` (~line 1662). Verbatim as of that commit. The interpretive claims (that splits are unexpressible, that tactic reassignment has no category) are my reading of the code, not MITRE statements.
