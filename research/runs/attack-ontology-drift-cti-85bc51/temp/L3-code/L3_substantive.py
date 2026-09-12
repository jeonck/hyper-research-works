#!/usr/bin/env python3
"""L3-C4: staleness clock under a SUBSTANTIVE-rewrite definition (token Jaccard < 0.8),
so the result cannot be dismissed as cosmetic/typo edits. Enterprise, post-v7.0 cohorts."""
import sys, re, json
from datetime import date
sys.path.insert(0,'/home/user/hyper-research-works/code'); import attackdrift as ad
W=re.compile(r"[a-z0-9]+")
def tok(s): return set(W.findall((s or "").lower()))
def d(s):
    y,m,dd=(s or '1970-01-01')[:10].split('-'); return date(int(y),int(m),int(dd))
def tset(o): return set(filter(None,(o["tactics"] or "").split(",")))
con=ad.connect(); DOM='enterprise-attack'
rels=ad.releases(con,DOM)
snaps={r.version: ad.load_snapshot(con,DOM,r.version,with_desc=True) for r in rels}
majors=[m for m in ad.major_releases(con,DOM) if int(m.version.split('.')[0])>=7]
print(f"{'src':>5} {'n':>4} | {'t10_sub':>7} {'rel':>5} | {'t25_sub':>7} {'rel':>5} | {'t50_sub':>7} | final_sub  final_any")
for src in majors:
    a=snaps[src.version]; base=a.live_tech()
    da={t: a.by_stix[a.tech[t]['stix_id']].get('description') for t in base}
    curve=[]
    for tgt in rels:
        if tgt.ordinal<=src.ordinal: continue
        b=snaps[tgt.version]; live=b.live_tech()
        hard={x for x in base if x not in live}
        sub=set(hard); any_=set(hard)
        for x in base-hard:
            if a.tech[x]['desc_sha']!=b.tech[x]['desc_sha'] or tset(a.tech[x])!=tset(b.tech[x]): any_.add(x)
            j=ad.jaccard(tok(da[x]), tok(b.by_stix[b.tech[x]['stix_id']].get('description')))
            if j<0.8 or tset(a.tech[x])!=tset(b.tech[x]): sub.add(x)
        curve.append({'tgt':tgt.version,'yrs':(d(tgt.date)-d(src.date)).days/365.25,
                      'sub':len(sub)/len(base),'any':len(any_)/len(base)})
    def hit(th):
        h=next((c for c in curve if c['sub']>=th),None)
        return (round(h['yrs'],2),h['tgt']) if h else (None,None)
    t10=hit(.10); t25=hit(.25); t50=hit(.50)
    f=curve[-1]
    print(f"{src.version:>5} {len(base):>4} | {str(t10[0]):>7} {str(t10[1]):>5} | {str(t25[0]):>7} {str(t25[1]):>5} | {str(t50[0]):>7} | {f['sub']:.3f}      {f['any']:.3f}")
