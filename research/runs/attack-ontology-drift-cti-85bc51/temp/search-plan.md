# Step 2 search plan — attack-ontology-drift-cti-85bc51

Environment note: this session's egress proxy blocks direct page fetching
(`hyperresearch fetch`, WebFetch, curl → 403 for arxiv.org, attack.mitre.org,
publisher sites). Two lanes work and the plan is built around them: the
`WebSearch` tool, and anonymous `git clone` of public GitHub repositories.
Batches are non-overlapping; each is dispatched to exactly one research agent.

| Batch | Atomic item(s) | Search query | Type | Lens | Target |
|---|---|---|---|---|---|
| B1 | Sub-Q1, Sub-Q2, Entity: ATT&CK | "MITRE ATT&CK changelog deprecated revoked technique semantics" | web | breadth | factual |
| B1 | Sub-Q1 | "ATT&CK sub-technique restructuring v7 migration guidance" | web | breadth | factual |
| B1 | Sub-Q1 | "ATT&CK STIX 2.1 spec x_mitre_deprecated revoked-by relationship" | web | depth | canonical |
| B1 | Sub-Q1 | "ATT&CK v19 release notes Impair Defenses T1562 revoked" | web | breadth | recency |
| B2 | Sub-Q5, Entity: attribution | "TTP-based threat actor attribution ATT&CK technique profile method" | academic | depth | canonical |
| B2 | Sub-Q5 | "automated ATT&CK technique extraction from threat reports rcATT TTPDrill AttacKG" | academic | depth | canonical |
| B2 | Sub-Q5 | "TTP extraction model ATT&CK version used training labels" | academic | depth | provenance |
| B2 | Sub-Q5 | "limitations of TTP-based attribution false flag" | web | adversarial | contrarian |
| B3 | Sub-Q7, Entity: benchmarks | "CTIBench benchmark LLM cyber threat intelligence ATT&CK technique extraction" | academic | depth | canonical |
| B3 | Sub-Q7 | "CTIArena CTIConnect heterogeneous CTI benchmark 2026" | academic | depth | recency |
| B3 | Sub-Q7 | "CTI benchmark label quality criticism contamination" | web | adversarial | contrarian |
| B3 | Sub-Q7 | "SEvenLLM SynthCTI ATT&CK mapping dataset construction version" | academic | depth | provenance |
| B4 | Sub-Q1, Sub-Q10 | "criticism of MITRE ATT&CK framework limitations taxonomy" | web | adversarial | contrarian |
| B4 | Sub-Q1 | "ATT&CK coverage bias reporting bias threat intelligence skew" | academic | adversarial | contrarian |
| B4 | Sub-Q5 | "why ATT&CK technique mapping is unreliable inter-rater agreement" | web | adversarial | contrarian |
| B4 | Sub-Q10 | "ATT&CK is not a taxonomy ontology critique" | web | adversarial | contrarian |
| B5 | Sub-Q7, Sub-Q9 | "cyber threat intelligence data quality accuracy timeliness study" | academic | breadth | factual |
| B5 | Sub-Q9 | "threat intelligence feed evaluation measurement study" | academic | depth | canonical |
| B5 | Sub-Q9 | "CTI sharing challenges evidence-driven analysis" | academic | breadth | factual |
| B5 | Sub-Q9 | "STIX TAXII data quality problems practitioners" | web | adversarial | contrarian |
| B6 | Sub-Q10, Entity: concept drift | "concept drift security machine learning label shift malware detection" | academic | depth | canonical |
| B6 | Sub-Q10 | "Tesseract temporal bias experimental design malware classification" | academic | depth | canonical |
| B6 | Sub-Q10 | "dos and don'ts of machine learning in computer security pitfalls" | academic | depth | canonical |
| B6 | Sub-Q10 | "benchmark decay dataset ageing reproducibility security research" | academic | adversarial | contrarian |
| B7 | Sub-Q8, Sub-Q9 | "ontology evolution versioning change management OWL mapping" | academic | depth | canonical |
| B7 | Sub-Q8 | "identifier deprecation semantic versioning controlled vocabulary curation" | academic | depth | canonical |
| B7 | Sub-Q8 | "CVE CWE CAPEC identifier reuse rejected entries data quality" | web | breadth | factual |
| B7 | Sub-Q8 | "NVD CVSS re-scoring historical data comparability" | web | adversarial | contrarian |
| B8 | Sub-Q6 | "ATT&CK detection coverage measurement Navigator layer methodology" | web | breadth | factual |
| B8 | Sub-Q6 | "vendor ATT&CK coverage claims criticism marketing" | web | adversarial | contrarian |
| B8 | Sub-Q6 | "MITRE ATT&CK Evaluations methodology criticism comparability across rounds" | web | adversarial | contrarian |
| B8 | Sub-Q6 | "security control coverage metric denominator problem" | web | depth | canonical |
