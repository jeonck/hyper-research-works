---
title: DeTT&CT omits the ATT&CK version from generated Navigator layers by default,
  and stamps its own build constant when it does not
id: dettct-omits-the-attck-version-from-generated-navigator-layers-by-default-and-st
tags:
- attack-ontology-drift-cti-85bc51
- coverage-claims
created: '2026-09-12T13:32:02.886829Z'
source: https://github.com/rabobank-cdc/DeTTECT
status: draft
type: note
tier: practitioner
content_type: docs
deprecated: false
summary: 'Source-verified: DeTT&CT writes versions.attack only if the user passes
  includeAttackVersion=True (default off), the value is a hardcoded ATTACK_VERSION=''19.1''
  build constant not data provenance, Navigator truncates it to ''19'' on load, and
  the technique-administration YAML that holds the real scores has no ATT&CK version
  field at all.'
---

# What it is

**DeTT&CT** (Detect Tactics, Techniques & Combat Threats), from the **Rabobank Blue Team /
Rabobank-CDC**, is the most widely used open-source tool for administering ATT&CK detection,
visibility and data-source coverage and emitting ATT&CK Navigator layers from it. Where the
Navigator is the *format*, DeTT&CT is what actually *produces* a large share of the coverage
layers practitioners publish. Also surfaced: NVISO Labs' walkthrough "DeTT&CT: Mapping
detection to MITRE ATT&CK" (blog.nviso.eu, 9 March 2022).

Read here as **primary source**: repository cloned anonymously
(`github.com/rabobank-cdc/DeTTECT`) at commit
`66ceddfe60a591de4bb45078eda0c5ff4b4a1e2e` (6 Aug 2026), with `constants.py`,
`navigator_layer.py`, `dettect.py`, `upgrade.py` and the sample administration YAML read in
the working tree.

# The headline finding: DeTT&CT omits the ATT&CK version from its layers by default

This is the downstream half of the Navigator layer-format question, and it is worse in
practice than the spec alone suggests.

`navigator_layer.py` builds every layer template as:

    layer['versions'] = {'navigator': ATTACK_NAVIGATOR_VERSION, 'layer': ATTACK_LAYER_VERSION}
    if 'includeAttackVersion' in layer_settings.keys() and layer_settings['includeAttackVersion'] == 'True':
        layer['versions']['attack'] = ATTACK_VERSION

**The two mandatory fields are always written; the ATT&CK content version is written only if
the user explicitly opted in.** And the opt-in is off by default: `dettect.py::_parse_layer_settings`
begins `layer_settings = {}` and populates it only from `--layer-settings key=value` arguments
(`action='append'`, no default), so a user who does not pass
`--layer-settings includeAttackVersion=True` gets a layer with **no `attack` key at all**.
Documented CLI example in the help text is `--layer-settings showAggregateScores=True`, i.e.
the version setting is not the advertised one.

Chain the two primary sources together and the result is exact:

> A default DeTT&CT-generated coverage layer contains no ATT&CK version. Opened in the
> Navigator, `view-model.ts` hits its `// layer with no specified version defaults to current
> version` branch and scores the layer against whatever ATT&CK release that Navigator instance
> currently serves. **The coverage artefact is silently re-based, every time it is opened,
> forever.**

This is not a hypothetical composed of two independent possibilities; it is the default
behaviour of the dominant producer feeding the default behaviour of the dominant consumer.

# Second finding: when the version IS written, it is the tool's build constant, not the data's provenance

`constants.py`:

    ATTACK_VERSION = '19.1'
    ATTACK_LAYER_VERSION = '4.5'
    ATTACK_NAVIGATOR_VERSION = '5.3.2'

`ATTACK_VERSION` is a **hardcoded module constant**, bumped by maintainers when they update
DeTT&CT. So `versions.attack` in a DeTT&CT layer records **which DeTT&CT build ran**, not which
ATT&CK release the analyst's scores were reasoned against. An administration file whose
`score_logbook` entries were written in 2021 will, when regenerated in 2026, be stamped `19.1`
with full confidence. **The version stamp attests to the rendering, not to the judgement** —
which is precisely the provenance a normalization protocol needs and precisely what it does not
get.

# Third finding: a minor-version round-trip loss, demonstrated end to end

DeTT&CT writes `'19.1'`. The Navigator parses `versions.attack` with
`obj.versions.attack.match(/\d+/g)[0]` — verified in `view-model.ts` in the cloned Navigator
repo, and confirmed by running the same regex: `'19.1' → '19'`, `'12.1' → '12'`,
`'v14.1' → '14'`. **The point release DeTT&CT carefully records is discarded on load.** Since
point releases are exactly where silent description and scope rewrites land, the producer/
consumer pair cannot represent the granularity at which the ontology actually moves — even in
the best case where everything is configured correctly.

# Fourth finding: the administration files — the real source of truth — carry no ATT&CK version at all

`sample-data/techniques-administration-endpoints.yaml` opens:

    version: 1.2
    file_type: technique-administration
    name: example
    domain: enterprise-attack
    platform:
    - Windows
    - Linux
    techniques:
    - technique_id: T1001
      ...

`version: 1.2` is DeTT&CT's **own file-schema version** (`constants.py`:
`FILE_TYPE_TECHNIQUE_ADMINISTRATION_VERSION = 1.2`, alongside
`FILE_TYPE_DATA_SOURCE_ADMINISTRATION_VERSION = 1.1` and
`FILE_TYPE_GROUP_ADMINISTRATION_VERSION = 1.0`). There is **no ATT&CK content version field** —
only `domain`. The long-lived artefact in which an organisation accumulates years of detection
and visibility scores against technique IDs therefore has no record of which ontology those IDs
were scored under. This is the same failure as layer formats 1.x–3.0, still shipping in 2026,
in the file that actually matters.

`upgrade.py` reinforces the point: DeTT&CT has real, careful machinery for migrating its **own**
YAML schema across versions (`_upgrade_data_source_yaml_10_to_11`, with a pre-upgrade health
check, backup via `file_output.backup_file`, and user-facing upgrade text from
`FILE_TYPE_DATA_SOURCE_UPGRADE_TEXT`). **The tool version-manages its own schema rigorously and
the ATT&CK ontology not at all.** That asymmetry — schema versioning solved, content-ontology
versioning absent — is the same asymmetry the Navigator shows (hard blocking dialog for a layer
*format* mismatch, optional wizard for an ATT&CK *content* mismatch), and it is a strong,
repeatable structural claim for the thesis.

# Mitigating features worth crediting

- **`score_logbook` with per-score `date`.** Every detection and visibility score carries a
  dated logbook entry (sample shows `date: 2021-09-22`, `score: -1` for unassessed). This is
  genuine, if indirect, temporal provenance: a date can be resolved to the ATT&CK release
  current at the time. **A normalization protocol could exploit this** — it is the one field in
  the ecosystem that would let a retrospective study re-base historical DeTT&CT scores onto the
  correct contemporaneous ontology. Worth flagging as an opportunity, not just a critique.
- **`--local-stix-path`** on the `data-sources`, `visibility` and `detection` sub-commands, with
  help text describing it as a path to a local STIX repository "to use DeTT&CT offline or to use
  a specific version of STIX objects", plus `attack_taxii_client.py`. Pinning to a chosen ATT&CK
  release **is** supported — it is just not the default, and it is not recorded in the output.
- DeTT&CT targets layer format **4.5** and Navigator **5.3.2**, i.e. it tracks the current
  Navigator closely.

# Why this matters to the thesis

This note converts the Navigator spec finding from a latent design weakness into a
**demonstrated ecosystem-wide defect**, with both halves verified in source:

1. The format makes the ATT&CK version optional (Navigator spec, verified).
2. The dominant producer omits it by default (DeTT&CT, verified).
3. The dominant consumer silently substitutes "current" when it is absent (Navigator source,
   verified).
4. When present it is the tool's build constant, not the data's provenance (verified).
5. Its precision is truncated to the major release on load (verified by running the parser's
   own regex).
6. The underlying administration file records no ATT&CK version whatsoever (verified).

That is a complete, source-verified causal chain from specification choice to unreproducible
published coverage claim, and it can be stated in the thesis without relying on a single
secondary source. The corresponding minimal protocol requirement follows directly: **make the
ATT&CK release mandatory and full-precision in the coverage artefact, record it at the point of
judgement (the administration file) rather than at the point of rendering, and carry a migration
log when scores are re-based.**

# Fidelity

**Primary-source, high fidelity.** Repository cloned at commit
`66ceddfe60a591de4bb45078eda0c5ff4b4a1e2e`; the code fragments from `navigator_layer.py`,
`constants.py`, `dettect.py::_parse_layer_settings` and the sample YAML header are transcribed
from the working tree. The default-off behaviour of `includeAttackVersion` was verified by
grepping the whole repository — the key appears in exactly two places (`navigator_layer.py:21`
and the `LAYER_SETTINGS` enumeration in `constants.py:215`), with no default-true assignment
anywhere and no config file setting it. The regex truncation was confirmed by executing the
Navigator's own pattern on `'19.1'` and related inputs. The Navigator-side behaviour cited here
is verified in the separately cloned `mitre-attack/attack-navigator` at commit
`734a1caba29fcd51f20b9ca239ce652b3354a47e` (see the companion note on the layer format).
**Not verified**: how many published layers in the wild actually lack `versions.attack` (a
corpus scan would settle it, and would be a strong empirical contribution); DeTT&CT's own
release notes and documentation site; the NVISO Labs walkthrough, which was not fetched (egress
blocked) and is listed here only as a pointer. DeTT&CT's status as "most widely used" is my
characterisation from its prominence in practitioner writing, not a measured claim.
