---
title: 'CTIBench CTI-ATE gold-label forensics: 60 items, 115 techniques, zero sub-techniques,
  undeclared ATT&CK v15 pin'
id: ctibench-cti-ate-gold-label-forensics-60-items-115-techniques-zero-sub-technique
tags:
- attack-ontology-drift-cti-85bc51
- cti-benchmarks
created: '2026-09-12T13:20:11.215432Z'
source: https://github.com/maveryn/cti-bench
status: draft
type: note
tier: ground_truth
content_type: dataset
deprecated: false
summary: 'Direct inspection of CTIBench''s released cti-ate.tsv: all 60 gold items
  are transcribed from attack.mitre.org software pages, 397 labels over 115 techniques
  with zero sub-technique IDs, and the prompt embeds a frozen 202-technique Enterprise
  catalogue matching ATT&CK v15.x that the repo never declares.'
---

# CTIBench CTI-ATE gold-label forensics (repo inspection)

## What it is
The released gold-label files of CTIBench (NeurIPS 2024 Datasets & Benchmarks, Spotlight; Alam, Bhusal, Nguyen, Rastogi), inspected directly from the public GitHub repo cloned locally at `/home/user/ext/cti-bench`.

Files inspected:
- `/home/user/ext/cti-bench/README.md`
- `/home/user/ext/cti-bench/data/cti-ate.tsv` (ATT&CK Technique Extraction — the ATT&CK-labelled task)
- `/home/user/ext/cti-bench/data/cti-mcq.tsv`, `cti-rcm.tsv`, `cti-rcm-2021.tsv`, `cti-vsp.tsv`, `cti-taa.tsv` (headers/row counts)
- `/home/user/ext/cti-bench/evaluation/` (notebooks, `alias_dict.pickle`, `related_dict.pickle`, `responses/*.tsv`)

## How the ATT&CK labels were actually built (measured, not paraphrased from the paper)
`cti-ate.tsv` has columns `URL / Platform / Description / Prompt / GT` and **60 data rows**. Every single `URL` value (60/60) points at `attack.mitre.org/software/S####/` — i.e. the gold labels are not independent expert annotation of field CTI reports, they are **transcriptions of MITRE's own software-page technique associations**, with the page prose lightly rewritten into the `Description` column. The label-generating process is therefore *definitionally* a snapshot of one ATT&CK release: whatever MITRE listed on those software pages at scrape time.

Measured label statistics:
- 397 total technique-ID mentions across the 60 rows; **115 unique technique IDs**; mean ~6.6 labels/item.
- **0 sub-technique IDs.** Not one `Txxxx.yyy` appears in any GT cell. The prompt enforces this explicitly, instructing the model to give "only the IDs for the main techniques ... excluding any subtechnique IDs."
- Platform split: 47 rows `Enterprise`, 13 rows `Mobile`.
- Most frequent labels: T1059 (24), T1071 (23), T1140 (18), T1573 (16), T1083 (15), T1105 (13).

## The implicit, undeclared ATT&CK version pin
Each prompt embeds a closed reference list ("**List of All MITRE Enterprise technique IDs**") that the model must choose from. That list is **byte-identical across all 47 Enterprise rows** (1 distinct list) and across all 13 Mobile rows (1 distinct list), so it is a single frozen catalogue.

- Enterprise reference list: **exactly 202 unique technique IDs, 0 sub-techniques**, highest ID T1665.
- Mobile reference list: **exactly 73 unique technique IDs**, highest ID T1664.

Version-marker probes against the Enterprise list:
- present: T1650, T1656, T1657, T1659 (all added in ATT&CK v14, Oct 2023), T1653 (v13), and **T1665 "Hide Infrastructure" (added in v15, April 2024)**.
- absent: T1667, T1668, T1669, T1671, T1674 (all v17-era, April 2025).

An Enterprise catalogue of 202 top-level techniques that includes T1665 but no v16/v17 additions matches **ATT&CK Enterprise v15.x (April–October 2024)**; the Mobile count of 73 is consistent with Mobile v15. This version pin is *implicit in the prompt payload only*. Grepping the whole repo (`*.md`, `*.ipynb`, `*.html`) for any ATT&CK version declaration (`ATT&CK v##`, `enterprise-attack-1#`, etc.) returns **nothing**. The README, the project page and the dataset card never state which ATT&CK release the labels came from.

## A concrete label defect traceable to ontology bookkeeping
Row `https://attack.mitre.org/software/S0440/` (Agent Smith) is tagged `Platform = Enterprise` but its GT is `T1577, T1404, T1643, T1628, T1630, T1655, T1406` — all **Mobile** technique IDs. Consequence: **7 gold IDs in that item do not exist in the 202-ID Enterprise reference list the prompt hands the model**. The item is unanswerable as posed: any model obeying the prompt's closed-world instruction is guaranteed to score 0 on it. This is exactly the failure mode where a matrix/domain reassignment in the ontology silently corrupts a benchmark item.

## Citable claims
- CTIBench's ATT&CK task is 60 items, 397 labels, 115 unique techniques, **zero sub-technique granularity**, sourced 100% from `attack.mitre.org` software pages.
- Its effective label space is a frozen 202-technique Enterprise catalogue + 73-technique Mobile catalogue, consistent with **ATT&CK v15.x**, but **no release version is declared anywhere in the repository or README**.
- At least 1 of 60 items (1.7%) carries a platform/label-space mismatch making 7 of its 397 labels (1.8% of all labels) unreachable under the item's own prompt.
- Repo self-reported totals: CTI-MCQ 2,500 / CTI-RCM 1,000 / CTI-RCM-2021 1,000 / CTI-VSP 1,000 / CTI-ATE 60 / CTI-TAA 50 = 4,610 released examples. The ATT&CK-labelled portion is **60/4,610 = 1.3%** of the benchmark.
- The repo ships `alias_dict.pickle` and `related_dict.pickle` for scoring CTI-TAA — i.e. threat-actor attribution is scored through an alias/related-group lookup table, itself an ATT&CK-derived artifact with no version stamp.

## Fidelity
Ground truth. All numbers above were computed directly from the released TSV files in the cloned repo, not read from the paper. The version inference (v15.x) is *my* inference from technique-count and ID-membership evidence, not a statement made by the authors — the authors state no version at all. I could not read the CTIBench paper PDF full text (arxiv.org and publisher domains are egress-blocked); claims attributed to the paper elsewhere are at summary fidelity.
