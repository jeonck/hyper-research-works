---
title: 'Multi-label ATT&CK classification (arXiv 2606.18166): TRAM annotations declared
  not-gold, best open LLM micro-F1 0.22'
id: multi-label-attck-classification-arxiv-260618166-tram-annotations-declared-not-g
tags:
- attack-ontology-drift-cti-85bc51
- cti-benchmarks
created: '2026-09-12T13:22:37.144448Z'
source: https://arxiv.org/abs/2606.18166
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Builds a 2,076-sentence / 83-report / 114-technique gold set at kappa 0.68
  after finding TRAM's annotations were never designed as gold and contain systematic
  over-annotation; best open-source LLM reaches only micro-F1 0.22, and its annotation
  rule makes official ATT&CK descriptions the sole label arbiter, hence release-dependent.
---

# Multi-label ATT&CK classification on complex CTI (arXiv:2606.18166) — the strongest label-quality critique

## What it is
*Evaluating Open-Source LLMs for Multi-Label ATT&CK Technique Classification on CTI Reports* (June 2026). Builds a purpose-made gold standard because the existing ones were judged unfit.

## What it says bearing on the query
**Critique of the incumbent labels.** The paper argues current CTI-classification evaluation relies on **simplified, single-technique sentences that ignore the complexity of real CTI reports, which inflates reported performance**. It states directly that the **TRAM dataset's annotations were not designed as a gold-standard evaluation benchmark**, and that review found two systematic classes of annotation error — notably **false positives / over-annotation**, where technique labels were attached to sentences describing generic system activity, reconnaissance context, or background narrative rather than a concrete attacker action.

**Its own construction protocol** is the closest thing in this literature to a reproducible labelling discipline:
- **2,076 human-annotated sentences** (1,281 technique-positive, 795 negative) from **83 complex unstructured CTI reports**.
- Mapped to **114 unique ATT&CK techniques**.
- **Six-phase annotation process**, inter-annotator agreement **κ = 0.68** (substantial).
- Annotators were **instructed to use the official MITRE ATT&CK technique descriptions as the sole reference** for deciding whether a label is warranted.

That last rule is the ontology-drift hinge: if the arbiter of a label is the *official technique description*, and ATT&CK silently rewrites those descriptions between releases, then the annotation function itself is release-dependent. The same sentence can be correctly labelled T-X under release N and correctly labelled not-T-X under release N+1, with no error by either annotator. Any gold standard built this way is only interpretable if it names the release — and the paper's abstract/snippets, as far as I could see, do not.

**Result.** Seven open-source LLMs, 8B–236B parameters, across prompt strategies and temperatures: best **micro-F1 = 0.22**. Parameter count correlated significantly and positively with F1; **prompt strategy and temperature gave no statistically significant gains**. Conclusion: open-source LLMs are insufficient for production-grade ATT&CK classification.

## Why this matters for positioning
It supplies the two things an SCI-level ontology-drift paper needs from the existing literature: (a) an explicit, citable finding that a widely used ATT&CK training/benchmark set (TRAM) has *systematic* annotation error and was never intended as gold, and (b) a demonstration that once you build a genuinely hard multi-label set, headline F1 collapses from the ~0.7–0.9 range reported on simplified sets to **0.22**. The drift argument extends this: even that 0.22 is version-conditional.

## Citable claims
- 2,076 annotated sentences (1,281 positive / 795 negative), 83 reports, 114 techniques, six-phase protocol, κ = 0.68.
- Best open-source LLM micro-F1 **0.22** across 7 models (8B–236B).
- Parameter size: significant positive correlation with F1. Prompt strategy and temperature: no significant effect.
- Explicit claim that **TRAM annotations were not designed as a gold-standard benchmark** and contain systematic over-annotation.
- Annotation rule: official ATT&CK technique descriptions used as the **sole** reference for label warrant.

## Fidelity
**Summary fidelity.** arxiv.org is egress-blocked; all of the above is reconstructed from search-result snippets of the abstract and body, not from the full text, and none of it is a verified verbatim quotation. Whether the paper names an ATT&CK release version is **unresolved** — I could not read the methods section to check.
