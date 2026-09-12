#!/usr/bin/env python3
"""Diagnostic for E5's back-projection: how much of a modern profile has no
ancestor in an older vocabulary, and how much the observation therefore shrinks.

Reported for transparency: the contemporaneous / naive / normalized conditions
all consume the same back-projected observation, so the comparison among them is
unaffected by this shrinkage; only the oracle upper bound sees the full set.
"""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import attackdrift as ad  # noqa: E402
from importlib import import_module

attr = import_module("04_attribution")
OUT = Path(__file__).resolve().parents[1] / "data" / "results"
DOMAIN = "enterprise-attack"


def main() -> None:
    con = ad.connect()
    majors = ad.major_releases(con, DOMAIN)
    w = ad.load_snapshot(con, DOMAIN, majors[-1].version)
    pw = w.group_techniques(include_software=True)
    rows = []
    for v_rel in majors[:-1]:
        v = ad.load_snapshot(con, DOMAIN, v_rel.version)
        back = attr.build_backmap(v, w)
        live_w = w.live_tech()
        no_ancestor = sum(1 for t in live_w if not back.get(t))
        shrink = []
        for g, prof in pw.items():
            if not prof:
                continue
            mapped = {back[t] for t in prof if back.get(t)}
            shrink.append(len(mapped) / len(prof))
        rows.append({
            "v": v_rel.version, "v_date": v_rel.date,
            "w": majors[-1].version,
            "modern_techniques": len(live_w),
            "no_v_era_ancestor": no_ancestor,
            "no_ancestor_frac": no_ancestor / len(live_w),
            "mean_profile_retention": statistics.fmean(shrink),
            "mean_profile_collapse": 1 - statistics.fmean(shrink),
        })
        print(f"  v{v_rel.version}: {no_ancestor}/{len(live_w)} modern techniques have no "
              f"v{v_rel.version} ancestor; profiles retain "
              f"{statistics.fmean(shrink):.3f} of their distinct identifiers",
              file=sys.stderr)
    (OUT / "e5c_backprojection.json").write_text(json.dumps(rows, indent=1))
    print(f"wrote {OUT/'e5c_backprojection.json'}", file=sys.stderr)


if __name__ == "__main__":
    main()
