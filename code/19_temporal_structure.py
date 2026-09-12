#!/usr/bin/env python3
"""E12: the temporal structure of drift risk — two clocks and a recurrence hazard.

Consolidates four analyses:

  C1 staleness clocks   For each major release cohort, time until X% of its live
                        identifiers are stale, under three definitions evaluated
                        against EVERY later release including patches:
                          hard      no longer live in the target
                          unrecov   hard and transitive revoked-by does not land live
                          semantic  hard, or still live with an edited description
                                    or a changed tactic set
  C2 substantive clock  the semantic clock restricted to substantive rewrites
                        (description token Jaccard < 0.8), so the result cannot be
                        dismissed as typo-level editing
  C3 recurrence hazard  how often a restructuring event (major-to-major identifier
                        Jaccard < 0.80) occurs, per transition and per domain-year,
                        with the anatomy of each event
  C4 leading indicators whether description edits, tactic changes or version-field
                        churn in one release predict a restructuring in the next
"""
from __future__ import annotations

import json
import re
import statistics
import sys
from datetime import date
from itertools import permutations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import attackdrift as ad  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "data" / "results"
DOMAINS = ["enterprise-attack", "mobile-attack", "ics-attack"]
THRESH = [0.05, 0.10, 0.25, 0.50]
WORD = re.compile(r"[a-z0-9]+")
JACCARD_EVENT = 0.80


def parse(s: str | None) -> date:
    y, m, d = (s or "1970-01-01")[:10].split("-")
    return date(int(y), int(m), int(d))


def tactics(o: dict) -> set[str]:
    return set(filter(None, (o["tactics"] or "").split(",")))


def tokens(text: str | None) -> set[str]:
    return set(WORD.findall((text or "").lower()))


def staleness(con) -> dict:
    out = {}
    for dom in DOMAINS:
        rels = ad.releases(con, dom)
        snaps = {r.version: ad.load_snapshot(con, dom, r.version, with_desc=True)
                 for r in rels}
        rows = []
        for src in ad.major_releases(con, dom):
            a = snaps[src.version]
            base = a.live_tech()
            if not base:
                continue
            desc_a = {t: a.by_stix[a.tech[t]["stix_id"]].get("description") for t in base}
            curve = []
            for tgt in rels:
                if tgt.ordinal <= src.ordinal:
                    continue
                b = snaps[tgt.version]
                live, rev = b.live_tech(), b.revoked_by()
                hard = {x for x in base if x not in live}
                unrec = {x for x in hard if ad.resolve_chain(x, rev) not in live}
                sem, sub = set(hard), set(hard)
                for x in base - hard:
                    moved = tactics(a.tech[x]) != tactics(b.tech[x])
                    edited = a.tech[x]["desc_sha"] != b.tech[x]["desc_sha"]
                    if edited or moved:
                        sem.add(x)
                    j = ad.jaccard(tokens(desc_a[x]),
                                   tokens(b.by_stix[b.tech[x]["stix_id"]].get("description")))
                    if j < 0.8 or moved:
                        sub.add(x)
                curve.append({"tgt": tgt.version, "tgt_date": tgt.date,
                              "years": (parse(tgt.date) - parse(src.date)).days / 365.25,
                              "hard": len(hard) / len(base),
                              "unrec": len(unrec) / len(base),
                              "sem": len(sem) / len(base),
                              "sub": len(sub) / len(base)})
            rec = {"domain": dom, "src": src.version, "src_date": src.date, "n": len(base)}
            for defn in ("hard", "unrec", "sem", "sub"):
                for th in THRESH:
                    hit = next((c for c in curve if c[defn] >= th), None)
                    rec[f"t{int(th*100)}_{defn}"] = round(hit["years"], 2) if hit else None
                    rec[f"r{int(th*100)}_{defn}"] = hit["tgt"] if hit else None
            rec["final"] = {k: curve[-1][k] for k in ("hard", "unrec", "sem", "sub")} if curve else {}
            # fixed-horizon fractions: censoring-free comparison across cohorts
            for horizon in (1, 2, 3):
                at = [c for c in curve if c["years"] <= horizon]
                rec[f"at_{horizon}y"] = ({k: at[-1][k] for k in ("hard", "unrec", "sem", "sub")}
                                         if at and curve[-1]["years"] >= horizon else None)
            rows.append(rec)
        out[dom] = rows
    return out


def recurrence(e123: dict) -> dict:
    events, transitions, domain_years = [], 0, 0.0
    for dom, v in e123.items():
        rels = v["releases"]
        domain_years += (parse(rels[-1]["date"]) - parse(rels[0]["date"])).days / 365.25
        for c in v["churn"]:
            transitions += 1
            if c["jaccard_id"] < JACCARD_EVENT:
                events.append({"domain": dom, "from": c["from"], "to": c["to"],
                               "date": c["to_date"], "jaccard": c["jaccard_id"],
                               "revoked": c["newly_revoked"],
                               "deprecated": c["newly_deprecated"],
                               "vanished": c["vanished"], "added": c["added"]})
    return {"events": events, "n_events": len(events), "n_transitions": transitions,
            "hazard_per_transition": len(events) / transitions if transitions else 0.0,
            "observed_domain_years": domain_years,
            "years_per_event": domain_years / len(events) if events else None}


def spearman(xs: list[float], ys: list[float]) -> float:
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        for pos, i in enumerate(order):
            r[i] = pos + 1
        return r
    rx, ry = rank(xs), rank(ys)
    mx, my = statistics.fmean(rx), statistics.fmean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return num / den if den else 0.0


def permutation_p(xs: list[float], ys: list[float], iters: int = 20000) -> float:
    import random
    obs = abs(spearman(xs, ys))
    rng = random.Random(20260912)
    hits = 0
    pool = list(ys)
    for _ in range(iters):
        rng.shuffle(pool)
        if abs(spearman(xs, pool)) >= obs:
            hits += 1
    return (hits + 1) / (iters + 1)


def leading_indicators(e123: dict) -> dict:
    """Does churn in transition i predict an identifier collapse in transition i+1?"""
    out = {}
    for dom, v in e123.items():
        ch = v["churn"]
        if len(ch) < 6:
            continue
        rows = {}
        for signal in ("desc_changed", "tactic_changed", "detection_changed", "renamed"):
            xs, ys = [], []
            for i in range(len(ch) - 1):
                denom = max(1, ch[i]["surviving"])
                xs.append(ch[i][signal] / denom)
                ys.append(1.0 - ch[i + 1]["jaccard_id"])
            rho = spearman(xs, ys)
            rows[signal] = {"rho": rho, "n": len(xs), "p_permutation": permutation_p(xs, ys)}
        out[dom] = rows
    return out


def main() -> None:
    con = ad.connect()
    e123 = json.loads((OUT / "e1_e2_e3.json").read_text())
    result = {
        "staleness_clocks": staleness(con),
        "recurrence": recurrence(e123),
        "leading_indicators": leading_indicators(e123),
    }
    (OUT / "e12_temporal_structure.json").write_text(json.dumps(result, indent=1))

    r = result["recurrence"]
    print(f"restructuring events (major-to-major identifier Jaccard < {JACCARD_EVENT}): "
          f"{r['n_events']} of {r['n_transitions']} transitions "
          f"({r['hazard_per_transition']:.3f} per transition); "
          f"{r['observed_domain_years']:.1f} observed domain-years, one event per "
          f"{r['years_per_event']:.1f} domain-years", file=sys.stderr)
    for e in r["events"]:
        print(f"  {e['domain']:18} v{e['from']}→v{e['to']} {e['date']} "
              f"J={e['jaccard']:.3f} revoked={e['revoked']} deprecated={e['deprecated']} "
              f"vanished={e['vanished']}", file=sys.stderr)
    ent = result["staleness_clocks"]["enterprise-attack"]
    print("\nEnterprise substantive-rewrite clock (years to 10% / 25% / 50%):", file=sys.stderr)
    for row in ent:
        if int(row["src"].split(".")[0]) >= 7:
            print(f"  v{row['src']:>5} n={row['n']:>3} "
                  f"t10={row['t10_sub']} t25={row['t25_sub']} t50={row['t50_sub']}",
                  file=sys.stderr)
    print(f"\nwrote {OUT/'e12_temporal_structure.json'}", file=sys.stderr)


if __name__ == "__main__":
    main()
