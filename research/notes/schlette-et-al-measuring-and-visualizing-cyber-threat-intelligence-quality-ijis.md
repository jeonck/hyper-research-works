---
title: Schlette et al. — Measuring and Visualizing Cyber Threat Intelligence Quality
  (IJIS 2021)
id: schlette-et-al-measuring-and-visualizing-cyber-threat-intelligence-quality-ijis
tags:
- attack-ontology-drift-cti-85bc51
- cti-quality
created: '2026-09-12T13:21:31.670167Z'
source: https://link.springer.com/article/10.1007/s10207-020-00490-y
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Computable CTI quality metrics at attribute/object/report level anchored
  to STIX 2, plus a Quality Indicator custom object — format-level scoring is blind
  to ontology drift by construction.
---

## What it is
Schlette, Böhm, Caselli & Pernul, "Measuring and visualizing cyber threat intelligence quality," *International Journal of Information Security* 20 (2021), DOI 10.1007/s10207-020-00490-y (online 2020). The main attempt to make CTI quality *computable* against an actual exchange format rather than merely enumerable.

## What it says bearing on the query
- Motivating premise: **inaccurate, incomplete, or outdated threat intelligence is a major problem**, since only high-quality CTI helps detect and defend against attacks.
- The authors select and structure relevant **data quality dimensions** (drawn from the general information-quality literature) and then instantiate **metrics in the context of a specific format**, using **STIX 2** (OASIS) as the reference model.
- Metrics are defined at **three granularities: attribute level, object level, and report level**.
- They propose a **STIX extension — a custom "Quality Indicator" object** — to carry computed quality alongside the intelligence, plus a visualization approach to communicate quality to analysts in a CTI analysis tool.

## Bearing on ATT&CK ontology drift
Directly relevant as the closest prior art to a version-aware quality metric, and directly relevant as another **absence**:
- The quality model is anchored to **STIX 2 syntax and object structure**. It can score whether a field is populated, well-formed, internally consistent, or stale. It has no construct for *which version of an external controlled vocabulary a label was drawn from*, and no construct for a label whose referent changed between releases (revoked-by / deprecated / sub-technique split).
- In STIX, ATT&CK techniques are carried in `attack-pattern` objects with `external_references`; a quality metric operating at "attribute level" would see a syntactically valid `external_id` (e.g. T1059.001) and score it as complete and consistent, even when that ID's definition was rewritten or its tactic reassigned two releases ago. **Format-level quality scoring is blind to ontology drift by construction.**
- The "Quality Indicator" custom-object mechanism is, however, a plausible carrier for a drift-aware annotation (e.g. a recorded `attack_spec_version` / normalization provenance stamp) — i.e. this paper supplies the engineering hook that a normalization protocol could reuse.

## Fidelity
Could not read full text (Springer and the Regensburg e-pub PDF are behind the blocked proxy). Claims are at abstract/summary fidelity from search-result descriptions plus the indexed figure caption "Definition of the Quality Indicator custom object for STIX 2". The attribute/object/report three-level structure and the STIX-2 anchoring are consistently reported; the inference about blindness to vocabulary drift is **mine**, not a claim made by the authors. No verbatim quotation asserted.
