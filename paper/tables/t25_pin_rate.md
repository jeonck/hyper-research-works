**Table 25.** Publication-side ATT\&CK release-pin rate: arXiv papers (2023-01-01 to 2026-09-01) that use ATT\&CK technique identifiers, Wilson 95% intervals, seed 20260912.

| Quantity | k / n | Estimate | 95% interval |
|---|---|---|---|
| Exact release declared (e.g. v14.1) | 6 / 33 | 0.182 | [0.086, 0.344] |
| Major-or-better declared (v14 or v14.1) | 9 / 33 | 0.273 | [0.151, 0.442] |
| Any declaration (incl. date-only) | 9 / 33 | 0.273 | [0.151, 0.442] |

Sampling funnel:

| Stage | Count |
|---|---|
| Sampling frame (arXiv, "MITRE ATT&CK") | 155 |
| Seeded sample | 60 |
| Fetch attempts used (cap 90) | 60 |
| Fetch failures | 0 |
| Fetched OK | 60 |
| Excluded (fewer than 3 technique-ID occurrences) | 27 |
| Included (uses ATT&CK technique IDs) | 33 |
| Included papers requiring manual reclassification | 5 |

By year:

| Year | n | Exact release k/n | 95% CI | Major-or-better k/n | 95% CI |
|---|---|---|---|---|---|
| 2023 | 1 | 0 / 1 | [0.000, 0.793] | 0 / 1 | [0.000, 0.793] |
| 2024 | 2 | 0 / 2 | [0.000, 0.658] | 1 / 2 | [0.095, 0.905] |
| 2025 | 15 | 3 / 15 | [0.070, 0.452] | 3 / 15 | [0.070, 0.452] |
| 2026 | 15 | 3 / 15 | [0.070, 0.452] | 5 / 15 | [0.152, 0.583] |

By sub-technique use:

| Group | k / n | Estimate | 95% interval |
|---|---|---|---|
| Uses sub-technique IDs (T####.###) | 8 / 24 | 0.333 | [0.180, 0.533] |
| Enterprise/major techniques only | 1 / 9 | 0.111 | [0.020, 0.435] |
