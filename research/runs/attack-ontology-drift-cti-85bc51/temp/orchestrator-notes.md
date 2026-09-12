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
