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
| `34_real_classifier.py` | E18 a trained text-to-technique classifier across eras, vocabulary drift separated from data drift |
| `35_end_to_end_cases.py` | E19 two real systems on three real gold sets with verdict flips; named public Navigator layers re-measured |
| `36_semantic_validation.py` | E20 rewrite-threshold sweep, convergent validity, the annotation instrument and the blind pilot |
| `37_statistics.py` | E21 Holm / Benjamini-Hochberg over the attribution rows, Clopper-Pearson / Wilson / Poisson intervals, Mobile and ICS coverage |
| `38_cwe_capec_drift.py` | E22 CWE and CAPEC measured on the same instrument as a same-institution control |
| `39_pin_rate_survey.py` | E23 share of recent arXiv papers using ATT&CK identifiers that declare a release |
| `attacknorm.py`, `test_attacknorm.py` | the residual-ledger tool of Section 8.4 and its self-check |
| `07_figures.py`, `10_tables.py`, `16_evidence_digest.py` | every figure, table and quoted number in the paper |
| `26_manuscript_check.py` | headings, length, citation density and quote integrity of the manuscript |
| `27_to_latex.py` | LaTeX export for journal submission |
| `28_number_provenance.py` | every number in the prose traced back to a computed result |
| `31_sources_section.py`, `32_cite_pairs.py` | the reference list, and the citation-sentence pairs the cite-check verifies |
| `33_build_web.py` | the reading edition of the manuscript as a single web page; `WEB_OUT` and `WEB_FIG_PREFIX` target it at `docs/` for GitHub Pages |
| `attackdrift.py` | shared loading, lineage and the ATT&CK-Norm implementation |

Run them in order with `bash code/run_all.sh`.

## Environment

The scripts read the ATT&CK clone from `$ATTACK_STIX_REPO` and the corpora from
`$HYPER_EXT` (defaults: `/home/user/mitre-attack/attack-stix-data` and
`/home/user/ext`). `run_all.sh` records the commit of every input repository in
`data/results/inputs.json` so the header line of Section 10 can be filled in.
The CWE and CAPEC XML archives are downloaded by `38_cwe_capec_drift.py` into
`$HYPER_EXT/cwe` and `$HYPER_EXT/capec`.

## attacknorm

```bash
.venv/bin/python code/attacknorm.py --input <labels.csv|layer.json|tram.json|cti-ate.tsv> \
    [--domain enterprise-attack] [--from 6.3] [--to 19.2] [--bundle-hash] [--json out.json] [--markdown]
.venv/bin/python code/attacknorm.py --input A.json --compare B.json --to 19.2
.venv/bin/python code/test_attacknorm.py
```

Prints the four header lines of the reporting contract (domain and source
release or inferred provenance interval, target release and bundle hash, the
kept / merged / demoted / dropped ledger, and the cross-time comparability
statement) followed by the ledger detail. A non-empty dropped list is
information, not an error.

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
