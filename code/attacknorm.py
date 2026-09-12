#!/usr/bin/env python3
"""attacknorm: verify the four-line reporting contract for an ATT&CK-denominated artefact.

Reads any file carrying ATT&CK technique identifiers (plain text or CSV, an
ATT&CK Navigator layer, a TRAM training file, a CTIBench TSV), projects the
identifiers onto a target release with ATT&CK-Norm, and prints the four header
lines the paper asks every such artefact to publish, followed by the residual
ledger. Stdlib only; the protocol itself lives in attackdrift.py.

    attacknorm.py --input layer.json [--domain enterprise-attack] [--from 17.0]
                  [--to 19.2] [--rollup] [--bundle-hash] [--json out.json]
                  [--markdown] [--compare other.json]
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import attackdrift as ad  # noqa: E402

csv.field_size_limit(10_000_000)

TID = re.compile(r"\bT\d{4}(?:\.\d{3})?\b")
DOMAINS = ["enterprise-attack", "mobile-attack", "ics-attack"]
PLATFORM_DOMAIN = {"enterprise": "enterprise-attack", "mobile": "mobile-attack",
                   "ics": "ics-attack"}
REPO = Path(os.environ.get("ATTACK_STIX_REPO", "/home/user/mitre-attack/attack-stix-data"))


# ----------------------------------------------------------------------
# input readers: each returns (ids, meta)
# ----------------------------------------------------------------------

def _regex(text: str) -> set[str]:
    return set(TID.findall(text))


def read_navigator(d: dict) -> tuple[set[str], dict]:
    ids = {t.get("techniqueID", "") for t in d.get("techniques", [])}
    meta = {"format": "navigator", "declared_release": (d.get("versions") or {}).get("attack"),
            "declared_domain": d.get("domain"), "layer_name": d.get("name")}
    return {i for i in ids if TID.fullmatch(i)}, meta


def read_tram(d: dict) -> tuple[set[str], dict]:
    ids = {m.get("attack_id", "") for s in d.get("sentences", []) for m in s.get("mappings") or []}
    return {i for i in ids if TID.fullmatch(i)}, {"format": "tram", "declared_release": None}


def read_ctibench(rows: list[dict], domain: str) -> tuple[set[str], dict]:
    ids: set[str] = set()
    skipped = 0
    for row in rows:
        plat = (row.get("Platform") or "").strip().lower()
        if plat and PLATFORM_DOMAIN.get(plat) != domain:
            skipped += 1
            continue
        ids |= _regex(row.get("GT") or "")
    meta = {"format": "ctibench", "declared_release": None,
            "notes": [f"{skipped} rows with a Platform outside {domain} ignored; "
                      f"rerun with --domain to cover them"] if skipped else []}
    return ids, meta


def read_wide_csv(header: list[str], rows: list[list[str]]) -> tuple[set[str], dict]:
    """rcATT shape: one column per technique, 1/0 cells."""
    cols = [(i, h.strip().strip('"')) for i, h in enumerate(header)
            if TID.fullmatch(h.strip().strip('"'))]
    ids = {tid for i, tid in cols
           if any(i < len(r) and r[i].strip().strip('"') in {"1", "1.0"} for r in rows)}
    return ids, {"format": "wide-csv", "declared_release": None,
                 "notes": [f"{len(cols)} technique columns in the header; identifiers "
                           f"taken from column names, not from free text"]}


def read_input(path: Path, fmt: str | None, domain: str) -> tuple[set[str], dict]:
    text = path.read_text(errors="replace")
    ext = path.suffix.lower()
    fmt = fmt or "auto"
    if fmt in ("auto", "navigator", "tram") and (ext == ".json" or fmt != "auto"):
        try:
            d = json.loads(text)
        except json.JSONDecodeError:
            d = None
        if isinstance(d, dict):
            if fmt == "navigator" or (fmt == "auto" and "techniques" in d):
                return read_navigator(d)
            if fmt == "tram" or (fmt == "auto" and "sentences" in d):
                return read_tram(d)
    if fmt in ("auto", "ctibench", "wide-csv") and (ext in (".csv", ".tsv") or fmt != "auto"):
        delim = "\t" if ext == ".tsv" or "\t" in text[:2000] else ","
        rows = list(csv.reader(text.splitlines(), delimiter=delim))
        header = rows[0] if rows else []
        if fmt == "ctibench" or (fmt == "auto" and "GT" in header):
            return read_ctibench([dict(zip(header, r)) for r in rows[1:]], domain)
        if fmt == "wide-csv" or (fmt == "auto" and any(TID.fullmatch(h.strip().strip('"'))
                                                        for h in header)):
            return read_wide_csv(header, rows[1:])
    return _regex(text), {"format": "text", "declared_release": None}


# ----------------------------------------------------------------------
# release resolution, provenance, hashing
# ----------------------------------------------------------------------

def resolve_release(con, domain: str, want: str | None) -> str | None:
    """'17.0' -> '17.0'; a bare major '17' -> the .0 release; unknown -> None."""
    if not want:
        return None
    want = str(want).lstrip("vV")
    versions = {r.version for r in ad.releases(con, domain)}
    if want in versions:
        return want
    for r in ad.major_releases(con, domain):
        if r.version.split(".")[0] == want:
            return r.version
    return None


def live_by_release(con, domain: str, ids: set[str]) -> dict[str, set[str]]:
    """release -> the subset of ids live there. One query instead of 41 snapshots."""
    if not ids:
        return {}
    marks = ",".join("?" * len(ids))
    out = {r.version: set() for r in ad.releases(con, domain)}
    for v, aid in con.execute(
            f"SELECT DISTINCT version, attack_id FROM objects WHERE domain=? AND otype=? "
            f"AND revoked=0 AND deprecated=0 AND attack_id IN ({marks})",
            (domain, ad.TECH, *sorted(ids))):
        out[v].add(aid)
    return out


def provenance(con, domain: str, ids: set[str]) -> dict:
    live = live_by_release(con, domain, ids)
    rels = ad.releases(con, domain)
    consistent = [r.version for r in rels if live.get(r.version) == ids]
    best = max(rels, key=lambda r: len(live.get(r.version, ()))) if rels else None
    return {"consistent_releases": consistent,
            "best_fit": {"release": best.version, "live": len(live[best.version]),
                         "of": len(ids)} if best and ids else None}


def bundle_hash(domain: str, version: str) -> dict | None:
    p = REPO / domain / f"{domain}-{version}.json"
    if not p.exists():
        return None
    return {"file": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}


# ----------------------------------------------------------------------
# the ledger
# ----------------------------------------------------------------------

def ledger(ids: set[str], target: ad.Snapshot, rollup: bool) -> dict:
    res = ad.normalize_with_ledger(ids, target, rollup=rollup)
    rev, sub, tech = target.revoked_by(), target.sub_of(), target.tech

    def is_sub(i: str) -> bool:
        return bool(tech[i]["is_subtechnique"]) if i in tech else "." in i

    demoted: dict[str, dict] = {}
    for aid, cur in res.kept.items():
        if aid == cur:
            continue
        if is_sub(aid) != is_sub(cur):
            demoted[aid] = {"to": cur, "direction":
                            "sub-technique→parent" if is_sub(aid) else "parent→sub-technique"}
        elif not is_sub(aid):
            # v19-style: the parent landed on the terminal one of its own children
            # also landed on, so a family became one former member with a flat id
            kids = [c for c in rev if sub.get(c) == aid and ad.resolve_chain(c, rev) == cur]
            if kids:
                child = min(kids)
                demoted[aid] = {"to": cur, "direction": "parent→sub-technique",
                                "via_former_child": child}
    dropped = {}
    for aid in res.dropped:
        cur = ad.resolve_chain(aid, rev)
        if cur not in tech:
            dropped[aid] = "absent"
        elif cur != aid or tech[cur]["revoked"]:
            dropped[aid] = "revoked-with-no-live-terminal"
        else:
            dropped[aid] = "deprecated"
    resolved = {a: c for a, c in res.kept.items() if a != c}
    return {"input": len(ids), "kept": len(res.kept),
            "kept_unchanged": len(res.kept) - len(resolved),
            "kept_via_revocation_chain": len(resolved),
            "distinct_after": len(res.ids), "merge_targets": len(res.merged),
            "absorbed_by_merges": sum(len(v) for v in res.merged.values()),
            "demoted": len(demoted), "dropped": len(dropped),
            "rolled_up": len(res.rolled_up),
            "detail": {"resolved": resolved, "merged": res.merged, "demoted": demoted,
                       "dropped": dropped, "rolled_up": res.rolled_up,
                       "ids_in": sorted(ids), "ids_after": sorted(res.ids)}}


# ----------------------------------------------------------------------
# one artefact -> report dict
# ----------------------------------------------------------------------

def analyse(con, path: Path, args) -> dict:
    ids, meta = read_input(path, args.format, args.domain)
    domain = args.domain
    notes = list(meta.pop("notes", []))
    if meta.get("declared_domain") and meta["declared_domain"] != domain:
        notes.append(f"layer declares domain {meta['declared_domain']}; analysed as {domain}")
    if not ids:
        notes.append("no technique identifiers found in the input")

    src_claim = args.from_release or meta.get("declared_release")
    src = resolve_release(con, domain, src_claim)
    if src_claim and not src:
        notes.append(f"declared release '{src_claim}' is not a {domain} release in the DB; "
                     f"treated as undeclared")
    prov = provenance(con, domain, ids)
    if src:
        live = live_by_release(con, domain, ids).get(src, set())
        src_block = {"release": src, "declared": src_claim,
                     "source": "cli --from" if args.from_release else "artefact",
                     "live_at_release": len(live), "of": len(ids),
                     "not_live_at_release": sorted(ids - live)}
    else:
        src_block = {"release": None, "declared": None, "source": "inferred"}
    src_block.update(prov)
    if args.bundle_hash and src:
        src_block["bundle"] = bundle_hash(domain, src)

    to = resolve_release(con, domain, args.to) or ad.releases(con, domain)[-1].version
    if args.to and to != args.to.lstrip("vV"):
        notes.append(f"--to {args.to} resolved to v{to}")
    target = ad.load_snapshot(con, domain, to)
    tgt_block = {"release": to, "date": target.released[:10]}
    if args.bundle_hash:
        tgt_block["bundle"] = bundle_hash(domain, to)
        if tgt_block["bundle"] is None:
            notes.append(f"bundle file for v{to} not found under {REPO} (set ATTACK_STIX_REPO)")

    return {"input": str(path), "domain": domain, "rollup": args.rollup, **meta,
            "source_release": src_block, "target_release": tgt_block,
            "ledger": ledger(ids, target, args.rollup), "notes": notes}


# ----------------------------------------------------------------------
# rendering
# ----------------------------------------------------------------------

def _src_line(r: dict) -> str:
    s = r["source_release"]
    if s["release"]:
        line = f"v{s['release']}"
        if s["declared"] and s["declared"] != s["release"]:
            line += f" (declared as '{s['declared']}')"
        line += f" [{s['source']}]; {s['live_at_release']}/{s['of']} identifiers live there"
    else:
        c = s["consistent_releases"]
        if c:
            line = f"undeclared; inferred provenance interval v{c[0]}–v{c[-1]} ({len(c)} releases)"
        elif s["best_fit"]:
            b = s["best_fit"]
            line = (f"undeclared; NO release has every identifier live (best fit v{b['release']}, "
                    f"{b['live']}/{b['of']} live)")
        else:
            line = "undeclared; no identifiers"
    if s.get("bundle"):
        line += f"; bundle sha256 {s['bundle']['sha256']}"
    return line


def header_lines(r: dict) -> list[str]:
    L = r["ledger"]
    t = r["target_release"]
    tgt = f"v{t['release']} ({t['date']})"
    if t.get("bundle"):
        tgt += f"; bundle sha256 {t['bundle']['sha256']}"
    merged = f"{L['absorbed_by_merges']} merged onto {L['merge_targets']} targets"
    return [
        f"1. domain {r['domain']}; source release {_src_line(r)}",
        f"2. normalized onto {r['domain']} {tgt}" + (" with roll-up" if r["rollup"] else ""),
        f"3. ledger: {L['input']} in; {L['kept']} kept ({L['kept_unchanged']} unchanged, "
        f"{L['kept_via_revocation_chain']} via revocation chain); {merged}; "
        f"{L['demoted']} changed abstraction level; {L['dropped']} dropped; "
        f"{L['distinct_after']} distinct after",
        f"4. cross-time comparison: any comparison must project both sides onto "
        f"{r['domain']} v{t['release']}; report the other side's ledger too",
    ]


def detail_lines(r: dict, md: bool = False) -> list[str]:
    d = r["ledger"]["detail"]
    b = "- " if md else "  "
    out = []
    if d["merged"]:
        out.append("merges (target ← absorbed):")
        out += [f"{b}{t} ← {', '.join(s)}" for t, s in sorted(d["merged"].items())]
    if d["demoted"]:
        out.append("abstraction changes:")
        for a, v in sorted(d["demoted"].items()):
            via = f" (via former child {v['via_former_child']})" if v.get("via_former_child") else ""
            out.append(f"{b}{a} → {v['to']}  {v['direction']}{via}")
    if d["rolled_up"]:
        out.append("rolled up to parent:")
        out += [f"{b}{a} → {t}" for a, t in sorted(d["rolled_up"].items())]
    if d["dropped"]:
        out.append("dropped:")
        out += [f"{b}{a}  {why}" for a, why in sorted(d["dropped"].items())]
    if d["resolved"]:
        plain = {a: t for a, t in d["resolved"].items() if a not in d["demoted"]}
        if plain:
            out.append("resolved via revocation chain (same level):")
            out += [f"{b}{a} → {t}" for a, t in sorted(plain.items())]
    return out


def render_text(r: dict) -> str:
    lines = [f"== {r['input']}  [{r['format']}]"]
    lines += r["notes"] and [f"note: {n}" for n in r["notes"]] or []
    lines += header_lines(r)
    lines += detail_lines(r)
    return "\n".join(lines)


def render_markdown(r: dict) -> str:
    lines = [f"**Artefact:** `{Path(r['input']).name}` ({r['format']})", ""]
    lines += [f"{h}" for h in header_lines(r)]
    if r["notes"]:
        lines += [""] + [f"> {n}" for n in r["notes"]]
    det = detail_lines(r, md=True)
    if det:
        lines += [""] + [x if x.startswith("- ") else f"**{x}**" for x in det]
    return "\n".join(lines)


def compare_block(a: dict, b: dict) -> dict:
    ia, ib = set(a["ledger"]["detail"]["ids_after"]), set(b["ledger"]["detail"]["ids_after"])
    ra, rb = set(a["ledger"]["detail"]["ids_in"]), set(b["ledger"]["detail"]["ids_in"])
    t = a["target_release"]["release"]
    return {"reference_release": t, "domain": a["domain"],
            "overlap_after": len(ia & ib), "jaccard_after": round(ad.jaccard(ia, ib), 4),
            "overlap_raw": len(ra & rb), "jaccard_raw": round(ad.jaccard(ra, rb), 4),
            "statement": (f"4. both artefacts projected onto {a['domain']} v{t}; "
                          f"comparable sets {len(ia)} vs {len(ib)}, overlap {len(ia & ib)} "
                          f"(Jaccard {ad.jaccard(ia, ib):.3f}); raw identifiers would have "
                          f"overlapped on {len(ra & rb)} (Jaccard {ad.jaccard(ra, rb):.3f})")}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--input", required=True)
    ap.add_argument("--compare", help="second artefact; both projected onto --to")
    ap.add_argument("--format", choices=["auto", "text", "navigator", "tram", "ctibench", "wide-csv"])
    ap.add_argument("--domain", default="enterprise-attack", choices=DOMAINS)
    ap.add_argument("--from", dest="from_release", help="release the artefact claims")
    ap.add_argument("--to", help="target release (default: newest in the DB)")
    ap.add_argument("--rollup", action="store_true")
    ap.add_argument("--bundle-hash", action="store_true",
                    help="sha256 of the bundle files under $ATTACK_STIX_REPO")
    ap.add_argument("--json", help="write the report as JSON to this path")
    ap.add_argument("--markdown", action="store_true", help="print a paste-ready markdown block")
    args = ap.parse_args(argv)

    con = ad.connect()
    try:
        reports = [analyse(con, Path(args.input), args)]
        if args.compare:
            reports.append(analyse(con, Path(args.compare), args))
    except (OSError, UnicodeDecodeError) as e:
        print(f"attacknorm: cannot read input: {e}", file=sys.stderr)
        return 2
    render = render_markdown if args.markdown else render_text
    out = {"artefacts": reports}
    print("\n\n".join(render(r) for r in reports))
    if len(reports) == 2:
        out["comparison"] = compare_block(*reports)
        print("\n" + out["comparison"]["statement"])
    if args.json:
        Path(args.json).write_text(json.dumps(out if args.compare else reports[0], indent=1,
                                              ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
