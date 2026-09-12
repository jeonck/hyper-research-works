#!/usr/bin/env python3
"""E21: intervals and multiple-comparison control for the reported point estimates.

Consolidates four analyses that answer reviewer objections to bare numbers:

  S1 multiple comparisons   The attribution experiment (E5) reports 18 source
                            vocabularies x 3 k, i.e. 54 rows, each with an exact
                            paired sign-test p-value for the drift penalty and for
                            the normalization gain (04_attribution.py). Holm and
                            Benjamini-Hochberg adjusted p-values are computed
                            across all 54 rows per contrast, and the survivor
                            counts at alpha = 0.05 reported at k = 10 and overall,
                            with the post-restructuring (v7.0+) survivors named.
  S2 recurrence intervals   The restructuring hazard (E12) is 5 events in 47
                            major transitions over 22.05 domain-years. Clopper-
                            Pearson and Wilson intervals for the per-transition
                            hazard, an exact (Garwood, chi-square) interval for
                            the Poisson rate per domain-year, and its reciprocal
                            for years per event.
  S3 proportion intervals   Wilson 95% intervals for every bare small-count
                            proportion in Sections 6-9 that is a simple binomial
                            with a known n: verdict-flip rates (500 trials),
                            coverage points (n = live techniques), the bookkeeping
                            share of added edges, and the v19 blast radius on
                            group profiles. Trial-sampled and census proportions
                            are labelled; a census interval describes sampling
                            variability the catalogue does not actually have and
                            is reported for scale only.
  S4 Mobile / ICS coverage  The E6 frozen-capability coverage measurement
                            (05_coverage.py) re-run for mobile-attack and
                            ics-attack: capability frozen at each major release as
                            the techniques reachable by `mitigates` edges, re-
                            measured at the newest major naively and after
                            ATT&CK-Norm. Mobile's 2018 renumbering (v2.0 -> v3.0)
                            removed every v1.0/v2.0 identifier with no revocation
                            edge, so a capability frozen there must read 0 naively.

Nothing here consumes the RNG streams of the scripts it reads from.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

from scipy.stats import beta, chi2

sys.path.insert(0, str(Path(__file__).resolve().parent))
import attackdrift as ad  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "results"
TABLES = ROOT / "paper" / "tables"
ALPHA = 0.05
Z = 1.959963984540054  # two-sided 95%
POST_RESTRUCTURING_MAJOR = 7


def _load_script(name: str):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(f"{name}.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ----------------------------------------------------------------------
# interval helpers
# ----------------------------------------------------------------------

def wilson(k: int, n: int) -> tuple[float, float]:
    if n == 0:
        return 0.0, 1.0
    p = k / n
    denom = 1 + Z * Z / n
    centre = (p + Z * Z / (2 * n)) / denom
    half = Z * ((p * (1 - p) / n + Z * Z / (4 * n * n)) ** 0.5) / denom
    return max(0.0, centre - half), min(1.0, centre + half)


def clopper_pearson(k: int, n: int) -> tuple[float, float]:
    lo = 0.0 if k == 0 else float(beta.ppf(ALPHA / 2, k, n - k + 1))
    hi = 1.0 if k == n else float(beta.ppf(1 - ALPHA / 2, k + 1, n - k))
    return lo, hi


def poisson_rate(k: int, exposure: float) -> tuple[float, float]:
    """Exact (Garwood) interval for a Poisson rate with k events over `exposure`."""
    lo = 0.0 if k == 0 else float(chi2.ppf(ALPHA / 2, 2 * k)) / (2 * exposure)
    hi = float(chi2.ppf(1 - ALPHA / 2, 2 * k + 2)) / (2 * exposure)
    return lo, hi


def holm(ps: list[float]) -> list[float]:
    m = len(ps)
    order = sorted(range(m), key=lambda i: ps[i])
    adj, running = [0.0] * m, 0.0
    for rank, i in enumerate(order):
        running = max(running, (m - rank) * ps[i])
        adj[i] = min(1.0, running)
    return adj


def benjamini_hochberg(ps: list[float]) -> list[float]:
    m = len(ps)
    order = sorted(range(m), key=lambda i: ps[i], reverse=True)
    adj, running = [0.0] * m, 1.0
    for pos, i in enumerate(order):
        rank = m - pos
        running = min(running, m * ps[i] / rank)
        adj[i] = min(1.0, running)
    return adj


def major(v: str) -> int:
    return int(v.split(".")[0])


# ----------------------------------------------------------------------
# S1 multiple comparisons over the 54 attribution rows
# ----------------------------------------------------------------------

def multiple_comparisons(e5: list[dict]) -> dict:
    rows = sorted(e5, key=lambda r: (major(r["v"]), r["k"]))
    out = {"n_rows": len(rows), "alpha": ALPHA, "contrasts": {}}
    for contrast in ("drift_penalty", "norm_gain"):
        ps = [r[f"{contrast}_p_sign"] for r in rows]
        h, bh = holm(ps), benjamini_hochberg(ps)
        per_row = []
        for r, p, ph, pb in zip(rows, ps, h, bh):
            per_row.append({"v": r["v"], "k": r["k"], "estimate": r[f"{contrast}_top1"],
                            "ci": r[f"{contrast}_ci"], "discordant": r[f"{contrast}_discordant"],
                            "p_raw": p, "p_holm": ph, "p_bh": pb,
                            "post_restructuring": major(r["v"]) >= POST_RESTRUCTURING_MAJOR})
        summary = {}
        for scope, sel in (("k10", [x for x in per_row if x["k"] == 10]),
                           ("all", per_row)):
            post = [x for x in sel if x["post_restructuring"]]
            summary[scope] = {
                "n": len(sel), "n_post_restructuring": len(post),
                "survive_raw": sum(x["p_raw"] < ALPHA for x in sel),
                "survive_holm": sum(x["p_holm"] < ALPHA for x in sel),
                "survive_bh": sum(x["p_bh"] < ALPHA for x in sel),
                "ci_excludes_zero": sum(min(x["ci"]) > 0 for x in sel),
                "post_survive_raw": [f"v{x['v']}/k{x['k']}" for x in post if x["p_raw"] < ALPHA],
                "post_survive_holm": [f"v{x['v']}/k{x['k']}" for x in post if x["p_holm"] < ALPHA],
                "post_survive_bh": [f"v{x['v']}/k{x['k']}" for x in post if x["p_bh"] < ALPHA],
                "post_ci_excludes_zero": [f"v{x['v']}/k{x['k']}" for x in post if min(x["ci"]) > 0],
            }
        out["contrasts"][contrast] = {"rows": per_row, "summary": summary}
    return out


# ----------------------------------------------------------------------
# S2 recurrence hazard intervals
# ----------------------------------------------------------------------

def recurrence_intervals(e12: dict) -> dict:
    rec = e12["recurrence"]
    k, n, years = rec["n_events"], rec["n_transitions"], rec["observed_domain_years"]
    rate_lo, rate_hi = poisson_rate(k, years)
    return {
        "n_events": k, "n_transitions": n, "observed_domain_years": years,
        "hazard_per_transition": rec["hazard_per_transition"],
        "hazard_clopper_pearson": clopper_pearson(k, n),
        "hazard_wilson": wilson(k, n),
        "rate_per_domain_year": k / years,
        "rate_per_domain_year_ci": [rate_lo, rate_hi],
        "years_per_event": rec["years_per_event"],
        "years_per_event_ci": [1 / rate_hi, 1 / rate_lo],
        "method": "Clopper-Pearson and Wilson for the binomial hazard; exact Garwood "
                  "chi-square interval for the Poisson rate, reciprocal for years per event",
    }


# ----------------------------------------------------------------------
# S3 Wilson intervals for bare proportions in Sections 6-9
# ----------------------------------------------------------------------

def _count(frac: float, n: int) -> int:
    k = round(frac * n)
    assert abs(k / n - frac) < 1e-9, (frac, n, k)
    return k


def proportion_intervals(e4: dict, e6: dict, e8: dict, e10: dict, e12: dict) -> list[dict]:
    items = []

    def add(section, label, k, n, key, sampling):
        lo, hi = wilson(k, n)
        items.append({"section": section, "label": label, "k": k, "n": n,
                      "estimate": k / n, "wilson": [lo, hi], "json_key": key,
                      "sampling": sampling})

    cum = e4["enterprise-attack"]["cumulative"]
    book = cum["ontology_refinement"] + cum["revocation_remap"]
    pre = cum["total_added"] - cum["new_actor"]
    add("6.4", "bookkeeping share of added edges to pre-existing groups", book, pre,
        "e4_growth.enterprise-attack.cumulative.{ontology_refinement+revocation_remap}/"
        "{total_added-new_actor}", "census")

    rec = e12["recurrence"]
    add("6.5", "restructuring hazard per major transition", rec["n_events"],
        rec["n_transitions"], "e12_temporal_structure.recurrence.n_events/n_transitions",
        "census")
    add("6.5", "v18.1 group profiles losing an identifier at v19", e8["groups_losing_an_identifier"],
        e8["groups_total"], "e8_case_v19.groups_losing_an_identifier/groups_total", "census")

    flips = {r["v"]: r for r in e10["attribution_verdicts"]}
    names = {"verdict_changed_frac": "named actor changed",
             "verdict_changed_and_now_wrong_frac": "changed and now wrong",
             "was_right_now_changed_frac": "was right, now changed",
             "normalization_changed_verdict_frac": "normalization changed verdict"}
    for v in ("1.0", "6.0", "18.0"):
        r = flips[v]
        for key, name in names.items():
            add("7.5", f"v{v} {name}", _count(r[key], r["trials"]), r["trials"],
                f"e10_conclusion_flips.attribution_verdicts[v={v}].{key}", "trial")

    cov = {(p["relation"], p["v"]): p for p in e6["portfolios"] if p["w"] == "19.0"}
    for rel, vs in (("mitigates", ("6.0", "10.0", "17.0", "18.0")), ("detects", ("10.0", "17.0"))):
        for v in vs:
            p = cov[(rel, v)]
            base = f"e6_coverage.portfolios[{rel},v={v},w=19.0]"
            add("7.6", f"{rel} frozen at v{v}: claimed then", p["portfolio"], p["live_v"],
                f"{base}.coverage_at_v", "census")
            add("7.6", f"{rel} frozen at v{v}: naive at v19.0",
                _count(p["coverage_naive"], p["live_w"]), p["live_w"],
                f"{base}.coverage_naive", "census")
            add("7.6", f"{rel} frozen at v{v}: normalized at v19.0",
                _count(p["coverage_normalized"], p["live_w"]), p["live_w"],
                f"{base}.coverage_normalized", "census")
    return items


# ----------------------------------------------------------------------
# S4 Mobile / ICS frozen-capability coverage
# ----------------------------------------------------------------------

def mobile_ics_coverage(con) -> list[dict]:
    portfolio = _load_script("05_coverage").portfolio
    rows = []
    for dom in ("mobile-attack", "ics-attack"):
        majors = ad.major_releases(con, dom)
        w_rel = majors[-1]
        w = ad.load_snapshot(con, dom, w_rel.version)
        live_w = w.live_tech()
        for v_rel in majors[:-1]:
            v = ad.load_snapshot(con, dom, v_rel.version)
            cap = portfolio(v, "mitigates")
            if not cap:
                rows.append({"domain": dom, "v": v_rel.version, "v_date": v_rel.date,
                             "w": w_rel.version, "portfolio": 0, "note": "no mitigates edges"})
                continue
            ledger = ad.normalize_with_ledger(cap, w)
            naive_n, norm_n = len(cap & live_w), len(ledger.ids)
            rows.append({
                "domain": dom, "v": v_rel.version, "w": w_rel.version,
                "v_date": v_rel.date, "w_date": w_rel.date,
                "portfolio": len(cap), "live_v": len(v.live_tech()), "live_w": len(live_w),
                "naive_matched": naive_n, "normalized_matched": norm_n,
                "dropped": len(ledger.dropped),
                "coverage_at_v": len(cap) / len(v.live_tech()),
                "coverage_naive": naive_n / len(live_w),
                "coverage_normalized": norm_n / len(live_w),
                "artefact_pp": (norm_n - naive_n) / len(live_w) * 100,
            })
    return rows


# ----------------------------------------------------------------------
# tables
# ----------------------------------------------------------------------

def fmt_p(p: float) -> str:
    return "<0.001" if p < 0.001 else f"{p:.3f}"


def write_t21(mc: dict) -> None:
    lines = ["**Table 21.** Multiple-comparison control over the 54 attribution rows "
             "(18 vocabularies x k in {5, 10, 20}), exact paired sign test per row, "
             "Holm and Benjamini-Hochberg adjusted across all 54 rows per contrast. "
             f"Survivors at alpha = {ALPHA}.", "",
             "| Contrast | Scope | Rows | CI excludes 0 | Raw p < 0.05 | Holm | BH | "
             "Post-restructuring survivors (Holm) |", "|---|---|---|---|---|---|---|---|"]
    for contrast, label in (("drift_penalty", "Drift penalty"), ("norm_gain", "Normalization gain")):
        for scope, name in (("k10", "k = 10"), ("all", "all k")):
            s = mc["contrasts"][contrast]["summary"][scope]
            lines.append(f"| {label} | {name} | {s['n']} | {s['ci_excludes_zero']} | "
                         f"{s['survive_raw']} | {s['survive_holm']} | {s['survive_bh']} | "
                         f"{len(s['post_survive_holm'])} of {s['n_post_restructuring']}: "
                         f"{', '.join(s['post_survive_holm']) or 'none'} |")
    lines += ["", "Per-row detail at k = 10 (pp = percentage points of top-1 accuracy; "
              "discordant = trials favouring the first condition / the second):", "",
              "| Vocabulary | Drift penalty (pp) [95% CI] | Discordant | p raw | p Holm | p BH | "
              "Norm. gain (pp) [95% CI] | Discordant | p raw | p Holm | p BH |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
    dp = {(r["v"], r["k"]): r for r in mc["contrasts"]["drift_penalty"]["rows"]}
    ng = {(r["v"], r["k"]): r for r in mc["contrasts"]["norm_gain"]["rows"]}
    for (v, k), d in dp.items():
        if k != 10:
            continue
        g = ng[(v, k)]
        cell = lambda r: (f"{r['estimate']*100:.1f} [{r['ci'][0]*100:.1f}, {r['ci'][1]*100:.1f}] | "  # noqa: E731
                          f"{r['discordant'][0]}/{r['discordant'][1]} | {fmt_p(r['p_raw'])} | "
                          f"{fmt_p(r['p_holm'])} | {fmt_p(r['p_bh'])}")
        lines.append(f"| v{v} | {cell(d)} | {cell(g)} |")
    (TABLES / "t21_multiple_comparisons.md").write_text("\n".join(lines) + "\n")


def write_t22(rec: dict, props: list[dict]) -> None:
    lines = ["**Table 22.** 95% intervals for point estimates reported bare in Sections 6-9. "
             "Trial-sampled proportions are Wilson intervals over the experiment's trials; "
             "census proportions are counts over a fixed catalogue, so the interval describes "
             "the sampling variability a same-sized random catalogue would show and is given "
             "for scale, not inference.", "",
             "| Section | Quantity | k / n | Estimate | 95% interval | Sampling |",
             "|---|---|---|---|---|---|"]
    h_cp, h_w = rec["hazard_clopper_pearson"], rec["hazard_wilson"]
    lines.append(f"| 6.5 | restructuring hazard per transition (Clopper-Pearson) | "
                 f"{rec['n_events']} / {rec['n_transitions']} | {rec['hazard_per_transition']:.3f} | "
                 f"[{h_cp[0]:.3f}, {h_cp[1]:.3f}] | census |")
    lines.append(f"| 6.5 | restructuring hazard per transition (Wilson) | "
                 f"{rec['n_events']} / {rec['n_transitions']} | {rec['hazard_per_transition']:.3f} | "
                 f"[{h_w[0]:.3f}, {h_w[1]:.3f}] | census |")
    r = rec["rate_per_domain_year_ci"]
    lines.append(f"| 6.5 | events per domain-year (Poisson, exact) | "
                 f"{rec['n_events']} / {rec['observed_domain_years']:.2f} y | "
                 f"{rec['rate_per_domain_year']:.3f} | [{r[0]:.3f}, {r[1]:.3f}] | census |")
    y = rec["years_per_event_ci"]
    lines.append(f"| 6.5 | domain-years per event | {rec['observed_domain_years']:.2f} y / "
                 f"{rec['n_events']} | {rec['years_per_event']:.2f} | [{y[0]:.2f}, {y[1]:.2f}] | census |")
    for p in props:
        if p["label"].startswith("restructuring hazard"):
            continue
        lines.append(f"| {p['section']} | {p['label']} | {p['k']} / {p['n']} | {p['estimate']:.3f} | "
                     f"[{p['wilson'][0]:.3f}, {p['wilson'][1]:.3f}] | {p['sampling']} |")
    (TABLES / "t22_intervals.md").write_text("\n".join(lines) + "\n")


def write_t23(rows: list[dict]) -> None:
    lines = ["**Table 23.** Frozen-capability mitigation coverage in Mobile and ICS, the E6 "
             "measurement applied outside Enterprise. Capability frozen at each major release "
             "as the techniques reachable by `mitigates` edges, re-measured at the newest major "
             "naively and after ATT&CK-Norm. Mobile v1.0 and v2.0 identifiers were all replaced "
             "in the 2018 renumbering (v2.0 to v3.0) with no revocation edges, so nothing frozen "
             "there is recoverable by any crosswalk.", "",
             "| Domain | Capability frozen at | Portfolio | Claimed then | Naive at newest | "
             "Normalized at newest | Dropped | Identifier artefact (pp) |",
             "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        if "note" in r:
            lines.append(f"| {r['domain']} | v{r['v']} ({r['v_date']}) | 0 | {r['note']} | | | | |")
            continue
        lines.append(f"| {r['domain'].split('-')[0]} | v{r['v']} ({r['v_date']}) | {r['portfolio']} | "
                     f"{r['coverage_at_v']*100:.1f}% | {r['coverage_naive']*100:.1f}% | "
                     f"{r['coverage_normalized']*100:.1f}% | {r['dropped']} | {r['artefact_pp']:.1f} |")
    (TABLES / "t23_mobile_ics_coverage.md").write_text("\n".join(lines) + "\n")


def main() -> None:
    load = lambda name: json.loads((OUT / name).read_text())  # noqa: E731
    e4, e5, e6 = load("e4_growth.json"), load("e5_attribution.json"), load("e6_coverage.json")
    e8, e10, e12 = load("e8_case_v19.json"), load("e10_conclusion_flips.json"), \
        load("e12_temporal_structure.json")

    mc = multiple_comparisons(e5)
    rec = recurrence_intervals(e12)
    props = proportion_intervals(e4, e6, e8, e10, e12)
    cov = mobile_ics_coverage(ad.connect())
    result = {"multiple_comparisons": mc, "recurrence_intervals": rec,
              "proportion_intervals": props, "mobile_ics_coverage": {"portfolios": cov}}
    (OUT / "e21_statistics.json").write_text(json.dumps(result, indent=1))
    write_t21(mc)
    write_t22(rec, props)
    write_t23(cov)

    for contrast in ("drift_penalty", "norm_gain"):
        for scope in ("k10", "all"):
            s = mc["contrasts"][contrast]["summary"][scope]
            print(f"{contrast:14} {scope:4} n={s['n']:2} ci>0={s['ci_excludes_zero']:2} "
                  f"raw={s['survive_raw']:2} holm={s['survive_holm']:2} bh={s['survive_bh']:2} "
                  f"post(holm)={len(s['post_survive_holm'])}/{s['n_post_restructuring']}",
                  file=sys.stderr)
    print(f"hazard {rec['n_events']}/{rec['n_transitions']} = {rec['hazard_per_transition']:.3f} "
          f"CP {rec['hazard_clopper_pearson']} Wilson {rec['hazard_wilson']}; "
          f"years/event {rec['years_per_event']:.2f} {rec['years_per_event_ci']}", file=sys.stderr)
    for r in cov:
        if "note" not in r:
            print(f"  {r['domain']:14} v{r['v']:>5}: claimed {r['coverage_at_v']:.3f} naive "
                  f"{r['coverage_naive']:.3f} norm {r['coverage_normalized']:.3f} "
                  f"artefact {r['artefact_pp']:.1f}pp dropped {r['dropped']}", file=sys.stderr)
    print(f"wrote {OUT/'e21_statistics.json'} and tables t21-t23", file=sys.stderr)


if __name__ == "__main__":
    main()
