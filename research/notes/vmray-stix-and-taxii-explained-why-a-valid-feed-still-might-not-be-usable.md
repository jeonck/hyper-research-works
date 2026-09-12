---
title: 'VMRay — STIX and TAXII Explained: Why a Valid Feed Still Might Not Be Usable'
id: vmray-stix-and-taxii-explained-why-a-valid-feed-still-might-not-be-usable
tags:
- attack-ontology-drift-cti-85bc51
- cti-quality
created: '2026-09-12T13:22:02.699928Z'
source: https://www.vmray.com/stix-taxii-explianed/
status: draft
type: note
tier: practitioner
content_type: article
deprecated: false
summary: Practitioner account that schema validity does not imply usability; the only
  versioning concern raised is STIX object versioning/update handling, not versioning
  of the label vocabulary.
---

## What it is
VMRay, "STIX and TAXII Explained: Why a Valid Feed Still Might Not Be Usable" (vendor/practitioner article), https://www.vmray.com/stix-taxii-explianed/. Practitioner-tier evidence on what actually degrades shared CTI in production pipelines.

## What it says bearing on the query
Practitioner claims, paraphrased (this is a vendor blog, treat as practitioner tier, not evidence of measurement):
- **Neither STIX nor TAXII guarantees quality** — schema validity is orthogonal to usefulness.
- **Content loss in transport**: a client that cannot paginate reliably, preserve state, **process object versions**, or handle updates correctly turns a good STIX model into incomplete data; platforms may import STIX but **hide relationships, drop sightings, ignore validity windows, or fail to handle updates cleanly**.
- **Contextual degradation**: a well-formatted STIX object carrying stale, low-fidelity or misattributed intel will **"produce confident wrong answers at every layer it touches"** (phrasing as reported in search results, not verified verbatim against the page).
- The most consistent implementation failure is treating STIX/TAXII as a **technical checkbox rather than an operational commitment**: incoming objects are not evaluated for quality and TAXII integrations are not monitored for failure.
- Recommended discipline: evaluate whether **context survives the trip** — relationships, confidence, validity, report grouping, sightings, **lifecycle metadata, and update handling** — and define explicit object-quality standards for both incoming and outgoing intelligence.

## Bearing on ATT&CK ontology drift
- This is the one source in the batch where something adjacent to versioning appears as a quality concern — but it is **STIX object versioning** (the `modified` timestamp / object-version semantics of an individual CTI object as it is updated by its producer), **not versioning of the controlled vocabulary the object's labels are drawn from**. The distinction matters and is worth making explicitly in the paper: practitioners already have a mental model for "did I handle the update to this object?", and no mental model for "did I handle the update to the meaning of T1547?".
- "Lifecycle metadata" and "update handling" are therefore the natural hooks into practitioner vocabulary for introducing ontology-version pinning: it can be framed as the missing lifecycle metadata *of the reference taxonomy* rather than as a new academic construct.

## Fidelity
Could not read the page (vmray.com blocked by the egress proxy). All bullets are at summary fidelity from search-result extraction of the page; the phrase in quotation marks above is reproduced as it appeared in the search result and is **not verified as verbatim page text** — do not cite it as a quotation without opening the page. Vendor source: rhetorical, not measured.
