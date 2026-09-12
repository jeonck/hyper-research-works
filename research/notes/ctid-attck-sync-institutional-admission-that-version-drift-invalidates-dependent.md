---
title: 'CTID ATT&CK Sync: institutional admission that version drift invalidates dependent
  projects, but tooling not measurement'
id: ctid-attck-sync-institutional-admission-that-version-drift-invalidates-dependent
tags:
- attack-ontology-drift-cti-85bc51
- attack-versioning
created: '2026-09-12T13:24:45.006240Z'
source: https://ctid.mitre.org/projects/attack-sync/
status: draft
type: note
tier: institutional
content_type: docs
deprecated: false
summary: MITRE's own centre states dependent projects are pinned to whatever ATT&CK
  version was current at development time and quickly become out-of-date; ATT&CK Sync
  flags affected mappings but publishes no quantification of corpus impact or analytic
  performance change.
---

## What this is
Md Nazmul Haque et al., *Beyond Single Reports: Evaluating Automated ATT&CK Technique Extraction in Multi-Report Campaign Settings*, arXiv:2604.07470 (2026). The largest comparative evaluation of ATT&CK technique extractors I located in this batch.

## What it reports (search-summary fidelity)
- Evaluates **29 state-of-the-art ATT&CK technique extraction methods** spanning three methodological families, using multiple CTI reports per campaign for the **SolarWinds, Log4j and XZ Utils** campaigns.
- Aggregating multiple reports on the same campaign improves **F1 by ~26%** over single-report analysis; most methods **saturate after 5–15 reports**.
- Even so, absolute performance stays low: **max F1 78.6% (SolarWinds), 54.9% (XZ Utils)**.
- **Up to 33.3% of misclassifications involve semantically similar techniques that share tactics and overlap in descriptions.**

## Why this bears on the query — the 33.3% figure is the key one
That error mode — confusion among techniques that share a tactic and have overlapping descriptions — is *the same structural property* that drives ATT&CK's own restructuring decisions. Techniques get merged, split into sub-techniques, or revoked into one another precisely because their descriptions overlap. So a large fraction of the residual error in TTP extraction is not model error at all: it is the extractor being penalised for failing to guess which side of a boundary MITRE drew in the release the labels came from. Under a different release, a meaningful share of those 33.3% would be scored correct.

This is the strongest published evidence in B2 that **extraction scores are partly a measurement of ontology boundary placement rather than of extraction skill** — and it supplies the natural normalization test: re-score under parent-collapse and under a sibling-equivalence relation, and report how much of the error survives.

## What it does not do
The summaries available give no indication that the 29 systems were re-baselined onto a common ATT&CK release before comparison. Since those 29 systems span at least rcATT (v5/v6 era), AttacKG (v9 era), TRAM (v13), TTPXHunter (undeclared) and LLM prompt-based methods (v15+ vocabularies), a like-for-like comparison would require exactly the normalization protocol the query proposes. **Whether they did this is the single most important thing to check in a follow-up wave.**

## Fidelity
**Search-summary.** Full text not fetchable (egress blocked, 403 confirmed on arXiv). All figures as reported in search summaries; no verbatim quotation asserted. The interpretation of the 33.3% figure is my argument, not the paper's stated conclusion.
