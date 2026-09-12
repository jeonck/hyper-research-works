#!/usr/bin/env python3
"""E18: a real text-to-technique classifier under vocabulary drift, with the
vocabulary-drift and data-drift contributions separated.

The synthetic scorer of E5 holds the intelligence constant by construction. A
reviewer can object that a trained model is different: its errors come from
the data it saw, not only from the labels it was given. This experiment trains
an ordinary supervised classifier on one era's corpus and evaluates it on a
later era's gold, then separates what the vocabulary cost from what the data
shift cost, in the spirit of TESSERACT-style temporal hygiene.

Model
  TF-IDF (word 1-2 grams, sublinear tf, min_df 2, 200k features) followed by
  one-vs-rest LinearSVC(class_weight="balanced"), multi-label, threshold at the
  decision boundary. A label is trainable only if it has at least MIN_SUPPORT
  positive documents in the training corpus; every other gold label is kept in
  the evaluation and counts against recall.

Corpora (all public, all consumed by published work)
  rcatt      1,490 full CTI reports, 215 technique labels in the pre-sub-
             technique vocabulary (v4.0-v6.3 live interval; V = 6.3 is used)
  tram       TRAM bootstrap sentences, union of the two shipped files, keyed
             on sentence text, negatives dropped (v13.0 best fit)
  ctibench   CTIBench CTI-ATE descriptions, Enterprise platform only, gold
             from the GT column (v14.0 best fit; Mobile items are a different
             ATT&CK domain and are excluded)

Conditions for a model of vocabulary V evaluated on gold of vocabulary W
  naive          predicted identifiers scored against gold verbatim
  normalized     both sides projected onto the newest release (ATT&CK-Norm,
                 revocation-chain resolution, ledger reported)
  vocab_matched  the modern side back-projected into the older vocabulary
                 (parent technique for sub-techniques, pre-revocation
                 identifier via the revocation graph, as build_backmap in
                 04_attribution.py); the same predictions, the same
                 intelligence, only the label space is held equal
  ceiling_matched  5-fold cross-fitted model trained on the test corpus itself
                 with its gold back-projected into the same older vocabulary:
                 same vocabulary, same data distribution
  ceiling_native   the same cross-fit in the test corpus's own vocabulary

Decomposition (per metric)
  total loss   = ceiling_matched - naive
  vocabulary   = vocab_matched  - naive      (only the label space moved)
  data drift   = ceiling_matched - vocab_matched
  norm gain    = normalized - naive          (what a practitioner recovers)

Paired bootstrap over test documents (2,000 resamples) gives 95% CIs and
two-sided p-values for each contrast; p-values are Holm-corrected within each
(pair, metric) family.
"""
from __future__ import annotations

import csv
import importlib
import json
import os
import re
import sys
import warnings
from collections import Counter
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import KFold
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC

sys.path.insert(0, str(Path(__file__).resolve().parent))
import attackdrift as ad  # noqa: E402

build_backmap = importlib.import_module("04_attribution").build_backmap

csv.field_size_limit(10_000_000)
OUT = Path(__file__).resolve().parents[1] / "data" / "results"
TABLES = Path(__file__).resolve().parents[1] / "paper" / "tables"
EXT = Path(os.environ.get("HYPER_EXT", "/home/user/ext"))
DOMAIN = "enterprise-attack"
TID = re.compile(r"\bT\d{4}(?:\.\d{3})?\b")
SEED = 20260912
MIN_SUPPORT = 5
N_FOLDS = 5
N_BOOT = 2000
# vocabulary release of each corpus: rcATT from the upper end of its fully
# consistent interval (closest to its 2019-10 release), the others from the
# best-fit release of E7
CORPUS_RELEASE = {"rcatt": "6.3", "tram": "13.0", "ctibench": "14.0"}


# ----------------------------------------------------------------------
# corpora: list of (text, set of technique ids)
# ----------------------------------------------------------------------

def load_rcatt() -> list[tuple[str, set[str]]]:
    p = EXT / "rcATT/classification_tools/data/training_data_original.csv"
    docs = []
    with p.open(encoding="ISO-8859-1") as fh:
        reader = csv.reader(fh)
        header = next(reader)
        cols = [(i, h) for i, h in enumerate(header) if TID.fullmatch(h)]
        for row in reader:
            labs = {t for i, t in cols if i < len(row) and row[i].strip() in {"1", "1.0"}}
            if labs and row[0].strip():
                docs.append((row[0], labs))
    return docs


def load_tram() -> list[tuple[str, set[str]]]:
    by_text: dict[str, set[str]] = {}
    for name in ("training/bootstrap-training-data.json",
                 "training/attack_may_2023_merged_bootstrap_data2.json"):
        for s in json.loads((EXT / "tram/data" / name).read_text())["sentences"]:
            labs = {m["attack_id"] for m in s.get("mappings") or []
                    if m.get("attack_id") and TID.fullmatch(m["attack_id"])}
            if labs:
                by_text.setdefault(s["text"].strip(), set()).update(labs)
    return [(t, l) for t, l in by_text.items() if t]


def load_ctibench(platform: str = "Enterprise") -> list[tuple[str, set[str]]]:
    docs = []
    p = EXT / "cti-bench/data/cti-ate.tsv"
    for row in csv.DictReader(p.open(), delimiter="\t"):
        if (row.get("Platform") or "").strip() != platform:
            continue
        labs = set(TID.findall(row.get("GT") or ""))
        if labs:
            docs.append((row["Description"], labs))
    return docs


CORPORA = {"rcatt": load_rcatt, "tram": load_tram, "ctibench": load_ctibench}


# ----------------------------------------------------------------------
# model
# ----------------------------------------------------------------------

def fit_model(texts: list[str], labelsets: list[set[str]], min_support: int = MIN_SUPPORT):
    support = Counter(t for ls in labelsets for t in ls)
    labels = sorted(t for t, c in support.items() if c >= min_support)
    vec = TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=200_000,
                          sublinear_tf=True, strip_accents="unicode", dtype=np.float32)
    X = vec.fit_transform(texts)
    idx = {t: i for i, t in enumerate(labels)}
    Y = np.zeros((len(texts), len(labels)), dtype=np.int64)  # int8 wraps class indices past 127 labels
    for r, ls in enumerate(labelsets):
        for t in ls:
            if t in idx:
                Y[r, idx[t]] = 1
    clf = OneVsRestClassifier(LinearSVC(class_weight="balanced", random_state=SEED), n_jobs=-1)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        clf.fit(X, Y)
    return {"vec": vec, "clf": clf, "labels": labels, "n_trainable": len(labels),
            "n_labels_total": len(support)}


def predict(model: dict, texts: list[str]) -> list[set[str]]:
    dec = model["clf"].decision_function(model["vec"].transform(texts))
    labels = model["labels"]
    return [{labels[j] for j in np.flatnonzero(row > 0)} for row in dec]


def crossfit(texts: list[str], labelsets: list[set[str]]) -> list[set[str]]:
    """Every document predicted by a model that did not see it (K-fold)."""
    preds: list[set[str] | None] = [None] * len(texts)
    for tr, te in KFold(N_FOLDS, shuffle=True, random_state=SEED).split(texts):
        m = fit_model([texts[i] for i in tr], [labelsets[i] for i in tr])
        for i, p in zip(te, predict(m, [texts[i] for i in te])):
            preds[i] = p
    return preds  # type: ignore[return-value]


# ----------------------------------------------------------------------
# vocabulary projections
# ----------------------------------------------------------------------

def back_project(ids: set[str], back: dict[str, str | None], w: ad.Snapshot,
                 ledger: Counter | None = None) -> set[str]:
    """W-vocabulary identifiers -> what a V-era analyst would have written."""
    rev = w.revoked_by()
    out, n_dropped = set(), 0
    for src in sorted(ids):
        t = src
        if t not in back:  # not live in W: resolve inside W first, then climb
            t2 = ad.resolve_chain(t, rev)
            if t2 in back:
                t = t2
            elif "." in t and t.split(".")[0] in back:
                t = t.split(".")[0]
        tgt = back.get(t)
        n_dropped += tgt is None
        if ledger is not None:
            if tgt is None:
                ledger["dropped"] += 1
            elif tgt == src:
                ledger["kept"] += 1
            elif "." in src and src.split(".")[0] == tgt:
                ledger["parent_collapsed"] += 1
            else:
                ledger["reverted_to_predecessor"] += 1
        if tgt is not None:
            out.add(tgt)
    if ledger is not None:
        ledger["input"] += len(ids)
        ledger["absorbed_by_merges"] += len(ids) - n_dropped - len(out)
    return out


def projection_ledger(docs_ids: list[set[str]], fn) -> dict:
    """Ledger over DISTINCT identifiers and over label instances."""
    distinct = set().union(*docs_ids) if docs_ids else set()
    led = Counter()
    fn(distinct, led)
    inst = Counter()
    for ids in docs_ids:
        fn(ids, inst)
    return {"distinct": dict(led), "instances": dict(inst)}


# ----------------------------------------------------------------------
# scoring
# ----------------------------------------------------------------------

def per_doc_counts(preds: list[set[str]], golds: list[set[str]]) -> dict[str, np.ndarray]:
    tp = np.array([len(p & g) for p, g in zip(preds, golds)], dtype=float)
    fp = np.array([len(p - g) for p, g in zip(preds, golds)], dtype=float)
    fn = np.array([len(g - p) for p, g in zip(preds, golds)], dtype=float)
    denom = 2 * tp + fp + fn
    sf1 = np.where(denom > 0, 2 * tp / np.maximum(denom, 1e-12), 1.0)
    return {"tp": tp, "fp": fp, "fn": fn, "sample_f1": sf1}


def micro_f1(c: dict[str, np.ndarray], idx=None) -> float:
    tp, fp, fn = (c[k] if idx is None else c[k][idx] for k in ("tp", "fp", "fn"))
    d = 2 * tp.sum() + fp.sum() + fn.sum()
    return float(2 * tp.sum() / d) if d else 1.0


def macro_f1(preds: list[set[str]], golds: list[set[str]]) -> float:
    labels = set().union(*preds, *golds)
    f1s = []
    for t in labels:
        tp = sum(1 for p, g in zip(preds, golds) if t in p and t in g)
        fp = sum(1 for p, g in zip(preds, golds) if t in p and t not in g)
        fn = sum(1 for p, g in zip(preds, golds) if t not in p and t in g)
        f1s.append(2 * tp / (2 * tp + fp + fn) if (2 * tp + fp + fn) else 0.0)
    return float(np.mean(f1s)) if f1s else 0.0


def metrics(preds: list[set[str]], golds: list[set[str]]) -> dict:
    c = per_doc_counts(preds, golds)
    tp, fp, fn = c["tp"].sum(), c["fp"].sum(), c["fn"].sum()
    return {"micro_f1": micro_f1(c),
            "micro_precision": float(tp / (tp + fp)) if tp + fp else 0.0,
            "micro_recall": float(tp / (tp + fn)) if tp + fn else 0.0,
            "macro_f1": macro_f1(preds, golds),
            "sample_f1": float(c["sample_f1"].mean()),
            "n_docs": len(golds),
            "gold_instances": int(sum(len(g) for g in golds)),
            "pred_instances": int(sum(len(p) for p in preds)),
            "gold_distinct": len(set().union(*golds)) if golds else 0,
            "docs_with_empty_gold": int(sum(1 for g in golds if not g))}


def paired_bootstrap(ca: dict, cb: dict, rng: np.random.Generator) -> dict:
    """Contrast a - b on micro-F1 and sample-F1 over resampled documents."""
    n = len(ca["tp"])
    d_micro, d_sample = np.empty(N_BOOT), np.empty(N_BOOT)
    for b in range(N_BOOT):
        idx = rng.integers(0, n, n)
        d_micro[b] = micro_f1(ca, idx) - micro_f1(cb, idx)
        d_sample[b] = ca["sample_f1"][idx].mean() - cb["sample_f1"][idx].mean()
    out = {}
    for name, d, point in (("micro_f1", d_micro, micro_f1(ca) - micro_f1(cb)),
                           ("sample_f1", d_sample,
                            ca["sample_f1"].mean() - cb["sample_f1"].mean())):
        p = 2 * min((d <= 0).mean(), (d >= 0).mean())
        out[name] = {"delta": float(point),
                     "ci": [float(np.quantile(d, 0.025)), float(np.quantile(d, 0.975))],
                     "p_boot": float(max(p, 1 / N_BOOT))}
    return out


def holm(pvals: dict[str, float]) -> dict[str, float]:
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m, out, running = len(items), {}, 0.0
    for i, (k, p) in enumerate(items):
        running = max(running, min(1.0, (m - i) * p))
        out[k] = running
    return out


# ----------------------------------------------------------------------
# one (train corpus, test corpus) pair
# ----------------------------------------------------------------------

def run_pair(train: str, test: str, corpora: dict, snaps: dict, newest: ad.Snapshot,
             models: dict) -> dict:
    tr_texts, tr_gold = zip(*corpora[train])
    te_texts, te_gold = zip(*corpora[test])
    te_texts, te_gold = list(te_texts), list(te_gold)
    v_rel, w_rel = CORPUS_RELEASE[train], CORPUS_RELEASE[test]
    model_is_older = _key(v_rel) < _key(w_rel)
    old_rel, new_rel = (v_rel, w_rel) if model_is_older else (w_rel, v_rel)
    old, new = snaps[old_rel], snaps[new_rel]
    back = build_backmap(old, new)

    if train not in models:
        models[train] = fit_model(list(tr_texts), list(tr_gold))
    model = models[train]
    preds = predict(model, te_texts)

    def norm_fn(ids, led):
        r = ad.normalize_with_ledger(ids, newest)
        for k, v in r.summary().items():
            led[k] += v
        return r.ids

    def back_fn(ids, led):
        return back_project(ids, back, new, led)

    conds: dict[str, tuple[list[set[str]], list[set[str]]]] = {}
    conds["naive"] = (preds, te_gold)
    conds["normalized"] = ([norm_fn(p, Counter()) for p in preds],
                           [norm_fn(g, Counter()) for g in te_gold])
    ledgers = {"normalized_predictions": projection_ledger(preds, norm_fn),
               "normalized_gold": projection_ledger(te_gold, norm_fn)}
    if model_is_older:  # gold is modern: back-project gold into the model's vocabulary
        matched_gold = [back_fn(g, Counter()) for g in te_gold]
        conds["vocab_matched"] = (preds, matched_gold)
        ledgers["backprojected_gold"] = projection_ledger(te_gold, back_fn)
    else:  # predictions are modern: back-project them into the gold's vocabulary
        matched_gold = te_gold
        conds["vocab_matched"] = ([back_fn(p, Counter()) for p in preds], te_gold)
        ledgers["backprojected_predictions"] = projection_ledger(preds, back_fn)

    ceiling_ok = len(te_texts) >= 200
    if ceiling_ok:
        conds["ceiling_matched"] = (crossfit(te_texts, matched_gold), matched_gold)
        conds["ceiling_native"] = ((conds["ceiling_matched"][0] if not model_is_older
                                    else crossfit(te_texts, te_gold)), te_gold)

    res = {"train": train, "test": test, "model_release": v_rel, "gold_release": w_rel,
           "reference_release": newest.version, "direction":
           "old model -> modern gold" if model_is_older else "modern model -> old gold",
           "n_train_docs": len(tr_texts), "n_test_docs": len(te_texts),
           "trainable_labels": model["n_trainable"], "train_labels_total": model["n_labels_total"],
           "min_support": MIN_SUPPORT, "ceiling_estimated": ceiling_ok,
           "conditions": {k: metrics(p, g) for k, (p, g) in conds.items()},
           "ledgers": ledgers}
    counts = {k: per_doc_counts(p, g) for k, (p, g) in conds.items()}
    rng = np.random.default_rng(SEED)
    contrasts = {"vocabulary": ("vocab_matched", "naive"),
                 "norm_gain": ("normalized", "naive")}
    if ceiling_ok:
        contrasts.update({"data_drift": ("ceiling_matched", "vocab_matched"),
                          "total": ("ceiling_matched", "naive"),
                          "granularity": ("ceiling_native", "ceiling_matched")})
    boot = {name: paired_bootstrap(counts[a], counts[b], rng) for name, (a, b) in contrasts.items()}
    for metric in ("micro_f1", "sample_f1"):
        adj = holm({name: boot[name][metric]["p_boot"] for name in boot})
        for name in boot:
            boot[name][metric]["p_holm"] = adj[name]
    res["contrasts"] = boot
    return res


def _key(v: str) -> tuple:
    return tuple(int(x) for x in v.split("."))


# ----------------------------------------------------------------------
# table
# ----------------------------------------------------------------------

def fmt_ci(c: dict) -> str:
    return f"{c['delta']:+.3f} [{c['ci'][0]:+.3f}, {c['ci'][1]:+.3f}]"


def write_table(rows: list[dict]) -> None:
    lines = ["| Train -> test | Model / gold vocab | Condition | micro-F1 | micro-P | micro-R | macro-F1 | sample-F1 | Gold labels (instances, distinct) |",
             "|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        for cond, m in r["conditions"].items():
            lines.append(f"| {r['train']} -> {r['test']} (n={r['n_test_docs']}) | v{r['model_release']} / v{r['gold_release']} | {cond} | "
                         f"{m['micro_f1']:.3f} | {m['micro_precision']:.3f} | {m['micro_recall']:.3f} | "
                         f"{m['macro_f1']:.3f} | {m['sample_f1']:.3f} | {m['gold_instances']}, {m['gold_distinct']} |")
    lines += ["", "| Train -> test | Contrast | micro-F1 delta [95% CI] | p (Holm) | sample-F1 delta [95% CI] | p (Holm) |",
              "|---|---|---|---|---|---|"]
    for r in rows:
        for name, c in r["contrasts"].items():
            lines.append(f"| {r['train']} -> {r['test']} | {name} | {fmt_ci(c['micro_f1'])} | "
                         f"{c['micro_f1']['p_holm']:.3g} | {fmt_ci(c['sample_f1'])} | {c['sample_f1']['p_holm']:.3g} |")
    lines += ["", "| Train -> test | Projection | Distinct: input / kept / collapsed-to-parent / reverted / merged-away / dropped / demoted |",
              "|---|---|---|"]
    for r in rows:
        for name, led in r["ledgers"].items():
            d = led["distinct"]
            lines.append(f"| {r['train']} -> {r['test']} | {name} | {d.get('input', 0)} / {d.get('kept', 0)} / "
                         f"{d.get('parent_collapsed', 0)} / {d.get('reverted_to_predecessor', 0)} / "
                         f"{d.get('absorbed_by_merges', 0)} / {d.get('dropped', 0)} / {d.get('demoted', 0)} |")
    (TABLES / "t18_real_classifier.md").write_text("\n".join(lines) + "\n")


def main() -> None:
    con = ad.connect()
    newest_rel = ad.releases(con, DOMAIN)[-1]
    newest = ad.load_snapshot(con, DOMAIN, newest_rel.version)
    snaps = {v: ad.load_snapshot(con, DOMAIN, v) for v in set(CORPUS_RELEASE.values())}
    corpora = {name: fn() for name, fn in CORPORA.items()}
    for name, docs in corpora.items():
        print(f"  {name}: {len(docs)} docs, {sum(len(l) for _, l in docs)} label instances, "
              f"{len(set().union(*(l for _, l in docs)))} distinct", file=sys.stderr)
    models: dict = {}
    rows = []
    for train, test in (("rcatt", "tram"), ("rcatt", "ctibench"), ("tram", "rcatt"),
                        ("tram", "ctibench")):
        r = run_pair(train, test, corpora, snaps, newest, models)
        rows.append(r)
        c = r["conditions"]
        print(f"  {train}->{test}: " + " | ".join(f"{k} {v['micro_f1']:.3f}/{v['sample_f1']:.3f}"
                                                  for k, v in c.items()), file=sys.stderr)
    out = {"seed": SEED, "min_support": MIN_SUPPORT, "n_boot": N_BOOT, "n_folds": N_FOLDS,
           "corpus_release": CORPUS_RELEASE, "reference_release": newest_rel.version,
           "model": "tfidf(1-2gram, sublinear, min_df=2, max_features=200k) + OvR LinearSVC(balanced)",
           "pairs": rows}
    (OUT / "e18_real_classifier.json").write_text(json.dumps(out, indent=1))
    write_table(rows)
    print(f"wrote {OUT/'e18_real_classifier.json'} and {TABLES/'t18_real_classifier.md'}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
