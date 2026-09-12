#!/usr/bin/env python3
"""E9: do deployed CTI corpora declare which ATT&CK release their labels encode?

A bounded, reproducible check: search each corpus's documentation and
configuration files (depth <= 3, extensions .md/.txt/.cfg/.toml/.yml/.yaml/.json
excluding data and log directories) for any explicit ATT&CK version declaration.
The check is deliberately generous in its patterns and deliberately narrow in
its scope, and the scope is reported with the result.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "data" / "results"
EXT = Path(os.environ.get("HYPER_EXT", "/home/user/ext"))
CORPORA = {"cti-bench": EXT / "cti-bench", "rcATT": EXT / "rcATT", "tram": EXT / "tram"}
SUFFIXES = {".md", ".txt", ".cfg", ".toml", ".yml", ".yaml", ".rst", ".ini"}
SKIP_DIRS = {".git", "logs", "data", "node_modules", "__pycache__"}
PATTERNS = [
    r"att&ck\s*v\s*\d+", r"attack\s*v\s*\d+", r"att&ck\s+version\s*\d*",
    r"version\s+\d+(\.\d+)?\s+of\s+(the\s+)?(mitre\s+)?att", r"enterprise-attack-\d+",
    r"attack[_-]version", r"attck[_-]version", r"x_mitre_version",
]
RX = re.compile("|".join(PATTERNS), re.IGNORECASE)


def main() -> None:
    results = {}
    for name, root in CORPORA.items():
        if not root.exists():
            continue
        scanned, hits = [], []
        for p in root.rglob("*"):
            rel = p.relative_to(root)
            if any(part in SKIP_DIRS for part in rel.parts):
                continue
            if len(rel.parts) > 3 or p.suffix.lower() not in SUFFIXES or not p.is_file():
                continue
            scanned.append(str(rel))
            try:
                text = p.read_text(errors="ignore")
            except OSError:
                continue
            for m in RX.finditer(text):
                line = text[:m.start()].count("\n") + 1
                hits.append({"file": str(rel), "line": line,
                             "match": text[max(0, m.start() - 60):m.end() + 60]
                             .replace("\n", " ")})
        results[name] = {
            "files_scanned": len(scanned),
            "scanned_files": sorted(scanned),
            "declarations_found": len(hits),
            "hits": hits[:20],
        }
        print(f"  {name}: {len(scanned)} documentation files scanned, "
              f"{len(hits)} ATT&CK-version declarations found", file=sys.stderr)
    (OUT / "e9_version_declaration.json").write_text(json.dumps(results, indent=1))
    print(f"wrote {OUT/'e9_version_declaration.json'}", file=sys.stderr)


if __name__ == "__main__":
    main()
