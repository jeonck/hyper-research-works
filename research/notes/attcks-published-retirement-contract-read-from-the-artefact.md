---
title: ATT&CK's published retirement contract, read from the artefact
id: attcks-published-retirement-contract-read-from-the-artefact
tags:
- attack-ontology-drift-cti-85bc51
- primary-artefact
created: '2026-09-12T13:47:48.421560Z'
source: https://github.com/mitre-attack/attack-stix-data/blob/master/USAGE.md
status: draft
type: note
tier: ground_truth
content_type: docs
deprecated: false
summary: Primary-artefact replacement for a quarantined note
---

# ATT&CK's published retirement contract, read from the artefact

Fidelity: PRIMARY ARTEFACT, read in full from the local clone of
`mitre-attack/attack-stix-data` (`USAGE.md`). This note replaces a quarantined
note of the same nominal subject whose body belonged to a different source.

What the file establishes:

- Retirement is two-class and non-destructive. Objects are marked `revoked` when
  another object takes their place, or `x_mitre_deprecated` when they are
  withdrawn without a replacement, and both remain in every published bundle.
  The stated reason is that workflows depending on them should not break, with
  the recommendation that consumers avoid using them.
- The canonical filter MITRE publishes for consumers drops any object where
  either flag is set, defaulting each flag to false when the property is absent.
  That single helper is the whole consumer-side retirement contract: an object is
  either current or it is not, with no gradation and no signal about how much a
  surviving object may have changed.
- Recovering a successor is a separate, explicit step: the file documents
  retrieving the revoking object through the `revoked-by` relationship, so
  resolution is available but opt-in.

What the file does not contain, checked by reading it: any mechanism for
signalling that a surviving object's meaning changed, any relation for an
inexact or partial successor, and any retirement mechanism for tactics.
