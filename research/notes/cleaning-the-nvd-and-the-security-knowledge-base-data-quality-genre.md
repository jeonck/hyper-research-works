---
title: Cleaning the NVD and the security knowledge-base data-quality genre
id: cleaning-the-nvd-and-the-security-knowledge-base-data-quality-genre
tags:
- attack-ontology-drift-cti-85bc51
- ontology-versioning
created: '2026-09-12T13:23:17.281806Z'
source: https://arxiv.org/pdf/2006.15074
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Established template - enumerate defects, quantify, publish a cleaned derivative,
  show which analyses change - plus the finding that security KB records mutate after
  publication, which is the argument for hash-pinning over version-pinning.
---

## What it is

"Cleaning the NVD: Comprehensive Quality Assessment, Improvements, and Analyses" (arXiv 2006.15074). A systematic quality assessment of the National Vulnerability Database, identifying defect classes and producing a cleaned derivative dataset.

## Concept/mechanism it contributes

The methodological pattern the manuscript should imitate for its ATT&CK census: (1) enumerate defect classes in a widely used security knowledge base; (2) quantify their prevalence; (3) publish a *cleaned or normalized* derivative artefact; (4) show the analyses that change when the cleaned artefact is used instead of the raw one. Step (4) is what elevates a data-quality paper above a complaint.

The broader NVD-quality literature it sits in supplies related, citable findings: the (un)reliability of NVD "vulnerable versions" data demonstrated on Google Chrome; "Half-Day Vulnerabilities", a study of how CVE entries change during their first days after publication (i.e. entries are not stable at publication time); and the general warning that if a data source contains wrong data, conclusions derived from it may be invalid.

The "Half-Day Vulnerabilities" strand is the sharpest for this batch: it establishes that entries in a security knowledge base are *mutable after publication*, so the version of a record a researcher retrieved depends on *when* they retrieved it, not only on which release they cite. That is the same failure mode as ATT&CK's version-unchanged patches, in a database that CTI researchers already accept is unstable.

## Mapping onto ATT&CK

- Precedent that the security-research community accepts "the knowledge base itself is the object of study" as a legitimate and publishable contribution. The manuscript does not need to argue that this genre is valid; it needs to argue that ATT&CK has not yet received this treatment at the required rigour.
- The "publish a cleaned derivative" step maps to the manuscript's deliverable: a version-normalized ATT&CK crosswalk plus re-expressed benchmark/training corpora, released as an artefact. Without it, the paper is an audit; with it, it is infrastructure.
- The mutability-after-publication finding is the argument for hash-pinning rather than version-pinning alone: citing a release name does not determine which bytes were used if records can be edited in place.
- Difference to state honestly: NVD quality problems are largely *errors* (wrong versions, missing fields, inconsistent scores), whereas ATT&CK drift is largely *intentional, legitimate curation*. The manuscript's framing must not treat ATT&CK drift as a defect — the point is that correct curation still destroys comparability if consumers do not normalize. This is a stronger and more interesting claim than "the data is dirty".

## Fidelity

Summary fidelity. arXiv could not be fetched (egress proxy returns 403 for arxiv.org). The description of the paper's structure, the related NVD-quality findings (Chrome vulnerable-versions study; Half-Day Vulnerabilities) and the general data-quality warning are from search-result snippets and titles, not from the full texts. No verbatim quotation is asserted; no specific numeric findings are claimed. Verify authorship, venue and the exact defect taxonomy before citing.
