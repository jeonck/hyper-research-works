---
title: 'Synthetic APTs (2026): LLM agents reproduce documented APT profiles at 55-80%
  precision'
id: synthetic-apts-2026-llm-agents-reproduce-documented-apt-profiles-at-55-80-precis
tags:
- attack-ontology-drift-cti-85bc51
- ttp-attribution
created: '2026-09-12T13:24:00.197467Z'
source: https://arxiv.org/abs/2606.07158
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 20 cyber-range experiments show agents given published ATT&CK group profiles
  match those profiles at 55-80% precision, bounding how discriminative a TTP profile
  can be.
---

## What this is
Mayoral-Vilches et al. (Alias Robotics and collaborators), *Synthetic APTs: the Collapse of TTP-Based Attribution*, arXiv:2606.07158 (2026). An adversarial-validity attack on the core premise of TTP-based attribution.

## What it reports (search-summary fidelity)
- LLM agents were configured with the profiles of **five APT groups — APT28, APT29, APT41, APT44 and Lazarus Group** — and run against AI-driven defender agents across two cyber ranges (CYBER RANGES Enterprise and Military).
- **20 experiments, two defender models.** All 10 Enterprise-range runs ended in compromise (2–12 hosts each); all 10 Military-range runs were defended or stalemated, regardless of APT profile or defender model.
- **MITRE ATT&CK verification against the official group profiles maps the observed kill chains back to the documented APT profiles with 55–80% precision** across the 10 Enterprise experiments reaching domain compromise.
- In **8 of 10** Enterprise experiments the attacking agents independently weaponised the defender's own **Velociraptor** endpoint-management platform as a C2 channel — a convergent behaviour **not encoded in any threat-intelligence profile**.
- Argument: if an agent given a published ATT&CK group profile can reproduce that group's documented signature at 55–80% precision with no specialised tradecraft, then false-flag operations become available to anyone with model access, and the entry barrier to "operating like a nation-state APT" collapses.

## Why this bears on the query
Two distinct contributions to the argument:
1. **Construct validity of the attribution target.** It gives a numeric upper bound on how distinctive an ATT&CK group profile actually is: 55–80% precision reproducibility means published profiles are substantially *imitable*. Any attribution benchmark scored against ATT&CK group profiles is therefore measuring profile-matching, not actor identity.
2. **The Velociraptor finding is an ontology-coverage result in disguise.** A behaviour that dominated 8/10 runs is absent from every group profile — i.e. the knowledge base lags observed adversary behaviour, which is the mirror image of the query's bookkeeping-vs-intelligence question. Growth in the KB is not tracking the behaviours that actually decide engagements.

## Relation to ontology drift
The paper attacks TTP attribution from the *adversary-behaviour* direction; the query attacks it from the *ontology-version* direction. They compose: if profiles are both imitable (55–80%) **and** re-indexed between releases, the effective discriminative power of a TTP profile is bounded well below what attribution papers report.

## Fidelity
**Search-summary.** arXiv full text not fetchable (egress blocked). All figures above are as reported in search summaries of the paper; no verbatim quotation asserted. Treat the 55–80% and 8/10 figures as needing verification against the PDF in a later pass.
