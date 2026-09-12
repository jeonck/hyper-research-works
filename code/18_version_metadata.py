#!/usr/bin/env python3
"""E11: is x_mitre_version a reliable signal that a technique's text changed?

For every consecutive pair of major releases and every technique live in both,
cross-tabulate whether the description text changed against whether the object's
x_mitre_version was incremented. A reliable change signal would put everything on
the diagonal.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import attackdrift as ad  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "data" / "results"
DOMAIN = "enterprise-attack"


def as_tuple(v: str | None) -> tuple:
    try:
        return tuple(int(x) for x in (v or "0").split("."))
    except ValueError:
        return (0,)


def main() -> None:
    con = ad.connect()
    majors = ad.major_releases(con, DOMAIN)
    snaps = {m.version: ad.load_snapshot(con, DOMAIN, m.version) for m in majors}
    tot = {"text_and_bump": 0, "text_no_bump": 0, "bump_no_text": 0, "neither": 0}
    rows = []
    for prev, cur in zip(majors, majors[1:]):
        a, b = snaps[prev.version], snaps[cur.version]
        shared = a.live_tech() & b.live_tech()
        cell = dict.fromkeys(tot, 0)
        for t in shared:
            text = a.tech[t]["desc_sha"] != b.tech[t]["desc_sha"]
            bump = as_tuple(b.tech[t]["obj_version"]) > as_tuple(a.tech[t]["obj_version"])
            key = ("text_and_bump" if text and bump else
                   "text_no_bump" if text else
                   "bump_no_text" if bump else "neither")
            cell[key] += 1
        for k in tot:
            tot[k] += cell[k]
        cell.update({"from": prev.version, "to": cur.version, "shared": len(shared)})
        rows.append(cell)

    pairs = sum(tot.values())
    changed = tot["text_and_bump"] + tot["text_no_bump"]
    signalled = tot["text_and_bump"] + tot["bump_no_text"]
    summary = {
        "carried_over_pairs": pairs,
        "description_changed": changed,
        "description_changed_frac": changed / pairs,
        "changed_without_version_bump": tot["text_no_bump"],
        "changed_without_bump_frac": tot["text_no_bump"] / changed if changed else 0,
        "bumped_without_text_change": tot["bump_no_text"],
        "bumped_without_text_frac": tot["bump_no_text"] / signalled if signalled else 0,
        "precision_of_version_bump": (tot["text_and_bump"] / signalled) if signalled else 0,
        "recall_of_version_bump": (tot["text_and_bump"] / changed) if changed else 0,
    }
    (OUT / "e11_version_metadata.json").write_text(
        json.dumps({"summary": summary, "per_transition": rows, "totals": tot}, indent=1))
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
