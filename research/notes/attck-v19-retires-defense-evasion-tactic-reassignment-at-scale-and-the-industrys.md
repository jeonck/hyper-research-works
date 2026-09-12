---
title: 'ATT&CK v19 retires Defense Evasion: tactic reassignment at scale, and the
  industry''s rapid-migration rebuttal'
id: attck-v19-retires-defense-evasion-tactic-reassignment-at-scale-and-the-industrys
tags:
- attack-ontology-drift-cti-85bc51
- critique
created: '2026-09-12T13:26:31.615257Z'
source: https://medium.com/mitre-attack/attack-v19-ff329cb65d66
status: draft
type: note
tier: practitioner
content_type: blog
deprecated: false
summary: v19 (28 Apr 2026) split TA0005 Defense Evasion into Stealth and Defense Impairment
  (TA0112), forcing rule remapping — a 1:N semantic re-cut revoked-by cannot express,
  yet absorbed by vendors within days.
---

## What it is
The industry response to **ATT&CK v19 (released 28 April 2026)**, which retired the long-standing **Defense Evasion (TA0005)** tactic and replaced it with two tactics — **Stealth** and **Defense Impairment (TA0112)**. Sources span MITRE's own announcement (Amy L. Robertson, "ATT&CK v19: The Defense Evasion Split...", MITRE ATT&CK Medium), vendor migration guides (D3 Security, Cymulate, SCYTHE, Deceptive Bytes, Hive Security, nhimg) and tool documentation (Elastic's "Remap detection rules to MITRE ATT&CK v19").

## What it demonstrates
This is the cleanest available natural experiment in tactic reassignment at scale:
- Most former Defense Evasion techniques moved into Stealth or Defense Impairment; new techniques (reported as T1684 and sub-techniques, T1685, T1686.003, T1687) and the new tactic TA0112 appeared.
- Elastic published explicit instructions to **remap detection rules**, i.e. every rule tagged `defense-evasion` in a customer deployment needed re-tagging.
- The conceptual boundary is semantic, not cosmetic: Stealth = blending in (masquerading, hiding artifacts); Defense Impairment = degrading/disabling/tampering with controls. Practitioner guidance stresses these warrant *different responses* — investigate quietly vs. treat as an active attack in progress.
- Pointed practitioner observation (D3): *"If your Defense Evasion detections were already broken or noisy, remapping them to Stealth and Defense Impairment gives you broken detections in two buckets instead of one."*

## Strength of evidence
High that the change happened and was disruptive (MITRE's own blog plus many independent vendor write-ups and a major SIEM vendor shipping remapping documentation). Low as *measurement*: nobody in this source set quantifies how many techniques moved, how many existing rules were invalidated, or what happened to longitudinal coverage metrics across the boundary.

## For or against the thesis
**The strongest single piece of evidence FOR the thesis, and simultaneously the clearest demonstration of the rebuttal.**

*For:* tactic reassignment is not a long-tail bookkeeping event. Defense Evasion was one of the most heavily populated and most frequently detected tactics in Enterprise ATT&CK. Any tactic-level time series — "our Defense Evasion coverage improved 12% this year," "this actor's Defense Evasion technique count," a benchmark whose labels include tactic strings — **discontinues at the v18/v19 boundary**. The identifier TA0005 does not merely change meaning; it ceases to have a referent while its successors partition its old extension along a new conceptual axis. `revoked-by` cannot express this: it is a 1:N split with a semantic re-cut, not a rename.

*Against:* the ecosystem absorbed it publicly, quickly and with documentation. MITRE pre-announced it, a half-dozen vendors published migration guides within days, Elastic shipped remapping instructions. A referee will say the community treats such changes as routine operational maintenance, which is evidence that drift is *managed*, not that it is *undetected*. The thesis's reply must be that operational remapping is not the same as **retrospective comparability**: nobody re-labelled the historical corpus, the published benchmarks, the training sets, or last year's coverage report. Forward migration was handled; the backward comparability of the existing scientific and evaluation record was not even attempted.

## Fidelity
Medium. The tactic split, date, and new-tactic/technique identifiers come from multiple independent vendor posts and MITRE's Medium announcement as surfaced by web search; I could not fetch any of these pages (egress blocked) and did not verify the technique IDs against a STIX bundle. The D3 "two buckets" line is a search-surfaced paraphrase and should not be quoted as verbatim without checking the original post.
