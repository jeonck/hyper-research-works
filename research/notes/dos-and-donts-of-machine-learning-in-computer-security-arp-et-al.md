---
title: Dos and Don'ts of Machine Learning in Computer Security (Arp et al.)
id: dos-and-donts-of-machine-learning-in-computer-security-arp-et-al
tags:
- attack-ontology-drift-cti-85bc51
- concept-drift
created: '2026-09-12T13:19:25.417608Z'
source: https://www.usenix.org/conference/usenixsecurity22/presentation/arp
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Ten pitfalls of security ML including label inaccuracy and temporal snooping,
  all assuming a static class vocabulary; the natural home for an eleventh pitfall
  covering ontology drift.
---

## What it is
Arp, Quiring, Pendlebury, Warnecke, Pierazzi, Wressnegger, Cavallaro, Rieck — USENIX Security 2022; a revised/condensed version appeared as "Pitfalls in Machine Learning for Computer Security", Communications of the ACM 67(6), 2024 (doi 10.1145/3643456). Preprint arXiv:2010.09470.

## Core claim
Ten recurring, subtle pitfalls afflict learning-based security systems across design, implementation and evaluation — among them sampling bias, label inaccuracy, data snooping (temporal, selective and test-set snooping), spurious correlations, inappropriate baselines, inappropriate performance measures, base-rate fallacy, lab-only evaluation, and inappropriate threat models. A review of 30 papers from top-tier security venues over ~10 years found every pitfall present in a substantial fraction of the corpus, often unacknowledged. The paper pairs each pitfall with actionable recommendations and flags open problems.

## Relation to ontology drift (label-space vs feature-space)
**Closest existing hook, but still short of the target.** Two of the ten pitfalls are adjacent to ontology drift:
- *Label inaccuracy* — the paper treats ground-truth labels as potentially noisy or wrong, but as noise around a **fixed, well-defined class vocabulary**. It does not treat the vocabulary itself as a versioned, mutating artefact.
- *Data snooping (temporal)* — treats leakage of future *data* into training, again with labels held semantically constant.

What is absent is the case where the label set L_t at annotation time differs structurally from L_{t'} at evaluation time: a class present in L_t is deprecated or revoked in L_{t'}; a class is split into sub-classes; a class is reparented to a different tactic/superclass; a class keeps its identifier but has its definition rewritten. Under Arp et al.'s taxonomy this would register, at best, as unexplained "label inaccuracy" — which mislocates the cause and therefore the remedy (better annotators will not fix it; version pinning and a migration map will).

## Why it matters for this manuscript
This is the paper the manuscript should explicitly extend. The rhetorical move available: Arp et al. enumerate ten pitfalls under the implicit assumption of a static label ontology; CTI analytics built on ATT&CK violate that assumption structurally, so the list needs an eleventh entry — *ontology drift / label-vocabulary snooping* — with its own recommendation set (declare the ATT&CK version, report labels under a single normalized version, publish the migration map, separate genuine-growth from bookkeeping-growth when claiming coverage). Framing the contribution as "pitfall #11, in the house style of Arp et al." is a credible SCI-level positioning.

## Fidelity
Summary-level only. Pitfall list and study design taken from the abstract and widely reproduced summaries via search results; full PDF (usenix.org/system/files/sec22summer_arp.pdf) was not retrievable through the blocked egress proxy. The specific enumeration of the ten pitfalls above is from general knowledge of this well-known paper and should be re-verified against the PDF before citation in the manuscript. No verbatim quotation given.
