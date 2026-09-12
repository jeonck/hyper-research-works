---
title: 'Summiting the Pyramid v5.0 (CTID): implementations replace techniques as the
  coverage denominator — 710 techniques map to 1,637 implementations'
id: summiting-the-pyramid-v50-ctid-implementations-replace-techniques-as-the-coverag
tags:
- attack-ontology-drift-cti-85bc51
- coverage-claims
created: '2026-09-12T13:27:49.723559Z'
source: https://github.com/center-for-threat-informed-defense/summiting-the-pyramid
status: draft
type: note
tier: institutional
content_type: docs
deprecated: false
summary: 'CTID''s Sept 2026 Detection Coverage Calculator: technique mappings are
  not coverage; replaces them with Detection Quality (robustness x precision) and
  Implementation Coverage over a 1,637-entry catalog (mean 2.31 impls/technique, max
  13), version-pins its data-component column to ATT&CK v19, and names ''outdated
  ATT&CK mapping'' as a cause of coverage gaps.'
---

# What it is

**Summiting the Pyramid (STP)**, a research project of the **MITRE Center for
Threat-Informed Defense (CTID)**, funded by named research participants. Read here as
**primary source**: repository cloned anonymously
(`github.com/center-for-threat-informed-defense/summiting-the-pyramid`) at commit
`f4f57673c07ac6910cd2fca1ccddb93d79e9a1b3` (9 Sep 2026), and the reStructuredText
documentation, the `DCC/` tooling directory and the Implementation Catalog workbook read and
parsed directly from the working tree.

**This is the most important source in the coverage-measurement batch**, because it is the
threat-informed-defense community's own institutional admission that technique-level
coverage is invalid, together with a concrete replacement denominator and a released tool.

# Release history is itself evidence (docs/changelog.rst, verbatim bullets)

- **Version 1.0 — September 14th, 2023**: initial release; model, methodology, definitions,
  worked examples.
- **Version 2.0 — December 17th, 2024**: defines "robustness" in detection engineering, how
  to quantify and improve it; adds elements for scoring **network** detections.
- **Version 3.0 — May 8th, 2025**: "Ambiguous Techniques" research — defines what makes a
  technique ambiguous, identifies examples **in MITRE ATT&CK**, contributes best practices
  for building robust detections for ambiguous techniques.
- **Version 4.0 — February 20th, 2026**: Telemetry Strategy & Readiness; **Telemetry
  Confidence (TC)** scoring methodology with examples and results from 10 use cases on
  ambiguous behaviours; methodology for automating the process using **AI/LLM augmentation**.
- **Version 5.0 — September 10th, 2026**: "Added **Detection Coverage Calculator** tool,
  supporting work, and documentation"; "Added conceptual work regarding **measuring detection
  coverage and examining precision and implementations as factors**".

(Bullet text above transcribed from the HTML block in `docs/changelog.rst`.) Note the
publication date: **the coverage-measurement work is two days old as of this run**, so the
literature review must treat it as the live state of the art and the closest institutional
competitor to any normalization proposal.

# What it establishes about coverage measurement

**1. CTID states outright that a technique mapping is not coverage.** From
`docs/detection-ttv/detectioncoverage/index.rst`: "Detection coverage is more than the
presence of an analytic mapped to an ATT&CK technique. Meaningful coverage requires
understanding both how much of the behavior can be detected and the quality of the detection
logic providing that coverage." And from `docs/overview/detectioncoverage.rst`: mappings
"do not necessarily describe how much of the technique can be detected or the quality of the
detections providing that coverage."

**2. The replacement is two orthogonal dimensions, neither of which is a technique count.**
- **Detection Quality** = **Robustness** ("how difficult a detection signal is for an
  adversary to evade or manipulate") × **Precision** ("how well a detection signal
  distinguishes malicious behavior from benign activity"). The docs stress these are
  independent: a highly specific indicator can be strong evidence yet trivially changed,
  while an unavoidable observable may also fire constantly on legitimate activity.
- **Implementation Coverage** = "how much of the known behavioral space for an ATT&CK
  technique can be detected."

The two questions are tabulated in the docs as: Detection Quality — *"How good are the
detections providing coverage?"*; Implementation Coverage — *"How much of the behavior can we
detect?"*. The stated goal: "The goal is not simply to maximize the number of ATT&CK
techniques associated with detection content. It is to understand the strength and depth of
the coverage behind those mappings." And, memorably: "The goal is not necessarily to produce
more green boxes. It is to make the green boxes more meaningful."

**3. A NEW ONTOLOGY LAYER is inserted between technique and procedure.** This is the
structural contribution and the direct answer to the denominator problem. From
`implementationcoverage.rst`:

> **Technique**: Describes adversary behavior at a broad, reusable level.
> **Implementation**: Describes a behaviorally distinct way of accomplishing that technique
> based on its execution path and required system interactions.
> **Procedure**: Describes a specific instance of that behavior, often involving a particular
> actor, tool, command, or configuration.

The rationale given: procedure examples' "incidental details can make individual examples too
specific to serve as reusable units of coverage", while implementations "abstract away those
details while retaining meaningful behavioral differences" — yielding "a unit of analysis
that is specific enough to measure detection coverage while remaining reusable across tools,
actors, and procedures." The worked example: a scheduled task created via PowerShell, direct
Registry modification, `schtasks.exe`, or an XML task definition — same ATT&CK behaviour,
different observables.

**Coverage is then expressed as a ratio over implementations, not techniques**: "if eight
implementations are represented for a technique and available detections meaningfully observe
two, the resulting coverage can be expressed as **2/8 implementations**." With the caveat
that this "does not imply that the remaining six implementations are necessarily
undetectable."

**4. Detection depth vs. detection quantity — and the tagging critique.** From the same file:
"Adding another ATT&CK tag can increase apparent coverage without adding telemetry, analytic
logic, or the ability to detect additional adversary behavior." This is CTID stating the
thesis's "bookkeeping vs. genuine intelligence" distinction in the detection domain.

**5. CTID names outdated mappings as a first-class cause of coverage gaps.** The documented
gap taxonomy lists, among the causes: "an implementation is not addressed by existing
detection logic"; "the required telemetry is not collected or lacks the necessary fields";
"an analytic relies on signals that do not sufficiently demonstrate the mapped behavior";
**"an ATT&CK mapping is inaccurate or outdated"**; or "the analytic observes a tool or
potential precursor to behavior rather than the behavior itself." And: "identifying the cause
is often more useful than the score itself." **Ontology drift is explicitly one of the five
enumerated reasons a coverage number is wrong**, in MITRE-affiliated documentation.

# Quantitative specifics I computed from the Implementation Catalog (verified in-run)

`DCC/implementation_catalog_with_attack_components.xlsx`, parsed directly (zipfile + XML;
openpyxl unavailable). Sheet1 columns: `ATT&CK Technique ID | ATT&CK Technique Name | STIX ID
| Technique Implementation | Implementation Step Number | Implementation Step | System
Interaction | ATT&CK Data Component (v19) | Detection Observable | Confidence Score`.

- **5,963 step-level rows.**
- **710 distinct ATT&CK techniques** — 223 parents and **487 sub-techniques**.
- **1,637 distinct (technique, implementation) pairs.**
- Implementations per technique: **mean 2.31, median 2, max 13**. Distribution:
  1 impl → 342 techniques; 2 → 130; 3 → 91; 4 → 56; 5 → 50; 6 → 16; 7 → 15; 8 → 8;
  10 → 1; 13 → 1.

**The consequence is the sharpest quantitative statement of the denominator problem I can
make from primary data:** moving from a technique denominator to an implementation
denominator multiplies the denominator by ≈2.3×, and does so **wildly non-uniformly** —
48% of catalogued techniques (342/710) have exactly one implementation while one has
thirteen. A technique-level coverage percentage therefore assigns equal weight to a
one-path technique and a thirteen-path technique. Two organisations with identical
technique-level coverage can differ by an order of magnitude in implementation coverage, and
**the direction of the error is not even consistent**, so technique-level numbers are not
merely imprecise but non-monotone with respect to real coverage.

- The catalog's data-component column is **explicitly version-pinned to ATT&CK v19**
  (`ATT&CK Data Component (v19)`) — CTID version-stamps its mapping column in the schema.
  **That is precisely the reporting discipline the Navigator layer format fails to require**,
  and it is a ready-made precedent to cite for "pin the version in the artefact, in-band."
- An `ATTCK_Audit` sheet records provenance metrics: `Rows updated = 1345`,
  `Rows with semicolon-delimited interactions = 380`, `Semicolon rows with matching
  interaction/component = 380` — i.e. the catalog ships a machine-readable record of its own
  normalization pass. Again, exactly the migration-provenance artefact the thesis argues for.
- A `No Equivalent Review` sheet (73 rows: "message sent", "remote session established",
  "remote command executed", …) enumerates system interactions with **no equivalent ATT&CK
  data component** — a published residue of concepts the ATT&CK ontology does not express.

# The tool

`DCC/coveragecalculator.py` (≈81 KB, Python ≥3.10). Per `DCC/README.md`, it "analyzes one or
more **Sigma** detection rules and produces an Excel workbook that connects those analytics
to ATT&CK technique implementations. It also scores analytic fields for robustness and
precision, and adds **OCSF** event/field context where available." It accepts a YAML file, a
directory, a glob, or a **GitHub URL** (documented example: the SigmaHQ
`rules/windows/process_access` tree). Reference workbooks shipped alongside:
`scoring_dictionary.xlsx`, `implementation_catalog_with_attack_components.xlsx`,
`mappings.xlsx` (sensor-field mappings, extending prior CTID sensor-mapping work with
**field-level** detail so that "the presence of an event or data source" is not treated as
sufficient evidence of detection). The Implementation Catalog itself is built from ATT&CK
procedure examples plus **Atomic Red Team** tests via an **LLM-based pipeline**
(`DCC/implementation_pipeline`) with automated schema validation.

# Related: the robustness ladder (docs/levels/)

STP's original contribution is a 5-level observable robustness ladder, each level a separate
`.rst`: **Level 1 Ephemeral** (adversary-controlled or varying between executions — file
hashes, names, PIDs); **Level 2 Implementation / Attacker-Controlled**; **Level 3
System-Constrained Interaction** (constrained by system, application, account, target,
protocol or environment); **Level 4 Low-Variance Behaviors / Core Sometimes** (recur across
multiple ways of performing a technique but not required by all); **Level 5 Invariant
Behaviors / Core to Technique**. Scored analytics are published as
`docs/analytics/ScoredAnalytics_12062024.csv` and `ScoredAnalytics_05062025.csv`, and per
search-derived reporting the SigmaHQ repository carries an STP flag for scoring open-source
analytics (**that last claim is from search summary, not verified in-run**).

# Why this matters to the thesis — and the competitive risk

STP v5.0 is simultaneously the strongest supporting citation and the nearest competitor. It
independently establishes: technique counts are not coverage; the denominator must be
behavioural, not taxonomic; outdated ATT&CK mappings are a named cause of wrong coverage;
version pinning belongs in the schema; and normalization passes should ship an audit record.

What it does **not** do, and where the contribution remains open:
1. **It is synchronic.** The catalog is pinned to ATT&CK v19 and there is no cross-version
   machinery — no statement of what happens to an implementation when its parent technique is
   split, deprecated or revoked, and no protocol for re-basing a catalog across releases.
   **Implementations inherit the instability of the technique IDs they hang off.**
2. **It does not quantify drift.** Nothing measures how much of ATT&CK's growth is
   bookkeeping; the catalog is a snapshot.
3. **It is prescriptive, not evaluative.** No experiment shows that implementation coverage
   predicts outcomes better than technique coverage — a gap this thesis could close, with the
   1,637-implementation catalog as ready-made ground truth.
4. Its own catalog is **LLM-generated**, which makes it a legitimate object of the same
   validity scrutiny the thesis applies to LLM CTI benchmarks.

# Fidelity

**Primary-source, high fidelity for everything drawn from the repository.** Repo cloned at
commit `f4f57673c07ac6910cd2fca1ccddb93d79e9a1b3`; all `.rst` prose quoted above was read in
the working tree and short quoted fragments are transcribed from those files
(`docs/detection-ttv/detectioncoverage/index.rst`, `implementationcoverage.rst`,
`implementationcatalog.rst`, `dcc.rst`, `docs/overview/detectioncoverage.rst`,
`docs/changelog.rst`, `docs/levels/*.rst`, `DCC/README.md`). The changelog bullets are
transcribed from the raw HTML in `changelog.rst`. All catalog statistics (5,963 rows; 710
techniques; 223 parents / 487 sub-techniques; 1,637 implementations; mean 2.31 / median 2 /
max 13; the full distribution; the `ATT&CK Data Component (v19)` column header; the
`ATTCK_Audit` and `No Equivalent Review` sheet contents) were **computed in-run** by parsing
the shipped `.xlsx` and are reproducible from the repo. **Not verified**: the project website
rendering at `center-for-threat-informed-defense.github.io/summiting-the-pyramid/` (egress
blocked); the claim that SigmaHQ carries an STP flag (search summary only); and the contents
of `scoring_dictionary.xlsx`, `mappings.xlsx` and `coveragecalculator.py`, which I listed but
did not analyse. My reading of implementations as "the denominator fix" and the
non-monotonicity argument are **my interpretation**, not CTID statements.
