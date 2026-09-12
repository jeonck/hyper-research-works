---
title: 'ATT&CK v19 Defense Evasion split measured: 29.4% of active techniques changed
  tactic, T1562 family revoked 3-to-1 into T1685'
id: attck-v19-defense-evasion-split-measured-294-of-active-techniques-changed-tactic
tags:
- attack-ontology-drift-cti-85bc51
- attack-versioning
- quarantined-metadata-mismatch
created: '2026-09-12T13:24:01.266049Z'
updated: '2026-09-12T13:45:46.459291Z'
source: https://github.com/mitre-attack/attack-stix-data
status: deprecated
type: note
tier: ground_truth
content_type: dataset
deprecated: true
summary: 'QUARANTINED: front matter and body describe different sources; excluded
  from the corpus (see data/results/e15_vault_integrity.json).'
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
