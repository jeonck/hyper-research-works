---
title: 'A Comprehensive Survey of Threat Intelligence Research: A Measurement-Based
  Study (ACM CSUR 2025)'
id: a-comprehensive-survey-of-threat-intelligence-research-a-measurement-based-study
tags:
- attack-ontology-drift-cti-85bc51
- cti-quality
created: '2026-09-12T13:22:03.216697Z'
source: https://dl.acm.org/doi/10.1145/3772280
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: '200+ studies 2001-2025 plus a measurement study of CTI datasets: evaluation
  results depend on which vendors are in the dataset; IoC-type gaps (DarkFox has no
  IPv6) and 19,491-vs-381 file-path counts; duplication flagged as a defect.'
---

## What it is
"A Comprehensive Survey of Threat Intelligence Research: A Measurement-Based Study," *ACM Computing Surveys*, December 2025, DOI 10.1145/3772280 (Tampere University-affiliated). A survey that does not merely catalogue papers but measures the datasets the field builds on.

## What it says bearing on the query
- Reviews **over 200 CTI studies published between 2001 and 2025** and analyses representative research trends.
- Claims (per the authors) to be the **first survey to run a measurement study on the datasets themselves** to derive guidance for constructing a well-balanced CTI dataset.
- Reported dataset pathologies:
  - **Evaluation results depend on which vendors are included in the dataset** — i.e. the reported performance of a CTI analytic is partly a property of the corpus, not of the method.
  - **Significant bias in the counts of each IoC type**; some dark-web datasets omit whole IoC types entirely (e.g. the **DarkFox dataset has no IPv6 and no file-path IoCs**).
  - **Strong cross-dataset variation for the same IoC type**: file-path IoCs number **19,491 in ExploitDB but only 381 in NVD**.
  - **A substantial number of duplicate IoCs across datasets.**

## Bearing on ATT&CK ontology drift
- The central transferable finding is the one this batch most needed: **CTI evaluation results are an artifact of the corpus rather than of the method** — a 2025 survey-level, citable statement of the validity threat that ontology drift instantiates at the label layer. If *which vendors you include* changes the result, *which ATT&CK release you label against* changes it too, and the latter has an even more direct path to the metric (it changes the label set itself, not just the sample).
- **Duplicate IoCs across datasets** is the indicator-layer analogue of technique duplication under sub-technique restructuring: an item counted twice because it appears under two identities. That the survey flags duplication as a dataset-construction defect supports treating split/merge bookkeeping as a defect rather than as growth.
- The survey's framing is still entirely **dataset composition** (which sources, which IoC types, how many duplicates). **It does not, in anything I could see, treat the versioning of the labeling vocabulary as a dataset-construction variable** — the recommendations are about balance across sources and types, not about pinning a taxonomy release.

## Fidelity
Could not read full text (ACM DL blocked). The 200+/2001–2025 scope, the DarkFox IPv6/file-path gap, and the 19,491-vs-381 file-path figure are at summary fidelity from search-result descriptions; they are specific enough to be worth re-verifying in the PDF before citation. No verbatim quotation asserted. The final "does not treat vocabulary versioning" sentence is an **absence claim at abstract-level evidence only** — it cannot be asserted as established without reading the full survey.
