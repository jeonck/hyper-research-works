#!/usr/bin/env python3
"""L3-C1: staleness clock. How long until X% of a pinned label set is stale?

Three staleness definitions, evaluated against EVERY subsequent release
(including patch releases), not just majors:
  hard      : source-live technique ID is no longer live in the target
              (absent, revoked, or deprecated)
  unrecov   : hard AND transitive revoked-by resolution does not land on a live ID
  semantic  : hard OR (still live but desc_sha changed) OR (still live but tactic set changed)
"""
import sys, json
from datetime import date
sys.path.insert(0, '/home/user/hyper-research-works/code')
import attackdrift as ad

def d(s):
    y, m, dd = (s or "1970-01-01")[:10].split("-")
    return date(int(y), int(m), int(dd))

def tset(o):
    return set(filter(None, (o["tactics"] or "").split(",")))

con = ad.connect()
THRESH = [0.05, 0.10, 0.25, 0.50]
out = {}
for dom in ["enterprise-attack", "mobile-attack", "ics-attack"]:
    rels = ad.releases(con, dom)
    snaps = {r.version: ad.load_snapshot(con, dom, r.version) for r in rels}
    majors = ad.major_releases(con, dom)
    rows = []
    for src in majors:
        a = snaps[src.version]
        base = a.live_tech()
        if not base:
            continue
        curve = []
        for tgt in rels:
            if tgt.ordinal <= src.ordinal:
                continue
            b = snaps[tgt.version]
            live = b.live_tech(); rev = b.revoked_by()
            hard = {x for x in base if x not in live}
            unrec = {x for x in hard if ad.resolve_chain(x, rev) not in live}
            sem = set(hard)
            for x in base - hard:
                if a.tech[x]["desc_sha"] != b.tech[x]["desc_sha"] or tset(a.tech[x]) != tset(b.tech[x]):
                    sem.add(x)
            curve.append({
                "tgt": tgt.version, "tgt_date": tgt.date,
                "years": (d(tgt.date) - d(src.date)).days / 365.25,
                "hard": len(hard)/len(base), "unrec": len(unrec)/len(base),
                "sem": len(sem)/len(base)})
        rec = {"src": src.version, "src_date": src.date, "n": len(base), "curve": curve}
        for defn in ("hard", "unrec", "sem"):
            for th in THRESH:
                hit = next((c for c in curve if c[defn] >= th), None)
                rec[f"t{int(th*100)}_{defn}"] = round(hit["years"], 2) if hit else None
                rec[f"r{int(th*100)}_{defn}"] = hit["tgt"] if hit else None
        rows.append(rec)
    out[dom] = rows

json.dump(out, open('/tmp/claude-0/-home-user-hyper-research-works/aa6e0fd0-b155-51a6-ad4a-ebbe528f3807/scratchpad/L3_staleness.json','w'), indent=1)

for dom, rows in out.items():
    print("="*70); print(dom)
    print(f"{'src':>5} {'date':>11} {'n':>4} | {'t10 hard':>9} {'rel':>5} | {'t10 unrec':>9} {'rel':>5} | {'t10 sem':>8} {'rel':>5} | {'t25 sem':>8}")
    for r in rows:
        print(f"{r['src']:>5} {r['src_date']:>11} {r['n']:>4} | "
              f"{str(r['t10_hard']):>9} {str(r['r10_hard']):>5} | "
              f"{str(r['t10_unrec']):>9} {str(r['r10_unrec']):>5} | "
              f"{str(r['t10_sem']):>8} {str(r['r10_sem']):>5} | {str(r['t25_sem']):>8}")
