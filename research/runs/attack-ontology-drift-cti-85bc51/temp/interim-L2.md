# Interim L2 — is the drift effect separable from, and additive to, the single-version labelling noise floor?

## 1. The objection, stated so it can be falsified

Virkud et al. (USENIX Security 2024) pin ATT&CK v11 and show that detection rules
from different vendors describing the *same* behaviour carry disjoint technique
labels — Elastic `e479` labels a named-pipe impersonation `T1134`, Splunk `s229`
labels the same `cmd.exe` pipe write `{T1059, T1059.003, T1543, T1543.003}`, zero
overlap (verified from the released RQ3 notebook, `/home/user/ext/edr-attack`).
Saha et al. (ASIA CCS 2026) show only ~34% of ATT&CK groups have any
group-specific technique. "Beyond Single Reports" adds that up to 33.3% of
extractor errors are between same-tactic, description-overlapping techniques.
Together: at a single pinned release there is a large *synchronic* variance term
ε, and TTP attribution is weakly identifiable before drift enters.

If the objection is right, three things follow, and each is testable:

- **P1 (non-separability).** The measured drift penalty should shrink toward zero
  once ε is present at a realistic rate — i.e. drift is a re-description of the
  same confusability, not an independent term.
- **P2 (non-identifiability drives the result).** The penalty should be carried by
  the ~66% of groups that were never attributable; conditional on the
  identifiable stratum it should vanish.
- **P3 (wrong unit).** Because ε operates on independently labelled incident
  data and the study operates on MITRE's own curated edges, the study measures a
  quantity that does not exist in the field.

## 2. Audit of the design

**What the design genuinely does.** `04_attribution.py` back-projects every
*modern* (v19) group profile into the V-era vocabulary via `build_backmap` —
pre-revocation identifier where one exists, surviving parent where the
sub-technique did not yet exist, drop where no V-era ancestor exists — and runs
four conditions over an identical candidate universe and identical draws. Because
every condition consumes the same underlying intelligence content, the contrast
`contemporaneous − naive` cannot be explained by a difference in *what* was
observed. That is a real and non-trivial control, and it is more than the
critique literature has.

**Residual confound 1 — ε is set to zero, not held constant.** This is the design's
actual weakness, and the contradiction graph's side_b overstates the case when it
says noise "cancels in the contrasts". Every condition draws from MITRE's own
edges, so ε = 0 everywhere. "Constant at zero" licenses *separability* but says
nothing about *additivity*: an interaction term cannot be seen in a design with
one level of the moderator. I ran the missing factorial (scratchpad
`l2_audit.py`, 1200 trials/cell, k=10): each observed technique is replaced with
probability ρ by a sibling sub-technique, its parent, or a same-tactic technique —
a Virkud-shaped labeller substitution — applied in W-vocabulary *before*
back-projection so it flows identically into all four conditions.

| V | ρ=0 | ρ=0.1 | ρ=0.2 | ρ=0.4 |
|---|---|---|---|---|
| v1.0 drift penalty | +0.439 | +0.417 | +0.399 | +0.342 |
| v6.0 drift penalty | +0.476 | +0.434 | +0.383 | +0.317 |
| v12.0 drift penalty | +0.017 | +0.011 | +0.016 | +0.021 |
| v18.0 drift penalty | +0.012 | +0.008 | +0.012 | +0.012 |

P1 is refuted: the penalty survives at every noise level. But strict additivity
also fails in the large-drift regime — at ρ=0.4 the pre-restructuring penalty is
attenuated 22–33%, because noise and drift consume the same finite signal. In the
modern regime the penalty is flat in ρ, i.e. effectively additive. The correct
claim is therefore **separable and sub-additive**, with the noise-free number an
*upper* bound on drift's contribution in a noisy world. Normalization degrades
faster than the penalty does: recovery at v1.0 falls from 0.44 (ρ=0) to 0.30
(ρ=0.4). The paper must state that ATT&CK-Norm recovers less as label quality
falls — that is an L4-relevant limitation the study does not currently carry.

**Residual confound 2 — `contemporaneous` is not a V-era system, and the docstring
says it is.** The docstring calls it "a self-consistent V-era system: no drift".
It is not: it is 2026 intelligence *transcribed* into a 2018 vocabulary. Running
the missing cell (real archival V-era labels against real archival V-era profiles,
IDF at V; `l2_audit2.py`) gives v1.0 = **0.969** against a back-projected
`contemporaneous` of **0.668**. The gap is a collision artefact: dense modern
profiles collapsed onto a coarse vocabulary collide with each other in a way no
deployed 2018 system experienced, because 2018 profiles were sparse. Two biases
therefore run in opposite directions — the collision effect depresses
`contemporaneous` (deflating the penalty), while `obs_v ⊆ prof_v` by construction
is a perfect-recall idealisation that inflates it. The measured net is downward:
the reported pre-restructuring penalty is conservative. In the modern regime the
two numbers converge (v12: 0.837 vs 0.856; v18: 0.841 vs 0.846), so the headline
modern claim is unaffected. **Required fix:** rename the condition to
`back-projected` or `V-vocabulary`, delete the "V-era system" gloss, and publish
the real-V-era cell as a diagnostic.

**Residual confound 3 — the loop is closed inside ATT&CK.** Observation, profile,
ground truth and the back-projection map all come from one curator, so the
absolute accuracies (0.67–0.97 top-1) must never be reported as attribution
performance; they are internal-consistency scores. The `historical` condition
partly opens the loop and shows how much is lost when it does: 0.159 at v1.0
versus 0.231 for the back-projection, i.e. real archival artefacts do *worse* than
the reconstruction. P3 lands to this extent — an independently double-labelled
incident corpus would be a strictly better instrument, and none exists.

**Residual confound 4 — `naive` is a worst case, not a typical case.** MITRE
re-mapped its own `uses` edges to the most specific sub-technique, so the modern
profiles are almost purely sub-technique-level while the back-projected artefact
is purely parent-level, and exact string matching scores zero across that
boundary. Real legacy artefacts are mixed-granularity, so the true naive
condition sits between `naive` and `normalized`. Relatedly, `normalize()` is
close to the algebraic inverse of `build_backmap` (both walk the target's
`revoked_by` and `subtechnique-of` graphs), so the reported recovery is an upper
bound on what normalization achieves on real, typo-bearing, cross-domain label
sets — exactly the defects E7 found in CTIBench.

**Confound checked and dismissed.** `rank_of` breaks ties alphabetically, which
could gift the alphabetically-first group free top-1 hits where all scores are
zero. Measured: 0 ties in 1500 trials at both v12 and v18 under idf-cosine, and
mid-rank scoring reproduces the penalty to four decimals (+0.0173, +0.0120). Not
an issue.

**P2 — the Saha stratification, which the study does not run.** Splitting the
universe by whether a group has any technique unique to it within the candidate
universe (paired bootstrap, 1500 trials, `l2_audit2.py`):

| V | specific groups | drift penalty, specific | drift penalty, non-specific |
|---|---|---|---|
| v12.0 | 40/123 (32.5%) | **+0.0344** [+0.0101, +0.0607] | +0.0089 [+0.0000, +0.0189] |
| v16.0 | 46/149 (30.9%) | **+0.0331** [+0.0166, +0.0497] | +0.0049 [−0.0010, +0.0118] |
| v18.0 | 48/161 (29.8%) | **+0.0239** [+0.0109, +0.0391] | +0.0067 [+0.0019, +0.0125] |

The specificity fraction independently reproduces Saha's ~34%/<30%. P2 is
refuted in the *opposite direction* from what the objection predicts: in the
modern regime the drift penalty is 2.5–7× larger on the identifiable stratum,
with a CI excluding zero at all three versions, while the non-specific stratum is
at or near zero. The mechanism is obvious once stated — a group's identifying
token is by definition a rare technique, and rare techniques are the ones ATT&CK
adds, splits and revokes. Drift attacks precisely the signal attribution depends
on. This stratified table should be promoted into the paper; it is the single
strongest available answer to the strongest published objection.

## 3. The long tail, adjudicated on `e6b_prevalence.json`

Documentation prevalence at v19 is only moderately head-heavy: top-15 = 28.5%,
top-50 = 55.1%, top-100 = 72.7% of all `uses` edges over 697 live techniques. The
frozen-capability artefact grows rather than shrinks under prevalence weighting —
17.1–20.0 pp weighted versus 12.6–16.5 pp unweighted for pre-restructuring
portfolios (v1.0–v6.0), converging to ~1.4–2.2 pp both ways afterwards. The head
is also itself a product of restructuring: 5 of the v19 top-15 did not exist
before v7.0, and T1027.013 — 11th, 246 edges — did not exist before v15.0 (April
2024). Head turnover is measurable: J(top-20, v19) is 0.176 for every release
v1.0–v6.0 and the v6→v7 transition drops consecutive-release top-20 Jaccard to
0.250. The most recent wave took T1562.001, rank 33 of 599 at v18 with 110 edges;
the whole 17-technique v19 revocation removed 1.64% of v18's edge mass and
touched 52 of 168 group profiles.

**The honest limitation.** `uses` edges are not sightings. They count how many
groups/malware/tools MITRE has *documented* as using a technique — a cumulative
stock over cited CTI reports, biased toward behaviours that are easy to narrate
in a report, and monotone (a 2019 edge never decays). CTID Sightings measures a
*flow* of defender telemetry over a window and is materially more concentrated.
Worse, the weight is computed from the same release whose churn is measured, so a
revocation carries its weight with it — the weighted artefact is not independent
evidence in the way telemetry would be. So: the long-tail objection is refuted on
documentation prevalence, i.e. for the fraction of the *written CTI corpus*
affected; it is untested for the fraction of the *alert stream* affected, and the
paper must say so in exactly those words rather than claim a general refutation.

## Committed position

The drift effect is separable from the single-version labelling noise floor and
the separation is demonstrated, not assumed: injecting a Virkud-shaped labeller
substitution at ρ up to 0.4 leaves the penalty intact at every release boundary
tested, and stratifying by Saha's own specificity criterion — which this corpus
independently reproduces at 29.8–32.5% — shows the modern penalty is 2.5–7× larger
on the identifiable groups (+0.024 to +0.034, CI excluding zero) than on the
non-identifiable ones, so the effect is not an artefact of averaging over groups
that were never attributable. It is however only *partially* additive: noise and
drift are sub-additive where drift is large, attenuating the pre-restructuring
penalty by 22–33% at ρ=0.4, so the noise-free figures are upper bounds and must be
reported as such. The strongest residual threat is not the noise floor at all but
the closed ATT&CK-internal loop: observation, profile, ground truth and
back-projection map all come from one curator, the `contemporaneous` condition is
a synthetic transcription rather than the "self-consistent V-era system" its
docstring claims (real V-era self-consistency is 0.969 at v1.0 against the
back-projection's 0.668), and `naive` is a uniform parent-level worst case that no
real mixed-granularity artefact attains. The experiment that would close this is
the one the field does not have — a double-labelled incident corpus in which two
independent analysts label the same intrusions under two ATT&CK releases, giving
the drift and the ε terms simultaneously and from outside MITRE's own edges.
