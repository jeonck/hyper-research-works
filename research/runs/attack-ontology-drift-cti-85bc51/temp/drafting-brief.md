# Drafting brief — shared by all three draft orchestrators and the synthesizer

## What is being written

A journal manuscript for an SCI-indexed venue in the *Computers & Security* /
*IEEE TIFS* class. Not a blog post, not a survey, not a report with bullet
points. Continuous academic prose, numbered sections, tables and figures
referenced by number, an explicit threats-to-validity section, and a
reproducibility statement.

## Required section headings, verbatim and in this order

```
## Abstract
## 1. Introduction
## 2. Background: ATT&CK as a Versioned Ontology
## 3. Related Work
## 4. Problem Formalization and Drift Taxonomy
## 5. Data and Methodology
## 6. Measuring Ontology Drift in ATT&CK
## 7. Downstream Impact of Drift on CTI Analytics
## 8. ATT&CK-Norm: A Version-Normalization Protocol
## 9. Label Validity of Deployed CTI Corpora
## 10. Discussion and Reporting Discipline for CTI Research
## 11. Threats to Validity
## 12. Conclusion
## Sources
```

## Length and citations

- 5,000–10,000 words in the body. Aim for roughly 9,000.
- Inline numbered citations `[N]`, grouped as `[7, 12]` where several apply.
- 80–150 citation markers total, at least 9 per 1,000 words.
- Numbers come ONLY from `temp/reference-registry.md`. Never invent an entry,
  never cite a number the registry does not list.
- This study's own measurements are NOT citations. Write "Table 4" or
  "Section 6.2", never "[42]", when referring to our own results.

## The thesis to defend

ATT&CK ontology drift is a first-class threat to the validity of CTI analytics:
it is measurable, it changes conclusions and not merely scores, it is only
partly repairable, and the part that is not repairable by identifier arithmetic
is precisely the part nobody currently detects. Two corollaries the manuscript
must carry rather than bury:

1. **Concede the apparatus.** MITRE publishes immutable per-release bundles,
   typed revocation edges, retained tombstones, a change-computation tool and a
   version-stamped layer format. The argument is that the mechanism is
   incomplete (a 1:1 revocation relation cannot express a 1:N re-cut, and one
   v19 revocation promoted a technique to a tactic) and that adoption is close
   to absent.
2. **Concede the noise floor.** Products disagree on the ATT&CK label for the
   same behaviour roughly half the time within a single pinned release. The
   paper does not claim drift dominates that noise. It claims drift is separable
   from it by construction — every experimental condition draws from the same
   ATT&CK data, so labelling noise is constant across conditions and cancels in
   the contrasts — and that it is additive on top.

## Register

Argue, do not report. Every section that touches a tension engages it
explicitly. No hedging where the measurement is clean; explicit uncertainty
where it is not. Never write "it is worth noting", "it should be emphasized",
or a paragraph that only announces what the next paragraph will say.

## Evidence discipline (this is the paper's own subject, so it is binding)

- Tier A — our measurements and artefacts we read in full: state plainly.
- Tier B — literature reached only through search summaries in this
  environment: attribute as reported, never quote verbatim, never place
  quotation marks around it.
- Tier C — audited absences: state the bound of the search that found the
  absence, and never upgrade an absence to a proof.
- `temp/evidence-digest.md` holds every number. Quote it exactly. Do not
  recompute, do not re-round, do not approximate "0.323" as "about a third"
  in a place where the precise figure belongs.

## Inputs every drafter must read before writing

- `research/runs/attack-ontology-drift-cti-85bc51/query.md` (gospel)
- `temp/evidence-digest.md` (every number)
- `temp/reference-registry.md` (every citation)
- `temp/contradiction-graph.json` (the fights that must be engaged)
- `temp/consensus-claims.json` (what can be asserted without hedging)
- `temp/interim-L1.md` … `interim-L4.md` (the committed positions)
- `paper/tables/*.md` (the tables to reference by number)
- `paper/figures/` (the figures to reference by number)

## Fixed figure and table numbering (all drafters use these, no renumbering)

| In text | File | Shows |
|---|---|---|
| Figure 1 | `paper/figures/fig1_growth_churn.pdf` | live technique count, and per-release adds, revocations and description rewrites |
| Figure 2 | `paper/figures/fig2_survival.pdf` | identifier survival curves by source release, and recoverability at the newest release |
| Figure 3 | `paper/figures/fig3_semantic_drift.pdf` | silent semantic drift among identifier-stable techniques |
| Figure 4 | `paper/figures/fig4_growth_decomposition.pdf` | per-transition decomposition of new edges for pre-existing groups |
| Figure 5 | `paper/figures/fig5_attribution.pdf` | attribution accuracy by condition, and the drift penalty with confidence bands |
| Figure 6 | `paper/figures/fig6_coverage.pdf` | coverage claims under a frozen capability, and the random-portfolio sweep |
| Figure 7 | `paper/figures/fig7_artifact_validity.pdf` | label-validity curves for four deployed CTI corpora |
| Figure 8 | `paper/figures/fig8_conclusion_flips.pdf` | attribution verdict instability and mitigation leaderboard reordering |
| Table 1 | `paper/tables/t1_corpus.md` | the release corpus |
| Table 2 | `paper/tables/t2_churn.md` | per-release churn |
| Table 3 | `paper/tables/t3_survival.md` | identifier survival and half-life |
| Table 4 | `paper/tables/t4_semantic.md` | semantic drift among identifier-stable techniques |
| Table 5 | `paper/tables/t5_growth.md` | knowledge-growth decomposition |
| Table 6 | `paper/tables/t6_attribution.md` | the controlled attribution experiment |
| Table 7 | `paper/tables/t7_robustness.md` | robustness across scoring functions and profile definitions |
| Table 8 | `paper/tables/t8_coverage.md` | coverage claims under a frozen capability |
| Table 9 | `paper/tables/t9_artifacts.md` | label validity of deployed corpora |
| Table 10 | `paper/tables/t10_verdict_instability.md` | attribution verdict instability |
| Table 11 | `paper/tables/t11_leaderboard_flips.md` | mitigation leaderboard reordering |
| Table 12 | `paper/tables/t12_version_declaration.md` | ATT&CK version declarations in deployed corpora |
| Table 13 | `paper/tables/t13_version_metadata.md` | text change versus version increment |

Tables are reproduced inline in the manuscript in markdown, under a caption of
the form `**Table N.** <caption>`. Figures are referenced by number and given a
caption of the form `**Figure N.** <caption>` at the point of first reference;
the manuscript is markdown, so a figure is referenced, not embedded.
