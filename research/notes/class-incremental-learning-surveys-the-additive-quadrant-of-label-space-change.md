---
title: 'Class-Incremental Learning surveys: the additive quadrant of label-space change'
id: class-incremental-learning-surveys-the-additive-quadrant-of-label-space-change
tags:
- attack-ontology-drift-cti-85bc51
- concept-drift
created: '2026-09-12T13:20:37.879317Z'
source: https://arxiv.org/abs/2302.03648
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: CIL formalises a label space that grows over time, covering technique additions
  only; no operation exists for removal, merge, split, reparenting or in-place redefinition.
---

## What it is
Zhou, Wang, Ye, Zhan, Liu et al. — "Deep Class-Incremental Learning: A Survey" / "Class-Incremental Learning: A Survey" (arXiv:2302.03648; HTML v2). Representative entry point to the class-incremental learning (CIL) literature; a 2026 Chinese-language review ("Recent advances in class-incremental learning", sciopen 10.11887/j.issn.1001-2486.26020018) covers the same ground.

## Core claim
Standard supervised learning assumes a fixed label space with all data available at once. CIL instead requires a model to absorb new classes over time **with the label space expanding**, while preserving performance on classes learned earlier; the central obstacle is catastrophic forgetting when only current-stage data is accessible. The survey taxonomises methods (regularisation, replay/rehearsal, dynamic architectures, prototype/representation methods), benchmarks them, and maps open directions (semi-supervised CIL, noisy labels, long-tailed CIL).

## Relation to ontology drift (label-space vs feature-space)
**Label-space — but only the additive, append-only case.** CIL is precisely "the label space grows", which is the closest general-ML framing of what happens when ATT&CK adds techniques. It is therefore the right citation for the *addition* quadrant of ontology drift.

Its limits are structural, not incidental:
- **Monotone growth.** Classes are added; the existing classes remain valid, disjoint and semantically stable. CIL has no operation for removing a class (deprecation), for redirecting a class to another (revocation), for splitting one class into several (sub-technique restructuring changes the *meaning* of the parent, not just adds siblings), for reparenting (tactic reassignment), or for rewriting a class's definition in place.
- **Forgetting, not comparability.** The evaluated quantity is accuracy retention across stages under a growing label set. Nobody asks whether results reported at stage t and stage t+1 are on the same scale, which is exactly the manuscript's question about CTI results reported against different ATT&CK versions.
- **Labels as indices.** CIL treats a class as an integer index with associated exemplars; there is no notion of an *intension* (a written definition) that can change while the index stays put — the silent-rewrite case.

Adjacent recent work does start to push past monotone addition and is worth citing alongside: "When Classes Evolve: A Benchmark and Framework for Stage-Aware Class-Incremental Learning" (arXiv:2602.00573), where a single semantic class undergoes structured morphological evolution; "Online Continual Learning with Dynamic Label Hierarchies" (arXiv:2605.11742); and "Taxonomy-Aware Continual Semantic Segmentation in Hyperbolic Spaces for Open-World Perception" (arXiv:2407.18145), which makes the taxonomy structure itself a first-class object.

## Why it matters for this manuscript
CIL lets the manuscript say precisely which quadrant of ontology drift is already covered by mainstream ML (additive growth) and which are not (deprecation, revocation, split/merge, reparenting, intension rewriting). It also supplies useful vocabulary — "label space expanding over time" — that a reviewer will recognise, making the novelty claim legible rather than eccentric.

## Fidelity
Summary-level only. Based on abstracts and search-result summaries of the survey and the adjacent arXiv entries listed above; no PDF was retrievable (egress proxy 403). Author list and taxonomy categories are from general knowledge of this survey and should be re-verified before citation. The adjacent-work titles/IDs come from search results and have not been read. No verbatim quotation given.
