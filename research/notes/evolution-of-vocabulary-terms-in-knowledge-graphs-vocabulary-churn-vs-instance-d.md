---
title: 'Evolution of vocabulary terms in knowledge graphs: vocabulary churn vs instance-data
  usage as two time series'
id: evolution-of-vocabulary-terms-in-knowledge-graphs-vocabulary-churn-vs-instance-d
tags:
- attack-ontology-drift-cti-85bc51
- ontology-versioning
created: '2026-09-12T13:24:04.826700Z'
source: https://arxiv.org/pdf/1710.00232
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Framing for measuring the lag between a term's deprecation in the vocabulary
  and its disappearance from deployed data - the design for measuring how long revoked
  ATT&CK techniques persist in published CTI corpora.
---

## What it is

"Towards Understanding the Evolution of Vocabulary Terms in Knowledge Graphs" (arXiv 1710.00232). An empirical study of how vocabulary terms (classes and properties) in Linked Data vocabularies change over time and what that does to the data described by them.

## Concept/mechanism it contributes

The measurement framing the manuscript needs for its "how much of the growth is real?" question. Rather than treating a vocabulary as a static schema, this line of work treats term-level change as the object of measurement: which terms are added, which fall out of use, which are deprecated, how the *usage* of terms in instance data tracks (or fails to track) changes in the vocabulary itself, and how long deprecated terms persist in deployed data after deprecation.

Two transferable ideas:

1. **Vocabulary change and data change are different time series.** A term can be deprecated in the vocabulary years before instance data stops using it. Measuring only the vocabulary understates the real cost of drift; measuring only the data misses drift that has been announced but not yet absorbed. The gap between the two is itself the quantity of interest.
2. **Term-level churn as a maintenance signal.** Counting per-release term additions, removals and deprecations gives a churn profile that distinguishes vocabularies in active conceptual expansion from those undergoing structural reorganisation — which is exactly the discrimination the manuscript's "genuine intelligence vs bookkeeping" question requires.

## Mapping onto ATT&CK

- The two-time-series idea is the design for the manuscript's most quotable result. Series A: ATT&CK's own per-release technique churn (additions, revocations, deprecations, splits). Series B: the technique IDs actually appearing in published CTI corpora, benchmarks, vendor coverage matrices and threat reports, over the same calendar period. The *lag* between a technique being revoked and its disappearance from downstream usage — and the residual population of never-migrated corpora — is a direct, defensible measure of drift's real-world cost, and it is a measurement nobody appears to have made for ATT&CK.
- Churn profiling gives a principled way to phrase the bookkeeping fraction: for each release, partition new technique IDs into (i) IDs whose content originates in a pre-existing technique (split/reorganisation products, identifiable via the revocation graph and description overlap) and (ii) IDs with no antecedent (genuine new adversary behaviour). The ratio, plotted per release, is the headline figure.
- Caveat to state: ATT&CK sub-techniques inflate the raw term count by construction. A count of "techniques" that mixes techniques and sub-techniques across the v6/v7 boundary is not a time series of the same quantity, and the manuscript must normalize the counting unit before plotting anything.

## Fidelity

Summary fidelity, and thin. arXiv could not be fetched (egress proxy 403); this note is built from the paper's title and a search-result snippet, plus general familiarity with the Linked Data vocabulary-evolution literature. The specific measurements the paper reports are not known to me and are not asserted here. The two transferable ideas above are stated as framings the manuscript can use, not as findings attributed to this paper. Obtain the full text before citing it for any empirical claim.
