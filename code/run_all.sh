#!/usr/bin/env bash
# Reproduce every number in the paper from a clean checkout.
#
#   git clone --depth 1 https://github.com/mitre-attack/attack-stix-data \
#       /home/user/mitre-attack/attack-stix-data
#   git clone --depth 1 https://github.com/maveryn/cti-bench        /home/user/ext/cti-bench
#   git clone --depth 1 https://github.com/vlegoy/rcATT             /home/user/ext/rcATT
#   git clone --depth 1 https://github.com/center-for-threat-informed-defense/tram \
#       /home/user/ext/tram
#   python -m venv .venv && .venv/bin/pip install matplotlib
#   bash code/run_all.sh
set -euo pipefail
cd "$(dirname "$0")/.."
PY=${PY:-.venv/bin/python}

echo "[1/8] extracting release corpus"          && $PY code/01_extract.py
echo "[2/8] churn, survival, semantic drift"    && $PY code/02_churn_survival.py
echo "[3/8] knowledge-growth decomposition"     && $PY code/03_growth_decomposition.py
echo "[4/8] controlled attribution experiment"  && $PY code/04_attribution.py
echo "[5/8] coverage-claim drift"               && $PY code/05_coverage.py
echo "[6/8] deployed-corpus label validity"     && $PY code/06_artifacts.py
echo "[7/8] robustness, half-life, diagnostics" && $PY code/09_robustness.py \
                                                 && $PY code/11_backprojection_diag.py \
                                                 && $PY code/12_case_v19.py \
                                                 && $PY code/13_version_declaration.py \
                                                 && $PY code/14_conclusion_flips.py \
                                                 && $PY code/15_prevalence_weighted.py \
                                                 && $PY code/18_version_metadata.py
echo "[8/8] figures, tables and digest"          && $PY code/07_figures.py \
                                                 && $PY code/10_tables.py \
                                                 && $PY code/16_evidence_digest.py
echo "done — results in data/results/, figures in paper/figures/, tables in paper/tables/"
