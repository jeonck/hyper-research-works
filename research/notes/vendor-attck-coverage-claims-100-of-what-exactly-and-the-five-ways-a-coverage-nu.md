---
title: 'Vendor ATT&CK coverage claims: ''100% of what, exactly?'' and the five ways
  a coverage number is padded'
id: vendor-attck-coverage-claims-100-of-what-exactly-and-the-five-ways-a-coverage-nu
tags:
- attack-ontology-drift-cti-85bc51
- coverage-claims
created: '2026-09-12T13:29:46.319200Z'
source: https://www.attackiq.com/2026/03/10/what-does-mitre-attack-coverage-really-mean/
status: draft
type: note
tier: practitioner
content_type: blog
deprecated: false
summary: Vendor and counter-vendor commentary enumerating scope manipulations behind
  coverage claims (partner integrations, sibling products, endpoint-centric scope,
  zero-filled non-participants); notably the market contests scope on four axes and
  has not noticed the version axis.
---

# What it is

The vendor-side and buyer-side commentary on what an "ATT&CK coverage" percentage actually
denominates. Principal items: **AttackIQ, "What Does MITRE ATT&CK Coverage Really Mean?"**
(March 2026; syndicated to Security Boulevard); **ExtraHop, "RevealX MITRE ATT&CK Coverage
2024"**; **Mitiga, "Measurements That Matter: What 80% MITRE Cloud ATT&CK Coverage Looks
Like"**; **Databahn, "MITRE under ATT&CK: Rethinking cybersecurity's gold standard"**; and
the aggregated criticism surfaced alongside them. Valuable precisely because several of these
are vendors criticising *other* vendors' coverage claims, which makes the enumerated tricks
credible as a description of common practice even where each author is self-interested.

**Fetch blocked**; **summary fidelity from indexed search text** throughout. Nothing quoted.

# What it establishes about coverage claims

**"100% coverage" is the canonical tell, and the diagnostic question is about the
denominator.** Reported framing: when a vendor claims 100% MITRE ATT&CK coverage the immediate
question is **"100% of what, exactly?"**, and coverage claims without context are one of the
most persistent sources of confusion in security tooling. No tool can reliably detect all
techniques. **This is the denominator problem in the market's own words** — and notably the
remedy proposed is disclosure of scope, which is the same move the thesis's reporting
discipline makes for version.

**Enumerated mechanisms by which coverage numbers are padded** (reported):
1. **Counting partner integrations** — techniques covered by an integration partner's product,
   not the vendor's own.
2. **Counting the vendor's other products** — e.g. an NDR vendor including techniques covered
   by its non-NDR products in an NDR coverage figure.
3. **Single-vendor framing** — presenting a single-product number as if it were an
   architecture-wide one.
4. **Scope mismatch with the buyer's estate** — most vendor coverage claims reflect
   endpoint-centric testing, while the attack surfaces that matter are increasingly cloud,
   SaaS, identity and AI. Coverage that does not map to your infrastructure is irrelevant
   coverage.
5. **Zero-filling non-participants** — in the evaluation-marketing variant, including vendors
   who chose not to participate in a test and averaging their "score" in as a zero.

Mechanism 5 is worth isolating: it is a **denominator manipulation over the comparison
population rather than over the technique set**, and it is the same class of error as comparing
ATT&CK coverage across releases with different technique counts. Both take a ratio over a set
that silently changed and present it as a like-for-like comparison.

**The domain-scoping counter-move, and its own problem.** Mitiga's framing — "what 80% MITRE
**Cloud** ATT&CK coverage looks like" — is the honest response to mechanism 4: restrict the
denominator to the relevant matrix. But it immediately creates a comparability break of its
own, since a cloud-scoped percentage and an enterprise-scoped percentage are not comparable
numbers, and ATT&CK's domain boundaries themselves move across releases (the Navigator
CHANGELOG records the removal of the PRE-ATT&CK *domain* at ATT&CK v8, its two tactics folded
into Enterprise under a `PRE` platform tag — a domain-level restructuring that silently
changes every domain-scoped denominator that straddles it). **Every escape from one denominator
problem lands in another, unless the denominator is declared explicitly with its version.**

**Structural criticism of the framework's use as a scorecard.** Databahn's "rethinking the gold
standard" and the general criticism literature report the recurring objections: ATT&CK was not
designed as a compliance or scoring checklist; treating it as one produces
optimise-to-the-matrix behaviour; and framework relevance varies sharply by environment.

# Citable specifics

- The diagnostic question "100% of what, exactly?" as the standard response to a coverage claim.
- The five padding mechanisms above (partner integrations; sibling products; single-vendor
  framing; endpoint-centric scope vs cloud/SaaS/identity/AI estate; zero-filling
  non-participants).
- Mitiga's cloud-scoped "80%" as an instance of denominator restriction changing the headline.
- AttackIQ's March 2026 piece is syndicated at Security Boulevard, so it is citable from two
  URLs — useful if one is paywalled or moves.

# Why this matters to the thesis

This is the evidence that the *market* already treats the coverage percentage as a contested,
manipulable figure, and that the contest is fought entirely over **scope** — which products,
which estate, which matrix, which comparison population. What is completely absent from the
entire genre is the **version** axis: I found no vendor or counter-vendor argument that a
coverage percentage is incomparable because it was computed against a different ATT&CK release.
That absence is itself a finding, and a good one for motivating the thesis: the ecosystem has
independently discovered four dimensions along which coverage is non-comparable and has not
noticed the fifth, even though the fifth is the one that silently changes numbers with no
author action at all.

# Fidelity

**Summary fidelity only, low-to-moderate reliability, commercially motivated sources.** No page
was fetched (egress proxy blocks retrieval). All mechanisms, figures and framings are
**paraphrased from indexed search-result summaries**; nothing was read in full and nothing is
quoted. These are **vendor marketing and vendor-on-vendor criticism**, not independent
research: each author has a commercial interest in the framing that favours its own product's
scope, and the padding mechanisms are *allegations about competitors* rather than documented
cases. Use them to characterise market practice and to motivate the disclosure requirements —
**never** as evidence that a named vendor did a named thing, and never for a number. The one
claim in this note verified from primary source elsewhere in this batch is the PRE-ATT&CK domain
removal at ATT&CK v8, which is documented in the ATT&CK Navigator `CHANGELOG.md` under
`# v4.0 - 27 October 2020` and read directly in the cloned repository. My "absent fifth axis"
observation is an inference from the absence of results across several searches, not a
systematic review.
