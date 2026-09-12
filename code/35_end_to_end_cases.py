#!/usr/bin/env python3
"""E19: end-to-end cases on real artefacts — do real conclusions move?

Two cases, both computed from public artefacts rather than from ATT&CK's own
edges, so neither is an internal-consistency score.

Case A  Two trained systems, three real gold sets, one leaderboard.
        S1 is a classifier trained on rcATT's 2019 report corpus (the v6.3
        vocabulary; rcATT's shipped joblib pipelines no longer unpickle under
        a current scikit-learn, so S1 is a faithful re-instantiation of its
        design: TF-IDF + linear SVM, trained on rcATT's own labels). S2 is the
        same design trained on the TRAM bootstrap sentences (v13.0). Each is
        scored on rcATT (v6.3 gold), TRAM (v13.0 gold; in-domain systems are
        scored by 5-fold cross-fit so no sentence is scored by a model that saw
        it) and CTIBench CTI-ATE (v14.0 gold), under naive scoring, ATT&CK-Norm
        scoring (predictions and gold both projected onto v19.2) and
        vocabulary-matched scoring (the modern side back-projected into the
        older vocabulary). An item passes if its sample-F1 is at least 0.5; a
        verdict flip is an item whose pass/fail differs between naive and
        normalized scoring. The leaderboard question is whether the ORDER of
        S1 and S2 on a gold set changes with the scoring vocabulary.

Case B  Named, published ATT&CK Navigator layers (vendor threat reports
        redistributed by DeTT&CT, and MITRE's own samples). For each layer:
        the release interval its annotations are simultaneously live in, the
        share of annotations that still denote at v19.2, the ledger of
        projecting them onto v19.2, and the layer's catalogue share (distinct
        live annotations over live techniques) as authored versus at v19.2.
"""
from __future__ import annotations

import importlib
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import attackdrift as ad  # noqa: E402

rc = importlib.import_module("34_real_classifier")
build_backmap = importlib.import_module("04_attribution").build_backmap

OUT = Path(__file__).resolve().parents[1] / "data" / "results"
TABLES = Path(__file__).resolve().parents[1] / "paper" / "tables"
EXT = Path(os.environ.get("HYPER_EXT", "/home/user/ext"))
NAV = Path(os.environ.get("ATTACK_STIX_REPO", "/home/user/mitre-attack/attack-stix-data")).parent / "attack-navigator"
DOMAIN = "enterprise-attack"
PASS_F1 = 0.5
SEED = 20260912
SYSTEMS = {"S1 (rcATT-era, v6.3)": "rcatt", "S2 (TRAM-era, v13.0)": "tram"}


def _key(v: str) -> tuple:
    return tuple(int(x) for x in v.split("."))


# ----------------------------------------------------------------------
# Case A
# ----------------------------------------------------------------------

def case_a(con) -> dict:
    corpora = {k: f() for k, f in rc.CORPORA.items()}
    rels = ad.releases(con, DOMAIN)
    newest = ad.load_snapshot(con, DOMAIN, rels[-1].version)
    snaps = {v: ad.load_snapshot(con, DOMAIN, v) for v in set(rc.CORPUS_RELEASE.values())}
    models = {name: rc.fit_model(*map(list, zip(*corpora[name]))) for name in SYSTEMS.values()}

    def project_norm(ids):
        return ad.normalize(ids, newest)

    results = {"reference_release": newest.version, "pass_threshold_sample_f1": PASS_F1,
               "gold_sets": {}}
    for gold_name, docs in corpora.items():
        texts, gold = [d[0] for d in docs], [d[1] for d in docs]
        g_rel = rc.CORPUS_RELEASE[gold_name]
        entry = {"n_items": len(docs), "gold_release": g_rel, "systems": {}}
        for sys_label, train_name in SYSTEMS.items():
            m_rel = rc.CORPUS_RELEASE[train_name]
            if train_name == gold_name:
                preds = rc.crossfit(texts, gold)
                how = "5-fold cross-fit (in-domain)"
            else:
                preds = rc.predict(models[train_name], texts)
                how = "direct"
            conds = {"naive": (preds, gold),
                     "normalized": ([project_norm(p) for p in preds], [project_norm(g) for g in gold])}
            if _key(m_rel) != _key(g_rel):
                old_rel, new_rel = (m_rel, g_rel) if _key(m_rel) < _key(g_rel) else (g_rel, m_rel)
                back = build_backmap(snaps[old_rel], snaps[new_rel])
                if _key(m_rel) < _key(g_rel):   # older model: back-project modern gold
                    conds["vocab_matched"] = (preds, [rc.back_project(g, back, snaps[new_rel]) for g in gold])
                else:                            # modern model: back-project its predictions
                    conds["vocab_matched"] = ([rc.back_project(p, back, snaps[new_rel]) for p in preds], gold)
            sc = {}
            counts = {}
            for c, (p, g) in conds.items():
                sc[c] = rc.metrics(p, g)
                counts[c] = rc.per_doc_counts(p, g)
            passed = {c: counts[c]["sample_f1"] >= PASS_F1 for c in conds}
            flips = {"fail_to_pass": int((~passed["naive"] & passed["normalized"]).sum()),
                     "pass_to_fail": int((passed["naive"] & ~passed["normalized"]).sum()),
                     "pass_naive": int(passed["naive"].sum()),
                     "pass_normalized": int(passed["normalized"].sum())}
            if "vocab_matched" in passed:
                flips["pass_vocab_matched"] = int(passed["vocab_matched"].sum())
                flips["fail_to_pass_vocab_matched"] = int((~passed["naive"] & passed["vocab_matched"]).sum())
            entry["systems"][sys_label] = {"model_release": m_rel, "scoring": how,
                                           "scores": sc, "verdicts": flips}
        # leaderboard order per condition
        order = {}
        for c in ("naive", "normalized", "vocab_matched"):
            ranked = sorted(((s["scores"][c]["micro_f1"], lab) for lab, s in entry["systems"].items()
                             if c in s["scores"]), reverse=True)
            if ranked:
                order[c] = [lab for _, lab in ranked]
        entry["leaderboard_order"] = order
        # only naive vs normalized: vocab_matched exists for one system per gold set
        entry["order_changes"] = order.get("normalized") != order["naive"]
        results["gold_sets"][gold_name] = entry
        print(f"  {gold_name}: " + " | ".join(
            f"{lab}: naive {s['scores']['naive']['micro_f1']:.3f} norm {s['scores']['normalized']['micro_f1']:.3f}"
            for lab, s in entry["systems"].items()), file=sys.stderr)
    return results


# ----------------------------------------------------------------------
# Case B
# ----------------------------------------------------------------------

def layer_files() -> list[Path]:
    roots = [EXT / "DeTTECT" / "threat-actor-data", NAV / "layers" / "samples"]
    out = []
    for r in roots:
        if r.exists():
            out += sorted(p for p in r.rglob("*.json"))
    return out


def layer_name(d: dict, p: Path) -> str:
    for t in d.get("techniques", []):
        for m in t.get("metadata") or []:
            if m.get("name") in ("Group", "Campaign", "Source") and m.get("value"):
                return str(m["value"])
    return d.get("name") or p.stem


def case_b(con) -> dict:
    rels = ad.releases(con, DOMAIN)
    snaps = {r.version: ad.load_snapshot(con, DOMAIN, r.version) for r in rels}
    live = {v: s.live_tech() for v, s in snaps.items()}
    newest_v = rels[-1].version
    newest = snaps[newest_v]
    rows = []
    for p in layer_files():
        try:
            d = json.loads(p.read_text())
        except Exception:
            continue
        if not isinstance(d, dict) or not isinstance(d.get("techniques"), list):
            continue
        if d.get("domain", "enterprise-attack") != "enterprise-attack":
            continue
        ids = {t["techniqueID"] for t in d["techniques"] if t.get("techniqueID")}
        if len(ids) < 5:
            continue
        declared = (d.get("versions") or {}).get("attack")
        consistent = [r.version for r in rels if ids <= live[r.version]]
        interval = (consistent[0], consistent[-1]) if consistent else None
        authored_v = consistent[0] if consistent else None
        led = ad.normalize_with_ledger(ids, newest)
        dead = sorted(t for t in ids if t not in live[newest_v])
        row = {"file": str(p.relative_to(EXT.parent) if str(p).startswith(str(EXT.parent)) else p),
               "layer": layer_name(d, p), "folder": p.parent.name, "declared_version": declared,
               "n_distinct": len(ids), "provenance_interval": interval,
               "n_consistent_releases": len(consistent),
               "dead_at_newest": len(dead), "dead_share": len(dead) / len(ids),
               "dead_ids": dead,
               "ledger": led.summary(),
               "demoted": led.demoted, "merged": led.merged, "dropped": led.dropped,
               "catalogue_share_authored": (len(ids & live[authored_v]) / len(live[authored_v])) if authored_v else None,
               "catalogue_share_naive_newest": len(ids & live[newest_v]) / len(live[newest_v]),
               "catalogue_share_normalized_newest": len(led.ids) / len(live[newest_v])}
        rows.append(row)
    rows.sort(key=lambda r: -r["dead_share"])
    return {"reference_release": newest_v, "n_layers": len(rows),
            "n_declaring_version": sum(1 for r in rows if r["declared_version"]),
            "layers": rows}


# ----------------------------------------------------------------------
# tables
# ----------------------------------------------------------------------

def write_tables(a: dict, b: dict) -> None:
    lines = ["| Gold set (release, items) | System | Scoring | micro-F1 | sample-F1 | Items passing | Verdict flips naive→normalized (fail→pass / pass→fail) |",
             "|---|---|---|---|---|---|---|"]
    for g, e in a["gold_sets"].items():
        for lab, s in e["systems"].items():
            v = s["verdicts"]
            for c in ("naive", "normalized", "vocab_matched"):
                if c not in s["scores"]:
                    continue
                passing = {"naive": v["pass_naive"], "normalized": v["pass_normalized"],
                           "vocab_matched": v.get("pass_vocab_matched")}[c]
                flips = f"{v['fail_to_pass']} / {v['pass_to_fail']}" if c == "normalized" else ""
                lines.append(f"| {g} (v{e['gold_release']}, n={e['n_items']}) | {lab} | {c} | "
                             f"{s['scores'][c]['micro_f1']:.3f} | {s['scores'][c]['sample_f1']:.3f} | {passing} | {flips} |")
    lines += ["", "| Gold set | Order under naive | Order under normalized | Order changes? |", "|---|---|---|---|"]
    for g, e in a["gold_sets"].items():
        o = e["leaderboard_order"]
        lines.append(f"| {g} | {' > '.join(o['naive'])} | {' > '.join(o['normalized'])} | {'yes' if e['order_changes'] else 'no'} |")
    lines += ["", f"| Layer (publisher folder) | Declares release | Distinct techniques | Live interval | Dead at v{b['reference_release']} | Kept / merged-away / demoted / dropped | Catalogue share authored → naive → normalized |",
              "|---|---|---|---|---|---|---|"]
    for r in b["layers"][:12]:
        iv = f"v{r['provenance_interval'][0]}–v{r['provenance_interval'][1]}" if r["provenance_interval"] else "none (mixed)"
        L = r["ledger"]
        cs = (f"{100*r['catalogue_share_authored']:.1f}% → " if r["catalogue_share_authored"] is not None else "n/a → ") + \
             f"{100*r['catalogue_share_naive_newest']:.1f}% → {100*r['catalogue_share_normalized_newest']:.1f}%"
        lines.append(f"| {r['layer']} ({r['folder']}) | {r['declared_version'] or 'no'} | {r['n_distinct']} | {iv} | "
                     f"{r['dead_at_newest']} ({r['dead_share']:.2f}) | {L['kept']} / {L['absorbed_by_merges'] - L['merge_targets'] if L['merge_targets'] else 0} / {L['demoted']} / {L['dropped']} | {cs} |")
    (TABLES / "t19_end_to_end.md").write_text("\n".join(lines) + "\n")
    print("  wrote", TABLES / "t19_end_to_end.md", file=sys.stderr)


def main() -> None:
    con = ad.connect()
    print("Case A: two systems, three gold sets", file=sys.stderr)
    a = case_a(con)
    print("Case B: named Navigator layers", file=sys.stderr)
    b = case_b(con)
    for r in b["layers"][:8]:
        print(f"  {r['layer'][:50]:50s} n={r['n_distinct']:3d} dead={r['dead_at_newest']:3d} "
              f"({r['dead_share']:.2f}) interval={r['provenance_interval']}", file=sys.stderr)
    (OUT / "e19_end_to_end.json").write_text(json.dumps({"seed": SEED, "case_a": a, "case_b": b}, indent=1))
    write_tables(a, b)
    print(f"wrote {OUT/'e19_end_to_end.json'}", file=sys.stderr)


if __name__ == "__main__":
    main()
