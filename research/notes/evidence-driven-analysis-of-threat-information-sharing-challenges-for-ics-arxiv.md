---
title: Evidence-Driven Analysis of Threat Information Sharing Challenges for ICS (arXiv
  2512.18714 / Computers & Security 2026)
id: evidence-driven-analysis-of-threat-information-sharing-challenges-for-ics-arxiv
tags:
- attack-ontology-drift-cti-85bc51
- cti-quality
created: '2026-09-12T13:21:45.934708Z'
source: https://arxiv.org/abs/2512.18714
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Empirical measurement of STIX volume/timeliness/coverage/quality across public
  sources; diagnoses insufficient standardization and TTPs lacking defined technical
  artifacts — underspecification, not version drift.
---

## What it is
"An Evidence-Driven Analysis of Threat Information Sharing Challenges for Industrial Control Systems and Future Directions," arXiv:2512.18714 (v2), also published in *Computers & Security* (2026), DOI path S0167404826001550. An empirical measurement of CTI *sharing* effectiveness rather than of a single feed.

## What it says bearing on the query
- Conducts a **comprehensive empirical measurement of CTI sharing effectiveness**, analysing **STIX volume, timeliness, coverage and quality across public sources**, and reports significant variation in feed quality across the shared-intelligence environment.
- Identifies persistent structural barriers: **governance issues, misaligned incentives, and insufficient standardization**; and at the systems level the **producer–consumer imbalance, data validity, legal/regulatory factors**, and the difficulty of sharing genuinely *intelligent* intelligence rather than raw indicators.
- ICS-specific and highly relevant to the TTP layer: a key challenge identified is the **lack of defined technical artifacts to support sharing OT threat indicators through STIX, with multiple TTPs lacking sufficiently defined technical artifacts**.
- Concludes that **domain-specific CTI methodologies** are required — the generic vocabulary does not fit every operational domain.

## Bearing on ATT&CK ontology drift
- The strongest source in this batch for the claim that **"insufficient standardization" is diagnosed at the level of format and governance, not at the level of vocabulary versioning**. The remedy proposed is more/better-defined artifacts, not version-pinned or drift-normalized ones.
- The "multiple TTPs lack sufficiently defined technical artifacts" finding is adjacent to, but distinct from, ontology drift: it is about *underspecification at a point in time*, whereas drift is about *respecification across time*. A contribution can cite this as evidence the community already accepts that TTP-level semantics are shaky, then show that the temporal dimension compounds it.
- ATT&CK for ICS is itself a separately-versioned matrix that has undergone structural reorganization (including absorption into the enterprise release cadence), which makes ICS an especially sharp case study for cross-version comparability.

## Fidelity
Could not read full text — arXiv HTML/PDF and ScienceDirect both returned 403 through the egress proxy (a direct fetch of arxiv.org/abs/2512.18714 was attempted and blocked). Claims are at summary fidelity from search-result descriptions. **No numeric results from the measurement are claimed here** because I could not read them; the STIX volume/timeliness/coverage figures must be taken from the paper itself. No verbatim quotation asserted.
