---
title: 'Virkud et al. (USENIX Security 2024): ATT&CK coverage is not comparable across
  products — recomputed from the public artefact'
id: virkud-et-al-usenix-security-2024-attck-coverage-is-not-comparable-across-produc
tags:
- attack-ontology-drift-cti-85bc51
- coverage-claims
created: '2026-09-12T13:22:26.055089Z'
source: https://www.usenix.org/conference/usenixsecurity24/presentation/virkud
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'USENIX Sec''24: products disagree on the ATT&CK label for the same threat
  51% of the time; recomputed from artefact repo: Splunk 38.9%, Elastic 37.5%, Sigma
  57.8% of ATT&CK v11, pairwise Jaccard ~0.5, parents 79.6% vs sub-techniques 60.2%,
  and live Sigma rules still tagging revoked T1035/T1043/T1050.'
---

# What it is

Virkud, Inam, Riddle, Liu, Wang and Bates, "How does Endpoint Detection use the MITRE
ATT&CK Framework?", **USENIX Security Symposium 2024** (33rd). The single strongest
peer-reviewed empirical attack on the validity of "ATT&CK coverage" as a security metric.
USENIX artifact-evaluated (Available, Functional, **Reproduced** badges). Analysis code and
data are public at `github.com/avirkud/endpoint-detection-mitreattack`; I cloned the
artefact repository and **recomputed the coverage statistics directly from it** (details and
my own numbers below). The paper PDF itself I could not fetch (egress blocked); the
paper-level findings quoted below come from indexed abstract/summary text, and are marked
as such.

# What it establishes about coverage measurement

**1. Coverage is bounded well below 100% and products do not even try.** Reported finding:
coverage across the studied products ranges roughly **48%–55%** of the matrix, and that
figure is itself **inflated by low-risk / low-severity rules** unlikely to be prioritised
in practice. A published coverage percentage is therefore not a measure of defensive
capability; it is a count of annotations, weighted by nothing.

**2. Large regions of ATT&CK are unimplementable as endpoint rules.** Reported finding:
**53 techniques** are unimplemented across *all* rulesets studied, substantially because
many techniques are not realizable as endpoint detection rules at all. This is the
**denominator problem** stated empirically: the full technique set is the wrong
denominator because part of it is out of scope for the sensor class by construction.
Coverage over "all of Enterprise ATT&CK" thus systematically understates, and coverage over
a self-chosen realizable subset is unauditable unless the subset is published.

**3. The killer result for comparability — products disagree about what technique they are
detecting.** Reported finding: when detecting the *same* malicious entity, products
**completely disagree** on the appropriate ATT&CK technique annotation **51%** of the time
and **fully agree only 2.7%** of the time. The authors' stated implication is that coverage
of an ATT&CK technique does not consistently imply coverage of the same real-world threat.
For this thesis this is decisive: even holding the ATT&CK version *fixed*, the technique
label is not an inter-rater-reliable unit. Ontology drift across versions therefore sits on
top of an already-unreliable base annotation, and the two error sources compound.

# Citable specifics I recomputed from the artefact (verified in-run)

Repository cloned and parsed with a short script; rulesets are the paper's **October 2022
snapshots** of Splunk `security_content`, Elastic `detection-rules`, and SigmaHQ `sigma`.
The denominator is the repo's own `data/techniques.csv`, which the README states enumerates
the techniques and tactics from **v11 of the MITRE ATT&CK Framework** — **578 technique
rows: 191 parent techniques and 387 sub-techniques.**

Distinct ATT&CK technique IDs referenced by each ruleset, as a fraction of that 578:

| ruleset | rule rows parsed | distinct technique IDs | coverage of v11 (578) |
| --- | --- | --- | --- |
| Splunk  | 955  | 225 | **38.9%** |
| Elastic | 563  | 217 | **37.5%** |
| Sigma   | 2515 | 337 | **57.8%** |
| union of all three | — | 385 | **66.6%** |
| intersection of all three | — | 140 | **24.2%** |

- **193 of 578 v11 techniques (33.4%) are referenced by none of the three rulesets.**
- Pairwise Jaccard similarity of the covered technique sets is only about **0.50–0.55**
  (Splunk/Elastic 0.509, Splunk/Sigma 0.503, Elastic/Sigma 0.548). Two vendors can each
  publish "≈38% coverage" and be talking about substantially different halves of the matrix.
  **The headline percentage is nearly uninformative about which techniques are covered.**
- Coverage is much thinner at sub-technique granularity than at parent granularity: the
  union covers **152/191 parents (79.6%)** but only **233/387 sub-techniques (60.2%)**.
  This is directly load-bearing for the sub-technique-restructuring question: **the same
  ruleset scores far higher against a parent-level denominator than a sub-technique-level
  one**, so a coverage number computed pre- and post-restructuring is not comparable, and a
  vendor free to choose the granularity can move its own score by ~20 points without
  changing a single rule.
- **11.1% of Sigma rules (279 of 2515) carry no ATT&CK technique tag at all** — a further
  reminder that the numerator of a coverage ratio is a labelling artefact, not a capability.

# Direct evidence of ontology drift leaking into production detection content

Three technique IDs tagged in the October 2022 Sigma snapshot **do not exist in the v11
technique list** used as the denominator: **T1035, T1043 and T1050**. All three are
legacy pre-sub-technique IDs that ATT&CK retired during the sub-technique restructuring
(they map, as I recall them, to Service Execution → T1569.002, Commonly Used Port → T1571,
and New Service → T1543.003 — *this replacement mapping is recalled, not verified in this
run; the absence from the v11 list is verified*). The observable point stands regardless of
the exact mapping: **a widely used, actively maintained open detection ruleset was still
carrying revoked ATT&CK identifiers roughly two years after the restructuring.** Any
coverage computation that joins such a ruleset to a current ATT&CK release will silently
drop those rules (unmatched ID) or, worse, keep them and inflate the numerator with dead
labels. This is precisely "ontology bookkeeping" masquerading as, or destroying, coverage.

# Position against the literature

This paper is the empirical anchor for the coverage-validity half of the thesis and should
be cited as prior art that must be *extended*, not repeated. What it does: fixes an ATT&CK
version (v11), fixes a ruleset snapshot (Oct 2022), and shows coverage is
non-comparable *across products at one version*. What it explicitly does **not** do: vary
the ATT&CK version and measure how the same fixed ruleset's coverage number moves across
releases. That longitudinal, version-varying experiment is the open gap this thesis can
occupy, and the artefact repository makes the baseline reproducible. The natural design is:
hold the ruleset constant, recompute coverage against every ATT&CK release, and decompose
the delta into (added techniques diluting the denominator) vs (deprecations/revocations
orphaning the numerator) vs (sub-technique splits changing granularity) vs (genuine rule
changes). The 79.6%-vs-60.2% parent/sub gap computed above is a first indication that this
decomposition will produce large numbers.

# Fidelity

**Mixed, clearly separated.** The *recomputed statistics* (578-row v11 universe; 225/217/337
distinct technique IDs; 38.9/37.5/57.8% and the union, intersection, Jaccard, parent/sub
splits; 279 untagged Sigma rules; T1035/T1043/T1050 absent from v11) are **primary and
verified in-run** — I cloned the public artefact repository and computed them from the CSVs
with a script; they are reproducible from that repo. Rule-row counts are as my parser read
the CSVs and may differ slightly from the paper's own counts depending on
deduplication/filtering. The *paper-level findings* (48–55% coverage range, 53 techniques
unimplemented in all rulesets, 51% complete disagreement / 2.7% full agreement, the
low-severity inflation claim) are at **summary fidelity only** — taken from indexed
abstract and summary text, **not read in the paper's full text**, which the egress proxy
blocked; they should be re-verified against `usenixsecurity24-virkud.pdf` before being
quoted in the thesis, and I have not reproduced any sentence from the paper verbatim.
