---
title: 'ATT&CK Navigator layer file format: the ATT&CK content version is an optional
  field that silently defaults to current'
id: attck-navigator-layer-file-format-the-attck-content-version-is-an-optional-field
tags:
- attack-ontology-drift-cti-85bc51
- coverage-claims
created: '2026-09-12T13:19:50.745503Z'
source: https://github.com/mitre-attack/attack-navigator/blob/master/layers/spec/v4.5/layerformat.md
status: draft
type: note
tier: institutional
content_type: docs
deprecated: false
summary: 'Navigator layer spec: versions.attack is optional and defaults to ''current
  ATT&CK''; formats 1.x-3.0 had no ATT&CK version at all; version-less layers are
  silently re-based; minor versions truncated; upgrade is manual, one-way and unrecorded.'
---

# What it is

The MITRE ATT&CK Navigator is the reference tool in which practitioners and vendors
author, store and publish "ATT&CK coverage" as a colour-coded heatmap over the matrix.
Coverage artefacts circulate as *layer files* — JSON documents conforming to the
"ATT&CK Navigator Layer File Format Definition". This note is based on a direct read of
the repository source, cloned anonymously at commit `734a1caba29fcd51f20b9ca239ce652b3354a47e`
(HEAD, 10 Sep 2026), not on blog summaries. Read in full: `layers/spec/v1.0` through
`layers/spec/v4.5` `layerformat.md`, `CHANGELOG.md`, `USAGE.md`,
`nav-app/src/app/services/data.service.ts`, `nav-app/src/app/classes/view-model.ts`,
`nav-app/src/app/classes/version-changelog.ts`, `nav-app/src/app/tabs/tabs.component.ts`.

# ANSWER: does a layer declare an ATT&CK version?

**Yes, but only since layer format v4.0 (Navigator v4.0, 27 October 2020), and the field
is OPTIONAL.** This is the central versioning fact for coverage artefacts.

Layer format v1.0, v1.1, v1.2, v1.3, v2.0, v2.1, v2.2 and v3.0 each define a single
scalar property, documented in the property table as:

    | version | String | Yes | n/a | Must be "3.0" |

i.e. the *layer-format* version only. **There is no field anywhere in layer formats 1.x–3.0
that records which ATT&CK content release the annotations were made against.** Every
coverage layer authored before late October 2020 — which includes the entire
pre-sub-technique era and the sub-techniques beta (layer format v3.0) — is therefore
*version-orphaned by construction*: the ATT&CK release it scores cannot be recovered
from the artefact.

Layer format v4.0 replaced the scalar with a `versions` **object**. `CHANGELOG.md` under
`# v4.0 - 27 October 2020` states the change as: replaced the `version` field with a
`versions` object which specifies the layer format, Navigator, and ATT&CK content
versions, in support of the mixed domains and versions update.

The Version Object property table in `layers/spec/v4.5/layerformat.md` reads:

    | attack    | String | No  | Current version of ATT&CK | ATT&CK version of this layer |
    | navigator | String | Yes |                           | Must be at least "4.9.0"     |
    | layer     | String | Yes |                           | Must be "4.5"                |

Three citable specifics follow:

1. **The ATT&CK content version is the only one of the three that is NOT required.**
   `navigator` and `layer` are mandatory; `attack` is `Required? = No`. The tool version
   and the file-schema version are enforced; the *semantic* version — the one that
   determines what T1055.012 means — is optional.
2. **Its documented default is "Current version of ATT&CK".** Not "unknown", not an
   error. Earlier specs pinned the default to a concrete number as it drifted — v4.0 and
   v4.1 say `Current version of ATT&CK: "8"`, v4.2 says `"9"`, and from v4.3 onward the
   spec stops naming a number and says simply `Current version of ATT&CK`, i.e. whatever
   the loading instance happens to serve.
3. **The default is silent and it floats.** A layer with no `versions.attack` is not
   rejected and does not warn; it is re-interpreted against *today's* ATT&CK.

# What happens to a saved layer when the underlying release changes

Three distinct behaviours, all verifiable in source:

**(a) A version-less layer is silently re-based onto the current release.**
`nav-app/src/app/classes/view-model.ts` (deserialization of the version block) carries the
comment `// layer with no specified version defaults to current version` immediately above
`this.version = this.dataService.latestVersion.number;`, and only overrides it if
`'versions' in obj` and `'attack' in obj.versions` and the value is a non-empty string.
`data.service.ts::getDomainVersionID` repeats the same fallback: `if (!versionNumber)`
then `versionNumber = this.versions[0].number;` with the identical comment. So the
artefact does not become invalid — it becomes *quietly wrong*: the same technique IDs are
looked up in a different ontology, the scores ride along unchanged, and nothing in the
rendered heatmap indicates the substitution.

**(b) Minor ATT&CK versions are truncated away.** The parser extracts the version with
`obj.versions.attack.match(/\d+/g)[0]` — the first run of digits only. `isSupported()`
does the same. A layer declaring ATT&CK "12.1" is loaded as "12". **Navigator layers
therefore have no better than major-release resolution**, even when the author wrote a
point release. Point releases are precisely where silent description/scope rewrites land,
so this is a fidelity ceiling on any version-aware re-analysis of published layers.

**(c) If a version IS declared and is older than current, the user is offered a manual,
one-way, non-resumable "Layer Upgrade" workflow.** Added in Navigator v4.0 (`CHANGELOG`,
issue #181). `USAGE.md` §"Upgrading a Layer to the Current Version" describes stepping
through added techniques, changed techniques, and removed/replaced techniques, copying
annotations forward. Two properties matter for reproducibility: annotation transfer is a
**human judgement call** (for tactic changes, USAGE.md instructs the user to *drag and
drop* the annotated tactic onto the new tactic(s)), and `USAGE.md` warns in bold: you will
not be able to return to the layer upgrade interface after the sidebar is closed. The
upgrade is also *not* recorded in the layer — there is no provenance field for "this layer
was migrated from ATT&CK vN by hand", so a migrated layer is indistinguishable from a
natively-authored one.

# The drift taxonomy is already encoded in MITRE's own tool

`nav-app/src/app/classes/version-changelog.ts` defines `VersionChangelog` with exactly six
buckets, with these source comments:

    additions      // new objects added to newest version
    changes        // object changes between versions
    minor_changes  // changes to objects without version increments
    deprecations   // objects deprecated since older version
    revocations    // objects revoked since older version
    unchanged      // objects which have not changed between versions

`data.service.ts::compareVersions(oldDomainVersionID, newDomainVersionID)` populates them
by joining old and new technique+subtechnique sets on STIX id, then branching. The
decision procedure is directly usable as a normalization primitive, and its detail is the
finding:

- Objects absent from the old version → `additions`, **except** if already
  deprecated/revoked in the new version, in which case they are skipped entirely (a code
  comment flags this as a data-integrity case, e.g. a sub-technique deprecated with its
  parent tie erroneously severed). So MITRE's own tool has a known class of objects that
  fall out of the accounting.
- `latestTechnique.modified == prevTechnique.modified` → `unchanged`. Equality of the STIX
  `modified` timestamp is the *only* unchanged test.
- Otherwise: newly `revoked` → `revocations`; newly `deprecated` → `deprecations`;
  else if `compareVersion(prev) != 0` (the object's `x_mitre_version` moved) → `changes`;
  **else → `minor_changes`**.

That last branch is the direct in-tool confirmation of "silent rewriting": an object whose
`modified` timestamp advanced but whose `x_mitre_version` did **not** is classified as a
*minor change*. MITRE's own data model admits edits that leave no version increment, and
the Navigator surfaces them in a separate, easily-skipped review pane. Any study of silent
description rewrites can define its population exactly as the `minor_changes` bucket:
`modified` advanced ∧ `x_mitre_version` unchanged ∧ ¬revoked ∧ ¬deprecated.

# Further citable specifics

- **Warnings are about the schema, not the ontology.** `tabs.component.ts::versionMismatchWarning`
  compares the *layer-format* version against `globals.layerVersion`: a minor mismatch gets
  a 6.5-second snackbar ("Please update to v… for optimal compatibility"), a major mismatch
  gets a blocking dialog. There is no equivalent hard stop for an ATT&CK *content* mismatch —
  that path only offers the optional upgrade dialog.
- **Default/embedded layers are never prompted at all.** `USAGE.md`: users will not be
  prompted to upgrade default layers to the current version of ATT&CK if they are outdated;
  `upgradeLayer(..., defaultLayers = true)` acts as if the user declined. Vendor pages and
  iframes that embed a coverage layer by URL therefore render stale ontologies with no
  version cue to the viewer whatsoever.
- **A real silent-failure regression is on record.** `CHANGELOG.md`, `# v4.5.1 - 21 October 2021`,
  "Fixes support for ATT&CK versions with more than 1 digit (ex. ATT&CK v10)": uploaded
  layers *without* a specified ATT&CK version would try and fail to load ATT&CK v1;
  layers using v10 would load as v1; and **downloaded layers using ATT&CK v10 would claim
  they use ATT&CK v1**. For roughly the v10 window, the version stamp written into exported
  layers was wrong. Version metadata in the wild is thus not merely absent-by-default but
  demonstrably corrupt for an identifiable cohort.
- **Custom-collection layers cannot be upgraded at all.** `CHANGELOG` v4.8.0 notes layers
  built from a custom Collection or STIX bundle (`customDataURL`, layer format v4.4) support
  all standard features "apart from upgrading the layer to a newer ATT&CK version".
- **Cross-version layer algebra is forbidden.** `USAGE.md` §"Creating Layers from Other
  Layers": layers can only inherit properties from other layers of the same domain and
  version. MITRE's tool refuses to average/diff coverage across ATT&CK versions — which is
  exactly what round-over-round vendor coverage claims do rhetorically.
- **Navigator no longer ships a version list.** `CHANGELOG` v5.0.0 removed the hardcoded
  ATT&CK version list from `config.json` in favour of the live
  `collection_index_url` = `https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/index.json`.
  Which historical versions a given Navigator instance can even *render* is now a function
  of a remote index at load time, not of the deployed artefact.

# Why this matters to the thesis

This is the mechanism by which coverage claims lose comparability, documented in the
vendor-neutral reference implementation:

1. The unit of published coverage (the layer) makes the ontology version **optional**, and
   defaults it to "whatever is current" rather than "unknown".
2. Absent a declared version, re-opening an old coverage artefact **silently re-scores it
   against a different technique set** — the denominator changes underneath a fixed
   numerator. A layer scoring 150 techniques reads as a different coverage percentage after
   a release that adds techniques, with no edit and no warning.
3. Where a version *is* declared, migration is manual, lossy, human-arbitrated, one-way,
   unrecorded in the artefact, and impossible for custom-collection layers.
4. Resolution is capped at the major release, so point-release silent rewrites are
   invisible to the format.

The normalization protocol argued for in the thesis can therefore be grounded in a concrete
minimum: a coverage claim is uninterpretable unless it carries (domain, ATT&CK major.minor,
STIX collection index pin, denominator definition, and migration provenance) — and the
Navigator format as specified supplies at most the first, optionally, at major granularity.

# Fidelity

**Primary-source, full-text, high fidelity.** Repository cloned and read directly at
commit `734a1caba29fcd51f20b9ca239ce652b3354a47e`; spec tables, `CHANGELOG` entries with
their release dates, `USAGE.md` prose and TypeScript source all read in the working tree.
Property-table rows, source-code comments and the `VersionChangelog` field comments quoted
above are transcribed from the files. Prose from `USAGE.md` and `CHANGELOG.md` is rendered
in close paraphrase rather than as quotation where line-wrapping made exact reproduction
unsafe; the `layerformat.md` table rows and the `version-changelog.ts` field comments are
verbatim. Not verified: how any *third-party* tool that emits Navigator layers handles the
`versions.attack` field, and the empirical prevalence of version-less layers in the wild
(worth measuring — a corpus scan of public `.json` layers on GitHub would quantify it).
