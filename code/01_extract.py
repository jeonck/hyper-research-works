#!/usr/bin/env python3
"""Extract a normalized longitudinal database from every public ATT&CK STIX release.

Input : a local clone of github.com/mitre-attack/attack-stix-data
Output: data/attack_drift.db (SQLite)

Tables
------
releases(domain, version, ordinal, released, n_objects)
objects(domain, version, stix_id, otype, attack_id, name, is_subtechnique,
        revoked, deprecated, obj_version, created, modified, tactics,
        platforms, desc_sha, desc_len, det_sha, det_len)
descriptions(domain, version, stix_id, description, detection)
relationships(domain, version, stix_id, rel_type, source_ref, target_ref,
              created, modified, has_desc)
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sqlite3
import sys
from pathlib import Path

REPO = Path(os.environ.get("ATTACK_STIX_REPO", "/home/user/mitre-attack/attack-stix-data"))
OUT = Path(__file__).resolve().parents[1] / "data" / "attack_drift.db"
DOMAINS = ["enterprise-attack", "mobile-attack", "ics-attack"]

SCHEMA = """
DROP TABLE IF EXISTS releases;
DROP TABLE IF EXISTS objects;
DROP TABLE IF EXISTS descriptions;
DROP TABLE IF EXISTS relationships;
CREATE TABLE releases(
  domain TEXT, version TEXT, ordinal INTEGER, released TEXT, n_objects INTEGER,
  PRIMARY KEY(domain, version));
CREATE TABLE objects(
  domain TEXT, version TEXT, stix_id TEXT, otype TEXT, attack_id TEXT, name TEXT,
  is_subtechnique INTEGER, revoked INTEGER, deprecated INTEGER, obj_version TEXT,
  created TEXT, modified TEXT, tactics TEXT, platforms TEXT,
  desc_sha TEXT, desc_len INTEGER, det_sha TEXT, det_len INTEGER);
CREATE TABLE descriptions(
  domain TEXT, version TEXT, stix_id TEXT, description TEXT, detection TEXT);
CREATE TABLE relationships(
  domain TEXT, version TEXT, stix_id TEXT, rel_type TEXT, source_ref TEXT,
  target_ref TEXT, created TEXT, modified TEXT, has_desc INTEGER);
"""

INDEXES = """
CREATE INDEX ix_obj_dv ON objects(domain, version);
CREATE INDEX ix_obj_aid ON objects(domain, attack_id);
CREATE INDEX ix_obj_sid ON objects(domain, version, stix_id);
CREATE INDEX ix_rel_dv ON relationships(domain, version);
CREATE INDEX ix_rel_type ON relationships(domain, version, rel_type);
CREATE INDEX ix_desc ON descriptions(domain, version, stix_id);
"""


def sha(text: str | None) -> tuple[str | None, int]:
    if not text:
        return None, 0
    norm = re.sub(r"\s+", " ", text).strip()
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()[:16], len(norm)


def attack_id_of(obj: dict) -> str | None:
    for ref in obj.get("external_references", []) or []:
        if ref.get("source_name") in {
            "mitre-attack", "mitre-mobile-attack", "mitre-ics-attack",
        } and ref.get("external_id"):
            return ref["external_id"]
    return None


def version_key(v: str) -> tuple:
    return tuple(int(x) for x in v.split("."))


def release_files(domain: str) -> list[tuple[str, Path]]:
    """Stable releases only.

    The repository also ships pre-release bundles (Mobile 11.0-beta, 11.1-beta,
    11.2-beta). They are excluded: they were never the published vocabulary any
    CTI artefact could have been authored against. 109 bundles are published in
    total; 106 are stable and analysed here.
    """
    d = REPO / domain
    out = []
    for p in d.glob(f"{domain}-*.json"):
        m = re.match(rf"{re.escape(domain)}-(\d+(?:\.\d+)*)\.json$", p.name)
        if m:
            out.append((m.group(1), p))
    return sorted(out, key=lambda t: version_key(t[0]))


def release_dates(domain: str) -> dict[str, str]:
    idx = json.loads((REPO / "index.json").read_text())
    want = {"enterprise-attack": "Enterprise ATT&CK",
            "mobile-attack": "Mobile ATT&CK",
            "ics-attack": "ICS ATT&CK"}[domain]
    for col in idx["collections"]:
        if col["name"] == want:
            return {v["version"]: v["modified"] for v in col["versions"]}
    return {}


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(OUT)
    con.executescript(SCHEMA)

    for domain in DOMAINS:
        if not (REPO / domain).exists():
            print(f"skip {domain}: not present", file=sys.stderr)
            continue
        dates = release_dates(domain)
        files = release_files(domain)
        print(f"{domain}: {len(files)} releases", file=sys.stderr)
        for ordinal, (version, path) in enumerate(files):
            bundle = json.loads(path.read_text())
            objs, rels, descs = [], [], []
            for o in bundle.get("objects", []):
                t = o.get("type")
                if t == "relationship":
                    rels.append((
                        domain, version, o["id"], o.get("relationship_type"),
                        o.get("source_ref"), o.get("target_ref"),
                        o.get("created"), o.get("modified"),
                        1 if o.get("description") else 0,
                    ))
                    continue
                if t in {"marking-definition", "identity"}:
                    continue
                desc = o.get("description")
                det = o.get("x_mitre_detection")
                dsha, dlen = sha(desc)
                tsha, tlen = sha(det)
                tactics = ",".join(
                    kc.get("phase_name", "") for kc in o.get("kill_chain_phases", []) or []
                )
                platforms = ",".join(o.get("x_mitre_platforms", []) or [])
                objs.append((
                    domain, version, o["id"], t, attack_id_of(o), o.get("name"),
                    1 if o.get("x_mitre_is_subtechnique") else 0,
                    1 if o.get("revoked") else 0,
                    1 if o.get("x_mitre_deprecated") else 0,
                    o.get("x_mitre_version"), o.get("created"), o.get("modified"),
                    tactics, platforms, dsha, dlen, tsha, tlen,
                ))
                if desc or det:
                    descs.append((domain, version, o["id"], desc, det))

            con.execute(
                "INSERT OR REPLACE INTO releases VALUES (?,?,?,?,?)",
                (domain, version, ordinal, dates.get(version), len(bundle.get("objects", []))),
            )
            con.executemany("INSERT INTO objects VALUES (" + ",".join("?" * 18) + ")", objs)
            con.executemany("INSERT INTO descriptions VALUES (?,?,?,?,?)", descs)
            con.executemany("INSERT INTO relationships VALUES (?,?,?,?,?,?,?,?,?)", rels)
            con.commit()
            print(f"  {domain} v{version}: {len(objs)} objects, {len(rels)} relationships",
                  file=sys.stderr)

    con.executescript(INDEXES)
    con.commit()
    con.close()
    print(f"wrote {OUT} ({OUT.stat().st_size / 1e6:.1f} MB)", file=sys.stderr)


if __name__ == "__main__":
    main()
