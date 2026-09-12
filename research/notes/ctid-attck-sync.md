---
title: CTID ATT&CK Sync
id: ctid-attck-sync
tags:
- attack-ontology-drift-cti-85bc51
- primary-artefact
created: '2026-09-12T13:47:48.916480Z'
source: ' what it publishes, read from the repository:https://github.com/center-for-threat-informed-defense/attack-sync'
status: draft
type: note
tier: ground_truth
content_type: docs
deprecated: false
summary: Primary-artefact replacement for a quarantined note
---

# CTID ATT&CK Sync: what it publishes, read from the repository

Fidelity: PRIMARY ARTEFACT, read from a local clone of
`center-for-threat-informed-defense/attack-sync`, including its README and the
machine-readable sample changelog shipped in `samples/`. This note replaces a
quarantined note of the same nominal subject.

ATT&CK Sync is the Center for Threat-Informed Defense's response to exactly the
problem this paper studies: the README states the project exists because
organisations have widespread difficulty keeping internal systems in sync with
ATT&CK releases, and offers tools, data and methodology to reduce that cost.
Its institutional existence is itself evidence that version drift is a
recognised operational burden rather than a hypothetical one.

What it emits, from the shipped v10.1-to-v12.1 sample: for each object type —
techniques, software, groups, campaigns, mitigations, data sources and data
components — a set of lists by change class (additions, major/minor/other
version changes, metadata changes, unknown changes, revocations, deprecations).
For techniques in that interval the sample carries 30 additions, 24 major
version changes, 132 minor version changes, 35 other version changes, 90
metadata changes and 2 revocations.

Two observations follow. The distribution is itself corroboration: across two
years of releases, technique change is overwhelmingly textual and versioned
rather than referential — 281 version or metadata changes against 2 revocations.
And the deliverable is an enumeration, plus spreadsheets that annotate an
organisation's own mappings with those changes. It tells a consumer what moved.
It does not tell them what the movement cost an analytic built on the earlier
release, which is the quantity this paper measures.
