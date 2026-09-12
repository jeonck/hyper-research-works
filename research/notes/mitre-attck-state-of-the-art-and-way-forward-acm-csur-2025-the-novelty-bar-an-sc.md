---
title: 'MITRE ATT&CK: State of the Art and Way Forward (ACM CSUR 2025) — the novelty
  bar an SCI contribution must clear'
id: mitre-attck-state-of-the-art-and-way-forward-acm-csur-2025-the-novelty-bar-an-sc
tags:
- attack-ontology-drift-cti-85bc51
- critique
created: '2026-09-12T13:26:32.140848Z'
source: https://dl.acm.org/doi/10.1145/3687300
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Second top-venue survey of ATT&CK research in two years; closes off critique-shaped
  contributions and forces the drift thesis into separable-effect-size, frequency-weighted,
  confounder-separated empirical territory.
---

## What it is
Al-Sada, Sadighian, Oligeri — "MITRE ATT&CK: State of the Art and Way Forward", **ACM Computing Surveys** (January 2025, DOI 10.1145/3687300; preprint arXiv 2308.14016). A survey of 50+ major research contributions using ATT&CK, categorised by use case, application scenario, methodology and use of additional data, closing with open issues and future research directions across threat analysis, threat modelling and CTI.

## The criticism it makes
As a survey its critical function is to map where ATT&CK-based research is thin or inconsistent, and to set a forward agenda for threat analysis, threat modelling and CTI. Its authority comes from the venue (ACM CSUR) and breadth rather than from any single measurement.

## Strength of evidence
High as a field map, peer-reviewed at a top survey venue; secondary/aggregating, so it establishes consensus rather than fact. I was unable to read the open-issues section (Section 6) — egress blocked — so I cannot state whether it names version churn among the open problems.

## For or against the thesis
**Against, chiefly as a novelty-and-positioning hazard rather than a substantive rebuttal.**

Together with the 2023 SoK (arXiv 2304.07411), this survey means the ATT&CK research landscape has been systematically mapped **twice** at top venues within two years. For an SCI-level contribution, two consequences follow:
1. **A survey-shaped or critique-shaped contribution is closed off.** "ATT&CK has limitations, here is a taxonomy of them" is occupied territory. The remaining space is empirical and longitudinal: a measurement nobody has made, with an effect size.
2. **The positioning burden is high.** The thesis must state precisely which of these surveys' open problems it answers and what it adds beyond them. The specific, defensible gap this batch could not find covered anywhere: *no published work recomputes an ATT&CK-based analytic across multiple ATT&CK versions and reports how much the result moves.* Both surveys catalogue analytics; neither versions them.

**What an SCI-level contribution must therefore demonstrate (batch-B4 view, derived adversarially):**
- A **separable effect size**: drift-induced variance quantified against, and shown additive to, the two rival variance sources this batch documented — inter-rater mapping variance at a fixed version (Virkud et al.) and intra-version technique confusability (arXiv 2604.07470).
- A **head-on defeat of the bookkeeping rebuttal**: show empirically where `revoked-by` + `x_mitre_deprecated` + pinned bundles are *insufficient* (1:N splits, merges, silent description rewrites, dangling revocation edges), not merely that drift exists.
- **Frequency weighting**: results weighted by observed technique prevalence (Sightings), not by raw technique counts, so the finding survives "the churn is all in the long tail."
- **Stratification by identifiability**: attribution effects measured on the ~34% of groups that have group-specific behaviour (Saha et al.), not on the full population.
- **Confounder separation**: adversary drift vs. source/reporting drift (CTI Echo Chamber) vs. ontology drift.
- A normalization protocol that is **executable and evaluated**, with a reproduction of at least one published CTI result showing the conclusion changes under normalization. A protocol without a flipped result is a style guide, not a finding.

## Fidelity
Medium-low. Abstract- and metadata-level only; the open-issues content is unread. Do not attribute specific limitation claims to this survey without reading Section 6. https://dl.acm.org/doi/10.1145/3687300
