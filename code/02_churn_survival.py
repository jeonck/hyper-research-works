#!/usr/bin/env python3
"""E1 release churn, E2 identifier survival, E3 silent semantic drift."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import attackdrift as ad  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "data" / "results"
DOMAINS = ["enterprise-attack", "mobile-attack", "ics-attack"]

WORD = re.compile(r"[a-z0-9]+")


def tokens(text: str | None) -> set[str]:
    return set(WORD.findall((text or "").lower()))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    con = ad.connect()
    results: dict[str, dict] = {}

    for domain in DOMAINS:
        majors = ad.major_releases(con, domain)
        snaps = {m.version: ad.load_snapshot(con, domain, m.version, with_desc=True)
                 for m in majors}

        # ---------------- E1: consecutive-release churn ----------------
        churn = []
        for prev, cur in zip(majors, majors[1:]):
            a, b = snaps[prev.version], snaps[cur.version]
            la, lb = a.live_tech(), b.live_tech()
            surviving = la & lb
            renamed = sum(1 for t in surviving if a.tech[t]["name"] != b.tech[t]["name"])
            desc_changed = sum(1 for t in surviving
                               if a.tech[t]["desc_sha"] != b.tech[t]["desc_sha"])
            det_changed = sum(1 for t in surviving
                              if a.tech[t]["det_sha"] != b.tech[t]["det_sha"])
            tactic_changed = sum(1 for t in surviving
                                 if set(filter(None, (a.tech[t]["tactics"] or "").split(","))) !=
                                 set(filter(None, (b.tech[t]["tactics"] or "").split(","))))
            newly_revoked = {t for t in la if t in b.tech and b.tech[t]["revoked"]}
            newly_deprecated = {t for t in la if t in b.tech and b.tech[t]["deprecated"]}
            vanished = {t for t in la if t not in b.tech}
            added = lb - la
            ga = a.group_techniques()
            gb = b.group_techniques()
            edges_a = {(g, t) for g, ts in ga.items() for t in ts}
            edges_b = {(g, t) for g, ts in gb.items() for t in ts}
            churn.append({
                "from": prev.version, "to": cur.version,
                "from_date": prev.date, "to_date": cur.date,
                "live_from": len(la), "live_to": len(lb),
                "added": len(added), "newly_revoked": len(newly_revoked),
                "newly_deprecated": len(newly_deprecated), "vanished": len(vanished),
                "surviving": len(surviving), "renamed": renamed,
                "desc_changed": desc_changed, "detection_changed": det_changed,
                "tactic_changed": tactic_changed,
                "group_edges_from": len(edges_a), "group_edges_to": len(edges_b),
                "group_edges_added": len(edges_b - edges_a),
                "group_edges_removed": len(edges_a - edges_b),
                "jaccard_id": ad.jaccard(la, lb),
            })

        # ---------------- E2: identifier survival ----------------------
        survival = []
        for i, src in enumerate(majors):
            base = snaps[src.version].live_tech()
            if not base:
                continue
            for tgt in majors[i:]:
                t = snaps[tgt.version]
                live = t.live_tech()
                rev = t.revoked_by()
                present = {x for x in base if x in t.tech}
                still_live = {x for x in base if x in live}
                revoked = {x for x in base if x in t.tech and t.tech[x]["revoked"]}
                deprecated = {x for x in base if x in t.tech and t.tech[x]["deprecated"]}
                absent = base - present
                recoverable = {x for x in (revoked | absent)
                               if ad.resolve_chain(x, rev) in live}
                survival.append({
                    "src": src.version, "tgt": tgt.version,
                    "src_date": src.date, "tgt_date": tgt.date,
                    "n": len(base),
                    "live": len(still_live), "revoked": len(revoked),
                    "deprecated": len(deprecated), "absent": len(absent),
                    "recoverable_via_revoked_by": len(recoverable),
                    "survival_rate": len(still_live) / len(base),
                })

        # ---------------- E3: silent semantic drift --------------------
        semantic = []
        for i, src in enumerate(majors):
            a = snaps[src.version]
            base = a.live_tech()
            if not base:
                continue
            desc_a = {t: next((a.by_stix[o["stix_id"]].get("description")
                               for o in [a.tech[t]]), None) for t in base}
            for tgt in majors[i + 1:]:
                b = snaps[tgt.version]
                stable = {t for t in base if t in b.live_tech()}
                if not stable:
                    continue
                changed, sims, big = 0, [], 0
                # iterate in a fixed order: set iteration order changes the
                # summation order and moves the last digit of the mean
                for t in sorted(stable):
                    if a.tech[t]["desc_sha"] != b.tech[t]["desc_sha"]:
                        changed += 1
                    ta = tokens(desc_a.get(t))
                    tb = tokens(b.by_stix[b.tech[t]["stix_id"]].get("description"))
                    if ta or tb:
                        s = ad.jaccard(ta, tb)
                        sims.append(s)
                        if s < 0.8:
                            big += 1
                semantic.append({
                    "src": src.version, "tgt": tgt.version,
                    "src_date": src.date, "tgt_date": tgt.date,
                    "id_stable": len(stable),
                    "desc_changed": changed,
                    "desc_changed_frac": changed / len(stable),
                    "mean_token_jaccard": (sum(sorted(sims)) / len(sims)) if sims else None,
                    "substantial_rewrites": big,
                    "substantial_frac": big / len(sims) if sims else None,
                })

        results[domain] = {
            "releases": [{"version": m.version, "date": m.date} for m in majors],
            "churn": churn, "survival": survival, "semantic": semantic,
        }
        print(f"{domain}: {len(churn)} transitions, {len(survival)} survival pairs",
              file=sys.stderr)

    (OUT / "e1_e2_e3.json").write_text(json.dumps(results, indent=1))
    print(f"wrote {OUT/'e1_e2_e3.json'}", file=sys.stderr)


if __name__ == "__main__":
    main()
