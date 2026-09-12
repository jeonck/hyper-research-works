---
title: 'ATT&CK Design and Philosophy: inclusion criteria are explicitly non-stationary
  and abstraction level is an interpretive standard'
id: attck-design-and-philosophy-inclusion-criteria-are-explicitly-non-stationary-and
tags:
- attack-ontology-drift-cti-85bc51
- attack-versioning
created: '2026-09-12T13:24:45.535458Z'
source: https://attack.mitre.org/docs/ATTACK_Design_and_Philosophy_March_2020.pdf
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: MITRE documents that its criteria for adding information have changed as
  scope expanded, that sub-technique goals are abstraction harmonisation and count
  management, and that technique abstraction is an interpretive standard - so ATT&CK
  is a non-stationary measuring instrument by design.
---

## What this source is
**MITRE ATT&CK: Design and Philosophy** (Strom, Applebaum et al.), March 2020 revision — the foundational methodology paper describing how ATT&CK objects are scoped, abstracted and maintained. Published at `attack.mitre.org/docs/ATTACK_Design_and_Philosophy_March_2020.pdf`; MITRE's `USAGE.md` explicitly recommends reading it for the "high-level overall approach, intention, and usage of ATT&CK".

## What it establishes (search-summary-derived)
- **Stated goals for sub-techniques**: "making the abstraction level of techniques similar across the knowledge base, reducing the number of techniques to a manageable level, and providing a structure to allow sub-techniques to be added easily."
- **Scope criteria evolve with the framework**: "As the scope of ATT&CK has expanded and been refined, so too have the criteria necessary to add information." Techniques "represent the individual actions adversaries make or pieces of information the adversary learns by performing an action."
- **Abstraction level is the defining design choice**: technique names focus on "the aspect of the technique that makes it unique", at "an intermediate level of abstraction", and the paper frames abstraction level as "an important distinction between it and other types of threat models."
- **Structural constraint on sub-techniques**: each sub-technique "will only have a relationship to a single parent technique and no other, to avoid complicated and difficult to maintain relationships across the model."

## Claims worth citing
- **MITRE documents that its own inclusion criteria change over time.** This is the single most important admission for the research query: if the criteria for what counts as a technique are themselves non-stationary, then **the ATT&CK catalogue is not a stable measuring instrument**, and longitudinal counts over it measure a moving definition as much as a moving threat landscape. Drift is not accidental maintenance debt; it is a designed property.
- **The sub-technique goals are explicitly bookkeeping goals** — abstraction harmonisation and count management — which is the institutional warrant for scoring the v7.0 expansion (266 → 428 active techniques, of which 120 new IDs are direct re-identifications and only 30 are new top-level concepts) as ontology work rather than intelligence accrual.
- **The single-parent constraint is a design trade-off with drift consequences.** Because a sub-technique may attach to exactly one parent, a behaviour spanning two parents must be duplicated or re-parented — and re-parenting is precisely what v19 did to the T1562 family (reissued under T1685/T1686/T1688/T1689/T1690). The constraint that keeps the model maintainable is the same constraint that forces ID churn when abstraction judgements are revised.
- **"Intermediate level of abstraction" is an explicitly interpretive standard**, not an operational test. Two curators can disagree, and the record shows MITRE revising its own judgements. This undercuts any treatment of ATT&CK labels as ground truth in the strict sense — relevant for CTI benchmarks that score model outputs against ATT&CK IDs as if they were objective classes.

## Bearing on the research query
Provides the theoretical grounding: it establishes from the publisher's own methodology document that ATT&CK is a curated, evolving model with acknowledged mutable inclusion criteria and an interpretive abstraction standard. That reframes "ontology drift" from a data-hygiene nuisance into a **validity threat inherent to the instrument** — which is the argument an SCI-level contribution needs in order to claim that drift-blind CTI analytics are not merely imprecise but measuring a non-stationary construct. It also directly supports treating ATT&CK labels as *curatorial judgements with version-dependent semantics* rather than as stable classes.

## Fidelity
**Search-summary-derived.** The egress proxy blocks attack.mitre.org and mitre.org, so I could not read the PDF in full. All phrases in quotation marks are as rendered in search-result content summaries of the paper and **must be re-verified against the PDF before being quoted in a manuscript** — this is a foundational citation where quotation accuracy matters and where page numbers will be required. Note also that the March 2020 revision predates v7 sub-technique release and every subsequent restructuring; a gap-filling pass should check whether a later revision exists. The ATT&CK population figures cited for contrast are my own primary-artefact computations and are exact.
