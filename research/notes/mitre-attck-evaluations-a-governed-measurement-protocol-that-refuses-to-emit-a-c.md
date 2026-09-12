---
title: 'MITRE ATT&CK Evaluations: a governed measurement protocol that refuses to
  emit a coverage score, and drifts round to round'
id: mitre-attck-evaluations-a-governed-measurement-protocol-that-refuses-to-emit-a-c
tags:
- attack-ontology-drift-cti-85bc51
- coverage-claims
created: '2026-09-12T13:23:47.296660Z'
source: https://evals.mitre.org/methodology-overview/
status: draft
type: note
tier: institutional
content_type: docs
deprecated: false
summary: Evals scores per-substep detection categories (None/Telemetry/General/Technique)
  with a pre-enumerated denominator and publishes no ranking or score; but scope,
  category semantics ('General' redefined, 'Tainted'->'Correlated') and detection
  criteria change every round, and MITRE's remedy is a diff tool not a normalized
  series.
---

# What it is

The public methodology documentation for **MITRE ATT&CK Evaluations** (`evals.mitre.org`),
comprising the "Methodology Overview" and the "Scoring Specification" pages plus the
per-round "Detection Categories" pages (`/enterprise/apt3/detection-categories`,
`/enterprise/apt29/detection-categories`, `/enterprise/wizard-spider-sandworm/detection-categories`,
`/enterprise/er6/detection-categories`, …). This is the closest thing the industry has to a
*governed*, vendor-neutral protocol for measuring ATT&CK-relative detection performance, and
it is therefore the natural benchmark against which a normalization protocol should be argued.

**Fetch was blocked** (egress proxy 403 on `evals.mitre.org`), so everything below is at
**summary fidelity from indexed search text**, not full-text reading. No sentence is quoted.

# What it establishes about coverage measurement

**Evaluations deliberately refuse to produce a coverage score.** The programme's own framing
is that it does not rank vendors or solutions, does not crown winners, does not publish
rankings or hand out scores; it releases the raw test data and basic comparison tools, and
leaves interpretation to the reader. Results are described as intended to help an
organisation judge fit against its own gaps. The methodology is characterised as a
collaborative, threat-informed, purple-team process: adversary selection and scenario design
from attributed threat intelligence, red-team execution of a full behaviour chain in a
controlled environment, and structured recording of detection/prevention/investigation
performance.

This matters enormously to the thesis. **The most rigorous ATT&CK-based measurement
programme in existence explicitly declines to emit the single number that the entire vendor
coverage-marketing genre emits.** The gap between what MITRE will assert and what vendors
assert *from MITRE's own data* is the cleanest available demonstration that the coverage
percentage is a marketing construct rather than a measurement.

**The unit of scoring is a per-substep detection category, not a technique tally.** For
Enterprise 2025 detections are classified into five categories capturing how much context
reaches the analyst — reported as **None** (sensors deployed but no data showing the event),
**Telemetry** (the event is recorded but not assessed malicious), **General** /
**General Behaviour** or **Tactic**-level (assessed malicious, and for the tactic-level
variant identified at ATT&CK Tactic granularity but *without* technique-level
classification — e.g. "Credential Access" but not "LSASS dumping"), and **Technique**
(identified at ATT&CK Technique or Sub-Technique level and meeting the documented Detection
Criteria). **Modifiers** — reported to include *Delayed* and *Config Change* — decorate a
main category. Earlier rounds are described with six detection categories and three
protection categories, split into "Main" and "Modifier" types, each detection receiving
exactly one main category and optionally one or more modifiers.

Two structural lessons for a normalization protocol:

1. **Granularity is an explicit, recorded property of each observation** — MITRE separates
   "right tactic, wrong/no technique" from "right technique/sub-technique". A coverage claim
   that collapses these is discarding the distinction MITRE found necessary. This is the
   same parent-vs-sub-technique granularity problem that sub-technique restructuring creates
   across versions, and MITRE's answer is to *record the granularity per observation* rather
   than pick one denominator.
2. **A "None" category exists.** The denominator is enumerated in advance (the substeps of
   the emulation), and non-detection is an explicit recorded value, not an absence. A
   coverage heatmap, by contrast, encodes non-coverage as an uncoloured cell that is
   indistinguishable from "not in scope" and from "technique did not exist in this version".

# What it establishes about round-to-round comparability

The round-to-round record is itself a case study in ontology and protocol drift, and the
drift is *in the measurement instrument*, not only in ATT&CK:

- **Scope changes with the emulated adversary.** Round 1 emulated APT3; Round 2 emulated
  APT29 and, per MITRE's own Round 2 site-update post, brought a **new scope of techniques**,
  reported as **58 Enterprise Windows techniques across 10 tactics**. Later rounds broadened
  to macOS, added false-positive/efficiency measurement, and incorporated the Reconnaissance
  tactic for the first time. **The denominator changes every round by design**, so a
  "detection rate" from one round and another are ratios over different, non-nested sets.
- **Category definitions were redefined under stable names.** The "General" category is
  reported to be defined *differently* from Round 1's "General Behavior", and the
  "Correlated" modifier is reported to be the Round 1 "Tainted" modifier **renamed**. This is
  exactly the ATT&CK failure mode the thesis is about — *silent semantic rewriting under a
  stable identifier* — occurring in the evaluation ontology rather than the technique
  ontology.
- **Detection criteria tightened.** For C2, established network sockets and DLL loads are
  reported to have been sufficient for a valid detection in earlier results, while in the
  Carbanak/FIN7 round MITRE shifted to requiring network analysis. **The same product
  behaviour scores differently in different rounds.**
- **Consolidation continues.** Enterprise 2026 is reported to eliminate the historical
  Enterprise / Managed Services separation, evaluating EDR, XDR, MDR, MSSP, SIEM and AI SOC
  vendors on the same scenarios and quality metrics — another discontinuity in the
  comparison population.
- Secondary commentary characterises the first three rounds as carrying notable
  methodological modification and the most recent three as substantially consistent.

**MITRE's own mitigation is a comparison tool, not a normalized score.** The Round 2 site
update is titled around a "Technique Comparison Tool" — i.e. the institutional response to
the incomparability of rounds is to let users diff, not to publish a migrated time series.
That is the same answer the ATT&CK Navigator gives for layers (a manual upgrade wizard, not
an automatic re-basing), and it is an important pattern for the thesis: **MITRE consistently
refuses to auto-normalize across versions and pushes the judgement onto the analyst**, while
the downstream ecosystem behaves as if the numbers were already normalized.

# Citable specifics

- Detection categories (Enterprise 2025, five): None, Telemetry, General/Tactic-level,
  Technique. Modifiers reported: Delayed, Config Change. Earlier rounds: six detection
  categories plus three protection categories, in Main/Modifier types.
- APT29 (Round 2) scope reported as 58 Enterprise Windows techniques over 10 tactics.
- "General" ≠ Round 1 "General Behavior"; "Correlated" = renamed Round 1 "Tainted".
- Participant counts by round as reported: APT3 12 vendors; APT29 12 vendors; Carbanak+FIN7
  29 vendors; Round 4 (Wizard Spider + Sandworm, March 2022) 30 vendors. A changing
  participant population is a further barrier to reading round-over-round movement as
  capability change.
- Programme stance: no ranking, no winners, no scores; raw data plus basic comparison tools.

# Why this matters to the thesis

Evaluations supplies the *positive* half of the argument. It shows that a defensible
ATT&CK-relative measurement is possible, and what it costs: a pre-enumerated denominator, an
explicit non-detection category, per-observation granularity recording, published detection
criteria, and an explicit refusal to aggregate into a single comparable number. It
simultaneously shows the *residual* problem: even with that discipline, round-to-round
comparability fails because scope, category semantics and criteria all drift, and MITRE's
answer is a diff tool rather than a normalization. The thesis's reporting discipline can be
framed as: adopt Evaluations' per-observation rigour, and add the thing Evaluations does not
provide — an explicit, machine-checkable version-migration record so that the time series
can be reconstructed rather than merely diffed by hand.

# Fidelity

**Summary fidelity only.** `evals.mitre.org` and the linked MITRE/Medium pages could not be
fetched in this environment (egress proxy returns 403; `hyperresearch fetch` on
`https://evals.mitre.org/methodology-overview/` failed with 403 Forbidden, verified in-run).
All category definitions, scope figures, renamings, criteria changes and participant counts
above are **paraphrased from indexed search-result summaries** and are **not verified against
the primary pages**. Nothing is quoted verbatim. Every specific in this note should be
re-checked against `evals.mitre.org/methodology-overview/`,
`evals.mitre.org/methodology-specification/` and the per-round detection-categories pages
before it appears in the thesis — particularly the exact five-category names for Enterprise
2025, the APT29 "58 techniques / 10 tactics" figure, and the General/General Behavior and
Correlated/Tainted redefinitions, which are the load-bearing claims here.
