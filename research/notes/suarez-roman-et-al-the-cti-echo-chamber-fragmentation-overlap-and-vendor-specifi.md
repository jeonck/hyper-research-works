---
title: 'Suarez-Roman et al. — The CTI Echo Chamber: Fragmentation, Overlap and Vendor
  Specificity in Twenty Years of Cyber Threat Reporting (arXiv 2602.17458)'
id: suarez-roman-et-al-the-cti-echo-chamber-fragmentation-overlap-and-vendor-specifi
tags:
- attack-ontology-drift-cti-85bc51
- cti-quality
created: '2026-09-12T13:22:02.961723Z'
source: https://arxiv.org/abs/2602.17458
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: '13,308 CTI reports over two decades: 88% niche vendors, very low pairwise
  overlap, diminishing returns; open-sources its actor-name normalization rules for
  reproducible longitudinal study — the horizontal analogue of ontology drift.'
---

## What it is
Suarez-Roman, Marciori, Conti & Tapiador, "The CTI Echo Chamber: Fragmentation, Overlap, and Vendor Specificity in Twenty Years of Cyber Threat Reporting," arXiv:2602.17458 (submitted 19 Feb 2026). A large-scale longitudinal measurement of the open-source CTI reporting corpus itself.

## What it says bearing on the query
- **LLM-based pipeline ingests and structures 13,308 open-source CTI reports spanning two decades**, extracting attributed threat actors, motivations, victims, reporting vendors, and technical indicators (IoCs and TTPs).
- **88% of vendors are niche players**; a small set of "super-vendors" supplies the bulk of global, multi-actor intelligence — a highly fragmented, long-tail ecosystem.
- **Average intelligence overlap between any two vendors is very low**, both in which threat actors they track and in the specific intelligence provided about a shared actor; additional sources yield **diminishing returns** beyond a few core providers.
- Vendors show significant **geographic and sectoral reporting biases** — distinct silos.
- Explicitly addresses **threat-actor naming fragmentation and normalization**: normalization aims to preserve consistent, vendor-agnostic naming while minimizing information loss from alias variability, and the **normalization rules are open-sourced to support reproducibility and future longitudinal studies**.

## Bearing on ATT&CK ontology drift
This is the **closest methodological sibling in the literature and the best model for the contribution's shape**:
1. It establishes the precedent that **name/label instability is a first-class measurement object in CTI**, and that quantifying it across twenty years is publishable, top-venue-adjacent work.
2. It establishes the **reporting-discipline precedent** the query asks for: publishing the normalization rule set as an artifact so longitudinal comparisons are reproducible. The ontology-drift protocol should mirror this exactly (publish the version-to-version technique mapping, not just the results computed under it).
3. It also marks the gap precisely: their normalization problem is **horizontal** (vendor A's "APT29" = vendor B's "Cozy Bear", at one time). The ontology-drift problem is **vertical** (ATT&CK v7's T1086 vs v8's T1059.001, across time), and is arguably harder because the authority is *singular and centralized* — there is no cross-vendor disagreement to average out, only a single publisher silently redefining the reference.
4. The "diminishing returns / low overlap" result is the vendor-side analogue of the growth-decomposition question: apparent corpus growth is substantially redundancy and re-description rather than new intelligence.

## Fidelity
Could not read full text (arXiv blocked). The 13,308-report count, the 88% niche-vendor figure, the low-overlap/diminishing-returns findings, and the open-sourced-normalization-rules claim are at summary fidelity from search-result descriptions of the abstract and body. No verbatim quotation asserted. Recent preprint (Feb 2026) — check for a peer-reviewed version before citing.
