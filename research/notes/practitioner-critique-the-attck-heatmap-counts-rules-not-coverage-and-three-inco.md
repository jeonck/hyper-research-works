---
title: 'Practitioner critique: the ATT&CK heatmap counts rules, not coverage, and
  three incompatible denominators now circulate'
id: practitioner-critique-the-attck-heatmap-counts-rules-not-coverage-and-three-inco
tags:
- attack-ontology-drift-cti-85bc51
- coverage-claims
created: '2026-09-12T13:30:01.669484Z'
source: https://dev.to/chrisray/your-attck-heatmap-is-counting-rules-not-coverage-2gh3
status: draft
type: note
tier: commentary
content_type: blog
deprecated: false
summary: 'Field articulation of the denominator problem: heatmaps count techniques
  with at least one mapped rule, a quantity unrelated to whether an alert fires; techniques
  vs implementations vs security-layers-per-technique are three non-inter-convertible
  denominators now in use.'
---

# What it is

A cluster of practitioner writing, all making the same structural argument, that the ATT&CK
coverage heatmap measures the wrong quantity. The lead item is **"Your ATT&CK Heatmap Is
Counting Rules, Not Coverage"** (chrisray, DEV Community). Converging items found in the same
searches: **"Measuring Detection Coverage Without Lying to Yourself"** (Mayank Joshi, Medium,
June 2026); **CardinalOps, "Security Layers — Measuring MITRE ATT&CK Detection Coverage"**;
**"Detection Coverage: Measuring What You Can Actually See"** (kcyerrid.com, March 2026);
Datadog's Cloud SIEM MITRE ATT&CK Map gap-analysis post. These are the field's own articulation
of the denominator problem, and they matter because they show it is not an academic objection.

**Fetch blocked**; all content below is at **summary fidelity from indexed search text**.
Nothing is quoted verbatim.

# What it establishes about coverage measurement

**The stated core problem, and it is exactly the thesis's:** the quantity being counted —
techniques with at least one mapped rule — has almost no relationship to the quantity that
matters — the probability that an attacker behaviour generates an alert someone acts on. The
compact reported formulation is that the heatmap **measures what is written, not what works**.
The associated observation is that every detection vendor ships an ATT&CK heatmap and every
one of them is mostly green.

**Coverage is a gradient, not a binary.** The reported argument: a single rule for a technique
does not mean you are covered, because a technique might have **50 different procedures**.
This is the same insight CTID formalised as Implementation Coverage, arrived at independently
from the practitioner side — good evidence that the technique-as-unit failure is
field-recognised rather than a niche critique.

**The numerator is a labelling artefact; the denominator is a taxonomy artefact.** Counting
"techniques with ≥1 mapped rule" makes the score movable in two ways that have nothing to do
with defence: add an ATT&CK tag to an existing rule (numerator up, capability unchanged), or
have MITRE restructure the matrix (denominator changes, capability unchanged). The first is
the practitioners' complaint; the second is the version-drift axis they do not discuss, and it
is the gap the thesis fills.

**CardinalOps' "Security Layers" is the vendor-side attempt at a fix and reveals a third free
parameter.** Reported: traditional approaches "simply compile the number of detection rules for
a given ATT&CK technique without considering the attack surface", and heatmaps are "too
simplistic because they only add up the total number of detections aligned to a given technique
– without measuring how much of the attack surface in your infrastructure is actually covered".
Their proposal maps each detection to a **security layer** — endpoint, network, email, cloud,
containers, IAM — and counts **distinct layers covered per technique**, aiming at
"detection-in-depth". Launched with press coverage in DarkReading, SecurityWeek and PRNewswire
and presented at Splunk .conf23.

The methodological point for the thesis: **there are now at least three competing, mutually
incompatible denominators in circulation** — techniques (classic), *implementations* (CTID
STP), and *security layers per technique* (CardinalOps) — and they are not
inter-convertible. A coverage percentage without a declared denominator definition is
therefore uninterpretable *even at a fixed ATT&CK version*, before drift is considered at all.
This strengthens the reporting-discipline argument considerably: the protocol must require the
denominator's definition, not merely the ATT&CK version.

**The proposed ground truth is execution, not mapping.** Reported across several of these
items: use **Atomic Red Team** to execute individual technique simulations in a controlled
environment and observe whether the expected alerts fire, feeding results back into gap
analysis to supply "the ground truth that rule-count-based coverage estimates cannot". Note
that CTID's Implementation Catalog is built from ATT&CK procedure examples **plus Atomic Red
Team tests** — the practitioner ground-truth source and the institutional catalog source are
the same corpus, which makes Atomic Red Team a natural third leg for any empirical study here
(and a natural place to look for its own version drift).

# Citable specifics

- Framing: counts "techniques with at least one mapped rule"; measures what is written, not
  what works; every vendor heatmap is mostly green.
- "A technique might have 50 different procedures"; coverage is a gradient, not a binary switch.
- CardinalOps security layers: endpoint, network, email, cloud, containers, IAM; metric is the
  count of distinct layers covered per technique; framed as "detection-in-depth".
- Atomic Red Team execution as the proposed ground truth for validating coverage claims.

# Fidelity

**Summary fidelity only, and weak provenance.** None of these pages could be fetched (egress
proxy blocks direct retrieval). Every claim above is **paraphrased from indexed search-result
summaries**; nothing was read in full text and nothing is quoted. The summaries blended several
of the listed sources, so **attribution of any specific phrasing to a specific author is not
reliable** — treat the arguments as "the practitioner denominator-critique cluster" and
re-read the individual posts before attributing. Source tier is community/practitioner
(DEV Community and Medium are self-published; CardinalOps is vendor marketing for its own
product and its framing of "traditional approaches" is self-serving). The "50 procedures"
figure is illustrative rhetoric, not a measurement. These sources are useful for establishing
that the problem is recognised in the field and for the three-competing-denominators argument;
they are **not** citable for any quantitative claim.
