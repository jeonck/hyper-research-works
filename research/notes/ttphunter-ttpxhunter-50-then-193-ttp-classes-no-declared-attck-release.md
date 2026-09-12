---
title: 'TTPHunter / TTPXHunter: 50 then 193 TTP classes, no declared ATT&CK release'
id: ttphunter-ttpxhunter-50-then-193-ttp-classes-no-declared-attck-release
tags:
- attack-ontology-drift-cti-85bc51
- ttp-extraction
created: '2026-09-12T13:22:54.391479Z'
source: https://arxiv.org/abs/2403.03267
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: TTPHunter trains on 50 TTPs, TTPXHunter on 193 over 10,906 sentences; neither
  declares an ATT&CK version, and TTPXHunter is the extractor feeding the CAPTAIN
  attribution system.
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
