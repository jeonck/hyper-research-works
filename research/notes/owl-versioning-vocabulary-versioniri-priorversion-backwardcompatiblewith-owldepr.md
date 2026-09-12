---
title: 'OWL versioning vocabulary: versionIRI, priorVersion, backwardCompatibleWith,
  owl:deprecated'
id: owl-versioning-vocabulary-versioniri-priorversion-backwardcompatiblewith-owldepr
tags:
- attack-ontology-drift-cti-85bc51
- ontology-versioning
created: '2026-09-12T13:21:56.043644Z'
source: https://www.w3.org/2007/OWL/wiki/Ontology_Versions
status: draft
type: note
tier: institutional
content_type: docs
deprecated: false
summary: Standard machine-readable slots for version identity, prior-version lineage,
  declared compatibility and deprecation - ATT&CK has counterparts for deprecation
  and revocation but none for lineage or compatibility.
---

## What it is

The W3C OWL working group's "Ontology Versions" wiki page and the associated OWL 2 versioning vocabulary. Standards-level documentation of how a widely deployed ontology language represents version identity, version lineage and deprecation.

## Concept/mechanism it contributes

OWL supplies *built-in, machine-readable* slots for exactly the metadata whose absence causes ATT&CK drift to be invisible:

- `owl:versionIRI` — the identifier of a specific version of the ontology, distinct from the ontology IRI that names the series. Two identities, deliberately: "which ontology" and "which version of it".
- `owl:versionInfo` — a human-readable version string.
- `owl:priorVersion` — an explicit link from a version to its predecessor, making lineage traversable rather than reconstructed by sorting release names.
- `owl:backwardCompatibleWith` / `owl:incompatibleWith` — *declared* compatibility relations between versions, asserted by the publisher.
- `owl:DeprecatedClass` / `owl:DeprecatedProperty` (OWL 1) and the `owl:deprecated` annotation property (OWL 2) — deprecation as a first-class, queryable statement on the entity.

The page also records the known failure mode: when different versions of an ontology are published online, the links between them are frequently lost because publishers rarely populate `owl:priorVersion` and the compatibility properties. The vocabulary exists; the discipline is what is missing. That is a useful precedent — the manuscript's contribution can be positioned as *supplying the discipline and the audit*, which is where the field's actual gap has historically been, rather than as inventing representation.

## Mapping onto ATT&CK

ATT&CK is distributed as STIX 2.1 bundles, not OWL, so the mapping is by analogy of function:

| OWL construct | ATT&CK counterpart | Status |
|---|---|---|
| `owl:versionIRI` | release version (v14, v15) + per-object `x_mitre_version` | two uncoordinated version axes; no single artefact identity |
| `owl:versionInfo` | release tag | present |
| `owl:priorVersion` | none | lineage must be reconstructed externally |
| `owl:backwardCompatibleWith` / `owl:incompatibleWith` | none | no compatibility assertion of any kind |
| `owl:deprecated` | `x_mitre_deprecated` | present, but metadata-only and with no obsolescence reason |
| (no OWL equivalent; OBO `replaced_by`) | `revoked` + `revoked-by` relationship | present, exact-successor only |

The two genuinely missing slots are **prior-version linkage** and **declared compatibility**. The manuscript's protocol should propose both as STIX extension properties on the `x-mitre-collection` object, explicitly citing OWL's long-standing vocabulary so the proposal reads as adoption of standard practice.

A second, subtler point: OWL's separation of *ontology IRI* (the series) from *version IRI* (the artefact) is the formal reason why "we used ATT&CK" in a CTI paper is an under-specified citation — it names the series, not the artefact.

## Fidelity

Summary fidelity for the wiki page itself (w3.org could not be fetched; egress proxy 403). The list of OWL versioning constructs and their semantics is standard, well-established OWL 1/OWL 2 knowledge and is stated here at summary fidelity without verbatim quotation; the observation about links between published versions being lost in practice is from a search-result snippet of this page. The ATT&CK column of the comparison table is grounded in the STIX property names observed in the mitreattack-python source artefact; the "no counterpart" rows are assertions of absence that should be double-checked against the current ATT&CK STIX specification before publication.
