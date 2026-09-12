---
title: 'TTPDrill (ACSAC 2017): the pre-sub-technique baseline everyone still compares
  against'
id: ttpdrill-acsac-2017-the-pre-sub-technique-baseline-everyone-still-compares-again
tags:
- attack-ontology-drift-cti-85bc51
- ttp-extraction
created: '2026-09-12T13:22:54.141471Z'
source: https://dl.acm.org/doi/10.1145/3134600.3134646
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: TTPDrill's 82%+ precision/recall was measured on a 2017 derived ontology,
  yet is still tabulated beside F1 scores computed on v12/v13 hierarchical label spaces.
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
