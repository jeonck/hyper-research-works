---
title: 'TTPrint (arXiv 2605.25836): TRAM-Clean fork and verification against official
  ATT&CK descriptions'
id: ttprint-arxiv-260525836-tram-clean-fork-and-verification-against-official-attck
tags:
- attack-ontology-drift-cti-85bc51
- cti-benchmarks
created: '2026-09-12T13:22:37.422946Z'
source: https://arxiv.org/abs/2605.25836
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Second independent 2026 rejection of TRAM's labels, shipping a cleaned TRAM-Clean
  plus a document-level TTPrint-Bench (Macro-F1 76.48 and 87.39); its verification
  stage adjudicates candidate techniques against the official ATT&CK description,
  making its scores explicitly release-conditional.
---

# TTPrint (arXiv:2605.25836) — TRAM-Clean, and verification against official technique descriptions

## What it is
*TTPrint: Evidence-Grounded TTP Extraction via Diverge-then-Converge Verification* (2026). A four-stage TTP-extraction pipeline plus **two new evaluation resources**.

## What it says bearing on the query
Architecture: a **divergent** phase decomposes a CTI report into atomic attack behaviours and proposes a deliberately broad candidate set of ATT&CK techniques per behaviour (coverage over confidence); a deterministic **span-localisation** stage anchors each candidate to a specific sentence window so downstream reasoning is confined to verifiable textual evidence; a **convergent** verification stage scores each candidate against *both* its localised evidence span **and the official MITRE ATT&CK technique description**, keeping only those above a confidence threshold.

Two contributed resources, both motivated by label quality:
- **TRAM-Clean** — a *cleaned* version of the TRAM benchmark, created explicitly "to address known annotation noise in existing benchmarks."
- **TTPrint-Bench** — a new annotated dataset at **document level** rather than sentence level.

Reported: Macro-F1 **76.48% on TRAM-Clean** and **87.39% on TTPrint-Bench**, beating the leading baseline by **63.5%** and **29.4%** relative.

## Why this matters for the drift argument
1. **Independent corroboration that TRAM's labels are noisy enough to require a cleaned fork.** Two separate 2026 papers (this and arXiv:2606.18166) independently reject TRAM's annotations as-is. TRAM is a primary training/eval set for ATT&CK mapping, so its defects propagate into much of the TTP-extraction literature.
2. **It hard-codes the drift dependency into the algorithm.** TTPrint's verification step consults the *official ATT&CK technique description* as the decision criterion. That makes the system's output a function of the ATT&CK release it is pointed at — the same input report can yield a different technique set after a release that rewrites a description or splits a technique into sub-techniques. A cross-version reproducibility claim for TTPrint therefore requires stating the release; the reported 76.48/87.39 figures are release-conditional scores.
3. **Fragmentation as bookkeeping.** Now in circulation: TRAM, TRAM-Clean, TTPrint-Bench, plus the 2,076-sentence set of arXiv:2606.18166 — four gold standards over the same underlying task, none obviously version-stamped, none mutually score-comparable. This is the benchmark-layer analogue of the ATT&CK-layer drift the query targets.

## Citable claims
- TTPrint Macro-F1: **76.48% (TRAM-Clean)**, **87.39% (TTPrint-Bench)**; relative gains over the leading baseline of **63.5%** and **29.4%**.
- Contributes **TRAM-Clean**, a cleaned TRAM benchmark explicitly addressing known annotation noise, and **TTPrint-Bench**, a document-level annotated set.
- Its verification stage adjudicates candidates against the **official MITRE ATT&CK technique description**.

## Fidelity
**Summary fidelity.** arxiv.org is egress-blocked; the description above is assembled from search-result snippets of the abstract/method, not the full text. No verbatim quotation is claimed. I could not determine whether TTPrint or TRAM-Clean names an ATT&CK release version, nor how many techniques TRAM-Clean retains after cleaning — both are open gaps.
