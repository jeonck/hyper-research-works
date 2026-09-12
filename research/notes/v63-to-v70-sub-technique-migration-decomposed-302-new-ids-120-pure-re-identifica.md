---
title: 'v6.3 to v7.0 sub-technique migration decomposed: 302 new IDs, 120 pure re-identifications,
  only 30 new top-level techniques'
id: v63-to-v70-sub-technique-migration-decomposed-302-new-ids-120-pure-re-identifica
tags:
- attack-ontology-drift-cti-85bc51
- attack-versioning
created: '2026-09-12T13:24:00.998918Z'
source: https://github.com/mitre-attack/attack-stix-data
status: draft
type: note
tier: ground_truth
content_type: dataset
deprecated: false
summary: 'The +61% v7.0 growth is mostly bookkeeping: 272 of 302 new IDs are sub-techniques,
  93% of the 129 revocations point at a sub-technique, and at least 39.7% of new IDs
  are direct re-IDs of existing v6.3 behaviours.'
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
