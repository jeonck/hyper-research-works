---
title: The CTI Echo Chamber — vendor fragmentation as the confounder the drift thesis
  must separate
id: the-cti-echo-chamber-vendor-fragmentation-as-the-confounder-the-drift-thesis-mus
tags:
- attack-ontology-drift-cti-85bc51
- critique
- rebuttal
created: '2026-09-12T13:23:56.599021Z'
source: https://arxiv.org/abs/2602.17458
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: '13,308 reports over 20 years: 88% niche vendors, siloed geographic/sectoral
  bias, low inter-vendor overlap, TTPs reported rarely and by few — source-composition
  drift is a third term the genuine-vs-bookkeeping split omits.'
---

## What it is
"The CTI Echo Chamber: Fragmentation, Overlap, and Vendor Specificity in Twenty Years of Cyber Threat Reporting" (arXiv 2602.17458, submitted 19 February 2026; authors from Universidad Carlos III de Madrid, University of Padova and others). Large-scale automated analysis of **13,308** open-source CTI reports spanning two decades, extracting attributed threat actors, motivations, victims, reporting vendors, IoCs and TTPs.

## The criticism it makes
The *input* to every ATT&CK-based analytic — the public CTI report corpus — is structurally biased, and the bias is large:
- The CTI market is a long-tail ecosystem: **88% of vendors are niche players**, with a small set of "super-vendors" producing the bulk of global, multi-actor intelligence.
- The ecosystem fragments into silos with significant **geographic and sectoral reporting bias** per vendor.
- **Inter-vendor overlap is typically low**; adding sources yields diminishing returns.
- **TTPs are reported significantly less often than IoCs, and by very few vendors.**

## Strength of evidence
Strong in scale (13k reports, 20 years) and directly on-point for the provenance of ATT&CK group/technique mappings, since ATT&CK group profiles are built from exactly this literature. Preprint, not yet peer-reviewed as far as I can tell. I read the abstract-level findings via search summary, not the full text.

## For or against the thesis
**Against, as a variance-decomposition argument — arguably the most quantitatively serious rebuttal in this batch.**

The thesis asks what fraction of apparent CTI knowledge-base growth is genuine adversary intelligence versus ontology bookkeeping. This paper implies the question is mis-specified, because there is a **third and probably larger term: source-composition drift**. ATT&CK group/technique entries are citations to vendor reports. If which vendors publish, about which regions and sectors, shifts over 20 years — and if TTPs are reported by only a few vendors — then year-over-year change in ATT&CK content reflects *who was writing*, not *what adversaries did* and not *how MITRE reorganised its schema*. A decomposition that offers only {genuine intelligence, bookkeeping} will attribute source-mix effects to one of those two buckets and be wrong.

It also weakens the practical stakes of drift: if TTP reporting is thin and vendor-siloed to begin with, the ATT&CK technique inventory is a low-resolution, biased sample of adversary behaviour in *any* single version. Comparability across versions is a modest concern relative to validity within a version.

**What the thesis can take from it:** the strongest version of the thesis is not "drift breaks CTI" but "CTI knowledge-base longitudinal series confound at least three drift processes — adversary drift, source/reporting drift, and ontology drift — and no published CTI analytic separates them." That framing survives this paper and uses it; it also connects cleanly to the concept-drift-in-security-ML literature, where the standard sin is exactly this confounding.

## Fidelity
Medium. Abstract/summary-level only; all figures (13,308 reports; 88% niche vendors) come from search-surfaced summaries of the arXiv listing, not from the PDF. https://arxiv.org/abs/2602.17458
