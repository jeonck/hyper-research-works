# L4 — What the field should do, and what ATT&CK-Norm provably cannot fix

Every number is read from `data/results/*.json` or computed by me against
`data/attack_drift.db` (enterprise-attack, v1.0–v19.2).

## 1. Where `normalize()` loses information

`normalize()` (`code/attackdrift.py`) is a three-branch function over a *set* of technique
IDs. Each branch leaks.

**(a) It is set-valued, so merges silently destroy cardinality.** The v19.2 Enterprise
bundle carries 149 technique `revoked-by` edges. Eight targets are many-to-one, absorbing
20 predecessor identifiers; the largest, **T1685, absorbs five** — T1054, T1089, T1562,
T1562.001 and T1562.006. Because the protocol returns a set, `{T1562, T1562.001, T1562.006}`
and `{T1562.001}` both return `{T1685}`. The mapping is a function, not an injection, and
`normalize()` reports no residual. On real corpora this is not hypothetical: TRAM's
bootstrap label set goes from **537 to 503 distinct live classes**, with 28 targets absorbing
62 source classes and **14.75% of its 25,770 label instances landing in a merged class**;
rcATT goes 215 → 199 with 9.37% of 6,235 instances merged.

**(b) The crosswalk it trusts performs unlabelled abstraction changes.** Of the 149 edges,
119 are top→sub, 13 top→top, 10 sub→sub and **7 are sub→top** — the official map *demoting*
a sub-technique to a parent. `normalize()` has no abstraction-level check.

**(c) It has no domain guard.** Step 4 discards anything absent from the target `Snapshot`,
so that bucket mixes withdrawn concepts, wrong-domain identifiers and scrape artefacts —
three conditions needing opposite remedies.

**(d) It is blind to intension drift by construction.** Between v18.1 and v19.2, 674
techniques are live and ID-stable in both. **198 of them (29.4%) changed their tactic
string** and **41 (6.1%) changed their description hash**. `normalize()` returns all 674
unchanged: zero drift signalled, on the release that dissolved the field's most-used tactic.

**(e) Its return type is the defect.** A set in, a set out, no residual. A caller cannot
distinguish "10 identifiers, all clean" from "10 in, 3 merged, 2 dropped". Every honest
use of this protocol requires an API it does not have.

## 2. Worked counter-example: a defensible-looking wrong answer

**The T1562 umbrella collapse (v18.1 → v19.2).** At v18.1, `T1562 "Impair Defenses"` is a
top-level technique with **twelve** children spanning firewalls, cloud logs, command
history, safe-mode boot and downgrade attacks. Three groups assert the *generic* parent
— G0059 Magic Hound, G1043 BlackByte, G1045 — the standard CTI convention for "the report
says defenses were impaired but does not say how."

v19 dissolved this. TA0005 was **renamed in place** from "Defense Evasion" to "Stealth"
(same identifier, new referent) and a new tactic **TA0112 "Defense Impairment"** was minted
to hold the old T1562 family. The concept `Impair Defenses` was promoted from technique to
tactic. `revoked-by` cannot point a technique at a tactic, so MITRE mapped
**T1562 → T1685 "Disable or Modify Tools"** — one of its own former children. Six of the
other eleven children went elsewhere entirely (T1686, T1686.001, T1686.002, T1688, T1689,
T1690).

So: `normalize({T1562}, v19.2)` returns `{T1685}`. It resolves in one hop, hits a live
identifier, reports full success and drops nothing. The answer is *wrong*. An analyst who
wrote T1562 because a report said "the actor disabled the host firewall" is now recorded
as asserting that the actor tampered with EDR tooling — a strictly narrower and factually
different claim, in a tactic that did not exist when the artefact was written. And Magic
Hound, which asserted `{T1562, T1562.001, T1562.002, T1562.004}`, normalizes to
`{T1685, T1685.001, T1686}`: four documented behaviours become three, so its measured
technique breadth falls by one purely as bookkeeping.

**A second failure: domain misassignment read as deprecation.** `e7_artifacts.json`
records CTI-Bench's CTI-ATE as having 8 identifiers invalid at v19.2, of which **7 are
"unrepairable"**. All seven — T1404, T1406, T1577, T1628, T1630, T1643, T1655 — come from
**one row** of `cti-ate.tsv` (row 8, source `attack.mitre.org/software/S0440/`) whose
`Platform` column says `Enterprise` while its entire 7-identifier gold set is mobile-only.
All seven are **live in mobile-attack v19.2**. So 87.5% of CTI-Bench's "drift damage" is
not drift; it is a single-version labelling error, and ATT&CK-Norm would report seven
unrepairable deprecations and be wrong seven times.

## 3. Roll-up or drop? Measure it — and the answer is neither

I re-ran the E5 attribution experiment with `rollup=True` and `rollup=False` as the only
difference (same seed, 54 conditions × 500 trials = 27,000 trials), and audited the
roll-up branch on real archival group profiles for all 18 major releases and on all four
CTI corpora (37,447 enterprise/undeclared label instances).

**The roll-up branch fires zero times. Everywhere.** Top-1 accuracy is identical to three
decimals in every one of the 54 conditions; the paired bootstrap CI on
(rollup − drop) is [+0.000, +0.000]. Across 18 archival profile sets the branch never
executes: every unrepairable identifier is a *top-level* deprecation with no parent (5–7
per release, 0 at v17–v18). Across CTI-Bench, rcATT, TRAM-bootstrap and TRAM2: 0 roll-ups.

The reason is structural. MITRE never orphans a sub-technique — a revoked sub-technique
always resolves to a live target — and deprecations-without-successor are top-level.
Roll-up's precondition does not arise in ATT&CK's data. So the debate is empty: **the
correct default is to drop and count**, not because drop wins a measured contest, but
because roll-up wins nothing measurable while adding an untested code path that can
fabricate a parent-level assertion the source never made. Delete it, or gate it behind an
explicit flag with a mandatory residual report. Everything ATT&CK-Norm actually buys comes
from step 1, transitive revocation resolution — and even that is a legacy migration tool,
not a standing cure: mean top-1 gain is **+20.1 points for pre-v7 artefacts** but
**+0.77 points post-v7**, with the gain's 95% CI including zero in **23 of 36 post-v7
conditions** (`e5_attribution.json`). Where it does work cleanly is coverage ranking:
mean Kendall τ rises 0.931 → 0.992, three of four naive rank-1 flips vanish and none are
introduced (`e10_conclusion_flips.json`).

And normalization is not verdict-neutral. It *changes the attribution verdict* in
36.8–44.2% of trials for v1–v6 artefacts and 0.6–3.0% for v7+ — so applying it silently is
itself a research-integrity event that must be declared.

## 4. A minimal, checkable reporting contract

Not a framework. Four lines a reviewer can check in under a minute. `e9_version_declaration.json`
shows the current baseline: **0 declarations across CTI-Bench, rcATT and TRAM** (19 files scanned).

**CTI paper / dataset.** (1) `domain` + exact release + SHA-256 of the STIX bundle, in the
artefact, not the prose. (2) Whether identifiers were normalized, and to which target.
(3) The residual — `kept / merged / dropped` counts plus the dropped IDs verbatim. (4) For
cross-time comparisons, that both sides were projected onto one reference release. *Cost:*
a JSON header, a table, ~30 lines of code. The real cost is reputational: a residual line
makes label decay public, and rcATT's would read 49.8% of identifiers and 38.0% of label
instances invalid at v19.2.

**Benchmark.** Also (5) the label *granularity policy* (parent-only vs mixed) and the class
count before and after normalization — a benchmark whose classes silently merge 537 → 503
is not the same benchmark; and (6) a CI re-validation script that fails when any gold label
is not live in the declared release. *Cost:* a standing maintenance obligation, and scores
stop being cross-release comparable by default — which is the point.

**Vendor coverage claim.** (7) The ATT&CK version and the denominator (live techniques in
that release, as a number) next to the percentage. (8) Re-stated against the current
release, or marked as-of. *Cost:* coverage percentages become non-monotone in public.

## 5. What MITRE should change — all of it ported, none of it invented

1. **A two-tier successor vocabulary.** `revoked-by` is 1:1 and cannot express a 1:N split
   or a cross-layer promotion. Adopt OBO Foundry Principle 19's split: `replaced_by` for
   exact successors, `consider` for inexact ones. T1562 should carry `consider` edges to all
   seven of its v19 successors and an explicit cross-layer pointer to TA0112 — not a single
   `revoked-by` to T1685.
2. **A controlled obsolescence-reason vocabulary** (superseded-by-split, merged,
   re-scoped, promoted-to-tactic, out-of-scope), as OBO does with IAO:0000231. Today
   `x_mitre_deprecated` carries no reason, so drop and merge are indistinguishable.
3. **Make drift visible in the human-readable field**, as OBO's mandatory `"obsolete "`
   label prefix does. ATT&CK's retirement is metadata-only, so any tool joining on name
   keeps working against a dead concept.
4. **Referent stability at a stable ID.** Renaming TA0005 from "Defense Evasion" to
   "Stealth" in place is the edit Principle 19 forbids: a changed referent requires a new
   identifier. Mint a new tactic ID for Stealth and obsolete TA0005.
5. **Prior-version and compatibility links** (`owl:priorVersion`,
   `owl:backwardCompatibleWith`/`incompatibleWith` analogues) as STIX properties on
   `x-mitre-collection`. ATT&CK has neither; lineage is reconstructed by sorting release names.
6. **Publish the evolution mapping as a first-class versioned artefact**, typed with
   COnto-Diff's complex operations (merge / split / move / substitute) rather than
   diffStix's eight untyped buckets. diffStix already computes the basic operations; typing
   them is what makes the bookkeeping-vs-intelligence split computable rather than asserted.
7. **Make the Navigator layer's `attack` version field mandatory.** It is optional and
   silently defaults to current, so every coverage layer is version-orphaned by default.

## Committed position

The field should stop treating "we used ATT&CK" as a citation and start treating an ATT&CK
label set as a dated artefact that carries its domain, its exact release, the bundle hash,
and a residual ledger of what normalization kept, merged and dropped — four lines that a
reviewer can check and that cost an author one JSON header and thirty lines of code —
while MITRE ports the two mechanisms it is missing from established ontology engineering:
an inexact-successor relation alongside `revoked-by`, and a typed, published evolution
mapping. ATT&CK-Norm should ship, but stripped: roll-up fires zero times across 27,000
attribution trials, 18 archival release profiles and 37,447 real label instances, so it
must be deleted or flag-gated, and the protocol must return a residual, not a set. What it
provably cannot deliver is meaning. It repairs identifiers, and it repairs them well enough
to move coverage-ranking τ from 0.931 to 0.992 and to recover roughly 47% of the attribution
penalty on pre-2020 artefacts — but it recovers +0.8 points post-v7 with a CI spanning zero
in two-thirds of conditions, it is silent on the 29.4% of v19 techniques that changed tactic
and the 6.1% that changed description under a stable ID, it collapses five distinct
identifiers into T1685 without saying so, it cannot represent a technique promoted to a
tactic, and on CTI-Bench it would confidently report seven unrepairable deprecations that
are in fact seven live mobile identifiers in a mis-typed row. Normalization buys
comparability of identifiers; it buys nothing about whether two identifiers mean the same
thing, and a paper that claims otherwise repeats the error it set out to diagnose.
