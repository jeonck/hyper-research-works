---
title: E3 silent semantic drift of ID-stable ATT&CK techniques
id: e3-silent-semantic-drift-of-id-stable-attck-techniques
tags:
- attack-ontology-drift-cti-85bc51
- measurement
created: '2026-09-12T13:17:55.263293Z'
source: https://github.com/mitre-attack/attack-stix-data
status: draft
type: note
tier: ground_truth
content_type: dataset
deprecated: false
summary: Description rewriting among techniques whose identifiers never changed
---

# E3 — silent semantic drift among ID-stable techniques (vs. v19.0)

Fidelity: PRIMARY ARTEFACT (computed). Only techniques whose identifier is
live in BOTH releases are counted, so every row isolates meaning change
from identifier change.

| source release | ID-stable techniques | description edited | mean token Jaccard | substantial rewrite (J<0.8) |
|---|---|---|---|---|
| v1.0 | 77 | 1.000 | 0.345 | 1.000 |
| v2.0 | 97 | 1.000 | 0.373 | 1.000 |
| v3.0 | 100 | 0.960 | 0.553 | 0.830 |
| v4.0 | 113 | 0.965 | 0.548 | 0.841 |
| v5.0 | 113 | 0.965 | 0.548 | 0.841 |
| v6.0 | 126 | 0.968 | 0.569 | 0.817 |
| v7.0 | 415 | 0.749 | 0.808 | 0.386 |
| v8.0 | 511 | 0.767 | 0.830 | 0.337 |
| v9.0 | 538 | 0.645 | 0.849 | 0.310 |
| v10.0 | 551 | 0.593 | 0.866 | 0.278 |
| v11.0 | 563 | 0.465 | 0.895 | 0.208 |
| v12.0 | 581 | 0.439 | 0.906 | 0.189 |
| v13.0 | 593 | 0.386 | 0.928 | 0.140 |
| v14.0 | 609 | 0.366 | 0.938 | 0.123 |
| v15.0 | 621 | 0.275 | 0.956 | 0.087 |
| v16.0 | 640 | 0.211 | 0.969 | 0.062 |
| v17.0 | 663 | 0.124 | 0.985 | 0.024 |
| v18.0 | 674 | 0.061 | 0.997 | 0.003 |