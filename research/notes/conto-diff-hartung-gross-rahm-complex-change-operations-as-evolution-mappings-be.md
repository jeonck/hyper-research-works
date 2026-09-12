---
title: 'COnto-Diff (Hartung, Gross, Rahm): complex change operations as evolution
  mappings between ontology versions'
id: conto-diff-hartung-gross-rahm-complex-change-operations-as-evolution-mappings-be
tags:
- attack-ontology-drift-cti-85bc51
- ontology-versioning
created: '2026-09-12T13:21:08.304294Z'
source: https://www.sciencedirect.com/science/article/pii/S1532046412000627
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Rule-based aggregation of basic inserts/deletes into complex merge/split/move
  operations - the published methodology for separating real growth from bookkeeping
  and for migrating annotations across versions.
---

## What it is

Hartung, Groß and Rahm, "COnto-Diff: generation of complex evolution mappings for life science ontologies", *Journal of Biomedical Informatics* (2013; ScienceDirect S1532046412000627). A rule-based algorithm that takes two versions of an ontology and produces an *evolution mapping* — not a raw textual diff, but a set of typed change operations.

## Concept/mechanism it contributes

The core idea is the two-level change model. A naive version comparison yields only **basic change operations** (insert / update / delete of terms, relationships and attributes). COnto-Diff applies transformation rules to aggregate these into a smaller set of **complex change operations** that describe what actually happened conceptually: `merge`, `split`, `move`/`substitute`, and changes affecting entire subgraphs. The result is compact, semantically meaningful, and — per the paper's framing — *invertible*, so the mapping can be used to migrate data forward or backward between versions.

Stated applications are version management and **annotation migration in collaborative curation**: given an evolution mapping, existing annotations made against the old version can be programmatically carried to the new one. Evaluation was on large life-science ontologies including the Gene Ontology and the NCI Thesaurus, compared against PromptDiff.

Related work from the same group extends this to the evolution of *mappings* between ontologies (i.e. the alignment itself drifts, not only the endpoints), and to measuring the impact of ontology evolution on semantic annotations.

## Mapping onto ATT&CK

This is the closest formal precedent for the manuscript's normalization machinery, and it means the manuscript must not present "classify ATT&CK changes into types" as a new idea.

- ATT&CK drift is expressible in exactly COnto-Diff's complex-change vocabulary: sub-technique restructuring is `split` (T1086 → T1059.001 and siblings) and sometimes `merge`; tactic reassignment is `move` (a change of the technique's position in the tactic partition); revocation-with-successor is `substitute`; deprecation-without-successor is `delete` at the conceptual level while the identifier persists.
- The distinction between basic and complex operations is the core of the manuscript's "genuine new intelligence vs ontology bookkeeping" measurement. A raw count of added ATT&CK objects is a count of *basic* operations and systematically overstates knowledge growth, because a single `split` manifests as N inserts plus one revocation. The bookkeeping fraction is, precisely, the share of basic operations that are absorbed into complex operations under the aggregation rules. Framing the measurement this way inherits a published, evaluated methodology instead of improvising a counting rule.
- "Annotation migration" is the CTI problem verbatim: CTI benchmark labels, training-set technique tags and threat-actor TTP profiles are annotations against a specific ATT&CK version, and the manuscript's crosswalk is an evolution mapping used to migrate them.
- Invertibility is the property to demand of the crosswalk. A forward-only mapping cannot re-express a modern labelled corpus in an older ontology, which is what is needed to compare against a legacy benchmark result.

## Fidelity

Summary fidelity. The ScienceDirect article and the Leipzig DBS copy could not be fetched (egress proxy 403). The description of the basic/complex change model, the merge/split/subgraph examples, the invertibility and annotation-migration framing, the GO and NCI Thesaurus evaluation, and the PromptDiff comparison are from search-result snippets and abstract text. No verbatim quotation is asserted; confirm the exact change-operation taxonomy against the paper before mapping it one-to-one onto ATT&CK.
