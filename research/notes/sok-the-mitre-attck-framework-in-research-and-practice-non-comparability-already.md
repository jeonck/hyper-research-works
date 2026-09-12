---
title: 'SoK: The MITRE ATT&CK Framework in Research and Practice — non-comparability
  already established, temporal instability not'
id: sok-the-mitre-attck-framework-in-research-and-practice-non-comparability-already
tags:
- attack-ontology-drift-cti-85bc51
- critique
created: '2026-09-12T13:23:56.861949Z'
source: https://arxiv.org/abs/2304.07411
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Canonical SoK finds no standardization in how products implement ATT&CK and
  discrepancies across the literature — occupying the non-comparability slot synchronically
  and raising the novelty bar for a drift paper.
---

## What it is
Roy, Panaousis, Noakes, Laszka, Panda, Loukas — "SoK: The MITRE ATT&CK Framework in Research and Practice" (arXiv 2304.07411, 2023). The first systematization of the research literature on ATT&CK: a taxonomic classification of papers using ATT&CK, an assessment of its usefulness per application area, and identification of gaps and discrepancies.

## The criticism it makes
- There was (as of 2023) **no systematic review** of how ATT&CK is used, and the literature contains **gaps and discrepancies** — i.e. papers using ATT&CK for incompatible purposes with incompatible assumptions.
- **There is no standardization in how cybersecurity products implement ATT&CK.** Vendors evaluate their own capabilities against ATT&CK with no common convention, so "ATT&CK coverage" numbers from two products are not comparable quantities.
- Calls for more research on the practical implementation and evaluation of ATT&CK.

## Strength of evidence
High as a survey of the field's state; it is a secondary/aggregating source, so its force is agenda-setting rather than measurement. Widely cited and it recurs as the canonical reference in almost every ATT&CK-related search I ran.

## For or against the thesis
**Mixed, leaning for — but it also pre-empts part of the thesis's novelty claim.**

*For:* "no standardization in how products implement ATT&CK" is the non-comparability claim, already established at SoK level. It gives the thesis its motivating premise for free.

*Against (novelty risk):* because this SoK already occupies the "ATT&CK-based analytics are not comparable and the literature is inconsistent" slot, an SCI-level contribution cannot simply re-assert it. To clear the bar the new work must add what the SoK does not have: a **longitudinal, version-resolved measurement**. The SoK is synchronic and qualitative — it catalogues papers, it does not recompute any analytic across ATT&CK versions or report an effect size. That gap is the thesis's opening, but it also means the thesis is judged on whether it delivers *numbers*, not on whether it re-motivates the problem.

*Also against, subtly:* the SoK frames the problem as **implementation heterogeneity across vendors and papers**, not as **temporal instability of the ontology**. A reviewer steeped in this SoK will default to "the known problem is that everyone maps differently" and will need to be argued, with data, into "and separately, the target moves." Batch-B4 conclusion: the thesis must show drift variance is **additive to, and separable from,** the implementation-heterogeneity variance the SoK already documented.

## Fidelity
Medium. Abstract- and summary-level; I could not fetch the PDF (egress blocked) and have not read the section on gaps. Claims above are drawn from the abstract and from search-surfaced summaries. https://arxiv.org/abs/2304.07411
