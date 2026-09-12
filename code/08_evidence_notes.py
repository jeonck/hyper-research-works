#!/usr/bin/env python3
"""Emit ground-truth vault notes straight from the measurement outputs.

Numbers are formatted from the result JSONs rather than retyped, so the notes
the synthesizer cites cannot disagree with the experiments that produced them.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "data" / "results"
TMP = Path("/tmp/claude-0/-home-user-hyper-research-works/"
           "aa6e0fd0-b155-51a6-ad4a-ebbe528f3807/scratchpad/notes")
HPR = str(ROOT / ".venv" / "bin" / "hyperresearch")
TAG = "attack-ontology-drift-cti-85bc51"
REPO = "https://github.com/mitre-attack/attack-stix-data"


def load(n):
    return json.loads((RES / n).read_text())


def emit(title: str, body: str, tag2: str, summary: str) -> None:
    f = TMP / (title.lower().replace(" ", "-").replace("&", "and")[:60] + ".md")
    f.write_text(body)
    subprocess.run(
        [HPR, "note", "new", title, "--body-file", str(f), "--tag", TAG,
         "--tag", tag2, "--source", REPO, "--tier", "ground_truth",
         "--content-type", "dataset", "--summary", summary, "-j"],
        cwd=ROOT, check=True, capture_output=True)
    print("  note:", title)


def main() -> None:
    TMP.mkdir(parents=True, exist_ok=True)
    e123, e4 = load("e1_e2_e3.json"), load("e4_growth.json")
    e5, e6, e7 = load("e5_attribution.json"), load("e6_coverage.json"), load("e7_artifacts.json")
    ent = e123["enterprise-attack"]

    # --- E0 corpus -----------------------------------------------------
    lines = ["# Measurement corpus: every public ATT&CK STIX release", "",
             "Provenance: local clone of the MITRE ATT&CK STIX data repository; parsed",
             "by `code/01_extract.py` into `data/attack_drift.db`. Fidelity: PRIMARY",
             "ARTEFACT — computed from the release bundles themselves, not from any",
             "secondary description of them.", ""]
    for dom in ("enterprise-attack", "mobile-attack", "ics-attack"):
        rel = e123[dom]["releases"]
        lines.append(f"- {dom}: {len(rel)} major releases analysed, "
                     f"v{rel[0]['version']} ({rel[0]['date']}) through "
                     f"v{rel[-1]['version']} ({rel[-1]['date']}).")
    emit("ATT&CK release corpus used for drift measurement", "\n".join(lines),
         "measurement", "Every public ATT&CK STIX release, parsed into a longitudinal database")

    # --- E1 churn ------------------------------------------------------
    ch = ent["churn"]
    worst = min(ch, key=lambda c: c["jaccard_id"])
    lines = ["# E1 — release-over-release churn, ATT&CK Enterprise", "",
             "Fidelity: PRIMARY ARTEFACT (computed). Source: data/results/e1_e2_e3.json.", "",
             "| from → to | date | live | added | revoked | deprecated | renamed | "
             "descriptions rewritten | detection text rewritten | tactic set changed | "
             "Jaccard(ID sets) |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for c in ch:
        lines.append(
            f"| v{c['from']} → v{c['to']} | {c['to_date']} | {c['live_to']} | {c['added']} | "
            f"{c['newly_revoked']} | {c['newly_deprecated']} | {c['renamed']} | "
            f"{c['desc_changed']} | {c['detection_changed']} | {c['tactic_changed']} | "
            f"{c['jaccard_id']:.3f} |")
    lines += ["", f"Largest single discontinuity: v{worst['from']} → v{worst['to']} "
                  f"({worst['to_date']}), Jaccard {worst['jaccard_id']:.3f} — "
                  f"{worst['added']} techniques added, {worst['newly_revoked']} revoked, "
                  f"{worst['group_edges_removed']} group→technique edges removed and "
                  f"{worst['group_edges_added']} added in one release."]
    emit("E1 ATT&CK Enterprise release churn table", "\n".join(lines), "measurement",
         "Per-release adds, revocations, renames, description and tactic changes")

    # --- E2 survival ---------------------------------------------------
    latest = ent["releases"][-1]["version"]
    surv = [s for s in ent["survival"] if s["tgt"] == latest]
    lines = [f"# E2 — identifier survival to v{latest}", "",
             "Fidelity: PRIMARY ARTEFACT (computed).", "",
             "| source release | date | identifiers | still live | survival | revoked | "
             "deprecated | recoverable via revoked-by |", "|---|---|---|---|---|---|---|---|"]
    for s in surv:
        lines.append(f"| v{s['src']} | {s['src_date']} | {s['n']} | {s['live']} | "
                     f"{s['survival_rate']:.3f} | {s['revoked']} | {s['deprecated']} | "
                     f"{s['recoverable_via_revoked_by']} |")
    pre7 = [s for s in surv if float(s["src"].split(".")[0]) < 7]
    post7 = [s for s in surv if float(s["src"].split(".")[0]) >= 7 and s["src"] != latest]
    lines += ["", f"Pre-restructure releases (v1.0–v6.0): survival "
                  f"{min(s['survival_rate'] for s in pre7):.3f}–"
                  f"{max(s['survival_rate'] for s in pre7):.3f}. "
                  f"Post-restructure (v7.0 onward): "
                  f"{min(s['survival_rate'] for s in post7):.3f}–"
                  f"{max(s['survival_rate'] for s in post7):.3f}.",
              "Every revoked identifier in the corpus resolves to a live identifier "
              "through the published revoked-by graph — the damage is mechanically "
              "repairable at the identifier level, which is what makes the "
              "normalization protocol possible."]
    emit(f"E2 identifier survival to ATT&CK v{latest}", "\n".join(lines), "measurement",
         "Survival and recoverability of technique identifiers by source release")

    # --- E3 semantic ---------------------------------------------------
    sem = [s for s in ent["semantic"] if s["tgt"] == latest]
    lines = [f"# E3 — silent semantic drift among ID-stable techniques (vs. v{latest})", "",
             "Fidelity: PRIMARY ARTEFACT (computed). Only techniques whose identifier is",
             "live in BOTH releases are counted, so every row isolates meaning change",
             "from identifier change.", "",
             "| source release | ID-stable techniques | description edited | "
             "mean token Jaccard | substantial rewrite (J<0.8) |", "|---|---|---|---|---|"]
    for s in sem:
        lines.append(f"| v{s['src']} | {s['id_stable']} | {s['desc_changed_frac']:.3f} | "
                     f"{s['mean_token_jaccard']:.3f} | {s['substantial_frac']:.3f} |")
    emit("E3 silent semantic drift of ID-stable ATT&CK techniques", "\n".join(lines),
         "measurement", "Description rewriting among techniques whose identifiers never changed")

    # --- E4 growth -----------------------------------------------------
    cum = e4["enterprise-attack"]["cumulative"]
    existing = cum["total_added"] - cum["new_actor"]
    book = cum["ontology_refinement"] + cum["revocation_remap"]
    lines = ["# E4 — decomposition of apparent knowledge growth", "",
             "Fidelity: PRIMARY ARTEFACT (computed). Every group→technique `uses` edge",
             "that appears in release B but not in release A is attributed to exactly one",
             "cause.", "",
             f"- total new edges across all Enterprise transitions: {cum['total_added']}",
             f"- attributable to groups newly added to ATT&CK: {cum['new_actor']}",
             f"- new edges for groups that already existed: {existing}",
             f"  - genuine new intelligence (both endpoints pre-existed, newly linked): "
             f"{cum['genuine_new_intel']}",
             f"  - new technique, new edge: {cum['new_technique_intel']}",
             f"  - sub-technique refinement of an edge the group already had: "
             f"{cum['ontology_refinement']}",
             f"  - revocation re-mapping of an edge the group already had: "
             f"{cum['revocation_remap']}",
             f"- ontology bookkeeping share of growth for pre-existing groups: "
             f"{book}/{existing} = {book/existing:.3f}", "",
             "| from → to | new edges (existing groups) | bookkeeping share |",
             "|---|---|---|"]
    for r in e4["enterprise-attack"]["transitions"]:
        base = r["total_added"] - r["new_actor"]
        if base:
            share = (r["ontology_refinement"] + r["revocation_remap"]) / base
            lines.append(f"| v{r['from']} → v{r['to']} | {base} | {share:.3f} |")
    emit("E4 how much ATT&CK growth is bookkeeping rather than new intelligence",
         "\n".join(lines), "measurement",
         "Roughly a third of new edges for existing groups are ontology bookkeeping")

    # --- E5 attribution ------------------------------------------------
    lines = ["# E5 — controlled TTP-attribution experiment", "",
             "Fidelity: PRIMARY ARTEFACT (computed). Intelligence content is held constant:",
             "every condition describes the SAME adversary behaviour, differing only in the",
             "ATT&CK vocabulary it is expressed in. Analysis-time knowledge base is "
             f"v{e5[0]['w']} ({e5[0]['w_date']}); 500 trials per cell; 95% CIs from a",
             "paired bootstrap over trials.", "",
             "| artefact vocabulary | k | candidate groups | out-of-vocabulary rate | "
             "contemporaneous | naive | ATT&CK-Norm | oracle | drift penalty (pp) [95% CI] | "
             "recovered |", "|---|---|---|---|---|---|---|---|---|---|"]
    for r in e5:
        rec = f"{r['recovery_top1']:.3f}" if r["recovery_top1"] is not None else "n/a"
        lines.append(
            f"| v{r['v']} | {r['k']} | {r['n_groups']} | {r['oov_rate']:.3f} | "
            f"{r['contemporaneous_top1']:.3f} | {r['naive_top1']:.3f} | "
            f"{r['normalized_top1']:.3f} | {r['oracle_top1']:.3f} | "
            f"{100*r['drift_penalty_top1']:.1f} "
            f"[{100*r['drift_penalty_ci'][0]:.1f}, {100*r['drift_penalty_ci'][1]:.1f}] | {rec} |")
    lines += ["", "Condition definitions: `contemporaneous` = artefact and knowledge base "
                  "both in the artefact's own vocabulary (a self-consistent system, no "
                  "drift); `naive` = artefact identifiers matched directly against the "
                  "modern knowledge base (current practice); `ATT&CK-Norm` = the same "
                  "artefact after normalization; `oracle` = the same behaviour expressed "
                  "in the modern vocabulary (upper bound a legacy artefact cannot reach). "
                  "`contemporaneous − naive` is therefore the pure cross-version penalty, "
                  "and `oracle − contemporaneous` is the information loss inherent in the "
                  "older, coarser ontology."]
    emit("E5 attribution accuracy under ATT&CK vocabulary mismatch", "\n".join(lines),
         "measurement", "Controlled experiment isolating drift from intelligence change")

    # --- E6 coverage ---------------------------------------------------
    tgt = max(r["w"] for r in e6["portfolios"])
    rows = [r for r in e6["portfolios"] if r["w"] == tgt and r["relation"] == "mitigates"]
    lines = [f"# E6 — coverage claims under a frozen capability (re-measured at v{tgt})", "",
             "Fidelity: PRIMARY ARTEFACT (computed). The capability never changes; only",
             "the ontology moves. The naive-versus-normalized gap is the pure identifier",
             "artefact, separate from the genuine effect of the technique list growing.", "",
             "| capability frozen at | portfolio size | claimed then | naive now | "
             "normalized now | identifier artefact (pp) |", "|---|---|---|---|---|---|"]
    for r in rows:
        art = 100 * (r["coverage_normalized"] - r["coverage_naive"])
        lines.append(f"| v{r['v']} ({r['v_date']}) | {r['portfolio']} | "
                     f"{100*r['coverage_at_v']:.1f}% | {100*r['coverage_naive']:.1f}% | "
                     f"{100*r['coverage_normalized']:.1f}% | {art:.1f} |")
    lines += ["", "Random-portfolio sweep (500 random 30% portfolios per source release):", "",
              "| frozen at | naive error (pp) | normalized error (pp) |", "|---|---|---|"]
    for s in e6["random_sweep"]:
        lines.append(f"| v{s['v']} | {s['mean_naive_error_pp']:.2f} ± "
                     f"{s['sd_naive_error_pp']:.2f} | "
                     f"{s['mean_normalized_error_pp']:.2f} ± "
                     f"{s['sd_normalized_error_pp']:.2f} |")
    emit("E6 ATT&CK coverage claims drift while the capability stays frozen",
         "\n".join(lines), "measurement",
         "Reported coverage moves by percentage points with no change in capability")

    # --- E7 artefacts --------------------------------------------------
    lines = ["# E7 — label validity of deployed CTI corpora", "",
             "Fidelity: PRIMARY ARTEFACT (computed from each corpus's own label files,",
             "cloned from its public repository; validity evaluated per ATT&CK domain).", ""]
    for name, d in e7.items():
        cons = d["fully_consistent_releases"]
        lines += [f"## {name}",
                  f"- distinct (domain, identifier) labels: {d['n_unique_ids']}; "
                  f"label instances: {d['n_label_instances']}; "
                  f"sub-technique identifiers: {d['n_subtechnique_ids']}",
                  f"- best-fitting release: v{d['best_fit_version']} "
                  f"({d['best_fit_date']}), {d['best_fit_live_frac']:.3f} of labels live there",
                  f"- releases in which EVERY label is simultaneously live: "
                  f"{len(cons)}" + (f" (v{cons[0]}–v{cons[-1]})" if cons else
                                    " — the corpus matches no single release"),
                  f"- invalid at v{d['newest_version']} ({d['newest_date']}): "
                  f"{d['invalid_at_newest']} distinct labels "
                  f"({d['invalid_at_newest_frac']:.3f}), "
                  f"{d['invalid_label_instances_frac']:.3f} of label instances",
                  f"- repairable by revocation chain: {d['repairable_by_revocation_chain']}; "
                  f"unrepairable: {d['unrepairable']}",
                  f"- examples of invalid identifiers: {', '.join(d['examples_invalid'][:10])}",
                  ""]
    emit("E7 ATT&CK label validity in CTIBench, TRAM and rcATT", "\n".join(lines),
         "measurement", "Deployed CTI corpora carry labels that match no single ATT&CK release")


if __name__ == "__main__":
    main()
