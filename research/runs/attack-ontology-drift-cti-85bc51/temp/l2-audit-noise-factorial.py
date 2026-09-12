#!/usr/bin/env python3
"""L2 adversarial audit of E5: (a) noise x drift factorial, (b) specificity stratification."""
import json, math, random, statistics, sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0, '/home/user/hyper-research-works/code')
import attackdrift as ad
from importlib import import_module
attr = import_module("04_attribution")

DOMAIN="enterprise-attack"; SEED=20260912; K=10; N=1200
RHOS=[0.0,0.1,0.2,0.4]
VS=["1.0","6.0","12.0","18.0"]

def confusables(w):
    """technique -> list of 'same-labeller-could-have-said' alternatives."""
    sub=w.sub_of(); live=w.live_tech()
    kids=defaultdict(list)
    for c,p in sub.items():
        if c in live: kids[p].append(c)
    tac=defaultdict(list)
    for t in live:
        for x in (w.tech[t]["tactics"] or "").split(","):
            if x: tac[x].append(t)
    out={}
    for t in live:
        alts=set()
        p=sub.get(t)
        if p:
            alts.update(x for x in kids.get(p,[]) if x!=t)
            if p in live: alts.add(p)
        alts.update(kids.get(t,[]))
        if not alts:
            for x in (w.tech[t]["tactics"] or "").split(","):
                if x: alts.update(tac[x][:40])
            alts.discard(t)
        out[t]=sorted(alts)
    return out

def perturb(obs, conf, rho, rng):
    out=set()
    for t in obs:
        if rho>0 and rng.random()<rho and conf.get(t):
            out.add(rng.choice(conf[t]))
        else:
            out.add(t)
    return out

def specific_groups(prof):
    df=defaultdict(int)
    for ts in prof.values():
        for t in ts: df[t]+=1
    return {g for g,ts in prof.items() if any(df[t]==1 for t in ts)}

def run(v,w,rho,rng,conf,back):
    pw=w.group_techniques(include_software=True); pv=v.group_techniques(include_software=True)
    universe=[g for g in sorted(set(pw)&set(pv)) if len(pw[g])>=K and len(pv[g])>=2]
    prof_w={g:pw[g] for g in universe}
    prof_v={g:{back[t] for t in pw[g] if back.get(t)} for g in universe}
    spec=specific_groups(prof_w)
    idf_w,idf_v=attr.idf_weights(prof_w),attr.idf_weights(prof_v)
    hits=defaultdict(list); strat=defaultdict(lambda: defaultdict(list))
    for _ in range(N):
        g=rng.choice(universe)
        obs_w0=set(rng.sample(sorted(prof_w[g]),K))
        obs_w=perturb(obs_w0,conf,rho,rng)
        obs_v={back[t] for t in obs_w if back.get(t)}
        if len(obs_v)<2: continue
        runs={"contemporaneous":(obs_v,prof_v,idf_v),"naive":(obs_v,prof_w,idf_w),
              "normalized":(ad.normalize(obs_v,w),prof_w,idf_w),"oracle":(obs_w,prof_w,idf_w)}
        for c,(o,p,wt) in runs.items():
            h=1.0 if attr.rank_of(g,o,p,wt,universe)==1 else 0.0
            hits[c].append(h)
            strat["spec" if g in spec else "nonspec"][c].append(h)
    out={c:statistics.fmean(x) for c,x in hits.items()}
    out["drift_penalty"]=out["contemporaneous"]-out["naive"]
    out["norm_gain"]=out["normalized"]-out["naive"]
    out["n_groups"]=len(universe); out["n_specific"]=len(spec)
    out["spec_frac"]=len(spec)/len(universe)
    for s in ("spec","nonspec"):
        d=strat[s]
        if d["naive"]:
            out[f"{s}_n"]=len(d["naive"])
            for c in ("contemporaneous","naive","normalized","oracle"):
                out[f"{s}_{c}"]=statistics.fmean(d[c])
            out[f"{s}_drift"]=out[f"{s}_contemporaneous"]-out[f"{s}_naive"]
    return out

def main():
    con=ad.connect()
    w=ad.load_snapshot(con,DOMAIN,"19.0")
    conf=confusables(w)
    res=[]
    for vv in VS:
        v=ad.load_snapshot(con,DOMAIN,vv)
        back=attr.build_backmap(v,w)
        for rho in RHOS:
            rng=random.Random(SEED)
            r=run(v,w,rho,rng,conf,back); r.update({"v":vv,"rho":rho}); res.append(r)
            print(f"v{vv} rho={rho}: cont={r['contemporaneous']:.3f} naive={r['naive']:.3f} "
                  f"drift={r['drift_penalty']:+.3f} norm_gain={r['norm_gain']:+.3f} "
                  f"| spec {r.get('spec_drift',float('nan')):+.3f} (n={r.get('spec_n')}) "
                  f"nonspec {r.get('nonspec_drift',float('nan')):+.3f} (n={r.get('nonspec_n')}) "
                  f"| spec_frac={r['spec_frac']:.3f}", flush=True)
    json.dump(res, open('/tmp/claude-0/-home-user-hyper-research-works/aa6e0fd0-b155-51a6-ad4a-ebbe528f3807/scratchpad/l2_audit.json','w'), indent=1)

main()
