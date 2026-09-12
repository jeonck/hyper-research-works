---
title: 'MITRE''s own bias taxonomy and the Sightings Ecosystem: top 15 techniques
  are >80% of observed events'
id: mitres-own-bias-taxonomy-and-the-sightings-ecosystem-top-15-techniques-are-80-of
tags:
- attack-ontology-drift-cti-85bc51
- critique
- rebuttal
created: '2026-09-12T13:25:12.525966Z'
source: https://ctid.mitre.org/projects/sightings-ecosystem/
status: draft
type: note
tier: institutional
content_type: article
deprecated: false
summary: MITRE publicly names novelty/visibility/producer/victim/availability bias
  and funds telemetry to correct it; with 15 of 353 sighted techniques carrying >80%
  of events, long-tail churn barely moves frequency-weighted coverage.
---

## What it is
MITRE's own documentation of bias in the open-source reporting that feeds ATT&CK (attack.mitre.org/resources/sightings/), together with the Center for Threat-Informed Defense's **Sightings Ecosystem** project — a two-year telemetry collection (August 2021 - September 2023) with AttackIQ, Cyber Threat Alliance, Fortinet, JPMorgan Chase, HCA Healthcare and Verizon Business, published as "Sightings Ecosystem: A Data-driven Analysis of ATT&CK in the Wild" (v1 and v2.0.0).

## The criticism it makes — made by MITRE, about MITRE
ATT&CK's technique inventory is built from open-source reporting, and that reporting is biased in at least five named ways:
- **novelty bias** (new/interesting techniques get reported, routine ones do not),
- **visibility bias** (organizations see different subsets of technique space),
- **producer bias** (a few organizations publish disproportionately),
- **victim bias** (some victims are more likely to be written about),
- **availability bias** (easily recalled techniques get reported more).
Consequence, stated by MITRE: using threat-report data to infer technique prevalence over time and across industries "might give deceiving answers." The Sightings Ecosystem exists to replace report-derived prevalence with real detection telemetry. Headline result: of **353 unique techniques sighted, the top 15 accounted for over 80% of events**, spanning 9 of 14 Enterprise tactics.

## Strength of evidence
High. Institutional, first-party, and the Sightings numbers come from pooled multi-organization telemetry rather than report counting. The bias taxonomy is qualitative but authoritative.

## For or against the thesis
**Against in two distinct ways, both of which a referee will raise.**

1. **The "we already know and already measure it" rebuttal.** MITRE publicly documents that ATT&CK content is a biased sample of reporting, and has funded a multi-year telemetry programme specifically to correct prevalence estimates. A thesis claiming that the field naively treats ATT&CK growth as adversary intelligence is arguing against a position the framework's own maintainers have publicly disavowed.
2. **The "prevalence is concentrated, so the tail doesn't matter" rebuttal.** This is the sharpest quantitative objection in the batch. If **15 techniques carry >80% of observed events**, then the operational consequence of churn in the long tail — where the great majority of additions, deprecations, revocations and sub-technique splits occur — is small for detection and mitigation coverage that is weighted by real-world frequency. Drift concentrated in rarely-sighted techniques changes the *catalogue* far more than it changes *defence*. The thesis's coverage-claim leg is therefore its weakest: to survive, it must show either (a) that drift touches the high-prevalence head (the v19 Defense Evasion split does, which is the one clean counter-example), or (b) that coverage claims are made unweighted — counting techniques, not events — in which case the harm is to the *metric*, not to the security posture, and must be scoped as such.

*For the thesis, modestly:* the bias taxonomy is exactly the vocabulary needed to argue that year-over-year ATT&CK growth is a reporting artefact rather than adversary evolution. And Sightings v1 vs v2 is itself a longitudinal dataset spanning ATT&CK version changes — a normalization test-bed.

## Fidelity
Medium-high. Bias taxonomy and the 353-techniques/top-15/80% figures come from MITRE-hosted pages and the CTID report as surfaced by web search; I could not fetch the PDF (egress blocked), so the figures are at summary fidelity and the release-version context for the telemetry mapping is unverified. https://attack.mitre.org/resources/sightings/ and https://ctid.mitre.org/projects/sightings-ecosystem/
