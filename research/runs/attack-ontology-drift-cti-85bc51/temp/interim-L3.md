# Interim L3 — the temporal structure of ontology-drift risk

**Locus:** one-time 2020 trauma, or continuing process? **Verdict:** neither, as stated.
The corpus supports a **two-clock, recurrent-regime** model. Identifier churn is episodic
and *per-domain recurrent*; semantic churn is continuous and has a stable rate.

---

## 1. The episodic case, at full strength

Every catastrophic Enterprise number is one release. At v6.0 → v7.0 (2019-10-23 →
2020-03-31) identifier Jaccard collapses to **0.222**, with **129 techniques revoked and 11
deprecated** in a single step (`e1_e2_e3.json`, enterprise churn). Nothing since comes close:
the next-largest Enterprise Jaccard drop is 0.944 (v18.0 → v19.0). The half-life analysis is
blunt about it — every pre-restructuring cohort (v1.0–v6.0) has its half-life release recorded
as **7.0**, and every cohort from v7.0 onward has `half_life_release: null` with final survival
**0.9696–0.9781** to the present (`e5b_e2b_robustness.json`, `half_life`). Six years and
twelve major releases after the restructuring, no post-v7.0 Enterprise cohort has lost even
3% of its identifiers.

My own recomputation (C1 below, against *all* 41 Enterprise releases including patches)
sharpens this rather than softening it. For cohorts v7.0–v18.0 the time to 10% **hard**
identifier staleness is `None` — it never happens. And once the published `revoked-by`
crosswalk is applied transitively, the *unrecoverable* fraction is **≤ 5.9% even for the v1.0
cohort** and **≤ 0.2% for every post-v7.0 cohort**. The Enterprise 2020 event, the one the
literature cites, is also the best-documented event in the corpus: almost all of it is
mechanically reversible. On identifiers alone, side A wins outright.

## 2. The continuing-process case, at full strength

Three independent measurements refuse to sit still after 2020.

**Revocation did not stop, it went quiet and came back.** v18.0 → v19.0 revoked **17 live
techniques**, including the entire T1562 *Impair Defenses* family, re-cut 1:N into T1684–T1690
(`e8_case_v19.json`). Blast radius: **84 group→technique edges, 155 software→technique edges,
47 mitigations, and 52 of 168 group profiles**, and it took **T1562.001**, the **33rd most
referenced technique of 599** in the release it left. In the same transition **198 of 674
surviving techniques changed tactic** (`e1_e2_e3.json`) and, by `e4_growth.json`, **47.0%** of
new edges for pre-existing groups (77 of 164) were `revocation_remap` bookkeeping, the highest
share since v7.0's 75.0%.

**Semantic rewriting never paused.** By v19.0, **46.5%** of v11.0's ID-stable Enterprise
techniques have edited descriptions and **20.8%** are substantial rewrites (token Jaccard < 0.8);
for v7.0 the figures are 74.9% and 38.6% (`e1_e2_e3.json`, semantic). Mass silent edits also
strike whole fields: v17.0 → v18.0 rewrote the `detection` field of **583 of 679** surviving
techniques, with only 49 description edits — an event no identifier-based diff would report.

**The episode is not unique to Enterprise, and not unique to 2020** — see C3.

## 3. Original computations

Scripts (run with `.venv/bin/python`, all against `data/attack_drift.db` via
`code/attackdrift.py`), preserved in the session scratchpad:
`temp/L3-code/{L3_staleness,L3_leading,L3_recurrence,L3_substantive}.py` (curves in `temp/L3-code/L3_staleness.json`).

### C1 — the practitioner's clock: "how long until 10% of my labels are stale?"

Cohort = live techniques at a major release; target = **every** later release, patches included.
Three staleness definitions: *hard* (no longer live), *unrecoverable* (hard and transitive
`revoked-by` does not land on a live ID), *substantive* (hard, or token Jaccard < 0.8, or tactic
set changed). Years to 10%, Enterprise:

| cohort era | t10 hard | t10 unrecoverable | t10 substantive | t10 text-only |
|---|---|---|---|---|
| v1.0–v6.0 (pre) | 0.44–2.20 yr | never | 0.25–0.52 yr | — |
| v7.0–v18.0 (post) | **never** | **never** | **0.50–2.01 yr** (median 1.51) | **0.99–2.01 yr** (median 1.52) |

The text-only column excludes tactic changes *and* revocations entirely, so it cannot be
attributed to the v19.0 re-cut: **10% of any pinned post-2020 Enterprise label set is
substantively rewritten within ~1.5 years, in every single cohort from v7.0 to v15.0**
(1.56, 1.49, 0.99, 1.51, 1.52, 1.49, 1.99, 1.99, 2.01 yr). Semantic *half*-life is 4.5–6.1 years
(v7.0: 6.08; v10.0: 4.52). The answer to the practitioner therefore inverts depending on the
question asked: identifier half-life post-v7.0 is **infinite**; semantic half-life is **~5 years**;
first 10% staleness arrives in **~18 months**.

### C2 — leading indicators: there are none

Release-level, Enterprise, 17 lagged pairs. Spearman ρ of feature at transition *k* against
kill rate at *k+1*: detection edits **+0.377** (permutation p = **0.134**, 20 000 shuffles),
version-field bumps +0.253, major-version bumps +0.258, description edits +0.032, tactic
changes **−0.120**. Nothing survives. Technique-level hazard is worse than null: the 131
techniques doomed at v7.0 had been edited *less* in the preceding release than survivors
(description edited 0.168 vs 0.336; version bumped 0.176 vs 0.372); the 16 doomed at v19.0
show 0.125 vs 0.071 on n=16 — noise. **Restructuring waves are not forecastable from the
public bundles.** This is a load-bearing negative result: a consumer cannot time-hedge, so the
protocol must be standing, not triggered.

### C3 — Mobile and ICS: the same episode, different years

| domain | event | date | id Jaccard | revoked / deprecated / vanished | unrecoverable |
|---|---|---|---|---|---|
| mobile | v2.0 → v3.0 | 2018-10-23 | **0.000** | 0 / 0 / **76** | **100%** |
| enterprise | v6.0 → v7.0 | 2020-03-31 | 0.222 | 129 / 11 / 0 | 5.9% (v1.0 cohort) |
| ics | v8.0 → v9.0 | 2021-04-29 | 0.778 | 0 / 10 / 1 | 16.0% (v8.0 cohort) |
| mobile | v10.0 → v11.3 | 2022-07-07 | 0.268 | 36 / 14 / 0 | 14.1% (v10.0 cohort) |
| ics | v18.0 → v19.0 | 2026-04-28 | 0.698 | 9 / 0 / 0 | 0% |

Mobile's 2018 event is a wholesale ATT&CK-ID renumbering (`MOB-T1001…` → `T1398…`): STIX IDs
are **100% preserved (128 of 128)** and technique *names* 60/76 overlap, yet **zero** of the 76
dead identifiers is recoverable through `revoked-by` (only 15 such edges exist in v3.0). It is
the most destructive event in the corpus, it is uncrosswalkable, it is invisible to
STIX-ID-keyed tooling, and it predates 2020. ICS's event is *now*: v19 revokes nine T0xxx
techniques into the shared T169x namespace (T0803 → T1691.001, T0855 → T1692.001, …) and
introduces ICS sub-techniques for the first time (**0 sub-techniques at v18.1, 18 at v19.0**) —
structurally the same move Enterprise made in 2020, six years later, all nine remaps recoverable.
Post-event domains then freeze: Mobile v11.3–v19.2 shows **0.0% hard staleness** and 8.4%
description edits; ICS v13.0–v18.0 cohorts sit at 13.6% substantive staleness.

**Recurrence hazard:** 5 of 47 major-to-major transitions have identifier Jaccard < 0.80 =
**0.106 per transition**, one event per **4.4 domain-years** over 22.1 observed domain-years —
i.e. roughly one restructuring somewhere in ATT&CK every **1.5 calendar years**.

## Committed position

The paper should adopt a **two-clock recurrent-regime model** and state it as such: ATT&CK
carries a *fast continuous semantic clock* and a *slow episodic identifier clock*, and the
2020 restructuring is one draw from a recurring hazard, not a closed historical wound. The
identifier clock is bursty with a per-domain hazard of about 0.11 per major release (one event
per 4.4 domain-years; five events across three domains in eight years, in 2018, 2020, 2021,
2022 and 2026), is **not predictable one release ahead** (best lead-1 ρ = +0.377, p = 0.134;
doomed techniques are edited *less* than survivors beforehand), and is only *sometimes*
crosswalkable — 100% recoverable for ICS v19, ≤5.9% unrecoverable for Enterprise v7.0, but
**0% recoverable for Mobile v3.0**. The semantic clock runs continuously at a rate that has
barely varied since v7.0: **10% of any pinned Enterprise label set is substantively rewritten
within ~1.5 years and half within ~5 years**, while its identifier survival stays above 0.97.
Therefore the correct risk statement is not "drift happened in 2020" but "a pinned ATT&CK
label set decays semantically on an 18-month first-10% schedule and faces an unhedgeable
~11%-per-release chance of an identifier discontinuity in its domain" — which is why the
normalization protocol must be standing and version-declaring rather than triggered by
observed revocations. **Falsification:** the model dies if (a) the next three major releases in
every domain show substantive-rewrite rates falling below ~3% per year, i.e. the semantic clock
stopping rather than merely the identifier clock idling; (b) a leading indicator reaches
ρ > 0.6 with p < 0.05 on an extended lagged panel, making bursts forecastable and hedgeable;
or (c) no domain experiences a Jaccard < 0.80 transition in the next eight domain-years, which
would put the observed 0.106-per-transition hazard outside plausible sampling error and
re-establish 2020-and-before as a closed era.
