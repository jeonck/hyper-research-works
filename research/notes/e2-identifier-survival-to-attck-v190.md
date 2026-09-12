---
title: E2 identifier survival to ATT&CK v19.0
id: e2-identifier-survival-to-attck-v190
tags:
- attack-ontology-drift-cti-85bc51
- measurement
created: '2026-09-12T13:17:55.022861Z'
source: https://github.com/mitre-attack/attack-stix-data
status: draft
type: note
tier: ground_truth
content_type: dataset
deprecated: false
summary: Survival and recoverability of technique identifiers by source release
---

# E2 — identifier survival to v19.0

Fidelity: PRIMARY ARTEFACT (computed).

| source release | date | identifiers | still live | survival | revoked | deprecated | recoverable via revoked-by |
|---|---|---|---|---|---|---|---|
| v1.0 | 2018-01-17 | 188 | 77 | 0.410 | 100 | 11 | 100 |
| v2.0 | 2018-04-18 | 219 | 97 | 0.443 | 111 | 11 | 111 |
| v3.0 | 2018-10-23 | 223 | 100 | 0.448 | 112 | 11 | 112 |
| v4.0 | 2019-04-30 | 244 | 113 | 0.463 | 120 | 11 | 120 |
| v5.0 | 2019-07-19 | 244 | 113 | 0.463 | 120 | 11 | 120 |
| v6.0 | 2019-10-23 | 266 | 126 | 0.474 | 129 | 11 | 129 |
| v7.0 | 2020-03-31 | 428 | 415 | 0.970 | 12 | 1 | 12 |
| v8.0 | 2020-10-27 | 525 | 511 | 0.973 | 13 | 1 | 13 |
| v9.0 | 2021-04-29 | 552 | 538 | 0.975 | 13 | 1 | 13 |
| v10.0 | 2021-10-21 | 566 | 551 | 0.973 | 15 | 0 | 15 |
| v11.0 | 2022-04-25 | 576 | 563 | 0.977 | 13 | 0 | 13 |
| v12.0 | 2022-10-25 | 594 | 581 | 0.978 | 13 | 0 | 13 |
| v13.0 | 2023-04-25 | 607 | 593 | 0.977 | 14 | 0 | 14 |
| v14.0 | 2023-10-31 | 625 | 609 | 0.974 | 16 | 0 | 16 |
| v15.0 | 2024-04-23 | 637 | 621 | 0.975 | 16 | 0 | 16 |
| v16.0 | 2024-10-31 | 656 | 640 | 0.976 | 16 | 0 | 16 |
| v17.0 | 2025-04-22 | 679 | 663 | 0.976 | 16 | 0 | 16 |
| v18.0 | 2025-10-28 | 691 | 674 | 0.975 | 17 | 0 | 17 |
| v19.0 | 2026-04-28 | 697 | 697 | 1.000 | 0 | 0 | 0 |

Pre-restructure releases (v1.0–v6.0): survival 0.410–0.474. Post-restructure (v7.0 onward): 0.970–0.978.
Every revoked identifier in the corpus resolves to a live identifier through the published revoked-by graph — the damage is mechanically repairable at the identifier level, which is what makes the normalization protocol possible.