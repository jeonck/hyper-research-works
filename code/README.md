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
| `07_figures.py`, `10_tables.py` | every figure and table in the paper |
| `attackdrift.py` | shared loading, lineage and the ATT&CK-Norm implementation |

Run them in order with `bash code/run_all.sh`.

## ATT&CK-Norm

The normalization protocol evaluated in the paper is `attackdrift.normalize`:
transitive `revoked-by` resolution against the target release, removal of
identifiers that are deprecated or absent there, and an optional roll-up of
orphaned sub-technique identifiers to a surviving parent. It is deliberately
small — the point of the paper is that this much is enough to repair a
measurable share of the damage, and that the remainder is not repairable by
identifier arithmetic at all.
