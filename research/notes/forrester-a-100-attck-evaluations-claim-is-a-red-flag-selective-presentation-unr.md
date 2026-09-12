---
title: 'Forrester: a 100% ATT&CK Evaluations claim is a red flag — selective presentation,
  unrealistic configuration, competition framing'
id: forrester-a-100-attck-evaluations-claim-is-a-red-flag-selective-presentation-unr
tags:
- attack-ontology-drift-cti-85bc51
- coverage-claims
created: '2026-09-12T13:25:20.573936Z'
source: https://www.forrester.com/blogs/dont-trust-vendor-claims-about-getting-100-on-the-mitre-attck-evaluations
status: draft
type: note
tier: practitioner
content_type: blog
deprecated: false
summary: Analyst-firm critique naming three mechanisms behind 100% coverage claims,
  and arguing per-technique counting is a category error because techniques like T1059.004
  are often benign.
---

# What it is

Forrester Research's running critique of ATT&CK Evaluations coverage marketing — a series of
analyst blog posts, principally **"Don't Trust Vendor Claims About Getting 100% On The MITRE
ATT&CK Evaluations"** and the companion **"MITRE ATT&CK Evals: Getting 100% Coverage Is Not
As Great As Your Vendor Says It Is"**, alongside "Quantifying Vendor Efficacy Using The MITRE
ATT&CK Evaluation", "Winning MITRE ATT&CK, Losing Sight Of Customers", and "MITRE ATT&CK
Evaluations Return: More Coverage, More Nuance" (all at forrester.com/blogs, with a dedicated
`category/mitre-attck` index). This is the most-cited *buyer-side* institutional criticism of
ATT&CK coverage claims, and it is the counterweight to the vendor press releases it names.

**Fetch was blocked** (egress proxy); content below is at **summary fidelity from indexed
search text**. Nothing is quoted verbatim.

# What it establishes about coverage claims

**A "100%" claim is a red flag, and Forrester enumerates the mechanisms that produce it.**
The reported taxonomy of what a vendor claiming 100% is likely doing:

1. **Selective presentation** — showing only the portions of the results that flatter them.
2. **Unrealistic configuration** — turning on product settings that would not be run in a
   real-world environment, in order to appear more effective.
3. **Treating the evaluation as a competition** rather than as a learning opportunity and a
   chance to improve the product.

All three are *denominator and scope manipulations*, and none of them is detectable from the
headline number alone. This is the practitioner-side confirmation of the thesis's core claim:
the coverage percentage is under-determined by the underlying data, so the same data supports
many numbers, and the publisher picks.

**Coverage of a technique does not imply detection of an attack, because some techniques are
benign.** Forrester's reported illustration is `T1059.004` (Unix Shell): launching a Unix
shell may be completely normal user activity, or it may be an attacker. A product that
"covers" T1059.004 has said nothing about whether it can separate those. **Techniques are
not equally informative, so a uniform-weight count over techniques is a category error** —
the coverage metric implicitly asserts that every technique is worth one unit, which is false
even within a single ATT&CK version. Cross-version, this compounds: sub-technique splits
multiply the unit count for exactly the techniques that got *more* descriptive detail, so
well-elaborated areas of the matrix acquire more "weight" in any coverage ratio purely
through bookkeeping.

**Reported framing worth carrying into the thesis:** detecting an attack inspired by a known
threat actor should be the *floor* for what security products can do, not the ceiling.
Applied to coverage claims, an emulation-derived or ATT&CK-derived score measures the floor
and is routinely reported as if it measured the ceiling.

# Citable specifics

- The three-mechanism taxonomy of a 100% claim: selective presentation; unrealistic
  configuration; competition framing. (Note that the second maps onto the Evaluations'
  own **Config Change** modifier — MITRE records the fact, vendors drop it from the
  headline. That link between MITRE's recorded modifier and Forrester's criticism is *my
  inference*, not a Forrester statement.)
- `T1059.004` as the worked example of a technique whose "coverage" is semantically empty
  without false-positive context.
- Forrester maintains a standing `mitre-attck` blog category, i.e. this is a sustained
  analyst position across evaluation rounds, not a one-off reaction.
- Concrete instance of the marketing genre these posts respond to, findable in the same
  result set: a March 2022 vendor press release headlined on achieving **100% prevention**
  in the fourth round of Enterprise Evaluations (CrowdStrike, via BusinessWire). The pairing
  of the press release and the analyst rebuttal is a citable exhibit of the gap between what
  MITRE published and what was claimed from it.

# Why this matters to the thesis

Forrester supplies the *reception-side* evidence: even setting ontology drift aside
completely, published coverage and evaluation numbers are known by professional analysts to
be non-comparable and routinely manipulated, and the manipulation levers are exactly the
under-specified parameters a normalization protocol must force into the open — which subset
of results, under which configuration, against which denominator, with which per-technique
weighting. The thesis's reporting discipline therefore has a ready-made audience argument:
the buyer-side literature already demands these disclosures on *non-versioning* grounds; the
versioning disclosures (ATT&CK release, migration provenance, granularity) are the missing
fourth and fifth columns of a form the market has already half-agreed it needs.

It also usefully bounds the contribution. Forrester's critique is qualitative and
journalistic; it names the failure modes but does not measure them, does not touch version
drift at all, and offers no protocol. An SCI-level contribution must do what Forrester does
not: quantify the effect, decompose it into identifiable causes, and specify a protocol that
is checkable rather than exhortative.

# Fidelity

**Summary fidelity only.** forrester.com could not be fetched (egress proxy blocks direct
page retrieval; confirmed in-run against another host). The three-mechanism taxonomy, the
T1059.004 example, and the "floor not ceiling" framing are **paraphrased from indexed
search-result summaries of the Forrester posts** and were **not read in the posts' full
text**; Forrester blogs are also partly gated, so full verification may require a
subscription or an archived copy. No sentence above is a quotation. Post titles and the
existence of the `category/mitre-attck` index are from the search result listing and are
reliable; the attribution of specific arguments to a *specific* one of the several posts is
**not** verified — treat the arguments as "the Forrester ATT&CK-evaluations series" rather
than citing a single post for a single claim until the text is confirmed. The CrowdStrike
press release is a real, dated (31 March 2022) BusinessWire item in the result set but was
likewise not read in full.
