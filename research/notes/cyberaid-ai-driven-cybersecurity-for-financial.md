---
title: 'CyberAId: AI-Driven Cybersecurity for Financial'
id: cyberaid-ai-driven-cybersecurity-for-financial
tags:
- attack-ontology-drift-cti-85bc51
- pin-rate-survey
created: '2026-09-12T21:35:58.929614Z'
updated: '2026-09-12T21:44:33.775181Z'
source: https://arxiv.org/abs/2605.01892v1
source_domain: arxiv.org
fetched_at: '2026-09-12T21:35:58.929095Z'
fetch_provider: crawl4ai
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'arXiv 2605.01892v1: 0 ATT&CK technique-ID occurrences, below the pin-rate-survey
  inclusion threshold of 3.'
raw_file: raw/cyberaid-ai-driven-cybersecurity-for-financial.pdf
doi: arXiv:2605.01892v1
---

CyberAId: AI-Driven Cybersecurity for Financial
Service Providers
George Fatouros∗, Georgios Makridis†, John Soldatos∗, Dimosthenis Kyriazis†, Pedro Malo¶,
George Kousiouris‡, Giannis Ledakis§, Louiza Kachrimani§, Panagiotis Rizomiliotis‡ Bruno Almeida¶,
Despina Tomkou∗, Kostas Metaxas∥, Konstantinos Ilias∥, Christos Gkizelis∗∗, Ernstjan de Gooyert††, Amin Babazadeh††,
Kostis Mavrogiorgos†, Pepi Paraskevoulakou†, Christos Xenakis‡‡, Giannis Chouchoulis‡‡, Konstantina Tripodi
x
∗Innov-Acts, Cyprus;
†University of Piraeus, Greece;
‡Harokopio University of Athens, Greece;
§Ubitech, Cyprus;
¶Unparallel Innovation, Portugal;
∥KM Cube Investment Services, Greece;
∗∗Hellenic Telecommunications Organisation, Greece;
††Qubo Technology, Austria;
‡‡InQbit, Romania;
xJRC Capital Management, Germany
{gfatouros, jsoldatos, dtomkou}@innov-acts.com; {gmakridis, dimos, komav, e.paraskevoulakou}@unipi.gr;
{gkousiou, prizomil}@hua.gr; {gledakis, lkachrimani}@ubitech.eu; {pedro.malo, bruno.almeida}@unparallel.pt;
{kostas, k.ilias}@km3.gr; cgkizelis@ote.gr; {ernstjan.degooyert,amin.babazadeh}@qubo.technology;
{chris, giannis.chouchoulis}@inqbit.io; ktripodi@jrconline.com;
Abstract—European financial institutions face mounting reg-
ulatory pressure under DORA, NIS2 and the EU AI Act while
their security operations centres remain constrained not by data
or staffing but by reasoning capacity: enterprise SIEMs cover
only a fraction of MITRE ATT&CK techniques, two thirds
of SOC teams cannot keep pace with alert volumes, and the
majority of breaches are preceded by alerts that are generated
but never investigated. Frontier large language models now
achieve state-of-the-art results on isolated cybersecurity tasks —
one-day vulnerability exploitation, code-level patching, intrusion
detection — yet no narrow win constitutes a platform that can
compose across functions, persist multi-tenant state, map findings
to regulatory regimes and survive an audit. This position paper
argues that the right unit of construction is a hybrid multi-
agent system in which specialised LLM subagents reason over
classical SIEM/XDR telemetry rather than replacing it, share
accumulated agent state across institutions through privacy-
preserving federation, and can connect to complementary capa-
bility packs such as quantum-based authentication, digital twins
for adversarial validation, and eBPF-based kernel telemetry.
We present CyberAId, a model-agnostic, on-premise-deployable
platform in which a Main Agent/CRA coordination layer, a
Reporting capability, and specialist subagents operate within
a shared runtime under bounded human-in-the-loop autonomy,
organised around four falsifiable design principles, and aligned
with DORA reporting timelines and the EU AI Act. CyberAId
will be validated at four representative financial use cases —
client impersonation, anti-money-laundering for payment service
providers, retail-banking incident response, and high-frequency-
trading resilience — and propose skill-based agent adaptation
as the most promising research direction for turning each de-
ployment into a contribution to a continuously refined collective
defence.
Index Terms—LLM agents, multi-agent systems, financial
cybersecurity, retrieval-augmented generation, DORA, digital
twins, cyberaid.
This work was supported by the European Union under the DIGITAL
EUROPE Programme, grant agreement No. 101249596 (CyberAId).
I. INTRODUCTION
The European financial sector manages over C100 trillion in
assets and processes more than 400,000 transactions per day,
while absorbing a 238% growth in cyberattacks since 2020
and roughly three times the attack volume of the next-most-
targeted industry [1], [2]. The threats are concrete and increas-
ingly automated: client impersonation via compromised email
and endpoint devices, payment and transaction fraud that stays
below detection thresholds, money laundering via structuring
and layering across e-money and card-payment ecosystems,
account takeover and credential stuffing, market manipulation
on trading platforms, insider threats that signature-based con-
trols cannot surface, and supply-chain compromise through the
thousands of third-party connections that characterise modern
finance. Each of these scenarios spans data sources, business
processes, and regulatory regimes that no single security tool
was designed to cover.
A. The reasoning bottleneck
Financial security operations centres (SOCs) are increas-
ingly limited not by data or staffing, but by reasoning capacity.
Industry surveys report that enterprise SIEMs detect only
∼21% of MITRE ATT&CK techniques despite ingesting data
that could in principle cover the great majority, that around
two thirds of SOC teams cannot keep pace with alert volumes,
and that the majority of breaches are preceded by alerts that
were generated but never investigated [3]. The consequence
is structural [2]: dwell times for advanced persistent threats
remain measured in months unless reasoning across heteroge-
neous signals is automated.
B. Why narrow LLM wins do not generalise
LLMs have begun to deliver state-of-the-art on isolated
cybersecurity tasks: frontier models autonomously exploit
arXiv:2605.01892v1  [cs.AI]  3 May 2026


---

87% of one-day Common Vulnerabilities and Exposures
(CVEs) from a textual description [4]; multi-agent teams
achieve a 4.3× improvement over single-agent baselines on
zero-day exploitation [5]; LLM-assisted static analysis raises
vulnerability-detection F1 above traditional SAST tools [6];
and domain-specific systems reach 0.97 F1 on intrusion de-
tection [7].
None of these is a platform. A SOC platform must compose
across functions, persist multi-tenant state, ingest live threat
intelligence, map findings to the regulatory regimes that govern
financial services, generate audit-grade artefacts, and survive
adversarial probing of the agents themselves. A monolithic
LLM bolted onto an existing SIEM does none of these things.
The right unit is a hybrid system: classical SIEM/XDR for
ground truth and high-throughput telemetry, specialised LLM
agents for reasoning, and architectural mechanisms for trust.
C. The CyberAId vision
CyberAId is conceived as an integrated, hybrid AI-cyber-
security platform for financial critical infrastructures that
coordinates state-of-the-art security tools through a shared
runtime of logical LLM subagents, federates accumulated
knowledge across institutions, can integrate complementary
capability packs (quantum token authentication, digital twins
for adversarial validation, eBPF-based kernel telemetry), and
operates under bounded human-in-the-loop autonomy. The
intended outcome is a system installed inside the institution,
not a cloud copilot.
D. Contributions
The paper makes four contributions: a position on hybrid
LLM-agent / SIEM-XDR cybersecurity for finance (Sec-
tion II–III); an agent-runtime architecture with one Main
Agent/CRA coordination layer, a Reporting capability, and
specialist subagents covering the financial cyber-resilience
lifecycle (Section IV); a methods stack combining partitioned
RAG, federated cross-institutional knowledge sharing, and
optional capability packs for digital-twin validation, eBPF
telemetry and quantum token authentication (Section V); and
four financial use cases that exercise the platform end-to-end
(Section VI), followed by a discussion of skill-based agent
adaptation as a research direction (Section VII).
II. BACKGROUND AND RELATED WORK
The literature directly relevant to CyberAId clusters around
three observations: LLM agents are now usable building
blocks; hybrid pipelines outperform end-to-end LLM pipelines
on the metrics that matter to a SOC; and the financial-sector
application is almost untouched despite imminent regulatory
pressure.
A. LLM agents as building blocks
Two design patterns now dominate practical agent con-
struction: ReAct-style tool-calling that interleaves reasoning
with tool invocation [8], and plan-and-execute that decom-
poses tasks before acting [9]. Both compose into multi-agent
orchestrations through frameworks such as AutoGen [10],
with retrieval-augmented generation, chain-of-thought prompt-
ing [11], [12] and programmatic tool use [13] providing the
substrate. A consistent pattern across cybersecurity-specific
systems is that orchestration quality matters more than model
scale: a small, well-orchestrated multi-agent system can out-
perform a single large model on incident-response actionability
by a wide margin [14], and hierarchical multi-agent attack
teams achieve a 4.3× improvement over single-agent baselines
on zero-day exploitation [5].
B. Hybrid LLM pipelines outperform end-to-end ones
The second observation is that grounding LLM reasoning in
classical detection, retrieval or planning consistently improves
accuracy, latency and auditability over end-to-end neural
pipelines. SIEM-grounded triage agents [15], agentic-RAG
attack-classification systems [16], and explainable intrusion-
detection agents [7] all retain a deterministic detection floor
and use the LLM for cross-domain synthesis, alert enrichment
and natural-language interaction. On the threat-intelligence
side, graph-augmented agents over CVE, CWE and ATT&CK
chains [17] produce structured CTI artefacts at consistencies
that are difficult to reach through manual curation; phishing
detection follows the same arc, with knowledge-graph- and
debate-augmented detectors outperforming single-pass LLM
classifiers [18]. The throughline is consistent: an LLM reason-
ing over a known-good telemetry surface, with a known-good
knowledge partition, is more accurate and more auditable than
the same model operating end-to-end.
C. Two gaps that motivate CyberAId
Two gaps in this literature directly motivate the position
taken here.
a) Financial cybersecurity is almost untouched: Despite
the regulatory pressure of DORA, NIS2 and the EU AI
Act [19]–[21] and EBA reporting that a majority of EU
payment institutions are adopting AI [1], peer-reviewed work
on LLM agents specifically targeting financial cybersecurity
is sparse: the closest dedicated study addresses STRIDE-based
banking threat-modelling [22], and to the best of our knowl-
edge no work proposes LLM-agent automation for DORA or
NIS2 compliance workflows, financial SOC operations under
regulatory reporting timelines, or cross-institutional federated
defence. CyberAId therefore builds on the agent literature in
cybersecurity rather than on a body of work in finance.
b) Agent-level adversarial robustness is rarely first-class:
Recent surveys catalogue an expanding threat surface against
agent systems: prompt injection, knowledge-base poisoning,
tool-call hijacking, and protocol-level exploits [23], [24].
Knowledge-base poisoning attacks reach high success rates
against unprotected RAG, and dedicated agent-targeted de-
fences remain a minority concern [25]. For a regulated finan-
cial deployment, agent-level adversarial robustness must be
an architectural requirement, not an afterthought; this directly
motivates principle P4 in Section III.


---

III. POSITION AND DESIGN PRINCIPLES
CyberAId is built around four principles, restated here as
falsifiable claims for future work to refute or refine.
P1. Hybrid grounding. Agents reason over SIEM/XDR
telemetry rather than replacing it. The LLM layer pro-
vides
cross-domain
synthesis,
regulatory
mapping,
and
natural-language interaction; classical tooling provides high-
throughput ingestion, deterministic detection on signatures,
and a stable ground truth that the agent can be held against.
Outputs flow back into the SIEM as detection rules, en-
richment fields, and Security Orchestration, Automation, and
Response (SOAR) playbooks [15], [16].
P2. Specialisation and composition. Domain expertise is
partitioned across specialist subagents, each with its own
system instructions, knowledge partition, tool set, and Finding
Schema. Composition is explicit and auditable: one Main
Agent/CRA coordination layer aggregates findings, resolves
conflicts and synthesises recommendations, while a Reporting
capability provides a direct query path to specialists for
compliance and incident reporting.
P3. Federated knowledge. The unit shared across institutions
is accumulated agent knowledge – playbooks, skills, be-
havioural baselines, critical findings from agent runtime – not
raw data. Federated learning, secure multi-party computation,
and differential privacy let smaller institutions inherit detection
capability from larger participants without exporting customer
data, replacing manual sectoral threat-intelligence sharing with
continuous machine-mediated exchange.
P4. Architectural trust. Trust is engineered, not assumed.
Bounded autonomy with tiered human-in-the-loop (HITL)
gates, partitioned RAG scoped by a Security Context object,
direct/CLI-first tool integration with deterministic schemas,
append-only audit, prompt-injection and output-sanitisation
guardrails, and dynamic skill-based adaptation together form
a trust envelope aligned with DORA’s reporting timelines and
Article 14 of the EU AI Act.
IV. THE CYBERAID MULTI-AGENT PLATFORM
This section focuses on the conceptual architecture of
the platform. As shown in Fig. 1, the platform is layered:
Integration and Messaging at the edge, a Domain Agents
layer in which all specialists co-exist within a single agent
runtime (e.g. LangGraph1) with shared messaging, memory
and observability, a Knowledge and Inference layer with
partitioned vector stores and the LLM inference service, and a
Presentation/HITL layer for analyst chat and executive dash-
boards. Co-locating the agents in one runtime keeps inter-agent
latency low and gives the Main Agent/CRA coordination layer
direct access to specialist state for conflict resolution. Tool
integration is therefore primarily through direct library calls
and CLI wrappers (Section V-A); the Model Context Protocol
(MCP) is retained as an optional external integration protocol
behind the Tool Adapter Layer, not as the agent transport.
A Security Context object created at the API gateway flows
1https://github.com/langchain-ai/langgraph
through every agent boundary and is enforced at retrieval and
tool-invocation time.
A. Specialist agent roster
A Main Agent/CRA coordination layer, a Reporting capabil-
ity, and specialist subagents run within a shared agent runtime,
with each specialist retaining its own system instructions,
knowledge partition, tool bindings, and standardised Finding
Schema. The composition mirrors the division of labour ob-
served in mature security teams.
a) Main Agent / Central Router Agent (CRA): Acts as the
analyst-facing triage and dispatch layer. Receives normalised
events from the SIEM event bus, performs initial severity
assessment and impact scoring, activates the appropriate spe-
cialists in parallel, aggregates structured findings, resolves
conflicts using calibrated confidence scores, and synthesises a
final recommendation with full chain-of-thought provenance.
The CRA is also the integration point for HITL escalation and
the entry point for autonomous CRA orchestration patterns
(sequential, peer, debate, scheduled) drawn from the multi-
agent literature [10].
b) Reporting capability: Provides a direct, lower-latency
query path to any specialist agent without routing through
the CRA, so compliance reporting and incident-response op-
erations can run concurrently without contention. Templates
regulatory artefacts (DORA 4-hour notifications, NIS2 24-hour
early warnings, MiFID II incident reports) and assembles audit
packages with traceable evidence references.
c) Threat Intelligence Agent (TIA): Tracks indicators of
compromise and TTPs (Tactics, Techniques, and Procedures),
maps observations to MITRE ATT&CK [26], attributes activ-
ity to known actors, and correlates campaigns across CTI feeds
(STIX/TAXII, vendor advisories). Knowledge is grounded
against a graph-augmented retrieval store spanning CVE/NVD,
CWE, CAPEC and ATT&CK.
d) Vulnerability Assessment Agent (VAA): Scores ex-
ploitability and impact against the institution’s actual expo-
sure profile, cross-references patch availability, and prioritises
remediation under business-impact and regulatory constraints.
Integrates SAST, DAST and LLM-assisted static analysis, and
can consume results from optional adversarial validation in
digital twins (Section V-D).
e) Compliance Verification Agent (CVA): Maintains live
awareness of DORA, NIS2, GDPR, PSD2, 4AML and the EU
AI Act [19]–[21], alongside NIST CSF, ISO/IEC 27001 and
PCI-DSS v4.0. Maps Findings to specific control objectives,
generates audit-ready evidence packages, and produces contin-
uously updated regulatory dashboards with control-by-control
status.
f) Behavioural Analysis Agent (BAA): Runs UEBA logic
against established baselines, surfaces insider threats, and flags
behavioural deviations that signature-based detection cannot
reach. Operates over kernel-level telemetry (Section V-E),
authentication patterns and transaction flows, with confidence-
scored output back to the CRA.


---

Fig. 1. Conceptual architecture of the CyberAId platform. Specialist LLM agents share a single multi-agent runtime that reasons over classical SIEM/XDR
telemetry; a Security Context object enforced at retrieval and tool-invocation time provides the trust envelope; outputs are written back to the SIEM as detection
rules and SOAR playbooks/skills.
g) Incident Response Agent (IRA): Generates structured
containment playbooks, coordinates cross-system isolation ac-
tions, manages recovery sequencing with full state tracking,
and drafts regulatory notifications. Tightly coupled with the
Forensic Analysis Agent for evidence preservation during
containment.
h) Forensic Analysis Agent (FAA): Reconstructs event
timelines from heterogeneous logs (system, application, net-
work, transaction), preserves evidence chains, and produces
findings in formats that meet legal and regulatory standards for
digital forensics. Output is admissible-grade by construction.
i) DevSecOps and Code Analysis Agent (DCA): Per-
forms static and dynamic code analysis, enforces secure-
coding policy in CI/CD, identifies introduced vulnerabili-
ties, and validates SDLC (Secure Software Development Life
Cycle) compliance with PCI-DSS and SOX-style controls,
closing the loop from development pipeline to operational
posture [27].
B. Bounded autonomy
As shown in Fig. 2, three HITL tiers are wired into the
CRA: Tier 1 (autonomous, reversible) for known-indicator
blocking and triage; Tier 2 (confidence-gated escalation) for
ambiguous cases evaluated against per-agent thresholds; and
Tier 3 (explicit approval) for high-severity, low-reversibility
actions. Every decision is recorded with full provenance,
directly implementing the human-oversight requirement of EU
AI Act Article 14 and the audit trail expected under DORA.
V. METHODS: HYBRID FOUNDATIONS AND
COMPLEMENTARY TECHNOLOGIES
The platform is model-agnostic: any sufficiently capable
LLM backbone can serve as the inference layer, with pri-
vate model deployment, for inference on infrastructure that
preserves data residency under DORA, NIS2 and GDPR. The
remainder of this section details the methods stack.
A. Hybrid integration with classical security tooling
The platform consumes normalised security events from a
generic SIEM/XDR over a messaging/alert system (streaming
bus) and writes back into it – detection rules synthesised from
agent-discovered patterns, alert enrichment with TTP and asset
context, and adaptable, by the CRA agent, SOAR playbooks
(agent skills) – closing the analytical loop without removing
the deterministic detection floor that the SIEM provides.
Tool integration on the agent side is primarily through direct
library bindings and CLI wrappers; throughput-sensitive paths
(telemetry ingestion, containment commands, vulnerability
scans, CI/CD hooks) require predictable latency, deterministic
argument schemas and full audit, which are easier to guarantee


---

Fig. 2. Agent orchestration and trust envelope. The Security Context flows
around the CRA and specialists; the CRA performs confidence scoring and
conflict resolution; HITL tiers route decisions to autonomous, gated, or
approval paths; every input, retrieval, tool call and confidence is written to an
append-only audit log; the Reporting capability feeds regulatory dashboards.
through versioned CLI wrappers than through dynamically
discovered MCP descriptors. MCP is an optional external
integration protocol behind the Tool Adapter Layer for cross-
service exploratory investigations and for integrating external
services that already expose MCP endpoints.
B. Knowledge stack and partitioned RAG
Each agent queries its own vector partition, scoped at
retrieval time by the Security Context, against four classes
of source: operational telemetry (system and application logs,
file-integrity events, kernel telemetry, transaction streams,
email and messaging, source-code and CI/CD events); ex-
ternal cyber threat intelligence (STIX/TAXII feeds, ven-
dor advisories, exploit prediction scoring system (EPSS)
and KEV2 scoring); authoritative knowledge bases (MITRE
ATT&CK, CVE/NVD, CWE, CAPEC, NIST CSF, NIST 800-
2https://www.cisa.gov/known-exploited-vulnerabilities-catalog
53, ISO/IEC 27001); and regulatory corpora (DORA, NIS2,
GDPR, PSD2, 4AML, AI Act, EBA and ECB guidelines).
Retrieval is hybrid (dense + sparse), augmented by graph
traversal over CVE →CWE →CAPEC →ATT&CK chains.
Continuous CTI ingestion keeps the partitions current; vector
stores are themselves treated as security-sensitive: encrypted at
rest and in transit, integrity-monitored, and protected against
poisoning attacks [24].
C. Federated cross-institutional knowledge sharing
What is shared across participating institutions is accu-
mulated agent knowledge such as detection rules or work-
flows, identified behavioural patterns (e.g., impersonation at-
tempts) and agent skills. These are aggregated under secure
multi-party computation, secure aggregation and differential-
privacy budgets calibrated to the sensitivity of the underlying
data. Smaller institutions inherit detection capability from
the collective without exporting customer data. Thus, each
deployment becomes a contribution to a continuously refined
collective agentic defence.
D. Autonomous adversarial validation in digital twins
The platform can attach digital-twin replicas of the institu-
tion’s critical infrastructure as an optional capability pack for
safe, continuous adversarial validation. LLM-driven red-team
agents [25] may operate inside the twin, attempting industry-
specific attack patterns against payment systems, banking
portals, trading APIs and credential flows. Successful exploit
paths can be converted into detection rules ingested by the
SIEM, prioritisation hints for the VAA, and updated guardrails
for the agents themselves, closing an otherwise asymmetric
offensive–defensive loop in a controlled environment.
E. eBPF-based kernel telemetry on financial endpoints
Critical financial infrastructure is increasingly composed of
edge devices: ATMs, POS terminals, mobile banking and pay-
ment apps, payment gateways, broker feeds. The platform can
consume eBPF (extended Berkeley Packet Filter) instrumenta-
tion through a telemetry provider for low-overhead syscall and
network visibility on these endpoints, feeding the Behavioural
and Forensic agents at sub-second latency without disturbing
production workloads [28]. The combination of eBPF teleme-
try and LLM-assisted reasoning can enable behaviour-level
detection of patterns that signature-based controls miss: lateral
movement on POS networks, unusual administrative escalation
on core banking servers, anomalous market-data feed handling.
F. Quantum Token authentication
For high-value transaction flows the platform can inte-
grate a quantum-token-based two-factor authentication (2FA)
provider, exploiting the no-cloning theorem [29]. It may be
used in bank-to-bank and custodian–asset-manager transac-
tions where each token is single-use, unforgeable, and any
tampering is detectable by construction.


---

G. Skill-based agent adaptation
Each agent loads a base capability surface plus a set of
skills – composable, versioned, signed packages that bundle a
prompt template, a tool binding, an RAG query pattern, a reg-
ulatory mapping and KPI targets. Skills replace the monolithic
system prompt with a context-activated, evolvable specialisa-
tion layer. Examples: an aml-eu-emoney skill for the AML
use case (Section VI-B); a mifid-ii-incident skill for
HFT regulatory reporting (Section VI-D); a pci-dss-v4
skill for the DCA. We discuss skill-based adaptation as an
open research direction in Section VII.
VI. USE CASES
CyberAId will be validated at four representative use cases
drawn from financial sub-sectors with materially different
threat profiles, data sources, regulatory regimes, and tool
integrations.
A. UC-1: Tiered client impersonation detection (private bank-
ing)
Smaller asset managers routinely relay client orders to
larger custodian institutions, creating opportunity for attack-
ers to insert fraudulent instructions via compromised email
accounts or endpoint devices – typically at amounts kept
below verification thresholds. The platform applies LLM-
driven content analysis of order and transfer emails to detect
linguistic deviation from the client’s communication base-
line, structural anomalies in headers and attachments, and
inconsistencies between the message and the client’s histor-
ical patterns. Federated learning across custodians and asset
managers shares detection improvements without exposing
client data, so smaller institutions inherit large-bank detection
capability. An optional quantum-token-based 2FA channel can
bind high-value instructions to a physically unforgeable token
(Section V-F). The end-to-end workflow is illustrated in Fig. 3.
Agents engaged: TIA, BAA, IRA, CVA. Regulatory hooks:
PSD2 strong customer authentication, GDPR, AI Act oversight
on automated decision support.
B. UC-2:
Anti-money-laundering
for
payment
service
providers
E-money institutions face a structural false-positive problem
with rule-based AML, with detection rates above 95% in name
only and limited capacity to catch sophisticated structuring
or layering [22]. The platform builds dynamic transaction
graphs across e-wallet, IBAN-connected and card-payment
ecosystems, applies graph analytics for detecting structuring,
smurfing and layering, and uses the BAA and TIA jointly
to identify shell-account and nominee-account patterns. The
Forensic Analysis Agent and the IRA can replay suspicious
flows inside a digital twin capability pack (Section V-D)
for safe analyst investigation. The CVA generates suspicious-
activity reports and audit packages aligned with 4AML and
national reporting templates. Federated knowledge sharing
accelerates detection of cross-institutional laundering rings.
Agents engaged: BAA, TIA, FAA, IRA, CVA, CRA, Report-
ing.
Fig. 3. Client-impersonation use case (UC-1). A suspicious order is wrapped
in a Security Context, triaged by the CRA, and analysed in parallel by
the Behavioural, Compliance, Vulnerability and Incident-Response agents; an
optional quantum-token authentication challenge can gate high-value flows;
an Evidence Bundle is assembled in the standard Finding Schema; HITL
escalation is determined by confidence, value, and regulatory obligation; every
decision is captured in an append-only audit log.
C. UC-3: Multi-channel anomaly detection and incident re-
sponse (retail banking)
Large retail banks operate at a scale – tens of thousands of
servers, millions of clients, multi-petabyte log warehouses –
at which alert volumes overwhelm even mature SOCs. The
platform can consume eBPF-enhanced telemetry across end-
points (Section V-E), feed the BAA with kernel-level syscall
and network signals, and use the CRA to perform pipelined
triage at low latency. Confirmed incidents trigger the IRA to
execute pre-approved playbooks under tier-2 HITL, while the
FAA preserves evidence in parallel. The CVA maintains a live
control dashboard and the Reporting capability drafts incident
notifications within the 4-hour DORA window. Agents en-
gaged: BAA, TIA, VAA, IRA, FAA, CVA, CRA, Reporting.
Complementary technologies: eBPF, federated detection-rule
sharing.


---

D. UC-4: Cyber-resilient high-frequency trading
High-frequency trading desks combine three high-value
asset classes: proprietary algorithms (intellectual property),
market-data feeds (integrity), and continuous availability under
regulatory observation by national supervisors. The platform
monitors algorithm repositories and runtime behaviour with
the DCA and the BAA for unauthorised access or model-
output drift, validates market-data feeds for integrity and
triggers established failover paths automatically, and uses
the CRA-Reporting pair to synthesise forensic evidence and
incident reports under DORA and MiFID II. Latency budget
for any agent-side action is below second on the trading-
critical path; the bulk of agent reasoning happens out-of-band
on the monitoring path. Agents engaged: DCA, BAA, VAA,
IRA, FAA, CVA, CRA, Reporting.
VII. DISCUSSION AND OPEN RESEARCH DIRECTIONS
A. Skill-based adaptation as a research direction
Section V-G introduced skills as composable specialisation
packages. Conceptually, skills generalise three ideas already
present in the agent literature: programmatic tool use [13], the
ReAct-style separation of reasoning and acting [8], and plan-
and-execute decomposition [9], [11], combined with modular
orchestration patterns [10]. What is novel for the regulated
cybersecurity setting is that skills must be provenance-bearing
(signed, versioned, attributable), conflict-resolvable (when two
skills disagree, the resolution must be auditable), and co-
trainable with the federated-learning loop of Section V-C:
aggregated agent knowledge and analyst feedback should
refine the global skill library over time.
This raises concrete research questions: the semantics of
skill conflict resolution when, e.g., an AML skill flags a
pattern that a PCI-DSS skill would suppress as a known
compliance scan; skill poisoning, since the threat model for
externally authored skills extends the known RAG-poisoning
surface; skill consistency under federated update, including
how differential-privacy budgets are allocated when each fed-
erated round refines multiple skills with overlapping evidence;
and skill-level evaluation, since existing benchmarks grade
agents end-to-end rather than skill by skill.
B. Other open directions
Three further gaps deserve attention before SOC-scale de-
ployment becomes routine: production-grade evaluation, since
the gap between laboratory evaluation and operational deploy-
ment remains the single largest barrier to adoption; benchmark
consolidation, since available benchmarks offer overlapping
coverage and incompatible scoring; and adversarial robustness
of the agents themselves, widely acknowledged as critical but
rarely treated as a first-class concern. CyberAId positions skill-
based adaptation, federated knowledge sharing and digital-
twin adversarial validation as the three operational levers most
likely to convert these gaps into measurable progress.
VIII. CONCLUSION
Securing financial critical infrastructures with LLMs re-
quires neither a smarter monolithic model nor a new SIEM
but a hybrid multi-agent system: specialist subagents reasoning
over classical security tooling, sharing accumulated knowledge
across institutions, and connecting to optional capability packs
for adversarial validation, kernel-level visibility and quantum-
token-based authentication. CyberAId implements this posi-
tion as a shared runtime with a Main Agent/CRA coordi-
nation layer, a Reporting capability, and specialist subagents
under bounded human-in-the-loop autonomy, with skill-based
adaptation as the most promising research direction toward
continuously refined collective defence.
ACKNOWLEDGMENT
This work has received funding from the European Union
under the DIGITAL EUROPE Programme, grant agreement
No. 101249596 (CyberAId).
The authors used the AI tool Claude Opus 4.7 for grammar
and style editing of the manuscript and Gemini NanoBanana
to assist in figure generation, with all content reviewed and
verified by the authors.
REFERENCES
[1] European Banking Authority, “Report on artificial intelligence in the
banking sector,” EBA, Paris, France, Tech. Rep., 2024. [Online].
Available: https://www.eba.europa.eu
[2] IBM
Security,
“Cost
of
a
data
breach
report
2024,”
IBM,
Armonk,
NY,
USA,
Tech.
Rep.,
2024,
accessed:
2026-04-01. [Online]. Available: https://www.ibm.com/think/insights/
cost-of-a-data-breach-2024-financial-industry
[3] S.
Srinivas,
B.
Kirk,
J.
Zendejas,
M.
Espino,
M.
Boskovich,
A.
Bari,
K.
Dajani,
and
N.
Alzahrani,
“Ai-augmented
soc:
A
survey of llms and agents for security automation,” Journal of
Cybersecurity and Privacy, vol. 5, no. 4, 2025. [Online]. Available:
https://www.mdpi.com/2624-800X/5/4/95
[4] R.
Fang,
R.
Bindu,
A.
Gupta,
and
D.
Kang,
“LLM
agents
can autonomously exploit one-day vulnerabilities,” arXiv preprint
arXiv:2404.08144, 2024.
[5] Y. Zhu, A. Kellermann, A. Gupta, P. Li, R. Fang, R. Bindu, and
D. Kang, “Teams of llm agents can exploit zero-day vulnerabilities,”
in Proceedings of the 19th Conference of the European Chapter of the
Association for Computational Linguistics (Volume 1: Long Papers),
2026, pp. 23–35.
[6] Z. Li, S. Dutta, and M. Naik, “IRIS: LLM-assisted static analysis
for detecting security vulnerabilities,” arXiv preprint arXiv:2405.17238,
2024, accepted at ICLR 2025.
[7] Y. Li, Z. Xiang, N. D. Bastian, D. Song, and B. Li, “Ids-agent:
An llm agent for explainable intrusion detection in iot networks,” in
NeurIPS 2024 Workshop on Open-World Agents: Synnergizing Reason-
ing and Decision-Making in Open-World Environments (OWA-2024),
2024, poster.
[8] S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. Narasimhan, and Y. Cao,
“ReAct: Synergizing reasoning and acting in language models,” in Pro-
ceedings of the International Conference on Learning Representations
(ICLR 2023), Kigali, Rwanda, 2023.
[9] L. Wang, C. Ma, X. Feng, Z. Zhang, H. Yang, J. Zhang, Z. Chen,
J. Tang, X. Chen, Y. Lin et al., “A survey on large language model based
autonomous agents,” Frontiers of Computer Science, vol. 18, no. 6, p.
186345, 2024.
[10] Q. Wu, G. Bansal, J. Zhang, Y. Wu, B. Li, E. Zhu, L. Jiang, X. Zhang,
S. Zhang, J. Liu et al., “Autogen: Enabling next-gen llm applications via
multi-agent conversations,” in First conference on language modeling,
2024.


---

[11] J. Wei, X. Wang, D. Schuurmans, M. Bosma, F. Xia, E. Chi, Q. V. Le,
D. Zhou et al., “Chain-of-thought prompting elicits reasoning in large
language models,” Advances in neural information processing systems,
vol. 35, pp. 24 824–24 837, 2022.
[12] G. Fatouros and K. Metaxas, “Signal or noise in multi-agent llm-based
stock recommendations?” arXiv preprint arXiv:2604.17327, 2026.
[13] T. Schick, J. Dwivedi-Yu, R. Dess`ı, R. Raileanu, M. Lomeli, E. Hambro,
L. Zettlemoyer, N. Cancedda, and T. Scialom, “Toolformer: Language
models can teach themselves to use tools,” Advances in neural informa-
tion processing systems, vol. 36, pp. 68 539–68 551, 2023.
[14] P. Drammeh, “Multi-agent llm orchestration achieves deterministic,
high-quality decision support for incident response,” arXiv preprint
arXiv:2511.15755, 2025.
[15] B. Wei, Y. S. Tay, H. Liu, J. Pan, K. Luo, Z. Zhu, and C. Jordan,
“CORTEX: Collaborative LLM agents for high-stakes alert triage,” arXiv
preprint arXiv:2510.00311, 2025.
[16] F. Blefari, C. Cosentino, F. A. Pironti, A. Furfaro, and F. Marozzo,
“Cyberrag: An agentic rag cyber attack classification and reporting tool,”
Future Generation Computer Systems, p. 108186, 2025.
[17] L. Huang and X. Xiao, “CTIKG: LLM-powered knowledge graph
construction from cyber threat intelligence,” in Proceedings of the First
Conference on Language Modeling (COLM 2024), Philadelphia, PA,
USA, 2024.
[18] Y. Li, C. Huang, S. Deng, M. L. Lock, T. Cao, N. Oo, H. W. Lim,
and B. Hooi, “KnowPhish: Large language models meet multimodal
knowledge graphs for enhancing reference-based phishing detection,” in
33rd USENIX Security Symposium (USENIX Security 24). Philadelphia,
PA: USENIX Association, 2024, pp. 793–810. [Online]. Available: https:
//www.usenix.org/conference/usenixsecurity24/presentation/li-yuexin
[19] European Parliament and Council, “Regulation (EU) 2022/2554 on
digital operational resilience for the financial sector (DORA),” Brussels,
Belgium, 2022.
[20] EU, “Directive (EU) 2022/2555 on measures for a high common level
of cybersecurity across the union (NIS2),” Brussels, Belgium, 2022.
[21] European Parliament and Council, “Regulation (EU) 2024/1689 laying
down harmonised rules on artificial intelligence (AI Act),” Brussels,
Belgium, 2024.
[22] T. Wu, S. Yang, S. Liu, D. Nguyen, S. Jang, and A. Abuadbba,
“Threatmodeling-llm: Automating threat modeling using large language
models for banking system,” arXiv preprint arXiv:2411.17058, 2024.
[23] F. He, T. Zhu, D. Ye, B. Liu, W. Zhou, and P. S. Yu, “The emerged
security and privacy of LLM agent: A survey with case studies,” ACM
Computing Surveys, 2025.
[24] M. A. Ferrag, N. Tihanyi, D. Hamouda, L. Maglaras, A. Lakas, and
M. Debbah, “From prompt injections to protocol exploits: Threats in
llm-powered ai agents workflows,” ICT Express, 2025.
[25] B. Challita and P. Parrend, “RedTeamLLM: An agentic AI framework
for offensive security,” arXiv preprint arXiv:2505.06913, 2025.
[26] MITRE Corporation, “MITRE ATT&CK Enterprise Matrix, Version 14,”
MITRE ATT&CK Enterprise Matrix, Version 14, McLean, VA, USA,
2023, available online: https://attack.mitre.org (accessed on 1 April
2026).
[27] S. Chippagiri and A. Ramesh, “Pci dss: A critical analysis of implemen-
tation, effectiveness, and legislative impact in payment card security,”
2025.
[28] D. Zhan, Z. Yu, X. Yu, H. Zhang, and L. Ye, “Shrinking the kernel
attack surface through static and dynamic syscall limitation,” IEEE
Transactions on Services Computing, vol. 16, no. 2, pp. 1431–1443,
2022.
[29] P. Schiansky, J. Kalb, E. Sztatecsny, M.-C. Roehsner, T. Guggemos,
A. Trenti, M. Bozzio, and P. Walther, “Demonstration of quantum-digital
payments,” nature communications, vol. 14, no. 1, p. 3849, 2023.
