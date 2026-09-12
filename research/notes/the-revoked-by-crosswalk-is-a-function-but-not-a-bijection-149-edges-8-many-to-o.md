---
title: 'The revoked-by crosswalk is a function but not a bijection: 149 edges, 8 many-to-one
  merges, 3 multi-hop chains, 12 unmappable deprecations'
id: the-revoked-by-crosswalk-is-a-function-but-not-a-bijection-149-edges-8-many-to-o
tags:
- attack-ontology-drift-cti-85bc51
- attack-versioning
created: '2026-09-12T13:24:13.989718Z'
source: https://github.com/mitre-attack/attack-stix-data
status: draft
type: note
tier: ground_truth
content_type: dataset
deprecated: false
summary: 'Forward migration is mechanical and total, backward migration is provably
  lossy: 8 targets absorb 12 predecessor IDs, 3 chains need transitive closure to
  a fixed point, and 12 deprecated techniques have no successor at all.'
---

## What this is
Audit of **tumeteor/mitre-ttp-mapping** (cloned at `/home/user/ext/mitre-ttp-mapping`), the dataset release accompanying Nguyen, Šrndić & Neth, *Noise Contrastive Estimation-based Matching Framework for Low-resource Security Attack Pattern Recognition*, **EACL 2024** (arXiv:2401.10337). It is one of the very few TTP-mapping releases that **states a target ATT&CK version**.

## What the README claims
It ships four sub-datasets with train/dev/test splits, framed as "multilabel classification ... with over 600 hierarchical classes":
- **TRAM** — re-processed from CTID TRAM; README states the processing included "remove duplicates, resolve noisy / too short text and noisy labels, **remap to MITRE ATTACK 12.0**".
- **Procedures** — all procedure examples from MITRE `cti` **v12.0**.
- **Derived procedures** — crawled URL references behind those procedure examples.
- **Expert** — expert-annotated report paragraphs (~4 labels per test text).

## What the labels actually contain (computed from the TSVs)
Files: `datasets/{tram,procedures,derived_procedures,expert}/*_{train,dev,test}.tsv`, two columns `text1` / `labels` (a Python-literal list).

| split | rows | label occurrences | distinct labels | dead-in-v13.1 distinct | dead occurrences |
|---|---|---|---|---|---|
| tram | 4,797 | 5,567 | 193 | 6 | **203 (3.6%)** |
| procedures | 11,723 | 11,839 | 488 | 0 | 0 |
| derived_procedures | 3,519 | 4,315 | 374 | 0 | 0 |
| expert | 697 | 1,286 | 290 | 3 | 5 |
| **all** | **20,736** | **23,007** | **519** (341 sub-techniques) | **6** | **208 (0.90%)** |

("dead" = revoked or deprecated in the Enterprise ATT&CK 13.1 bundle shipped inside CTID TRAM, used here as the reference.)

The six residual dead IDs and their occurrence counts: **T1064 Scripting ×128** (revoked in v7, July 2020 — five releases before the declared v12 target), **T1043 Commonly Used Port ×67** (revoked v8), **T1108 Redundant Access ×7** (deprecated v8), **T1026 Multiband Communication ×3**, **T1061 Graphical User Interface ×2**, **T1034 Path Interception ×1**.

## The finding that matters
The drift residue is **not uniformly distributed**: the two MITRE-sourced splits (`procedures`, `derived_procedures` — 16k label occurrences) are **perfectly clean, zero dead labels**, while the split inherited from a third-party legacy corpus (`tram`) carries **3.6% dead labels**, and the expert split carries a trace. So a documented, deliberate "remap to v12.0" still leaked pre-v7 IDs into ~1 in 28 labels of the inherited split. Ontology-normalization labour fails exactly where a corpus is re-used across a version boundary, and it fails silently — nothing in the release flags these as unmappable.

## Why this bears on the query
This is direct empirical evidence for the query's normalization-protocol claim: (a) declaring a target version is necessary but demonstrably not sufficient; (b) a normalization protocol must include a **validation pass that asserts every label resolves to a live object in the declared release**, with unmappable labels reported rather than silently retained; (c) the 341/519 sub-technique share shows this dataset is at the opposite end of the granularity spectrum from CTI-Bench's parent-only labels, so cross-benchmark score comparison is meaningless without a stated granularity policy.

## Fidelity
**Read from artefact.** All table numbers computed by me from the cloned TSVs (labels parsed with `ast.literal_eval` of the `labels` column, so the counts are of actual labels, not regex hits in free text). The README quotes above are verbatim from `/home/user/ext/mitre-ttp-mapping/README.md`. I did not read the EACL paper full text.
