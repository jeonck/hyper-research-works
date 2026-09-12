---
title: 'CTI-Bench data audit: v15-era vocabulary hard-coded into prompts, sub-techniques
  erased, attribution task unlabelled'
id: cti-bench-data-audit-v15-era-vocabulary-hard-coded-into-prompts-sub-techniques-e
tags:
- attack-ontology-drift-cti-85bc51
- cti-benchmarks
created: '2026-09-12T13:21:47.680448Z'
source: https://github.com/maveryn/cti-bench
status: draft
type: note
tier: ground_truth
content_type: dataset
deprecated: false
summary: CTI-ATE inlines a 202-entry v15-era Enterprise ID list in every prompt and
  its 397 GT ids contain zero sub-techniques; CTI-TAA ships 50 rows with no ground-truth
  column at all.
---

## What this is
Direct audit of the **CTI-Bench** data release (cloned at `/home/user/ext/cti-bench`, HEAD `4543e5b`), focusing on the two tasks inside B2's scope: **CTI-ATE** (ATT&CK technique extraction) and **CTI-TAA** (threat-actor attribution).

## CTI-ATE (`data/cti-ate.tsv`) — the ontology is embedded in the prompt, and it is v15-era
Columns: `URL, Platform, Description, Prompt, GT`. **60 rows** — 47 `Enterprise`, 13 `Mobile`.

Findings:
1. **The prompt literally inlines the entire technique vocabulary.** Each Enterprise row's prompt contains a fixed "List of All MITRE Enterprise technique IDs" of **202 `Txxxx : Name` entries**; the Mobile rows inline a **73-entry** Mobile list. The benchmark's ontology is therefore a hard-coded string in the data file, not a versioned reference.
2. **Version dating of that inline list (computed):** it contains T1650 Acquire Access and T1651 Cloud Administration Command (v13), T1652/T1653/T1654/T1656/T1657/T1659 (v14), and **T1665 Hide Infrastructure (added v15, April 2024)**. It does **not** contain v17-era additions (T1664/T1667/T1669/T1673). It also uses post-rename names — "Domain or Tenant Policy Modification" (T1484), "Browser Information Discovery" (T1217), "Indicator Removal" (T1070), "System Binary Proxy Execution" (T1218), "Compromise Host Software Binary" (T1554, renamed from "Compromise Client Software Binary" in v15), "Network Service Discovery" (T1046), "Financial Theft" (T1657). **The label space is ATT&CK v15/v16-era Enterprise.** No version string is recorded in the TSV itself.
3. **Sub-techniques are deliberately erased.** The prompt instructs: extract "only the IDs for the main techniques ... excluding any subtechnique IDs". Across all 60 rows the GT column contains **397 technique-ID occurrences (115 distinct) and zero dot-notation sub-technique IDs.** Enterprise rows: 299 GT ids / 84 distinct; Mobile rows: 98 / 36.
4. Ground truth is derived from ATT&CK's own software/group pages (`URL` column points at e.g. `https://attack.mitre.org/software/S0066/`), so the "gold" labels are MITRE's own mappings at whatever date the page was scraped — a snapshot with no recorded timestamp.

## CTI-TAA (`data/cti-taa.tsv`) — no ground truth ships at all
Columns are only `URL, Text, Prompt`. **50 rows, and there is no `GT` column.** Every attribution item is unlabelled in the public release; the actor name in the source report is masked as `[PLACEHOLDER]`. Threat-actor attribution in CTI-Bench is therefore **not machine-scorable from the released artefact** — it depends on judgement external to the dataset.

## Why this bears on the query
- CTI-ATE is the clearest example of a benchmark that resolves sub-technique restructuring by **collapsing to parent level**. That makes the benchmark partially version-robust (sub-technique splits stop mattering) but it **discards the entire post-v7 hierarchy**, so an "ATT&CK extraction" score on CTI-Bench is a score on 202 coarse classes, not on ATT&CK's ~600-label ontology. Scores are not comparable with sub-technique-level systems (TRAM2, tumeteor/mitre-ttp-mapping) at all.
- Embedding the vocabulary as a literal prompt string means the benchmark **cannot be re-versioned without regenerating every prompt** — the ontology and the task instance are fused.
- The missing GT column in CTI-TAA is a concrete comparability/reproducibility gap for TTP-based attribution evaluation.

## Fidelity
**Read from artefact.** All counts computed by me from `data/cti-ate.tsv` and `data/cti-taa.tsv` in the clone. Version dating is my inference from which IDs/names are present, not a statement the dataset makes about itself. I did not read the CTI-Bench paper full text (egress blocked).
