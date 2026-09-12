---
title: 'OBO Foundry Identifier Policy: global uniqueness, no reuse, and persistence
  as a provider obligation'
id: obo-foundry-identifier-policy-global-uniqueness-no-reuse-and-persistence-as-a-pr
tags:
- attack-ontology-drift-cti-85bc51
- ontology-versioning
created: '2026-09-12T13:21:08.059098Z'
source: https://obofoundry.org/id-policy.html
status: draft
type: note
tier: institutional
content_type: policy
deprecated: false
summary: 'Artefact-read identifier policy: one ID per concept forever, bidirectional
  ID-URI mapping, persistence that must outlive the maintainer - the codified guarantee
  ATT&CK follows in practice but has never published.'
---

## What it is

The OBO Foundry Identifier Policy (`id-policy.md`), read as an **artefact** from a shallow clone of `github.com/OBOFoundry/OBOFoundry.github.io`. It governs how term identifiers are minted, mapped to URIs, and maintained over time.

## Concept/mechanism it contributes

Stated design goals, verbatim:

> "- There must be a predictable, bidirectional mapping between OBO IDs, and OBO Foundry-compliant URIs.
> - The URIs should resolve to useful information about a term.
> - The URIs should be designed so that they can be maintained over time to keep pointing to useful information.
> - Each OBO ID is assigned to a only single term within the set of all OBO ontologies.
> - There is a 1:1 mapping of OBO IDs to Foundry-compliant URIs."

Two properties matter for the manuscript. First, **global uniqueness with no reuse**: an ID is assigned to exactly one term across the whole federation, forever; there is no scenario in which an identifier is recycled for a different concept. Second, **persistence as an obligation on the provider, not a courtesy**: the policy imports Shared Name Initiative criteria, including that it must be clearly stated what the intended referent of each URI is, that URI documentation must be an ongoing concern whose provision "may have to outlive the original ontology developer's group or creator", and that the provider must be responsive to community needs such as having mistakes fixed in a timely manner. If a project's service lapses, the Foundry may take over serving the identifiers.

The complementary practice, documented in the OBO Academy "Obsoleting an Existing Ontology Term" guide, is to keep obsolete terms in the released artefact indefinitely at the same IRI so that old data continues to resolve — obsolete terms are never dead links.

## Mapping onto ATT&CK

- ATT&CK technique IDs (`Txxxx`) are, to the best of public evidence, not reused after revocation or deprecation — but this is *practice*, not published policy. The manuscript can note the absence of a written non-reuse guarantee as a reproducibility risk, framed against a vocabulary (OBO) where it is codified and dashboard-checked.
- ATT&CK's sub-technique restructuring is exactly the case OBO's 1:1 policy anticipates: T1086 (PowerShell) becoming T1059.001 means a *new* identifier for a re-scoped concept, with the old one revoked and pointing forward. That is the OBO-correct behaviour, and the manuscript should say so — the ontology-engineering criticism of ATT&CK is not that it restructured, it is that downstream CTI corpora were not migrated and the migration mapping is not first-class.
- The "URI documentation must outlive the creator" criterion is the argument for the manuscript's requirement that a CTI paper archive the ATT&CK bundle it used rather than cite a live URL: ATT&CK's website renders the *current* definition at `attack.mitre.org/techniques/Txxxx/`, so a citation to that URL silently re-resolves to a possibly rewritten concept.
- Practical protocol item: the manuscript's crosswalk table (old ID → successor ID(s) → version range in which the mapping holds) is the CTI analogue of the OBO ID↔URI bidirectional mapping plus `replaced_by`, and should be published as a versioned, machine-readable artefact with the same non-reuse and persistence guarantees.

## Fidelity

Ground truth for the quoted design goals and the Shared Name Initiative criteria: read from `/home/user/ext/obofoundry/id-policy.md` in a shallow clone taken 2026-09-12. The OBO Academy obsoletion-guide claim ("maintain obsolete terms indefinitely at the same IRI") is at search-snippet fidelity — the page itself was not fetched (egress blocked) — and should be re-verified before quotation. Claims about ATT&CK ID-reuse practice are inference from observed data, not from a published MITRE policy statement; treat as a hypothesis to test, not an established fact.
