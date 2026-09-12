#!/usr/bin/env python3
"""E6b: prevalence-weighted coverage drift.

Answers the strongest published objection to E6 — that ATT&CK's observed
sightings are dominated by a short head, so churn in the long tail barely moves
a coverage number anyone cares about. We repeat the frozen-capability experiment
with each technique weighted by its prevalence, proxied by the number of `uses`
edges the release itself publishes for that technique (groups, malware and tools
combined). If the prevalence-weighted artefact is much smaller than the
unweighted one, the objection lands and the paper must say so.
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import attackdrift as ad  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "data" / "results"
DOMAIN = "enterprise-attack"


def prevalence(snap: ad.Snapshot) -> Counter:
    c: Counter = Counter()
    live = snap.live_tech()
    for s, t in snap.rels.get("uses", []):
        to = snap.by_stix.get(t)
        if to and to["otype"] == ad.TECH and to["attack_id"] in live:
            c[to["attack_id"]] += 1
    return c


def portfolio(snap: ad.Snapshot, rel_type: str) -> set[str]:
    live = snap.live_tech()
    return {o["attack_id"] for _, t in snap.rels.get(rel_type, [])
            if (o := snap.by_stix.get(t)) and o["otype"] == ad.TECH
            and o["attack_id"] in live}


def main() -> None:
    con = ad.connect()
    majors = ad.major_releases(con, DOMAIN)
    snaps = {m.version: ad.load_snapshot(con, DOMAIN, m.version) for m in majors}
    w_rel = majors[-1]
    w = snaps[w_rel.version]
    prev_w = prevalence(w)
    live_w = w.live_tech()
    total_w = sum(prev_w.get(t, 0) for t in live_w)

    rows = []
    for v_rel in majors[:-1]:
        v = snaps[v_rel.version]
        cap = portfolio(v, "mitigates")
        if len(cap) < 20:
            continue
        prev_v = prevalence(v)
        live_v = v.live_tech()
        total_v = sum(prev_v.get(t, 0) for t in live_v) or 1
        unw_at_v = len(cap) / len(live_v)
        wt_at_v = sum(prev_v.get(t, 0) for t in cap) / total_v
        naive = cap & live_w
        norm = ad.normalize(cap, w)
        rows.append({
            "v": v_rel.version, "v_date": v_rel.date, "w": w_rel.version,
            "portfolio": len(cap),
            "unweighted_at_v": unw_at_v,
            "unweighted_naive": len(naive) / len(live_w),
            "unweighted_normalized": len(norm) / len(live_w),
            "unweighted_artefact_pp": 100 * (len(norm) - len(naive)) / len(live_w),
            "weighted_at_v": wt_at_v,
            "weighted_naive": sum(prev_w.get(t, 0) for t in naive) / total_w,
            "weighted_normalized": sum(prev_w.get(t, 0) for t in norm) / total_w,
            "weighted_artefact_pp": 100 * (sum(prev_w.get(t, 0) for t in norm) -
                                           sum(prev_w.get(t, 0) for t in naive)) / total_w,
        })
        r = rows[-1]
        print(f"  v{v_rel.version}: unweighted artefact {r['unweighted_artefact_pp']:+.2f} pp, "
              f"prevalence-weighted {r['weighted_artefact_pp']:+.2f} pp", file=sys.stderr)

    # head concentration, to state the objection's own premise quantitatively
    head = prev_w.most_common(15)
    concentration = sum(c for _, c in head) / (sum(prev_w.values()) or 1)
    (OUT / "e6b_prevalence.json").write_text(json.dumps(
        {"rows": rows,
         "top15_share_of_uses_edges": concentration,
         "top15": [{"technique": t, "edges": c} for t, c in head]}, indent=1))
    print(f"  top-15 techniques carry {concentration:.3f} of all `uses` edges at "
          f"v{w_rel.version}", file=sys.stderr)
    print(f"wrote {OUT/'e6b_prevalence.json'}", file=sys.stderr)


if __name__ == "__main__":
    main()
