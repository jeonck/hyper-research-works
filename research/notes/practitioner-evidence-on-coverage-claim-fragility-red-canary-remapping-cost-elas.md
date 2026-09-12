---
title: 'Practitioner evidence on coverage-claim fragility: Red Canary remapping cost,
  Elastic v19 remap docs, and the counting-rules-not-coverage critique'
id: practitioner-evidence-on-coverage-claim-fragility-red-canary-remapping-cost-elas
tags:
- attack-ontology-drift-cti-85bc51
- coverage-claims
created: '2026-09-12T13:24:45.273243Z'
source: https://redcanary.com/blog/threat-detection/mitre-sub-techniques/
status: draft
type: note
tier: practitioner
content_type: blog
deprecated: false
summary: Red Canary painstakingly remapped thousands of behavioural analytics after
  sub-techniques; vendors still ship v19 remap docs; and coverage heatmaps are criticised
  as counting tagged rules rather than protection - a metric that moves whenever the
  ID space moves.
---

## What this is
*IncreTTP: An Incremental TTPs Classification Model* (Springer, chapter DOI 10.1007/978-3-032-23450-6_2). The only work located in this batch that treats **ATT&CK version updates as the primary problem** rather than as an implementation detail.

## What it says bearing on the query (search-summary fidelity)
- Problem statement: current TTP classification models are "predominantly static and heavily dependent on **fixed versions** of the ATT&CK framework", which limits their ability to adapt to knowledge-base updates while balancing performance, efficiency and parameter scale.
- It frames the evolution of ATT&CK — new techniques and attack patterns appearing across releases — explicitly as **concept drift**, and proposes **incremental/continual learning** so that a model absorbs a new release without full retraining.

## Why this is the closest prior art to the query's thesis, and where it stops short
IncreTTP establishes that the field recognises version dependence as a research problem. But (from what is visible in summaries) it addresses only **one of the six drift modes** in the query — *technique additions*. Incremental learning gives you new classes; it does not tell you what to do about:
- **revocations and deprecations** (labels that must be retired or forwarded, not learned),
- **sub-technique restructuring** (one class becoming a hierarchy — a re-parameterisation of the label space, not an addition to it),
- **tactic reassignment** (the same technique changing its position in the taxonomy, which silently invalidates tactic-level metrics),
- **silent description rewriting** (the text a model was trained to associate with a label changes while the label ID stays fixed — a pure feature-distribution shift, invisible to any ID-level diff).

That last mode is the one no incremental-learning framing can absorb, because the drift is inside the class definition, not in the class inventory. **This is the strongest single argument in B2 for why a drift-aware normalization protocol is a distinct contribution from incremental learning.**

## Fidelity
**Search-summary.** Springer full text not fetchable (egress blocked). The quoted phrase "predominantly static and heavily dependent on fixed versions" is reproduced from a search-result summary of the chapter and should be re-verified against the published text before being used as a quotation. The four-drift-modes critique is my analysis, not the chapter's.
