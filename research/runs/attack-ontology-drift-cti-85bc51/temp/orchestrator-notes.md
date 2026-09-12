## Wave 1 dispatched (8 batches, B1-B8)

Thinking while fetchers run.

The measurement is already in and it has a shape I did not expect. The story is
NOT "ATT&CK churns constantly and everything rots". It is sharper and more
interesting than that:

1. There is one catastrophic event — the v7.0 sub-technique restructuring
   (March 2020). Identifier Jaccard across that boundary is 0.222; 129
   techniques revoked in a single release; 750 group->technique edges removed
   and 1235 added. Every pre-v7 identifier set has a half-life of 0.4-2.2 years
   and all of it is the same event.
2. Since v7.0 no release cohort has lost half its identifiers. Ongoing
   identifier churn is genuinely mild (survival 0.97+ to the present).
3. But two slower processes never stopped: silent semantic rewriting (46.5% of
   v11.0's ID-stable techniques have edited descriptions by v19.0, mean token
   Jaccard 0.895) and periodic bookkeeping bursts (v18->v19 revoked the entire
   T1562 Impair Defenses family into T1685/T1686 — 47% of that transition's new
   edges for existing groups are re-mapping, not intelligence).

So the honest thesis is dialectical: the ontology is far more stable than the
v7.0 trauma suggests, AND the residual drift is concentrated, unannounced and
lands precisely on the most-used identifiers. A reader who concludes "pin a
version and you are fine" is half right — pinning fixes identifier matching but
not semantic drift, and it silently freezes the analytic against a vocabulary
the field has moved past.

The strongest rebuttal I expect from B4: "revoked-by mappings exist, so this is
solved bookkeeping." Our own E2 concedes the premise — 100% of revoked
identifiers resolve — and then refutes the conclusion: E5 shows normalization
recovers only 42-53% of the attribution penalty at k=10, because resolution is
lossy in granularity, not just in identity. That concession-then-refutation is
the spine of the argument.

Open question for the loci stage: is the right unit of analysis the identifier
or the *behaviour*? If ATT&CK is a moving description of a fixed reality, then
drift is a measurement instrument problem, and the paper should say so in
instrument terms — calibration, not decay.

## After wave 1 (all eight batches returned) — what the corpus changed about the thesis

Three things arrived that I did not have when I wrote the first note, and each
one moves the argument.

**The apparatus is better than I assumed, and that makes the paper harder and
better.** B1, B4, B7 and B8 read MITRE's own artefacts rather than blog posts
about them: immutable per-release bundles, typed revoked-by edges, retained
tombstones so dependent workflows do not break, diffStix computing an eight-class
change taxonomy including line-level description diffs, Navigator mandating a
layer version stamp. If I had written the naive version of this paper — "ATT&CK
churns and nobody handles it" — a reviewer holding USAGE.md would have destroyed
it. The paper has to concede the apparatus completely and then attack on two
specific fronts: mechanism (revoked-by is 1:1 and cannot express v19's 1:N
re-cut; one revocation promoted a technique to a *tactic*, a cross-layer move no
identifier crosswalk can represent) and adoption (zero version declarations
across nineteen documentation files in three deployed corpora; six of eight
sample layers in MITRE's own Navigator repo carry no ATT&CK version; Navigator
silently re-scores a version-less layer against today's release and truncates
"19.1" to "19").

**The strongest objection is empirical, not rhetorical.** Virkud et al. show
products disagree on the ATT&CK label for the same behaviour about half the time
*within one pinned release*. That is a noise floor far larger than most of my
per-release drift penalties. The answer is not to argue the noise is small — it
is to point out that my design holds the labelling process fixed across
conditions, so the noise cancels in the contrast and what remains is vocabulary
alone. That is a claim about experimental design, and L2 is auditing it rather
than asserting it, which is the only way it survives review.

**Someone else already ran this experiment, in biology.** Tomczak et al. froze a
pipeline, swept the Gene Ontology version, and showed the biological conclusions
moved. That is the template, it is a decade old, and it sets the bar: showing
scores change is not enough, conclusions must change. E10 now does that — the
named actor changes in 72-79% of pre-restructuring observations, and 2.2% even
across a single release boundary; mitigation leaderboards reorder at tau 0.665
and normalization restores them to 0.968.

**What I got wrong and am fixing.** My first instinct was to headline the
catastrophic v1-v6 numbers. They are real but they are one event, and a reviewer
would say so in the first paragraph of their review. The honest headline is the
one the half-life analysis forces: identifier churn is episodic and currently
mild, semantic drift is continuous, and the ecosystem has no mechanism that
detects the second at all — x_mitre_version has precision 0.447 and recall 0.641
as a change detector, which is barely better than not looking.
