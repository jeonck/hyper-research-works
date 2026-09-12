#!/usr/bin/env python3
"""Generate the manuscript's Sources section from the canonical registry.

Only entries actually cited in the body are listed, numbered exactly as the
registry numbers them, so a reader following [N] lands where the drafting
process intended. Titles are the registry's own; nothing is re-worded here.
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
CITE = re.compile(r"\[(\d+(?:\s*,\s*\d+)*)\]")


def shorten(title: str, limit: int = 90) -> str:
    title = " ".join(title.split())
    if len(title) <= limit:
        return title
    cut = title[:limit].rsplit(" ", 1)[0]
    return cut.rstrip(" ,;:—-") + "…"


def main() -> int:
    text = REPORT.read_text()
    body = text.split("\n## Sources", 1)[0]
    cited = sorted({int(n) for m in CITE.findall(body)
                    for n in re.split(r"\s*,\s*", m)})
    registry = {e["n"]: e for e in json.loads(REGISTRY.read_text())}
    missing = [n for n in cited if n not in registry]
    if missing:
        print(f"citations with no registry entry: {missing}", file=sys.stderr)
        return 1

    lines = ["", "## Sources", "",
             "Entries are numbered as in this study's reference registry; only entries",
             "cited in the text are listed. Sources marked as read in full were obtained",
             "from local clones of the named repositories; the remainder were reachable",
             "in this environment only through search summaries and are attributed as",
             "reported rather than quoted.", ""]
    for n in cited:
        e = registry[n]
        url = (e.get("url") or "").strip()
        lines.append(f"{n}. {shorten(e['title'])}." + (f" {url}" if url else ""))
    out = "\n".join(lines) + "\n"

    if "\n## Sources" in text:
        text = text.split("\n## Sources", 1)[0]
    REPORT.write_text(text.rstrip() + "\n" + out)
    words = len(out.split())
    print(f"wrote Sources with {len(cited)} entries ({words} words); "
          f"manuscript now {len(REPORT.read_text().split())} words", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
