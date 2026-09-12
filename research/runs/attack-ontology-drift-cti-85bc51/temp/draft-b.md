# Ontology Drift as a Threat to Validity in Cyber Threat Intelligence Analytics: Measurement, Consequences, and a Reporting Discipline for MITRE ATT&CK

## Abstract

Security machine learning spent a decade learning to control for bias in its data. Temporal splits, spatial base rates, snapshot leakage and conformal rejection under drift are now expected of any credible evaluation. All of that discipline assumes something it never states: that the label space is fixed. In cyber threat intelligence it is not. MITRE ATT&CK, the vocabulary in which almost every TTP-level claim is written, is a versioned ontology that adds, revokes, deprecates, re-cuts, re-parents and silently rewrites its own terms between releases. We name the resulting failure mode *ontology drift*, formalize it as a change in the label space rather than in the distribution over a fixed label space, and show that it is a first-class threat to the validity of CTI analytics — measurable, conclusion-changing, only partly repairable, and undetected by every mechanism the ecosystem currently deploys.

We measure drift across 19 major Enterprise releases, 19 Mobile and 12 ICS releases (Table 1). Identifier churn is episodic: the v6.0-to-v7.0 boundary has an identifier-set Jaccard of 0.222, and pre-restructuring cohorts have identifier half-lives of 0.4 to 2.2 years, while every post-2020 cohort retains above 0.97 of its identifiers (Tables 2 and 3). Semantic churn never stopped: 0.465 of v11.0's identifier-stable techniques have edited descriptions by v19.0, and ATT&CK's own version field detects text change with precision 0.447 and recall 0.641 (Tables 4 and 13). Of 3,074 group-technique edges added for pre-existing groups, 0.323 are bookkeeping rather than intelligence (Table 5). Downstream, a controlled attribution experiment shows a drift penalty of 42.2 points for v1.0 vocabularies and 1.6 points across a single modern release boundary, with the named actor changing in 0.722 and 0.022 of observations respectively (Tables 6 and 10). A frozen detection capability that claimed 97.0% coverage at v6.0 measures 17.4% at v19.0 (Table 8). Across four deployed CTI corpora, 0.498 of rcATT's label vocabulary is invalid today and no ATT&CK release makes CTIBench-ATE's labels simultaneously valid (Table 9); zero of nineteen scanned documentation files declare an ATT&CK release (Table 12).

We meet the strongest published objection — that products disagree on the ATT&CK label for the same behaviour within one pinned release — by experimental design rather than by argument, and verify separability with a noise-injection factorial that also shows the headline penalties are upper bounds. We show that identifier normalization repairs legacy identifiers and buys almost nothing modern, and that the residual is precisely the part nobody detects. The contribution is therefore a threat, its control, and a four-line reporting contract that makes the vocabulary of a CTI artefact a declared, checkable property of that artefact.

## 1. Introduction

The most likely reader of this paper has published a result that is not comparable to the result it is compared against, and does not know it.

That is a strong opening claim, so let us make it concrete. Suppose you published a TTP-based attribution system in 2019, evaluated it against a labelled corpus, and reported that it beat the prior state of the art. Suppose a successor system published in 2023 reports a higher number on the same corpus under the same metric. Between those two dates, the label space in which both systems express their predictions lost roughly half of its identifiers in a single release, gained a second level of abstraction that did not previously exist, and rewrote three-quarters of the descriptions of the terms that survived. Neither paper declares which ATT&CK release it used. Neither could, in practice, because no venue asks. The comparison is not a weak comparison; it is a comparison between two different measurement instruments whose readings are reported in the same units by convention alone.

Security machine learning has an unusually mature literature on exactly this class of error. TESSERACT established that malware classifiers evaluated without temporal and spatial constraints report accuracies that do not survive deployment, and gave the field a vocabulary — temporal bias, spatial bias, time-aware splits — in which such failures can be named and controlled [67]. The catalogue of pitfalls assembled by Arp et al. formalized ten recurring methodological errors across security ML and showed that a large share of published work at top venues commits several of them [35]. Work on concept drift detection and rejection extended this from experimental hygiene into deployed practice: CADE detects and explains drifting samples [22], conformal evaluation supplies calibrated rejection under drift [70], and dataset-shift taxonomies supply the formal machinery that distinguishes covariate shift from prior-probability shift from real concept drift [33]. Malware-specific drift adaptation has become its own subfield [50].

Every one of those instruments operates on a fixed label space. Dataset-shift taxonomy is defined over the joint distribution $P(X, Y)$ with $\mathcal{Y}$ held constant [33]; the temporal-consistency constraints in TESSERACT are constraints on the timestamps of samples, not on the meaning of classes [67]; conformal rejection calibrates non-conformity against a known class set [70]. Where the class set itself changes, the machinery of class-incremental learning addresses only the additive quadrant — new classes arrive, old ones persist unchanged [24] — and only recent work on continual learning with evolving class ontologies treats relabelling of existing classes as a first-class phenomenon at all [43]. Within security, one line of work has explicitly framed ATT&CK version updates as concept drift and proposed incremental learning as the remedy [42], which is closer than anything else in the field and still treats the ontology as a source of distributional disturbance rather than as the coordinate system in which the measurement is expressed.

MITRE ATT&CK is that coordinate system for cyber threat intelligence. It is the label space of TTP extraction [71, 72], of threat-actor attribution [23, 12], of CTI benchmarks for large language models [30, 29, 13], of detection engineering and coverage reporting [74, 46], and of the mitigation and control mappings that security programmes use to justify spend [58, 64]. It is also, by its own design documentation, non-stationary: inclusion criteria are explicitly stated to evolve with observed adversary behaviour, and the level of abstraction at which a behaviour is described is an acknowledged design decision rather than a fact about the world [14]. A practitioner defence of ATT&CK's structure makes the same point from the other direction, arguing that ATT&CK is an ontology rather than a taxonomy and that ontologies are expected to evolve [77]. We agree with both. That is the problem, not the answer.

This paper makes four claims.

**First, ontology drift is a distinct and nameable threat to validity, and it belongs in the same catalogue as temporal bias and sampling bias.** Section 4 formalizes it. Concept drift is a change in $P(Y \mid X)$ over a fixed $\mathcal{Y}$; ontology drift is a change in $\mathcal{Y}$ itself, together with a partial and typed correspondence between the old and new label spaces. The two are not special cases of one another: a system can be perfectly robust to concept drift and still report an incomparable number, because the incomparability is in the units and not in the data. We give a six-operator taxonomy of ontology drift, a distinction between its referential and intensional components, and a distinction between *signalled* and *unsignalled* drift that turns out to carry most of the practical weight.

**Second, the threat is measurable, and we measure it.** Section 6 quantifies drift across the full published release history of three ATT&CK domains. The result is a two-clock model: a slow, episodic referential clock and a fast, continuous intensional clock. The catastrophic identifier numbers that the literature already cites [63] are one event, and a paper that headlines them invites and deserves the rebuttal that the event is six years old. The numbers that survive that rebuttal are the semantic ones.

**Third, drift changes conclusions and not merely scores.** Section 7 reports controlled experiments on attribution, coverage and mitigation prioritization. The template is a decade old and comes from outside security: Tomczak et al. froze a biological analysis pipeline, swept the Gene Ontology version, and showed that the biological conclusions moved [69]. Showing that a score moves is a hygiene complaint. Showing that the named actor changes, that the top-ranked mitigation changes, that a coverage claim falls by four-fifths — that is a validity finding.

**Fourth, the repair is partial, and the unrepairable part is exactly the part that is invisible.** Section 8 evaluates a version-normalization protocol honestly, including a branch of it that we demonstrate never fires, and Section 9 applies label-validity analysis to four deployed CTI corpora. Identifier arithmetic repairs identifiers. It says nothing about whether two identifiers mean the same thing, and the evidence in Section 6 is that meaning is what moves.

We also concede two things loudly, because the argument does not survive without the concessions. MITRE's versioning apparatus is better than most scientific vocabularies: immutable per-release bundles, typed revocation edges with retained tombstones, a published change-computation tool, and a version-stamped layer format for coverage claims [1, 7, 15, 34]. For Enterprise techniques, the identifier accounting is complete — every revoked identifier in our corpus resolves to a live identifier through the published revocation graph. And the synchronic labelling noise floor is large: detection products assign different ATT&CK labels to the same behaviour within a single pinned release [74], and most ATT&CK groups have no technique unique to them [59], so TTP attribution is weakly identifiable before drift enters the picture. We do not claim drift dominates that noise. We claim it is separable from it by construction, we verify that claim with a factorial rather than asserting it, and we report the resulting bounds as bounds.

## 2. Background: ATT&CK as a Versioned Ontology

ATT&CK is published as a series of immutable STIX bundles, one per release per domain, each addressable at a stable path [1]. The consumer-facing usage contract recommends the static-copy workflow explicitly, on the grounds that a downloaded copy does not change underneath an automated pipeline [1]. Pinning is therefore not a community workaround; it is the documented first-class path, and any argument that begins by accusing MITRE of negligence is refuted by that one document.

The retirement contract is likewise normative and well designed. Objects that are no longer useful to track are marked *deprecated*; objects replaced by a different object are marked *revoked* and carry a typed `revoked-by` relationship pointing at the replacement; both classes are retained in every published bundle so that dependent workflows do not break [1]. A helper for resolving revocation targets and a filter for removing retired objects ship in the same document. MITRE further publishes `diffStix`, a change-computation tool whose class taxonomy includes not only additions, revocations and deprecations but a `patches` class covering objects changed while their version field stays the same [7, 34, 48]. The tool's documentation concedes that version-field discipline broke historically and that unintended version changes exist in earlier releases [48]. ATT&CK Navigator, the canonical format for expressing coverage as a layer over the technique matrix, defines a `versions` object carrying the ATT&CK content version the layer was authored against [15], and the Navigator usage documentation describes a layer-upgrade flow for migrating a layer to a newer release [16]. The Center for Threat-Informed Defense funds ATT&CK Sync specifically to flag mappings affected by a release [5], whose existence is an institutional concession that staying in sync is an operational burden.

Against this apparatus, three structural facts matter for what follows.

**The March 2020 restructuring.** ATT&CK v7.0 introduced sub-techniques, a second level of abstraction beneath the technique. This was not an addition; it was a re-cut. Existing techniques whose scope spanned several distinct behaviours were revoked and replaced by a parent-plus-children structure, and existing group and software mappings were re-pointed to the most specific applicable sub-technique. Table 2 quantifies the result. The restructuring is the single most-cited instability in the ATT&CK literature [63], and it is also the best-handled event in the corpus: every revoked Enterprise identifier resolves.

**The v19 tactic re-cut.** In April 2026, ATT&CK retired *Defense Evasion* as a tactic, splitting its content between a renamed *Stealth* and a newly minted *Defense Impairment* [78]. The industry response was a rapid-migration narrative: tooling updates, remapping guides, an expectation that the ecosystem would absorb the change within a release cycle. Section 6 shows what the change actually does to a pinned analytic. The mechanism matters as much as the magnitude: the tactic identifier TA0005 was recycled in place, keeping its identifier while changing its name and referent, and there are no revocation edges on tactic objects at all. A pipeline joining on TA0005 across that boundary compares two different concepts with nothing to follow.

**The 1:1 revocation relation.** The `revoked-by` relation in the Enterprise bundle is total over revoked techniques and never one-to-many. This is a stronger property than the literature usually credits, and it is also the source of a specific defect. A split cannot be expressed by a function into a single successor, so MITRE encodes splits as many-to-one merges onto whichever survivor is narrowest. Eight merge targets in the current Enterprise bundle absorb twenty predecessor identifiers, and the largest absorbs five. The crosswalk is mechanically total and semantically lossy, and the loss is unannounced. We return to this in Sections 4 and 8; the point here is that it is a design consequence of the relation's arity, not an oversight in its population.

A final background fact is about where ATT&CK lives in practice. Coverage claims are authored as Navigator layers whose ATT&CK version field is optional and silently defaults to the current release [15]. An audit of the sample layers shipped in MITRE's own Navigator repository finds that six of eight carry no ATT&CK version [18]. The widely used DeTT&CT tooling omits the ATT&CK version from generated layers by default and stamps its own build constant instead [79]. The declared version, in other words, is the field the ecosystem most reliably leaves empty.

## 3. Related Work

**CTI quality.** A substantial literature measures the quality of threat intelligence. Feed-level evaluations find low overlap and limited timeliness across commercial and open feeds [41, 45]; quality frameworks enumerate dimensions and propose measurement instruments [60, 76]; automated and community-driven assessment schemes score feeds against weighted criteria [27, 38]; and interview-based work documents what quality assurance actually looks like inside CTI teams [40]. The recurring dimensions are accuracy, completeness, timeliness, relevance, provenance and interoperability. None of this literature defines a dimension over the *reference vocabulary* in which intelligence is expressed. A comprehensive measurement-based survey of threat-intelligence research reaches the same enumeration [11]. We searched this literature specifically for a vocabulary-versioning dimension and did not find one; consistent with our evidence discipline, we state that as a bounded absence over the sources we could reach, not as a proof that no such treatment exists.

**ATT&CK as an object of study.** A systematization of ATT&CK in research and practice established that ATT&CK-based results are frequently non-comparable and flagged temporal instability among its open problems [63]; a subsequent survey set out the state of the art and the directions a contribution must advance [47]. Both treat version instability as a known hazard. Neither quantifies its effect on a downstream conclusion, which is the gap this paper occupies.

**Coverage claims.** The strongest empirical work here shows that ATT&CK coverage is not comparable across detection products, because vendors labelling the same behaviour choose different techniques within one pinned release [74]. MITRE's own evaluation programme refuses to emit a single coverage score and governs its protocol precisely to avoid that comparison [46]; independent re-analysis of those evaluations argues that per-technique tallies are the wrong unit and that whole-graph analysis tells a different story [62]. Practitioners are blunter still: a 100% claim is treated as a red flag [80], a widely circulated critique observes that heatmaps count rules rather than coverage and that several incompatible denominators are now in circulation [84], and vendor-side commentary enumerates the ways a coverage percentage is padded [82]. Work on mitigation coverage shows that the achievable ceiling is set by the control catalogue rather than by the defender [58], and CTID's Summiting the Pyramid replaces techniques with implementations as the coverage denominator outright [64]. How coverage layers are built in practice — ad hoc scoring over a data-source mapping that is itself versioned — has been documented from the practitioner side [81]. This literature establishes cross-product incomparability at a fixed version. It does not establish cross-version incomparability at a fixed product, which is the frozen-capability experiment in Section 7.

**CTI benchmarks.** CTIBench introduced a multi-task benchmark including ATT&CK technique extraction, designed around authoritative sources and including a time-controlled split for one of its tasks [30]. Successors have grown the question set under a stable identifier [29], moved to live-API evaluation explicitly to counter benchmark staleness [13], and expanded the label space substantially [6]. Sequence-level ATT&CK reasoning benchmarks add tactic ordering as a surface [17]. Large instruction corpora for security events span two decades of reports without declaring an ATT&CK release [61]. Multi-label ATT&CK classification work has begun declaring existing annotation sets to be non-gold [52], and a fork explicitly verifies labels against official ATT&CK descriptions [73]. Synthesis work targets the ATT&CK long tail directly [65]. The general question of whether static benchmarks decay as their answer keys age has been quantified outside security [75]. What none of this work does is declare the ATT&CK release its gold labels encode, which is what Section 9 measures.

**TTP extraction and attribution.** TTPDrill remains the pre-sub-technique baseline that later systems compare against [71]; TTPHunter and TTPXHunter expand the class count without declaring a release [72]; rcATT is a widely used multi-label ATT&CK classifier whose released label space is a 2019-era flat vocabulary [44, 8]; CAPTAIN represents the current generation of TTP-sequence attribution, also without a declared release [23]. A survey of APT attribution organizes the field by artefact type rather than by ontology version [12]. AttacKG constructs attack graphs against an ATT&CK ontology frozen as a dated HTML scrape [2]. An audit of six TTP systems finds five different ATT&CK ontologies and two declared versions among them [3], and one published remapping dataset declares a target release while still carrying identifiers revoked five releases earlier [10]. Two recent results bound what TTP attribution can achieve at all: two-thirds of ATT&CK threat groups have no group-specific behaviour [59], and LLM agents reproduce documented APT profiles at 55-80% precision, which is an adversarial-validity attack on the premise of TTP-based attribution [66]. Multi-report evaluation of extractors finds that a large share of errors are between same-tactic, description-overlapping techniques [20], which is a rival explanation for label instability that Section 7 must separate from drift. Telemetry-grounded detection evaluation has been proposed as the structurally drift-resistant alternative [28].

**Concept drift and evolving label spaces.** The formal machinery is mature [33] and the security instantiation is well developed [22, 67, 70, 50]. Open-set and unstable class sets have been studied in malware family labelling [51], and label normalization across inconsistent vendor vocabularies has prior art in AVClass [19]. Class-incremental learning covers additive label-space change [24], and continual learning with evolving class ontologies covers relabelling [43]. IncreTTP is the closest security work, framing ATT&CK version updates as drift [42]. The boundary is the point: this literature stops where the label space starts moving in non-additive ways, and a synthesis of that boundary is what motivates our formalization [21].

**Ontology engineering and other versioned vocabularies.** Everything ATT&CK lacks exists elsewhere. OBO Foundry's identifier policy mandates global uniqueness, non-reuse and persistence [53]; its Principle 4 mandates version IRIs, release immutability and perpetual resolvability [55]; its Principle 19 governs stability of term meaning and distinguishes exact from inexact successors [54]. OWL supplies `versionIRI`, `priorVersion`, `backwardCompatibleWith` and `owl:deprecated` [57]. Change management is recognized as the core task of ontology versioning and evolution [56], COnto-Diff types complex change operations as evolution mappings between versions [26], and vocabulary churn versus instance-data usage has been studied as two separate time series in knowledge graphs [37]. Most directly, Tomczak et al. showed that Gene Ontology evolution changes the interpretation of biological experiments [69] — the template for this paper's downstream experiments. Within security, vocabulary instability is documented for CVE lifecycle states [31], for CVE-CWE-CPE abstraction-ladder mappings [32], for CVSS score fragmentation across versions [39], and for NVD data quality generally [25].

**The gap.** The field has the diff and lacks the measurement. MITRE publishes change enumeration [34]; CTID publishes affected-mapping flags [5]; the SoK names temporal instability as an open problem [63]. Nobody has measured what a release costs an analytic built on the previous one, and no quality framework names the vocabulary as a quality-bearing property.

## 4. Problem Formalization and Drift Taxonomy

### 4.1 Setup

Let $V$ index the published releases of an ATT&CK domain, ordered by publication date. A release $V$ determines a label space $\mathcal{L}_V$, the set of technique identifiers live in that release, together with an *intension* map $\iota_V : \mathcal{L}_V \to \mathcal{D}$ assigning to each identifier the description, tactic assignment, platform set and detection guidance that define what the identifier denotes. A CTI analytic is a function $f : \mathcal{X} \to 2^{\mathcal{L}_V}$ from evidence — a report, a telemetry window, an incident — to a set of technique labels. A CTI artefact is a pair $(A, V)$ where $A \subseteq \mathcal{L}_V$ is a label set and $V$ is the release whose vocabulary it uses. In deployed practice, $V$ is almost never recorded (Table 12), so what circulates is $A$ alone.

Two artefacts are *comparable* when they are expressed in the same label space under the same intension map. Two results are *comparable* when the analytics that produced them are. This is not a strong requirement; it is the ordinary requirement that measurements reported in the same units be reported in the same units.

### 4.2 Why this is not concept drift

Concept drift is defined over a fixed label space. In the standard taxonomy, drift is a change in the joint distribution $P_t(X, Y)$ decomposed into covariate shift, prior-probability shift and real concept drift, all with $\mathcal{Y}$ held constant [33]. The security instruments built on that definition inherit the assumption: temporal splits control when samples were drawn [67], drift detectors compare feature-space distances against a reference distribution [22], and conformal rejection calibrates non-conformity scores against a known class set [70]. The catalogue of security-ML pitfalls contains no entry for a label space that changes between the training corpus and the evaluation corpus [35], because at the time it was written no security label space was expected to.

Class-incremental learning relaxes the assumption in one direction only: classes are added, and previously learned classes retain their meaning [24]. That covers ATT&CK's additions and nothing else. The only formalism that comes close is continual learning with evolving class ontologies, which explicitly models the case where old data is relabelled under a refined class structure [43]. Even that assumes the refinement is known, typed and complete. In ATT&CK it is partially typed, occasionally lossy, and — for the component that matters most — entirely unrecorded.

The distinction that matters is this. Concept drift moves the data under a fixed ruler. Ontology drift moves the ruler. A model that is perfectly robust to concept drift, retrained continuously, conformally calibrated and deployed under a rigorous time-aware split, will still produce an incomparable number if its label space changed and it did not say so. Robustness is not the remedy, because the failure is not in the model's predictions but in the interpretation of its outputs.

### 4.3 Six drift operators

We type ontology drift by the operators that transform $(\mathcal{L}_V, \iota_V)$ into $(\mathcal{L}_W, \iota_W)$ for $W > V$.

**O1. Addition.** $\ell \in \mathcal{L}_W \setminus \mathcal{L}_V$ with no predecessor. This is the only operator that is genuinely benign for backward comparison and the only one the class-incremental literature handles [24]. It is not benign for forward comparison: a coverage denominator that grows makes a frozen capability's percentage fall without any change in the capability, which is the mechanism behind Table 8.

**O2. Deprecation.** $\ell \in \mathcal{L}_V \setminus \mathcal{L}_W$ with no successor. The concept is withdrawn. ATT&CK marks these and retains the object [1]. A pipeline that filters retired objects will drop such a label; a pipeline that does not will silently carry a dead term.

**O3. Revocation with a typed successor.** $\ell \in \mathcal{L}_V \setminus \mathcal{L}_W$ with a `revoked-by` edge to some $\ell' \in \mathcal{L}_W$. This is the well-handled case and the one the ecosystem's defence rests on. In our corpus every revoked Enterprise identifier resolves to a live identifier through the published revocation graph (Table 3). The relation is a total function into the live label space.

**O4. Re-cut.** A concept is split across several successors, or several concepts are merged into one. Because `revoked-by` is a function and never one-to-many, a split is representable only as a set of many-to-one merges onto the narrowest survivor. The relation can express the v19 re-cut — it is simply not true that it cannot — and the defect is not expressiveness but annotation: the merge is unlabelled, so a consumer applying the crosswalk mechanically cannot distinguish an exact successor from a narrowing. Ontology engineering solved this decades ago by splitting the successor relation into exact and inexact variants [54], and by typing complex change operations — merge, split, move, substitute — as first-class evolution mappings [26]. ATT&CK has one untyped relation where the literature specifies at least two.

**O5. Cross-layer reassignment.** A concept moves between levels of the ontology: a technique becomes a sub-technique, a sub-technique is promoted to a technique, or a technique is promoted to a tactic. In the current Enterprise bundle the large majority of revocation edges demote a top-level technique onto a sub-technique, and a small number promote in the opposite direction; the crosswalk carries no abstraction-level annotation, so a consumer cannot detect that the granularity of its assertion has changed. The v19 promotion of a technique concept to a tactic is not representable at all, because `revoked-by` cannot point a technique at a tactic. Tactic reassignment at the instance level is also unsignalled: 198 identifier-stable techniques changed their tactic assignment in a single transition (Table 2), and tactic objects carry no revocation edges.

**O6. Intensional rewriting.** $\ell \in \mathcal{L}_V \cap \mathcal{L}_W$ with $\iota_V(\ell) \neq \iota_W(\ell)$. The identifier survives; what it denotes moves. This operator is invisible to every identifier-based mechanism in the ecosystem, including the crosswalk, the retired-object filter and the layer-version stamp. It is the operator our downstream analysis cannot repair and the one Section 6 shows never stops.

### 4.4 Referential and intensional drift; signalled and unsignalled

O1-O5 are *referential*: they change which identifiers exist and how they correspond across releases. O6 is *intensional*: it changes what a surviving identifier means. The distinction is the paper's organizing axis, because the two components have different dynamics (Section 6), different downstream consequences (Section 7) and different repair prospects (Section 8).

Cutting across that is a second distinction we consider more practically important. Call a drift operator *signalled* if the published artefact carries a machine-readable marker that a consumer can test for. O2 and O3 are signalled: deprecation flags and revocation edges are explicit and reliable. O4 and O5 are *partially* signalled: the edges exist but carry no type, so the consumer learns that something changed and not what. O6 is *unsignalled*. ATT&CK's object version field is the only candidate marker, and as a detector of description change it has precision 0.447 and recall 0.641 (Section 6.3, Table 13). A detector at that operating point is not a detector; a consumer who trusts it will both miss a third of real rewrites and chase a majority of false alarms.

This is the sharpest statement of the paper's thesis. The component of ontology drift that is well handled is the component everybody points at, and the component that is not handled at all is the component nobody can see.

### 4.5 The two-clock model

Drift in ATT&CK does not run at one rate. The referential clock is episodic: long quiet periods punctuated by restructuring events that re-identify a large fraction of the catalogue at once. The intensional clock is continuous: a steady rate of description and field rewriting that does not pause between restructuring events and has barely varied since 2020.

Formally, let $\sigma_V(t)$ be the fraction of a cohort of identifiers live at $V$ that remains live at time $t$, and let $\tau_V(t)$ be the fraction whose intension has substantively changed. The referential clock is characterized by $\sigma$; the intensional clock by $\tau$. Section 6 estimates both. The practical consequence is that the two clocks give opposite answers to the practitioner's question "how long is my pinned label set good for?" — infinite on identifiers for any post-2020 Enterprise cohort, and roughly eighteen months to first 10% substantive staleness. A risk model that reports only one of these is wrong in a predictable direction, and the direction depends on which one it reports.

### 4.6 Ontology drift as a threat to validity

We can now place the phenomenon in the experimental-methodology tradition. Temporal bias is the failure to respect the arrow of time when partitioning data; its control is the time-aware split [67]. Spatial bias is the failure to respect deployment base rates; its control is a realistic class ratio in the test set [67]. Sampling bias, label inaccuracy, data snooping and inappropriate baselines each have a recognized name and a recognized control [35]. Ontology drift is the failure to hold the label space fixed across the comparisons a paper makes, and it damages validity in four distinguishable ways.

*Construct validity.* The label is supposed to denote a behaviour. After O6, the same label denotes a different behaviour, so the construct the analytic measures is not the construct its labels name. A system trained on descriptions of T-something as it was defined in 2020 and evaluated against gold labels assigned under the 2026 definition is measuring the agreement of two different constructs.

*Internal validity.* After O4 or O5, a label set's cardinality and granularity change under normalization. A group whose profile contained four distinct documented behaviours can, after mechanical migration, contain three — its measured breadth falls with no change in the underlying intelligence. Any analysis that treats profile size as a feature inherits that artefact.

*External validity.* After O1, the denominator of any coverage or recall claim grows. A capability that is unchanged in the world reports a falling number, and a capability that is unchanged in the world reports a rising number if the denominator shrinks. Neither movement is about the world.

*Conclusion validity.* This is the one that matters for a journal. If the drift effect were confined to scores, the appropriate response would be an error bar. Section 7 shows it reaches conclusions: the named actor, the top-ranked mitigation, the pass/fail verdict on a coverage target.

The control for ontology drift is not a better algorithm. It is declaration plus projection: state the release, state the domain, state the bundle hash, and project both sides of any cross-time comparison onto one reference release with a published residual. Section 10 gives the contract; Sections 8 and 11 state precisely how far it goes and where it stops.

### 4.7 What a valid measurement of drift requires

Because drift is a threat to validity, a study of drift is unusually exposed to its own subject matter. We commit in advance to four design requirements, each of which Section 11 audits against the delivered study.

**R1. Fixed labelling process across conditions.** The contrast that identifies a drift effect must hold constant everything except the vocabulary. If conditions differ in what was observed as well as in how it is labelled, the contrast is confounded with intelligence content.

**R2. A stated noise model.** Holding the labelling process fixed at a noise level of zero establishes separability and says nothing about additivity. A study claiming additivity must vary the noise rate and show the effect at more than one level.

**R3. A declared closure boundary.** If observation, profile, ground truth and the migration map all derive from one curator, the absolute levels are internal-consistency scores and must never be reported as task performance.

**R4. A named falsifier.** The study must state what evidence would overturn it.

## 5. Data and Methodology

### 5.1 Corpus

We build a normalized relational corpus from the published ATT&CK STIX bundles for all three domains. Release-level analyses use the first release of each major version; the deployed-corpus validity analysis in Section 9 uses every published release, including patch releases, so that a corpus can be dated against the finest available grid.

**Table 1.** The release corpus.

| Domain | Releases analysed (major / all) | First | Last |
|---|---|---|---|
| Enterprise | 19 / 41 | v1.0 (2018-01-17) | v19.0 (2026-04-28) |
| Mobile | 19 / 38 | v1.0 (2018-01-17) | v19.0 (2026-04-28) |
| Ics | 12 / 27 | v8.0 (2020-10-27) | v19.0 (2026-04-28) |

### 5.2 Measurements

Seven measurement families support the argument. **E1** computes per-release churn: live technique count, additions, revocations, deprecations, renames, description and detection rewrites, tactic reassignments, identifier-set Jaccard and group-technique edge deltas. **E2** computes identifier survival from each source release forward to v19.0, together with recoverability through the transitive closure of the revocation graph and an identifier half-life. **E3** restricts attention to identifier-stable techniques and measures intensional drift by token Jaccard over descriptions. **E4** decomposes each newly added group-technique edge into genuine new intelligence, an edge to a newly added technique, a sub-technique refinement of an existing edge, or a re-mapping forced by a revocation. **E5** is the controlled attribution experiment. **E6** is the frozen-capability coverage experiment, with a prevalence-weighted variant. **E7** dates four deployed CTI corpora against every published release and measures label validity. **E10** re-runs the attribution and mitigation-ranking analyses at the level of conclusions rather than scores. Auxiliary analyses cover version-metadata reliability, the v19 revocation wave, the tactic layer, noise injection and stratification, and corpus integrity.

### 5.3 The attribution design and its contrast logic

The attribution experiment is the load-bearing design, so we state it precisely. Fix a modern release $W$ = v19.0 and a legacy release $V$. Take the set of threat groups documented at $W$ with their technique profiles. For each trial, sample a group and draw $k = 10$ observed techniques from its modern profile. Then back-project each observed technique into $\mathcal{L}_V$: use the pre-revocation identifier where one exists, use the surviving ancestor where the sub-technique did not yet exist, and drop where no $V$-era ancestor exists. This produces a $V$-vocabulary observation of a $W$-era intrusion.

Four conditions score that observation against candidate profiles. **Back-projected** (labelled *contemporaneous* in our released code and tables) scores the $V$-vocabulary observation against $V$-vocabulary profiles — self-consistent, no vocabulary mismatch. **Naive** scores the $V$-vocabulary observation directly against $W$-vocabulary profiles — the analyst who ignores drift. **ATT&CK-Norm** applies the normalization protocol of Section 8 to the observation before scoring against $W$ profiles. **Oracle** scores the original $W$-vocabulary observation against $W$ profiles — the upper bound.

The *drift penalty* is the back-projected accuracy minus the naive accuracy, and *recovery* is the fraction of that penalty that normalization returns. Every condition consumes the same underlying intelligence content and the same draws, which satisfies R1: the contrast cannot be explained by a difference in what was observed. Because all four conditions draw their labels from the same curator's data, inter-labeller noise is identically zero in all of them and therefore cancels in the contrast. Section 7.2 varies it.

Robustness is assessed across three scoring functions (IDF-weighted cosine, Jaccard, overlap) and two profile definitions (direct group-technique edges, and edges mediated through software the group is documented as using), reported in Table 7.

### 5.4 Evidence discipline

This paper's subject is the reliability of what artefacts declare about themselves, so we state our own evidence tiers. **Tier A** covers our own measurements over the ATT&CK bundles and the repository artefacts we read in full; these are stated plainly and reproduced by the released code. **Tier B** covers secondary literature reached in this environment only through search summaries, because the egress path blocks publisher sites and preprint servers; every Tier B claim is attributed as reported, and no verbatim quotation is asserted from a source we did not read in full. **Tier C** covers audited absences — the claim that no CTI quality framework names vocabulary versioning as a dimension is Tier C, stated with the bound of the search that found it and never upgraded to a proof. Section 11.6 reports what this cost.

## 6. Measuring Ontology Drift in ATT&CK

### 6.1 The referential clock is episodic

**Figure 1.** Live technique count over the release history, with per-release additions, revocations and description rewrites.

**Table 2.** Per-release churn, ATT&CK Enterprise.

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

One transition dominates. At v6.0 to v7.0 the identifier-set Jaccard is 0.222, with 302 techniques added, 129 revoked and 11 deprecated, and 750 group-technique edges removed against 1,235 added in a single release. Nothing else in the Enterprise history is within a factor of three of that dislocation on any column.

**Figure 2.** Identifier survival curves by source release, with recoverability at the newest release.

**Table 3.** Identifier survival and half-life to v19.0.

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

The pre-restructuring cohorts lose most of their identifiers, with half-lives of 0.4 to 2.2 years, and every one of those half-lives lands on the same release. Every cohort from v7.0 onward retains at least 0.970 of its identifiers to the present and none reaches a half-life at all. In the `Recoverable` column, the count equals the revoked count in every row: every revoked identifier in the corpus resolves to a live identifier through the published revocation graph. This is the concession, and we make it in the results rather than in a footnote. On identifiers alone, and for Enterprise alone, the position that drift is solved bookkeeping is correct.

It is not correct for Enterprise alone. The same analysis over Mobile finds a 2018 transition with an identifier-set Jaccard of 0.000 in which 76 techniques vanish with no tombstone and no successor, none of them recoverable through the revocation graph — a wholesale renumbering that is more destructive than the Enterprise restructuring and predates it by eighteen months. ICS is undergoing its own sub-technique restructuring in the current release, six years after Enterprise, with all of its remappings recoverable. Counting transitions with identifier Jaccard below 0.80 across all three domains gives five events in eight years, a hazard of 0.106 per major transition, or roughly one restructuring somewhere in ATT&CK every 1.5 calendar years. The 2020 event is a draw from a live hazard, not a closed wound, and a consumer cannot time-hedge against it: across seventeen lagged release pairs, the best leading indicator of the next transition's revocation rate reaches a Spearman correlation of +0.377 with a permutation p-value of 0.134, and the techniques that were revoked at v7.0 had been *edited less* in the preceding release than those that survived. Restructuring waves are not forecastable from the public bundles. That negative result is load-bearing for Section 10: the protocol must be standing, not triggered.

### 6.2 The intensional clock is continuous

**Figure 3.** Silent semantic drift among identifier-stable techniques.

**Table 4.** Semantic drift among identifier-stable techniques, measured to v19.0.

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

Read this table as a decay curve rather than as a ranking. Every row measures the same endpoint, so the rows differ in elapsed time. The v7.0 cohort has had six years and 0.749 of its identifier-stable techniques have edited descriptions, with 0.386 substantially rewritten at a token Jaccard below 0.8. The v11.0 cohort has had four years: 0.465 edited, 0.208 substantially rewritten. The v15.0 cohort has had two: 0.275 edited, 0.087 substantially rewritten. Fitting a staleness clock to those cohorts gives a first-10%-substantive-staleness time of roughly 1.5 years and a semantic half-life of 4.5 to 6.1 years, and the per-cohort figures do not trend downward across the post-2020 era. Critically, the text-only variant of that clock — excluding tactic changes and revocations entirely, so it cannot be attributed to the v19 re-cut — gives essentially the same answer.

Set this against Table 3. For any post-2020 Enterprise cohort the identifier half-life is never reached, while the semantic half-life is about five years and the first 10% of substantive rewriting arrives in about eighteen months. Those are the two clocks, and they answer the practitioner's question in opposite directions.

Table 2 also records an event that no identifier-based diff would surface: the v17.0-to-v18.0 transition rewrote the detection field of 583 surviving techniques against only 49 description edits. A defender whose detection engineering is keyed to ATT&CK's detection guidance had its entire reference text replaced in one release, at an identifier-set Jaccard of 0.983.

### 6.3 The signal that is not a signal

The obvious reply is that a consumer should watch ATT&CK's own object version field. We tested it as a detector.

**Table 13.** Text change versus version increment, identifier-stable Enterprise techniques.

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

Across 8,359 carried-over technique pairs, 1,358 had their description rewritten — 0.162 of the total. Of those, 487 (0.359) carried no version increment at all, while 1,077 version increments carried no text change whatsoever. As a detector of description change, the version field has precision 0.447 and recall 0.641. MITRE's own tooling knows this: `diffStix` defines a change class specifically for objects patched while their version stayed the same, and its documentation acknowledges that unintended version changes exist in earlier releases [34, 48]. The tool that computes the diff can see intensional drift. The consumer-facing contract, which offers a live/retired filter and a revocation resolver [1], cannot express it. The gap between those two artefacts is architectural rather than accidental, and it is the cleanest available evidence that O6 is unsignalled by design rather than by neglect.

### 6.4 Growth decomposition: how much is intelligence?

The query asks what fraction of apparent growth in a CTI knowledge base is genuine new adversary intelligence versus ontology bookkeeping. We answer it on the group-technique edge, the atom of "we have learned that this actor does this".

**Figure 4.** Per-transition decomposition of new edges for pre-existing groups.

**Table 5.** Knowledge-growth decomposition, ATT&CK Enterprise.

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

Across all Enterprise transitions, 5,516 group-technique edges were added, of which 2,442 belong to groups newly added to ATT&CK. Of the 3,074 added for groups that already existed, 1,752 are genuine new intelligence, 330 are edges to newly added techniques, 487 are sub-technique refinements of an assertion already present, and 505 are re-mappings forced by a revocation. The bookkeeping share is 992 of 3,074, or 0.323.

The distribution matters more than the aggregate. The restructuring transition is 0.750 bookkeeping. But so is the most recent transition, at 0.470, and two ordinary mid-decade transitions run at 0.380 and 0.340. Bookkeeping bursts are not confined to restructuring events. An analyst measuring "how fast is our knowledge of this actor growing" from release-to-release edge counts — which is what a growth curve over ATT&CK measures — will attribute roughly a third of the observed growth to intelligence that was never acquired. This is an independent argument against treating ATT&CK edge counts as a knowledge-accumulation time series, and it parallels the distinction between vocabulary churn and instance-data usage that the knowledge-graph literature draws explicitly [37].

### 6.5 The most recent wave

The v19 transition deserves separate treatment because it is the ecosystem's live test case and because the industry narrative around it is one of rapid, unproblematic migration [78]. Between v18.1 and v19.2, 17 live techniques were revoked, including the whole T1562 family. On the v18.1 graph this touches 84 group-technique edges, 155 software-technique edges, 47 mitigations and 17 detection relationships, and 52 of 168 group profiles lose at least one identifier. One of the revoked identifiers, T1562.001, was ranked 33 of 599 techniques by documented `uses` edges in the release it left. This is not long-tail churn.

The structural move is the one the crosswalk cannot carry. The concept *Impair Defenses* was promoted from a technique to a tactic. Because a revocation edge cannot point a technique at a tactic, the parent technique was instead revoked onto one of its own former children, while the remaining children fanned out across six other successors. At the same time the tactic identifier TA0005 was recycled in place, keeping its identifier while its name and referent changed, and no revocation edge exists on any tactic object. In the same transition, 198 identifier-stable live techniques changed their tactic assignment (Table 2). An analytic that joins on tactic identifiers across this boundary is comparing two different concepts with no signal, no edge and no version increment to warn it.

## 7. Downstream Impact of Drift on CTI Analytics

### 7.1 Attribution under vocabulary mismatch

**Figure 5.** Attribution accuracy by condition, with the drift penalty and confidence bands.

**Table 6.** The controlled attribution experiment, k = 10, analysis at v19.0.

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

A 2018-vocabulary artefact scored against a 2026 knowledge base loses 42.2 points [37.8, 46.8] relative to a self-consistent baseline; a 2019 artefact loses 46.2 points [41.6, 51.0]. Those are the headline numbers, and they are also the ones a reviewer should discount hardest, because they are one restructuring event seen from six different sides.

The number that survives scrutiny is 1.6 points [0.6, 2.8] for a v18.0 artefact — a single release boundary, six months of elapsed time, an era in which identifier survival exceeds 0.97, and an interval that excludes zero. That is the drift cost of being one release out of date in the current, stable, well-maintained regime. It is small in aggregate. Section 7.3 shows it is not small where it matters.

**Table 7.** Robustness across scoring functions and profile definitions.

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

The absolute accuracies move a great deal across scorers and profile definitions — overlap scoring on software-mediated profiles is a far harder task than IDF-cosine on direct edges. The sign and the ordering of the drift penalty do not: it is large and positive in every pre-restructuring cell and small and positive in every post-restructuring cell. Drift is not an artefact of one similarity function.

### 7.2 Meeting the strongest objection

The strongest published objection to everything above is not that our numbers are wrong. It is that they are irrelevant, because a much larger source of label variance already exists at a single pinned release. Virkud et al. show that detection products describing the same behaviour carry different ATT&CK labels within one pinned release, often with no overlap at all [74]. Saha et al. show that roughly a third of ATT&CK groups have any technique unique to them, so TTP attribution is weakly identifiable before drift is considered [59]. Multi-report extractor evaluation adds that a substantial share of extraction errors are between same-tactic, description-overlapping techniques [20]. Vendor fragmentation has been characterized as an echo chamber effect that any drift claim must separate itself from [68]. If a labelling process has that much synchronic variance, why should anyone care about a 1.6-point diachronic effect?

We take this objection seriously enough to make it falsifiable. It implies three testable consequences, and we tested all three.

**Separability.** The objection implies that the measured drift penalty is a re-description of the same confusability and should collapse once realistic labelling noise is present. Our design holds the labelling process fixed across conditions by construction: every condition draws from the same curated data, so the noise term is identical in all four and cancels in the contrast. That establishes separability but sets the noise rate to zero, which — as R2 in Section 4.7 anticipates — licenses separability without testing additivity. An interaction cannot be observed at one level of a moderator. So we ran the factorial. Each observed technique is replaced with probability $\rho$ by a sibling sub-technique, its parent, or a same-tactic technique, applied in the modern vocabulary before back-projection so that the substitution flows identically into all four conditions. At 1,200 trials per cell, the drift penalty at v1.0 moves from 0.439 at $\rho = 0$ to 0.416, 0.392 and 0.328 at $\rho = 0.1, 0.2, 0.4$; at v6.0 from 0.476 to 0.411, 0.398 and 0.312; at v12.0 it is 0.017, 0.023, 0.018, 0.014; at v18.0 it is 0.012, 0.005, 0.011, 0.010.

The penalty survives at every noise level and at every boundary, so the first consequence of the objection is refuted. Strict additivity, however, also fails in the large-drift regime: at $\rho = 0.4$ the pre-restructuring penalties are attenuated by roughly a fifth to a third, because noise and drift consume the same finite signal. **The correct statement is that drift is separable from labelling noise and sub-additive with it, and that the noise-free figures in Table 6 are therefore upper bounds on drift's contribution in a noisy world.** We state this in the results rather than in a limitation, because it changes how the headline numbers should be read. In the modern regime the penalty is flat in $\rho$ and the additive reading holds. Normalization degrades faster than the penalty does: recovery at v1.0 falls from 0.441 at $\rho = 0$ to 0.279 at $\rho = 0.4$, so the repair protocol of Section 8 buys less as label quality falls.

**Non-identifiability.** The objection implies that the penalty is carried by the majority of groups that were never attributable, and should vanish on the identifiable subset. We stratified by whether a group has any technique unique to it within the candidate universe. The specificity fraction our corpus produces — 0.325 at v12.0, 0.309 at v16.0, 0.298 at v18.0 — independently reproduces the published figure [59], which is a useful check that we are measuring the same property. The drift penalty on the stratum with a unique technique is 0.0344 [0.0101, 0.0607] at v12.0, 0.0331 [0.0166, 0.0497] at v16.0 and 0.0239 [0.0109, 0.0391] at v18.0. On the stratum without one it is 0.0089, 0.0049 and 0.0067, with confidence intervals touching or crossing zero at two of three versions.

The second consequence of the objection is refuted in the opposite direction from what it predicts. In the modern regime the drift penalty is two-and-a-half to seven times *larger* on the identifiable groups than on the non-identifiable ones. The mechanism is transparent once stated: a group's identifying token is by definition a rare technique, and rare techniques are exactly the ones ATT&CK adds, splits, refines and revokes. Drift attacks the signal that attribution depends on. A small average over a population that is mostly non-identifiable conceals a material effect on the subset that carries the task.

**Wrong unit.** The third consequence — that the study measures a quantity that does not exist in the field, because real labelling happens on independently observed incidents rather than inside one curator's graph — is not refuted. It is conceded, and Section 11.1 treats it as the study's central residual threat.

The scoping statement we are entitled to is therefore precise. Noise bounds the *absolute* accuracy of TTP attribution and our design does not claim otherwise; every figure in Table 6 is an internal-consistency score, and the contemporaneous baselines sitting between 0.62 and 0.86 rather than near 1.0 are where non-identifiability has already been absorbed. Drift bounds *comparability across time*, which is a different quantity, and it is additive on top of the noise floor in the modern regime and sub-additive in the pre-restructuring regime.

### 7.3 Conclusions, not scores

Score movements are a hygiene complaint. The Gene Ontology precedent sets a higher bar: show that the conclusions move [69].

**Figure 8.** Attribution verdict instability and mitigation leaderboard reordering.

**Table 10.** Attribution verdict instability.

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

For a v1.0 artefact the named actor changes in 0.722 of observations and changes to a *wrong* actor in 0.712; for v6.0 the figures are 0.790 and 0.774. Across a single modern release boundary the named actor still changes in 0.022 of observations, and in that regime essentially every change is a change to a wrong actor. These are not score deltas. They are different answers to the question the analysis was run to answer.

The final column is the one a research-integrity reviewer should notice. Applying normalization *itself* changes the verdict in 0.368 to 0.442 of trials for pre-restructuring artefacts and in 0.006 to 0.030 for modern ones. A repair that silently changes the answer in two-fifths of cases is not a neutral preprocessing step, and applying it without declaring it is itself a reporting failure.

**Table 11.** Mitigation leaderboard reordering under a frozen portfolio.

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

A mitigation leaderboard is a budget document: it says which control to fund first. Frozen at v6.0 the naive ranking has Kendall's tau of 0.665 against the correct ranking, three members displaced from the top ten, and a changed rank-1. Normalization repairs this well, raising tau to 0.968. But the modern rows carry the sting: at v16.0 and v17.0 the rank correlation is 0.976 to 0.977 — nearly perfect — and the top-ranked mitigation *still changes*. A high rank correlation is not a guarantee about the decision the ranking is used to make, because the decision depends on the head of the distribution and the correlation is dominated by the tail.

### 7.4 Coverage claims under a frozen capability

**Figure 6.** Coverage claims under a frozen capability, and the random-portfolio sweep.

**Table 8.** Coverage claims under a frozen capability, re-measured at v19.0.

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

The capability does not change. Only the ontology does. A portfolio that claimed 97.0% coverage at v6.0 measures 17.4% naively at v19.0 and 33.9% after normalization; the 16.5-point gap between those two is pure identifier artefact, and the remaining fall is denominator growth under O1. A portfolio frozen at v18.0, one release ago, claimed 84.2% and measures 81.1% naively, with a 2.2-point identifier artefact. Every published ATT&CK coverage percentage is therefore a function of two things: the capability, and the release against which it was computed. The literature has already established that coverage is not comparable across products at a fixed version [74, 46, 62] and that the denominator is contested [64, 84]. Table 8 establishes that it is not comparable across versions for a fixed product, which is the complementary half and the one that bites an organization tracking its own coverage trend over time.

**The long-tail objection.** MITRE's own bias work documents that observed telemetry is dominated by a short head of techniques [49], which suggests that churn among rare identifiers should barely move any frequency-weighted number. We repeated the frozen-capability experiment with techniques weighted by documented prevalence. The artefact gets *larger*, not smaller: at v6.0 it is +16.50 points unweighted and +20.01 points prevalence-weighted. In the modern regime the two converge — +1.58 versus +1.43 at v10.0, +2.15 versus +1.57 at v18.0 — so the weighting neither creates nor destroys the modern effect. Documented prevalence at v19.0 is only moderately head-heavy: the fifteen most-referenced techniques carry 0.285 of all `uses` edges. And Section 6.5 already established that the most recent revocation wave took a technique ranked 33 of 599 by that measure.

The objection is refuted on documentation prevalence. It is *not* refuted on telemetry prevalence, and the distinction is real rather than rhetorical: documented `uses` edges count how many groups, malware families and tools MITRE has recorded as using a technique — a cumulative, monotone stock biased toward behaviours that are easy to narrate in a report — whereas sightings telemetry measures a flow of defender alerts over a window and is materially more concentrated [49]. The sightings data is not reachable in this environment. We therefore claim that the long-tail objection fails for the fraction of the *written CTI corpus* affected by drift, and we leave it untested for the fraction of the *alert stream* affected. Section 11.3 restates this as a limitation rather than a result.

## 8. ATT&CK-Norm: A Version-Normalization Protocol

ATT&CK-Norm is the projection half of the control proposed in Section 4.6. Given a label set $A \subseteq \mathcal{L}_V$ and a target release $W$, it resolves each identifier by: (1) following the transitive closure of `revoked-by` to a live identifier in $W$; (2) keeping identifiers already live in $W$; (3) optionally rolling an unresolvable sub-technique up to its parent; and (4) dropping identifiers absent from $W$. It is intentionally trivial. Its value is not algorithmic novelty — alias resolution and label normalization have prior art in malware labelling [19] and the crosswalk it consumes is MITRE's own — but as a reference implementation against which the *limits* of identifier repair can be measured.

Three of those limits are results.

**Roll-up is a dead branch.** We re-ran the attribution experiment with roll-up enabled and disabled as the only difference across 54 conditions and 27,000 trials. Top-1 accuracy is identical to three decimals in every condition, and the paired bootstrap confidence interval on the difference is [+0.000, +0.000]. Auditing the branch directly on archival group profiles across all major releases and on all four deployed CTI corpora, a broader sweep finds three firings in 12,027 resolutions across every domain and major release. The reason is structural: MITRE never orphans a sub-technique — a revoked sub-technique always resolves to a live target — and deprecations without a successor are top-level, so roll-up's precondition essentially does not arise in ATT&CK's data. The correct default is therefore to drop and count, not because drop wins a measured contest but because roll-up wins nothing measurable while adding a code path that can fabricate a parent-level assertion the source never made. We ship it disabled and flag-gated.

**The protocol must return a residual, not a set.** The current Enterprise crosswalk has 149 revocation edges, of which eight targets are many-to-one, absorbing twenty predecessor identifiers; the largest absorbs five. A set-valued protocol cannot distinguish a clean ten-identifier migration from one where three identifiers merged and two were dropped, because both return a set. On real corpora this is not hypothetical: TRAM's bootstrap label set goes from 537 to 503 distinct live classes under normalization, with 0.1475 of its 25,770 label instances landing in a merged class; rcATT goes from 215 to 199 with 0.0937 of its 6,235 instances merged. A benchmark whose class count silently collapses by 34 is not the same benchmark. We therefore redefine the protocol's return type as a ledger — kept, merged, dropped, demoted — and treat an unreported residual as a reporting failure. The crosswalk also performs unannounced abstraction changes: of the 149 edges, 119 demote a top-level technique onto a sub-technique and seven promote a sub-technique to a parent, with no abstraction-level annotation for a consumer to test.

**A defensible-looking wrong answer.** The v19 T1562 collapse is the cleanest counter-example. At the prior release, T1562 was a top-level technique with twelve children spanning firewall modification, cloud log tampering, command-history manipulation, safe-mode boot and downgrade attacks, and three documented groups assert the generic parent — the standard CTI convention for "the report says defenses were impaired but does not say how". After v19, normalizing the parent identifier resolves in one hop to a live identifier, reports full success and drops nothing. The answer is wrong: an analyst who wrote the parent because a report said the actor disabled the host firewall is now recorded as asserting that the actor tampered with security tooling — a strictly narrower and factually different claim, in a tactic that did not exist when the artefact was written. One group whose profile asserted four identifiers in that family normalizes to three, so its measured technique breadth falls by one as pure bookkeeping. This is the O4/O5 defect of Section 4.3 made concrete, and no amount of identifier arithmetic fixes it, because the crosswalk is doing exactly what it was specified to do.

**What it buys, honestly.** On pre-restructuring artefacts, normalization recovers 0.42 to 0.53 of the attribution penalty (Table 6) — a mean top-1 gain of about twenty points. Post-restructuring, the mean gain is under one point and its 95% confidence interval includes zero in roughly two-thirds of conditions. Where it works cleanly is coverage ranking: mean Kendall's tau rises from 0.931 to 0.992 across the conditions of Table 11, three of four naive rank-1 flips vanish and none is introduced. And it is blind to intension by construction: across the release that dissolved the field's most-used tactic, normalization returns all 674 identifier-stable techniques unchanged — zero drift signalled — while 198 of them changed tactic and 41 changed their description hash.

ATT&CK-Norm is therefore a bounded legacy-migration tool, not a cure. It restores identifier comparability on old artefacts and buys almost nothing modern. Any paper claiming that normalization restores comparability is repeating the error this paper set out to diagnose.

## 9. Label Validity of Deployed CTI Corpora

If drift were a theoretical hazard, the deployed corpora would show little of it. We dated four widely used CTI label sets against every published ATT&CK release.

**Figure 7.** Label-validity curves for four deployed CTI corpora.

**Table 9.** Label validity of deployed corpora, measured at v19.2.

| Corpus | Distinct labels | Label instances | Sub-technique labels | Best-fit release | Fit | Releases where all labels valid | Invalid today | Repairable |
|---|---|---|---|---|---|---|---|---|
| ctibench-ate | 120 | 397 | 0 | v14.0 (2023-10-31) | 0.942 | **none** | 8 (0.067) | 1 |
| rcatt | 215 | 6235 | 0 | v4.0 (2019-04-30) | 1.000 | 8 (v4.0–v6.3) | 107 (0.498) | 99 |
| tram-bootstrap | 537 | 25770 | 344 | v13.0 (2023-04-25) | 0.939 | **none** | 43 (0.080) | 43 |
| tram2 | 50 | 5143 | 24 | v8.2 (2021-01-27) | 1.000 | 18 (v8.2–v16.1) | 2 (0.040) | 2 |

Three findings follow.

**Corpora are datable, and dating them is diagnostic.** rcATT's label space fits v4.0 exactly and is simultaneously valid across eight consecutive releases spanning 2019 to early 2020 — consistent with its publication date [44] and with a repository audit finding a 2019-era flat label space [8]. It carries zero sub-technique identifiers, which is the signature of a pre-restructuring vocabulary. Today 0.498 of its distinct labels and 0.380 of its label instances are invalid. A model trained on that corpus and evaluated against modern gold labels is measuring agreement between two vocabularies, and 99 of the 107 dead labels are mechanically repairable — which means the repair is available and, judging by Table 12, not applied.

**Two corpora fit no release at all.** CTIBench-ATE and TRAM's bootstrap set have a best fit below 1.0 at every release: there is no ATT&CK version at which all their labels are simultaneously live. This is a stronger statement than "they are out of date". A corpus that fits no release was not drawn from a single release; its labels were assembled across time or across domains, and no pinning discipline applied after the fact can make it internally consistent. For a benchmark this is disqualifying for cross-version comparison, and benchmark generations that report continuity of measurement under a stable identifier [29, 13] inherit the problem from their predecessors [30].

**Not every invalidity is drift, and this cuts against us.** CTIBench-ATE shows eight labels invalid at v19.2, of which seven are recorded as unrepairable. All seven come from a single row whose platform column says Enterprise while its entire gold identifier set is Mobile-only — and all seven are live in the Mobile domain at the same release. Seven-eighths of that corpus's apparent drift damage is not drift; it is a single-version labelling error, and a normalization protocol without a domain guard would confidently report seven unrepairable deprecations and be wrong seven times. We report this because it is the strongest available counter-example to our own instrument, and because it is a design requirement: domain must be declared alongside release, and the residual ledger must distinguish withdrawn concepts from wrong-domain identifiers from scrape artefacts, since the three need opposite remedies.

**Table 12.** ATT&CK version declarations in deployed corpora.

| Corpus | Documentation files scanned | ATT&CK version declarations found |
|---|---|---|
| cti-bench | 2 | 0 |
| rcATT | 2 | 0 |
| tram | 15 | 0 |

Zero declarations across nineteen documentation files. This scan is narrow — two of the three repositories contributed only two files each — and we do not rest the adoption claim on it alone. It is corroborated on the coverage side, where the version field exists, is optional, and silently defaults to the current release [15]: six of eight sample layers shipped in MITRE's own Navigator repository carry no ATT&CK version [18], and the most widely used layer-generation tool omits the field by default while stamping its own build constant instead [79]. Independent audits of deployed TTP systems find five different ATT&CK ontologies across six systems with two declared versions between them [3], one system whose ontology is frozen as a dated HTML scrape [2], and one dataset that declares a target release while still carrying identifiers revoked five releases earlier [10]. The pattern is consistent across every part of the ecosystem we could inspect: the mechanism exists, and the field does not use it.

## 10. Discussion and Reporting Discipline for CTI Research

### 10.1 What the measurement licenses

Three claims are now supported and three are not.

Supported: ontology drift is measurable and separable from the synchronic labelling noise floor (Sections 6, 7.2); it changes conclusions and not merely scores (Section 7.3); and the mechanism that would repair it exists, is nearly as good as an identifier crosswalk can be, and is close to unused (Sections 8, 9).

Not supported, and we will not say them. Not that `revoked-by` cannot express the v19 re-cut — it can, as merges, and the defect is that merging is lossy and unannounced. Not that normalization restores comparability — it restores identifier comparability on legacy artefacts and buys almost nothing modern. Not that ATT&CK is unstable — post-2020 Enterprise identifiers are remarkably stable, and the instability is in meaning, in the tactic layer, and in other domains. And not any absolute attribution accuracy as a statement about attribution, for the reasons in Section 11.1.

### 10.2 A four-line reporting contract

The control for ontology drift is declaration plus projection. We state it as something a reviewer can check in under a minute rather than as a framework.

*For a CTI paper or dataset.* (1) The ATT&CK domain, the exact release, and the SHA-256 of the STIX bundle — in the artefact, not in the prose. (2) Whether identifiers were normalized, and to which target release. (3) The residual ledger: kept, merged, dropped and demoted counts, with the dropped identifiers listed verbatim. (4) For any cross-time comparison, a statement that both sides were projected onto one reference release. The engineering cost is a JSON header, a table, and on the order of thirty lines of code. The real cost is reputational: a residual line makes label decay public, and for one of the corpora in Table 9 that line would read 0.498 of identifiers and 0.380 of label instances invalid today.

*For a benchmark, additionally.* (5) The label granularity policy — parent-only or mixed — and the class count before and after normalization, because a benchmark whose classes silently collapse from 537 to 503 is not the same benchmark. (6) A continuous-integration re-validation script that fails when any gold label is not live in the declared release. The cost is a standing maintenance obligation and the loss of cross-release score comparability by default, which is the point rather than a side effect. Benchmarks that have moved to live-API evaluation are pursuing the same objective by a different route [13], and work quantifying answer-key decay in static benchmarks supplies the general argument [75].

*For a vendor coverage claim, additionally.* (7) The ATT&CK release and the denominator — the count of live techniques in that release — printed next to the percentage. (8) The claim restated against the current release, or explicitly marked as-of. The cost is that coverage percentages become non-monotone in public. Given Table 8 and the existing critique of coverage denominators [64, 82, 84], that is a feature.

Because restructuring waves are not forecastable one release ahead (Section 6.1), this discipline must be standing rather than triggered by an observed revocation. There is no early-warning signal to wait for.

### 10.3 What MITRE could port, and from where

None of the following is invented here; all of it is standard practice in ontology engineering and would be a port rather than a research programme.

A two-tier successor vocabulary, distinguishing exact successors from inexact ones as OBO Foundry Principle 19 specifies [54], would let a split be expressed as several inexact pointers instead of one misleading exact one. A controlled obsolescence-reason vocabulary — superseded-by-split, merged, re-scoped, promoted-to-tactic, out-of-scope — would make drop and merge distinguishable, which today they are not. Making retirement visible in the human-readable label, as OBO does with a mandatory prefix, would stop tools that join on name from silently working against a dead concept. Referent stability at a stable identifier is the principle that renaming a tactic in place violates: a changed referent requires a new identifier [53, 54]. Prior-version and backward-compatibility links on the release collection object are standard OWL vocabulary [57] and ATT&CK has neither, so lineage is reconstructed by sorting release names. And publishing the evolution mapping as a first-class versioned artefact typed with complex change operations — merge, split, move, substitute — is exactly what COnto-Diff specifies [26]; `diffStix` already computes the underlying operations [34, 48], and typing them is what would make the bookkeeping-versus-intelligence split of Table 5 computable rather than asserted. Finally, making the Navigator layer's ATT&CK version field mandatory rather than optional [15] would close the single largest adoption gap we measured.

### 10.4 The missing quality dimension

CTI quality frameworks enumerate accuracy, completeness, timeliness, relevance, provenance and interoperability [60, 76, 27], and quality-assurance practice studies describe what teams actually do [40]. Across the sources we could reach, none defines a dimension over the reference vocabulary — which release the intelligence is expressed in, and whether that release is declared. We state this as an audited absence over a bounded search, not as a proof of non-existence. We propose *vocabulary currency* as the missing dimension, operationalized by exactly the four lines of Section 10.2 and measurable, for any corpus, by the label-validity analysis of Section 9. It is a quality property in the ordinary sense: it is a property of the artefact, it is checkable without access to the producer, and it degrades predictably with time at a rate this paper estimates.

### 10.5 What an SCI-level contribution here must demonstrate

The query asks this directly, so we answer it directly. Naming drift is not enough: the SoK already flags temporal instability [63] and MITRE already publishes the diff [34]. Counting churn is not enough either; anyone can run `diffStix`. The bar, set by the Gene Ontology precedent [69], has four parts. A contribution must (i) formalize the phenomenon in a way that distinguishes it from concept drift rather than subsuming it, (ii) measure it longitudinally over the full published release history rather than at selected boundaries, (iii) demonstrate that it changes *conclusions* under a design that holds the labelling process fixed, so the effect is not a re-description of known synchronic noise [74, 59], and (iv) state honestly what the proposed repair cannot do. A paper that does (i) through (iii) and skips (iv) has produced a tool paper with an inflated claim. This is why Section 11 is long.

## 11. Threats to Validity

This paper argues that CTI research under-reports the limits of its own instruments. It would be absurd to make that argument and then under-report ours. What follows is ordered by severity as we assess it, and the first item is the one we would attack first if we were reviewing this paper.

### 11.1 The closed ATT&CK-internal loop

The attribution experiment is a closed loop. The observations, the candidate profiles, the ground-truth group assignment and the back-projection map all derive from a single curator's knowledge base. Nothing in the design is an independent measurement of an intrusion.

Three consequences follow and we accept all of them.

*The absolute accuracies are not attribution performance.* The values between 0.62 and 0.86 in Table 6 are internal-consistency scores: they measure how reliably a sample drawn from a group's documented profile identifies that group within its own graph. They must never be cited as evidence that TTP attribution works at that rate, and no claim in this paper depends on their level — only on differences between conditions that share the loop.

*The self-consistent baseline is a reconstruction, not a historical system.* The condition our released code and Table 6 label *contemporaneous* is a back-projection: 2026 intelligence transcribed into an earlier vocabulary, not a system as it existed in that year. We ran the missing archival cell — real archival profiles scored against real archival observations in the era's own vocabulary — and it gives 0.969 at v1.0 against the back-projection's 0.668. The gap is a collision artefact: dense modern profiles collapsed onto a coarse vocabulary collide with one another in a way no 2018 system experienced, because 2018 profiles were sparse. This matters for the sign of our bias. Two biases run in opposite directions — the collision effect depresses the self-consistent baseline and therefore *deflates* the reported penalty, while the construction guaranteeing that observed techniques are drawn from the true profile is a perfect-recall idealization that *inflates* it. The measured net at the pre-restructuring boundaries is downward, so the pre-restructuring penalties are conservative. In the modern regime the two constructions converge (0.837 versus 0.856 at v12.0; 0.841 versus 0.846 at v18.0), so the modern headline is unaffected. We nonetheless consider the condition misnamed, and the fix — rename to *back-projected* and publish the archival cell as a diagnostic — is adopted in the released artefacts even though Table 6 retains the original column header for consistency with the released results files.

*Real archival artefacts do worse than the reconstruction.* A partially open-loop condition, scoring genuine archival group profiles against the modern knowledge base, reaches 0.159 at v1.0 against the back-projection's 0.231. Opening the loop costs accuracy rather than gaining it, which is evidence that the closed loop is, if anything, generous to the systems it evaluates.

The experiment that would close this threat is the one the field does not have: a double-labelled incident corpus in which two independent analysts label the same intrusions under two ATT&CK releases, yielding the drift term and the inter-analyst term simultaneously and from outside the curator's own edges. We searched for one and did not find a public instance. Until such a corpus exists, the honest status of our attribution result is *a lower bound on the incomparability induced by vocabulary change inside a maximally favourable, internally consistent setting*.

### 11.2 The headline penalties are upper bounds

Section 7.2 already states this in the results, and we restate it here because it is a limitation and belongs in both places. The conditions in Table 6 hold labelling noise at exactly zero. Under injected Virkud-shaped labeller substitution the pre-restructuring penalty attenuates by roughly a fifth to a third at $\rho = 0.4$ — from 0.439 to 0.328 at v1.0 and from 0.476 to 0.312 at v6.0 — because drift and noise consume the same finite signal. The modern penalties are flat in $\rho$ and therefore additive, but the modern penalties are also the small ones. A reader should take the pre-restructuring figures as upper bounds on drift's marginal contribution in a realistically noisy world, and should take the recovery fractions as upper bounds too: normalization degrades faster than the penalty does, with recovery at v1.0 falling from 0.441 to 0.279 across the same noise sweep.

Two further idealizations inflate specific quantities. The *naive* condition is a uniform worst case: because the modern profiles are almost purely sub-technique-level while the back-projected artefact is purely parent-level, exact matching scores near zero across the restructuring boundary, whereas real legacy artefacts are mixed-granularity and would sit between *naive* and *normalized*. And the normalization function is close to the algebraic inverse of the back-projection function, since both walk the same revocation and sub-technique graphs; the reported recovery is therefore an upper bound on what normalization achieves on real label sets carrying typographical errors, cross-domain identifiers and scrape artefacts — exactly the defects Section 9 found in a deployed benchmark.

### 11.3 Documentation prevalence is not telemetry prevalence

The prevalence-weighted coverage analysis in Section 7.4 weights techniques by documented `uses` edges. These are not sightings. A `uses` edge counts how many groups, malware families and tools MITRE has documented as employing a technique: a cumulative stock over cited CTI reports, monotone in time because a 2019 edge never decays, and biased toward behaviours that are easy to narrate in a written report. Defender telemetry measures a flow over a window and is materially more concentrated [49]. Worse for us, the weight is computed from the same release whose churn is being measured, so a revoked technique carries its weight out of the corpus with it; the weighted artefact is not independent evidence in the way an external telemetry distribution would be.

The correct scope statement is therefore narrow and we hold to it. The long-tail objection is refuted for the fraction of the *written CTI corpus* affected by drift. It is untested for the fraction of the *alert stream* affected, because the telemetry that would test it on its own data is not reachable in this environment. A reader who believes the alert stream is far more concentrated than the documentation stock — and the published bias work suggests it is [49] — should discount our prevalence-weighted result accordingly. It would not change the unweighted results, the attribution results or the label-validity results.

### 11.4 Construct validity of the drift measures

Semantic drift is operationalized as token Jaccard over technique descriptions with a substantial-rewrite threshold at 0.8. Token overlap is a coarse proxy for meaning: an editorial rewrite that preserves the referent scores as drift, and a two-word change that narrows the scope of a technique may not. We chose it because it is transparent, reproducible without a model, and stable across the eight-year corpus, but a reviewer is entitled to read our intensional-drift rates as an upper bound on referent change and our substantial-rewrite rates as the more conservative of the two columns in Table 4. The direction of the resulting bias is not obvious, and we do not claim it is small.

The bookkeeping classification in Table 5 is likewise rule-based. An edge is classified as sub-technique refinement when it is a more specific child of an assertion already present for that group, and as revocation re-mapping when it follows a revocation edge. Both rules are conservative in the sense that an edge is only classified as bookkeeping when the mechanical evidence is present; an edge that is substantively a re-description but carries no crosswalk evidence is counted as genuine new intelligence. The 0.323 aggregate is therefore a lower bound on the bookkeeping share under our definitions, and it is a lower bound of a quantity whose definition is itself contestable.

The identifier half-life in Table 3 is computed on the major-release grid. A cohort that crosses a restructuring boundary has its half-life attributed to that release, which is correct but compresses the timing: the pre-restructuring cohorts' half-lives of 0.4 to 2.2 years are all measurements of the same event at different distances from it, and reading them as six independent observations of a decay process would be wrong. We report them as one event seen six times.

### 11.5 Internal inconsistency in our own change counts

Two computations of the same quantity in our own pipeline disagree, and we report the disagreement rather than silently picking one. The release-grid analysis behind Table 13 finds 1,358 description rewrites over 8,359 carried-over pairs, of which 487 carry no version increment. An independent recomputation directly from the release bundles, with a different treatment of whitespace and reference-block normalization, finds 1,366 and 494. The precision and recall figures we quote for the version field (0.447 and 0.641) are computed from the first. The discrepancy is under 0.6% and does not affect any qualitative claim, but it illustrates the paper's own thesis at an uncomfortable angle: two implementations of "did the description change?" disagree, and neither is wrong, because the question depends on a normalization choice that neither implementation declares in its output. Our reporting contract (Section 10.2) would require declaring it. We now do.

Similarly, the count of techniques changing tactic across the most recent transition is 198 on the major-release grid (Table 2) and 201 when computed between the specific patch releases at each end. Both are correct measurements of slightly different intervals. The lesson for the contract is that a release must be declared to patch-level precision, not to major version.

### 11.6 Evidence tiers and the fidelity of the secondary literature

The positioning in Section 3 rests on secondary literature that, in this environment, was reachable only through search summaries: the egress path blocks publisher sites and preprint servers. We therefore observe a strict rule and state it plainly. No verbatim quotation is asserted from any source we did not read in full; every Tier B claim is attributed as reported rather than as verified; and where a Tier B source is load-bearing for an argument, we say which part of the argument it carries. The three places where this matters most are the synchronic labelling-noise floor [74], the group-specificity fraction [59], and the multi-report extractor error analysis [20]. For the first two we have partial independent corroboration — our own stratification reproduces the specificity fraction at 0.298 to 0.325 — but for the noise floor we rely on the reported result, and our refutation of the non-separability consequence is conducted against a *model* of that noise (sibling, parent and same-tactic substitution at rate $\rho$) rather than against the measured joint distribution of vendor labels. If the real substitution structure is systematically different from our model — for instance if vendor disagreements cluster on exactly the techniques that also churn — the separability argument weakens. We flag this as the most consequential Tier B dependency in the paper.

Tier C claims are audited absences. The statement that no established CTI quality framework names vocabulary or ontology versioning as a dimension is bounded by the sources we could reach [27, 38, 40, 41, 60, 76, 11], and we state it as an absence over that bound and never as a proof. The same applies to our inability to determine whether the largest comparative extraction evaluation re-baselines its systems onto a common release before comparing; the relevant note could not be verified and no claim about it appears in the manuscript.

### 11.7 A corpus integrity incident in our own evidence pipeline

We ran an integrity check over the 112 structured evidence notes accumulated during this study, comparing each note's declared title and source URL against the content of its body. Ten notes failed: their front matter — title, source URL, tier — was attached to the body of a different note entirely. In two cases the body cited a host inconsistent with the declared source. The affected notes span both primary-artefact records and secondary-literature records, and they include notes whose declared titles concerned MITRE's change taxonomy, the ATT&CK Sync project, the v19 announcement, the sub-technique release announcement and the ATT&CK changelog.

We report this for three reasons. First, because it happened in a study whose thesis is that undeclared provenance corrupts downstream conclusions, and concealing it would be indefensible. Second, because the remedy is instructive: every claim that had rested on an affected note was quarantined and re-collected from the primary artefact — the change taxonomy was re-read directly from the tool's source, the ATT&CK Sync claims were re-collected from the repository, and the tactic-layer and revocation-arity claims were recomputed from the release bundles rather than carried forward from a note. Third, because it bounds what a reader should trust. Our Tier A claims are reproducible from `code/` against the published bundles and do not depend on the note corpus at all. Our Tier B claims depend on notes, and ten of 112 notes were found to be corrupted in a way that automated checking caught only because we looked. We cannot rule out that a subtler corruption — a body attached to the right title but summarizing the wrong section — escaped the check, and we have no mechanism that would detect it. Readers should weight the Tier B positioning claims accordingly, and we would encourage any reviewer to verify the three load-bearing Tier B dependencies named in Section 11.6 against the published sources directly.

### 11.8 External validity and scope

The measurement study covers ATT&CK Enterprise in full and Mobile and ICS in the recurrence analysis only; the downstream experiments are Enterprise-only. Given that Mobile hosts the most destructive event in the corpus and ICS is restructuring now, Enterprise-only downstream results are likely to *understate* the ecosystem-wide effect, but we have not measured that and do not claim it.

The four deployed corpora in Table 9 are not a random sample of CTI datasets. They were selected because their label files are publicly available and machine-readable, which biases toward open, research-oriented artefacts and away from commercial corpora that may be better or worse maintained. The adoption evidence in Section 9 is similarly drawn from what could be cloned. The direction of that bias is unknown to us.

The attribution task is top-1 identification within a candidate universe of documented ATT&CK groups at $k = 10$ observed techniques. Real attribution uses infrastructure, malware lineage, targeting and timing alongside TTPs, and a purely TTP-based top-1 task is a deliberately narrow instrument chosen because it isolates the vocabulary. Results should not be read as statements about attribution practice. Recent work suggesting that LLM agents can reproduce documented APT profiles at high precision [66] is a further reason to treat profile-matching accuracy as a property of the documentation rather than of the adversary.

Finally, the specific numbers in this paper have a shelf life. Table 4 measures every cohort to a fixed endpoint, and that endpoint moves with every release. Under the two-clock model the identifier columns will be stable and the semantic columns will grow. We regard the fact that this paper's own results require a declared reference release in order to be comparable to a future replication as confirmation of its thesis rather than as an embarrassment, and the released artefacts declare it.

### 11.9 What would overturn the thesis

We name the falsifier, as R4 requires. The thesis dies if someone assembles a representative sample of published CTI artefacts in which a majority carry a resolvable ATT&CK release pin *and* mechanically applying the revocation crosswalk forward from that pin reproduces an independently authored current-version mapping to within inter-analyst agreement. If migration is that faithful and that common, the residual gaps we identify are a footnote and this paper is a reporting-discipline note rather than a threat-to-validity finding. Table 12 and the corroborating audits [3, 18, 79] are why we do not expect that sample to exist, but the test is available to anyone and we would welcome it.

The two-clock model of Section 4.5 has its own falsifiers. It dies if the next three major releases in every domain show substantive-rewrite rates falling below roughly 3% per year — the semantic clock stopping rather than the identifier clock merely idling; if a leading indicator of restructuring reaches a Spearman correlation above 0.6 at p < 0.05 on an extended lagged panel, making bursts forecastable and the protocol triggerable rather than standing; or if no domain experiences an identifier-Jaccard transition below 0.80 in the next eight domain-years, which would place the observed hazard outside plausible sampling error and re-establish the pre-2021 era as closed.

## 12. Conclusion

Security machine learning learned, painfully and over a decade, to control for bias in its data. Time-aware splits, realistic base rates, drift detection and conformal rejection are now the price of admission [67, 35, 22, 70]. This paper argues that the discipline stopped one level too early. Every one of those controls presumes a fixed label space, and in cyber threat intelligence the label space is a versioned ontology that moves underneath the analytics built on it.

We named the failure mode, formalized it as distinct from concept drift, and measured it. Identifier churn in ATT&CK is episodic, currently mild for Enterprise, fully recoverable through a crosswalk that is complete and almost never used — and recurrent across domains at a hazard that gives roughly one restructuring somewhere in ATT&CK every eighteen months, with no forecastable warning. Semantic churn is continuous, unsignalled, and undetected by every mechanism the ecosystem deploys, including ATT&CK's own version field, which as a change detector operates at precision 0.447 and recall 0.641. A third of the apparent growth in documented actor behaviour for pre-existing groups is bookkeeping rather than intelligence. Downstream, the effect reaches conclusions: the named actor changes in 0.722 of pre-restructuring observations and still in 0.022 across a single modern release boundary; a frozen capability's coverage claim falls from 97.0% to 17.4%; a mitigation leaderboard's top-ranked control changes even where the rank correlation exceeds 0.97. And the effect is concentrated, in the modern regime, on precisely the groups that are identifiable at all.

We are explicit about what we did not show. We did not show that drift dominates the synchronic labelling noise floor, and our design deliberately does not measure that floor. We showed separability by construction and verified it under injected noise, which also told us that our headline pre-restructuring penalties are upper bounds. We did not show that identifier normalization restores comparability; we showed that it recovers about half the penalty on legacy artefacts, under a point in the modern regime, and nothing at all about meaning. And we did not escape our own subject: our evidence pipeline suffered a provenance failure in ten of 112 notes, which we found, quarantined and re-collected, and which stands as the paper's own demonstration that undeclared provenance is not a hypothetical risk.

What remains is a small, checkable discipline. Declare the domain, the exact release and the bundle hash in the artefact. Declare whether identifiers were normalized and to what. Publish the residual — kept, merged, dropped, demoted. Project both sides of any cross-time comparison onto one reference release. Four lines, a JSON header and thirty lines of code, and a reviewer can check them in a minute. The field asks far more of itself on temporal splits, and that expectation was also once new.

## Sources

[1] ATT&CK's published retirement contract, read from the artefact — https://github.com/mitre-attack/attack-stix-data/blob/master/USAGE.md
[2] AttacKG repo audit: ATT&CK ontology frozen as a 2021-08-31 HTML scrape — https://github.com/li-zhenyuan/Knowledge-enhanced-Attack-Graph
[3] B2 synthesis: six TTP systems, five different ATT&CK ontologies, two declared versions — https://github.com/center-for-threat-informed-defense/tram
[5] CTID ATT&CK Sync: what it publishes, read from the repository — https://github.com/center-for-threat-informed-defense/attack-sync
[6] Measured: 4.3x label-space growth between CTIBench and AthenaBench — https://github.com/Athena-Software-Group/athenabench
[7] MITRE's own change taxonomy, read from diffStix source — https://github.com/mitre-attack/mitreattack-python
[8] rcATT repo audit: a 2019-era flat ATT&CK label space — https://github.com/vlegoy/rcATT
[10] tumeteor/mitre-ttp-mapping audit: a declared v12.0 remap that still leaks pre-v7 revoked IDs — https://github.com/tumeteor/mitre-ttp-mapping
[11] A Comprehensive Survey of Threat Intelligence Research: A Measurement-Based Study (ACM CSUR 2025) — https://dl.acm.org/doi/10.1145/3772280
[12] APT attribution survey (JISA 2025) — https://doi.org/10.1016/j.jisa.2025.104076
[13] AthenaBench (arXiv 2511.01144) — https://arxiv.org/abs/2511.01144
[14] ATT&CK Design and Philosophy — https://attack.mitre.org/docs/ATTACK_Design_and_Philosophy_March_2020.pdf
[15] ATT&CK Navigator layer file format — https://github.com/mitre-attack/attack-navigator/blob/master/layers/spec/v4.5/layerformat.md
[16] ATT&CK Navigator layer upgrade — https://github.com/mitre-attack/attack-navigator/blob/master/USAGE.md
[17] AttackSeqBench (arXiv 2503.03170) — https://arxiv.org/abs/2503.03170
[18] Audit: six of eight sample layers shipped in MITRE's own Navigator repository carry no ATT&CK version — https://github.com/mitre-attack/attack-navigator/tree/master/layers/samples
[19] AVClass: alias resolution and label normalization — https://software.imdea.org/~juanca/papers/avclass_raid16.pdf
[20] Beyond Single Reports — intra-version technique confusability — https://arxiv.org/abs/2604.07470
[21] Boundary synthesis: where concept-drift literature stops and ontology drift begins
[22] CADE: Detecting and Explaining Concept Drift Samples for Security Applications — https://www.usenix.org/conference/usenixsecurity21/presentation/yang-limin
[23] CAPTAIN / Chasing the Shadows: TTP-sequence attribution with no declared ATT&CK version — https://arxiv.org/abs/2409.16400
[24] Class-Incremental Learning surveys — https://arxiv.org/abs/2302.03648
[25] Cleaning the NVD and the security knowledge-base data-quality genre — https://arxiv.org/pdf/2006.15074
[26] COnto-Diff: complex change operations as evolution mappings — https://www.sciencedirect.com/science/article/pii/S1532046412000627
[27] CTI Quality Assessment Cluster — https://www.sciencedirect.com/science/article/pii/S0167404824003845
[28] CTI-REALM (arXiv 2603.13517) — https://arxiv.org/abs/2603.13517
[29] CTIArena to CTIConnect (arXiv 2510.11974) — https://arxiv.org/abs/2510.11974
[30] CTIBench (NeurIPS 2024) — https://proceedings.neurips.cc/paper_files/paper/2024/file/5acd3c628aa1819fbf07c39ef73e7285-Paper-Datasets_and_Benchmarks_Track.pdf
[31] CVE identifier lifecycle — https://www.cve.org/Resources/Media/Archives/OldWebsite/about/faqs.html
[32] CVE-CWE-CPE mapping instability — https://dl.acm.org/doi/10.1145/3641819
[33] Dataset shift and concept drift taxonomies — https://dl.acm.org/doi/10.1145/2523813
[34] diffStix: MITRE's own machine-readable ontology-drift ledger — https://github.com/mitre-attack/mitreattack-python/tree/master/mitreattack/diffStix
[35] Dos and Don'ts of Machine Learning in Computer Security (Arp et al.) — https://www.usenix.org/conference/usenixsecurity22/presentation/arp
[37] Evolution of vocabulary terms in knowledge graphs — https://arxiv.org/pdf/1710.00232
[38] FeedMeter — Evaluating the Quality of Community-Driven Threat Intelligence (2024) — https://www.scitepress.org/Papers/2024/123576/123576.pdf
[39] Fragmentation of CVSS scores in the NVD — https://www.sciencedirect.com/science/article/abs/pii/S0167404826001549
[40] Geras & Schreck — The Big Beast to Tackle: Practices in Quality Assurance for CTI (RAID 2024) — https://dl.acm.org/doi/10.1145/3678890.3678903
[41] Griffioen, Booij & Doerr — Quality Evaluation of Cyber Threat Intelligence Feeds (ACNS 2020) — https://link.springer.com/chapter/10.1007/978-3-030-57878-7_14
[42] IncreTTP: ATT&CK version updates framed as concept drift — https://link.springer.com/chapter/10.1007/978-3-032-23450-6_2
[43] LECO: Continual Learning with Evolving Class Ontologies (NeurIPS 2022) — https://arxiv.org/abs/2210.04993
[44] Legoy et al. 2020 — Automated Retrieval of ATT&CK Tactics and Techniques — https://arxiv.org/abs/2004.14322
[45] Li et al. — Reading the Tea Leaves: A Comparative Analysis of Threat Intelligence (USENIX Security 2019) — https://www.usenix.org/conference/usenixsecurity19/presentation/li
[46] MITRE ATT&CK Evaluations methodology — https://evals.mitre.org/methodology-overview/
[47] MITRE ATT&CK: State of the Art and Way Forward (ACM CSUR 2025) — https://dl.acm.org/doi/10.1145/3687300
[48] MITRE diffStix changelog_helper — https://github.com/mitre-attack/mitreattack-python/blob/master/mitreattack/diffStix/changelog_helper.py
[49] MITRE's own bias taxonomy and the Sightings Ecosystem — https://ctid.mitre.org/projects/sightings-ecosystem/
[50] Modern malware drift adaptation — https://arxiv.org/pdf/2401.12790
[51] MOTIF: ground-truth malware family labels and the open, unstable class set — https://arxiv.org/abs/2111.15031
[52] Multi-label ATT&CK classification (arXiv 2606.18166) — https://arxiv.org/abs/2606.18166
[53] OBO Foundry Identifier Policy — https://obofoundry.org/id-policy.html
[54] OBO Foundry Principle 19: Stability of Term Meaning — https://obofoundry.org/principles/fp-019-term-stability.html
[55] OBO Foundry Principle 4: Versioning — https://obofoundry.org/principles/fp-004-versioning.html
[56] Ontology evolution vs ontology versioning: change management as the core task — https://www.researchgate.net/publication/37538421_Change_Management_The_Core_Task_of_Ontology_Versioning_and_Evolution
[57] OWL versioning vocabulary — https://www.w3.org/2007/OWL/wiki/Ontology_Versions
[58] Rahman & Williams (arXiv:2211.06500): mitigation coverage has a ceiling set by the control catalogue — https://arxiv.org/abs/2211.06500
[59] Saha et al. — Kitten or Panda? Two-thirds of ATT&CK threat groups have no group-specific behaviour — https://arxiv.org/abs/2506.10645
[60] Schlette et al. — Measuring and Visualizing Cyber Threat Intelligence Quality (IJIS 2021) — https://link.springer.com/article/10.1007/s10207-020-00490-y
[61] SEvenLLM (arXiv 2405.03446) — https://arxiv.org/abs/2405.03446
[62] Shen et al. (ASIA CCS 2024): whole-graph re-analysis of MITRE Evaluations — https://arxiv.org/abs/2401.15878
[63] SoK: The MITRE ATT&CK Framework in Research and Practice — https://arxiv.org/abs/2304.07411
[64] Summiting the Pyramid v5.0 (CTID) — https://github.com/center-for-threat-informed-defense/summiting-the-pyramid
[65] SynthCTI (arXiv 2507.16852) — https://arxiv.org/abs/2507.16852
[66] Synthetic APTs (2026): LLM agents reproduce documented APT profiles at 55-80% precision — https://arxiv.org/abs/2606.07158
[67] TESSERACT: Eliminating Experimental Bias in Malware Classification across Space and Time — https://arxiv.org/abs/1807.07838
[68] The CTI Echo Chamber — vendor fragmentation as the confounder the drift thesis must separate — https://arxiv.org/abs/2602.17458
[69] Tomczak et al. (2018): Gene Ontology evolution changes the interpretation of biological experiments — https://www.nature.com/articles/s41598-018-23395-2
[70] Transcend and Transcendent: Conformal Evaluation and Rejection under Concept Drift — https://arxiv.org/abs/2010.03856
[71] TTPDrill (ACSAC 2017) — https://dl.acm.org/doi/10.1145/3134600.3134646
[72] TTPHunter / TTPXHunter: 50 then 193 TTP classes, no declared ATT&CK release — https://arxiv.org/abs/2403.03267
[73] TTPrint (arXiv 2605.25836) — https://arxiv.org/abs/2605.25836
[74] Virkud et al. (USENIX Security 2024): ATT&CK coverage is not comparable across products — https://www.usenix.org/conference/usenixsecurity24/presentation/virkud
[75] When Benchmarks Age: quantifying answer-key decay in static benchmarks — https://arxiv.org/abs/2510.07238
[76] Zibak et al. — Threat Intelligence Quality Dimensions for Research and Practice (DTRAP 2022) — https://dl.acm.org/doi/full/10.1145/3484202
[77] 'ATT&CK is an ontology, not a taxonomy' — https://www.tripwire.com/state-of-security/attck-structure-ontology
[78] ATT&CK v19 retires Defense Evasion — https://medium.com/mitre-attack/attack-v19-ff329cb65d66
[79] DeTT&CT omits the ATT&CK version from generated Navigator layers by default — https://github.com/rabobank-cdc/DeTTECT
[80] Forrester: a 100% ATT&CK Evaluations claim is a red flag — https://www.forrester.com/blogs/dont-trust-vendor-claims-about-getting-100-on-the-mitre-attck-evaluations
[81] How coverage layers are actually built — https://blog.reconinfosec.com/automating-coverage-analysis-with-att-ck-navigator
[82] Vendor ATT&CK coverage claims: '100% of what, exactly?' — https://www.attackiq.com/2026/03/10/what-does-mitre-attack-coverage-really-mean/
[84] Practitioner critique: the ATT&CK heatmap counts rules, not coverage — https://dev.to/chrisray/your-attck-heatmap-is-counting-rules-not-coverage-2gh3
