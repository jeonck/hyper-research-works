---
title: 'Boundary synthesis: where concept-drift literature stops and ontology drift
  begins'
id: boundary-synthesis-where-concept-drift-literature-stops-and-ontology-drift-begin
tags:
- attack-ontology-drift-cti-85bc51
- concept-drift
created: '2026-09-12T13:22:35.236564Z'
status: draft
type: note
tier: institutional
content_type: article
deprecated: false
summary: Five-tier map of what the surveyed literature lets change over time, showing
  that non-monotone curator-driven schema evolution and cross-version comparability
  are covered nowhere.
---

## What it is
Synthesis note for batch B6 (concept drift and temporal bias in security ML, experimental-design pitfalls, benchmark decay, evolving label spaces). Not a source note — a positioning statement derived from the eleven source notes tagged `concept-drift` in this run.

## The boundary, stated precisely
Sort the surveyed literature by *what is allowed to change over time*:

1. **P(X) and P(Y|X) change; label space fixed.** Gama/Moreno-Torres/Lu taxonomies; Transcend/Transcendent; MORPH, ADAPT, NDSS-2025 Windows adaptation; TESSERACT (which fixes *when* samples may be drawn, not what labels mean). This is the overwhelming bulk of security drift work. It cannot express ontology drift: the standard shift vocabulary (covariate / prior-probability / concept shift) is defined over a fixed measurable space for Y, so when the class set changes the source and target distributions live on different spaces and no divergence between them is even well-typed.

2. **Label space grows; existing classes stable.** Class-incremental learning; CADE (new-class *discovery* from data). Covers ATT&CK technique **additions** only, and only when accompanied by new observations.

3. **Label space refines: coarse to fine.** LECO (NeurIPS 2022) — the only surveyed work whose explicit subject is the ontology changing between time periods, with real dataset instances (COCO→LVIS, Mapillary 1.2→2.0). Covers ATT&CK **sub-technique restructuring** structurally, but treats it as a training problem (annotate new vs relabel old), is monotone and structure-preserving, and asks nothing about cross-version comparability of published results.

4. **Answer key decays while items stay fixed.** "When Benchmarks Age" (EACL 2026) with DDS/EMR/TAG. The right analogue for **silent rewriting** of technique descriptions and for stale gold labels in CTI benchmarks — but caused by the world moving, not by a curator revising a schema, and remedied heuristically by re-retrieval rather than by an authoritative migration map.

5. **Label vocabulary is fragmented and open at a single moment.** AVClass (normalization + alias resolution + voting), MOTIF (measured 47–62% agreement). Synchronic disagreement among labellers; no version axis, no deprecation semantics.

**Not covered anywhere in the surveyed corpus:** non-monotone, authoritative, curator-driven schema evolution — deprecation (class removed with no successor), revocation (class redirected to another existing class), merge, tactic reassignment (the parent changes while the leaf id persists), and in-place rewriting of a retained identifier's *intension*. Nor does any surveyed work ask the accounting question — what share of apparent knowledge-base growth is genuine new intelligence versus bookkeeping — or the comparability question — how to restate results published against version v so they can be compared with results published against version v'.

## Consequences for the manuscript
- Do **not** claim to invent label-space drift: LECO and CIL own the additive and refinement cases, and Arp et al. own "label inaccuracy". Claim the non-monotone, versioned, intension-changing case in a curated security knowledge base, and claim *measurement and comparability* rather than *continual training* as the object.
- The eleventh-pitfall framing (extending Arp et al.) plus the DDS/EMR/TAG-style metric framing (extending When Benchmarks Age) is the most defensible SCI-level shape: named drift operations, a computable per-operation decay metric over ATT&CK releases, a deterministic migration map exploiting ATT&CK's own published deprecated/revoked-by relations, and a demonstration that normalization *changes the ranking* of systems on an existing CTI benchmark.
- Strongest single sentence available for a related-work section: **concept drift is a change of probability measure over a fixed label space; ontology drift is a change of the label space itself, and is therefore logically prior to — not a subtype of — concept drift.**

## Fidelity
Synthesis of the eleven B6 source notes, every one of which is itself summary-level (full texts were unreachable: the egress proxy returns 403 for arXiv, USENIX, ACM and publisher hosts). No verbatim quotation anywhere in this batch. The "not covered anywhere" claim is scoped to the sources surveyed in this batch and should be treated as a hypothesis to be stress-tested against the ontology-evolution / semantic-web versioning literature, which was not in B6's scope.
