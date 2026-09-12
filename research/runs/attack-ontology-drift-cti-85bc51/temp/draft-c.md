# Ontology Drift in MITRE ATT&CK: Measurement, Downstream Validity, and a Reporting Discipline for Cyber Threat Intelligence Research

## Abstract

Cyber threat intelligence analytics are built on a vocabulary that moves. MITRE ATT&CK adds, revokes, deprecates, re-cuts, re-parents and silently rewrites the techniques that CTI benchmarks, attribution systems and coverage claims use as their label space, yet the field cites ATT&CK as though it were a constant. We measure that movement across 19 Enterprise, 19 Mobile and 12 ICS major releases and trace it into three downstream analytics. Identifier churn is episodic: the v6.0 to v7.0 transition has an identifier Jaccard of 0.222, and every post-2020 Enterprise cohort retains above 0.97 of its identifiers to v19.0. Semantic churn is continuous: 0.465 of v11.0's identifier-stable techniques have edited descriptions by v19.0, and ATT&CK's own object-version field detects a description rewrite with precision 0.447 and recall 0.641. Of 3074 new group-technique edges attaching to pre-existing groups, 0.323 are bookkeeping rather than intelligence. In a controlled attribution experiment the vocabulary of the artefact alone moves top-1 accuracy by 42.2 points for a 2018 artefact and 1.6 points across a single modern release boundary, and changes the named actor in 0.722 and 0.022 of observations respectively. We then take our own remedy apart. ATT&CK-Norm, the version-normalization protocol we specify and evaluate, recovers roughly half the legacy penalty and lifts mitigation-ranking Kendall tau from 0.931 to 0.992, but its roll-up branch fires three times in 12,027 resolutions, 119 of 149 Enterprise revocation edges demote a top-level technique onto a sub-technique, five identifiers collapse into T1685 unannounced, it cannot represent the v19 promotion of a technique to a tactic, and it is silent on the 198 of 674 techniques that changed tactic under a stable identifier in that same release. Across four deployed CTI corpora we find label sets that match no single ATT&CK release and zero version declarations in 19 documentation files. The contribution is therefore not the crosswalk. It is a four-line reporting contract a reviewer can check, and named ports from ontology engineering that MITRE could adopt without inventing anything.

## 1. Introduction

There is a sentence that appears, in some form, in a large fraction of the CTI literature: *we label techniques using the MITRE ATT&CK framework*. It is offered as a methods statement. It is not one. It names neither a domain, nor a release, nor a granularity policy, nor what was done with the labels that the release no longer recognises. Written in 2019 and read in 2026 it denotes a vocabulary in which roughly half of the identifiers it could have used are now revoked or deprecated, in which the tactic its labels were grouped under has been renamed in place to mean something else, and in which three quarters of the surviving techniques carry descriptions that have since been edited. The sentence is a citation where a version pin should be.

This paper is about what that costs and what to do about it on Monday morning. The remedy, as the measurements below force, is not primarily technical. Ontology engineering solved the hard parts of vocabulary evolution decades ago and wrote the solutions down: referent stability at a stable identifier, a distinction between exact and inexact successors, version identifiers with perpetual resolvability, declared backward compatibility, and typed evolution mappings between releases [53, 55, 56, 57, 26]. Biology then demonstrated that ignoring them changes published conclusions and not merely scores [69]. Security's flagship ontology adopted almost none of that machinery, and — this is what makes it a research-validity problem rather than a vendor complaint — security's consumers adopted none of the discipline either, including the discipline ATT&CK does support.

The argument has to begin with a concession, because the opposing case is strong. MITRE publishes immutable, individually addressable per-release STIX bundles; it types retirement, distinguishing revocation with a successor from deprecation without one; it retains both classes of object so dependent workflows do not break; it ships diffStix, which computes a nine-class change set including a `patches` class for objects edited without a version increment; it gives Navigator layers a version field; and CTID funds ATT&CK Sync to flag mappings affected by a release [1, 7, 34, 15, 5]. Our own audit confirms the strongest part of that claim: in the v19.2 Enterprise bundle there are 149 `revoked-by` edges from 149 distinct sources, no revoked technique has more than one successor, and no Enterprise identifier has ever silently vanished. A paper asserting that ATT&CK churns and nobody handles it would be refuted by MITRE's own usage document in one paragraph.

What the apparatus does not do is the subject of Sections 6 through 10. It has no crosswalk for tactics at all, and v19 renamed TA0005 from *Defense Evasion* to *Stealth* in place, keeping the STIX identifier and the object version, while minting TA0112 *Defense Impairment* for the separated concept [78]. It cannot represent a split, so a 1:N re-cut is encoded as merges onto the narrowest survivor, asserting that a parent concept equals one of its own former children. It emits no reliable signal for a description rewrite. And its consumer-facing contract offers a binary filter — current or retired — with no vocabulary for a surviving object whose meaning moved.

Against that, adoption. Across 19 documentation files in three deployed CTI corpora we found zero ATT&CK version declarations (Table 12), and an audit of published Navigator coverage layers is worse: of 57 vendor threat-report layers, zero declare an ATT&CK content version, and 739 of their 2,143 technique annotations — 34.5% — name an identifier that is revoked or deprecated at v19.2 [79]. Opened today in a current Navigator, every one of those layers silently re-bases onto the present release [15, 16, 18].

Our contributions are four. First, a longitudinal measurement separating two clocks — an episodic identifier clock with a per-transition hazard of 0.106, and a continuous semantic clock that rewrites 10% of any pinned Enterprise label set within roughly eighteen months (Section 6). Second, a decomposition of apparent knowledge growth showing that 0.323 of new intelligence edges for pre-existing groups are bookkeeping (Section 6.4). Third, three downstream experiments in which drift changes conclusions and not merely scores (Section 7). Fourth — the section we ask reviewers to read hardest — a version-normalization protocol, ATT&CK-Norm, which we specify, evaluate, and then argue against as the paper's centrepiece (Section 8), because what it provably cannot deliver is meaning. The constructive claim we defend is a reporting contract of four checkable lines and named ports from established ontology practice (Section 10).

## 2. Background: ATT&CK as a Versioned Ontology

ATT&CK's design document is explicit that its inclusion criteria are non-stationary and that the abstraction level at which a behaviour is described is an editorial decision rather than a fact about the world [14]. That is an unusually honest thing for a reference vocabulary to say, and it has a consequence its consumers have not absorbed: a technique identifier denotes a curatorial decision at a point in time, not a fixed adversary behaviour. Practitioner commentary defends ATT&CK on exactly this ground — it is an ontology, not a taxonomy, and ontologies evolve [77]. We accept the defence and press it: ontologies evolve *under discipline*, and the discipline has a literature.

The published apparatus has four parts. Releases are immutable and individually addressable, so pinning is a first-class documented workflow rather than a community workaround [1]. Retirement is typed: objects no longer worth tracking are deprecated, objects replaced by another are revoked and carry a `revoked-by` relationship to the replacement, and both are retained so dependent workflows do not break [1]. Change between releases is computed and published by diffStix, whose class definitions include `patches` for objects changed while the version field stayed the same [34, 48]. And coverage artefacts have a place to record their vocabulary: the Navigator layer format defines a `versions` object [15], upgraded manually and one-way [16].

Three structural properties matter downstream. `revoked-by` is a function, never one-to-many: in the v19.2 Enterprise bundle zero revoked techniques have more than one target, and eight targets absorb 20 predecessors between them. The tactic layer has no revocation edges whatsoever — zero across all domains at v19.2 — so a tactic can only change by being edited in place. And `x_mitre_version` is an author-maintained field, not a computed hash, which is why diffStix needs a `patches` class at all [48].

Set against ontology-engineering practice, the gaps are omissions rather than mysteries. OBO Foundry's identifier policy requires global uniqueness, no reuse, and persistence as a provider obligation [53]; Principle 19 requires that a changed referent take a new identifier, distinguishes exact successors from inexact ones, and mandates that obsolescence be visible in the human-readable label [54]; Principle 4 requires version IRIs, release immutability and perpetual resolvability [55]. OWL supplies `versionIRI`, `priorVersion`, `backwardCompatibleWith` and `owl:deprecated` as first-class vocabulary [57]. COnto-Diff computes typed complex change operations — merge, split, move, substitute — as an explicit evolution mapping rather than an untyped diff [26], and the ontology-versioning literature has argued since the early 2000s that change management, not diffing, is the core task [56, 37]. ATT&CK has release immutability and a single untyped successor relation. It has none of the rest.

## 3. Related Work

**CTI data quality.** The quality literature is mature and converges on a stable set of dimensions — accuracy, completeness, timeliness, relevance, provenance, interoperability — across feed studies, weighted-criteria frameworks, practitioner interviews and measurement surveys [76, 60, 41, 40, 11]. Reading it for a dimension defined over the *reference vocabulary* returns nothing. This is an audited absence and we state its bound: across the quality-dimension sources reachable in this environment, no framework names ontology or vocabulary versioning as a quality dimension, and we make no claim about sources we could not reach. Practitioner accounts and migration tooling both describe version churn as a recurring operational cost [5, 27, 38, 45, 83]; Section 10 proposes the missing dimension.

**ATT&CK in research and practice.** The SoK literature has already established that ATT&CK-based results are not comparable across studies and has flagged temporal instability as a concern [63], and the recent state-of-the-art survey sets the bar an SCI-level contribution must clear in this space [47]. Neither quantifies what a release transition costs an analytic built on the earlier release. Virkud et al. establish, under a pinned release, that ATT&CK coverage is not comparable across detection products, recomputing coverage from the products' own rules [74]; Shen et al. show by whole-graph re-analysis that per-technique tallies from MITRE's Evaluations are the wrong unit [62]; MITRE's Evaluations methodology refuses to emit a coverage score [46], and analyst and vendor commentary treat a 100% coverage claim as a red flag [80, 82]. Practitioner accounts describe coverage layers built by ad hoc scoring over a data-source mapping that is itself versioned [81], and a widely-read critique observes that the heatmap counts rules rather than coverage, with three incompatible denominators now in circulation [84]. Summiting the Pyramid replaces techniques with implementations as the denominator entirely [64]; Rahman and Williams show the mitigation side has a ceiling set by the control catalogue [58]. Every one of these is a *synchronic* comparability result. None asks what the same claim means one release later.

**TTP extraction, benchmarks and attribution.** TTPDrill remains the pre-sub-technique baseline systems are still compared against [71]; rcATT trained on a 2019-era flat label space [44]; TTPHunter and TTPXHunter report 50 and then 193 TTP classes without declaring a release [72]; CAPTAIN performs TTP-sequence attribution with no declared version [23]. Our own artefact audits confirm the pattern at file level: six TTP systems, five different ATT&CK ontologies, two declared versions [3]; AttacKG freezes ATT&CK as a 2021 HTML scrape with parent-only templates [2]; rcATT's label space is half revoked by v13 [8]; and a repository declaring a deliberate remap to v12.0 still leaks pre-v7 revoked identifiers [10]. On the benchmark side, CTIBench treats ATT&CK as a fixed authoritative source [30], its successors expand under one identifier while keeping the same task taxonomy [29], AthenaBench answers staleness with live-API benchmarking [13], and SEvenLLM spans reports from 2004 onward with no ATT&CK release declared [61]. Multi-label ATT&CK classification work declares TRAM annotations non-gold [52]; TTPrint forks a cleaned TRAM [73]; SynthCTI synthesises the long tail [65]; AttackSeqBench reasons at sequence level and so inherits the tactic-reassignment surface directly [17]; CTI-REALM grounds evaluation in telemetry and is structurally the only drift-resistant design of the group [28]. The benchmark-ageing literature quantifies answer-key decay generically [75]; ours is the ATT&CK-specific instance, and we measured the growth claim on one successor pair: 4.3x label-space growth is approximately 96% pre-existing catalogue and six genuinely new items [6].

**Attribution and its identifiability floor.** APT attribution surveys taxonomise by artefact type rather than by ontology version [12, 66]. The sharpest objection to any drift result comes from this literature: roughly two-thirds of ATT&CK threat groups have no group-specific behaviour at all [59], and same-tactic, description-overlapping confusability accounts for a large share of extractor error within a single version [20]. Section 7.4 engages this with a stratified re-analysis rather than an argument.

**Concept drift.** Formal dataset-shift and concept-drift taxonomies are defined over a fixed label space: covariate shift, prior shift and conditional shift all presuppose that the set of classes is constant [33]. TESSERACT names temporal and spatial bias in security evaluation [67], CADE explains drifting samples [22], conformal evaluation rejects under drift [70], and modern malware-drift adaptation still operates over a fixed vocabulary [50]; the field's own methodological guidance stops short of the label space [35]. Continual learning reaches closest: class-incremental learning handles the additive quadrant [24], LECO addresses evolving class ontologies [43], and MOTIF documents the open, unstable class set for malware families [51]. IncreTTP is the nearest security-side neighbour, framing ATT&CK version updates as concept drift [42], and a boundary analysis makes the demarcation explicit [21]. The gap is precise: concept-drift theory can express a change in *P(y|x)*; it cannot express a change in the *set* of *y*, which is what a revocation, a re-cut or a tactic reassignment is. Other security vocabularies have met the same wall — CVE's REJECTED and DISPUTED states [31], CVE-CWE-CPE mapping instability along the abstraction ladder [32], CVSS fragmentation across versions [39, 25] — and AVClass alias resolution is the closest prior art for a migration map in security [19]. What none of them supplies is a measurement of what the vocabulary change costs a downstream analytic. That is the gap this paper occupies.

## 4. Problem Formalization and Drift Taxonomy

Let a CTI analytic be a function *f* from evidence to a set of labels drawn from a vocabulary *V*. Concept drift, as the machine-learning literature formalises it, is movement in the joint distribution over evidence and labels while *V* stays fixed [33]. Ontology drift is movement in *V* itself, and it is not reducible to the first: when a class ceases to exist, the conditional distribution over it is undefined rather than shifted. We therefore distinguish six operations on *V*, ordered by how much of the damage identifier arithmetic can repair.

**D1 — Addition.** A new identifier enters *V*. This is the well-behaved quadrant, the one continual learning already addresses [43]. It still breaks comparability in one direction: a system evaluated against a smaller *V* cannot be compared to one evaluated against a larger one without declaring both.

**D2 — Deprecation without successor.** An identifier is retired with no replacement. No arithmetic repairs this; any assertion that used it is now unexpressible. In ATT&CK these are top-level and rare: 11 in the v6.0→v7.0 transition, 0 in most modern ones (Table 2).

**D3 — Revocation with successor.** An identifier is replaced and carries a typed edge to the replacement [1]. This is the well-handled case and the one ATT&CK does correctly for Enterprise.

**D4 — Re-cut (split and merge).** A concept is redistributed across several successors, or several are absorbed into one. ATT&CK's relation is 1:1, so a split is encoded as merges onto the narrowest survivor: representable but lossy, and the loss is unannounced. COnto-Diff types exactly these as first-class complex operations [26]; ATT&CK does not.

**D5 — Re-parenting and cross-layer promotion.** An identifier keeps its name but changes its place in the hierarchy: a technique is re-parented, changes tactic, or — the v19 case — is promoted out of the technique layer into the tactic layer. No technique-to-technique relation can express the last of these.

**D6 — Intensional drift.** The identifier, its name and its position are all stable while its description, detection guidance or scope changes. This is invisible to every identifier-keyed mechanism in the ecosystem. It is the category that OBO Principle 19 exists to govern [54] and the category ATT&CK has no signal for.

Two properties do the analytical work. First, **repairability is not monotone in severity**: D3 is fully repairable, D4 mechanically repairable but semantically lossy, D5 partly representable, and D6 — the mildest-looking operation — entirely unrepairable by identifier arithmetic, because there is nothing to arithmetic over. Second, **detectability is inversely related to repairability**: the operations a consumer can detect from the bundles are precisely the ones that can be fixed, and the one that cannot be fixed is also the one whose published signal, `x_mitre_version`, has precision 0.447 and recall 0.641 (Section 6.3). A consumer watching for drift with the mechanisms the ecosystem provides sees D1 through D4 clearly, D5 partially, and D6 barely at all.

We also separate two clocks, because conflating them produces the two wrong headline claims this literature oscillates between. The **identifier clock** governs D2 through D5 and is episodic, bursty and per-domain recurrent; the **semantic clock** governs D6 and has run at a stable rate since 2020. "ATT&CK is unstable" is false of the identifier clock in the modern Enterprise regime; "the damage was a one-off in 2020" is false of both. Section 6 measures both.

Finally, the definition the downstream sections depend on. Given a label set *L* asserted under release *V* and a target *W*, **normalization** is a map *L → L'* over identifiers, computed from *W*'s published revocation graph. **Comparability** is the property that two label sets expressed under different releases can be placed on one axis without changing what either asserts. Normalization is necessary and not sufficient for comparability, and Section 8 argues that the gap between the two is where the field's actual problem lives.

## 5. Data and Methodology

We extracted every public ATT&CK STIX bundle for the three domains into a normalized relational store, recording for each object its STIX identifier, ATT&CK identifier, type, name, sub-technique flag, revoked and deprecated flags, object version, timestamps, tactic assignment, platforms, and SHA-256 hashes of the description and detection fields, together with every relationship. Release-level analyses use the first release of each major version; the deployed-corpus analysis in Section 9 uses every published release — 41 Enterprise, 38 Mobile, 27 ICS.

**Table 1.** The release corpus.

| Domain | Releases analysed (major / all) | First | Last |
|---|---|---|---|
| Enterprise | 19 / 41 | v1.0 (2018-01-17) | v19.0 (2026-04-28) |
| Mobile | 19 / 38 | v1.0 (2018-01-17) | v19.0 (2026-04-28) |
| Ics | 12 / 27 | v8.0 (2020-10-27) | v19.0 (2026-04-28) |

Churn between consecutive major releases is computed over live techniques: additions, revocations, deprecations, renames, description rewrites detected by hash inequality, detection-field rewrites, tactic-set changes, identifier-set Jaccard and edge deltas. Identifier survival traces every identifier live at a source release forward to v19.0, classifying it as live, revoked, deprecated or absent, and marking it recoverable when transitive `revoked-by` resolution from the source identifier terminates on a live identifier at v19.0. Semantic drift is measured only over identifier-stable techniques — live at both endpoints, same identifier — using token Jaccard between descriptions, with J < 0.8 as the substantial-rewrite threshold.

Growth decomposition classifies every new group-technique `uses` edge into five mutually exclusive buckets: edges belonging to groups newly added to ATT&CK; **genuine new intelligence**, where the technique existed at the earlier release and the group did not previously assert it; **new technique**; **sub-technique refinement**, where the new edge is a child of a technique the group already asserted; and **revocation re-mapping**, where the new edge is the successor of an edge the group lost in the same transition. The last two are bookkeeping by construction.

The attribution experiment (Section 7.1) back-projects modern group profiles into a legacy vocabulary and runs four conditions over an identical candidate universe with identical random draws: *back-projected*, *naive* (legacy artefact matched against modern profiles by exact identifier), *ATT&CK-Norm* (normalized onto the modern release first), and *oracle*. Because every condition consumes the same underlying intelligence content, a contrast between conditions cannot be explained by a difference in what was observed. The coverage experiment (Section 7.2) freezes a detection portfolio at a release and re-measures its claimed coverage against v19.0, naively and after normalization.

Three commitments bind the reporting. Absolute accuracies from the attribution experiment are internal-consistency scores computed inside one curator's graph and are never reported as attribution performance. The condition we call *back-projected* is a transcription of 2026 intelligence into a legacy vocabulary, not a reconstruction of a legacy system; the real archival control scores 0.969 at v1.0 against the back-projection's 0.668, and we publish that cell as a diagnostic. And the headline penalties are noise-free and therefore upper bounds, as Section 7.4's factorial establishes.

## 6. Measuring Ontology Drift in ATT&CK

### 6.1 Churn is one large event and a long quiet tail

**Figure 1.** Live technique count, and per-release adds, revocations and description rewrites, Enterprise v1.0 to v19.0.

**Table 2.** Per-release churn, Enterprise (selected transitions; the full table covers all 18).

| Transition | Date | Live | Added | Revoked | Deprecated | Renamed | Desc. rewritten | Detection rewritten | Tactic changed | J(ID) | Edges +/- |
|---|---|---|---|---|---|---|---|---|---|---|---|
| v2.0→v3.0 | 2018-10-23 | 223 | 4 | 0 | 0 | 1 | 219 | 218 | 4 | 0.982 | +285/−0 |
| v5.0→v6.0 | 2019-10-23 | 266 | 22 | 0 | 0 | 2 | 60 | 24 | 2 | 0.917 | +102/−0 |
| v6.0→v7.0 | 2020-03-31 | 428 | 302 | 129 | 11 | 17 | 106 | 60 | 10 | 0.222 | +1235/−750 |
| v7.0→v8.0 | 2020-10-27 | 525 | 97 | 0 | 0 | 3 | 34 | 17 | 0 | 0.815 | +102/−2 |
| v8.0→v9.0 | 2021-04-29 | 552 | 27 | 0 | 0 | 6 | 149 | 52 | 5 | 0.951 | +642/−2 |
| v10.0→v11.0 | 2022-04-25 | 576 | 12 | 2 | 0 | 9 | 151 | 44 | 0 | 0.976 | +288/−1 |
| v12.0→v13.0 | 2023-04-25 | 607 | 13 | 0 | 0 | 1 | 87 | 13 | 0 | 0.979 | +112/−16 |
| v14.0→v15.0 | 2024-04-23 | 637 | 12 | 0 | 0 | 3 | 98 | 4 | 0 | 0.981 | +208/−34 |
| v16.0→v17.0 | 2025-04-22 | 679 | 24 | 1 | 0 | 5 | 79 | 5 | 2 | 0.963 | +313/−558 |
| v17.0→v18.0 | 2025-10-28 | 691 | 12 | 0 | 0 | 2 | 49 | 583 | 0 | 0.983 | +328/−11 |
| v18.0→v19.0 | 2026-04-28 | 697 | 23 | 17 | 0 | 4 | 41 | 0 | 198 | 0.944 | +270/−86 |

One row dominates. The v6.0 to v7.0 transition of 2020-03-31 has an identifier-set Jaccard of 0.222, adds 302 techniques, revokes 129 and deprecates 11, and removes 750 group-technique edges while adding 1235. Nothing else in eight years comes close; the next-largest Enterprise Jaccard drop is 0.944. A reviewer is entitled to say the catastrophic numbers in this paper are one release, and we say it first.

But two rows refuse the "closed wound" reading. The v17.0→v18.0 transition rewrote the detection field of 583 of 679 surviving techniques while editing only 49 descriptions — an event no consumer-facing filter can express. And v18.0→v19.0 revoked 17 live techniques and changed the tactic assignment of 198 identifier-stable ones in one step. The identifier clock is quiet, not stopped.

### 6.2 Identifier survival: the concession, measured

**Figure 2.** Identifier survival curves by source release, and recoverability at the newest release.

**Table 3.** Identifier survival and half-life, Enterprise, measured to v19.0.

| Source release | Date | Identifiers | Live at v19.0 | Survival | Revoked | Deprecated | Recoverable | Half-life |
|---|---|---|---|---|---|---|---|---|
| v1.0 | 2018-01-17 | 188 | 77 | 0.410 | 100 | 11 | 100 | v7.0 (2.2 y) |
| v6.0 | 2019-10-23 | 266 | 126 | 0.474 | 129 | 11 | 129 | v7.0 (0.4 y) |
| v7.0 | 2020-03-31 | 428 | 415 | 0.970 | 12 | 1 | 12 | not reached |
| v12.0 | 2022-10-25 | 594 | 581 | 0.978 | 13 | 0 | 13 | not reached |
| v18.0 | 2025-10-28 | 691 | 674 | 0.975 | 17 | 0 | 17 | not reached |

The v1.0 cohort retains 0.410 of its identifiers to v19.0 with a half-life of 2.2 years; the v6.0 cohort retains 0.474 with a half-life of 0.4 years. Both half-lives fall at v7.0, which is to say both are the same event. From v7.0 onward no cohort has a half-life at all: survival to v19.0 is 0.970, 0.978 and 0.975 for the v7.0, v12.0 and v18.0 cohorts. In every Enterprise row the recoverable count equals the revoked count exactly: every revoked Enterprise identifier in the corpus resolves to a live one through the published revocation graph. The apparatus works.

Three facts keep this from being the end of the paper. First, the guarantee is Enterprise-only. Mobile's v2.0→v3.0 transition of 2018 renumbered the entire identifier namespace: Jaccard 0.000, 76 techniques vanishing with no tombstone and no successor, zero recoverable — the most destructive event in the corpus, uncrosswalkable, invisible to STIX-identifier-keyed tooling, and two years *before* the event the literature cites. Second, recurrence: five of 47 major-to-major transitions across the three domains have an identifier Jaccard below 0.80, a hazard of 0.106 per transition, one event per 4.4 domain-years, or roughly one restructuring somewhere in ATT&CK every 1.5 calendar years — in 2018, 2020, 2021, 2022 and 2026. ICS is drawing right now: v18.0→v19.0 revokes nine techniques into a shared namespace and introduces ICS sub-techniques for the first time, structurally the move Enterprise made six years earlier. Third, the hazard is unhedgeable: over 17 lagged Enterprise transition pairs the best leading indicator of next-release revocation is detection-field edits at Spearman rho +0.377, permutation p 0.134, and the techniques doomed at v7.0 had been edited *less* beforehand than the survivors. A consumer cannot time-hedge against a restructuring, which is why any protocol must be standing rather than triggered.

### 6.3 The semantic clock, and why nobody hears it

**Figure 3.** Silent semantic drift among identifier-stable techniques.

**Table 4.** Semantic drift among identifier-stable techniques, measured to v19.0.

| Source release | ID-stable techniques | Description edited | Mean token Jaccard | Substantial rewrite (J<0.8) |
|---|---|---|---|---|
| v7.0 | 415 | 0.749 | 0.808 | 0.386 |
| v11.0 | 563 | 0.465 | 0.895 | 0.208 |
| v15.0 | 621 | 0.275 | 0.956 | 0.087 |
| v18.0 | 674 | 0.061 | 0.997 | 0.003 |

Read as a decay curve, these rows say what the identifier analysis cannot. Of the techniques live and identifier-stable from v7.0 to v19.0, 0.749 have edited descriptions and 0.386 are substantially rewritten at a token Jaccard below 0.8; from v11.0 the figures are 0.465 and 0.208; from v15.0, 0.275 and 0.087; from v18.0, over one release, 0.061 and 0.003. Across all post-2020 cohorts, 10% of any pinned Enterprise label set is substantively rewritten within roughly 1.5 years, and the semantic half-life is 4.5 to 6.1 years. The two clocks give opposite answers to one practitioner question: identifier half-life after 2020 is infinite, semantic half-life is about five years, and first 10% staleness arrives in about eighteen months.

This matters only because the drift is *silent*, and the silence is measurable.

**Table 13.** Text change versus version increment, Enterprise, carried-over technique pairs across consecutive major releases.

| Transition | Techniques live in both | Text changed, version bumped | Text changed, no bump | Bump, no text change | Neither |
|---|---|---|---|---|---|
| v7.0→v8.0 | 428 | 26 | 8 | 46 | 348 |
| v10.0→v11.0 | 564 | 114 | 37 | 31 | 382 |
| v14.0→v15.0 | 625 | 73 | 25 | 46 | 481 |
| v16.0→v17.0 | 655 | 79 | 0 | 304 | 272 |
| v18.0→v19.0 | 674 | 22 | 19 | 179 | 454 |
| **All** | **8359** | **871** | **487** | **1077** | **5924** |

Across 8359 carried-over technique pairs, 1358 (0.162) had their description rewritten. Of those, 487 (0.359) carried no `x_mitre_version` increment, while 1077 version increments carried no text change at all. As a detector of description change, the field ATT&CK publishes for the purpose has precision 0.447 and recall 0.641: a consumer polling it to decide whether to re-read a technique is wrong more often than right in both directions [9]. This is not a criticism of diffStix, which explicitly defines a `patches` class for objects changed while the version stayed the same and concedes that the discipline broke historically [48, 34]. It is the observation that MITRE's tooling knows about semantic change while the contract its consumers actually follow — a binary filter that drops revoked and deprecated objects and is silent about surviving objects whose meaning moved [1] — cannot express it. The gap is architectural, not an oversight.

### 6.4 How much of ATT&CK's growth is bookkeeping

**Figure 4.** Per-transition decomposition of new edges for pre-existing groups.

**Table 5.** Knowledge-growth decomposition, Enterprise group-technique edges.

| Transition | New edges (pre-existing groups) | Genuine new intel | New technique | Sub-technique refinement | Revocation re-mapping | Bookkeeping share |
|---|---|---|---|---|---|---|
| v6.0→v7.0 | 1059 | 78 | 187 | 390 | 404 | 0.750 |
| v11.0→v12.0 | 43 | 39 | 2 | 2 | 0 | 0.047 |
| v12.0→v13.0 | 71 | 39 | 5 | 27 | 0 | 0.380 |
| v14.0→v15.0 | 100 | 62 | 4 | 34 | 0 | 0.340 |
| v17.0→v18.0 | 123 | 105 | 13 | 5 | 0 | 0.041 |
| v18.0→v19.0 | 164 | 72 | 15 | 0 | 77 | 0.470 |
| **All transitions** | **3074** | **1752** | **330** | **487** | **505** | **0.323** |

Across all Enterprise transitions 5516 group-technique edges were added; 2442 belong to groups newly added to ATT&CK, which is genuine expansion of the actor catalogue and not in dispute. Of the 3074 added for pre-existing groups — the edges a reader reads as "we learned more about actors we were already tracking" — 1752 are genuine new intelligence, 330 attach to a technique that did not previously exist, 487 are sub-technique refinements of a behaviour already asserted, and 505 are re-mappings of an edge the group lost to a revocation in the same transition. The bookkeeping share is 992 of 3074, or 0.323.

The share is not uniform and its distribution is the argument. It is 0.750 at v6.0→v7.0, as expected, and 0.047 at v11.0→v12.0, which is reassuring. But it is 0.380 at v12.0→v13.0, 0.340 at v14.0→v15.0 and 0.470 at v18.0→v19.0 — three transitions in the supposedly quiet modern era where between a third and a half of the apparent new knowledge about existing actors is the ontology rearranging itself. Any longitudinal claim of the form "ATT&CK now documents *n*% more actor behaviour than at release *k*" is, in expectation, about one third bookkeeping and in specific transitions about half. This is the vocabulary-churn-versus-instance-data separation the knowledge-graph evolution literature insists on keeping as two time series [37], and the direct answer to the benchmark-growth claim we measured independently at approximately 96% pre-existing catalogue [6].

## 7. Downstream Impact of Drift on CTI Analytics

### 7.1 Attribution

**Figure 5.** Attribution accuracy by condition, and the drift penalty with confidence bands.

**Table 6.** The controlled attribution experiment, k = 10, analysis at v19.0.

| Artefact vocabulary | k | Groups | OOV | Contemporaneous | Naive | ATT&CK-Norm | Oracle | Drift penalty (pp) [95% CI] | Recovered |
|---|---|---|---|---|---|---|---|---|---|
| v1.0 (2018-01-17) | 10 | 47 | 0.256 | 0.696 | 0.274 | 0.450 | 0.912 | 42.2 [37.8, 46.8] | 0.42 |
| v6.0 (2019-10-23) | 10 | 78 | 0.283 | 0.684 | 0.222 | 0.468 | 0.850 | 46.2 [41.6, 51.0] | 0.53 |
| v7.0 (2020-03-31) | 10 | 88 | 0.013 | 0.810 | 0.740 | 0.750 | 0.862 | 7.0 [4.4, 9.8] | 0.14 |
| v12.0 (2022-10-25) | 10 | 123 | 0.011 | 0.840 | 0.820 | 0.832 | 0.878 | 2.0 [0.6, 3.8] | 0.60 |
| v18.0 (2025-10-28) | 10 | 161 | 0.015 | 0.860 | 0.844 | 0.858 | 0.858 | 1.6 [0.6, 2.8] | 0.88 |

Holding the intelligence content constant and varying only the vocabulary the observation is expressed in, top-1 attribution accuracy falls by 42.2 points [37.8, 46.8] for a v1.0 artefact and 46.2 points [41.6, 51.0] for a v6.0 artefact. Across the 2020 boundary the penalty is 7.0 points [4.4, 9.8]; in the modern regime it is 2.0 points [0.6, 3.8] at v12.0 and 1.6 points [0.6, 2.8] across the single v18.0-to-v19.0 boundary. Normalization recovers 0.42 and 0.53 of the legacy penalty and 0.60 to 0.88 of the much smaller modern one. Two disclosures belong in the result rather than a footnote. The legacy conditions all consume the same back-projected observation and the back-projection is lossy — 389 of 697 modern techniques have no v1.0 ancestor and profiles retain 0.618 of their distinct identifiers, against 155 of 697 and 0.903 at v7.0, and 7 of 697 and 0.998 at v18.0 — and the absolute numbers are internal-consistency scores inside one curator's graph, never attribution performance.

**Table 7.** Robustness across scoring functions and profile definitions.

| Vocabulary | Scorer | Software-mediated | Contemporaneous | Naive | ATT&CK-Norm | Drift penalty (pp) | Norm. gain (pp) |
|---|---|---|---|---|---|---|---|
| v1.0 | idf-cosine | yes | 0.693 | 0.237 | 0.443 | 45.7 | 20.7 |
| v1.0 | jaccard | yes | 0.447 | 0.260 | 0.390 | 18.7 | 13.0 |
| v1.0 | overlap | no | 0.790 | 0.337 | 0.573 | 45.3 | 23.7 |
| v6.0 | idf-cosine | no | 0.907 | 0.410 | 0.730 | 49.7 | 32.0 |
| v7.0 | idf-cosine | yes | 0.780 | 0.727 | 0.737 | 5.3 | 1.0 |
| v12.0 | jaccard | yes | 0.500 | 0.470 | 0.473 | 3.0 | 0.3 |
| v18.0 | idf-cosine | yes | 0.867 | 0.843 | 0.863 | 2.3 | 2.0 |
| v18.0 | overlap | no | 0.987 | 0.983 | 0.987 | 1.0 | 1.0 |

The penalty survives every scoring function and both profile definitions; its magnitude does not. The robust claim is the sign and the ordering.

### 7.2 Coverage claims

**Figure 6.** Coverage claims under a frozen capability, and the random-portfolio sweep.

**Table 8.** Coverage claims under a frozen capability, re-measured at v19.0.

| Capability frozen at | Portfolio | Claimed then | Naive at v19.0 | Normalized at v19.0 | Identifier artefact (pp) |
|---|---|---|---|---|---|
| v6.0 (2019-10-23) | 258 | 97.0% | 17.4% | 33.9% | 16.5 |
| v10.0 (2021-10-21) | 512 | 90.5% | 71.3% | 72.9% | 1.6 |
| v17.0 (2025-04-22) | 575 | 84.7% | 80.2% | 82.2% | 2.0 |
| v18.0 (2025-10-28) | 582 | 84.2% | 81.1% | 83.2% | 2.2 |

A capability that covered 97.0% of ATT&CK at v6.0 covers 17.4% of v19.0 if its identifiers are matched naively, and 33.9% after normalization. The 16.5-point gap is pure identifier artefact — coverage the capability still has, hidden by a dead label. The modern rows are small in the same way the modern attribution penalty is small: 1.6, 2.0 and 2.2 points. They are not zero, and a 2.2-point identifier artefact on a claim published to two significant figures is wrong in its last digit for reasons that have nothing to do with detection engineering. This is the temporal complement of the synchronic non-comparability Virkud et al. established under a pinned release [74] and of Shen et al.'s finding that per-technique tallies are the wrong unit [62], and it is why MITRE's own Evaluations methodology declines to emit a coverage number at all [46].

### 7.3 Conclusions, not scores

Showing that scores move is not enough; the bar set by the Gene Ontology precedent is that conclusions move [69].

**Table 10.** Attribution verdict instability.

| Artefact vocabulary | Verdict changed | Changed and now wrong | Was right, then changed | Both wrong but different actor | Normalization changed the verdict |
|---|---|---|---|---|---|
| v1.0 (2018-01-17) | 0.722 | 0.712 | 0.444 | 0.268 | 0.368 |
| v6.0 (2019-10-23) | 0.790 | 0.774 | 0.516 | 0.258 | 0.442 |
| v7.0 (2020-03-31) | 0.116 | 0.100 | 0.066 | 0.034 | 0.028 |
| v12.0 (2022-10-25) | 0.070 | 0.054 | 0.028 | 0.026 | 0.016 |
| v18.0 (2025-10-28) | 0.022 | 0.022 | 0.016 | 0.006 | 0.020 |

The named actor changes in 0.722 of observations for a v1.0 artefact and 0.790 for a v6.0 artefact, and in 0.712 and 0.774 it changes to a *wrong* actor. Across a single modern boundary the figure is 0.022 — small, but not a rounding error where an attribution verdict is an operational and sometimes diplomatic act [12].

**Table 11.** Mitigation leaderboard reordering.

| Portfolios frozen at | Mitigations ranked | Kendall tau, naive | Kendall tau, normalized | Rank-1 changed |
|---|---|---|---|---|
| v6.0 (2019-10-23) | 32 | 0.665 | 0.968 | yes |
| v12.0 (2022-10-25) | 44 | 0.983 | 0.998 | no |
| v17.0 (2025-04-22) | 43 | 0.976 | 1.000 | yes |
| v18.0 (2025-10-28) | 43 | 0.978 | 0.998 | no |

A mitigation leaderboard frozen at v6.0 re-ranks at Kendall tau 0.665 and its top-ranked mitigation changes; normalization restores tau to 0.968. Two modern rows also flip rank-1 at tau above 0.97, which is the more uncomfortable finding: a leaderboard can be almost perfectly rank-correlated and still recommend a different first control, and the first control is the only row most readers act on.

### 7.4 The two strongest objections, engaged

**"Drift is second-order next to labelling noise."** Products detecting the same behaviour assign disjoint ATT&CK labels within a single pinned release [74], roughly two-thirds of ATT&CK groups have no group-specific behaviour [59], and same-tactic confusability accounts for a large share of extractor error [20]; vendor fragmentation compounds all three [68]. If drift were merely a re-description of that confusability, the penalty should collapse once realistic noise is present. It does not. Injecting a labeller substitution — each observed technique replaced with probability rho by a sibling sub-technique, its parent, or a same-tactic technique, applied before back-projection so it flows identically into all four conditions — leaves the penalty intact at every boundary: +0.439 at rho=0 falling to +0.342 at rho=0.4 for v1.0, +0.017 to +0.021 for v12.0, +0.012 to +0.012 for v18.0. Separability holds; strict additivity does not. In the large-drift regime the penalty attenuates 22–33% at rho=0.4, because noise and drift consume the same finite signal. The noise-free numbers in Tables 6 and 10 are therefore upper bounds, and normalization degrades faster than the penalty does — recovery at v1.0 falls from 0.44 to 0.30. ATT&CK-Norm recovers less as label quality falls, which is exactly the regime real corpora occupy.

The stratified result cuts against the objection in the opposite direction from its prediction. Splitting the candidate universe by whether a group has any technique unique to it — a criterion this corpus independently reproduces at Saha's own rate, 40 of 123 groups (32.5%) at v12.0 and 48 of 161 (29.8%) at v18.0 — the modern drift penalty on the *identifiable* stratum is +0.0344 [+0.0101, +0.0607] at v12.0 and +0.0239 [+0.0109, +0.0391] at v18.0, against +0.0089 and +0.0067 on the non-identifiable stratum. Drift is 2.5 to 7 times larger precisely where attribution is possible at all. The mechanism is obvious once stated: a group's identifying token is by definition a rare technique, and rare techniques are the ones ATT&CK adds, splits and revokes. A small average over a mostly non-identifiable population hides a material effect on the subset that carries the task.

**"Drift only touches the long tail."** Documentation prevalence at v19.0 is moderately head-heavy: the fifteen most-referenced techniques carry 0.285 of all `uses` edges. Re-running the frozen-capability experiment with techniques weighted by that prevalence makes the artefact *larger* for pre-restructuring portfolios, not smaller: +16.50 points unweighted becomes +20.01 weighted at v6.0, while the modern rows converge (+1.58 to +1.43 at v10.0, +2.15 to +1.57 at v18.0). The most recent revocation wave took T1562.001, ranked 33 of 599 techniques by `uses` edges in the release it left. The head is also itself a product of restructuring, so head-weighting is not a neutral operation.

We state this refutation with its bound. `uses` edges count how many groups, malware families and tools MITRE has *documented* as using a technique: a cumulative, monotone stock over cited reports, biased toward behaviours that are easy to narrate. CTID's Sightings Ecosystem measures a *flow* of defender telemetry over a window and is materially more concentrated [49]. The long-tail objection is refuted on documentation prevalence — the fraction of the written CTI corpus affected — and untested for the fraction of the alert stream affected, because the telemetry that would test it on its own data is not reachable here.

## 8. ATT&CK-Norm: A Version-Normalization Protocol

This section specifies the protocol, reports what it buys, and then argues that it should not be the contribution of this paper. We put the case against it at full strength because the alternative — shipping a crosswalk as the remedy for a semantic problem — repeats the error the paper set out to diagnose.

### 8.1 Specification

ATT&CK-Norm maps a set of technique identifiers asserted under some release onto a target release snapshot in three steps. **Step 1** resolves each identifier transitively through the target's `revoked-by` graph, with a hop limit and cycle detection. **Step 2** classifies the landing identifier as live in the target or not. **Step 3**, disabled by default, attempts roll-up: if the resolved identifier is not live and is a sub-technique, climb to the surviving parent.

The load-bearing design decision is the return type. `normalize_with_ledger` returns a `NormalizationResult` with five fields: `kept`, identifiers that resolved one-for-one; `merged`, a map from target identifier to the several predecessors that landed on it; `dropped`, identifiers with no live successor; `demoted`, resolutions that crossed an abstraction level; and `rolled_up`. A set-valued wrapper exists and its docstring says what it is — a bare set cannot report how many identifiers were merged away or dropped, and reporting only the set is the reporting failure this study is about. We say this plainly because our own earlier specification was set-valued, and the audit below is what changed it.

### 8.2 What it buys

Two things, both real and both narrow. On legacy artefacts, transitive revocation resolution recovers 0.42 to 0.53 of the attribution penalty (Table 6), a mean top-1 gain of +20.1 points for pre-v7.0 artefacts, and it lifts frozen-capability coverage from 17.4% to 33.9% at v6.0 (Table 8). On coverage ranking it works cleanly across the whole corpus: mean Kendall tau rises from 0.931 to 0.992, three of the four naive rank-1 flips vanish, and none are introduced (Table 11).

That is the entire measured benefit. Post-v7.0 the mean top-1 gain is +0.77 points, and the gain's 95% confidence interval includes zero in 23 of 36 post-v7.0 conditions. ATT&CK-Norm is a bounded legacy-migration tool, not a standing cure.

### 8.3 Five ways the protocol is wrong, and one way it is dangerous

**(a) It destroys cardinality without saying so.** The v19.2 Enterprise bundle carries 149 technique `revoked-by` edges. Eight targets are many-to-one, absorbing 20 predecessor identifiers between them, and the largest — T1685 — absorbs five: T1054, T1089, T1562, T1562.001 and T1562.006. A set-valued normalizer maps `{T1562, T1562.001, T1562.006}` and `{T1562.001}` to the same singleton `{T1685}`. The map is a function, not an injection, and the information destroyed is exactly the information a longitudinal comparison needs. This is not hypothetical on real corpora: TRAM's bootstrap label set goes from 537 to 503 distinct live classes, with 28 targets absorbing 62 source classes and 14.75% of its 25,770 label instances landing in a merged class; rcATT goes from 215 to 199 with 9.37% of its 6,235 instances merged. A benchmark whose class count silently falls from 537 to 503 is not the same benchmark, and a score reported against it is not comparable to a score reported against its predecessor.

**(b) The crosswalk it trusts performs unlabelled abstraction changes.** Of the 149 Enterprise revocation edges, 119 map a top-level technique onto a sub-technique, 13 map top to top, 10 map sub to sub, and 7 map a sub-technique *up* to a parent. That is 126 of 149 edges — 85% — changing the abstraction level of the assertion, silently. Applying the map to a parent-level legacy label therefore narrows its extension in the overwhelmingly common case. ATT&CK's design document is explicit that abstraction level is an editorial choice [14], and Summiting the Pyramid's move to a different coverage denominator is a downstream consequence of the same instability [64]. Our protocol detects this only because we added a `demoted` field after the audit; nothing in the published data flags it.

**(c) It has no domain guard.** Step 2 drops anything not live in the target snapshot. That single bucket mixes three conditions requiring opposite remedies: a concept genuinely withdrawn, an identifier from another ATT&CK domain, and a scrape or transcription artefact. Section 8.4 shows what this costs on a real benchmark.

**(d) It is blind to intensional drift by construction.** Between v18.1 and v19.2, 674 techniques are live and identifier-stable at both ends. Of those, 198 changed their tactic assignment and 41 changed their description. `normalize_with_ledger` returns all 674 unchanged, with an empty residual: zero drift signalled, on the release that dissolved the field's most-used tactic. The protocol reports success on the single most disruptive semantic event in the corpus.

**(e) It cannot represent a cross-layer promotion at all.** In v19, the concept *Impair Defenses* was promoted from the technique layer to the tactic layer. There is no relation in the data model that can point a technique at a tactic, and there are zero revocation edges on any tactic in any domain at v19.2. The event is unrepresentable, not merely unrepresented.

**(f) The roll-up branch is dangerous and empty.** We re-ran the attribution experiment with `rollup=True` and `rollup=False` as the only difference, and separately audited the branch across every domain and major release. Top-1 accuracy is identical to three decimal places in every condition, and the branch fires three times in 12,027 resolutions. The reason is structural: MITRE does not orphan sub-techniques — a revoked sub-technique always resolves to a live target — and deprecations without a successor are top-level, so roll-up's precondition essentially does not arise in ATT&CK's data. The branch buys nothing measurable while adding an untested code path capable of fabricating a parent-level assertion the source artefact never made. We ship it disabled and recommend deleting it. A protocol whose most interesting-sounding feature fires three times in 12,027 opportunities should report that rather than describe the feature.

To this list we add a design caution about our own evaluation. `normalize_with_ledger` is close to the algebraic inverse of the back-projection used to build the legacy artefacts in Section 7.1 — both walk the target's revocation and sub-technique graphs — so the recovery fractions in Table 6 are an upper bound on what normalization achieves on real, typo-bearing, cross-domain label sets. Section 8.4 is the demonstration.

### 8.4 A worked counter-example, and a second one

**The T1562 collapse.** At v18.1, T1562 *Impair Defenses* is a top-level technique with twelve children spanning firewalls, cloud logs, command history, safe-mode boot and downgrade attacks. Three groups assert the generic parent rather than a child — the standard CTI convention for "the report says defenses were impaired but not how". Version 19 dissolved this: TA0005 was renamed in place from *Defense Evasion* to *Stealth*, keeping its STIX identifier and object version, and a new tactic TA0112 *Defense Impairment* was minted to hold the old family [78]. Because `revoked-by` cannot point a technique at a tactic, MITRE mapped T1562 onto T1685 *Disable or Modify Tools* — one of its own former children — while six of the other eleven children went to T1686, T1686.001, T1686.002, T1688, T1689 and T1690.

So `normalize_with_ledger({T1562}, v19.2)` resolves in one hop, lands on a live identifier, and reports one kept, zero dropped, zero merged. It succeeds, and the answer is wrong. An analyst who wrote T1562 because a report said the actor disabled the host firewall is now recorded as asserting that the actor tampered with EDR tooling: a strictly narrower and factually different claim, in a tactic that did not exist when the artefact was written. One group asserting `{T1562, T1562.001, T1562.002, T1562.004}` normalizes to `{T1685, T1685.001, T1686}` — four documented behaviours become three, and its measured technique breadth falls by one purely as bookkeeping. The only part of our protocol that catches any of this is the `demoted` field, which reports an abstraction change, not a wrong answer. Read this example as the paper's own falsification of its constructive claim: the protocol's failure mode is not an error message, it is a confident, plausible, wrong result.

**Domain misassignment read as deprecation.** Our validity analysis records CTI-Bench's CTI-ATE as carrying 8 identifiers invalid at v19.2, of which 7 are unrepairable (Table 9). All seven — T1404, T1406, T1577, T1628, T1630, T1643, T1655 — come from a single row of the label file whose platform column says Enterprise while its entire seven-identifier gold set is mobile-only. All seven are live in mobile-attack v19.2. So 87.5% of that benchmark's apparent drift damage is not drift at all; it is a single-version labelling error [4]. Run naively, ATT&CK-Norm would report seven unrepairable deprecations and be wrong seven times, and a paper reporting that number would have laundered a data-entry mistake into a finding about ontology churn. The remedy is the domain guard in Section 10's contract, not a cleverer crosswalk.

### 8.5 What follows

Three things. First, roll-up is off by default and should probably be removed. Second, the protocol returns a residual ledger, not a set, and any use that discards the residual is not a use of this protocol. Third — and this is what we ask reviewers to weigh against the rest of the paper — normalization is not verdict-neutral and must never be applied silently. It changes the attribution verdict in 0.368 to 0.442 of trials for v1.0 to v6.0 artefacts and 0.006 to 0.030 for v7.0 and later (Table 10). Silently normalizing a label set is a research-integrity event of the same kind as silently re-labelling data. AVClass established the precedent in security that a normalization map is an artefact to be published and versioned, not a preprocessing step to be mentioned [19]; ATT&CK-Norm should be held to that standard and no lower one.

## 9. Label Validity of Deployed CTI Corpora

**Figure 7.** Label-validity curves for four deployed CTI corpora.

**Table 9.** Label validity of deployed corpora, evaluated against every published release.

| Corpus | Distinct labels | Label instances | Sub-technique labels | Best-fit release | Fit | Releases where all labels valid | Invalid today | Repairable |
|---|---|---|---|---|---|---|---|---|
| ctibench-ate | 120 | 397 | 0 | v14.0 (2023-10-31) | 0.942 | **none** | 8 (0.067) | 1 |
| rcatt | 215 | 6235 | 0 | v4.0 (2019-04-30) | 1.000 | 8 (v4.0–v6.3) | 107 (0.498) | 99 |
| tram-bootstrap | 537 | 25770 | 344 | v13.0 (2023-04-25) | 0.939 | **none** | 43 (0.080) | 43 |
| tram2 | 50 | 5143 | 24 | v8.2 (2021-01-27) | 1.000 | 18 (v8.2–v16.1) | 2 (0.040) | 2 |

Two of these four corpora match no ATT&CK release at all. CTI-Bench's CTI-ATE achieves a best fit of 0.942 at v14.0 and there is no release at which every one of its 120 labels is simultaneously valid; TRAM's bootstrap set achieves 0.939 at v13.0 with the same property. A label set that is internally inconsistent with respect to every release its authors could have used is not a snapshot of a vocabulary; it is an accretion, and its "version" is a fiction even before drift is considered. For CTI-ATE, seven of the eight currently-invalid identifiers are the mis-typed mobile row of Section 8.4, and its entire label space contains zero sub-technique identifiers — a parent-only granularity policy, undeclared, that makes any comparison with a successor benchmark at sub-technique granularity a category error rather than a score difference [4, 30, 29].

rcATT is the honest case and the worst one. Its label space fits v4.0 exactly and is fully valid across eight consecutive releases, v4.0 to v6.3 — a well-constructed 2019 artefact [44, 8]. Measured today, 107 of its 215 identifiers (0.498) and 0.380 of its 6,235 label instances are invalid at v19.2; 99 of the 107 are repairable by revocation chain and eight are not. A model trained on rcATT and evaluated against a current gold set is scored against a vocabulary in which half its output alphabet no longer exists, and nothing in the artefact says so, because nothing in it says which release it encodes.

TRAM2 is the counter-example that proves the discipline is achievable: 50 labels, fully valid across 18 consecutive releases, 2 invalid today and both repairable. A deliberately small, parent-mixed label set with a long validity window is a design choice, and it is the right one for a corpus intended to survive.

**Table 12.** ATT&CK version declarations in deployed corpora.

| Corpus | Documentation files scanned | ATT&CK version declarations found |
|---|---|---|
| cti-bench | 2 | 0 |
| rcATT | 2 | 0 |
| tram | 15 | 0 |

Zero declarations across 19 files. We state the bound of this scan honestly: two of the three repositories contributed only two files each, and an absence over 19 files is a weak instrument. We therefore measured adoption where coverage claims actually live. Across 69 Navigator-format layer files in the local clones, five declare `versions.attack` and all five are MITRE's own sample or test fixtures [18]. Of 57 published vendor threat-report layers, zero declare an ATT&CK content version: 39 are in a layer format where no such field exists and 18 are in a format where it exists and all 18 omit it [79]. Those 57 layers carry 2,143 technique annotations, of which 739 (34.5%) name an identifier revoked or deprecated at v19.2; 49 of the 57 files contain at least one; 72 of the dead annotations are deprecations with no successor; and five name identifiers absent from v19.2 entirely, four of them Mobile identifiers, one on a layer whose declared domain is Enterprise. Because the layer format's version field is optional and defaults to the current release [15], opening any of these today silently re-bases the claim onto v19.2 [16].

Declaring a version is necessary and not sufficient. One repository we audited announces a deliberate remap to ATT&CK v12.0 and its inherited label split still carries 203 dead label occurrences, 128 of them a technique revoked five releases before the declared target [10]. A declaration without a validation step is a statement of intent.

## 10. Discussion and Reporting Discipline for CTI Research

### 10.1 The contract, in four lines

The constructive contribution of this paper is not a tool. It is a contract that costs an author one JSON header and roughly thirty lines of code, and that a reviewer can check in under a minute. We state it as line items because that is how it must be checkable.

**For any CTI paper or dataset.** (1) The ATT&CK **domain** and **exact release**, plus the **SHA-256 of the STIX bundle**, recorded *in the artefact* and not only in the prose. Domain is not optional: the seven mis-typed mobile identifiers of Section 8.4 are a domain failure, not a version failure, and no version pin would have caught them. (2) Whether identifiers were **normalized**, and onto which target release. (3) The **residual** — `kept / merged / dropped` counts, with the dropped identifiers listed verbatim. (4) For any cross-time comparison, a statement that **both sides were projected onto one reference release**.

**For a benchmark, additionally.** (5) The **label granularity policy** — parent-only, sub-technique-only, or mixed — and the class count before and after normalization. CTI-ATE's 120 labels contain zero sub-technique identifiers; a successor evaluated at sub-technique granularity is measuring a different task under the same metric name [30, 29, 4]. (6) A **CI re-validation script** that fails the build when any gold label is not live in the declared release. Answer keys decay measurably in static benchmarks generally [75]; this is the domain-specific detector.

**For a vendor coverage claim, additionally.** (7) The ATT&CK version **and the denominator as a number** — live techniques in that release — printed next to the percentage. Three incompatible denominators are already in circulation [84, 64, 82]. (8) The claim **re-stated against the current release, or explicitly marked as-of**.

We are specific about the costs because a contract nobody pays is a recommendation, not a discipline. For an author the cost is reputational rather than technical: a residual line makes label decay public, and rcATT's would read 0.498 of identifiers and 0.380 of label instances invalid at v19.2 (Table 9). For a benchmark it is a standing maintenance obligation and the loss of cross-release comparability by default — which is the point, because that comparability was never real. For a vendor it is that coverage percentages become non-monotone in public: a capability that improves can report a lower number because the denominator grew, and Table 8 is that phenomenon with the capability held still.

We also propose the missing quality dimension. The CTI quality literature assesses accuracy, completeness, timeliness, relevance, provenance and interoperability of an intelligence item [76, 60, 41, 27, 40, 11]. None is defined over the coordinate system the item is expressed in. We name the gap **vocabulary provenance**: the property that an artefact's reference vocabulary is declared, resolvable, and validated against. It is measurable — the residual ledger *is* its measurement — and on current evidence the field scores zero on it.

### 10.2 What MITRE should change: seven ports, no inventions

Every item below already exists in ontology engineering or in another security vocabulary. None is a research proposal.

1. **A two-tier successor vocabulary.** `revoked-by` is 1:1 and cannot express a split or a cross-layer promotion. Port OBO Principle 19's distinction: an exact-successor relation alongside an inexact-successor relation of the `consider` kind [54]. T1562 should carry inexact-successor edges to all seven of its v19 successors and an explicit cross-layer pointer to TA0112, not a single revocation edge to T1685.
2. **A controlled obsolescence-reason vocabulary** — superseded-by-split, merged, re-scoped, promoted-to-tactic, out-of-scope — as OBO does with a dedicated annotation property [54]. Today deprecation carries no reason, so *dropped because the concept was withdrawn* and *dropped because it was absorbed* are indistinguishable to a consumer, which is precisely the conflation Section 8.3(c) identifies in our own protocol.
3. **Make retirement visible in the human-readable field**, as OBO's mandatory obsolescence label prefix does [54, 53]. ATT&CK's retirement is metadata-only, so any tool that joins on technique name — and many do — keeps working silently against a dead concept.
4. **Referent stability at a stable identifier.** Renaming TA0005 in place from *Defense Evasion* to *Stealth* is the edit Principle 19 forbids: a changed referent requires a new identifier [54]. The remedy is to mint a new tactic identifier for the new concept and obsolete TA0005. We measured 102 renamed-in-place objects across the corpus, two of them tactics; the technique-level cases are usually benign clarifications, and the tactic-level cases are not.
5. **Prior-version and compatibility links.** OWL has supplied `priorVersion`, `backwardCompatibleWith` and `incompatibleWith` for two decades [57]; OBO Principle 4 requires version identifiers and perpetual resolvability [55]. ATT&CK has release immutability and nothing else: lineage is reconstructed by sorting release names. These belong as properties on the collection object, and a declared `incompatibleWith` on the v7.0 and v19.0 boundaries would have told every consumer in one field what this paper took a measurement study to establish.
6. **Publish the evolution mapping as a first-class versioned artefact, typed.** diffStix already computes the basic operations and publishes them as an untyped change set [34, 48, 7]. COnto-Diff's contribution was showing that typing them — merge, split, move, substitute — turns a diff into an evolution mapping that downstream tools can execute [26]. Typing is what makes the bookkeeping-versus-intelligence split of Section 6.4 computable rather than asserted, and it is what would let CTID's ATT&CK Sync move from enumerating affected mappings to quantifying what a change costs [5].
7. **Make the Navigator layer's ATT&CK version field mandatory.** It is optional and defaults silently to the current release [15], which is why every one of the 57 vendor layers we audited is version-orphaned and re-bases on open [16, 79]. This is a one-line schema change with the largest adoption effect of anything on this list.

Two of these — the inexact-successor relation and the typed published mapping — are load-bearing for the rest. The other five are hygiene that ontology providers in other disciplines treat as table stakes, and the reason to say so bluntly is the Gene Ontology precedent: it shows what happens when a discipline's flagship vocabulary evolves without them [69].

### 10.3 What a contribution in this space must demonstrate

The query asks what an SCI-level contribution here must show, and the state-of-the-art survey sets the bar [47, 63]. On our evidence it is four things: **measurement over the full release history rather than a pair of endpoints**, because the two clocks are only visible longitudinally; **conclusions, not scores**, the standard the Gene Ontology precedent set a decade ago [69]; **an adversarial audit of the paper's own remedy**, which is what Section 8 is, because a normalization protocol evaluated only by its author is a tool paper wearing a measurement paper's clothes; and **a separability argument demonstrated rather than assumed**, because the labelling-noise objection is strong enough to end a paper that merely asserts its design controls for it [74, 59].

One structural limitation bounds the whole genre, this paper included. Every experiment here draws its observations, profiles, ground truth and back-projection map from one curator's graph. The instrument that would open that loop is a double-labelled incident corpus in which two independent analysts label the same intrusions under two ATT&CK releases, yielding the drift term and the inter-analyst term simultaneously and from outside MITRE's own edges. No such corpus exists publicly; telemetry-grounded evaluation is the nearest structurally drift-resistant design we know of [28], and building the double-labelled corpus is the most valuable infrastructure the CTI research community could fund [36].

Finally, a caution about the obvious remedy. "Pin the version" is correct and insufficient, and the insufficiency is the paper's most transferable finding. Pinning fixes identity and does nothing about intension, because 0.465 of v11.0's identifier-stable techniques have edited descriptions by v19.0 and the published change signal has precision 0.447 and recall 0.641 (Section 6.3). Worse, pinning freezes an analytic against a vocabulary the field has moved past, which is a trade and should be named as one. The discipline is to pin, declare, validate and re-project — not to pin and stop.

## 11. Threats to Validity

**Construct.** The absolute accuracies in Tables 6 and 7 are internal-consistency scores computed inside ATT&CK's own graph, not attribution performance. The condition labelled *contemporaneous* is 2026 intelligence transcribed into a legacy vocabulary, not a reconstruction of a legacy system: the real archival control scores 0.969 at v1.0 against the back-projection's 0.668. Two biases run in opposite directions — dense modern profiles collapsed onto a coarse vocabulary collide in ways no 2018 system experienced, deflating the penalty, while the perfect-recall construction inflates it — and the measured net is downward, so the pre-restructuring penalties are conservative. In the modern regime the two converge and the headline modern claims are unaffected. The *naive* condition is a uniform parent-level worst case; real mixed-granularity artefacts sit between *naive* and *ATT&CK-Norm*.

**Internal.** `normalize_with_ledger` is close to the algebraic inverse of the back-projection, so Table 6's recovery fractions are upper bounds on what normalization achieves on real label sets, as Section 8.4 demonstrates on CTI-ATE. The headline penalties are noise-free: at a realistic labeller-substitution rate the pre-restructuring penalty attenuates 22–33% and normalization's recovery at v1.0 falls from 0.44 to 0.30 (Section 7.4). Ties in the ranking function were checked and are absent at the modern releases.

**External.** The prevalence weighting uses documented `uses` edges — a cumulative, monotone documentation stock — not defender telemetry, which is materially more concentrated [49]. The version-declaration scan covers 19 files in three repositories and is a weak instrument on its own; the 69-layer Navigator audit is the stronger measurement and we rest the adoption claim there. Our four deployed corpora are not a random sample.

**Evidence fidelity.** Positioning claims about the secondary literature rest on search summaries rather than full texts, because the egress path in this environment blocks publisher sites and preprint servers. No verbatim quotation is asserted from any source read only at summary fidelity, and every such claim is attributed as reported. Claims about primary artefacts — ATT&CK bundles, diffStix source, Navigator layer files, benchmark label files — are read from the artefacts themselves. Audited absences, including the missing vocabulary-versioning dimension in the CTI quality literature and the missing version declarations in the corpora scanned, are stated with the bound of the search that found them and never upgraded to proofs. One gap we name rather than paper over: whether the largest comparative extraction evaluation re-baselines its systems onto a common release before comparing is unresolved, and we make no claim about it.

**The evidence that would overturn us.** A representative sample of published CTI artefacts in which a majority carry a resolvable release pin *and* in which mechanically applying the revocation map forward from that pin reproduces an independently authored current-version mapping to within inter-analyst agreement. If migration were that faithful and that common, the residual mechanical gaps would be a footnote and this paper would be a reporting-discipline note rather than a threat-to-validity finding. On the adoption evidence in Section 9, that sample does not currently exist.

## 12. Conclusion

ATT&CK is a better-governed vocabulary than its critics assume and a worse-governed one than its consumers behave as though it were. Its identifier accounting for Enterprise is complete: 149 revocations, 149 edges, zero dangling, zero silent deletions. Its semantic accounting does not exist: 0.162 of carried-over technique pairs are rewritten, 0.359 of those without a version increment, and the only published change signal has precision 0.447 and recall 0.641. Between those two facts sits everything this paper measures — a 42.2-point attribution penalty on a 2018 artefact and 1.6 points across a single modern boundary, a 16.5-point identifier artefact in a frozen capability's coverage claim, a verdict that changes in 0.722 of pre-restructuring observations and 0.022 across one release, a mitigation leaderboard whose top recommendation flips at Kendall tau 0.976, and 0.323 of new intelligence edges for pre-existing groups that are the ontology rearranging itself.

Our normalization protocol repairs the identifier half of that, and we have spent a section arguing against treating it as the contribution. It recovers roughly half the legacy attribution penalty and lifts coverage-ranking tau from 0.931 to 0.992; it also collapses five identifiers into one, demotes an abstraction level in 119 of 149 edges, returns a clean bill of health on the release that dissolved *Defense Evasion*, cannot represent a technique promoted to a tactic, and fires its most-discussed branch three times in 12,027 resolutions. Identifier arithmetic buys comparability of identifiers; it buys nothing about whether two identifiers mean the same thing.

What remains is governance, and it is unglamorous on purpose. Four lines in an artefact header — domain, release and bundle hash; whether normalization was applied and onto what; the kept/merged/dropped residual; and, for cross-time work, the common reference release — plus seven changes to ATT&CK that are ports of practices ontology engineering settled decades ago. The field's habit of citing ATT&CK where it should be pinning it is not a small notational sloppiness. It is the reason a measurable, recurrent and largely unsignalled source of invalidity has gone unmeasured until now.

