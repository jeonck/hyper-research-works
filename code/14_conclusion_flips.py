#!/usr/bin/env python3
"""E10: does ontology drift change conclusions, not merely scores?

E10a — attribution verdict instability. For each observation, compare the actor
named by a self-consistent V-era system against the actor named when the same
artefact is read by the modern knowledge base. A changed name is a changed
conclusion, and a changed-and-wrong name is a false attribution caused by
nothing but vocabulary.

E10b — coverage leaderboard flips. Freeze every mitigation's technique portfolio
at release V, then re-rank the mitigations at release W using (i) raw identifier
matching and (ii) ATT&CK-Norm. Nothing about the mitigations changed, so any
change in their ordering is a measurement artefact. Reported as Kendall's tau
against the V-era ordering plus the number of discordant top-10 pairs.
"""
from __future__ import annotations

import json
import random
import statistics
import sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import attackdrift as ad  # noqa: E402
from importlib import import_module

attr = import_module("04_attribution")

OUT = Path(__file__).resolve().parents[1] / "data" / "results"
DOMAIN = "enterprise-attack"
SEED = 20260912
N_TRIALS = 500
K = 10


def kendall_tau(order_a: list[str], order_b: list[str]) -> float:
    pos_a = {x: i for i, x in enumerate(order_a)}
    pos_b = {x: i for i, x in enumerate(order_b)}
    common = [x for x in order_a if x in pos_b]
    conc = disc = 0
    for x, y in combinations(common, 2):
        sa = pos_a[x] - pos_a[y]
        sb = pos_b[x] - pos_b[y]
        if sa * sb > 0:
            conc += 1
        elif sa * sb < 0:
            disc += 1
    total = conc + disc
    return (conc - disc) / total if total else 1.0


def attribution_flips(v: ad.Snapshot, w: ad.Snapshot, rng: random.Random) -> dict | None:
    pw = w.group_techniques(include_software=True)
    pv = v.group_techniques(include_software=True)
    back = attr.build_backmap(v, w)
    universe = [g for g in sorted(set(pw) & set(pv)) if len(pw[g]) >= K]
    if len(universe) < 10:
        return None
    prof_w = {g: pw[g] for g in universe}
    prof_v = {g: {back[t] for t in pw[g] if back.get(t)} for g in universe}
    idf_w, idf_v = attr.idf_weights(prof_w), attr.idf_weights(prof_v)

    changed = wrong_after = right_before = both_wrong_different = 0
    norm_changed = trials = 0
    for _ in range(N_TRIALS):
        g = rng.choice(universe)
        obs_w = set(rng.sample(sorted(prof_w[g]), K))
        obs_v = {back[t] for t in obs_w if back.get(t)}
        if len(obs_v) < 2:
            continue
        trials += 1
        top = {}
        for cond, (obs, profs, weights) in {
                "contemporaneous": (obs_v, prof_v, idf_v),
                "naive": (obs_v, prof_w, idf_w),
                "normalized": (ad.normalize(obs_v, w), prof_w, idf_w)}.items():
            scored = sorted(
                ((-attr.rank_of(x, obs, profs, weights, universe), x) for x in [g]),
                key=lambda t: t[0])
            # rank_of gives the truth's rank; recover the top-1 prediction directly
            best, best_score = None, -1.0
            obs_norm = sum(weights.get(t, 0.0) for t in obs) ** 0.5 or 1.0
            for cand in universe:
                prof = profs[cand]
                inter = obs & prof
                if not inter:
                    continue
                num = sum(weights.get(t, 0.0) for t in inter)
                den = obs_norm * ((sum(weights.get(t, 0.0) for t in prof) ** 0.5) or 1.0)
                s = num / den
                if s > best_score:
                    best, best_score = cand, s
            top[cond] = best
            del scored
        if top["contemporaneous"] != top["naive"]:
            changed += 1
            if top["contemporaneous"] == g:
                right_before += 1
            if top["naive"] != g:
                wrong_after += 1
            if top["contemporaneous"] != g and top["naive"] != g:
                both_wrong_different += 1
        if top["normalized"] != top["naive"]:
            norm_changed += 1
    if not trials:
        return None
    return {
        "trials": trials,
        "verdict_changed_frac": changed / trials,
        "verdict_changed_and_now_wrong_frac": wrong_after / trials,
        "was_right_now_changed_frac": right_before / trials,
        "both_wrong_but_different_actor_frac": both_wrong_different / trials,
        "normalization_changed_verdict_frac": norm_changed / trials,
    }


def coverage_flips(v: ad.Snapshot, w: ad.Snapshot) -> dict | None:
    live_v, live_w = v.live_tech(), w.live_tech()
    port: dict[str, set[str]] = {}
    for s, t in v.rels.get("mitigates", []):
        so, to = v.by_stix.get(s), v.by_stix.get(t)
        if so and to and to["otype"] == ad.TECH and to["attack_id"] in live_v \
                and so["attack_id"]:
            port.setdefault(so["attack_id"], set()).add(to["attack_id"])
    port = {m: ts for m, ts in port.items() if len(ts) >= 3}
    if len(port) < 10:
        return None
    order_v = sorted(port, key=lambda m: (-len(port[m]), m))
    order_naive = sorted(port, key=lambda m: (-len(port[m] & live_w), m))
    order_norm = sorted(port, key=lambda m: (-len(ad.normalize(port[m], w)), m))
    top10 = set(order_v[:10])
    return {
        "mitigations": len(port),
        "tau_naive": kendall_tau(order_v, order_naive),
        "tau_normalized": kendall_tau(order_v, order_norm),
        "top10_membership_changed_naive": len(top10 - set(order_naive[:10])),
        "top10_membership_changed_normalized": len(top10 - set(order_norm[:10])),
        "rank1_changed_naive": order_v[0] != order_naive[0],
        "rank1_changed_normalized": order_v[0] != order_norm[0],
    }


def main() -> None:
    con = ad.connect()
    majors = ad.major_releases(con, DOMAIN)
    w = ad.load_snapshot(con, DOMAIN, majors[-1].version)
    rows_a, rows_b = [], []
    for v_rel in majors[:-1]:
        v = ad.load_snapshot(con, DOMAIN, v_rel.version)
        rng = random.Random(SEED)
        a = attribution_flips(v, w, rng)
        if a:
            a.update({"v": v_rel.version, "v_date": v_rel.date, "w": majors[-1].version})
            rows_a.append(a)
        b = coverage_flips(v, w)
        if b:
            b.update({"v": v_rel.version, "v_date": v_rel.date, "w": majors[-1].version})
            rows_b.append(b)
        print(f"  v{v_rel.version} done", file=sys.stderr)
    (OUT / "e10_conclusion_flips.json").write_text(
        json.dumps({"attribution_verdicts": rows_a, "coverage_rankings": rows_b}, indent=1))
    print(f"wrote {OUT/'e10_conclusion_flips.json'}", file=sys.stderr)


if __name__ == "__main__":
    main()
