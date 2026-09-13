#!/usr/bin/env python3
"""E24: LLM technique extractors under ontology drift — stale, fabricated, or live?

Section 7.8 measured a classical classifier. Deployed extractors are now LLMs,
whose "training corpus" is whatever ATT&CK looked like when the model was
trained, so the question is different: when a model is asked for technique
identifiers, which release is it answering from, and how much of its error is
drift rather than fabrication?

Every emitted identifier is classified against the release database:
  live         live in the analysis release (v19.2)
  stale        live in SOME earlier Enterprise release but revoked, deprecated
               or absent now — the only class that is ontology-drift-induced;
               split into resolvable (a revoked-by chain lands live) and not
  fabricated   never an Enterprise technique identifier in any release
               (a sub-class: exists only in Mobile or ICS = domain confusion)
The model's "home release" is the release at which the largest share of its
distinct emitted identifiers is live (the best-fit release of E7 applied to a
model instead of a corpus).

Prompt conditions (identical items, identical decoding):
  unspecified   no release named — the deployed default
  latest        "the current release, v19.2"
  era_pinned    the gold set's own release (TRAM v13.0, CTIBench v14.0, rcATT v6.3)
  legacy_pinned "ATT&CK v6.3", the pre-sub-technique vocabulary, for every gold set

Scoring against gold is as in E18: naive (verbatim), normalized (both sides
projected onto v19.2 with the ledger reported). Prompt sensitivity: two
paraphrases of the unspecified prompt on a subset, one model.

Decoding is pinned: temperature 0, fixed seed, num_predict cap, and each
model's ollama digest is recorded — the reporting contract of Section 10
applied to the paper's own experiment. Models are small local ones (the
environment has no API access); Section 11 states the limit.

Resumable: every response is checkpointed to the output JSON.
"""
from __future__ import annotations

import csv
import importlib
import json
import os
import random
import re
import sys
import time
import urllib.request
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import attackdrift as ad  # noqa: E402

rc = importlib.import_module("34_real_classifier")

OUT = Path(__file__).resolve().parents[1] / "data" / "results"
TABLES = Path(__file__).resolve().parents[1] / "paper" / "tables"
CKPT = OUT / "e24_llm_extractor.json"
OLLAMA = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
MODELS = os.environ.get("E24_MODELS", "gemma3:4b,llama3.2:3b").split(",")
SEED = 20260912
DOMAIN = "enterprise-attack"
N_TRAM, N_RCATT, RCATT_CHARS = 150, 50, 6000
N_SENS = 60  # items for the paraphrase-sensitivity check
NUM_PREDICT = 120
TID = re.compile(r"\bT\d{4}(?:\.\d{3})?\b")

SYSTEM = ("You are a cyber threat intelligence analyst. Map the text to MITRE ATT&CK "
          "Enterprise technique identifiers{release}. Answer with a JSON array of at most "
          "five technique IDs (for example [\"T1059.001\", \"T1053\"]) and nothing else.")
RELEASE_CLAUSE = {
    "unspecified": "",
    "latest": " from the current ATT&CK release, v19.2",
    "era_pinned": " from ATT&CK release v{gold}",
    "legacy_pinned": " from ATT&CK release v6.3 (the vocabulary before sub-techniques existed)",
}
PARAPHRASES = [
    "Identify the MITRE ATT&CK Enterprise techniques described in the following text. Return only a JSON list of up to five technique IDs.",
    "Which ATT&CK Enterprise technique IDs does this text describe? Reply with a JSON array of at most five IDs and no explanation.",
]


# ----------------------------------------------------------------------
# data
# ----------------------------------------------------------------------

def items() -> list[dict]:
    rng = random.Random(SEED)
    out = []
    tram = rc.load_tram()
    for i in sorted(rng.sample(range(len(tram)), N_TRAM)):
        out.append({"gold_set": "tram", "gold_release": "13.0", "idx": i,
                    "text": tram[i][0], "gold": sorted(tram[i][1])})
    for i, (t, g) in enumerate(rc.load_ctibench()):
        out.append({"gold_set": "ctibench", "gold_release": "14.0", "idx": i,
                    "text": t, "gold": sorted(g)})
    rca = rc.load_rcatt()
    for i in sorted(rng.sample(range(len(rca)), N_RCATT)):
        out.append({"gold_set": "rcatt", "gold_release": "6.3", "idx": i,
                    "text": rca[i][0][:RCATT_CHARS], "gold": sorted(rca[i][1])})
    return out


# ----------------------------------------------------------------------
# ollama
# ----------------------------------------------------------------------

def chat(model: str, system: str, user: str) -> dict:
    body = {"model": model, "stream": False,
            "options": {"temperature": 0, "seed": SEED, "num_predict": NUM_PREDICT},
            "messages": [{"role": "system", "content": system},
                         {"role": "user", "content": user}]}
    req = urllib.request.Request(f"{OLLAMA}/api/chat", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                d = json.load(r)
            return {"content": d["message"]["content"], "eval_count": d.get("eval_count"),
                    "ms": d.get("total_duration", 0) / 1e6}
        except Exception as e:  # noqa: BLE001
            if attempt == 2:
                return {"content": "", "error": repr(e)[:200]}
            time.sleep(5)


def digest(model: str) -> str | None:
    """The model's content digest from /api/tags — the version pin of the experiment."""
    try:
        with urllib.request.urlopen(f"{OLLAMA}/api/tags", timeout=60) as r:
            d = json.load(r)
        for m in d.get("models", []):
            if m.get("name") == model or m.get("model") == model:
                return (m.get("digest") or "")[:12] or None
    except Exception:  # noqa: BLE001
        return None
    return None


# ----------------------------------------------------------------------
# classification of emitted identifiers
# ----------------------------------------------------------------------

class Vocab:
    def __init__(self, con):
        self.rels = ad.releases(con, DOMAIN)
        self.live: dict[str, set[str]] = {}
        self.present: dict[str, set[str]] = {}
        for r in self.rels:
            s = ad.load_snapshot(con, DOMAIN, r.version)
            self.live[r.version] = s.live_tech()
            self.present[r.version] = set(s.tech)
        self.newest_v = self.rels[-1].version
        self.newest = ad.load_snapshot(con, DOMAIN, self.newest_v)
        self.ever_live = set().union(*self.live.values())
        self.other = set()
        for dom in ("mobile-attack", "ics-attack"):
            for r in ad.releases(con, dom):
                self.other |= set(ad.load_snapshot(con, dom, r.version).tech)
        self.rev = self.newest.revoked_by()

    def classify(self, tid: str) -> str:
        if tid in self.live[self.newest_v]:
            return "live"
        if tid in self.ever_live:
            term = ad.resolve_chain(tid, self.rev)
            return "stale_resolvable" if term in self.live[self.newest_v] else "stale_unresolvable"
        if tid in self.other:
            return "fabricated_other_domain"
        return "fabricated"

    def home_release(self, ids: set[str]) -> dict:
        if not ids:
            return {}
        shares = {r.version: len(ids & self.live[r.version]) / len(ids) for r in self.rels}
        best = max(shares.items(), key=lambda kv: (kv[1], self.rels.index(next(x for x in self.rels if x.version == kv[0]))))
        consistent = [v for v, s in shares.items() if s == 1.0]
        return {"best_fit_release": best[0], "best_fit_share": best[1],
                "share_by_release": shares,
                "fully_consistent_releases": consistent}


def parse_ids(content: str) -> list[str]:
    seen, out = set(), []
    for t in TID.findall(content or ""):
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out[:10]


# ----------------------------------------------------------------------
# run
# ----------------------------------------------------------------------

def load_ckpt() -> dict:
    if CKPT.exists():
        return json.loads(CKPT.read_text())
    return {"seed": SEED, "num_predict": NUM_PREDICT, "models": {}, "responses": {}}


def save_ckpt(d: dict) -> None:
    CKPT.write_text(json.dumps(d, indent=1))


def main() -> None:
    con = ad.connect()
    vocab = Vocab(con)
    its = items()
    ck = load_ckpt()
    ck["items"] = [{k: v for k, v in it.items() if k != "text"} | {"chars": len(it["text"])} for it in its]
    ck["prompts"] = {"system": SYSTEM, "release_clause": RELEASE_CLAUSE, "paraphrases": PARAPHRASES}
    for m in MODELS:
        ck["models"].setdefault(m, {"digest": digest(m)})
    save_ckpt(ck)

    jobs = []
    for m in MODELS:
        for cond in RELEASE_CLAUSE:
            for j, it in enumerate(its):
                jobs.append((m, cond, "p0", j))
    sens_model = MODELS[0]
    for pi in (1, 2):
        for j in range(min(N_SENS, N_TRAM)):
            jobs.append((sens_model, "unspecified", f"p{pi}", j))
    todo = [jb for jb in jobs if "|".join(map(str, jb)) not in ck["responses"]]
    print(f"{len(jobs)} calls, {len(todo)} to do", file=sys.stderr)
    t0 = time.time()
    for n, (m, cond, para, j) in enumerate(todo, 1):
        it = its[j]
        if para == "p0":
            system = SYSTEM.format(release=RELEASE_CLAUSE[cond].format(gold=it["gold_release"]))
            user = it["text"]
        else:
            system = PARAPHRASES[int(para[1]) - 1]
            user = it["text"]
        r = chat(m, system, user)
        r["ids"] = parse_ids(r.get("content", ""))
        ck["responses"]["|".join(map(str, (m, cond, para, j)))] = r
        if n % 10 == 0 or n == len(todo):
            save_ckpt(ck)
            el = time.time() - t0
            print(f"  {n}/{len(todo)}  {el/60:.1f} min elapsed, ~{el/n*(len(todo)-n)/60:.0f} min left",
                  file=sys.stderr)
    save_ckpt(ck)
    analyse(ck, its, vocab)


def analyse(ck: dict, its: list[dict], vocab: Vocab) -> None:
    for m in MODELS:
        ck.setdefault("models", {}).setdefault(m, {})["digest"] = digest(m)
    res = {"reference_release": vocab.newest_v, "by_model_condition": {}, "sensitivity": {}}
    rng = np.random.default_rng(SEED)

    def score(preds, golds, proj=None):
        if proj:
            preds = [proj(set(p)) for p in preds]
            golds = [proj(set(g)) for g in golds]
        c = rc.per_doc_counts([set(p) for p in preds], [set(g) for g in golds])
        return {"micro_f1": rc.micro_f1(c), "sample_f1": float(c["sample_f1"].mean()), "_c": c}

    def norm(ids):
        return ad.normalize(ids, vocab.newest)

    for m in MODELS:
        for cond in RELEASE_CLAUSE:
            keyed = {}
            for j, it in enumerate(its):
                r = ck["responses"].get("|".join(map(str, (m, cond, "p0", j))))
                if r is not None:
                    keyed[j] = r
            if not keyed:
                continue
            entry = {"n_items": len(keyed), "errors": sum(1 for r in keyed.values() if r.get("error")),
                     "by_gold_set": {}}
            all_ids = Counter()
            for j, r in keyed.items():
                for t in r["ids"]:
                    all_ids[t] += 1
            cls_inst = Counter()
            for t, k in all_ids.items():
                cls_inst[vocab.classify(t)] += k
            n_inst = sum(cls_inst.values())
            distinct = set(all_ids)
            cls_dist = Counter(vocab.classify(t) for t in distinct)
            entry["emitted_instances"] = n_inst
            entry["emitted_distinct"] = len(distinct)
            entry["class_share_instances"] = {k: v / n_inst for k, v in cls_inst.items()} if n_inst else {}
            entry["class_count_distinct"] = dict(cls_dist)
            entry["empty_responses"] = sum(1 for r in keyed.values() if not r["ids"])
            entry["home_release"] = vocab.home_release(distinct)
            # ledger of projecting the emitted stale identifiers
            led = ad.normalize_with_ledger(distinct, vocab.newest)
            entry["ledger_distinct"] = led.summary()
            entry["stale_examples"] = sorted(t for t in distinct if vocab.classify(t).startswith("stale"))[:15]
            entry["fabricated_examples"] = sorted(t for t in distinct if vocab.classify(t) == "fabricated")[:15]
            for gs in ("tram", "ctibench", "rcatt"):
                idx = [j for j in keyed if its[j]["gold_set"] == gs]
                if not idx:
                    continue
                preds = [keyed[j]["ids"] for j in idx]
                golds = [its[j]["gold"] for j in idx]
                naive, normd = score(preds, golds), score(preds, golds, norm)
                # gold-era validity of emitted ids: live at the gold release?
                gold_rel = its[idx[0]]["gold_release"]
                em = Counter(t for p in preds for t in p)
                live_at_gold = sum(k for t, k in em.items() if t in vocab.live[gold_rel]) / max(sum(em.values()), 1)
                d = normd["_c"]["sample_f1"] - naive["_c"]["sample_f1"]
                boots = [float(rng.choice(d, len(d)).mean()) for _ in range(2000)] if len(d) > 1 else [0.0]
                entry["by_gold_set"][gs] = {
                    "n": len(idx), "gold_release": gold_rel,
                    "naive": {k: v for k, v in naive.items() if k != "_c"},
                    "normalized": {k: v for k, v in normd.items() if k != "_c"},
                    "norm_gain_sample_f1": float(d.mean()),
                    "norm_gain_ci": [float(np.quantile(boots, 0.025)), float(np.quantile(boots, 0.975))],
                    "emitted_share_live_at_gold_release": live_at_gold,
                    "items_pass_naive": int((naive["_c"]["sample_f1"] >= 0.5).sum()),
                    "items_pass_normalized": int((normd["_c"]["sample_f1"] >= 0.5).sum()),
                }
            res["by_model_condition"][f"{m}|{cond}"] = entry

    # paraphrase sensitivity: unspecified condition, first model, TRAM subset
    m = MODELS[0]
    sens = {}
    for para in ("p0", "p1", "p2"):
        ids_all, keyed = Counter(), {}
        for j in range(min(N_SENS, N_TRAM)):
            r = ck["responses"].get("|".join(map(str, (m, "unspecified", para, j))))
            if r is not None:
                keyed[j] = r
                for t in r["ids"]:
                    ids_all[t] += 1
        if not keyed:
            continue
        n = sum(ids_all.values())
        cls = Counter()
        for t, k in ids_all.items():
            cls[vocab.classify(t)] += k
        sc = score([keyed[j]["ids"] for j in keyed], [its[j]["gold"] for j in keyed])
        sens[para] = {"n_items": len(keyed), "stale_share": (cls["stale_resolvable"] + cls["stale_unresolvable"]) / n if n else None,
                      "fabricated_share": (cls["fabricated"] + cls["fabricated_other_domain"]) / n if n else None,
                      "live_share": cls["live"] / n if n else None, "micro_f1_naive": sc["micro_f1"]}
    res["sensitivity"] = {"model": m, "condition": "unspecified", "by_prompt": sens}
    ck["results"] = res
    save_ckpt(ck)
    write_table(res, ck)
    for k, e in res["by_model_condition"].items():
        cs = e["class_share_instances"]
        print(f"  {k:28s} live {cs.get('live',0):.2f} stale {cs.get('stale_resolvable',0)+cs.get('stale_unresolvable',0):.2f} "
              f"fab {cs.get('fabricated',0)+cs.get('fabricated_other_domain',0):.2f} home v{e['home_release'].get('best_fit_release')}", file=sys.stderr)


def write_table(res: dict, ck: dict) -> None:
    L = ["| Model (digest) | Prompt condition | Emitted IDs (distinct) | Live at v19.2 | Stale, resolvable | Stale, unresolvable | Fabricated | Other-domain | Home release (share live) |",
         "|---|---|---|---|---|---|---|---|---|"]
    for k, e in res["by_model_condition"].items():
        m, cond = k.split("|")
        dg = (ck["models"].get(m, {}).get("digest") or "")[:12]
        cs = e["class_share_instances"]
        hr = e["home_release"]
        L.append(f"| {m} ({dg}) | {cond} | {e['emitted_instances']} ({e['emitted_distinct']}) | {cs.get('live',0):.3f} | "
                 f"{cs.get('stale_resolvable',0):.3f} | {cs.get('stale_unresolvable',0):.3f} | {cs.get('fabricated',0):.3f} | "
                 f"{cs.get('fabricated_other_domain',0):.3f} | v{hr.get('best_fit_release')} ({hr.get('best_fit_share',0):.2f}) |")
    L += ["", "| Model | Condition | Gold set (release, n) | Emitted share live at gold release | micro-F1 naive | micro-F1 normalized | sample-F1 naive → normalized | Gain [95% CI] | Items passing naive → normalized |",
          "|---|---|---|---|---|---|---|---|---|"]
    for k, e in res["by_model_condition"].items():
        m, cond = k.split("|")
        for gs, g in e["by_gold_set"].items():
            L.append(f"| {m} | {cond} | {gs} (v{g['gold_release']}, {g['n']}) | {g['emitted_share_live_at_gold_release']:.3f} | "
                     f"{g['naive']['micro_f1']:.3f} | {g['normalized']['micro_f1']:.3f} | {g['naive']['sample_f1']:.3f} → {g['normalized']['sample_f1']:.3f} | "
                     f"{g['norm_gain_sample_f1']:+.3f} [{g['norm_gain_ci'][0]:+.3f}, {g['norm_gain_ci'][1]:+.3f}] | {g['items_pass_naive']} → {g['items_pass_normalized']} |")
    s = res.get("sensitivity", {}).get("by_prompt", {})
    if s:
        L += ["", f"Prompt sensitivity ({res['sensitivity']['model']}, unspecified condition, TRAM subset):", "",
              "| Prompt | n | Live share | Stale share | Fabricated share | micro-F1 naive |", "|---|---|---|---|---|---|"]
        for p, v in s.items():
            L.append(f"| {p} | {v['n_items']} | {v['live_share']:.3f} | {v['stale_share']:.3f} | {v['fabricated_share']:.3f} | {v['micro_f1_naive']:.3f} |")
    (TABLES / "t28_llm_extractor.md").write_text("\n".join(L) + "\n")
    print("  wrote", TABLES / "t28_llm_extractor.md", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--analyse":
        con = ad.connect()
        ck = load_ckpt()
        analyse(ck, items(), Vocab(con))
    else:
        main()
