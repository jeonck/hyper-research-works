---
title: An Alignment Between the CRA’s Essential
id: an-alignment-between-the-cras-essential
tags:
- attack-ontology-drift-cti-85bc51
- pin-rate-survey
created: '2026-09-12T21:32:32.882191Z'
updated: '2026-09-12T21:44:20.173855Z'
source: https://arxiv.org/abs/2505.13641v2
source_domain: arxiv.org
fetched_at: '2026-09-12T21:32:32.881101Z'
fetch_provider: crawl4ai
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'arXiv 2505.13641v2: 0 ATT&CK technique-ID occurrences, below the pin-rate-survey
  inclusion threshold of 3.'
raw_file: raw/an-alignment-between-the-cras-essential.pdf
doi: arXiv:2505.13641v2
---

An Alignment Between the CRA’s Essential
Requirements and the ATT&CK
®’s Mitigations
Jukka Ruohonen
University of Southern Denmark
Email: juk@mmmi.sdu.dk
Eun-Young Kang
University of Southern Denmark
Email: eyk@mmmi.sdu.dk
Qusai Ramadan
University of Southern Denmark
Email: qura@mmmi.sdu.dk
Abstract—The paper presents an alignment evaluation between
the mitigations present in the MITRE’s ATT&CK® framework
and the essential cyber security requirements of the recently
introduced Cyber Resilience Act (CRA) in the European Union.
In overall, the two align well with each other. With respect to the
CRA, there are notable gaps only in terms of data minimization,
data erasure, and vulnerability coordination. In terms of the
ATT&CK® framework, gaps are present only in terms of threat
intelligence, training, out-of-band communication channels, and
residual risks. The evaluation presented contributes to narrowing
of a common disparity between law and technical frameworks.
Index Terms—Security requirements, legal requirements, reg-
ulations, security countermeasures, evaluation, mapping, gaps
I. INTRODUCTION
The CRA [1] was agreed upon in 2024. The enforcement
will start in 2027. The CRA is a new product-specific cyber
security law covering most products with a network connection
functionality; the notable exclusions are medical devices,
motor vehicles, ships and maritime equipment, and cloud
computing. Although stricter obligations are imposed upon
products categorized as important or critical, all products must
comply with the CRA’s essential cyber security requirements.
To help in bridging a gap between legal and techni-
cal domains, the paper investigates an alignment between
the CRA’s essential cyber security requirements and the
ATT&CK® framework [2]. It is a comprehensive empirical
catalog of real-world adversarial tactics and techniques main-
tained by the non-profit MITRE corporation. It was initiated in
2013. Although the framework’s focus is on advanced persis-
tent threats, the mitigations offered in the framework general-
ize to countering other threat actors as well. Perhaps partially
due to this generalizability, the ATT&CK® framework has
been extensively used also in academic research [3], [4], [5].
Among this research is also a previous work for using the
framework to elicit security requirements [6]. Another related
work worth explicitly mentioning is about the ATT&CK®’s
alignment with standards [7]. The paper aligns with and
contributes to this line of elicitation and evaluation research.
Recently, the alignment of the CRA’s essential cyber se-
curity requirements has been evaluated against the legal re-
quirements imposed by the GDPR, that is, the General Data
Protection Regulation [8]. In addition, the CRA’s reporting
obligations with respect to severe cyber security incidents have
been analyzed in conjunction with the EU’s NIS2 directive
for critical infrastructure protection [9]. There is also existing
work on the CRA’s other reporting obligations with respect
to vulnerability coordination and disclosure, including the
mandatory reporting of actively exploited vulnerabilities [10].
The present paper continues this comparative evaluation work.
The alignment evaluation raises also the paper’s practical
relevance because the regulation will be supported by stan-
dards. To this end, also European standardization and other
related organizations have already conducted CRA-specific
evaluation studies [11], [12]. Related work is being done
by open source software communities [13] who too perceive
standards and standardized processes as important for reaching
compliance with the CRA [14]. While recognizing that the
terms validation and evaluation have specific meanings in
requirements engineering [15], the evaluation term is used
because the CRA’s requirements and the ATT&CK®’s mit-
igations are not validated with an existing product or an
implementation. It should be also mentioned that the CRA’s
essential cyber security requirements are legal requirements
imposed by a law. Therefore, the paper can be framed also
toward existing requirements engineering research dealing
with legal requirements specifically [8], [16], [17].
A further important point is that the ATT&CK®’s mit-
igations are categorized into three groups: enterprise, mo-
bile, and industrial control systems. Thus, not all of the
mitigations are strictly about products, which is what the
CRA is mainly about, but their generality still allows to
evaluate the alignment. In fact, many of the natural language
descriptions for the mitigations resemble actual requirements
to some extent. They are also known as countermeasures [18]
or security controls [19]. It should be further emphasized
that the CRA’s essential cyber security requirements are risk-
based; they should be prioritized according to results from
risk analyses. Even though the ATT&CK® framework could
be used to help at a risk analysis, as also demonstrated in
the literature [20], the paper only considers the alignment
evaluation. Even under this restriction, the paper helps at
identifying relevant mitigations that can support compliance
with the CRA’s essential requirements at a conceptual level,
thus also bridging the gap between legal and technical domains
The paper’s remainder is structured into three sections.
The opening Section II elaborates the analytical evaluation
methodology, presenting also research questions to guide the
evaluation. Then, the evaluation results are presented in Sec-
tion III. The final Section IV presents a concluding discussion.
Proceedings of the IEEE 33rd International Requirements Engineering Conference Workshops (REW 2025), Valencia, IEEE, 2025, pp. 209–214.
This version is the authors’ copy. The publisher’s definite version is available online via https://doi.org/10.1109/REW66121.2025.00033.
arXiv:2505.13641v2  [cs.CR]  15 Oct 2025


---

II. APPROACH
A terminological clarification is required to elaborate the
analytical evaluation methodology and the research ques-
tions (RQs). The alignment is evaluated by using a generic
concept of a mapping. Different mappings have also frequently
been used to compare, evaluate, and develop standards and
frameworks [5], [19], [21], [22]. Specifically, “a mapping is
a bi-directional connection between information contained in
two artifacts”, whereas “a link is a uni-directional connection
from one artifact to another” [23, p. 67]. With this simple
terminology, which closely resembles definitions used in soft-
ware traceability research [24], [25], the artifacts examined
refer to the ATT&CK®’s mitigations and the CRA’s essential
requirements categorized into requirement groups in previous
work [8]. A bidirectional connection between the two means
that in case an essential cyber security requirement is picked
from the CRA, a corresponding mitigation is present in the
ATT&CK® framework—and the other way around. To sim-
plify the analysis, a restriction is placed: each mitigation can
only map to one essential cyber security requirement. Thus, in
terms of Fig. 1, only one-to-one mappings are considered. In
practice, a mapping of a mitigation was done by considering
the most representative and illuminating requirement.
The CRA's essential
cyber security
requirements
The ATT&CK®'s
mitigations
Requirement j
Requirement i
Mitigation l
Mitigation m
Excluded:
®one-to-many
®mappings (and
®many-to-many 
mappings)
Requirement k
Mitigation n
  Included:
®one-to-one
®mappings
Alignment based on the mappings
Gap
Excluded:
® within-CRA (and
within-ATT&CK®) 1
® mappings
Fig. 1. Alignment, Gaps, and Mappings
Because the CRA is a law and the MITRE’s ATT&CK® is
a framework, a prior hypothesis is that at least some of the
essential requirements map to multiple mitigations because
legal requirements cannot be specified in detailed, technical
terms. This point also correlates with research on the real or
perceived ambiguity of many legal requirements [17], [26].
Having said that, also the ATT&CK® operates at a rather high
abstraction level, meaning that fine-grained technical details
are absent from the mitigations offered and suggested by the
framework. In other words, standards too are often ambiguous
and incoherent. For instance, there is a lack of consistency
even regarding the definitions for fundamental concepts, in-
cluding for the confidentiality, integrity, and availability (CIA)
triad [19]. As the alignment evaluation is based on manually
done mappings, which have been the de facto approach in
existing work [21], [22], the ambiguities and inconsistencies
also raise a validity threat, as is typical in qualitative research.
To address the threat, a collaboration process used in
previous work [27] was adopted. The collaboration involved
three steps: (1) the first author made the initial mappings and
identified the initial gaps; (2) the other two authors reviewed
these and raised arguments in case of disagreements; (3) all
three authors resolved the disagreements by short negotiations.
As usual, a perfect consensus holds for the final mappings and
gaps—after all, otherwise an author would not be an author.
Another point to draw from Fig. 1 is that some of the
requirements may not map to any mitigations, or the other way
around, which would indicate a presence of a gap or several
gaps. Explicit identification of gaps in elicited requirements is
generally important [28], including with respect to changing
requirements [29], which can be seen to frame also the
CRA’s essential cyber security requirements [8]. With the
previous points about legal requirements in mind, a prior
expectation again is that there are some gaps in the CRA.
On one hand: not everything can be covered in a law—and
arguably not everything should even be covered in a law.
On the other hand: if there are numerous gaps in the CRA
vis-`a-vis the ATT&CK®, it could be argued that the policy-
makers overlooked some important aspects—a criticism that
has been expressed in relation to funding or other support for
open source software projects and communities [27]. In any
case, the overall alignment can be summarized by counting
the gaps, one-to-one mappings, and one-to-many mappings.
With these elaborations, the following RQs are evaluated:
• RQ.1: How well the CRA aligns with the ATT&CK®?
• RQ.2: How many and what kinds of gaps there are?
Before continuing to the results, a couple of additional
remarks are warranted about the manually but collaboratively
done mappings. The first is that the CRA’s essential cyber
security requirements were mapped to the mitigations by us-
ing the twelve collated non-functional requirement groupings
elicited and conceptualized in previous work [8], [16]. These
simplify the presentation because no explicit legal references
are required. However, the second point follows: the CRA’s
essential requirements contain also the CIA triad, which can
be argued to be related, either explicitly or implicitly, to
all other essential requirements. Initial disagreements were
present particularly with respect to the CIA triad’s relation to
the CRA’s essential cyber security requirement to review and
apply exploitation mitigation techniques. As said, these were
resolved through negotiations between the authors. A guiding
principle for the negotiations was about the earlier remark
about mapping the mitigations to the “most representative and
illuminating requirement”. To apply this guideline in practice,
all authors were instructed to first consider other requirements
than the CIA triad, and then, if no suitable candidate was
present, to use the triad for a given ATT&CK®’s mitigation.


---

a
Account 
use policies 
Active directory
configuration
Credential
access 
protection
Data 
backup
Data loss
prevention
Encrypt 
sensitive
information
The CIA triad
Multi-factor
authentication
Privileged
account
management
Privileged
process 
integrity
User account
control
Audit
Remote
data storage
Traceability
Data
minimization
Data 
erasure
Security 
testing
Application
developer
guidance
No known
vulnerabilities
Update
software
Vulnerability
scanning
Security
updates
ATT&CK®'s mitigations
for enterprises
a
Disable or
remove feature
or program
Limit access to
resource over
network
Limit
software
installation
Restrict
library 
loading
Restrict
web-based
content
Attack surface minimization
Environment
variable
permissions
Limit
hardware
installation
Restrict file 
and directory
permissions
Restrict 
registry
permissions
a
Anti-virus and
anti-malware
Behavioral
prevention on
endpoint
Code
signing
Exploit
protection
Network 
intrusion
prevention
SSL/TLS
inspection
Exploitation mitigation
Application
isolation and
sandboxing
Boot 
integrity
Execution
prevention
Filter 
network
traffic
Network
segmentation
Vulnerability
coordination
SBOMs
Do not
mitigate
Operating 
system
configuration
Password
policies
Secure defaults
Software
configuration
CRA's essential cyber
 security requirements
Out-of-band
communications
channel
Pre-compromise
Threat
intelligence
program
User
training
User account
management
Fig. 2. The Mappings Between the CRA’s Essential Cyber Security Requirements and the ATT&CK®’s Mitigations for Enterprises


---

Access
management
Active directory
configuration
Data 
backup
Data loss
prevention
Encrypt 
sensitive
information
The CIA triad
Multi-factor
authentication
Privileged
account
management
User account
control
Audit
Traceability
Data
minimization
Data 
erasure
Security 
testing
Application
developer
guidance
No known
vulnerabilities
Update
software
Vulnerability
scanning
Security
updates
a
Disable or
remove feature
or program
Limit access to
resource over
network
Restrict
library 
loading
Restrict
web-based
content
Attack surface minimization
Limit
hardware
installation
Restrict file 
and directory
permissions
Restrict 
registry
permissions
a
Anti-virus and
anti-malware
Code
signing
Exploit
protection
Network 
intrusion
prevention
SSL/TLS
inspection
Exploitation mitigation
Application
isolation and
sandboxing
Boot 
integrity
Execution
prevention
Filter 
network
traffic
Network
segmentation
Vulnerability
coordination
SBOMs
Operating 
system
configuration
Password
policies
Secure defaults
Software
configuration
Out-of-band
communications
channel
Threat
intelligence
program
User
training
Authorization
enforcement
Communication
authenticity
Encrypt
network
traffic
Human user
authentication
Mechanical
protection
layers
Minimize
wireless signal
propagation
Mitigation 
limited or not
effective
Account use
policies
Network
allowlists
Operational
information
confidentiality
Redundancy
of service
Safety
instrumented
systems
Software process
and device
configuration
Static
network
configuration
Supply
chain
management
Validate
program
inputs
Watchdog
timers
ATT&CK®'s mitigations
for industrial 
control systems
CRA's essential cyber
 security requirements
User account
management
Fig. 3.
The Mappings Between the CRA’s Essential Cyber Security Requirements and the ATT&CK®’s Mitigations for Industrial Control Systems
(rectangles colored in white denote those mitigations that are absent in Fig. 2)


---

III. RESULTS
The manually and collaboratively done mappings are shown
in Figs. 2 and 3 for the ATT&CK®’s mitigations for enterprises
and industrial control systems, respectively. Before continuing
to unpack these mappings, a remark should be made: as
the ATT&CK® framework has grown substantially throughout
the years [3], the mappings apply only to the situation at
the of writing, May 2025. With this point in mind, it can
be started by remarking that agreement between the three
authors was very good: in total, only four disagreements
were recorded. In addition, five disagreements were raised
by the two reviewing authors about within-CRA and within-
ATT&CK® mappings, which indicates that the exclusions in
Fig. 1 are too restrictive. As has already been pointed out [8],
even the CRA’s requirements are related to each other.
The main conclusion to draw from the two figures is
that the alignment is generally very good. Regarding the
12 collated non-functional requirements of the CRA and the
44 mitigations for enterprises, only three mitigations could
not be mapped. These are the ATT&CK®’s mitigations to
have a threat intelligence platform, to build an out-of-band
communications channel for secure exchanges during incident
management, as also recommended by other frameworks [30],
and to provide training for users on matters such as phishing
and social engineering in general. All three gaps can be seen
to be on the organizational side. Also the CRA’s essential
requirements about security testing and vulnerability coor-
dination have been seen as being on an organizational side
instead of the technical product-side [8]. Thus, in addition
to the disagreements already noted, some ambivalence is
present regarding functional and non-functional but technical
requirements and organizational cyber security requirements.
Regarding the ATT&CK®’s mitigations for industrial con-
trol systems, the gaps are the same but with an addition
of mitigations that cannot be reasonably implemented. This
“mitigation limited or not effective” category connotes with
a concept of residual risk in cyber security risk management
research and practice [30], [31]. In other words, a risk—as
a probabilistic concept, still remains after a design and an
implementation of mitigations. Otherwise, the mitigations in
Fig. 3 are more comprehensive than the mitigations for enter-
prises. The CIA triad stands out in this regard. Unlike with the
enterprise mitigations, also supply chain security is accounted
for. It maps to the CRA’s obligation to establish a machine-
readable software bill of materials (SBOM). SBOMs are either
required or recommended also by other cyber security laws and
frameworks [22], [32]. That said, the two mitigation categories
are related also in a sense that the CRA is envisioned to reduce
supply chain management costs, risk management costs, and
incident management costs for users, including enterprises,
using the products covered by the law [33]. Also a few other
mitigations for industrial control systems can be explicitly
mentioned. Among these are recommendations to establish
safety segmentation and mechanical or physical protection
layers, to minimize unnecessary wireless signal propagation,
to prefer predefined allowlists regarding network destinations
to which a device can connect, and to ensure availability by
means such as watchdog timers and redundancy solutions.
Finally, regarding the CRA’s essential requirements, there
are three visible gaps: data minimization, data erasure, and
vulnerability coordination. None of these legal requirements
can be seen to directly and explicitly map to any of the miti-
gations. This observation supports an argument raised earlier
in the literature [5] about a need to continuously update the
ATT&CK® framework, including with respect to mitigations
and countermeasures. This updating point notwithstanding, as
said, the framework aligns well with the CRA in overall.
IV. CONCLUSION
The paper presented an alignment evaluation of the Cyber
Resilience Act and the ATT&CK® framework’s mitigations
for enterprises and industrial control systems. The conclusion
is clear: the two align generally well with each other (RQ.1).
This conclusion can be seen to also raise the CRA’s legitimacy
in a sense that its essential cyber security requirements are
well-known means to improve the cyber security of network-
connected products. With respect to the CRA, only data
minimization, data erasure, and vulnerability coordination are
absent among the ATT&CK®’s mitigations considered (RQ.2).
With respect to the mitigations, there are also some but not
many gaps (RQ.2). Among these gaps is a recommendation
related to residual risks. Since the CRA is a risk-based regula-
tion, meaning that also its essential cyber security requirements
should be prioritized according to risks identified, the residual
risk concept is worth explicitly singling out from the gaps.
Regarding future research, (a) it seems sensible to further
continue alignment studies with alternative cyber security
frameworks [34] and particularly standards. Such studies are
important because following the upcoming harmonized stan-
dards will in most cases provide a presumption of conformity
and compliance with the CRA, as is typical also in many
other domains in the European Union [35], [36]. However,
alignment evaluations are not sufficient alone; (b) once the
standards have been made, also they should be evaluated,
including with respect to their practical usefulness, preciseness
and clarity [12], rigor, scope, complexity, and other related
evaluation criteria for standards. In a similar vein, (c) it seems
that empirical evaluations are mostly absent with respect to the
ATT&CK®’s usefulness for practitioners. As was noted, the
framework operates at a rather high abstraction level, which
may—or may not—decrease its practical usefulness.
Regarding these three paths for future research, the concepts
of layering and layers could be used to move beyond mappings
and alignments—a high-level concept, such as a legal cyber
security requirement, should ideally descend into lower level
layers, including concrete, technical layers [18]. This point
also reiterates the importance of standards, which too should
arguably be specific enough but still applicable to a wide range
of products. Reaching a good balance in this regard may even
be crucial for a success of the CRA in improving the cyber
security of network-connected products in the future.


---

REFERENCES
[1] The European Union, “Regulation (EU) 2024/2847 of the European Par-
liament and of the Council of 23 October 2024 on Horizontal Cyberse-
curity Requirements for Products With Digital Elements and Amending
Regulations (EU) No 168/2013 and (EU) 2019/1020 and Directive (EU)
2020/1828 (Cyber Resilience Act) (Text With EEA Relevance).” Avail-
able online: https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng, 2024.
[2] MITRE, “ATT&CK®.” Available online: https://attack.mitre.org/, 2025.
[3] B. Al-Sada, A. Sadighian, and G. Oligeri, “MITRE ATT&CK: State of
the Art and Way Forward,” ACM Computing Surveys, vol. 57, no. 1,
pp. 1–37, 2024.
[4] Y. Jiang, Q. Meng, F. Shang, N. Oo, L. T. H. Minh, H. W. Lim, and
B. Sikdar, “MITRE ATT&CK Applications in Cybersecurity and the
Way Forward.” Archived manuscript, available online: https://doi.org/
10.48550/arXiv.2502.10825, 2025.
[5] S. Roy, E. Panaousis, C. Noakes, A. Laszka, S. Panda, and G. Loukas,
“SoK: The MITRE ATT&CK Framework in Research and Practice.”
Archived manuscript, available online in May 2025: https://doi.org/10.
48550/arXiv.2304.07411, 2023.
[6] A. P. Golushko and V. G. Zhukov, “Application of Advanced Persistent
Threat Actors’ Techniques aor Evaluating Defensive Countermeasures,”
in Proceedings of the IEEE Conference of Russian Young Researchers in
Electrical and Electronic Engineering (EIConRus 2020), (St. Petersburg
and Moscow), pp. 312–317, IEEE, 2020.
[7] M. Kern, M. Landauer, F. Skopik, and E. Weippl, “A Logging Maturity
and Decision Model for the Selection of Intrusion Detection Cyber
Security Solutions,” Computers & Security, vol. 141, p. 103844, 2024.
[8] J. Ruohonen, K. Hjerppe, and E.-Y. Kang, “A Mapping Analysis of
Requirements Between the CRA and the GDPR,” in Proceedings of
the IEEE 33rd International Requirements Engineering Conference
Workshops (REW 2025), (Valencia), IEEE, 2025.
[9] J. Ruohonen, K. Rindell, and S. Busetti, “From Cyber Security Incident
Management to Cyber Security Crisis Management in the European
Union.” Archived manuscript, available online: https://doi.org/10.48550/
arXiv.2504.14220, 2025.
[10] J. Ruohonen and P. Timmers, “Vulnerability Coordination Under the
Cyber Resilience Act.” Archived manuscript, available online: https://
doi.org/10.48550/arXiv.2412.06261, 2024.
[11] ENISA and JRC, “Cyber Resilience Act Requirements Standards
Mapping.”
European
Union
Agency
for
Cybersecurity
(ENISA)
and
Joint
Research
Center
(JRC)
of
the
European
Comission.
Available online in March 2025: https://www.enisa.europa.eu/sites/
default/files/2024-11/Cyber%20Resilience%20Act%20Requirements%
20Standards%20Mapping%20-%20final with identifiers 0.pdf, 2024.
[12] ETSI, “Cyber Security (CYBER); Standards Mapping and Gap Anal-
ysis Against Regulatory Expectations.” European Telecommunications
Standards Institute (ETSI), ETSI TR 103 990 V1.1.1 (2024-03), avail-
able online in May 2025: https://www.etsi.org/deliver/etsi tr/103900
103999/103990/01.01.01 60/tr 103990v010101p.pdf, 2024.
[13] ORC WG, “CRA Hub.” The Open Regulatory Compliance Working
Group (ORC WG) of the Eclipse Foundation, available online: https:
//github.com/orcwg/, 2025.
[14] A. Lawson and S. Hendrick, “Unaware and Uncertain: The Stark
Realities of Cyber Resilience Act Readiness in Open Source.” The Linux
Foundation, available online: https://www.linuxfoundation.org/hubfs/
Research%20Reports/lfr cra readiness 050125a.pdf?hsLang=en, 2025.
[15] R. Wieringa, N. Maiden, N. Mead, and C. Rolland, “Requirements
Engineering Paper Classification and Evaluation Criteria: A Proposal
and a Discussion,” Requirements Engineering, vol. 11, pp. 102–107,
2006.
[16] K. Hjerppe, J. Ruohonen, and V. Lepp¨anen, “The General Data Pro-
tection Regulation: Requirements, Architectures, and Constraints,” in
Proceedings of the 27th IEEE International Requirements Engineering
Conference (RE 2019), (Jeju Island), pp. 265–275, IEEE, 2019.
[17] D. Netto, C. Silva, and J. Ara´ujo, “Identifying How the Brazilian
Software Industry Specifies Legal Requirements,” in Proceedings of the
XXXIII Brazilian Symposium on Software Engineering (SBES 2019),
(Salvador), pp. 181–186, ACM, 2019.
[18] M. Schumacher, Security Engineering with Patterns: Origins, Theoreti-
cal Model, and New Applications. Berlin: Springer, 2003.
[19] H. Boyes and M. D. Higgins, “An Overview of Information and Cyber
Security Standards,” Journal of ICT Standardization, vol. 12, no. 1,
pp. 95–134, 2024.
[20] M. Ahmed, S. Panda, C. Xenakis, and E. Panaousis, “ATT&CK-Driven
Cyber Risk Assessment,” in Proceedings of the 17th International Con-
ference on Availability, Reliability and Security (ARES 2022), (Vienna),
pp. 1–10, ACM, 2022.
[21] A. Mussmann, M. Brunner, and R. Breu, “Mapping the State
of
Security
Standards
Mappings,”
in
Proceedings
of
the
15th
International Conference on Wirtschaftsinformatik, (Potsdam), 2020.
Available online: https://library.gito.de/wp-content/uploads/2021/08/L4
Mussmann-Mapping the State of Security Standards Mappings-305
c.pdf.
[22] L. Williams, S. Migues, J. Boote, and B. Hutchison, “Proactive Software
Supply Chain Risk Management Framework (P-SSCRM).” Archived
manuscript, available online in May 2025: https://doi.org/10.48550/
arXiv.2404.12300, 2025.
[23] M. Unterkalmsteiner, T. Gorschek, R. Feldt, and E. Klotins, “Assessing
Requirements Engineering and Software Test Alignment—Five Case
Studies,” Journal of Systems and Software, vol. 109, pp. 62–77, 2015.
[24] G. Jadoon, M. Shafi, and S. Jan, “A Model-Oriented Requirements
Traceability Framework for Small and Medium Software Industries,”
in Proceedings of the International Arab Conference on Information
Technology (ACIT 2019), (Al Ain), pp. 91–96, IEEE, 2019.
[25] M. A. Javed and U. Zdun, “A Systematic Literature Review of Trace-
ability Approaches Between Software Architecture and Source Code,”
in Proceedings of the 18th International Conference on Evaluation and
Assessment in Software Engineering (EASE 2014), (London), pp. 1–10,
ACM, 2024.
[26] E. Kempe, S. Semsar, A. Massey, S. Sampath, and C. Seaman, “Model-
ing, Analyzing and Communicating Regulatory Ambiguity: An Empir-
ical Study,” in Proceedings of the 1st IEEE/ACM Workshop on Multi-
disciplinary, Open, and RElevant Requirements Engineering (MO2RE
2024), (Lisbon), pp. 28–34, ACM, 2024.
[27] J. Ruohonen, G. Choudhary, and A. Alami, “An Overview of Cyber
Security Funding for Open Source Software.” Archived manuscript,
available online: https://doi.org/10.48550/arXiv.2412.05887, 2025.
[28] C. Gaebert, “Dilemma Structures Between Contracting Parties in Soft-
ware Development Projects,” in Proceedings of the 9th International
Conference on Software Engineering and Applications (ICSOFT-EA
2014), (Vienna), pp. 539–548, IEEE, 2014.
[29] C. Rolland, C. Salinesi, and A. Etie, “Eliciting Gaps in Requirements
Change,” Requirements Engineering, vol. 9, pp. 1–15, 2004.
[30] P. Cichonski, T. Millar, T. Grance, and K. Scarfone, “Computer Security
Incident Handling Guide Recommendations of the National Institute
of Standards and Technology.” National Institute of Standards and
Technology (NIST), Special Publication 800-61, available online in
January 2025: https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.
sp.800-61r2.pdf, 2012.
[31] A. Khan, J. Bryans, and G. Sabaliauskaite, “Framework for Calculating
Residual Cybersecurity Risk of Threats to Road Vehicles in Alignment
with ISO/SAE 21434,” in Proceedings of the Applied Cryptography
and Network Security Workshops (ACNS 2022), (Rome), pp. 235–247,
Springer, 2022.
[32] N. Zahan, E. Lin, M. Tamanna, W. Enck, and L. Williams, “Software
Bills of Materials Are Required. Are We There Yet?,” IEEE Security &
Privacy, vol. 21, no. 2, pp. 82–88, 2023.
[33] ENISA, “2024 Report on the State of Cybersecurity in the Union.”
The European Union Agency for Cybersecurity (ENISA), available
online in May 2025: https://www.enisa.europa.eu/sites/default/files/
2024-11/2024%20Report%20on%20the%20State%20of%20the%
20Cybersecurity%20in%20the%20Union.pdf, 2024.
[34] NIST, “Cybersecurity Framework.” National Institute of Standards
and
Technology,
available
online
in
July:
https://www.nist.gov/
cyberframework, 2025.
[35] S. Hallensleben, “Generative AI and International Standardization,”
Cambridge Forum on AI: Law and Governance, vol. 1, pp. 1–5, 2025.
[36] J. Ruohonen, “A Review of Product Safety Regulations in the European
Union,” International Cybersecurity Law Review, vol. 3, pp. 345–366,
2022.
