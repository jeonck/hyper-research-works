---
title: MITRE's own change taxonomy, read from diffStix source
id: mitres-own-change-taxonomy-read-from-diffstix-source
tags:
- attack-ontology-drift-cti-85bc51
- primary-artefact
created: '2026-09-12T13:47:48.674863Z'
source: https://github.com/mitre-attack/mitreattack-python
status: draft
type: note
tier: ground_truth
content_type: docs
deprecated: false
summary: Primary-artefact replacement for a quarantined note
---

# MITRE's own change taxonomy, read from diffStix source

Fidelity: PRIMARY ARTEFACT, read from `mitreattack-python` at the cloned commit
(`mitreattack/diffStix/changelog_helper.py` and the module's README). This note
replaces a quarantined note of the same nominal subject.

MITRE ships a tool that computes, for any two releases, nine classes of change:
additions; major version changes (1.0 to 2.0); minor version changes (1.0 to
1.1); other version changes (any other increment); patches (the object changed
while its version stayed the same — the source names typos, URLs and metadata);
revocations; deprecations; deletions; and unchanged.

Two properties of that taxonomy matter for this study.

First, MITRE has already named the phenomenon this paper measures. The `patches`
class is, by its own definition, a change to an object that leaves its version
untouched — silent rewriting, given a name and a code path inside the reference
tooling.

Second, the tooling documents its own version metadata as unreliable: the
README's row for `other_version_changes` describes those increments as
unintended, while noting they occur in previous releases. A change-detection
scheme whose own maintainers annotate one of its classes as unintended is not a
signal a downstream consumer can build on, which is what the measurement in this
paper quantifies from the other direction.

What diffStix does not do: it enumerates what changed between two releases. It
does not express what that change costs any analytic that consumed the earlier
release.
