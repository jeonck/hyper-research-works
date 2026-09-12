---
title: 'CAPTAIN / Chasing the Shadows: TTP-sequence attribution with no declared ATT&CK
  version'
id: captain-chasing-the-shadows-ttp-sequence-attribution-with-no-declared-attck-vers
tags:
- attack-ontology-drift-cti-85bc51
- ttp-attribution
created: '2026-09-12T13:23:59.941436Z'
source: https://arxiv.org/abs/2409.16400
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Reference automated TTP-attribution pipeline (TTPXHunter extraction + kill-chain
  sequencing + sequence similarity) that names no ATT&CK release for either its evidence
  or its group profiles.
---

## What this is
Rani, Saha, Conti et al., *Chasing the Shadows: TTPs in Action to Attribute Advanced Persistent Threats*, arXiv:2409.16400 (2024). Introduces **CAPTAIN** (Comprehensive Advanced Persistent Threat AttrIbutioN), the current reference design for automated TTP-based threat-actor attribution.

## Method (search-summary fidelity)
Three stages:
1. **TTP extraction** — builds a structured TTP database from vendor threat reports using **TTPXHunter** (same group) to map natural-language descriptions to ATT&CK techniques.
2. **TTP sequencing** — orders the extracted TTPs along the **Unified Kill Chain** and ATT&CK matrices, so each actor is represented by common behavioural sequences rather than an unordered set, capturing modus operandi.
3. **Attribution matching** — a novel similarity measure over TTP sequences yields the attributed group.

## How it handles ATT&CK versions — the answer is: it does not say
Nothing in the summaries I could obtain names an ATT&CK release for the technique vocabulary, the group profiles, or the actor→TTP ground truth. The pipeline inherits TTPXHunter's undeclared, ~193-class label space (see companion note), and the group ground truth necessarily comes from ATT&CK's own `intrusion-set` → `attack-pattern` relationships at some unrecorded date.

## Why this matters for the query, specifically
TTP-based attribution is **doubly exposed** to ontology drift, in a way the classification literature is not:
- The **actor profile** side drifts. MITRE re-maps group profiles between releases; a technique split into sub-techniques redistributes an actor's profile across new IDs, and a revocation deletes profile entries. Two actors' profiles can therefore converge or diverge purely from bookkeeping.
- The **evidence** side drifts independently, because the extractor is frozen at a different release than the profiles.
- Any similarity measure over sequences is sensitive to label *cardinality*: splitting one technique into six sub-techniques changes both the sequence length and the denominator of every Jaccard/cosine-style score. A parent-collapse normalization (as CTI-Bench does) and a sub-technique-expanded normalization will give materially different attribution rankings from identical evidence.
None of this is addressed in the CAPTAIN description available to me. That gap is precisely the contribution space the query is probing.

## Fidelity
**Search-summary.** arXiv full text not fetchable (egress blocked, 403 confirmed). No verbatim quotation asserted, and no performance numbers are recorded here because I could not verify them. The analysis of double exposure to drift is **my argument**, not a claim made by the paper.
