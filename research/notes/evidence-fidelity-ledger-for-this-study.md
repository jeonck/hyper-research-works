---
title: Evidence fidelity ledger for this study
id: evidence-fidelity-ledger-for-this-study
tags:
- attack-ontology-drift-cti-85bc51
- methodology
created: '2026-09-12T13:23:20.040652Z'
source: https://github.com/mitre-attack/attack-stix-data
status: draft
type: note
tier: ground_truth
content_type: dataset
deprecated: false
summary: Which claims rest on primary artefacts, which on search summaries, which
  on audited absences
---

# Evidence fidelity ledger for this study

Fidelity: AUTHORED. This note records what kind of evidence each claim class in
the manuscript rests on, so that the distinction survives into the paper instead
of being smoothed away.

## Tier A — primary artefact, read in full, recomputable

- Every ATT&CK measurement (E1–E8). Computed by `code/` from the STIX release
  bundles in `mitre-attack/attack-stix-data`, which are cloned locally and read
  in full. Any reader with the repository can rerun `code/run_all.sh` and obtain
  the same numbers; the only stochastic components are seeded.
- Every label-validity claim about CTIBench, rcATT, TRAM and TRAM 2 (E7). Read
  from each corpus's own label files in its public repository, not from its
  paper's description of those files.

## Tier B — secondary literature at summary fidelity

- All positioning claims about prior work. In this environment the egress proxy
  blocks direct retrieval of arXiv, publisher sites and the ATT&CK website; the
  literature was surveyed through a web-search tool that returns titles, URLs
  and content summaries. Those summaries are sufficient to establish that a work
  exists, what problem it addresses, and its headline findings. They are NOT
  sufficient to support a verbatim quotation, a precise numeric claim attributed
  to a paper's table, or an exhaustive statement about what a paper does not say.
- Consequence for the manuscript: no quotation marks are placed around text from
  a Tier-B source. Where a Tier-B source's number is reported it is attributed
  as reported, not as verified.

## Tier C — audited absences

- "No published CTI quality framework names vocabulary versioning as a quality
  dimension." This is an absence established by targeted search across the
  canonical quality-dimension literature. It is stated in the manuscript as what
  it is — an absence found by a bounded search, with the search recorded — and
  never as proof that no such framework exists. A full-text keyword pass over
  the named frameworks is listed in the threats-to-validity section as work a
  camera-ready version should complete.

The distinction matters for this paper in particular. Its thesis is that the
field has been careless about the provenance of its labels; a paper making that
argument cannot itself be careless about the provenance of its claims.
