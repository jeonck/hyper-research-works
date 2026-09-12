# Reproduction package — ATT&CK ontology drift

Everything in the paper is computed from public data by the scripts in this
directory. No API keys, no network access beyond the initial clones, no
randomness that is not seeded (`SEED = 20260912`).

## Inputs

| Artefact | Source | Role |
|---|---|---|
| ATT&CK STIX releases | `github.com/mitre-attack/attack-stix-data` | the measurement corpus: 41 Enterprise, 38 Mobile, 27 ICS releases |
| CTIBench | `github.com/maveryn/cti-bench` | deployed benchmark labels (CTI-ATE) |
| rcATT | `github.com/vlegoy/rcATT` | deployed training corpus, pre-sub-technique era |
| TRAM / TRAM 2 | `github.com/center-for-threat-informed-defense/tram` | deployed training corpora |

## Scripts

| Script | Produces |
|---|---|
| `01_extract.py` | `data/attack_drift.db` — every release, normalized |
| `02_churn_survival.py` | E1 churn, E2 identifier survival, E3 semantic drift |
| `03_growth_decomposition.py` | E4 growth decomposition |
| `04_attribution.py` | E5 controlled attribution experiment |
| `05_coverage.py` | E6 coverage-claim drift |
| `06_artifacts.py` | E7 label validity of deployed corpora |
| `09_robustness.py` | E5b scorer/profile robustness, E2b half-life |
| `11_backprojection_diag.py` | E5c back-projection information loss |
| `12_case_v19.py` | E8 blast radius of the v19.0 revocation wave |
| `12_case_v19.py` | E8 blast radius of the v19.0 revocation wave |
| `13_version_declaration.py` | E9 whether deployed corpora declare an ATT&CK release |
| `14_conclusion_flips.py` | E10 attribution verdict instability and leaderboard reordering |
| `15_prevalence_weighted.py` | E6b prevalence-weighted coverage drift |
| `18_version_metadata.py` | E11 is `x_mitre_version` a usable change signal |
| `19_temporal_structure.py` | E12 staleness clocks, recurrence hazard, leading indicators |
| `23_tactic_layer.py` | E13 the tactic layer and the arity of the revocation relation |
| `24_noise_and_stratification.py` | E14 noise factorial, specificity stratification, archival control |
| `25_vault_integrity.py` | E15 corpus integrity check over the evidence notes |
| `07_figures.py`, `10_tables.py`, `16_evidence_digest.py` | every figure, table and quoted number in the paper |
| `26_manuscript_check.py` | headings, length, citation density and quote integrity of the manuscript |
| `27_to_latex.py` | LaTeX export for journal submission |
| `28_number_provenance.py` | every number in the prose traced back to a computed result |
| `31_sources_section.py`, `32_cite_pairs.py` | the reference list, and the citation-sentence pairs the cite-check verifies |
| `33_build_web.py` | the reading edition of the manuscript as a single web page; `WEB_OUT` and `WEB_FIG_PREFIX` target it at `docs/` for GitHub Pages |
| `attackdrift.py` | shared loading, lineage and the ATT&CK-Norm implementation |

Run them in order with `bash code/run_all.sh`.

## ATT&CK-Norm

The normalization protocol evaluated in the paper is
`attackdrift.normalize_with_ledger`: transitive `revoked-by` resolution against
the target release, identifiers that are deprecated or absent there dropped and
counted rather than silently discarded, and a residual ledger reporting what was
kept, merged, demoted across abstraction levels, and dropped.

Roll-up to a surviving parent is **off by default**. The branch fires three
times in 12,027 resolutions across every domain and major release, so it buys
nothing measurable while being able to fabricate a parent-level assertion the
artefact never made. `normalize()` remains as a set-returning convenience
wrapper, but reporting only the set is the reporting failure this study is
about.
