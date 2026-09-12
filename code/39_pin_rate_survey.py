#!/usr/bin/env python3
"""E23: publication-side falsifier check for the Section 11 claim.

The repository-side evidence (E9, E16) is that deployed CTI artefacts almost
never declare the ATT&CK release they were built against. This measures the
other half: of recent arXiv papers that actually use ATT&CK technique
identifiers, what share declares the release?

Pipeline: pull a sampling frame from the arXiv API (2023-01-01 to
2026-09-01, "MITRE ATT&CK"), draw a seeded sample of 60, fetch full text via
`hyperresearch fetch` (replacing fetch failures from the frame, capped at 90
total fetch attempts), keep papers that use >=3 technique IDs, classify each
kept paper's best ATT&CK-release declaration by regex + context read, and
report the pin rate with a Wilson 95% interval.

Resumable: progress is checkpointed to OUT after every fetch, so a re-run
picks up where it left off instead of re-fetching.
"""
from __future__ import annotations

import json
import random
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "results" / "e23_pin_rate.json"
RAW_XML = ROOT / "data" / "results" / "e23" / "arxiv_raw_0.xml"  # provenance: the raw API response
TABLE = ROOT / "paper" / "tables" / "t25_pin_rate.md"
HR = ROOT / ".venv" / "bin" / "hyperresearch"
TAGS = ["attack-ontology-drift-cti-85bc51", "pin-rate-survey"]

SEED = 20260912
SAMPLE_N = 60
FETCH_CAP = 90
FRAME_CAP = 300
DATE_LO, DATE_HI = "20230101", "20260901"
Z = 1.959963984540054  # two-sided 95%

TECH_ID_RE = re.compile(r"\bT\d{4}(?:\.\d{3})?\b")
SUBTECH_RE = re.compile(r"\bT\d{4}\.\d{3}\b")

ATOM_NS = {"a": "http://www.w3.org/2005/Atom"}

# (bucket, regex) — first bucket with a hit wins, in this priority order.
MONTHS = ("January|February|March|April|May|June|July|August|September|"
          "October|November|December")
PATTERNS: list[tuple[str, re.Pattern]] = [
    ("exact_release", re.compile(
        r"ATT&CK\s*(?:Enterprise\s*)?v(?:ersion)?\.?\s*(\d{1,2}\.\d{1,2}(?:\.\d{1,2})?)",
        re.I)),
    ("exact_release", re.compile(
        r"version\s+(\d{1,2}\.\d{1,2})\s+of\s+(?:the\s+)?(?:MITRE\s+)?ATT&CK", re.I)),
    ("exact_release", re.compile(
        r"ATT&CK\s*(?:Enterprise\s*)?(?:release|version)\s*(\d{1,2}\.\d{1,2})", re.I)),
    ("exact_release", re.compile(
        r"(?:commit\s+[0-9a-f]{7,40}[^.]{0,80}?(?:attack-stix-data|ATT&CK)"
        r"|(?:attack-stix-data|ATT&CK)[^.]{0,80}?commit\s+[0-9a-f]{7,40})", re.I)),
    ("exact_release", re.compile(
        r'"?versions"?\s*:?\s*\{?\s*"?attack"?\s*"?:\s*"?(\d{1,2}\.\d{1,2})', re.I)),
    ("major_only", re.compile(
        r"ATT&CK\s*(?:Enterprise\s*)?v(?:ersion)?\.?\s*(\d{1,2})\b(?!\.\d)", re.I)),
    ("major_only", re.compile(
        r"version\s+(\d{1,2})\s+of\s+(?:the\s+)?(?:MITRE\s+)?ATT&CK\b(?!\.\d)", re.I)),
    ("major_only", re.compile(
        r"ATT&CK\s*(?:Enterprise\s*)?(?:release|version)\s*(\d{1,2})\b(?!\.\d)", re.I)),
    ("date_only", re.compile(
        rf"(?:{MONTHS})\s+20\d{{2}}\s+(?:release|version)", re.I)),
    ("date_only", re.compile(
        r"the\s+20\d{2}\s+version\s+of\s+(?:the\s+)?(?:MITRE\s+)?ATT&CK", re.I)),
    ("date_only", re.compile(r"ATT&CK\s*\(?20\d{2}\)?\s*(?:release|version)", re.I)),
]
BUCKET_RANK = {"exact_release": 3, "major_only": 2, "date_only": 1, "none": 0}

VERSION_CHANGE_KEYWORDS = [
    "sub-technique", "subtechnique", "restructuring", "restructure",
    "deprecated technique", "revoked technique", "technique id change",
    "version change", "schema change", "renumbering",
]

# Manual overrides from the "confirm by reading the surrounding sentence" pass
# (protocol step 4). The regex/proximity sweep in classify() has real recall
# gaps it cannot close cheaply: it misses declarations phrased as "whose
# version 19.1 catalogue", "the Enterprise bundle" instead of the literal
# string "ATT&CK", a version pin split across a sentence boundary in a
# citation, or a paper's own dataset row buried in a related-work comparison
# table. Each entry here was confirmed by reading the note body directly; the
# reasoning is in the comment, the evidence string is a verbatim excerpt.
MANUAL_OVERRIDES: dict[str, dict] = {
    "2607.25572v1": {  # "Mapping CVEs to MITRE ATT&CK Techniques"
        "classification": "exact_release",
        "evidence": "We target the Enterprise domain, whose version 19.1 catalogue "
                     "contains 697 active techniques and sub-techniques.",
    },
    "2512.12078v3": {  # "The Procedural Semantics Gap in Structured CTI"
        "classification": "exact_release",
        "evidence": "We use version 18.1 of the Enterprise bundle as the "
                     "authoritative source for all quantitative analyses.",
    },
    "2504.05866v1": {  # "CTI-HAL: A Human-Annotated Dataset" — own dataset row
        "classification": "exact_release",  # in a related-work comparison table
        "evidence": "CTI-HAL ... statement level json 116 81 real CTI reports v15.1 "
                     "[own dataset row, Table 1: CTI Dataset Overview]",
    },
    "2608.17361v1": {  # "Trusted Workflow Relays" — reference-list citation
        "classification": "major_only",
        "evidence": "The MITRE Corporation. MITRE ATT&CK for enterprise, 2026. "
                     "Version 19; accessed August 17, 2026.",
    },
    "2604.26217v1": {  # "OpenSOC-AI"
        "classification": "major_only",
        "evidence": "Ground-truth labels were derived from MITRE ATT&CK framework "
                     "v14 and annotated by the author with reference to established "
                     "threat intelligence sources.",
    },
}


def sh(*args: str) -> dict:
    """Run a hyperresearch subcommand and return its parsed JSON envelope."""
    proc = subprocess.run([str(HR), *args, "-j"], capture_output=True, text=True)
    try:
        return json.loads(proc.stdout)
    except ValueError:
        return {"ok": False, "error": f"non-JSON output: {proc.stdout[:300]!r} {proc.stderr[:300]!r}"}


# ----------------------------------------------------------------------
# step 1: sampling frame
# ----------------------------------------------------------------------

def fetch_frame() -> list[dict]:
    query = f'all:"MITRE ATT&CK" AND submittedDate:[{DATE_LO} TO {DATE_HI}]'
    entries = _arxiv_query(query, FRAME_CAP)
    if not entries:
        # fallback: unbounded query, filter dates client-side
        entries = [e for e in _arxiv_query('all:"MITRE ATT&CK"', 400)
                   if DATE_LO <= e["published"].replace("-", "")[:8] <= DATE_HI]
    return entries[:FRAME_CAP]


def _arxiv_query(query: str, max_results: int) -> list[dict]:
    encoded = urllib.parse.quote(query, safe="")
    url = (f"http://export.arxiv.org/api/query?search_query={encoded}"
           f"&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending")
    req = urllib.request.Request(
        url, headers={"User-Agent": "hyper-research-works pin-rate-survey "
                                     "(mailto:jeonck2000@gmail.com)"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()
    if b"<entry>" not in data:
        raise RuntimeError(f"arXiv API returned no entries ({len(data)} bytes) for {query!r}")
    RAW_XML.parent.mkdir(parents=True, exist_ok=True)
    RAW_XML.write_bytes(data)  # overwrites the 14-byte broken file from the prior attempt
    root = ET.fromstring(data)
    out = []
    for e in root.findall("a:entry", ATOM_NS):
        arxiv_url = e.findtext("a:id", default="", namespaces=ATOM_NS)
        arxiv_id = arxiv_url.rsplit("/abs/", 1)[-1].rsplit("/", 1)[-1]
        cat_el = e.find("a:category", ATOM_NS)
        out.append({
            "id": arxiv_id,
            "title": " ".join(e.findtext("a:title", default="", namespaces=ATOM_NS).split()),
            "published": e.findtext("a:published", default="", namespaces=ATOM_NS)[:10],
            "primary_category": cat_el.get("term") if cat_el is not None else "",
        })
    return out


# ----------------------------------------------------------------------
# step 2/3: seeded sample, fetch with replacement, inclusion test
# ----------------------------------------------------------------------

SELF_REF_RE = re.compile(
    r"\b(we|our|this (paper|study|work|dataset|system)|dataset|implementation|"
    r"evaluat\w*|experiment\w*|method\w*|use[sd]?|adopt\w*|align\w*|"
    r"map(?:ped|ping)?|built|construct\w*|snapshot|based on)\b", re.I)
# background trivia about ATT&CK's own release history is not a declaration of
# which release *this paper* used — the false positive that motivated this list
# was "Sub-techniques were first introduced in ATT&CK Version 7"
HISTORY_RE = re.compile(
    r"first introduced|originally (released|introduced)|history of att&ck|"
    r"was introduced|initially released|since its inception", re.I)


def evidence_window(body: str, m: re.Match) -> str:
    lo, hi = max(0, m.start() - 100), min(len(body), m.end() + 100)
    snippet = " ".join(body[lo:hi].split())
    return snippet[:200]


def _candidates(body: str, bucket: str) -> list[re.Match]:
    out = []
    for b, pat in PATTERNS:
        if b == bucket:
            out.extend(pat.finditer(body))
    return out


def classify(body: str) -> tuple[str, str]:
    """Return (classification, evidence_sentence).

    Within the highest-priority bucket that has a hit, prefer a match whose
    context reads as the paper's own methodology over one that reads as
    background trivia about ATT&CK's release history (a real false positive
    seen in manual review: "sub-techniques were first introduced in ATT&CK
    Version 7").
    """
    for bucket in ("exact_release", "major_only", "date_only"):
        matches = _candidates(body, bucket)
        if not matches:
            continue
        scored = []
        for m in matches:
            window = evidence_window(body, m)
            is_history = bool(HISTORY_RE.search(window))
            is_self_ref = bool(SELF_REF_RE.search(window))
            scored.append((is_self_ref and not is_history, not is_history, m))
        scored.sort(key=lambda t: (t[0], t[1]), reverse=True)
        best = scored[0][2]
        if scored[0][1]:  # at least a non-history match exists in this bucket
            return bucket, evidence_window(body, best)
        # every candidate in this bucket looked like history/trivia — fall
        # through to the next, less specific bucket instead of reporting a hit
    return "none", ""


def analyze_paper(cand: dict, note: dict) -> dict:
    body = note["body"]
    tech_ids = TECH_ID_RE.findall(body)
    result = {
        "arxiv_id": cand["id"],
        "title": cand["title"],
        "year": int(cand["published"][:4]) if cand["published"] else None,
        "note_id": note["id"],
        "tech_id_count": len(tech_ids),
        "included": len(tech_ids) >= 3,
    }
    if not result["included"]:
        result["exclusion_reason"] = f"only {len(tech_ids)} technique-ID occurrences (<3)"
        return result
    classification, evidence = classify(body)
    result["classification"] = classification
    result["evidence"] = evidence
    result["uses_subtechniques"] = bool(SUBTECH_RE.search(body))
    low = body.lower()
    result["mentions_version_change"] = any(k in low for k in VERSION_CHANGE_KEYWORDS)
    return result


def run_survey(state: dict) -> None:
    rng = random.Random(SEED)
    frame = state["frame"]
    order = list(range(len(frame)))
    rng.shuffle(order)
    primary_idx, replacement_idx = order[:SAMPLE_N], order[SAMPLE_N:]
    queue = [frame[i]["id"] for i in primary_idx] + [frame[i]["id"] for i in replacement_idx]
    by_id = {f["id"]: f for f in frame}

    done_ids = {r["arxiv_id"] for r in state["fetch_log"]}
    attempts = len(state["fetch_log"])
    included_count = sum(1 for p in state["papers"] if p.get("included"))
    q_iter = iter([qid for qid in queue if qid not in done_ids])

    while included_count + len(state["excluded"]) < SAMPLE_N and attempts < FETCH_CAP:
        try:
            arxiv_id = next(q_iter)
        except StopIteration:
            break
        cand = by_id[arxiv_id]
        attempts += 1
        url = f"https://arxiv.org/abs/{arxiv_id}"
        print(f"[{attempts}/{FETCH_CAP}] fetching {arxiv_id} — {cand['title'][:70]}", file=sys.stderr)
        resp = sh("fetch", url, "--tag", TAGS[0], "--tag", TAGS[1])
        log_entry = {"arxiv_id": arxiv_id, "attempt": attempts}
        if not resp.get("ok"):
            log_entry["status"] = "fetch_failed"
            log_entry["error"] = resp.get("error", "unknown error")
            state["fetch_log"].append(log_entry)
            save(state)
            time.sleep(1.0)
            continue
        note_id = resp["data"]["note_id"]
        log_entry["status"] = "ok"
        log_entry["note_id"] = note_id
        log_entry["word_count"] = resp["data"].get("word_count")
        state["fetch_log"].append(log_entry)

        show = sh("note", "show", note_id)
        if not show.get("ok"):
            log_entry["status"] = "read_failed"
            log_entry["error"] = show.get("error", "unknown error")
            save(state)
            time.sleep(1.0)
            continue
        result = analyze_paper(cand, show["data"])
        state["papers"].append(result)
        if result["included"]:
            included_count += 1
        else:
            state["excluded"].append(result)
        save(state)
        time.sleep(1.0)

    state["fetch_attempts_used"] = attempts


def reclassify_included(state: dict) -> None:
    """Re-run classify() against already-fetched note bodies (no re-fetch).

    Lets a fix to the classification regex/heuristics apply retroactively
    without re-downloading anything — `note show` reads the local vault.
    """
    for p in state["papers"]:
        if not p.get("included"):
            continue
        show = sh("note", "show", p["note_id"])
        if not show.get("ok"):
            continue
        body = show["data"]["body"]
        classification, evidence = classify(body)
        p["classification"] = classification
        p["evidence"] = evidence
        p["uses_subtechniques"] = bool(SUBTECH_RE.search(body))
        p["mentions_version_change"] = any(k in body.lower() for k in VERSION_CHANGE_KEYWORDS)


def apply_manual_overrides(state: dict) -> None:
    for p in state["papers"]:
        override = MANUAL_OVERRIDES.get(p["arxiv_id"])
        if not override:
            continue
        p["classification"] = override["classification"]
        p["evidence"] = override["evidence"]
        p["manual_override"] = True


# ----------------------------------------------------------------------
# step 4: statistics
# ----------------------------------------------------------------------

def wilson(k: int, n: int) -> tuple[float, float]:
    if n == 0:
        return 0.0, 1.0
    p = k / n
    denom = 1 + Z * Z / n
    centre = (p + Z * Z / (2 * n)) / denom
    half = Z * ((p * (1 - p) / n + Z * Z / (4 * n * n)) ** 0.5) / denom
    return max(0.0, centre - half), min(1.0, centre + half)


def rate_block(k: int, n: int) -> dict:
    lo, hi = wilson(k, n)
    return {"k": k, "n": n, "rate": (k / n if n else None), "wilson_lo": lo, "wilson_hi": hi}


def compute_results(state: dict) -> dict:
    included = [p for p in state["papers"] if p["included"]]
    n = len(included)
    exact = sum(1 for p in included if p["classification"] == "exact_release")
    major_or_better = sum(1 for p in included if p["classification"] in ("exact_release", "major_only"))
    any_decl = sum(1 for p in included if p["classification"] != "none")

    by_year: dict[str, dict] = {}
    for p in included:
        y = str(p["year"])
        by_year.setdefault(y, {"n": 0, "exact": 0, "major_or_better": 0})
        by_year[y]["n"] += 1
        if p["classification"] == "exact_release":
            by_year[y]["exact"] += 1
        if p["classification"] in ("exact_release", "major_only"):
            by_year[y]["major_or_better"] += 1
    by_year_stats = {
        y: {"exact": rate_block(v["exact"], v["n"]),
            "major_or_better": rate_block(v["major_or_better"], v["n"])}
        for y, v in sorted(by_year.items())
    }

    sub_yes = [p for p in included if p["uses_subtechniques"]]
    sub_no = [p for p in included if not p["uses_subtechniques"]]
    by_subtech = {
        "uses_subtechniques": rate_block(
            sum(1 for p in sub_yes if p["classification"] in ("exact_release", "major_only")),
            len(sub_yes)),
        "no_subtechniques": rate_block(
            sum(1 for p in sub_no if p["classification"] in ("exact_release", "major_only")),
            len(sub_no)),
    }

    return {
        "n_frame": len(state["frame"]),
        "n_manual_overrides": sum(1 for p in included if p.get("manual_override")),
        "n_sampled": SAMPLE_N,
        "n_fetch_attempts": state.get("fetch_attempts_used", len(state["fetch_log"])),
        "n_fetch_failures": sum(1 for f in state["fetch_log"] if f["status"] != "ok"),
        "n_fetched_ok": sum(1 for f in state["fetch_log"] if f["status"] == "ok"),
        "n_excluded": len(state["excluded"]),
        "n_included": n,
        "pin_exact": rate_block(exact, n),
        "pin_major_or_better": rate_block(major_or_better, n),
        "pin_any_declaration": rate_block(any_decl, n),
        "by_year": by_year_stats,
        "by_subtechnique_use": by_subtech,
    }


def write_table(results: dict) -> None:
    def ci(block: dict) -> str:
        if block["n"] == 0:
            return "n/a"
        return f"[{block['wilson_lo']:.3f}, {block['wilson_hi']:.3f}]"

    def est(block: dict) -> str:
        return "n/a" if block["n"] == 0 else f"{block['rate']:.3f}"

    def kn(block: dict) -> str:
        return f"{block['k']} / {block['n']}"

    lines = [
        f"**Table 25.** Publication-side ATT\\&CK release-pin rate: arXiv papers "
        f"({DATE_LO[:4]}-01-01 to {DATE_HI[:4]}-{DATE_HI[4:6]}-{DATE_HI[6:]}) that use "
        f"ATT\\&CK technique identifiers, Wilson 95% intervals, seed {SEED}.",
        "",
        "| Quantity | k / n | Estimate | 95% interval |",
        "|---|---|---|---|",
        f"| Exact release declared (e.g. v14.1) | {kn(results['pin_exact'])} | {est(results['pin_exact'])} | {ci(results['pin_exact'])} |",
        f"| Major-or-better declared (v14 or v14.1) | {kn(results['pin_major_or_better'])} | {est(results['pin_major_or_better'])} | {ci(results['pin_major_or_better'])} |",
        f"| Any declaration (incl. date-only) | {kn(results['pin_any_declaration'])} | {est(results['pin_any_declaration'])} | {ci(results['pin_any_declaration'])} |",
        "",
        "Sampling funnel:",
        "",
        "| Stage | Count |",
        "|---|---|",
        f"| Sampling frame (arXiv, \"MITRE ATT&CK\") | {results['n_frame']} |",
        f"| Seeded sample | {results['n_sampled']} |",
        f"| Fetch attempts used (cap {FETCH_CAP}) | {results['n_fetch_attempts']} |",
        f"| Fetch failures | {results['n_fetch_failures']} |",
        f"| Fetched OK | {results['n_fetched_ok']} |",
        f"| Excluded (fewer than 3 technique-ID occurrences) | {results['n_excluded']} |",
        f"| Included (uses ATT&CK technique IDs) | {results['n_included']} |",
        f"| Included papers requiring manual reclassification | {results['n_manual_overrides']} |",
        "",
        "By year:",
        "",
        "| Year | n | Exact release k/n | 95% CI | Major-or-better k/n | 95% CI |",
        "|---|---|---|---|---|---|",
    ]
    for y, v in results["by_year"].items():
        lines.append(f"| {y} | {v['exact']['n']} | {kn(v['exact'])} | {ci(v['exact'])} | "
                     f"{kn(v['major_or_better'])} | {ci(v['major_or_better'])} |")
    lines += [
        "",
        "By sub-technique use:",
        "",
        "| Group | k / n | Estimate | 95% interval |",
        "|---|---|---|---|",
        f"| Uses sub-technique IDs (T####.###) | {kn(results['by_subtechnique_use']['uses_subtechniques'])} | "
        f"{est(results['by_subtechnique_use']['uses_subtechniques'])} | {ci(results['by_subtechnique_use']['uses_subtechniques'])} |",
        f"| Enterprise/major techniques only | {kn(results['by_subtechnique_use']['no_subtechniques'])} | "
        f"{est(results['by_subtechnique_use']['no_subtechniques'])} | {ci(results['by_subtechnique_use']['no_subtechniques'])} |",
    ]
    TABLE.write_text("\n".join(lines) + "\n")


# ----------------------------------------------------------------------
# step 5: curation
# ----------------------------------------------------------------------

def curate(state: dict) -> None:
    for p in state["papers"]:
        cls = p.get("classification", "excluded")
        if not p["included"]:
            summary = (f"arXiv {p['arxiv_id']}: {p['tech_id_count']} ATT&CK technique-ID "
                       f"occurrences, below the pin-rate-survey inclusion threshold of 3.")
        else:
            summary = (f"arXiv {p['arxiv_id']} ({p['year']}): uses {p['tech_id_count']} ATT&CK "
                       f"technique-ID occurrences "
                       f"({'with' if p['uses_subtechniques'] else 'without'} sub-techniques); "
                       f"ATT&CK release declaration classified as {cls}.")
        sh("note", "update", p["note_id"], "--summary", summary, "--add-tag", "pin-rate-survey")


def save(state: dict) -> None:
    OUT.write_text(json.dumps(state, indent=2))


def load_or_init() -> dict:
    if OUT.exists():
        try:
            return json.loads(OUT.read_text())
        except ValueError:
            pass
    return {"seed": SEED, "date_range": [DATE_LO, DATE_HI], "frame": [],
            "fetch_log": [], "papers": [], "excluded": []}


def main() -> None:
    state = load_or_init()
    if not state["frame"]:
        print("fetching arXiv sampling frame...", file=sys.stderr)
        state["frame"] = fetch_frame()
        save(state)
    print(f"frame size: {len(state['frame'])}", file=sys.stderr)

    run_survey(state)
    save(state)

    print("reclassifying included papers against current heuristics...", file=sys.stderr)
    reclassify_included(state)
    apply_manual_overrides(state)
    save(state)

    results = compute_results(state)
    state["results"] = results
    save(state)
    write_table(results)

    curate(state)
    lint = sh("lint")
    state["lint_after_curation"] = lint
    save(state)

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
