---
title: Corpus integrity incident and how it was handled
id: corpus-integrity-incident-and-how-it-was-handled
tags:
- attack-ontology-drift-cti-85bc51
- methodology
created: '2026-09-12T13:46:28.185824Z'
source: https://github.com/mitre-attack/attack-stix-data
status: draft
type: note
tier: ground_truth
content_type: dataset
deprecated: false
summary: Ten of 112 notes had mismatched front matter and body; all quarantined and
  excluded
---

# Corpus integrity incident and how it was handled

Fidelity: AUTHORED process record, with a reproducible check in
`code/25_vault_integrity.py` and its output in
`data/results/e15_vault_integrity.json`.

## What happened

The literature corpus for this study was assembled by parallel research agents,
each writing notes into a shared vault. A check of all 112 notes found **10**
whose front matter and body describe different sources — a note titled for
MITRE's `USAGE.md` carrying a body that audits AttacKG, a note titled for CTID's
ATT&CK Sync carrying a body about a multi-report extraction benchmark, and eight
more of the same shape. The most likely cause is concurrent agents writing note
bodies through a shared temporary file path, so that one agent's body was read
while another's title was being committed.

## Why it matters here more than usual

A note whose title names one source and whose body summarises another is a
provenance failure: any claim drawn from it would be attributed to a source that
never made it. That is the precise failure mode this paper studies, arriving
inside the paper's own evidence base. It is recorded rather than quietly fixed.

## What was done

1. All 112 notes were checked automatically: content-bearing tokens of each
   title were compared against the first 1,200 characters of its body, with a
   secondary check on whether the body cites a different host than the front
   matter declares.
2. The 10 flagged notes were deprecated, tagged `quarantined-metadata-mismatch`,
   and excluded from the reference registry. None is cited in the manuscript.
3. Findings that had been attributed to a quarantined note were either dropped
   or re-derived from a primary artefact the author could verify directly. In
   particular, the revocation-arity and tactic-layer claims are now computed by
   `code/23_tactic_layer.py` from the release bundles rather than taken from any
   note.

## What this costs the study

The corpus is 82 external references rather than 92. Two leads are now
unsupported below summary level and are listed as open gaps: the CTID ATT&CK
Sync project's published outputs, and MITRE's own `diffStix` change-class
documentation. Both are reachable in principle by cloning
`center-for-threat-informed-defense/attack-sync` and `mitre-attack/mitreattack-python`
directly, and a camera-ready version should do exactly that rather than rely on
a re-summarised account.
