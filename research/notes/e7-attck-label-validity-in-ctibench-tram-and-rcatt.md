---
title: E7 ATT&CK label validity in CTIBench, TRAM and rcATT
id: e7-attck-label-validity-in-ctibench-tram-and-rcatt
tags:
- attack-ontology-drift-cti-85bc51
- measurement
created: '2026-09-12T13:17:56.244178Z'
source: https://github.com/mitre-attack/attack-stix-data
status: draft
type: note
tier: ground_truth
content_type: dataset
deprecated: false
summary: Deployed CTI corpora carry labels that match no single ATT&CK release
---

# E7 — label validity of deployed CTI corpora

Fidelity: PRIMARY ARTEFACT (computed from each corpus's own label files,
cloned from its public repository; validity evaluated per ATT&CK domain).

## ctibench-ate
- distinct (domain, identifier) labels: 120; label instances: 397; sub-technique identifiers: 0
- best-fitting release: v14.0 (2023-10-31), 0.942 of labels live there
- releases in which EVERY label is simultaneously live: 0 — the corpus matches no single release
- invalid at v19.2 (2026-08-05): 8 distinct labels (0.067), 0.020 of label instances
- repairable by revocation chain: 1; unrepairable: 7
- examples of invalid identifiers: T1404, T1406, T1562, T1577, T1628, T1630, T1643, T1655

## rcatt
- distinct (domain, identifier) labels: 215; label instances: 6235; sub-technique identifiers: 0
- best-fitting release: v4.0 (2019-04-30), 1.000 of labels live there
- releases in which EVERY label is simultaneously live: 8 (v4.0–v6.3)
- invalid at v19.2 (2026-08-05): 107 distinct labels (0.498), 0.380 of label instances
- repairable by revocation chain: 99; unrepairable: 8
- examples of invalid identifiers: T1002, T1004, T1009, T1013, T1015, T1019, T1022, T1023, T1024, T1026

## tram-bootstrap
- distinct (domain, identifier) labels: 537; label instances: 25770; sub-technique identifiers: 344
- best-fitting release: v13.0 (2023-04-25), 0.939 of labels live there
- releases in which EVERY label is simultaneously live: 0 — the corpus matches no single release
- invalid at v19.2 (2026-08-05): 43 distinct labels (0.080), 0.025 of label instances
- repairable by revocation chain: 43; unrepairable: 0
- examples of invalid identifiers: T1002, T1013, T1019, T1022, T1023, T1024, T1031, T1032, T1045, T1050

## tram2
- distinct (domain, identifier) labels: 50; label instances: 5143; sub-technique identifiers: 24
- best-fitting release: v8.2 (2021-01-27), 1.000 of labels live there
- releases in which EVERY label is simultaneously live: 18 (v8.2–v16.1)
- invalid at v19.2 (2026-08-05): 2 distinct labels (0.040), 0.033 of label instances
- repairable by revocation chain: 2; unrepairable: 0
- examples of invalid identifiers: T1562.001, T1574.002
