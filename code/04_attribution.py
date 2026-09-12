#!/usr/bin/env python3
"""E5: controlled TTP-attribution experiment that isolates ontology drift.

Threat model of the experiment
------------------------------
A CTI artefact (incident report, dataset label set) is written in the ATT&CK
vocabulary of release V. It is later consumed by an analytic platform whose
knowledge base is at release W > V. Nothing about the adversary changed; only
the vocabulary did.

To hold intelligence content constant we take every group profile from the
*same* release W and back-project it into V's vocabulary, i.e. reconstruct the
identifiers a V-era analyst would have written for the same behaviours
(pre-revocation identifiers; parent techniques where the sub-technique did not
yet exist; behaviours with no V-era ancestor are dropped, as they were then
unknown).

Four conditions, identical candidate-group universe (groups present in both V
and W), identical observations:

  contemporaneous  V-vocabulary observation vs. V-vocabulary profiles
                   (a self-consistent V-era system: no drift)
  naive            V-vocabulary observation vs. W-vocabulary profiles
                   (current practice: legacy artefact, modern knowledge base)
  normalized       ATT&CK-Norm applied to the observation, then vs. W profiles
  oracle           W-vocabulary observation vs. W profiles (modern upper bound)

Decomposition
  oracle - contemporaneous : information loss inherent in the older ontology
  contemporaneous - naive  : the pure cross-version drift penalty
  (normalized - naive) / (contemporaneous - naive) : drift penalty recovered

A secondary "historical" condition samples from the *actual* V-era profile
(real archival labels) and reflects the combined effect of drift and genuine
intelligence change.

Per-row significance. Each contrast is also given an exact two-sided p-value
from a paired sign test (McNemar's exact form): among trials where exactly one
of the two conditions hit top-1, the number favouring the first condition is
binomial(n_discordant, 1/2) under the null. It uses no random numbers, so the
bootstrap and trial RNG streams are untouched; 37_statistics.py applies the
Holm and Benjamini-Hochberg corrections across all rows.
"""
from __future__ import annotations

import json
import math
import random
import statistics
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import attackdrift as ad  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "data" / "results"
DOMAIN = "enterprise-attack"
K_VALUES = [5, 10, 20]
N_TRIALS = 500
N_BOOT = 2000
SEED = 20260912
CONDITIONS = ("contemporaneous", "naive", "normalized", "oracle", "historical")


def build_backmap(v: ad.Snapshot, w: ad.Snapshot) -> dict[str, str | None]:
    """W-era technique id -> identifier a V-era analyst would have written."""
    v_live = v.live_tech()
    rev_w, sub_w = w.revoked_by(), w.sub_of()
    resolves_to: dict[str, list[str]] = defaultdict(list)
    for old in v_live:
        tgt = ad.resolve_chain(old, rev_w)
        if tgt != old:
            resolves_to[tgt].append(old)
    back: dict[str, str | None] = {}
    for t in w.live_tech():
        if t in v_live:
            back[t] = t
        elif resolves_to.get(t):
            back[t] = sorted(resolves_to[t])[0]
        else:
            cur, found = t, None
            for _ in range(5):
                parent = sub_w.get(cur)
                if not parent:
                    break
                if parent in v_live:
                    found = parent
                    break
                cur = parent
            back[t] = found
    return back


def idf_weights(profiles: dict[str, set[str]]) -> dict[str, float]:
    n = len(profiles)
    df: dict[str, int] = defaultdict(int)
    for ts in profiles.values():
        for t in ts:
            df[t] += 1
    return {t: math.log((n + 1) / (c + 0.5)) for t, c in df.items()}


def rank_of(truth: str, obs: set[str], profiles: dict[str, set[str]],
            w: dict[str, float], order: list[str]) -> int:
    """1-based rank of the true group; ties broken by a fixed group ordering."""
    obs_norm = math.sqrt(sum(w.get(t, 0.0) for t in obs)) or 1.0
    scored = []
    for g in order:
        prof = profiles[g]
        inter = obs & prof
        if inter:
            num = sum(w.get(t, 0.0) for t in inter)
            denom = obs_norm * (math.sqrt(sum(w.get(t, 0.0) for t in prof)) or 1.0)
            scored.append((num / denom, g))
        else:
            scored.append((0.0, g))
    scored.sort(key=lambda x: (-x[0], x[1]))
    for i, (_, g) in enumerate(scored, 1):
        if g == truth:
            return i
    return len(order) + 1


def paired_bootstrap(a: list[float], b: list[float], rng: random.Random) -> tuple[float, float]:
    """95% CI for mean(a) - mean(b) over paired trials."""
    n = len(a)
    diffs = [x - y for x, y in zip(a, b)]
    means = []
    for _ in range(N_BOOT):
        means.append(statistics.fmean(diffs[rng.randrange(n)] for _ in range(n)))
    means.sort()
    return means[int(0.025 * N_BOOT)], means[int(0.975 * N_BOOT)]


def sign_test(a: list[float], b: list[float]) -> tuple[float, int, int]:
    """Exact two-sided paired sign test on per-trial differences a - b.

    Returns (p, n_plus, n_minus): trials where a hit and b missed, and the
    reverse. Ties carry no information and are discarded. Deterministic.
    """
    n_plus = sum(1 for x, y in zip(a, b) if x > y)
    n_minus = sum(1 for x, y in zip(a, b) if x < y)
    n = n_plus + n_minus
    if n == 0:
        return 1.0, n_plus, n_minus
    tail = sum(math.comb(n, i) for i in range(min(n_plus, n_minus) + 1)) / 2 ** n
    return min(1.0, 2 * tail), n_plus, n_minus


def evaluate(v: ad.Snapshot, w: ad.Snapshot, k: int, rng: random.Random) -> dict:
    pw_all = w.group_techniques(include_software=True)
    pv_all = v.group_techniques(include_software=True)
    back = build_backmap(v, w)

    # candidate universe: groups present in BOTH releases with enough techniques
    universe = [g for g in sorted(set(pw_all) & set(pv_all))
                if len(pw_all[g]) >= k and len(pv_all[g]) >= 2]
    if len(universe) < 10:
        return {}
    prof_w = {g: pw_all[g] for g in universe}
    prof_v = {g: {back[t] for t in pw_all[g] if back.get(t)} for g in universe}
    prof_hist = {g: pv_all[g] for g in universe}
    idf_w, idf_v = idf_weights(prof_w), idf_weights(prof_v)
    idf_hist = idf_weights(prof_hist)

    hits = {c: [] for c in CONDITIONS}
    top5 = {c: [] for c in CONDITIONS}
    rr = {c: [] for c in CONDITIONS}
    oov_tokens = unresolved = tok_total = 0
    trials = 0
    for _ in range(N_TRIALS):
        g = rng.choice(universe)
        obs_w = set(rng.sample(sorted(prof_w[g]), k))
        obs_v = {back[t] for t in obs_w if back.get(t)}
        if len(obs_v) < 2:
            continue
        hist_pool = sorted(prof_hist[g])
        obs_hist = set(rng.sample(hist_pool, min(k, len(hist_pool))))
        trials += 1
        tok_total += len(obs_v)
        live_w = w.live_tech()
        oov_tokens += sum(1 for t in obs_v if t not in live_w)
        unresolved += sum(1 for t in obs_v
                          if ad.resolve_chain(t, w.revoked_by()) not in live_w)
        runs = {
            "contemporaneous": (obs_v, prof_v, idf_v),
            "naive": (obs_v, prof_w, idf_w),
            "normalized": (ad.normalize(obs_v, w), prof_w, idf_w),
            "oracle": (obs_w, prof_w, idf_w),
            "historical": (obs_hist, prof_w, idf_w),
        }
        for cond, (obs, profs, weights) in runs.items():
            r = rank_of(g, obs, profs, weights, universe)
            hits[cond].append(1.0 if r == 1 else 0.0)
            top5[cond].append(1.0 if r <= 5 else 0.0)
            rr[cond].append(1.0 / r)
    if not trials:
        return {}

    out = {"k": k, "trials": trials, "n_groups": len(universe),
           "oov_rate": oov_tokens / tok_total if tok_total else 0.0,
           "unresolvable_rate": unresolved / tok_total if tok_total else 0.0}
    for c in CONDITIONS:
        out[f"{c}_top1"] = statistics.fmean(hits[c])
        out[f"{c}_top5"] = statistics.fmean(top5[c])
        out[f"{c}_mrr"] = statistics.fmean(rr[c])
    boot = random.Random(SEED + 7)
    lo, hi = paired_bootstrap(hits["contemporaneous"], hits["naive"], boot)
    out["drift_penalty_top1"] = out["contemporaneous_top1"] - out["naive_top1"]
    out["drift_penalty_ci"] = [lo, hi]
    lo2, hi2 = paired_bootstrap(hits["normalized"], hits["naive"], boot)
    out["norm_gain_top1"] = out["normalized_top1"] - out["naive_top1"]
    out["norm_gain_ci"] = [lo2, hi2]
    out["granularity_loss_top1"] = out["oracle_top1"] - out["contemporaneous_top1"]
    d = out["drift_penalty_top1"]
    out["recovery_top1"] = (out["norm_gain_top1"] / d) if d > 1e-9 else None
    # exact sign-test p-values (appended after the bootstrap so the RNG order is unchanged)
    p, np_, nm = sign_test(hits["contemporaneous"], hits["naive"])
    out["drift_penalty_p_sign"] = p
    out["drift_penalty_discordant"] = [np_, nm]
    p, np_, nm = sign_test(hits["normalized"], hits["naive"])
    out["norm_gain_p_sign"] = p
    out["norm_gain_discordant"] = [np_, nm]
    return out


def main() -> None:
    con = ad.connect()
    majors = ad.major_releases(con, DOMAIN)
    w_rel = majors[-1]
    w = ad.load_snapshot(con, DOMAIN, w_rel.version)
    rows = []
    for v_rel in majors[:-1]:
        v = ad.load_snapshot(con, DOMAIN, v_rel.version)
        for k in K_VALUES:
            rng = random.Random(SEED + k)
            r = evaluate(v, w, k, rng)
            if r:
                r.update({"v": v_rel.version, "v_date": v_rel.date,
                          "w": w_rel.version, "w_date": w_rel.date})
                rows.append(r)
        print(f"  v{v_rel.version} done", file=sys.stderr)
    (OUT / "e5_attribution.json").write_text(json.dumps(rows, indent=1))
    print(f"wrote {OUT/'e5_attribution.json'} ({len(rows)} rows)", file=sys.stderr)


if __name__ == "__main__":
    main()
