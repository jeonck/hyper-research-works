#!/usr/bin/env python3
"""E16: do published ATT&CK coverage layers declare the release they were built against?

Scans every ATT&CK Navigator layer file found in the locally cloned public
repositories, records whether it declares `versions.attack`, and checks each of
its technique annotations for liveness at the newest release. A layer that
declares no version is re-scored by the Navigator against whatever release is
current when it is opened, so its annotations silently change meaning.
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import attackdrift as ad  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "data" / "results"
ROOTS = [Path("/home/user/ext"), Path("/home/user/mitre-attack")]
SKIP = {"node_modules", ".git", "dist", "build", "__pycache__", "site-packages"}
# the same upstream repository is cloned under two names in this workspace;
# scanning both would double-count its sample layers
DUPLICATE_CLONES = {"attack-navigator"}
DOMAIN_MAP = {"enterprise-attack": "enterprise-attack", "mobile-attack": "mobile-attack",
              "ics-attack": "ics-attack"}


def is_layer(d: object) -> bool:
    return (isinstance(d, dict) and isinstance(d.get("techniques"), list)
            and ("domain" in d or "versions" in d) and "name" in d)


def declared_version(d: dict) -> str | None:
    v = d.get("versions")
    if isinstance(v, dict) and v.get("attack"):
        return str(v["attack"])
    # layer formats before 4.0 have no field for it; a bare scalar `version` is
    # the file-schema version, not the ATT&CK release
    return None


def main() -> None:
    con = ad.connect()
    newest = {}
    for dom in DOMAIN_MAP.values():
        rels = ad.releases(con, dom)
        snap = ad.load_snapshot(con, dom, rels[-1].version)
        newest[dom] = {"release": rels[-1].version, "live": snap.live_tech(),
                       "known": set(snap.tech), "rev": snap.revoked_by(), "snap": snap}

    layers, by_repo = [], Counter()
    for root in ROOTS:
        if not root.exists():
            continue
        for p in root.rglob("*.json"):
            if any(part in SKIP for part in p.parts):
                continue
            if p.is_relative_to(root) and p.relative_to(root).parts[0] in DUPLICATE_CLONES:
                continue
            try:
                if p.stat().st_size > 8_000_000:
                    continue
                d = json.loads(p.read_text(errors="ignore"))
            except (OSError, ValueError):
                continue
            if not is_layer(d):
                continue
            dom = DOMAIN_MAP.get(str(d.get("domain") or "enterprise-attack"),
                                 "enterprise-attack")
            ref = newest[dom]
            ids = [t.get("techniqueID") for t in d["techniques"]
                   if isinstance(t, dict) and t.get("techniqueID")]
            dead = [t for t in ids if t not in ref["live"]]
            unknown = [t for t in ids if t not in ref["known"]]
            recoverable = [t for t in dead
                           if ad.resolve_chain(t, ref["rev"]) in ref["live"]]
            repo = p.relative_to(root).parts[0] if p.is_relative_to(root) else str(root)
            by_repo[repo] += 1
            layers.append({
                "path": str(p), "repo": repo, "name": str(d.get("name"))[:80],
                "domain": dom, "layer_format": str(d.get("versions", {}).get("layer")
                                                   or d.get("version") or ""),
                "declares_attack_version": declared_version(d),
                "annotations": len(ids),
                "dead_at_newest": len(dead),
                "unknown_at_newest": len(unknown),
                "recoverable": len(recoverable),
            })

    with_ann = [l for l in layers if l["annotations"] > 0]
    declaring = [l for l in with_ann if l["declares_attack_version"]]
    total_ann = sum(l["annotations"] for l in with_ann)
    total_dead = sum(l["dead_at_newest"] for l in with_ann)
    # MITRE's own fixtures and third-party published layers behave differently
    # enough that the pooled number hides the finding
    groups = {"mitre_repositories": [l for l in with_ann
                                     if l["repo"] in {"navigator", "mitreattack-python"}],
              "third_party": [l for l in with_ann
                              if l["repo"] not in {"navigator", "mitreattack-python"}]}
    by_group = {}
    for gname, g in groups.items():
        ann = sum(l["annotations"] for l in g)
        dead = sum(l["dead_at_newest"] for l in g)
        by_group[gname] = {
            "layers": len(g),
            "declaring": sum(1 for l in g if l["declares_attack_version"]),
            "annotations": ann, "dead": dead,
            "dead_share": dead / ann if ann else 0.0,
        }

    summary = {
        "layers_found": len(layers),
        "layers_with_annotations": len(with_ann),
        "layers_declaring_attack_version": len(declaring),
        "declaring_share": len(declaring) / len(with_ann) if with_ann else 0.0,
        "declared_values": sorted({l["declares_attack_version"] for l in declaring}),
        "annotations_total": total_ann,
        "annotations_dead_at_newest": total_dead,
        "dead_share": total_dead / total_ann if total_ann else 0.0,
        "layers_with_at_least_one_dead": sum(1 for l in with_ann if l["dead_at_newest"]),
        "annotations_recoverable": sum(l["recoverable"] for l in with_ann),
        "newest_releases": {d: r["release"] for d, r in newest.items()},
        "by_repository": dict(by_repo),
        "by_group": by_group,
    }
    (OUT / "e16_layer_adoption.json").write_text(
        json.dumps({"summary": summary, "layers": layers}, indent=1))
    for gname, g in by_group.items():
        print(f"  {gname}: {g['layers']} layers, {g['declaring']} declaring, "
              f"{g['dead']}/{g['annotations']} dead ({g['dead_share']:.3f})", file=sys.stderr)
    for k, v in summary.items():
        print(f"  {k}: {v}", file=sys.stderr)
    print(f"wrote {OUT/'e16_layer_adoption.json'}", file=sys.stderr)


if __name__ == "__main__":
    main()
