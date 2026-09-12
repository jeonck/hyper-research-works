---
title: Formal drift taxonomy and the ATT&CK-Norm protocol
id: formal-drift-taxonomy-and-the-attck-norm-protocol
tags:
- attack-ontology-drift-cti-85bc51
- measurement
created: '2026-09-12T13:22:37.854986Z'
source: https://github.com/mitre-attack/attack-stix-data
status: draft
type: note
tier: ground_truth
content_type: dataset
deprecated: false
summary: Six-kind drift taxonomy, the normalization protocol, and the reporting contract
---

# Formal drift taxonomy and the ATT&CK-Norm protocol

Fidelity: AUTHORED FORMALISM for this study. The definitions are ours; every
quantity they name is measured by the scripts in `code/`.

## The object

Let a release be `R_v = (T_v, S_v, G_v, E_v, rev_v, sub_v, d_v)` where `T_v` is
the set of technique identifiers published at version `v`; `S_v ⊆ T_v` are
identifiers flagged revoked and `D_v ⊆ T_v` deprecated; the **live vocabulary**
is `L_v = T_v \ (S_v ∪ D_v)`. `G_v` is the set of intrusion-set identifiers and
`E_v ⊆ G_v × T_v` the published `uses` edges. `rev_v : S_v → T_v` is the
revocation map, `sub_v : T_v → T_v` the sub-technique parent map, and
`d_v : T_v → Σ*` the natural-language description.

A CTI artefact authored at version `v` is a set of identifiers `A ⊆ L_v`. An
analytic executing at version `w > v` interprets `A` against `L_w`. Ontology
drift is any difference between `R_v` and `R_w` that changes that
interpretation.

## Six kinds of drift

1. **Extension** — `L_w \ L_v ≠ ∅`. New techniques. Harmless to `A` itself, but
   it moves every denominator computed over the vocabulary (§ coverage).
2. **Revocation** — `t ∈ L_v ∩ S_w`. The identifier still exists but no longer
   denotes; `rev_w` names its successor. Mechanically repairable.
3. **Deprecation** — `t ∈ L_v ∩ D_w` with no successor. The concept was
   withdrawn. Not repairable: there is nothing to map to.
4. **Refinement** — `t ∈ L_v ∩ L_w` but `{c : sub_w(c) = t}` grew. The identifier
   survives and its extension narrows, because behaviour that used to be
   recorded under `t` is now recorded under its children. An artefact written
   at `v` and one written at `w` can describe identical behaviour with
   non-identical identifier sets, and neither is wrong.
5. **Reassignment** — the tactic set or platform set of `t` changes while `t`
   stays live. Any analytic that groups by tactic silently regroups.
6. **Semantic drift** — `t ∈ L_v ∩ L_w` and `d_v(t) ≠ d_w(t)`. The identifier
   and the hierarchy are untouched; only the meaning moved. This is the kind no
   identifier arithmetic can detect, and the kind every "just pin the version"
   remedy ignores.

Kinds 2–4 are *identity* drift and are visible in the STIX data. Kinds 5–6 are
*intension* drift: nothing in the bundle marks them as breaking changes.

## ATT&CK-Norm

`normalize(A, R_w)` maps an artefact onto a target release:

1. **Resolve.** For each `t ∈ A`, follow `rev_w` transitively (bounded at ten
   hops, cycle-guarded) to a terminal identifier `t*`.
2. **Accept.** If `t* ∈ L_w`, keep it.
3. **Roll up.** Otherwise, if `t*` has a parent under `sub_w` (or, absent the
   relationship, under the dotted-identifier convention), resolve that parent
   and keep it if live.
4. **Drop.** Otherwise discard `t` and record it: a dropped identifier is a
   *deprecation without successor*, and the honest report is that the artefact
   asserted something the current ontology no longer represents.

The protocol is deliberately minimal. Its value is not sophistication; it is
that this much is enough to repair a measurable share of the damage, that the
share is measurable at all, and that what remains after it is a genuine loss of
resolution rather than a bookkeeping error. Step 3 is where resolution is lost:
a v6-era `T1055` recovers as `T1055`, not as the sub-technique a modern analyst
would have written, and the attribution experiment is what puts a number on the
difference.

## What a drift-aware CTI report must declare

- the ATT&CK domain and the exact release version of every identifier set it
  publishes, in the artefact itself rather than in prose;
- whether identifiers were normalized, and to which target release;
- the count of identifiers dropped as unrepairable, not merely the ones kept;
- for any comparison across time, whether both sides were projected onto a
  single reference release before comparison.
