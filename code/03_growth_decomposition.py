#!/usr/bin/env python3
"""E4: decompose apparent CTI knowledge growth into genuine intelligence vs. bookkeeping.

For every consecutive pair of major ATT&CK releases (A -> B) each group->technique
`uses` edge that appears in B but not in A is attributed to exactly one cause:

  new_actor            the group itself is new in B
  ontology_refinement  the technique is new in B and is a sub-technique of a
                       technique the group was already credited with in A
  revocation_remap     the edge restates an A-edge whose technique was revoked
                       and replaced (transitively) by this technique
  new_technique_intel  the technique is new in B and is not a refinement of an
                       existing edge for that group
  genuine_new_intel    both endpoints already existed in A and were unlinked

Disappearing edges are classified symmetrically.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import attackdrift as ad  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "data" / "results"
DOMAINS = ["enterprise-attack", "mobile-attack", "ics-attack"]


def classify_additions(a: ad.Snapshot, b: ad.Snapshot) -> dict[str, int]:
    ga, gb = a.group_techniques(), b.group_techniques()
    edges_a = {(g, t) for g, ts in ga.items() for t in ts}
    edges_b = {(g, t) for g, ts in gb.items() for t in ts}
    added = edges_b - edges_a
    sub_b = b.sub_of()
    rev_b = b.revoked_by()
    # technique in A that B revoked into something else
    a_tech = set(a.tech)
    counts = dict.fromkeys(
        ["new_actor", "ontology_refinement", "revocation_remap",
         "new_technique_intel", "genuine_new_intel"], 0)
    for g, t in added:
        if g not in a.groups:
            counts["new_actor"] += 1
            continue
        prior = ga.get(g, set())
        # revocation remap: some A-technique of this group resolves to t in B
        if any(ad.resolve_chain(o, rev_b) == t and o != t for o in prior):
            counts["revocation_remap"] += 1
            continue
        if t not in a_tech:
            parent = sub_b.get(t)
            if parent and parent in prior:
                counts["ontology_refinement"] += 1
            else:
                counts["new_technique_intel"] += 1
            continue
        counts["genuine_new_intel"] += 1
    counts["total_added"] = len(added)
    counts["total_removed"] = len(edges_a - edges_b)
    counts["edges_a"] = len(edges_a)
    counts["edges_b"] = len(edges_b)
    return counts


def normalized_growth(a: ad.Snapshot, b: ad.Snapshot, ref: ad.Snapshot) -> dict[str, float]:
    """Growth measured after projecting both releases onto a common reference."""
    ga, gb = a.group_techniques(), b.group_techniques()
    shared_groups = set(ga) & set(gb)
    raw_a = sum(len(ga[g]) for g in shared_groups)
    raw_b = sum(len(gb[g]) for g in shared_groups)
    norm_a = sum(len(ad.normalize(ga[g], ref)) for g in shared_groups)
    norm_b = sum(len(ad.normalize(gb[g], ref)) for g in shared_groups)
    return {
        "shared_groups": len(shared_groups),
        "raw_a": raw_a, "raw_b": raw_b,
        "norm_a": norm_a, "norm_b": norm_b,
        "raw_growth": (raw_b - raw_a) / raw_a if raw_a else None,
        "norm_growth": (norm_b - norm_a) / norm_a if norm_a else None,
    }


def main() -> None:
    con = ad.connect()
    results = {}
    for domain in DOMAINS:
        majors = ad.major_releases(con, domain)
        snaps = {m.version: ad.load_snapshot(con, domain, m.version) for m in majors}
        ref = snaps[majors[-1].version]
        rows, norm_rows = [], []
        for prev, cur in zip(majors, majors[1:]):
            a, b = snaps[prev.version], snaps[cur.version]
            c = classify_additions(a, b)
            c.update({"from": prev.version, "to": cur.version,
                      "from_date": prev.date, "to_date": cur.date})
            rows.append(c)
            n = normalized_growth(a, b, ref)
            n.update({"from": prev.version, "to": cur.version,
                      "from_date": prev.date, "to_date": cur.date})
            norm_rows.append(n)
        # cumulative, first post-restructure release -> latest
        agg = dict.fromkeys(
            ["new_actor", "ontology_refinement", "revocation_remap",
             "new_technique_intel", "genuine_new_intel", "total_added",
             "total_removed"], 0)
        for r in rows:
            for k in agg:
                agg[k] += r[k]
        results[domain] = {"transitions": rows, "normalized": norm_rows,
                           "cumulative": agg}
        print(f"{domain}: cumulative {agg}", file=sys.stderr)
    (OUT / "e4_growth.json").write_text(json.dumps(results, indent=1))
    print(f"wrote {OUT/'e4_growth.json'}", file=sys.stderr)


if __name__ == "__main__":
    main()
