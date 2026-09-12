---
title: 'Rahman & Williams (arXiv:2211.06500): mitigation coverage has a ceiling set
  by the control catalogue, and the ceiling moves with each ATT&CK release'
id: rahman-williams-arxiv221106500-mitigation-coverage-has-a-ceiling-set-by-the-cont
tags:
- attack-ontology-drift-cti-85bc51
- coverage-claims
created: '2026-09-12T13:29:46.565184Z'
source: https://arxiv.org/abs/2211.06500
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Study of 298 NIST SP800-53 controls against 188 ATT&CK techniques across
  669 groups/malware; reported that only a minority of controls mitigate anything
  and some techniques are unmitigable, implying mitigation-coverage percentages have
  an unstated, version-dependent ceiling.
---

# What it is

Md Rayhanur Rahman and Laurie Williams, **"An investigation of security controls and MITRE
ATT&CK techniques"**, arXiv:2211.06500 (submitted 11 November 2022). North Carolina State
University. A quantitative study of **how much of ATT&CK the control catalogue can actually
mitigate** — i.e. the mitigation-side counterpart to detection coverage, and the cleanest
academic statement that the full technique set is the wrong denominator.

**Fetch blocked**; **summary fidelity from indexed abstract/summary text**. Nothing quoted.

# What it establishes about coverage measurement

**The study's reported scope:** the extent of mitigation of **298 NIST SP 800-53 controls**
over **188 adversarial techniques** used by **669 cybercrime groups and malware** catalogued in
MITRE ATT&CK.

**The two figures that make this a denominator paper** (both from indexed summary text, and
both requiring verification against the PDF — see Fidelity):
- **Only 107 of the 298 controls are capable of mitigating adversarial techniques**, i.e.
  roughly 64% of the control catalogue contributes nothing to ATT&CK-relative mitigation
  coverage.
- **50 attack techniques cannot be mitigated by existing controls at all.**

If the second figure holds, it is directly load-bearing: **a mitigation-coverage percentage
computed over all techniques has a hard ceiling below 100%**, and the ceiling is a property of
the control catalogue, not of the defender. Reporting "we mitigate X% of ATT&CK" against the
full technique set therefore understates by a fixed, unstated amount — and, critically for the
thesis, **that amount changes with every ATT&CK release**, since new techniques arrive
un-mitigated by an unchanged control catalogue and subsequently acquire mappings on MITRE's
own schedule. **A defender's mitigation-coverage percentage can fall between releases with no
change in their controls**, purely because ATT&CK added techniques faster than the mapping
project mapped them. That is ontology bookkeeping producing an apparent security regression,
and it is a mechanism the thesis can state crisply and, with the CTID control-mapping data,
measure.

**The stated motivation is prioritisation under infeasibility.** Reported: standards specify
hundreds of controls, implementing all simultaneously can be infeasible, so controls must be
assessed by their mitigation ability over techniques actually used in attacks. The reported
recommendations — organisations with no controls should prioritise the highest-mitigation
controls; organisations with controls should **continuously reassess** effectiveness against
the more frequent techniques — amount to an argument that coverage must be **frequency-weighted
and re-evaluated over time**, not counted once at uniform weight. That is the same conclusion
this batch reaches from the detection side (Forrester on benign techniques, CTID on
implementation depth): **uniform-weight technique counting is indefensible from every
direction.**

# Related institutional infrastructure

The same searches surface the upstream data source: **CTID's "NIST 800-53 Controls to ATT&CK
Mappings"** project (`ctid.mitre.org/projects/nist-800-53-control-mappings/`), introduced in
Jon Baker's "Security Control Mappings: A Bridge to Threat-Informed Defense" (MITRE Engenuity,
Medium). This matters for the thesis beyond this paper: **the control-to-technique mapping is
itself a versioned artefact that drifts**, both when NIST revises 800-53 and when ATT&CK
revises techniques, so mitigation coverage has *two* moving ontologies rather than one. A
normalization protocol for mitigation claims must therefore pin both the ATT&CK release and
the mapping-set release. Adjacent items in the result set: "Threat modeling in smart
firefighting systems: Aligning MITRE ATT&CK matrix and NIST security controls" (ScienceDirect),
"Threat-based Security Controls to Protect Industrial Control Systems" (arXiv:2501.13268), and
"Risk-Based MITRE TTP Scoring for Proactive Cyber Threat Prioritization and Response"
(ICSCA 2025, ACM). None read.

# Citable specifics

- 298 NIST SP 800-53 controls; 188 adversarial techniques; 669 groups/malware.
- 107/298 controls capable of mitigating techniques (**verify**).
- 50 techniques not mitigable by existing controls (**verify**).
- Authors Rahman & Williams; arXiv:2211.06500; submitted 11 Nov 2022; also on ResearchGate.

# Fidelity

**Summary fidelity only.** arxiv.org could not be fetched (egress proxy 403). The scope figures
(298/188/669) come from indexed abstract text and are moderately reliable. **The two headline
numbers — 107 of 298 controls, and 50 unmitigable techniques — surfaced in a search summary
that blended results across several papers in the result set, and I could not confirm from the
indexed text that both belong to this paper rather than to a neighbouring one.** They must be
verified against `arxiv.org/pdf/2211.06500` before being cited, and should not be attributed to
Rahman & Williams until they are. Nothing above is quoted verbatim. The paper is a preprint;
check for a peer-reviewed version before citing. The argument that the un-mitigable ceiling
drifts with each ATT&CK release is **my inference**, not a claim made in the paper — the paper
as indexed is synchronic.
