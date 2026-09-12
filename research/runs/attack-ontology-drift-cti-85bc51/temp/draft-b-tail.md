
## 6. Measuring Ontology Drift in ATT&CK

### 6.1 The referential clock is episodic — and recurrent

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

Pre-restructuring cohorts lose most of their identifiers, with half-lives of 0.4 to 2.2 years that all land on the same release. Every cohort from v7.0 onward retains at least 0.970 to the present and none reaches a half-life at all. The `Recoverable` column equals the `Revoked` column in every row: every revoked identifier in the corpus resolves to a live identifier through the published revocation graph. We make that concession in the results rather than a footnote. On identifiers alone, and for Enterprise alone, the position that drift is solved bookkeeping is correct.

It is not correct for Enterprise alone. The same analysis over Mobile finds a 2018 transition with an identifier Jaccard of 0.000 in which 76 techniques vanish with no tombstone and no successor, none recoverable — a wholesale renumbering more destructive than the Enterprise restructuring and eighteen months earlier. ICS is undergoing its own sub-technique restructuring in the current release, six years after Enterprise, with all remappings recoverable. Counting transitions with identifier Jaccard below 0.80 across the three domains gives five events in eight years: a hazard of 0.106 per major transition, or roughly one restructuring somewhere in ATT&CK every 1.5 calendar years. The 2020 event is a draw from a live hazard, not a closed wound. Nor can a consumer time-hedge against it: across seventeen lagged release pairs the best leading indicator of the next transition's revocation rate reaches a Spearman correlation of +0.377 at a permutation p-value of 0.134, and techniques revoked at v7.0 had been *edited less* in the preceding release than those that survived. Restructuring is not forecastable from the public bundles — a negative result that forces the protocol of Section 10.2 to be standing rather than triggered.

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

Read this as a decay curve, not a ranking: every row measures the same endpoint, so rows differ in elapsed time. The v7.0 cohort has had six years — 0.749 of its identifier-stable techniques have edited descriptions and 0.386 are substantially rewritten at a token Jaccard below 0.8. The v11.0 cohort has had four: 0.465 and 0.208. The v15.0 cohort has had two: 0.275 and 0.087. Fitting a staleness clock to these cohorts gives a first-10%-substantive-staleness time of roughly 1.5 years and a semantic half-life of 4.5 to 6.1 years, and the per-cohort figures do not trend downward across the post-2020 era. The text-only variant of that clock — excluding tactic changes and revocations entirely, so it cannot be attributed to the v19 re-cut — gives essentially the same answer.

Set this against Table 3. For any post-2020 Enterprise cohort the identifier half-life is never reached, while the semantic half-life is about five years and the first 10% of substantive rewriting arrives in about eighteen months. Those are the two clocks, and they answer the practitioner's question in opposite directions. Table 2 also records an event no identifier-based diff would surface: the v17.0-to-v18.0 transition rewrote the detection field of 583 surviving techniques against only 49 description edits, at an identifier Jaccard of 0.983. A defender whose detection engineering is keyed to ATT&CK's detection guidance had its entire reference text replaced in one release.

### 6.3 The signal that is not a signal

The obvious reply is that a consumer should watch ATT&CK's object version field. We tested it as a detector.

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

Across 8,359 carried-over technique pairs, 1,358 had their description rewritten — 0.162 of the total. Of those, 487 (0.359) carried no version increment, while 1,077 version increments carried no text change whatsoever. As a detector of description change the version field has precision 0.447 and recall 0.641. MITRE's own tooling knows this: `diffStix` defines a change class specifically for objects patched while their version stayed the same, and acknowledges that unintended version changes exist in earlier releases [34, 48]. The tool that computes the diff can see intensional drift; the consumer-facing contract, which offers a live/retired filter and a revocation resolver [1], cannot express it. The gap between those two artefacts is architectural rather than accidental, and it is the cleanest available evidence that O6 is unsignalled by design.

### 6.4 Growth decomposition: how much is intelligence?

The query asks what fraction of apparent growth in a CTI knowledge base is new adversary intelligence versus ontology bookkeeping. We answer on the group-technique edge, the atom of "we have learned that this actor does this".

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

Across all Enterprise transitions 5,516 group-technique edges were added, of which 2,442 belong to groups newly added to ATT&CK. Of the 3,074 added for pre-existing groups, 1,752 are genuine new intelligence, 330 are edges to newly added techniques, 487 are sub-technique refinements of an assertion already present, and 505 are re-mappings forced by a revocation. The bookkeeping share is 992 of 3,074, or 0.323.

The distribution matters more than the aggregate. The restructuring transition is 0.750 bookkeeping — but so is the most recent transition at 0.470, and two ordinary mid-decade transitions run at 0.380 and 0.340. Bookkeeping bursts are not confined to restructuring events. An analyst measuring how fast knowledge of an actor is growing from release-to-release edge counts will attribute roughly a third of observed growth to intelligence that was never acquired. This parallels the distinction between vocabulary churn and instance-data usage drawn explicitly in the knowledge-graph literature [37].

### 6.5 The most recent wave

The v19 transition is the ecosystem's live test case, and the industry narrative around it is one of rapid, unproblematic migration [78]. Between v18.1 and v19.2, 17 live techniques were revoked, including the whole T1562 family. On the v18.1 graph this touches 84 group-technique edges, 155 software-technique edges, 47 mitigations and 17 detection relationships, and 52 of 168 group profiles lose at least one identifier. One revoked identifier, T1562.001, was ranked 33 of 599 techniques by documented `uses` edges in the release it left. This is not long-tail churn.

The structural move is the one the crosswalk cannot carry. The concept *Impair Defenses* was promoted from a technique to a tactic; because a revocation edge cannot point a technique at a tactic, the parent was instead revoked onto one of its own former children while the remaining children fanned out across six other successors. Simultaneously TA0005 was recycled in place and 198 identifier-stable techniques changed tactic (Table 2). An analytic joining on tactic identifiers across this boundary compares two different concepts with no signal, no edge and no version increment to warn it.

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

A 2018-vocabulary artefact scored against a 2026 knowledge base loses 42.2 points [37.8, 46.8] against a self-consistent baseline; a 2019 artefact loses 46.2 points [41.6, 51.0]. Those are the headline numbers, and also the ones a reviewer should discount hardest, because they are one restructuring event seen from six sides. The number that survives scrutiny is 1.6 points [0.6, 2.8] for a v18.0 artefact — one release boundary, six months elapsed, an era of 0.97-plus identifier survival, an interval excluding zero. That is the cost of being one release out of date in the current, stable, well-maintained regime. It is small in aggregate. Section 7.2 shows it is not small where it matters.

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

Absolute accuracies move a great deal across scorers and profile definitions. The sign and ordering of the drift penalty do not: large and positive in every pre-restructuring cell, small and positive in every post-restructuring cell. Drift is not an artefact of one similarity function.

### 7.2 Meeting the strongest objection

The strongest published objection is not that our numbers are wrong but that they are irrelevant, because a much larger source of label variance already exists at a single pinned release. Virkud et al. show that detection products describing the same behaviour carry different ATT&CK labels within one pinned release, often with no overlap [74]. Saha et al. show that roughly a third of ATT&CK groups have any technique unique to them [59]. Multi-report evaluation adds that a substantial share of extraction errors are between same-tactic, description-overlapping techniques [20], and vendor fragmentation has been characterized as an echo-chamber effect that any drift claim must separate itself from [68]. If a labelling process has that much synchronic variance, why care about a 1.6-point diachronic effect?

We take the objection seriously enough to make it falsifiable. It implies three testable consequences and we tested all three.

**Separability.** The objection implies the measured penalty is a re-description of the same confusability and should collapse once realistic labelling noise is present. Our design holds the labelling process fixed across conditions by construction, so the noise term is identical in all four conditions and cancels in the contrast. That establishes separability but sets the noise rate to zero, which — as R2 anticipates — licenses separability without testing additivity; an interaction cannot be observed at one level of a moderator. So we ran the factorial. Each observed technique is replaced with probability $\rho$ by a sibling sub-technique, its parent, or a same-tactic technique, applied in the modern vocabulary *before* back-projection so the substitution flows identically into all four conditions. At 1,200 trials per cell the drift penalty at v1.0 moves from 0.439 at $\rho = 0$ to 0.416, 0.392 and 0.328 at $\rho = 0.1, 0.2, 0.4$; at v6.0 from 0.476 to 0.411, 0.398 and 0.312; at v12.0 it is 0.017, 0.023, 0.018, 0.014; at v18.0, 0.012, 0.005, 0.011, 0.010.

The penalty survives at every noise level and every boundary, so the first consequence is refuted. Strict additivity, however, also fails where drift is large: at $\rho = 0.4$ the pre-restructuring penalties attenuate by roughly a fifth to a third, because noise and drift consume the same finite signal. **The correct statement is that drift is separable from labelling noise and sub-additive with it, and the noise-free figures in Table 6 are therefore upper bounds on drift's contribution in a noisy world.** We state this in the results rather than in a limitation, because it changes how the headline numbers should be read. In the modern regime the penalty is flat in $\rho$ and the additive reading holds. Normalization degrades faster than the penalty does: recovery at v1.0 falls from 0.441 at $\rho = 0$ to 0.279 at $\rho = 0.4$, so the Section 8 repair buys less as label quality falls.

**Non-identifiability.** The objection implies the penalty is carried by the majority of groups that were never attributable and should vanish on the identifiable subset. We stratified by whether a group has any technique unique to it within the candidate universe. The specificity fraction our corpus produces — 0.325 at v12.0, 0.309 at v16.0, 0.298 at v18.0 — independently reproduces the published figure [59], a useful check that we measure the same property. The drift penalty on the stratum with a unique technique is 0.0344 [0.0101, 0.0607] at v12.0, 0.0331 [0.0166, 0.0497] at v16.0 and 0.0239 [0.0109, 0.0391] at v18.0. On the stratum without one it is 0.0089, 0.0049 and 0.0067, with intervals touching or crossing zero at two of three versions.

The second consequence is refuted in the opposite direction from what it predicts. In the modern regime the drift penalty is two-and-a-half to seven times *larger* on identifiable groups. The mechanism is transparent once stated: a group's identifying token is by definition a rare technique, and rare techniques are exactly the ones ATT&CK adds, splits, refines and revokes. Drift attacks the signal attribution depends on, and a small average over a population that is mostly non-identifiable conceals a material effect on the subset that carries the task.

**Wrong unit.** The third consequence — that we measure a quantity that does not exist in the field, because real labelling happens on independently observed incidents rather than inside one curator's graph — is not refuted. It is conceded, and Section 11.1 treats it as the study's central residual threat.

The scoping statement we are entitled to is therefore precise. Noise bounds the *absolute* accuracy of TTP attribution, and our design does not claim otherwise: every figure in Table 6 is an internal-consistency score, and the self-consistent baselines sitting between 0.62 and 0.86 rather than near 1.0 are where non-identifiability has already been absorbed. Drift bounds *comparability across time*, a different quantity, additive on top of the noise floor in the modern regime and sub-additive in the pre-restructuring regime.

### 7.3 Conclusions, not scores

Score movements are a hygiene complaint. The Gene Ontology precedent sets a higher bar: show the conclusions move [69].

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

For a v1.0 artefact the named actor changes in 0.722 of observations and changes to a *wrong* actor in 0.712; for v6.0 the figures are 0.790 and 0.774. Across a single modern release boundary the named actor still changes in 0.022 of observations, and in that regime essentially every change is to a wrong actor. These are not score deltas; they are different answers to the question the analysis was run to answer.

The final column is what a research-integrity reviewer should notice. Applying normalization *itself* changes the verdict in 0.368 to 0.442 of trials for pre-restructuring artefacts and 0.006 to 0.030 for modern ones. A repair that silently changes the answer in two-fifths of cases is not a neutral preprocessing step, and applying it without declaring it is itself a reporting failure.

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

A mitigation leaderboard is a budget document: it says which control to fund first. Frozen at v6.0 the naive ranking has Kendall's tau of 0.665 against the correct ranking, three members displaced from the top ten, and a changed rank-1; normalization repairs this well, raising tau to 0.968. The modern rows carry the sting: at v16.0 and v17.0 the rank correlation is 0.976 to 0.977 — nearly perfect — and the top-ranked mitigation *still changes*. A high rank correlation is not a guarantee about the decision the ranking is used to make, because the decision depends on the head of the distribution while the correlation is dominated by the tail.

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

The capability does not change; only the ontology does. A portfolio claiming 97.0% coverage at v6.0 measures 17.4% naively at v19.0 and 33.9% after normalization — the 16.5-point gap is pure identifier artefact, and the remaining fall is denominator growth under O1. A portfolio frozen one release ago at v18.0 claimed 84.2% and measures 81.1% naively, with a 2.2-point identifier artefact. Every published ATT&CK coverage percentage is therefore a function of two things: the capability, and the release it was computed against. The literature already establishes that coverage is not comparable across products at a fixed version [74, 46, 62] and that the denominator is contested [64, 84]. Table 8 establishes that it is not comparable across versions for a fixed product — the complementary half, and the one that bites an organization tracking its own coverage trend over time.

**The long-tail objection.** MITRE's bias work documents that observed telemetry is dominated by a short head of techniques [49], which suggests churn among rare identifiers should barely move a frequency-weighted number. We repeated the experiment with techniques weighted by documented prevalence. The artefact gets *larger*: at v6.0 it is +16.50 points unweighted and +20.01 points prevalence-weighted. In the modern regime the two converge — +1.58 versus +1.43 at v10.0, +2.15 versus +1.57 at v18.0 — so weighting neither creates nor destroys the modern effect. Documented prevalence at v19.0 is only moderately head-heavy: the fifteen most-referenced techniques carry 0.285 of all `uses` edges. And the most recent revocation wave took a technique ranked 33 of 599 by that measure (Section 6.5).

The objection is refuted on documentation prevalence. It is *not* refuted on telemetry prevalence, and the distinction is real rather than rhetorical: documented `uses` edges are a cumulative, monotone stock over cited CTI reports, biased toward behaviours easy to narrate, whereas sightings telemetry measures a flow of defender alerts over a window and is materially more concentrated [49]. That telemetry is not reachable in this environment. We therefore claim the long-tail objection fails for the fraction of the *written CTI corpus* affected by drift, and leave it untested for the fraction of the *alert stream* affected. Section 11.3 restates this as a limitation rather than a result.

## 8. ATT&CK-Norm: A Version-Normalization Protocol

ATT&CK-Norm is the projection half of the control proposed in Section 4.6. Given $A \subseteq \mathcal{L}_V$ and a target release $W$ it resolves each identifier by: (1) following the transitive closure of `revoked-by` to a live identifier in $W$; (2) keeping identifiers already live in $W$; (3) optionally rolling an unresolvable sub-technique up to its parent; (4) dropping identifiers absent from $W$. It is intentionally trivial. Its value is not algorithmic novelty — alias resolution has prior art in malware labelling [19] and the crosswalk it consumes is MITRE's own — but as a reference implementation against which the *limits* of identifier repair can be measured. Three of those limits are results.

**Roll-up is a dead branch.** We re-ran the attribution experiment with roll-up enabled and disabled as the only difference across 54 conditions and 27,000 trials. Top-1 accuracy is identical to three decimals in every condition and the paired bootstrap interval on the difference is [+0.000, +0.000]. A broader sweep over archival group profiles and all four deployed corpora finds three firings in 12,027 resolutions across every domain and major release. The reason is structural: MITRE never orphans a sub-technique — a revoked sub-technique always resolves to a live target — and deprecations without a successor are top-level, so roll-up's precondition essentially does not arise. The correct default is to drop and count, not because drop wins a measured contest but because roll-up wins nothing measurable while adding a code path that can fabricate a parent-level assertion the source never made. We ship it disabled and flag-gated.

**The protocol must return a residual, not a set.** The current Enterprise crosswalk has 149 revocation edges, of which eight targets are many-to-one, absorbing twenty predecessors; the largest absorbs five. A set-valued protocol cannot distinguish a clean ten-identifier migration from one where three identifiers merged and two were dropped, because both return a set. This is not hypothetical: TRAM's bootstrap label set goes from 537 to 503 distinct live classes under normalization, with 0.1475 of its 25,770 instances landing in a merged class; rcATT goes from 215 to 199 with 0.0937 of its 6,235 instances merged. A benchmark whose class count silently collapses by 34 is not the same benchmark. We therefore redefine the return type as a ledger — kept, merged, dropped, demoted — and treat an unreported residual as a reporting failure.

**A defensible-looking wrong answer.** The v19 T1562 collapse is the cleanest counter-example. At the prior release T1562 was a top-level technique with twelve children spanning firewall modification, cloud log tampering, command-history manipulation, safe-mode boot and downgrade attacks, and three documented groups assert the generic parent — the standard CTI convention for "the report says defenses were impaired but does not say how". After v19, normalizing the parent resolves in one hop to a live identifier, reports full success and drops nothing. The answer is wrong: an analyst who wrote the parent because a report said the actor disabled the host firewall is now recorded as asserting the actor tampered with security tooling — a strictly narrower and factually different claim, in a tactic that did not exist when the artefact was written. One group whose profile asserted four identifiers in that family normalizes to three, so its measured technique breadth falls by one as pure bookkeeping. This is the O4/O5 defect made concrete, and no identifier arithmetic fixes it, because the crosswalk is doing exactly what it was specified to do.

**What it buys, honestly.** On pre-restructuring artefacts normalization recovers 0.42 to 0.53 of the attribution penalty (Table 6), a mean top-1 gain of about twenty points. Post-restructuring the mean gain is under one point and its 95% interval includes zero in roughly two-thirds of conditions. Where it works cleanly is coverage ranking: mean Kendall's tau rises from 0.931 to 0.992 across the conditions of Table 11, three of four naive rank-1 flips vanish and none is introduced. And it is blind to intension by construction: across the release that dissolved the field's most-used tactic it returns all 674 identifier-stable techniques unchanged — zero drift signalled — while 198 changed tactic and 41 changed description hash. ATT&CK-Norm is a bounded legacy-migration tool, not a cure. A paper claiming that normalization restores comparability repeats the error this paper set out to diagnose.

## 9. Label Validity of Deployed CTI Corpora

If drift were a theoretical hazard, deployed corpora would show little of it. We dated four widely used CTI label sets against every published release.

**Figure 7.** Label-validity curves for four deployed CTI corpora.

**Table 9.** Label validity of deployed corpora, measured at v19.2.

| Corpus | Distinct labels | Label instances | Sub-technique labels | Best-fit release | Fit | Releases where all labels valid | Invalid today | Repairable |
|---|---|---|---|---|---|---|---|---|
| ctibench-ate | 120 | 397 | 0 | v14.0 (2023-10-31) | 0.942 | **none** | 8 (0.067) | 1 |
| rcatt | 215 | 6235 | 0 | v4.0 (2019-04-30) | 1.000 | 8 (v4.0–v6.3) | 107 (0.498) | 99 |
| tram-bootstrap | 537 | 25770 | 344 | v13.0 (2023-04-25) | 0.939 | **none** | 43 (0.080) | 43 |
| tram2 | 50 | 5143 | 24 | v8.2 (2021-01-27) | 1.000 | 18 (v8.2–v16.1) | 2 (0.040) | 2 |

**Corpora are datable, and dating them is diagnostic.** rcATT's label space fits v4.0 exactly and is simultaneously valid across eight consecutive releases spanning 2019 to early 2020, consistent with its publication date [44] and with a repository audit finding a 2019-era flat label space [8]. It carries zero sub-technique identifiers, the signature of a pre-restructuring vocabulary. Today 0.498 of its distinct labels and 0.380 of its label instances are invalid. A model trained on that corpus and evaluated against modern gold labels measures agreement between two vocabularies — and 99 of the 107 dead labels are mechanically repairable, meaning the repair is available and, judging by Table 12, not applied.

**Two corpora fit no release at all.** CTIBench-ATE and TRAM's bootstrap set have a best fit below 1.0 at every release: there is no ATT&CK version at which all their labels are simultaneously live. This is stronger than "out of date". A corpus fitting no release was not drawn from a single release; its labels were assembled across time or across domains, and no pinning discipline applied after the fact makes it internally consistent. For a benchmark this is disqualifying for cross-version comparison, and benchmark generations reporting continuity of measurement under a stable identifier [29, 13] inherit the problem from their predecessors [30].

**Not every invalidity is drift, and this cuts against us.** CTIBench-ATE shows eight labels invalid at v19.2, of which seven are recorded as unrepairable. All seven come from a single row whose platform column says Enterprise while its entire gold identifier set is Mobile-only — and all seven are live in the Mobile domain at the same release. Seven-eighths of that corpus's apparent drift damage is not drift; it is a single-version labelling error, and a normalization protocol without a domain guard would confidently report seven unrepairable deprecations and be wrong seven times. We report this because it is the strongest available counter-example to our own instrument, and because it is a design requirement: domain must be declared alongside release, and the residual ledger must distinguish withdrawn concepts from wrong-domain identifiers from scrape artefacts, since the three need opposite remedies.

**Table 12.** ATT&CK version declarations in deployed corpora.

| Corpus | Documentation files scanned | ATT&CK version declarations found |
|---|---|---|
| cti-bench | 2 | 0 |
| rcATT | 2 | 0 |
| tram | 15 | 0 |

Zero declarations across nineteen documentation files. This scan is narrow — two of three repositories contributed two files each — and we do not rest the adoption claim on it alone. It is corroborated where the version field exists and is optional [15]: six of eight sample layers in MITRE's own Navigator repository carry no ATT&CK version [18], and the most widely used layer-generation tool omits it by default [79]. Independent audits of deployed TTP systems find five different ATT&CK ontologies across six systems with two declared versions between them [3], one system whose ontology is a dated HTML scrape [2], and one dataset declaring a target release while carrying identifiers revoked five releases earlier [10]. The pattern is consistent across every part of the ecosystem we could inspect: the mechanism exists, and the field does not use it.

## 10. Discussion and Reporting Discipline for CTI Research

### 10.1 What the measurement licenses

Supported: ontology drift is measurable and separable from the synchronic labelling noise floor (Sections 6, 7.2); it changes conclusions and not merely scores (Section 7.3); and the mechanism that would repair it exists, is nearly as good as an identifier crosswalk can be, and is close to unused (Sections 8, 9).

Not supported, and we will not say it. Not that `revoked-by` cannot express the v19 re-cut — it can, as merges, and the defect is that merging is lossy and unannounced. Not that normalization restores comparability — it restores identifier comparability on legacy artefacts and buys almost nothing modern. Not that ATT&CK is unstable — post-2020 Enterprise identifiers are remarkably stable, and the instability is in meaning, in the tactic layer, and in other domains. And not any absolute attribution accuracy as a statement about attribution, for the reasons in Section 11.1.

### 10.2 A four-line reporting contract

*For a CTI paper or dataset.* (1) The ATT&CK domain, the exact release, and the SHA-256 of the STIX bundle — in the artefact, not the prose. (2) Whether identifiers were normalized, and to which target. (3) The residual ledger: kept, merged, dropped and demoted counts, with dropped identifiers listed verbatim. (4) For any cross-time comparison, a statement that both sides were projected onto one reference release. The engineering cost is a JSON header, a table and about thirty lines of code. The real cost is reputational: a residual line makes label decay public, and for one corpus in Table 9 it would read 0.498 of identifiers and 0.380 of label instances invalid today.

*For a benchmark, additionally.* (5) The label granularity policy — parent-only or mixed — and the class count before and after normalization, because a benchmark whose classes silently collapse from 537 to 503 is not the same benchmark. (6) A continuous-integration re-validation script that fails when any gold label is not live in the declared release. The cost is a standing maintenance obligation and the loss of cross-release score comparability by default, which is the point rather than a side effect; benchmarks moving to live-API evaluation pursue the same objective by a different route [13], and answer-key decay supplies the general argument [75].

*For a vendor coverage claim, additionally.* (7) The release and the denominator — live techniques in that release, as a number — printed next to the percentage. (8) The claim restated against the current release, or explicitly marked as-of. The cost is that coverage percentages become non-monotone in public. Given Table 8 and the existing critique of denominators [64, 82, 84], that is a feature.

Because restructuring is not forecastable one release ahead (Section 6.1), this discipline must be standing rather than triggered by an observed revocation. There is no early-warning signal to wait for.

### 10.3 What MITRE could port, and from where

None of the following is invented here; all of it is standard ontology-engineering practice and would be a port rather than a research programme. A two-tier successor vocabulary distinguishing exact from inexact successors, as OBO Foundry Principle 19 specifies [54], would let a split be expressed as several inexact pointers instead of one misleading exact one. A controlled obsolescence-reason vocabulary — superseded-by-split, merged, re-scoped, promoted-to-tactic, out-of-scope — would make drop and merge distinguishable, which today they are not. Making retirement visible in the human-readable label would stop tools that join on name from silently working against a dead concept. Referent stability at a stable identifier is the principle that renaming a tactic in place violates [53, 54]. Prior-version and backward-compatibility links on the release collection object are standard OWL vocabulary [57], and ATT&CK has neither, so lineage is reconstructed by sorting release names. Publishing the evolution mapping as a first-class versioned artefact typed with complex change operations is exactly what COnto-Diff specifies [26]; `diffStix` already computes the underlying operations [34, 48], and typing them is what would make the bookkeeping-versus-intelligence split of Table 5 computable rather than asserted. Finally, making the Navigator layer's ATT&CK version field mandatory [15] would close the largest adoption gap we measured.

### 10.4 The missing quality dimension

CTI quality frameworks enumerate accuracy, completeness, timeliness, relevance, provenance and interoperability [60, 76, 27], and practice studies describe what teams actually do [40]. Across the sources we could reach, none defines a dimension over the reference vocabulary. We state that as an audited absence over a bounded search, not a proof of non-existence, and propose *vocabulary currency* as the missing dimension — operationalized by the four lines of Section 10.2 and measurable, for any corpus, by the analysis of Section 9. It is a quality property in the ordinary sense: a property of the artefact, checkable without access to the producer, degrading predictably with time at a rate this paper estimates.

### 10.5 What an SCI-level contribution here must demonstrate

Naming drift is not enough: the SoK already flags temporal instability [63] and MITRE already publishes the diff [34]. Counting churn is not enough either; anyone can run `diffStix`. The bar, set by the Gene Ontology precedent [69], has four parts. A contribution must (i) formalize the phenomenon so that it is distinguished from concept drift rather than subsumed by it, (ii) measure it longitudinally over the full published release history rather than at selected boundaries, (iii) demonstrate that it changes *conclusions* under a design holding the labelling process fixed, so the effect is not a re-description of known synchronic noise [74, 59], and (iv) state honestly what the proposed repair cannot do. A paper that does (i) through (iii) and skips (iv) has produced a tool paper with an inflated claim. That is why Section 11 is long.

## 11. Threats to Validity

This paper argues that CTI research under-reports the limits of its own instruments. It would be absurd to make that argument and then under-report ours. What follows is ordered by severity as we assess it, and the first item is the one we would attack first if we were reviewing this paper.

### 11.1 The closed ATT&CK-internal loop

The attribution experiment is a closed loop: observations, candidate profiles, ground-truth group assignment and the back-projection map all derive from a single curator's knowledge base. Nothing in the design is an independent measurement of an intrusion. Three consequences follow and we accept all of them.

*The absolute accuracies are not attribution performance.* The values between 0.62 and 0.86 in Table 6 are internal-consistency scores: they measure how reliably a sample drawn from a group's documented profile identifies that group within its own graph. They must never be cited as evidence that TTP attribution works at that rate, and no claim here depends on their level — only on differences between conditions that share the loop.

*The self-consistent baseline is a reconstruction, not a historical system.* The condition our released code and Table 6 label *contemporaneous* is a back-projection: 2026 intelligence transcribed into an earlier vocabulary, not a system as it existed in that year. We ran the missing archival cell — real archival profiles scored against real archival observations in the era's own vocabulary — and it gives 0.969 at v1.0 against the back-projection's 0.668. The gap is a collision artefact: dense modern profiles collapsed onto a coarse vocabulary collide with one another in a way no 2018 system experienced, because 2018 profiles were sparse. This matters for the sign of our bias. Two biases run in opposite directions — the collision effect depresses the self-consistent baseline and therefore *deflates* the reported penalty, while the construction guaranteeing that observed techniques are drawn from the true profile is a perfect-recall idealization that *inflates* it. The measured net at the pre-restructuring boundaries is downward, so those penalties are conservative. In the modern regime the two constructions converge (0.837 versus 0.856 at v12.0; 0.841 versus 0.846 at v18.0), so the modern headline is unaffected. We nonetheless consider the condition misnamed, and the fix — rename to *back-projected* and publish the archival cell as a diagnostic — is adopted in the released artefacts, though Table 6 retains the original column header for consistency with the released results files.

*Real archival artefacts do worse than the reconstruction.* A partially open-loop condition, scoring genuine archival group profiles against the modern knowledge base, reaches 0.159 at v1.0 against the back-projection's 0.231. Opening the loop costs accuracy rather than gaining it, which is evidence that the closed loop is, if anything, generous to the systems it evaluates.

The experiment that would close this threat is the one the field does not have: a double-labelled incident corpus in which two independent analysts label the same intrusions under two ATT&CK releases, yielding the drift term and the inter-analyst term simultaneously and from outside the curator's own edges. We searched for one and did not find a public instance. Until such a corpus exists, the honest status of our attribution result is *a lower bound on the incomparability induced by vocabulary change inside a maximally favourable, internally consistent setting*.

### 11.2 The headline penalties are upper bounds

Section 7.2 states this in the results and we restate it here because it is also a limitation. The conditions in Table 6 hold labelling noise at exactly zero. Under injected Virkud-shaped substitution the pre-restructuring penalty attenuates by roughly a fifth to a third at $\rho = 0.4$ — from 0.439 to 0.328 at v1.0 and from 0.476 to 0.312 at v6.0 — because drift and noise consume the same finite signal. The modern penalties are flat in $\rho$ and therefore additive, but the modern penalties are also the small ones. A reader should take the pre-restructuring figures as upper bounds on drift's marginal contribution in a realistically noisy world, and the recovery fractions as upper bounds too: recovery at v1.0 falls from 0.441 to 0.279 across the same sweep.

Two further idealizations inflate specific quantities. The *naive* condition is a uniform worst case: because the modern profiles are almost purely sub-technique-level while the back-projected artefact is purely parent-level, exact matching scores near zero across the restructuring boundary, whereas real legacy artefacts are mixed-granularity and would sit between *naive* and *normalized*. And the normalization function is close to the algebraic inverse of the back-projection, since both walk the same revocation and sub-technique graphs; the reported recovery is therefore an upper bound on what normalization achieves on real label sets carrying typographical errors, cross-domain identifiers and scrape artefacts — exactly the defects Section 9 found in a deployed benchmark.

### 11.3 Documentation prevalence is not telemetry prevalence

The prevalence-weighted coverage analysis weights techniques by documented `uses` edges, which are not sightings. A `uses` edge counts how many groups, malware families and tools MITRE has documented as employing a technique: a cumulative stock over cited CTI reports, monotone in time because a 2019 edge never decays, and biased toward behaviours easy to narrate in a written report. Defender telemetry measures a flow over a window and is materially more concentrated [49]. Worse for us, the weight is computed from the same release whose churn is being measured, so a revoked technique carries its weight out of the corpus with it; the weighted artefact is not independent evidence in the way an external telemetry distribution would be.

The correct scope statement is therefore narrow and we hold to it: the long-tail objection is refuted for the fraction of the *written CTI corpus* affected by drift, and untested for the fraction of the *alert stream* affected, because the telemetry that would test it on its own data is not reachable in this environment. A reader who believes the alert stream is far more concentrated than the documentation stock — and the published bias work suggests it is [49] — should discount our prevalence-weighted result accordingly. It would not change the unweighted, attribution or label-validity results.

### 11.4 Construct validity of the drift measures

Semantic drift is operationalized as token Jaccard over technique descriptions with a substantial-rewrite threshold at 0.8. Token overlap is a coarse proxy for meaning: an editorial rewrite preserving the referent scores as drift, and a two-word change that narrows a technique's scope may not. We chose it because it is transparent, reproducible without a model, and stable across an eight-year corpus, but a reviewer is entitled to read our intensional-drift rates as an upper bound on referent change and the substantial-rewrite column as the more conservative of the two in Table 4. The direction of the resulting bias is not obvious and we do not claim it is small.

The bookkeeping classification in Table 5 is rule-based. An edge counts as sub-technique refinement when it is a more specific child of an assertion already present for that group, and as revocation re-mapping when it follows a revocation edge. Both rules are conservative: an edge is classified as bookkeeping only when mechanical evidence is present, so an edge that is substantively a re-description but carries no crosswalk evidence is counted as genuine new intelligence. The 0.323 aggregate is therefore a lower bound under our definitions — of a quantity whose definition is itself contestable.

The identifier half-life in Table 3 is computed on the major-release grid. A cohort crossing a restructuring boundary has its half-life attributed to that release, which is correct but compresses the timing: the six pre-restructuring half-lives are measurements of the same event at different distances from it, and reading them as six independent observations of a decay process would be wrong. We report them as one event seen six times.

### 11.5 Internal inconsistency in our own change counts

Two computations of the same quantity in our own pipeline disagree, and we report the disagreement rather than silently picking one. The release-grid analysis behind Table 13 finds 1,358 description rewrites over 8,359 carried-over pairs, of which 487 carry no version increment. An independent recomputation directly from the bundles, with a different treatment of whitespace and reference-block normalization, finds 1,366 and 494. The precision and recall we quote for the version field (0.447 and 0.641) come from the first. The discrepancy is under 0.6% and changes no qualitative claim, but it illustrates this paper's thesis at an uncomfortable angle: two implementations of "did the description change?" disagree, and neither is wrong, because the answer depends on a normalization choice that neither implementation declares in its output. Our own contract would require declaring it; we now do. Similarly, the count of techniques changing tactic across the most recent transition is 198 on the major-release grid (Table 2) and 201 when computed between the specific patch releases at each end. Both are correct measurements of slightly different intervals, and the lesson for the contract is that a release must be declared to patch-level precision, not to major version.

### 11.6 Evidence tiers and the fidelity of the secondary literature

The positioning in Section 3 rests on secondary literature that, in this environment, was reachable only through search summaries, because the egress path blocks publisher sites and preprint servers. We observe a strict rule: no verbatim quotation is asserted from any source we did not read in full, every Tier B claim is attributed as reported rather than verified, and where a Tier B source is load-bearing we say which part of the argument it carries. Three places matter most: the synchronic labelling-noise floor [74], the group-specificity fraction [59], and the multi-report extractor error analysis [20]. For the second we have independent corroboration — our own stratification reproduces the specificity fraction at 0.298 to 0.325 — but for the noise floor we rely on the reported result, and our refutation of the non-separability consequence is conducted against a *model* of that noise (sibling, parent and same-tactic substitution at rate $\rho$) rather than against the measured joint distribution of vendor labels. If the real substitution structure differs systematically from our model — for instance if vendor disagreements cluster on exactly the techniques that also churn — the separability argument weakens. This is the most consequential Tier B dependency in the paper.

Tier C claims are audited absences. The statement that no established CTI quality framework names vocabulary or ontology versioning as a dimension is bounded by the sources we could reach [11, 27, 38, 40, 41, 60, 76], stated as an absence over that bound and never as a proof. The same applies to our inability to determine whether the largest comparative extraction evaluation re-baselines its systems onto a common release before comparing; that could not be verified and no claim about it appears in the manuscript.

### 11.7 A corpus integrity incident in our own evidence pipeline

We ran an integrity check over the 112 structured evidence notes accumulated during this study, comparing each note's declared title and source URL against its body. Ten failed: their front matter — title, source URL, tier — was attached to the body of a different note entirely, and in two cases the body cited a host inconsistent with the declared source. The affected notes span both primary-artefact and secondary-literature records, including notes whose declared titles concerned MITRE's change taxonomy, the ATT&CK Sync project, the v19 announcement, the sub-technique release announcement and the ATT&CK changelog.

We report this for three reasons. First, because it happened in a study whose thesis is that undeclared provenance corrupts downstream conclusions, and concealing it would be indefensible. Second, because the remedy is instructive: every claim resting on an affected note was quarantined and re-collected from the primary artefact — the change taxonomy re-read directly from the tool's source, the ATT&CK Sync claims re-collected from the repository, and the tactic-layer and revocation-arity claims recomputed from the release bundles rather than carried forward from a note. Third, because it bounds what a reader should trust. Our Tier A claims are reproducible from `code/` against the published bundles and do not depend on the note corpus at all. Our Tier B claims depend on notes, and ten of 112 notes were corrupted in a way that automated checking caught only because we looked. We cannot rule out a subtler corruption — a body attached to the right title but summarizing the wrong section — and we have no mechanism that would detect it. Readers should weight the Tier B positioning claims accordingly, and any reviewer is encouraged to verify the three load-bearing Tier B dependencies of Section 11.6 against the published sources directly.

### 11.8 External validity and scope

The measurement study covers ATT&CK Enterprise in full and Mobile and ICS in the recurrence analysis only; the downstream experiments are Enterprise-only. Given that Mobile hosts the most destructive event in the corpus and ICS is restructuring now, Enterprise-only downstream results likely *understate* the ecosystem-wide effect — but we have not measured that and do not claim it.

The four corpora in Table 9 are not a random sample of CTI datasets. They were selected because their label files are public and machine-readable, which biases toward open, research-oriented artefacts and away from commercial corpora that may be better or worse maintained. The adoption evidence in Section 9 is similarly drawn from what could be cloned. The direction of that bias is unknown to us.

The attribution task is top-1 identification within a candidate universe of documented ATT&CK groups at $k = 10$ observed techniques. Real attribution uses infrastructure, malware lineage, targeting and timing alongside TTPs; a purely TTP-based top-1 task is a deliberately narrow instrument chosen because it isolates the vocabulary, and results should not be read as statements about attribution practice. Recent work suggesting LLM agents can reproduce documented APT profiles at high precision [66] is a further reason to treat profile-matching accuracy as a property of the documentation rather than of the adversary.

Finally, the numbers in this paper have a shelf life. Table 4 measures every cohort to a fixed endpoint that moves with every release; under the two-clock model the identifier columns will be stable and the semantic columns will grow. That this paper's own results require a declared reference release in order to be comparable to a future replication is confirmation of its thesis rather than an embarrassment, and the released artefacts declare it.

### 11.9 What would overturn the thesis

We name the falsifier, as R4 requires. The thesis dies if someone assembles a representative sample of published CTI artefacts in which a majority carry a resolvable ATT&CK release pin *and* mechanically applying the revocation crosswalk forward from that pin reproduces an independently authored current-version mapping to within inter-analyst agreement. If migration is that faithful and that common, the residual gaps we identify are a footnote and this paper is a reporting-discipline note rather than a threat-to-validity finding. Table 12 and the corroborating audits [3, 18, 79] are why we do not expect that sample to exist, but the test is available to anyone and we would welcome it.

The two-clock model has its own falsifiers. It dies if the next three major releases in every domain show substantive-rewrite rates falling below roughly 3% per year — the semantic clock stopping rather than the identifier clock merely idling; if a leading indicator of restructuring reaches a Spearman correlation above 0.6 at p < 0.05 on an extended lagged panel, making bursts forecastable and the protocol triggerable rather than standing; or if no domain experiences an identifier-Jaccard transition below 0.80 in the next eight domain-years, which would place the observed hazard outside plausible sampling error and re-establish the pre-2021 era as closed.

## 12. Conclusion

Security machine learning learned, painfully and over a decade, to control for bias in its data [67, 35, 22, 70]. This paper argues the discipline stopped one level too early: every one of those controls presumes a fixed label space, and in cyber threat intelligence the label space is a versioned ontology that moves underneath the analytics built on it.

We named the failure mode, formalized it as distinct from concept drift, and measured it. Identifier churn in ATT&CK is episodic, currently mild for Enterprise, fully recoverable through a crosswalk that is complete and almost never used — and recurrent across domains at a hazard giving roughly one restructuring somewhere in ATT&CK every eighteen months, with no forecastable warning. Semantic churn is continuous, unsignalled, and undetected by every mechanism the ecosystem deploys, including ATT&CK's own version field, which as a change detector operates at precision 0.447 and recall 0.641. A third of the apparent growth in documented actor behaviour for pre-existing groups is bookkeeping rather than intelligence. Downstream, the effect reaches conclusions: the named actor changes in 0.722 of pre-restructuring observations and still in 0.022 across a single modern release boundary; a frozen capability's coverage claim falls from 97.0% to 17.4%; a mitigation leaderboard's top-ranked control changes even where rank correlation exceeds 0.97. And in the modern regime the effect concentrates on precisely the groups that are identifiable at all.

We are explicit about what we did not show. We did not show that drift dominates the synchronic labelling noise floor, and our design deliberately does not measure that floor; we showed separability by construction and verified it under injected noise, which also told us our headline pre-restructuring penalties are upper bounds. We did not show that identifier normalization restores comparability; we showed it recovers about half the penalty on legacy artefacts, under a point in the modern regime, and nothing at all about meaning. And we did not escape our own subject: our evidence pipeline suffered a provenance failure in ten of 112 notes, which we found, quarantined and re-collected, and which stands as this paper's own demonstration that undeclared provenance is not a hypothetical risk.

What remains is a small, checkable discipline. Declare the domain, the exact release and the bundle hash in the artefact. Declare whether identifiers were normalized and to what. Publish the residual — kept, merged, dropped, demoted. Project both sides of any cross-time comparison onto one reference release. Four lines, a JSON header and thirty lines of code, and a reviewer can check them in a minute. The field asks far more of itself on temporal splits, and that expectation was also once new.
