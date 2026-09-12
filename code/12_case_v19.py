#!/usr/bin/env python3
"""Case study: the blast radius of the v19.0 revocation wave (T1562 family)."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import attackdrift as ad  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "data" / "results"
PREV, CUR = "18.1", "19.2"


def main() -> None:
    con = ad.connect()
    p = ad.load_snapshot(con, "enterprise-attack", PREV)
    n = ad.load_snapshot(con, "enterprise-attack", CUR)
    rev = n.revoked_by()
    fam = {t for t in p.live_tech() if t in n.tech and n.tech[t]["revoked"]}

    uses = Counter()
    group_edges = software_edges = 0
    groups_hit: dict[str, set[str]] = {}
    for s, t in p.rels.get("uses", []):
        so, to = p.by_stix.get(s), p.by_stix.get(t)
        if not to or to["otype"] != ad.TECH or not to["attack_id"]:
            continue
        uses[to["attack_id"]] += 1
        if to["attack_id"] not in fam or not so:
            continue
        if so["otype"] == ad.GROUP:
            group_edges += 1
            if so["attack_id"]:
                groups_hit.setdefault(so["attack_id"], set()).add(to["attack_id"])
        elif so["otype"] in ad.SOFTWARE:
            software_edges += 1

    def touching(rtype: str) -> int:
        return sum(1 for _, t in p.rels.get(rtype, [])
                   if (o := p.by_stix.get(t)) and o.get("attack_id") in fam)

    rank = {a: i + 1 for i, (a, _) in enumerate(uses.most_common())}
    out = {
        "previous_release": PREV, "current_release": CUR,
        "revoked_techniques": sorted(fam),
        "n_revoked": len(fam),
        "replacements": {t: rev.get(t) for t in sorted(fam)},
        "names": {t: p.tech[t]["name"] for t in sorted(fam)},
        "group_technique_edges_affected": group_edges,
        "software_technique_edges_affected": software_edges,
        "mitigations_affected": touching("mitigates"),
        "detections_affected": touching("detects"),
        "groups_losing_an_identifier": len(groups_hit),
        "groups_total": len(p.group_techniques()),
        "usage_rank": {t: {"edges": uses.get(t, 0), "rank": rank.get(t),
                           "of": len(uses)} for t in sorted(fam)},
    }
    (OUT / "e8_case_v19.json").write_text(json.dumps(out, indent=1))
    print(json.dumps({k: v for k, v in out.items()
                      if k not in ("replacements", "names", "usage_rank",
                                   "revoked_techniques")}, indent=1))


if __name__ == "__main__":
    main()
