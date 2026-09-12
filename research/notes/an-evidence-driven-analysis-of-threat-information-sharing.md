---
title: An Evidence-Driven Analysis of Threat Information Sharing
id: an-evidence-driven-analysis-of-threat-information-sharing
tags:
- attack-ontology-drift-cti-85bc51
- pin-rate-survey
created: '2026-09-12T21:35:24.437523Z'
updated: '2026-09-12T21:44:31.748277Z'
source: https://arxiv.org/abs/2512.18714v3
source_domain: arxiv.org
fetched_at: '2026-09-12T21:35:24.437117Z'
fetch_provider: crawl4ai
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'arXiv 2512.18714v3 (2025): uses 102 ATT&CK technique-ID occurrences (without
  sub-techniques); ATT&CK release declaration classified as none.'
raw_file: raw/an-evidence-driven-analysis-of-threat-information-sharing.pdf
doi: arXiv:2512.18714v3
---

An Evidence-Driven Analysis of Threat Information Sharing
Challenges for Industrial Control Systems and Future Directions
Adam Hahn1, Rubin Krief2,3, Daniel Rebori-Carretero1, Rami Puzis2,3, Aviad Elyashar3,4, and Nik Urlaub5
1The MITRE Corporation, McLean, VA, USA
2Department of Software and Information Systems Engineering, Ben-Gurion University of the Negev, Beer-Sheva,
Israel
3Cyber@BGU, Ben-Gurion University of the Negev, Beer-Sheva, Israel
4Department of Computer Science, Shamoon College of Engineering, Beer-Sheva, Israel
5National Renewable Energy Laboratory (NREL)
January 28, 2026
Abstract
The increasing cyber threats to critical infrastructure highlight the importance of private companies
and government agencies in detecting and sharing information about threat activities. Although the
need for improved threat information sharing is widely recognized, various technical and organizational
challenges persist, hindering effective collaboration. In this study, we review the challenges that disturb
the sharing of usable threat information to critical infrastructure operators within the industrial control
system (ICS) domain. We analyze three major incidents: Stuxnet, Industroyer, and Triton. In addition,
we perform a systematic analysis of 196 procedure examples across 79 MITRE ATT&CK® techniques
from 22 ICS-related malware families, utilizing automated natural language processing techniques to
systematically extract and categorize threat observables. Additionally, we investigated nine recent ICS
vulnerability advisories from the Cybersecurity and Infrastructure Security Agency (CISA) Known
Exploitable Vulnerability catalog. Our analysis identified four important limitations in the ICS threat
information sharing ecosystem: (i) the lack of coherent representation of artifacts related to ICS
adversarial techniques in information sharing language standards (e.g., Structured Threat Information
Expression (STIX)); (ii) the dependence on undocumented proprietary technologies; (iii) limited
technical details provided in vulnerability and threat incident reports; and (iv) the accessibility of
technical details for observed adversarial techniques. This study aims to guide the development of
future information-sharing standards, including the enhancement of the cyber-observable objects
schema in STIX, to ensure accurate representation of artifacts specific to ICS environments.
Keywords— Threat information sharing cyber threat intelligence reports ATT&CK techniques STIX
1
Introduction
As critical infrastructure increasingly becomes the target of cyber threats, organizations and governments must be
able to detect and share information about threat actor activity. Numerous government reports, such as Executive
Order 13691 [1] and the Cyberspace Solarium Commission report [2], have highlighted the need for enhanced
information sharing to safeguard critical infrastructure. Additionally, numerous government programs have been
established to facilitate information sharing between the public and private sectors.
Effective information sharing enhances collective situational awareness, enabling quicker responses to emerging
threats, and reducing the risk of widespread disruption. However, realizing these benefits requires not only the
collection and dissemination of threat information but also ensuring that the shared intelligence contains sufficient
technical detail and can be represented in standardized formats that enable operational use by asset owners.
While the need for improved threat information sharing is well-defined, several technical and organizational
challenges persist that hinder effective sharing. Prior work has assessed indicators of compromises (IOCs) in
industrial control system (ICS), but has not reviewed ATT&CK techniques to determine what observables are
required to capture attack behavior.
In this paper, we examine the challenges that hinder the sharing of actionable threat information with asset
owners within the ICS domain. This study leverages the MITRE ATT&CK for ICS [3] knowledge base, which
aggregates cyber threat intelligence reports across known ICS incidents.
1
arXiv:2512.18714v3  [cs.CR]  27 Jan 2026


---

Our paper highlights the key challenges by reviewing three well-known incidents: Stuxnet [4], Industroyer [5],
and Triton [6]. This analysis aims to identify the adversarial techniques employed by threat actors and to determine
the information that asset owners need to implement effective detection mechanisms against these techniques.
We also explore nine recent ICS vulnerability advisories with evidence of exploitation as documented in the
Cybersecurity and Infrastructure Security Agency (CISA) Known Known Exploitable Vulnerability (KEV) Catalog
[7].
To provide a comprehensive assessment beyond these three high-profile incidents, this study extends the
analysis to a systematic examination of 196 procedure examples across 79 techniques from 22 malware families
documented in the MITRE ATT&CK for ICS framework. Using a large language model (LLM) to extract and
categorize threat observables, we analyzed 361 total observables to understand the breadth of representation
and actionability challenges across the entire knowledge base. This comprehensive analysis revealed that only
101 observables had full Structured Threat Information Expression (STIX) observable support, 191 had partial
support, and 69 lacked any STIX representation. Furthermore, only 87 observables contained actionable technical
details sufficient for detection development, while 274 lacked the necessary specificity for operational use.
The primary research questions driving this study are:
1. What are the technical artifacts necessary to detect known ICS adversarial techniques?
Can current
information-sharing standards adequately represent them? (see Section 4.1).
2. To what extent do existing threat reports provide actionable technical details for detection development?
(see Section 4.2.2).
3. To what extent do existing vulnerability advisories provide actionable technical details for detection
development? (see Section 5).
4. What are the main challenges and systemic barriers preventing effective threat information sharing in ICS
environments? (see Section 6).
The outcome of this analysis identifies four important limitations in the ICS threat information sharing
ecosystem that impact the ability of asset owners to effectively use such information. Specifically, this effective
information sharing is limited by (i) the lack of coherent representation of artifacts associated with known ICS
adversarial techniques in information sharing language standards (e.g., STIX), (ii) the reliance on undocumented
and proprietary technologies, especially network protocols without open-source parsers, (iii) the insufficient
technical details provided in vulnerability and threat incident reports, and (iv) the availability of technical details
across all observed adversarial techniques.
This paper intends to inform the development of future information-sharing standards in ICS, including the
expansion of the STIX Cyber-observable Object (SCO) schema. Our study reviews systematically ATT&CK
techniques to determine the necessary indicators or observables that represent adversarial behavior across the full
spectrum of documented ICS incidents. This approach provides both depth through detailed case study analysis
and breadth through a comprehensive systematic assessment of the entire ATT&CK for ICS knowledge base.
2
Related Work
Recent advancements in Cyber Threat Intelligence (CTI) have underscored the complexities of securing ICS and
broader Cyber-Physical Systems (CPSs), particularly in the context of critical infrastructure. ICSs and CPSs
often rely on proprietary and specialized protocols that are difficult to monitor and integrate with conventional
cybersecurity tools. Krasznay et al. [8] highlighted the critical vulnerabilities in these systems, which stem from
their original design priorities focused on safety rather than cybersecurity. The increasing connectivity of ICS and
Operational Technology (OT) systems has exposed these vulnerabilities to sophisticated adversaries, including
state-sponsored actors, necessitating a paradigm shift in cybersecurity practices. The SeConSys initiative in
Hungary represents a significant milestone in addressing these challenges. This initiative facilitates sector-specific
threat intelligence sharing and detection through the development of tailored CTI feeds, honeypots that simulate
energy-sector environments, and the implementation of the Network and Information Systems (NIS) Directive.
These efforts have been instrumental in promoting localized, collaborative approaches to cybersecurity and
advancing frameworks for real-time threat information sharing among key stakeholders in the energy sector.
López-Morales et al. [9] extended these contributions by developing innovative methodologies that advance the
state-of-the-art in CTI for CPSs. Their work introduces the ICS2 Matrix, an enhanced version of the MITRE
ATT&CK framework tailored specifically to ICSs. The ICS2 Matrix incorporates novel attack techniques and
mitigation strategies derived from an extensive analysis of Programmable Logic Controller (PLC)-related security
research spanning 17 years. Additionally, the development of a high-interaction satellite honeypot provides a
groundbreaking tool for simulating realistic adversary interactions, collecting data on emerging threats, and
advancing the understanding of satellite-specific attack vectors. This work further proposes the creation of a
sandbox environment for connected autonomous vehicles, enabling the simulation and analysis of cyberattacks on
autonomous systems to improve resilience. Such contributions underscore the necessity of domain-specific CTI
methodologies that address the unique operational and security challenges inherent in different CPSs.
2


---

2.1
Empirical Measurements and Quality Assessment of CTI Sharing
At the ecosystem level, empirical studies have begun to quantify the effectiveness and challenges of CTI sharing at
scale. Jin et al. [10] provided one of the first comprehensive empirical measurements of CTI sharing effectiveness,
analyzing STIX volume, timeliness, coverage, and quality across public sources. Their findings reveal significant
variations in feed quality and highlight the challenges that organizations encounter while operating in a shared
intelligence environment. This empirical foundation complements broader systematic reviews that examine how
organizations actually use CTI for security decision-making [11] and identify persistent barriers to effective CTI
sharing, including governance issues, misaligned incentives, and insufficient standardization [12].
Quality and trust of shared feeds remain persistent issues across the CTI ecosystem. Griffioen et al. [13]
conducted systematic quality evaluations of cyber threat intelligence feeds, revealing inconsistent timeliness and
specificity that can undermine the operational value of shared intelligence. Similarly, Schaberreiter et al. [14]
developed quantitative frameworks for evaluating trust in CTI quality, demonstrating that trust and quality
metrics vary significantly across different sources and feed types. Together, these studies highlight the need for
more rigorous quality assurance mechanisms in CTI sharing initiatives.
2.2
Standardization and Technical Implementation
Standardization efforts play a crucial role in making threat observables portable and actionable across different
organizational contexts. STIX 2.1, approved as an OASIS Standard (on 10 June 2021), serves as the exchange
format used across many CTI producers and consumers [15]. However, challenges remain in effectively representing
complex ICS-specific artifacts within existing STIX objects. Zych and Mavroeidis [16] have proposed enhancements
to MITRE ATT&CK representations by STIX, to improve filtering and prioritization tasks, while RFC 9424 [17]
provides important clarification on the capabilities and limitations of IOCs, reinforcing the value of higher-fidelity
observables for creating durable detection capabilities.
Recent advances in natural language processing have introduced new approaches for extracting threat intelligence
from unstructured reports. While some pipelines pursue full STIX coverage through classical NLP techniques
combined with external knowledge bases [18], alternative approaches rely on large language models to extract
observables directly from text without requiring extensive knowledge graphs. These automated extraction techniques
show promise for scaling CTI processing, though systematic evaluation reveals significant limitations and failure
modes. Alam et al. [19] developed CTIBench, a comprehensive benchmark specifically designed to evaluate
LLM performance in cyber threat intelligence tasks across multiple cognitive dimensions, including memorization,
understanding, problem-solving, and reasoning. Their evaluation of five state-of-the-art models revealed concerning
patterns: all models struggled significantly with tasks requiring domain expertise, with even the best-performing
model (GPT-4) achieving only 71% accuracy on foundational CTI knowledge questions. More critically, their
analysis identified systematic failure modes, including overestimation of threat severity scores, difficulty with
out-of-knowledge cutoff information, and particularly poor performance on questions related to mitigation strategies
and adversarial tools. These findings highlight substantial gaps in LLM reliability for cybersecurity applications.
Fieblinger et al. [20] developed a comprehensive methodology for automating the extraction of actionable CTI
using LLMs for generating Knowledge Graphs. Their approach systematically evaluates multiple open-source
LLMs (including Llama 2 series, Mistral 7B Instruct, and Zephyr) across different extraction techniques, such
as few-shot prompt engineering, guidance frameworks, and fine-tuning to optimize the extraction of meaningful
triples from CTI texts. Notably, their methodology demonstrates that guidance frameworks significantly improve
extraction performance beyond what is achievable with prompt engineering alone, while fine-tuning proves essential
for extracting triples that adhere to specified ontologies. The extracted triples are subsequently used to construct
knowledge graphs that provide structured, queryable representations of threat intelligence, facilitating downstream
applications such as link prediction and threat analysis.
The development of domain-specific evaluation datasets has become increasingly important for assessing auto-
mated threat intelligence processing. Bhusal et al. [21] developed the SECURE benchmark using MITRE ATT&CK
as a foundation for generating cybersecurity LLM performance evaluation across extraction, understanding, and
reasoning tasks. Their approach demonstrates the potential of leveraging structured threat intelligence frameworks
like ATT&CK for creating systematic evaluation datasets. However, the reliability of LLM-based approaches in
cybersecurity contexts remains a critical concern. Their comprehensive evaluation of seven state-of-the-art models
revealed significant limitations, including hallucinations when models lack current information, difficulty with
out-of-distribution detection, and substantial performance variations across different cybersecurity task types. Im-
portantly, their findings demonstrate that while LLMs show promise for cybersecurity advisory roles, closed-source
models consistently outperform open-source alternatives, particularly in problem-solving and out-of-distribution
scenarios. These results underscore the importance of meticulous validation and human oversight when deploying
LLMs for threat intelligence processing, particularly in critical infrastructure environments where inaccurate
information can have severe consequences.
ATT&CK Framework Application in OT Environments.
For technique-level grounding in OT envi-
ronments, the MITRE ATT&CK framework and its ICS extension provide structured approaches to understanding
adversary behaviors [22, 23]. Afenu et al. [24] have leveraged ATT&CK to validate ICS defense mechanisms and
3


---

testbed implementations. Choi et al. [25] generated realistic OT attack sequences based on analysis of real-world
datasets. These applications demonstrate the framework’s utility in bridging the gap between theoretical threat
models and practical security implementations.
D3FEND Framework Extension for OT Environments.
Recently, MITRE extended its D3FENDT M[26]
cybersecurity ontology to OT, creating a structured knowledge base for defending cyber-physical systems, including
new artifacts, such as controllers, sensors, and physical process actuators. Yet, their additional new artifacts and
techniques do not fundamentally resolve the ontological issues in D3FEND’s core modeling approach, which were
raised back in 2023 by Oliveira et al. [27], such as missing concepts, semantic overload, and a systematic lack of
constraints that make the model under-specified. D3FEND can be integrated into Cyber Threat Intelligence (CTI)
exchange processes, but it does not fit the exchange formats natively in the same way MITRE ATT&CK does, as
it is an ontology for defensive techniques, not a data exchange format in and of itself. While ATT&CK is widely
supported by CTI exchange standards like STIX, D3FEND lacks native support for these formats for primary CTI
exchange.
The existing literature highlights several recurring challenges in CTI, including limited interoperability of
detection tools, insufficient standardization of threat-sharing protocols, and a lack of actionable intelligence for
specific adversarial behaviors. While Krasznay et al. [8] emphasized the importance of legislative and collaborative
frameworks, López-Morales et al. [9] focused on advancing technical methodologies to enhance the granularity and
applicability of CTI. Both approaches converge on the need for tailored threat intelligence that integrates
sector-specific requirements into practical and effective security solutions. Building on these foundational works,
this study aims to address critical gaps in the ICS threat information-sharing ecosystem. Our research specifically
focuses on expanding the cyber observable objects schema within the STIX standard to ensure the accurate
representation of ICS-specific artifacts and adversarial techniques. Unlike prior studies that primarily
concentrated on domain-specific or geographically localized advancements, this work seeks to generalize CTI
enhancements across diverse ICS environments. By integrating detailed technical insights into standardized
threat-sharing protocols, this study aspires to bridge the gap between theoretical threat models and actionable
intelligence, thereby facilitating more effective collaboration and situational awareness across ICS stakeholders.
3
Key Roles and Functions in Sharing Threat/Vulnerability In-
formation
This section provides a brief overview of the ICS information sharing ecosystem, including key organizations,
information flows, artifacts, and systems that support the sharing of threat and vulnerability information.
Specifically, we focus on the needs of the asset owners who rely on this information to support security operations
and detection efforts (see Figure 1).
Figure 1: Overview of Threat/Vulnerability Information Sharing Roles and Technical Capabilities. Solid
boxes represent stakeholders. Dashed boxes represent components. Solid arrows represent common
existing information flows.
Typically, governments facilitate information sharing by providing reports with threat or vulnerability in-
formation to critical infrastructures and other organizations [28]. The National Cyber Emergency Response
Teams (CERT) is an important information-sharing hub, as it has unique access to threat information through
the facilitation of information-sharing programs with both federal, defense, and intelligence agencies, as well as
partnerships with private sector organizations.
Security vendors provide tools/platforms and information to support the detection and mitigation of cyber
threats [29, 30]. Many of these vendors search for vulnerabilities and threat actor activity to develop analytics or
rules to be incorporated into detection tools. Some vendors provide machine-readable threat information feeds,
4


---

which can be directly consumed by security products, including those used to monitor for cyber threats. Further,
many vendors obtain data from their detection infrastructures deployed at asset owner sites or collect information
while supporting incident response efforts.
ICS vendors typically support information sharing efforts through the disclosure of security advisories and
patches when a vulnerability is discovered in their software or devices [31]. Most importantly, ICS vendors have
unique knowledge regarding the technical details for their products, which are typically based on proprietary
technology.
Asset owners are responsible for managing the risk presented by the cyber threats. The larger organizations
that maintain critical infrastructures typically have dedicated security operations teams, the smaller commercial
asset owners commonly rely on their national CERT [32]. They may have a person partially employed in security
operations to comply with regulations. The security team of an asset owner is responsible for monitoring their
systems for threats and reporting to their auditors or the CERT.
Security operations teams depend on several different security products to support this, including detection
platforms that monitor ICS devices and networks for threat activities based on various detection rules and analytics.
The security operations teams depend on governments, ICS vendors, and security vendors to provide information
about a range of vulnerabilities and threats.
In addition to the previously identified organizations, other entities contribute to information-sharing capabilities.
For example, various organizations have provided open-source tools to parse network traffic, extract security-related
data, and apply analytics to detect adversary behaviors shared with the organizations. Examples of key open-source
efforts supporting the dissemination and detection of threat behaviors are included below.
• Standardized threat information languages: One key contribution to make threat information sharing more
effective is the development of standard languages. For example, STIX standard provides a JSON format to
communicate threat behaviors. This includes definitions of SCOs [15] for specific types of artifacts that can
be used to detect malicious activities or collect information about them. Other formats include OpenIOC1
and MISP XML2.
• Detection Rules/Analytics: Various security vendors provide rules or analytics that can be integrated within
a detection platform to enable the automated detection of specific behaviors. While many commercial
detection platforms consume their own proprietary feed of detection rules or analytics, others rely on
open-source formats. Examples include the NSA ELITEWOLF3 and CISA ATT&CK-based Control-system
Indicator Detection (ACID),4 and various repositories of YARA rules.
• ICS Protocol Parsers: Many detection platforms lack inherent support for ICS protocols; therefore, dedicated
parsers for ICS protocols have been developed to enable the monitoring of ICS networks. Programs like
CISA’s Industrial Control Systems Network Protocol Parsers5 have defined several parsers for key ICS
protocols for Zeek, while Cisco Talos has also now identified Snort inspectors for specific ICS protocols.6
Requirements for Threat Detection: To ensure an asset owner can detect a specific threat behavior, they
must either (i) obtain a detection rule or analytic to support that detection, or (ii) develop a detection based on
known technical data about that threat and the associated technology it targets. Accordingly, the following two
requirements are defined to support the analysis of information sharing effectiveness and identify associated gaps.
• Requirement #1 - The information should include a detection rule/analytics or structured cyber observables
that could be directly integrated within a detection platform.
• Requirement #2 - The information should include sufficient technical details to enable the development of a
detection rule/analytic. However, to ensure the end-user has sufficient information to establish a detection,
the following additional sub-requirements must be met:
a) Technical details about the threat activity, including the adversarial technique used, and the specific
artifacts manipulated during the threat activity.
b) A thorough understanding of the underlying technology and protocols targeted by the threat is required
to develop an effective detection.
This is particularly relevant when a threat targets a vendor’s
proprietary technology, especially if the technology is not adequately documented. Developing detectors
for undocumented third-party technologies is a laborious and unreliable task.
4
Threat Information Sharing Analysis
This section reviews the procedure examples defined in MITRE ATT&CK for ICS associated with the Stuxnet,
Industroyer, and Triton events. While the ATT&CK for ICS does not represent any single threat report, the
1https://www.scribd.com/document/653654203/An-Introduction-to-OpenIOC
2https://www.misp-project.org/
3https://github.com/nsacyber/ELITEWOLF
4https://github.com/cisagov/ACID
5https://github.com/cisagov/ICSNPP
6https://blog.talosintelligence.com/ics-protocol-coverage-snort-3/
5


---

procedure examples are based on information extracted from reports and provide an aggregate view of the available
information about that event from numerous sources. Each procedure example from these three events was
reviewed to extract/synthesize and document the data or technical artifacts that can be used to detect the activity.
The key criteria reviewed for each procedure example are defined below.
• Data Source (1): Each technique within the ATT&CK knowledge base is mapped to a set of Data Sources
that could potentially be used to detect that activity.7 This specifies what ATT&CK for ICS data source
would have been most effective in detecting this procedure example.
• Supporting Artifacts (2): This more precisely defines the technical artifact that would support the detection.
This identifies the specific information that needs to be shared to enable the receiving party to detect
the same threat/procedure example on their network. Supporting artifacts are not explicitly defined in
ATT&CK, but they can often be derived from the procedure descriptions.
• STIX Observable Supported (3): This evaluates whether the artifacts needed to detect that threat are
documented as SCO. This is important because unless an artifact is documented by STIX, it cannot be
formally communicated through STIX-based threat intelligence reports. These will be categorized into
the following three types. While an artifact could have multiple possible STIX observable mappings, this
example only illustrates one possible mapping that supports its associated categorization.
– No Support: STIX lacks a relevant observable object that could correctly represent the identified
artifact, thereby limiting the sharing of an observable.
– Partial Support: STIX has an observable that could represent this artifact, but the observable does
not fully encompass the semantics of the artifact, or the observable does not define significant fields
to completely represent it. The partial nature implies ambiguity in the representation of observable
artifacts, which in turn may yield unreliable detections or only support a limited set of aspects of
the behavior. For example, a network traffic object may be used to represent an ICS command,
with the protocol field representing the relevant ICS protocol (e.g., Supervisory Control and Data
Acquisition (SCADA)) but missing specific support to represent the command itself.
– Full Support: An existing STIX observable is fully capable of documenting this artifact, thereby
enabling the creation of robust detection for the behavior.
• Artifact Detailedness level (4): This specifies whether the information necessary to detect this specific threat
behavior is available from the threat intelligence. This criterion is not intended to provide criticisms of the
specific reports. Rather, it is intended to help identify whether information necessary to detect the threat is
consistently available, or whether broader challenges exist in collecting the technical artifact that inhibit its
sharing. For example, prior victims may be lacking adequate detection infrastructure or forensic capabilities
to collect the evidence. These will be categorized into the following four types:
– Missing: The procedure description does not mention the identified artifact nor any details about it.
– Mentioned: The artifact was mentioned in the procedure description, but not addressed.
– Described: Notable specific or distinguishing details about the artifact are described in the procedure
description, but without sufficient unique information that would allow detecting it. These kinds of
artifacts are non-searchable.
– Actionable: The artifact is fully described in the procedure description with unique and specific
information, in a way that a detection rule can be formed to match it with low false positives. These
artifacts are searchable and can drive an automated response; they can be operated immediately or
after a simple transform.
• Proprietary artifacts (5): This identifies whether the artifact requires the understanding of some proprietary
technology developed by a vendor/OEM, or whether that artifact is based on open/public standards or
technologies. For example, many network protocols used by ICS devices lack public documentation of
their functionality, while devices may contain proprietary logs or files with complex structures and content.
Developing detections based on proprietary artifacts presents significant difficulty, as organizations often lack
sufficient information on how to properly collect, parse, or analyze that data. These artifacts are categorized
as follows:
– Open/Standard Technology: These are technologies/protocols with publicly accessible documentation
or are defined within an industry standard.
– Proprietary - Documented Technology: These are also technologies/protocols developed and owned by
a specific organization or company; however, in these cases, the documentation is publicly available. It
is worth noting that such protocols often include undocumented features that may be relevant to the
behavior of threat actors.
7https://attack.mitre.org/datasources/
6


---

– Proprietary - Undocumented Technology: These are technologies/protocols developed and owned by a
specific organization or company. This refers to protocols for which documents are not available. The
organization or company likely has internal documents, but they are not shared publicly. Proprietary
but undocumented technologies can limit an organization’s ability to collect and analyze the data
necessary to perform various security functions.
• Protocol Parsers (6): If the artifact and associated data source include the detection of a network protocol,
this identifies whether there are publicly available parsers for that protocol.
4.1
Deep Dive into Threat Information of Three Major Attacks
In this section, we review the procedure examples of Triton, Stuxnet, and Industroyer from the MITRE ATT&CK
for ICS according to the criteria defined in the previous section.
4.1.1
Triton
The Triton malware [33], also known as TRISIS or HatMan, targeted safety instrumented systems within an
oil refinery by manipulating both an engineering workstation and the Triconex safety controllers used in the
sulfur recovery units and burn management systems. While the broader campaign during this attack included
activities used to gain access to the facility (references as TEMP.Veles in ATT&CK), the defined Tactics,
Techniques and Proceduress (TTPs) specific to the ICS environment primarily address the behaviors associated
with the manipulation of Windows-based engineering workstations, safety controllers, and the associated network
communications between them. The following sections will review the adversary activity associated with these
three areas based on the previously defined criteria.
TriStation Workstation (Table 1): The Triton malware initially targeted the engineering workstation and
associated TriStation software running on that device. The malware included a Python program that was compiled
into an EXE, but which included a file name that masquerades as the authentic TriStation executable [T0849].
The malware then used the same Application Programming Interface (API) that TriStation uses to communicate
with and manage the Triconex devices to access those devices [T0834]. Because the workstation is a traditional
Windows-based platform, both of these techniques could be determined by reviewing files matching the hash of
the EXE file, leveraging the STIX File: Hash object. This hash value was provided in the threat intelligence
reports, and the Windows-based functionality is well-documented. However, detecting the malicious API uses
likely depends on the runtime analysis of the specific system calls used by the TriStation workstations, which are
not specified in any documentation, and there is no available STIX object to represent these system calls.
Table 1: Analysis of Triton Software TriStation Workstation Activity.
Tech.
1-Data Source
2-Artifact
3-STIX
4-Artifact
Detailed-
ness
5-Proprietary
6-Parser
T0849
File-
Metadata
File hash of exe
Full
-
File:hashes
Actionable
Proprietary
-
Documented
NA
-
host
T0853
Command/
Process
File hash of exe
Full
-
File:hashes
Actionable
T0871
Process
-
Operating
System (OS)
API Exec
TriStation API
calls
No
Actionable
Proprietary
-
Undocumented
TriStation Protocol (Table 2): The TriStation protocol, which is a proprietary protocol without any available
open-source parsers, was heavily used throughout the attack. The adversarial techniques using this protocol
include discovering target devices [T0846], detecting and changing their operating mode [T0858] [T0868],
downloading programs to the targeted safety controller [T0843], executing the program [T0871], and extracting
programs from the device [T0845]. Developing detections for this activity requires the ability to (i) understand
and parse the TriStation protocol [34], (ii) identify specific functions of the protocol, and (iii) represent function
payloads (e.g., program downloads contents). The STIX Network Traffic observable could be used to represent
this activity, specifically the src/dst_payload_ref objects, which reference specific strings within the protocol
payloads. However, using the src/dst_payload_ref STIX objects for the TriStation protocols techniques, any
detection utilizing these objects is likely to be fragile.
7


---

Table 2: Analysis of Triton Software TriStation Protocol Activity.
Tech.
1-Data Source
2-Artifact
3-STIX
4-Artifact
Detailed-
ness
5-Proprietary
6-Parser
T0846
Network Traf-
fic Content
Parsing of TriS-
tation Protocol –
Device discovery
Partial
–
Network
Traffic
src/
dst_payload_
ref
Described
Proprietary
-
Undocumented
No
T0858
-
Operating
mode changes
T0868
-
Operating
mode status
T0843
- Program down-
loads/appends
T0845
- Program up-
loads
T0885
Custom
mal-
ware C2 payload
Actionable
NA
NA
Triconex (Table 3): Triton’s targeting of the Triconex safety controller required multiple adversary techniques
used to manipulate devices that execute custom logic. Once the malicious program was downloaded to the device,
it was executed on the device [T0821]. Then, the malware gained excessive privileges by executing a vulnerable
system call on the device [T0890], and manipulated the running firmware of the device [T0857] to maintain an
implant. Next, it enabled Command and Control (C2) [T0869] by manipulating a protocol handler to link to
malicious code injected into the device [T0874]. Detecting this activity requires the ability to extract and audit
programs on the device, such as through program upload functions or integrity checks. This could potentially be
detected by the Process: Hash STIX object, while many devices produce CRC’s or checksums of deployed
programs, these could be easily converted to a hash to support this object type. These Cyclic Redundancy
Checks (CRCs) within the Triconex devices are a proprietary but documented function [35]. Most of these other
Triconex behaviors are difficult to detect because they manipulate the device’s run-time memory, which depends
on the undocumented and proprietary operation of the device. Detecting the exploitation of a vulnerable system
call typically requires a runtime agent running on the device, while detecting the runtime manipulation in the
underlying firmware requires mechanisms that perform integrity checks of a device’s OS and runtime
environments. Therefore, these specific techniques likely cannot be detected through traditional detection
platforms and STIX based information sharing.
Table 3: Analysis of Triton Software Triconex Activity.
Tech.
1-Data Source
2-Artifact
3-STIX
4-Artifact
Detailed-
ness
5-Proprietary
6-Parser
T0821
Asset
Soft-
ware
PLC
program
CRC
Partial
–
Process:
Hash
Actionable
Proprietary
-
Documented
NA
-
host
T0890
Process - OS
API Exec
OS API calls
No
Described
Proprietary
-
Undocumented
T0834
T0857
Firmware
FW/Memory
Contents
Partial
–
Process:
Hash
T0874
4.1.2
Stuxnet
The Stuxnet malware targeted Siemens PLCs used to support uranium enrichment cascades. The malware targeted
both the PLCs, by manipulating the application program deployed on the device, and the engineering software
8


---

deployed on the workstation (WinCC). Therefore, the associated TTPs then heavily focuses on the manipulation
of the PLC, the software on the engineering workstation, and their associated network communications. Tables
4-6 enumerate each adversarial technique defined within ATT&CK for ICS associated with the Stuxnet malware.
SIMATIC WinCC Workstation (Table 4): The malware was initially deployed to engineering workstations
using the SIMATIC WinCC software using either hard-coded credentials [T0891] or by copying itself to connected
USB drives [T0847]. The hard-coded credential used could have been represented by the STIX User Account:
Credential observable to enable sharing this information. The malware also propagates by modifying the content
of SIMATIC Step 78 project files found on the device by searching for files with the appropriate Step 7 format
[T0873]. The modified project files could be detected by sharing the malicious contents or by representing the
overall hashes of the activity, either through the STIX File: String or File: Hash observable.
Then, the malware installs a malicious dynamic-link library (DLL) which masquerades as an authentic file [T0849],
the hash of this file could be represented by the File: Hash STIX observable. This DLL further injects any project
files loaded [T0863]. The malicious DLL identifies targets by reviewing the contents of incoming data blocks to
identify specific devices [T0888]. The DLL then downloads code to the PLC [T0843] and manipulates data sent
between the PLC and workstation [T0851]. Since these activities all require understanding the execution of DLL,
detecting this activity would require an understanding of specific function calls both within the DLL and OS
system calls. However, as previously stated, STIX currently lacks support for this.
Table 4: Analysis of Stuxnet WinCC Workstation Activity.
Tech.
1-Data Source
2-Artifact
3-STIX
4-Artifact
Detailed-
ness
5-Proprietary
6-Parser
T0891
Logon Session
- Metadata
SQL
Server
password
Full – User
Acct: Cred
Actionable
Proprietary
-
Documented
NA
-
host
T0847
File - Meta-
data
Malicious
file
names
Full – File:
Name
Actionable
Proprietary
-
Documented
NA
-
host
T0873
File - Meta-
data
PLC
Project
Files
Full – File:
String/Hash
Described
Proprietary
-
Documented
NA
-
host
T0849
File - Meta-
data
DLL hash
Full – File:
String/Hash
Actionable
Proprietary
-
Documented
NA
-
host
T0863
Command Ex-
ecution / Pro-
cess Creation
Command name
Full - File:
Name
Described
Proprietary
-
Documented
NA
-
host
T0874
Process – OS
API Exec
OS API calls
No
Mentioned
Proprietary
-
Documented
NA
-
host
T0888
T0851
Network Activity (Table 5): Stuxnet used a wide array of network activity to both propagate malware across
devices and also to manipulate the control of the operational process. The malware utilized various SQL
server-stored procedures to transfer files and execute malware [T0886], including transferring the Stuxnet DLL to
other systems [T0867] and executing the malware [T0866]. This would require monitoring the SQL Server protocol
for the execution of those specific stored procedures. This could be potentially shared by using the STIX Network
Traffic: src/dst_payload_ref observable; however, it is unclear whether the SQL protocols could be effectively
represented by payload strings. Then, the malware attempts to establish a C2 connection to external servers
[T0885] over port 80, which could have been shared using the STIX Network Traffic: dst_port observable.
The Siemens S7Comm protocol was used to perform program downloads from the WinCC workstation to the
PLCs [T0843]. Once the malicious code was deployed to the PLC, it then sends Profibus messages to frequency
converter drives [T0836]. While Profibus is an International Electrotechnical Commission (IEC) standard,
S7Comm (Siemens) is a proprietary protocol, though both have publicly available parsers. These activities would
also likely need to be shared using the STIX Network Traffic: src/dst_payload_ref observable, though it is
unclear whether these behaviors could be effectively shared using it.
8https://www.siemens.com/global/en/products/automation/industry-software/automation-software/tia-
portal/software/step7-tia-portal.html
9


---

Table 5: Analysis of Stuxnet Network Activity.
Tech.
1-Data Source
2-Artifact
3-STIX
4-Artifact
Detailed-
ness
5-Proprietary
6-Parser
T0866
Network Traf-
fic Content
SQL
Strings/
Protocol Parser
Partial
–
Network
Traffic:
src/
dst_payload_
ref
Actionable
Proprietary
-
Documented
Yes
T0867
T0885
Network
Traffic
Con-
nection
Connection
to
Port 80
Full
–
Net-
work
Traffic:
dst _port
Mentioned
Proprietary
-
Documented
NA
T0843
Network Traf-
fic Content
Parsing
of
S7Comm
Pro-
tocol Functions:
Program Down-
loads/Appends
Partial
–
Network
Traffic:
src/
dst_payload_
ref
Missing
Proprietary
-
Undocumented
Yes
T0836
Network Traf-
fic Content
Profibus
Net-
work Traffic
Partial
–
Network
Traffic:
src/
dst_payload_
ref
Described
Open
/
Stan-
dard
No
Siemens PLCs (Table 6): The malware deploys malicious programs by manipulating controller tasking (e.g.,
OB1, OB35) [T0851][T0821] on the PLCs. The manipulation of controller tasking and programs can be detected
by either performing program uploads or performing integrity checks. These could be partially represented by
File: Hash STIX observables, since many PLC application programs are frequently represented by other message
digest mechanisms, such as PLCs or checksums. This malicious program then performs a number of additional
techniques on the PLCs, including sniffing Profibus message contents [T0842] and monitoring the state of the
operational process [T0801] and calls an existing system function block used by the device [T0834]. The program
collects data from the I/O image [T0877] and then intercept/overwrite peripheral output to prevent detection
[T0835]. These could either be detected through some sort of run-time analysis, by verifying the specific OS API
calls made, or by extracting and performing an analysis of the malicious program performed on the device. The
former would depend on the device’s ability to perform run-time monitoring of device functions; this capability is
typically not supported by PLCs. Since most PLCs do support application program uploads, the specific PLC
API calls can be analyzed to observe this behavior. Unfortunately, this presents a clear gap in STIX, as there is
currently no way to reference specific PLC application logic functions.
10


---

Table 6: Analysis of Stuxnet PLC Activity.
Tech.
1-Data Source
2-Artifact
3-STIX
4-Artifact
Detailed-
ness
5-Proprietary
6-Parser
T0821
Asset – Software
PLC code
Partial
–
File: Hash
Described
Proprietary
-
Documented
NA
-
Host
T0842
Asset – Software /
Process – OS API
Exec
PLC
OS
API calls
No
Described
Proprietary
-
Documented
NA
-
Host
T0801
Asset – Software /
Process – OS API
Exec
PLC
OS
API calls
T0869
Asset – Software /
Process – OS API
Exec
PLC
OS
API calls
Actionable
T0834
Asset – Software /
Process – OS API
Exec
PLC
OS
API calls
Described
T0877
Asset – Software /
Process – OS API
Exec
PLC
OS
API calls
Actionable
T0835
Asset – Software /
Process – OS API
Exec
PLC
OS
API calls
Described
4.1.3
Industroyer
The Industroyer or CrashOverride malware was used as part of an attack that occurred in December 2016, targeting
Ukraine’s power grid and causing a blackout in the northern part of the capital, Kyiv. It was capable of operating a
substation’s switches and circuit breakers, utilizing several common industrial communication protocols, including
IEC 60870-5-101, IEC 60870-5-104, IEC 61850, and OPC DA. Additionally, this malware features a built-in "wiper"
module that can erase the configuration files for the equipment controlling the circuit breakers, making recovery
more challenging.
Windows Activity (Table 7): The malware launcher is initially executed as a .dll through a command
line parameter [T0807], and multiple other modules were also executed as .dlls. This could be represented as a
STIX File Name object, while the initial launcher .dll name is not included in the report, the associated wiper
.dlls are provided. The malware then enumerates systems call on the system, which requires executing Windows
system calls [T0840]. Furthermore, the malware connects to COM ports on the Windows system, which involves
executing Windows system calls. However, neither of these system-call-focused artifacts can be represented by
STIX observables [T0803] [T0804] [T0805]. Later, the malware executes a wiper that disables system services and
wipes files on the device. While the specific system calls used to perform this are not defined, there are likely a
limited set of Windows calls that enable this. Furthermore, STIX lacks an observable to represent system calls
used to understand runtime malware functions.
11


---

Table 7: Analysis of Industroyer Windows Activity.
Tech.
1-Data Source
2-Artifact
3-STIX
4-Artifact
Detailed-
ness
5-Proprietary
6-Parser
T0807
Command Ex-
ecution
CMD line parame-
ter w/ DLL
Full – File:
Name
Actionable
Proprietary
-
Documented
NA
-
Host
T0881
Service
-
Metadata
/
Process – OS
API Exec
OS API call asso-
ciated with service
stop
No
Actionable
Proprietary
-
Documented
NA
-
Host
T0809
Process – OS
API Exec
OS API calls asso-
ciated with wiper
functions
No
Actionable
Proprietary
-
Documented
NA
-
Host
T0840
Process – OS
API Exec
OS API calls as-
sociated with net-
work enumeration
No
Actionable
Proprietary
-
Documented
NA
-
Host
T0803
Process – OS
API Exec
System Calls for
COM Ports
No
Mentioned
Proprietary
-
Documented
NA
-
Host
T0804
T0805
Network Activity (Table 8): The first network-focused activity is the establishment of a proxy through
port 3128 [T0884], which can be represented by the STIX Network Traffic src/dest_port observable. Then, the
malware has a broad set of behaviors that utilize a set of automation protocols to interact with substation devices,
including supporting remote discovery, collection, monitoring, and sending unauthorized command messages.
At least two protocols, OPC and 61850 leveraged discover functions within the protocols to identify devices
supporting those protocols [T0846]. Then, several protocol functions were utilized to collect and monitor the status
of devices using the 61850, OPC, and IEC 104 protocols [T0888][T0801]. The unauthorized command messages
were used to manipulate the operation of devices, specifically to open/close breakers [T0855][T0806]. While none
of these protocols have specific representation in STIX, they could be partially represented by the Net Traffic
src/dst_payload_ref object. Fortunately, these are all open or standards-based protocols, and all have available
parsers.
12


---

Table 8: Analysis of Industroyer Network Activity.
Tech.
1-Data Source
2-Artifact
3-STIX
4-Artifact
Detailed-
ness
5-
Proprietary
6-Parser
T0884
Network
Traffic
Con-
nection
Connection
to
Port 3128
Full
–
Net-
work
Traf-
fic:
sr-
c/dest_port
Described
Open
/
Standard
NA
T0846
Network Traf-
fic Content
61850
discovery
functions
Partial
Network
Traffic:
src/
dst_payload_
ref
Described
Open
/
Standard
Yes
T0846
Network Traf-
fic Content
OPC
discovery
functions
Partial
Network
Traffic:
src/
dst_payload_
ref
Actionable
Open
/
Standard
Yes
T0801
OPC/61850 moni-
tor functions
T0888
61850
collection
functions
T0888
OPC
collection
functions
T0888
104 collection func-
tions
T0855
104
command
functions
T0806
104
command
functions
SIPROTEC/Relay Activity (Table 9): Industroyer also has the capability to use the CVE-2015-5374
vulnerability to make a SIPROTEC relay unresponsive. The malware sends a SIPROTECH message to a relay,
causing the device to enter an unresponsive state, requiring the device to be rebooted [T0814][T0816]. This
message is an 18-byte packet to a proprietary UDP port 50,000 on the device. This 18-byte string is provided in
the threat intelligence and could be represented by the STIX payload_ref object; however, it is unclear whether
this is a reliable or precise indicator, as it is a proprietary protocol. On the device side, the message initiates an
incomplete firmware update, which is not completed, leaving the device unresponsive [T0800]. This is potentially
available in device application logs; however, there is no detail about this activity from the device side, and no
existing STIX observable to support log events.
Table 9: Analysis of Industroyer Network Activity.
Tech.
1-Data Source
2-Artifact
3-STIX
4-Artifact
Detailed-
ness
5-Proprietary
6-Parser
T0814
Network Traf-
fic Content
Strings/ SIPRO-
TECH protocol
parser & mgmt
functions
Partial
–
Network
Traffic:
src/
dst_payload_
ref
Actionable
Proprietary
-
Undocumented
No
T0816
T0800
Application
Log Content
Device
Log
Events
No
Missing
Proprietary
-
Undocumented
NA
-
host
13


---

4.2
Thorough Analysis of Threat Information Sharing at ATT&CK for ICS
4.2.1
Methodology
To provide a comprehensive assessment beyond the three detailed case studies, we conducted a systematic analysis
of all 196 procedure examples across 79 techniques documented in ATT&CK for ICS. Our methodology consists of
four phases:
1. Data Acquisition and Preparation - All procedure descriptions were retrieved from the public MITRE
ATT&CK STIX data for ICS9 and normalized into plain-text records. Each record retained its corresponding
technique identifier, and malware family linkage.
2. Automated Observable Extraction - Each procedure description was processed by a LLM (GPT o3-mini)
using a structured prompt that explicitly defined the task, decision rules, and expected JSON output format.
The model was instructed to identify every observable mentioned in the text, ranging from file names and
commands to ICS-specific protocol elements, and to classify each one according to the pre-defined attributes.
3. Observable Categorization - Every extracted observable was represented as a structured schema record
containing the key criteria we defined before.
4. Post-processing and Quality Control - According to the STIX 2.1 specification, the software Cyber-
Observable Object is defined as "high-level properties associated with software, including software prod-
ucts".10 This equivocal definition can mislead an LLM into labelling malware identifiers as observables. Yet,
STIX classifies malware itself as a distinct Domain Object11 rather than as an observable artifact. Because
SCOs are intended to capture low-level forensic evidence, while Domain Objects (e.g., malware encodes
higher-order threat-intelligence concepts), keeping malware entries in the observable layer would blur these
semantic boundaries.12 To preserve the intended separation of concerns, we therefore filtered out every item
that the model had incorrectly flagged as malware-related. The resulting dataset was manually reviewed to
eliminate duplicates, to remove entities incorrectly labeled as Observables, and to correct misclassifications.
Overall, out of 361 observables, 103 observables’ data were manually modified:
• 34 observables specifications were modified to be more ICS specific domain
• 27 observables were manually classified as Actionable instead of Described
Extracted Observable example:
1
{
2
’observable_value ’: ’CSW ’,
3
’artifact_details ’: ’Described ’,
4
’data_source ’: ’ICS
historian ’,
5
’classification ’: ’ICS
Data Tag ’,
6
’STIX_supported ’: ’No ’,
7
’proprietary_artifact ’: ’Open/Standard
Technology ’,
8
’parser ’: ’libiec61850’,
9
’notes ’: ’Logical -node
data
attribute
indicating
circuit -breaker / switch
control
capability.’,
10
’description ’: "The [Industroyer ](https:// attack.mitre.org/software/S0604) IEC 61850 component
sends
the domain -specific
MMSgetNameList
request
to
determine
what
logical
nodes
the
device
supports. It then
searches
the
logical
nodes
for
the CSW
value, which
indicates
the
device
performs a circuit
breaker
or
switch
control
function .( Citation: ESET
Industroyer)\n\n[Industroyer ](https:// attack.mitre.org/software/S0604)’s OPC DA module
also
uses
IOPCBrowseServerAddressSpace
to look
for
items
with
the
following
strings: ctlSelOn, ctlOperOn, ctlSelOff, ctlOperOff
, Pos and
stVal .( Citation: ESET
Industroyer)\n\n[Industroyer ](https:// attack.mitre.org/software/S0604) IEC 60870-5-10
4 module
includes a range
mode to
discover
Information
Object
Addresses (IOAs) by
enumerating
through
each .( Citation:
ESET
Industroyer)",
11
’technique_num ’: ’T0888’,
12
’description_id ’: ’relationship --62e818b8-38e6-42ff -9424-9a327332eb2a’,
13
’related_malware ’: ’Industroyer ’
14
}
The systematic analysis revealed patterns that directly address our research questions. The following sections
present the empirical findings, organized by: (i) STIX representation gaps; (ii) actionability of extracted observables;
and (iii) dependency on proprietary technologies.
4.2.2
Observation and Analysis
STIX GAP Taxonomy
Out of 361 extracted observables, over half of the observables (191, around 53%)
have only partial support in STIX 2.1, meaning they can only be approximated via generic or custom objects.
About 19% (69 observables) have no support at all in STIX (i.e., no relevant cyber observable exists), while only
around 28% (101 observables) are fully supported by an existing STIX object type. This indicates a significant
coverage gap for many ICS-specific artifact types.
9https://github.com/mitre-attack/attack-stix-data/blob/master/ics-attack/ics-attack.json
10https://docs.oasis-open.org/cti/stix/v2.1/csprd01/stix-v2.1-csprd01.html#_Toc16070740
11https://docs.oasis-open.org/cti/stix/v2.1/csprd01/stix-v2.1-csprd01.html#_Toc16070566
12https://docs.oasis-open.org/cti/stix/v2.1/csprd01/stix-v2.1-csprd01.html#_Toc16070567
14


---

1. Fully Supported (101) - These are mostly standard Information Technology (IT) indicators (e.g., files,
network addresses, domain names) which map cleanly to STIX SCOs like File, IPv4-Addr, Domain-Name,
etc. Few ICS-specific items fall in this category, underscoring that STIX 2.1’s built-in types were not
designed with ICS nuances in mind.
2. Partially Supported (191) - The majority of ICS observables fall here. They often correspond to ICS
domain concepts that lack a first-class STIX object, but can be accommodated within a generic object
or a custom extension. For example: MMSgetNameList (an ICS protocol command) is labeled Partial:
network-traffic, meaning it can be captured as network traffic data, but STIX has no explicit "ICS command"
type. Many PLC programming functions (e.g., Siemens S7 functions like SFC1 or block names like OB1)
were marked Partial: artifact, indicating they could only be represented as generic file/artifact content.
3. Not Supported (69) - These are observables with no meaningful STIX representation. They include
highly ICS-specific elements for which even an approximation is lacking. For example: ctlSelOn – an ICS
data tag/field from a control system historian – is marked "No support" because STIX has no concept
of a tag or point name in a PLC/SCADA database. Likewise, ICS memory addresses and register values
(e.g., Information Object Addressess (IOAs) in IEC-104) are also unsupported. In general, ICS data tags,
device configurations, and field values (e.g., status flags, function codes) show up repeatedly among the "No
support" entries. This trend highlights that industrial control system observables are a major gap area in
STIX 2.1, the schema covers IT-centric artifacts well, but things like control logic variables, PLC memory
blocks, or proprietary protocol fields fall outside its current scope.
Trends in Unsupported Types.
The unsupported entries tend to cluster in specific classifications. Many
ICS Data Tag artifacts (control system historian points, device tags) had no STIX support. Even some general IT
items like specific software tool names or report identifiers were marked unsupported when they do not correspond
to STIX’s defined objects (e.g., an internal report ID or a code function name has no direct STIX analog). In
contrast, common network or host indicators, such as files, IP addresses, and user accounts, are typically fully
covered. This suggests that STIX 2.1’s coverage gap is most pronounced for specialized ICS domain artifacts, such
as data related to industrial devices, proprietary protocols, and control logic, whereas typical enterprise observables
are well-supported.
Figure 2: Distribution of Artifact Details within Top 10 Classification Categories ("Actionable" in blue,
"Described" in teal, "Mentioned" in orange).
Artifact Detail Level Distribution
The observables were categorized into over 100 classification types, but
a few dominate (see Figure 2). It is worth noting that an ICS data artifact class, ICS Data Tag (8), also makes
the top 10, indicating that specific tag names/variables from control system databases were noted multiple times
despite STIX gaps. In general, the classification distribution highlights that ICS/OT entities (devices, protocols,
and commands) were prominent, alongside a mix of traditional IT indicators (files and network configurations)
present in the threat reports.
15


---

Figure 3: Distribution of Artifact Details within Top 5 Data Sources("Actionable" in blue, "Described" in
teal, "Mentioned" in orange).
Each observable was also tagged with a data source indicating where that artifact could be collected. The most
common source by far is network traffic (93 observables). This aligns with the many ICS protocol messages and
network indicators extracted (since those would be seen in network captures or Packet Captures (PCAPs)). Notably,
ICS historian logs (50) are the third-largest category; many of the ICS-specific observables, such as tag values
and device status changes, are recorded in historian databases or engineering logs, emphasizing the importance
of historian data in detecting ICS attacks. It is worth highlighting that ICS-specific telemetry (Historian, PLC
ladder logic captures) together make up a significant chunk, demonstrating that to fully monitor these observables,
one must pull from ICSs and not just traditional IT logs.
Actionable Observables Lacking STIX Support
One important observation is that several observables
deemed "Actionable" (high-value IOCs) are not fully supported in STIX 2.1, which could hinder information
sharing. In our results, 48 actionable observables (over half of all actionable ones) were only partial or not
supported in STIX. These include ICS-specific items, such as ctlSelOn, which is a precise, unique tag name that
an attacker can manipulate (actionable for detection in ICS logs); yet, STIX has no way to represent it except as
a generic artifact or custom field. The same goes for certain PLC function codes or protocol commands that are
very specific (and thus actionable within that context) but have no STIX presentation.
The key insight is that being "Actionable" does not guarantee STIX support. There is a misalignment
where CTI producers can identify a highly specific ICS indicator, but when codifying it in STIX format to share
with others, they struggle due to the schema’s limitations. This can complicate the intelligence sharing process for
ICS threats; either the observable has to be dropped (if there’s no representation) or shared in an unstructured way
(in notes or description fields), reducing its utility. It reinforces the earlier point that extending STIX or developing
custom SCOs for ICS could significantly enhance our ability to share and leverage these crucial observables.
The fact that dozens of actionable ICS indicators fall through the cracks in STIX 2.1 is a call to action for the
community to address these schema gaps for industrial security.
5
Analysis of Vulnerability Information Sharing
In addition to studying cyber threat activity, the analysis also reviews the sharing of vulnerability advisories
associated with known exploitable ICS vulnerabilities based on their inclusion in the CISA KEV Catalog. This list
was produced by reviewing the KEV Catalog for Common Vulnerabilities and Exposuress (CVEs) identified since
2023, which are associated with CISA ICS Alerts. Since these vulnerabilities have been known to be exploited by
threat actors, they present a clear risk to asset owner environments, requiring some mitigating actions. While
within IT environments these vulnerabilities are typically patched, it is well documented asset owners struggle to
16


---

quickly deploy patches [36]. If an asset owner cannot quickly patch these vulnerabilities to mitigate their risk,
they may need to deploy detection mechanisms to prevent their exploitation. Therefore, vulnerability information
is reviewed in accordance with the same requirements as defined in Section 2. That is, evaluating whether the
vendor provided some rule to support the detection of the vulnerability, or whether sufficient technical details are
available about the product and associated vulnerability for the asset owner to generate their own detection.
Table 10 documents the analysis of the 9 CISA vulnerability advisories and the associated vendor-provided
vulnerability advisories. For each advisory, the CISA ICS Advisory number, the associated CVEs, vendor, and
associated protocols (if applicable) are defined. Each advisory was reviewed for the following criteria.
1. Rules/Analytics Available (1): This identifies whether the advisory provides any information about detection
rules (e.g., a Snort rule) or analytics that can be deployed to detect the advisories.
2. Availability of Technical Details (2): This criterion assesses whether the report or advisory includes sufficient
technical information such that a detection rule or analytic could be developed based on that information.
While many vulnerability advisories provide high-level discussion about the vulnerability and mappings to
known Common Weakness Enumerations (CWEs), they also do not provide the technical details required
to develop rules or analytics to detect exploitation. If technical information is available but insufficient to
inform a detection, it is labeled as ’Partial.’
3. Proprietary (3), and Parsers (4): For vulnerabilities that are associated with a network protocol, this
explores whether the protocol is open, proprietary, and documented, or proprietary and undocumented (3).
Next, it reviews whether a parser exist for that protocol (4). If a parser exists but does not fully cover the
protocol’s use or implementation, it is labeled as Partial.
Table 10: Table 10: Review of 9 ICS vulnerabilities with known exploitation.
ICSA Alert
CVE
Vendor
Protocol
1- Rules
2 - Tech Detail
3 - Proprietary
4 - Parsers
23-355-01
2023-49897
FXC
HTTP
No
No
Open - HTTP
Partial
23-355-02
2023-47565
QNAP
HTTP
No
No
Open - HTTP
Partial
23-348-15
2023-4911
2023-44487
Siemens
NA - Host
No
Partial
N/A
N/A
23-320-11
2023-6448
Unitronics
PCOM
No
No
Proprietary -
Undocumented
No
23-297-01
2023-20273
2023-20198
Rockwell
Automation
HTTP
Yes -
External
Partial
Open - HTTP
Partial
23-264-05
2020-16017
Rockwell
Automation
HTTP
No
Partial
Open - HTTP
Partial
23-075-01
2021-4034
Siemens
NA - Host
No
Yes
N/A
N/A
23-193-01
Documented
exploit but
not in KEV
2023-3595
2023-3596
Rockwell
Automation
CIP
Yes
Yes
Proprietary -
Documented
Yes
5.1
Key Outcomes
The outcome of this analysis highlights that current vulnerability advisories lack sufficient technical details for asset
owners to create their own detections. Only two out of the nine vendor advisories reviewed include a detection
rule or analytic for the vulnerabilities. Furthermore, vulnerability advisories often lack the necessary technical
details to support the development of effective detections. Four provided no technical details, excluding the
two vulnerabilities that included detection rules, while three provided partial technical discussions, which were
insufficient for developing a detection. Further, one protocol was fully proprietary and undocumented. At the
same time, five were based on HTTP, an open protocol, but can have highly diverse specific customization, making
parsing difficult without details of the specific application functions. While parsers for HTTP exist, they would
still need to be heavily tailored towards the particular device’s application. This analysis highlights that detection
rules are not consistently provided and critical information about device vulnerabilities or associated protocols not
provided with sufficient detail to enable the development of detections. Based on this analysis, it’s unclear how
asset owners are expected to protect themselves from the reported vulnerabilities.
6
Challenges in Threat Information Sharing
The prior sections provide an evidence-driven review of both available threat intelligence data (through ATT&CK
for ICS), and recent vulnerabilities advisories defined by vendors and CISA. This analysis identifies four key
17


---

challenges that should be addressed to ensure threat information can be more shared more effectively to ensure
asset owners can effectively detect these threats.
1. A lack of defined technical artifacts to support sharing of indicators of OT threats through
STIX. This analysis demonstrated that while existing STIX Observables would be sufficient for detecting
a large majority of the TTPs identified in the previous analysis, there remain multiple TTPs that lack
sufficiently defined technical artifacts. Therefore, expanding STIX observables is necessary to support the
sharing of all known adversarial techniques associated with ICS incidents. Key examples include:
• PLC Code/Logic: Numerous techniques include the deployment of malicious logic on a PLC. While
many PLCs leverage vendor-specific tailoring of their logic, many devices share some fundamental
capabilities and languages, especially as they align with the IEC 61131-3 standard for developing
programs. These programs are typically compiled before deployment to the controller. However,
the source code is typically transferred alongside the binaries to support diagnostics of the deployed
program. Therefore, mechanisms to support understanding program segments on the controller, both
through source and compiled code, may be effective in detecting malicious logic.
• Integrity checks: Further, many controllers also use integrity check mechanisms, typically based on
CRCs or Checksums, to verify that programs have not changed
[37]. On the one hand, security
products can verify that a specific program has been downloaded to the device by validating its
signatures. On the other hand, CRC/Checksum integrity checks are not sufficient against threat actors
who intentionally modify the PLC code
[38]. There is a need for a wider deployment of secured
integrity signatures [39].
• ICS Protocols: Currently, the STIX standard supports prevalent IT protocols, including HTTP and
SMTP. However, each incident reviewed above has techniques that utilize ICS-specific protocols. While
these could potentially be parsed through more general NetworkTraffic payload objects, the associated
observables will still likely be ineffective without tailored objects. Therefore, developing observable
objects to support key ICS protocols and fields would improve the effectiveness of sharing and detection
of techniques targeting those protocols. It may be possible to craft a general ICS protocol object using
typical functionality associated with ICS protocols.
2. The dependence on proprietary technologies and protocols without available parsers hinders
the ability to develop detections. While vendor technologies may require custom/proprietary protocols
or the customization of standard protocols to address unique challenges faced when interfacing with devices,
these protocols are increasingly targeted by threat actors, and therefore necessitate the ability to be monitored
for threats by the asset owner. The following table reviews the unique protocols identified in this analysis.
Of the nine overall protocols, at least three proprietary protocols were identified, and two had no publicly
available parsers. Unfortunately, organizations are required to monitor network traffic in order to identify
the behavior of threat actors. However, this dependency on proprietary and undocumented protocols, along
with limited access to parsers, prevents the deployment of the necessary detection capabilities.
Table 11: Available Network Parsers for ICS Protocols.
Threat/vuln
Protocol
Parsers available
Industoryer
IEC 61850 MMS
Yes
IEC 60870-5-104
Yes
OPC DA
No
Stuxnet
S7Comm
Yes
MS SQL(TDS)
Yes
Profibus
No, but Profinet does
Triton
Tristation
No
Icsa-23-348-15
PCOM
No
Icsa-23-193-01
CIP
Yes
While proprietary and undocumented protocols were acceptable when vendors could assume only their own
devices would operate within a closed ecosystem, the need to integrate network monitoring capabilities
invalidates this assumption.
Therefore, vendors must provide standard documentation and available
parsers for network protocols to ensure asset owners can sufficiently detect threat actor behaviors in their
environments.
3. Vulnerability advisories lack sufficient technical details to develop a detection of exploited
vulnerability and lack rules/analytics to support that detection. Current industry norms suggest
that vendors are responsible for providing timely patches or updates to address product vulnerabilities,
thereby mitigating the associated risks. However, it is well known that most asset owners struggle to
18


---

perform patching in OT environments due to shortages of OT security personnel, limited maintenance
periods, and high availability requirements. If a patch cannot be deployed, the organization may not have
an alternative mechanism to mitigate that risk. It may only be able to monitor for any exploitation activity
of this vulnerability. Unfortunately, vulnerability advisories constantly lacked an associated detection rule
or analytic, and also lacked sufficient technical details necessary to devise an effective rule. Specifically, in
the sampling of the nine vendor advisories reviewed for this study, five did not have mitigations other than
patching, and seven lacked sufficient detail to support the detection, and only two included actual detection
rules. Without sufficient technical details about vulnerabilities, asset owners cannot effectively develop their
own detection rules or analytics, as this would likely require time- and resource-intensive reverse engineering
of the device and associated protocols. Organizations are therefore primarily dependent on external security
firms to perform these actions, but this ultimately presents additional costs to the organizations, both
through the cost of the detection product and through the staff time dealing with false positives from an
ineffective or imprecise rule. The two vulnerability advisories that contribute to associated detection rules
demonstrate the feasibility of publishing these rules and should be acknowledged as an exemplar of leading
industry practices.
4. Threat reports/advisories lack sufficient technical details or supporting technical artifacts across
many procedure examples, constraining the development of detection rules or analytics. Similar
to the above challenge regarding the lack of technical details about vulnerabilities and associated detection
rules or alerts, threat advisories do not consistently provide sufficient technical details or analytics/rules
to enable the development of detections. In the sampling of the 51 procedure examples identified for
this study, at least 44 did not have sufficient technical detail to create a detection.
However, unlike
vulnerability advisories, security firms or government agencies typically release threat advisories. These
organizations typically have limited access to information about threat activity due to constraints on the
available data sources required for forensically analyzing the environments and devices. Furthermore, as
previously identified, detection vendors typically have limited information about vendor technologies, which
may require additional reverse engineering to fully understand the threats’ technical actions and develop the
required detections. Therefore, this challenge should not be perceived as an inadequacy or deficiency of
the organizations developing these reports, especially when the developing organization is producing this
information to support their commercial product. Instead, this is only intended to highlight the need for a
more consistent approach/format for the structure and content of threat advisories. While many reports
document specific ATT&CK TTPs, they lack specific technical artifacts or technical details necessary to
detect that threat.
7
Limitations and Implications
This study, while comprehensive in scope, has several limitations that should be considered when interpreting the
findings. The first limitation is that our analysis primarily relies on MITRE ATT&CK for ICS as the aggregated
source of threat intelligence.
While ATT&CK represents one of the most comprehensive publicly available
knowledge bases of ICS threats, this choice introduces potential coverage bias. ATT&CK may overrepresent
well-documented, publicly disclosed incidents while underrepresenting threats that remain classified or proprietary.
If alternative sources such as sector-specific Information Sharing and Analysis Centers (ISACs), regional CERTs,
or commercial threat intelligence were analyzed, we might observe different patterns in observable types and
documentation quality. A second important limitation arises from the methodological constraints. While we
validated the LLM-based extraction through manual review and correction of 103 observables, automated extraction
may have missed implicit observables or misclassified complex ICS-specific artifacts. The 87% inter-rater reliability,
while acceptable, indicates some subjective interpretation in observable classification.
8
Conclusion
This study presents the first comprehensive, evidence-based analysis of the challenges associated with threat
information sharing in industrial control systems. Through a deep analysis of threat information from three major
attacks, a systematic examination of 196 procedure examples from ATT&CK for ICS, and nine recent vulnerability
advisories, we have empirically demonstrated four critical barriers that impede effective threat intelligence sharing
in OT environments.
Our findings reveal a fundamental misalignment between the information needed for ICS threat detection
and the capabilities of current sharing mechanisms. The analysis reveals that 53% of ICS-specific observables
lack adequate STIX representation, and 19% have no STIX representation, while 77% of extracted artifacts
lack sufficient technical detail for operational use. These are not merely technical oversights but systemic issues
stemming from the unique characteristics of OT environment’s proprietary protocols, specialized devices, and
domain-specific operational constraints.
The implications extend beyond technical standards. Our results suggest that effective ICS threat intelligence
sharing requires a paradigm shift in how the community approaches information collection, representation, and
19


---

dissemination. Vendors must recognize that security-by-obscurity, achieved through undocumented protocols, is no
longer tenable when these same protocols become attack vectors. Security researchers must balance the need for
operational security with providing actionable technical details. Standard bodies must evolve frameworks like
STIX to accommodate ICS-specific artifacts that do not fit traditional IT paradigms.
Looking forward, this research establishes a baseline for measuring progress in ICS threat intelligence sharing.
The methodology developed, combining manual analysis with automated extraction, provides a reproducible
framework for ongoing assessment. As the ICS threat landscape continues to evolve, regular application of this
methodology can track improvements in information sharing quality and identify emerging gaps.
The path forward requires coordinated action across multiple stakeholders. We recommend: (i) expansion
of STIX to include ICS-specific observable types identified in this study; (ii) industry adoption of standardized
vulnerability disclosure templates that include detection rules; (iii) development of open-source protocol parsers
for critical ICS protocols; and (iv) establishment of sector-specific information sharing practices that balance
operational security with actionable intelligence.
9
Summary
This paper presents a data-driven analysis of threat information sharing challenges in industrial control systems,
examining real-world threat intelligence and vulnerability advisories. We analyzed 196 procedure examples across
79 techniques from the MITRE ATT&CK for ICS framework and nine recent CISA vulnerability advisories,
identifying four key challenges:
1. Insufficient STIX Observable Support: 72% of ICS-specific threat observables cannot be adequately
represented in current STIX standards, with critical gaps in PLC logic representation, ICS protocol specifics,
and device-level artifacts.
2. Dependency on Proprietary Technologies: Critical threat detection depends on understanding
undocumented proprietary protocols, with 4 out of 9 identified ICS protocols lacking publicly available
parsers.
3. Inadequate Vulnerability Advisory Details:Only 22% of reviewed advisories provided detection rules,
and 78% lacked sufficient technical detail for developing custom detections.
4. Limited Actionable Threat Intelligence: Only 23% of threat procedure examples contained actionable
technical details, constraining defenders’ ability to develop effective detections.
Our systematic methodology, which combines manual analysis with automated LLM-based extraction, provides a
reproducible framework for assessing the quality of threat intelligence. The findings demonstrate that current
information sharing practices, while improved from previous years, still fail to meet the operational needs of ICS
defenders. Addressing these challenges requires coordinated efforts from vendors, researchers, and standards
bodies to develop ICS-specific sharing mechanisms that balance security concerns with operational utility.
References
[1] Executive Order No. 13691.
Promoting private sector cybersecurity information sharing.
3 C.F.R.
13691, Feb 2015.
Available:
https://obamawhitehouse.archives.gov/the-press-office/2015/02/13/
executive-order-promoting-private-sector-cybersecurity-information-shari.
[2] Cyberspace Solarium Commission. 2023 annual report on implementation. Technical report, Cyberspace
Solarium Commission, Sep 2023. Available: https://cybersolarium.org/wp-content/uploads/2023/09/
CSC2.0_Report_2023AnnualReport.pdf.
[3] The MITRE Corporation. Mitre att&ck® for ics, 2024. Accessed: Sep. 6, 2024. Available: https://attack.
mitre.org/matrices/ics/.
[4] NATO Cooperative Cyber Defence Centre of Excellence. Stuxnet facts report: A technical and strategic
analysis. Technical report, NATO Cooperative Cyber Defence Centre of Excellence, 2013. Available: https://
ccdcoe.org/library/publications/stuxnet-facts-report-a-technical-and-strategic-analysis-2/.
[5] A. Case, D. P. Y. A. Babcock, and S. Hilt. Analysis of the cyber attack on the ukrainian power grid. Technical
report, SANS Industrial Control Systems, 2016. Available: https://ics.sans.org/media/E-ISAC_SANS_
Ukraine_DUC_5.pdf.
[6] N.
Perlroth.
A
cyberattack
in
saudi
arabia
had
a
deadly
goal.
experts
fear
another
try.
The New York Times,
Mar 2018.
Available:
https://www.nytimes.com/2018/03/15/technology/
saudi-arabia-hacks-cyberattacks.html.
[7] Cybersecurity and Infrastructure Security Agency. Known exploited vulnerabilities catalog, 2024. Accessed:
Sep. 6, 2024. Available: https://www.cisa.gov/known-exploited-vulnerabilities-catalog.
20


---

[8] C. Krasznay and G. Gyebnár. Possibilities and limitations of cyber threat intelligence in energy systems. In
2021 13th International Conference on Cyber Conflict (CyCon), pages 171–188. IEEE, May 2021.
[9] E. López-Morales. Securing cyber-physical systems via advanced cyber threat intelligence methods. In
Proceedings of the 2024 on ACM SIGSAC Conference on Computer and Communications Security, pages
5119–5121, Dec 2024.
[10] B. Jin, E. Kim, H. Lee, E. Bertino, and D. Won. Sharing cyber threat intelligence: Does it really help? In NDSS
2024, 2024. Available: https://www.ndss-symposium.org/wp-content/uploads/2024-228-paper.pdf.
[11] S. Ainslie, D. Thompson, and S. Maynard.
Cyber-threat intelligence for security decision-making: A
review and research agenda for practice.
Computers & Security, 132:103352, 2023.
Available: https:
//www.sciencedirect.com/science/article/pii/S0167404823002626.
[12] P. Alaeifar et al. Current approaches and future directions for cyber threat intelligence sharing. Journal
of Information Security and Applications, page 103786, 2024. Available: https://www.sciencedirect.com/
science/article/pii/S2214212624000899.
[13] H. Griffioen, T. Booij, and C. Doerr. Quality evaluation of cyber threat intelligence feeds. In ACNS 2019,
LNCS 12146, pages 277–296, 2019. Available: https://dl.acm.org/doi/10.1007/978-3-030-57878-7_14.
[14] T. Schaberreiter et al. A quantitative evaluation of trust in the quality of cyber threat intelligence. In ARES
2019, 2019. Available: https://dl.acm.org/doi/10.1145/3339252.3342112.
[15] OASIS Open. Stix™version 2.1. Oasis standard, OASIS, Jun 2021. Approved 10 June 2021. Available:
https://docs.oasis-open.org/cti/stix/v2.1/os/stix-v2.1-os.pdf.
[16] M. Zych and V. Mavroeidis. Enhancing the stix representation of mitre att&ck for group filtering and technique
prioritization. arXiv preprint arXiv:2204.11368, 2022. Available: https://arxiv.org/abs/2204.11368.
[17] K. Paine, O. Whitehouse, J. Sellwood, and A. Shaw. Rfc 9424: Indicators of compromise (iocs) and their role
in attack defence. IETF RFC, 2024. Available: https://datatracker.ietf.org/doc/rfc9424/.
[18] F. Marchiori, M. Conti, and N. V. Verde. Stixnet: A novel and modular solution for extracting all stix objects in
cti reports. In ACM ARES 2023 (W), 2023. Available: https://dl.acm.org/doi/10.1145/3600160.3600182.
[19] M. T. Alam et al. Ctibench: A benchmark for evaluating llms in cyber threat intelligence. In NeurIPS 2024
Datasets & Benchmarks, 2024. Available: https://proceedings.neurips.cc/paper_files/paper/2024/
file/5acd3c628aa1819fbf07c39ef73e7285-Paper-Datasets_and_Benchmarks_Track.pdf.
[20] R.
Fieblinger,
M.
T.
Alam,
and
N.
Rastogi.
Actionable
cyber
threat
intelligence
using
knowledge
graphs
and
large
language
models.
In
IEEE
EuroS&PW
2024,
2024.
Available:
https://www.researchgate.net/publication/383535439_Actionable_Cyber_Threat_Intelligence_
Using_Knowledge_Graphs_and_Large_Language_Models.
[21] D. Bhusal, M. T. Alam, L. Nguyen, A. Mahara, Z. Lightcap, R. Frazier, R. Fieblinger, G. L. Torales, B. A.
Blakely, and N. Rastogi. Secure: Benchmarking large language models for cybersecurity advisory. arXiv
preprint arXiv:2405.20441v3, Sep 2024. Available: https://arxiv.org/pdf/2405.20441v3.
[22] B. Strom et al.
Mitre att&ck®: Design and philosophy.
Technical report, MITRE, 2020.
Available:
https://attack.mitre.org/docs/ATTACK_Design_and_Philosophy_March_2020.pdf.
[23] O. Alexander et al. Mitre att&ck® for industrial control systems: Design and philosophy. Technical report,
MITRE, 2020. Available: https://attack.mitre.org/docs/ATTACK_for_ICS_Philosophy_March_2020.pdf.
[24] D. S. Afenu et al. Industrial control systems security validation based on mitre att&ck. Electronics, 13(5):917,
2024. Available: https://www.mdpi.com/2079-9292/13/5/917.
[25] S. Choi, J-H. Yun, and B-G. Min. Probabilistic attack sequence generation and execution based on mitre
att&ck for ics datasets. In CSET @ USENIX Security 2021, 2021. Available: https://cset21.isi.edu/
papers/cset21-4.pdf.
[26] MITRE Corporation. MITRE D3FEND: A knowledge graph of cybersecurity countermeasures. https:
//d3fend.mitre.org/, 2025. Version 1.3.0. Accessed: January 11, 2026.
[27] Ítalo Oliveira, Gal Engelberg, Pedro Paulo F. Barcelos, Tiago Prince Sales, Mattia Fumagalli, Riccardo
Baratella, Dan Klein, and Giancarlo Guizzardi. Boosting d3fend: Ontological analysis and recommendations.
In Torsten Hahmann, Antony Galton, Maria M. Hedblom, and Nathalie Aussenac-Gilles, editors, Formal
Ontology in Information Systems - Proceedings of the 13th International Conference, FOIS 2023, volume 377
of Frontiers in Artificial Intelligence and Applications, pages 334–348. IOS Press BV, December 2023.
[28] U.S. Government Accountability Office. Cybersecurity: Federal actions urgently needed to better protect the
nation’s critical infrastructure. Technical Report GAO-23-105468, U.S. Government Accountability Office,
Mar 2023. Available: https://www.gao.gov/products/gao-23-105468.
[29] Splunk. Threat detection, investigation, and response (tdir). Blog post, 2023. Available: https://www.splunk.
com/en_us/blog/learn/tdir-threat-detection-investigation-response.html.
21


---

[30] CrowdStrike.
Threat
detection,
investigation,
and
response
(tdir).
Website,
2024.
Available:
https://www.crowdstrike.com/cybersecurity-101/threat-intelligence/
threat-detection-investigation-response-tdir/.
[31] SecurityWeek.
Ics
patch
tuesday
advisories
published
by
siemens,
schneider
elec-
tric,
aveva,
cisa.
SecurityWeek,
2024.
Available:
https://www.securityweek.com/
ics-patch-tuesday-advisories-published-by-siemens-schneider-electric-aveva-cisa/.
[32] Anastasios Papathanasiou, George Liontos, Athanasios Katsouras, Vasiliki Liagkou, and E. Glavas. Cybersecu-
rity guide for smes: Protecting small and medium-sized enterprises in the digital era. Journal of Information
Security, 16:1–43, 01 2025.
[33] Cybersecurity and Infrastructure Security Agency. MAR-17-352-01 HatMan—Safety System Targeted Malware.
Malware Analysis Report MAR-17-352-01, U.S. Department of Homeland Security, 2017. Accessed: January
28, 2026.
[34] S. Miller. Reversing the tristation network protocol. Presentation at SEC-T, Sep 2018. Available: https:
//www.youtube.com/watch?v=U-BO7y1HU8k.
[35] U.S. Nuclear Regulatory Commission. Final safety evaluation by the office of nuclear reactor regulation:
Triconex topical report 7286-545-1, revision 4 - invensys operations management project no. 709. Tech-
nical report, U.S. Nuclear Regulatory Commission, 2012. Available: https://www.nrc.gov/docs/ML1209/
ML120900890.pdf.
[36] D. Parsons. The state of ics/ot cybersecurity in 2022 and beyond. Technical report, SANS, Oct 2022. Available:
https://www.sans.org/white-papers/state-ics-ot-cybersecurity-2022-beyond/.
[37] PLC Security. Top 20 secure plc coding practices v1.0, Jun 2021. Available: https://www.plc-security.com.
[38] C. Schuett, J. Butts, and S. Dunlap. An evaluation of modification attacks on programmable logic controllers.
Int. J. Crit. Infrastruct. Prot., 7:61–68, 2014.
[39] S. Banerjee. Designing Lightweight Cryptographic Primitives for Securing Industrial Control Systems. PhD
thesis, ResearchSpace@ Auckland, 2024.
APPENDIX
Observable Extraction Prompt
The following prompt was used to systematically extract observables from ATT&CK for ICS procedure descriptions
using GPT o3-mini:
System Prompt: You are a helpful Cybersecurity assistant for identifying observables in Cyber Threat
Intelligence text snippets.
Task
1. You will receive a text snippet of a CTI report from a user.
2. Read the given snippet (plain text) carefully.
3. Extract every observable (artifact) mentioned – do not omit any.
4. For code snippets, include the full code, including triple backticks.
5. For each observable, output a JSON object with the exact fields listed in the Response format
section.
Definitions
1. Actionable Observable
• Unique & specific →a deterministic IDS/YARA/SIEM rule could match it with low FP.
• Immediately operable as-is (code snippet, exact URL, command, file name or path, API function)
or after simple transform (e.g., Base64 decode, hash lookup, parameter substitution, memory
dump).
• Searchable and can drive automated response.
• If the observable meets these criteria →artifact_details = "Actionable".
2. Described Observable
• Has notable specifics, but still not unique enough for detection; non-searchable.
22


---

• If the observable meets this criteria and not the Actionable Observable criteria →artifact_details
= "Described".
3. Mentioned Observable
• A non-searchable observable, which doesn’t stand in the Actionable Observable criteria, nor the
Described Observable criteria.
• For such observables →artifact_details = "Mentioned".
4. STIX Supported This evaluates whether the observable is documented as STIX 2.1 Cyber-observable
Object
• Full: the observable’s type exists in STIX Cyber-Observable Objects.
• Partial: the observable does not map cleanly to a first-class STIX SCO, but can be approximated
or expressed indirectly, or supported only via x_ custom properties or the generic artifact
object.
• No: the observable isn’t Fully STIX supported nor Partially supported
5. Proprietary Artifact
• Open/Standard Technology
• Proprietary-Documented Technology
• Proprietary-Undocumented Technology
Fields to produce for every observable
Field
Description
observable_value
Exact string (or faithful paraphrase). Escape any internal backticks.
artifact_details
"Mentioned" | "Described" | "Actionable" based on the definitions
above.
data_source
Where it can be observed or collected (see cheat-sheet below).
classification
Short type label (e.g., "ICS Command", "URL", "Software/Tool").
STIX_supported
"Full: <STIX_Object_Name>" | "Partial: <STIX_Object_Name>"
| "No".
proprietary_artifact "Open/Standard Technology" | "Proprietary-Documented Technology"
| "Proprietary-Undocumented Technology".
parser
Known open-source/commercial parser name(s) for the data format,
else null or "N/A" if not applicable.
notes
Any extra comments or context (Markdown allowed), or null if none.
Common data_source cheat-sheet
Network traffic • Netflow • PCAP • DNS logs • Web proxy logs • Endpoint (EDR) logs • System logs
(Windows Event, syslog) • ICS historian • PLC ladder logic • Firewall logs • Cloud API audit logs • Memory
dump • None (if not observable via telemetry)
Response format (return only this JSON)
1
{
2
"observables ": [
3
{
4
" observable_value ": "<VAL >",
5
" artifact_details ": "Mentioned | Described | Actionable",
6
" data_source": "<text >",
7
" classification ": "<one of
allowed
values >",
8
" STIX_supported ": "Full: <STIX_Object_Name > | Partial: <STIX_Object_Name > | No",
9
" proprietary_artifact ": "Open/Standard
Technology | Proprietary -Documented
Technology | Proprietary - Undocumented
Technology",
10
"parser": "<text >" | null | "N/A",
11
"notes": "<text >" | null
12
}
13
]
14
}
23
