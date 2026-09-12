# Evidence digest — attack-ontology-drift-cti-85bc51

Every figure below is computed by `code/` from public artefacts and is
reproducible with `bash code/run_all.sh`. Drafting agents must quote these
numbers exactly and must not recompute or round them differently.

## 1. The corpus

- enterprise-attack: 19 major releases, v1.0 (2018-01-17) to v19.0 (2026-04-28).
- mobile-attack: 19 major releases, v1.0 (2018-01-17) to v19.0 (2026-04-28).
- ics-attack: 12 major releases, v8.0 (2020-10-27) to v19.0 (2026-04-28).
- Release-level analyses use the first release of each major version; the
  deployed-corpus validity analysis uses every published release (41
  Enterprise, 38 Mobile, 27 ICS).

## 2. The discontinuity

- v6.0 to v7.0 (2020-03-31): identifier-set Jaccard 0.222; 302 techniques added, 129 revoked, 11 deprecated; 750 group-technique edges removed and 1235 added in a single release.

## 3. Identifier survival

- v1.0 (2018-01-17): 188 identifiers, 0.410 still live at v19.0, 100 revoked, 11 deprecated, 100 recoverable via revoked-by; half-life 2.2 years (at v7.0).
- v6.0 (2019-10-23): 266 identifiers, 0.474 still live at v19.0, 129 revoked, 11 deprecated, 129 recoverable via revoked-by; half-life 0.4 years (at v7.0).
- v7.0 (2020-03-31): 428 identifiers, 0.970 still live at v19.0, 12 revoked, 1 deprecated, 12 recoverable via revoked-by; half-life never reached.
- v12.0 (2022-10-25): 594 identifiers, 0.978 still live at v19.0, 13 revoked, 0 deprecated, 13 recoverable via revoked-by; half-life never reached.
- v18.0 (2025-10-28): 691 identifiers, 0.975 still live at v19.0, 17 revoked, 0 deprecated, 17 recoverable via revoked-by; half-life never reached.
- Every revoked identifier in the corpus resolves to a live identifier through
  the published revocation graph.

## 4. Silent semantic drift (identifier-stable techniques only)

- v7.0: 415 identifier-stable techniques; 0.749 have edited descriptions by v19.0; mean token Jaccard 0.808; 0.386 substantially rewritten (J < 0.8).
- v11.0: 563 identifier-stable techniques; 0.465 have edited descriptions by v19.0; mean token Jaccard 0.895; 0.208 substantially rewritten (J < 0.8).
- v15.0: 621 identifier-stable techniques; 0.275 have edited descriptions by v19.0; mean token Jaccard 0.956; 0.087 substantially rewritten (J < 0.8).
- v18.0: 674 identifier-stable techniques; 0.061 have edited descriptions by v19.0; mean token Jaccard 0.997; 0.003 substantially rewritten (J < 0.8).

## 5. Growth decomposition

- 5516 group-technique edges added across all Enterprise
  transitions; 2442 belong to groups newly added to ATT&CK.
- Of the 3074 added for pre-existing groups: 1752 genuine new intelligence, 330 new technique, 487 sub-technique refinement, 505 revocation re-mapping.
- Bookkeeping share: 992/3074 = 0.323.

  - v6.0 to v7.0: 0.750 bookkeeping (1059 edges for pre-existing groups).
  - v18.0 to v19.0: 0.470 bookkeeping (164 edges for pre-existing groups).
  - v12.0 to v13.0: 0.380 bookkeeping (71 edges for pre-existing groups).
  - v14.0 to v15.0: 0.340 bookkeeping (100 edges for pre-existing groups).

## 6. Attribution under vocabulary mismatch (k = 10, analysis at v19.0)

- artefact at v1.0: contemporaneous 0.696, naive 0.274, normalized 0.450, oracle 0.912; drift penalty 42.2 pp [37.8, 46.8]; recovered 0.42.
- artefact at v6.0: contemporaneous 0.684, naive 0.222, normalized 0.468, oracle 0.850; drift penalty 46.2 pp [41.6, 51.0]; recovered 0.53.
- artefact at v7.0: contemporaneous 0.810, naive 0.740, normalized 0.750, oracle 0.862; drift penalty 7.0 pp [4.4, 9.8]; recovered 0.14.
- artefact at v12.0: contemporaneous 0.840, naive 0.820, normalized 0.832, oracle 0.878; drift penalty 2.0 pp [0.6, 3.8]; recovered 0.60.
- artefact at v18.0: contemporaneous 0.860, naive 0.844, normalized 0.858, oracle 0.858; drift penalty 1.6 pp [0.6, 2.8]; recovered 0.88.

Back-projection loss (for transparency: all three legacy conditions consume
the same back-projected observation; only the oracle sees the full modern set):
- v1.0: 389 of 697 modern techniques have no v1.0 ancestor; profiles retain 0.618 of their distinct identifiers.
- v7.0: 155 of 697 modern techniques have no v7.0 ancestor; profiles retain 0.903 of their distinct identifiers.
- v18.0: 7 of 697 modern techniques have no v18.0 ancestor; profiles retain 0.998 of their distinct identifiers.

## 7. Conclusion flips

- artefact at v1.0: the named actor changes in 0.722 of observations; 0.712 change to a wrong actor; normalization changes the verdict in 0.368.
- artefact at v6.0: the named actor changes in 0.790 of observations; 0.774 change to a wrong actor; normalization changes the verdict in 0.442.
- artefact at v7.0: the named actor changes in 0.116 of observations; 0.100 change to a wrong actor; normalization changes the verdict in 0.028.
- artefact at v12.0: the named actor changes in 0.070 of observations; 0.054 change to a wrong actor; normalization changes the verdict in 0.016.
- artefact at v18.0: the named actor changes in 0.022 of observations; 0.022 change to a wrong actor; normalization changes the verdict in 0.020.

- mitigation leaderboard frozen at v6.0: Kendall tau 0.665 naive, 0.968 normalized; rank-1 changed: yes.
- mitigation leaderboard frozen at v12.0: Kendall tau 0.983 naive, 0.998 normalized; rank-1 changed: no.
- mitigation leaderboard frozen at v17.0: Kendall tau 0.976 naive, 1.000 normalized; rank-1 changed: yes.
- mitigation leaderboard frozen at v18.0: Kendall tau 0.978 naive, 0.998 normalized; rank-1 changed: no.

## 8. Coverage claims under a frozen capability (re-measured at v9.0)

- frozen at v6.0: claimed 97.0%, naive 21.9%, normalized 43.1%; identifier artefact 21.2 pp.

Prevalence-weighted (answering the long-tail objection):
- frozen at v6.0: artefact +16.50 pp unweighted, +20.01 pp prevalence-weighted.
- frozen at v10.0: artefact +1.58 pp unweighted, +1.43 pp prevalence-weighted.
- frozen at v18.0: artefact +2.15 pp unweighted, +1.57 pp prevalence-weighted.
- the fifteen most-referenced techniques carry 0.285 of all `uses` edges at v9.0.

## 9. Deployed corpora

- ctibench-ate: 120 distinct labels, 397 instances, 0 sub-technique identifiers; best fit v14.0 (0.942); **no release makes every label simultaneously valid**; 8 invalid at v19.2 (0.067 of labels, 0.020 of instances), 1 repairable, 7 not.
- rcatt: 215 distinct labels, 6235 instances, 0 sub-technique identifiers; best fit v4.0 (1.000); all labels simultaneously live in 8 releases (v4.0–v6.3); 107 invalid at v19.2 (0.498 of labels, 0.380 of instances), 99 repairable, 8 not.
- tram-bootstrap: 537 distinct labels, 25770 instances, 344 sub-technique identifiers; best fit v13.0 (0.939); **no release makes every label simultaneously valid**; 43 invalid at v19.2 (0.080 of labels, 0.025 of instances), 43 repairable, 0 not.
- tram2: 50 distinct labels, 5143 instances, 24 sub-technique identifiers; best fit v8.2 (1.000); all labels simultaneously live in 18 releases (v8.2–v16.1); 2 invalid at v19.2 (0.040 of labels, 0.033 of instances), 2 repairable, 0 not.

- Version declarations: 0 found across 19 documentation files in 3 deployed corpora.

## 10. The most recent revocation wave

- v18.1 to v19.2: 17 live techniques revoked, including the whole T1562 family.
- Blast radius on the v18.1 graph: 84 group-technique edges, 155 software-technique edges, 47 mitigations, 17 detection relationships; 52 of 168 group profiles lose at least one identifier.
- T1562.001 was ranked 33 of 599 techniques by `uses` edges in the release it left.
