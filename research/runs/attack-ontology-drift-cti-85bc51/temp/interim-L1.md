# Interim L1 — Is ATT&CK ontology drift a solved bookkeeping problem or an unmeasured threat to validity?

Locus type: dialectical, must commit. Clusters: `solved-bookkeeping`, `pin-the-version`.
All figures below trace to a named file. Where I recomputed a number myself, I say so.

## 1. The "it is already solved" position, at full strength

MITRE does not merely tolerate drift; it operates a versioning regime that is better than
most scientific vocabularies.

**Immutable, addressable releases.** `/home/user/mitre-attack/attack-stix-data/index.json`
lists 41 Enterprise, 41 Mobile and 27 ICS versioned bundles (109 total; confirmed by file
count in the three domain directories). Every historical release is a frozen artefact at a
stable path. `USAGE.md` (867 lines) recommends the static-copy workflow in exactly these
terms at line 106: *"Downloaded copy is static, so updates to the ATT&CK catalog won't cause
bugs in automated workflows."* Pinning is not a workaround the community invented; it is the
documented first-class path.

**Typed, non-destructive retirement.** `USAGE.md` §"Working with deprecated and revoked
objects" (lines 816–824) is normative: *"Objects that are deemed no longer beneficial to
track as part of the knowledge base are marked as deprecated, and objects which are replaced
by a different object are revoked… In the case of revoked objects, a relationship of type
`revoked-by` is also created targeting the replacing object"*, and *"Revoked and deprecated
objects are kept in the knowledge base so that workflows relying on those objects are not
broken."* A `getRevokedBy()` helper and a `remove_revoked_deprecated()` filter ship in the
same document.

**And the contract holds, for Enterprise.** This is the part our own draft understates.
Recomputing from `enterprise-attack-19.2.json`: 858 attack-patterns — 697 live, 149 revoked,
12 deprecated — and **149 `revoked-by` edges with 149 distinct attack-pattern sources. Every
revoked Enterprise technique has exactly one successor; there are zero dangling revocations.**
`data/results/e1_e2_e3.json` agrees independently: across all 190 Enterprise survival rows,
`recoverable_via_revoked_by` equals `revoked` in every row and `absent` is 0 everywhere. No
Enterprise identifier has ever silently vanished.

**Change is computed and published.** `mitreattack-python/mitreattack/diffStix/changelog_helper.py`
(lines 204–213) defines nine change classes including `patches` — *"objects that have been
patched while keeping the version the same"* — so description edits are diffed and rendered,
not hidden. `attack-navigator/layers/spec/v4.5/layerformat.md` gives coverage artefacts a
`versions` object. CTID's ATT&CK Sync exists to flag mappings affected by a release.

A reviewer can fairly say: the map exists, it is free, it is complete for Enterprise, and
anyone who publishes an incomparable number chose not to use it.

## 2. The mechanical gaps

**(a) `revoked-by` is a total function that is never one-to-many.** In `enterprise-attack-19.2.json`
**zero** revoked techniques have more than one target. A split therefore cannot be represented;
MITRE encodes it as an N:1 merge onto the *narrowest* survivor. In v19, `T1562 Impair Defenses`
— the parent of thirteen sub-techniques — and `T1562.001 Disable or Modify Tools` and
`T1562.006 Indicator Blocking` **all point to `T1685 Disable or Modify Tools`**, while the other
ten siblings fan out to T1685.001–.004, T1686, T1686.001–.002, T1688, T1689, T1690. The crosswalk
is mechanically total and semantically wrong: it asserts that a parent concept equals one of its
own former children. Eight merge targets absorb 20 predecessor IDs and three chains need
transitive closure (recomputed; matches the count in the `revoked-by crosswalk` note title).
A pipeline that applies the official map to a historical parent-level label silently narrows
its extension.

**(b) Tactics have no crosswalk at all, and TA0005 was recycled in place.** In v19.2 there are
**zero `revoked-by` edges involving any `x-mitre-tactic`**. Comparing `enterprise-attack-18.1.json`
to `19.2`: the STIX object `x-mitre-tactic--78b23412-0651-46d7-a540-170a1ce8bd5a` keeps both its
UUID and its ATT&CK ID **TA0005**, while its name changes from *Defense Evasion* to *Stealth*,
its shortname from `defense-evasion` to `stealth`, and its `x_mitre_version` stays at 1.0; a new
TA0112 *Defense Impairment* is created alongside. Any analytic that joins on TA0005 across that
boundary compares two different concepts with no revocation, no version bump and no edge to
follow. **201 ID-stable live techniques changed `kill_chain_phases` across 18.1→19.2** (my count;
`e1_e2_e3.json` reports 198 for 18.0→19.0), three of them with no version bump.

**(c) `x_mitre_version` is not a change detector.** Recomputed directly from the 19 major-release
bundles over 8,359 carried-over live technique pairs: **1,366 description changes (16.3%), of
which 494 carried no `x_mitre_version` bump, while 1,076 version bumps carried no text change.**
MITRE's own `diffStix/README.md` line 120 concedes the discipline broke historically —
`other_version_changes` are *"unintended, but can be found in previous releases."* Pinning fixes
identity; it does not fix intension.

**(d) The non-destructive guarantee is Enterprise-only.** `changelog_helper.py` carries a
`deletions` bucket — *"ATT&CK objects which are no longer found in the STIX data"* — and deletions
are real. In `e1_e2_e3.json`, Mobile ATT&CK has 34 survival rows with `absent > 0`: all 76 of
v1.0's techniques are simply gone from v3.0 onward, with no tombstone, and five Mobile rows have
dangling revocations (3.0→17.0: 27 revoked, 25 recoverable).

**(e) Migration destroys provenance.** In `layers/spec/v4.5/layerformat.md` the `versions.attack`
field is `Required? = No` and defaults to *"Current version of ATT&CK"*; the Navigator upgrade
flow is manual, human-arbitrated, one-way, and writes no record into the output layer, so a
migrated coverage claim is indistinguishable from a native one.

**(f) ATT&CK Sync — evidence gap, flagged.** The vault note
`ctid-attck-sync-…` has *orphaned front matter*: its body is the text of a different note. Seven
B7-batch notes are affected. The claim "flags mappings, publishes no impact quantification"
currently rests on a summary line with no body behind it and must be re-collected before it
appears in the manuscript.

## 3. Adoption

`data/results/e9_version_declaration.json` reports 0 ATT&CK-version declarations across 19 files
in three repos — but 2 of those repos contributed only 2 files each. It is too thin to carry the
claim. I therefore measured adoption where coverage claims actually live, in Navigator layers.

Across the local clones (`/home/user/ext/`), **69 Navigator-format layer files**: DeTT&CT 57,
attack-navigator 8, mitreattack-python 4. **Five declare `versions.attack` — and all five are
MITRE's own sample or test fixtures.** Of DeTT&CT's 57 published vendor threat-report layers
(CrowdStrike, FireEye/Mandiant, Red Canary, Cisco Talos, Kaspersky, McAfee, Sophos, PwC, Rapid7,
Recorded Future, ACSC), **zero declare an ATT&CK content version**: 39 are layer format 2.2, where
no such field exists, and 18 are format 4.1–4.3, where the field exists and all 18 omit it.

The cost, measured: those 57 layers carry **2,143 technique annotations, of which 739 (34.5%) name
an identifier that is revoked or deprecated in v19.2**; 49 of 57 files contain at least one; 72 of
the dead annotations are deprecations with no successor; and 5 name IDs absent from v19.2 entirely
(four Mobile IDs, one of them on a layer whose `domain` is `enterprise-attack`). Opened today in a
current Navigator, every one of these silently re-bases onto v19.2.

Label corpora agree (`data/results/e7_artifacts.json`): rcATT 107 of 215 IDs invalid at v19.2
(49.8%; 38.0% of 6,235 label instances; 99 repairable by revocation chain, 8 not); TRAM bootstrap
43 of 537 (8.0%, all repairable); CTIBench-ATE 120 IDs, best-fit release v14.0, **zero releases at
which the label set is fully consistent**. And declaring a version is not sufficient:
`/home/user/ext/mitre-ttp-mapping` announces a deliberate "remap to MITRE ATTACK 12.0" and its
inherited TRAM split still carries 203 dead label occurrences (3.6%), 128 of them T1064, revoked
five releases before the declared target.

## 4. Corrections to our own numbers

1. `e1_e2_e3.json` records **1,358** description changes; the bundles give **1,366** (and 1,076,
   not 1,072, bumps with no text change). Pick one computation and state its normalization.
2. The scaffold's "all 106 public ATT&CK releases" should read **109 versioned bundles** (41/41/27).
3. "revoked-by is 1:1 and cannot express the v19 1:N re-cut" is **wrong as stated** and will be
   shot down: every v19 revocation has exactly one successor. Restate as the semantic defect —
   parents merged onto former children.
4. "survival since v7.0 is above 0.97": v7.0→v19.0 is **0.9696**.
5. CTIBench-ATE is 120 unique IDs with best fit at **v14.0**, not "115 techniques, v15-era".

## Committed position

Drift is **not** a solved bookkeeping problem, and the paper should say so on narrower and harder
ground than the draft currently occupies. MITRE's identifier accounting for Enterprise is in fact
complete — 149 revocations, 149 edges, zero dangling, zero silent deletions — and conceding that
loudly is what buys the rest of the argument. The apparatus fails on three things it was never
built to carry: it has no crosswalk for tactics and recycled TA0005 from *Defense Evasion* to
*Stealth* in place while 201 techniques changed tactic; it cannot represent a split, so it merges
parents onto their own former children; and it emits no semantic-change signal, with 494 of 1,366
description rewrites carrying no version bump. Those gaps would still be bookkeeping if the
apparatus were used, and it is not: of 57 published vendor coverage layers, zero declare an ATT&CK
version and 34.5% of their 2,143 annotations are dead at v19.2. Mechanism-insufficient plus
adoption-absent is a threat to validity, not a hygiene complaint. **The single piece of evidence
that would overturn me:** a representative sample of published CTI artefacts — vendor layers,
benchmark label files, detection mappings — in which a majority carry a resolvable release pin
*and* mechanically applying `revoked-by` forward from that pin reproduces an independently authored
current-version mapping to within inter-analyst agreement. If migration is that faithful and that
common, the remaining gaps are a footnote and this paper is a reporting-discipline note.
