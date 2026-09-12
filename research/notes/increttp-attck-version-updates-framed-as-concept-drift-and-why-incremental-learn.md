---
title: 'IncreTTP: ATT&CK version updates framed as concept drift — and why incremental
  learning is not enough'
id: increttp-attck-version-updates-framed-as-concept-drift-and-why-incremental-learn
tags:
- attack-ontology-drift-cti-85bc51
- ttp-extraction
created: '2026-09-12T13:24:00.731929Z'
source: https://link.springer.com/chapter/10.1007/978-3-032-23450-6_2
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Closest prior art: treats ATT&CK releases as concept drift and proposes
  incremental learning, but addresses only technique additions, not revocation, sub-technique
  restructuring, tactic reassignment or silent description rewriting.'
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
