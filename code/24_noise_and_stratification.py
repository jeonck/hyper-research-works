#!/usr/bin/env python3
"""E14: three audits of the attribution experiment, run against its own design.

A1  Noise x drift factorial. The published attribution numbers are measured with
    inter-labeller noise set to zero. Products disagree on the ATT&CK label for
    the same behaviour roughly half the time within one pinned release, so the
    right question is not whether drift survives that noise but whether it is
    additive on top of it. Noise is injected before back-projection, so it flows
    into every condition: with probability rho an observed technique is replaced
    by something the same labeller could plausibly have written instead — a
    sibling sub-technique, its parent, or another technique in the same tactic.

A2  Specificity stratification. Only about a third of ATT&CK groups have any
    technique unique to them, which is the published reason to doubt that
    TTP attribution is identifiable at all. If drift mattered only for the
    non-identifiable groups it would be an artefact of an already-broken task.

A3  The archival control. The experiment's self-consistent baseline is built by
    back-projecting modern profiles into an older vocabulary. This runs the
    other control as well: the real archival release judged against itself,
    using the labels ATT&CK actually published at the time.
"""
from __future__ import annotations

import json
import random
import statistics
import sys
from collections import defaultdict
from importlib import import_module
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import attackdrift as ad  # noqa: E402

attr = import_module("04_attribution")

OUT = Path(__file__).resolve().parents[1] / "data" / "results"
DOMAIN = "enterprise-attack"
SEED = 20260912
K = 10
N_TRIALS = 1200
N_STRAT = 1500
N_BOOT = 2000
RHOS = [0.0, 0.1, 0.2, 0.4]
FACTORIAL_VERSIONS = ["1.0", "6.0", "12.0", "18.0"]
STRAT_VERSIONS = ["12.0", "16.0", "18.0"]
CONTROL_VERSIONS = ["1.0", "6.0", "7.0", "12.0", "18.0"]


def confusables(w: ad.Snapshot) -> dict[str, list[str]]:
    """For each live technique, what a labeller could plausibly have said instead."""
    sub, live = w.sub_of(), w.live_tech()
    kids: dict[str, list[str]] = defaultdict(list)
    for c, p in sub.items():
        if c in live:
            kids[p].append(c)
    by_tactic: dict[str, list[str]] = defaultdict(list)
    for t in live:
        for x in (w.tech[t]["tactics"] or "").split(","):
            if x:
                by_tactic[x].append(t)
    out = {}
    for t in live:
        alts = set()
        p = sub.get(t)
        if p:
            alts.update(x for x in kids.get(p, []) if x != t)
            if p in live:
                alts.add(p)
        alts.update(kids.get(t, []))
        if not alts:
            for x in (w.tech[t]["tactics"] or "").split(","):
                if x:
                    alts.update(by_tactic[x][:40])
            alts.discard(t)
        out[t] = sorted(alts)
    return out


def perturb(obs: set[str], conf: dict[str, list[str]], rho: float,
            rng: random.Random) -> set[str]:
    out = set()
    for t in obs:
        if rho > 0 and rng.random() < rho and conf.get(t):
            out.add(rng.choice(conf[t]))
        else:
            out.add(t)
    return out


def specific_groups(prof: dict[str, set[str]]) -> set[str]:
    df: dict[str, int] = defaultdict(int)
    for ts in prof.values():
        for t in ts:
            df[t] += 1
    return {g for g, ts in prof.items() if any(df[t] == 1 for t in ts)}


def bootstrap_ci(diffs: list[float], rng: random.Random) -> tuple[float, float]:
    n = len(diffs)
    means = sorted(statistics.fmean(diffs[rng.randrange(n)] for _ in range(n))
                   for _ in range(N_BOOT))
    return means[int(0.025 * N_BOOT)], means[int(0.975 * N_BOOT)]


def universe_for(v: ad.Snapshot, w: ad.Snapshot):
    pw = w.group_techniques(include_software=True)
    pv = v.group_techniques(include_software=True)
    uni = [g for g in sorted(set(pw) & set(pv)) if len(pw[g]) >= K and len(pv[g]) >= 2]
    return pw, pv, uni


def factorial(con) -> list[dict]:
    w = ad.load_snapshot(con, DOMAIN, "19.0")
    conf = confusables(w)
    rows = []
    for vv in FACTORIAL_VERSIONS:
        v = ad.load_snapshot(con, DOMAIN, vv)
        back = attr.build_backmap(v, w)
        pw, pv, uni = universe_for(v, w)
        if len(uni) < 10:
            continue
        prof_w = {g: pw[g] for g in uni}
        prof_v = {g: {back[t] for t in pw[g] if back.get(t)} for g in uni}
        idf_w, idf_v = attr.idf_weights(prof_w), attr.idf_weights(prof_v)
        for rho in RHOS:
            rng = random.Random(SEED)
            hits = defaultdict(list)
            for _ in range(N_TRIALS):
                g = rng.choice(uni)
                obs_w = perturb(set(rng.sample(sorted(prof_w[g]), K)), conf, rho, rng)
                obs_v = {back[t] for t in obs_w if back.get(t)}
                if len(obs_v) < 2:
                    continue
                hits["contemporaneous"].append(
                    1.0 if attr.rank_of(g, obs_v, prof_v, idf_v, uni) == 1 else 0.0)
                hits["naive"].append(
                    1.0 if attr.rank_of(g, obs_v, prof_w, idf_w, uni) == 1 else 0.0)
                hits["normalized"].append(
                    1.0 if attr.rank_of(g, ad.normalize(obs_v, w), prof_w, idf_w, uni) == 1
                    else 0.0)
            if not hits["naive"]:
                continue
            c, n_, nm = (statistics.fmean(hits[k]) for k in
                         ("contemporaneous", "naive", "normalized"))
            rows.append({"v": vv, "rho": rho, "trials": len(hits["naive"]),
                         "contemporaneous": c, "naive": n_, "normalized": nm,
                         "drift_penalty": c - n_, "norm_gain": nm - n_,
                         "recovery": (nm - n_) / (c - n_) if c - n_ > 1e-9 else None})
            print(f"  v{vv} rho={rho}: penalty {100*(c-n_):.1f} pp, "
                  f"recovery {rows[-1]['recovery']}", file=sys.stderr)
    return rows


def stratified(con) -> list[dict]:
    w = ad.load_snapshot(con, DOMAIN, "19.0")
    rows = []
    for vv in STRAT_VERSIONS:
        v = ad.load_snapshot(con, DOMAIN, vv)
        back = attr.build_backmap(v, w)
        pw, pv, uni = universe_for(v, w)
        if len(uni) < 10:
            continue
        prof_w = {g: pw[g] for g in uni}
        prof_v = {g: {back[t] for t in pw[g] if back.get(t)} for g in uni}
        spec = specific_groups(prof_w)
        idf_w, idf_v = attr.idf_weights(prof_w), attr.idf_weights(prof_v)
        rng = random.Random(SEED)
        pairs: dict[str, list[float]] = defaultdict(list)
        for _ in range(N_STRAT):
            g = rng.choice(uni)
            obs_w = set(rng.sample(sorted(prof_w[g]), K))
            obs_v = {back[t] for t in obs_w if back.get(t)}
            if len(obs_v) < 2:
                continue
            d = ((1.0 if attr.rank_of(g, obs_v, prof_v, idf_v, uni) == 1 else 0.0) -
                 (1.0 if attr.rank_of(g, obs_v, prof_w, idf_w, uni) == 1 else 0.0))
            pairs["all"].append(d)
            pairs["group_has_a_unique_technique" if g in spec
                  else "group_has_none"].append(d)
        br = random.Random(SEED + 1)
        row = {"v": vv, "n_groups": len(uni), "groups_with_unique_technique": len(spec),
               "specificity_fraction": len(spec) / len(uni)}
        for stratum, d in pairs.items():
            lo, hi = bootstrap_ci(d, br)
            row[stratum] = {"drift_penalty": statistics.fmean(d), "ci": [lo, hi],
                            "n": len(d)}
        rows.append(row)
        print(f"  v{vv}: specificity {row['specificity_fraction']:.3f}; "
              f"penalty all {row['all']['drift_penalty']:+.4f}", file=sys.stderr)
    return rows


def archival_control(con) -> list[dict]:
    w = ad.load_snapshot(con, DOMAIN, "19.0")
    rows = []
    for vv in CONTROL_VERSIONS:
        v = ad.load_snapshot(con, DOMAIN, vv)
        back = attr.build_backmap(v, w)
        pw, pv, uni = universe_for(v, w)
        if len(uni) < 10:
            continue
        prof_w = {g: pw[g] for g in uni}
        prof_v = {g: {back[t] for t in pw[g] if back.get(t)} for g in uni}
        prof_h = {g: pv[g] for g in uni}
        idf_w, idf_v, idf_h = (attr.idf_weights(prof_w), attr.idf_weights(prof_v),
                               attr.idf_weights(prof_h))
        rng = random.Random(SEED)
        acc = defaultdict(list)
        for _ in range(N_STRAT):
            g = rng.choice(uni)
            obs_w = set(rng.sample(sorted(prof_w[g]), K))
            obs_v = {back[t] for t in obs_w if back.get(t)}
            if len(obs_v) < 2:
                continue
            hp = sorted(prof_h[g])
            obs_h = set(rng.sample(hp, min(K, len(hp))))
            acc["backprojected_self_consistent"].append(
                1.0 if attr.rank_of(g, obs_v, prof_v, idf_v, uni) == 1 else 0.0)
            acc["archival_self_consistent"].append(
                1.0 if attr.rank_of(g, obs_h, prof_h, idf_h, uni) == 1 else 0.0)
            acc["archival_against_modern"].append(
                1.0 if attr.rank_of(g, obs_h, prof_w, idf_w, uni) == 1 else 0.0)
            acc["obs_size_backprojected"].append(len(obs_v))
            acc["obs_size_archival"].append(len(obs_h))
        rows.append({"v": vv, **{k: statistics.fmean(x) for k, x in acc.items()}})
        print(f"  v{vv}: back-projected {rows[-1]['backprojected_self_consistent']:.3f}, "
              f"archival self-consistent {rows[-1]['archival_self_consistent']:.3f}, "
              f"archival vs modern {rows[-1]['archival_against_modern']:.3f}",
              file=sys.stderr)
    return rows


def main() -> None:
    con = ad.connect()
    print("A1 noise x drift factorial", file=sys.stderr)
    f = factorial(con)
    print("A2 specificity stratification", file=sys.stderr)
    s = stratified(con)
    print("A3 archival control", file=sys.stderr)
    a = archival_control(con)
    (OUT / "e14_noise_stratification.json").write_text(json.dumps(
        {"factorial": f, "stratified": s, "archival_control": a}, indent=1))
    print(f"wrote {OUT/'e14_noise_stratification.json'}", file=sys.stderr)


if __name__ == "__main__":
    main()
