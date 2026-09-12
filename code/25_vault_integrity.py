#!/usr/bin/env python3
"""Corpus integrity check: does each note's body actually belong to its title?

A width-sweep agent can write a note whose front matter names one source and
whose body describes another. A drafter would then attribute the wrong content
to the wrong source, which is exactly the failure this paper is about, so the
corpus is checked before anything is drafted.

Flags a note when the content-bearing tokens of its title barely appear in its
body, and when the body names a different source URL than the front matter.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HPR = str(ROOT / ".venv" / "bin" / "hyperresearch")
TAG = "attack-ontology-drift-cti-85bc51"
OUT = ROOT / "data" / "results" / "e15_vault_integrity.json"

WORD = re.compile(r"[a-z0-9&.]+")
STOP = set("""the a an and or of for to in on with as is are was were be been it its
this that these those from by at into over under how what why which who when where
not no but if then than so such can could may might will would should must about
using use used via across between within without more most less least new old
attack att&ck mitre note notes paper study report data""".split())
BOILER = re.compile(r"<untrusted-source[^>]*>|\[NOTE TO READER:.*?\]", re.S)
URL = re.compile(r"https?://[^\s)>\]]+")


def content_tokens(text: str) -> set[str]:
    return {t for t in WORD.findall((text or "").lower()) if t not in STOP and len(t) > 2}


def host(url: str) -> str:
    m = re.match(r"https?://([^/]+)", url or "")
    return m.group(1).lower().removeprefix("www.") if m else ""


def main() -> None:
    listed = json.loads(subprocess.run(
        [HPR, "note", "list", "--tag", TAG, "--all", "-j"],
        cwd=ROOT, capture_output=True, text=True, check=True).stdout)["data"]
    ids = [n["id"] for n in listed]
    flagged, checked = [], 0
    for i in range(0, len(ids), 10):
        out = subprocess.run([HPR, "note", "show", *ids[i:i + 10], "-j"],
                             cwd=ROOT, capture_output=True, text=True, check=True).stdout
        data = json.loads(out)["data"]
        notes = data.get("notes", [data]) if isinstance(data, dict) else data
        for n in notes:
            checked += 1
            title = n.get("title") or ""
            body = BOILER.sub(" ", n.get("body") or "")
            head = body[:1200]
            tt, bt = content_tokens(title), content_tokens(head)
            overlap = len(tt & bt) / len(tt) if tt else 1.0
            src_host = host(n.get("source") or "")
            body_hosts = {host(u) for u in URL.findall(head)} - {""}
            host_conflict = bool(src_host and body_hosts and src_host not in body_hosts)
            if overlap < 0.25 or (overlap < 0.45 and host_conflict):
                flagged.append({
                    "id": n["id"], "title": title, "source": n.get("source"),
                    "title_token_overlap": round(overlap, 3),
                    "body_hosts": sorted(body_hosts)[:4],
                    "host_conflict": host_conflict,
                    "body_head": head.strip()[:240].replace("\n", " "),
                })
    OUT.write_text(json.dumps({"checked": checked, "flagged": flagged}, indent=1))
    print(f"checked {checked} notes, flagged {len(flagged)}", file=sys.stderr)
    for f in flagged:
        print(f"  [{f['title_token_overlap']:.2f}] {f['id'][:60]}", file=sys.stderr)
        print(f"        title: {f['title'][:90]}", file=sys.stderr)
        print(f"        body : {f['body_head'][:120]}", file=sys.stderr)


if __name__ == "__main__":
    main()
