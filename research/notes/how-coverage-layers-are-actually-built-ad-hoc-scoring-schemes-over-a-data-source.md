---
title: 'How coverage layers are actually built: ad hoc scoring schemes over a data-source
  mapping that is itself version-dependent'
id: how-coverage-layers-are-actually-built-ad-hoc-scoring-schemes-over-a-data-source
tags:
- attack-ontology-drift-cti-85bc51
- coverage-claims
created: '2026-09-12T13:33:48.386428Z'
source: https://blog.reconinfosec.com/automating-coverage-analysis-with-att-ck-navigator
status: draft
type: note
tier: practitioner
content_type: blog
deprecated: false
summary: Practitioner recipes score layers binary / TTP-vs-IOC / confidence-banded
  with no declared semantics, and build the 'could be detected' denominator from MITRE's
  technique-to-data-source mapping — a second versioned artefact, remodelled at ATT&CK
  v10, that no recipe pins.
---

# What it is

The practitioner literature on **how an ATT&CK coverage layer is actually constructed** —
the operational recipes behind the published heatmap. Principal items: **Recon InfoSec,
"Automating Detection Coverage Analysis with ATT&CK Navigator"** (blog.reconinfosec.com);
**Gigamon, "Dialing in Your Detection Coverage with MITRE ATT&CK"** (30 March 2021);
**NVISO Labs, "DeTT&CT: Mapping detection to MITRE ATT&CK"** (9 March 2022); Exabeam's
Navigator explainer; dogesec's "Getting Started with the MITRE ATT&CK Navigator"; Lennart
Erikson's "Three ways to use the ATT&CK Navigator for threat-informed decision making"
(Medium); and Securelist's "What MITRE ATT&CK techniques to detect first?" on detection-backlog
prioritisation. This batch's assigned search #1 landed here, and the value is in what these
recipes *silently assume*.

**Fetch blocked**; **summary fidelity from indexed search text** throughout. Nothing quoted.

# What it establishes about coverage measurement

**Layers are a heatmap over the matrix driven by a numeric `score`, and the scoring scheme is
chosen ad hoc by each author.** Reported approaches, in increasing sophistication:

1. **Binary** — the reported "most obvious method": you either have some level of coverage for
   a technique or you have none.
2. **Provenance-differentiated** — colour techniques covered by *behaviour*-based (TTP-level)
   rules differently from those covered by targeted, tool-specific **IOC-based** rules, on the
   argument that these are not the same kind of coverage. (This is the Pyramid-of-Pain
   intuition that CTID later formalised as *robustness*.)
3. **Quality-banded** — green if at least one **high-confidence** detection exists, yellow for
   a low-confidence or easily bypassed detection, blank if uncovered.

Reported Navigator mechanics consistent with the spec read directly in the repo: layers work
like graphics-editor layers, overlaying datasets for comparison without altering the underlying
data; the `score` field carries the relative quality of coverage for a technique; the `metadata`
field records where the coverage comes from and the associated data source.

**The dominant construction method is data-source-driven, which imports MITRE's data-source
ontology as a hidden dependency.** Recon InfoSec's reported pipeline: use **MITRE's own mapping
of data sources to techniques** to determine where techniques *could* be detected; then
programmatically analyse the existing ruleset to determine what is *actually* configured to
detect; emit the result as a `.json` Navigator layer with `score` and `metadata` populated. The
reported per-technique data-source examples are process creation logs, network traffic, Windows
event logs, command history.

**This is the finding that matters for the thesis.** A coverage layer built this way is a
function of *two* ATT&CK-versioned artefacts, not one: the technique set **and** the
technique↔data-source mapping. And the data-source ontology is among the most heavily
restructured parts of ATT&CK — the Navigator's own `CHANGELOG.md` records a **data sources
panel** added to search/multiselect for **ATT&CK v10** support (v4.5.0, 21 October 2021,
verified in the cloned repo), corresponding to the release in which data sources were
re-modelled into data source / data component objects. CTID's Implementation Catalog likewise
version-pins its mapping column to **ATT&CK v19** (verified in that repo). **A "what could be
detected" denominator computed from data-source mappings therefore shifts when MITRE remodels
data sources, entirely independently of any change to the technique set or to the defender's
sensors.** None of the practitioner recipes surfaced mentions pinning either artefact, and the
automation framing ("real-time mappings", "staying current with adversarial methodologies in a
dynamic environment") actively encourages regenerating against latest — which maximises drift
exposure while presenting the output as a stable time series.

**Prioritisation writing concedes the denominator is not the matrix.** Securelist's
detection-backlog prioritisation piece, and the widely repeated practitioner position that
striving for 100% coverage of ATT&CK is both unadvisable and unachievable, both amount to
saying the operative denominator is a *selected* subset. Also surfaced: a claim that roughly
**65% detection coverage** suffices for many outcomes — cited here only as an example of the
genre's unsourced numerics, **not as a finding**.

# Citable specifics

- Three scoring schemes: binary; TTP-rule vs IOC-rule differentiated; high/low-confidence banded.
- Navigator layer mechanics: `score` = relative coverage quality; `metadata` = coverage source
  and data source; layers overlay without altering underlying data.
- Recon InfoSec pipeline: MITRE data-source→technique mapping for "could detect", programmatic
  ruleset analysis for "does detect", emitted as a Navigator `.json` layer.
- DeTT&CT as the tooled version of this workflow (NVISO walkthrough) — see the companion
  DeTT&CT note, which is source-verified.

# Why this matters to the thesis

These recipes are the mechanism by which incomparability is manufactured in the field. Three
authors following three of these guides produce three layers whose `score` fields mean three
different things, none declared in the artefact (the layer format has no field for "what the
score means" beyond free-text `description` and `legendItems`). Add the undeclared ATT&CK
version, the undeclared data-source-mapping version, and the undeclared denominator definition,
and a published coverage layer is under-specified along at least four axes simultaneously. **The
reporting discipline the thesis proposes can be stated as closing exactly these four gaps**, and
this literature is the evidence that all four are currently open in routine practice.

# Fidelity

**Summary fidelity only for the practitioner sources; the ATT&CK-side facts are verified.** None
of the blog posts could be fetched (egress proxy blocks direct retrieval). The scoring schemes,
Navigator mechanics and Recon InfoSec pipeline description are **paraphrased from indexed
search-result summaries** blending several of the listed posts; nothing was read in full,
nothing is quoted, and **attribution of a specific scheme to a specific author is not reliable**
— re-read the individual posts before attributing. The "65% suffices" figure is unsourced genre
rhetoric and must not be cited. By contrast, the two ATT&CK-side facts used in the argument are
**verified in cloned repositories in this session**: the Navigator data-sources panel added for
ATT&CK v10 support (`CHANGELOG.md`, `# v4.5.0 - 21 October 2021`, commit
`734a1caba29fcd51f20b9ca239ce652b3354a47e`), and CTID's `ATT&CK Data Component (v19)` column
header in the Implementation Catalog (commit `f4f57673c07ac6910cd2fca1ccddb93d79e9a1b3`). The
inference that data-source remodelling shifts the "could be detected" denominator is **mine**,
and is well-motivated but not directly evidenced by a source that states it; it would be worth
demonstrating empirically by recomputing a data-source-derived layer across the v9→v10 boundary.
