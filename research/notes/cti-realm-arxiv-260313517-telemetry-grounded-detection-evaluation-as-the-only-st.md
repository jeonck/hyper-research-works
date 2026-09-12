---
title: 'CTI-REALM (arXiv 2603.13517): telemetry-grounded detection evaluation as the
  only structurally drift-resistant CTI benchmark design'
id: cti-realm-arxiv-260313517-telemetry-grounded-detection-evaluation-as-the-only-st
tags:
- attack-ontology-drift-cti-85bc51
- cti-benchmarks
created: '2026-09-12T13:24:05.355501Z'
source: https://arxiv.org/abs/2603.13517
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Scores agents on detection rules fired against authentic telemetry from sandboxed
  Azure attack emulations rather than on ATT&CK ID-string matching, making it the
  one design in this batch immune to renumbering and sub-technique splits, at the
  cost of relocating irreproducibility from ontology versioning to environment versioning.
---

# CTI-REALM (arXiv:2603.13517) — moving the gold standard from ATT&CK labels to executed telemetry

## What it is
*CTI-REALM: Benchmark to Evaluate Agent Performance on Security Detection Rule Generation Capabilities* (Cyber Threat Real-world Evaluation and LLM Benchmarking, 2026). A packaged variant exists at https://github.com/AnyEvalOrg/eval-cti_realm ("packaged for OpenEvalz, sandbox-local").

## What it says bearing on the query
CTI-REALM evaluates AI agents on **end-to-end detection engineering**, not on label agreement. It is grounded in **authentic telemetry from real attack emulations executed on sandboxed Azure infrastructure**; agents use specialised tools to analyse CTI reports and construct queries that produce **detection rules**, which are then evaluated against that telemetry.

## Why this is the most important methodological contrast in the batch
Every other benchmark here (CTIBench, AthenaBench, CTIArena/CTIConnect, TRAM-derived sets) scores a model by whether its predicted **ATT&CK technique ID string** matches a human- or MITRE-assigned ID string. That metric is *definitionally* hostage to ontology drift: renumber a technique, split it into sub-techniques, revoke it, or reassign its tactic, and the score moves without any change in the model, the report, or the adversary.

CTI-REALM breaks that dependency by making the ground truth **executed behaviour in telemetry**: a detection rule either fires on the emulated attack's real events or it does not. Technique IDs become an intermediate representation rather than the thing being scored. This is the only design in this batch that is **structurally drift-resistant** at the metric layer.

The cost is equally important for positioning: telemetry-grounded evaluation is expensive, small-scale, environment-specific (Azure sandbox, specific emulation set), and its own kind of unreproducible — the emulation infrastructure is harder to version and share than a TSV of IDs. So it does not dissolve the problem; it relocates it from *ontology versioning* to *environment versioning*.

## Bearing on an SCI-level contribution
It marks the boundary of what a normalization protocol must cover. A credible protocol needs to (a) restore comparability for the large existing body of ID-matching analytics, and (b) state explicitly when a claim should instead be grounded in telemetry because no amount of ID normalization can rescue it — coverage and mitigation-efficacy claims in particular, which are about whether a detection *works*, not about whether an ID *matches*.

## Citable claims
- CTI-REALM evaluates agents on end-to-end detection-rule generation against **authentic telemetry from real attack emulations on sandboxed Azure infrastructure**.
- It is an **ID-matching-free** CTI benchmark design, in contrast to CTIBench/AthenaBench/CTIArena.
- A repackaged evaluation harness exists at `AnyEvalOrg/eval-cti_realm` (created 2026-08).

## Fidelity
**Summary fidelity.** arxiv.org is egress-blocked; the description comes from search-result snippets of the abstract, not full text, and contains no verified verbatim quotation. I did not clone or inspect `AnyEvalOrg/eval-cti_realm` (out of this batch's four-search budget); its rule set, telemetry format, and whether it references any ATT&CK release are unexamined.
