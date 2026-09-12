---
title: 'OBO Foundry Principle 4: Versioning (version IRIs, release immutability, perpetual
  resolvability)'
id: obo-foundry-principle-4-versioning-version-iris-release-immutability-perpetual-r
tags:
- attack-ontology-drift-cti-85bc51
- ontology-versioning
created: '2026-09-12T13:20:21.347201Z'
source: https://obofoundry.org/principles/fp-004-versioning.html
status: draft
type: note
tier: institutional
content_type: policy
deprecated: false
summary: Artefact-read policy requiring distinct resolvable version IRIs and immutable
  official releases - the established justification for version-pinned (and hash-pinned)
  CTI reporting.
---

## What it is

OBO Foundry Principle 4, "Versioning" (`principles/fp-004-versioning.md`), read as an **artefact** from a shallow clone of `github.com/OBOFoundry/OBOFoundry.github.io`.

## Concept/mechanism it contributes

The requirement that makes cross-version comparability possible at all:

> "The ontology provider MUST have documented procedures for versioning the ontology, and different versions of ontology MUST be marked, stored, and officially released."

with the rationale stated in reproducibility terms:

> "Consumers of ontologies must be able to specify exactly which ontology files they used to encode their data or build their applications, and be able to retrieve unaltered copies of those files in perpetuity."

Three concrete mechanisms:

1. **Version IRI, distinct from the release IRI.** Every official release MUST have a unique version IRI that resolves to that exact artefact, and the version identifier string inside the artefact MUST match the one in the IRI. Identifiers MUST be ISO-8601 `YYYY-MM-DD` or a numbering scheme; the dated form is preferred and variants (two-digit years, other delimiters, other orderings) are explicitly forbidden.
2. **Release immutability.** > "Note that the content of official release files MUST NOT be changed. For example, if a bug is found in some official released file for some ontology, the bug MUST NOT be fixed by changing the file(s) for that official release. Instead the bug fixes should be included in a new official release, with new files."
3. **Perpetual resolvability** via versioned PURLs (`http://purl.obolibrary.org/obo/idspace/YYYY-MM-DD/idspace.owl`), maintained even if files move.

Compliance is machine-checked (version IRI present, well-formed, and resolving to an artefact carrying the same version identifier).

## Mapping onto ATT&CK

ATT&CK satisfies part of this and violates part of it, and the distinction is what the manuscript's reporting discipline turns on:

- ATT&CK *does* ship numbered releases and the `mitre-attack/attack-stix-data` repository does retain per-version STIX bundles, giving a de facto immutable archive — so a version-pinned CTI experiment is *possible*. The manuscript's reporting rule ("state the ATT&CK version, domain and bundle hash") is the direct analogue of citing a version IRI, and should be justified by this principle rather than asserted.
- ATT&CK has **two** version numbers in play — the framework release (e.g. v14, v15) and the per-object `x_mitre_version` — and only the former is what papers cite. OBO's insistence that the version identifier inside the artefact match the version IRI is the fix: a CTI paper citing "ATT&CK v13" is under-specifying, because objects inside v13 carry independent per-object versions and `modified` timestamps.
- The immutability clause is the one to press on: ATT&CK content *is* corrected in place at the object level between releases (see the `patches` category in MITRE's own diffStix tool, where the object version is unchanged but `modified` advances). Under OBO rules a correction gets a new release; under ATT&CK it can arrive as a silent within-ID edit. This is the mechanism behind "silent rewriting of technique descriptions", stated as a policy gap rather than as an accusation.
- Practical protocol item: because ATT&CK does not guarantee artefact immutability the way versioned PURLs do, the manuscript should require a **content hash** of the exact bundle alongside the version string — the strengthening OBO gets from PURLs, CTI must get from hashes.

## Fidelity

Ground truth for the quoted text: read from `/home/user/ext/obofoundry/principles/fp-004-versioning.md` in a shallow clone taken 2026-09-12. Claims about ATT&CK's own release practice in the mapping section are from the `mitreattack-python` source artefact (see the diffStix note), not from this file.
