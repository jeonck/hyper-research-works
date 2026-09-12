# Step 6 — cross-locus reconciliation

Four investigators committed independently. They agree on more than they
disagree, and where they disagree the disagreement is productive: it forces the
manuscript onto narrower, defensible ground and strips it of three claims it was
comfortable making a few hours ago.

## What all four converge on

**The apparatus is real, and conceding it is what buys the argument.** L1
verified from the bundles that Enterprise identifier accounting is complete —
149 revocations, 149 edges, zero dangling, zero silent deletions. L4 confirmed
the same relation is never one-to-many. Any version of this paper that opens
with "ATT&CK churns and nobody handles it" is refuted by MITRE's own
`USAGE.md` in one paragraph. The argument has to start from the concession.

**The damage that remains is semantic, not referential.** L1: no tactic
crosswalk exists and TA0005 was recycled in place from *Defense Evasion* to
*Stealth*, same STIX identifier, object version untouched. L3: the substantive
rewrite clock runs at 10% in roughly eighteen months and has not slowed since
2020. L4: normalization returns all 674 identifier-stable techniques unchanged
across the release that dissolved Defense Evasion, signalling zero drift on the
most disruptive semantic event in the corpus. Three investigators reached the
same place from three directions.

**Adoption is the load-bearing empirical fact.** L1 measured it hardest: across
69 Navigator layers in the clones only five declare `versions.attack` and all
five are MITRE's own fixtures; of 57 published vendor layers, zero declare a
version, and 739 of their 2,143 annotations (34.5%) are revoked or deprecated at
v19.2. That single measurement does more work than any of the release-level
churn statistics.

## Where they pull against each other, and how it resolves

**L3 against the framing of the whole paper.** L3 refuses both horns: identifier
churn is episodic and currently mild, semantic churn is continuous and steady.
Its recurrence analysis then dissolves the "one-time 2020 trauma" reading that
the Enterprise-only view invites — five restructuring events across three
domains in eight years, a hazard of 0.106 per major transition, roughly one
somewhere in ATT&CK every 1.5 calendar years, with Mobile's 2018 renumbering
being the worst of them (identifier Jaccard 0.000 and, unlike Enterprise 2020,
*zero* recoverable). The manuscript adopts L3's two-clock model. The Enterprise
2020 event is one draw from a live hazard, not a closed wound, and ICS is
drawing right now.

**L2 against the experiment.** L2 was asked to audit the attribution design and
found a real defect: the design sets inter-labeller noise to zero rather than
holding it at a realistic level, which licenses separability but leaves
additivity untested. It then ran the missing factorial. The penalty survives
injected labeller noise at every boundary, but is attenuated 22–33% at ρ=0.4 in
the pre-restructuring regime, so the headline numbers are upper bounds and the
manuscript must say so in the results, not in a footnote. L2 also caught a
misnamed control: what the code calls `contemporaneous` is a back-projected
transcription, not a V-era system, and the real archival control scores 0.969 at
v1.0 against the back-projection's 0.668. Both corrections are adopted.

**L2 against L4, productively.** L2's stratification shows the modern drift
penalty is 2.5–7× larger on groups that have at least one unique technique
(+0.024 to +0.034, confidence interval excluding zero) than on those that do
not — drift bites hardest exactly where attribution is identifiable at all. L4,
looking at the same modern regime from the protocol side, finds normalization
buys only +0.8 points there with a confidence interval spanning zero in
two-thirds of conditions. Both are right and the combination is the honest
finding: the residual modern effect is small in aggregate, concentrated where it
matters most, and not repairable by identifier arithmetic.

**L4 against the contribution as originally conceived.** This is the sharpest
reversal. ATT&CK-Norm was going to be the paper's constructive centrepiece. L4
demonstrated that its roll-up branch never fires — a broader sweep confirms
three firings in 12,027 resolutions across every domain and major release — that
it collapses five identifiers into T1685 without saying so, that 119 of 149
Enterprise revocation edges demote a top-level technique onto a sub-technique,
and that on CTI-Bench it would confidently report seven unrepairable
deprecations which are in fact seven live Mobile identifiers sitting in a row
mis-typed as Enterprise. The protocol has been rewritten accordingly: roll-up is
off by default, and it returns a residual ledger — kept, merged, dropped,
demoted — rather than a set. The paper's constructive claim is now the reporting
contract, with normalization demoted to a bounded legacy-migration tool whose
limits are themselves a result.

## What the manuscript must therefore not say

- Not "revoked-by cannot express the v19 re-cut". It can, as merges; the defect
  is that merging is lossy and unannounced. (L1, L4; the earlier contradiction
  graph had this wrong and has been corrected.)
- Not "normalization restores comparability". It restores identifier
  comparability on legacy artefacts and buys almost nothing modern.
- Not "ATT&CK is unstable". Enterprise identifiers since 2020 are very stable;
  the instability is in meaning, in the tactic layer, and in other domains.
- Not any absolute attribution accuracy as a statement about attribution. Every
  number is an internal-consistency score computed inside one curator's graph.

## The thesis after reconciliation

Ontology drift in ATT&CK is a measurable, recurrent, and largely *unsignalled*
threat to the validity of CTI analytics. Its referential component is well
handled by MITRE and almost never used by consumers; its semantic component is
not handled at all, by anyone, and no mechanism in the ecosystem detects it. The
remedy is not a smarter crosswalk — the crosswalk is nearly as good as a
crosswalk can be — but a reporting discipline that makes the vocabulary of a CTI
artefact a declared, checkable property of that artefact.
