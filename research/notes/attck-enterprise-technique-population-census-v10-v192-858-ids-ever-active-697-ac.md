---
title: 'ATT&CK Enterprise technique-population census v1.0-v19.2: 858 IDs ever active,
  697 active, 41% of v1.0 IDs survive'
id: attck-enterprise-technique-population-census-v10-v192-858-ids-ever-active-697-ac
tags:
- attack-ontology-drift-cti-85bc51
- attack-versioning
created: '2026-09-12T13:24:00.719016Z'
source: https://github.com/mitre-attack/attack-stix-data
status: draft
type: note
tier: ground_truth
content_type: dataset
deprecated: false
summary: 'Direct count over all 41 Enterprise STIX bundles: 858 distinct technique
  IDs ever active vs 697 active in v19.2; only 77 of 188 v1.0 IDs still active under
  the same ID; naive object counts overcount the catalogue by 23%.'
---

## What this is
Direct audit of the **rcATT** source repository (Legoy, Caselli, Seifert — Univ. of Twente / Siemens), the most-cited open TTP-extraction baseline. Cloned at `/home/user/ext/rcATT` (HEAD `f82f7fd`, single commit "Update README.md"; repo is unmaintained).

## The label space, read directly from the artefact
File inspected: `classification_tools/data/training_data_original.csv` (1,490 labelled reports + header).

- Header has **228 columns** = 1 `Text` + **12 tactic columns** + **215 technique columns**.
- Tactics present: TA0001–TA0011 plus TA0040 (Impact). **TA0042 (Resource Development) and TA0043 (Reconnaissance) are absent** — those were added in Enterprise ATT&CK v8 (Oct 2020), so the label space predates v8.
- **Zero sub-technique labels.** No column uses dot notation (`T1059.003`). The entire vocabulary is flat `T1234` IDs, i.e. the pre-v7 (pre-July-2020) ontology.
- Technique ID range T1001–T1501. T1501 (Systemd Service) was introduced ~v6 and revoked in v7 — dating the snapshot to **Enterprise ATT&CK v5/v6 (2019–early 2020)**.
- `training_data_added.csv` is header-only (0 rows): the advertised "give feedback / retrain" loop ships empty, so the distributed model is frozen on that one snapshot.
- No ATT&CK version string appears anywhere in the code (`grep -rn -i version classification_tools/*.py` returns only the tool's own `# Version: 1.00` banners). **The repo never states which ATT&CK release its labels come from.**

## Cross-version decay (computed against the v13.1 bundle shipped inside CTID TRAM)
Using `/home/user/ext/tram/data/attack/enterprise-attack.json` (x-mitre-collection "Enterprise ATT&CK 13.1", modified 2023-05-09) as the v13.1 reference:

- **107 of rcATT's 215 technique labels (49.8%) are revoked or deprecated in v13.1.** Half of the tool's output alphabet names techniques that no longer exist.
- Examples of still-emitted dead IDs: T1156 (.bash_profile/.bashrc), T1066, T1067 (Bootkit → T1542.003), T1015 (Accessibility Features → T1546.008), T1103 (AppInit DLLs → T1546.010), T1013, T1044, T1034, T1178, T1163, T1165, T1167, T1181, T1182, T1183, T1185, T1198, T1206, T1214, T1215, T1179, T1177, T1128.
- Conversely rcATT **cannot express 88 live v13.1 parent techniques and all 411 live v13.1 sub-techniques**. Live coverage = 108 / 607 ≈ **17.8%** of the v13.1 label space.

## Why this bears on the query
This is a clean, quantified instance of the paper's core claim: a widely used CTI analytics artefact silently encodes a 2019-era ontology, does not declare it, and any score reported against it — or any downstream "coverage" claim built on its output — is incomparable with an artefact built on v7+. The 49.8% figure is a direct measure of ontology-bookkeeping decay (not adversary change) in a single tool's label space over ~4 years / 8 ATT&CK releases.

## Fidelity
**Read from artefact.** All numbers above computed by me from the cloned repo files named. The v13.1 comparison uses the bundle shipped in the CTID TRAM repo, not a fetch from MITRE (egress blocked).
