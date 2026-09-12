---
title: 'Transcend and Transcendent: Conformal Evaluation and Rejection under Concept
  Drift'
id: transcend-and-transcendent-conformal-evaluation-and-rejection-under-concept-drif
tags:
- attack-ontology-drift-cti-85bc51
- concept-drift
created: '2026-09-12T13:19:25.684419Z'
source: https://arxiv.org/abs/2010.03856
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Conformal rejection quarantines samples unlike the training distribution;
  handles new-class arrival in the data but has no mechanism for labels being deprecated,
  merged, split or redefined.
---

## What it is
Two linked works. **Transcend** (Jordaney, Sharad, Dash, Wang, Papini, Nouretdinov, Cavallaro — USENIX Security 2017) introduced conformal evaluation and p-value-based rejection for malware classification under drift. **Transcendent** (Barbero, Pendlebury, Pierazzi, Cavallaro — IEEE S&P 2022; arXiv:2010.03856; code at github.com/s2labres/transcendent-release) gives the formal treatment linking conformal prediction to conformal evaluation, adds cheaper conformal evaluators, and generalises across malware domains and classifiers.

## Core claim
Rather than trying to keep a classifier accurate forever, quarantine the predictions it should not be trusted to make. Nonconformity measures yield per-sample p-values; samples whose conformity to the training distribution is too low are **rejected** and routed to expert analysis instead of being scored. Transcendent shows the original Transcend framework was under-formalised, supplies the missing statistical link, and matches or beats it at lower computational cost.

## Relation to ontology drift (label-space vs feature-space)
**Feature/data-distribution, with a partial and instructive gesture toward label novelty.** The rejection mechanism fires when a *sample* is unlike anything in the calibration set — which in practice includes the case of a genuinely new malware family, i.e. a class not in the training label set. So conformal rejection does touch the open-set / new-class problem. But the direction of change is strictly **additive and sample-driven**: new things appear in the world and the model abstains. There is no machinery for the inverse operations that dominate ATT&CK drift — a class being *withdrawn*, *merged into another*, *renamed while retaining its id*, *split into children*, or *silently redefined*. Nothing in conformal evaluation gives an answer to "the label T1086 no longer exists; what is the correct disposition of the 400 historical samples annotated with it?" Rejection handles unknown-unknowns arriving in the data; it does not handle known labels disappearing from the schema.

## Why it matters for this manuscript
Useful as the strongest counterexample to a reviewer's likely objection ("isn't this just concept drift, already solved by rejection?"). The answer: rejection is a *runtime* response to distributional novelty in X, decided per sample; ontology drift is a *bookkeeping* defect in the label schema that is invisible to any statistic computed over X, because the features of a historical sample do not change when MITRE deprecates its technique. A conformal evaluator would sail past a whole corpus relabelled by a version bump without raising a single rejection.

## Fidelity
Summary-level only. Based on abstracts and search-result summaries for both papers; full texts (arXiv PDF, USENIX page, IEEE S&P) were not retrievable — the egress proxy returns 403. The characterisation of what conformal rejection cannot do is analytic inference from the method's definition, not a quotation of any limitations section. No verbatim quotation given.
