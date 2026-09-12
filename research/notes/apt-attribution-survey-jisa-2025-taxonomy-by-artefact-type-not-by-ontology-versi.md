---
title: 'APT attribution survey (JISA 2025): taxonomy by artefact type, not by ontology
  version'
id: apt-attribution-survey-jisa-2025-taxonomy-by-artefact-type-not-by-ontology-versi
tags:
- attack-ontology-drift-cti-85bc51
- ttp-attribution
created: '2026-09-12T13:25:01.866834Z'
source: https://doi.org/10.1016/j.jisa.2025.104076
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: The field's reference attribution survey taxonomises evidence types and compares
  datasets, but does not appear to treat ATT&CK release version as a dimension of
  dataset comparability.
---

## What this is
Rani, Saha, Conti et al., *A Comprehensive Survey of Advanced Persistent Threat Attribution: Taxonomy, Methods, Challenges and Open Research Problems*, arXiv:2409.11415; journal version in *Journal of Information Security and Applications* **92** (2025), DOI 10.1016/j.jisa.2025.104076.

## What it says bearing on the query (search-summary fidelity)
- Proposes a taxonomy that "standardizes the attribution process", organising the heterogeneous artefacts (IoCs, malware artefacts, infrastructure, TTPs) attribution methods consume, to enable consistent classification and systematic evaluation.
- Provides a **classification and comparison of available attribution datasets** and of automated attribution methods, with strengths, limitations and applicability.
- Identifies open challenges and research directions for automated attribution.

## Why it matters for positioning
This is the field's own statement of what an attribution-methods contribution should look like, and therefore the yardstick against which the query's proposed contribution is judged. Two observations:

1. **The survey's framing is artefact-type-centric, not version-centric.** It taxonomises *what kind of evidence* an attribution method uses. Nothing in the available summary indicates that ATT&CK release version is treated as a dimension of dataset comparability — which means the field's reference survey does not yet register ontology drift as a category of attribution error. That is the gap the query occupies.
2. It confirms that **dataset comparison is already recognised as the weak point** of automated attribution ("comprehensive classification and comparison of available attribution datasets ... identifying their strengths, limitations"). A normalization protocol and version-reporting discipline is the natural next layer on top of that comparison, not a competing framing.

## Use in the SCI-level contribution argument
To exceed this survey, a contribution must do what a survey cannot: **measure** the effect. Specifically it must show, on real artefacts, that (a) attribution rankings change when the same evidence is scored under two ATT&CK releases; (b) a stated normalization restores agreement by a quantified margin; and (c) the residual disagreement after normalization is attributable to genuine intelligence change rather than bookkeeping. B2's repo audits supply the raw material for (a): the systems this survey compares are frozen at ATT&CK v5/v6 (rcATT), v9 (AttacKG), v12 (tumeteor), v13.1 (TRAM) and v15-era (CTI-Bench prompts).

## Fidelity
**Search-summary.** Neither the arXiv nor the ScienceDirect full text was fetchable (egress blocked). Claims above are at summary fidelity; no verbatim quotation asserted beyond short phrases reproduced from search summaries, which should be re-verified before quoting. Observation (1) is an inference from absence in the summary, not a verified fact about the paper's contents — flag for the gap-filling wave.
