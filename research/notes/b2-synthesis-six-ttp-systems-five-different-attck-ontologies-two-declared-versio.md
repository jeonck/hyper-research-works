---
title: 'B2 synthesis: six TTP systems, five different ATT&CK ontologies, two declared
  versions'
id: b2-synthesis-six-ttp-systems-five-different-attck-ontologies-two-declared-versio
tags:
- attack-ontology-drift-cti-85bc51
- ontology-versioning
created: '2026-09-12T13:25:02.129353Z'
source: https://github.com/center-for-threat-informed-defense/tram
status: draft
type: note
tier: ground_truth
content_type: dataset
deprecated: false
summary: 'Cross-artefact audit: 2/6 TTP systems declare an ATT&CK version; rcATT has
  49.8% dead labels, v13.1 itself is 19.1% tombstones, and a declared v12 remap still
  leaks 3.6% pre-v7 IDs in its inherited split.'
---

## What this is
**Cross-artefact synthesis of B2's repository audits.** Not a source note: this consolidates the file-level evidence I extracted from five cloned TTP-extraction/attribution artefacts into the single table the query needs. Every figure here is computed by me from the named files; the reference ontology throughout is the **Enterprise ATT&CK 13.1** STIX bundle shipped inside CTID TRAM (`x-mitre-collection` "Enterprise ATT&CK 13.1", modified 2023-05-09), which contains **750 attack-patterns: 607 live (196 parents + 411 sub-techniques), 131 revoked, 12 deprecated**.

## The version-declaration audit

| System | Declares ATT&CK version? | Where the ontology is actually frozen | Inferred release | Label space | Sub-techniques? |
|---|---|---|---|---|---|
| **rcATT** | **No** — no version string anywhere in code or data | CSV header columns of `training_data_original.csv` | v5/v6 (2019–early 2020) | 12 tactics + **215** flat techniques | **None** |
| **AttacKG** | **No** | scraped `MITRE ATT&CK-20210831.html` + hand-built graph templates | v9 era (Aug 2021) | **185** IDs in the reference GML | **None** |
| **tumeteor/mitre-ttp-mapping** (EACL'24) | **Yes** — README states "remap to MITRE ATTACK 12.0" | TSV `labels` column | v12.0 (declared) | **519** distinct labels / 23,007 occurrences | **341 of 519** |
| **TRAM / TRAM2** (CTID) | **Yes** — README badge "MITRE ATT&CK v13" + bundled STIX | `data/attack/enterprise-attack.json` | **13.1** (explicit) | **50** trained classes | 24 of 50 |
| **CTI-Bench** (CTI-ATE) | **No** | a 202-entry ID list **inlined as literal text in every prompt** | v15/v16 era (contains T1665, added v15) | **202** Enterprise + 73 Mobile | **Deliberately excluded** |
| **TTPXHunter** | Not stated in any summary obtained | unverified (repo would not clone) | unknown | 193 TTPs / 10,906 sentences | unverified |

**Score: 2 of 6 declare a version. 0 of 6 declare a granularity policy explicitly enough to compare against another system.**

## The three headline drift measurements

1. **Half of a baseline's alphabet is dead.** **107 of rcATT's 215 technique labels (49.8%)** are revoked or deprecated in v13.1. Its live coverage is **108/607 = 17.8%** of the v13.1 label space; it cannot express 88 live parents or any of the 411 live sub-techniques. rcATT is still used as a comparison baseline in 2024–2026 papers.

2. **A fifth of a release is bookkeeping.** In the official v13.1 Enterprise bundle, **143/750 = 19.1%** of attack-pattern objects are revoked or deprecated tombstones. Any "the knowledge base grew to N techniques" claim that counts objects in a bundle over-counts by roughly this margin, and the tombstone fraction is itself a per-release measurable.

3. **Declaring a version does not achieve one.** tumeteor/mitre-ttp-mapping declares a v12.0 remap, yet **208 of 23,007 label occurrences (0.90%)** are dead in v13.1 — and the residue is entirely concentrated in the split inherited from a third-party corpus: **203/5,567 = 3.6% of the TRAM-derived split**, vs **0.00% in both MITRE-sourced splits**. The dead IDs are T1064 Scripting ×128 (revoked in v7 — five releases before the declared target), T1043 ×67, T1108 ×7, T1026 ×3, T1061 ×2, T1034 ×1.

## What this establishes for the query
- **Comparability**: five systems routinely tabulated against one another sit on five different ontologies spanning v5→v15, differing not only in ID inventory but in *granularity* (flat vs. parent-collapsed vs. 341-sub-technique). No arithmetic relation exists between their F1 scores.
- **Reproducibility**: in 4 of 6 artefacts the ontology version is recoverable only by forensic inspection of data files — exactly what I had to do here. It is not recorded, so it cannot be re-created.
- **Normalization protocol, minimum viable form, as implied by these findings**: (i) declare the release as a version *and* a bundle hash; (ii) declare a granularity policy (parent-collapse / sub-technique-native / hierarchy-aware scoring); (iii) run a **liveness assertion** — every label must resolve to a non-revoked, non-deprecated object in the declared release — and report unmappable labels rather than retaining them silently; (iv) when forward-porting, follow `revoked-by` relationships and report the count of forwarded, split and dropped labels; (v) report scores under at least two releases so drift sensitivity is visible.

## Fidelity
**Read from artefact** for every number concerning rcATT, AttacKG, tumeteor/mitre-ttp-mapping, TRAM and CTI-Bench. **Search-summary** for the TTPXHunter row. Release-name inferences (v5/v6 for rcATT, v9 for AttacKG, v15/v16 for CTI-Bench) are my dating from which IDs and names are present, not statements those artefacts make about themselves.
