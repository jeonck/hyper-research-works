---
title: E4 how much ATT&CK growth is bookkeeping rather than new intelligence
id: e4-how-much-attck-growth-is-bookkeeping-rather-than-new-intelligence
tags:
- attack-ontology-drift-cti-85bc51
- measurement
created: '2026-09-12T13:17:55.512139Z'
source: https://github.com/mitre-attack/attack-stix-data
status: draft
type: note
tier: ground_truth
content_type: dataset
deprecated: false
summary: Roughly a third of new edges for existing groups are ontology bookkeeping
---

# E4 — decomposition of apparent knowledge growth

Fidelity: PRIMARY ARTEFACT (computed). Every group→technique `uses` edge
that appears in release B but not in release A is attributed to exactly one
cause.

- total new edges across all Enterprise transitions: 5516
- attributable to groups newly added to ATT&CK: 2442
- new edges for groups that already existed: 3074
  - genuine new intelligence (both endpoints pre-existed, newly linked): 1752
  - new technique, new edge: 330
  - sub-technique refinement of an edge the group already had: 487
  - revocation re-mapping of an edge the group already had: 505
- ontology bookkeeping share of growth for pre-existing groups: 992/3074 = 0.323

| from → to | new edges (existing groups) | bookkeeping share |
|---|---|---|
| v1.0 → v2.0 | 36 | 0.000 |
| v2.0 → v3.0 | 123 | 0.000 |
| v3.0 → v4.0 | 144 | 0.000 |
| v4.0 → v5.0 | 33 | 0.000 |
| v5.0 → v6.0 | 30 | 0.000 |
| v6.0 → v7.0 | 1059 | 0.750 |
| v7.0 → v8.0 | 81 | 0.000 |
| v8.0 → v9.0 | 285 | 0.014 |
| v9.0 → v10.0 | 187 | 0.005 |
| v10.0 → v11.0 | 231 | 0.017 |
| v11.0 → v12.0 | 43 | 0.047 |
| v12.0 → v13.0 | 71 | 0.380 |
| v13.0 → v14.0 | 48 | 0.021 |
| v14.0 → v15.0 | 100 | 0.340 |
| v15.0 → v16.0 | 182 | 0.077 |
| v16.0 → v17.0 | 134 | 0.216 |
| v17.0 → v18.0 | 123 | 0.041 |
| v18.0 → v19.0 | 164 | 0.470 |