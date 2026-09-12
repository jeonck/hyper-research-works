#!/usr/bin/env python3
"""L3-C3: recurrence hazard of restructuring events, + ICS/Mobile event anatomy."""
import sys, json, random, itertools
sys.path.insert(0,'/home/user/hyper-research-works/code')
import attackdrift as ad
from datetime import date
def d(s):
    y,m,dd=(s or '1970-01-01')[:10].split('-'); return date(int(y),int(m),int(dd))

res=json.load(open('/home/user/hyper-research-works/data/results/e1_e2_e3.json'))
print("== restructuring events: major-to-major transitions with identifier Jaccard < 0.80 ==")
ev=[]; tot=0; span=0
for dom,v in res.items():
    rels=v['releases']
    span+= (d(rels[-1]['date'])-d(rels[0]['date'])).days/365.25
    for c in v['churn']:
        tot+=1
        if c['jaccard_id']<0.80:
            ev.append((dom,c['from'],c['to'],c['to_date'],round(c['jaccard_id'],3),
                       c['newly_revoked'],c['newly_deprecated'],c['vanished']))
for e in ev: print("  ",e)
print(f"  {len(ev)} events / {tot} major transitions = {len(ev)/tot:.3f} per transition")
print(f"  total domain-years observed = {span:.1f}  ->  one event per {span/len(ev):.2f} domain-years")
print(f"  Enterprise alone: 1 event / {(d('2026-04-28')-d('2018-01-17')).days/365.25:.1f} yr")

# --- permutation p for the best lead-1 correlation ---
import math
def spearman(x,y):
    n=len(x)
    def rk(v):
        s=sorted(range(n),key=lambda i:v[i]); r=[0.0]*n; i=0
        while i<n:
            j=i
            while j+1<n and v[s[j+1]]==v[s[i]]: j+=1
            for k in range(i,j+1): r[s[k]]=(i+j)/2+1
            i=j+1
        return r
    rx,ry=rk(x),rk(y); mx=sum(rx)/n; my=sum(ry)/n
    num=sum((a-mx)*(b-my) for a,b in zip(rx,ry))
    den=(sum((a-mx)**2 for a in rx)*sum((b-my)**2 for b in ry))**.5
    return num/den if den else 0.0
det=[0.000,0.995,0.045,0.000,0.098,0.476,0.040,0.099,0.120,0.078,0.000,0.022,0.003,0.006,0.000,0.008,0.859]
kil=[0.000,0.000,0.000,0.000,0.526,0.000,0.000,0.002,0.004,0.000,0.000,0.000,0.000,0.000,0.002,0.000,0.025]
obs=spearman(det,kil); random.seed(0)
cnt=sum(1 for _ in range(20000) if abs(spearman(det,random.sample(kil,len(kil))))>=abs(obs))
print(f"\n== lead-1 detection-edit -> next-release kill rate: rho={obs:+.3f}, permutation p={cnt/20000:.3f} (n=17) ==")

con=ad.connect()
print("\n== ICS v18.1 -> v19.2 anatomy ==")
a=ad.load_snapshot(con,'ics-attack','18.1'); b=ad.load_snapshot(con,'ics-attack','19.2')
la,lb=a.live_tech(),b.live_tech(); rev=b.revoked_by()
dead=la-lb
print("  live 18.1=%d  live 19.2=%d  added=%d  dead=%d"%(len(la),len(lb),len(lb-la),len(dead)))
print("  dead ids:",sorted(dead))
print("  recoverable via revoked-by:",sorted(x for x in dead if ad.resolve_chain(x,rev) in lb))
print("  replacements:",{x:ad.resolve_chain(x,rev) for x in sorted(dead)})
print("  new ids:",sorted(lb-la)[:40])
print("  ICS group->technique edges 18.1=%d 19.2=%d"%(
    sum(len(v) for v in a.group_techniques().values()),sum(len(v) for v in b.group_techniques().values())))

print("\n== Mobile v2.0 -> v3.0 anatomy (Jaccard 0.0) ==")
a=ad.load_snapshot(con,'mobile-attack','2.0'); b=ad.load_snapshot(con,'mobile-attack','3.0')
print("  sample v2.0 ids:",sorted(a.live_tech())[:6])
print("  sample v3.0 ids:",sorted(b.live_tech())[:6])
print("  stix_id overlap:",len(set(a.by_stix)&set(b.by_stix)),"of",len(a.by_stix),"/",len(b.by_stix))
sa={a.tech[t]['name'] for t in a.live_tech()}; sb={b.tech[t]['name'] for t in b.live_tech()}
print("  technique-NAME overlap:",len(sa&sb),"of",len(sa),"/",len(sb))
print("  revoked-by edges in v3.0:",len(b.revoked_by()))

print("\n== Mobile v10.0 -> v11.3 anatomy ==")
a=ad.load_snapshot(con,'mobile-attack','10.1'); b=ad.load_snapshot(con,'mobile-attack','11.3')
la,lb=a.live_tech(),b.live_tech(); rev=b.revoked_by()
dead=la-lb
print("  live=%d->%d dead=%d recoverable=%d"%(len(la),len(lb),len(dead),
      sum(1 for x in dead if ad.resolve_chain(x,rev) in lb)))
