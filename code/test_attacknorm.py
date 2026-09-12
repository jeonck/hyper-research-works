#!/usr/bin/env python3
"""Self-check for attacknorm.py: .venv/bin/python code/test_attacknorm.py

Plain asserts. External corpora are skipped when absent; the paper's worked
counter-example (T1562 -> T1685 must be a level change, not a clean keep) and
the format readers run unconditionally.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import attackdrift as ad  # noqa: E402
import attacknorm as an  # noqa: E402

EXT = Path(os.environ.get("HYPER_EXT", "/Users/mac/ws/ext"))
NAV = Path(os.environ.get("ATTACK_NAVIGATOR", "/Users/mac/ws/mitre-attack/attack-navigator"))
TMP = Path(tempfile.mkdtemp())


def run(path: Path, **kw) -> dict:
    args = argparse.Namespace(domain="enterprise-attack", format=None, from_release=None,
                              to="19.2", rollup=False, bundle_hash=False)
    vars(args).update(kw)
    return an.analyse(ad.connect(), path, args)


def check_counterexample() -> None:
    p = TMP / "one.txt"
    p.write_text("see T1562 for details\n")
    r = run(p)
    L = r["ledger"]
    assert L["input"] == 1 and L["kept"] == 1 and L["dropped"] == 0, L
    d = L["detail"]["demoted"]
    assert d == {"T1562": {"to": "T1685", "direction": "parent→sub-technique",
                           "via_former_child": "T1562.001"}}, d
    # the library's dotted-id rule alone does NOT flag this; the tool must
    res = ad.normalize_with_ledger({"T1562"}, ad.load_snapshot(ad.connect(), "enterprise-attack", "19.2"))
    assert res.kept == {"T1562": "T1685"} and not res.demoted
    assert "T1562 → T1685" in an.render_text(r)
    print("ok  counter-example: T1562 -> T1685 reported as parent->sub-technique via T1562.001")


def check_readers() -> None:
    nav = TMP / "layer.json"
    nav.write_text(json.dumps({"name": "x", "domain": "enterprise-attack",
                               "versions": {"attack": "17"},
                               "techniques": [{"techniqueID": "T1562.001"}, {"techniqueID": "T1059"}]}))
    r = run(nav)
    assert r["format"] == "navigator" and r["declared_release"] == "17"
    assert r["source_release"]["release"] == "17.0" and r["source_release"]["live_at_release"] == 2
    assert r["ledger"]["detail"]["demoted"]["T1562.001"]["direction"] == "sub-technique→parent"
    tram = TMP / "tram.json"
    tram.write_text(json.dumps({"sentences": [{"mappings": [{"attack_id": "T1095"}, {"attack_id": "T1064"}]}]}))
    r = run(tram)
    assert r["format"] == "tram" and r["ledger"]["detail"]["dropped"] == {"T1064": "deprecated"}
    tsv = TMP / "b.tsv"
    tsv.write_text("URL\tPlatform\tGT\nu\tEnterprise\tT1059, T1089\nu\tMobile\tT1404\n")
    r = run(tsv)
    assert r["format"] == "ctibench" and r["ledger"]["input"] == 2 and r["notes"]
    assert r["ledger"]["detail"]["resolved"] == {"T1089": "T1685"}
    wide = TMP / "w.csv"
    wide.write_text("Text,T1059,T1089,T9000\n\"a\",1,0,1\n")
    r = run(wide)
    assert r["format"] == "wide-csv" and r["ledger"]["detail"]["ids_in"] == ["T1059", "T9000"]
    assert r["ledger"]["detail"]["dropped"] == {"T9000": "absent"}
    print("ok  readers: navigator / tram / ctibench / wide-csv")


def check_rcatt() -> None:
    p = EXT / "rcATT/classification_tools/data/training_data_original.csv"
    if not p.exists():
        print("skip rcATT (file absent)"); return
    r = run(p)
    L = r["ledger"]
    assert L["input"] == 215, L
    assert L["kept_via_revocation_chain"] + L["dropped"] == 107, L   # invalid at v19.2 (e7)
    assert L["kept_via_revocation_chain"] == 99 and L["dropped"] == 8, L  # repairable / not (e7)
    assert L["merge_targets"] == 7 and L["absorbed_by_merges"] == 15 and L["distinct_after"] == 199  # e17
    assert L["demoted"] >= 88, L                                          # e17 dotted-rule count
    assert r["source_release"]["consistent_releases"][0] == "4.0"
    assert r["source_release"]["consistent_releases"][-1] == "6.3"
    print("ok  rcATT matches e7/e17: 215 ids, 107 invalid, 99 repaired, 8 dropped, 199 after")


def check_ctibench() -> None:
    p = EXT / "cti-bench/data/cti-ate.tsv"
    if not p.exists():
        print("skip CTIBench (file absent)"); return
    r = run(p)
    L = r["ledger"]
    assert L["input"] == 84 and L["dropped"] == 7 and L["kept_via_revocation_chain"] == 1, L
    assert r["source_release"]["consistent_releases"] == []          # e7: no consistent release
    assert set(L["detail"]["dropped"].values()) == {"absent"}         # Mobile ids in Enterprise rows
    print("ok  CTIBench: 84 enterprise ids, 7 absent (mobile ids), T1562 repaired, no provenance interval")


def check_layers() -> None:
    bear = NAV / "layers/samples/Bear_APT.json"
    if bear.exists():
        r = run(bear)
        assert r["declared_release"] == "17" and r["source_release"]["release"] == "17.0"
        assert r["ledger"]["input"] == 126 and r["ledger"]["dropped"] == 0
        print("ok  Navigator sample layer declares attack 17 -> v17.0; 126 ids, 0 dropped")
    else:
        print("skip Navigator sample (absent)")
    det = EXT / "DeTTECT/threat-actor-data/ATT&CK-Navigator-layers"
    layers = sorted(det.glob("*/*.json")) if det.exists() else []
    if layers:
        r = run(layers[0])
        assert r["format"] == "navigator" and r["declared_release"] is None
        assert r["ledger"]["kept"] + r["ledger"]["dropped"] == r["ledger"]["input"] > 0
        print(f"ok  DeTTECT layer {layers[0].name[:40]}...: no declared release, {r['ledger']['input']} ids")
    else:
        print("skip DeTTECT layers (absent)")


def check_cli() -> None:
    out = TMP / "o.json"
    a, b = TMP / "one.txt", TMP / "layer.json"
    assert an.main(["--input", str(a), "--compare", str(b), "--to", "19.2", "--json", str(out)]) == 0
    j = json.loads(out.read_text())
    assert j["comparison"]["reference_release"] == "19.2" and j["comparison"]["overlap_after"] == 1
    assert an.main(["--input", str(a), "--markdown"]) == 0
    assert an.main(["--input", str(TMP / "missing.txt")]) == 2
    print("ok  cli: compare + json + markdown, exit 2 on unreadable input")


if __name__ == "__main__":
    check_counterexample()
    check_readers()
    check_rcatt()
    check_ctibench()
    check_layers()
    check_cli()
    print("all checks passed")
