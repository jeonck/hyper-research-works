"""Shared loading + lineage utilities for the ATT&CK ontology-drift study."""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

DB = Path(__file__).resolve().parents[1] / "data" / "attack_drift.db"

TECH = "attack-pattern"
GROUP = "intrusion-set"
SOFTWARE = ("malware", "tool")


def connect() -> sqlite3.Connection:
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con


@dataclass
class Release:
    domain: str
    version: str
    ordinal: int
    released: str

    @property
    def date(self) -> str:
        return (self.released or "")[:10]


def releases(con: sqlite3.Connection, domain: str) -> list[Release]:
    rows = con.execute(
        "SELECT domain, version, ordinal, released FROM releases "
        "WHERE domain=? ORDER BY ordinal", (domain,)).fetchall()
    return [Release(r["domain"], r["version"], r["ordinal"], r["released"]) for r in rows]


def major_releases(con: sqlite3.Connection, domain: str) -> list[Release]:
    """One release per major version (the .0 release, or the earliest available)."""
    out: dict[int, Release] = {}
    for r in releases(con, domain):
        major = int(r.version.split(".")[0])
        if major not in out:
            out[major] = r
    return [out[k] for k in sorted(out)]


@dataclass
class Snapshot:
    """One ATT&CK release, indexed for analysis."""
    domain: str
    version: str
    released: str
    # attack_id -> record
    tech: dict[str, dict] = field(default_factory=dict)
    groups: dict[str, dict] = field(default_factory=dict)
    software: dict[str, dict] = field(default_factory=dict)
    by_stix: dict[str, dict] = field(default_factory=dict)
    # relationship_type -> list[(source_stix, target_stix)]
    rels: dict[str, list[tuple[str, str]]] = field(default_factory=dict)

    # --- derived views -------------------------------------------------
    def live_tech(self) -> set[str]:
        return {a for a, o in self.tech.items() if not o["revoked"] and not o["deprecated"]}

    def sub_of(self) -> dict[str, str]:
        """child attack_id -> parent attack_id (from subtechnique-of relationships)."""
        out = {}
        for s, t in self.rels.get("subtechnique-of", []):
            so, to = self.by_stix.get(s), self.by_stix.get(t)
            if so and to and so["attack_id"] and to["attack_id"]:
                out[so["attack_id"]] = to["attack_id"]
        # fall back to the dotted-ID convention for releases that omit the relationship
        for aid in self.tech:
            if "." in aid and aid not in out:
                out[aid] = aid.split(".")[0]
        return out

    def revoked_by(self) -> dict[str, str]:
        """revoked attack_id -> replacement attack_id."""
        out = {}
        for s, t in self.rels.get("revoked-by", []):
            so, to = self.by_stix.get(s), self.by_stix.get(t)
            if so and to and so["attack_id"] and to["attack_id"]:
                out[so["attack_id"]] = to["attack_id"]
        return out

    def group_techniques(self, include_software: bool = False) -> dict[str, set[str]]:
        """group attack_id -> set of technique attack_ids (direct `uses` edges)."""
        prof: dict[str, set[str]] = {}
        for s, t in self.rels.get("uses", []):
            so, to = self.by_stix.get(s), self.by_stix.get(t)
            if not so or not to:
                continue
            if so["otype"] != GROUP or to["otype"] != TECH:
                continue
            if not so["attack_id"] or not to["attack_id"]:
                continue
            prof.setdefault(so["attack_id"], set()).add(to["attack_id"])
        if include_software:
            sw_tech: dict[str, set[str]] = {}
            for s, t in self.rels.get("uses", []):
                so, to = self.by_stix.get(s), self.by_stix.get(t)
                if so and to and so["otype"] in SOFTWARE and to["otype"] == TECH \
                        and so["attack_id"] and to["attack_id"]:
                    sw_tech.setdefault(so["stix_id"], set()).add(to["attack_id"])
            for s, t in self.rels.get("uses", []):
                so, to = self.by_stix.get(s), self.by_stix.get(t)
                if so and to and so["otype"] == GROUP and to["otype"] in SOFTWARE \
                        and so["attack_id"]:
                    prof.setdefault(so["attack_id"], set()).update(
                        sw_tech.get(to["stix_id"], set()))
        return prof


def load_snapshot(con: sqlite3.Connection, domain: str, version: str,
                  with_desc: bool = False) -> Snapshot:
    rel_row = con.execute(
        "SELECT released FROM releases WHERE domain=? AND version=?",
        (domain, version)).fetchone()
    snap = Snapshot(domain, version, rel_row["released"] if rel_row else "")
    rows = con.execute(
        "SELECT stix_id, otype, attack_id, name, is_subtechnique, revoked, deprecated, "
        "obj_version, created, modified, tactics, platforms, desc_sha, desc_len, "
        "det_sha, det_len FROM objects WHERE domain=? AND version=?",
        (domain, version)).fetchall()
    for r in rows:
        o = dict(r)
        snap.by_stix[o["stix_id"]] = o
        aid = o["attack_id"]
        if not aid:
            continue
        if o["otype"] == TECH:
            snap.tech.setdefault(aid, o)
        elif o["otype"] == GROUP:
            snap.groups.setdefault(aid, o)
        elif o["otype"] in SOFTWARE:
            snap.software.setdefault(aid, o)
    for r in con.execute(
            "SELECT rel_type, source_ref, target_ref FROM relationships "
            "WHERE domain=? AND version=?", (domain, version)):
        snap.rels.setdefault(r["rel_type"], []).append((r["source_ref"], r["target_ref"]))
    if with_desc:
        for r in con.execute(
                "SELECT stix_id, description, detection FROM descriptions "
                "WHERE domain=? AND version=?", (domain, version)):
            if r["stix_id"] in snap.by_stix:
                snap.by_stix[r["stix_id"]]["description"] = r["description"]
                snap.by_stix[r["stix_id"]]["detection"] = r["detection"]
    return snap


# ----------------------------------------------------------------------
# Normalization (the ATT&CK-Norm protocol evaluated in the paper)
# ----------------------------------------------------------------------

def resolve_chain(aid: str, revoked_map: dict[str, str], max_hops: int = 10) -> str:
    """Follow revoked-by edges transitively to a terminal identifier."""
    seen = {aid}
    cur = aid
    for _ in range(max_hops):
        nxt = revoked_map.get(cur)
        if not nxt or nxt in seen:
            break
        seen.add(nxt)
        cur = nxt
    return cur


def normalize(ids: set[str], target: Snapshot, *, rollup: bool = True) -> set[str]:
    """Map a set of ATT&CK technique IDs onto a target release.

    1. transitive revoked-by resolution (uses the target release's revocation graph)
    2. drop identifiers that are deprecated or absent in the target
    3. optional roll-up of orphaned sub-technique IDs to their surviving parent
    """
    rev = target.revoked_by()
    sub = target.sub_of()
    live = target.live_tech()
    out: set[str] = set()
    for aid in ids:
        cur = resolve_chain(aid, rev)
        if cur in live:
            out.add(cur)
            continue
        if rollup:
            parent = sub.get(cur) or (cur.split(".")[0] if "." in cur else None)
            if parent:
                parent = resolve_chain(parent, rev)
                if parent in live:
                    out.add(parent)
    return out


def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)
