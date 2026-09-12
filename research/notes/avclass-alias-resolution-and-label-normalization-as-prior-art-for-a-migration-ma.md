---
title: 'AVClass: alias resolution and label normalization as prior art for a migration
  map'
id: avclass-alias-resolution-and-label-normalization-as-prior-art-for-a-migration-ma
tags:
- attack-ontology-drift-cti-85bc51
- concept-drift
created: '2026-09-12T13:21:42.543127Z'
source: https://software.imdea.org/~juanca/papers/avclass_raid16.pdf
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Canonicalises divergent AV family labels via normalization, alias resolution
  and plurality voting - the structural ancestor of a cross-version ATT&CK normalization
  protocol, but across labellers rather than across releases.
---

## What it is
Sebastián, Rivera, Kotzias, Caballero — "AVclass: A Tool for Massive Malware Labeling", RAID 2016 (software.imdea.org/~juanca/papers/avclass_raid16.pdf); tool at github.com/malicialab/avclass, with successors AVClass2/AVCLASS++ and semantic variants such as AVMiner (arXiv:2208.14221).

## Core claim
Given the many divergent antivirus signatures attached to a sample, produce one family label. The pipeline is: **normalize** each AV signature into tokens, **resolve aliases** (different vendor names for the same family mapped to a canonical name), strip generic tokens, then **plurality-vote** across engines. Stated main limitation: output quality is bounded by input AV labels — AVClass compensates for noise but cannot invent a family tag if no engine emits a non-generic token.

## Relation to ontology drift (label-space vs feature-space)
**Label-space normalization — and the closest existing example of the *kind of artefact* the manuscript must build.** AVClass is essentially a migration/canonicalisation layer over a fragmented label vocabulary: an alias map plus a normalization function plus a voting rule that projects many vocabularies onto one. The structural analogy to an ATT&CK cross-version normalization protocol is direct: alias resolution ≈ revocation mapping (old id redirected to canonical successor); generic-token stripping ≈ handling deprecated/too-coarse techniques; plurality voting ≈ reconciling annotations made under different versions.

Where the analogy breaks, instructively: AVClass canonicalises **across labellers at one moment in time**; ATT&CK normalization must canonicalise **across releases of one labeller over time**. AVClass's alias map is heuristic, community-maintained and lossy; ATT&CK publishes authoritative, machine-readable version-to-version relationships (deprecated/revoked-by markers in the STIX bundles), so the corresponding map can be exact and auditable rather than heuristic. And AVClass has no concept of an identifier whose *definition* changed while the identifier stayed fixed.

## Why it matters for this manuscript
Gives the normalization protocol a recognised ancestor in the security community, which helps a reviewer see the proposal as an established engineering pattern applied to a new axis rather than an invention. It also sets the bar: AVClass earned its citation count by being *released and adopted*, not by being described. An SCI-level ontology-drift contribution should likewise ship a versioned, re-runnable normalization tool plus the migration maps, not only an analysis.

## Fidelity
Summary-level only. Pipeline description (normalization, alias resolution, plurality voting) and the stated limitation come from search-result summaries of the paper abstract and the GitHub README; the RAID PDF was not retrievable through the blocked egress proxy. The claim that ATT&CK STIX bundles carry explicit deprecated/revoked-by markers is from my own background knowledge of the ATT&CK data model and must be verified against the bundles in another batch. No verbatim quotation given.
