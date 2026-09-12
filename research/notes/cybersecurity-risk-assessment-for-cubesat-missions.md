---
title: 'Cybersecurity Risk Assessment for CubeSat Missions:'
id: cybersecurity-risk-assessment-for-cubesat-missions
tags:
- attack-ontology-drift-cti-85bc51
- pin-rate-survey
created: '2026-09-12T21:36:07.522824Z'
updated: '2026-09-12T21:44:34.696285Z'
source: https://arxiv.org/abs/2604.00303v1
source_domain: arxiv.org
fetched_at: '2026-09-12T21:36:07.522358Z'
fetch_provider: crawl4ai
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'arXiv 2604.00303v1 (2026): uses 6 ATT&CK technique-ID occurrences (without
  sub-techniques); ATT&CK release declaration classified as none.'
raw_file: raw/cybersecurity-risk-assessment-for-cubesat-missions.pdf
doi: arXiv:2604.00303v1
---

Cybersecurity Risk Assessment for CubeSat Missions:
Adapting Established Frameworks for
Resource-Constrained Environments
Jonathan Shelby∗
Department of Computer Science, University of Oxford
jonathan.shelby@cs.ox.ac.uk
Abstract
CubeSats have democratised access to space for universities, start-ups and emerging space nations, but the same
design decisions that reduce cost and complexity introduce distinctive cybersecurity risks. Existing risk assessment
frameworks—NIST SP 800-37/53 [1,2], ISO/IEC 27001/27005 [3,4] and supply-chain guidance such as NIST SP 800-
161 [5]—assume abundant computational resources, centralised monitoring and mature governance structures that do
not hold for power-limited, intermittently connected CubeSat missions.
This paper develops a contextually appropriate risk assessment framework tailored to CubeSat environments,
grounded in a 42-entry vulnerability register coded using STRIDE [6], MITRE ATT&CK [7] and CVSS v3.1 [8].
The register reveals that risks concentrate in communication and ground segments (mean CVSS 8.0–8.2) rather than
distributing uniformly across subsystems.
The framework introduces two constructs: a Security-per-Watt (SpW)
heuristic that quantifies security benefit per unit power, and a Distributed Security Paradigm (DSP) that reconcep-
tualises incident response as an autonomous, constellation-level function rather than a purely ground-centric process.
Scenario-based analysis demonstrates that adapted controls and distributed incident handling can achieve up to 2.7×
higher SpW for cryptographic choices and 1.98× higher SpW for incident-response strategies compared with naïve ter-
restrial transpositions, while remaining feasible for typical CubeSat power and governance constraints. The approach
provides mission designers, operators and regulators with proportionate, auditable guidance, and offers a reusable
pattern for adapting enterprise security frameworks to other severely constrained cyber-physical systems.
Keywords: CubeSat, cybersecurity, risk assessment, NIST SP 800-53, ISO/IEC 27001, Security-per-Watt, distributed
security, small satellites
1
Introduction
CubeSat technology has transformed the economics and
accessibility of space, evolving from educational demon-
strators into operational platforms for Earth observation,
communications and technology demonstration [9, 10].
Standardised 1U form factors (10×10×10 cm), reli-
ance on commercial off-the-shelf (COTS) components
and university- or start-up-led programmes have reduced
costs—a 1U CubeSat may cost as little as $50,000 USD,
compared with millions for a conventional satellite [11]—
but created heterogeneous, globally distributed supply
chains with uneven security assurance [12].
Concurrently, CubeSats increasingly operate in con-
tested or safety-critical contexts:
defence, commercial
imaging and commercial communications.
Jamming,
spoofing and cyber compromise in these domains carry
non-trivial operational and geopolitical implications [13,
14]. Traditional cybersecurity frameworks, notably NIST
SP 800-37/53 [1, 2], ISO/IEC 27001/27005 [3, 4] and C-
SCRM guidance [5], offer mature control catalogues and
governance processes but embed assumptions of continu-
ous monitoring, substantial computational headroom and
stable organisational structures that are misaligned with
1–2 W power budgets and short contact windows.
This paper addresses the central question: how should
established cybersecurity risk frameworks be proportion-
ately adapted for CubeSat missions operating under
severe resource constraints, without discarding their pro-
tective intent?
The contributions are fourfold:
(i) A structured vulnerability register for CubeSats
(42 entries) using dual STRIDE/ATT&CK cod-
ing and CVSS v3.1 scoring, demonstrating that
risks cluster in communication and ground segments
(mean CVSS 8.0–8.2 versus 6.9 for onboard comput-
ing).
(ii) A Security-per-Watt (SpW) heuristic that quantifies
risk-reduction benefit per unit of operational power,
enabling systematic, auditable trade-off decisions.
(iii) A Distributed Security Paradigm (DSP) that re-
conceptualises incident response as an autonomous,
constellation-level function suited to intermittent
connectivity.
(iv) An adapted risk framework that reinterprets selec-
ted NIST and ISO controls for sub-watt budgets, val-
idated through scenario-based analytical assessment
reflecting legal and ethical constraints on attacking
operational spacecraft.
1
arXiv:2604.00303v1  [cs.CR]  31 Mar 2026


---

The paper is structured as follows. Section 2 reviews
CubeSat architecture, the cyber threat landscape and ex-
isting risk frameworks. Section 3 describes the method-
ology. Section 4 presents the vulnerability register and
analysis. Section 5 details the adapted framework, the
SpW heuristic and illustrative control adaptations. Sec-
tion 6 reports scenario-based validation. Section 7 dis-
cusses implications and limitations, and Section 8 con-
cludes with future research directions.
2
Background and Related Work
2.1
CubeSat Evolution and Constraints
The CubeSat Design Specification [15] standardises
10 cm cubes (1U) with a mass limit of approximately
1.33 kg and typical power budgets of 1–2 W. Since
their introduction, more than 2,500 CubeSats have been
launched [16], including PlanetScope Earth-observation
constellations providing 3–4 m resolution imagery [17]
and NASA’s MarCO CubeSats, which demonstrated
deep-space communication viability by relaying tele-
metry across 140 million kilometres during the Mars In-
Sight mission [18].
These capabilities are enabled by miniaturised sensors,
low-power ARM Cortex-M class microcontrollers, and
software-defined radios (SDRs) [19, 20]. Architecturally,
typical CubeSats comprise four major subsystems, each
presenting distinct attack surfaces.
Ground segment.
Ground stations use SDRs oper-
ating in UHF (300–3,000 MHz) and S-band (2–4 GHz)
within short contact windows per orbit [21].
Mission
control systems handle telemetry, scheduling and pay-
load data dissemination, often with links to external net-
works. This connectivity creates exposure: weak authen-
tication or poorly segmented interfaces can enable com-
mand injection, with effects ranging from configuration
drift to mission interruption [22]. Ground assets may also
be at risk from unpatched firmware, inconsistent access
control and heterogeneous vendor practices—including
SDRs with uneven update policies or baseline security
controls [14,23].
Onboard
computer
(OBC).
The OBC executes
commands,
manages navigation,
coordinates subsys-
tems and processes payload data.
Most CubeSats
employ ARM Cortex-M class microcontrollers running
RTOS variants such as FreeRTOS under strict power
budgets [19,20]. These devices are technically capable of
cryptographic operations (including AES-256 and ECC),
but sustained use at high duty cycles competes with
navigation, communications and payload operations for
power, CPU time and memory.
In practice, operat-
ors make trade-offs that constrain algorithm choice, key
length or invocation frequency rather than forgoing cryp-
tography entirely. Relevant attack surfaces include firm-
ware exploitation (e.g., buffer overflows or unsafe update
paths), inconsistent patching and provenance for COTS
microcontrollers, limited memory protection that can fa-
cilitate privilege escalation, and risks of data exfiltration
where nodes inter-share data in constellations [24,25].
Communication subsystem.
Communication sub-
systems enable telemetry downlink, command uplink
and, increasingly, inter-satellite coordination.
AX.25
(from amateur radio heritage) and CCSDS families are
commonly employed [26, 27].
These were designed
primarily for simplicity, reliability and interoperability
rather than resistance to active adversaries. As a result,
eavesdropping on unencrypted or lightly protected links
can compromise confidentiality; spoofing can allow un-
authorised command injection; jamming can block short
LEO passes; and man-in-the-middle attacks may exploit
insufficient authentication to modify traffic [28].
Network infrastructure.
Constellations increasingly
employ inter-satellite links (ISLs) and distributed ar-
chitectures to coordinate swarms and maintain global
coverage.
Technologies include SpaceWire, CAN bus
within spacecraft and IP-based networking across seg-
ments. Distributed architectures introduce failure modes
distinct from single-satellite operations: denial-of-service
attacks can saturate shared channels and desynchronise
operations, while compromise of one node may propagate
effects to others in decentralised topologies [14,29].
2.2
Cybersecurity in Satellite and Small-
Sat Systems
Cyber threats against satellite infrastructures span in-
terception of unencrypted telemetry, jamming, spoofing
of navigation and telecommand links, command injec-
tion, and manipulation of spacecraft subsystems [13,14].
Small satellites are particularly exposed because resource
constraints preclude direct deployment of heavyweight
terrestrial security stacks, and operational contexts of-
ten assume benign users [30]. Documented incidents—
including the AcidRain malware campaign against Viasat
infrastructure [31]—demonstrate that space systems are
viable and attractive cyber targets.
For CubeSats, legacy AX.25 and minimally secured
CCSDS profiles lack strong authentication and confiden-
tiality, making uplink spoofing, link-layer tampering and
denial of service realistic threats, particularly given the
accessibility of low-cost ground hardware [23,24]. Multi-
vendor COTS integration introduces inconsistent firm-
ware provenance and patching practices across ground
and space segments, amplifying supply-chain risk [5,32].
2.3
Existing Risk Frameworks
Established frameworks relevant to CubeSats include the
NIST Cybersecurity Framework [33], NIST SP 800-37
and 800-53 [1,2], ISO/IEC 27001/27005 [3,4] and NIST
C-SCRM [5].
Each reflects distinct intellectual tradi-
tions and embeds assumptions about the environments
in which it will be applied.
NIST SP 800-37 structures risk management as a six-
stage lifecycle—system categorisation, control selection,
2


---

implementation, assessment, authorisation and continu-
ous monitoring [1]. While CubeSats operate in dynamic
threat environments, the reliance on extensive document-
ation and near-constant oversight poses significant chal-
lenges: CubeSats may have only minutes of communica-
tion time per orbit and operate autonomously for long
periods.
The central premise that continuous human
oversight is possible is at odds with orbital realities.
NIST SP 800-53 provides a comprehensive catalogue
of security controls across twenty control families [2]. Of
particular relevance are SC-8 (Transmission Confidenti-
ality and Integrity), AU-6 (Audit Record Review, Ana-
lysis and Reporting) and IR-4 (Incident Handling). In
terrestrial systems, SC-8 would typically be implemen-
ted through TLS or IPsec tunnels; for CubeSats, stand-
ard TLS/IPsec is infeasible, but equivalent protections
via ECC key exchanges and compact authenticated en-
cryption are viable subject to platform constraints. This
illustrates a central theme: while the controls themselves
are conceptually relevant, their implementation must be
radically reinterpreted for resource-constrained environ-
ments.
ISO/IEC 27001 adopts an explicitly organisational ori-
entation, requiring creation of an Information Security
Management System tailored to stakeholder context [3].
Its companion, ISO 27005, provides structured method-
ologies for risk identification, analysis and treatment [4].
While the flexibility of these standards is advantageous
in principle, they implicitly assume centralised organ-
isations with consistent governance structures. CubeSat
projects often involve temporary consortia of universit-
ies, start-ups and agencies where authority, resourcing
and risk appetite vary dramatically.
The C-SCRM framework addresses the provenance and
trustworthiness of suppliers [5,34]. Its relevance to Cube-
Sats is striking: reliance on COTS components from di-
verse international vendors creates exposure to counter-
feit parts, compromised firmware and uneven patching
practices. Yet, designed primarily for the U.S. Depart-
ment of Defence, C-SCRM prescribes compliance-heavy
procedures and extensive supplier certification that are
misaligned with lean CubeSat budgets.
Prior work has adapted these frameworks for larger
satellite programmes [35, 36], but direct transplantation
to CubeSats fails on assumptions of persistent human
oversight, ample logging capacity and extensive supplier
vetting.
2.4
Emerging Technologies
Several technologies have been proposed to enhance
CubeSat security. Table 1 synthesises a comparative feas-
ibility assessment.
AI-driven anomaly detection emerges as the most vi-
able near-term intervention, combining high conceptual
potential with practical deployability on microcontrol-
ler hardware [37].
Lightweight model architectures—
decision trees, one-class support vector machines and
pruned autoencoders—can provide anomaly detection
within milliwatt power budgets when quantised for ARM
Cortex-M class processors. The principal constraint re-
mains data realism: representative telemetry datasets for
CubeSats are scarce, and overfitting to laboratory con-
ditions risks reduced efficacy in orbit. Adversarial ma-
chine learning techniques may deliberately craft inputs
to evade detection, highlighting the need for adversarial
robustness evaluation as a standard part of model quali-
fication [38].
Zero-trust architectures, while requiring hybrid ad-
aptation to accommodate communication-window con-
straints, represent a realistic medium-term opportun-
ity [39,40]. Full “never trust, always verify” implementa-
tion is infeasible given CubeSat contact schedules, but
bounded reinterpretation—mutual authentication once
per orbital pass, anomaly-triggered re-authentication
and least-privilege command-set design—can achieve the
same protective intent.
Such hybrid approaches lever-
age the principle that “continuous” must be interpreted
as “event-of-contact-driven” in intermittently connected
systems.
Blockchain-based authentication has been proposed to
address identity management in multi-actor constella-
tions. Conventional proof-of-work consensus is infeasible,
but permissioned blockchains using algorithms such as
Practical Byzantine Fault Tolerance could be adapted.
However, implementation requires non-trivial computa-
tional overhead, additional inter-satellite bandwidth and
coordination across multiple stakeholders; orbital demon-
strations suitable for peer-reviewed evaluation remain ab-
sent from the literature.
Post-quantum cryptography and quantum key distri-
bution face the most severe constraints.
Lattice-based
schemes such as Kyber offer quantum resilience but re-
quire significantly larger key sizes and computational
overhead compared with ECC [41–43]. For typical short-
lived LEO missions, PQC is more relevant as a research
direction than immediate adoption; QKD requires optical
payloads and precise pointing that exceed most CubeSat
capabilities entirely.
3
Methodology
The study adopts a pragmatic mixed-methods design
combining
systematic
literature
review,
structured
vulnerability assessment,
framework adaptation and
scenario-based analytical validation [44].
Pragmatism
was selected because it permits the combination of struc-
tured, rule-guided analysis (e.g., vulnerability categorisa-
tion and scoring) with interpretive judgement (e.g., map-
ping the intent of controls to CubeSat realities), priorit-
ising usable knowledge over strict allegiance to a single
epistemic doctrine.
The overall design proceeded in four interlocking
phases. First, a systematic literature review established
the current state of knowledge and surfaced gaps relevant
to small-satellite security (Section 2). Second, a struc-
tured vulnerability assessment translated domain-specific
risks into a consistent taxonomy and severity scale (Sec-
tion 4). Third, a comparative framework analysis and
adaptation step recomposed NIST, ISO/IEC and supply-
chain guidance into a resource-aware methodology at-
3


---

Table 1: Emerging cybersecurity technologies: feasibility assessment for CubeSat deployment.
Technology
Conceptual
Potential
Near-Term
Practicality
Key Constraints
Rating*
Zero-trust
architec-
tures
High
Medium/High
(hybrid)
Contact-window length; pro-
tocol overhead
3.5
AI-driven
anomaly
detection
High
High
Limited training data; false
positives
4.0
Blockchain
authen-
tication
Medium
Low/Medium
Consensus overhead; no in-
orbit validation
2.5
Post-quantum cryp-
tography
High
(long-
term)
Low
Processing
power;
mission
duration
2.0
Quantum key distri-
bution
Very high
Very low
Optical payload; ground in-
frastructure
2.0
*1 = not viable; 2 = long-term research; 3 = partially feasible with adaptation; 4 = near-term feasible; 5 = fully feasible.
tuned to CubeSat constraints (Section 5).
Finally, an
analytical validation used realistic but illustrative scen-
arios to test the internal coherence and decision utility of
the adapted framework (Section 6).
3.1
Data Collection
A PRISMA-guided search [45] across IEEE Xplore, ACM
Digital Library, ScienceDirect, SpringerLink and special-
ist small-satellite outlets (Acta Astronautica, Journal of
Small Satellites) identified peer-reviewed work on Cube-
Sat and small-sat security, relevant risk frameworks and
operational characteristics.
Standards including NIST
SP 800-37/53 [1, 2], ISO/IEC 27001/27005 [3, 4] and
CCSDS security guidelines [26] were treated as author-
itative expressions of control intent and architectural
baselines. Grey literature (ESA technical notes, CubeSat
Developers Workshop proceedings, vendor white papers)
was used cautiously, critically appraised for provenance
and triangulated against scholarly sources before inclu-
sion.
Records were included where they addressed: (i) secur-
ity properties or vulnerabilities of small satellites or adja-
cent constrained systems; (ii) risk governance frameworks
and control families germane to communications, cryp-
tography, logging, incident response or supply chains; or
(iii) operational realities of CubeSat missions, including
power budgets, onboard computing, contact windows and
ground-segment architectures.
3.2
Vulnerability Assessment
From this corpus, vulnerabilities relevant to CubeSat ar-
chitectures were extracted and encoded using a bespoke
taxonomy combining three layers. The top layer classi-
fied entries by system domain: ground segment, onboard
computing, communications or network/constellation.
The middle layer adopted the STRIDE model [6, 46] to
ensure comprehensive threat coverage (spoofing, tamper-
ing, repudiation, information disclosure, denial of ser-
vice, elevation of privilege). The bottom layer mapped
MITRE ATT&CK tactics and techniques where appro-
priate [7, 47], allowing cross-walk to a widely used ad-
versary model.
Each entry recorded source, context, affected compon-
ent, preconditions, likely impact and plausible mitiga-
tions.
Entries were then assigned a CVSS v3.1 base
score [8] with justification recorded to support auditab-
ility. Attack vectors were interpreted for orbital environ-
ments: Network includes RF interception; Physical re-
flects orbital inaccessibility. Impact scoring was weighted
towards mission-critical functions, maintaining compat-
ibility with established threat intelligence while acknow-
ledging space-specific operational constraints.
3.3
Framework Adaptation
Adaptation proceeded in three steps. First, a constraint
analysis identified mismatches between framework as-
sumptions and CubeSat realities—continuous monitor-
ing versus short contact windows, extensive audit log-
ging versus limited onboard storage, extensive supplier
vetting versus lean mission budgets. Second, a control-
intent extraction articulated what each control is de-
signed to achieve in principle:
SC-8’s preservation of
confidentiality and integrity for data in transit, AU-6’s
support for accountability, IR-4’s requirement for effect-
ive incident handling irrespective of environment. Third,
a contextual reinterpretation mapped control intent to
CubeSat-feasible implementations, taking into account
power, storage, connectivity and governance limitations.
The SpW heuristic was applied to rank candidate con-
trols where power budget is a binding constraint. Be-
cause SpW values depend on implementation detail and
mission context, the study did not claim universal con-
stants; instead, it illustrated how the ratio helps structure
choices transparently.
3.4
Scenario-Based Validation
Legal and ethical constraints precluded experimental at-
tacks on operational satellites (UK Computer Misuse
Act 1990; ethical impracticability of attacking space-
craft). Validation relied on scenario-based analysis us-
ing templates that link vulnerabilities, adapted con-
trols and SpW-based decisions.
Three scenarios were
developed: (i) cryptographic selection for a university
4


---

Table 2: CVSS v3.1 severity summary by subsystem (n =
42).
Subsystem
n
Mean
Median
IQR
Ground segment
10
8.2
8.4
1.4
Onboard computing
11
6.9
6.8
1.7
Communications
12
8.0
8.2
2.0
Network/constellation
9
7.5
7.3
1.3
Earth-observation CubeSat, (ii) incident handling for a
24-satellite LEO constellation and (iii) supply-chain as-
surance for a multi-vendor radio procurement. Each was
evaluated against five criteria: traceability to adapted
controls, proportionality to constraints, feasibility of im-
plementation path, alignment with the vulnerability re-
gister, and reproducibility of rationale.
The scenarios were intentionally analytical rather than
empirically validated; their purpose was to demonstrate
that the framework produces defensible, proportionate
decisions when confronted with typical CubeSat limita-
tions.
3.5
Quality Assurance
Methodological quality was addressed through several
strategies. Transparency was achieved by documenting
inclusion criteria, search strings, screening decisions and
coding rules. Analytic reliability was supported by main-
taining an audit trail of coding decisions; where ambigu-
ities arose (e.g., whether a vulnerability should be coded
as spoofing or tampering), the decision and rationale
were recorded. Triangulation reduced single-source bias:
vulnerabilities and mitigation claims were cross-checked
across peer-reviewed articles, standards and independ-
ent technical notes.
Coherence checks were embedded
between sections: vulnerabilities prioritised in Section 4
were required to be addressable by adaptations in Sec-
tion 5, and scenarios in Section 6 were required to exer-
cise those same adaptations under plausible constraints.
4
CubeSat
Vulnerability
Land-
scape
4.1
Subsystem Severity Distribution
The vulnerability register comprises 42 entries across four
principal subsystems. Table 2 summarises the CVSS v3.1
base score statistics.
Communications and ground segment vulnerabilities
receive the highest mean severities (8.0–8.2), reflect-
ing adversary accessibility via ground networks and ra-
dio links.
Onboard computing, while non-trivially ex-
posed, benefits from orbital isolation and more con-
strained attack surfaces (mean CVSS 6.9). Network and
constellation-level vulnerabilities fall between these ex-
tremes, with risks related to lateral movement, key li-
fecycle management and denial of service across inter-
satellite links.
This distribution is consistent with the expectation
that external interfaces broaden the attack surface most
significantly [14, 28].
Many CubeSats still use plain
AX.25 or legacy CCSDS protocols without modern en-
cryption or authentication, making it relatively straight-
forward for an attacker within range to spoof commands
or intercept telemetry [24,26].
4.2
STRIDE and ATT&CK Mapping
Threats were mapped across subsystems using STRIDE
categories, revealing systematic patterns. Spoofing and
tampering dominate ground and communication com-
ponents, reflecting risks of unauthorised command injec-
tion, falsified telemetry and man-in-the-middle attacks
on protocol stacks. Denial-of-service arises from the sus-
ceptibility of narrowband links and short passes to jam-
ming and flooding. Elevation-of-privilege issues appear
more prominently in onboard and ground software, where
insecure update mechanisms and weak isolation enable
privilege escalation once footholds are gained.
Table 3 summarises selected STRIDE threats across
major components.
Mapping to MITRE ATT&CK confirmed alignment
with known adversary behaviours: unauthenticated up-
links correspond to Valid Accounts (T1078),
plain-
text telemetry reflects Application Layer Protocol abuse
(T1071), and insecure bootloaders resemble Boot Persist-
ence (T1547) [7,48]. This alignment indicates that Cube-
Sat adversaries can reuse established terrestrial tactics
adapted to space-specific protocols, enabling defenders
to leverage ATT&CK-informed threat intelligence.
4.3
Supply-Chain Risk
CubeSat projects draw on global supply chains span-
ning hardware, firmware and software.
Multi-national
sourcing
introduces
inconsistent
patching,
opaque
provenance and opportunities for malicious insertion [5,
49].
Practical vectors include malicious microcode in
embedded controllers, modified SDR firmware and com-
promised ground software, with limited options for post-
deployment remediation once assets are on-orbit [24].
Frameworks such as NIST SP 800-161 provide structured
C-SCRM guidance, but full adoption is unrealistic for
small academic or start-up missions [34].
4.4
Advanced Persistent Threats
The threat picture extends beyond isolated jamming,
spoofing or ad-hoc intrusions. Adversaries with sustained
capability—state and non-state—can mount campaigns
that integrate technical, organisational and geopolitical
elements.
Supply-chain
compromise
as
strategic
vector.
Terrestrial incidents (e.g., software supply-chain com-
promises) illustrate the impact of tampered compon-
ents or dependencies.
In the CubeSat context, multi-
national sourcing, academic collaboration and subcon-
tracting complicate assurance [49]. Feasible vectors in-
5


---

Table 3: STRIDE threat mapping across CubeSat components.
Component
Threat
Example
Ground segment
Spoofing
Impersonation of ground stations to submit commands
where authentication is weak or absent
Ground segment
Tampering
Alteration of commands or telemetry in transit or at
rest, leading to unsafe state or operator misinterpreta-
tion
Ground segment
Elevation
of
privilege
Unauthorised access to mission control platforms en-
ables broad operational impact
OBC
Tampering
Firmware modification via unsafe update paths, altering
mission logic or disabling subsystems
OBC
Elevation
of
privilege
Exploitation of limited memory protection and process
isolation in microcontroller RTOS
Communications
Information
disclosure
Interception of unencrypted telemetry over AX.25 or
minimally secured CCSDS links
Communications
Denial of ser-
vice
Uplink/downlink jamming during short LEO passes,
causing missed tasking or data loss
Communications
Spoofing
Faked identities or frames over weakly authenticated
protocol stacks
Network
Spoofing
Forged identities within distributed networks permitting
unauthorised access to shared services
Network
Denial of ser-
vice
Saturation of inter-satellite links disrupting coordinated
constellation operations
clude malicious microcode in embedded controllers or
modified SDR firmware that subverts expected beha-
viour. Compared with terrestrial systems, opportunities
for post-deployment remediation are narrower, increasing
the value of pre-launch assurance.
Constellation-level
campaigns.
Distributed
con-
stellations can concentrate risk as well as resilience.
Where inter-satellite links, shared timing sources or com-
mon ground infrastructure are employed, compromise of
one node or service may enable lateral movement if au-
thentication, authorisation and update processes are in-
sufficiently segregated [29,50]. Protocol analyses relevant
to small satellites indicate that permissive or optional
handshakes, if adopted for simplicity, can weaken resist-
ance to spoofing or man-in-the-middle attacks. In prac-
tice, consequences are likely to be service degradation
(missed passes, delayed tasking), integrity issues in fused
products or selective denial of function rather than im-
mediate loss of an entire constellation.
Nation-state capabilities.
Public reporting from re-
cent conflicts demonstrates combined use of cyber opera-
tions and electronic warfare against satellite services and
their ground segments [31]. Small satellites that employ
widely known protocols and educational-industrial sup-
ply chains can be attractive targets where defences are
minimal. For CubeSat operators, practical implications
include planning for interference and outage, adopting
authenticated control links, ensuring recoverable config-
urations and exercising incident procedures that account
for short contact windows.
Quantum
computing
threats.
Most
CubeSat
designs use symmetric cryptography for link protection
and ECC for key establishment. If large-scale quantum
computing becomes practical, widely deployed public-key
schemes will be at risk, creating “harvest-now-decrypt-
later” considerations for missions whose data retains
value beyond the cryptoperiod [41,42]. A proportionate
approach for near-term LEO missions is to maintain
robust symmetric primitives, employ forward-secure or
frequent rekeying strategies and consider PQC in cases
where operational life or data sensitivity justify the
overhead [43].
AI-powered adaptive attacks.
As lightweight AI for
anomaly detection matures for onboard use, adversar-
ies may apply related methods to evade detection or op-
timise interference—for example, reinforcement-learning
strategies that adapt jamming parameters within link
budgets, or generation of synthetic telemetry to mislead
operators [37]. The immediate risk for CubeSats is less
about sophisticated autonomy in the threat and more
about the brittleness of models trained on narrow data-
sets.
Defensive use of AI should therefore include ad-
versarial evaluation, explicit fall-backs to rules or simple
invariants for safety-critical checks, and clear thresholds
for isolating suspect subsystems when confidence is low.
6


---

5
Adapting Risk Frameworks for
CubeSats
5.1
Framework Strengths and Limita-
tions
Table 4 summarises the strengths, limitations and high-
level adaptations of major frameworks when applied to
CubeSats.
The core observation is that control intent often re-
mains valid, but implementation detail must be altered
radically to respect CubeSat resource envelopes.
5.2
Risk Classification
Definition 5.1 (Three-Tier Risk Classification). To re-
place complex CVSS-based scoring for operational use, a
three-tier classification is defined:
• High risk:
Threats directly affecting telemetry,
command or navigation integrity, where exploitation
could result in mission failure.
• Medium risk: Threats affecting payload confidenti-
ality or ground-segment data flows, with potential for
operational degradation but not catastrophic failure.
• Low risk: Threats primarily affecting availability
during short communication windows or introducing
non-critical inefficiencies.
This simplification does not diminish rigour but pri-
oritises decision-making in environments where time, ex-
pertise and resources are scarce.
5.3
Security-per-Watt (SpW) Heuristic
SpW is formalised as a decision-support construct. Para-
meters are analytical placeholders derived from the
vulnerability register and literature-based plausibility
bounds; calibration is deferred to future empirical work.
Definition 5.2 (Security Gain). Security effectiveness
is quantified using risk-weighted vulnerability reduction:
SG =
X
i
 CVSSi × Pi × Mi × RRFi

,
(1)
where CVSSi is the base score of vulnerability i, Pi the es-
timated exploitation probability (0–1), Mi a mission crit-
icality weight (0–1) and RRFi the risk-reduction factor
of the candidate control (0–1).
Definition 5.3 (Operational Power). Operational power
consumption accounts for duty cycle and environmental
factors:
Poperational = Pbase×Duty_Cycle×Environmental_Factor,
(2)
where the environmental factor adjusts for temperature,
radiation and component ageing in LEO.
Definition 5.4 (Security-per-Watt). The complete SpW
formulation is:
SpW =
SG
Poperational
± σ(SpW),
(3)
where σ(SpW) represents uncertainty bands to be estab-
lished during calibration studies.
SpW does not attempt to be a universal metric.
It
provides a transparent ratio that allows designers to com-
pare candidate controls in terms of risk-reduction benefit
per watt, under clearly stated assumptions. Empirical
validation would require ARM Cortex-M4 test platforms
under controlled conditions, power measurement accur-
acy of ≥±5% using precision current monitoring, secur-
ity effectiveness validation through standardised penet-
ration testing, and statistical significance testing (n ≥30
trials, ANOVA analysis). To enable meaningful compar-
ison, SpW values can be normalised against baseline im-
plementations:
SpWnormalised = SpWcandidate
SpWbaseline
.
(4)
Multi-criteria optimisation extends beyond power con-
sumption:
SEI = α(SpW)+β(Latency)+γ(Storage)+δ(Complexity),
(5)
where weighting factors (α, β, γ, δ) sum to unity and re-
flect mission-specific priorities.
5.4
Illustrative Control Adaptations
Several NIST SP 800-53 controls [2] illustrate the adapt-
ation pattern.
SC-8: Transmission Confidentiality and Integrity.
In terrestrial systems SC-8 is commonly implemented via
TLS or IPsec tunnels; in CubeSats this is infeasible. In-
stead, SC-8 intent can be met using elliptic-curve key ex-
change (e.g., Curve25519) combined with compact Au-
thenticated Encryption with Associated Data (AEAD)
such as AES-CCM or ChaCha20-Poly1305, tuned for mi-
crocontroller platforms [51]. Key renegotiation per or-
bital pass rather than continuously provides adequate
confidentiality with manageable overhead.
AU-6: Audit Record Review, Analysis and Re-
porting.
Continuous verbose logging is unsustainable
onboard a 1–2 W CubeSat. AU-6 intent is preserved by
logging only critical state transitions—safe-mode entry,
subsystem resets, command acceptance events—in a cyc-
lic buffer and downlinking opportunistically [52]. This
reduces logging overhead to less than 0.05 W while main-
taining accountability.
IR-4:
Incident Handling.
Traditional IR-4 imple-
mentations assume human-in-the-loop response, patch
deployment and forensic analysis.
For CubeSats, IR-4
is reinterpreted as pre-authorised autonomous responses:
safe-mode fallback, rate-limited command acceptance,
and temporary isolation of anomalous subsystems when
locally detectable thresholds are exceeded [53].
7


---

Table 4: Risk frameworks versus CubeSat constraints.
Framework
Strengths
Key CubeSat Lim-
itations
Proposed Adaptations
NIST SP 800-37
Systematic
lifecycle
methodology
Assumes
continuous
monitoring and cent-
ralised
management;
documentation
over-
head
high
for
small
teams
Simplified
metrics;
anomaly-driven
mon-
itoring;
decentralised
management
NIST SP 800-53
Comprehensive con-
trol catalogue
Control
volume
and
logging
assumptions
exceed
power
and
storage budgets
Lightweight
crypto-
graphy;
rationalised
supply-chain
checks;
SpW-guided selection
ISO/IEC
27001/27005
Flexible ISMS, struc-
tured risk methods
Presupposes stable or-
ganisations and recur-
ring audits;
CubeSat
projects are often tem-
porary consortia
Simplified
audit
cycles;
mission-specific controls
C-SCRM
Supply-chain
focus,
high COTS relevance
Defence-centric,
compliance-heavy;
unrealistic
for
low-
budget missions
Baseline vendor require-
ments; contractual obliga-
tions for firmware proven-
ance
C-SCRM Adaptation.
Full military-grade supply-
chain certification is unrealistic for CubeSat missions.
The framework reframes supply-chain governance as
baseline practices: contractual obligations for firmware
update provenance, a shared register of approved com-
ponent versions, and documented acceptance testing at
integration [5,34].
5.5
Distributed
Security
Paradigm
(DSP)
The DSP reconceptualises incident response and mon-
itoring from centralised ground-station operations to
a constellation-level function with autonomous local
decision-making.
This reconceptualisation is motiv-
ated by the fundamental mismatch between traditional
incident-response models and CubeSat operational real-
ities:
centralised ground-based response assumes con-
tinuous communication, real-time telemetry analysis and
human-in-the-loop decision-making, none of which are re-
liably available for LEO constellations with contact win-
dows of minutes per orbit.
Remark 5.1 (DSP Architectural Principles). The DSP
rests on four principles:
(i) Per-node credentials with revocation: each satellite
maintains individual cryptographic identity with the
ability to revoke compromised credentials fleet-wide
during the next contact window.
(ii) Signed configuration and update artefacts: all firm-
ware updates and configuration changes are crypto-
graphically signed, with rollback protection to prevent
reversion to vulnerable states.
(iii) Rate-limiting on shared services: inter-satellite links
and shared resources enforce rate limits that bound
the impact of a compromised node on constellation-
level operations.
(iv) Control–payload
partitioning:
command-and-
control pathways are architecturally separated from
payload data pathways, so that data compromise
does not imply command compromise.
The paradigm embodies a design philosophy in which
each satellite is equipped with pre-authorised contain-
ment actions—safe-mode entry, command rate-limiting,
subsystem isolation—that can be triggered autonomously
when locally detectable anomaly thresholds are exceeded.
This approach sacrifices some absolute security effect-
iveness (the risk-reduction factor drops from 0.95 under
centralised human oversight to approximately 0.85 under
autonomous detection) but achieves substantially better
security efficiency per unit of power consumed, as valid-
ated in the scenario analysis that follows.
6
Scenario-Based Validation
6.1
Scenario 1: Cryptographic Selection
A university-led Earth-observation CubeSat operating in
a 500 km sun-synchronous orbit must select a protec-
tion scheme for telemetry and command links. The mis-
sion employs a 1U platform with a total power budget of
2 W, of which approximately 0.3 W is available for secur-
ity functions after allocating power to attitude determ-
ination and control, payload imaging and housekeeping.
The ground segment uses an SDR operating in UHF, with
contact windows of approximately 8–12 minutes per pass,
four to six passes per day over the university’s ground
station.
Two candidate cryptographic approaches are evalu-
ated against the vulnerability register entry for unau-
8


---

thenticated uplinks (CVSS 9.0, classified as high risk un-
der Definition 5.1). The CVSS score of 9.0 reflects the
severity of unprotected command channels: an adversary
within radio range could inject commands to alter space-
craft attitude, disable payload operations, or place the
satellite into a non-recoverable state.
ECC implementation (Curve25519 key exchange with
ChaCha20-Poly1305 AEAD):
SGECC = 9.0 × 0.8 × 1.0 × 0.9 = 6.48
Pop = 0.18 W ± 0.02 W
SpWECC = 6.48/0.18 = 36.0 ± 4.2
The RRF of 0.9 (rather than 1.0) accounts for the re-
sidual risk that side-channel attacks or implementation
flaws could weaken the protection. The power figure of
0.18 W reflects the duty-cycled cost of ECC key exchange
once per pass plus continuous AEAD on the telemetry
stream, based on published benchmarks for ARM Cortex-
M4 processors [51,54].
RSA implementation (RSA-2048 key exchange with
AES-256-GCM):
SGRSA = 9.0 × 0.8 × 1.0 × 0.95 = 6.84
Pop = 0.52 W ± 0.05 W
SpWRSA = 6.84/0.52 = 13.2 ± 2.8
RSA-2048 achieves a marginally higher RRF (0.95) ow-
ing to the longer cryptanalytic track record of the al-
gorithm, but at nearly three times the power cost. The
0.52 W figure consumes over 25% of the total power
budget, materially constraining payload duty cycle and
potentially reducing mission science return.
Proposition 6.1 (ECC Dominance under SpW). ECC
provides 2.7× superior SpW efficiency (p < 0.001), justi-
fying selection despite marginally lower absolute security
gain.
The
framework
directed
the
team
towards
ECC/AEAD, satisfying SC-8 intent without exhausting
scarce power resources.
Key renegotiation per orbital
pass provides adequate confidentiality with manageable
overhead,
and the framework further recommended
strict command authentication using ECDSA signatures
to address the specific spoofing risk identified in the
vulnerability register.
6.2
Scenario 2:
Constellation Incident
Response
A commercial operator running a 24-satellite LEO con-
stellation for IoT data relay detects anomalous behaviour
in one node: unexpected attitude changes, irregular tele-
metry patterns and command-acceptance anomalies sug-
gestive of firmware compromise. The constellation op-
erates with 90-minute orbital periods and contact win-
dows of approximately 10 minutes per ground station
per pass, with four geographically distributed ground
stations providing intermittent coverage. Two incident-
response strategies are evaluated using both SpW ana-
lysis and multi-criteria optimisation.
Strategy
A—Centralised
Ground-Based
Re-
sponse:
This strategy follows traditional IR-4 implementation:
manual ground intervention with real-time telemetry
analysis, full constellation shutdown pending investiga-
tion, and human-in-the-loop decision-making for remedi-
ation. Addressing vulnerabilities N1 (inter-satellite rout-
ing compromise, CVSS 7.4), N5 (constellation key man-
agement failure, CVSS 8.3) and O2 (firmware integrity
violation, CVSS 9.0):
SGA = (7.4 × 0.9 × 1.0 × 0.95) + (8.3 × 0.8 × 1.0 × 0.95)
+ (9.0 × 0.7 × 1.0 × 0.95) = 18.62
Pop,A = 11.7 W ± 1.2 W
SpWA = 18.62/11.7 = 1.59 ± 0.18
The power budget for Strategy A breaks down as fol-
lows: continuous telemetry uplink at 0.4 W per satellite
across the 24-node constellation (9.6 W total), plus the
allocated proportion of ground-station processing power
(2.1 W). The high aggregate power cost reflects the cent-
ralised architecture’s requirement that all satellites main-
tain active telemetry streams to enable ground-based an-
omaly detection.
Strategy B—Distributed Autonomous Response
(DSP):
This strategy implements the Distributed Security
Paradigm:
pre-authorised local safe-mode activation
upon detection of anomaly thresholds, autonomous isol-
ation of the compromised node from inter-satellite links,
and automated fleet-level containment procedures that
quarantine the affected orbital plane while maintaining
service on remaining planes. Risk-reduction factors are
reduced to 0.85 (from 0.95) to account for the inherent
limitations of autonomous detection compared with hu-
man analysis—primarily the risk of false positives lead-
ing to unnecessary safe-mode entry and the possibility of
sophisticated attacks that evade simple threshold-based
detection:
SGB = (7.4 × 0.9 × 1.0 × 0.85) + (8.3 × 0.8 × 1.0 × 0.85)
+ (9.0 × 0.7 × 1.0 × 0.85) = 16.67
Pop,B = 5.28 W ± 0.6 W
SpWB = 16.67/5.28 = 3.16 ± 0.41
The power budget for Strategy B is substantially lower:
local anomaly detection at 0.05 W per satellite (1.2 W
total), safe-mode monitoring overhead at 0.02 W per
satellite (0.48 W), and inter-satellite coordination mes-
saging at 0.15 W per satellite (3.6 W). The distrib-
uted approach eliminates the need for continuous high-
bandwidth telemetry uplink, instead relying on light-
weight local monitoring with event-driven reporting.
Proposition
6.2
(DSP Efficiency). The distributed
strategy achieves 1.98× superior SpW while consuming
55% less power, at a cost of only 10.5% reduction in ab-
solute security effectiveness.
Multi-criteria
assessment.
Using
mission-specific
weights that prioritise SpW efficiency and response time
9


---

over implementation complexity (α = 0.4, β = 0.3,
γ = 0.2, δ = 0.1):
SEIA = 0.4(1.59) + 0.3(0.2) + 0.2(0.1) + 0.1(0.9) = 0.806
SEIB = 0.4(3.16) + 0.3(0.8) + 0.2(0.7) + 0.1(0.6) = 1.666
The distributed approach produces a Security Effect-
iveness Index more than double that of the centralised
baseline, supporting the thesis that autonomous, pre-
planned containment offers better security-per-resource
under CubeSat constraints.
The 10.5% security effectiveness reduction is offset
by 65% faster incident detection (autonomous versus
ground-loop delays), elimination of single-point-of-failure
in ground operations, and maintained constellation func-
tionality during incident containment.
6.3
Scenario 3: Supply-Chain Assurance
An academic consortium procured radios from mul-
tiple vendors for a multi-mission CubeSat programme.
Full military-grade C-SCRM certification was unreal-
istic given budget and timeline constraints. The frame-
work recommended a graduated set of baseline prac-
tices: contractual obligations requiring firmware proven-
ance and patch transparency for all critical components;
a shared register of approved component versions, main-
tained across the consortium; documented acceptance
testing at integration, including basic firmware integrity
verification; and a named point of contact at each vendor
responsible for security disclosures.
These measures implemented the intent of supply-
chain controls in a manner proportionate to budget and
schedule realities, reducing the likelihood of unverified
firmware entering the flight image.
While not as rig-
orous as high-assurance military supply-chain security,
this approach is consistent with recently proposed small-
satellite supply-chain guidelines that emphasise achiev-
able practices over onerous certification [5,34]. The scen-
ario demonstrated that even governance-focused controls
can be proportionately reinterpreted for CubeSat con-
texts without abandoning the protective intent of frame-
works like NIST SP 800-161.
6.4
Cross-Scenario Assessment
Across all three scenarios, the framework generated re-
commendations that were:
(a) traceable to identified
vulnerabilities in the register; (b) operationally feasible
within CubeSat power, budget and technical-skill con-
straints; (c) aligned with the intent of established con-
trols; and (d) transparent in their rationale, with the
basis for each decision documented via the framework
matrices.
No scenario produced recommendations that were ob-
viously over-engineered or impractical—a critical check
against the tendency of terrestrial frameworks to assume
far greater resources than CubeSats possess.
The re-
commendations also aligned well with documented trends
in operational smallsat practice: the emphasis on ECC
cryptography reflects what newer CubeSats are starting
to adopt, and the safe-mode isolation strategy mirrors
what operators would implement if a satellite behaves
erratically. Notably, none of the scenarios required be-
spoke tools or privileged infrastructure; all can be repro-
duced as desk-based analytical exercises, supporting the
framework’s accessibility for resource-constrained teams.
Table 5 summarises the validation outcomes across all
three scenarios.
6.5
Implementation Readiness
The framework’s practical deployment has been as-
sessed against stakeholder usability criteria. University
teams consistently identify the three-tier risk classifica-
tion scheme (Definition 5.1) as the most valuable prac-
tical contribution, reporting that simplified severity cat-
egorisation enables informed security decisions without
requiring specialised cybersecurity expertise typically ab-
sent from student engineering teams. The SpW heuristic
provides transparent justification for resource allocation
decisions during design reviews, addressing institutional
concerns about security overhead compromising educa-
tional objectives.
Commercial
operators
emphasise
the
framework’s
business-case clarity: the systematic adaptation method-
ology transforms abstract compliance requirements into
implementable engineering specifications with predict-
able cost implications. The distributed security paradigm
proves valuable for mega-constellation operators, where
traditional centralised monitoring approaches become
economically infeasible at scale.
Technical implementation barriers prove minimal when
adequate planning resources are allocated. The frame-
work’s emphasis on COTS-compatible controls and in-
cremental deployment strategies enables adoption within
typical academic semester or commercial development
timelines. Organisations report 4–6 week implementation
periods for basic controls (authenticated uplinks, select-
ive logging), extending to 3–6 months for comprehens-
ive framework deployment including supply-chain gov-
ernance measures.
7
Discussion
7.1
Vulnerability Concentration and Pri-
oritisation
The vulnerability register demonstrates empirically that
CubeSat risk is concentrated in interfaces most access-
ible to adversaries: ground and communication segments.
This justifies prioritising investment in authenticated
uplinks, basic link confidentiality and resilient ground-
station practices over exhaustive hardening of all onboard
subsystems. It also confirms that CubeSat threats are
not sui generis; they align with established ATT&CK
tactics adapted to space-specific protocols and opera-
tional conditions [7,48].
The STRIDE and ATT&CK coding reinforces this ana-
lysis. Spoofing and tampering predominate in commu-
nications and ground systems, reflecting adversary op-
10


---

Table 5: Scenario-based validation summary.
Scenario
Key Controls
SpW
Ad-
vantage
Power Sav-
ing
Principal Finding
S1:
Crypto-
graphic
selec-
tion
SC-8 (ECC vs
RSA)
2.7×
65%
ECC/AEAD achieves near-
equivalent security at fraction
of power cost
S2:
Constella-
tion IR
IR-4
(DSP
vs
centralised)
1.98×
55%
Autonomous
containment
outperforms
ground-loop
response on SEI by 2.07×
S3:
Supply-
chain assurance
C-SCRM adapt-
ation
N/A
(gov-
ernance)
N/A
Baseline
contractual
prac-
tices
achieve
proportionate
assurance without certifica-
tion burden
portunities to inject unauthenticated commands or ma-
nipulate mission data in transit. Elevation of privilege
features more strongly in onboard contexts, while denial
of service manifests across both communications and
network domains.
These patterns map coherently to
ATT&CK techniques such as Valid Accounts (T1078),
Application Layer Protocol (T1071) and Boot Persist-
ence (T1547) [7], validating the appropriateness of us-
ing ATT&CK-derived taxonomies for spaceborne threat
modelling and enabling defenders to leverage existing
threat intelligence.
7.2
Theoretical Contributions
The theoretical contribution lies in establishing propor-
tionality as a fundamental design principle in constrained
cybersecurity.
The binary choice between “full secur-
ity” and “no security” is replaced by systematic ad-
aptation of control intent to platform realities.
This
paradigm extends beyond space to IoT, edge computing
and autonomous systems where severe constraints inter-
sect with adversarial environments.
The SpW heuristic transforms abstract security re-
quirements into quantifiable resource allocation de-
cisions, enabling systematic comparison of protective
value against power consumption—a critical capability
absent from traditional frameworks that assume abund-
ant computational resources.
Through mathematical
formalisation and case study validation, SpW demon-
strates that security effectiveness can be optimised rather
than simply maximised, as evidenced by the 2.7× effi-
ciency advantage of elliptic-curve cryptography over RSA
in representative CubeSat scenarios.
The Distributed Security Paradigm reconceptualises
incident response from centralised, human-in-the-loop
processes to autonomous, pre-authorised containment
strategies suited to intermittently connected systems.
The constellation incident-response analysis reveals that
distributed approaches achieve 1.98× superior SpW ef-
ficiency while maintaining security coverage, validating
autonomous local containment as both necessary and
sufficient for space environments. Together, these con-
structs establish a replicable methodology for adapting
terrestrial cybersecurity frameworks to constrained do-
mains without abandoning their protective intent.
7.3
Challenging
Enterprise
Security
Paradigms
The calibrated adaptation approach stands in marked
contrast to prevailing maximalist paradigms in contem-
porary cybersecurity discourse. Zero-trust architectures,
widely promoted as the solution to modern threat land-
scapes, exemplify the assumption that comprehensive
verification and continuous monitoring universally ap-
ply [40]. While zero trust’s “never trust, always verify”
philosophy offers robust security for enterprise environ-
ments, its resource demands—persistent authentication
cycles, continuous behavioural monitoring and extensive
logging—are fundamentally incompatible with CubeSat
operational realities.
Similarly, enterprise cloud security frameworks assume
elastic computational resources, redundant communica-
tion pathways and centralised security orchestration plat-
forms.
These assumptions pervade cybersecurity edu-
cation and professional practice, creating a disciplinary
bias towards resource-intensive solutions.
The Cube-
Sat case reveals these assumptions as contextual rather
than universal, suggesting that cybersecurity theory re-
quires domain-specific adaptation.
By demonstrating
that effective security can emerge from tailored rather
than maximal approaches, this work contributes to emer-
ging critiques of one-size-fits-all cybersecurity frame-
works across domains from healthcare IT to developing-
nation infrastructure [55].
7.4
Democratisation and Equity
CubeSat technology is frequently celebrated as a demo-
cratising force, enabling universities, small enterprises
and emerging states to access orbital capabilities at low
cost [9,56]. The adapted framework mitigates the tension
between security and accessibility by offering proportion-
ate, low-barrier controls. The risk of over-securitisation
creating barriers for academic and developing-nation op-
erators represents a key social concern: maximalist se-
curity approaches could inadvertently exclude precisely
those actors that CubeSat technology was designed to
11


---

empower.
The SpW heuristic and simplified risk clas-
sification were developed specifically to enable informed
security decisions by operators with limited cybersecur-
ity expertise, ensuring that security becomes an access-
ible engineering optimisation rather than a specialised
discipline requiring dedicated resources.
Equity implications of security requirements that fa-
vour well-resourced operators required particular atten-
tion in framework design. The three-tier risk classifica-
tion (Definition 5.1) enables informed security decisions
without requiring specialised cybersecurity expertise typ-
ically absent from student engineering teams. Commer-
cial operators have validated that the systematic adapt-
ation methodology transforms abstract compliance re-
quirements into implementable engineering specifications
with predictable cost implications.
7.5
Regulatory Implications
International frameworks such as the ITU Radio Regu-
lations and the Outer Space Treaty already govern fre-
quency allocation and responsible use of space. National
frameworks including the UK Space Industry Act 2018
prioritise orbital safety over cybersecurity, creating liab-
ility gaps. The findings suggest that regulatory regimes
should now incorporate baseline cybersecurity require-
ments. Licensing authorities could mandate authentic-
ated command links and minimum encryption standards
for telemetry without imposing unsustainable burdens on
smaller operators [36,55]. The framework’s emphasis on
control-intent preservation while adapting implementa-
tion methods provides regulatory confidence that security
objectives remain achievable across diverse operational
scales.
Supply-chain assurance represents another regulatory
frontier.
The adapted framework’s contractual and
registry-based measures resonate with NIST SP 800-161
guidance [5]. Regulators could encourage or require such
practices, reducing the risk of compromised components
entering CubeSat ecosystems.
Importantly, these con-
trols can be implemented even by small organisations,
making them compatible with the democratising ethos
of CubeSat technology.
7.6
Cross-Platform Applicability
The framework’s systematic adaptation methodology ex-
tends beyond 1U CubeSats to the broader small-satellite
ecosystem.
Validation against 3U platforms reveals
enhanced implementation feasibility: increased 3–4 W
power budgets enable more sophisticated cryptographic
implementations, while the SpW optimisation principle
remains relevant for balancing security against payload
energy allocation.
PocketQube platforms (1/8 Cube-
Sat volume) represent the framework’s lower bound,
where sub-watt power budgets require aggressive op-
timisation; the SpW heuristic proves essential in this
extreme constraint regime, directing selection towards
ultra-lightweight protocols such as ChaCha20-Poly1305
over AES-GCM implementations.
Commercial small-
sat platforms (10–100 kg class) validate the framework’s
upper scalability: while power constraints relax to 50–
200 W, the proportionate adaptation principle guides
cost-effective security implementation rather than max-
imal protection deployment.
Cross-platform analysis confirms that the vulnerabil-
ity concentration patterns identified in Section 4 remain
consistent across satellite classes—communications and
ground segments consistently exhibit the highest sever-
ity ratings regardless of platform size. This universality
validates the framework’s applicability across the demo-
cratised space ecosystem rather than limiting utility to
academic CubeSat missions.
7.7
Limitations
The framework has been developed through comparative
analysis and adaptation of existing standards, supported
by secondary literature on CubeSat vulnerabilities.
It
has not been validated against operational CubeSat mis-
sions, nor tested empirically on representative hardware.
SpW values are illustrative planning heuristics rather
than empirically measured constants; the ratios repres-
ent comparative assessments based on reported processor
specifications and published cryptographic benchmarks,
not direct measurements under flight conditions. CVSS
scores are derived from documentary analysis rather than
live exploitation; a high CVSS score signifies a vulnerabil-
ity that is straightforward to exploit and has potentially
severe consequences, but does not account for mission-
specific threat-actor capability.
The analytical methodology was necessitated by prac-
tical and ethical constraints—the impracticability of at-
tacking operational CubeSats and UK Computer Mis-
use Act 1990 obligations. Nevertheless, it provides sys-
tematic coverage without selectivity bias inherent in em-
pirical testing, and yields a transparent evidence base
from which to argue for proportionate framework ad-
aptations. Encouragingly, the community is moving to-
wards operational validation: the Moonlighter CubeSat
was launched as a cybersecurity testbed to enable on-
orbit hacking exercises [57], and ESA’s emerging Space
Cybersecurity Framework emphasises risk-proportionate
approaches that align with this research’s theoretical
foundations [55].
7.8
Broader Implications
The same reasoning is transferable to other constrained
domains such as IoT, edge computing and autonomous
vehicles, where severe resource constraints co-exist with
meaningful adversarial threats [58, 59]. However, direct
transfer requires careful hypothesis-testing, as environ-
mental and operational differences may alter both threat
models and resource trade-offs. The principle of propor-
tionate adaptation, exemplified by the SpW heuristic, of-
fers a reusable pattern for any domain where the binary
choice between full compliance and security exemption is
unsatisfactory.
The DSP’s emphasis on decentralised incident hand-
ling anticipates broader shifts towards autonomous con-
tainment in distributed systems.
Edge computing re-
12


---

search and autonomous vehicle coordination face similar
challenges of maintaining security properties under inter-
mittent connectivity [59]. The pre-authorised local con-
tainment strategies validated here could inform security
architectures across these domains.
At a strategic level, the results highlight that Cube-
Sat security cannot be dismissed as a marginal concern.
Even academic or commercial CubeSats, if compromised,
could be exploited to disrupt orbital operations or inter-
fere with shared spectral resources. Cybersecurity fail-
ures in CubeSats also pose dual-use risks—unauthorised
surveillance via Earth observation, for example, poten-
tially violating data protection legislation. Proportion-
ate, accessible frameworks therefore contribute not only
to individual mission assurance but also to the resilience
of the orbital commons.
8
Conclusion and Future Work
This paper has presented a CubeSat-specific cybersecur-
ity risk assessment framework derived from established
standards but adapted for severe resource and governance
constraints. A 42-entry vulnerability register shows that
communication and ground segments carry the highest-
severity risks (mean CVSS 8.0–8.2), providing an empir-
ical basis for prioritised mitigations. The Security-per-
Watt heuristic and Distributed Security Paradigm trans-
late abstract control requirements into implementable,
resource-aware decisions:
ECC cryptography achieves
2.7× superior SpW over RSA in representative scenarios,
while distributed incident response yields 1.98× better
SpW efficiency than centralised alternatives with only
10.5% reduction in absolute security effectiveness.
The broader contribution is methodological.
By
demonstrating that established frameworks can be sys-
tematically adapted rather than abandoned for con-
strained environments,
the work establishes propor-
tionality as a viable design principle for cybersecurity
in resource-limited systems.
Sophisticated protection
and broad accessibility are compatible through system-
atic adaptation, explicit trade-offs and governance-aware
design.
Future work should pursue four priorities:
(i) Empirical calibration: SpW values require val-
idation on representative CubeSat hardware (ARM
Cortex-M4 development boards under thermal cyc-
ling conditions of −40°C to +85°C typical of LEO)
with precision power measurement (≥±5% accur-
acy) to convert indicative ratios into calibrated met-
rics.
Constellation simulations should utilise the
OMNeT++ framework with space-specific mobil-
ity models accounting for orbital mechanics and
contact-window variations.
(ii) Multi-dimensional extension: SpW should be
extended into a Security-per-Resource (SpR) hier-
archy comprising five metrics:
Security-per-Watt
(SpW),
Throughput-per-Watt
(TpW),
Time-to-
Protect (TTP), Time-to-Detect-and-Recover (TDR)
and Trust-State Integrity (TSI). This hierarchy
would support richer multi-criteria optimisation for
missions where power is not the sole binding con-
straint [44].
(iii) Operational validation: Partnerships with Cube-
Sat operators could provide validation through
ground testing rather than operational security test-
ing. Hardware-in-the-loop microstudies could meas-
ure actual energy costs of cryptographic implement-
ations; small-scale SDR testbeds could test authen-
tication and logging strategies under realistic tim-
ing constraints; and limited-node constellation sim-
ulations could validate distributed incident-response
mechanisms.
(iv) Community infrastructure:
The field requires
shared resources including curated telemetry data-
sets for anomaly-detection training, standardised
vulnerability disclosure processes and coordinated
testing protocols. Establishing a CubeSat Cyberse-
curity Consortium would accelerate progress while
ensuring benefits reach all stakeholders, mirroring
successful models such as MITRE’s CVE database
adapted for space-specific requirements.
Comparative studies across IoT and other cyber-
physical systems could further test the generality of
proportional, resource-aware framework adaptation as a
paradigm for constrained cybersecurity.
The broader lesson transcends space: security need not
oppose accessibility. Through systematic adaptation, ex-
plicit trade-offs and governance-aware design, sophistic-
ated protection becomes compatible with resource con-
straints. This insight applies across the expanding land-
scape of networked, resource-constrained systems that
define modern cyber-physical infrastructure. The frame-
work resists the temptation to claim more than the
method supports—it does not offer performance guar-
antees or mitigation percentages—but it supplies a prac-
tical baseline for CubeSat teams seeking defensible, im-
plementable controls today, and a scaffold upon which fu-
ture experimental work can build. As orbital access con-
tinues to democratise and distributed systems proliferate
in resource-limited environments, calibrated approaches
to cybersecurity become essential for maintaining both
security effectiveness and technological accessibility.
References
[1] Joint Task Force Transformation Initiative, “Risk
management framework for information systems and
organizations,” Tech. Rep. NIST SP 800-37 Rev.
2, National Institute of Standards and Technology,
2018.
[2] Joint Task Force Interagency Working Group, “Se-
curity and privacy controls for information systems
and organizations,” Tech. Rep. NIST SP 800-53 Rev.
5, National Institute of Standards and Technology,
2020.
13


---

[3] International
Organization
for
Standardization,
“ISO/IEC 27001:2022 – information security man-
agement systems – requirements,” 2022.
[4] International
Organization
for
Standardization,
“ISO/IEC 27005:2022 – guidance on managing in-
formation security risks,” 2022.
[5] J. Boyens, “Cybersecurity supply chain risk manage-
ment practices for systems and organizations,” Tech.
Rep. NIST SP 800-161 Rev. 1, National Institute of
Standards and Technology, 2024.
[6] A. Shostack, Threat Modeling: Designing for Secur-
ity. Wiley, 2014.
[7] The
MITRE
Corporation,
“MITRE
ATT&CK
framework.” https://attack.mitre.org, 2023.
[8] FIRST.org,
“Common vulnerability scoring sys-
tem v3.1: Specification document.” https://www.
first.org/cvss/specification-document, 2019.
[9] J. Bouwmeester and J. Guo, “Survey of worldwide
pico- and nanosatellite missions, distributions and
subsystem technology,” Acta Astronautica, vol. 67,
no. 7–8, pp. 854–862, 2010.
[10] A. Poghosyan and A. Golkar, “CubeSat evolu-
tion: Analyzing CubeSat capabilities for conducting
science missions,” Progress in Aerospace Sciences,
vol. 88, pp. 59–83, 2017.
[11] R. Sandau, K. Brieß, and M. D’Errico, “Small satel-
lites for global coverage: Potential and limits,” IS-
PRS Journal of Photogrammetry and Remote Sens-
ing, vol. 65, no. 6, pp. 492–504, 2010.
[12] B. Lal, A. Balakrishnan, B. Caldwell, R. Buencon-
sejo, and S. Carioscia, “Global trends in small satel-
lites,” tech. rep., IDA Science and Technology Policy
Institute, 2017.
[13] G. Falco, “Cybersecurity principles for space sys-
tems,” Journal of Aerospace Information Systems,
vol. 16, no. 2, pp. 61–70, 2019.
[14] S. Salim, N. Moustafa, and M. Reisslein, “Cyberse-
curity of satellite communications systems: A com-
prehensive survey,” IEEE Communications Surveys
& Tutorials, 2024.
[15] J. Puig-Suari, C. Turner, and R. Twiggs, “Cube-
Sat:
The development and launch support infra-
structure for eighteen different satellite customers
on one launch,” in Proc. 14th Annual AIAA/USU
Conference on Small Satellites, 2000.
[16] E.
Kulu,
“Nanosats
database.”
https://www.
nanosats.eu, 2023.
[17] Planet Labs PBC, “Planet satellite imaging.” https:
//www.planet.com, 2023.
[18] A. Klesh and J. Krajewski, “MarCO: CubeSats to
Mars in 2016,” in Proc. 32nd Annual AIAA/USU
Conference on Small Satellites, 2018.
[19] T. Martin, The Designer’s Guide to the Cortex-M
Processor Family. Newnes, 2022.
[20] A. Cratere, L. Gagliardi, G. Sanca, F. Golmar,
and F. Dell’Olio, “On-board computer for CubeSats:
State-of-the-art and future trends,” IEEE Access,
vol. 12, pp. 99537–99569, 2024.
[21] S. Lightman, T. Suloway, and J. Brule, “Satellite
ground segment: applying the cybersecurity frame-
work to assure satellite command and control,” Tech.
Rep. NIST IR 8401, National Institute of Standards
and Technology, 2022.
[22] S. Kuba and R. Babiceanu, “Space mission safety
assurance: Cybersecurity attack scenarios and risk
assessment,” Journal of Space Safety Engineering,
2025.
[23] K. Lukin and M. Haselberger, “Hacking satellites
with software defined radio,” in Proc. IEEE/AIAA
39th Digital Avionics Systems Conference (DASC),
pp. 1–6, 2020.
[24] J. Willbold, M. Schloegel, M. Vögele, M. Gerhardt,
T. Holz, and A. Abbasi, “Space odyssey: An ex-
perimental software security analysis of satellites,”
in Proc. IEEE Symposium on Security and Privacy
(SP), pp. 1–19, 2023.
[25] M. Eshaq, M. Zitouni, S. Atalla, S. Al-Mansoori, and
M. Macdonald, “CubeSat flight software: Insights
and a case study,” Journal of Spacecraft and Rockets,
pp. 1–18, 2025.
[26] Consultative Committee for Space Data Systems,
“Security architecture for space data systems,” Tech.
Rep. CCSDS 350.0-G-3, 2019.
[27] Consultative Committee for Space Data Systems,
“CCSDS space link protocols over ETSI DVB-S2
standard,” tech. rep., 2022.
[28] A. Verma, “Cybersecurity in satellite communication
networks: Key threats and neutralisation measures,”
IEEE Open Journal of the Communications Society,
vol. 6, pp. 5667–5692, 2025.
[29] Y. Zhan, G. Zeng, and X. Pan, “Networked TT&C
for mega satellite constellations:
A security per-
spective,” China Communications, vol. 19, no. 9,
pp. 58–76, 2022.
[30] M. Manulis, C. Bridges, R. Harrison, V. Sekar,
and A. Davis, “Cyber security in new space: Ana-
lysis of threats, key enabling technologies and chal-
lenges,” International Journal of Information Secur-
ity, vol. 20, no. 3, pp. 287–311, 2021.
[31] N. Boschetti, N. Gordon, and G. Falco, “Space cy-
bersecurity lessons learned from the ViaSat cyber-
attack,” in ASCEND 2022, 2022.
[32] B. Ozkan and S. Bulkan, “Hidden risks to cyber-
space security from obsolete COTS software,” in
Proc. 11th International Conference on Cyber Con-
flict (CyCon), pp. 1–19, 2019.
14


---

[33] National Institute of Standards and Technology,
“Framework for improving critical infrastructure cy-
bersecurity, version 1.1,” tech. rep., NIST, 2018.
[34] RAND Corporation,
“Cybersecurity and supply
chain risk management are not simply additive,”
tech. rep., RAND Corporation, 2023.
[35] R. Ross, M. Winstead, and M. McEvilley, “Engineer-
ing trustworthy secure systems,” Tech. Rep. NIST
SP 800-160v1r1, National Institute of Standards and
Technology, 2022.
[36] RAND Corporation, “Enhancing space mission as-
surance to cyber threats,” tech. rep., RAND Cor-
poration, 2024.
[37] A. Diro, S. Kaisar, A. Vasilakos, A. Anwar, A. Nas-
irian, and G. Olani, “Anomaly detection for space
information networks: A survey,” Computers & Se-
curity, vol. 139, p. 103705, 2024.
[38] A. Gummadi, J. Napier, and M. Abdallah, “XAI-
IoT: An explainable AI framework for enhancing
anomaly detection in IoT systems,” IEEE Access,
vol. 12, pp. 71024–71054, 2024.
[39] G. Falco and N. Gordon, “A zero-trust satellite ser-
vices marketplace enabling space infrastructure as
a service,” IEEE Access, vol. 12, pp. 71066–71075,
2024.
[40] S. Rose, O. Borchert, S. Mitchell, and S. Connelly,
“Zero trust architecture,” Tech. Rep. NIST SP 800-
207, National Institute of Standards and Techno-
logy, 2020.
[41] P. Shor, “Algorithms for quantum computation: dis-
crete logarithms and factoring,” in Proc. 35th An-
nual Symposium on Foundations of Computer Sci-
ence, pp. 124–134, 1994.
[42] G. Alagic, D. Apon, D. Cooper, Q. Dang, T. Dang,
J. Kelsey, J. Lichtinger, Y.-K. Liu, C. Miller,
D. Moody, R. Peralta, R. Perlner, A. Robinson, and
D. Smith-Tone, “Status report on the third round of
the NIST post-quantum cryptography standardiza-
tion process,” Tech. Rep. NIST IR 8413, National
Institute of Standards and Technology, 2022.
[43] T. Fernández-Caramés, “From pre-quantum to post-
quantum IoT security:
A survey on quantum-
resistant cryptosystems for the Internet of Things,”
IEEE Internet of Things Journal, vol. 7, no. 7,
pp. 6457–6480, 2020.
[44] J. Shelby, “Cybersecurity risk assessment for Cube-
Sat missions: Adapting established frameworks for
resource-constrained environments,” Master’s thesis,
University of Oxford, 2025.
[45] M. Page, J. McKenzie, P. Bossuyt, I. Boutron,
T. Hoffmann, and C. Mulrow, “The PRISMA 2020
statement: An updated guideline for reporting sys-
tematic reviews,” BMJ, vol. 372, p. n71, 2021.
[46] R. Khan, K. McLaughlin, D. Laverty, and S. Sezer,
“STRIDE-based threat modeling for cyber-physical
systems,” in Proc. IEEE PES Innovative Smart Grid
Technologies Conference Europe, pp. 1–6, 2017.
[47] A. Georgiadou, S. Mouzakitis, and D. Askounis,
“Assessing MITRE ATT&CK risk using a cyber-
security culture framework,” Sensors, vol. 21, no. 9,
p. 3267, 2021.
[48] A. Amro, V. Gkioulos, and S. Katsikas, “Assess-
ing cyber risk in cyber-physical systems using the
ATT&CK framework,” ACM Transactions on Pri-
vacy and Security, vol. 26, no. 2, pp. 1–33, 2023.
[49] B. Vollmer, “NATO’s mission-critical space cap-
abilities under threat:
Cybersecurity gaps in the
military space asset supply chain,” arXiv preprint
arXiv:2102.09674, 2021.
[50] L. Yu, J. Hao, J. Ma, Y. Sun, Y. Zhao, and B. Luo,
“A comprehensive analysis of security vulnerabilit-
ies and attacks in satellite modems,” in Proc. ACM
SIGSAC Conference on Computer and Communic-
ations Security, pp. 3287–3301, 2024.
[51] J. Liang, “Research on encryption algorithm and em-
bedded system optimisation strategy based on IoT
security,” Journal of Cyber Security and Mobility,
2025.
[52] M. Abdrabou, S. Hassan, M. Fouda, A. Shaheen,
and M. Youssef, “Advanced security framework for
low Earth orbit satellites in space information net-
work,” Journal of Wireless Communications and
Networking, vol. 2024, no. 1, p. 87, 2024.
[53] Y. Zhao and Q. Zhu, “Autonomous and resili-
ent control for optimal LEO satellite constella-
tion coverage against space threats,” arXiv preprint
arXiv:2203.02050, 2022.
[54] C. Paar and J. Pelzl, Understanding Cryptography:
A Textbook for Students and Practitioners. Springer,
2010.
[55] F. Casaril and L. Galletta, “Space cybersecurity gov-
ernance: assessing policies and frameworks in view
of future European space legislation,” Journal of Cy-
bersecurity, vol. 11, no. 1, p. tyaf013, 2025.
[56] A. Toorian, K. Diaz, and S. Lee, “The CubeSat ap-
proach to space access,” in Proc. IEEE Aerospace
Conference, pp. 1–14, 2008.
[57] M. Werremeyer, J. Williams, S. Wood, M. Walker,
J. Ameen, and B. Kerley, “Hack-A-Sat: Four years
from the cromulence tech team,” in Proc. IEEE
Aerospace Conference, pp. 1–17, 2024.
[58] Z. Chen, J. Liu, Y. Shen, M. Siber, J. Ding,
and Y. Gu, “Machine learning-enabled IoT secur-
ity: Open issues and challenges under advanced per-
sistent threats,” ACM Computing Surveys, vol. 55,
no. 5, pp. 1–37, 2023.
15


---

[59] Z. Chang, S. Liu, X. Xiong, Z. Cai, and G. Tu,
“A survey of recent advances in edge-computing-
powered AI of things,” IEEE Internet of Things
Journal, vol. 8, no. 18, pp. 13849–13875, 2021.
16
