## Abstract

Cyber threat intelligence measures adversary behaviour with an instrument: the MITRE ATT&CK
knowledge base, whose technique identifiers are the units in which detection coverage,
threat-actor attribution and benchmark labels are all denominated. That instrument has been
re-issued 109 times across three domains since January 2018, and each re-issue is a
recalibration — identifiers retired and minted, concepts re-cut across abstraction levels,
technique meanings rewritten in place, and tactics reassigned. We can find no published CTI
result that reports which calibration it used. This paper treats that omission as a
measurement failure and quantifies it. From every public ATT&CK STIX release we build a
longitudinal database of 106 domain-release pairs and measure four drift processes
separately: identifier churn, abstraction re-cutting, intensional rewriting under a stable
identifier, and relational reassignment. We then run four controlled downstream experiments
that hold intelligence content fixed and vary only the vocabulary. The measurement is
dialectical and we report both halves. MITRE's identifier accounting for Enterprise is
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
technique identifier. When a vendor reports that a product covers 84.2% of ATT&CK, when a
paper reports that a classifier attains a given micro-F1 over ATT&CK labels, or when an
analytic names an intrusion set from a set of observed TTPs, the number is meaningful only
relative to a particular edition of the catalogue that supplies both the numerator's
vocabulary and the denominator's cardinality [63, 74]. The ATT&CK project is unusually
disciplined about publishing those editions: each release is an immutable, addressable STIX
bundle, retired objects are retained rather than deleted, and every revoked technique carries
a typed edge to its successor [1, 7]. The discipline is asymmetric. The producer versions
scrupulously; the consumer literature does not report the version at all.

This paper takes that asymmetry literally and treats ATT&CK as an instrument that has been
silently recalibrated. The framing is not rhetorical. An instrument has a scale, and drift in
the scale is separable from drift in the thing measured — precisely the separation that
concept-drift theory in security machine learning cannot express, because it is formulated
over a fixed label space and models change in the data-generating process, not in the
vocabulary of the labels [22, 33, 67]. The literature that does study label-space change,
under class-incremental learning or evolving class ontologies, models the additive case and
occasionally relabelling, but not retirement, merger, promotion across abstraction levels, or
silent redefinition of a retained class [24, 43]. ATT&CK performs all of these. A measurement
vocabulary that performs all of these, and is consumed by a field that reports none of them,
is a validity problem rather than a hygiene complaint.

We make the argument by measurement, and we make the concessions that the measurement forces.
The first concession is the apparatus. Anyone who opens MITRE's own usage documentation can
refute a naive version of this paper in a paragraph: pinning a release is the documented
first-class workflow, tombstones are guaranteed, and a change-computation tool ships in
MITRE's Python library with an explicit class for objects patched without a version increment
[1, 34, 48]. Our own extraction confirms the strongest form of the claim for Enterprise
technique identifiers: at v19.2 there are 149 revoked-by edges from 149 distinct revoked
techniques, zero dangling revocations, and no Enterprise identifier has ever vanished without
a tombstone (Section 6.2). The second concession is the noise floor. Detection products
pinned to a single ATT&CK release disagree about the label for the same behaviour roughly
half the time [74], and roughly two-thirds of ATT&CK groups have no technique unique to them
at all [59]. We do not claim drift dominates that noise. We claim it is separable from it by
construction — every condition in our experiments draws from the same curated ATT&CK data, so
the labelling process is held constant and cancels in the contrasts — and we test additivity
rather than assuming it (Section 7.4). The third concession is the remedy. Identifier
normalization is worth 42 to 53 points of recovered attribution penalty on pre-2020 artefacts
and under one point on modern ones, with a confidence interval spanning zero in most modern
conditions (Section 8). The constructive claim of this paper is not the crosswalk. It is what
a CTI artefact must declare about its own calibration.

The contributions are four. First, a longitudinal measurement of ATT&CK drift over every
public release of all three domains, decomposed into four processes that behave differently
in time and must be reported separately (Section 6). Second, four controlled experiments —
attribution, coverage, mitigation ranking and benchmark label validity — in which the
adversary intelligence is held fixed and only the vocabulary moves, so that every reported
difference is attributable to the instrument (Sections 7 and 9). Third, a decomposition of
apparent knowledge growth into intelligence and bookkeeping, answering the question of how
much of ATT&CK's expansion is new adversary knowledge (Section 6.5). Fourth, a normalization
protocol whose measured limits are themselves the result, and the reporting discipline that
follows from those limits (Sections 8 and 10). A reader should be able to reconstruct every
quantity in this paper from Section 5 alone; where a number is fragile, we say by how much
and in which direction.

## 2. Background: ATT&CK as a Versioned Ontology

ATT&CK organises adversary behaviour into tactics (adversary goals), techniques and
sub-techniques (the means), and links them to intrusion sets, software, mitigations and data
components. Its design documentation is explicit that inclusion criteria are non-stationary
and that the abstraction level of a technique is a deliberate editorial choice rather than a
natural kind [14]. This matters for measurement: the catalogue is not an inventory that only
grows as adversaries innovate, it is an editorial artefact that is periodically re-cut. The
project describes itself, and is described by practitioners, as an ontology rather than a
taxonomy [77], which places it squarely inside a literature with well-developed machinery for
exactly the problem this paper measures: ontology evolution versus ontology versioning, and
change management as the core task of both [56].

That literature supplies the yardstick. OBO Foundry's versioning principle requires version
IRIs, release immutability and perpetual resolvability of prior versions [55]; its identifier
policy requires global uniqueness and forbids reuse [53]; its term-stability principle
requires that the referent of an identifier not change, distinguishes exact successors
(`replaced_by`) from inexact ones (`consider`), and requires an obsoletion to be visible in
the human-readable label rather than only in metadata [54]. OWL supplies `versionIRI`,
`priorVersion`, `backwardCompatibleWith` and `owl:deprecated` [57], and COnto-Diff supplies
typed complex change operations — merge, split, move, substitute — as a first-class evolution
mapping between two versions of an ontology rather than an untyped diff [26]. Biomedicine has
already demonstrated the downstream consequence we measure here: Gene Ontology evolution
changes the interpretation of enrichment analyses computed over it, so a conclusion can move
without any new experiment [69]. The security vocabularies have their own version of the
problem — CVE has typed lifecycle states including rejection and dispute [31], CVE-to-CWE-to-CPE
mappings are unstable along the abstraction ladder [32], and CVSS scores fragment across
versions in ways that defeat cross-version comparison [39] — and the knowledge-graph
literature has argued that vocabulary churn and instance-data usage must be tracked as two
distinct time series [37].

Against that yardstick, ATT&CK scores well on some axes and has nothing on others. Releases
are immutable and addressable, which satisfies the substance of the versioning principle [1,
55]. Retirement is typed and non-destructive: an object with a successor is revoked and
carries a `revoked-by` edge to its replacement, an object without one is deprecated, and both
are retained in the bundle so that dependent workflows do not break [1]. MITRE ships
`diffStix`, which computes a per-release change set across several classes including a
`patches` class for objects changed while the version field stayed the same, and which
annotates unintended version changes as a known historical defect [34, 48]; the Center for
Threat-Informed Defense operates ATT&CK Sync to flag mappings affected by a release [5]; and
the Navigator layer format carries a `versions` object able to record the ATT&CK content
version of a coverage layer [15]. What ATT&CK lacks is the inexact-successor relation, the
controlled obsolescence-reason vocabulary, the label-level visibility of obsoletion, the
prior-version and compatibility links, and a typed evolution mapping published as an artefact
in its own right. Sections 6.2 and 6.4 show what each absence costs.

One further structural fact shapes everything downstream. The single largest editorial event
in ATT&CK's history is the March 2020 introduction of sub-techniques, which re-cut a large
fraction of the existing catalogue in one release. It is well documented and widely discussed
[47, 63]. It is also, as Section 6.6 shows, not unique: it is one draw from a recurring
per-domain hazard, and the same move is being executed in the ICS domain in 2026.

## 3. Related Work

Four literatures bear on this problem and none of them measures it.

**CTI quality.** A mature line of work defines quality dimensions for threat intelligence and
builds instruments to score feeds against them: completeness, accuracy, timeliness,
relevance, provenance and interoperability recur across the canonical treatments [60, 76],
with dynamic automated assessment and weighted criteria added more recently [27], and
empirical feed evaluations establishing that public feeds overlap little and age badly [41,
45]. Practitioner-facing quality assurance has been studied directly [40], community feeds
have been metered [38], and a 2025 measurement-based survey consolidates the field [11].
Structural and syntactic validity of the exchange formats themselves is a separate recurring
complaint [83]. None of these frameworks names the reference vocabulary's version as a
quality dimension. This is an audited absence and we state its bound: across the
quality-dimension sources reachable in this environment we found no dimension defined over
the vocabulary edition, and we did not have full text for all of them, so we claim the
absence of a named dimension rather than the absence of any awareness. The burden is
nonetheless reported by practitioners and conceded institutionally by the existence of
migration tooling [5, 81].

**ATT&CK-based analytics.** The SoK on ATT&CK in research and practice already establishes
that coverage claims are not comparable across products and flags temporal instability as an
open issue [63], and a 2025 survey sets the bar for what a contribution here must show [47].
Virkud et al. demonstrate the non-comparability empirically at a single pinned release:
detection rules from different vendors describing the same behaviour carry disjoint technique
labels, and recomputing coverage from raw artefacts rather than vendor claims collapses the
differences between products [74]. Shen et al. re-analyse MITRE's own Evaluations as whole
attack graphs and show that per-technique tallies are the wrong unit [62]; MITRE's Evaluations
programme itself refuses to emit a single coverage score [46]; and practitioners have made
the same argument in blunter terms, that a heatmap counts rules rather than coverage and that
at least three incompatible denominators are in circulation [80, 82, 84]. The
Summiting-the-Pyramid line goes further and replaces techniques with implementations as the
coverage denominator outright [64], while mitigation coverage has been shown to have a
ceiling set by the control catalogue rather than by the product [58]. All of this is about
disagreement at one version. None of it measures what happens when the version changes.

**TTP extraction, benchmarks and attribution.** The extraction line runs from TTPDrill [71]
through rcATT [44] to TTPHunter and its successor [72], with graph-based systems such as
AttacKG alongside [2] and recent multi-label treatments that explicitly decline to treat TRAM
annotations as gold [52, 73]. LLM-era benchmarks are now the dominant evaluation surface:
CTIBench treats authoritative sources as fixed and includes a time-controlled split for the
CVE task but not for the ATT&CK task [30]; CTIArena grew into a successor with 691 to 1,860
QA pairs under one identifier and the same nine-task taxonomy [29]; AthenaBench argues that
static benchmarks go stale and proposes live-API construction as the remedy [13]; SEvenLLM
assembles 90k samples from reports spanning two decades with no ATT&CK release declared [61];
SynthCTI synthesises the long tail [65]; and CTI-REALM grounds evaluation in telemetry, which
is the only structurally drift-resistant design in the set [28]. The staleness of static
benchmarks has itself been quantified as answer-key decay [75]. Attribution work has moved to
TTP sequences [17, 23] and is surveyed by artefact type rather than by ontology version [12],
while two recent results bound what TTP attribution can do at all: roughly a third of ATT&CK
groups have any group-specific technique [59], and LLM agents can reproduce documented APT
profiles at 55-80% precision, which attacks the premise that a TTP profile identifies an
actor [66]. Extractor errors concentrate among same-tactic, description-overlapping
techniques, up to a third of them [20]. The common feature of this entire literature, as read
through the repository audits in Section 9, is that the gold label space is a file whose
provenance is undeclared.

**Concept drift in security ML.** Dataset-shift taxonomies are formulated over a fixed label
space and model change in the joint distribution [33]; TESSERACT establishes temporal
experimental hygiene for malware classification [67]; CADE detects and explains drifting
samples [22]; conformal evaluation rejects under drift [70]; and a long line of adaptation
work assumes the vocabulary is fixed while the distribution moves [50]. Arp et al.'s catalogue
of methodological pitfalls in security ML does not include vocabulary versioning [35]. Where
the label space itself changes, the machinery is class-incremental learning and continual
learning with evolving class ontologies [24, 43], and the closest security instance is
MOTIF's open and unstable malware-family class set [51], with AVClass as the prior art for
alias resolution as a normalization step [19]. IncreTTP is, as far as we found, the only work
that frames ATT&CK version updates as concept drift directly, and its remedy is incremental
learning rather than measurement [42]. The boundary is the contribution point: concept drift
is change in P(y|x) with y fixed; ontology drift is change in the set y ranges over and in
what its members mean [21].

Positioned against all four, this paper's novelty is not the observation that ATT&CK changes.
It is the quantification of what the change costs a downstream conclusion, under a design
where nothing but the vocabulary moves.

## 4. Problem Formalization and Drift Taxonomy

Let an ATT&CK release be a triple `R_v = (L_v, ⊑_v, μ_v)`. `L_v` is the set of live technique
identifiers at release `v` — those present in the bundle and marked neither revoked nor
deprecated. `⊑_v` is the abstraction relation, the partial order induced by `subtechnique-of`
edges (with the dotted-identifier convention as a fallback for releases that omit the
relationship). `μ_v` is the intension map, sending each identifier to its textual definition:
the description, the detection guidance, and the set of tactic phases the technique is
assigned to. A release also carries a retirement relation `ρ_v ⊆ L̄ × L_v` given by
`revoked-by` edges, where `L̄` is the set of retired identifiers.

A CTI artefact written at release `v` is a multiset of identifiers drawn from `L_v`, plus an
implicit commitment to `⊑_v` and `μ_v`. It is consumed at release `w > v`. Four drift
operators can have acted in between, and they are independent enough that any one of them can
be zero while the others are large.

**D1 — extensional drift.** `L_v ≠ L_w`. Identifiers are added, revoked with a successor,
deprecated without one, or absent entirely. This is the only drift class that a naive
consumer notices, because it is the only one that produces a failed lookup. It is fully
observable from the bundles and, for Enterprise, fully repairable by transitive closure over
`ρ_w`.

**D2 — structural drift.** `⊑_v ≠ ⊑_w` on identifiers present in both, or a retirement that
crosses abstraction levels. A parent technique re-cut into children, a sub-technique promoted,
or — the pathological case — a technique promoted to a tactic, which no technique-to-technique
relation can express. D2 is partly observable: the abstraction level of both endpoints of a
retirement edge is computable, so an abstraction change can be detected even though it cannot
be repaired.

**D3 — intensional drift.** `μ_v(t) ≠ μ_w(t)` for `t ∈ L_v ∩ L_w`. The identifier survives,
the words change. This is the class that identifier arithmetic cannot see by construction,
and the class for which ATT&CK emits no reliable signal (Section 6.4).

**D4 — relational drift.** The tactic assignment of a surviving technique changes, or the
tactic layer itself is re-cut. Formally a special case of D3 restricted to the kill-chain
phase component of `μ`, but it deserves separation because tactic identifiers carry no
retirement edges at all (Section 6.3), and because tactic-level aggregation is the most common
way coverage and profile statistics are reported.

Two artefacts are **version-comparable** when both have been projected onto one reference
release and the projection's residual is declared. Projection is the map `π_w : 2^{L_v} → 2^{L_w}`
defined by transitive closure over `ρ_w`. It is a function, not an injection: it can merge,
and it can land on a different abstraction level. The residual is the four-way ledger `(kept,
merged, demoted, dropped)`. A protocol that returns only `π_w(S)` and not the residual has
destroyed exactly the information a reader needs to judge comparability — which is the
reporting failure this paper is about, and which Section 8 shows is not hypothetical.

Finally, a note on what none of these operators express. ATT&CK is a description of adversary
behaviour, not the behaviour itself. A technique whose description is rewritten may be
tracking a genuine change in the threat landscape, an improvement in the curator's
understanding, or an editorial preference. Our measurements cannot distinguish these, and we
do not claim to. The claim is narrower and sufficient: whatever the reason, a downstream
artefact written against the old text and scored against the new one is being measured with a
recalibrated instrument, and nothing in the current publication practice of the field records
that this has happened.

## 5. Data and Methodology

The study is a measurement study, so the instrument we use to measure the instrument is
described in enough detail to be rebuilt.

### 5.1 The release corpus

We clone MITRE's `attack-stix-data` repository, which publishes every ATT&CK release as an
immutable STIX 2.1 bundle at a stable path [1]. Its index enumerates 109 versioned bundle
entries across the three domains, 41 Enterprise, 41 Mobile and 27 ICS. Our extraction
materialises 106 distinct domain-release pairs: 41 Enterprise, 38 Mobile, 27 ICS. The
three-entry difference falls entirely at Mobile v11.0 to v11.2, where the published Mobile
sequence steps from v10.1 to v11.3. We report both counts rather than quietly adopting the
convenient one, because the point of this paper is that undeclared denominators are how
measurements go wrong.

Each bundle is parsed into a SQLite database with four tables. `releases` records the domain,
version string, ordinal and release date. `objects` records, per domain and version, every
STIX object's identifier, type, ATT&CK identifier, name, sub-technique flag, revoked and
deprecated flags, `x_mitre_version`, creation and modification timestamps, the
comma-joined kill-chain phase shortnames, the platform list, and SHA-256 digests and character
lengths of the description and detection fields. `descriptions` retains the full text of both
fields so that token-level similarity can be computed after the fact. `relationships` records
every typed edge with its source and target STIX references. Storing digests alongside full
text lets an "edited or not" indicator be computed exactly and cheaply while leaving the
similarity computation exact rather than approximate.

Release-level analyses use **major releases only**: one release per major version, taken as
the `.0` release or, where that does not exist, the earliest available release of that major
version. This yields 19 Enterprise, 19 Mobile and 12 ICS analysis points. The reason is
comparability of transitions: ATT&CK's patch releases are irregular in cadence and in scope,
and mixing them into a per-transition series would make "per release" mean different things
in different eras. The deployed-corpus validity analysis in Section 9 deliberately does the
opposite and uses every published release, because there the question is which release a
given label file could have been written against, and excluding patch releases would bias
that answer.

**Table 1.** The release corpus. Major releases are the analysis points for churn, survival
and drift; all releases are used for the label-validity analysis of Section 9.

| Domain | Releases analysed (major / all) | First | Last |
|---|---|---|---|
| Enterprise | 19 / 41 | v1.0 (2018-01-17) | v19.0 (2026-04-28) |
| Mobile | 19 / 38 | v1.0 (2018-01-17) | v19.0 (2026-04-28) |
| Ics | 12 / 27 | v8.0 (2020-10-27) | v19.0 (2026-04-28) |

### 5.2 Definitions of the measured quantities

**Live technique set.** `L_v` is the set of ATT&CK identifiers of `attack-pattern` objects in
release `v` with both the revoked and deprecated flags false. Every count of "techniques" in
this paper is `|L_v|` unless stated otherwise, and every coverage denominator is `|L_v|` at
the release at which the coverage is being stated.

**Identifier Jaccard.** For consecutive majors `a → b`, `J(L_a, L_b) = |L_a ∩ L_b| / |L_a ∪ L_b|`.
A technique that is present in `b` but flagged revoked is not in `L_b`, so a revocation
lowers `J` exactly as a deletion would; this is the intended behaviour, because a revoked
identifier is unusable as a label even though it is still present in the file.

**Survival and recoverability.** For a source release `v` and target `w`, survival is
`|{t ∈ L_v : t ∈ L_w}| / |L_v|`. An identifier is *recoverable* at `w` if it is revoked or
absent at `w` and following `revoked-by` edges transitively from it (at most ten hops, cycle-safe)
terminates at a member of `L_w`. Half-life is the first target release at which survival falls
below 0.5, reported with the elapsed years from the source release date; "not reached" means
survival never fell to 0.5 through v19.0.

**Semantic drift.** For identifiers live in both `v` and `w`, "description edited" is
inequality of the SHA-256 digests of the description strings. Token similarity is the Jaccard
index over the sets of lowercased alphanumeric tokens extracted by the regular expression
`[a-z0-9]+`; a *substantial rewrite* is token Jaccard below 0.8. The 0.8 cut is a convention
and we report the full mean-similarity series alongside it so that a reader who prefers a
different cut can read the consequence off the distribution rather than take ours on trust.
Set Jaccard over bags of words is a crude similarity, and it is deliberately crude: it is
monotone in shared vocabulary, requires no model, and cannot be accused of importing an
embedding's own drift into a measurement of drift.

**Version-metadata reliability.** For every pair of consecutive major releases we take the
techniques live in both and cross-tabulate "description text changed" against
"`x_mitre_version` incremented". Treating a version increment as a detector of a text change
gives precision = (text changed and bumped) / (all bumped) and recall = (text changed and
bumped) / (all text changed). These are the only two numbers needed to say whether a consumer
can use the version field to decide what to re-read.

**Growth decomposition.** For consecutive majors `a → b`, every group-to-technique `uses`
edge present in `b` and absent in `a` is assigned to exactly one cause, tested in this order:
*new actor* if the group is not in `a`; *revocation re-mapping* if some technique already
credited to that group in `a` resolves transitively through `b`'s revocation graph onto this
technique; *sub-technique refinement* if the technique is new in `b` and its parent was
already credited to that group in `a`; *new technique intelligence* if the technique is new in
`b` and is not such a refinement; and *genuine new intelligence* if both endpoints existed in
`a` and were simply not linked. The *bookkeeping share* is (refinement + re-mapping) divided
by all new edges for pre-existing groups. The ordering of the tests is a modelling choice and
it is conservative in the direction that matters: re-mapping is tested before refinement, so
an edge that could be read either way is charged to bookkeeping. New actors are excluded from
the denominator because a newly documented intrusion set is unambiguously new intelligence
and including it would flatter the intelligence share.

### 5.3 The four downstream experiments

All four share one principle: the adversary intelligence is held fixed and only the
vocabulary is varied. This is what makes the contrasts attributable to the instrument.

**Attribution (Section 7.1).** The analysis release is `w` = v19.0 throughout. For a legacy
vocabulary `v`, every *modern* group profile is back-projected into `v`'s vocabulary by a map
built once per pair: a modern technique maps to itself if it is live at `v`; else to the
pre-revocation identifier that resolves onto it, taking the lexicographically first if several
do; else to the nearest ancestor under `⊑_w` that is live at `v`, climbing at most five hops;
else it is dropped as a behaviour with no `v`-era expression. The candidate universe is the
groups present in both releases with at least `k` techniques at `w` and at least two at `v`.
Each of 500 trials samples a group uniformly, samples `k` = 10 techniques from its modern
profile, and scores four conditions over identical draws and an identical candidate set:
*back-projected* (the `v`-vocabulary observation against `v`-vocabulary profiles),
*naive* (the `v`-vocabulary observation against modern profiles), *ATT&CK-Norm* (the
observation projected forward, then against modern profiles) and *oracle* (the modern
observation against modern profiles). Scoring is IDF-weighted cosine over technique sets with
IDF computed within the condition's own profile set; ties break on a fixed group ordering.
The **drift penalty** is back-projected minus naive in top-1 accuracy; **recovery** is
(ATT&CK-Norm − naive) / (back-projected − naive). Confidence intervals are paired bootstrap
over trials with 2,000 resamples. A fifth *historical* condition draws from the real archival
`v`-era profile and is reported as a diagnostic, because it mixes drift with genuine
intelligence change and therefore cannot serve as the control.

Two properties of this design must be stated before the results rather than after. The
back-projected condition is not a v-era system; it is 2026 intelligence transcribed into an
older vocabulary, and Section 11 quantifies the gap. And because the observation is drawn
from the profile, recall is perfect by construction, which inflates every absolute accuracy.
Absolute accuracies here are internal-consistency scores inside one curator's graph and must
never be read as attribution performance.

**Coverage (Section 7.2).** A defender's capability is frozen at release `v` as the set of
live techniques reachable by `mitigates` (or `detects`) edges in that release — a
capability that by construction does not change afterwards. Its coverage is then recomputed
against v19.0 both naively (raw identifiers intersected with the modern live set, over the
modern denominator) and after normalization. Portfolios with fewer than 20 techniques are
excluded. A random-portfolio sweep repeats the exercise with 500 random 30% samples of each
release's live set to give the distribution of the artefact independently of what MITRE
happened to write mitigations for.

**Conclusion instability (Sections 7.3 and 7.5).** Two conclusion-level readouts are computed
on top of the same machinery: the fraction of attribution trials in which the *named actor*
differs between conditions, decomposed by whether the changed verdict is now wrong and whether
a correct verdict was lost; and, for mitigations, the Kendall tau between the ranking of
mitigations by the number of techniques they address at the frozen release and the ranking of
the same mitigation set re-measured at v19.0, with the identity of the top-ranked mitigation
tracked separately.

**Label validity (Section 9).** Four deployed corpora are parsed directly from their own
label files rather than from their papers. Every distinct identifier is checked for liveness
at every published release of the domain the artefact assigns it, or of any domain where the
artefact declares none. The *best-fit release* maximises the share of distinct identifiers
that are live; the *provenance interval* is the set of releases at which **every** identifier
is simultaneously live, and an empty interval is the diagnostic finding that the artefact
mixes mutually exclusive vocabularies.

### 5.4 Reproducibility and evidence tiers

Every number in Sections 6 to 9 is produced by a script in `code/` from the public bundles and
public label files, and the pipeline runs end to end from one shell script. Results are
written as JSON and the tables in this paper are generated from those files, not transcribed.
Three evidence tiers are used and marked throughout. Tier A is our own measurement and
artefacts we read in full from local clones, stated plainly. Tier B is secondary literature
reachable in this environment only through search summaries; it is attributed as reported and
never quoted. Tier C is an audited absence, always stated with the bound of the search that
found it. Section 11 reports one integrity incident inside our own evidence corpus and what
we did about it.

## 6. Measuring Ontology Drift in ATT&CK

### 6.1 Churn: one catastrophe and a floor that never reaches zero

**Figure 1.** Live technique count across Enterprise releases, with per-release additions,
revocations and description rewrites on a shared time axis.

Table 2 is the primary measurement of this paper and most of the rest follows from it.

**Table 2.** Per-release Enterprise churn across consecutive major releases. "Live" is the
technique count after the transition; "Desc. rewritten", "Detection rewritten" and "Tactic
changed" count only techniques live in both releases; `J(ID)` is the identifier Jaccard;
"Edges" counts group-to-technique `uses` edges added and removed.

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

Read the identifier column alone and the episodic reading is irresistible. One transition,
v6.0 to v7.0 on 2020-03-31, has an identifier Jaccard of 0.222, adds 302 techniques, revokes
129 and deprecates 11, and rewrites the group-technique graph by removing 750 edges and
adding 1235. The next largest Jaccard drop in eight years is 0.944, at the most recent
transition. Twelve major releases after the restructuring the catalogue has grown from 428 to
697 live techniques with almost no identifier destruction.

Read any other column and the episodic reading collapses. Description rewrites among
surviving techniques never fall below 27 in any transition and reach 219 out of 223 surviving
techniques at v2.0 to v3.0 and 151 at v10.0 to v11.0, a release whose identifier Jaccard is
0.976. Detection-guidance rewrites are burstier and larger: 583 of 691 surviving techniques
had their detection text rewritten between v17.0 and v18.0, a transition whose identifier
Jaccard is 0.983 and whose description-rewrite count is 49. That single release rewrote the
operational guidance of 84% of the catalogue and would be reported by any identifier-keyed
diff as one of the quietest releases in ATT&CK's history. And the tactic column, empty or
near-empty for sixteen transitions, reads 198 at the most recent one.

This is the two-clock structure, and stating it precisely is the first result. ATT&CK carries
a slow episodic identifier clock and a fast continuous semantic clock, and any risk statement
that reports one without the other is wrong by a factor that depends entirely on which
column the reader happened to look at.

### 6.2 Survival: the concession, measured

**Figure 2.** Identifier survival curves by source release to v19.0, with the recoverable
fraction under transitive `revoked-by` closure overlaid.

**Table 3.** Identifier survival to v19.0 by source release. "Recoverable" counts revoked or
absent identifiers whose transitive `revoked-by` closure terminates at a live identifier.

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

The recoverable column equals the revoked column in every one of the 190 Enterprise survival
rows, and the absent count is zero in every row. Recomputing directly from the v19.2 bundle
gives 858 `attack-pattern` objects — 697 live, 149 revoked, 12 deprecated — and 149
`revoked-by` edges from 149 distinct sources. Every revoked Enterprise technique has exactly
one successor and none dangle. MITRE's Enterprise identifier accounting is complete, and this
paper concedes it without qualification, because conceding it is what makes the remaining
argument non-trivial. A reader holding the usage documentation can defeat any weaker claim in
one paragraph [1].

The concession has a precise scope, and each boundary of that scope is a finding. First, it
is Enterprise-only: in Mobile, 34 survival rows record identifiers absent rather than
tombstoned, and all 76 techniques of Mobile v1.0 are simply gone from v3.0 onward with no
successor edge of any kind (Section 6.6). Second, the relation is never one-to-many. At v19.2
no revoked Enterprise technique has more than one target, so a *split* is representable only
as a set of merges onto whichever survivor the curator judges narrowest. Eight Enterprise
targets absorb 20 predecessor identifiers, the largest — T1685 — absorbing five, and three
chains require transitive closure to resolve. Third, the retirement relation routinely
crosses abstraction levels: of the 149 edges, 119 map a top-level technique onto a
sub-technique, 13 top onto top, 10 sub onto sub, and 7 *promote* a sub-technique to a parent.
An identifier crosswalk that resolves in one hop onto a live identifier, reports complete
success, and silently narrows the extension of the original assertion is not a broken
crosswalk. It is a crosswalk doing exactly what a 1:1 relation can do, in a situation that
needs more than a 1:1 relation — which is why the remedy in Section 10 is borrowed from an
ontology framework that already separates exact from inexact successors [54].

### 6.3 The tactic layer, and the one move no crosswalk can express

Across all three domains and every release our extraction finds 5,599 revocation edges. Zero
of them involve an `x-mitre-tactic` object. The tactic layer has no retirement relation at
all.

This is not a theoretical gap. Between v18.1 and v19.2 the STIX object carrying ATT&CK
identifier TA0005 keeps its UUID and its identifier, while its name changes from *Defense
Evasion* to *Stealth*, its shortname from `defense-evasion` to `stealth`, and its
`x_mitre_version` stays at 1.0. A new tactic TA0112, *Defense Impairment*, is minted alongside
it to hold the separated concept, and the technique T1562 *Impair Defenses* — a top-level
technique with twelve children — is retired into the new arrangement [78]. Any analytic that
joins on TA0005 across that boundary compares two different concepts, with no revocation, no
version increment and no edge to follow. Our corpus finds 102 in-place renames across all
object types and both domains' tactic layers contain one: TA0005 in Enterprise, and TA0034
in Mobile, renamed from *Effects* to *Impact* with an unchanged object version. This is the
edit that OBO Foundry's term-stability principle exists to forbid: a changed referent requires
a new identifier [54].

The technique-level consequence is the merge pattern of Section 6.2 in its sharpest form.
`revoked-by` cannot point a technique at a tactic, so the promoted concept *Impair Defenses*
is mapped to T1685 *Disable or Modify Tools* — one of its own former children. Normalizing
`{T1562}` forward returns `{T1685}` in one hop, against a live identifier, with nothing
dropped. An analyst who wrote T1562 because a report said the actor disabled a host firewall
is thereby recorded as asserting that the actor tampered with security tooling: a narrower
and different claim, in a tactic that did not exist when the artefact was written. The
mechanism reports success. The measurement is wrong.

### 6.4 Intensional drift, and why ATT&CK cannot signal it

**Figure 3.** Silent semantic drift among identifier-stable techniques: share with edited
descriptions and share substantially rewritten, by source release, measured at v19.0.

**Table 4.** Semantic drift among techniques live at both the source release and v19.0.
Token Jaccard is computed over lowercased alphanumeric token sets of the description;
a substantial rewrite is token Jaccard below 0.8.

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

Table 4 must be read as a function of elapsed time, not of release quality. The v18.0 row is
low because only one transition separates it from the analysis release, not because ATT&CK
has stopped rewriting. The right reading is the decay of a cohort: of the 415 techniques that
were live at v7.0 and are still live at v19.0, 0.749 have had their descriptions edited and
0.386 have been rewritten past the substantial threshold, with mean token similarity 0.808.
For the v11.0 cohort the corresponding figures at v19.0 are 0.465, 0.208 and 0.895; for the
v15.0 cohort, 0.275, 0.087 and 0.956. These are identifiers whose survival rate over the same
interval is 0.977 and 0.975. The instrument keeps the scale markings and moves what they mean.

Converted to a practitioner's clock, the two clocks run at different speeds and in opposite
directions. For every Enterprise cohort from v7.0 onward the time to 10% *hard* identifier
staleness is never — it does not happen through v19.0 — and the unrecoverable fraction is at
most 0.2%. The time to 10% *substantive* staleness, counting a technique as stale if it is
gone, substantially rewritten, or reassigned to a different tactic, is 0.50 to 2.01 years with
a median of 1.51. Restricting to text change alone, excluding both tactic changes and
revocations so that the most recent re-cut cannot be blamed, gives 0.99 to 2.01 years with a
median of 1.52. Semantic half-life is 4.5 to 6.1 years. A pinned post-2020 Enterprise label
set therefore has an infinite identifier half-life and an eighteen-month first-10% semantic
staleness schedule, simultaneously.

Could a consumer detect this from the bundles? ATT&CK carries `x_mitre_version` on every
object, and the natural assumption is that a change in meaning is announced by a change in
that field. It is not.

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

Over 8,359 carried-over technique pairs, 1,358 (0.162) had their description rewritten. Of
those, 487 (0.359) carried no version increment. In the other direction, 1,077 version
increments carried no text change at all. As a detector of description change, `x_mitre_version`
has **precision 0.447 and recall 0.641**: it misses more than a third of the rewrites and more
than half of its alarms are false. A consumer who re-reads every technique whose version
increased does nearly half the work for nothing and still misses over a third of the changes.
MITRE's own tooling knows this — `diffStix` defines a distinct change class for objects
patched while the version stayed the same, and annotates unintended version changes as a
historical defect it must defend against [34, 48]. The contract consumers actually follow
offers a binary current-or-retired filter and no expression for a surviving object whose
meaning moved [1]. The gap is architectural, not an oversight: the tooling can see the change
and the published consumer interface has no vocabulary in which to state it.

This is the paper's central negative result, and it is the answer to the strongest practical
objection in the field. The advice to pin a release is correct and insufficient. Pinning fixes
identity. It does not fix intension, it leaves the analytic silently diverging from the
meaning its own labels now carry, and no signal in the published data reliably tells the
consumer when that has happened.

### 6.5 How much of ATT&CK's growth is intelligence?

**Figure 4.** Per-transition decomposition of new group-technique edges for pre-existing
groups into genuine new intelligence, new technique, sub-technique refinement and revocation
re-mapping.

**Table 5.** Knowledge-growth decomposition, Enterprise. Edges for groups newly added to
ATT&CK are excluded from the denominator; bookkeeping share is (refinement + re-mapping) over
all new edges for pre-existing groups.

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

Across all Enterprise transitions 5,516 group-technique edges are added, of which 2,442 belong
to groups newly added to ATT&CK. Of the remaining 3,074 added for groups that already existed,
1,752 are genuine new intelligence about a pre-existing pairing, 330 credit a group with a
newly minted technique, 487 are sub-technique refinements of an edge the group already had,
and 505 restate an edge whose technique was revoked and replaced. The bookkeeping share is
**992/3074 = 0.323**.

That headline conceals a distribution with a heavy tail, and the tail is the point. The
restructuring transition is 0.750 bookkeeping over 1,059 edges. Eight transitions are below
0.05. But three recent transitions are not: v12.0 to v13.0 is 0.380 over 71 edges, v14.0 to
v15.0 is 0.340 over 100, and the most recent transition, v18.0 to v19.0, is **0.470 over 164
edges** — the highest share since the restructuring, driven entirely by 77 revocation
re-mappings. A reader who plots ATT&CK's edge count over time and reads it as a curve of
accumulating adversary knowledge is reading a curve that is roughly a third bookkeeping
overall, and nearly half bookkeeping in the release that shipped four months before this
analysis. Independent evidence from the benchmark side points the same way: the 4.3x
label-space growth between one LLM CTI benchmark generation and its successor is roughly 96%
pre-existing catalogue, with only six genuinely new entries [6].

### 6.6 Recurrence: this is a hazard, not a wound

The episodic reading of Table 2 has one more defence available: that the 2020 restructuring
was a singular event, now finished. Extending the measurement to all three domains refutes
it. Five major-to-major transitions across the corpus have identifier Jaccard below 0.80:
Mobile v2.0 to v3.0 (2018-10-23, J = 0.000), Enterprise v6.0 to v7.0 (2020-03-31, J = 0.222),
ICS v8.0 to v9.0 (2021-04-29, J = 0.778), Mobile v10.0 to v11.3 (2022-07-07, J = 0.268) and
ICS v18.0 to v19.0 (2026-04-28, J = 0.698). That is 5 events in 47 transitions, a hazard of
**0.106 per major transition**, one event per 4.41 domain-years over 22.05 observed
domain-years — roughly one restructuring somewhere in ATT&CK every 1.5 calendar years.

Two of these events matter more than their Jaccard suggests. Mobile's 2018 event is the most
destructive in the corpus and it predates the Enterprise restructuring: a wholesale ATT&CK-ID
renumbering in which all 128 STIX identifiers are preserved but all 76 old ATT&CK identifiers
vanish, with only 15 `revoked-by` edges in the target release and **zero** of the 76
recoverable. It is invisible to STIX-identifier-keyed tooling and uncrosswalkable by any
mechanism MITRE publishes. And ICS's event is happening now: v19 revokes nine T0xxx techniques
into a shared namespace and introduces ICS sub-techniques for the first time — 0 at v18.1, 18
at v19.0 — which is structurally the same move Enterprise made in 2020, six years later, with
all nine remaps recoverable.

Can a consumer see one coming? We tested for leading indicators at the release level over 17
lagged Enterprise pairs, correlating each candidate feature at transition *k* with the
revocation rate at *k+1* by Spearman rank correlation with 20,000-shuffle permutation tests.
The largest coefficient is detection-field edits at ρ = +0.377, permutation *p* = 0.134;
nothing else comes close, and tactic changes correlate negatively. The largest coefficient
anywhere in the three-domain panel, ICS renames at ρ = +0.733, has *p* = 0.054 on *n* = 10.
Technique-level hazard modelling is worse than null: the 131 techniques doomed at v7.0 had
been *edited less* in the preceding release than the survivors, on both description edits
(0.168 against 0.336) and version bumps (0.176 against 0.372). Restructuring waves are not
forecastable from the public bundles. This is a load-bearing negative result, because it
removes the option of a triggered response: a consumer cannot time-hedge, so any protocol that
helps must be standing rather than event-driven.

### 6.7 The most recent wave, measured as a case

The v18.1 to v19.2 revocation wave is the cleanest available test of whether drift still
lands on things that matter. Seventeen live techniques were revoked, including the whole
T1562 *Impair Defenses* family, re-cut across T1684 to T1690 [78]. Measured on the v18.1
graph, the blast radius is 84 group-technique edges, 155 software-technique edges, 47
mitigations and 17 detection relationships, and 52 of 168 group profiles lose at least one
identifier. T1562.001 *Disable or Modify Tools* was ranked **33 of 599** techniques by `uses`
edges in the release it left. This is not the long tail. Section 7.6 settles the long-tail
objection properly.

## 7. Downstream Impact of Drift on CTI Analytics

Section 6 measured the instrument. This section measures what the recalibration does to
conclusions drawn with it. Every experiment holds the adversary intelligence fixed and moves
only the vocabulary, so every difference reported below is attributable to the instrument and
to nothing else.

### 7.1 Attribution under vocabulary mismatch

**Figure 5.** Top-1 attribution accuracy by condition against the artefact's vocabulary
release, with the drift penalty and its bootstrap confidence band.

**Table 6.** Controlled attribution experiment at k = 10, analysis release v19.0. "OOV" is the
share of observed identifiers not live at v19.0. The drift penalty is back-projected minus
naive; recovery is the share of that penalty returned by ATT&CK-Norm.

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
effect tracks the instrument, not the adversary. A legacy artefact written in the v1.0
vocabulary and consumed by a v19.0 analytic loses 42.2 points of top-1 accuracy relative to the
same intelligence consumed in its own vocabulary, with a bootstrap interval of [37.8, 46.8];
at v6.0 the penalty is 46.2 [41.6, 51.0]. After the restructuring the penalty collapses to 7.0
at v7.0 and settles between 1.2 and 3.4 points thereafter, with the interval touching or
crossing zero at v11.0, v14.0 and v16.0.

Three readings of that table are available and only one survives.

The first is that the modern penalty is negligible, so the problem is historical. This fails on
its own arithmetic. A 1.6-point penalty at v18.0 is one release boundary, six months. It is not
an asymptote; it is a per-release increment, and the artefacts the field actually consumes —
benchmark label files, published coverage layers, training corpora — are years old, not six
months (Section 9). Moreover the aggregate hides its own concentration. Stratifying the
candidate universe by whether a group has at least one technique unique to it within that
universe, the modern penalty is 2.5 to 7 times larger on the identifiable stratum: +0.0344
[+0.0101, +0.0607] against +0.0089 [−0.0010, +0.0189] at v12.0; +0.0331 [+0.0166, +0.0497]
against +0.0049 [−0.0010, +0.0118] at v16.0; +0.0239 [+0.0109, +0.0391] against +0.0067
[+0.0019, +0.0125] at v18.0. The specificity fraction our corpus computes independently —
0.325, 0.309, 0.298 — reproduces the published finding that roughly a third of ATT&CK groups
have any group-specific technique [59]. The mechanism is immediate once stated: a group's
identifying token is by definition a rare technique, and rare techniques are the ones ATT&CK
adds, splits and revokes. Drift attacks precisely the signal on which attribution depends. An
average taken over a population that is mostly unattributable understates the effect on the
subset that carries the task.

The second reading is that the enormous legacy penalties are the real finding. They are not,
or not straightforwardly, because they are inflated by the back-projection. Collapsing dense
modern profiles onto a coarse pre-2020 vocabulary makes them collide with each other in a way
no 2018 system experienced, since 2018 profiles were genuinely sparse. Running the missing
control — real archival v-era labels against real archival v-era profiles — gives self-consistency
0.969 at v1.0 against the back-projected condition's 0.668, and 0.900 against 0.663 at v6.0.
The collision artefact depresses the control condition and therefore *deflates* the reported
penalty, while the perfect-recall idealisation inflates it; in the modern regime the two
converge (0.856 against 0.837 at v12.0; 0.846 against 0.841 at v18.0), so the modern claim is
unaffected either way. Table 6 also reports the back-projection loss directly: at v1.0, 389 of
697 modern techniques have no v1.0 ancestor and profiles retain 0.618 of their distinct
identifiers; at v7.0, 155 of 697 and 0.903; at v18.0, 7 of 697 and 0.998. The legacy
conditions all consume the same lossy observation, so the contrast between them is clean even
though their absolute level is not.

The third reading, and the one we defend, is that the table measures comparability rather than
capability. Every absolute number here is an internal-consistency score computed inside one
curator's graph, where observation, profile, ground truth and back-projection map all come
from MITRE. None of them is a statement about how well TTP attribution works. What the design
licenses is the *contrast*, because the contrast holds the intelligence fixed.

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

The absolute accuracies in Table 7 move enormously with the design choices — IDF-cosine over
software-mediated profiles scores 0.693 at v1.0 where plain overlap scores 0.240 — which is
itself a warning about reading any absolute attribution number. The penalty's *sign and order
of magnitude* do not move. Every one of the 30 cells shows a positive drift penalty; the
pre-restructuring penalty ranges from 18.7 to 56.7 points and the post-restructuring penalty
from 0.3 to 5.3. Normalization gain follows the same pattern, 6.0 to 32.0 points before the
restructuring and 0.0 to 2.0 after it. Whatever else is fragile here, the existence and the
regime structure of the drift penalty are not.

### 7.3 From scores to verdicts

A score movement is a methodological curiosity; a changed verdict is a changed conclusion.
Table 10 reports the verdict-level readout of the same trials.

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

For a v1.0-vocabulary artefact the named actor changes in 0.722 of observations and 0.712
change to a *wrong* actor; at v6.0 the figures are 0.790 and 0.774. These are not score
degradations, they are different answers to the question the analytic was asked. Across a
single modern release boundary the verdict still changes in 0.022 of observations and every one
of those changes is to a wrong actor. The final column is the finding that should most trouble
a practitioner: applying normalization *itself* changes the verdict in 0.368 to 0.442 of
pre-restructuring observations and in 0.006 to 0.030 of modern ones. Silently normalizing an
inherited label set is therefore not a neutral cleanup step. It is an intervention that
changes published conclusions, and it must be declared as one.

### 7.4 Is this separable from the single-version noise floor?

The strongest published objection to everything above is that ATT&CK labelling is so noisy at
a *single* pinned release that drift is a second-order term on a first-order problem.
Detection products pinned to one release assign disjoint technique labels to the same
behaviour — one vendor's rule for a named-pipe impersonation carries T1134 while another's
rule for the same pipe write carries a four-identifier set with zero overlap [74] — roughly a
third of extraction errors fall between same-tactic, description-overlapping techniques [20],
and most ATT&CK groups have no group-specific technique at all [59]. Recent work goes further
and argues that LLM agents can reproduce documented APT profiles well enough to undermine the
premise of TTP-based attribution [66]. We concede the noise floor completely: it is large, and
this paper does not claim drift dominates it.

Separability is a design property here, not an assumption. Every condition draws its
observations from the same curated ATT&CK edges, so the labelling process is identical across
conditions and cancels in the contrast. But holding a nuisance term at *zero* licenses
separability while leaving *additivity* untested, and an interaction cannot be seen in a design
with one level of the moderator. We therefore ran the missing factorial: each observed
technique is replaced with probability ρ by a sibling sub-technique, its parent, or a
same-tactic technique — a substitution shaped like the vendor disagreement the objection
describes — applied in the modern vocabulary before back-projection so that it flows
identically into all four conditions, at 1,200 trials per cell.

The penalty survives at every noise level and at every boundary. At v1.0 it falls from +0.439
at ρ = 0 to +0.342 at ρ = 0.4; at v6.0 from +0.476 to +0.317; at v12.0 it is +0.017 against
+0.021 and at v18.0 +0.012 against +0.012. Strict additivity fails in the large-drift regime:
the pre-restructuring penalty is attenuated by 22 to 33 percent at ρ = 0.4, because noise and
drift consume the same finite signal. In the modern regime the penalty is flat in ρ, that is,
effectively additive. The correct claim is therefore **separable and sub-additive**, and the
noise-free figures in Table 6 are *upper bounds* on drift's contribution in a noisy world.
Normalization degrades faster than the penalty does — recovery at v1.0 falls from 0.44 at
ρ = 0 to 0.30 at ρ = 0.4 — so a repair protocol returns less exactly as label quality falls,
which is the regime where it is most needed.

### 7.5 Coverage claims and mitigation leaderboards

**Figure 6.** Coverage claims under a frozen capability, and the random-portfolio sweep of the
same artefact.

**Table 8.** Coverage claims under a capability frozen at release V and re-measured at v19.0.
The identifier artefact is the gap between the naive and normalized re-measurements.

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

A capability frozen at v6.0 that could legitimately claim 97.0% coverage reads 17.4% when its
identifiers are matched naively against v19.0 and 33.9% after normalization. Nothing about the
capability changed. The 79.6-point collapse decomposes into two entirely different quantities:
16.5 points are pure identifier artefact, repairable by arithmetic, and the remaining 63.1
points are the catalogue growing underneath a fixed portfolio, which is not an artefact at all
but the honest statement that the defender's coverage of the current threat model has fallen.
Conflating those two is exactly what an undeclared coverage percentage does. In the modern
regime the artefact term shrinks to 1.1 to 2.2 points while the growth term remains large:
frozen at v17.0, a claim of 84.7% reads 80.2% one year later, of which 2.0 points are
bookkeeping. The random-portfolio sweep confirms that none of this depends on which techniques
MITRE happened to write mitigations for: over 500 random 30% portfolios per release the mean
naive error is −26.49 points at v1.0 and −1.00 at v18.0, with standard deviations under 0.55
throughout, and normalization removes roughly four points of it at v1.0 and 0.70 at v18.0.
This is the measurement behind a practitioner complaint that has been made repeatedly without
numbers: that vendor coverage percentages are padded, that a 100% claim is a red flag, and
that at least three incompatible denominators circulate [80, 82, 84].

Ranking is the more consequential readout, because defenders use ATT&CK to prioritise.

**Table 11.** Mitigation leaderboard reordering. Kendall tau compares the ranking of
mitigations by techniques addressed at the frozen release against the same mitigations
re-measured at v19.0.

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

Here, and only here, normalization is close to a cure: mean Kendall tau rises from 0.931 to
0.992 across the sweep, three of the four naive rank-1 flips vanish and none are introduced.
But the rank-1 column is a warning on its own terms. The single highest-priority mitigation
changes identity at four of fourteen frozen releases, including at v17.0 — one release before
the analysis — where naive tau is 0.976. A near-perfect rank correlation coexisting with a
changed top-ranked control is exactly the failure mode a defender cannot afford, because the
leaderboard is consumed at the top and reported as an aggregate.

### 7.6 The long tail objection, adjudicated

The remaining defence is that drift lands on techniques nobody reports. MITRE's own bias
analysis and sightings work establish that observed adversary behaviour is heavily
concentrated in a short head of techniques [49], so churn among rare identifiers should barely
move any frequency-weighted quantity.

We tested it by repeating the frozen-capability experiment with techniques weighted by
documented prevalence, the number of `uses` edges a technique carries at v19.0. The artefact
*grows* under weighting rather than shrinking: frozen at v6.0 it is +16.50 points unweighted
and +20.01 weighted; at v10.0, +1.58 against +1.43; at v18.0, +2.15 against +1.57. In this
corpus the head is only moderately concentrated — the fifteen most-referenced techniques carry
0.285 of all `uses` edges at v19.0 — and the head is itself a product of restructuring, since
the most recent revocation wave removed T1562.001 at rank 33 of 599 (Section 6.7).

The limitation must be stated in the terms it deserves rather than argued away. `uses` edges
count how many groups, malware families and tools MITRE has *documented* as employing a
technique. That is a cumulative documentation stock, biased toward behaviours that are easy to
narrate in a report and monotone in time, and it is not an alert stream. Defender telemetry is
materially more concentrated than documentation. So: the long-tail objection is refuted for the
fraction of the *written CTI corpus* affected by drift, and it is untested for the fraction of
the *alert stream* affected, because the telemetry that would test it on its own data is not
reachable here. We claim the first and not the second.

## 8. ATT&CK-Norm: A Version-Normalization Protocol

The protocol evaluated throughout this paper is deliberately minimal. Given a set of
identifiers and a target release, ATT&CK-Norm (1) resolves each identifier transitively
through the target's `revoked-by` graph, cycle-safe and bounded at ten hops; (2) drops and
*counts* identifiers that are deprecated or absent in the target rather than discarding them
silently; and (3) returns a four-way residual ledger — kept, merged, demoted, dropped — rather
than a set. A fourth branch, rolling an unresolvable identifier up to a surviving parent, is
off by default. Each of those three design decisions is a measurement result, not a
preference.

**Roll-up is dead code, and measuring that is the finding.** We re-ran the attribution
experiment with roll-up as the only difference, 54 conditions by 500 trials, and audited the
branch on real archival group profiles for all 18 major releases and on four deployed CTI
corpora covering 37,447 label instances. Top-1 accuracy is identical to three decimals in
every condition and the paired bootstrap interval on the difference is [+0.000, +0.000]. A
broader sweep across every domain and major release fires the branch three times in 12,027
resolutions. The reason is structural: MITRE never orphans a sub-technique — a revoked
sub-technique always resolves to a live target — and deprecations without a successor are
top-level, so roll-up's precondition does not arise in ATT&CK's data. The correct default is
therefore to drop and count, not because drop wins a contest but because roll-up wins nothing
measurable while adding an untested path that can fabricate a parent-level assertion the source
never made.

**The residual ledger is the whole protocol.** A set-valued normalizer destroys cardinality at
merges: because the map is a function and not an injection, `{T1562, T1562.001, T1562.006}` and
`{T1562.001}` both return `{T1685}`, and a caller cannot distinguish ten clean identifiers from
ten of which three merged and two dropped. On real corpora this is not hypothetical. TRAM's
bootstrap label set goes from 537 to 503 distinct live classes, with 28 targets absorbing 62
source classes and 14.75% of its 25,770 label instances landing in a merged class; rcATT goes
from 215 to 199 with 9.37% of 6,235 instances merged. A benchmark whose classes silently merge
537 into 503 is not the same benchmark, and a score computed on it is not comparable to a score
computed before the merge.

**Demotion is detectable even though it is not repairable.** Because 119 of 149 Enterprise
revocation edges map a top-level technique onto a sub-technique and 7 map the other way
(Section 6.2), a resolution that succeeds mechanically routinely changes what the artefact
asserts. ATT&CK-Norm cannot fix this — no identifier arithmetic can — but it can and does
report it, which is the difference between a lossy transformation and a silent one.

What the protocol provably cannot deliver is meaning. Across the release that dissolved the
field's most-used tactic, normalization returns all 674 identifier-stable techniques unchanged
and signals zero drift, while 198 of them changed tactic and 41 changed description hash. Its
attribution gain is +20.1 points on average for pre-v7.0 artefacts and +0.77 points after
v7.0, with the gain's 95% interval including zero in 23 of 36 post-v7.0 conditions; its one
clean win is ranking (Section 7.5). And it fails in a way that matters on real data: on the
CTIBench extraction corpus it would confidently report seven unrepairable deprecations which
are in fact seven live Mobile identifiers on a single row mis-typed as Enterprise (Section 9).
Normalization buys comparability of identifiers. It buys nothing about whether two identifiers
mean the same thing, and a paper that claims otherwise repeats the error it set out to
diagnose.

## 9. Label Validity of Deployed CTI Corpora

Sections 6 to 8 measure what drift can do. This section measures what it has already done to
artefacts the field is using now. Each corpus is parsed from its own label file rather than
from its paper, because the paper is not what the model is trained on.

**Figure 7.** Label-validity curves for four deployed CTI corpora across every published
ATT&CK release.

**Table 9.** Label validity of deployed corpora. "Fit" is the best achievable share of
distinct identifiers live at any single release; "releases where all labels valid" is the
provenance interval.

| Corpus | Distinct labels | Label instances | Sub-technique labels | Best-fit release | Fit | Releases where all labels valid | Invalid today | Repairable |
|---|---|---|---|---|---|---|---|---|
| ctibench-ate | 120 | 397 | 0 | v14.0 (2023-10-31) | 0.942 | **none** | 8 (0.067) | 1 |
| rcatt | 215 | 6235 | 0 | v4.0 (2019-04-30) | 1.000 | 8 (v4.0–v6.3) | 107 (0.498) | 99 |
| tram-bootstrap | 537 | 25770 | 344 | v13.0 (2023-04-25) | 0.939 | **none** | 43 (0.080) | 43 |
| tram2 | 50 | 5143 | 24 | v8.2 (2021-01-27) | 1.000 | 18 (v8.2–v16.1) | 2 (0.040) | 2 |

Two of the four corpora have an **empty provenance interval**: no ATT&CK release ever
published makes every one of their labels simultaneously valid. For CTIBench's extraction task
the best any release achieves is 0.942 at v14.0 — a benchmark whose gold answer key cannot be
attributed to any edition of the vocabulary it is written in. The rcATT training corpus is
internally consistent and dates cleanly to the v4.0–v6.3 window, and that is precisely why it
is the starkest case: 107 of its 215 identifiers (0.498), covering 0.380 of its 6,235 label
instances, are invalid at v19.2. It was consistent when it was made and it is half dead now
[8, 44]. TRAM's bootstrap set has 43 invalid identifiers, all repairable, over 25,770
instances [3].

Version declarations are the mechanism that would make all of this checkable. There are none.

**Table 12.** ATT&CK version declarations found in the documentation of deployed corpora.

| Corpus | Documentation files scanned | ATT&CK version declarations found |
|---|---|---|
| cti-bench | 2 | 0 |
| rcATT | 2 | 0 |
| tram | 15 | 0 |

Table 12 is a thin scan and we do not rest the adoption claim on it: two of the three
repositories contributed two files each. We therefore measured adoption where coverage claims
actually live, in ATT&CK Navigator layers, whose format has carried a `versions.attack` field
since layer format 4.0 [15]. Across 69 Navigator-format layer files in local clones, five
declare it — and all five are MITRE's own sample or test fixtures [18]. Of 57 published vendor
threat-report layers from eleven security companies, **zero** declare an ATT&CK content
version: 39 are in layer format 2.2, where the field does not exist, and 18 are in formats
4.1 to 4.3, where it exists and every one of them omits it [79]. The cost is measurable: those
57 layers carry 2,143 technique annotations of which **739 (34.5%) name an identifier that is
revoked or deprecated at v19.2**; 49 of the 57 files contain at least one; 72 of the dead
annotations are deprecations with no successor; and 5 name identifiers absent from v19.2
entirely, four of them Mobile identifiers, one sitting on a layer whose declared domain is
Enterprise. Opened today in a current Navigator, every one of these silently re-bases onto the
current release, because the version field is optional and defaults to current [15, 16].

Declaring a version is necessary and not sufficient. One public remapping repository announces
a deliberate migration to ATT&CK v12.0 and its inherited label split still carries 203 dead
label occurrences, 128 of them T1064, an identifier revoked five releases before the declared
target [10]. Two further audits point the same way: a widely used attack-graph system froze its
ATT&CK ontology as a dated HTML scrape with parent-only templates [2], and a six-system survey
of TTP tooling found five different ATT&CK ontologies and two declared versions between them
[3]. The benchmark generation problem is the same problem in a more consequential place.
CTIBench's extraction task carries zero sub-technique identifiers against an undeclared,
roughly v15-era vocabulary [4, 30], while its successor generation is dominated by
sub-technique labels and overlaps it only partially at parent level [6]; a separate benchmark
line grew from 691 to 1,860 QA pairs under one identifier and the same nine-task taxonomy
[29]. Comparability across benchmark generations is asserted by construction and established
nowhere, which is why the live-API and telemetry-grounded designs are the right structural
response even where their other trade-offs are worse [13, 28].

One finding here cuts against our own thesis and we report it as such. Of CTIBench's eight
invalid identifiers, seven are marked unrepairable — and all seven come from a single row
whose platform column says Enterprise while its entire gold set is Mobile-only, and all seven
are live in `mobile-attack` v19.2. Seven-eighths of that corpus's apparent drift damage is not
drift at all; it is a single-version labelling error, and a normalizer without a domain guard
would report seven confident deprecations and be wrong seven times. Label-validity analysis
that does not separate drift from data-entry error will over-attribute to drift, and ours would
have, had we not checked the rows.

## 10. Discussion and Reporting Discipline for CTI Research

The measurements support a narrower thesis than the one this paper set out to test, and a more
durable one. ATT&CK's referential machinery is close to as good as a 1:1 crosswalk can be, and
it is almost never used. Its semantic machinery does not exist, and nothing in the ecosystem
detects semantic change. The remedy is therefore not a better crosswalk. It is a reporting
discipline that makes the vocabulary of a CTI artefact a declared, checkable property of that
artefact.

Concretely, four lines a reviewer can check in under a minute. **(1)** The ATT&CK domain, the
exact release, and the SHA-256 of the bundle, recorded in the artefact rather than in the
prose. **(2)** Whether identifiers were normalized, and onto which target release. **(3)** The
residual: kept, merged, demoted and dropped counts, with the dropped identifiers listed
verbatim. **(4)** For any cross-time comparison, a statement that both sides were projected
onto one reference release. Benchmarks carry two more: **(5)** the label granularity policy —
parent-only or mixed — and the class count before and after normalization, and **(6)** a
continuous-integration check that fails when any gold label is not live in the declared
release. Vendor coverage claims carry two of their own: **(7)** the ATT&CK version and the
denominator as an absolute number of live techniques next to the percentage, and **(8)** the
claim re-stated against the current release, or explicitly marked as-of.

The engineering cost is a JSON header, a table and roughly thirty lines of code. The real cost
is reputational, and naming it is part of the argument: a residual line makes label decay
public. rcATT's would read 0.498 of identifiers and 0.380 of label instances invalid at v19.2.
Coverage percentages would become non-monotone in public, because item (8) forces a vendor to
restate an 84.7% claim as 80.2% one year later. Benchmark scores would stop being
cross-release comparable by default, which is the point rather than a side effect. This is the
same trade the malware-classification literature made when it accepted temporal splitting: a
class of impressive numbers became unpublishable, and the field got better [35, 67].

For MITRE the recommendations are ported rather than invented, and each one already exists in
a neighbouring vocabulary. Adopt a two-tier successor relation, keeping `revoked-by` for exact
successors and adding an inexact-successor relation so that T1562 can point at all seven of its
v19 successors and at the tactic that absorbed it, instead of at one of its own former
children [54]. Add a controlled obsolescence-reason vocabulary — superseded-by-split, merged,
re-scoped, promoted-to-tactic, out-of-scope — so that drop and merge are distinguishable, as
OBO does with a dedicated annotation property [54]. Make obsolescence visible in the
human-readable label, so that tools joining on name stop working against a dead concept rather
than working silently [54]. Enforce referent stability at a stable identifier: renaming TA0005
in place is the specific edit the stability principle forbids, and *Stealth* should have been
a new tactic identifier with TA0005 obsoleted [53, 54]. Add prior-version and
backward-compatibility links on the collection object, which OWL has had for two decades [57].
Publish the evolution mapping as a first-class versioned artefact typed with complex change
operations — merge, split, move, substitute — rather than as an untyped diff; `diffStix`
already computes the underlying operations, and typing them is what makes the
bookkeeping-versus-intelligence split of Section 6.5 computable rather than asserted [26, 34].
Finally, make the Navigator layer's ATT&CK version field mandatory: it is optional today and
defaults to current, which is why every published coverage layer we found is
version-orphaned [15, 16].

There is also a claim the CTI quality literature should absorb. Vocabulary versioning is a
quality dimension in its own right, orthogonal to accuracy, timeliness, provenance and
interoperability as those are currently defined [60, 76]. It is not provenance, which records
where an item came from rather than in what vocabulary it is expressed; it is not
interoperability, which concerns format; and it is not timeliness, which concerns the age of
the intelligence rather than the age of the scale it is measured on. An artefact can score
perfectly on all four and still be uninterpretable, which is what Table 9 shows for rcATT.

Finally, what an SCI-level contribution in this space must demonstrate, stated as the bar we
have tried to clear. It must measure the ontology rather than describe it, over the full
release history rather than a convenient window. It must show a *conclusion* changing, not a
score moving — Tables 10 and 11 are the form that takes. It must hold intelligence content
fixed while varying the vocabulary, or it cannot attribute anything to drift. It must concede
the producer's apparatus where the apparatus is complete, and locate the failure precisely. It
must test its result against the strongest published rival explanation rather than the
weakest, which here means the single-version noise floor and the long tail. And it must state
what its remedy cannot do: ours cannot repair meaning, and we measured how much it cannot
repair.

## 11. Threats to Validity

**The loop is closed inside ATT&CK.** In the attribution experiment the observation, the
profiles, the ground truth and the back-projection map all originate from one curator. The
absolute accuracies of 0.67 to 0.97 are therefore internal-consistency scores and are never
statements about attribution performance. The `historical` diagnostic partly opens the loop
and shows what opening it costs: real archival artefacts score 0.159 at v1.0 against the
back-projection's 0.231, that is, worse. The experiment that would close this threat properly
is the one the field does not have: a double-labelled incident corpus in which two independent
analysts label the same intrusions under two ATT&CK releases, yielding the drift term and the
inter-analyst term simultaneously and from outside MITRE's own edges. We name it as the
decisive missing instrument rather than approximating it.

**The control condition is a reconstruction.** What we call the back-projected condition is
2026 intelligence transcribed into an older vocabulary, not a system that existed in that era;
Section 7.1 quantifies the gap at 0.969 against 0.668 at v1.0 and near-zero in the modern
regime. Two biases run in opposite directions — profile collision deflates the penalty,
perfect recall inflates it — and the measured net in the pre-restructuring regime is downward,
so the legacy penalties are conservative. The naive condition is also a worst case rather than
a typical one: MITRE re-mapped its own `uses` edges to the most specific sub-technique, so
modern profiles are nearly pure sub-technique level while the back-projected artefact is pure
parent level, and exact matching scores zero across that boundary. Real legacy artefacts are
mixed-granularity, so the true naive condition lies between our naive and normalized columns.
Relatedly, the normalizer is close to the algebraic inverse of the back-projection, so the
reported recovery is an upper bound on what it achieves on real, typo-bearing, cross-domain
label sets — as the CTIBench row in Section 9 demonstrates directly.

**Prevalence is documentation, not telemetry.** The weighting in Section 7.6 uses `uses` edge
counts, a cumulative and monotone documentation stock computed from the same release whose
churn is being measured, so a revoked technique carries its weight with it. The weighted result
is therefore not independent evidence in the way telemetry would be, and the long-tail
objection remains untested on the alert stream.

**Metric choices.** Token-set Jaccard with a 0.8 threshold is a blunt instrument for semantic
change: it will call a substantial reorganisation of identical content a rewrite, and will miss
a meaning-reversing edit of a few words. We mitigate by reporting the mean-similarity series
alongside the thresholded share (Table 4) and by showing that the identifier-level and
text-level clocks behave differently regardless of the cut. The bookkeeping decomposition of
Section 6.5 depends on the order in which causes are tested; we test re-mapping before
refinement, which charges ambiguous edges to bookkeeping, so 0.323 is an upper bound under
that ordering and we say so rather than presenting it as the only possible reading.

**Internal number discipline.** Two of our own quantities have small discrepancies between
independent computations over the same bundles, and we report them rather than silently
selecting one. The semantic-metadata analysis records 1,358 description changes and 487
without a version increment; a direct recomputation over the release bundles under a slightly
different carried-over-pair rule returns 1,366 and 494, a difference of roughly 0.6% that does
not move precision or recall to three decimals. The tactic-change count for the most recent
transition is 198 over major releases and 201 when computed over the patch releases that
actually bracket the change. Both are the same phenomenon measured with two eligibility rules,
which is exactly the ambiguity this paper argues must be declared.

**Evidence tiering and one corpus-integrity incident.** Secondary literature was reachable in
this environment only through search summaries; it is attributed as reported and never quoted,
and no positioning claim rests on a number we could not see in an artefact. An automated
integrity check over our own 112 evidence notes flagged 10 whose front matter had become
detached from their body. Every affected claim was either re-derived from a primary artefact
or removed; one claim about a third-party synchronisation project's published outputs was
removed from the manuscript entirely rather than repaired, and the audited-absence claims in
Section 3 are stated with the bound of the search that found them. We report this because a
paper about undeclared provenance that concealed a provenance failure in its own evidence base
would be self-refuting.

## 12. Conclusion

ATT&CK is the measuring instrument of cyber threat intelligence, and it has been re-issued 109
times without any downstream result recording which issue it used. We measured the
recalibration. Identifier churn is episodic, currently mild in Enterprise, fully accounted for
by MITRE, and recurrent across domains at a hazard of 0.106 per major transition that no
leading indicator in the public bundles predicts. Semantic churn is continuous, invisible to
identifier arithmetic, and undetectable from ATT&CK's own metadata at precision 0.447 and
recall 0.641. Nearly a third of apparent knowledge growth for pre-existing actors is
bookkeeping, rising to 0.470 in the most recent release. Downstream, vocabulary mismatch alone
moves a coverage claim from 97.0% to 17.4% and changes the named threat actor in 0.722 of
pre-restructuring observations and 0.022 across a single modern boundary, concentrated two to
seven times more heavily on exactly the groups that are attributable at all. Identifier
normalization repairs about half the legacy penalty, almost none of the modern one, and no
part of the semantic one — and applying it silently changes published verdicts in up to 0.442
of cases, so it is itself a reportable intervention.

The part of the problem that identifier arithmetic can repair, MITRE has already solved and
consumers do not use. The part it cannot repair is the part nobody currently detects. Closing
the gap does not need a better crosswalk; it needs CTI artefacts to declare their calibration —
domain, release, bundle hash, and the residual ledger of what any migration kept, merged,
demoted and dropped — and it needs ATT&CK to adopt the two mechanisms ontology engineering
settled decades ago: an inexact-successor relation, and a typed evolution mapping published as
an artefact in its own right.
