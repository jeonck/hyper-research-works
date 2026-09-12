#!/usr/bin/env python3
"""E7: label validity and version provenance of real, widely used CTI artefacts.

Corpora (all public, all consumed by published work):
  ctibench-ate    CTIBench CTI-ATE gold technique labels (NeurIPS'24 benchmark)
  rcatt           rcATT training corpus (pre-sub-technique tooling, 2019)
  tram-bootstrap  TRAM bootstrap training data
  tram2           TRAM 2 multi-label training data

Identifier validity is evaluated **per ATT&CK domain**: an identifier counts as
valid in a release if it is live in the domain the artefact assigns to it, or —
when the artefact declares no domain — in any of Enterprise, Mobile or ICS.

Outputs per corpus
  * per-release validity curve (share of distinct identifiers that are live)
  * provenance interval: releases in which *every* identifier is simultaneously
    live; an empty interval means the artefact mixes mutually exclusive
    vocabularies and can be attributed to no single release
  * repair achieved by ATT&CK-Norm against the newest release
"""
from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import attackdrift as ad  # noqa: E402

csv.field_size_limit(10_000_000)

OUT = Path(__file__).resolve().parents[1] / "data" / "results"
EXT = Path("/home/user/ext")
DOMAINS = ["enterprise-attack", "mobile-attack", "ics-attack"]
TID = re.compile(r"\bT\d{4}(?:\.\d{3})?\b")
PLATFORM_DOMAIN = {"enterprise": "enterprise-attack", "mobile": "mobile-attack",
                   "ics": "ics-attack"}


def load_ctibench() -> Counter:
    """(domain, technique_id) -> label count; domain taken from the Platform column."""
    c: Counter = Counter()
    p = EXT / "cti-bench/data/cti-ate.tsv"
    for row in csv.DictReader(p.open(), delimiter="\t"):
        dom = PLATFORM_DOMAIN.get((row.get("Platform") or "").strip().lower())
        for tid in TID.findall(row.get("GT") or ""):
            c[(dom, tid)] += 1
    return c


def load_rcatt() -> Counter:
    c: Counter = Counter()
    p = EXT / "rcATT/classification_tools/data/training_data_original.csv"
    with p.open() as fh:
        reader = csv.reader(fh)
        header = next(reader)
        cols = [(i, h.strip('"')) for i, h in enumerate(header) if TID.fullmatch(h.strip('"'))]
        for row in reader:
            for i, tid in cols:
                if i < len(row) and row[i].strip().strip('"') in {"1", "1.0"}:
                    c[(None, tid)] += 1
    return c


def load_tram_bootstrap() -> Counter:
    c: Counter = Counter()
    for name in ("training/bootstrap-training-data.json",
                 "training/attack_may_2023_merged_bootstrap_data2.json"):
        p = EXT / "tram/data" / name
        if not p.exists():
            continue
        for s in json.loads(p.read_text()).get("sentences", []):
            for m in s.get("mappings", []) or []:
                if m.get("attack_id") and TID.fullmatch(m["attack_id"]):
                    c[(None, m["attack_id"])] += 1
    return c


def load_tram2() -> Counter:
    c: Counter = Counter()
    p = EXT / "tram/data/tram2-data/multi_label.json"
    if not p.exists():
        return c
    for rec in json.loads(p.read_text()):
        for lab in rec.get("labels") or []:
            for tid in TID.findall(str(lab)):
                c[(None, tid)] += 1
    return c


CORPORA = {
    "ctibench-ate": load_ctibench,
    "rcatt": load_rcatt,
    "tram-bootstrap": load_tram_bootstrap,
    "tram2": load_tram2,
}


def main() -> None:
    con = ad.connect()
    rel_list = {d: ad.releases(con, d) for d in DOMAINS}
    snaps = {d: {r.version: ad.load_snapshot(con, d, r.version) for r in rel_list[d]}
             for d in DOMAINS}
    live = {d: {v: s.live_tech() for v, s in snaps[d].items()} for d in DOMAINS}
    present = {d: {v: set(s.tech) for v, s in snaps[d].items()} for d in DOMAINS}
    # enterprise release list drives the timeline; other domains are matched by version
    timeline = rel_list["enterprise-attack"]
    newest = timeline[-1]

    def domains_for(dom: str | None) -> list[str]:
        return [dom] if dom else DOMAINS

    # Mobile and ICS do not publish every Enterprise version number; align each
    # timeline point to the most recent release each domain actually shipped.
    def _key(v: str) -> tuple:
        return tuple(int(x) for x in v.split("."))

    aligned: dict[str, dict[str, str | None]] = {}
    for d in DOMAINS:
        avail = sorted((r.version for r in rel_list[d]), key=_key)
        aligned[d] = {}
        for r in timeline:
            cands = [v for v in avail if _key(v) <= _key(r.version)]
            aligned[d][r.version] = cands[-1] if cands else None

    def is_live(dom: str | None, tid: str, version: str) -> bool:
        for d in domains_for(dom):
            av = aligned[d].get(version)
            if av and tid in live[d][av]:
                return True
        return False

    def is_present(dom: str | None, tid: str, version: str) -> bool:
        for d in domains_for(dom):
            av = aligned[d].get(version)
            if av and tid in present[d][av]:
                return True
        return False

    results = {}
    for name, loader in CORPORA.items():
        counts = loader()
        keys = set(counts)
        if not keys:
            print(f"  {name}: no identifiers, skipping", file=sys.stderr)
            continue
        by_domain: dict[str | None, set[str]] = defaultdict(set)
        for dom, tid in keys:
            by_domain[dom].add(tid)

        curve = []
        for r in timeline:
            n_live = sum(1 for dom, tid in keys if is_live(dom, tid, r.version))
            n_present = sum(1 for dom, tid in keys if is_present(dom, tid, r.version))
            curve.append({"version": r.version, "date": r.date,
                          "live": n_live, "present": n_present,
                          "live_frac": n_live / len(keys),
                          "unknown": len(keys) - n_present})
        best = max(curve, key=lambda c: c["live_frac"])
        consistent = [c["version"] for c in curve if c["live"] == len(keys)]

        invalid_now = {(dom, tid) for dom, tid in keys if not is_live(dom, tid, newest.version)}
        repaired = set()
        for dom, tid in invalid_now:
            for d in domains_for(dom):
                av = aligned[d].get(newest.version)
                tgt = snaps[d].get(av) if av else None
                if tgt and ad.resolve_chain(tid, tgt.revoked_by()) in live[d][av]:
                    repaired.add((dom, tid))
                    break
        total_labels = sum(counts.values())
        invalid_labels = sum(counts[k] for k in invalid_now)
        results[name] = {
            "n_unique_ids": len(keys),
            "n_label_instances": total_labels,
            "n_subtechnique_ids": sum(1 for _, t in keys if "." in t),
            "domains_declared": sorted(d for d in by_domain if d),
            "ids_without_declared_domain": len(by_domain.get(None, set())),
            "curve": curve,
            "best_fit_version": best["version"], "best_fit_date": best["date"],
            "best_fit_live_frac": best["live_frac"],
            "fully_consistent_releases": consistent,
            "invalid_at_newest": len(invalid_now),
            "invalid_at_newest_frac": len(invalid_now) / len(keys),
            "invalid_label_instances_frac": invalid_labels / total_labels if total_labels else 0,
            "repairable_by_revocation_chain": len(repaired),
            "unrepairable": len(invalid_now) - len(repaired),
            "newest_version": newest.version, "newest_date": newest.date,
            "examples_invalid": sorted(t for _, t in invalid_now)[:20],
        }
        print(f"  {name}: {len(keys)} ids | best fit v{best['version']} "
              f"({best['live_frac']:.3f}) | consistent releases: "
              f"{len(consistent)} | invalid now {len(invalid_now)} "
              f"({len(repaired)} repairable)", file=sys.stderr)

    (OUT / "e7_artifacts.json").write_text(json.dumps(results, indent=1))
    print(f"wrote {OUT/'e7_artifacts.json'}", file=sys.stderr)


if __name__ == "__main__":
    main()
