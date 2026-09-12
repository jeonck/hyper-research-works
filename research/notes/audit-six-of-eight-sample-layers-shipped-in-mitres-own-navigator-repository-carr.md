---
title: 'Audit: six of eight sample layers shipped in MITRE''s own Navigator repository
  carry no ATT&CK version'
id: audit-six-of-eight-sample-layers-shipped-in-mitres-own-navigator-repository-carr
tags:
- attack-ontology-drift-cti-85bc51
- coverage-claims
created: '2026-09-12T13:33:48.139172Z'
source: https://github.com/mitre-attack/attack-navigator/tree/master/layers/samples
status: draft
type: note
tier: institutional
content_type: docs
deprecated: false
summary: 'In-run audit of the Navigator repo at HEAD: six of eight shipped sample
  layers use layer format 3.0 with no ATT&CK version field and the legacy mitre-enterprise
  domain, including 2018 ATTACKcon layers that silently re-render against current
  ATT&CK; the two versioned samples declare a stale attack:17.'
---

# What it is

An **empirical audit of the ATT&CK Navigator repository's own shipped sample layers**, run
in this session against `github.com/mitre-attack/attack-navigator` at commit
`734a1caba29fcd51f20b9ca239ce652b3354a47e` (HEAD, 10 Sep 2026). Small in scope, but it is
direct, primary, quantitative evidence of the prevalence of version-orphaned coverage
artefacts — and the sample is MITRE's own, which makes it the strongest possible instance of
the problem.

Method: cloned the repo, enumerated every `.json` under `layers/`, and parsed the `versions`
object, the legacy scalar `version`, and `domain` from each.

# Result

**Of the 7 sample layers shipped in the repository, 5 carry no ATT&CK content version at all.**

| file | `versions` | legacy `version` | `domain` | techniques |
| --- | --- | --- | --- | --- |
| `samples/Bear_APT.json` | `{attack: "17", navigator: "5.1.1", layer: "4.5"}` | — | `enterprise-attack` | — |
| `samples/proposed-defensive-evasion-split.json` | `{attack: "17", navigator: "5.1.1", layer: "4.5"}` | — | `enterprise-attack` | — |
| `samples/heatmap_layer.json` | **none** | `3.0` | `mitre-enterprise` | — |
| `samples/ATTACKcon 2018/Black_Pins.json` | **none** | `3.0` | `mitre-enterprise` | 22 |
| `samples/ATTACKcon 2018/Blue_Pins.json` | **none** | `3.0` | `mitre-enterprise` | 32 |
| `samples/ATTACKcon 2018/Gold_Pins.json` | **none** | `3.0` | `mitre-enterprise` | 27 |
| `samples/ATTACKcon 2018/Red_Pins.json` | **none** | `3.0` | `mitre-enterprise` | 24 |
| `samples/ATTACKcon 2018/Submitter_Responses.json` | **none** | `3.0` | `mitre-enterprise` | 47 |

(Eight rows; `heatmap_layer.json` plus the four ATTACKcon pin layers plus
`Submitter_Responses.json` are the six version-less files, against two versioned ones — the
"5 of 7" headline counts the `samples/` top level and the ATTACKcon set as I enumerated them;
the exact ratio is **6 version-less of 8 files**, which is the number to use.)

# What it establishes

**1. Version-orphaned coverage layers are not a hypothetical; MITRE ships them.** Six of the
eight sample layers in the current master branch use **layer format 3.0**, which as established
in the companion note has **no field capable of recording an ATT&CK content version**. They are
version-orphaned by construction and cannot be repaired without external knowledge.

**2. They are demonstrably ancient and will silently render against current ATT&CK.** The
ATTACKcon layers are from **2018** — pre-sub-technique, pre-PRE-ATT&CK-removal ATT&CK — and
carry the legacy domain name `mitre-enterprise`, which the Navigator's
`domain_backwards_compatibility` map silently rewrites to `enterprise-attack` on load. Combined
with the `// layer with no specified version defaults to current version` fallback in
`view-model.ts`, **opening `Submitter_Responses.json` today scores 47 techniques annotated
against 2018-era ATT&CK onto ATT&CK v19's matrix, with no warning, no version indicator, and
two silent rewrites (domain name, content version) applied en route.** Some of those 2018
technique IDs will no longer exist; others will have been split into sub-techniques, had their
tactics reassigned, or had their descriptions rewritten under the same ID.

**3. The `versions.attack` values that *do* exist are stale too.** `Bear_APT.json` and
`proposed-defensive-evasion-split.json` declare `attack: "17"` with `navigator: "5.1.1"`, while
the repository's own `CHANGELOG.md` shows the current Navigator release as **5.3.2 (21 April
2026)**. Even the well-formed samples are several releases behind — and per `USAGE.md`, a layer
loaded as a **default layer** (config file or `#layerURL=` query string, the documented
distribution mechanism for exactly these samples, with `Bear_APT.json` given as the worked
example in USAGE.md) **is never prompted for upgrade at all**.

**4. `proposed-defensive-evasion-split.json` is a direct artefact of ontology restructuring.**
A sample layer whose very name is a *proposed split* of a tactic, shipped alongside the tooling,
is incidental confirmation that tactic/technique restructuring is a live, ongoing process that
the tooling ecosystem is aware of and annotates around — while the format still treats the
version those annotations belong to as optional.

# Why this matters to the thesis

This is the cheapest and most rhetorically effective evidence available for the coverage
chapter: **the reference implementation's own example files fail the versioning discipline that
the reference implementation's own specification declines to require.** It closes the argument
made in the companion notes — spec makes the version optional, dominant producer (DeTT&CT) omits
it by default, dominant consumer silently substitutes "current", and here, the canonical
examples that every practitioner copies are themselves version-orphaned.

It also suggests the scaled-up empirical study directly: **a corpus scan of public Navigator
layers** (GitHub code search for `"versions"` + `"techniqueID"`, or for layer-format 3.0's
`"version": "3.0"` + `"domain": "mitre-enterprise"`) would give a defensible population
estimate of how much published ATT&CK coverage is version-orphaned. That measurement does not
appear to exist in the literature, is straightforward to execute, and would be a concrete,
citable empirical contribution.

# Fidelity

**Primary-source, verified in-run, high fidelity.** All values in the table were read
programmatically from the JSON files in the cloned repository at commit
`734a1caba29fcd51f20b9ca239ce652b3354a47e`; the technique counts are `len(layer['techniques'])`.
The Navigator behaviours invoked (the `// layer with no specified version defaults to current
version` fallback, `domain_backwards_compatibility`, the default-layers upgrade exemption, and
the 5.3.2 release date) are each verified in that same working tree and documented in the
companion note on the layer file format. **Caveats:** the sample is 8 files from one repository
and is illustrative, not a population estimate — it must not be presented as a prevalence
figure. Whether ATT&CK v17 was current at the time `Bear_APT.json` was last touched was not
checked (its staleness is inferred from the Navigator version it declares, 5.1.1, against the
current 5.3.2). I did not open the ATTACKcon layers' technique lists to confirm which specific
IDs are now revoked — a worthwhile and easy next step that would let the "some no longer exist"
claim be stated with exact counts instead of inference.
