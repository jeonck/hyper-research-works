#!/usr/bin/env python3
"""Figures and LaTeX tables for the ATT&CK ontology-drift paper."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "data" / "results"
FIG = ROOT / "paper" / "figures"
TAB = ROOT / "paper" / "tables"

plt.rcParams.update({
    "figure.dpi": 160, "savefig.dpi": 300, "font.size": 8,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": 0.25, "grid.linewidth": 0.5,
    "legend.frameon": False, "figure.constrained_layout.use": True,
})
C = {"a": "#1b4965", "b": "#c1666b", "c": "#5f8d4e", "d": "#d08c34", "e": "#7d6b91"}


def load(name):
    return json.loads((RES / name).read_text())


def fig1_growth_churn(e123):
    e = e123["enterprise-attack"]
    ch = e["churn"]
    x = [c["to_date"][:7] for c in ch]
    fig, ax = plt.subplots(2, 1, figsize=(6.4, 4.2), sharex=True)
    idx0 = list(range(len(ch)))
    ax[0].plot(idx0, [c["live_to"] for c in ch], "o-", color=C["a"], ms=3, lw=1.4,
               label="live techniques")
    ax[0].annotate(f"v{ch[0]['from']}: {ch[0]['live_from']}", xy=(0, ch[0]["live_to"]),
                   xytext=(0.4, ch[0]["live_to"] - 60), fontsize=6, color=C["a"])
    ax[0].set_ylabel("live techniques")
    ax[0].legend(loc="upper left")
    w = 0.38
    idx = range(len(ch))
    ax[1].bar([i - w / 2 for i in idx], [c["added"] for c in ch], w,
              color=C["c"], label="added")
    ax[1].bar([i + w / 2 for i in idx], [-(c["newly_revoked"] + c["newly_deprecated"])
                                        for c in ch], w, color=C["b"],
              label="revoked / deprecated")
    ax[1].plot(list(idx), [c["desc_changed"] for c in ch], "s--", color=C["d"], ms=3,
               lw=1.1, label="descriptions rewritten (ID stable)")
    ax[1].axhline(0, color="k", lw=0.6)
    ax[1].set_xticks(list(idx))
    ax[1].set_xticklabels([f"v{c['to']}" for c in ch], rotation=60, fontsize=6)
    ax[1].set_ylabel("techniques")
    ax[1].legend(loc="upper left", ncol=1, fontsize=6)
    fig.savefig(FIG / "fig1_growth_churn.pdf")
    fig.savefig(FIG / "fig1_growth_churn.png")
    plt.close(fig)


def fig2_survival(e123):
    e = e123["enterprise-attack"]
    fig, ax = plt.subplots(1, 2, figsize=(6.4, 2.5))
    for src in ("1.0", "4.0", "6.0", "7.0", "11.0", "15.0"):
        pts = [s for s in e["survival"] if s["src"] == src]
        if not pts:
            continue
        ax[0].plot([p["tgt_date"][:4] for p in pts], [p["survival_rate"] for p in pts],
                   "o-", ms=2.5, lw=1.2, label=f"v{src}")
    ax[0].set_ylabel("identifiers still live")
    ax[0].set_ylim(0, 1.02)
    ax[0].legend(fontsize=6, ncol=2, title="source release", title_fontsize=6)
    ax[0].tick_params(axis="x", rotation=45, labelsize=6)

    latest = [s for s in e["survival"] if s["tgt"] == e["releases"][-1]["version"]]
    ax[1].bar(range(len(latest)), [s["survival_rate"] for s in latest], color=C["a"])
    ax[1].bar(range(len(latest)),
              [(s["recoverable_via_revoked_by"]) / s["n"] for s in latest],
              bottom=[s["survival_rate"] for s in latest], color=C["c"],
              label="recoverable by ATT&CK-Norm")
    ax[1].set_xticks(range(len(latest)))
    ax[1].set_xticklabels([f"v{s['src']}" for s in latest], rotation=60, fontsize=6)
    ax[1].set_ylabel(f"share at v{e['releases'][-1]['version']}")
    ax[1].legend(fontsize=6)
    fig.savefig(FIG / "fig2_survival.pdf")
    fig.savefig(FIG / "fig2_survival.png")
    plt.close(fig)


def fig3_semantic(e123):
    e = e123["enterprise-attack"]
    latest = e["releases"][-1]["version"]
    pts = [s for s in e["semantic"] if s["tgt"] == latest]
    fig, ax = plt.subplots(figsize=(3.3, 2.4))
    ax.plot([f"v{p['src']}" for p in pts], [p["desc_changed_frac"] for p in pts],
            "o-", color=C["b"], ms=3, lw=1.3, label="description edited")
    ax.plot([f"v{p['src']}" for p in pts], [p["substantial_frac"] for p in pts],
            "s-", color=C["d"], ms=3, lw=1.3, label="substantial rewrite (J<0.8)")
    ax.plot([f"v{p['src']}" for p in pts], [p["mean_token_jaccard"] for p in pts],
            "^-", color=C["a"], ms=3, lw=1.3, label="mean token Jaccard")
    ax.tick_params(axis="x", rotation=60, labelsize=6)
    ax.set_ylabel(f"vs. v{latest}, ID-stable techniques")
    ax.legend(fontsize=6)
    fig.savefig(FIG / "fig3_semantic_drift.pdf")
    fig.savefig(FIG / "fig3_semantic_drift.png")
    plt.close(fig)


def fig4_growth(e4):
    t = e4["enterprise-attack"]["transitions"]
    keys = [("genuine_new_intel", "genuine new intelligence", C["a"]),
            ("new_technique_intel", "new technique, new edge", C["c"]),
            ("ontology_refinement", "sub-technique refinement", C["d"]),
            ("revocation_remap", "revocation re-mapping", C["b"])]
    fig, ax = plt.subplots(figsize=(6.4, 2.6))
    bottom = [0.0] * len(t)
    idx = list(range(len(t)))
    for k, lab, col in keys:
        vals = []
        for r in t:
            base = r["total_added"] - r["new_actor"]
            vals.append(100 * r[k] / base if base else 0.0)
        ax.bar(idx, vals, 0.75, bottom=bottom, color=col, label=lab)
        bottom = [b + v for b, v in zip(bottom, vals)]
    ax.set_xticks(idx)
    ax.set_xticklabels([f"v{r['from']}→v{r['to']}" for r in t], rotation=70, fontsize=6)
    ax.set_ylabel("% of new edges for pre-existing groups")
    ax.legend(fontsize=6, ncol=2)
    fig.savefig(FIG / "fig4_growth_decomposition.pdf")
    fig.savefig(FIG / "fig4_growth_decomposition.png")
    plt.close(fig)


def fig5_attribution(e5):
    fig, ax = plt.subplots(1, 2, figsize=(6.4, 2.5))
    rows = [r for r in e5 if r["k"] == 10]
    xs = [f"v{r['v']}" for r in rows]
    for key, lab, col, mk in (("oracle_top1", "oracle (modern vocabulary)", C["e"], "^"),
                              ("contemporaneous_top1", "contemporaneous (no drift)", C["a"], "o"),
                              ("normalized_top1", "ATT&CK-Norm", C["c"], "s"),
                              ("naive_top1", "naive cross-version", C["b"], "v")):
        ax[0].plot(xs, [r[key] for r in rows], mk + "-", color=col, ms=3, lw=1.3, label=lab)
    ax[0].set_ylabel("top-1 attribution accuracy")
    ax[0].tick_params(axis="x", rotation=60, labelsize=6)
    ax[0].legend(fontsize=5.5)
    ax[0].set_title("k = 10 observed techniques", fontsize=7)

    for k, col, mk in ((5, C["a"], "o"), (10, C["b"], "s"), (20, C["c"], "^")):
        rk = [r for r in e5 if r["k"] == k]
        ax[1].plot([f"v{r['v']}" for r in rk],
                   [100 * r["drift_penalty_top1"] for r in rk], mk + "-", color=col,
                   ms=3, lw=1.3, label=f"k={k}")
        lo = [100 * r["drift_penalty_ci"][0] for r in rk]
        hi = [100 * r["drift_penalty_ci"][1] for r in rk]
        ax[1].fill_between([f"v{r['v']}" for r in rk], lo, hi, color=col, alpha=0.15)
    ax[1].axhline(0, color="k", lw=0.6)
    ax[1].set_ylabel("drift penalty (pp, top-1)")
    ax[1].tick_params(axis="x", rotation=60, labelsize=6)
    ax[1].legend(fontsize=6)
    fig.savefig(FIG / "fig5_attribution.pdf")
    fig.savefig(FIG / "fig5_attribution.png")
    plt.close(fig)


def fig6_coverage(e6):
    rows = [r for r in e6["portfolios"] if r["w"] == "19.2" and r["relation"] == "mitigates"]
    if not rows:
        rows = [r for r in e6["portfolios"]
                if r["w"] == max(x["w"] for x in e6["portfolios"]) and r["relation"] == "mitigates"]
    fig, ax = plt.subplots(1, 2, figsize=(6.4, 2.4))
    xs = [f"v{r['v']}" for r in rows]
    ax[0].plot(xs, [100 * r["coverage_at_v"] for r in rows], "o-", color=C["a"], ms=3,
               lw=1.3, label="claimed at release V")
    ax[0].plot(xs, [100 * r["coverage_normalized"] for r in rows], "s-", color=C["c"],
               ms=3, lw=1.3, label="re-measured, normalized")
    ax[0].plot(xs, [100 * r["coverage_naive"] for r in rows], "v-", color=C["b"], ms=3,
               lw=1.3, label="re-measured, naive")
    ax[0].set_ylabel("reported coverage (%)")
    ax[0].tick_params(axis="x", rotation=60, labelsize=6)
    ax[0].legend(fontsize=6)

    sweep = e6["random_sweep"]
    xs2 = [f"v{s['v']}" for s in sweep]
    ax[1].plot(xs2, [s["mean_naive_error_pp"] for s in sweep], "v-", color=C["b"], ms=3,
               lw=1.3, label="naive")
    ax[1].plot(xs2, [s["mean_normalized_error_pp"] for s in sweep], "s-", color=C["c"],
               ms=3, lw=1.3, label="normalized")
    ax[1].axhline(0, color="k", lw=0.6)
    ax[1].set_ylabel("coverage error (pp)")
    ax[1].tick_params(axis="x", rotation=60, labelsize=6)
    ax[1].legend(fontsize=6)
    ax[1].set_title("random 30% portfolios", fontsize=7)
    fig.savefig(FIG / "fig6_coverage.pdf")
    fig.savefig(FIG / "fig6_coverage.png")
    plt.close(fig)


def fig7_artifacts(e7):
    fig, ax = plt.subplots(figsize=(3.4, 2.4))
    for (name, d), col in zip(e7.items(), [C["a"], C["b"], C["c"], C["d"]]):
        ax.plot([f"v{c['version']}" for c in d["curve"]],
                [c["live_frac"] for c in d["curve"]], "-", color=col, lw=1.4,
                label=f"{name} (n={d['n_unique_ids']})")
    step = 4
    ticks = [i for i in range(len(next(iter(e7.values()))["curve"])) if i % step == 0]
    ax.set_xticks(ticks)
    ax.set_xticklabels([f"v{next(iter(e7.values()))['curve'][i]['version']}" for i in ticks],
                       rotation=60, fontsize=6)
    ax.set_ylabel("share of labels live")
    ax.set_ylim(0, 1.02)
    ax.legend(fontsize=5.5)
    fig.savefig(FIG / "fig7_artifact_validity.pdf")
    fig.savefig(FIG / "fig7_artifact_validity.png")
    plt.close(fig)


def main() -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    TAB.mkdir(parents=True, exist_ok=True)
    e123 = load("e1_e2_e3.json")
    e4 = load("e4_growth.json")
    e5 = load("e5_attribution.json")
    e6 = load("e6_coverage.json")
    e7 = load("e7_artifacts.json")
    fig1_growth_churn(e123)
    fig2_survival(e123)
    fig3_semantic(e123)
    fig4_growth(e4)
    fig5_attribution(e5)
    fig6_coverage(e6)
    fig7_artifacts(e7)
    fig8_flips(load("e10_conclusion_flips.json"))
    print("figures written to", FIG, file=sys.stderr)




def fig8_flips(e10):  # appended: conclusion-flip figure
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(6.4, 2.4))
    a = e10["attribution_verdicts"]
    xs = [f"v{r['v']}" for r in a]
    ax[0].plot(xs, [100 * r["verdict_changed_frac"] for r in a], "o-", color=C["b"],
               ms=3, lw=1.3, label="named actor changes")
    ax[0].plot(xs, [100 * r["verdict_changed_and_now_wrong_frac"] for r in a], "s-",
               color=C["d"], ms=3, lw=1.3, label="changes to a wrong actor")
    ax[0].plot(xs, [100 * r["normalization_changed_verdict_frac"] for r in a], "^-",
               color=C["c"], ms=3, lw=1.3, label="normalization changes the verdict")
    ax[0].set_ylabel("% of observations")
    ax[0].tick_params(axis="x", rotation=60, labelsize=6)
    ax[0].legend(fontsize=5.5)
    ax[0].set_title("attribution verdicts", fontsize=7)

    b = e10["coverage_rankings"]
    xs2 = [f"v{r['v']}" for r in b]
    ax[1].plot(xs2, [r["tau_naive"] for r in b], "v-", color=C["b"], ms=3, lw=1.3,
               label="naive")
    ax[1].plot(xs2, [r["tau_normalized"] for r in b], "s-", color=C["c"], ms=3, lw=1.3,
               label="ATT&CK-Norm")
    ax[1].set_ylabel("Kendall τ vs. original ranking")
    ax[1].set_ylim(0.6, 1.02)
    ax[1].tick_params(axis="x", rotation=60, labelsize=6)
    ax[1].legend(fontsize=6)
    ax[1].set_title("mitigation coverage leaderboard", fontsize=7)
    fig.savefig(FIG / "fig8_conclusion_flips.pdf")
    fig.savefig(FIG / "fig8_conclusion_flips.png")
    plt.close(fig)


if __name__ == "__main__":
    main()
