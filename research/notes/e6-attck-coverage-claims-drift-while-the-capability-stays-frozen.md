---
title: E6 ATT&CK coverage claims drift while the capability stays frozen
id: e6-attck-coverage-claims-drift-while-the-capability-stays-frozen
tags:
- attack-ontology-drift-cti-85bc51
- measurement
created: '2026-09-12T13:17:55.996775Z'
source: https://github.com/mitre-attack/attack-stix-data
status: draft
type: note
tier: ground_truth
content_type: dataset
deprecated: false
summary: Reported coverage moves by percentage points with no change in capability
---

# E6 — coverage claims under a frozen capability (re-measured at v9.0)

Fidelity: PRIMARY ARTEFACT (computed). The capability never changes; only
the ontology moves. The naive-versus-normalized gap is the pure identifier
artefact, separate from the genuine effect of the technique list growing.

| capability frozen at | portfolio size | claimed then | naive now | normalized now | identifier artefact (pp) |
|---|---|---|---|---|---|
| v1.0 (2018-01-17) | 183 | 97.3% | 13.6% | 29.7% | 16.1 |
| v2.0 (2018-04-18) | 215 | 98.2% | 17.4% | 35.3% | 17.9 |
| v3.0 (2018-10-23) | 222 | 99.6% | 18.1% | 36.6% | 18.5 |
| v4.0 (2019-04-30) | 243 | 99.6% | 20.5% | 40.4% | 19.9 |
| v5.0 (2019-07-19) | 243 | 99.6% | 20.5% | 40.4% | 19.9 |
| v6.0 (2019-10-23) | 258 | 97.0% | 21.9% | 43.1% | 21.2 |
| v7.0 (2020-03-31) | 382 | 89.3% | 69.2% | 69.2% | 0.0 |
| v8.0 (2020-10-27) | 477 | 90.9% | 86.4% | 86.4% | 0.0 |

Random-portfolio sweep (500 random 30% portfolios per source release):

| frozen at | naive error (pp) | normalized error (pp) |
|---|---|---|
| v1.0 | -26.49 ± 0.43 | -22.35 ± 0.24 |
| v2.0 | -25.56 ± 0.48 | -20.98 ± 0.24 |
| v3.0 | -25.37 ± 0.48 | -20.73 ± 0.23 |
| v4.0 | -25.04 ± 0.51 | -20.07 ± 0.26 |
| v5.0 | -25.07 ± 0.53 | -20.07 ± 0.25 |
| v6.0 | -24.31 ± 0.54 | -18.99 ± 0.25 |
| v7.0 | -12.09 ± 0.23 | -11.61 ± 0.10 |
| v8.0 | -7.99 ± 0.23 | -7.45 ± 0.10 |
| v9.0 | -6.81 ± 0.24 | -6.29 ± 0.10 |
| v10.0 | -6.23 ± 0.24 | -5.67 ± 0.09 |
| v11.0 | -5.75 ± 0.24 | -5.23 ± 0.08 |
| v12.0 | -4.98 ± 0.24 | -4.48 ± 0.08 |
| v13.0 | -4.48 ± 0.24 | -3.92 ± 0.08 |
| v14.0 | -3.76 ± 0.26 | -3.13 ± 0.08 |
| v15.0 | -3.27 ± 0.26 | -2.63 ± 0.08 |
| v16.0 | -2.47 ± 0.24 | -1.81 ± 0.09 |
| v17.0 | -1.46 ± 0.27 | -0.81 ± 0.07 |
| v18.0 | -1.00 ± 0.27 | -0.30 ± 0.07 |