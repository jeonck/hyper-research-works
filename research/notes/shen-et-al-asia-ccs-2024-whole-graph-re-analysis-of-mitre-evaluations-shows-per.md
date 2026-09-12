---
title: 'Shen et al. (ASIA CCS 2024): whole-graph re-analysis of MITRE Evaluations
  shows per-technique tallies are the wrong unit'
id: shen-et-al-asia-ccs-2024-whole-graph-re-analysis-of-mitre-evaluations-shows-per
tags:
- attack-ontology-drift-cti-85bc51
- coverage-claims
created: '2026-09-12T13:25:20.848983Z'
source: https://arxiv.org/abs/2401.15878
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Re-analyses multi-year MITRE Evaluations data with control/data-flow whole-graph
  analysis; finds graph-level correlation is what determines defence, protection delay
  is ubiquitous, and per-test protection rates are dominated by scenario construction.
---

# What it is

Xiangmin Shen et al., **"Decoding the MITRE Engenuity ATT&CK Enterprise Evaluation: An
Analysis of EDR Performance in Real-World Environments"**, arXiv:2401.15878, published at
**ACM ASIA CCS 2024** (19th ACM Asia Conference on Computer and Communications Security,
1–5 July 2024), DOI 10.1145/3634737.3645012. A re-analysis of MITRE's *published Evaluations
data* — i.e. a secondary analysis of the same artefact vendors mine for coverage claims,
done properly.

**Fetch was blocked**; this note is at **summary fidelity from indexed abstract/HTML
summary text**. Nothing is quoted verbatim.

# What it establishes about coverage measurement

**The paper's method is itself the argument.** Rather than counting detections per substep
(the Evaluations' native unit, and the one vendor marketing aggregates), the authors build a
**whole-graph analysis** using **control-flow and data-flow information** to measure EDR
performance across the attack chain. The reported analysis dimensions are **detection
coverage, detection confidence, detection modifier, data source, and compatibility** — and it
spans **multiple years / multiple rounds** of MITRE evaluation results.

That design encodes the central methodological claim for this batch: **a per-technique tally
is the wrong unit, because detection value is a property of the graph, not of isolated
nodes.** Reported Finding 1 is that attack-graph-level *correlation* capability is necessary
for good defence, because isolated single steps do not give an EDR enough confidence to
respond. If that is right, then any coverage metric that sums independent per-technique
indicators is measuring something that does not determine the outcome it claims to predict —
a validity failure prior to, and independent of, any version drift.

Reported Finding 2 identifies three practical problems even among EDRs with good
graph-level correlation: **delay in protection, lack of protection, and lack of cross-host
correlation capability.** Delay is reported as ubiquitous across all scenarios: in the
analysed cases the adversary logs in and downloads a payload, more than half of the
protection occurs at that point, and the remainder occurs either *after* malicious behaviour
had already happened or not at all. **"Covered" and "covered in time" are different
predicates, and the coverage heatmap cannot express the difference** — which is exactly what
the Evaluations' *Delayed* modifier records and what an aggregated score discards.

The authors also report large variation in protection rate across individual tests, with a
significant drop in tests 3, 4 and 5, and Test 4 — reported as containing only two steps,
which dumped system information — receiving the lowest protection rate. **Per-substep
protection rates are highly sensitive to how many and which substeps a test contains**, so
a test-level or round-level aggregate is dominated by scenario construction rather than by
product capability. This is the round-to-round comparability problem stated quantitatively.

# Citable specifics

- Venue/identifiers: arXiv:2401.15878; ASIA CCS '24; DOI 10.1145/3634737.3645012; authors
  led by Xiangmin Shen (five authors reported); arXiv listing updated April 2024.
- Method: whole-graph analysis over control flow and data flow, applied to MITRE Evaluations
  results across multiple years.
- Five reported analysis dimensions: detection coverage, detection confidence, detection
  modifier, data source, compatibility.
- Finding 1 (reported): graph-level correlation is necessary; isolated single steps give
  insufficient confidence to respond.
- Finding 2 (reported): delay in protection, lack of protection, lack of cross-host
  correlation; delay ubiquitous in all scenarios; more than half of protection concentrated
  at the login-and-download stage, the rest late or absent.
- Reported per-test variance: significant protection-rate drop in tests 3–5; Test 4
  (two steps, system-information dumping) lowest.

# Position against the literature

This is the closest existing work to a *methodological* re-analysis of ATT&CK-relative
measurement, and it pairs with Virkud et al. (USENIX Sec '24) to bracket the problem:
Virkud shows the *labels* are inconsistent across products at a fixed version; Shen et al.
show the *aggregation* over labels is invalid even when the labels are MITRE's own. Neither
varies the ATT&CK version. Together they establish that coverage is broken along the
cross-product and cross-substep axes, leaving the **cross-version axis as the unclaimed
third** — which is this thesis's territory. Methodologically the paper is also a template
for what an SCI-level contribution here looks like: take the community's canonical published
measurement artefact, re-derive it under an explicitly defended alternative unit of analysis,
and show the two disagree.

Also surfaced in the same result set and worth pairing: **"Are we there yet? An Industrial
Viewpoint on Provenance-based Endpoint Detection and Response Tools"** (arXiv:2307.08349),
and **"MITRE ATT&CK Applications in Cybersecurity and The Way Forward"** (arXiv:2502.10825),
a survey that positions ATT&CK applications and open problems. Neither read here.

# Fidelity

**Summary fidelity only.** arxiv.org could not be fetched in this environment (egress proxy
403). All findings, numbers and the method description above are **paraphrased from indexed
abstract and HTML-summary text** and were **not read in the paper's full text**. Nothing is
quoted verbatim. The finding numbering ("Finding 1", "Finding 2") and the test indices
(3, 4, 5) are as reported in the indexed summary and should be re-checked against
`arxiv.org/pdf/2401.15878` before citation — in particular the "more than half of the
protection" figure and the Test 4 characterisation, which are the most specific claims here.
The bibliographic metadata (arXiv ID, venue, DOI, lead author) is high-confidence, coming
from multiple independent listings including the ACM DL record.
