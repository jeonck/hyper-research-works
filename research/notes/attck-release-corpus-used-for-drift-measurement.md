---
title: ATT&CK release corpus used for drift measurement
id: attck-release-corpus-used-for-drift-measurement
tags:
- attack-ontology-drift-cti-85bc51
- measurement
created: '2026-09-12T13:17:54.519726Z'
source: https://github.com/mitre-attack/attack-stix-data
status: draft
type: note
tier: ground_truth
content_type: dataset
deprecated: false
summary: Every public ATT&CK STIX release, parsed into a longitudinal database
---

# Measurement corpus: every public ATT&CK STIX release

Provenance: local clone of the MITRE ATT&CK STIX data repository; parsed
by `code/01_extract.py` into `data/attack_drift.db`. Fidelity: PRIMARY
ARTEFACT — computed from the release bundles themselves, not from any
secondary description of them.

- enterprise-attack: 19 major releases analysed, v1.0 (2018-01-17) through v19.0 (2026-04-28).
- mobile-attack: 19 major releases analysed, v1.0 (2018-01-17) through v19.0 (2026-04-28).
- ics-attack: 12 major releases analysed, v8.0 (2020-10-27) through v19.0 (2026-04-28).