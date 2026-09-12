---
title: '''ATT&CK is an ontology, not a taxonomy'' — the definitional defence and the
  ontology-evolution prior-art objection'
id: attck-is-an-ontology-not-a-taxonomy-the-definitional-defence-and-the-ontology-ev
tags:
- attack-ontology-drift-cti-85bc51
- critique
- rebuttal
created: '2026-09-12T13:25:12.878031Z'
source: https://www.tripwire.com/state-of-security/attck-structure-ontology
status: draft
type: note
tier: practitioner
content_type: blog
deprecated: false
summary: If ATT&CK is an ontology then evolution is expected and ontology-versioning
  research already covers it; the counter is that ATT&CK's change contract (revoked-by
  + deprecated flag) is far weaker than OWL's.
---

## What it is
Two-part practitioner essay by Tripwire's State of Security: "ATT&CK Structure Part I: A Taxonomy of Adversarial Behavior" and "ATT&CK Structure Part II: From Taxonomy to Ontology." The standard reference articulating what kind of knowledge-representation artefact ATT&CK actually is. Adjacent scholarly anchors: "The Design of an Ontology for ATT&CK and its Application to Cybersecurity" (ACM CODASPY 2023, DOI 10.1145/3577923.3585051) and "Rethinking Cybersecurity Ontology Classification and Evaluation: Towards a Credibility-Centered Framework" (arXiv 2512.01651, Springer 2025).

## The argument it makes — and it is a defence, not an attack
Against the common critique that "ATT&CK is not a proper taxonomy" (techniques are not mutually exclusive, the hierarchy is shallow and inconsistent, category membership is ad hoc), the Tripwire position is that the critique **targets the wrong object**: ATT&CK is a *burgeoning formal ontology*, not a taxonomy. The distinguishing claim is that *where a taxonomy classifies, an ontology specifies* — ATT&CK declares entities (techniques, tactics, groups, software, mitigations, data sources, campaigns) and precisely typed interrelationships among them, which is strictly more than hierarchical classification. The CODASPY paper takes the complementary path of formalising ATT&CK *as* an OWL ontology, implicitly conceding that the native representation is not formal but demonstrating that it is formalisable. arXiv 2512.01651 argues that cybersecurity-ontology proliferation is driven not by technical quality deficits but by a **credibility deficit** — trust, endorsement, institutional support, practitioner validation, industrial adoption — and proposes credibility indicators for selecting among ontologies.

## Strength of evidence
Weak-to-moderate as evidence: the Tripwire pieces are argued essays by a vendor, not measurements. The CODASPY paper is peer-reviewed but is a construction, not an evaluation of ATT&CK's native consistency. arXiv 2512.01651 is peer-reviewed (Springer chapter) and reframes the evaluation criteria rather than measuring ATT&CK.

## For or against the thesis
**Against, on a definitional flank that is easy to lose.**

If ATT&CK is an ontology rather than a taxonomy, then **change is a feature of the artefact class, not a defect**. Ontologies are expected to evolve; the ontology-engineering literature has mature machinery for exactly this (versioned ontologies, `owl:deprecated`, `owl:equivalentClass`/`owl:sameAs` mappings, ontology-matching and ontology-evolution research going back two decades). A referee can say: "the author has rediscovered ontology evolution, a solved problem with a 20-year literature, and named it ontology drift." That is a survivable but genuine hit.

The thesis's defensible replies, and it should make them explicitly:
1. ATT&CK's change contract is **weaker than OWL's**. It has `revoked-by` (1:1 replacement) and a deprecation boolean, but no equivalence, no subsumption change record, no 1:N split/merge relation, and no machine-readable statement of *semantic* compatibility. So the ontology-evolution toolkit cannot actually be applied to ATT&CK as published.
2. The credibility framing of arXiv 2512.01651 is a double-edged gift: ATT&CK scores maximally on credibility indicators (institutional support, adoption, practitioner validation) while its *technical* stability properties go unmeasured — which is precisely the reason nobody checks, and a good motivation for a stability audit.
3. The taxonomy-vs-ontology argument cuts against a different critique than the thesis's. The thesis does not need techniques to be mutually exclusive; it needs identifiers to denote stable concepts across time. "It's an ontology" does not grant that.

## Fidelity
Low-to-medium. The "where a taxonomy classifies, an ontology specifies" formulation and the "burgeoning formal ontology" phrasing were surfaced by web search from the Tripwire pieces; I could not fetch the articles (egress blocked) and so cannot guarantee they are verbatim from the published text. The CODASPY and Springer/arXiv items are cited at abstract fidelity only.
