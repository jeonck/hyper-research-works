#!/usr/bin/env python3
"""Step 9 — evidence digest: the load-bearing numbers, formatted from the results.

Written to research/runs/<tag>/temp/evidence-digest.md so that every drafting
agent quotes the same figures and none of them retypes one.
"""
from __future__ import annotations

import json
from pathlib import Path

def _vkey(v: str) -> tuple:
    """Version ordering. Plain string comparison puts "9.0" above "19.2"."""
    return tuple(int(x) for x in v.split("."))


ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "data" / "results"
TAG = "attack-ontology-drift-cti-85bc51"
OUT = ROOT / "research" / "runs" / TAG / "temp" / "evidence-digest.md"


def load(n):
    return json.loads((RES / n).read_text())


def main() -> None:
    e123, e4 = load("e1_e2_e3.json"), load("e4_growth.json")
    e5, e6, e7 = load("e5_attribution.json"), load("e6_coverage.json"), load("e7_artifacts.json")
    rb, e8 = load("e5b_e2b_robustness.json"), load("e8_case_v19.json")
    e9, e10 = load("e9_version_declaration.json"), load("e10_conclusion_flips.json")
    e6b, e5c = load("e6b_prevalence.json"), load("e5c_backprojection.json")
    e11 = load("e11_version_metadata.json")["summary"]
    ent = e123["enterprise-attack"]
    latest = ent["releases"][-1]["version"]

    L = ["# Evidence digest — " + TAG, "",
         "Every figure below is computed by `code/` from public artefacts and is",
         "reproducible with `bash code/run_all.sh`. Drafting agents must quote these",
         "numbers exactly and must not recompute or round them differently.", ""]

    L += ["## 1. The corpus", ""]
    for dom in ("enterprise-attack", "mobile-attack", "ics-attack"):
        r = e123[dom]["releases"]
        L.append(f"- {dom}: {len(r)} major releases, v{r[0]['version']} ({r[0]['date']}) "
                 f"to v{r[-1]['version']} ({r[-1]['date']}).")
    L += ["- Release-level analyses use the first release of each major version; the",
          "  deployed-corpus validity analysis uses every published release (41",
          "  Enterprise, 38 Mobile, 27 ICS).", ""]

    worst = min(ent["churn"], key=lambda c: c["jaccard_id"])
    L += ["## 2. The discontinuity", "",
          f"- v{worst['from']} to v{worst['to']} ({worst['to_date']}): identifier-set Jaccard "
          f"{worst['jaccard_id']:.3f}; {worst['added']} techniques added, "
          f"{worst['newly_revoked']} revoked, {worst['newly_deprecated']} deprecated; "
          f"{worst['group_edges_removed']} group-technique edges removed and "
          f"{worst['group_edges_added']} added in a single release.", ""]

    surv = {s["src"]: s for s in ent["survival"] if s["tgt"] == latest}
    hl = {h["src"]: h for h in rb["half_life"]}
    L += ["## 3. Identifier survival", ""]
    for v in ("1.0", "6.0", "7.0", "12.0", "18.0"):
        s = surv[v]
        h = hl[v]
        hs = (f"half-life {h['half_life_years']:.1f} years (at v{h['half_life_release']})"
              if h["half_life_release"] else "half-life never reached")
        L.append(f"- v{v} ({s['src_date']}): {s['n']} identifiers, {s['survival_rate']:.3f} "
                 f"still live at v{latest}, {s['revoked']} revoked, {s['deprecated']} "
                 f"deprecated, {s['recoverable_via_revoked_by']} recoverable via revoked-by; {hs}.")
    L += ["- Every revoked identifier in the corpus resolves to a live identifier through",
          "  the published revocation graph.", ""]

    sem = {s["src"]: s for s in ent["semantic"] if s["tgt"] == latest}
    L += ["## 4. Silent semantic drift (identifier-stable techniques only)", ""]
    for v in ("7.0", "11.0", "15.0", "18.0"):
        s = sem[v]
        L.append(f"- v{v}: {s['id_stable']} identifier-stable techniques; "
                 f"{s['desc_changed_frac']:.3f} have edited descriptions by v{latest}; "
                 f"mean token Jaccard {s['mean_token_jaccard']:.3f}; "
                 f"{s['substantial_frac']:.3f} substantially rewritten (J < 0.8).")
    L.append("")

    c = e4["enterprise-attack"]["cumulative"]
    base = c["total_added"] - c["new_actor"]
    book = c["ontology_refinement"] + c["revocation_remap"]
    L += ["## 4b. Is ATT&CK's own change metadata a usable signal?", "",
          f"- {e11['carried_over_pairs']} carried-over technique pairs across consecutive "
          f"major releases; {e11['description_changed']} "
          f"({e11['description_changed_frac']:.3f}) had their description rewritten.",
          f"- {e11['changed_without_version_bump']} of those "
          f"({e11['changed_without_bump_frac']:.3f}) carried no x_mitre_version increment, "
          f"and {e11['bumped_without_text_change']} version increments carried no text "
          f"change at all.",
          f"- As a detector of description change, x_mitre_version has precision "
          f"{e11['precision_of_version_bump']:.3f} and recall "
          f"{e11['recall_of_version_bump']:.3f}.", ""]

    L += ["## 5. Growth decomposition", "",
          f"- {c['total_added']} group-technique edges added across all Enterprise",
          f"  transitions; {c['new_actor']} belong to groups newly added to ATT&CK.",
          f"- Of the {base} added for pre-existing groups: {c['genuine_new_intel']} genuine "
          f"new intelligence, {c['new_technique_intel']} new technique, "
          f"{c['ontology_refinement']} sub-technique refinement, {c['revocation_remap']} "
          f"revocation re-mapping.",
          f"- Bookkeeping share: {book}/{base} = {book/base:.3f}.", ""]
    peaks = sorted(e4["enterprise-attack"]["transitions"],
                   key=lambda r: -((r["ontology_refinement"] + r["revocation_remap"]) /
                                   max(1, r["total_added"] - r["new_actor"])))[:4]
    for r in peaks:
        b = r["total_added"] - r["new_actor"]
        L.append(f"  - v{r['from']} to v{r['to']}: "
                 f"{(r['ontology_refinement']+r['revocation_remap'])/b:.3f} bookkeeping "
                 f"({b} edges for pre-existing groups).")
    L.append("")

    L += ["## 6. Attribution under vocabulary mismatch (k = 10, analysis at v"
          f"{e5[0]['w']})", ""]
    for r in e5:
        if r["k"] != 10 or r["v"] not in ("1.0", "6.0", "7.0", "12.0", "18.0"):
            continue
        rec = f"{r['recovery_top1']:.2f}" if r["recovery_top1"] is not None else "n/a"
        L.append(f"- artefact at v{r['v']}: contemporaneous {r['contemporaneous_top1']:.3f}, "
                 f"naive {r['naive_top1']:.3f}, normalized {r['normalized_top1']:.3f}, "
                 f"oracle {r['oracle_top1']:.3f}; drift penalty "
                 f"{100*r['drift_penalty_top1']:.1f} pp "
                 f"[{100*r['drift_penalty_ci'][0]:.1f}, {100*r['drift_penalty_ci'][1]:.1f}]; "
                 f"recovered {rec}.")
    bp = {x["v"]: x for x in e5c}
    L += ["", "Back-projection loss (for transparency: all three legacy conditions consume",
          "the same back-projected observation; only the oracle sees the full modern set):"]
    for v in ("1.0", "7.0", "18.0"):
        x = bp[v]
        L.append(f"- v{v}: {x['no_v_era_ancestor']} of {x['modern_techniques']} modern "
                 f"techniques have no v{v} ancestor; profiles retain "
                 f"{x['mean_profile_retention']:.3f} of their distinct identifiers.")
    L.append("")

    L += ["## 7. Conclusion flips", ""]
    for r in e10["attribution_verdicts"]:
        if r["v"] not in ("1.0", "6.0", "7.0", "12.0", "18.0"):
            continue
        L.append(f"- artefact at v{r['v']}: the named actor changes in "
                 f"{r['verdict_changed_frac']:.3f} of observations; "
                 f"{r['verdict_changed_and_now_wrong_frac']:.3f} change to a wrong actor; "
                 f"normalization changes the verdict in "
                 f"{r['normalization_changed_verdict_frac']:.3f}.")
    L.append("")
    for r in e10["coverage_rankings"]:
        if r["v"] not in ("6.0", "12.0", "17.0", "18.0"):
            continue
        L.append(f"- mitigation leaderboard frozen at v{r['v']}: Kendall tau "
                 f"{r['tau_naive']:.3f} naive, {r['tau_normalized']:.3f} normalized; "
                 f"rank-1 changed: {'yes' if r['rank1_changed_naive'] else 'no'}.")
    L.append("")

    tgt = max((r["w"] for r in e6["portfolios"]), key=_vkey)
    L += [f"## 8. Coverage claims under a frozen capability (re-measured at v{tgt})", ""]
    for r in e6["portfolios"]:
        if r["w"] == tgt and r["relation"] == "mitigates" and \
                r["v"] in ("6.0", "10.0", "17.0", "18.0"):
            art = 100 * (r["coverage_normalized"] - r["coverage_naive"])
            L.append(f"- frozen at v{r['v']}: claimed {100*r['coverage_at_v']:.1f}%, "
                     f"naive {100*r['coverage_naive']:.1f}%, normalized "
                     f"{100*r['coverage_normalized']:.1f}%; identifier artefact {art:.1f} pp.")
    L.append("")
    L.append("Prevalence-weighted (answering the long-tail objection):")
    for r in e6b["rows"]:
        if r["v"] in ("6.0", "10.0", "18.0"):
            L.append(f"- frozen at v{r['v']}: artefact {r['unweighted_artefact_pp']:+.2f} pp "
                     f"unweighted, {r['weighted_artefact_pp']:+.2f} pp prevalence-weighted.")
    L.append(f"- the fifteen most-referenced techniques carry "
             f"{e6b['top15_share_of_uses_edges']:.3f} of all `uses` edges at v{tgt}.")
    L.append("")

    L += ["## 9. Deployed corpora", ""]
    for name, d in e7.items():
        cons = d["fully_consistent_releases"]
        cs = (f"all labels simultaneously live in {len(cons)} releases "
              f"(v{cons[0]}–v{cons[-1]})" if cons else
              "**no release makes every label simultaneously valid**")
        L.append(f"- {name}: {d['n_unique_ids']} distinct labels, "
                 f"{d['n_label_instances']} instances, {d['n_subtechnique_ids']} "
                 f"sub-technique identifiers; best fit v{d['best_fit_version']} "
                 f"({d['best_fit_live_frac']:.3f}); {cs}; {d['invalid_at_newest']} "
                 f"invalid at v{d['newest_version']} "
                 f"({d['invalid_at_newest_frac']:.3f} of labels, "
                 f"{d['invalid_label_instances_frac']:.3f} of instances), "
                 f"{d['repairable_by_revocation_chain']} repairable, "
                 f"{d['unrepairable']} not.")
    tot_files = sum(d["files_scanned"] for d in e9.values())
    tot_decl = sum(d["declarations_found"] for d in e9.values())
    L += ["", f"- Version declarations: {tot_decl} found across {tot_files} documentation "
              f"files in {len(e9)} deployed corpora.", ""]

    L += ["## 10. The most recent revocation wave", "",
          f"- v{e8['previous_release']} to v{e8['current_release']}: {e8['n_revoked']} live "
          f"techniques revoked, including the whole T1562 family.",
          f"- Blast radius on the v{e8['previous_release']} graph: "
          f"{e8['group_technique_edges_affected']} group-technique edges, "
          f"{e8['software_technique_edges_affected']} software-technique edges, "
          f"{e8['mitigations_affected']} mitigations, {e8['detections_affected']} detection "
          f"relationships; {e8['groups_losing_an_identifier']} of {e8['groups_total']} "
          f"group profiles lose at least one identifier.",
          f"- T1562.001 was ranked {e8['usage_rank']['T1562.001']['rank']} of "
          f"{e8['usage_rank']['T1562.001']['of']} techniques by `uses` edges in the release "
          f"it left."]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(L) + "\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
