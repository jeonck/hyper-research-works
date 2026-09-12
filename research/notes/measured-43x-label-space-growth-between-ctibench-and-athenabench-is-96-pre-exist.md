---
title: 'Measured: 4.3x label-space growth between CTIBench and AthenaBench is ~96%
  pre-existing catalogue, only 6 new top-level techniques'
id: measured-43x-label-space-growth-between-ctibench-and-athenabench-is-96-pre-exist
tags:
- attack-ontology-drift-cti-85bc51
- cti-benchmarks
created: '2026-09-12T13:25:02.031511Z'
source: https://github.com/Athena-Software-Group/athenabench
status: draft
type: note
tier: ground_truth
content_type: dataset
deprecated: false
summary: 'Direct computation over both cloned benchmark files: distinct gold ATT&CK
  IDs grew 115 to 500 across the v15-to-v17 transition, but 70.4% of the new labels
  are sub-techniques of pre-existing parents, 155 of 161 parents were already in the
  v15 catalogue, and exactly 6 genuinely new top-level techniques appear, with parent-space
  Jaccard of only 0.26 between the two benchmarks.'
---

# Cross-benchmark label-space measurement: CTIBench vs AthenaBench, and how much "growth" is bookkeeping

## What this is
A computed comparison between the two released ATT&CK-labelled benchmark files in this batch, both produced by overlapping author teams roughly one year apart. Everything below was measured from the cloned repos, not read from either paper.

Files: `/home/user/ext/cti-bench/data/cti-ate.tsv` and `/home/user/ext/athenabench/benchmark/athena-cti-ate.jsonl`.

## The measurements

**Label spaces.**
| | CTIBench CTI-ATE | AthenaBench ATE |
|---|---|---|
| items | 60 | 500 |
| gold labels | 397 (multi-label) | 500 (single-label) |
| distinct gold IDs | 115 | 500 |
| sub-technique IDs in gold | **0 (0.0%)** | **352 (70.4%)** |
| distinct parent techniques | 115 | 161 |
| effective catalogue | 202 Enterprise + 73 Mobile (frozen, in-prompt) | live-API, none declared |
| era inferred from max ID | T1665 → **ATT&CK v15.x** | T1675 → **v17 era** |

**Overlap.**
- Parent-technique overlap between the two gold sets: **57** shared; 58 CTIBench-only; 104 AthenaBench-only. Jaccard ≈ 0.26.
- Of CTIBench's frozen 202-technique v15 Enterprise catalogue, **155 of AthenaBench's 161 parent techniques (96.3%) were already present**.
- AthenaBench parent techniques absent from the v15 catalogue: **exactly 6** — T1666, T1667, T1669, T1671, T1672, T1675.

## What this establishes for the query's second question
Between the v15-era benchmark and the v17-era benchmark — roughly two years of ATT&CK releases — the label space visible to these benchmarks grew from 115 to 500 distinct gold IDs, a **4.3× expansion**. Decomposed:

- **Genuinely new top-level techniques: 6** (T1666, T1667, T1669, T1671, T1672, T1675) — **3.7%** of AthenaBench's 161-parent space, and **1.2%** of its 500-ID gold label space.
- **Descent into pre-existing sub-techniques: 352 of 500 gold IDs (70.4%)** — these are refinements of techniques that already existed in the v15 catalogue, i.e. the ontology re-cut what was already there.
- **Re-sampling of already-catalogued parents: 155 of 161 parents (96.3%)** were available to CTIBench and simply not sampled by its 60-item design.

So on the only direct like-for-like measurement available in this batch, **the overwhelming majority of apparent label-space growth between two ATT&CK-derived CTI benchmarks is ontology bookkeeping — sub-technique decomposition and denser sampling of an existing catalogue — not new adversary intelligence.** A defensible headline framing: *of the 4.3× growth in distinct gold labels, on the order of 1–4% is attributable to newly catalogued top-level adversary techniques.*

Caveat stated plainly: this is a bound computed from two benchmarks' *sampled* label spaces, not from a full release-to-release diff of ATT&CK itself. A full diff (v15 → v17 technique/sub-technique adds, deprecations, revocations) would be the authoritative version of this number and is not in scope for this batch.

## What this establishes for the query's first question
The two benchmarks report the same-named metric ("ATE accuracy/F1") over label spaces sharing only ~26% of their parent techniques, with 0% vs 70.4% sub-technique granularity, one multi-label and one single-label, one drawn from MITRE's own software-page prose and one from LLM-written synthetic scenarios. **No score on one is comparable to a score on the other**, yet the literature treats them as successive measurements of the same capability. Reported ATE numbers rise steeply across the transition (AthenaBench README: GPT-4 35.8 → GPT-5 76.0), and none of that delta can be cleanly attributed to model capability.

## What a normalization protocol must therefore report
Derived from what was missing in both repos:
1. **Declare the release** — exact ATT&CK version and domain(s) (`enterprise-attack-15.1`, `mobile-attack-15.1`), stated in the dataset card, not implied by an in-prompt ID list.
2. **Declare the granularity contract** — top-level only, sub-technique, or mixed; and whether sub-technique predictions are rolled up to parents before scoring.
3. **Declare label arity** — single-label vs multi-label, and whether gold arity is leaked to the model (AthenaBench RMS leaks it in 500/500 items).
4. **Ship a remap table** — deprecated/revoked/split IDs with their successor mapping, so a score can be recomputed under a target release.
5. **Report a drift-adjusted score** alongside the raw one: raw score, score after remapping to a common release, and the number of items that become unscorable under remapping.
6. **Validate label-space closure** — every gold ID must exist in the declared release *and* in any closed-world list handed to the model. CTIBench fails this on item S0440 (7 Mobile IDs against an Enterprise-only reference list).
7. **Version the auxiliary tables** — alias and related-group tables used for attribution scoring (AthenaBench ships 1,611 alias rows and 2,091 related-group rows, unversioned) are ontology artifacts and drift with Group merges and renames.

## Fidelity
**Ground truth** for every count, overlap and percentage above — all computed directly from the two cloned repositories in this session. The ATT&CK release attributions (v15.x, v17-era) are **my inference** from technique-ID membership and catalogue size, since neither repository declares a version; they are labelled as inference, not as author claims. The normalization-protocol list is my synthesis of observed gaps, not a protocol proposed by any source read in this batch.
