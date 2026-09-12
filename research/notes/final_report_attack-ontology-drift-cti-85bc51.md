# Ontology Drift as a Threat to Validity in CTI Analytics: Measuring MITRE ATT&CK, Its Downstream Cost, and the Reporting Discipline That Follows

## Abstract

Security machine learning spent a decade learning to control for bias in its data: temporal splits, realistic base rates, drift detection, conformal rejection. All of that discipline assumes something it never states, that the label space is fixed. In cyber threat intelligence it is not. MITRE ATT&CK is the instrument in which coverage, attribution and benchmark labels are denominated, and it has been re-issued 109 times across three domains since January 2018 without any downstream result recording which issue it used. We build a longitudinal database of 106 domain-release pairs and measure four drift processes separately, then run controlled experiments in which the adversary intelligence is held fixed and only the vocabulary moves. We report both halves. MITRE's Enterprise identifier accounting is complete — every revoked technique carries exactly one successor edge and none dangle — and post-2020 identifier survival to the newest release never falls below 0.970. Yet 0.749 of the identifier-stable techniques of v7.0 have edited descriptions by v19.0, ATT&CK's own version field detects a rewrite at precision 0.447 and recall 0.641, 0.323 of new group-technique edges for pre-existing groups are bookkeeping rather than intelligence, and a frozen capability that claimed 97.0% coverage reads 17.4% at v19.0. Vocabulary mismatch alone changes the named threat actor in 0.722 of pre-restructuring observations and still in 0.022 across one modern release boundary. Identifier normalization recovers 0.42 to 0.53 of the legacy penalty, almost nothing modern, and nothing semantic. The contribution is therefore not a crosswalk but a reporting contract.

## 1. Introduction

A coverage percentage, an attribution verdict and a benchmark score are all measurements, and every measurement is stated in units. In cyber threat intelligence the unit is the ATT&CK technique identifier, and the number is meaningful only relative to the edition of the catalogue that supplies both the numerator's vocabulary and the denominator's cardinality [63, 74]. Consider a TTP-based attribution system published in 2019 and a successor published in 2023 reporting a higher number on the same corpus under the same metric. Between those dates the label space lost roughly half of its identifiers in a single release, gained a level of abstraction that did not previously exist, and rewrote three-quarters of the descriptions of the terms that survived. Neither paper declares its ATT&CK release; no venue asks. That is not a weak comparison, it is a comparison between two instruments whose readings are reported in the same units by convention alone.

The failure has a shape security machine learning already knows how to name. TESSERACT gave the field a vocabulary for temporal and spatial bias [67], Arp et al. catalogued ten recurring methodological errors [35], and drift detection and conformal rejection carried the concern into deployment [22, 70]. Every one of those instruments operates on a fixed label space: dataset-shift taxonomy is defined over the joint distribution with the class set held constant [33], and where the class set does move, class-incremental learning handles only the additive quadrant [24] and evolving-class-ontology work only relabelling [43]. ATT&CK performs addition, deprecation, revocation, re-cutting, cross-layer promotion and silent redefinition. Concept drift moves the data under a fixed ruler; ontology drift moves the ruler.

We make the argument by measurement, and we make the concessions the measurement forces. The first is the apparatus: pinning a release is MITRE's documented first-class workflow, tombstones are guaranteed, revocation edges are typed, and a change-computation tool ships in MITRE's Python library with an explicit class for objects patched without a version increment [1, 7, 34, 48]. Anyone holding that documentation can refute a naive version of this paper in a paragraph. The second is the noise floor: detection products pinned to one release disagree about the label for the same behaviour [74], and roughly a third of ATT&CK groups have any technique unique to them [59]. We do not claim drift dominates that noise; we claim it is separable by construction and we test additivity rather than assuming it (Section 7.3). The third is the remedy: identifier normalization is worth tens of points on pre-2020 artefacts and under one point on modern ones, with a confidence interval spanning zero in most modern conditions (Section 8).

The contributions are four. A longitudinal measurement of drift over every public release of all three domains, decomposed into processes that behave differently in time (Section 6). Controlled experiments on attribution, coverage, mitigation ranking and benchmark label validity in which only the vocabulary moves (Sections 7 and 9). A decomposition of apparent knowledge growth into intelligence and bookkeeping (Section 6.4). And a normalization protocol whose measured limits are themselves the result, with the reporting discipline that follows from those limits (Sections 8 and 10). The most current instance of the problem is four months old: ATT&CK v19 retired Defense Evasion as a tactic, renamed TA0005 in place to Stealth, minted TA0112 Defense Impairment, and revoked the twelve-child T1562 family into the new arrangement [78].

## 2. Background: ATT&CK as a Versioned Ontology

ATT&CK organises adversary behaviour into tactics, techniques and sub-techniques and links them to intrusion sets, software, mitigations and data components. Its design documentation states that inclusion criteria are non-stationary and that the abstraction level of a technique is an editorial choice rather than a natural kind [14]. The project is described, by practitioners defending its structure, as an ontology rather than a taxonomy [77], which places it inside a literature with mature machinery for exactly this problem: ontology evolution versus versioning, with change management as the core task of both [56].

That literature supplies the yardstick. OBO Foundry requires version IRIs, release immutability and perpetual resolvability [55]; its identifier policy mandates global uniqueness and forbids reuse [53]; its term-stability principle requires that the referent of an identifier not change, separates exact successors from inexact ones, and requires obsoletion to be visible in the human-readable label [54]. OWL has supplied `versionIRI`, `priorVersion`, `backwardCompatibleWith` and `owl:deprecated` for two decades [57], and COnto-Diff types complex change operations — merge, split, move, substitute — as a first-class evolution mapping rather than an untyped diff [26]. Biomedicine has already demonstrated the downstream consequence: Gene Ontology evolution changes the interpretation of enrichment analyses computed over it, so a conclusion moves with no new experiment [69]. Security vocabularies have their own instances, in CVE lifecycle states [31], in CVE-to-CWE-to-CPE abstraction-ladder instability [32], in CVSS fragmentation across versions [39], and in knowledge-graph work that tracks vocabulary churn and instance usage as two separate time series [37].

Measured against that yardstick ATT&CK scores well on some axes and has nothing on others. Releases are immutable and addressable, satisfying the substance of the versioning principle [1, 55]. Retirement is typed and non-destructive: an object with a successor is revoked and carries a `revoked-by` edge, an object without one is deprecated, and both are retained so dependent workflows do not break [1]. The Center for Threat-Informed Defense funds ATT&CK Sync to flag mappings affected by a release [5], an institutional concession that staying in sync is an operational burden, and the Navigator layer format carries a `versions` object able to record the content version of a coverage layer [15]. What ATT&CK lacks is the inexact-successor relation, the controlled obsolescence-reason vocabulary, label-level visibility of obsoletion, prior-version and compatibility links, and a typed evolution mapping published as an artefact in its own right. Sections 6 and 8 price each absence. One further structural fact shapes everything downstream: the March 2020 introduction of sub-techniques was not an addition but a re-cut, it is the single most-cited instability in the ATT&CK literature [47, 63], and Section 6.5 shows it is one draw from a live hazard rather than a closed wound.

## 3. Related Work

Four literatures bear on this problem and none of them measures it.

**CTI quality.** A mature line of work defines quality dimensions for threat intelligence and builds instruments to score feeds against them: accuracy, completeness, timeliness, relevance, provenance and interoperability recur across the canonical treatments [60, 76], with dynamic automated assessment and weighted criteria added later [27], empirical feed evaluations establishing that public feeds overlap little and age badly [41, 45], practitioner quality assurance studied directly [40], community feeds metered [38], and a 2025 measurement-based survey consolidating the field [11]. Structural validity of the exchange formats is a separate recurring complaint [83], as is data quality in the vulnerability databases generally [25]. None of these frameworks names the reference vocabulary's edition as a quality dimension. This is an audited absence and we state its bound: across the sources reachable in this environment we found no such dimension defined, and we did not have full text for all of them, so we claim the absence of a named dimension rather than the absence of any awareness.

**ATT&CK-based analytics.** The systematization of ATT&CK in research and practice already establishes that coverage claims are not comparable across products and flags temporal instability as an open problem [63]; a 2025 survey sets the bar a contribution must clear [47]. Virkud et al. demonstrate non-comparability empirically at a single pinned release: rules from different vendors describing the same behaviour carry disjoint technique labels, and recomputing coverage from raw artefacts collapses the differences between products [74]. Shen et al. re-analyse MITRE's own Evaluations as whole attack graphs and argue per-technique tallies are the wrong unit [62]; the Evaluations programme itself refuses to emit a coverage score [46]; practitioners make the same argument in blunter terms, that a heatmap counts rules rather than coverage, that a 100% claim is a red flag, and that several incompatible denominators are in circulation [80, 82, 84], with the ad hoc construction of coverage layers documented from the practitioner side [81]. Summiting the Pyramid replaces techniques with implementations as the coverage denominator outright [64], and mitigation coverage has a ceiling set by the control catalogue rather than by the product [58]. All of this establishes disagreement at one version. None of it measures what a version change costs.

**Extraction, benchmarks and attribution.** The extraction line runs from TTPDrill [71] through rcATT [44] to TTPHunter and its successor [72], with graph-based systems alongside [2] and recent multi-label treatments that decline to treat existing annotations as gold [52, 73]. LLM-era benchmarks are now the dominant evaluation surface: CTIBench treats authoritative sources as fixed and time-controls one task but not the ATT&CK task [30]; a successor line grew from 691 to 1,860 QA pairs under one identifier and the same nine-task taxonomy [29]; AthenaBench argues static benchmarks go stale and proposes live-API construction [13]; large instruction corpora span two decades of reports with no declared release [61]; synthesis work targets the long tail [65]; and telemetry-grounded evaluation is the only structurally drift-resistant design in the set [28]. Answer-key decay in static benchmarks has been quantified outside security [75], and sequence-level reasoning benchmarks add tactic ordering as a further drift surface [17]. Attribution has moved to TTP sequences [23] and is surveyed by artefact type rather than by ontology version [12], while two results bound what it can do at all: most ATT&CK groups have no group-specific behaviour [59], and LLM agents reproduce documented APT profiles at 55-80% precision [66]. Extractor errors concentrate among same-tactic, description-overlapping techniques [20], and vendor fragmentation compounds all of it [68]. The common feature of this literature, as the repository audits of Section 9 show, is that the gold label space is a file whose provenance is undeclared [3, 6].

**Concept drift in security ML.** Dataset-shift taxonomies are formulated over a fixed label space [33]; TESSERACT establishes temporal hygiene [67]; CADE detects and explains drifting samples [22]; conformal evaluation rejects under drift [70]; adaptation work assumes a fixed vocabulary while the distribution moves [50]; and the catalogue of security-ML pitfalls contains no entry for a label space that changes between training and evaluation [35]. Where the label space does change, the machinery is class-incremental learning [24] and continual learning with evolving class ontologies [43], the closest security instance is MOTIF's open and unstable family set [51], and AVClass is the prior art for alias resolution as a published normalization artefact [19]. IncreTTP is, as far as we found, the only work framing ATT&CK version updates as concept drift, and its remedy is incremental learning rather than measurement [42]. The boundary is the contribution point: concept drift is change in the conditional distribution with the label set fixed, ontology drift is change in the set itself and in what its members mean [21].

## 4. Problem Formalization and Drift Taxonomy

Let a release `V` of an ATT&CK domain determine a label space `L_V`, the set of live technique identifiers, together with an intension map `ι_V` sending each identifier to what defines it: description, detection guidance, tactic assignment and platform set. A CTI analytic maps evidence to a subset of `L_V`; a CTI artefact is a pair `(A, V)` with `A ⊆ L_V`. In deployed practice `V` is almost never recorded (Table 12), so what circulates is `A` alone. Two artefacts are comparable when they are expressed in the same label space under the same intension map. That is not a strong requirement. It is the ordinary requirement that measurements reported in the same units be reported in the same units.

We type drift by the operators that transform `(L_V, ι_V)` into `(L_W, ι_W)` for `W > V`.

**O1 Addition.** A new identifier with no predecessor. This is the only operator the class-incremental literature handles [24] and the only one benign for backward comparison. It is not benign forward: a growing coverage denominator makes a frozen capability's percentage fall with no change in the capability, which is the mechanism behind Table 8.

**O2 Deprecation.** An identifier withdrawn with no successor. ATT&CK marks these and retains the object [1]. A pipeline that filters retired objects drops the label; one that does not carries a dead term.

**O3 Revocation with a typed successor.** The well-handled case, and the one the ecosystem's defence rests on. Every revoked Enterprise identifier in our corpus resolves to a live identifier through the published graph (Table 3). The relation is a total function into the live label space.

**O4 Re-cut.** A concept split across successors, or several merged into one. Because `revoked-by` is a function and never one-to-many, a split is representable only as a set of many-to-one merges onto the narrowest survivor. It is simply not true that the relation cannot express the v19 re-cut; it can, as merges. The defect is not expressiveness but annotation: the merge is unlabelled, so a consumer applying the crosswalk mechanically cannot distinguish an exact successor from a narrowing. Ontology engineering settled this by splitting the successor relation into exact and inexact variants [54] and by typing complex change operations as evolution mappings [26]. ATT&CK has one untyped relation where the literature specifies at least two.

**O5 Cross-layer reassignment.** A concept moves between levels: a technique demoted to a sub-technique, a sub-technique promoted, or a technique promoted to a tactic. The crosswalk carries no abstraction-level annotation, so a consumer cannot detect that the granularity of its assertion changed, and the promotion of a technique to a tactic is not representable at all because `revoked-by` cannot point a technique at a tactic. Tactic reassignment at the instance level is also unsignalled: tactic objects carry no revocation edges anywhere in the corpus.

**O6 Intensional rewriting.** The identifier survives and what it denotes moves. This operator is invisible to every identifier-based mechanism in the ecosystem — the crosswalk, the retired-object filter and the layer version stamp alike.

O1 to O5 are *referential*; O6 is *intensional*. Cutting across that is a distinction we consider more practically important. Call an operator *signalled* if the published artefact carries a machine-readable marker a consumer can test. O2 and O3 are signalled. O4 and O5 are partially signalled: the edges exist but carry no type, so the consumer learns that something changed and not what. O6 is unsignalled, because the only candidate marker, the object version field, operates at precision 0.447 and recall 0.641 (Section 6.3). This is the sharpest statement of the thesis: the component of drift that is well handled is the component everybody points at, and the component that is not handled at all is the component nobody can see.

Two artefacts are **version-comparable** when both have been projected onto one reference release and the projection's residual is declared. Projection is transitive closure over the retirement relation. It is a function and not an injection: it can merge, and it can land on a different abstraction level. The residual is the four-way ledger of kept, merged, demoted and dropped. A protocol returning only the projected set has destroyed exactly the information a reader needs to judge comparability, and Section 8 shows that this is not hypothetical.

Placed in the experimental-methodology tradition, ontology drift damages validity in four distinguishable ways. *Construct validity*: after O6 the same label denotes a different behaviour, so the construct measured is not the construct the labels name. *Internal validity*: after O4 or O5 a profile's cardinality and granularity change under migration, so measured breadth falls with no change in the intelligence. *External validity*: after O1 the denominator of any coverage claim grows, and a capability unchanged in the world reports a falling number. *Conclusion validity*: if the effect were confined to scores the response would be an error bar; Section 7 shows it reaches the named actor, the top-ranked mitigation and the pass/fail verdict. The control is not a better algorithm. It is declaration plus projection.

Because a study of drift is unusually exposed to its own subject, we commit in advance to four requirements and audit them in Section 11. **R1**, the contrast must hold everything constant except the vocabulary. **R2**, a stated noise model, since holding a nuisance term at zero establishes separability and says nothing about additivity. **R3**, a declared closure boundary, since if observation, profile, ground truth and migration map all come from one curator the absolute levels are internal-consistency scores. **R4**, a named falsifier.

## 5. Data and Methodology

We clone MITRE's `attack-stix-data` repository, which publishes every release as an immutable STIX 2.1 bundle at a stable path [1]. Its index enumerates 109 versioned bundle entries, 41 Enterprise, 41 Mobile and 27 ICS; our extraction materialises 106 domain-release pairs, 41 Enterprise, 38 Mobile and 27 ICS. The three-entry difference falls entirely at Mobile v11.0 to v11.2, entries the published Mobile sequence skips as it steps from v10.1 to v11.3, and which are excluded as pre-release placeholders. We report both counts rather than quietly adopting the convenient one, because undeclared denominators are how measurements go wrong. Each bundle is parsed into a relational store recording, per domain and release, every object's identifiers, flags, `x_mitre_version`, timestamps, kill-chain phases, platforms and the full text plus SHA-256 digests of description and detection fields, together with every typed relationship.

Release-level analyses use **major releases only**: one release per major version, the `.0` release or the earliest available release of that version, giving 19 Enterprise, 19 Mobile and 12 ICS analysis points. Patch releases are irregular in cadence and scope, and mixing them in would make a per-release transition mean different things in different eras. The deployed-corpus analysis of Section 9 deliberately does the opposite and uses every published release, because there the question is which release a label file could have been written against, and excluding patch releases would bias that answer.

**Table 1.** The release corpus. Major releases are the analysis points for churn, survival and drift; all releases are used for the label-validity analysis of Section 9.

| Domain | Releases analysed (major / all) | First | Last |
|---|---|---|---|
| Enterprise | 19 / 41 | v1.0 (2018-01-17) | v19.0 (2026-04-28) |
| Mobile | 19 / 38 | v1.0 (2018-01-17) | v19.0 (2026-04-28) |
| Ics | 12 / 27 | v8.0 (2020-10-27) | v19.0 (2026-04-28) |

The live set is the `attack-pattern` objects with both retirement flags false, and it is the denominator of every coverage claim. Identifier Jaccard is computed over consecutive majors, with a revoked identifier treated as absent because a revoked identifier is unusable as a label even though the object is retained. An identifier is *recoverable* at a target if transitive `revoked-by` closure from it, cycle-safe and bounded at ten hops, terminates in the live set. Semantic drift is measured on identifier-stable techniques only: description edited is inequality of digests, similarity is the Jaccard index over lowercased alphanumeric token sets, and a *substantial rewrite* is token similarity below 0.8. The cut is a convention and we report the mean-similarity series alongside it. Set Jaccard over bags of words is deliberately crude: it is monotone in shared vocabulary, requires no model, and cannot import an embedding's own drift into a measurement of drift. Growth decomposition assigns each newly added group-technique edge to exactly one cause, tested in a fixed order — new actor, revocation re-mapping, sub-technique refinement, new technique, genuine new intelligence — with re-mapping tested before refinement so that an ambiguous edge is charged to bookkeeping.

Four downstream experiments share one principle: the adversary intelligence is held fixed and only the vocabulary varies, which satisfies R1 and makes every contrast attributable to the instrument. **Attribution.** The analysis release is v19.0 throughout. Modern group profiles are back-projected into a legacy vocabulary by a map built once per pair: a modern technique maps to itself if live at the legacy release, else to the pre-revocation identifier resolving onto it, else to the nearest live ancestor within five hops, else it is dropped as a behaviour with no expression in that era. Each of 500 trials samples a group, draws k = 10 techniques from its modern profile, and scores four conditions over identical draws: *back-projected* (labelled *contemporaneous* in the released results files), *naive*, *ATT&CK-Norm* and *oracle*. Scoring is IDF-weighted cosine; the drift penalty is back-projected minus naive top-1 accuracy; recovery is the share of that penalty returned by normalization; intervals are paired bootstrap with 2,000 resamples. Robustness sweeps three scorers and two profile definitions (Table 7). **Coverage.** A capability is frozen at a release as the techniques reachable by `mitigates` edges there and re-measured at v19.0 naively and after normalization, with a 500-sample random-portfolio sweep and a prevalence-weighted variant. **Conclusion instability.** The same machinery is read out at verdict level and as Kendall tau over mitigation rankings. **Label validity.** Four deployed corpora are parsed from their own label files rather than from their papers, and every identifier is checked for liveness at every published release; the *provenance interval* is the set of releases at which every identifier is simultaneously live, and an empty interval means the artefact mixes mutually exclusive vocabularies.

Every number in Sections 6 to 9 is produced by scripts in `code/` from public bundles and public label files and runs end to end from one shell script; tables are generated from the result files rather than transcribed. Three evidence tiers are marked throughout. Tier A is our own measurement and artefacts read in full from local clones. Tier B is secondary literature reachable in this environment only through search summaries, attributed as reported and never quoted. Tier C is an audited absence, stated with the bound of the search that found it.

## 6. Measuring Ontology Drift in ATT&CK

### 6.1 Two clocks, not one

**Figure 1.** Live technique count across Enterprise releases, with per-release additions, revocations and description rewrites on a shared time axis.

**Table 2.** Per-release Enterprise churn across consecutive major releases. Rewrite and tactic columns count only techniques live in both releases; `J(ID)` is the identifier Jaccard; edges are group-to-technique `uses` edges.

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

Read the identifier column alone and the episodic reading is irresistible: one transition, v6.0 to v7.0, has an identifier Jaccard of 0.222, adds 302 techniques, revokes 129, deprecates 11 and rewrites the group-technique graph by removing 750 edges and adding 1,235. The next largest drop in eight years is 0.944, at the most recent transition. Read any other column and the episodic reading collapses. Description rewrites among surviving techniques never fall below 27 and reach 151 at v10.0 to v11.0, a transition whose identifier Jaccard is 0.976. Detection rewrites are burstier and larger: 583 of 691 surviving techniques had their detection guidance rewritten between v17.0 and v18.0, a transition any identifier-keyed diff would report as one of the quietest in ATT&CK's history. The tactic column, empty or near-empty for sixteen transitions, reads 198 at the most recent one. This is the two-clock structure, and stating it precisely is the first result: a slow episodic referential clock and a fast continuous intensional clock, so that any risk statement reporting one without the other is wrong by a factor that depends on which column the reader happened to look at.

### 6.2 Survival: the concession, measured

**Figure 2.** Identifier survival curves by source release to v19.0, with the recoverable fraction under transitive `revoked-by` closure overlaid.

**Table 3.** Identifier survival to v19.0 by source release. Recoverable counts revoked or absent identifiers whose transitive closure terminates at a live identifier.

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

The recoverable column equals the revoked column in every Enterprise row and the absent count is zero in every row. Recomputing from the v19.2 bundle gives 858 `attack-pattern` objects — 697 live, 149 revoked, 12 deprecated — and 149 `revoked-by` edges from 149 distinct sources. Every revoked Enterprise technique has exactly one successor and none dangle. We concede this without qualification, because conceding it is what makes the remaining argument non-trivial [1].

The concession has a precise scope and each boundary of that scope is a finding. It is Enterprise-only: in Mobile, 34 survival rows record identifiers absent rather than tombstoned, and all 76 ATT&CK identifiers of Mobile v1.0 are simply gone from v3.0 onward with no successor edge of any kind. The relation is never one-to-many, so a split is representable only as a set of merges onto whichever survivor the curator judges narrowest; eight Enterprise targets absorb 20 predecessor identifiers, the largest absorbing five. And retirement routinely crosses abstraction levels: of the 149 edges, 119 map a top-level technique onto a sub-technique, 13 top onto top, 10 sub onto sub, and 7 promote a sub-technique to a parent. A crosswalk that resolves in one hop, reports complete success and silently narrows the extension of the original assertion is not a broken crosswalk. It is a 1:1 relation doing what a 1:1 relation can do in a situation that needs more, which is why the remedy in Section 10 is borrowed from a framework that already separates exact from inexact successors [54].

The tactic layer is worse, because it has no retirement relation at all: across all three domains and every release our extraction finds 5,599 revocation edges and zero of them involve a tactic object. Between v18.1 and v19.2 the object carrying TA0005 keeps its UUID and identifier while its name changes from Defense Evasion to Stealth, its shortname from `defense-evasion` to `stealth`, and its `x_mitre_version` stays at 1.0; TA0112 Defense Impairment is minted alongside it, and T1562 is retired into the new arrangement [78]. Any analytic joining on TA0005 across that boundary compares two different concepts with no revocation, no version increment and nothing to follow. This is the edit that OBO Foundry's stability principle exists to forbid: a changed referent requires a new identifier [54].

### 6.3 Intensional drift, and why ATT&CK cannot signal it

**Figure 3.** Silent semantic drift among identifier-stable techniques: share with edited descriptions and share substantially rewritten, by source release, measured at v19.0.

**Table 4.** Semantic drift among techniques live at both the source release and v19.0. Token Jaccard is over lowercased alphanumeric token sets of the description; a substantial rewrite is below 0.8.

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

Table 4 must be read as a function of elapsed time, not of release quality: the v18.0 row is low because one transition separates it from the analysis release. The right reading is cohort decay. Of the 415 techniques live at v7.0 and still live at v19.0, 0.749 have edited descriptions and 0.386 are rewritten past the substantial threshold, at mean similarity 0.808; for the v11.0 cohort, 0.465, 0.208 and 0.895; for v15.0, 0.275, 0.087 and 0.956. These are identifiers whose survival over the same interval is 0.977 and 0.975. The instrument keeps the scale markings and moves what they mean. Converted to a practitioner's clock, for every Enterprise cohort from v7.0 onward the time to 10% hard identifier staleness is never, while the time to 10% substantive staleness — gone, substantially rewritten, or reassigned to a different tactic — is 0.50 to 2.01 years with a median of 1.51, and 0.99 to 2.01 years with a median of 1.52 when tactic changes and revocations are excluded so that the recent re-cut cannot be blamed. Semantic half-life is 4.5 to 6.1 years. A pinned post-2020 label set has an infinite identifier half-life and an eighteen-month first-10% semantic staleness schedule, simultaneously.

Could a consumer detect this from the bundles? ATT&CK carries `x_mitre_version` on every object, and the natural assumption is that a change in meaning is announced there. It is not.

**Table 13.** Text change versus version increment for techniques live in both releases of a consecutive major pair, Enterprise.

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

Over 8,359 carried-over pairs, 1,358 (0.162) had their description rewritten; 487 of those (0.359) carried no version increment, and 1,077 version increments carried no text change at all. As a detector of description change, `x_mitre_version` has precision 0.447 and recall 0.641: a consumer who re-reads every technique whose version increased does nearly half the work for nothing and still misses over a third of the changes. MITRE's own tooling knows this — `diffStix` defines a distinct change class for objects patched while the version stayed the same, and annotates unintended version changes as a historical defect it defends against [34, 48] — while the published consumer contract offers a binary current-or-retired filter and no expression for a surviving object whose meaning moved [1]. The gap is architectural, not an oversight. This is the paper's central negative result and the answer to the strongest practical objection in the field: the advice to pin a release is correct and insufficient. Pinning fixes identity, not intension, and no signal in the published data reliably tells a consumer when intension has moved.

### 6.4 How much of ATT&CK's growth is intelligence?

**Figure 4.** Per-transition decomposition of new group-technique edges for pre-existing groups into genuine new intelligence, new technique, sub-technique refinement and revocation re-mapping.

**Table 5.** Knowledge-growth decomposition, Enterprise. Edges for groups newly added to ATT&CK are excluded from the denominator; bookkeeping share is refinement plus re-mapping over all new edges for pre-existing groups.

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

Across all Enterprise transitions 5,516 group-technique edges are added, of which 2,442 belong to groups newly added to ATT&CK. Of the remaining 3,074, 1,752 are genuine new intelligence about a pre-existing pairing, 330 credit a group with a newly minted technique, 487 are sub-technique refinements of an edge the group already had, and 505 restate an edge whose technique was revoked and replaced. The bookkeeping share is 992/3074 = 0.323. The headline conceals a heavy tail, and the tail is the point: the restructuring transition is 0.750 bookkeeping over 1,059 edges, eight transitions are below 0.05, but v12.0 to v13.0 is 0.380 over 71 edges, v14.0 to v15.0 is 0.340 over 100, and the most recent transition is 0.470 over 164 edges, the highest share since the restructuring and driven entirely by 77 revocation re-mappings. A reader who plots ATT&CK's edge count as a curve of accumulating adversary knowledge is reading a curve that is roughly a third bookkeeping overall and nearly half bookkeeping in the release that shipped four months before this analysis. Evidence from the benchmark side points the same way: the 4.3x label-space growth between one LLM CTI benchmark generation and its successor is roughly 96% pre-existing catalogue, with only six genuinely new entries [6].

### 6.5 Recurrence: a hazard, not a wound

The episodic reading of Table 2 has one defence left, that the 2020 restructuring was singular and is finished. Extending the measurement to all three domains refutes it. Five major transitions in the corpus have identifier Jaccard below 0.80: Mobile v2.0 to v3.0 (J = 0.000), Enterprise v6.0 to v7.0 (0.222), ICS v8.0 to v9.0 (0.778), Mobile v10.0 to v11.3 (0.268) and ICS v18.0 to v19.0 (0.698). That is 5 events in 47 transitions, a hazard of 0.106 per major transition, one event per 4.41 domain-years over 22.05 observed domain-years — roughly one restructuring somewhere in ATT&CK every 1.5 calendar years. Two matter more than their Jaccard suggests. Mobile's 2018 event is the most destructive in the corpus and predates the Enterprise restructuring: all 128 STIX identifiers are preserved while all 76 ATT&CK identifiers vanish, with zero of the 76 recoverable, making it invisible to STIX-keyed tooling and uncrosswalkable by any mechanism MITRE publishes. And the ICS event is happening now, introducing sub-techniques for the first time — 0 at v18.1, 18 at v19.0 — six years after Enterprise made the same move, with all nine remaps recoverable. So the two-clock model is not a story about one bad year: the referential clock is episodic and recurrent across domains, and the intensional clock never stopped.

Can a consumer see one coming? Testing leading indicators over 17 lagged Enterprise pairs by Spearman correlation with 20,000-shuffle permutation tests, the largest coefficient is detection-field edits at ρ = +0.377, p = 0.134, and nothing else comes close; the largest anywhere in the three-domain panel, ICS renames at ρ = +0.733, has p = 0.054 on n = 10. Technique-level hazard modelling is worse than null: the 131 techniques doomed at v7.0 had been edited *less* than the survivors in the preceding release, on description edits (0.168 against 0.336) and on version bumps (0.176 against 0.372). Restructuring waves are not forecastable from the public bundles, which removes the option of a triggered response and means any protocol that helps must be standing rather than event-driven. The most recent wave shows what standing exposure looks like: 17 live techniques revoked between v18.1 and v19.2, a blast radius on the v18.1 graph of 84 group-technique edges, 155 software-technique edges, 47 mitigations and 17 detection relationships, 52 of 168 group profiles losing at least one identifier, and T1562.001 ranked 33 of 599 techniques by `uses` edges in the release it left.
