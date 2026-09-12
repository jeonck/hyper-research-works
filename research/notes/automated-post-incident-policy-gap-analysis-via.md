---
title: Automated Post-Incident Policy Gap Analysis via
id: automated-post-incident-policy-gap-analysis-via
tags:
- attack-ontology-drift-cti-85bc51
- pin-rate-survey
created: '2026-09-12T21:34:18.833479Z'
updated: '2026-09-12T21:44:27.123443Z'
source: https://arxiv.org/abs/2601.03287v1
source_domain: arxiv.org
fetched_at: '2026-09-12T21:34:18.833080Z'
fetch_provider: crawl4ai
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'arXiv 2601.03287v1 (2026): uses 4 ATT&CK technique-ID occurrences (without
  sub-techniques); ATT&CK release declaration classified as none.'
raw_file: raw/automated-post-incident-policy-gap-analysis-via.pdf
doi: arXiv:2601.03287v1
---

Automated Post-Incident Policy Gap Analysis via
Threat-Informed Evidence Mapping using Large
Language Models
Oh Huan Lin, Jay Yong Jun Jie, Lee Ling Siu Mandy, Dr Jonathan Pan
Nanyang Technological University, Singapore
Emails: W240001@e.ntu.edu.sg, JAYY0002@e.ntu.edu.sg, MANDY001@e.ntu.edu.sg, JonathanPan@ntu.edu.sg
Abstract—Cybersecurity post-incident reviews are essential
for identifying control failures and improving organisational
resilience, yet they remain labour-intensive, time-consuming, and
heavily reliant on expert judgment. This paper investigates
whether Large Language Models (LLMs) can augment post-
incident review workflows by autonomously analysing system
evidence and identifying security policy gaps. We present a
threat-informed, agentic framework that ingests log data, maps
observed behaviours to the MITRE ATT&CK framework, and
evaluates organisational security policies for adequacy and com-
pliance. Using a simulated brute-force attack scenario against
a Windows OpenSSH service (MITRE ATT&CK T1110), the
system leverages GPT-4o for reasoning, LangGraph for multi-
agent workflow orchestration, and LlamaIndex for traceable pol-
icy retrieval. Experimental results indicate that the LLM-based
pipeline can interpret log-derived evidence, identify insufficient
or missing policy controls, and generate actionable remediation
recommendations with explicit evidence-to-policy traceability.
Unlike prior work that treats log analysis and policy validation
as isolated tasks, this study integrates both into a a unified
end-to-end proof-of-concept post-incident review framework. The
findings suggest that LLM-assisted analysis has the potential
to improve the efficiency, consistency, and auditability of post-
incident evaluations, while highlighting the continued need for
human oversight in high-stakes cybersecurity decision-making.
Index Terms—Large Language Models, Agentic AI, Cybersecu-
rity, Post-Incident Review, Policy Compliance, MITRE ATT&CK
I. INTRODUCTION
Cybersecurity post-incident reviews are essential for iden-
tifying control failures, understanding attacker behaviour, and
improving organisational security posture [1], [2]. In practice,
these reviews remain largely manual and expert-driven, par-
ticularly when correlating large volumes of system logs with
organisational security policies [3], [4]. As cyber threats evolve
rapidly, static and infrequently reviewed policies increasingly
struggle to reflect real-world attack techniques and operational
conditions [5], [6].
Recent advances in Large Language Models (LLMs) have
demonstrated strong capabilities in reasoning over semi-
structured data and orchestrating multi-step analytical tasks,
suggesting potential applicability in post-incident analysis
workflows [7], [8]. While prior work has explored LLMs
for isolated tasks such as log analysis or policy compliance
checking [9], [10], limited research has examined their use
in integrated post-incident review workflows that connect
technical evidence with governance-oriented policy evaluation.
This paper investigates whether an LLM-driven, agentic
workflow can support post-incident reviews by analysing log-
derived evidence, mapping observed behaviours to the MITRE
ATT&CK framework, and identifying gaps in organisational
security policies in a traceable and auditable manner. Rather
than replacing human analysts, the approach is intended as a
feasibility-focused, decision-support framework that augments
evidence interpretation and policy evaluation.
The contributions of this paper are as follows:
• An end-to-end, agentic post-incident review workflow
integrating log analysis, threat attribution, and policy gap
identification.
• A threat-informed evidence-to-policy mapping approach
grounded in the MITRE ATT&CK framework.
• An interpretable and auditable workflow design to support
governance and compliance-oriented post-incident evalu-
ation.
II. RELATED WORK
A. LLMs in Cybersecurity Analysis
Recent studies demonstrate that Large Language Models
(LLMs) can support a range of cybersecurity tasks, including
log interpretation, vulnerability analysis, and partial audit au-
tomation [11]. Survey literature further reports that LLMs can
enhance analyst productivity by reasoning over complex, semi-
structured security data and coordinating multi-step analytical
workflows [12], [13]. Agentic LLM architectures have enabled
systems that map vulnerabilities to the MITRE ATT&CK
framework or simulate attacker behaviour in controlled en-
vironments [14].
While these approaches highlight the technical potential
of LLMs, they primarily focus on isolated analytical tasks
and do not explicitly connect observed incident evidence to
organisational governance or security policy evaluation.
B. AI-Assisted Audits and Policy Compliance
An emerging body of work explores the use of LLMs
to support security audits and compliance management [10],
[15]. Prior studies show that LLMs can assist in interpreting
regulatory texts, mapping standards such as NIST or CIS
controls to operational procedures, and automating portions of
arXiv:2601.03287v1  [cs.CR]  4 Jan 2026


---

audit planning and reporting. Industry position papers similarly
argue that LLM-based compliance tools can reduce manual
effort and improve consistency in policy assessment [15].
However, most existing approaches treat compliance as a
document-centric task, focusing on policy-to-policy or control-
to-standard comparisons. These systems rarely incorporate
post-incident technical evidence, limiting their ability to as-
sess whether documented controls remain effective under real
attack conditions.
C. Threat-Informed Post-Incident Auditing and Governance
Traditional cybersecurity auditing frameworks adopt a top–
down, policy-centric approach, where compliance is assessed
against predefined controls through periodic and manually in-
tensive reviews [3]. Industry postmortem practices emphasize
organisational learning and process improvement following in-
cidents, but remain largely qualitative and human-driven, with
limited mechanisms for evidence traceability or repeatable
policy validation [2].
Threat modeling frameworks such as MITRE ATT&CK
provide a standardized abstraction layer between low-level
system events and higher-level adversarial techniques [16].
Despite this, existing audit and postmortem methodologies
rarely operationalise threat-informed evidence mapping in
an automated or auditable manner, leaving policy evaluation
largely decoupled from observed attacker behaviour.
D. Gaps in Automated Post-Incident Review
Despite advances in LLM-based security analytics and
compliance automation, fully integrated post-incident review
workflows remain underexplored. Existing research typically
addresses log analysis, threat detection, or policy compliance
as separate problem domains, lacking end-to-end frameworks
that unify evidence interpretation with policy gap identifi-
cation. Practical challenges, including model hallucination,
limited context windows, and insufficient traceability, further
hinder adoption in audit-critical environments [17], [18].
Traditional statistical and deep learning approaches to log
analysis are effective for anomaly detection but lack the
semantic reasoning required to relate observed behaviour to or-
ganisational policy adequacy [19]. Few studies provide explicit
mechanisms for linking analytical conclusions to verifiable log
evidence and policy clauses, which is essential for forensic
soundness and governance accountability. This work addresses
this gap by integrating log-derived evidence, threat abstraction,
and policy evaluation into a single, traceable LLM-assisted
post-incident review framework.
III. RESEARCH AIM AND SCOPE
The primary aim of this research is to evaluate whether
Large Language Models (LLMs) can effectively augment
cybersecurity post-incident review processes by autonomously
analysing system evidence and identifying gaps in organisa-
tional security policies. Specifically, this study investigates
the feasibility of using an agentic LLM-driven workflow to
interpret log-derived evidence, map observed behaviours to
established threat frameworks, and assess the adequacy of
documented security controls. Rather than replacing human
analysts, the research aims to determine whether LLMs can
improve the efficiency, consistency, and traceability of post-
incident evaluations by providing evidence-grounded and au-
ditable insights that support cybersecurity governance and
decision-making.
The scope of this study is limited to a simulated post-
incident review scenario involving a brute-force authentication
attack against a Windows OpenSSH service, mapped to the
MITRE ATT&CK technique T1110. The analysis focuses on
Windows Event Log (EVTX) data as the primary source of
technical evidence and evaluates organisational user account
policies against baseline security controls. The system is im-
plemented using a single large language model for reasoning
and does not perform model fine-tuning or comparative bench-
marking across multiple models. This research emphasises
feasibility, interpretability, and workflow integration rather
than detection accuracy or large-scale performance evaluation.
IV. METHODOLOGY
A. Experimental Design
This study employs an experimental design to assess the
feasibility of using a Large Language Model (LLM)-driven,
agentic workflow to support cybersecurity post-incident re-
views. The experiment simulates a realistic incident scenario
in which system-generated evidence is analysed and compared
against organisational security policies to identify control
gaps. The workflow is structured to mirror the reasoning
process of a human security analyst, progressing from evi-
dence interpretation to threat attribution and policy evaluation.
Evaluation focuses on interpretability, evidence traceability,
and the ability to produce auditable and actionable outputs
rather than detection accuracy or performance benchmarking.
B. Agentic Workflow Architecture
The proposed system is implemented as a multi-agent
pipeline orchestrated using LangGraph. [20], [21] Each agent
performs a distinct function, including log interpretation, threat
attribution, policy retrieval, and policy gap identification, while
maintaining a shared global state. GPT-4o is used as the
primary reasoning model, and LlamaIndex supports semantic
indexing and retrieval of organisational policy documents
with line-level metadata. This modular architecture enables
structured information flow across analysis stages and sup-
ports traceable reasoning throughout the post-incident review
process.
Recent empirical evaluations of multi-step reasoning in
large language models indicate that newer models exhibit
greater resilience to reasoning complexity and reduced in-
consistency across chained inference tasks, supporting their
suitability for structured analytical workflows. [22] Prior
benchmarking studies in domain-specific classification tasks
suggest that GPT-4o demonstrates strong consistency and
reasoning performance, reinforcing its selection for evidence-
driven reasoning in audit-critical contexts. [23]


---

Unlike linear LLM pipelines, the agentic design allows
intermediate outputs to be validated and reused across stages,
reducing redundant inference and limiting error propagation.
Persistent state management enables explicit tracking of ev-
idence, policy excerpts, and intermediate findings, which is
particularly important in audit and compliance contexts where
traceability is required.
C. Incident Data and Threat Attribution
The experiment uses Windows Event Log (EVTX) data
representing a brute-force authentication attack against a Win-
dows OpenSSH service. As EVTX files are stored in binary
format, the logs are converted to XML and subsequently
flattened into CSV format using a deterministic preprocessing
script. The log analysis agent examines authentication-related
events to identify temporal patterns and behavioural indicators
of brute-force activity. Detected behaviours are mapped to the
MITRE ATT&CK framework, specifically Technique T1110
(Brute Force), providing a standardised threat context for
policy evaluation. [16]
Authentication logs were selected because they are com-
monly available in enterprise environments and frequently
used in incident investigations. The selected dataset contains
repeated authentication failures followed by a successful lo-
gin, a pattern commonly associated with credential guessing
attacks. This makes it suitable for evaluating both threat
attribution and policy adequacy, particularly for access control
and authentication policies.
D. Policy Evaluation and Evidence Traceability
Organisational security policies and baseline best-practice
controls are ingested in PDF format and indexed using
LlamaIndex. Relevant policy clauses are retrieved based on
semantic similarity to the detected threat behaviour. The policy
evaluation agent compares the organisation’s controls against
the baseline to identify insufficient or missing safeguards.
Each identified gap is supported by explicit references to log-
derived evidence and policy excerpts, along with a confidence
assessment to support human validation. This design ensures
that findings remain evidence-driven, auditable, and suitable
for governance and compliance contexts in post-incident au-
thentication policy evaluation.
Baseline security controls referenced in this study are de-
rived from widely adopted governance frameworks, including
NIST SP 800-53, ISO/IEC 27001, and the CIS Critical Se-
curity Controls, which define best-practice requirements for
access control and credential management. [24]–[26]
E. Implementation Details and Prompt Control
To ensure reproducibility and audit suitability, the imple-
mentation places strict boundaries around data preprocessing,
prompt structure, and model inference behaviour. All log pre-
processing steps are deterministic and performed outside the
Large Language Model (LLM). Windows Event Log (EVTX)
files are converted to XML and subsequently flattened into
CSV format using a fixed Python script, preserving key fields
such as Event ID, timestamp, target account, and authentica-
tion status. This design avoids introducing variability at the
data ingestion stage and ensures that identical evidence is
supplied across repeated executions.
Prompting is structured at a high level to reflect the role
of each agent in the workflow. Rather than using open-ended
instructions, each agent receives task-specific prompts that
constrain its responsibility, such as summarising authentication
events, mapping observed behaviour to the MITRE ATT&CK
framework, or comparing retrieved policy clauses. Prompts
explicitly instruct the model to reference observable evidence
and retrieved policy text, discouraging speculative reasoning
and unsupported conclusions.
Model inference is performed using a fixed temperature
setting to minimise output variability across runs. Although
minor variations in phrasing may still occur due to the
probabilistic nature of LLMs, constraining sampling behaviour
improves consistency in findings and supports repeatable
analysis. This combination of deterministic preprocessing,
structured prompting, and controlled inference contributes to
the overall traceability and reliability of the proposed post-
incident review workflow.
Start
Process Evidence
Map to MITRE ATT&CK
Retrieve Relevant Policies
Validate Policies Against Evidence
Generate Report
End
Fig. 1. End-to-end workflow for evidence-driven policy compliance analysis
V. FINDINGS
A. Threat Identification and Interpretation
The LLM-driven workflow successfully identified the simu-
lated brute-force authentication attack by analysing Windows
Event Log patterns. Repeated failed logon attempts (Event ID
4625) followed by a successful authentication (Event ID 4624)
within a short time window were consistently interpreted as


---

indicative of brute-force behaviour. The model was able to
summarise these patterns, with traceable reasoning, despite
incomplete or noisy log fields, demonstrating an ability to rea-
son over semi-structured evidence rather than relying on strict
rule-based signatures. The identified behaviour was correctly
mapped to MITRE ATT&CK Technique T1110 (Brute Force),
providing a standardised threat classification that supported
downstream policy evaluation.
B. Policy Gap Identification
Based on the detected threat behaviour, the system retrieved
relevant clauses from both the baseline policy and the organ-
isation’s target policy and performed comparative analysis.
The workflow identified multiple policy gaps, including an
overly permissive account lockout threshold and an infrequent
password rotation requirement. These findings were framed as
risk-based deficiencies rather than binary compliance failures,
highlighting how existing controls could be insufficient under
observed attack conditions. Each gap was accompanied by a
concise rationale and a recommended remediation aligned with
industry best practices.
C. Evidence-to-Policy Traceability
All identified policy gaps were explicitly linked to sup-
porting log evidence and policy excerpts. The system pro-
vided references to specific event patterns and policy clauses,
enabling independent verification by human reviewers. This
evidence-to-policy traceability reduced reliance on generative
explanations and improved auditability. Confidence levels as-
signed to each finding reflected the quantity and consistency of
supporting evidence, supporting prioritisation during review.
D. Operational Implications
The findings indicate that LLM-assisted, agentic workflows
can meaningfully augment post-incident review processes by
reducing manual effort while preserving interpretability and
governance requirements. The structured outputs demonstrate
potential for integration into audit and compliance workflows,
particularly as a decision-support mechanism rather than a
fully autonomous system. Human oversight remains essential,
but the results suggest that LLMs can accelerate incident-
driven policy evaluation and improve the consistency of post-
incident analyses.
VI. DISCUSSION
The findings of this study demonstrate that Large Language
Models (LLMs) can meaningfully augment cybersecurity post-
incident reviews by bridging technical evidence analysis and
organisational policy evaluation. Unlike traditional approaches
that treat log analysis and compliance assessment as sepa-
rate activities, the proposed agentic workflow integrates both
within a single, traceable reasoning process. This integration
enables incident-driven policy evaluation, allowing organisa-
tions to assess not only whether controls exist, but whether
they are sufficient under observed attack conditions.
A key contribution of this work is the emphasis on evidence-
to-policy traceability. By grounding each identified policy gap
in verifiable log patterns and specific policy clauses, the system
addresses a common barrier to adopting LLMs in audit-critical
environments: trust. Rather than relying on opaque generative
explanations, the workflow produces structured, auditable out-
puts that can be independently validated by human analysts.
This positions LLMs as decision-support tools that enhance
analyst efficiency while preserving accountability.
The results also highlight the practical role of agentic
orchestration in managing complex reasoning tasks. By de-
composing the post-incident review into modular stages, the
system mirrors human analytical workflows and supports ex-
tensibility to additional evidence sources or policy domains.
However, the study reinforces that LLM-assisted analysis
should complement, not replace, human judgment. Expert
oversight remains essential for contextual interpretation, risk
acceptance decisions, and governance accountability. Overall,
the findings suggest that LLM-driven post-incident review
has strong potential to improve the timeliness, consistency,
and governance alignment of cybersecurity operations when
deployed within well-defined procedural and oversight frame-
works.
VII. LIMITATIONS
This study has several limitations that affect the generalis-
ability and operational applicability of the proposed approach.
First, the evaluation is limited to a single simulated incident
scenario involving Windows Event Logs and a brute-force
authentication attack. While this scenario is representative
of common enterprise threats, the findings may not directly
extend to more complex, multi-stage attacks or heterogeneous
log sources such as network telemetry or cloud-native audit
logs.
Second, the workflow relies on a single large language
model for reasoning and does not include comparative bench-
marking across alternative models or configurations. The
probabilistic nature of LLM outputs introduces variability
across runs, which may affect consistency in high-stakes audit
contexts. Although structured prompts and validation steps
mitigate this issue, full determinism is not guaranteed.
Third, the quality of policy gap identification is inherently
dependent on the completeness and clarity of the organisa-
tional policy documents ingested. Ambiguous, outdated, or
poorly structured policies may limit retrieval accuracy and
lead to incomplete assessments. Additionally, the system does
not perform quantitative performance evaluation or measure
time savings relative to human analysts, focusing instead on
feasibility and interpretability.
Finally, operational deployment raises broader considera-
tions around data governance, privacy, and accountability. In-
cident logs and policy documents often contain sensitive infor-
mation, requiring robust access controls and secure handling
when integrated with external model APIs. These limitations
indicate that while the approach is promising, further research
is needed to validate scalability, reliability, and governance
readiness in real-world enterprise environments.


---

VIII. FUTURE WORK
Future research can extend this work along several di-
mensions to improve robustness, scalability, and real-world
applicability. First, the proposed workflow should be evalu-
ated across a broader range of incident scenarios, including
multi-stage attacks and heterogeneous evidence sources such
as network logs, endpoint telemetry, and cloud audit trails.
Incorporating cross-system correlation would enable more
comprehensive incident reconstruction and strengthen policy
evaluation in complex enterprise environments.
Second, future studies should explore controlled compar-
isons across multiple large language models and configura-
tions to assess reasoning consistency, reliability, and cost-
performance trade-offs. Techniques such as ensemble infer-
ence, deterministic decoding, or verification-based prompting
could further reduce output variability in audit-critical con-
texts. Additionally, integrating retrieval-augmented generation
more tightly into the reasoning process may improve ground-
ing and reduce unsupported conclusions.
Third, quantitative evaluation metrics should be introduced
to complement qualitative findings. These may include analyst
time savings, consistency of findings across runs, and agree-
ment between LLM-assisted outputs and expert assessments.
Finally, future work should examine governance and deploy-
ment considerations, including secure on-premise or private-
cloud deployments, access control mechanisms, and human-in-
the-loop validation frameworks. Addressing these areas would
support the transition of LLM-assisted post-incident review
from proof-of-concept to operational use.
IX. CONCLUSION
This paper investigated the feasibility of using Large Lan-
guage Models (LLMs) to augment cybersecurity post-incident
reviews through an evidence-driven, agentic workflow. By in-
tegrating log analysis, threat attribution, and policy evaluation
within a single framework, the study demonstrates how LLMs
can support incident-driven identification of security policy
gaps with explicit evidence-to-policy traceability. The find-
ings indicate that such workflows can improve the efficiency,
consistency, and auditability of post-incident analysis while
preserving the need for human oversight.
Rather than positioning LLMs as autonomous decision-
makers, this work highlights their value as decision-support
tools that assist analysts in navigating complex evidence
and governance requirements. While limitations remain in
scalability, determinism, and data governance, the results
suggest meaningful potential for LLM-assisted post-incident
review to enhance cybersecurity operations. This study lays
a foundation for future research into trustworthy, transparent,
and governance-aligned applications of agentic AI in security
analysis.
X. CODE AVAILABILITY
The GitHub repository will be made publicly available after
acceptance of the paper at a peer-reviewed conference.
REFERENCES
[1] C. Connolly, “Post-incident review: Boost your cybersecurity resilience,”
2025, cyber Defense Group. Available: https://www.cdg.io/blog/post-
incident-review/.
[2] Atlassian, “The importance of an incident postmortem process,”
n.d.,
online.
Available:
https://www.atlassian.com/incident-
management/postmortem.
[3] M. Antunes, M. Maximiano, and R. Gomes, “A client-centered informa-
tion security and cybersecurity auditing framework,” Applied Sciences,
vol. 12, no. 9, p. 4102, 2022.
[4] D. T. Hanson, “Normalizing cybersecurity: Improving cyber incident
response with the incident command system,” 2021, homeland Security
Digital Library.
[5] I. Linkov, E. Anklam, and Z. A. Collier, “Risk-based standards: Inte-
grating top–down and bottom–up approaches,” Environment Systems &
Decisions, vol. 34, no. 1, pp. 134–137, 2014.
[6] J. Hill, “New research shows brute force attacks rise 671%,” 2021,
abnormal AI Blog.
[7] J. Huang and K.-W. Chang, “Towards reasoning in large language
models: A survey,” Findings of ACL, 2023.
[8] J. Wei, X. Wang, D. Schuurmans et al., “Chain-of-thought prompting
elicits reasoning in large language models,” arXiv, 2022.
[9] J. Zhang, H. Bu, H. Wen et al., “When llms meet cybersecurity: A
systematic literature review,” Cybersecurity, vol. 8, no. 1, p. 55, 2025.
[10] E. Cadet, E. D. Etim, I. A. Essien et al., “Large language models
for cybersecurity policy compliance and risk mitigation,” International
Journal of Scientific Research in Humanities and Social Sciences, vol. 1,
no. 2, pp. 612–643, 2024.
[11] J. H. Chin, P. Zhang, Y. X. Cheong, and J. Pan, “Automating security
audit using large language model based agent,” 2025, arXiv:2505.10732.
[12] J. Ruan, Y. Chen, B. Zhang et al., “Tptu: Large language model-based
ai agents for task planning and tool usage,” 2023, arXiv:2308.03427.
[13] R. Fang, R. Bindu, A. Gupta, Q. Zhan, and D. Kang, “Llm agents can
autonomously hack websites,” 2024, arXiv:2402.06664.
[14] J. Jin, B. Tang, M. Ma et al., “Crimson: Empowering strategic reasoning
in cybersecurity through large language models,” ICCBD+AI, pp. 18–24,
2024.
[15] A. Salman, S. Creese, and M. Goldsmith, “Leveraging large language
models for cybersecurity compliance,” IEEE European Symposium on
Security and Privacy Workshops, pp. 496–503, 2024.
[16] MITRE, “Mitre att&ck framework,” 2024, https://attack.mitre.org.
[17] F. Y. Loumachi, M. C. Ghanem, and M. A. Ferrag, “Advancing cyber
incident timeline analysis through retrieval-augmented generation and
large language models,” Computers, vol. 14, no. 2, p. 67, 2025.
[18] W. Zhang and J. Zhang, “Hallucination mitigation for retrieval-
augmented large language models: A review,” Mathematics, vol. 13,
no. 5, p. 856, 2025.
[19] L. Chourasiya, S. Khatri, U. K. Lilhore et al., “Advanced system log
analyzer for anomaly detection and cyber forensic investigations using
lstm and transformer networks,” Journal of Cloud Computing, vol. 14,
no. 1, p. 60, 2025.
[20] LangChain, “Langgraph: Build resilient language agents as graphs,”
2025, gitHub Repository.
[21] T. Taulli and G. Deshmukh, “Introduction to langgraph,” in Building
Generative AI Agents.
Apress, 2025.
[22] P. Hoza, “Evaluating reasoning in large language models with a modified
think-a-number game,” Acta Informatica Pragensia, vol. 14, no. 2, pp.
246–260, 2025.
[23] K.-H. Lin, T.-H. Kao, L.-C. Wang et al., “Benchmarking large language
models gpt-4o, llama 3.1, and qwen 2.5 for cancer genetic variant
classification,” NPJ Precision Oncology, vol. 9, p. 141, 2025.
[24] NIST, “Security and privacy controls for information systems and
organizations (sp 800-53),” 2020.
[25] ISO, “Iso/iec 27001:2022 information security management systems,”
2022.
[26] Center for Internet Security, “Cis critical security controls v8.1,” 2023.
