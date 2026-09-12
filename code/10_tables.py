#!/usr/bin/env python3
"""Emit the manuscript's tables as markdown, formatted directly from the results.

Every number in the paper comes from here, so the prose can never disagree with
the experiments.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "data" / "results"
TAB = ROOT / "paper" / "tables"


def load(n):
    return json.loads((RES / n).read_text())


def w(name: str, text: str) -> None:
    (TAB / name).write_text(text.rstrip() + "\n")
    print("  wrote", name)


def main() -> None:
    TAB.mkdir(parents=True, exist_ok=True)
    e123, e4 = load("e1_e2_e3.json"), load("e4_growth.json")
    e5, e6, e7 = load("e5_attribution.json"), load("e6_coverage.json"), load("e7_artifacts.json")
    rb = load("e5b_e2b_robustness.json")
    ent = e123["enterprise-attack"]

    # T1 corpus
    rows = ["| Domain | Releases analysed (major / all) | First | Last |",
            "|---|---|---|---|"]
    all_counts = {"enterprise-attack": 41, "mobile-attack": 38, "ics-attack": 27}
    for dom in ("enterprise-attack", "mobile-attack", "ics-attack"):
        r = e123[dom]["releases"]
        rows.append(f"| {dom.replace('-attack','').capitalize()} | {len(r)} / "
                    f"{all_counts[dom]} | v{r[0]['version']} ({r[0]['date']}) | "
                    f"v{r[-1]['version']} ({r[-1]['date']}) |")
    w("t1_corpus.md", "\n".join(rows))

    # T2 churn
    rows = ["| Transition | Date | Live | Added | Revoked | Deprecated | Renamed | "
            "Desc. rewritten | Detection rewritten | Tactic changed | J(ID) | "
            "Edges +/- |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for c in ent["churn"]:
        rows.append(f"| v{c['from']}→v{c['to']} | {c['to_date']} | {c['live_to']} | "
                    f"{c['added']} | {c['newly_revoked']} | {c['newly_deprecated']} | "
                    f"{c['renamed']} | {c['desc_changed']} | {c['detection_changed']} | "
                    f"{c['tactic_changed']} | {c['jaccard_id']:.3f} | "
                    f"+{c['group_edges_added']}/−{c['group_edges_removed']} |")
    w("t2_churn.md", "\n".join(rows))

    # T3 survival + half-life
    latest = ent["releases"][-1]["version"]
    hl = {h["src"]: h for h in rb["half_life"]}
    rows = [f"| Source release | Date | Identifiers | Live at v{latest} | Survival | "
            "Revoked | Deprecated | Recoverable | Half-life |",
            "|---|---|---|---|---|---|---|---|---|"]
    for s in [x for x in ent["survival"] if x["tgt"] == latest]:
        h = hl.get(s["src"], {})
        hstr = (f"v{h['half_life_release']} ({h['half_life_years']:.1f} y)"
                if h.get("half_life_release") else "not reached")
        rows.append(f"| v{s['src']} | {s['src_date']} | {s['n']} | {s['live']} | "
                    f"{s['survival_rate']:.3f} | {s['revoked']} | {s['deprecated']} | "
                    f"{s['recoverable_via_revoked_by']} | {hstr} |")
    w("t3_survival.md", "\n".join(rows))

    # T4 semantic
    rows = [f"| Source release | ID-stable techniques | Description edited | "
            f"Mean token Jaccard | Substantial rewrite (J<0.8) |", "|---|---|---|---|---|"]
    for s in [x for x in ent["semantic"] if x["tgt"] == latest]:
        rows.append(f"| v{s['src']} | {s['id_stable']} | {s['desc_changed_frac']:.3f} | "
                    f"{s['mean_token_jaccard']:.3f} | {s['substantial_frac']:.3f} |")
    w("t4_semantic.md", "\n".join(rows))

    # T5 growth decomposition
    rows = ["| Transition | New edges (pre-existing groups) | Genuine new intel | "
            "New technique | Sub-technique refinement | Revocation re-mapping | "
            "Bookkeeping share |", "|---|---|---|---|---|---|---|"]
    for r in e4["enterprise-attack"]["transitions"]:
        base = r["total_added"] - r["new_actor"]
        if not base:
            continue
        book = r["ontology_refinement"] + r["revocation_remap"]
        rows.append(f"| v{r['from']}→v{r['to']} | {base} | {r['genuine_new_intel']} | "
                    f"{r['new_technique_intel']} | {r['ontology_refinement']} | "
                    f"{r['revocation_remap']} | {book/base:.3f} |")
    c = e4["enterprise-attack"]["cumulative"]
    base = c["total_added"] - c["new_actor"]
    book = c["ontology_refinement"] + c["revocation_remap"]
    rows.append(f"| **All transitions** | **{base}** | **{c['genuine_new_intel']}** | "
                f"**{c['new_technique_intel']}** | **{c['ontology_refinement']}** | "
                f"**{c['revocation_remap']}** | **{book/base:.3f}** |")
    w("t5_growth.md", "\n".join(rows))

    # T6 attribution
    rows = ["| Artefact vocabulary | k | Groups | OOV | Contemporaneous | Naive | "
            "ATT&CK-Norm | Oracle | Drift penalty (pp) [95% CI] | Recovered |",
            "|---|---|---|---|---|---|---|---|---|---|"]
    for r in e5:
        if r["k"] != 10:
            continue
        rec = f"{r['recovery_top1']:.2f}" if r["recovery_top1"] is not None else "n/a"
        rows.append(f"| v{r['v']} ({r['v_date']}) | {r['k']} | {r['n_groups']} | "
                    f"{r['oov_rate']:.3f} | {r['contemporaneous_top1']:.3f} | "
                    f"{r['naive_top1']:.3f} | {r['normalized_top1']:.3f} | "
                    f"{r['oracle_top1']:.3f} | {100*r['drift_penalty_top1']:.1f} "
                    f"[{100*r['drift_penalty_ci'][0]:.1f}, "
                    f"{100*r['drift_penalty_ci'][1]:.1f}] | {rec} |")
    w("t6_attribution.md", "\n".join(rows))

    # T7 robustness
    rows = ["| Vocabulary | Scorer | Software-mediated | Contemporaneous | Naive | "
            "ATT&CK-Norm | Drift penalty (pp) | Norm. gain (pp) |",
            "|---|---|---|---|---|---|---|---|"]
    for r in rb["attribution_robustness"]:
        rows.append(f"| v{r['v']} | {r['scorer']} | "
                    f"{'yes' if r['include_software'] else 'no'} | "
                    f"{r['contemporaneous']:.3f} | {r['naive']:.3f} | "
                    f"{r['normalized']:.3f} | {100*r['drift_penalty']:.1f} | "
                    f"{100*r['norm_gain']:.1f} |")
    w("t7_robustness.md", "\n".join(rows))

    # T8 coverage
    tgt = max(r["w"] for r in e6["portfolios"])
    rows = [f"| Capability frozen at | Portfolio | Claimed then | Naive at v{tgt} | "
            f"Normalized at v{tgt} | Identifier artefact (pp) |",
            "|---|---|---|---|---|---|"]
    for r in e6["portfolios"]:
        if r["w"] == tgt and r["relation"] == "mitigates":
            art = 100 * (r["coverage_normalized"] - r["coverage_naive"])
            rows.append(f"| v{r['v']} ({r['v_date']}) | {r['portfolio']} | "
                        f"{100*r['coverage_at_v']:.1f}% | {100*r['coverage_naive']:.1f}% | "
                        f"{100*r['coverage_normalized']:.1f}% | {art:.1f} |")
    w("t8_coverage.md", "\n".join(rows))

    # T9 artefacts
    rows = ["| Corpus | Distinct labels | Label instances | Sub-technique labels | "
            "Best-fit release | Fit | Releases where all labels valid | "
            "Invalid today | Repairable |", "|---|---|---|---|---|---|---|---|---|"]
    for name, d in e7.items():
        cons = d["fully_consistent_releases"]
        cstr = f"{len(cons)} (v{cons[0]}–v{cons[-1]})" if cons else "**none**"
        rows.append(f"| {name} | {d['n_unique_ids']} | {d['n_label_instances']} | "
                    f"{d['n_subtechnique_ids']} | v{d['best_fit_version']} "
                    f"({d['best_fit_date']}) | {d['best_fit_live_frac']:.3f} | {cstr} | "
                    f"{d['invalid_at_newest']} ({d['invalid_at_newest_frac']:.3f}) | "
                    f"{d['repairable_by_revocation_chain']} |")
    w("t9_artifacts.md", "\n".join(rows))


if __name__ == "__main__":
    main()
