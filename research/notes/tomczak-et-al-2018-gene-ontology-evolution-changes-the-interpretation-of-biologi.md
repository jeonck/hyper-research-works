---
title: 'Tomczak et al. (2018): Gene Ontology evolution changes the interpretation
  of biological experiments'
id: tomczak-et-al-2018-gene-ontology-evolution-changes-the-interpretation-of-biologi
tags:
- attack-ontology-drift-cti-85bc51
- ontology-versioning
created: '2026-09-12T13:19:31.593789Z'
source: https://www.nature.com/articles/s41598-018-23395-2
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Canonical prior art: holding the pipeline fixed and sweeping GO versions
  shows enrichment conclusions are version-dependent - the direct methodological template
  for the ATT&CK drift experiment.'
---

## What it is

Tomczak et al., "Interpretation of biological experiments changes with evolution of the Gene Ontology and its annotations", *Scientific Reports* 8:5115 (2018). A longitudinal study of Gene Ontology (GO) releases and GO annotations from 2004-2015, re-running GO enrichment analysis on gene sets drawn from 104 multi-cohort meta-analyses spanning 92 human diseases and >23,000 samples, once per historical ontology version.

## Concept/mechanism it contributes

This is the single closest methodological precedent for the manuscript. It establishes the *experimental design* for measuring ontology drift's downstream impact: freeze the analytic pipeline and the input data, vary only the ontology version, and measure how much the *conclusions* move. Reported findings (at search-snippet fidelity): low consistency between enrichment results computed with early versus recent GO versions; p-values for enriched terms vary substantially across versions; and a persistent annotation bias in which roughly 58% of annotations attach to about 16% of human genes. The authors' recommendation — re-examine prior analyses against the current ontology, and provide version-aware tooling — is the "reporting discipline" half of the manuscript's contribution, already stated for a different domain.

Also relevant: the GO project's stated response was to publish the full history of term changes since 2005 and to build an enrichment tool that can analyse gene sets *at a specified point in time*. That is precisely a version-pinned analytics protocol.

## Mapping onto ATT&CK

GO term obsoletion/merging/splitting is isomorphic to ATT&CK deprecation/revocation/sub-technique restructuring; GO annotation churn (gene→term assertions) is isomorphic to ATT&CK's group/software→technique relationship churn, which is what TTP-based attribution actually consumes. The manuscript's "hold the pipeline fixed, sweep the ATT&CK version" experiment should be framed explicitly as the CTI analogue of this study, and the annotation-bias finding predicts an ATT&CK counterpart (a small set of techniques carrying a disproportionate share of group/software relationships), which is a directly testable secondary result.

Crucially, this paper is the prior art that makes the manuscript's *framing* unoriginal-if-unattributed: "ontology drift changes scientific conclusions" was demonstrated in 2018 for biology. The ATT&CK contribution must therefore be the CTI-specific mechanisms (revocation-with-successor, tactic reassignment, version-silent description rewriting) and the normalization protocol, not the general claim.

## Fidelity

Summary fidelity only. Egress proxy blocked direct fetch of nature.com, PMC and biorxiv; findings above are from search-result snippets plus the abstract as surfaced by search. No verbatim quotation is asserted. Numbers (104 analyses, 92 diseases, >23,000 samples, 58%/16% annotation bias, 2004-2015 window) should be re-verified against the PDF before citation.
