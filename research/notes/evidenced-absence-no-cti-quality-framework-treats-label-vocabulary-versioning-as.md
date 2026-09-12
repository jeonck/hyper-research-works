---
title: Evidenced Absence — No CTI Quality Framework Treats Label-Vocabulary Versioning
  as a Quality Dimension (B5 negative result)
id: evidenced-absence-no-cti-quality-framework-treats-label-vocabulary-versioning-as
tags:
- attack-ontology-drift-cti-85bc51
- cti-quality
- gap
created: '2026-09-12T13:22:17.758258Z'
source: https://dl.acm.org/doi/full/10.1145/3484202
status: draft
type: note
tier: commentary
content_type: article
deprecated: false
summary: 'Systematic negative result with search log: every CTI quality dimension
  found is defined over item content, item timing or item container; interoperability,
  compliance, provenance, maintenance and STIX object versioning are near-misses,
  none covers ontology versioning.'
---

## What it is
A **negative-result / evidenced-absence note** for batch B5, not a source note. It records the systematic finding that **no CTI data-quality framework located in this sweep contains a dimension covering the versioning, stability or semantic continuity of the label vocabulary (ontology/taxonomy) in which intelligence is expressed**, together with the search log that supports the absence.

## The claim
Across the recognised CTI quality frameworks — the Delphi-derived dimension set, the STIX-anchored computable metric set, the feed measurement metric sets, the operational continuous-monitoring metric set, the MISP weighted-criteria set, and the 2025 measurement-based survey of 200+ CTI studies — **every quality dimension is defined over one of three things**:
1. **the item's content** (accuracy, completeness, verifiability, false positives, relevance, extensiveness, similarity);
2. **the item's timing** (timeliness, latency, maintenance, lifecycle/validity windows);
3. **the item's container** (interoperability, compliance, provenance, reliability, actionability).
**None is defined over the reference vocabulary the item's labels point into.**

### The four near-misses, and why each is not the missing dimension
- **Interoperability** — exchangeability of *format* (STIX/TAXII, MISP schema). Answers "can your platform parse it?", not "does T1086 still mean what it meant?". An ATT&CK ID that was revoked three releases ago is perfectly interoperable.
- **Compliance** — conformance to a standard's syntax. A syntactically valid `external_reference` to a deprecated technique passes.
- **Provenance** — who produced the item and through what chain. Not *which release of the reference taxonomy the labels were drawn from*. Notably, provenance is the dimension a version-pinning practice would naturally extend, and no framework found makes that extension.
- **STIX object versioning / "update handling"** (raised in practitioner material) — versioning of the *individual CTI object* by its producer (`modified` timestamps, update semantics). This is the only versioning concept present anywhere in the sweep, and it is a **different object**: the CTI item, not the vocabulary.
- **Maintenance** — whether the *source/feed* is still actively maintained. Not whether the *taxonomy* moved.

## Why this matters for the query
1. **The gap is real and is the paper's opening.** A proposed additional dimension — *referential stability* / *vocabulary-version integrity* — is not redundant with any of the seven Delphi dimensions or the nine-parameter extended list. It can be introduced as an eighth dimension into an existing, already-accepted weighting apparatus (fuzzy-AHP / entropy) rather than as a rival framework.
2. **The field already concedes the underlying validity threat, in a different register.** The ACM CSUR 2025 measurement survey states that CTI evaluation results depend on which vendors are in the dataset; Zibak et al. report that no concrete metrics exist for *any* dimension; RAID 2024 interview evidence (n=25) reports practitioners have no systematic QA processes. So the argument does not have to establish that CTI quality is unmeasured — only that the *label vocabulary* is the unmeasured part that nobody has named.
3. **The method template already exists.** Li et al. (USENIX '19) supply differential vs. exclusive contribution across time; the CTI Echo Chamber paper (arXiv 2602.17458) supplies the discipline of open-sourcing normalization rules so longitudinal comparisons reproduce. Both apply this to *sources*; neither applies it to the *ontology*.

## Search log supporting the absence (WebSearch only; direct fetching blocked)
Assigned queries run: (1) "cyber threat intelligence data quality accuracy timeliness study"; (2) "threat intelligence feed evaluation measurement study"; (3) "CTI sharing challenges evidence-driven analysis"; (4) "STIX TAXII data quality problems practitioners".
Follow-ups run: (5) the Zibak seven-dimension Delphi paper by name; (6) Schlette "Measuring and visualizing CTI quality" STIX dimensions/metrics; (7) "Reading the Tea Leaves" metrics/overlap findings; (8) "Big Beast to Tackle" QA interview findings; (9) **CTI quality framework dimension "ontology" OR "taxonomy" versioning consistency ATT&CK version** — returned ATT&CK-ontology-design papers (D3FEND/OWL, ATT&CK ontology design) and TTP-extraction papers, **not a single quality framework with a versioning dimension**; (10) **quality dimension completeness consistency + taxonomy version / label vocabulary change / reproducibility CTI dataset** — surfaced the CSUR survey and the Echo Chamber normalization work, again **no versioning quality dimension**; (11) CTI Echo Chamber specifics; (12) CSUR measurement survey specifics; (13) temporal dynamics of CTI (arXiv 2412.19086) — that line is about **IoC publication timing relative to CVEs**, i.e. temporality of *publication*, not of *vocabulary*.

## Strength of the absence claim (honest grading)
- **Strong** for: the Zibak/DTRAP seven-dimension set (the dimension list is reported consistently and completely across sources, and no versioning item appears in it).
- **Moderate** for: Schlette/STIX metrics, the MISP weighted-criteria set, the feed-measurement metric sets — the metric lists are reported at abstract level and are complete enough to see what is absent, but one could not rule out a versioning remark inside the body text.
- **Weak/provisional** for: FeedMeter (its eight metrics were **not** enumerable from search results) and the CSUR 200+-study survey (a sentence about taxonomy versioning could exist somewhere in a survey that long).
- **Action before submission**: the absence claim must be upgraded by full-text reading of at least Zibak et al. (DTRAP 2022), Schlette et al. (IJIS 2021), the CSUR 2025 survey, and FeedMeter, plus a keyword pass for "version", "deprecat", "revok", "ATT&CK v" in each.

## Fidelity
This note is analysis over search-result summaries; **no source in batch B5 was readable in full text** because the egress proxy blocked `hyperresearch fetch` (tested once against arXiv: 403), WebFetch and curl. No verbatim quotation from any source is asserted anywhere in this batch. The absence finding is a well-scoped *provisional* negative result with its evidence grade stated per-framework above.
