## Coverage Matrix — query phrase → atomic item mapping

| Query phrase (verbatim) | Mapped atomic item(s) | Scope check | Gap? |
|---|---|---|---|
| "ontology drift in the MITRE ATT&CK knowledge base" | Sub-Q1; Entity: MITRE ATT&CK; Sub-Q on drift taxonomy (§4) | OK — all three domains (Enterprise, Mobile, ICS), not Enterprise only | No |
| "technique additions" | Sub-Q1 (churn measurement, E1) | OK | No |
| "deprecations" | Sub-Q1, Sub-Q2 (deprecated flag tracked separately from revoked) | OK — deprecation and revocation kept distinct, as ATT&CK defines them | No |
| "revocations" | Sub-Q1, Sub-Q2, Sub-Q8 (revoked-by chains drive normalization) | OK | No |
| "sub-technique restructuring" | Sub-Q1, Sub-Q4, Sub-Q5 (v7.0 discontinuity) | OK | No |
| "tactic reassignment" | Sub-Q1 (tactic-set change among ID-stable techniques) | OK — measured, not merely mentioned | No |
| "silent rewriting of technique descriptions" | Sub-Q3 (semantic drift, E3) | OK — both edit incidence and edit magnitude | No |
| "across releases" | Time horizon 2018-01→2026-08; all 106 public releases | OK — every release, not a sample | No |
| "validity, comparability and reproducibility" | Sub-Q7 (validity), Sub-Q5/Q6 (comparability), Sub-Q9 (reproducibility discipline) | OK — three distinct properties, each with its own evidence | No |
| "cyber threat intelligence analytics" | Entities: attribution, benchmark labels, coverage claims | OK — scope condition records that these three stand for the wider class | No |
| "TTP-based threat-actor attribution" | Sub-Q5; Entity: attribution | OK | No |
| "CTI benchmark and training-set labels" | Sub-Q7; Entity: CTIBench/TRAM/rcATT | OK — both evaluation benchmarks and training corpora | No |
| "detection/mitigation coverage claims" | Sub-Q6 | OK — both relations measured (mitigates and detects) | No |
| "what fraction of apparent growth ... genuine new adversary intelligence versus ontology bookkeeping" | Sub-Q4 (E4 decomposition) | OK | No |
| "normalization protocol" | Sub-Q8; Entity: ATT&CK-Norm | OK — includes measured failure modes, not only gains | No |
| "reporting discipline" | Sub-Q9 (§10) | OK | No |
| "existing literature on CTI quality" | Sub-Q10; §3 Related Work | OK | No |
| "ATT&CK-based analytics" | Sub-Q10; §3 | OK | No |
| "LLM CTI benchmarks (CTIBench, CTIArena and successors)" | Sub-Q10; Sub-Q7; §3 | OK — "and successors" read as the post-2024 benchmark family broadly | No |
| "TTP extraction and attribution" | Sub-Q10; §3 | OK — extraction covered as well as attribution | No |
| "concept drift in security machine learning" | Sub-Q10; Entity: concept drift; §3 and §4 (distinction argued) | OK — treated as a neighbouring but distinct phenomenon | No |
| "what an SCI-level contribution in this space must demonstrate" | Sub-Q10; §10 | OK | No |
