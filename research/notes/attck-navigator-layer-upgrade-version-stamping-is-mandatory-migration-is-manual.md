---
title: 'ATT&CK Navigator layer upgrade: version stamping is mandatory, migration is
  manual, irreversible and unaudited'
id: attck-navigator-layer-upgrade-version-stamping-is-mandatory-migration-is-manual
tags:
- attack-ontology-drift-cti-85bc51
- critique
- rebuttal
created: '2026-09-12T13:22:50.650192Z'
source: https://github.com/mitre-attack/attack-navigator/blob/master/USAGE.md
status: draft
type: note
tier: institutional
content_type: docs
deprecated: false
summary: Layer format mandates a versions.attack stamp and Navigator ships a guided
  cross-version upgrade, but the migration is human-judgement, writes no provenance
  and cannot be revisited — the official remedy launders a coverage claim's history.
---

## What it is
`USAGE.md` and the layer-format specs (`layers/spec/v1.0` … `v4.5/layerformat.md`) from MITRE's `attack-navigator` repo, read from a sparse clone at `/home/user/ext/navigator`. ATT&CK Navigator is the de facto tool in which practitioners express coverage claims, threat-actor profiles and gap analyses as "layers."

## The position it takes (third rebuttal artefact: version discipline is built into the file format)
1. **Version stamping is mandatory in the artefact itself.** Every Navigator layer carries a `versions` object: `{"attack": "18", "navigator": "5.2.0", "layer": "4.5"}`. A coverage claim serialised as a layer is *self-describing about which ATT&CK version it was made against*, and there have been 15 layer-format spec versions (v1.0 → v4.5) tracking this. The reporting discipline the thesis wants to prescribe is, for this artefact class, already mandatory schema.
2. **A guided cross-version migration workflow exists.** Verbatim from USAGE.md: *"The layer upgrade interface allows users to upgrade an ATT&CK Navigator layer created on a previous version of ATT&CK to the current version of the dataset."* It walks the user through techniques added since the layer was created, techniques whose definitions changed, and — verbatim — *"if any annotated techniques have been removed or replaced by new techniques and in the latter case copy annotations to the replacing technique(s)."* It also lets the user *"verify what techniques haven't changed since the layer was created."* The feature request (issue #181) asked for a UI matching the older `update-layers` script, with *"notification to users of the revocations that were followed."*

## Strength of evidence
High for what exists (primary docs + spec files, read locally). Zero evidence on adoption: nothing here shows practitioners *use* the upgrade flow or that published coverage claims cite `versions.attack`.

## For or against the thesis
**Against on paper; the thesis's best counter-punch is hiding in the same document.**

*Against:* an SCI-level claim that the community lacks a normalization protocol is hard to sustain when the dominant tool ships one, and the dominant file format mandates a version stamp.

*For, on close reading of the mechanism's properties:*
- The migration is **human-in-the-loop and judgemental**, not deterministic. "Copy annotations to the replacing technique(s)" is a decision the analyst makes per technique. Two analysts migrating the same layer from v16 to v19 can produce different layers — so migration re-injects exactly the inter-rater variance documented in Virkud et al., and does so *invisibly*, because the output layer is stamped only with the destination version.
- It is **irreversible and unaudited**. Verbatim: *"You will not be able to return to the layer upgrade interface after the sidebar is closed."* No migration provenance is written into the layer: nothing records which techniques were dropped, which annotations were copied to which successor, or which sections were skipped. The upgraded layer is indistinguishable from one authored natively at v19. **A migrated coverage claim launders its own history** — which is precisely the reproducibility failure the thesis is about, and it is a failure of the official remedy, not of its absence.
- USAGE.md also notes *"Users will not be prompted to upgrade default layers to the current version of ATT&CK if they are outdated"* — stale layers circulate silently.

## Fidelity
High — quotations read verbatim from the cloned `USAGE.md` and the `versions` block read from `layers/spec/v4.5/layerformat.md`. Sources: https://github.com/mitre-attack/attack-navigator/blob/master/USAGE.md and https://github.com/mitre-attack/attack-navigator/issues/181
