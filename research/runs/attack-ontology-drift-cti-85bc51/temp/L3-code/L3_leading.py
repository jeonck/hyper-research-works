#!/usr/bin/env python3
"""L3-C2: is there a leading indicator of a restructuring/revocation burst?

(a) release-level: features at transition k vs. burst size at transition k+1
(b) technique-level hazard: do techniques that are about to be revoked show
    elevated edit activity in the release BEFORE the revocation?
"""
import sys, json, statistics as st
sys.path.insert(0,'/home/user/hyper-research-works/code')
import attackdrift as ad

def tset(o): return set(filter(None,(o["tactics"] or "").split(",")))
def spearman(x,y):
    n=len(x)
    def rk(v):
        s=sorted(range(n),key=lambda i:v[i]); r=[0.0]*n; i=0
        while i<n:
            j=i
            while j+1<n and v[s[j+1]]==v[s[i]]: j+=1
            avg=(i+j)/2+1
            for k in range(i,j+1): r[s[k]]=avg
            i=j+1
        return r
    rx,ry=rk(x),rk(y)
    mx,my=sum(rx)/n,sum(ry)/n
    num=sum((a-mx)*(b-my) for a,b in zip(rx,ry))
    den=(sum((a-mx)**2 for a in rx)*sum((b-my)**2 for b in ry))**.5
    return num/den if den else float('nan')

con=ad.connect()
DOM="enterprise-attack"
majors=ad.major_releases(con,DOM)
snaps={m.version:ad.load_snapshot(con,DOM,m.version) for m in majors}

# ---- (a) release-level features ----
feat=[]
for prev,cur in zip(majors,majors[1:]):
    a,b=snaps[prev.version],snaps[cur.version]
    la,lb=a.live_tech(),b.live_tech()
    surv=la&lb
    desc=sum(1 for t in surv if a.tech[t]["desc_sha"]!=b.tech[t]["desc_sha"])
    det =sum(1 for t in surv if a.tech[t]["det_sha"]!=b.tech[t]["det_sha"])
    tac =sum(1 for t in surv if tset(a.tech[t])!=tset(b.tech[t]))
    ren =sum(1 for t in surv if a.tech[t]["name"]!=b.tech[t]["name"])
    vbump=sum(1 for t in surv if (a.tech[t]["obj_version"] or "")!=(b.tech[t]["obj_version"] or ""))
    vmajor=0
    for t in surv:
        try:
            if int(float(a.tech[t]["obj_version"] or 0))<int(float(b.tech[t]["obj_version"] or 0)): vmajor+=1
        except Exception: pass
    kill=len({t for t in la if t in b.tech and (b.tech[t]["revoked"] or b.tech[t]["deprecated"])})+len(la-set(b.tech))
    feat.append({"to":cur.version,"n":len(surv),
                 "desc_f":desc/len(surv),"det_f":det/len(surv),"tac_f":tac/len(surv),
                 "ren_f":ren/len(surv),"vbump_f":vbump/len(surv),"vmajor_f":vmajor/len(surv),
                 "kill":kill,"kill_f":kill/len(la)})
print("release-level features (enterprise), kill = revoked+deprecated+vanished at that transition")
print(f"{'to':>5} {'desc_f':>7} {'det_f':>7} {'tac_f':>7} {'ren_f':>7} {'vbump_f':>8} {'vmaj_f':>7} {'kill':>5} {'kill_f':>7}")
for f in feat:
    print(f"{f['to']:>5} {f['desc_f']:7.3f} {f['det_f']:7.3f} {f['tac_f']:7.3f} {f['ren_f']:7.3f} {f['vbump_f']:8.3f} {f['vmajor_f']:7.3f} {f['kill']:5d} {f['kill_f']:7.3f}")

print("\nSpearman rho, feature at transition k  vs  kill_f at transition k+1  (n=%d)"%(len(feat)-1))
for k in ["desc_f","det_f","tac_f","ren_f","vbump_f","vmajor_f","kill_f"]:
    x=[f[k] for f in feat[:-1]]; y=[f["kill_f"] for f in feat[1:]]
    print(f"  lead-1 {k:>9}: rho={spearman(x,y):+.3f}")
print("same-transition (contemporaneous) control:")
for k in ["desc_f","tac_f","ren_f"]:
    print(f"  lag-0  {k:>9}: rho={spearman([f[k] for f in feat],[f['kill_f'] for f in feat]):+.3f}")

# ---- (b) technique-level hazard, v19.0 and v7.0 waves ----
def hazard(prev2,prev1,cur):
    """edit activity between prev2->prev1 for techniques killed at prev1->cur"""
    a,b,c=snaps[prev2],snaps[prev1],snaps[cur]
    surv=a.live_tech()&b.live_tech()
    killed={t for t in b.live_tech() if t in c.tech and (c.tech[t]["revoked"] or c.tech[t]["deprecated"])}
    killed|= (b.live_tech()-set(c.tech))
    doomed=surv&killed; safe=surv-killed
    def rate(S,f): return sum(1 for t in S if f(t))/len(S) if S else float('nan')
    for lbl,f in [("desc edited",lambda t:a.tech[t]["desc_sha"]!=b.tech[t]["desc_sha"]),
                  ("tactic changed",lambda t:tset(a.tech[t])!=tset(b.tech[t])),
                  ("renamed",lambda t:a.tech[t]["name"]!=b.tech[t]["name"]),
                  ("version bumped",lambda t:(a.tech[t]["obj_version"] or "")!=(b.tech[t]["obj_version"] or ""))]:
        print(f"   {lbl:>16}: doomed {rate(doomed,f):.3f} (n={len(doomed)})  vs  survivors {rate(safe,f):.3f} (n={len(safe)})")

print("\n(b) prior-release edit activity of techniques killed in the NEXT release")
print(" v19.0 wave -- edits during 17.0->18.0:"); hazard("17.0","18.0","19.0")
print(" v7.0 wave  -- edits during 5.0->6.0:");  hazard("5.0","6.0","7.0")
print(" control (no wave) v15.0 -- edits during 13.0->14.0:"); hazard("13.0","14.0","15.0")
