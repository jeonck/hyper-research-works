#!/usr/bin/env python3
"""(a) paired-bootstrap CIs on the specificity-stratified drift penalty;
   (b) the missing control: the V-era system evaluated against itself."""
import json, random, statistics, sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0,'/home/user/hyper-research-works/code')
import attackdrift as ad
from importlib import import_module
attr=import_module("04_attribution")
DOMAIN="enterprise-attack"; SEED=20260912; K=10; N=1500; NB=2000

def boot(d,rng):
    n=len(d); ms=[]
    for _ in range(NB):
        ms.append(statistics.fmean(d[rng.randrange(n)] for _ in range(n)))
    ms.sort(); return ms[int(.025*NB)], ms[int(.975*NB)]

def spec_set(prof):
    df=defaultdict(int)
    for ts in prof.values():
        for t in ts: df[t]+=1
    return {g for g,ts in prof.items() if any(df[t]==1 for t in ts)}

def main():
    con=ad.connect(); w=ad.load_snapshot(con,DOMAIN,"19.0")
    pw=w.group_techniques(include_software=True)
    for vv in ["12.0","16.0","18.0"]:
        v=ad.load_snapshot(con,DOMAIN,vv); back=attr.build_backmap(v,w)
        pv=v.group_techniques(include_software=True)
        uni=[g for g in sorted(set(pw)&set(pv)) if len(pw[g])>=K and len(pv[g])>=2]
        prof_w={g:pw[g] for g in uni}
        prof_v={g:{back[t] for t in pw[g] if back.get(t)} for g in uni}
        sp=spec_set(prof_w)
        iw,iv=attr.idf_weights(prof_w),attr.idf_weights(prof_v)
        rng=random.Random(SEED); pairs=defaultdict(list)
        for _ in range(N):
            g=rng.choice(uni)
            ow=set(rng.sample(sorted(prof_w[g]),K))
            ov={back[t] for t in ow if back.get(t)}
            if len(ov)<2: continue
            c=1.0 if attr.rank_of(g,ov,prof_v,iv,uni)==1 else 0.0
            nv=1.0 if attr.rank_of(g,ov,prof_w,iw,uni)==1 else 0.0
            pairs["spec" if g in sp else "nonspec"].append(c-nv); pairs["all"].append(c-nv)
        br=random.Random(SEED+1)
        line=f"v{vv} (n_groups={len(uni)}, specific={len(sp)}/{len(uni)}={len(sp)/len(uni):.3f}) "
        for s in ("all","spec","nonspec"):
            d=pairs[s]; lo,hi=boot(d,br)
            line+=f"| {s}: drift={statistics.fmean(d):+.4f} CI[{lo:+.4f},{hi:+.4f}] n={len(d)} "
        print(line, flush=True)

    # ---- missing control: V-era system judged against itself ----
    print("\n--- V-era self-consistent system (real archival labels AND archival profiles) ---")
    for vv in ["1.0","6.0","7.0","12.0","18.0"]:
        v=ad.load_snapshot(con,DOMAIN,vv); back=attr.build_backmap(v,w)
        pv=v.group_techniques(include_software=True)
        uni=[g for g in sorted(set(pw)&set(pv)) if len(pw[g])>=K and len(pv[g])>=2]
        prof_w={g:pw[g] for g in uni}
        prof_v={g:{back[t] for t in pw[g] if back.get(t)} for g in uni}
        prof_h={g:pv[g] for g in uni}
        iw=attr.idf_weights(prof_w); iv=attr.idf_weights(prof_v); ih=attr.idf_weights(prof_h)
        rng=random.Random(SEED); r=defaultdict(list)
        for _ in range(N):
            g=rng.choice(uni)
            ow=set(rng.sample(sorted(prof_w[g]),K))
            ov={back[t] for t in ow if back.get(t)}
            if len(ov)<2: continue
            hp=sorted(prof_h[g]); oh=set(rng.sample(hp,min(K,len(hp))))
            r["contemporaneous_backproj"].append(1.0 if attr.rank_of(g,ov,prof_v,iv,uni)==1 else 0.0)
            r["V_era_self"].append(1.0 if attr.rank_of(g,oh,prof_h,ih,uni)==1 else 0.0)
            r["historical_vs_W"].append(1.0 if attr.rank_of(g,oh,prof_w,iw,uni)==1 else 0.0)
            r["obs_size_v"].append(len(ov)); r["obs_size_h"].append(len(oh))
        print(f"v{vv}: back-proj contemporaneous={statistics.fmean(r['contemporaneous_backproj']):.3f}  "
              f"REAL V-era self-consistent={statistics.fmean(r['V_era_self']):.3f}  "
              f"historical->W={statistics.fmean(r['historical_vs_W']):.3f}  "
              f"|obs_v|={statistics.fmean(r['obs_size_v']):.2f} |obs_hist|={statistics.fmean(r['obs_size_h']):.2f}",
              flush=True)
main()
