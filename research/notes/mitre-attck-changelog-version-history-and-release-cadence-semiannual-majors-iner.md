---
title: 'MITRE ATT&CK changelog, version history and release cadence: semiannual majors,
  inert minors, and out-of-band agile Group/Software updates'
id: mitre-attck-changelog-version-history-and-release-cadence-semiannual-majors-iner
tags:
- attack-ontology-drift-cti-85bc51
- attack-versioning
created: '2026-09-12T13:24:27.612541Z'
source: https://attack.mitre.org/resources/changelog.html
status: draft
type: note
tier: institutional
content_type: docs
deprecated: false
summary: Official cadence is twice-yearly majors with minors carrying only corrections;
  deprecation is an editorial scope judgement not evidence behaviour ceased; agile
  out-of-band Group/Software/Campaign updates mean a release tag alone no longer pins
  the dataset.
---

## What this is
Two linked systems from the same group: **TTPHunter** (Rani et al., ACSW 2023, DOI 10.1145/3579375.3579391) and its successor **TTPXHunter** (arXiv:2403.03267; published in ACM *Digital Threats: Research and Practice*, DOI 10.1145/3696427). Sentence-level BERT/SecureBERT classifiers mapping report sentences to ATT&CK technique IDs.

## What they say bearing on the query (search-summary fidelity)
- **TTPHunter** fine-tunes BERT/RoBERTa on a sentence–TTP dataset harvested from the MITRE knowledge base, with a filter that discards sentences not describing a TTP. Because of sparse per-technique sentence data, **TTPHunter is trained on only 50 TTPs** — the same order of coverage as TRAM2's 50 classes, and roughly 8% of a contemporary ATT&CK release's live label space.
- **TTPXHunter** expands this to **193 TTPs**, fine-tuned on an augmented corpus of **10,906 sentences over those 193 TTPs**, and emits STIX.
- Neither summary I could obtain states an ATT&CK release number for the label space. The 193-class figure is close to the count of *parent* Enterprise techniques in the v12–v14 era (196 live parents in v13.1, per my TRAM bundle audit), which strongly suggests **parent-level-only labels from an undeclared release** — but I could not confirm this from an artefact: the TTPXHunter repo (`nanda-rani/TTPXHunter`) did not clone (404/unavailable from this environment), so I have no file-level evidence.

## Why this bears on the query
TTPXHunter is the extraction engine feeding CAPTAIN, the TTP-based *attribution* system (see companion note on arXiv:2409.16400). So an attribution result is built on a 193-class, version-undeclared, parent-level extractor. Every attribution claim inherits that extractor's ontology snapshot, silently. This is the cleanest instance in the batch of drift propagating from extraction into attribution.

## Fidelity
**Search-summary only.** The 50-TTP and 193-TTP / 10,906-sentence figures are as reported in secondary summaries of the two papers; I could not read either full text (egress blocked) and could not clone the repo to verify the label file. The inference that the 193 classes are parent-level is **my hypothesis, not an established fact** — flagged for the gap-filling wave.
