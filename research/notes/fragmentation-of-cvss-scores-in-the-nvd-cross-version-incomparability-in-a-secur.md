---
title: 'Fragmentation of CVSS scores in the NVD: cross-version incomparability in
  a security vocabulary'
id: fragmentation-of-cvss-scores-in-the-nvd-cross-version-incomparability-in-a-secur
tags:
- attack-ontology-drift-cti-85bc51
- ontology-versioning
created: '2026-09-12T13:23:17.021894Z'
source: https://www.sciencedirect.com/science/article/abs/pii/S0167404826001549
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Peer-reviewed census showing CVSS version choice systematically shifts severity
  classification across ~298k CVEs and that NVD/CNA scores disagree on 34.1% of dual-assessed
  entries - the security-domain precedent for the drift thesis, and the bar the ATT&CK
  paper must exceed by flipping a downstream conclusion.
---

## What it is

"Fragmentation of CVSS scores in the NVD: A quantitative analysis of inconsistency across vulnerability scoring standards", *Computers & Security* (ScienceDirect S0167404826001549, 2026). A large-scale empirical audit of scoring inconsistency in the NVD.

## Concept/mechanism it contributes

The closest existing security-domain study to what the manuscript proposes, but for a *scoring standard* rather than a *behavioural taxonomy*. Reported scale and findings (search-snippet fidelity): analysis of 297,780 CVE records and 506,653 metric entries covering CVSS v2.0, v3.0, v3.1 and v4.0; the conclusion that CVSS non-uniformity is systemic and limits long-term comparability, with the choice of CVSS version producing systematic shifts in severity classification; and that NVD and CNA scores disagree for 34.1% of dual-assessed CVEs.

Two mechanisms generalise directly:

1. **Standard-version shifts as a confound.** The same underlying vulnerability receives a materially different severity depending on which version of the scoring standard was applied. Any longitudinal claim about "severity trends" is partly an artefact of standard migration rather than of the threat landscape. This is the same logical structure as "growth in ATT&CK technique coverage" being partly an artefact of sub-technique restructuring.
2. **Partial coverage across versions.** Because v3 arrived in 2015, only a fraction of NVD entries carry v3 scores; analysts must either use v2 with its known limitations or restrict to a subset. The "restrict to the intersection where both encodings exist" manoeuvre is exactly the comparability trade-off the manuscript's normalization protocol faces when aligning pre- and post-sub-technique ATT&CK corpora.
3. **Multi-assessor disagreement.** The 34.1% NVD/CNA disagreement figure shows that even within a single release of a single standard, the *labels* are not a single authoritative signal. The CTI analogue is disagreement between MITRE's own group→technique assertions and vendor/report-derived technique tags.

## Mapping onto ATT&CK

- This paper is the strongest evidence that the manuscript's thesis is not idiosyncratic: a canonical security knowledge base has already been shown to be internally fragmented across versions of its own vocabulary, in a peer-reviewed venue. The ATT&CK contribution is the harder case, because ATT&CK drift changes the *identity and extension of concepts*, not merely the numeric value attached to a stable concept.
- It supplies a template for scale and framing: a census over the full corpus, quantified cross-version shift, and an explicit "limits long-term comparability" conclusion. An SCI-level ATT&CK paper should match this in corpus completeness (all releases, all domains) rather than sampling.
- It also sets the bar for what is *not* enough: showing that scores/labels differ is now an established genre. The differentiating move for the manuscript is demonstrating that a *downstream analytic conclusion* (an attribution ranking, a benchmark leaderboard order, a coverage percentage) flips under version substitution — the Tomczak-style design, which this CVSS paper does not appear to perform.

## Fidelity

Summary fidelity. The article is paywalled and ScienceDirect could not be fetched (egress proxy 403). All figures above (297,780 CVE records; 506,653 metric entries; 34.1% NVD/CNA disagreement; v2.0/v3.0/v3.1/v4.0 coverage) come from search-result snippets of the abstract and must be re-verified against the published paper before citation. No verbatim quotation is asserted, and the claim that the paper does not perform a downstream-conclusion-flip experiment is an inference from the abstract, not a verified absence.
