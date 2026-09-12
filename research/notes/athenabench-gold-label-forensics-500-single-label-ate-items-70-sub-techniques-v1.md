---
title: 'AthenaBench gold-label forensics: 500 single-label ATE items, 70% sub-techniques,
  v17-era, no version pin'
id: athenabench-gold-label-forensics-500-single-label-ate-items-70-sub-techniques-v1
tags:
- attack-ontology-drift-cti-85bc51
- cti-benchmarks
created: '2026-09-12T13:21:05.917718Z'
source: https://github.com/Athena-Software-Group/athenabench
status: draft
type: note
tier: ground_truth
content_type: dataset
deprecated: false
summary: 'Direct inspection of AthenaBench''s released JSONL: ATE is 500 single-label
  items with 70.4% sub-technique IDs reaching T1675 (v17 era), overlapping CTIBench''s
  technique space on only 57 parents, with attribution scored through 1,611 aliases
  and 2,091 related-group edges and no ATT&CK version declared.'
---

# AthenaBench gold-label forensics (repo inspection)

## What it is
The released benchmark files of **AthenaBench: A Dynamic Benchmark for Evaluating LLMs in Cyber Threat Intelligence** (WAITI Workshop 2025; Alam, Bhusal, Ahmad, Rastogi, Worth — arXiv:2511.01144), the direct successor to CTIBench by overlapping authors. Cloned to `/home/user/ext/athenabench`.

Files inspected: `readme.md`; `benchmark/athena-cti-{ate,rms,taa,ckt-3k,rcm,vsp}.jsonl`; `benchmark-mini/*`; `athena_eval/taa/aliases.csv`; `athena_eval/taa/related_groups.csv`; `athena_eval/config.yaml`; `athena_eval/{run,evaluate,answer_extractors}.py`.

## Measured structure
| Task | n (full) | n (mini) | label shape |
|---|---|---|---|
| CKT (knowledge) | 3,000 | — | 5-option MCQ (a–e) |
| ATE (technique extraction) | 500 | 100 | **one** ATT&CK technique ID per item |
| RMS (risk mitigation, new task) | 500 | — | ordered set of ATT&CK M-IDs |
| RCM | 2,000 | — | CWE |
| VSP | 2,000 | — | CVSS v3.1 vector |
| TAA | 100 | — | threat-actor name |

ATE, measured from `benchmark/athena-cti-ate.jsonl`:
- 500 items, **500 distinct technique IDs** (exactly one item per technique — a one-shot sweep over the catalogue, not a sample of real reports).
- **352/500 = 70.4% of gold labels are sub-technique IDs** (`Txxxx.yyy`), spanning **161 distinct parent techniques**.
- 0 multi-label items. `answer == technique_id` for all 500.
- Highest IDs present include T1667, T1669, T1671, T1672, **T1675** — all v17-era (2025) additions.
- Each item is a **synthetic `scenario`** paired with a `description` copied from the ATT&CK technique page; the model must name the single technique.

RMS (`athena-cti-rms.jsonl`): 500 items, 500 distinct technique IDs (same 70.4% sub-technique share), gold answers drawn from **44 distinct ATT&CK mitigation IDs**; most common M1018 (104), M1026 (101), M1047 (91), M1038 (68), M1056 (68). Gold arity is heavily skewed: 1 mitigation (194 items), 2 (118), 3 (78), 4 (50), 5 (26), 6–10 (34). Each prompt states the required count, and **prompt-requested arity equals gold arity in 500/500 items** (verified) — so the arity is leaked to the model as an evaluation scaffold.

TAA (`athena-cti-taa.jsonl`): 100 items, each with an explicit `timestamp`, **ranging 2024-04 to 2025-07**, mass concentrated in 2025-02..2025-06; only **54 distinct gold actor names** across 100 items. Scored against `aliases.csv` (**1,611 actor→alias pairs**) and `related_groups.csv` (**2,091 actor→related-group pairs**) — attribution "correctness" is therefore defined by a naming/merger table, not by the actor itself.

## Bearing on the query
1. **The drift is visible as a benchmark discontinuity.** CTIBench ATE (v15-era, main-techniques-only) and AthenaBench ATE (v17-era, 70% sub-techniques) come from the same lab one year apart, and their parent-technique label spaces overlap on only **57 techniques** (CTIBench 115, AthenaBench 161, CTIBench-only 58, AthenaBench-only 104). A score on one is not comparable to a score on the other, yet both are reported as "ATE accuracy/F1."
2. **"Dynamic" benchmarking removes the version pin rather than declaring it.** AthenaBench's stated remedy for CTIBench's staleness is to regenerate items from **live** MITRE ATT&CK and NVD APIs. That fixes currency and worsens reproducibility: a live-API benchmark has, by construction, no stable release identifier, and the repo contains **no ATT&CK version declaration anywhere** (grep for `ATT&CK v#`/`enterprise-attack-1#` across `*.py`, `*.yaml`, `*.md`, `*.jsonl` returns only CVE product-version strings, no ATT&CK release).
3. **Attribution scoring is an ontology artifact.** 54 gold actors / 100 items adjudicated through 1,611 aliases + 2,091 "related group" edges means merges, splits and renames in ATT&CK's Groups objects directly move the measured attribution accuracy.
4. **Task-format drift confounds difficulty comparisons.** CTIBench ATE = multi-label, main-technique-only, from real ATT&CK software prose. AthenaBench ATE = single-label, mostly sub-technique, from LLM-written synthetic scenarios. Reported ATE numbers rose sharply (e.g. GPT-4 35.8, GPT-4o 51.6, GPT-5 76.0, Gemini-2.5-pro 76.2 in the AthenaBench README) but the measurement changed underneath.

## Citable claims
- AthenaBench ATE: 500 items / 500 unique techniques / **70.4% sub-technique labels** / 161 parent techniques / max ID T1675 (v17 era).
- AthenaBench vs CTIBench ATE parent-technique overlap: **57 shared, 58 CTIBench-only, 104 AthenaBench-only** — under 30% Jaccard.
- AthenaBench RMS: 500 items, 44 distinct mitigation IDs, prompt leaks gold arity in 500/500 items.
- AthenaBench TAA: 100 items, 54 unique actors, timestamps 2024-04 → 2025-07, scored via a 1,611-row alias table and a 2,091-row related-group table.
- Neither CTIBench nor AthenaBench declares an ATT&CK release version in its repository.

## Fidelity
Ground truth for every count above — computed from the cloned JSONL/CSV files. The README's results tables are quoted as the authors' own reported numbers. The characterisation of AthenaBench's motivation ("static knowledge", live ATT&CK/NVD APIs, duplicate removal) is at **summary fidelity** from search-result snippets of the paper; I could not read arXiv:2511.01144 full text (arxiv.org egress-blocked) and I have not verified those phrases verbatim.
