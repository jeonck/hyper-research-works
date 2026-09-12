---
title: Dataset shift and concept drift taxonomies (Gama, Moreno-Torres, Lu et al.)
id: dataset-shift-and-concept-drift-taxonomies-gama-moreno-torres-lu-et-al
tags:
- attack-ontology-drift-cti-85bc51
- concept-drift
created: '2026-09-12T13:20:38.144831Z'
source: https://dl.acm.org/doi/10.1145/2523813
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Covariate, prior-probability and concept shift are all defined over a fixed
  label space, so the standard drift formalism cannot even express a change in the
  class vocabulary.
---

## What it is
The foundational formal vocabulary for drift, from mainstream ML rather than security:
- Gama, Žliobaitė, Bifet, Pechenizkiy, Bouchachia — "A Survey on Concept Drift Adaptation", ACM Computing Surveys 46(4), 2014 (doi 10.1145/2523813).
- Moreno-Torres, Raeder, Alaiz-Rodríguez, Chawla, Herrera (2012) — the unifying view of *dataset shift*.
- Lu, Liu, Dong, Gu, Gama, Zhang — "Learning under Concept Drift: A Review" (arXiv:2004.05785).

## Core claim
"Dataset shift" is the umbrella; concept drift is one species of it. The standard decomposition of a change from source to target distribution:
- **Covariate shift** — P(X) changes, P(Y|X) stable.
- **Prior probability shift** — P(Y) changes, P(X|Y) stable.
- **Concept shift / real concept drift** — P(Y|X) changes (the decision function itself moves), with or without visible change in P(X).
Plus the orthogonal distinction between *real* drift (P(Y|X) moves, performance degrades) and *virtual* drift (only P(X) moves). Gama et al. organise adaptation methods — drift detectors, windowing, ensembles, forgetting mechanisms — around this decomposition and around supervised settings where true labels eventually arrive.

## Relation to ontology drift (label-space vs feature-space)
**This is where the boundary is formally located, and it is a boundary of the formalism itself.** Every term in the taxonomy — P(X), P(Y), P(Y|X), P(X|Y) — is defined over a **fixed measurable space for Y**. The taxonomy can express "the probabilities attached to the classes changed"; it has no way to express "the set of classes changed". Prior probability shift is the nearest term and is routinely mis-invoked for this situation, but it is not the same thing: prior shift moves mass *among a fixed set of classes*, whereas ontology drift alters the set, so the source and target distributions are not even defined over a common sample space and no divergence between them is computable without an explicit alignment map first.

That is the sharpest available formulation of the manuscript's gap: **concept drift is a change of probability measure over a fixed label space; ontology drift is a change of the label space itself, which makes the concept-drift formalism inapplicable until a migration map restores a common space.** Ontology drift is therefore logically *prior* to concept drift, not a subtype of it.

## Why it matters for this manuscript
Gives the manuscript a rigorous, citable formal statement of non-coverage instead of a rhetorical one, and supplies the normalization protocol's justification: the map from version-v labels to a canonical reference vocabulary is precisely the object that must exist before any concept-drift statistic (or any cross-version accuracy comparison) is even well-typed.

## Fidelity
Summary-level only. The shift taxonomy (covariate / prior probability / concept shift, real vs virtual drift) is reported from search-result summaries plus standard knowledge of these widely cited surveys; none of the three full texts was retrievable (egress proxy 403). The measure-theoretic argument about fixed sample spaces is my own analytic framing, not a claim made by these authors. No verbatim quotation given.
