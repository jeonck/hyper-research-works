---
title: 'When Benchmarks Age: quantifying answer-key decay in static benchmarks'
id: when-benchmarks-age-quantifying-answer-key-decay-in-static-benchmarks
tags:
- attack-ontology-drift-cti-85bc51
- concept-drift
created: '2026-09-12T13:21:41.963319Z'
source: https://arxiv.org/abs/2510.07238
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Measures benchmark staleness with Dataset Drift Score, Evaluation Misleading
  Rate and Temporal Alignment Gap; the methodological template for measuring CTI benchmark
  decay under ATT&CK versioning.
---

## What it is
"When Benchmarks Age: Temporal Misalignment through Large Language Model Factuality Evaluation" — arXiv:2510.07238; published at EACL 2026 (aclanthology.org/2026.eacl-short.37/). A measurement study of benchmark decay.

## Core claim
Static evaluation benchmarks silently go out of date as the world changes, and the community keeps using them anyway. The authors take five widely used factuality benchmarks — TriviaQA (2017), BoolQ (2019), Natural Questions (2019), TruthfulQA (2022), SelfAware (2023) — and eight LLMs spanning several release years, run an up-to-date fact-retrieval pipeline over the benchmark items, and quantify decay with three purpose-built metrics:
- **Dataset Drift Score (DDS)** — share of items whose gold answer no longer matches current reality;
- **Evaluation Misleading Rate (EMR)** — rate at which stale items flip the evaluation verdict;
- **Temporal Alignment Gap (TAG)** — gap between real-world accuracy and agreement with the benchmark.
Reported DDS across the five benchmarks ranges roughly 24%–64% as of mid-2025, highest in the oldest (BoolQ). The consequence named: an aged benchmark rewards models that reproduce outdated facts over models that learned current ones.

## Relation to ontology drift (label-space vs feature-space)
**Neither, exactly — and that is what makes it the most transferable template in this batch.** It is not feature-distribution drift and not vocabulary change; it is decay of the **answer key** while the questions stay fixed. Formally it is drift in the *ground-truth labelling function* over a static item set — the closest general-ML analogue to ATT&CK's silent rewriting of technique descriptions and to CTI benchmark items whose gold ATT&CK technique id was deprecated or revoked after the benchmark was built.

What does not transfer: the cause here is the world moving (facts change), whereas ATT&CK decay has a second, distinct cause — the *schema* moving by curatorial decision with adversary behaviour unchanged. And their remedy is refresh-the-key via retrieval; ATT&CK has an authoritative, machine-readable version history, so the remedy available to the manuscript is stronger (a deterministic migration map, not a retrieval heuristic).

## Why it matters for this manuscript
This is the methodological template to imitate for the empirical core. It shows that (a) "how stale is this benchmark?" is a publishable quantitative question at a top NLP venue, (b) the right output is a small set of named, computable decay metrics, and (c) the killer result is showing the decay *changes model rankings*, not merely that items are stale. The manuscript's strongest empirical claim would be the direct analogue: recompute a CTI benchmark (CTIBench/CTIArena-class) under a normalized ATT&CK version and show that reported scores — and ideally the ordering of systems — move. DDS/EMR/TAG give ready-made names for ATT&CK-specific counterparts (e.g. a technique-label drift score, a version-induced misranking rate).

## Fidelity
Summary-level only. Metric names, the five benchmarks, the eight-model design and the ~24–64% DDS range are from the abstract and search-result summaries; the arXiv HTML and the ACL Anthology page were not retrievable through the blocked egress proxy. Exact numbers and metric definitions must be re-verified before citing. No verbatim quotation given.
