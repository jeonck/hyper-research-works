---
title: Legoy et al. 2020 — Automated Retrieval of ATT&CK Tactics and Techniques (rcATT
  paper)
id: legoy-et-al-2020-automated-retrieval-of-attck-tactics-and-techniques-rcatt-paper
tags:
- attack-ontology-drift-cti-85bc51
- ttp-extraction
created: '2026-09-12T13:20:59.102448Z'
source: https://arxiv.org/abs/2004.14322
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Canonical multi-label report-to-ATT&CK baseline whose reported scores are
  conditional on an undeclared pre-sub-technique ontology.
---

## What this is
Legoy, Caselli, Seifert, Peter, *Automated Retrieval of ATT&CK Tactics and Techniques for Cyber Threat Reports*, arXiv:2004.14322 (2020). The paper behind rcATT; the standard multi-label baseline for report→ATT&CK classification.

## What it says bearing on the query (search-summary fidelity)
- Frames TTP extraction as **multi-label text classification** of CTR text onto ATT&CK tactics and techniques, using TF-IDF features plus linear classifiers, with post-processing that exploits tactic–technique hierarchy.
- Training data is assembled from ATT&CK's own procedure/report references plus collected threat reports — i.e. the **labels are inherited from whatever ATT&CK release was current at collection time**, and the paper reports performance against that fixed snapshot.
- The published artefact fixes the label space at 12 tactics and 215 flat techniques (see companion note on the repo audit), so the reported F-scores are conditional on a pre-sub-technique ontology.
- Notably, the paper does **not** establish a protocol for re-labelling or re-scoring when ATT&CK changes; the tool's own "add feedback and retrain" loop is the only offered update mechanism, and it ships with an empty added-data file.

## Citable use
Use as the canonical example of "baseline whose reported numbers are version-conditional and whose version is undeclared in the artefact." Subsequent work (TTPHunter, TTPXHunter, tumeteor/mitre-ttp-mapping, TRAM2) compares against rcATT numbers **across different ATT&CK ontologies**, which is exactly the comparability failure the query targets.

## Fidelity
**Search-summary.** Abstract/summary level only; arXiv full text could not be fetched (egress blocked, confirmed 403 on `hyperresearch fetch`). No verbatim quotation is asserted. The concrete label-space numbers come from the repo audit note, not from this paper.
