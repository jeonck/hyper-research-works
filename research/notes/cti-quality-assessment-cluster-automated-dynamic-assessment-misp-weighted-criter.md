---
title: CTI Quality Assessment Cluster — automated dynamic assessment, MISP weighted
  criteria, completeness/timeliness of artefacts, STIX graphs
id: cti-quality-assessment-cluster-automated-dynamic-assessment-misp-weighted-criter
tags:
- attack-ontology-drift-cti-85bc51
- cti-quality
created: '2026-09-12T13:22:03.476074Z'
source: https://www.sciencedirect.com/science/article/pii/S0167404824003845
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Pointer bundle for the CTI quality-metric family: fuzzy-AHP/entropy weighting,
  nine-parameter quality vocabulary (compliance, maintenance, extensiveness...) —
  compliance means format conformance and maintenance means feed upkeep, neither is
  taxonomy versioning.'
---

## What it is
Two further CTI-quality-assessment entries in the same family, recorded together because neither could be read past abstract level:
1. "An automated dynamic quality assessment method for cyber threat intelligence," *Computers & Security* (2024), ScienceDirect S0167404824003845.
2. "Weighted quality criteria for cyber threat intelligence: assessment and prioritisation in the MISP data model" (2025), and the related MISP/quality-criteria line.
Plus adjacent: Tundis et al., "On the Assessment of Completeness and Timeliness of Actionable Cyber Threat Intelligence Artefacts," Springer (2020), DOI 10.1007/978-3-030-59000-0_5; and "Improving quality of indicators of compromise using STIX graphs," *Computers & Security* (2024), DOI 10.1016/j.cose.2024.103972.

## What they say bearing on the query
- The automated-dynamic-assessment paper's stated motivation: **current CTI evaluation practice either lacks standardized, comprehensive, quantifiable quality metrics, or fails to balance subjective expert judgement against objective data variability.** It surveys ML-based CTI quality assessment using KNN, Random Forest, SVM, Logistic Regression, DBN, and graph mining.
- The MISP weighted-criteria work defines **quantifiable quality metrics as mathematical expressions** and two weighting schemes: **subjective (fuzzy-AHP)** and **objective (entropy-based)**.
- The parameter vocabulary circulating in this cluster: **similarity, completeness, timeliness, compliance, interoperability, verifiability, false positives, maintenance, extensiveness**.
- Tundis et al. target **completeness and timeliness of actionable CTI artefacts** specifically.
- The STIX-graph paper improves IoC quality by exploiting **relationship structure in STIX graphs** rather than scoring fields in isolation.

## Bearing on ATT&CK ontology drift
- The circulating nine-parameter vocabulary (similarity, completeness, timeliness, compliance, interoperability, verifiability, false positives, maintenance, extensiveness) is the **widest quality-dimension list this batch surfaced**, and it still has **no vocabulary-versioning dimension**. Two look superficially close and are not:
  - **compliance** = conformance to a format/standard (does this validate as STIX 2.1?), not "was this labelled under ATT&CK v12 or v17?";
  - **maintenance** = whether the *feed/source* is actively maintained, not whether the *reference taxonomy* moved under the data.
- The fuzzy-AHP/entropy weighting machinery is directly reusable if a drift/referential-stability dimension is added: the contribution can slot in as a new criterion in an existing, already-accepted weighting framework rather than proposing a rival framework.
- The STIX-graph approach is the best existing argument that **structure carries quality information** — which is the same intuition behind using ATT&CK's own `revoked-by` / `x_mitre_deprecated` / sub-technique parent relations as the normalization substrate.

## Fidelity
None of these were readable (ScienceDirect, Springer, ACM, ResearchGate all blocked). Everything above is at summary fidelity from search-result descriptions; the nine-parameter list in particular was reported in a search summary and **its source paper was not identified with certainty** — attribute it carefully or re-derive it. No verbatim quotation asserted. This note is a pointer bundle for a later full-text pass, not a citable analysis.
