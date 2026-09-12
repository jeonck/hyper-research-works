---
title: Zibak et al. — Threat Intelligence Quality Dimensions for Research and Practice
  (DTRAP 2022)
id: zibak-et-al-threat-intelligence-quality-dimensions-for-research-and-practice-dtr
tags:
- attack-ontology-drift-cti-85bc51
- cti-quality
created: '2026-09-12T13:21:31.392891Z'
source: https://dl.acm.org/doi/full/10.1145/3484202
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Delphi study with ~30 experts fixes seven CTI quality dimensions (accuracy,
  actionability, interoperability, provenance, relevance, reliability, timeliness)
  — none covers label-vocabulary versioning; no concrete metrics exist in practice.
---

## What it is
Zibak, Simpson & Martin, "Threat Intelligence Quality Dimensions for Research and Practice," ACM *Digital Threats: Research and Practice* (DTRAP), 2022, DOI 10.1145/3484202. Methodologically the reference paper for "what counts as CTI quality": a systematic literature review of the threat-intelligence literature followed by a modified Delphi study with ~30 threat-intelligence experts in Europe.

## What it says bearing on the query
This is the canonical enumeration of CTI quality dimensions, and it is the strongest single piece of evidence that **the field's quality vocabulary contains no ontology/label-versioning dimension**.

Citable claims (summary fidelity, from abstract/landing text):
- The Delphi panel converged on **seven quality dimensions**: accuracy, actionability, interoperability, provenance, relevance, reliability, timeliness.
- Frequency counts in the prior literature reviewed: **timeliness (n=14), completeness (n=13), accuracy (n=12)** were the most commonly named dimensions.
- Ranking differs by product type: for **threat data**, the top three are timeliness, relevance, interoperability; for **threat intelligence**, the top three are relevance, actionability, timeliness.
- Key negative finding for measurement science: organizations **"are yet to develop concrete metrics"** for any of the dimensions and largely rely on **consumer feedback and anecdotal evidence** (paraphrase of the reported finding, not verbatim).

## Bearing on ATT&CK ontology drift
None of the seven dimensions captures the stability, versioning, or semantic continuity of the *label vocabulary* used to express the intelligence. The closest neighbours are:
- **interoperability** — about format/schema exchangeability (STIX/TAXII-level), not about whether T1086 in one release means the same thing as its successor in the next;
- **accuracy** — assessed against ground truth *at a point in time*, with no notion that the reference taxonomy itself moved;
- **provenance** — about who produced the item, not which ATT&CK version its labels were drawn from.
This is the gap an ontology-drift contribution occupies: a proposed eighth dimension (call it *referential stability* or *vocabulary versioning*) is not a redundant addition to this list.

## Fidelity
Could not read full text — ACM DL and the Oxford ORA PDF are behind the blocked egress proxy. All claims above are at summary/abstract fidelity, reconstructed from search-result descriptions of the paper's abstract and findings. The seven-dimension list and the n=14/13/12 counts are reported consistently across multiple independent search snippets. **No verbatim quotation from the paper is asserted.** Numbers should be re-verified against the PDF before being cited in a submission.
