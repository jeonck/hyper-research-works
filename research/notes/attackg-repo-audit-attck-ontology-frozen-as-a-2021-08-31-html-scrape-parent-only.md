---
title: 'AttacKG repo audit: ATT&CK ontology frozen as a 2021-08-31 HTML scrape, parent-only
  templates, unvalidated non-Enterprise IDs'
id: attackg-repo-audit-attck-ontology-frozen-as-a-2021-08-31-html-scrape-parent-only
tags:
- attack-ontology-drift-cti-85bc51
- ttp-extraction
created: '2026-09-12T13:22:53.894188Z'
source: https://github.com/li-zhenyuan/Knowledge-enhanced-Attack-Graph
status: draft
type: note
tier: ground_truth
content_type: dataset
deprecated: false
summary: AttacKG's technique knowledge is a dated HTML scrape (MITRE ATT&CK-20210831.html,
  v9 era); its reference graph has 185 parent-only IDs plus ICS and non-ATT&CK identifiers
  scraped in unvalidated.
---

## What this is
Audit of **AttacKG** (Li, Zheng, Li, Wang, Chen, *AttacKG: Constructing Knowledge-enhanced Attack Graphs from Cyber Threat Intelligence Reports*, ESORICS 2022), cloned at `/home/user/ext/Knowledge-enhanced-Attack-Graph`. AttacKG is the leading *graph-template-matching* (as opposed to text-classification) TTP extraction system, and its templates are built by scraping ATT&CK technique procedure examples.

## How its ATT&CK vocabulary is frozen — read from the artefact
- The technique knowledge is not a versioned STIX bundle but a **date-stamped HTML scrape**: `Archive-v0.1/Mitre_TTPs/mitre_html/` contains **`MITRE ATT&CK-20210831.html`** alongside `Techniques-Enterprise.html` and `MITRE ATT&CK.html`. The filename dates the ontology snapshot to **31 August 2021 — Enterprise ATT&CK v9 era** (v9 Apr 2021; v10 shipped Oct 2021). Nothing else in the repo states a version.
- The distributed reference graph `Tactic_Technique_Reference_Example.gml` contains **185 distinct `Txxxx` identifiers and zero sub-technique (dot-notation) identifiers** — parent-level only, even though the 2021 snapshot already had ~380 sub-techniques. Post-v7 parents such as T1547 and T1059 are present, and pre-v7 IDs (T1064, T1085, T1086) are absent, confirming a post-restructuring but parent-collapsed vocabulary.
- The same file also contains identifiers that are **not Enterprise technique IDs at all**: `T0037`, `T0550` (ICS ATT&CK), and `T2038`, `T2040`, `T2080`, `T2420`, `T9000` (`T9000` is a malware family name, S0098). These are scrape artefacts that entered the reference graph unvalidated.
- `output_techniques.json` (the shipped sample output) resolves to only 20 distinct technique IDs, all parent-level.

## Reported results (search-summary, from the repo README's paper abstract)
AttacKG was evaluated against 1,515 real-world CTI reports, identifying 28,262 attack techniques with 8,393 unique IoCs; on eight manually labelled reports it reports F1 of 0.895 (entities), 0.911 (dependencies), **0.819 (techniques)**, compared against EXTRACTOR and TTPDrill. Note the README abstract and the search-result summary quote slightly different technique F1 figures (0.819 vs 0.789), which is itself a small reproducibility wrinkle.

## Why this bears on the query
AttacKG shows a third mode of version freezing, distinct from rcATT (CSV label columns) and TRAM (declared STIX bundle): **the ontology is baked into scraped HTML and into hand-derived graph templates**, so re-versioning requires regenerating templates, not just remapping IDs. Template-matching systems are therefore the hardest class of TTP extractor to re-baseline across ATT&CK releases — a point a normalization protocol must address explicitly. The unvalidated non-Enterprise IDs in its reference graph are a concrete instance of ontology hygiene failing silently.

## Fidelity
**Mixed.** The version dating, ID counts, sub-technique absence and spurious-ID findings are **read from artefact** (files named above). The evaluation numbers are **search-summary / README-abstract level**; I could not fetch the published ESORICS paper (egress blocked).
