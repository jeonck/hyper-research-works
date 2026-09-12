---
title: 'CADE: Detecting and Explaining Concept Drift Samples for Security Applications'
id: cade-detecting-and-explaining-concept-drift-samples-for-security-applications
tags:
- attack-ontology-drift-cti-85bc51
- concept-drift
created: '2026-09-12T13:19:25.946495Z'
source: https://www.usenix.org/conference/usenixsecurity21/presentation/yang-limin
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Closest security-side neighbour: detects individual samples deviating from
  existing classes (new-class discovery), but cannot see label-space changes that
  leave features untouched.'
---

## What it is
Yang, Guo, Hao, Ciptadi, Ahmadzadeh, Xing, Wang — "CADE: Detecting and Explaining Concept Drift Samples for Security Applications", USENIX Security 2021. Code: github.com/whyisyoung/CADE (mirror aiforsec/CADE).

## Core claim
Statistical drift detection needs many new labels before it can declare drift; CADE instead flags *individual* drifting samples on arrival. It uses contrastive learning over the existing labelled training set to learn a low-dimensional embedding plus a distance function, then treats samples far (in that learned metric) from every known class centroid as drifting — i.e. as belonging to a class outside the training label set. It adds a distance-based explanation method, arguing that explaining *distance to a class* is more useful here than explaining a decision boundary.

## Relation to ontology drift (label-space vs feature-space)
**Feature-space detection of one specific label-space event: class arrival.** CADE is the most label-space-aware of the mainstream security drift papers — its explicit target is "samples that deviate from *existing classes*", which is open-set/new-class detection, not mere covariate shift. That makes it the closest neighbour in the security literature to the manuscript's concern, and it must be cited as such.

But the coverage is one-directional and data-driven. CADE discovers that a *new class exists in the wild* because samples show up that fit none of the old ones. ATT&CK ontology drift is a curatorial event in a *document*: the class list changes by editorial fiat, with no new samples required and often no change to the underlying adversary behaviour at all. CADE has no representation for deprecation, revocation, merge, split-into-sub-technique, tactic reassignment, or in-place redefinition of a retained identifier. Crucially, ATT&CK's dominant structural event — a technique being *refined into sub-techniques*, so that one old label maps to many new ones over the same behaviours — produces **no drift signal in feature space whatsoever**, because the samples are identical; only the answer key moved.

## Why it matters for this manuscript
CADE marks the frontier of what security-side drift work reaches: new-class *discovery* from data. The manuscript should position ontology drift one step beyond that frontier — change in the label vocabulary that is (a) not discoverable from feature-space statistics, (b) not necessarily accompanied by any change in adversary behaviour, and (c) bidirectional (labels vanish as well as appear). That triple is a clean statement of novelty.

## Fidelity
Summary-level only. Method description from the abstract and search-result summaries; the USENIX PDF was not retrievable (egress blocked, 403). The analysis of what CADE does not cover is my inference from the method as described, not from a stated limitation in the paper. No verbatim quotation given.
