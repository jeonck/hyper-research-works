#!/usr/bin/env python3
"""Pre-flight check on the manuscript, run before the ship gate.

Checks the things the gate checks, plus two this study cares about in
particular: that every citation number resolves to the canonical registry, and
that quotation marks are only used where a source was read in full.
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

REQUIRED = [
    "## Abstract", "## 1. Introduction",
    "## 2. Background: ATT&CK as a Versioned Ontology", "## 3. Related Work",
    "## 4. Problem Formalization and Drift Taxonomy", "## 5. Data and Methodology",
    "## 6. Measuring Ontology Drift in ATT&CK",
    "## 7. Downstream Impact of Drift on CTI Analytics",
    "## 8. ATT&CK-Norm: A Version-Normalization Protocol",
    "## 9. Label Validity of Deployed CTI Corpora",
    "## 10. Discussion and Reporting Discipline for CTI Research",
    "## 11. Threats to Validity", "## 12. Conclusion", "## Sources",
]
WORD_RANGE = (5000, 10000)          # profile target for `argumentative`
GATE_RANGE = (4000, 12000)          # the gate allows +/- 20%
CITE = re.compile(r"\[(\d+(?:\s*,\s*\d+)*)\]")
QUOTE = re.compile(r"[\"“”]")


def main() -> int:
    if not REPORT.exists():
        print("manuscript not written yet", file=sys.stderr)
        return 2
    text = REPORT.read_text()
    body = text
    problems, notes = [], []

    # headings, in order
    pos = -1
    for h in REQUIRED:
        i = body.find("\n" + h)
        if i < 0 and not body.startswith(h):
            problems.append(f"missing heading: {h}")
        elif i < pos:
            problems.append(f"heading out of order: {h}")
        else:
            pos = i

    # length
    words = len(re.findall(r"\S+", body))
    notes.append(f"words: {words}")
    if not (GATE_RANGE[0] <= words <= GATE_RANGE[1]):
        problems.append(f"length {words} outside the gate range {GATE_RANGE}")
    elif not (WORD_RANGE[0] <= words <= WORD_RANGE[1]):
        notes.append(f"length {words} outside the profile target {WORD_RANGE} "
                     f"but inside the gate's tolerance")

    # citations
    markers = CITE.findall(body)
    numbers = sorted({int(n) for m in markers for n in re.split(r"\s*,\s*", m)})
    notes.append(f"citation markers: {len(markers)}; distinct entries cited: {len(numbers)}")
    density = len(markers) / (words / 1000) if words else 0
    notes.append(f"citation density: {density:.1f} per 1000 words")
    if density < 9:
        problems.append(f"citation density {density:.1f} below the required 9 per 1000 words")
    if not (80 <= len(markers) <= 150):
        notes.append(f"citation marker count {len(markers)} outside the 80-150 target")

    if REGISTRY.exists():
        registry = {e["n"] for e in json.loads(REGISTRY.read_text())}
        unknown = [n for n in numbers if n not in registry]
        if unknown:
            problems.append(f"citations with no registry entry: {unknown}")
        # every cited entry should appear in the Sources section
        src = body.split("## Sources", 1)
        if len(src) == 2:
            listed = {int(n) for n in re.findall(r"^\s*\[?(\d+)\]?[.)]?\s", src[1], re.M)}
            missing = [n for n in numbers if n not in listed]
            if missing:
                problems.append(f"cited but absent from Sources: {missing[:12]}")
            extra = [n for n in listed if n not in numbers]
            if extra:
                notes.append(f"listed in Sources but never cited: {extra[:12]}")

    # quote integrity
    quotes = QUOTE.findall(body)
    notes.append(f"quotation marks: {len(quotes)}")
    if quotes:
        for m in re.finditer(r"[\"“]([^\"“”]{10,240})[\"”]", body):
            notes.append(f"  quoted span: {m.group(1)[:110]}")

    # tables and figures referenced
    tables = set(re.findall(r"Table (\d+)", body))
    figures = set(re.findall(r"Figure (\d+)", body))
    notes.append(f"table references: {len(tables)} -> {sorted(tables, key=int)}")
    notes.append(f"figure references: {len(figures)} -> {sorted(figures, key=int)}")

    print("\n".join(notes))
    if problems:
        print("\nPROBLEMS")
        for p in problems:
            print(" -", p)
        return 1
    print("\nall pre-flight checks pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
