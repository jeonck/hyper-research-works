#!/usr/bin/env bash
# Reproduce every number in the paper from a clean checkout.
#
#   git clone --depth 1 https://github.com/mitre-attack/attack-stix-data \
#       /home/user/mitre-attack/attack-stix-data
#   git clone --depth 1 https://github.com/maveryn/cti-bench /home/user/ext/cti-bench
#   git clone --depth 1 https://github.com/vlegoy/rcATT      /home/user/ext/rcATT
#   git clone --depth 1 https://github.com/center-for-threat-informed-defense/tram \
#       /home/user/ext/tram
#   python -m venv .venv && .venv/bin/pip install matplotlib
#   bash code/run_all.sh
set -euo pipefail
cd "$(dirname "$0")/.."
PY=${PY:-.venv/bin/python}

run() { echo; echo "### $1"; shift; "$PY" "$@"; }

# record the exact inputs so the header line of the reporting contract can be filled in
ATTACK_STIX_REPO=${ATTACK_STIX_REPO:-/home/user/mitre-attack/attack-stix-data}
HYPER_EXT=${HYPER_EXT:-/home/user/ext}
export ATTACK_STIX_REPO HYPER_EXT
{
  echo "{"
  echo "  \"attack-stix-data\": \"$(git -C "$ATTACK_STIX_REPO" rev-parse HEAD 2>/dev/null)\","
  for r in cti-bench rcATT tram DeTTECT; do
    echo "  \"$r\": \"$(git -C "$HYPER_EXT/$r" rev-parse HEAD 2>/dev/null)\","
  done
  echo "  \"recorded\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\""
  echo "}"
} > data/results/inputs.json

run "extract the release corpus"            code/01_extract.py
run "E1-E3 churn, survival, semantic drift" code/02_churn_survival.py
run "E4 knowledge-growth decomposition"     code/03_growth_decomposition.py
run "E5 controlled attribution experiment"  code/04_attribution.py
run "E6 coverage-claim drift"               code/05_coverage.py
run "E7 deployed-corpus label validity"     code/06_artifacts.py
run "E5b/E2b robustness and half-life"      code/09_robustness.py
run "E5c back-projection diagnostics"       code/11_backprojection_diag.py
run "E8 the v19 revocation wave"            code/12_case_v19.py
run "E9 version declarations in corpora"    code/13_version_declaration.py
run "E10 conclusion flips"                  code/14_conclusion_flips.py
run "E6b prevalence-weighted coverage"      code/15_prevalence_weighted.py
run "E11 version-metadata reliability"      code/18_version_metadata.py
run "E12 temporal structure of the risk"    code/19_temporal_structure.py
run "E13 tactic layer and revocation arity" code/23_tactic_layer.py
run "E14 noise, stratification, archival"   code/24_noise_and_stratification.py
run "E18 trained classifier across eras"    code/34_real_classifier.py
run "E19 end-to-end cases on real artefacts" code/35_end_to_end_cases.py
run "E20 rewrite-threshold validation"      code/36_semantic_validation.py
run "E21 corrections, intervals, Mobile/ICS" code/37_statistics.py
run "E22 CWE and CAPEC control"             code/38_cwe_capec_drift.py
run "figures"                               code/07_figures.py
run "tables"                                code/10_tables.py
run "evidence digest"                       code/16_evidence_digest.py

echo
echo "done — results in data/results/, figures in paper/figures/, tables in paper/tables/"
echo "corpus-side checks (need the research vault, not the ATT&CK data):"
echo "  $PY code/25_vault_integrity.py     # note front-matter/body integrity"
echo "  $PY code/17_reference_registry.py  # canonical reference numbering"
echo "  $PY code/08_evidence_notes.py      # write measurements back as vault notes"
echo "  $PY code/39_pin_rate_survey.py     # E23: needs network (arXiv API + hyperresearch fetch)"
echo "  $PY code/40_llm_extractor.py       # E24: needs a local ollama with gemma3:4b and llama3.2:3b (~1 h)"
echo "  $PY code/test_attacknorm.py        # self-check of the ledger tool"
