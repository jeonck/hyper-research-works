---
title: 'OBO Foundry Principle 19: Stability of Term Meaning (referent stability, obsoletion
  mechanics, replaced_by vs consider)'
id: obo-foundry-principle-19-stability-of-term-meaning-referent-stability-obsoletion
tags:
- attack-ontology-drift-cti-85bc51
- ontology-versioning
created: '2026-09-12T13:20:21.081963Z'
source: https://obofoundry.org/principles/fp-019-term-stability.html
status: draft
type: note
tier: institutional
content_type: policy
deprecated: false
summary: Artefact-read policy forbidding referent-changing edits at a stable ID and
  specifying obsoletion mechanics (deprecation flag, visible label prefix, no dangling
  axioms, exact vs inexact successors, controlled obsolescence reasons) - the protocol
  ATT&CK lacks.
---

## What it is

OBO Foundry Principle 19, "Stability of Term Meaning" (`principles/fp-019-term-stability.md`). Read as an **artefact**: cloned from `github.com/OBOFoundry/OBOFoundry.github.io` and read in full from disk, so the text below is ground truth, not a search summary.

## Concept/mechanism it contributes

The principle states the rule that ATT&CK does not have, verbatim:

> "The definition of a term MUST always denote the same thing(s)--known as "referent(s)"--in reality. If a proposed change to the definition would substantially change its referents, then a new term with new IRI and definition MUST instead be created."

and

> "If changing a term definition would change its referents, then instead a new term MUST be created with a new IRI and the new definition. Minor changes to the definition for clarity, grammar, and/or proper punctuation that do not change the referents are permitted."

It then specifies the *mechanics* of obsoletion, which is the reusable engineering content:

- MUST mark with `owl:deprecated true` (OWL) / `is_obsolete: true` (OBO);
- MUST prepend the exact string `"obsolete "` to the label, so drift is visible in the human-readable field, not only in metadata;
- MUST remove all logical axioms from the obsoleted term, and MUST remove or replace all uses of it elsewhere in the ontology (worked example: if `A part-of B` and B is deprecated in favour of C, the axiom becomes `A part-of C`) — i.e. **no dangling references to deprecated entities**;
- MUST NOT delete the textual definition ("It is not necessary (and not advisable) to delete the textual definition");
- SHOULD record an exact successor via `term replaced by` (IAO:0100001) / `replaced_by:`, and inexact successors via `oboInOwl:consider` / `consider:` — a two-tier successor vocabulary distinguishing *substitutable* from *merely related*;
- MAY record a machine-readable **obsolescence reason** drawn from a controlled list (IAO:0000231 valued by individuals of IAO:0000225, e.g. "terms merged");
- SHOULD pre-announce obsoletions (cross-references Principle 13, notification).

Compliance is machine-checked: the OBO Dashboard raises ERRORs for an obsolete term lacking the label prefix, for an obsolete term lacking the deprecation flag, and for an obsolete term that still carries or is referenced by logical axioms.

## Mapping onto ATT&CK

Point-by-point, this is the normalization protocol the manuscript needs, and it already exists:

- ATT&CK's `revoked` + `revoked-by` relationship is the analogue of `replaced_by` (exact successor). ATT&CK has no analogue of `consider` (inexact successor), which is exactly the case that breaks sub-technique restructuring: when T1086 is superseded by a *set* of successors, or when a technique is split, there is no one-to-one replacement and the exact-successor slot is the wrong instrument.
- ATT&CK's `x_mitre_deprecated` is the analogue of `owl:deprecated`, but ATT&CK records **no obsolescence reason** from a controlled vocabulary. The manuscript can propose exactly such a reason vocabulary (superseded-by-split, merged, out-of-scope, never-observed, renamed-only) and back the proposal with OBO precedent rather than inventing it.
- The label-prefix requirement is the pointed one: OBO forces drift into the *visible* field. ATT&CK's deprecation is metadata-only, so downstream tooling that joins on technique name or ID silently keeps working with a dead concept.
- Principle 19's referent-stability rule is the formal statement of what the manuscript calls "silent rewriting of technique descriptions": under OBO rules, a description edit that changes which real-world behaviours a technique denotes is *not permitted* at the same ID. ATT&CK permits it and records it only as a bumped `modified` timestamp.
- The "remove or replace all usages" requirement maps directly onto the dangling-reference problem in ATT&CK bundles (group→technique and software→technique relationships pointing at revoked/deprecated techniques), which is a measurable integrity metric.

The manuscript should therefore present its protocol as *porting OBO Principle 19 to ATT&CK*, and its drift audit as a dashboard-style conformance check, not as novel machinery.

## Fidelity

Ground truth. The quoted strings above were read from the cloned repository file `/home/user/ext/obofoundry/principles/fp-019-term-stability.md` at HEAD of the default branch (shallow clone, 2026-09-12). Verbatim quotations are exact as of that commit; the principle is a living document, so pin the commit when citing.
