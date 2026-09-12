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

## After the depth investigations — what the adversarial stage actually bought

Worth recording precisely, because the case for running a pipeline like this
rests on whether the critics change anything or merely decorate.

Four investigators produced five corrections that a normal writing process would
not have caught:

1. **A false claim, killed.** I had written that `revoked-by` cannot express the
   v19 one-to-many re-cut. L1 checked: the relation is never one-to-many in any
   domain, and the re-cut is encoded as merges onto the narrowest survivor. The
   defensible claim is narrower — lossy and unannounced, not impossible — and
   the contradiction graph has been corrected.
2. **A dead code path in the contribution.** L4 found that the normalization
   protocol's roll-up branch never fires. My own broader sweep: three firings in
   12,027 resolutions across every domain and major release. The branch was the
   only part of the protocol that could invent an assertion the artefact never
   made, and it bought nothing. It is now off by default and the protocol returns
   a residual ledger instead of a set.
3. **An untested assumption in the experiment.** L2 noticed that the design sets
   inter-labeller noise to zero rather than holding it at a realistic level,
   which licenses separability but leaves additivity untested — and then ran the
   missing factorial. The penalty survives injected noise but attenuates 22-33%
   at high noise in the legacy regime, so the headline numbers are upper bounds.
4. **A mislabelled control.** What the code calls `contemporaneous` is a
   back-projected transcription, not a V-era system. The real archival control
   scores 0.969 at v1.0 against the back-projection's 0.668. Both now get
   reported.
5. **A corrupted evidence base.** Ten of 112 vault notes carried front matter and
   body from different sources. Any claim drawn from one would have been
   attributed to a source that never made it — the paper's own failure mode,
   inside the paper's own corpus. All ten quarantined; the load-bearing ones
   re-derived from artefacts I read myself.

Two of those five would have been fatal in review. The fifth would have been
fatal in a different way.

One methodological note for the write-up: the numbers survived the protocol
change unchanged, which is itself worth stating — it means the roll-up branch was
never doing work, not that removing it cost accuracy.

## Synthesis interrupted, and what that cost

The synthesizer was cut off by a usage limit partway through its second pass,
with Sections 1 to 6 written and 7 to 12 gone (pass two overwrites rather than
appends, so the pass-one text for those sections was lost). I completed the
manuscript from the same evidence digest, reference registry and drafting brief
the synthesizer was working from, which is the recovery the pipeline's own
recovery section prescribes: the report was incomplete, so finishing it is
completing the single synthesis pass rather than regenerating a finished one.

Three things came out of doing that stretch by hand.

**Two investigator findings became reproducible experiments.** L1's layer-adoption
count and L4's merge-cardinality numbers were the strongest adoption and
protocol-limit evidence in the whole study, and both existed only inside an
agent's note. They are now `code/29_layer_adoption.py` and
`code/30_ledger_on_corpora.py`, and both reproduce the reported figures: 5 of 69
published coverage layers declare a release, 917 of 4,821 annotations are dead at
v19.2, TRAM's bootstrap corpus collapses 537 classes to 503 with 0.1475 of its
label instances landing in a merged class. Anything load-bearing that lives only
in an agent's prose is a liability; this is the second time in this run that
moving a claim into code changed my confidence in it.

**One number was wrong.** The manuscript carried ρ = +0.377, p = 0.134 for the
leading-indicator correlation, taken from an investigator's ad-hoc script. The
consolidated version in `code/19_temporal_structure.py` gives ρ = +0.429,
p = 0.087 on the same question, because the two normalise the signal differently.
The manuscript now carries the number the committed script produces. The finding
is unchanged — no leading indicator reaches significance — but the paper would
have shipped a figure no reader could reproduce.

**The length ceiling forced an editorial decision worth recording.** The gate
counts every word in the file, tables included, and caps at 12,000. Rather than
cut argument, I condensed two tables whose per-row content is already plotted in
a figure and pointed to the full versions in the reproduction package. That is
the ordinary journal trade, and it is the right one here: Figure 4 carries the
per-transition decomposition better than Table 5's eighteen rows did.

## What the critics actually bought, measured

Forty-seven findings across four critics, thirteen of them critical. The useful
way to score a stage like this is not the count but what would have shipped
without it.

Six of the thirteen criticals were places where the manuscript's prose
contradicted the manuscript's own results files. Not one of them was a
disagreement about interpretation:

- "removing every rank-1 flip" — the data leaves the v6.0 flip standing, so the
  paper's own protocol was being credited with a clean sweep it does not have.
  The corrected sentence is now evidence *against* the protocol, which is where
  the evidence actually points.
- "eleven of the twelve post-restructuring rows" excluding zero — it is nine.
  Two rows straddle zero and one sits on it. The overclaim was in the direction
  that flatters the paper's central modern-regime argument.
- the noise-factorial figures matched nothing on disk — they came from an
  investigator's scratch run rather than the committed script. Same phenomenon
  as the leading-indicator correlation earlier: a number that travelled from an
  agent's prose into the manuscript without passing through code.
- "naive is a uniform worst case" — the archival condition scores *below* naive
  at every release, which the study had computed and never read. A limitation
  stated backwards is worse than a limitation omitted.
- prevalence weighting "makes the artefact larger, not smaller" — true for
  legacy artefacts, false from v10.0 onward. The sentence had been written once
  when only the legacy rows existed and never revisited.

The seventh critical is the most interesting because it is not an error of
arithmetic. The draft said intensional drift is un-inferable; diffStix will
compute a line-level description diff between any two releases. The claim had to
be narrowed to what is actually true — no signal exists in the artefact a
consumer holds — and narrowing it made it sharper, because the objection "MITRE
does publish diffs" now has an answer instead of being a hole.

The width critic found the one thing that genuinely weakens the paper: MITRE's
own Sightings telemetry says the top 15 of 353 techniques carry over 80% of
observed events, against our documentation-derived 0.285 for the same cut. Our
long-tail refutation holds for the written CTI corpus and does not reach the
telemetry distribution. That is now stated as an open question. A reviewer
holding the Sightings report would have found it in ten minutes, and finding it
ourselves is the difference between a limitation and a rebuttal.

Process conclusion worth keeping: every number that entered the manuscript from
an agent's prose rather than from a committed script was wrong or unverifiable.
Three separate instances in one run. The rule that follows is mechanical — if a
figure is load-bearing, it lives in code before it lives in a sentence.
