---
title: E1 ATT&CK Enterprise release churn table
id: e1-attck-enterprise-release-churn-table
tags:
- attack-ontology-drift-cti-85bc51
- measurement
created: '2026-09-12T13:17:54.776751Z'
source: https://github.com/mitre-attack/attack-stix-data
status: draft
type: note
tier: ground_truth
content_type: dataset
deprecated: false
summary: Per-release adds, revocations, renames, description and tactic changes
---

# E1 — release-over-release churn, ATT&CK Enterprise

Fidelity: PRIMARY ARTEFACT (computed). Source: data/results/e1_e2_e3.json.

| from → to | date | live | added | revoked | deprecated | renamed | descriptions rewritten | detection text rewritten | tactic set changed | Jaccard(ID sets) |
|---|---|---|---|---|---|---|---|---|---|---|
| v1.0 → v2.0 | 2018-04-18 | 219 | 31 | 0 | 0 | 2 | 28 | 0 | 5 | 0.858 |
| v2.0 → v3.0 | 2018-10-23 | 223 | 4 | 0 | 0 | 1 | 219 | 218 | 4 | 0.982 |
| v3.0 → v4.0 | 2019-04-30 | 244 | 21 | 0 | 0 | 1 | 27 | 10 | 1 | 0.914 |
| v4.0 → v5.0 | 2019-07-19 | 244 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 1.000 |
| v5.0 → v6.0 | 2019-10-23 | 266 | 22 | 0 | 0 | 2 | 60 | 24 | 2 | 0.917 |
| v6.0 → v7.0 | 2020-03-31 | 428 | 302 | 129 | 11 | 17 | 106 | 60 | 10 | 0.222 |
| v7.0 → v8.0 | 2020-10-27 | 525 | 97 | 0 | 0 | 3 | 34 | 17 | 0 | 0.815 |
| v8.0 → v9.0 | 2021-04-29 | 552 | 27 | 0 | 0 | 6 | 149 | 52 | 5 | 0.951 |
| v9.0 → v10.0 | 2021-10-21 | 566 | 15 | 0 | 1 | 2 | 76 | 66 | 0 | 0.972 |
| v10.0 → v11.0 | 2022-04-25 | 576 | 12 | 2 | 0 | 9 | 151 | 44 | 0 | 0.976 |
| v11.0 → v12.0 | 2022-10-25 | 594 | 18 | 0 | 0 | 2 | 50 | 0 | 0 | 0.970 |
| v12.0 → v13.0 | 2023-04-25 | 607 | 13 | 0 | 0 | 1 | 87 | 13 | 0 | 0.979 |
| v13.0 → v14.0 | 2023-10-31 | 625 | 18 | 0 | 0 | 1 | 41 | 2 | 6 | 0.971 |
| v14.0 → v15.0 | 2024-04-23 | 637 | 12 | 0 | 0 | 3 | 98 | 4 | 0 | 0.981 |
| v15.0 → v16.0 | 2024-10-31 | 656 | 19 | 0 | 0 | 1 | 61 | 0 | 0 | 0.971 |
| v16.0 → v17.0 | 2025-04-22 | 679 | 24 | 1 | 0 | 5 | 79 | 5 | 2 | 0.963 |
| v17.0 → v18.0 | 2025-10-28 | 691 | 12 | 0 | 0 | 2 | 49 | 583 | 0 | 0.983 |
| v18.0 → v19.0 | 2026-04-28 | 697 | 23 | 17 | 0 | 4 | 41 | 0 | 198 | 0.944 |

Largest single discontinuity: v6.0 → v7.0 (2020-03-31), Jaccard 0.222 — 302 techniques added, 129 revoked, 750 group→technique edges removed and 1235 added in one release.