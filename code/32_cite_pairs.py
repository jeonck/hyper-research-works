#!/usr/bin/env python3
"""Extract every (sentence, citation) pair from the manuscript for verification.

The packaged extractor expects a different citation convention, so the pairs are
built here against this manuscript's own numbering: each [N] marker is resolved
through the canonical registry to the vault note it names, and the sentence
carrying it is recorded. Pairs whose sentence carries a number are flagged, since
a numeric claim attributed to a source is the binding most worth checking.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAG = "attack-ontology-drift-cti-85bc51"
REPORT = ROOT / "research" / "notes" / f"final_report_{TAG}.md"
REGISTRY = ROOT / "research" / "runs" / TAG / "temp" / "reference-registry.json"
OUT = ROOT / "research" / "runs" / TAG / "cite-check-pairs.json"

CITE = re.compile(r"\[(\d+(?:\s*,\s*\d+)*)\]")
SENT = re.compile(r"(?<=[.!?])\s+(?=[A-Z(])")
HAS_NUMBER = re.compile(r"\d")


def main() -> int:
    text = REPORT.read_text()
    body = text.split("\n## Sources", 1)[0]
    registry = {e["n"]: e for e in json.loads(REGISTRY.read_text())}

    pairs, dangling = [], []
    section = ""
    for para in body.split("\n\n"):
        if para.startswith("## "):
            section = para.strip()
            continue
        if para.startswith("|") or para.startswith("**Table"):
            continue
        for sentence in SENT.split(para.replace("\n", " ")):
            nums = [int(n) for m in CITE.findall(sentence)
                    for n in re.split(r"\s*,\s*", m)]
            for n in nums:
                entry = registry.get(n)
                if entry is None:
                    dangling.append({"citation": n, "sentence": sentence.strip()})
                    continue
                pairs.append({
                    "citation": n,
                    "note_id": entry["id"],
                    "source_title": entry["title"],
                    "source_url": entry.get("url"),
                    "tier": entry.get("tier"),
                    "section": section,
                    "sentence": sentence.strip(),
                    "number_bearing": bool(HAS_NUMBER.search(
                        CITE.sub("", sentence))),
                })
    summary = {
        "total": len(pairs),
        "dangling": len(dangling),
        "number_bearing": sum(1 for p in pairs if p["number_bearing"]),
        "distinct_sources": len({p["citation"] for p in pairs}),
    }
    OUT.write_text(json.dumps({"summary": summary, "dangling": dangling,
                               "pairs": pairs}, indent=1))
    print(json.dumps(summary, indent=1))
    if dangling:
        print("DANGLING:", dangling, file=sys.stderr)
    return 0


if __name__ == "__main__":
    main()
