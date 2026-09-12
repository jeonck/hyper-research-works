#!/usr/bin/env python3
"""E17: what normalization actually costs a deployed corpus.

Applies the protocol's residual ledger to each deployed CTI corpus and reports
what a bare set-returning normalizer would have hidden: how many distinct label
classes survive, how many are lost to merges, how many label instances land in
a merged class, how many resolutions change abstraction level, and how many
identifiers have no live successor at all.
"""
from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import attackdrift as ad  # noqa: E402

artifacts = importlib.import_module("06_artifacts")
OUT = Path(__file__).resolve().parents[1] / "data" / "results"
DOMAINS = ["enterprise-attack", "mobile-attack", "ics-attack"]


def main() -> None:
    con = ad.connect()
    newest = {}
    for dom in DOMAINS:
        rels = ad.releases(con, dom)
        newest[dom] = ad.load_snapshot(con, dom, rels[-1].version)

    rows = {}
    for name, loader in artifacts.CORPORA.items():
        counts = loader()
        if not counts:
            continue
        # group identifiers by the domain the corpus declares, defaulting to the
        # domain in which the identifier is live
        per_domain: dict[str, set[str]] = {d: set() for d in DOMAINS}
        for (dom, tid), _ in counts.items():
            if dom in per_domain:
                per_domain[dom].add(tid)
            else:
                placed = next((d for d in DOMAINS if tid in newest[d].live_tech()
                               or tid in newest[d].tech), "enterprise-attack")
                per_domain[placed].add(tid)

        kept = merged_targets = absorbed = dropped = demoted = 0
        distinct_after: set[tuple[str, str]] = set()
        merge_map: dict[tuple[str, str], list[str]] = {}
        for dom, ids in per_domain.items():
            if not ids:
                continue
            res = ad.normalize_with_ledger(ids, newest[dom])
            kept += len(res.kept)
            dropped += len(res.dropped)
            demoted += len(res.demoted)
            merged_targets += len(res.merged)
            absorbed += sum(len(v) for v in res.merged.values())
            distinct_after |= {(dom, t) for t in res.ids}
            for tgt, srcs in res.merged.items():
                merge_map[(dom, tgt)] = srcs

        before = sum(len(v) for v in per_domain.values())
        instances_total = sum(counts.values())
        merged_sources = {(d, s) for (d, _t), srcs in merge_map.items() for s in srcs}
        instances_merged = sum(c for k, c in counts.items()
                               if (k[0] or "enterprise-attack", k[1]) in
                               {(d, s) for d, s in merged_sources})
        rows[name] = {
            "labels_before": before,
            "labels_after": len(distinct_after),
            "classes_lost_to_merges": before - dropped - len(distinct_after),
            "kept": kept, "dropped": dropped, "demoted": demoted,
            "merge_targets": merged_targets, "absorbed_by_merges": absorbed,
            "label_instances": instances_total,
            "instances_in_a_merged_class": instances_merged,
            "instances_in_a_merged_class_share":
                instances_merged / instances_total if instances_total else 0.0,
            "largest_merge": max(((t, len(s)) for t, s in merge_map.items()),
                                 key=lambda x: x[1], default=(None, 0)),
        }
        r = rows[name]
        print(f"  {name}: {r['labels_before']} -> {r['labels_after']} distinct classes "
              f"({r['classes_lost_to_merges']} lost to merges, {r['dropped']} dropped, "
              f"{r['demoted']} abstraction changes); "
              f"{r['instances_in_a_merged_class_share']:.4f} of label instances land "
              f"in a merged class", file=sys.stderr)
    (OUT / "e17_ledger_on_corpora.json").write_text(json.dumps(rows, indent=1))
    print(f"wrote {OUT/'e17_ledger_on_corpora.json'}", file=sys.stderr)


if __name__ == "__main__":
    main()
