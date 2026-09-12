#!/usr/bin/env python3
"""E20: validation of the semantic-drift instrument (token Jaccard, J < 0.8).

Four parts, all over Enterprise ATT&CK:

  V1 threshold sensitivity   the substantial-rewrite share per source cohort at
                             v19.0 (Table 4) and per consecutive major transition,
                             at thresholds 0.5 .. 0.95; the time-to-10% substantive
                             staleness clock of E12 recomputed at every threshold
  V2 convergent validity     J < 0.8 against signals it did not use: MITRE's own
                             major x_mitre_version increment, tactic / platform /
                             name changes, and four alternative text similarities
  V3 annotation instrument   a seeded, Jaccard-stratified sample of 150 edited
                             description pairs for double human annotation
                             (paper/annotation/), with the key kept separate
  V4 pilot scoring           if paper/annotation/pilot_annotator_{1,2}.csv exist,
                             inter-annotator kappa and the concordance of
                             "substantive" (level >= 2) with J < 0.8

The pilot annotators shipped with the package are language models, not humans;
V4 is a dry run of the instrument, not the validation study it is built for.
"""
from __future__ import annotations

import csv
import difflib
import json
import random
import re
import statistics
import sys
from datetime import date
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import cohen_kappa_score, roc_auc_score

sys.path.insert(0, str(Path(__file__).resolve().parent))
import attackdrift as ad  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "results"
TABLES = ROOT / "paper" / "tables"
ANNOT = ROOT / "paper" / "annotation"
DOMAIN = "enterprise-attack"
SEED = 20260912
THRESHOLDS = [0.5, 0.6, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
PAPER_T = 0.8
CLOCK_COHORTS = range(7, 19)          # v7.0 .. v18.0, the paper's 0.50-2.01 range
BINS = [("J>=0.95", 0.95, 1.01), ("0.80-0.95", 0.80, 0.95), ("0.60-0.80", 0.60, 0.80),
        ("0.40-0.60", 0.40, 0.60), ("J<0.40", -1.0, 0.40)]
PER_BIN = 30
# items quoted as worked examples in codebook.md; flagged in the key so the
# human study can exclude them from kappa
CODEBOOK_EXAMPLES = {"A075", "A039", "A085", "A090", "A071", "A046", "A045", "A031"}
WORD = re.compile(r"[a-z0-9]+")
SENT = re.compile(r"(?<=[.!?])\s+")


def tokens(text: str | None) -> set[str]:
    return set(WORD.findall((text or "").lower()))


def parse(s: str | None) -> date:
    y, m, d = (s or "1970-01-01")[:10].split("-")
    return date(int(y), int(m), int(d))


def split_field(s: str | None) -> set[str]:
    return set(filter(None, (s or "").split(",")))


def major_of(v: str | None) -> int:
    try:
        return int((v or "0").split(".")[0])
    except ValueError:
        return 0


def as_tuple(v: str | None) -> tuple:
    try:
        return tuple(int(x) for x in (v or "0").split("."))
    except ValueError:
        return (0,)


def bin_of(j: float) -> str:
    return next(name for name, lo, hi in BINS if lo <= j < hi)


# ---------------------------------------------------------------- alt metrics
def char3(text: str) -> set[str]:
    t = re.sub(r"\s+", " ", (text or "").lower()).strip()
    return {t[i:i + 3] for i in range(len(t) - 2)}


def sentences(text: str) -> set[str]:
    return {s.strip().lower() for s in SENT.split(text or "") if s.strip()}


def desc(snap, t: str) -> str:
    return snap.by_stix[snap.tech[t]["stix_id"]].get("description") or ""


# ------------------------------------------------------------------ V1 + data
def consecutive_pairs(snaps, majors) -> list[dict]:
    rows = []
    for prev, cur in zip(majors, majors[1:]):
        a, b = snaps[prev.version], snaps[cur.version]
        for t in sorted(a.live_tech() & b.live_tech()):
            oa, ob = a.tech[t], b.tech[t]
            da, db = desc(a, t), desc(b, t)
            rows.append({
                "attack_id": t, "release_a": prev.version, "release_b": cur.version,
                "name_a": oa["name"], "name_b": ob["name"],
                "description_a": da, "description_b": db,
                "edited": oa["desc_sha"] != ob["desc_sha"],
                "jaccard": ad.jaccard(tokens(da), tokens(db)),
                "version_a": oa["obj_version"], "version_b": ob["obj_version"],
                "major_bump": major_of(ob["obj_version"]) > major_of(oa["obj_version"]),
                "any_bump": as_tuple(ob["obj_version"]) > as_tuple(oa["obj_version"]),
                "tactic_changed": split_field(oa["tactics"]) != split_field(ob["tactics"]),
                "platform_changed": split_field(oa["platforms"]) != split_field(ob["platforms"]),
                "name_changed": oa["name"] != ob["name"],
            })
    for r in rows:
        r["structured_changed"] = r["tactic_changed"] or r["platform_changed"] or r["name_changed"]
        if not r["edited"]:
            r["seqmatch"] = r["char3_jaccard"] = r["sentence_jaccard"] = 1.0
        else:
            da, db = r["description_a"], r["description_b"]
            r["seqmatch"] = difflib.SequenceMatcher(None, da, db).ratio()
            r["char3_jaccard"] = ad.jaccard(char3(da), char3(db))
            r["sentence_jaccard"] = ad.jaccard(sentences(da), sentences(db))
    texts = sorted({r["description_a"] for r in rows} | {r["description_b"] for r in rows})
    X = TfidfVectorizer(token_pattern=WORD.pattern, lowercase=True).fit_transform(texts)
    idx = {t: i for i, t in enumerate(texts)}
    for r in rows:   # rows are L2-normalised, so the dot product is the cosine
        r["tfidf_cosine"] = (1.0 if not r["edited"] else
                             float(X[idx[r["description_a"]]].multiply(
                                 X[idx[r["description_b"]]]).sum()))
    return rows


def cohort_shares(snaps, majors, final) -> list[dict]:
    b = snaps[final.version]
    live_b = b.live_tech()
    out = []
    for src in majors:
        if src.version == final.version:
            continue
        a = snaps[src.version]
        sims = sorted(ad.jaccard(tokens(desc(a, t)), tokens(desc(b, t)))
                      for t in sorted(a.live_tech() & live_b))
        out.append({"src": src.version, "n": len(sims),
                    "mean_jaccard": statistics.fmean(sims),
                    "share_below": {str(th): sum(s < th for s in sims) / len(sims)
                                    for th in THRESHOLDS}})
    return out


def transition_shares(pairs) -> list[dict]:
    out = []
    for (fa, fb) in sorted({(r["release_a"], r["release_b"]) for r in pairs},
                           key=lambda x: major_of(x[0])):
        js = [r["jaccard"] for r in pairs if r["release_a"] == fa]
        out.append({"from": fa, "to": fb, "n": len(js),
                    "share_below": {str(th): sum(j < th for j in js) / len(js)
                                    for th in THRESHOLDS}})
    return out


def boilerplate_confound(pairs) -> dict:
    """Up to v2.0 the description embedded Detection / Platforms / Data Sources
    boilerplate that v3.0 moved into structured fields. Removing it is not a
    change of meaning, but it is a large token change. Sized here so the low
    cohorts of Table 4 can be read correctly."""
    tag = re.compile(r"(Detection:|Platforms:|Data Sources:)")
    out = {}
    for tr in sorted({(r["release_a"], r["release_b"]) for r in pairs}, key=lambda x: major_of(x[0])):
        rows = [r for r in pairs if r["release_a"] == tr[0] and r["edited"]]
        hit = [r for r in rows if tag.search(r["description_a"]) and not tag.search(r["description_b"])]
        if hit:
            low = [r for r in rows if r["jaccard"] < PAPER_T]
            out[f"{tr[0]}->{tr[1]}"] = {
                "edited": len(rows), "boilerplate_removed": len(hit),
                "j_below_0.8": len(low),
                "j_below_0.8_with_boilerplate_removed": sum(r["jaccard"] < PAPER_T for r in hit),
                "mean_j_boilerplate_removed": statistics.fmean(r["jaccard"] for r in hit)}
    return out


def staleness_clock(con, all_snaps, rels, majors) -> dict:
    """E12's substantive clock (hard, or J < th, or tactic moved) and a J-only
    variant, at every threshold. Curves are evaluated against every later
    release including patches, exactly as 19_temporal_structure.staleness does."""
    per_cohort = {}
    for src in majors:
        a = all_snaps[src.version]
        base = a.live_tech()
        curve = []
        for tgt in rels:
            if tgt.ordinal <= src.ordinal:
                continue
            b = all_snaps[tgt.version]
            live = b.live_tech()
            hard = {x for x in base if x not in live}
            js, moved = {}, set()
            for x in base - hard:
                if split_field(a.tech[x]["tactics"]) != split_field(b.tech[x]["tactics"]):
                    moved.add(x)
                js[x] = ad.jaccard(tokens(desc(a, x)), tokens(desc(b, x)))
            row = {"years": (parse(tgt.date) - parse(src.date)).days / 365.25}
            for th in THRESHOLDS:
                low = {x for x, j in js.items() if j < th}
                row[f"sub_{th}"] = len(hard | moved | low) / len(base)
                row[f"jonly_{th}"] = len(low) / len(base)
            curve.append(row)
        rec = {}
        for th in THRESHOLDS:
            for defn in ("sub", "jonly"):
                hit = next((c for c in curve if c[f"{defn}_{th}"] >= 0.10), None)
                rec[f"t10_{defn}_{th}"] = round(hit["years"], 2) if hit else None
        per_cohort[src.version] = rec
    summary = {}
    for th in THRESHOLDS:
        for defn in ("sub", "jonly"):
            vals = [per_cohort[f"{m}.0"][f"t10_{defn}_{th}"] for m in CLOCK_COHORTS]
            got = [v for v in vals if v is not None]
            summary[f"{defn}_{th}"] = {
                "min": min(got) if got else None,
                "median": round(statistics.median(got), 2) if got else None,
                "max": max(got) if got else None,
                "censored": vals.count(None), "n_cohorts": len(vals)}
    return {"per_cohort": per_cohort, "summary_v7_to_v18": summary}


# ------------------------------------------------------------------------ V2
def binary_concordance(pred: list[bool], ref: list[bool]) -> dict:
    p, r = np.asarray(pred, bool), np.asarray(ref, bool)
    tp, fp, fn = int((p & r).sum()), int((p & ~r).sum()), int((~p & r).sum())
    return {"n": len(p), "ref_positive": int(r.sum()), "pred_positive": int(p.sum()),
            "agreement": float((p == r).mean()),
            "kappa": float(cohen_kappa_score(p, r)) if len(set(r)) > 1 and len(set(p)) > 1 else None,
            "precision": tp / (tp + fp) if tp + fp else None,
            "recall": tp / (tp + fn) if tp + fn else None}


def auc(score: list[float], ref: list[bool]) -> float | None:
    return float(roc_auc_score(ref, score)) if len(set(ref)) > 1 else None


def youden(j: list[float], ref: list[bool]) -> dict:
    """The J threshold t (rule: substantive iff J < t) maximising TPR - FPR."""
    j, r = np.asarray(j), np.asarray(ref, bool)
    best = None
    for t in sorted(set(j.tolist()) | {1.01}):
        pred = j < t
        tpr = (pred & r).sum() / r.sum() if r.sum() else 0.0
        fpr = (pred & ~r).sum() / (~r).sum() if (~r).sum() else 0.0
        if best is None or tpr - fpr > best["youden"] + 1e-12:
            best = {"threshold": float(t), "youden": float(tpr - fpr),
                    "tpr": float(tpr), "fpr": float(fpr)}
    return best


def convergent_validity(pairs) -> dict:
    metrics = ["jaccard", "seqmatch", "char3_jaccard", "sentence_jaccard", "tfidf_cosine"]
    signals = ["major_bump", "any_bump", "tactic_changed", "platform_changed",
               "name_changed", "structured_changed"]
    out = {}
    for pop, rows in (("all_pairs", pairs), ("edited_pairs", [r for r in pairs if r["edited"]])):
        low = [r["jaccard"] < PAPER_T for r in rows]
        block = {"n": len(rows), "j_below_0.8": sum(low),
                 "signal_rates": {s: sum(r[s] for r in rows) / len(rows) for s in signals},
                 "concordance_j_lt_0.8": {}, "auc_for_major_bump": {},
                 "auc_for_structured_change": {}, "spearman_vs_jaccard": {},
                 "youden_threshold": {}}
        for s in signals:
            ref = [r[s] for r in rows]
            block["concordance_j_lt_0.8"][s] = binary_concordance(low, ref)
            block["youden_threshold"][s] = youden([r["jaccard"] for r in rows], ref)
        for m in metrics:
            dist = [1 - r[m] for r in rows]
            block["auc_for_major_bump"][m] = auc(dist, [r["major_bump"] for r in rows])
            block["auc_for_structured_change"][m] = auc(dist, [r["structured_changed"] for r in rows])
            if m != "jaccard":
                rho = spearmanr([r["jaccard"] for r in rows], [r[m] for r in rows])
                block["spearman_vs_jaccard"][m] = float(rho.statistic)
        out[pop] = block
    return out


# ------------------------------------------------------------------------ V3
def draw_sample(pairs) -> list[dict]:
    rng = random.Random(SEED)
    frame = [r for r in pairs if r["edited"]]
    chosen = []
    for name, lo, hi in BINS:
        cand = [r for r in frame if lo <= r["jaccard"] < hi]
        chosen += rng.sample(cand, PER_BIN)
    rng.shuffle(chosen)
    for i, r in enumerate(chosen, 1):
        r["item_id"] = f"A{i:03d}"
    return chosen


def write_sample(sample, pairs) -> dict:
    ANNOT.mkdir(parents=True, exist_ok=True)
    blind = ["item_id", "attack_id", "release_a", "release_b", "name_a", "name_b",
             "description_a", "description_b"]
    with (ANNOT / "sample_150.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=blind, extrasaction="ignore")
        w.writeheader()
        w.writerows(sample)
    keyf = ["item_id", "attack_id", "release_a", "release_b", "bin", "jaccard",
            "seqmatch", "char3_jaccard", "sentence_jaccard", "tfidf_cosine",
            "version_a", "version_b", "major_bump", "any_bump", "tactic_changed",
            "platform_changed", "name_changed", "codebook_example"]
    with (ANNOT / "sample_150_key.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keyf, extrasaction="ignore")
        w.writeheader()
        for r in sample:
            w.writerow({**r, "bin": bin_of(r["jaccard"]),
                        "codebook_example": r["item_id"] in CODEBOOK_EXAMPLES})
    frame = [r for r in pairs if r["edited"]]
    return {"n": len(sample), "per_bin": PER_BIN, "seed": SEED,
            "frame_edited_pairs": len(frame),
            "frame_per_bin": {name: sum(lo <= r["jaccard"] < hi for r in frame)
                              for name, lo, hi in BINS},
            "codebook_examples": sorted(CODEBOOK_EXAMPLES)}


# ------------------------------------------------------------------------ V4
def read_pilot(path: Path) -> dict[str, int]:
    with path.open() as f:
        return {row["item_id"]: int(row["level"]) for row in csv.DictReader(f)}


def concordance_block(items, sample_by_id, frame_weights) -> dict:
    """items: list of (item_id, substantive_bool)."""
    ids = [i for i, _ in items]
    ref = [s for _, s in items]
    j = [sample_by_id[i]["jaccard"] for i in ids]
    low = [x < PAPER_T for x in j]
    blk = binary_concordance(low, ref)
    blk["auc_1_minus_j"] = auc([1 - x for x in j], ref)
    blk["youden"] = youden(j, ref)
    # re-weight each item by (frame pairs in its bin) / (sampled pairs in its bin)
    # so precision / recall refer to the edited-pair population, not the
    # stratified sample
    w = np.array([frame_weights[bin_of(sample_by_id[i]["jaccard"])] for i in ids])
    p, r = np.array(low), np.array(ref)
    tp, fp, fn = w[p & r].sum(), w[p & ~r].sum(), w[~p & r].sum()
    blk["population_weighted"] = {"precision": float(tp / (tp + fp)) if tp + fp else None,
                                  "recall": float(tp / (tp + fn)) if tp + fn else None,
                                  "substantive_rate": float(w[r].sum() / w.sum())}
    blk["rate_ge2_by_bin"] = {name: (statistics.fmean(s for i, s in items
                                                       if bin_of(sample_by_id[i]["jaccard"]) == name)
                                     if any(bin_of(sample_by_id[i]["jaccard"]) == name for i, _ in items)
                                     else None) for name, _, _ in BINS}
    return blk


def pilot(sample, sample_meta) -> dict | None:
    files = [ANNOT / f"pilot_annotator_{k}.csv" for k in (1, 2)]
    if not all(f.exists() for f in files):
        return None
    a1, a2 = (read_pilot(f) for f in files)
    ids = [r["item_id"] for r in sample]
    missing = [i for i in ids if i not in a1 or i not in a2]
    ids = [i for i in ids if i in a1 and i in a2]
    by_id = {r["item_id"]: r for r in sample}
    fw = {name: sample_meta["frame_per_bin"][name] / PER_BIN for name, _, _ in BINS}
    l1, l2 = [a1[i] for i in ids], [a2[i] for i in ids]
    b1, b2 = [x >= 2 for x in l1], [x >= 2 for x in l2]
    conf = [[sum(1 for x, y in zip(l1, l2) if x == i and y == k) for k in range(4)]
            for i in range(4)]
    out = {
        "note": "pilot annotators are language models (annotator 1: sonnet, "
                "annotator 2: opus); this is a dry run of the instrument, not the "
                "human study",
        "n_scored": len(ids), "missing_items": missing,
        "level_distribution": {"annotator_1": [l1.count(k) for k in range(4)],
                               "annotator_2": [l2.count(k) for k in range(4)]},
        "confusion_rows_a1_cols_a2": conf,
        "kappa_4_level": {
            "unweighted": float(cohen_kappa_score(l1, l2)),
            "linear": float(cohen_kappa_score(l1, l2, weights="linear")),
            "quadratic": float(cohen_kappa_score(l1, l2, weights="quadratic")),
            "exact_agreement": sum(x == y for x, y in zip(l1, l2)) / len(ids),
            "within_one_level": sum(abs(x - y) <= 1 for x, y in zip(l1, l2)) / len(ids)},
        "kappa_binary_ge2": {"unweighted": float(cohen_kappa_score(b1, b2)),
                             "agreement": sum(x == y for x, y in zip(b1, b2)) / len(ids)},
        "concordance_with_j_lt_0.8": {
            "annotator_1": concordance_block(list(zip(ids, b1)), by_id, fw),
            "annotator_2": concordance_block(list(zip(ids, b2)), by_id, fw),
            "agreement_subset_binary": concordance_block(
                [(i, x) for i, x, y in zip(ids, b1, b2) if x == y], by_id, fw),
            "agreement_subset_exact_level": concordance_block(
                [(i, x >= 2) for i, x, y in zip(ids, l1, l2) if x == y], by_id, fw)},
    }
    ex = [i for i in ids if i not in CODEBOOK_EXAMPLES]
    if len(ex) < len(ids):
        k1, k2 = [a1[i] for i in ex], [a2[i] for i in ex]
        out["excluding_codebook_examples"] = {
            "n": len(ex),
            "kappa_unweighted": float(cohen_kappa_score(k1, k2)),
            "kappa_quadratic": float(cohen_kappa_score(k1, k2, weights="quadratic")),
            "kappa_binary_ge2": float(cohen_kappa_score([x >= 2 for x in k1], [x >= 2 for x in k2]))}
    return out


# --------------------------------------------------------------------- tables
def f3(x) -> str:
    return "n/a" if x is None else f"{x:.3f}"


def write_tables(res) -> None:
    ths = [str(t) for t in THRESHOLDS]
    lines = ["| Source release | n | " + " | ".join(f"J<{t}" for t in ths) + " |",
             "|---|---|" + "---|" * len(ths)]
    for c in res["threshold_sensitivity"]["cohorts_at_v19"]:
        lines.append(f"| v{c['src']} | {c['n']} | " +
                     " | ".join(f3(c["share_below"][t]) for t in ths) + " |")
    lines += ["", "| Transition | n | " + " | ".join(f"J<{t}" for t in ths) + " |",
              "|---|---|" + "---|" * len(ths)]
    for c in res["threshold_sensitivity"]["consecutive_transitions"]:
        lines.append(f"| v{c['from']} to v{c['to']} | {c['n']} | " +
                     " | ".join(f3(c["share_below"][t]) for t in ths) + " |")
    s = res["threshold_sensitivity"]["staleness_clock"]["summary_v7_to_v18"]
    lines += ["", "| Threshold | t10 substantive (min / median / max, years) | censored cohorts "
              "| t10 J-only (min / median / max) | censored |", "|---|---|---|---|---|"]
    for t in THRESHOLDS:
        a, b = s[f"sub_{t}"], s[f"jonly_{t}"]
        lines.append(f"| {t} | {a['min']} / {a['median']} / {a['max']} | {a['censored']}/{a['n_cohorts']} "
                     f"| {b['min']} / {b['median']} / {b['max']} | {b['censored']}/{b['n_cohorts']} |")
    (TABLES / "t20_threshold_sensitivity.md").write_text("\n".join(lines) + "\n")

    cv = res["convergent_validity"]
    lines = []
    for pop, label in (("all_pairs", "all identifier-stable pairs"),
                       ("edited_pairs", "pairs with an edited description")):
        blk = cv[pop]
        lines += [f"**{label}** (n = {blk['n']}, J<0.8 in {blk['j_below_0.8']})", "",
                  "| Reference signal | base rate | agreement | kappa | precision of J<0.8 "
                  "| recall of J<0.8 | AUC of 1-J | Youden-optimal J threshold |",
                  "|---|---|---|---|---|---|---|---|"]
        for sname, c in blk["concordance_j_lt_0.8"].items():
            a = (blk["auc_for_major_bump"]["jaccard"] if sname == "major_bump" else
                 blk["auc_for_structured_change"]["jaccard"] if sname == "structured_changed"
                 else auc_lookup(res, pop, sname))
            y = blk["youden_threshold"][sname]
            lines.append(f"| {sname} | {f3(blk['signal_rates'][sname])} | {f3(c['agreement'])} "
                         f"| {f3(c['kappa'])} | {f3(c['precision'])} | {f3(c['recall'])} "
                         f"| {f3(a)} | {y['threshold']:.3f} (Youden {y['youden']:.3f}) |")
        lines += ["", "| Metric | AUC for major version bump | AUC for structured-field change "
                  "| Spearman rho with token Jaccard |", "|---|---|---|---|"]
        for m in blk["auc_for_major_bump"]:
            lines.append(f"| {m} | {f3(blk['auc_for_major_bump'][m])} "
                         f"| {f3(blk['auc_for_structured_change'][m])} "
                         f"| {f3(blk['spearman_vs_jaccard'].get(m))} |")
        lines.append("")
    (TABLES / "t20_convergent_validity.md").write_text("\n".join(lines))

    p = res.get("pilot")
    if not p:
        return
    k4, kb = p["kappa_4_level"], p["kappa_binary_ge2"]
    lines = [f"Pilot: two model annotators, {p['n_scored']} items. Not the human study.", "",
             "| Statistic | value |", "|---|---|",
             f"| kappa, 4-level, unweighted | {f3(k4['unweighted'])} |",
             f"| kappa, 4-level, linear weights | {f3(k4['linear'])} |",
             f"| kappa, 4-level, quadratic weights | {f3(k4['quadratic'])} |",
             f"| exact agreement / within one level | {f3(k4['exact_agreement'])} / {f3(k4['within_one_level'])} |",
             f"| kappa, binary (level >= 2) | {f3(kb['unweighted'])} (agreement {f3(kb['agreement'])}) |",
             "", "| Reference | n | substantive rate | precision of J<0.8 | recall of J<0.8 "
             "| pop.-weighted precision / recall | AUC of 1-J | Youden-optimal J threshold |",
             "|---|---|---|---|---|---|---|---|"]
    for name, c in p["concordance_with_j_lt_0.8"].items():
        pw, y = c["population_weighted"], c["youden"]
        lines.append(f"| {name} | {c['n']} | {f3(c['ref_positive'] / c['n'])} | {f3(c['precision'])} "
                     f"| {f3(c['recall'])} | {f3(pw['precision'])} / {f3(pw['recall'])} "
                     f"| {f3(c['auc_1_minus_j'])} | {y['threshold']:.3f} (Youden {y['youden']:.3f}) |")
    lines += ["", "| Jaccard bin | " + " | ".join(p["concordance_with_j_lt_0.8"]) + " |",
              "|---|" + "---|" * len(p["concordance_with_j_lt_0.8"])]
    for name, _, _ in BINS:
        lines.append(f"| {name} | " + " | ".join(
            f3(c["rate_ge2_by_bin"][name]) for c in p["concordance_with_j_lt_0.8"].values()) + " |")
    (TABLES / "t20_pilot_annotation.md").write_text("\n".join(lines) + "\n")


def auc_lookup(res, pop, sname):
    rows = res["_pairs_all"] if pop == "all_pairs" else [r for r in res["_pairs_all"] if r["edited"]]
    return auc([1 - r["jaccard"] for r in rows], [r[sname] for r in rows])


# ----------------------------------------------------------------------- main
def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    con = ad.connect()
    rels = ad.releases(con, DOMAIN)
    majors = ad.major_releases(con, DOMAIN)
    snaps = {r.version: ad.load_snapshot(con, DOMAIN, r.version, with_desc=True) for r in rels}

    pairs = consecutive_pairs(snaps, majors)
    cohorts = cohort_shares(snaps, majors, majors[-1])
    clock = staleness_clock(con, snaps, rels, majors)

    # self-checks against the published numbers
    e3 = json.loads((OUT / "e1_e2_e3.json").read_text())[DOMAIN]["semantic"]
    pub = {r["src"]: r["substantial_frac"] for r in e3 if r["tgt"] == majors[-1].version}
    for c in cohorts:
        assert abs(c["share_below"]["0.8"] - pub[c["src"]]) < 1e-9, c["src"]
    e12 = json.loads((OUT / "e12_temporal_structure.json").read_text())["staleness_clocks"][DOMAIN]
    for row in e12:
        assert clock["per_cohort"][row["src"]]["t10_sub_0.8"] == row["t10_sub"], row["src"]
    e11 = json.loads((OUT / "e11_version_metadata.json").read_text())["summary"]
    assert len(pairs) == e11["carried_over_pairs"]

    sample = draw_sample(pairs)
    sample_meta = write_sample(sample, pairs)

    res = {
        "domain": DOMAIN, "seed": SEED, "thresholds": THRESHOLDS,
        "threshold_sensitivity": {
            "cohorts_at_v19": cohorts,
            "consecutive_transitions": transition_shares(pairs),
            "boilerplate_confound": boilerplate_confound(pairs),
            "staleness_clock": clock},
        "convergent_validity": convergent_validity(pairs),
        "annotation_sample": sample_meta,
        "pilot": pilot(sample, sample_meta),
        "_pairs_all": pairs,
    }
    write_tables(res)
    del res["_pairs_all"]
    (OUT / "e20_semantic_validation.json").write_text(json.dumps(res, indent=1))

    s = clock["summary_v7_to_v18"]
    print("t10 substantive clock, v7.0-v18.0 cohorts (min/median/max):", file=sys.stderr)
    for t in THRESHOLDS:
        print(f"  J<{t}: sub {s[f'sub_{t}']['min']}/{s[f'sub_{t}']['median']}/{s[f'sub_{t}']['max']}"
              f"  J-only {s[f'jonly_{t}']['min']}/{s[f'jonly_{t}']['median']}/{s[f'jonly_{t}']['max']}",
              file=sys.stderr)
    cv = res["convergent_validity"]["all_pairs"]
    print(f"\n{cv['n']} consecutive-major pairs; AUC(1-J) for major bump "
          f"{cv['auc_for_major_bump']['jaccard']:.3f}, for structured change "
          f"{cv['auc_for_structured_change']['jaccard']:.3f}", file=sys.stderr)
    print(f"sample: {sample_meta['n']} items from {sample_meta['frame_edited_pairs']} edited pairs, "
          f"frame per bin {sample_meta['frame_per_bin']}", file=sys.stderr)
    if res["pilot"]:
        k = res["pilot"]["kappa_4_level"]
        print(f"pilot kappa unweighted {k['unweighted']:.3f}, quadratic {k['quadratic']:.3f}",
              file=sys.stderr)
    else:
        print("no pilot files; skipped V4", file=sys.stderr)
    print(f"wrote {OUT/'e20_semantic_validation.json'}", file=sys.stderr)


if __name__ == "__main__":
    main()
