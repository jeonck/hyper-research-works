#!/usr/bin/env python3
"""E22: is the two-clock structure an ATT&CK-only phenomenon?

Re-runs the paper's referential and intensional measurements on two other
MITRE-curated, versioned vocabularies with archived XML releases: CWE
(weaknesses) and CAPEC (attack patterns). Both deprecate in place, so the
referential clock is read from Status="Deprecated" rather than from revocation
edges, and "typed retirement" means the deprecation note names a successor.

Inputs are downloaded on first run into $EXT/cwe and $EXT/capec (default
/Users/mac/ws/ext). Any release that fails to download or parse is logged and
skipped. ATT&CK Enterprise numbers are read from e1_e2_e3.json,
e12_temporal_structure.json and e13_tactic_layer.json, never retyped.

Outputs: data/results/e22_cwe_capec.json, paper/tables/t24_cwe_capec.md,
paper/figures/fig10_cwe_capec.{png,pdf}.
"""
from __future__ import annotations

import io
import json
import os
import re
import subprocess
import sys
import zipfile
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

from scipy.stats import beta

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "data" / "results"
FIG = ROOT / "paper" / "figures"
TAB = ROOT / "paper" / "tables"
EXT = Path(os.environ.get("EXT", "/Users/mac/ws/ext"))
SEED = 20260912  # nothing here is random; kept for the package convention

# All x.0 majors plus a spread of minors. Edit these lists to change the grid.
VERSIONS = {
    "cwe": ["1.0", "1.5", "1.10", "2.0", "2.5", "2.10", "3.0", "3.4.1",
            "4.0", "4.4", "4.8", "4.12", "4.16", "4.20"],
    "capec": ["1.0", "1.5", "1.7.1", "2.0", "2.5", "2.8", "2.11",
              "3.0", "3.2", "3.4", "3.6", "3.8", "3.9"],
}
URL = {"cwe": "https://cwe.mitre.org/data/xml/cwec_v{v}.xml.zip",
       "capec": "https://capec.mitre.org/data/xml/capec_v{v}.xml"}
ENTRY = {"cwe": "Weakness", "capec": "Attack_Pattern"}
PREFIX = {"cwe": "CWE", "capec": "CAPEC"}
HORIZON_YEARS = 5.0
RESTRUCTURE_J = 0.80
WORD = re.compile(r"[a-z0-9]+")
ID_RE = re.compile(r"\b(?:CWE|CAPEC)-(\d+)\b")


def log(*a):
    print(*a, file=sys.stderr)


def tokens(text: str | None) -> set[str]:
    return set(WORD.findall((text or "").lower()))


def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def years(a: str, b: str) -> float:
    return (date.fromisoformat(b) - date.fromisoformat(a)).days / 365.25


def clopper_pearson(k: int, n: int, alpha: float = 0.05) -> list[float]:
    lo = 0.0 if k == 0 else float(beta.ppf(alpha / 2, k, n - k + 1))
    hi = 1.0 if k == n else float(beta.ppf(1 - alpha / 2, k + 1, n - k))
    return [lo, hi]


# ----------------------------------------------------------------------
# download + parse
# ----------------------------------------------------------------------

def fetch(vocab: str, v: str) -> Path | None:
    url = URL[vocab].format(v=v)
    path = EXT / vocab / url.rsplit("/", 1)[-1]
    if path.exists() and path.stat().st_size > 0:
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(["curl", "-sfL", "--retry", "2", "-o", str(path), url])
    if r.returncode != 0 or not path.exists() or path.stat().st_size == 0:
        path.unlink(missing_ok=True)
        log(f"  SKIP {vocab} v{v}: download failed ({url})")
        return None
    return path


def read_xml(path: Path) -> bytes:
    if path.suffix == ".zip":
        with zipfile.ZipFile(path) as z:
            name = next(n for n in z.namelist() if n.endswith(".xml"))
            return z.read(name)
    return path.read_bytes()


def ln(el) -> str:
    return el.tag.rsplit("}", 1)[-1]


def text(el) -> str:
    return " ".join("".join(el.itertext()).split()) if el is not None else ""


def child(el, name):
    return next((c for c in el if ln(c) == name), None)


def description(entry) -> str:
    d = child(entry, "Description")
    if d is None:
        return ""
    # 1.x/2.x wrap the summary in Description_Summary (CWE) or Summary (CAPEC)
    # and put the extended text alongside it inside Description; 3.x+ put the
    # summary text directly in Description and the extended text in a sibling.
    # Both eras' summary is the one-paragraph field compared here.
    for c in d.iter():
        if ln(c) in ("Description_Summary", "Summary"):
            return text(c)
    return text(d)


def parents(entry) -> set[str]:
    """ChildOf targets in the primary hierarchy view (1000) when a view is
    given, else any ChildOf. Handles Relationship / Related_Weakness /
    Related_Attack_Pattern across schema eras."""
    out = set()
    for el in entry.iter():
        if ln(el) not in ("Relationship", "Related_Weakness", "Related_Attack_Pattern"):
            continue
        nature = el.get("Nature") or text(child(el, "Relationship_Nature"))
        if nature != "ChildOf":
            continue
        target = el.get("CWE_ID") or el.get("CAPEC_ID") or text(child(el, "Relationship_Target_ID"))
        views = {el.get("View_ID")} if el.get("View_ID") else \
            {text(c) for c in el.iter() if ln(c) == "Relationship_View_ID"}
        if target and (not views or "1000" in views):
            out.add(target.strip())
    return out


def parse(vocab: str, v: str, path: Path) -> dict | None:
    raw = read_xml(path)
    root = ET.fromstring(raw)
    rel_date = root.get("Date") or root.get("Catalog_Date")
    date_src = "header"
    entries = {}
    for el in root.iter():
        if ln(el) != ENTRY[vocab]:
            continue
        eid = el.get("ID") or el.get("CAPEC_ID")
        if not eid:
            continue
        name = el.get("Name") or ""
        status = el.get("Status") or ("Deprecated" if name.upper().startswith("DEPRECATED") else "Draft")
        desc = description(el)
        succ = sorted({s for s in ID_RE.findall(name + " " + desc) if s != eid}, key=int) \
            if status == "Deprecated" else []
        entries[eid] = {
            "name": name, "status": status, "deprecated": status == "Deprecated",
            "desc": desc,
            "abstraction": el.get("Abstraction") or el.get("Weakness_Abstraction")
            or el.get("Pattern_Abstraction") or "",
            "parents": parents(el), "successors": succ,
        }
    if not rel_date:  # CWE 1.0 / CAPEC 1.0 carry no catalog date: use the newest content-history date
        dates = re.findall(rb"<(?:[a-z]+:)?Modification_Date>(\d{4}-\d{2}-\d{2})", raw)
        rel_date = max(dates).decode() if dates else None
        date_src = "max Modification_Date in file"
    # self-check: parsed entries against a raw count of entry tags in the text
    tag = ENTRY[vocab].encode()
    raw_n = len(re.findall(rb"<(?:[a-z]+:)?" + tag + rb"\s", raw))
    if raw_n != len(entries):
        log(f"  WARN {vocab} v{v}: parsed {len(entries)} entries, raw tag count {raw_n}")
    if not entries or not rel_date:
        log(f"  SKIP {vocab} v{v}: no entries or no date")
        return None
    live = [e for e in entries.values() if not e["deprecated"]]
    return {"version": v, "date": rel_date[:10], "date_source": date_src,
            "file": path.name, "bytes": path.stat().st_size,
            "n_entries": len(entries), "n_live": len(live),
            "n_deprecated": len(entries) - len(live),
            "has_hierarchy": any(e["parents"] for e in live),
            "has_abstraction": any(e["abstraction"] for e in live),
            "entries": entries}


# ----------------------------------------------------------------------
# measures
# ----------------------------------------------------------------------

def live_ids(s) -> set[str]:
    return {i for i, e in s["entries"].items() if not e["deprecated"]}


def stable_stats(a, b, ids: set[str]) -> dict:
    ea, eb = a["entries"], b["entries"]
    sims, edited, renamed, absch, parch = [], 0, 0, 0, 0
    for x in ids:
        da, db = ea[x]["desc"], eb[x]["desc"]
        if da != db:
            edited += 1
        sims.append(jaccard(tokens(da), tokens(db)))
        renamed += ea[x]["name"] != eb[x]["name"]
        if ea[x]["abstraction"] and eb[x]["abstraction"]:
            absch += ea[x]["abstraction"] != eb[x]["abstraction"]
        parch += ea[x]["parents"] != eb[x]["parents"]
    n = len(ids)
    hier = a["has_hierarchy"] and b["has_hierarchy"]
    abst = a["has_abstraction"] and b["has_abstraction"]
    moved = sum(1 for x in ids if (abst and ea[x]["abstraction"] and eb[x]["abstraction"]
                                   and ea[x]["abstraction"] != eb[x]["abstraction"])
                or (hier and ea[x]["parents"] != eb[x]["parents"]))
    sub = sum(1 for s in sims if s < 0.8)
    return {"id_stable": n, "desc_changed": edited,
            "desc_changed_frac": edited / n if n else None,
            "mean_token_jaccard": sum(sims) / n if n else None,
            "substantial_rewrites": sub, "substantial_frac": sub / n if n else None,
            "renamed": renamed, "renamed_frac": renamed / n if n else None,
            "abstraction_changed": absch if abst else None,
            "abstraction_changed_frac": (absch / n if n else None) if abst else None,
            "parent_changed": parch if hier else None,
            "parent_changed_frac": (parch / n if n else None) if hier else None,
            "structural_reassignment": moved if (abst or hier) else None,
            "structural_reassignment_frac": (moved / n if n else None) if (abst or hier) else None}


def churn(a, b) -> dict:
    la, lb = live_ids(a), live_ids(b)
    all_a, all_b = set(a["entries"]), set(b["entries"])
    newly_dep = {x for x in la if x in all_b and b["entries"][x]["deprecated"]}
    typed = {x for x in newly_dep if b["entries"][x]["successors"]}
    typed_live = {x for x in typed if any(s in lb for s in b["entries"][x]["successors"])}
    stable = la & lb
    row = {"from": a["version"], "to": b["version"], "from_date": a["date"], "to_date": b["date"],
           "years": round(years(a["date"], b["date"]), 2),
           "live_from": len(la), "live_to": len(lb),
           "added": len(lb - all_a), "revived": len(lb & (all_a - la)),
           "newly_deprecated": len(newly_dep), "typed_successor": len(typed),
           "typed_successor_live": len(typed_live),
           "absent": len(la - all_b), "surviving": len(stable),
           "jaccard_id": jaccard(la, lb)}
    row.update(stable_stats(a, b, stable))
    return row


def resolve(x: str, s, hops: int = 10) -> str | None:
    """Follow deprecation-note successors at release s until a live id."""
    seen = set()
    while x in s["entries"] and x not in seen and hops:
        if not s["entries"][x]["deprecated"]:
            return x
        seen.add(x)
        succ = s["entries"][x]["successors"]
        if len(succ) != 1:  # zero or several named ids: not a typed pointer
            return None
        x, hops = succ[0], hops - 1
    return None


def survival(a, b) -> dict:
    la, lb = live_ids(a), live_ids(b)
    dep = {x for x in la if x in b["entries"] and b["entries"][x]["deprecated"]}
    absent = la - set(b["entries"])
    rec = {x for x in dep if resolve(x, b) in lb}
    return {"src": a["version"], "tgt": b["version"], "src_date": a["date"], "tgt_date": b["date"],
            "years": round(years(a["date"], b["date"]), 2), "n": len(la),
            "live": len(la & lb), "deprecated": len(dep), "absent": len(absent),
            "recoverable_via_successor": len(rec),
            "survival_rate": len(la & lb) / len(la) if la else None}


def staleness(snaps: list[dict]) -> list[dict]:
    """Per cohort: first analysed release at which >= 10% of the cohort is
    hard-stale / semantically stale / substantively stale, plus the shares at
    the fixed HORIZON_YEARS mark (last analysed release within the horizon)."""
    out = []
    for i, a in enumerate(snaps):
        base = live_ids(a)
        curve = []
        for b in snaps[i + 1:]:
            lb = live_ids(b)
            hard = {x for x in base if x not in lb}
            st = stable_stats(a, b, base - hard)
            sem = len(hard) + sum(1 for x in base - hard if
                                  a["entries"][x]["desc"] != b["entries"][x]["desc"]
                                  or (a["has_hierarchy"] and b["has_hierarchy"]
                                      and a["entries"][x]["parents"] != b["entries"][x]["parents"])
                                  or (a["has_abstraction"] and b["has_abstraction"]
                                      and a["entries"][x]["abstraction"] and b["entries"][x]["abstraction"]
                                      and a["entries"][x]["abstraction"] != b["entries"][x]["abstraction"]))
            sub = len(hard) + sum(1 for x in base - hard if
                                  jaccard(tokens(a["entries"][x]["desc"]), tokens(b["entries"][x]["desc"])) < 0.8
                                  or (a["has_hierarchy"] and b["has_hierarchy"]
                                      and a["entries"][x]["parents"] != b["entries"][x]["parents"])
                                  or (a["has_abstraction"] and b["has_abstraction"]
                                      and a["entries"][x]["abstraction"] and b["entries"][x]["abstraction"]
                                      and a["entries"][x]["abstraction"] != b["entries"][x]["abstraction"]))
            curve.append({"tgt": b["version"], "years": round(years(a["date"], b["date"]), 2),
                          "hard": len(hard) / len(base), "sem": sem / len(base), "sub": sub / len(base),
                          "desc_changed_frac": st["desc_changed_frac"]})
        rec = {"src": a["version"], "src_date": a["date"], "n": len(base)}
        for k in ("hard", "sem", "sub"):
            hit = next((c for c in curve if c[k] >= 0.10), None)
            rec[f"t10_{k}"] = hit["years"] if hit else None
            rec[f"r10_{k}"] = hit["tgt"] if hit else None
        within = [c for c in curve if c["years"] <= HORIZON_YEARS]
        rec[f"at_{int(HORIZON_YEARS)}y"] = within[-1] if within and curve[-1]["years"] >= HORIZON_YEARS else None
        rec["final"] = curve[-1] if curve else None
        out.append(rec)
    return out


def analyse(vocab: str) -> dict:
    log(f"== {vocab}")
    snaps, skipped = [], []
    for v in VERSIONS[vocab]:
        p = fetch(vocab, v)
        s = parse(vocab, v, p) if p else None
        if s is None:
            skipped.append(v)
            continue
        log(f"  v{v:<6} {s['date']} ({s['date_source']}) {s['bytes']:>9} B  entries={s['n_entries']} "
            f"live={s['n_live']} deprecated={s['n_deprecated']} hierarchy={s['has_hierarchy']} "
            f"abstraction={s['has_abstraction']}")
        snaps.append(s)
    snaps.sort(key=lambda s: tuple(int(x) for x in s["version"].split(".")))
    newest = snaps[-1]
    ch = [churn(a, b) for a, b in zip(snaps, snaps[1:])]
    ev = [c for c in ch if c["jaccard_id"] < RESTRUCTURE_J]
    typed_total = sum(c["newly_deprecated"] for c in ch)
    typed_named = sum(c["typed_successor"] for c in ch)
    # typed retirement at the newest release, over every deprecated entry
    dep_new = [e for e in newest["entries"].values() if e["deprecated"]]
    dep_named = [e for e in dep_new if e["successors"]]
    dep_single = [e for e in dep_new if len(e["successors"]) == 1]
    return {
        "releases": [{k: s[k] for k in ("version", "date", "date_source", "file", "bytes",
                                        "n_entries", "n_live", "n_deprecated",
                                        "has_hierarchy", "has_abstraction")} for s in snaps],
        "skipped": skipped,
        "churn": ch,
        "survival": [survival(a, newest) for a in snaps],
        "semantic": [dict(src=a["version"], tgt=newest["version"], src_date=a["date"],
                          tgt_date=newest["date"], years=round(years(a["date"], newest["date"]), 2),
                          **stable_stats(a, newest, live_ids(a) & live_ids(newest))) for a in snaps[:-1]],
        "staleness": staleness(snaps),
        "recurrence": {"threshold": RESTRUCTURE_J, "n_events": len(ev), "n_transitions": len(ch),
                       "hazard_per_transition": len(ev) / len(ch),
                       "hazard_ci95": clopper_pearson(len(ev), len(ch)),
                       "observed_years": round(years(snaps[0]["date"], newest["date"]), 2),
                       "events": [{k: c[k] for k in ("from", "to", "to_date", "jaccard_id", "added",
                                                     "newly_deprecated", "absent")} for c in ev],
                       "min_jaccard": min(c["jaccard_id"] for c in ch)},
        "retirement": {"newly_deprecated_over_grid": typed_total,
                       "with_named_successor": typed_named,
                       "typed_frac": typed_named / typed_total if typed_total else None,
                       "deprecated_at_newest": len(dep_new),
                       "deprecated_at_newest_named": len(dep_named),
                       "deprecated_at_newest_single_successor": len(dep_single),
                       "deprecated_at_newest_named_frac": len(dep_named) / len(dep_new) if dep_new else None,
                       "successor_examples": [{"id": i, "name": e["name"][:60], "successors": e["successors"]}
                                              for i, e in sorted(newest["entries"].items(), key=lambda kv: int(kv[0]))
                                              if e["deprecated"]][:5]},
    }


# ----------------------------------------------------------------------
# ATT&CK Enterprise reference row (from existing results, not retyped)
# ----------------------------------------------------------------------

def nearest_cohort(rows, key_src, key_date, newest_date):
    target = date.fromisoformat(newest_date).toordinal() - HORIZON_YEARS * 365.25
    return min(rows, key=lambda r: abs(date.fromisoformat(r[key_date]).toordinal() - target))


def attack_tactic_reassignment(src: str, tgt: str) -> float | None:
    """Share of ID-stable techniques whose tactic set changed src->tgt. Needs
    the local ATT&CK database; returns None when it is not there."""
    try:
        sys.path.insert(0, str(ROOT / "code"))
        import attackdrift as ad
        con = ad.connect()
        a, b = (ad.load_snapshot(con, "enterprise-attack", v) for v in (src, tgt))
    except Exception as e:  # noqa: BLE001
        log(f"  tactic reassignment unavailable: {e}")
        return None
    stable = a.live_tech() & b.live_tech()
    tac = lambda o: set(filter(None, (o["tactics"] or "").split(",")))  # noqa: E731
    return sum(tac(a.tech[x]) != tac(b.tech[x]) for x in stable) / len(stable) if stable else None


def attack_row() -> dict:
    e123 = json.loads((RES / "e1_e2_e3.json").read_text())["enterprise-attack"]
    e12 = json.loads((RES / "e12_temporal_structure.json").read_text())
    e13 = json.loads((RES / "e13_tactic_layer.json").read_text())
    rel = e123["releases"]
    newest = rel[-1]["version"]
    surv = [s for s in e123["survival"] if s["tgt"] == newest]
    sem = [s for s in e123["semantic"] if s["tgt"] == newest]
    ev = [c for c in e123["churn"] if c["jaccard_id"] < RESTRUCTURE_J]
    last_ev = max(ev, key=lambda c: tuple(int(x) for x in c["to"].split("."))) if ev else None
    post = next((s for s in surv if s["src"] == last_ev["to"]), None) if last_ev else None
    h = nearest_cohort(sem, "src", "src_date", rel[-1]["date"])
    arity = e13["revocation_arity"]["enterprise-attack"]
    return {
        "label": "ATT&CK Enterprise", "n_releases": len(rel),
        "first": rel[0], "last": rel[-1], "span_years": round(years(rel[0]["date"], rel[-1]["date"]), 2),
        "survival_oldest": surv[0]["survival_rate"], "oldest_cohort": surv[0]["src"],
        "post_restructuring_survival": post["survival_rate"] if post else None,
        "post_restructuring_cohort": post["src"] if post else None,
        "n_events": len(ev), "n_transitions": len(e123["churn"]),
        "hazard_per_transition": len(ev) / len(e123["churn"]),
        "hazard_ci95": clopper_pearson(len(ev), len(e123["churn"])),
        "all_domain_events": e12["recurrence"]["n_events"],
        "all_domain_transitions": e12["recurrence"]["n_transitions"],
        "typed_retirement": "revoked-by edge, exactly one successor "
                            f"({arity['revocation_edges']} edges, {arity['sources_with_multiple_targets']} "
                            "with >1 target); deprecated: none",
        "horizon_cohort": h["src"], "horizon_cohort_date": h["src_date"], "horizon_years": round(years(h["src_date"], rel[-1]["date"]), 2),
        "horizon_id_stable": h["id_stable"],
        "horizon_desc_changed_frac": h["desc_changed_frac"],
        "horizon_mean_token_jaccard": h["mean_token_jaccard"],
        "horizon_substantial_frac": h["substantial_frac"],
        "horizon_structural_frac": attack_tactic_reassignment(h["src"], newest),
        "structural_definition": "tactic set changed",
        "sources": ["e1_e2_e3.json", "e12_temporal_structure.json", "e13_tactic_layer.json"],
    }


def vocab_row(label: str, r: dict, structural_def: str) -> dict:
    rel = r["releases"]
    newest_date = rel[-1]["date"]
    ev = r["recurrence"]["events"]
    post = next((s for s in r["survival"] if s["src"] == ev[-1]["to"]), None) if ev else None
    h = nearest_cohort(r["semantic"], "src", "src_date", newest_date)
    ret = r["retirement"]
    return {
        "label": label, "n_releases": len(rel), "first": rel[0], "last": rel[-1],
        "span_years": r["recurrence"]["observed_years"],
        "survival_oldest": r["survival"][0]["survival_rate"], "oldest_cohort": rel[0]["version"],
        "post_restructuring_survival": post["survival_rate"] if post else None,
        "post_restructuring_cohort": post["src"] if post else None,
        "n_events": r["recurrence"]["n_events"], "n_transitions": r["recurrence"]["n_transitions"],
        "hazard_per_transition": r["recurrence"]["hazard_per_transition"],
        "hazard_ci95": r["recurrence"]["hazard_ci95"],
        "typed_retirement": f"deprecated in place; note names a successor for "
                            f"{ret['deprecated_at_newest_named']}/{ret['deprecated_at_newest']} "
                            f"({ret['deprecated_at_newest_single_successor']} exactly one)",
        "horizon_cohort": h["src"], "horizon_cohort_date": h["src_date"], "horizon_years": h["years"],
        "horizon_id_stable": h["id_stable"],
        "horizon_desc_changed_frac": h["desc_changed_frac"],
        "horizon_mean_token_jaccard": h["mean_token_jaccard"],
        "horizon_substantial_frac": h["substantial_frac"],
        "horizon_structural_frac": h["structural_reassignment_frac"],
        "structural_definition": structural_def,
    }


# ----------------------------------------------------------------------
# outputs
# ----------------------------------------------------------------------

def f3(x):
    return "n/a" if x is None else f"{x:.3f}"


def table(rows: list[dict]) -> str:
    out = ["| Vocabulary | Releases analysed | Span | Survival, oldest cohort → newest | "
           "Post-restructuring survival | Restructuring events / transitions (hazard, 95% CI) | "
           "Typed successor on retirement? | Horizon cohort (years) | Stable IDs with edited description | "
           "Substantial rewrite (J<0.8) | Structural reassignment |",
           "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        ci = r["hazard_ci95"]
        post = (f"{f3(r['post_restructuring_survival'])} (v{r['post_restructuring_cohort']} cohort)"
                if r["post_restructuring_survival"] is not None else "no event")
        out.append(
            f"| {r['label']} | {r['n_releases']} | v{r['first']['version']} ({r['first']['date']}) → "
            f"v{r['last']['version']} ({r['last']['date']}), {r['span_years']:.1f} y | "
            f"{f3(r['survival_oldest'])} (v{r['oldest_cohort']}) | {post} | "
            f"{r['n_events']} / {r['n_transitions']} ({r['hazard_per_transition']:.3f}, {ci[0]:.3f}–{ci[1]:.3f}) | "
            f"{r['typed_retirement']} | v{r['horizon_cohort']} → v{r['last']['version']} ({r['horizon_years']:.1f} y, "
            f"n={r['horizon_id_stable']}) | {f3(r['horizon_desc_changed_frac'])} | "
            f"{f3(r['horizon_substantial_frac'])} | {f3(r['horizon_structural_frac'])} ({r['structural_definition']}) |")
    out.append("")
    out.append(f"Horizon: the analysed cohort nearest {HORIZON_YEARS:.0f} years before each vocabulary's newest "
               "release, measured at that newest release over identifier-stable, non-deprecated entries. "
               "Restructuring event: identifier-set Jaccard < 0.80 between consecutive analysed releases, "
               "deprecated entries treated as absent. ATT&CK all-domain recurrence: "
               f"{rows[0]['all_domain_events']} events / {rows[0]['all_domain_transitions']} transitions.")
    return "\n".join(out)


def figure(cwe: dict, capec: dict, e123_ent: dict) -> None:
    from matplotlib import pyplot as plt
    plt.rcParams.update({
        "figure.dpi": 160, "savefig.dpi": 300, "font.size": 8,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.alpha": 0.25, "grid.linewidth": 0.5,
        "legend.frameon": False, "figure.constrained_layout.use": True,
    })
    C = {"a": "#1b4965", "b": "#c1666b", "c": "#5f8d4e", "d": "#d08c34", "e": "#7d6b91"}
    fig, ax = plt.subplots(1, 2, figsize=(6.4, 2.5))
    # left: the referential clock, identifier Jaccard per transition against release date
    for lab, ch, col, mk in (("ATT&CK Enterprise", e123_ent["churn"], C["a"], "o"),
                             ("CWE", cwe["churn"], C["c"], "s"),
                             ("CAPEC", capec["churn"], C["d"], "^")):
        ax[0].plot([date.fromisoformat(c["to_date"]) for c in ch], [c["jaccard_id"] for c in ch],
                   mk + "-", color=col, ms=3, lw=1.2, label=lab)
    ax[0].axhline(RESTRUCTURE_J, color="k", lw=0.7, ls="--")
    ax[0].set_ylim(0, 1.02)
    ax[0].set_ylabel("identifier-set Jaccard, consecutive releases")
    ax[0].tick_params(axis="x", rotation=45, labelsize=6)
    ax[0].legend(fontsize=6, loc="lower right")
    ax[0].set_title("the referential clock", fontsize=7)
    # right: the intensional clock, description-edited share of each cohort at the newest release
    newest = e123_ent["releases"][-1]["version"]
    sem_att = [s for s in e123_ent["semantic"] if s["tgt"] == newest]
    for lab, sem, col, mk in (("ATT&CK Enterprise", sem_att, C["a"], "o"),
                              ("CWE", cwe["semantic"], C["c"], "s"),
                              ("CAPEC", capec["semantic"], C["d"], "^")):
        ax[1].plot([years(s["src_date"], s["tgt_date"]) for s in sem],
                   [s["desc_changed_frac"] for s in sem], mk + "-", color=col, ms=3, lw=1.2, label=lab)
        ax[1].plot([years(s["src_date"], s["tgt_date"]) for s in sem],
                   [s["substantial_frac"] for s in sem], mk + ":", color=col, ms=2.5, lw=1.0, alpha=0.7)
    ax[1].set_xlabel("cohort age at the newest release (years)")
    ax[1].set_ylabel("share of identifier-stable entries")
    ax[1].set_ylim(0, 1.02)
    ax[1].legend(fontsize=6, loc="lower right", title="solid: edited; dotted: J<0.8", title_fontsize=5.5)
    ax[1].set_title("the intensional clock", fontsize=7)
    fig.savefig(FIG / "fig10_cwe_capec.pdf")
    fig.savefig(FIG / "fig10_cwe_capec.png")
    plt.close(fig)


def main() -> None:
    RES.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)
    TAB.mkdir(parents=True, exist_ok=True)
    cwe, capec = analyse("cwe"), analyse("capec")
    rows = [attack_row(),
            vocab_row("CWE", cwe, "abstraction level or ChildOf parent (view 1000) changed"),
            vocab_row("CAPEC", capec, "abstraction level or ChildOf parent changed")]
    out = {"seed": SEED, "horizon_years": HORIZON_YEARS, "restructure_jaccard": RESTRUCTURE_J,
           "versions_requested": VERSIONS, "comparison": rows, "cwe": cwe, "capec": capec}
    (RES / "e22_cwe_capec.json").write_text(json.dumps(out, indent=1))
    (TAB / "t24_cwe_capec.md").write_text(table(rows) + "\n")
    figure(cwe, capec, json.loads((RES / "e1_e2_e3.json").read_text())["enterprise-attack"])
    for r in rows:
        log(f"{r['label']:<18} releases={r['n_releases']} survival(oldest)={f3(r['survival_oldest'])} "
            f"events={r['n_events']}/{r['n_transitions']} horizon v{r['horizon_cohort']}: "
            f"edited={f3(r['horizon_desc_changed_frac'])} sub={f3(r['horizon_substantial_frac'])} "
            f"struct={f3(r['horizon_structural_frac'])}")
    log(f"wrote {RES/'e22_cwe_capec.json'}, {TAB/'t24_cwe_capec.md'}, {FIG/'fig10_cwe_capec.png'}")


if __name__ == "__main__":
    main()
