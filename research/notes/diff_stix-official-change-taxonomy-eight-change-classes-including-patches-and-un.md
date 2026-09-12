---
title: 'diff_stix official change taxonomy: eight change classes including patches
  and unintended version changes'
id: diff_stix-official-change-taxonomy-eight-change-classes-including-patches-and-un
tags:
- attack-ontology-drift-cti-85bc51
- attack-versioning
- quarantined-metadata-mismatch
created: '2026-09-12T13:24:27.278827Z'
updated: '2026-09-12T13:45:45.718728Z'
source: https://github.com/mitre-attack/mitreattack-python/blob/master/mitreattack/diffStix/README.md
status: deprecated
type: note
tier: institutional
content_type: docs
deprecated: true
summary: 'QUARANTINED: front matter and body describe different sources; excluded
  from the corpus (see data/results/e15_vault_integrity.json).'
---

## What this is
Husari, Al-Shaer, Ahmed, Chu, Niu, *TTPDrill: Automatic and Accurate Extraction of Threat Actions from Unstructured Text of CTI Sources*, **ACSAC 2017** (DOI 10.1145/3134600.3134646). The earliest widely cited TTP-extraction system and the baseline nearly every later system compares against.

## What it says bearing on the query (search-summary fidelity)
- TTPDrill builds a **custom threat-action ontology** derived from ATT&CK (and CAPEC), then extracts subject–verb–object "threat actions" from report text and matches them to ontology entries with **BM25** similarity, emitting STIX.
- Reported detection precision and recall **above 82%**.
- Crucially for the query: TTPDrill's evaluation predates the sub-technique restructuring (ATT&CK v7, July 2020) by ~3 years, and predates the Reconnaissance/Resource-Development tactic additions (v8) by ~3 years. Its ontology is a **derived artefact**, not the ATT&CK release itself, so it cannot be re-pointed at a newer release by ID remapping; the ontology has to be rebuilt.
- Later systems (AttacKG, EXTRACTOR, TTPHunter/TTPXHunter, the multi-report study) continue to quote TTPDrill's 2017 numbers as a comparison point. **Those comparisons are across at least 10 ATT&CK releases and across the parent/sub-technique boundary** — the single clearest example in the TTP-extraction literature of cross-version score comparison presented as if it were like-for-like.

## Citable use
Anchor for the claim that the field's baseline numbers are ontology-incommensurable: the 82%+ figure is measured on a pre-v7, ~200-flat-technique ontology and is routinely tabulated next to F1 scores measured on v12/v13 ontologies with 600+ hierarchical labels.

## Fidelity
**Search-summary.** ACM DL full text not retrievable (egress blocked). No verbatim quotation asserted; the 82% figure is as reported in secondary summaries of the paper. The ATT&CK-release dating is my own, derived from publication date against MITRE's release history.
