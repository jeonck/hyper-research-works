---
title: 'Practitioner critique cluster: ATT&CK coverage percentages were never a valid
  metric, drift or no drift'
id: practitioner-critique-cluster-attck-coverage-percentages-were-never-a-valid-metr
tags:
- attack-ontology-drift-cti-85bc51
- critique
- rebuttal
created: '2026-09-12T13:26:31.866608Z'
source: https://www.attackiq.com/2026/03/10/what-does-mitre-attack-coverage-really-mean/
status: draft
type: note
tier: practitioner
content_type: blog
deprecated: false
summary: Vendor '100% coverage' claims, T1059-style granularity, unrealizable techniques
  and no severity weighting make coverage uninformative within any single version
  — weakening the drift thesis's coverage leg.
---

## What it is
The practitioner critique cluster on ATT&CK **coverage** as a metric: AttackIQ / Security Boulevard "What Does MITRE ATT&CK Coverage Really Mean?" (March 2026), ReliaQuest "Measuring Detection Coverage with MITRE ATT&CK", TeckPath "MITRE ATT&CK: Relevance, Criticism...", Cyderes "Limitations of the MITRE ATT&CK Framework for Modern Defense", and Elastic/CSA coverage guidance.

## The criticism it makes
A consolidated list of the standing practitioner objections to ATT&CK:
- **"100% ATT&CK coverage" vendor claims are misleading**; no tool reliably detects all techniques, and coverage claims without context are a persistent source of confusion.
- **Technique granularity makes coverage meaningless.** Claiming coverage of a broad technique such as T1059 (Command and Scripting Interpreter), which is overwhelmingly used for legitimate purposes, says nearly nothing.
- **Reactive by design** — ATT&CK documents observed behaviour, so it cannot model or predict novel attacks.
- **Checklist mentality / false sense of security**; coverage counts are optimised rather than risk.
- **No prioritization**: ATT&CK does not tell you which techniques matter for your industry or threat model.
- **Limited mitigation guidance** beyond high-level suggestions; **detection efficacy varies wildly** by technique; poor fit for non-linear or cross-vector attack chains; hundreds of techniques make adoption hard.
- Counter-guidance from the same cluster: prefer a focused 40-60 technique coverage map over a scattered 200-technique one; let threat intelligence, not technique count, drive prioritization; use DeTT&CT to make coverage measurable.

## Strength of evidence
Low-to-moderate individually — vendor blogs, partly marketing-adjacent, with unsourced numbers. Moderate in aggregate: these objections recur consistently across independent vendors and align with the peer-reviewed finding (Virkud et al., USENIX Sec 2024) that many techniques are unrealizable as detection rules and that coverage does not imply real-world threat coverage.

## For or against the thesis
**Against the "coverage claims" leg of the thesis specifically.**

The thesis treats detection/mitigation coverage claims as a victim of ontology drift — coverage percentages become incomparable across versions because the denominator (technique count) and the partition both move. The practitioner consensus is that **coverage percentages were never meaningful in the first place**, for reasons entirely independent of versioning: wrong granularity, unrealizable techniques, no severity weighting, no threat-model weighting, vendor incentive to inflate. If the metric is already not a valid measurement of security posture at any single version, then demonstrating that it is *also* not comparable across versions is a minor addition — you cannot corrupt a number that carries no information.

The thesis's viable response, which should be stated explicitly rather than assumed: even a *relative*, self-consistent coverage series (an organization comparing itself to itself over time) is broken by drift, and that self-comparison is the one use of the metric that practitioners do defend. Showing that the denominator shift alone can manufacture an apparent year-over-year coverage gain or loss — with no change in detection capability whatsoever — would be a concrete, falsifiable, and genuinely damaging result. Without that specific demonstration, this leg of the thesis is the easiest one for a reviewer to dismiss.

*Small point for the thesis:* "prefer a focused 40-60 technique map" is itself advice that guarantees drift sensitivity, since a small hand-picked technique set is far more likely to be materially disrupted by a handful of revocations or a sub-technique split than a full-matrix map.

## Fidelity
Low-to-medium. All content is from web-search summaries of practitioner blogs; I could not fetch the pages (egress blocked). The "coverage drops to 25-26% when filtering low/medium-risk rules" figure appears in this cluster attributed to academic work (probably Virkud et al.) and is unverified here. Treat every number in this note as summary fidelity.
