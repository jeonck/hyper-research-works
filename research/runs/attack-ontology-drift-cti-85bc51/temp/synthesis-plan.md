# Step 11 — synthesis plan

## What the three drafts gave us

- **Draft A (measurement-first, ~13,650 words, truncated after Section 8).** The
  best methodology section by a distance, and the best framing device: ATT&CK is
  a measuring instrument that has been re-issued 109 times and never once
  reported its calibration. Sections 5 and 6 are the ones to keep almost whole.
  Stops mid-Section 8, so it contributes nothing to 9–12.
- **Draft B (threat-to-validity, ~19,340 words, complete, 241 citation markers).**
  The strongest positioning for the venue: security machine learning learned to
  control for bias in the data and never noticed the label space was moving.
  Best Sections 3, 4 and 11. Far too long and over-cited; needs roughly halving.
- **Draft C (remedy and governance, ~12,110 words, complete, no Sources
  section).** The most honest. Its Section 8 dismantles our own protocol, and its
  Sections 9 and 10 turn the finding into something a reviewer can check. Keep
  its self-critique intact — softening it would repeat the error the paper
  diagnoses.

All three report identical numbers, which is the point of the shared evidence
digest. No reconciliation of figures is needed; only of voice and length.

## Section-by-section source

| Section | Primary source | Notes |
|---|---|---|
| Abstract | new, built from B's framing and A's numbers | must state the concession as well as the finding |
| 1. Introduction | B, opened with A's instrument framing | lead with the v19 T1562 case, it is concrete and current |
| 2. Background | A | keep the STIX mechanics precise and short |
| 3. Related Work | B | concept drift cannot express label-space change; ontology engineering already solved it; CTI quality frameworks omit it |
| 4. Formalization | B, with A's six-kind taxonomy | the identity/intension split is load-bearing for the whole paper |
| 5. Data and Methodology | A | the reproducibility spine; state the beta-release exclusion and the major-release convention explicitly |
| 6. Measuring drift | A, compressed | Tables 2–5, 13; Figures 1–4 |
| 7. Downstream impact | B for the experiment's logic, A for the numbers | Tables 6, 7, 8, 10, 11; Figures 5, 6, 8; the noise factorial belongs here, not in a footnote |
| 8. ATT&CK-Norm | C, unsoftened | the worked T1562 counter-example, the ledger, roll-up fires 3 in 12,027 |
| 9. Deployed corpora | C, with A's CTIBench forensics | Table 9, 12; Figure 7 |
| 10. Discussion | C | the four-line contract and the named ports |
| 11. Threats to validity | B | the closed ATT&CK-internal loop first, then the rest |
| 12. Conclusion | new, short | no new numbers |
| Sources | rebuilt from the registry | only entries actually cited |

## Budget

9,000 words ± 500. Sections 6 and 7 get roughly 2,600 together; 8, 9 and 10
roughly 2,400; 1–5 roughly 2,800; 11 and 12 roughly 1,000. Citation markers
between 100 and 130.

## Three things the synthesis must not lose

1. The concession. Enterprise identifier accounting is complete, the inter-labeller
   noise floor is large, and normalization buys almost nothing in the modern
   regime. The paper earns its claim by conceding all three early.
2. The two-clock model. Identifier churn is episodic and recurrent across
   domains, one event per 4.4 domain-years; semantic churn is continuous at 10%
   substantively rewritten in roughly eighteen months. Neither half alone is the
   finding.
3. The self-critique of the protocol. Draft C's Section 8 is the paper's
   credibility. It stays.
