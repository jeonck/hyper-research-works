#!/usr/bin/env python3
"""E13: the tactic layer, and the arity of ATT&CK's revocation relation.

Two questions the identifier-level analysis cannot see:

1. Does the tactic layer have a retirement mechanism at all? Techniques carry
   typed revoked-by edges; tactics are checked here for the same.
2. Is the revocation relation ever one-to-many? A semantic split of one concept
   into several can only be represented faithfully by a 1:N relation. If the
   relation is always N:1 or 1:1, splits are recorded as merges onto whichever
   survivor the curator picked, and the crosswalk is lossy by construction.

Also records identifier recycling: an ATT&CK identifier retained across releases
while the object it names is renamed, which is the change class no consumer can
detect from the identifier alone.
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import attackdrift as ad  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "data" / "results"
DOMAINS = ["enterprise-attack", "mobile-attack", "ics-attack"]
TACTIC = "x-mitre-tactic"


def main() -> None:
    con = ad.connect()

    tactic_revocations = con.execute(
        "SELECT COUNT(*) FROM relationships r JOIN objects o "
        "ON o.domain = r.domain AND o.version = r.version AND o.stix_id = r.source_ref "
        "WHERE r.rel_type = 'revoked-by' AND o.otype = ?", (TACTIC,)).fetchone()[0]
    total_revocations = con.execute(
        "SELECT COUNT(*) FROM relationships WHERE rel_type = 'revoked-by'").fetchone()[0]

    arity = {}
    recycled: list[dict] = []
    for dom in DOMAINS:
        rels = ad.releases(con, dom)
        newest = ad.load_snapshot(con, dom, rels[-1].version)
        src, tgt = Counter(), Counter()
        for a, b in newest.rels.get("revoked-by", []):
            src[a] += 1
            tgt[b] += 1
        arity[dom] = {
            "release": rels[-1].version,
            "revocation_edges": sum(src.values()),
            "sources_with_multiple_targets": sum(1 for v in src.values() if v > 1),
            "targets_absorbing_multiple": sum(1 for v in tgt.values() if v > 1),
            "max_predecessors_absorbed": max(tgt.values()) if tgt else 0,
        }

        # identifier recycling: same ATT&CK id, name changes, object not retired
        prev = None
        for r in rels:
            snap = ad.load_snapshot(con, dom, r.version)
            cur = {o["attack_id"]: o for o in snap.by_stix.values()
                   if o["attack_id"] and o["otype"] in (TACTIC, ad.TECH)}
            if prev is not None:
                for aid, o in cur.items():
                    p = prev.get(aid)
                    if not p or o["otype"] != p["otype"]:
                        continue
                    if p["name"] != o["name"] and not o["revoked"] and not o["deprecated"]:
                        recycled.append({
                            "domain": dom, "from": prev_version, "to": r.version,
                            "attack_id": aid, "otype": o["otype"],
                            "old_name": p["name"], "new_name": o["name"],
                            "stix_id_unchanged": p["stix_id"] == o["stix_id"],
                            "object_version_from": p["obj_version"],
                            "object_version_to": o["obj_version"],
                        })
            prev, prev_version = cur, r.version

    # how often does the protocol's roll-up branch actually have anything to do?
    rollup_fired = rollup_checked = 0
    for dom in DOMAINS:
        rels = ad.releases(con, dom)
        tw = ad.load_snapshot(con, dom, rels[-1].version)
        trev, tsub, tlive = tw.revoked_by(), tw.sub_of(), tw.live_tech()
        for r in ad.major_releases(con, dom):
            snap = ad.load_snapshot(con, dom, r.version)
            for aid in snap.live_tech():
                rollup_checked += 1
                cur = ad.resolve_chain(aid, trev)
                if cur in tlive:
                    continue
                parent = tsub.get(cur) or (cur.split(".")[0] if "." in cur else None)
                if parent and ad.resolve_chain(parent, trev) in tlive:
                    rollup_fired += 1

    tactic_renames = [r for r in recycled if r["otype"] == TACTIC]
    result = {
        "tactic_revocation_edges": tactic_revocations,
        "total_revocation_edges": total_revocations,
        "revocation_arity": arity,
        "rollup_branch_fired": rollup_fired,
        "rollup_resolutions_checked": rollup_checked,
        "renamed_in_place_total": len(recycled),
        "renamed_in_place_tactics": tactic_renames,
        "renamed_in_place_techniques_sample": [r for r in recycled
                                               if r["otype"] == ad.TECH][:25],
    }
    (OUT / "e13_tactic_layer.json").write_text(json.dumps(result, indent=1))
    print(f"revoked-by edges originating at a tactic: {tactic_revocations} of "
          f"{total_revocations} across the whole corpus", file=sys.stderr)
    for dom, a in arity.items():
        print(f"  {dom} v{a['release']}: {a['revocation_edges']} edges, "
              f"{a['sources_with_multiple_targets']} one-to-many splits, "
              f"{a['targets_absorbing_multiple']} many-to-one merges "
              f"(max {a['max_predecessors_absorbed']} absorbed)", file=sys.stderr)
    print(f"  roll-up branch fired {rollup_fired} times in {rollup_checked} resolutions",
          file=sys.stderr)
    print(f"  tactics renamed in place (identifier retained, object not retired): "
          f"{len(tactic_renames)}", file=sys.stderr)
    for r in tactic_renames:
        print(f"    {r['domain']} v{r['from']}→v{r['to']} {r['attack_id']}: "
              f"{r['old_name']} → {r['new_name']} "
              f"(same STIX id: {r['stix_id_unchanged']}, object version "
              f"{r['object_version_from']} → {r['object_version_to']})", file=sys.stderr)
    print(f"wrote {OUT/'e13_tactic_layer.json'}", file=sys.stderr)


if __name__ == "__main__":
    main()
