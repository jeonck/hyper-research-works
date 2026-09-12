---
title: 'Ontology evolution vs ontology versioning: change management as the core task
  (Klein, Fensel, Noy, Stojanovic line)'
id: ontology-evolution-vs-ontology-versioning-change-management-as-the-core-task-kle
tags:
- attack-ontology-drift-cti-85bc51
- ontology-versioning
created: '2026-09-12T13:21:55.774845Z'
source: https://www.researchgate.net/publication/37538421_Change_Management_The_Core_Task_of_Ontology_Versioning_and_Evolution
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Foundational distinction between evolution (keeping one ontology consistent)
  and versioning (coexisting versions and their declared relations) - CTI analytics
  is a versioning problem that the field treats as an evolution problem.
---

## What it is

Klein and Fensel's line of work on ontology versioning, exemplified by "Change Management: The Core Task of Ontology Versioning and Evolution" (widely circulated via ResearchGate) and the related literature on multiple-version ontology management. Foundational knowledge-engineering framing from the early Semantic Web period.

## Concept/mechanism it contributes

Three distinctions the manuscript should adopt as vocabulary rather than re-derive:

1. **Ontology evolution vs ontology versioning.** Evolution is the process of changing the ontology while keeping it consistent; versioning is the problem of *coexisting* versions and the relations between them. A CTI paper that says "we used a newer ATT&CK version" is treating a versioning problem as if it were an evolution problem — it assumes the old analysis is simply superseded, when in fact both versions remain in use across the ecosystem (vendor mappings, published benchmarks, historical reports) and the relation between them is what needs stating.
2. **Change as the unit of management.** The literature's position is that change management — identifying, characterising and propagating changes — is the core task, not diffing per se. Managing change means knowing, for each change, its effect on (a) logical consistency of the ontology, (b) instance data annotated against it, and (c) applications built on it. The manuscript's contribution sits in (b) and (c) for CTI.
3. **Compatibility as a declared relation.** Multiple-version management includes explicitly recording whether a new version is backward compatible with an old one, and specifying transformation rules between versions. This is a *published assertion by the maintainer*, not something each consumer re-derives.

The broader framing in this literature (Noy & Klein; Stojanovic) also covers ontology libraries, importing/reusing, merging, aligning and mapping between versions — the full task list that "multiple-ontology management" comprises.

## Mapping onto ATT&CK

- ATT&CK releases make no compatibility declaration. There is no ATT&CK statement of the form "v15 is backward compatible with v14 except for the following N techniques". MITRE publishes changelogs (and ships diffStix to generate them) but a changelog is an enumeration of changes, not a compatibility assertion with defined semantics. Proposing that ATT&CK releases carry a machine-readable compatibility declaration is a concrete, literature-grounded recommendation.
- The evolution/versioning distinction gives the manuscript its sharpest normative claim: because multiple ATT&CK versions coexist in the CTI ecosystem simultaneously, CTI analytics is inherently a *versioning* problem, and every cross-corpus comparison is implicitly an inter-version mapping whether or not the authors acknowledge it.
- The three impact channels (consistency / instance data / applications) map onto the manuscript's three victim classes: ontology consistency ≈ dangling revoked references in STIX bundles; instance data ≈ CTI benchmark and training-set labels; applications ≈ detection and mitigation coverage claims and attribution pipelines.

## Fidelity

Summary fidelity, and weaker than most notes in this batch. The ResearchGate entry and the related PDFs could not be fetched (egress proxy 403), so this note reconstructs the well-established conceptual framing from search-result snippets and general familiarity with the Klein/Fensel/Noy/Stojanovic ontology-versioning literature. No verbatim quotation is asserted, no page numbers or specific claims are attributed. Before citing, obtain the actual papers and pin the distinctions to specific sources — the evolution-vs-versioning distinction in particular is stated across several papers and the manuscript should cite the canonical one (likely Klein & Fensel, "Ontology versioning on the Semantic Web", SWWS 2001) rather than this entry.
