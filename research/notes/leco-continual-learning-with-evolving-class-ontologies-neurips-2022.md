---
title: 'LECO: Continual Learning with Evolving Class Ontologies (NeurIPS 2022)'
id: leco-continual-learning-with-evolving-class-ontologies-neurips-2022
tags:
- attack-ontology-drift-cti-85bc51
- concept-drift
created: '2026-09-12T13:20:37.601528Z'
source: https://arxiv.org/abs/2210.04993
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'The one prior work squarely on label-space drift: coarse-to-fine ontology
  refinement across time periods, but monotone, training-focused, and without deprecation,
  revocation, reparenting or silent redefinition.'
---

## What it is
Zhiqiu Lin, Deepak Pathak, Yu-Xiong Wang, Deva Ramanan, Shu Kong — "Continual Learning with Evolving Class Ontologies", NeurIPS 2022 (arXiv:2210.04993; project page linzhiqiu.github.io/papers/leco). **This is the single most important source in this batch**: it is the one paper in the surveyed literature whose subject is drift in the label space itself.

## Core claim
LECO formalises learning across distinct time periods (TPs) where **each TP introduces a new ontology of "fine" labels that refines the previous TP's "coarse" labels** — e.g. "dog" in TP1 becomes specific breeds in TP2. This is a real and common phenomenon in production datasets, and the paper names the real-world instances: COCO→LVIS, Mapillary Vistas 1.2→2.0. It poses the operational questions directly: should you annotate new data under the new ontology, or relabel the old data? Can the old coarse labels be exploited rather than discarded? Finetune from the previous TP's model or retrain from scratch? Its headline empirical finding is that the field's status quo — *relabelling existing data under the new ontology* — is the worse strategy; annotating new data under the new ontology, and treating old coarse labels as weak supervision via semi-supervised/pseudo-labelling methods, does better. Evaluated on CIFAR, iNaturalist and Mapillary.

## Relation to ontology drift (label-space vs feature-space)
**Label-space, explicitly and exclusively.** Features and data distribution are held fixed by construction; what changes across time periods is the class vocabulary. This is exactly the family of operations ATT&CK performs when a technique is split into sub-techniques (T1086 PowerShell → T1059.001), which is a coarse→fine refinement of precisely the LECO form.

Where it stops short of ATT&CK ontology drift:
1. **Refinement only.** LECO's ontology change is monotone and structure-preserving: old coarse classes partition into new fine classes, so a well-defined coarse↦fine mapping always exists. ATT&CK also *deprecates* (class removed, no successor), *revokes* (class redirected to a different existing class), *reassigns tactics* (the parent/superclass changes, not the leaf), and *silently rewrites descriptions* (the identifier and position are stable but the intension of the class changes). None of these are LECO operations.
2. **Learning, not measurement.** LECO asks how to *train well* across an ontology change. It does not ask the manuscript's questions: how much of the apparent growth in a knowledge base is real, whether two papers using different ontology versions are comparable, or how to retrospectively normalize a published benchmark's labels.
3. **No security/CTI instantiation.** Vision datasets, not threat-intelligence knowledge bases; no adversary-behaviour semantics, no coverage claims, no attribution.

## Why it matters for this manuscript
LECO is both the strongest prior art and the clearest demonstration of the gap. It proves the label-space-drift problem is recognised and formalisable in mainstream ML — so the manuscript should not claim to invent the concept. It equally proves that the formalisation on offer covers only the benign, monotone, refinement case, and addresses training strategy rather than cross-version comparability of published results. The manuscript's precise novelty statement writes itself: *LECO handles coarse→fine refinement for model training in vision; ATT&CK ontology drift is a non-monotone, multi-operation, intension-changing schema evolution in a security knowledge base, and the open problem is measurement and cross-version comparability rather than continual training.*

## Fidelity
Summary-level only. Drawn from the abstract and search-result summaries (NeurIPS proceedings page, project page, arXiv listing); the PDF was not retrievable through the blocked egress proxy. The COCO→LVIS / Mapillary 1.2→2.0 examples and the "annotate new data beats relabelling old data" finding are reported as summarised, not quoted. No verbatim quotation given; re-verify exact claims against the PDF before citing.
