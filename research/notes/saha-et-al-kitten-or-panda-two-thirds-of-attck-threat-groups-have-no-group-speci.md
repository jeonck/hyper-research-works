---
title: Saha et al. — Kitten or Panda? Two-thirds of ATT&CK threat groups have no group-specific
  behaviour
id: saha-et-al-kitten-or-panda-two-thirds-of-attck-threat-groups-have-no-group-speci
tags:
- attack-ontology-drift-cti-85bc51
- critique
- rebuttal
created: '2026-09-12T13:23:56.333010Z'
source: https://arxiv.org/abs/2506.10645
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Only 34% of ATT&CK groups (24% in Malpedia) have any group-specific technique
  — TTP attribution is non-identifiable for most groups within a single version, before
  drift enters.
---

## What it is
Saha, Lindorfer, Caballero — "Kitten or Panda? Measuring the Specificity of Threat Group Behaviors in Public CTI Knowledge Bases", ACM ASIA CCS 2026 (arXiv 2506.10645, DOI 10.1145/3779208.3786258). Systematic measurement of threat-group behavioural profiles built from MITRE ATT&CK and Malpedia.

## The criticism it makes
TTP-based threat-actor attribution rests on an assumption that the data does not support: that groups have *distinguishing* behaviours. Headline findings (from the abstract and search-surfaced summary; I could not fetch the full text):
- Only **34%** of threat groups in ATT&CK have any group-specific technique — i.e. ~two-thirds of groups share their entire technique set with at least one other group, so techniques cannot serve as a behavioural signature for them.
- In the broader Malpedia dataset the figure drops to **24%**.
- Combining both sources improves coverage only modestly; the proportion of groups with group-specific behaviours stays **under 30%**, and even after adding exploited vulnerabilities and techniques extracted from threat reports, **64% of groups still lack any group-specific behaviour**.
- Conclusion: caution is required when using these profiles for threat-group attribution.

## Strength of evidence
Strong — peer-reviewed at a top-tier venue, measurement over two large public knowledge bases, headline numbers are concrete and falsifiable.

## For or against the thesis
**This is the single most damaging paper to the thesis's framing, and it is not a version-drift paper at all.** It shows that TTP-based attribution is already near-useless for ~two-thirds of tracked groups **at a single point in time, within one version of the knowledge base**. If technique profiles are non-discriminative *before* any drift is applied, then showing that drift further perturbs those profiles is showing that a broken instrument also wobbles. The referee's question writes itself: *what is the marginal effect size of ontology drift on attribution accuracy, conditional on the 66% of groups for which attribution was never identifiable?*

Three consequences the thesis must absorb:
1. Any "drift degrades attribution" experiment must **stratify by group specificity** — measure the drift effect on the 34% identifiable subset separately, or the aggregate effect is dominated by groups that were never attributable.
2. Conversely, this paper is a gift if reframed: group profiles are *sparse and fragile*, so adding or revoking a handful of techniques can flip a group in or out of the identifiable set. Quantifying **how much of the 34%/24% specificity figure is itself version-dependent** — i.e. recomputing Saha et al.'s metric across v8…v19 — would be a genuinely new, publishable result that this paper does not report (it appears to use a single snapshot).
3. It independently corroborates that the *knowledge base*, not just the analytics, is the weak link — which supports the broader "CTI knowledge-base quality" agenda even while undercutting the drift-specific claim.

## Fidelity
Medium-high. Abstract-level findings only; the percentages come from the arXiv abstract as surfaced by search, not from the full PDF (egress blocked). The ASIA CCS'26 venue and author list are confirmed from multiple independent listings. I have NOT verified whether the paper reports which ATT&CK version it used.
