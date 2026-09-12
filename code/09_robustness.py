#!/usr/bin/env python3
"""E5b robustness of the attribution result, and E2b identifier half-life.

E5b varies the two free choices in the attribution experiment — the similarity
function and whether software-mediated techniques count toward a group profile —
and re-runs the same four conditions. A finding that survives all four settings
is not an artefact of the scoring rule.

E2b reports, for each release, the elapsed time until half of that release's
technique identifiers are no longer live.
"""
from __future__ import annotations

import json
import math
import random
import statistics
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import attackdrift as ad  # noqa: E402
from importlib import import_module

attr = import_module("04_attribution")

OUT = Path(__file__).resolve().parents[1] / "data" / "results"
DOMAIN = "enterprise-attack"
SEED = 20260912
N_TRIALS = 300
K = 10
SRC_VERSIONS = ["1.0", "6.0", "7.0", "12.0", "18.0"]


def score_jaccard(obs, prof, _w):
    return ad.jaccard(obs, prof)


def score_overlap(obs, prof, _w):
    return len(obs & prof) / (len(obs) or 1)


def score_idf(obs, prof, w):
    inter = obs & prof
    if not inter:
        return 0.0
    num = sum(w.get(t, 0.0) for t in inter)
    denom = (math.sqrt(sum(w.get(t, 0.0) for t in obs)) or 1.0) * \
            (math.sqrt(sum(w.get(t, 0.0) for t in prof)) or 1.0)
    return num / denom


SCORERS = {"idf-cosine": score_idf, "jaccard": score_jaccard, "overlap": score_overlap}


def rank_of(truth, obs, profiles, w, order, scorer):
    scored = sorted(((-scorer(obs, profiles[g], w), g) for g in order))
    for i, (_, g) in enumerate(scored, 1):
        if g == truth:
            return i
    return len(order) + 1


def run_cell(v, w, scorer_name, include_software, rng):
    scorer = SCORERS[scorer_name]
    pw = w.group_techniques(include_software=include_software)
    pv = v.group_techniques(include_software=include_software)
    back = attr.build_backmap(v, w)
    universe = [g for g in sorted(set(pw) & set(pv)) if len(pw[g]) >= K]
    if len(universe) < 10:
        return None
    prof_w = {g: pw[g] for g in universe}
    prof_v = {g: {back[t] for t in pw[g] if back.get(t)} for g in universe}
    idf_w, idf_v = attr.idf_weights(prof_w), attr.idf_weights(prof_v)
    hits = defaultdict(list)
    for _ in range(N_TRIALS):
        g = rng.choice(universe)
        obs_w = set(rng.sample(sorted(prof_w[g]), K))
        obs_v = {back[t] for t in obs_w if back.get(t)}
        if len(obs_v) < 2:
            continue
        for cond, (obs, profs, weights) in {
                "contemporaneous": (obs_v, prof_v, idf_v),
                "naive": (obs_v, prof_w, idf_w),
                "normalized": (ad.normalize(obs_v, w), prof_w, idf_w),
                "oracle": (obs_w, prof_w, idf_w)}.items():
            hits[cond].append(1.0 if rank_of(g, obs, profs, weights, universe, scorer) == 1 else 0.0)
    if not hits["naive"]:
        return None
    out = {c: statistics.fmean(v_) for c, v_ in hits.items()}
    out["drift_penalty"] = out["contemporaneous"] - out["naive"]
    out["norm_gain"] = out["normalized"] - out["naive"]
    out["n_groups"] = len(universe)
    out["trials"] = len(hits["naive"])
    return out


def half_life(con) -> list[dict]:
    majors = ad.major_releases(con, DOMAIN)
    snaps = {m.version: ad.load_snapshot(con, DOMAIN, m.version) for m in majors}
    rows = []
    for i, src in enumerate(majors):
        base = snaps[src.version].live_tech()
        if not base:
            continue
        d0 = date.fromisoformat(src.date)
        reached, years = None, None
        for tgt in majors[i:]:
            rate = len(base & snaps[tgt.version].live_tech()) / len(base)
            if rate <= 0.5:
                reached = tgt.version
                years = (date.fromisoformat(tgt.date) - d0).days / 365.25
                break
        rows.append({"src": src.version, "src_date": src.date,
                     "n": len(base), "half_life_release": reached,
                     "half_life_years": years,
                     "final_survival": len(base & snaps[majors[-1].version].live_tech()) / len(base)})
    return rows


def main() -> None:
    con = ad.connect()
    majors = {m.version: m for m in ad.major_releases(con, DOMAIN)}
    w_ver = max(majors, key=lambda v: tuple(int(x) for x in v.split(".")))
    w = ad.load_snapshot(con, DOMAIN, w_ver)
    rows = []
    for v_ver in SRC_VERSIONS:
        v = ad.load_snapshot(con, DOMAIN, v_ver)
        for scorer in SCORERS:
            for inc_sw in (True, False):
                rng = random.Random(SEED)
                r = run_cell(v, w, scorer, inc_sw, rng)
                if r:
                    r.update({"v": v_ver, "w": w_ver, "scorer": scorer,
                              "include_software": inc_sw})
                    rows.append(r)
        print(f"  v{v_ver} done", file=sys.stderr)
    hl = half_life(con)
    (OUT / "e5b_e2b_robustness.json").write_text(
        json.dumps({"attribution_robustness": rows, "half_life": hl}, indent=1))
    print(f"wrote {OUT/'e5b_e2b_robustness.json'}", file=sys.stderr)


if __name__ == "__main__":
    main()
