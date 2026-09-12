#!/usr/bin/env python3
"""E6: detection/mitigation coverage claims under a frozen capability.

A defender fixes a capability at release V: the set of techniques it claims to
mitigate (or detect). Nothing about the capability changes afterwards. We then
recompute the *reported* coverage percentage against later releases W, both
naively (raw identifiers against W's technique list) and after ATT&CK-Norm.
The spread between the three numbers is pure measurement artefact.
"""
from __future__ import annotations

import json
import random
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import attackdrift as ad  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "data" / "results"
DOMAIN = "enterprise-attack"
SEED = 20260912
N_RANDOM = 500


def portfolio(snap: ad.Snapshot, rel_type: str) -> set[str]:
    live = snap.live_tech()
    out = set()
    for s, t in snap.rels.get(rel_type, []):
        to = snap.by_stix.get(t)
        if to and to["otype"] == ad.TECH and to["attack_id"] in live:
            out.add(to["attack_id"])
    return out


def main() -> None:
    con = ad.connect()
    majors = ad.major_releases(con, DOMAIN)
    snaps = {m.version: ad.load_snapshot(con, DOMAIN, m.version) for m in majors}
    rows = []
    for rel_type in ("mitigates", "detects"):
        for i, v_rel in enumerate(majors[:-1]):
            v = snaps[v_rel.version]
            cap = portfolio(v, rel_type)
            if len(cap) < 20:
                continue
            base_cov = len(cap) / len(v.live_tech())
            for w_rel in majors[i + 1:]:
                w = snaps[w_rel.version]
                live_w = w.live_tech()
                naive = len(cap & live_w) / len(live_w)
                norm = len(ad.normalize(cap, w)) / len(live_w)
                rows.append({
                    "relation": rel_type, "v": v_rel.version, "w": w_rel.version,
                    "v_date": v_rel.date, "w_date": w_rel.date,
                    "portfolio": len(cap), "live_v": len(v.live_tech()),
                    "live_w": len(live_w),
                    "coverage_at_v": base_cov, "coverage_naive": naive,
                    "coverage_normalized": norm,
                    "naive_error_pp": (naive - base_cov) * 100,
                    "normalized_error_pp": (norm - base_cov) * 100,
                })

    # random-portfolio sweep: distribution of the measurement artefact
    rng = random.Random(SEED)
    sweep = []
    for i, v_rel in enumerate(majors[:-1]):
        v = snaps[v_rel.version]
        live_v = sorted(v.live_tech())
        w_rel = majors[-1]
        w = snaps[w_rel.version]
        live_w = w.live_tech()
        errs_naive, errs_norm = [], []
        for _ in range(N_RANDOM):
            size = max(20, int(0.3 * len(live_v)))
            cap = set(rng.sample(live_v, size))
            base = len(cap) / len(live_v)
            errs_naive.append((len(cap & live_w) / len(live_w) - base) * 100)
            errs_norm.append((len(ad.normalize(cap, w)) / len(live_w) - base) * 100)
        sweep.append({
            "v": v_rel.version, "v_date": v_rel.date, "w": w_rel.version,
            "mean_naive_error_pp": statistics.fmean(errs_naive),
            "sd_naive_error_pp": statistics.pstdev(errs_naive),
            "mean_normalized_error_pp": statistics.fmean(errs_norm),
            "sd_normalized_error_pp": statistics.pstdev(errs_norm),
        })

    (OUT / "e6_coverage.json").write_text(json.dumps(
        {"portfolios": rows, "random_sweep": sweep}, indent=1))
    print(f"wrote {OUT/'e6_coverage.json'} ({len(rows)} rows)", file=sys.stderr)


if __name__ == "__main__":
    main()
