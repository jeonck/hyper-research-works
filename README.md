# Ontology drift in cyber threat intelligence

A measurement study of the MITRE ATT&CK knowledge base as a *versioned* object,
and of what its versioning costs the analytics built on top of it.

The work was produced with the `hyperresearch` adversarial research pipeline:
the research question was decomposed, a literature corpus was swept in parallel,
four adversarial investigators audited the study's own claims and experimental
design, three independent drafts were written and synthesised into one
manuscript, and a four-critic panel then audited the manuscript itself. Several
of the study's headline claims were corrected or narrowed by that process, and
the record of those corrections is kept in `research/runs/`.

## Layout

| Path | What is there |
|---|---|
| `paper/` | the manuscript's figures and tables |
| `research/notes/final_report_attack-ontology-drift-cti-85bc51.md` | the manuscript |
| `research/runs/attack-ontology-drift-cti-85bc51/` | the full pipeline record: decomposition, contradiction graph, loci, the four investigators' committed positions, the reconciliation, the three drafts, the critic findings and the patch log |
| `research/notes/` | the evidence corpus, one note per source |
| `code/` | the reproduction package — see `code/README.md` |
| `data/results/` | every computed result, as JSON |

## Reproducing the results

```bash
git clone --depth 1 https://github.com/mitre-attack/attack-stix-data /home/user/mitre-attack/attack-stix-data
git clone --depth 1 https://github.com/maveryn/cti-bench  /home/user/ext/cti-bench
git clone --depth 1 https://github.com/vlegoy/rcATT       /home/user/ext/rcATT
git clone --depth 1 https://github.com/center-for-threat-informed-defense/tram /home/user/ext/tram
python -m venv .venv && .venv/bin/pip install matplotlib
bash code/run_all.sh
```

Everything is computed from public artefacts. No API keys, no network access
beyond those clones, and every stochastic component is seeded.

## The short version of the finding

ATT&CK's identifier accounting is sound and almost nobody uses it. Its semantic
change — techniques rewritten, re-tactic'd, or renamed in place under a stable
identifier — is not accounted for at all, by anyone, and no mechanism in the
ecosystem detects it. The damage that follows is measurable, it changes
conclusions rather than merely scores, and the part of it that a crosswalk can
repair is the part the ecosystem was already equipped to handle.
