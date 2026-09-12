## Abstract

Cyber threat intelligence measures adversary behaviour with an instrument: the MITRE ATT&CK
knowledge base, whose technique identifiers are the units in which detection coverage, threat-actor
attribution and benchmark labels are all denominated. That instrument has been re-issued 109 times
across three domains since January 2018, and each re-issue is a recalibration — identifiers retired
and minted, concepts re-cut across abstraction levels, meanings rewritten in place, tactics
reassigned. We can find no published CTI result that reports which calibration it used. From every
public ATT&CK STIX release we build a longitudinal database of 106 domain-release pairs, measure
four drift processes separately — identifier churn, abstraction re-cutting, intensional rewriting
under a stable identifier, relational reassignment — and run four controlled downstream experiments
that hold intelligence content fixed and vary only the vocabulary. The measurement is dialectical
and we report both halves. MITRE's identifier accounting for Enterprise is
complete — every revoked technique carries exactly one successor edge and none dangle — and
post-2020 identifier survival to the newest release never falls below 0.970. Yet 0.749 of
the identifier-stable techniques of v7.0 have had their descriptions edited by v19.0, the
object version field detects a description rewrite with precision 0.447 and recall 0.641,
0.323 of all new group-technique edges for pre-existing groups are ontology bookkeeping
rather than intelligence, and a coverage claim of 97.0% re-measured against a later release
reads 17.4%. Vocabulary mismatch alone changes the named threat actor in 0.722 of
pre-restructuring observations and still in 0.022 across a single modern release boundary.
Identifier normalization recovers 0.42 to 0.53 of the legacy penalty and close to nothing
modern, and is silent on every semantic change by construction. The contribution is
therefore not a crosswalk but a reporting contract: an ATT&CK label set must declare its
domain, its exact release, the bundle hash, and a residual ledger of what any normalization
kept, merged, demoted and dropped.

## 1. Introduction

A coverage percentage, an attribution verdict and a benchmark score are all measurements, and
every measurement is stated in units. In cyber threat intelligence the unit is the ATT&CK
technique identifier. When a vendor reports that a product covers 84.2% of ATT&CK, when a paper
reports a micro-F1 over ATT&CK labels, or when an analytic names an intrusion set from a set of
observed TTPs, the number is meaningful only relative to a particular edition of the catalogue,
which supplies both the numerator's vocabulary and the denominator's cardinality [63, 74]. The
ATT&CK project is unusually disciplined about publishing those editions: each release is an
immutable, addressable STIX bundle, retired objects are retained rather than deleted, and every
revoked technique carries a typed edge to its successor [1, 7]. The discipline is asymmetric.
The producer versions scrupulously; the consumer literature does not report the version at all.

This paper takes that asymmetry literally and treats ATT&CK as an instrument that has been
silently recalibrated. The framing is not rhetorical. Drift in the scale is separable from drift
in the thing measured — precisely the separation that concept-drift theory in security machine
learning cannot express, being formulated over a fixed label space [22, 33, 67], and that
class-incremental and evolving-ontology work models only in its additive form [24, 43]. ATT&CK
also retires, merges, promotes across abstraction levels, and silently redefines classes it
retains. A measurement vocabulary that does all of this, consumed by a field that reports none
of it, is a validity problem rather than a hygiene complaint.

We make the argument by measurement, and we make the concessions the measurement forces. The first
is the apparatus: pinning a release is MITRE's documented first-class workflow, tombstones are
guaranteed, and a change-computation tool ships with an explicit class for objects patched without
a version increment [1, 34, 48]. Our extraction confirms the strongest form of that
claim for Enterprise technique identifiers — 149 revoked-by edges from 149 distinct revoked
techniques, zero dangling, no identifier ever vanished without a tombstone (Section 6.2). The
second concession is the noise floor. Detection products pinned to one ATT&CK release disagree
about the label for the same behaviour roughly half the time [74], and roughly two-thirds of
ATT&CK groups have no technique unique to them [59]. We do not claim drift dominates that noise.
We claim it is separable by construction — every condition in our experiments draws from the
same curated ATT&CK data, so the labelling process is constant across conditions and cancels in
the contrasts — and we test additivity rather than assume it (Section 7.4). The third concession
is the remedy: identifier normalization is worth 42 to 53 points of recovered attribution
penalty on pre-2020 artefacts and under one point on modern ones, with an interval spanning zero
in most modern conditions (Section 8).

The contributions are four: a longitudinal measurement of ATT&CK drift over every public release
of all three domains, decomposed into four processes that behave differently in time (Section 6);
four controlled experiments — attribution, coverage, mitigation ranking, benchmark label validity
— in which intelligence is held fixed and only the vocabulary moves (Sections 7 and 9); a
decomposition of apparent knowledge growth into intelligence and bookkeeping (Section 6.5); and a
normalization protocol whose measured limits are themselves the result, with the reporting
discipline that follows from them (Sections 8 and 10). A reader should be able to reconstruct
every quantity here from Section 5 alone; where a number is fragile we say by how much and in
which direction.

## 2. Background: ATT&CK as a Versioned Ontology

ATT&CK organises adversary behaviour into tactics, techniques and sub-techniques, and links them
to intrusion sets, software, mitigations and data components. Its design documentation is explicit
that inclusion criteria are non-stationary and that a technique's abstraction level is an editorial
choice rather than a natural kind [14]. The catalogue is therefore not an inventory that grows only
as adversaries innovate; it is an editorial artefact that is periodically re-cut. MITRE and
practitioners alike describe it as an ontology rather than a taxonomy [77], which places it inside
a literature with mature machinery for exactly this problem: ontology evolution versus versioning,
with change management as the core task of both [56].

That literature supplies the yardstick. OBO Foundry's versioning principle requires version IRIs,
release immutability and perpetual resolvability of prior versions [55]; its identifier policy
requires uniqueness and forbids reuse [53]; its term-stability principle requires that an
identifier's referent not change, separates exact successors (`replaced_by`) from inexact ones
(`consider`), and requires obsoletion to be visible in the human-readable label rather than only in
metadata [54]. OWL supplies `versionIRI`, `priorVersion`, `backwardCompatibleWith` and
`owl:deprecated` [57]; COnto-Diff supplies typed complex change operations — merge, split, move,
substitute — as a first-class evolution mapping rather than an untyped diff [26]; and Gene Ontology
evolution has already been shown to change the interpretation of analyses computed over it, moving
a conclusion without any new experiment [69]. Security vocabularies have their own version of the
problem: CVE carries typed lifecycle states including rejection and dispute [31], CVE-to-CWE-to-CPE
mappings are unstable along the abstraction ladder [32], CVSS scores fragment across versions [39],
and the knowledge-graph literature treats vocabulary churn and instance-data usage as two distinct
time series [37].

Against that yardstick ATT&CK scores well on some axes and has nothing on others. Releases are
immutable and addressable [1, 55]. Retirement is typed and non-destructive: an object with a
successor is revoked and carries a `revoked-by` edge, one without is deprecated, and both are
retained so dependent workflows do not break [1]. MITRE ships `diffStix`, which computes
per-release change sets including a `patches` class for objects changed while the version field
stayed the same, and annotates unintended version changes as a known defect [34, 48]; ATT&CK Sync
flags mappings affected by a release [5]; and the Navigator layer format can record the ATT&CK
content version of a coverage layer [15]. What ATT&CK lacks is the inexact-successor relation, a
controlled obsolescence-reason vocabulary, label-level visibility of obsoletion, prior-version and
compatibility links, and a typed evolution mapping published as an artefact in its own right.
Sections 6.2 to 6.4 measure what each absence costs. One structural fact shapes everything
downstream: the largest editorial event in ATT&CK's history, the March 2020 introduction of
sub-techniques [47, 63], is — as Section 6.6 shows — one draw from a recurring per-domain hazard
rather than a closed event.

## 3. Related Work

Four literatures bear on this problem and none of them measures it.

**CTI quality.** A mature line of work defines quality dimensions and scores feeds against them:
completeness, accuracy, timeliness, relevance, provenance and interoperability recur across the
canonical treatments [60, 76], with dynamic assessment and weighted criteria added later [27],
empirical evaluations showing public feeds overlap little and age badly [41, 45], practitioner
quality assurance studied directly [40], community feeds metered [38], a 2025 measurement survey
consolidating the field [11], and format validity as a separate complaint [83]. None of these
frameworks names the reference vocabulary's version as a quality dimension. This is an audited
absence with a stated bound: across the sources reachable here we found no dimension defined over
the vocabulary edition, and we did not hold full text for all of them, so we claim the absence of a
named dimension rather than of awareness. The burden is conceded institutionally by the existence
of migration tooling [5, 81].

**ATT&CK-based analytics.** The SoK on ATT&CK establishes that coverage claims are not comparable
across products and flags temporal instability as open [63]; a 2025 survey sets the bar a
contribution must clear [47]. Virkud et al. demonstrate non-comparability empirically at a single
pinned release: vendor rules for the same behaviour carry disjoint technique labels, and
recomputing coverage from raw artefacts collapses the differences between products [74]. Shen et
al. show per-technique tallies are the wrong unit for MITRE's Evaluations [62], which themselves
refuse to emit a coverage score [46]; practitioners argue that a heatmap counts rules rather than
coverage and that incompatible denominators circulate [80, 82, 84]; Summiting the Pyramid replaces
techniques with implementations as the denominator [64]; and mitigation coverage has a ceiling set
by the control catalogue rather than the product [58]. All of this concerns disagreement at one
version; none of it measures what happens when the version changes.

**TTP extraction, benchmarks and attribution.** The extraction line runs from TTPDrill [71] through
rcATT [44] to TTPHunter and its successor [72], with graph-based systems alongside [2] and recent
multi-label treatments that decline to treat TRAM annotations as gold [52, 73]. LLM-era benchmarks
are now the dominant evaluation surface: CTIBench treats authoritative sources as fixed and
time-controls only its CVE task [30]; CTIArena grew into a successor with 691 to 1,860 QA pairs
under one identifier and the same nine-task taxonomy [29]; AthenaBench proposes live-API
construction against benchmark staleness [13]; SEvenLLM assembles 90k samples from two decades of
reports with no ATT&CK release declared [61]; SynthCTI synthesises the long tail [65]; CTI-REALM
grounds evaluation in telemetry, the only structurally drift-resistant design in the set [28]; and
answer-key decay has itself been quantified [75]. Attribution work has moved to TTP sequences [17,
23] and is surveyed by artefact type rather than ontology version [12], while two results bound
what it can do at all: roughly a third of ATT&CK groups have any group-specific technique [59], and
LLM agents reproduce documented APT profiles at 55-80% precision [66]. Extractor errors concentrate
among same-tactic, description-overlapping techniques [20]. The common feature, as Section 9 shows,
is a gold label space whose provenance is undeclared.

**Concept drift in security ML.** Dataset-shift taxonomies are formulated over a fixed label space
[33]; TESSERACT establishes temporal hygiene [67]; CADE explains drifting samples [22]; conformal
evaluation rejects under drift [70]; adaptation work assumes a fixed vocabulary [50]; and the
standard catalogue of security-ML pitfalls omits vocabulary versioning entirely [35]. Where the
label space itself changes, the machinery is class-incremental and continual learning with evolving
class ontologies [24, 43], the closest security instance being MOTIF's unstable family set [51],
with AVClass as prior art for alias resolution as normalization [19]. IncreTTP is the only work we
found framing ATT&CK version updates as concept drift, and its remedy is incremental learning
rather than measurement [42]. The boundary is the contribution point: concept drift is change in
P(y|x) with y fixed; ontology drift is change in the set y ranges over and in what its members mean
[21]. The novelty here is therefore not that ATT&CK changes but the quantification of what the
change costs a conclusion, under a design where nothing but the vocabulary moves.

## 4. Problem Formalization and Drift Taxonomy

Let an ATT&CK release be a triple `R_v = (L_v, ⊑_v, μ_v)`: `L_v` the set of live technique
identifiers; `⊑_v` the abstraction relation induced by `subtechnique-of` edges, with the
dotted-identifier convention as a fallback where the relationship is omitted; and `μ_v` the
intension map, sending each identifier to its description, detection guidance and assigned tactic
phases. A release also carries a retirement relation `ρ_v ⊆ L̄ × L_v` given by `revoked-by` edges,
`L̄` being the retired identifiers. A CTI artefact written at `v` is a multiset over `L_v` plus an
implicit commitment to `⊑_v` and `μ_v`, and is consumed at `w > v`. Four drift operators may have
acted in between, and any one can be zero while the others are large.

**D1 — extensional drift.** `L_v ≠ L_w`: identifiers added, revoked with a successor, deprecated
without one, or absent entirely. This is the only class a naive consumer notices, because it is the
only one that produces a failed lookup, and for Enterprise it is fully repairable by transitive
closure over `ρ_w`.

**D2 — structural drift.** `⊑_v ≠ ⊑_w` on shared identifiers, or a retirement crossing abstraction
levels: a parent re-cut into children, a sub-technique promoted, or — the pathological case — a
technique promoted to a tactic, which no technique-to-technique relation can express. It is partly
observable, since the abstraction level of both endpoints of a retirement edge is computable, so
the change can be detected where it cannot be repaired.

**D3 — intensional drift.** `μ_v(t) ≠ μ_w(t)` for `t ∈ L_v ∩ L_w`: the identifier survives, the
words change. Identifier arithmetic cannot see this by construction, and ATT&CK emits no reliable
signal for it (Section 6.4).

**D4 — relational drift.** The tactic assignment of a surviving technique changes, or the tactic
layer is re-cut. Formally a restriction of D3 to the kill-chain component of `μ`, it earns
separation because tactic identifiers carry no retirement edges at all (Section 6.3) and because
tactic-level aggregation is the commonest way coverage and profile statistics are reported.

Two artefacts are **version-comparable** when both have been projected onto one reference release
and the projection's residual is declared. Projection is `π_w : 2^{L_v} → 2^{L_w}`, transitive
closure over `ρ_w`. It is a function, not an injection: it can merge, and it can land on a
different abstraction level. The residual is the four-way ledger `(kept, merged, demoted, dropped)`,
and a protocol returning `π_w(S)` without it has destroyed exactly the information a reader needs
to judge comparability — the reporting failure this paper is about, and which Section 8 shows is
not hypothetical.

One caveat bounds every operator above. ATT&CK is a description of adversary behaviour, not the
behaviour; a rewritten description may track a real change in the threat landscape, an improvement
in the curator's understanding, or an editorial preference, and our measurements cannot
distinguish these. The claim is narrower and sufficient: whatever the reason, an artefact written
against the old text and scored against the new one is being measured with a recalibrated
instrument, and nothing in current publication practice records that this has happened.

## 5. Data and Methodology

This is a measurement study, so the instrument we use to measure the instrument is described in
enough detail to be rebuilt.

### 5.1 The release corpus

We clone MITRE's `attack-stix-data` repository, which publishes every ATT&CK release as an
immutable STIX 2.1 bundle at a stable path [1]. Its index enumerates 109 versioned bundle entries
across three domains — 41 Enterprise, 41 Mobile, 27 ICS. Our extraction materialises 106 distinct
domain-release pairs: 41 Enterprise, 38 Mobile, 27 ICS. The three-entry difference falls entirely
at Mobile v11.0 to v11.2, where the published Mobile sequence steps from v10.1 to v11.3. We report
both counts rather than adopting the convenient one, because the subject of this paper is what
undeclared denominators do to a measurement.

Each bundle is parsed into a SQLite database of four tables: `releases` (domain, version, ordinal,
date); `objects` (per domain and version, each STIX object's identifier, type, ATT&CK identifier,
name, sub-technique flag, revoked and deprecated flags, `x_mitre_version`, timestamps, kill-chain
phase shortnames, platforms, and SHA-256 digests and lengths of the description and detection
fields); `descriptions`, retaining both text fields in full so token similarity is computed exactly
rather than approximated from digests; and `relationships`, recording every typed edge.

Release-level analyses use **major releases only**: one release per major version, taken as the
`.0` release or the earliest available release of that version. This yields 19 Enterprise, 19
Mobile and 12 ICS analysis points and makes "per release" mean one thing across eras, which mixing
in irregular patch releases would not. Section 9 deliberately does the opposite and uses every
published release, because there the question is which release a label file could have been written
against, and excluding patch releases would bias the answer.

**Table 1.** The release corpus. Major releases are the analysis points for churn, survival and
drift; all releases are used for the label-validity analysis of Section 9.

| Domain | Releases analysed (major / all) | First | Last |
|---|---|---|---|
| Enterprise | 19 / 41 | v1.0 (2018-01-17) | v19.0 (2026-04-28) |
| Mobile | 19 / 38 | v1.0 (2018-01-17) | v19.0 (2026-04-28) |
| Ics | 12 / 27 | v8.0 (2020-10-27) | v19.0 (2026-04-28) |

### 5.2 Definitions of the measured quantities

**Live technique set.** `L_v` is the set of ATT&CK identifiers of `attack-pattern` objects in
release `v` with both the revoked and deprecated flags false. Every technique count below is
`|L_v|`, and every coverage denominator is `|L_v|` at the release the coverage is stated against.

**Identifier Jaccard.** For consecutive majors, `J(L_a, L_b) = |L_a ∩ L_b| / |L_a ∪ L_b|`. A
revoked technique is absent from `L_b` even though its object remains in the file, so a revocation
lowers `J` exactly as a deletion would — intended, because a revoked identifier is unusable as a
label.

**Survival and recoverability.** Survival from `v` to `w` is `|{t ∈ L_v : t ∈ L_w}| / |L_v|`. An
identifier is *recoverable* at `w` if it is revoked or absent there and following `revoked-by`
edges transitively (at most ten hops, cycle-safe) terminates in `L_w`. Half-life is the first
target release at which survival falls below 0.5, reported with elapsed years.

**Semantic drift.** For identifiers live in both releases, "description edited" is inequality of
the SHA-256 digests of the description strings. Token similarity is the Jaccard index over sets of
lowercased alphanumeric tokens matched by `[a-z0-9]+`; a *substantial rewrite* is token Jaccard
below 0.8, a convention beside which we report the full mean-similarity series. Set Jaccard over
bags of words is deliberately crude: monotone in shared vocabulary, model-free, and unable to
import an embedding's own drift into a measurement of drift.

**Version-metadata reliability.** For each consecutive major pair we take the techniques live in
both and cross-tabulate "description text changed" against "`x_mitre_version` incremented".
Treating an increment as a detector of text change gives precision = (changed and bumped) / (all
bumped) and recall = (changed and bumped) / (all changed) — the two numbers deciding whether a
consumer can use the version field to know what to re-read.

**Growth decomposition.** Every group-to-technique `uses` edge present in `b` and absent in `a` is
assigned one cause, tested in this order: *new actor* if the group is absent from `a`; *revocation
re-mapping* if a technique already credited to that group in `a` resolves transitively onto this
one in `b`; *sub-technique refinement* if the technique is new in `b` and its parent was already
credited to the group; *new technique intelligence* if it is new in `b` and not such a refinement;
*genuine new intelligence* if both endpoints existed in `a` unlinked. The *bookkeeping share* is
(refinement + re-mapping) over all new edges for pre-existing groups. Test order is conservative in
the direction that matters — re-mapping is tested first, so an ambiguous edge is charged to
bookkeeping — and new actors are excluded from the denominator because a newly documented intrusion
set is unambiguously new intelligence.

### 5.3 The four downstream experiments

All four hold the adversary intelligence fixed and vary only the vocabulary, which is what makes
the contrasts attributable to the instrument.

**Attribution (Section 7.1).** The analysis release is v19.0 throughout. For a legacy vocabulary
`v`, every *modern* group profile is back-projected into `v` by a map built once per pair: a modern
technique maps to itself if live at `v`; else to the pre-revocation identifier that resolves onto
it, lexicographically first if several do; else to the nearest ancestor under `⊑_w` live at `v`,
climbing at most five hops; else it is dropped as a behaviour with no `v`-era expression. The
candidate universe is groups present in both releases with at least `k` techniques at `w` and two
at `v`. Each of 500 trials samples a group uniformly, samples `k` = 10 techniques from its modern
profile, and scores four conditions over identical draws and an identical candidate set:
*back-projected* (`v`-vocabulary observation against `v`-vocabulary profiles), *naive*
(`v`-vocabulary observation against modern profiles), *ATT&CK-Norm* (observation projected forward,
then against modern profiles), and *oracle* (modern observation against modern profiles). Scoring
is IDF-weighted cosine over technique sets, IDF computed within each condition's own profile set,
ties broken on a fixed group ordering. The **drift penalty** is back-projected minus naive top-1
accuracy; **recovery** is (ATT&CK-Norm − naive) / (back-projected − naive); intervals are paired
bootstrap over trials with 2,000 resamples. A fifth *historical* condition draws from the real
archival `v`-era profile and is a diagnostic only, mixing drift with genuine intelligence change.
Two properties bound every absolute number: the back-projected condition is a reconstruction, not a
v-era system, and observations are drawn from the profile, so recall is perfect by construction
(Section 11).

**Coverage (Section 7.2).** A capability is frozen at release `v` as the live techniques reachable
by `mitigates` (or `detects`) edges there, and never changes again. Its coverage is recomputed
against v19.0 naively (raw identifiers against the modern live set, over the modern denominator)
and after normalization. Portfolios below 20 techniques are excluded. A sweep of 500 random 30%
samples of each release's live set gives the distribution of the artefact independently of what
MITRE happened to write mitigations for.

**Conclusion instability (Sections 7.3 and 7.5).** Two readouts sit on the same machinery: the
share of attribution trials in which the *named actor* differs between conditions, decomposed by
whether the new verdict is wrong and whether a correct one was lost; and the Kendall tau between
mitigations ranked by techniques addressed at the frozen release and the same set re-measured at
v19.0, with the top-ranked mitigation tracked separately.

**Label validity (Section 9).** Four deployed corpora are parsed from their own label files, not
their papers. Every distinct identifier is checked for liveness at every published release of the
domain the artefact assigns it, or of any domain where it declares none. The *best-fit release*
maximises the share of distinct identifiers live; the *provenance interval* is the set of releases
at which **every** identifier is simultaneously live, and an empty interval is the diagnostic that
the artefact mixes mutually exclusive vocabularies.

### 5.4 Reproducibility and evidence tiers

Every number in Sections 6 to 9 is produced by a script in `code/` from public bundles and label
files; the pipeline runs end to end from one shell script, writes JSON, and the tables here are
generated from that JSON rather than transcribed. Three evidence tiers are marked throughout:
Tier A, our own measurements and artefacts read in full from local clones; Tier B, secondary
literature reachable here only through search summaries, attributed as reported and never quoted;
Tier C, audited absences, stated with the bound of the search that found them.

## 6. Measuring Ontology Drift in ATT&CK

### 6.1 Churn: one catastrophe and a floor that never reaches zero

**Figure 1.** Live technique count across Enterprise releases, with per-release additions,
revocations and description rewrites on a shared time axis.

Table 2 is the primary measurement of this paper and most of the rest follows from it.

**Table 2.** Per-release Enterprise churn across consecutive major releases. "Live" is the
technique count after the transition; the rewrite and tactic columns count only techniques live in
both releases; `J(ID)` is the identifier Jaccard; "Edges" counts group-to-technique `uses` edges
added and removed.

| Transition | Date | Live | Added | Revoked | Deprecated | Renamed | Desc. rewritten | Detection rewritten | Tactic changed | J(ID) | Edges +/- |
|---|---|---|---|---|---|---|---|---|---|---|---|
| v1.0→v2.0 | 2018-04-18 | 219 | 31 | 0 | 0 | 2 | 28 | 0 | 5 | 0.858 | +135/−0 |
| v2.0→v3.0 | 2018-10-23 | 223 | 4 | 0 | 0 | 1 | 219 | 218 | 4 | 0.982 | +285/−0 |
| v3.0→v4.0 | 2019-04-30 | 244 | 21 | 0 | 0 | 1 | 27 | 10 | 1 | 0.914 | +237/−2 |
| v4.0→v5.0 | 2019-07-19 | 244 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 1.000 | +100/−0 |
| v5.0→v6.0 | 2019-10-23 | 266 | 22 | 0 | 0 | 2 | 60 | 24 | 2 | 0.917 | +102/−0 |
| v6.0→v7.0 | 2020-03-31 | 428 | 302 | 129 | 11 | 17 | 106 | 60 | 10 | 0.222 | +1235/−750 |
| v7.0→v8.0 | 2020-10-27 | 525 | 97 | 0 | 0 | 3 | 34 | 17 | 0 | 0.815 | +102/−2 |
| v8.0→v9.0 | 2021-04-29 | 552 | 27 | 0 | 0 | 6 | 149 | 52 | 5 | 0.951 | +642/−2 |
| v9.0→v10.0 | 2021-10-21 | 566 | 15 | 0 | 1 | 2 | 76 | 66 | 0 | 0.972 | +312/−1 |
| v10.0→v11.0 | 2022-04-25 | 576 | 12 | 2 | 0 | 9 | 151 | 44 | 0 | 0.976 | +288/−1 |
| v11.0→v12.0 | 2022-10-25 | 594 | 18 | 0 | 0 | 2 | 50 | 0 | 0 | 0.970 | +252/−0 |
| v12.0→v13.0 | 2023-04-25 | 607 | 13 | 0 | 0 | 1 | 87 | 13 | 0 | 0.979 | +112/−16 |
| v13.0→v14.0 | 2023-10-31 | 625 | 18 | 0 | 0 | 1 | 41 | 2 | 6 | 0.971 | +178/−1 |
| v14.0→v15.0 | 2024-04-23 | 637 | 12 | 0 | 0 | 3 | 98 | 4 | 0 | 0.981 | +208/−34 |
| v15.0→v16.0 | 2024-10-31 | 656 | 19 | 0 | 0 | 1 | 61 | 0 | 0 | 0.971 | +417/−14 |
| v16.0→v17.0 | 2025-04-22 | 679 | 24 | 1 | 0 | 5 | 79 | 5 | 2 | 0.963 | +313/−558 |
| v17.0→v18.0 | 2025-10-28 | 691 | 12 | 0 | 0 | 2 | 49 | 583 | 0 | 0.983 | +328/−11 |
| v18.0→v19.0 | 2026-04-28 | 697 | 23 | 17 | 0 | 4 | 41 | 0 | 198 | 0.944 | +270/−86 |

Read the identifier column alone and the episodic reading is irresistible. One transition, v6.0 to
v7.0 on 2020-03-31, has an identifier Jaccard of 0.222, adds 302 techniques, revokes 129 and
deprecates 11, and rewrites the group-technique graph by removing 750 edges and adding 1235. The
next largest Jaccard drop in eight years is 0.944, at the most recent transition.

Read any other column and that reading collapses. Description rewrites among surviving techniques
never fall below 27 in any transition, reaching 219 of 223 at v2.0 to v3.0 and 151 at v10.0 to
v11.0, whose identifier Jaccard is 0.976. Detection rewrites are burstier: 583 of 691 surviving
techniques had their detection text rewritten between v17.0 and v18.0, a transition whose
identifier Jaccard is 0.983 and whose description-rewrite count is 49. That one release rewrote
the operational guidance of 84% of the catalogue, and any identifier-keyed diff would report it
among the quietest in ATT&CK's history. The tactic column, near-empty for sixteen transitions,
reads 198 at the most recent one. This two-clock structure is the first result: a slow episodic
identifier clock and a fast continuous semantic clock, so any risk statement reporting one without
the other is wrong by a factor set entirely by which column the reader happened to read.

### 6.2 Survival: the concession, measured

**Figure 2.** Identifier survival curves by source release to v19.0, with the recoverable fraction
under transitive `revoked-by` closure overlaid.

**Table 3.** Identifier survival to v19.0 by source release. "Recoverable" counts revoked or absent
identifiers whose transitive `revoked-by` closure terminates at a live identifier.

| Source release | Date | Identifiers | Live at v19.0 | Survival | Revoked | Deprecated | Recoverable | Half-life |
|---|---|---|---|---|---|---|---|---|
| v1.0 | 2018-01-17 | 188 | 77 | 0.410 | 100 | 11 | 100 | v7.0 (2.2 y) |
| v2.0 | 2018-04-18 | 219 | 97 | 0.443 | 111 | 11 | 111 | v7.0 (2.0 y) |
| v3.0 | 2018-10-23 | 223 | 100 | 0.448 | 112 | 11 | 112 | v7.0 (1.4 y) |
| v4.0 | 2019-04-30 | 244 | 113 | 0.463 | 120 | 11 | 120 | v7.0 (0.9 y) |
| v5.0 | 2019-07-19 | 244 | 113 | 0.463 | 120 | 11 | 120 | v7.0 (0.7 y) |
| v6.0 | 2019-10-23 | 266 | 126 | 0.474 | 129 | 11 | 129 | v7.0 (0.4 y) |
| v7.0 | 2020-03-31 | 428 | 415 | 0.970 | 12 | 1 | 12 | not reached |
| v8.0 | 2020-10-27 | 525 | 511 | 0.973 | 13 | 1 | 13 | not reached |
| v9.0 | 2021-04-29 | 552 | 538 | 0.975 | 13 | 1 | 13 | not reached |
| v10.0 | 2021-10-21 | 566 | 551 | 0.973 | 15 | 0 | 15 | not reached |
| v11.0 | 2022-04-25 | 576 | 563 | 0.977 | 13 | 0 | 13 | not reached |
| v12.0 | 2022-10-25 | 594 | 581 | 0.978 | 13 | 0 | 13 | not reached |
| v13.0 | 2023-04-25 | 607 | 593 | 0.977 | 14 | 0 | 14 | not reached |
| v14.0 | 2023-10-31 | 625 | 609 | 0.974 | 16 | 0 | 16 | not reached |
| v15.0 | 2024-04-23 | 637 | 621 | 0.975 | 16 | 0 | 16 | not reached |
| v16.0 | 2024-10-31 | 656 | 640 | 0.976 | 16 | 0 | 16 | not reached |
| v17.0 | 2025-04-22 | 679 | 663 | 0.976 | 16 | 0 | 16 | not reached |
| v18.0 | 2025-10-28 | 691 | 674 | 0.975 | 17 | 0 | 17 | not reached |
| v19.0 | 2026-04-28 | 697 | 697 | 1.000 | 0 | 0 | 0 | not reached |

The recoverable column equals the revoked column in every one of the 190 Enterprise survival rows,
and the absent count is zero in every row. Recomputing from the v19.2 bundle gives 858
`attack-pattern` objects — 697 live, 149 revoked, 12 deprecated — and 149 `revoked-by` edges from
149 distinct sources. Every revoked Enterprise technique has exactly one successor and none dangle.
MITRE's Enterprise identifier accounting is complete, and we concede it without qualification,
because conceding it is what makes the remaining argument non-trivial: a reader holding the usage
documentation can defeat any weaker claim in one paragraph [1].

Each boundary of that concession is a finding. It is Enterprise-only: in Mobile, 34 survival rows
record identifiers absent rather than tombstoned, and all 76 techniques of Mobile v1.0 are gone
from v3.0 onward with no successor edge of any kind (Section 6.6). The relation is never
one-to-many, so a *split* is representable only as merges onto whichever survivor the curator
judges narrowest: eight Enterprise targets absorb 20 predecessor identifiers, the largest — T1685
— absorbing five, and three chains need transitive closure. And retirement routinely crosses
abstraction levels: of the 149 edges, 119 map a top-level technique onto a sub-technique, 13 top
onto top, 10 sub onto sub, and 7 *promote* a sub-technique to a parent. A crosswalk that resolves in
one hop onto a live identifier, reports success, and silently narrows the original assertion is not
broken; it is a 1:1 relation in a situation needing more, which is why the remedy in Section 10 is
borrowed from a framework separating exact from inexact successors [54].

### 6.3 The tactic layer, and the one move no crosswalk can express

Across all three domains and every release our extraction finds 5,599 revocation edges. Zero of
them involve an `x-mitre-tactic` object: the tactic layer has no retirement relation at all.

This is not a theoretical gap. Between v18.1 and v19.2 the STIX object carrying TA0005 keeps its
UUID and its ATT&CK identifier while its name changes from *Defense Evasion* to *Stealth*, its
shortname from `defense-evasion` to `stealth`, and its `x_mitre_version` stays at 1.0. A new tactic
TA0112, *Defense Impairment*, is minted alongside to hold the separated concept, and T1562 *Impair
Defenses* — a top-level technique with twelve children — is retired into the new arrangement [78].
Any analytic joining on TA0005 across that boundary compares two different concepts, with no
revocation, no version increment and no edge to follow. Our corpus finds 102 in-place renames
across all object types, and each domain's tactic layer contains one: TA0005 in Enterprise, TA0034
in Mobile (*Effects* to *Impact*), both with unchanged object versions. This is the edit OBO
Foundry's term-stability principle exists to forbid [54].

The technique-level consequence is the merge pattern of Section 6.2 at its sharpest. `revoked-by`
cannot point a technique at a tactic, so the promoted concept *Impair Defenses* is mapped to T1685
*Disable or Modify Tools* — one of its own former children — resolving in one hop, onto a live
identifier, dropping nothing. An analyst who wrote T1562 because a report said the actor disabled a host firewall is
thereby recorded as asserting that the actor tampered with security tooling: a narrower and
different claim, in a tactic that did not exist when the artefact was written. The mechanism
reports success; the measurement is wrong.

### 6.4 Intensional drift, and why ATT&CK cannot signal it

**Figure 3.** Silent semantic drift among identifier-stable techniques: share with edited
descriptions and share substantially rewritten, by source release, measured at v19.0.

**Table 4.** Semantic drift among techniques live at both the source release and v19.0. Token
Jaccard is computed over lowercased alphanumeric token sets of the description; a substantial
rewrite is token Jaccard below 0.8.

| Source release | ID-stable techniques | Description edited | Mean token Jaccard | Substantial rewrite (J<0.8) |
|---|---|---|---|---|
| v1.0 | 77 | 1.000 | 0.345 | 1.000 |
| v2.0 | 97 | 1.000 | 0.373 | 1.000 |
| v3.0 | 100 | 0.960 | 0.553 | 0.830 |
| v4.0 | 113 | 0.965 | 0.548 | 0.841 |
| v5.0 | 113 | 0.965 | 0.548 | 0.841 |
| v6.0 | 126 | 0.968 | 0.569 | 0.817 |
| v7.0 | 415 | 0.749 | 0.808 | 0.386 |
| v8.0 | 511 | 0.767 | 0.830 | 0.337 |
| v9.0 | 538 | 0.645 | 0.849 | 0.310 |
| v10.0 | 551 | 0.593 | 0.866 | 0.278 |
| v11.0 | 563 | 0.465 | 0.895 | 0.208 |
| v12.0 | 581 | 0.439 | 0.906 | 0.189 |
| v13.0 | 593 | 0.386 | 0.928 | 0.140 |
| v14.0 | 609 | 0.366 | 0.938 | 0.123 |
| v15.0 | 621 | 0.275 | 0.956 | 0.087 |
| v16.0 | 640 | 0.211 | 0.969 | 0.062 |
| v17.0 | 663 | 0.124 | 0.985 | 0.024 |
| v18.0 | 674 | 0.061 | 0.997 | 0.003 |

Table 4 must be read as a function of elapsed time, not of release quality: the v18.0 row is low
because one transition separates it from the analysis release, not because ATT&CK stopped
rewriting. The right reading is cohort decay. Of the 415 techniques live at v7.0 and still live at
v19.0, 0.749 have had their descriptions edited and 0.386 rewritten past the substantial
threshold, at mean token similarity 0.808. For the v11.0 cohort: 0.465, 0.208, 0.895. For v15.0:
0.275, 0.087, 0.956. These are identifiers whose survival over the same interval is 0.977 and
0.975. The instrument keeps the scale markings and moves what they mean.

On a practitioner's clock the two clocks run in opposite directions. For every Enterprise cohort
from v7.0 onward the time to 10% *hard* identifier staleness is never, and the unrecoverable
fraction is at most 0.2%. The time to 10% *substantive* staleness — gone, substantially rewritten,
or reassigned to another tactic — is 0.50 to 2.01 years, median 1.51. Restricting to text change
alone, excluding tactic changes and revocations so the recent re-cut cannot be blamed, gives 0.99
to 2.01 years, median 1.52, against a semantic half-life of 4.5 to 6.1 years. A pinned post-2020
Enterprise label set therefore has an infinite identifier half-life and an eighteen-month
first-10% semantic staleness schedule at the same time.

Could a consumer detect this from the bundles? ATT&CK carries `x_mitre_version` on every object,
and the natural assumption is that a change in meaning is announced there. It is not.

**Table 13.** Text change versus version increment for techniques live in both releases of a
consecutive major pair, Enterprise.

| Transition | Techniques live in both | Text changed, version bumped | Text changed, no bump | Bump, no text change | Neither |
|---|---|---|---|---|---|
| v1.0→v2.0 | 188 | 0 | 28 | 0 | 160 |
| v2.0→v3.0 | 219 | 0 | 219 | 0 | 0 |
| v3.0→v4.0 | 223 | 15 | 12 | 7 | 189 |
| v4.0→v5.0 | 244 | 0 | 2 | 0 | 242 |
| v5.0→v6.0 | 244 | 53 | 7 | 12 | 172 |
| v6.0→v7.0 | 126 | 94 | 12 | 0 | 20 |
| v7.0→v8.0 | 428 | 26 | 8 | 46 | 348 |
| v8.0→v9.0 | 525 | 55 | 94 | 64 | 312 |
| v9.0→v10.0 | 551 | 73 | 3 | 98 | 377 |
| v10.0→v11.0 | 564 | 114 | 37 | 31 | 382 |
| v11.0→v12.0 | 576 | 47 | 3 | 31 | 495 |
| v12.0→v13.0 | 594 | 81 | 6 | 58 | 449 |
| v13.0→v14.0 | 607 | 38 | 3 | 80 | 486 |
| v14.0→v15.0 | 625 | 73 | 25 | 46 | 481 |
| v15.0→v16.0 | 637 | 56 | 5 | 104 | 472 |
| v16.0→v17.0 | 655 | 79 | 0 | 304 | 272 |
| v17.0→v18.0 | 679 | 45 | 4 | 17 | 613 |
| v18.0→v19.0 | 674 | 22 | 19 | 179 | 454 |
| **All** | **8359** | **871** | **487** | **1077** | **5924** |

Over 8,359 carried-over technique pairs, 1,358 (0.162) had their description rewritten, of which
487 (0.359) carried no version increment; in the other direction 1,077 version increments carried
no text change at all. As a detector of description change, `x_mitre_version` has **precision 0.447
and recall 0.641**. A consumer who re-reads every technique whose version increased does more than
half that work for nothing and still misses over a third of the changes. MITRE's own tooling knows
this — `diffStix` defines a change class for objects patched while the version stayed the same [34,
48] — while the contract consumers follow offers a binary current-or-retired filter and no
expression for a surviving object whose meaning moved [1]. The gap is architectural: the tooling
sees the change and the published consumer interface has no vocabulary in which to state it. This
is the paper's central negative result and the answer to the strongest practical objection in the
field: pinning a release is correct and insufficient, because it fixes identity, not intension, and
no published signal reliably says when intension has moved.

### 6.5 How much of ATT&CK's growth is intelligence?

**Figure 4.** Per-transition decomposition of new group-technique edges for pre-existing groups
into genuine new intelligence, new technique, sub-technique refinement and revocation re-mapping.

**Table 5.** Knowledge-growth decomposition, Enterprise. Edges for groups newly added to ATT&CK are
excluded from the denominator; bookkeeping share is (refinement + re-mapping) over all new edges
for pre-existing groups.

| Transition | New edges (pre-existing groups) | Genuine new intel | New technique | Sub-technique refinement | Revocation re-mapping | Bookkeeping share |
|---|---|---|---|---|---|---|
| v1.0→v2.0 | 36 | 12 | 24 | 0 | 0 | 0.000 |
| v2.0→v3.0 | 123 | 121 | 2 | 0 | 0 | 0.000 |
| v3.0→v4.0 | 144 | 134 | 10 | 0 | 0 | 0.000 |
| v4.0→v5.0 | 33 | 33 | 0 | 0 | 0 | 0.000 |
| v5.0→v6.0 | 30 | 21 | 9 | 0 | 0 | 0.000 |
| v6.0→v7.0 | 1059 | 78 | 187 | 390 | 404 | 0.750 |
| v7.0→v8.0 | 81 | 57 | 24 | 0 | 0 | 0.000 |
| v8.0→v9.0 | 285 | 270 | 11 | 4 | 0 | 0.014 |
| v9.0→v10.0 | 187 | 183 | 3 | 1 | 0 | 0.005 |
| v10.0→v11.0 | 231 | 223 | 4 | 0 | 4 | 0.017 |
| v11.0→v12.0 | 43 | 39 | 2 | 2 | 0 | 0.047 |
| v12.0→v13.0 | 71 | 39 | 5 | 27 | 0 | 0.380 |
| v13.0→v14.0 | 48 | 44 | 3 | 1 | 0 | 0.021 |
| v14.0→v15.0 | 100 | 62 | 4 | 34 | 0 | 0.340 |
| v15.0→v16.0 | 182 | 164 | 4 | 14 | 0 | 0.077 |
| v16.0→v17.0 | 134 | 95 | 10 | 9 | 20 | 0.216 |
| v17.0→v18.0 | 123 | 105 | 13 | 5 | 0 | 0.041 |
| v18.0→v19.0 | 164 | 72 | 15 | 0 | 77 | 0.470 |
| **All transitions** | **3074** | **1752** | **330** | **487** | **505** | **0.323** |

Across all Enterprise transitions 5,516 group-technique edges are added, of which 2,442 belong to
groups newly added to ATT&CK. Of the remaining 3,074 added for pre-existing groups, 1,752 are
genuine new intelligence about a pre-existing pairing, 330 credit a group with a newly minted
technique, 487 are sub-technique refinements of an edge the group already had, and 505 restate an
edge whose technique was revoked and replaced. The bookkeeping share is **992/3074 = 0.323**.

The headline conceals a heavy tail, and the tail is the point. The restructuring transition is
0.750 bookkeeping over 1,059 edges and eight transitions are below 0.05, but three recent ones are
not: 0.380 at v12.0 to v13.0, 0.340 at v14.0 to v15.0, and **0.470 over 164 edges** at v18.0 to
v19.0 — the highest share since the restructuring, driven entirely by 77 revocation re-mappings. A
reader who plots ATT&CK's edge count as a curve of accumulating adversary knowledge is reading a
curve roughly a third bookkeeping overall and nearly half bookkeeping in the release that shipped
four months before this analysis. The benchmark side agrees: the 4.3x label-space growth between
one LLM CTI benchmark generation and its successor is roughly 96% pre-existing catalogue, with only
six genuinely new entries [6].

### 6.6 Recurrence: this is a hazard, not a wound

The episodic reading has one defence left: that the 2020 restructuring was singular and finished.
Extending the measurement to all three domains refutes it. Five major-to-major transitions have
identifier Jaccard below 0.80: Mobile v2.0 to v3.0 (2018-10-23, J = 0.000), Enterprise v6.0 to
v7.0 (2020-03-31, J = 0.222), ICS v8.0 to v9.0 (2021-04-29, J = 0.778), Mobile v10.0 to v11.3
(2022-07-07, J = 0.268) and ICS v18.0 to v19.0 (2026-04-28, J = 0.698). That is 5 events in 47
transitions, a hazard of **0.106 per major transition**, one event per 4.41 domain-years over
22.05 observed domain-years — roughly one restructuring somewhere in ATT&CK every 1.5 calendar
years.

Two events matter more than their Jaccard suggests. Mobile's 2018 event is the most destructive in
the corpus and predates the Enterprise restructuring: a wholesale ATT&CK-ID renumbering in which
all 128 STIX identifiers are preserved but all 76 old ATT&CK identifiers vanish, with only 15
`revoked-by` edges in the target release and **zero** of the 76 recoverable. It is invisible to
STIX-identifier-keyed tooling and uncrosswalkable by any mechanism MITRE publishes. And the ICS
event is happening now: v19 revokes nine T0xxx techniques into a shared namespace and introduces
ICS sub-techniques for the first time — 0 at v18.1, 18 at v19.0 — structurally the move Enterprise
made in 2020, six years later, with all nine remaps recoverable.

Can a consumer see one coming? Correlating each candidate feature at transition *k* with the
revocation rate at *k+1* over 17 lagged Enterprise pairs (Spearman ρ, 20,000-shuffle permutation
tests), the largest coefficient is detection-field edits at ρ = +0.377, *p* = 0.134; nothing else
comes close and tactic changes correlate negatively. The largest coefficient in the three-domain
panel, ICS renames at ρ = +0.733, has *p* = 0.054 on *n* = 10. Technique-level hazard modelling is
worse than null: the 131 techniques doomed at v7.0 had been *edited less* than survivors
beforehand, on description edits (0.168 against 0.336) and version bumps (0.176 against 0.372).
Restructuring waves are not forecastable from the public bundles — a load-bearing negative result,
because it removes the triggered response: a consumer cannot time-hedge, so a protocol that helps
must be standing.

### 6.7 The most recent wave, measured as a case

The v18.1 to v19.2 wave is the cleanest test of whether drift still lands on things that matter.
Seventeen live techniques were revoked, including the whole T1562 family, re-cut across T1684 to
T1690 [78]. On the v18.1 graph the blast radius is 84 group-technique edges, 155 software-technique
edges, 47 mitigations and 17 detection relationships, and 52 of 168 group profiles lose at least
one identifier — and T1562.001 was ranked **33 of 599** techniques by `uses` edges in the release
it left. This is not the long tail; Section 7.6 settles that objection.

## 7. Downstream Impact of Drift on CTI Analytics

Section 6 measured the instrument. This section measures what the recalibration does to
conclusions drawn with it. Every experiment holds the adversary intelligence fixed and moves only
the vocabulary, so every difference below is attributable to the instrument and to nothing else.

### 7.1 Attribution under vocabulary mismatch

**Figure 5.** Top-1 attribution accuracy by condition against the artefact's vocabulary release,
with the drift penalty and its bootstrap confidence band.

**Table 6.** Controlled attribution experiment at k = 10, analysis release v19.0. "OOV" is the
share of observed identifiers not live at v19.0. The drift penalty is back-projected minus naive;
recovery is the share of that penalty returned by ATT&CK-Norm.

| Artefact vocabulary | k | Groups | OOV | Contemporaneous | Naive | ATT&CK-Norm | Oracle | Drift penalty (pp) [95% CI] | Recovered |
|---|---|---|---|---|---|---|---|---|---|
| v1.0 (2018-01-17) | 10 | 47 | 0.256 | 0.696 | 0.274 | 0.450 | 0.912 | 42.2 [37.8, 46.8] | 0.42 |
| v2.0 (2018-04-18) | 10 | 55 | 0.256 | 0.624 | 0.252 | 0.414 | 0.908 | 37.2 [32.6, 41.8] | 0.44 |
| v3.0 (2018-10-23) | 10 | 64 | 0.262 | 0.658 | 0.236 | 0.448 | 0.874 | 42.2 [37.6, 46.6] | 0.50 |
| v4.0 (2019-04-30) | 10 | 70 | 0.264 | 0.684 | 0.206 | 0.420 | 0.878 | 47.8 [42.8, 52.6] | 0.45 |
| v5.0 (2019-07-19) | 10 | 75 | 0.267 | 0.648 | 0.198 | 0.432 | 0.872 | 45.0 [40.4, 49.6] | 0.52 |
| v6.0 (2019-10-23) | 10 | 78 | 0.283 | 0.684 | 0.222 | 0.468 | 0.850 | 46.2 [41.6, 51.0] | 0.53 |
| v7.0 (2020-03-31) | 10 | 88 | 0.013 | 0.810 | 0.740 | 0.750 | 0.862 | 7.0 [4.4, 9.8] | 0.14 |
| v8.0 (2020-10-27) | 10 | 90 | 0.014 | 0.834 | 0.804 | 0.806 | 0.858 | 3.0 [0.8, 5.2] | 0.07 |
| v9.0 (2021-04-29) | 10 | 102 | 0.016 | 0.836 | 0.804 | 0.816 | 0.868 | 3.2 [1.2, 5.4] | 0.37 |
| v10.0 (2021-10-21) | 10 | 110 | 0.014 | 0.818 | 0.794 | 0.800 | 0.860 | 2.4 [0.6, 4.4] | 0.25 |
| v11.0 (2022-04-25) | 10 | 113 | 0.016 | 0.780 | 0.768 | 0.772 | 0.822 | 1.2 [-0.6, 3.2] | 0.33 |
| v12.0 (2022-10-25) | 10 | 123 | 0.011 | 0.840 | 0.820 | 0.832 | 0.878 | 2.0 [0.6, 3.8] | 0.60 |
| v13.0 (2023-04-25) | 10 | 126 | 0.013 | 0.832 | 0.798 | 0.810 | 0.836 | 3.4 [1.8, 5.2] | 0.35 |
| v14.0 (2023-10-31) | 10 | 131 | 0.017 | 0.828 | 0.814 | 0.832 | 0.850 | 1.4 [-0.4, 3.2] | 1.29 |
| v15.0 (2024-04-23) | 10 | 138 | 0.013 | 0.834 | 0.818 | 0.826 | 0.842 | 1.6 [0.4, 3.0] | 0.50 |
| v16.0 (2024-10-31) | 10 | 149 | 0.014 | 0.806 | 0.794 | 0.800 | 0.818 | 1.2 [0.0, 2.4] | 0.50 |
| v17.0 (2025-04-22) | 10 | 156 | 0.014 | 0.814 | 0.802 | 0.816 | 0.820 | 1.2 [0.4, 2.2] | 1.17 |
| v18.0 (2025-10-28) | 10 | 161 | 0.015 | 0.860 | 0.844 | 0.858 | 0.858 | 1.6 [0.6, 2.8] | 0.88 |

The structure of Table 6 mirrors the structure of Table 3, which is the point: the downstream
effect tracks the instrument, not the adversary. A legacy artefact in the v1.0 vocabulary
consumed by a v19.0 analytic loses 42.2 points of top-1 accuracy relative to the same
intelligence consumed in its own vocabulary, interval [37.8, 46.8]; at v6.0 the penalty is 46.2
[41.6, 51.0]. After the restructuring it collapses to 7.0 at v7.0 and settles between 1.2 and 3.4
points, with the interval touching or crossing zero at v11.0, v14.0 and v16.0.

The obvious reading — that the modern penalty is negligible, so the problem is historical — fails
on its own arithmetic. A 1.6-point penalty at v18.0 is *one release boundary*, six months: a
per-release increment, not an asymptote, and the artefacts the field consumes are years old
(Section 9). The aggregate also hides its concentration. Stratifying the candidate universe by
whether a group has at least one technique unique to it, the modern penalty is 2.5 to 7 times
larger on the identifiable stratum: +0.0344 [+0.0101, +0.0607]
against +0.0089 [−0.0010, +0.0189] at v12.0; +0.0331 [+0.0166, +0.0497] against +0.0049 [−0.0010,
+0.0118] at v16.0; +0.0239 [+0.0109, +0.0391] against +0.0067 [+0.0019, +0.0125] at v18.0. The
specificity fractions our corpus computes independently — 0.325, 0.309, 0.298 — reproduce the
published finding that roughly a third of ATT&CK groups have any group-specific technique [59].
The mechanism is immediate: a group's identifying token is by definition a rare technique, and rare
techniques are the ones ATT&CK adds, splits and revokes. Drift attacks precisely the signal
attribution depends on, and an average over a mostly unattributable population understates the
effect on the subset carrying the task.

The legacy penalties, conversely, must not be over-read: the back-projection collapses dense
modern profiles onto a coarse pre-2020 vocabulary and makes them collide in a way no 2018 system
experienced. The missing control — real archival labels against real archival profiles — gives
self-consistency 0.969 at v1.0 against the back-projected condition's 0.668, and 0.900 against
0.663 at v6.0, converging in the modern regime (0.856 against 0.837 at v12.0; 0.846 against 0.841
at v18.0). Back-projection loss is reported directly: at v1.0, 389 of 697 modern techniques have
no v1.0 ancestor and profiles retain 0.618 of their distinct identifiers; at v7.0, 155 of 697 and
0.903; at v18.0, 7 of 697 and 0.998. All three legacy conditions consume the same lossy
observation, so the contrast between them is clean even where their absolute level is not. That is
the reading we defend: every absolute number in Table 6 is an internal-consistency score inside one
curator's graph, and what the design licenses is the *contrast*.

### 7.2 Robustness: the penalty is not an artefact of one scorer

**Table 7.** Robustness across scoring functions and profile definitions. "Software-mediated"
indicates whether techniques reached through a group's malware and tools are folded into its
profile.

| Vocabulary | Scorer | Software-mediated | Contemporaneous | Naive | ATT&CK-Norm | Drift penalty (pp) | Norm. gain (pp) |
|---|---|---|---|---|---|---|---|
| v1.0 | idf-cosine | yes | 0.693 | 0.237 | 0.443 | 45.7 | 20.7 |
| v1.0 | idf-cosine | no | 0.877 | 0.433 | 0.713 | 44.3 | 28.0 |
| v1.0 | jaccard | yes | 0.447 | 0.260 | 0.390 | 18.7 | 13.0 |
| v1.0 | jaccard | no | 0.663 | 0.397 | 0.510 | 26.7 | 11.3 |
| v1.0 | overlap | yes | 0.240 | 0.033 | 0.103 | 20.7 | 7.0 |
| v1.0 | overlap | no | 0.790 | 0.337 | 0.573 | 45.3 | 23.7 |
| v6.0 | idf-cosine | yes | 0.690 | 0.190 | 0.473 | 50.0 | 28.3 |
| v6.0 | idf-cosine | no | 0.907 | 0.410 | 0.730 | 49.7 | 32.0 |
| v6.0 | jaccard | yes | 0.433 | 0.227 | 0.377 | 20.7 | 15.0 |
| v6.0 | jaccard | no | 0.700 | 0.337 | 0.597 | 36.3 | 26.0 |
| v6.0 | overlap | yes | 0.297 | 0.050 | 0.110 | 24.7 | 6.0 |
| v6.0 | overlap | no | 0.897 | 0.330 | 0.623 | 56.7 | 29.3 |
| v7.0 | idf-cosine | yes | 0.780 | 0.727 | 0.737 | 5.3 | 1.0 |
| v7.0 | idf-cosine | no | 0.977 | 0.963 | 0.967 | 1.3 | 0.3 |
| v7.0 | jaccard | yes | 0.467 | 0.417 | 0.423 | 5.0 | 0.7 |
| v7.0 | jaccard | no | 0.853 | 0.800 | 0.810 | 5.3 | 1.0 |
| v7.0 | overlap | yes | 0.457 | 0.413 | 0.430 | 4.3 | 1.7 |
| v7.0 | overlap | no | 0.973 | 0.943 | 0.943 | 3.0 | 0.0 |
| v12.0 | idf-cosine | yes | 0.823 | 0.810 | 0.813 | 1.3 | 0.3 |
| v12.0 | idf-cosine | no | 0.983 | 0.977 | 0.977 | 0.7 | 0.0 |
| v12.0 | jaccard | yes | 0.500 | 0.470 | 0.473 | 3.0 | 0.3 |
| v12.0 | jaccard | no | 0.807 | 0.800 | 0.803 | 0.7 | 0.3 |
| v12.0 | overlap | yes | 0.487 | 0.450 | 0.463 | 3.7 | 1.3 |
| v12.0 | overlap | no | 0.967 | 0.940 | 0.943 | 2.7 | 0.3 |
| v18.0 | idf-cosine | yes | 0.867 | 0.843 | 0.863 | 2.3 | 2.0 |
| v18.0 | idf-cosine | no | 0.997 | 0.993 | 0.997 | 0.3 | 0.3 |
| v18.0 | jaccard | yes | 0.527 | 0.520 | 0.527 | 0.7 | 0.7 |
| v18.0 | jaccard | no | 0.893 | 0.883 | 0.890 | 1.0 | 0.7 |
| v18.0 | overlap | yes | 0.533 | 0.523 | 0.533 | 1.0 | 1.0 |
| v18.0 | overlap | no | 0.987 | 0.983 | 0.987 | 0.3 | 0.3 |

Absolute accuracies move enormously with design choices — IDF-cosine over software-mediated
profiles scores 0.693 at v1.0 where plain overlap scores 0.240, itself a warning against reading
any absolute attribution number — but the penalty's sign and order of magnitude do not. All 30
cells show a positive drift penalty: 18.7 to 56.7 points before the restructuring, 0.3 to 5.3
after; normalization gain follows the same pattern, 6.0 to 32.0 points before and 0.0 to 2.0
after.

### 7.3 From scores to verdicts

A score movement is a methodological curiosity; a changed verdict is a changed conclusion.

**Figure 8.** Attribution verdict instability and mitigation leaderboard reordering by frozen
release.

**Table 10.** Attribution verdict instability. "Verdict changed" is the share of observations
where the named top-1 actor differs between the back-projected and naive conditions.

| Artefact vocabulary | Verdict changed | Changed and now wrong | Was right, then changed | Both wrong but different actor | Normalization changed the verdict |
|---|---|---|---|---|---|
| v1.0 (2018-01-17) | 0.722 | 0.712 | 0.444 | 0.268 | 0.368 |
| v2.0 (2018-04-18) | 0.730 | 0.722 | 0.446 | 0.276 | 0.370 |
| v3.0 (2018-10-23) | 0.744 | 0.728 | 0.474 | 0.254 | 0.408 |
| v4.0 (2019-04-30) | 0.760 | 0.738 | 0.476 | 0.262 | 0.392 |
| v5.0 (2019-07-19) | 0.768 | 0.740 | 0.466 | 0.274 | 0.414 |
| v6.0 (2019-10-23) | 0.790 | 0.774 | 0.516 | 0.258 | 0.442 |
| v7.0 (2020-03-31) | 0.116 | 0.100 | 0.066 | 0.034 | 0.028 |
| v8.0 (2020-10-27) | 0.080 | 0.062 | 0.042 | 0.020 | 0.022 |
| v9.0 (2021-04-29) | 0.086 | 0.070 | 0.034 | 0.036 | 0.012 |
| v10.0 (2021-10-21) | 0.054 | 0.042 | 0.018 | 0.024 | 0.006 |
| v11.0 (2022-04-25) | 0.074 | 0.058 | 0.034 | 0.024 | 0.030 |
| v12.0 (2022-10-25) | 0.070 | 0.054 | 0.028 | 0.026 | 0.016 |
| v13.0 (2023-04-25) | 0.072 | 0.056 | 0.028 | 0.028 | 0.022 |
| v14.0 (2023-10-31) | 0.038 | 0.032 | 0.026 | 0.006 | 0.014 |
| v15.0 (2024-04-23) | 0.032 | 0.028 | 0.024 | 0.004 | 0.020 |
| v16.0 (2024-10-31) | 0.020 | 0.016 | 0.014 | 0.002 | 0.008 |
| v17.0 (2025-04-22) | 0.018 | 0.018 | 0.012 | 0.006 | 0.010 |
| v18.0 (2025-10-28) | 0.022 | 0.022 | 0.016 | 0.006 | 0.020 |

For a v1.0-vocabulary artefact the named actor changes in 0.722 of observations and 0.712 change
to a *wrong* actor; at v6.0, 0.790 and 0.774. These are not degraded scores, they are different
answers to the question the analytic was asked. Across a single modern release boundary the
verdict still changes in 0.022 of observations, and every one of those changes is to a wrong
actor. The final column is the finding a practitioner should find hardest: applying normalization
*itself* changes the verdict in 0.368 to 0.442 of pre-restructuring observations and 0.006 to
0.030 of modern ones. Silently normalizing an inherited label set is not a neutral cleanup step;
it is an intervention that changes published conclusions and must be declared as one.

### 7.4 Is this separable from the single-version noise floor?

The strongest published objection is that ATT&CK labelling is so noisy at a *single* pinned
release that drift is a second-order term on a first-order problem. Products pinned to one release
assign disjoint technique labels to the same behaviour [74], roughly a third of extraction errors
fall between same-tactic, description-overlapping techniques [20], most ATT&CK groups have no
group-specific technique [59], and LLM agents can reproduce documented APT profiles well enough to
undermine the premise of TTP attribution [66]. We concede the noise floor completely: it is large,
and we do not claim drift dominates it.

Separability is a design property rather than an assumption: every condition draws observations
from the same curated edges, so the labelling process is identical across conditions and cancels
in the contrast. But holding a nuisance term at *zero* licenses separability while leaving
*additivity* untested. We therefore ran the missing factorial: each observed technique is replaced
with probability ρ by a sibling sub-technique, its parent, or a same-tactic technique, applied in
the modern vocabulary before back-projection so it flows identically into all four conditions, at
1,200 trials per cell.

The penalty survives at every noise level and every boundary: at v1.0 it falls from +0.439 at
ρ = 0 to +0.342 at ρ = 0.4; at v6.0 from +0.476 to +0.317; at v12.0 it is +0.017 against +0.021 and
at v18.0 +0.012 against +0.012. Strict additivity fails where drift is large — the pre-restructuring
penalty is attenuated 22 to 33 percent at ρ = 0.4, because noise and drift consume the same finite
signal — while in the modern regime the penalty is flat in ρ, effectively additive. The correct
claim is **separable and sub-additive**, and the noise-free figures in Table 6 are *upper bounds*.
Normalization degrades faster than the penalty: recovery at v1.0 falls from 0.44 to 0.30, so the
repair returns least exactly where label quality is worst.

### 7.5 Coverage claims and mitigation leaderboards

**Figure 6.** Coverage claims under a frozen capability, and the random-portfolio sweep of the
same artefact.

**Table 8.** Coverage claims under a capability frozen at release V and re-measured at v19.0. The
identifier artefact is the gap between the naive and normalized re-measurements.

| Capability frozen at | Portfolio | Claimed then | Naive at v19.0 | Normalized at v19.0 | Identifier artefact (pp) |
|---|---|---|---|---|---|
| v1.0 (2018-01-17) | 183 | 97.3% | 10.8% | 23.4% | 12.6 |
| v2.0 (2018-04-18) | 215 | 98.2% | 13.8% | 27.8% | 14.1 |
| v3.0 (2018-10-23) | 222 | 99.6% | 14.3% | 28.7% | 14.3 |
| v4.0 (2019-04-30) | 243 | 99.6% | 16.2% | 31.7% | 15.5 |
| v5.0 (2019-07-19) | 243 | 99.6% | 16.2% | 31.7% | 15.5 |
| v6.0 (2019-10-23) | 258 | 97.0% | 17.4% | 33.9% | 16.5 |
| v7.0 (2020-03-31) | 382 | 89.3% | 52.9% | 54.1% | 1.1 |
| v8.0 (2020-10-27) | 477 | 90.9% | 66.4% | 67.7% | 1.3 |
| v9.0 (2021-04-29) | 501 | 90.8% | 69.9% | 71.2% | 1.3 |
| v10.0 (2021-10-21) | 512 | 90.5% | 71.3% | 72.9% | 1.6 |
| v11.0 (2022-04-25) | 520 | 90.3% | 72.7% | 74.2% | 1.4 |
| v12.0 (2022-10-25) | 535 | 90.1% | 74.9% | 76.3% | 1.4 |
| v13.0 (2023-04-25) | 547 | 90.1% | 76.5% | 78.0% | 1.6 |
| v14.0 (2023-10-31) | 563 | 90.1% | 78.5% | 80.3% | 1.9 |
| v15.0 (2024-04-23) | 576 | 90.4% | 80.3% | 82.2% | 1.9 |
| v16.0 (2024-10-31) | 589 | 89.8% | 82.2% | 84.1% | 1.9 |
| v17.0 (2025-04-22) | 575 | 84.7% | 80.2% | 82.2% | 2.0 |
| v18.0 (2025-10-28) | 582 | 84.2% | 81.1% | 83.2% | 2.2 |

A capability frozen at v6.0 that could legitimately claim 97.0% coverage reads 17.4% matched
naively against v19.0 and 33.9% after normalization, with nothing about the capability changed.
The 79.6-point collapse decomposes into two different quantities: 16.5 points of pure identifier
artefact, repairable by arithmetic, and 63.1 points of catalogue growing underneath a fixed
portfolio — not an artefact at all, but the honest statement that coverage of the current threat
model has fallen. Conflating them is precisely what an undeclared coverage percentage does. In the
modern regime the artefact shrinks to 1.1 to 2.2 points while the growth term stays large: 84.7%
frozen at v17.0 reads 80.2% a year later, of which 2.0 points are bookkeeping. The
random-portfolio sweep shows none of this depends on which techniques MITRE wrote mitigations for:
over 500 random 30% portfolios per release the mean naive error is −26.49 points at v1.0 and −1.00
at v18.0, standard deviations under 0.55 throughout. This is the measurement behind a practitioner
complaint long made without numbers — that coverage percentages are padded and that incompatible
denominators circulate [80, 82, 84].

Ranking is the more consequential readout, because defenders use ATT&CK to prioritise.

**Table 11.** Mitigation leaderboard reordering. Kendall tau compares the ranking of mitigations
by techniques addressed at the frozen release against the same mitigations re-measured at v19.0.

| Portfolios frozen at | Mitigations ranked | Kendall tau, naive | Kendall tau, normalized | Top-10 members displaced (naive) | Top-10 displaced (normalized) | Rank-1 changed |
|---|---|---|---|---|---|---|
| v5.0 (2019-07-19) | 32 | 0.694 | 0.956 | 2 | 1 | yes |
| v6.0 (2019-10-23) | 32 | 0.665 | 0.968 | 3 | 1 | yes |
| v7.0 (2020-03-31) | 41 | 0.959 | 0.995 | 0 | 0 | no |
| v8.0 (2020-10-27) | 42 | 0.970 | 0.991 | 0 | 0 | no |
| v9.0 (2021-04-29) | 43 | 0.965 | 0.998 | 0 | 0 | no |
| v10.0 (2021-10-21) | 44 | 0.962 | 0.994 | 0 | 0 | no |
| v11.0 (2022-04-25) | 44 | 0.977 | 1.000 | 0 | 0 | no |
| v12.0 (2022-10-25) | 44 | 0.983 | 0.998 | 0 | 0 | no |
| v13.0 (2023-04-25) | 44 | 0.983 | 0.998 | 0 | 0 | no |
| v14.0 (2023-10-31) | 44 | 0.975 | 0.996 | 0 | 0 | no |
| v15.0 (2024-04-23) | 44 | 0.977 | 0.996 | 1 | 0 | no |
| v16.0 (2024-10-31) | 46 | 0.977 | 1.000 | 0 | 0 | yes |
| v17.0 (2025-04-22) | 43 | 0.976 | 1.000 | 0 | 0 | yes |
| v18.0 (2025-10-28) | 43 | 0.978 | 0.998 | 0 | 0 | no |

Here, and only here, normalization is close to a cure: mean Kendall tau rises from 0.931 to 0.992,
three of four naive rank-1 flips vanish and none are introduced. The rank-1 column is nonetheless
a warning on its own terms. The single highest-priority mitigation changes identity at four of
fourteen frozen releases, including v17.0 — one release before the analysis — where naive tau is
0.976. A near-perfect rank correlation coexisting with a changed top-ranked control is exactly the
failure a defender cannot afford, because the leaderboard is consumed at the top.

### 7.6 The long tail objection, adjudicated

The remaining defence is that drift lands on techniques nobody reports: observed adversary
behaviour is concentrated in a short head [49], so churn among rare identifiers should barely move
a frequency-weighted quantity. We repeated the frozen-capability experiment with techniques
weighted by documented prevalence, the `uses` edge count at v19.0. The artefact *grows* under
weighting: frozen at v6.0 it is +16.50 points unweighted and +20.01 weighted; at v10.0, +1.58
against +1.43; at v18.0, +2.15 against +1.57. The head here is only moderately concentrated — the
fifteen most-referenced techniques carry 0.285 of all `uses` edges at v19.0 — and is itself a
product of restructuring, the most recent wave having removed T1562.001 at rank 33 of 599.

The limitation deserves its own terms rather than an argument. `uses` edges count how many groups,
malware families and tools MITRE has *documented* as employing a technique: a cumulative stock,
biased toward behaviours easy to narrate, monotone in time, and not an alert stream, which is
materially more concentrated. The long-tail objection is refuted for the fraction of the *written
CTI corpus* affected and untested for the fraction of the *alert stream* affected. We claim the
first and not the second.

## 8. ATT&CK-Norm: A Version-Normalization Protocol

The protocol evaluated throughout this paper is deliberately minimal. Given a set of identifiers
and a target release, ATT&CK-Norm (1) resolves each identifier transitively through the target's
`revoked-by` graph, cycle-safe and bounded at ten hops; (2) drops and *counts* identifiers that
are deprecated or absent in the target rather than discarding them silently; and (3) returns a
four-way residual ledger — kept, merged, demoted, dropped — rather than a set. A fourth branch,
rolling an unresolvable identifier up to a surviving parent, is off by default. Each decision is
a measurement result, not a preference.

**Roll-up is dead code, and measuring that is the finding.** We re-ran the attribution experiment
with roll-up as the only difference, 54 conditions by 500 trials, and audited the branch on
archival profiles for all 18 major releases and on four deployed corpora covering 37,447 label
instances. Top-1 accuracy is identical to three decimals in every condition, the paired bootstrap
interval on the difference is [+0.000, +0.000], and a broader sweep fires the branch three times in
12,027 resolutions across every domain and major release. The reason is structural: MITRE never
orphans a sub-technique, and deprecations without a successor are top-level, so roll-up's
precondition does not arise in ATT&CK's data. The correct default is to drop and count — not
because drop wins a contest, but because roll-up wins nothing measurable while adding an untested
path that can fabricate a parent-level assertion the source never made.

**The residual ledger is the whole protocol.** A set-valued normalizer destroys cardinality at
merges: because the map is a function and not an injection, `{T1562, T1562.001, T1562.006}` and
`{T1562.001}` both return `{T1685}`, and a caller cannot distinguish ten clean identifiers from
ten of which three merged and two dropped. On real corpora this is not hypothetical. TRAM's
bootstrap label set goes from 537 to 503 distinct live classes, 28 targets absorbing 62 source
classes, with 14.75% of its 25,770 label instances landing in a merged class; rcATT goes from 215
to 199 with 9.37% of 6,235 instances merged. A benchmark whose classes silently merge 537 into
503 is not the same benchmark, and a score on it is not comparable to a score computed before the
merge. Demotion is the same story with a different remedy: 119 of 149 Enterprise revocation edges
map a top-level technique onto a sub-technique and 7 map the other way, so a mechanically
successful resolution routinely changes what the artefact asserts. No identifier arithmetic can
repair that; reporting it is the difference between a lossy transformation and a silent one.

What the protocol provably cannot deliver is meaning. Across the release that dissolved the
field's most-used tactic it returns all 674 identifier-stable techniques unchanged and signals
zero drift, while 198 of them changed tactic and 41 changed description hash. Its attribution
gain averages +20.1 points for pre-v7.0 artefacts and +0.77 points afterwards, with the gain's
95% interval including zero in 23 of 36 post-v7.0 conditions; its one clean win is ranking
(Section 7.5). And it fails informatively on real data: on the CTIBench extraction corpus it
would confidently report seven unrepairable deprecations which are in fact seven live Mobile
identifiers on a single row mis-typed as Enterprise (Section 9). Normalization buys comparability
of identifiers. It buys nothing about whether two identifiers mean the same thing, and a paper
claiming otherwise repeats the error it set out to diagnose.

## 9. Label Validity of Deployed CTI Corpora

Sections 6 to 8 measure what drift can do. This section measures what it has already done to
artefacts the field uses now. Each corpus is parsed from its own label file rather than from its
paper, because the paper is not what the model is trained on.

**Figure 7.** Label-validity curves for four deployed CTI corpora across every published ATT&CK
release.

**Table 9.** Label validity of deployed corpora. "Fit" is the best achievable share of distinct
identifiers live at any single release; "releases where all labels valid" is the provenance
interval.

| Corpus | Distinct labels | Label instances | Sub-technique labels | Best-fit release | Fit | Releases where all labels valid | Invalid today | Repairable |
|---|---|---|---|---|---|---|---|---|
| ctibench-ate | 120 | 397 | 0 | v14.0 (2023-10-31) | 0.942 | **none** | 8 (0.067) | 1 |
| rcatt | 215 | 6235 | 0 | v4.0 (2019-04-30) | 1.000 | 8 (v4.0–v6.3) | 107 (0.498) | 99 |
| tram-bootstrap | 537 | 25770 | 344 | v13.0 (2023-04-25) | 0.939 | **none** | 43 (0.080) | 43 |
| tram2 | 50 | 5143 | 24 | v8.2 (2021-01-27) | 1.000 | 18 (v8.2–v16.1) | 2 (0.040) | 2 |

Two of the four corpora have an **empty provenance interval**: no ATT&CK release ever published
makes every one of their labels simultaneously valid. For CTIBench's extraction task the best any
release achieves is 0.942 at v14.0 — a benchmark whose gold answer key cannot be attributed to any
edition of the vocabulary it is written in. rcATT is internally consistent and dates cleanly to the
v4.0–v6.3 window, which is why it is the starkest case: 107 of its 215 identifiers (0.498),
covering 0.380 of its 6,235 label instances, are invalid at v19.2. It was consistent when made and
is half dead now [8, 44]. TRAM's bootstrap set has 43 invalid identifiers over 25,770 instances,
all repairable [3].

Version declarations would make all of this checkable. There are none.

**Table 12.** ATT&CK version declarations found in the documentation of deployed corpora.

| Corpus | Documentation files scanned | ATT&CK version declarations found |
|---|---|---|
| cti-bench | 2 | 0 |
| rcATT | 2 | 0 |
| tram | 15 | 0 |

Table 12 is a thin scan and we do not rest the adoption claim on it. We therefore measured
adoption where coverage claims actually live, in ATT&CK Navigator layers, whose format has
carried a `versions.attack` field since layer format 4.0 [15]. Across 69 Navigator-format layer
files in local clones, five declare it — all five MITRE's own sample or test fixtures [18]. Of 57
published vendor threat-report layers from eleven security companies, **zero** declare an ATT&CK
content version: 39 are layer format 2.2, where the field does not exist, and 18 are formats 4.1
to 4.3, where it exists and every one omits it [79]. The cost is measurable: those 57 layers
carry 2,143 technique annotations of which **739 (34.5%) name an identifier revoked or deprecated
at v19.2**; 49 of the 57 files contain at least one; 72 of the dead annotations are deprecations
with no successor; and 5 name identifiers absent from v19.2 entirely, four of them Mobile
identifiers, one on a layer whose declared domain is Enterprise. Opened today in a current
Navigator, every one silently re-bases onto the current release, because the version field is
optional and defaults to current [15, 16].

Declaring a version is necessary and not sufficient. One public remapping repository announces a
deliberate migration to ATT&CK v12.0 and its inherited label split still carries 203 dead label
occurrences, 128 of them T1064, revoked five releases before the declared target [10]; a widely
used attack-graph system froze its ontology as a dated HTML scrape with parent-only templates [2];
and a six-system survey of TTP tooling found five different ATT&CK ontologies and two declared
versions between them [3]. Benchmark generations are the same problem in a more consequential
place: CTIBench's extraction task carries zero sub-technique identifiers against an undeclared,
roughly v15-era vocabulary [4, 30] while its successor is dominated by sub-technique labels and
overlaps it only partially at parent level [6], and a separate line grew from 691 to 1,860 QA pairs
under one identifier and the same taxonomy [29]. Comparability across benchmark generations is
asserted and established nowhere, which is why live-API and telemetry-grounded designs are the
right structural response [13, 28].

One finding cuts against our own thesis and we report it as such. Of CTIBench's eight invalid
identifiers, seven are marked unrepairable — and all seven come from a single row whose platform
column says Enterprise while its entire gold set is Mobile-only, all seven live in
`mobile-attack` v19.2. Seven-eighths of that corpus's apparent drift damage is not drift; it is a
single-version labelling error, and a normalizer without a domain guard would report seven
confident deprecations and be wrong seven times. Label-validity analysis that does not separate
drift from data-entry error over-attributes to drift, and ours would have, had we not read the
rows.

## 10. Discussion and Reporting Discipline for CTI Research

The measurements support a narrower thesis than the one we set out to test, and a more durable one.
ATT&CK's referential machinery is close to as good as a 1:1 crosswalk can be, and it is almost
never used. Its semantic machinery does not exist, and nothing in the ecosystem detects semantic
change. The remedy is therefore not a better crosswalk but a reporting discipline that makes the
vocabulary of a CTI artefact a declared, checkable property of that artefact.

Four lines a reviewer can check in under a minute. **(1)** The ATT&CK domain, the exact release,
and the SHA-256 of the bundle, recorded in the artefact rather than the prose. **(2)** Whether
identifiers were normalized, and onto which target. **(3)** The residual: kept, merged, demoted and
dropped counts, with the dropped identifiers listed verbatim. **(4)** For any cross-time
comparison, a statement that both sides were projected onto one reference release. Benchmarks carry
two more: **(5)** the label granularity policy — parent-only or mixed — with class counts before
and after normalization; **(6)** a continuous-integration check that fails when any gold label is
not live in the declared release. Vendor coverage claims carry two of their own: **(7)** the ATT&CK
version and the denominator as an absolute count of live techniques beside the percentage; **(8)**
the claim re-stated against the current release, or explicitly marked as-of.

The engineering cost is a JSON header, a table and about thirty lines of code. The real cost is
reputational, and naming it is part of the argument: a residual line makes label decay public —
rcATT's would read 0.498 of identifiers and 0.380 of instances invalid at v19.2 — coverage
percentages become non-monotone in public, since item (8) forces a vendor to restate 84.7% as 80.2%
a year later, and benchmark scores stop being cross-release comparable by default, which is the
point rather than a side effect. This is the trade the malware-classification literature made when
it accepted temporal splitting: a class of impressive numbers became unpublishable and the field
got better [35, 67].

For MITRE, the recommendations are ported rather than invented. Keep `revoked-by` for exact
successors and add an inexact-successor relation, so T1562 can point at all seven of its v19
successors and at the tactic that absorbed it rather than at one of its own former children; add a
controlled obsolescence-reason vocabulary — superseded-by-split, merged, re-scoped,
promoted-to-tactic, out-of-scope — so drop and merge become distinguishable; and make obsolescence
visible in the human-readable label so tools joining on name break loudly rather than working
silently against a dead concept [54]. Enforce referent stability at a stable identifier: renaming
TA0005 in place is the edit the stability principle forbids [53, 54]. Add prior-version and
backward-compatibility links on the collection object, which OWL has had for two decades [57].
Publish the evolution mapping as a first-class versioned artefact typed with complex change
operations rather than an untyped diff — `diffStix` already computes the operations, and typing
them is what makes the split of Section 6.5 computable rather than asserted [26, 34]. And make the
Navigator layer's version field mandatory, since it defaults to current, which is why every
published coverage layer we found is version-orphaned [15, 16].

The CTI quality literature should absorb one further claim: vocabulary versioning is a quality
dimension in its own right, orthogonal to those currently defined [60, 76]. It is not provenance,
which records where an item came from rather than in what vocabulary it is expressed; not
interoperability, which concerns format; and not timeliness, which concerns the age of the
intelligence rather than of the scale it is measured on. An artefact can score perfectly on all
four and still be uninterpretable, which is what Table 9 shows for rcATT.

Finally, the bar an SCI-level contribution here must clear, stated as the one we tried to meet: it
must measure the ontology rather than describe it, over the full release history; show a
*conclusion* changing rather than a score moving, as Tables 10 and 11 do; hold intelligence content
fixed while varying the vocabulary, or attribute nothing to drift; concede the producer's apparatus
where it is complete and locate the failure precisely; test against the strongest published rival
explanation rather than the weakest, here the noise floor and the long tail; and state what its
remedy cannot do. Ours cannot repair meaning, and we measured how much it cannot repair.

## 11. Threats to Validity

**The loop is closed inside ATT&CK.** Observation, profiles, ground truth and back-projection map
all originate from one curator, so the absolute accuracies of 0.67 to 0.97 are internal-consistency
scores and never statements about attribution performance. The `historical` diagnostic partly opens
the loop and shows what opening it costs: real archival artefacts score 0.159 at v1.0 against the
back-projection's 0.231, that is, worse. The experiment that would close this threat is the one the
field does not have — a double-labelled incident corpus in which two independent analysts label the
same intrusions under two ATT&CK releases, yielding the drift and inter-analyst terms
simultaneously from outside MITRE's own edges. We name it rather than approximate it.

**Both experimental poles are extremes.** The back-projected condition is a reconstruction, not a
v-era system, and Section 7.1 quantifies the gap; profile collision deflates the penalty while
perfect recall inflates it, with the measured net before the restructuring downward, so the legacy
penalties are conservative. The naive condition is likewise a worst case: MITRE re-mapped its own
`uses` edges to the most specific sub-technique, so modern profiles are nearly pure sub-technique
level while the back-projected artefact is pure parent level, and exact matching scores zero across
that boundary. Real legacy artefacts are mixed-granularity, so the true naive condition lies
between our naive and normalized columns. The normalizer is also close to the algebraic inverse of
the back-projection, making reported recovery an upper bound on what it achieves on real,
typo-bearing, cross-domain label sets — as the CTIBench row in Section 9 shows.

**Prevalence is documentation, not telemetry.** The weighting in Section 7.6 uses `uses` edge
counts computed from the same release whose churn is measured, so a revoked technique carries its
weight with it. The weighted result is therefore not independent evidence in the way telemetry
would be, and the long-tail objection remains untested on the alert stream.

**Metric choices.** Token-set Jaccard at a 0.8 threshold is blunt: it calls a reorganisation of
identical content a rewrite and misses a meaning-reversing edit of a few words, which is why we
report the mean-similarity series beside the thresholded share (Table 4). The growth decomposition
depends on test order; re-mapping is tested before refinement, charging ambiguous edges to
bookkeeping, so 0.323 is an upper bound under that ordering.

**Internal number discipline.** Two of our quantities differ slightly between independent
computations over the same bundles, and we report rather than select. The semantic-metadata
analysis records 1,358 description changes and 487 without a version increment; recomputation under
a different carried-over-pair rule returns 1,366 and 494, a 0.6% difference moving neither precision
nor recall to three decimals. The tactic-change count for the most recent transition is 198 over
major releases and 201 over the patch releases that bracket the change — the same phenomenon under
two eligibility rules, exactly the ambiguity this paper argues must be declared.

**Evidence tiering and one corpus-integrity incident.** Secondary literature was reachable here
only through search summaries; it is attributed as reported, never quoted, and no positioning claim
rests on a number we could not see in an artefact. An automated integrity check over our own 112
evidence notes flagged 10 whose front matter had become detached from their body. Every affected
claim was re-derived from a primary artefact or removed — one claim about a third-party
synchronisation project's outputs was removed rather than repaired — and the audited-absence claims
in Section 3 carry the bound of the search that found them. A paper about undeclared provenance
that concealed a provenance failure in its own evidence base would be self-refuting.

## 12. Conclusion

ATT&CK is the measuring instrument of cyber threat intelligence, and it has been re-issued 109
times without any downstream result recording which issue it used. We measured the recalibration.
Identifier churn is episodic, currently mild in Enterprise, fully accounted for by MITRE, and
recurrent across domains at a hazard of 0.106 per major transition that no leading indicator in
the public bundles predicts. Semantic churn is continuous, invisible to identifier arithmetic, and
undetectable from ATT&CK's own metadata at precision 0.447 and recall 0.641. Nearly a third of
apparent knowledge growth for pre-existing actors is bookkeeping, rising to 0.470 in the most
recent release. Downstream, vocabulary mismatch alone moves a coverage claim from 97.0% to 17.4%
and changes the named threat actor in 0.722 of pre-restructuring observations and 0.022 across a
single modern boundary, concentrated two to seven times more heavily on exactly the groups that
are attributable at all. Identifier normalization repairs about half the legacy penalty, almost
none of the modern one, and no part of the semantic one — and applying it silently changes
published verdicts in up to 0.442 of cases, so it is itself a reportable intervention.

The part identifier arithmetic can repair, MITRE has solved and consumers do not use; the part it
cannot repair is the part nobody detects. Closing the gap needs no better crosswalk. It needs CTI
artefacts to declare their calibration — domain, release, bundle hash, and the residual ledger of
what any migration kept, merged, demoted and dropped — and it needs ATT&CK to adopt the two
mechanisms ontology engineering settled decades ago: an inexact-successor relation, and a typed
evolution mapping published as an artefact in its own right.
