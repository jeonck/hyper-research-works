---
title: 'TRAM repo audit: declared ATT&CK v13.1, 19% of shipped attack-patterns are
  tombstones, 50-class trained vocabulary'
id: tram-repo-audit-declared-attck-v131-19-of-shipped-attack-patterns-are-tombstones
tags:
- attack-ontology-drift-cti-85bc51
- ttp-extraction
created: '2026-09-12T13:20:59.337494Z'
source: https://github.com/center-for-threat-informed-defense/tram
status: draft
type: note
tier: ground_truth
content_type: dataset
deprecated: false
summary: TRAM declares ATT&CK v13; its bundled v13.1 STIX has 750 attack-patterns
  of which 131 revoked + 12 deprecated (19.1% tombstones), and TRAM2 trains on only
  50 of 607 live labels.
---

## What this is
Audit of **TRAM** (Threat Report ATT&CK Mapper), the Center for Threat-Informed Defense's reference TTP-extraction system. Cloned at `/home/user/ext/tram` (HEAD `f29793d`).

## Version declaration — TRAM does it right, and the version is still stale
- `README.md` line 3 carries an explicit badge: **MITRE ATT&CK v13**, linking to `https://attack.mitre.org/versions/v13/`. This is one of the few systems in this batch that *declares* its ontology version at all.
- The bundled STIX file `data/attack/enterprise-attack.json` (40 MB) contains an `x-mitre-collection` object named **"Enterprise ATT&CK 13.1"**, `modified` 2023-05-09T14:00:00.188Z, STIX spec_version 2.1. 20,050 objects total.

## Composition of the shipped v13.1 bundle (computed)
- **750 `attack-pattern` objects**, of which **414 are sub-techniques**.
- **131 revoked** and **12 deprecated** → only **607 live** (196 live parents + 411 live sub-techniques).
- i.e. **19.1% of the attack-pattern objects in the official v13.1 distribution are tombstones.** Any naive "count the techniques in the bundle" growth metric over-counts by roughly that margin — a direct measure of ontology bookkeeping vs. live intelligence.
- Earliest `modified` among attack-patterns is 2020-10-27; latest 2023-05-09.

## The trained label space is far smaller than the ontology
Files inspected: `data/tram2-data/single_label.json` and `multi_label.json`.
- single_label: **5,089 sentence examples**, **exactly 50 distinct labels**, of which **24 are sub-technique IDs** (e.g. `T1003.001`, `T1059.003`, `T1071.001`).
- multi_label: **19,178 examples**, same **50-class** vocabulary, 24 sub-techniques.
- Top classes are heavily skewed: T1027 (685/678), T1140 (455/466), T1059.003 (345/358), T1055, T1105, T1106, T1078.
- **50 of 607 live v13.1 labels = 8.2% coverage.** Training data also includes the legacy `data/training/bootstrap-training-data.json` and `attack_may_2023_merged_bootstrap_data2.json` (filename itself pins the merge date).

## Why this bears on the query
TRAM is the best-behaved artefact in the batch and still shows both failure modes: (a) an ontology version that is declared but frozen (v13.1, 2023) inside a tool still in active use; (b) an evaluation label space (50 classes) so much smaller than the ontology (607 live) that "ATT&CK coverage" claims derived from it are not claims about ATT&CK at all. The 131-revoked / 12-deprecated split is a reusable ground-truth number for quantifying bookkeeping content in a single release.

## Fidelity
**Read from artefact.** Every number computed by me from the cloned repo files named above.
