#!/usr/bin/env python3
"""Check that every number in the manuscript traces to a computed result.

The paper's thesis is that CTI claims should carry their provenance. The same
discipline is applied to the paper: each decimal or percentage in the prose is
searched for in the study's own result files and tables. Anything not found is
listed for a human to justify or remove — the check is deliberately noisy on
the side of flagging, since a false flag costs a glance and a missed one costs
a wrong number in print.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAG = "attack-ontology-drift-cti-85bc51"
REPORT = ROOT / "research" / "notes" / f"final_report_{TAG}.md"
RESULTS = ROOT / "data" / "results"
TABLES = ROOT / "paper" / "tables"

NUM = re.compile(r"(?<![\w.])(\d+\.\d+|\d{2,})(?![\w])")
# numbers that are structural rather than measured
IGNORE_CONTEXT = re.compile(
    r"(Table|Figure|Section|v\d|ATT&CK v|\[\d|20\d\d|T\d{4}|TA\d{4}|S\d{4})", re.I)


def haystack() -> set[str]:
    """Every number that appears anywhere in the computed results or tables."""
    out: set[str] = set()

    def harvest(text: str) -> None:
        for m in re.finditer(r"-?\d+(?:\.\d+)?", text):
            v = m.group(0).lstrip("-")
            out.add(v)
            try:
                f = float(v)
            except ValueError:
                continue
            # the prose may round, scale to a percentage, or drop a trailing zero
            for cand in (f, f * 100, f / 100):
                for nd in (0, 1, 2, 3):
                    out.add(f"{cand:.{nd}f}")
                    out.add(f"{cand:.{nd}f}".rstrip("0").rstrip("."))
    for p in sorted(RESULTS.glob("*.json")):
        harvest(p.read_text())
    for p in sorted(TABLES.glob("*.md")):
        harvest(p.read_text())
    return {v for v in out if v}


def main() -> int:
    if not REPORT.exists():
        print("manuscript not written yet", file=sys.stderr)
        return 2
    known = haystack()
    text = REPORT.read_text()
    body = text.split("## Sources", 1)[0]
    unknown: list[tuple[str, str]] = []
    seen: set[str] = set()
    for line in body.splitlines():
        if line.startswith("|"):        # tables are copied from the generators
            continue
        for m in NUM.finditer(line):
            v = m.group(1)
            if v in known or v in seen:
                continue
            ctx = line[max(0, m.start() - 45):m.end() + 45]
            if IGNORE_CONTEXT.search(ctx):
                continue
            seen.add(v)
            unknown.append((v, ctx.strip()))
    print(f"distinct numbers in the results and tables: {len(known)}")
    print(f"numbers in the prose with no match: {len(unknown)}")
    for v, ctx in unknown[:60]:
        print(f"  {v:>10}  ...{ctx}...")
    return 1 if unknown else 0


if __name__ == "__main__":
    sys.exit(main())
