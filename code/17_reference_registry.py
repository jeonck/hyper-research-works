#!/usr/bin/env python3
"""Build one canonical numbered reference list from the vault.

All drafting agents and the synthesizer cite by these numbers, so the final
manuscript's [N] markers resolve consistently no matter which agent wrote the
sentence. Sources are deduplicated by URL; this study's own measurement notes
are grouped first as the primary-artefact block.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HPR = str(ROOT / ".venv" / "bin" / "hyperresearch")
TAG = "attack-ontology-drift-cti-85bc51"
OUT = ROOT / "research" / "runs" / TAG / "temp" / "reference-registry.md"

TIER_RANK = {"ground_truth": 0, "institutional": 1, "practitioner": 2, "community": 3}


def main() -> None:
    raw = subprocess.run([HPR, "note", "list", "--tag", TAG, "--all", "-j"],
                         cwd=ROOT, capture_output=True, text=True, check=True).stdout
    listed = json.loads(raw)["data"]
    # `note list` omits the source URL; `note show` carries it and accepts batches
    notes = []
    ids = [n["id"] for n in listed]
    for i in range(0, len(ids), 20):
        chunk = ids[i:i + 20]
        out = subprocess.run([HPR, "note", "show", *chunk, "-j"],
                             cwd=ROOT, capture_output=True, text=True, check=True).stdout
        data = json.loads(out)["data"]
        if isinstance(data, dict):
            data = data.get("notes", [data])
        for d in data:
            rec = {k: d.get(k) for k in
                   ("id", "title", "source", "tier", "content_type", "summary")}
            rec["tags"] = d.get("tags") or []
            notes.append(rec)
    # This study's own measurement notes are not external references: they are
    # cited in the manuscript as its own tables and sections. Keep them in a
    # separate index so a drafter never turns "our Table 3" into a citation.
    internal = [n for n in notes
                if {"measurement", "methodology"} & set(n.get("tags") or [])]
    external = [n for n in notes if n not in internal]

    by_url: dict[str, dict] = {}
    for n in external:
        url = (n.get("source") or "").strip()
        if not n.get("id"):
            continue
        key = url or f"note:{n['id']}"
        cur = by_url.get(key)
        rank = TIER_RANK.get(n.get("tier") or "community", 4)
        if cur is None or rank < cur["_rank"]:
            by_url[key] = {"id": n["id"], "title": (n.get("title") or n["id"] or "").strip() or n["id"],
                           "url": url, "tier": n.get("tier") or "community",
                           "summary": (n.get("summary") or "").strip(),
                           "content_type": n.get("content_type") or "",
                           "_rank": rank}
    entries = sorted(by_url.values(), key=lambda e: (e["_rank"], e["title"].lower()))

    lines = ["# Canonical reference registry — " + TAG, "",
             "Cite by the number in the left column. Do not renumber, do not invent",
             "entries, do not cite a number that is not in this table. An assertion that",
             "no entry supports must be written as an assertion of this study's own",
             "measurement, citing the measurement note, or not made at all.", "",
             "| # | Tier | Title | URL |", "|---|---|---|---|"]
    registry = []
    for i, e in enumerate(entries, 1):
        lines.append(f"| {i} | {e['tier']} | {e['title'][:110]} | {e['url']} |")
        registry.append({"n": i, **{k: v for k, v in e.items() if k != "_rank"}})
    lines += ["", "## This study's own evidence — cite as our tables and sections, never as [N]",
              "", "| Note | Backing results file |", "|---|---|"]
    for n in sorted(internal, key=lambda x: (x.get("title") or "").lower()):
        lines.append(f"| {n.get('title')} | data/results/ |")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n")
    (OUT.parent / "reference-registry.json").write_text(json.dumps(registry, indent=1))
    print(f"wrote {OUT} with {len(entries)} entries")
    counts: dict[str, int] = {}
    for e in entries:
        counts[e["tier"]] = counts.get(e["tier"], 0) + 1
    print("  by tier:", counts)


if __name__ == "__main__":
    main()
