---
title: JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021
id: journal-of-latex-class-files-vol-14-no-8-august-2021-2
tags:
- attack-ontology-drift-cti-85bc51
- pin-rate-survey
created: '2026-09-12T21:33:37.366921Z'
updated: '2026-09-12T21:44:24.307786Z'
source: https://arxiv.org/abs/2510.14233v1
source_domain: arxiv.org
fetched_at: '2026-09-12T21:33:37.366524Z'
fetch_provider: crawl4ai
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'arXiv 2510.14233v1 (2025): uses 45 ATT&CK technique-ID occurrences (with
  sub-techniques); ATT&CK release declaration classified as none.'
raw_file: raw/journal-of-latex-class-files-vol-14-no-8-august-2021-2.pdf
doi: arXiv:2510.14233v1
---

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021
1
RHINO: Guided Reasoning for Mapping Network Logs to Adversarial
Tactics and Techniques with Large Language Models
Fanchao Meng1, Jiaping Gui1, Yunbo Li1, and Yue Wu1
1Shanghai Jiao Tong University
Abstract—Modern Network Intrusion Detection Systems (NIDS)
generate vast volumes of low-level alerts, yet these outputs remain
semantically fragmented, requiring labor-intensive manual correla-
tion with high-level adversarial behaviors. Existing solutions for au-
tomating this mapping—rule-based systems and machine learning
classifiers—suffer from critical limitations: rule-based approaches
fail to adapt to novel attack variations, while machine learning
methods lack contextual awareness and treat tactic-technique
(TT) mapping as a syntactic matching problem rather than a
reasoning task. Although Large Language Models (LLMs) have
shown promise in cybersecurity tasks, preliminary experiments
reveal that existing LLM-based methods frequently hallucinate
technique names or produce decontextualized mappings due to
their single-step classification approach.
To address these challenges, we introduce RHINO, a novel
framework that decomposes LLM-based attack analysis into
three interpretable phases mirroring human reasoning: (1)
behavioral abstraction, where raw logs are translated into
contextualized narratives; (2) multi-role collaborative inference,
generating candidate techniques by evaluating behavioral evidence
against MITRE ATT&CK knowledge; and (3) validation, cross-
referencing predictions with official MITRE definitions to rectify
hallucinations. RHINO bridges the semantic gap between low-
level observations and adversarial intent while improving output
reliability through structured reasoning.
We evaluate RHINO on three benchmarks (DAPT2020, CI-
CIDS2017, IoT23) across four backbone models (ChatGPT-4o,
Gemini 2.5 Flash, Claude Sonnet 4, and DeepSeek V3). RHINO
achieved high accuracy, with model performance ranging from
86.38% to 88.45%, resulting in relative gains from 24.25% to
76.50% compared to the strongest baseline across different models.
Our results demonstrate that RHINO significantly enhances
the interpretability and scalability of threat analysis, offering
a blueprint for deploying LLMs in operational security settings.
I. INTRODUCTION
M
ODERN cybersecurity defenses rely heavily on Network
Intrusion Detection Systems (NIDS) to monitor and
flag malicious activities within network traffic [1]. These
systems, ranging from signature-based tools like Snort [2] to
machine learning-based anomaly detectors such as Kitsune [3],
generate vast volumes of low-level alerts and events (i.e., NIDS
logs). However, these outputs remain semantically fragmented,
requiring security analysts to manually correlate them with
high-level adversarial behaviors—a process that is not only
time-consuming but also prone to human error. Studies indicate
that analysts misclassify up to 30% of alerts when mapping
them to threat frameworks like MITRE ATT&CK [4], while
mactavishmeng@sjtu.edu.cn
jgui@sjtu.edu.cn
li-yun-bo@sjtu.edu.cn
wuyue@sjtu.edu.cn
the sheer volume of daily alerts (often exceeding 10,000 in
enterprise environments [5]) further exacerbates operational
inefficiencies.
Existing solutions for automating this mapping process fall
into two broad categories: rule-based systems [6], [7] and
machine learning classifiers [8]–[10]. Rule-based approaches,
such as M2ASK [11], rely on predefined correlation rules to
associate alerts with ATT&CK techniques. While effective for
known attack patterns, these methods fail to adapt to novel
tactics or variations in log phrasing—for instance, treating “FTP
PASS Command detected” and “FTP Login Attempt” as distinct
behaviors despite their semantic equivalence. Machine learning-
based methods, such as PATRL [9], leverage annotated datasets
to train classifiers for tactic and technique (TT) prediction.
However, they often lack contextual awareness, leading to
misinterpretations when behavioral cues (e.g., repeated login
attempts or temporal patterns) are absent from the training
data. More fundamentally, both approaches treat TT mapping
as a syntactic matching problem rather than a reasoning task,
limiting their ability to infer adversarial intent from incomplete
or noisy observations.
Recent advancements in Large Language Models (LLMs)
have demonstrated potential in addressing these limitations,
with applications ranging from malware analysis [12] to phish-
ing detection [13]. However, our preliminary experiments reveal
that LLM-based methods suffer from critical shortcomings.
Without structured reasoning, LLMs frequently hallucinate
technique names (about 24% invalid predictions in our tests)
or produce decontextualized mappings that ignore multi-stage
attack dynamics.
We observe that in real-world analyst workflows, accurate
attribution requires progressive reasoning from NIDS logs to
behavioral abstractions, then to adversarial intent, and finally
to MITRE technique alignment. Inspired by this, to bridge this
gap, we introduce RHINO, a framework that decomposes LLM-
based attack analysis into three interpretable phases mirroring
human reasoning. First, the model acts as a network analyst,
extracting key behaviors (e.g., “rapid sequential SSH login
failures from a single IP”) from NIDS logs while preserving
contextual signals like IP relationships and protocol semantics.
Next, a multi-role collaborative inference stage generates
candidate techniques (e.g., T1110 Brute Force) by jointly
evaluating behavioral evidence and ATT&CK knowledge.
Finally, a validation phase cross-references candidates against
official MITRE definitions, rectifying hallucinations (reducing
errors by 4.9%) and ranking outputs by confidence.
RHINO’s design addresses three core challenges in LLM-
arXiv:2510.14233v1  [cs.CR]  16 Oct 2025


---

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021
2
based log analysis: (1) Complex attack reasoning. By
partitioning inference into modular stages, RHINO improves
F1 scores for TT prediction by 38.4% compared to monolithic
prompting. (2) Semantic gaps. Explicit modeling of network
context (e.g., flow asymmetry, protocol anomalies) reduces
behavioral misinterpretations by about 35.8% in average. (3)
Output reliability. The review-and-refinement mechanism
enforces consistency with MITRE’s taxonomy, eliminating
technically invalid predictions.
Our evaluation demonstrates that RHINO achieves top-
1 accuracy in the range of 86.38%–88.45% for technique
prediction across advanced backbones, including ChatGPT-
4o, Gemini 2.5 Flash, Claude Sonnet 4, and DeepSeek V3.
Compared with their strongest baselines, RHINO delivers
substantial absolute improvements of 16.86–38.21 percentage
points. Moreover, these gains are achieved while preserving
robust generalization across diverse attack datasets (DAPT2020,
CICIDS2017, IoT23). The framework’s multi-stage design
proves critical, with ablation studies showing the abstraction
module alone contributes to a 78% accuracy gain by con-
textualizing low-level observations. When integrated with a
production NIDS, RHINO provides interpretable ATT&CK
mappings without compromising the NIDS’s detection accuracy
and achieves strong performance (>90% top-1 accuracy)
across different datasets. These results demonstrate RHINO’s
effectiveness in bridging the gap between raw network data
and actionable threat intelligence.
This paper makes the following contributions:
• Structured Reasoning Framework: We propose RHINO,
a novel multi-stage prompting strategy that guides LLMs
to systematically analyze network logs, infer adversarial
behaviors, and map them to MITRE ATT&CK tactics and
techniques (TTs). Our framework decomposes the complex
reasoning process into interpretable phases, mirroring
human analyst workflows.
• Context-Aware Abstraction: We introduce a semantic
parsing module that translates low-level network logs
into high-level behavioral narratives, preserving critical
contextual signals (e.g., protocol semantics, temporal
patterns) to bridge the gap between raw observations and
adversarial intent.
• Collaborative Multi-Role Inference: Our approach em-
ploys role-specific reasoning to generate and validate TT
hypotheses, reducing hallucinations and improving align-
ment with MITRE’s taxonomy. This design addresses the
limitations of monolithic LLM prompting in cybersecurity
tasks.
• Practical Validation: We demonstrate RHINO ’s effec-
tiveness across diverse attack scenarios (APTs, intrusions,
IoT botnets) and multiple state-of-the-art LLMs, show-
ing consistent improvements in mapping accuracy and
interpretability compared to existing methods.
By reframing TT mapping as a structured reasoning task
rather than a classification problem, RHINO advances the
state of the art in interpretable, scalable threat analysis.
Its design principles—modularity, contextual grounding, and
validation against authoritative knowledge—offer a blueprint
for deploying LLMs in operational security settings.
Open Science. We release the source code of this project at
https://github.com/MengFanchao2025/RHINO.
II. BACKGROUND AND MOTIVATION
Accurate mapping of network logs to adversarial tactics
and techniques (TTs) is a foundational capability for modern
cybersecurity defenses. This process enables security teams
to reconstruct attack kill chains and derive actionable threat
intelligence, playing a critical role in incident response and
mitigation strategies. However, operational challenges arise
from the inherent limitations of Network Intrusion Detection
Systems (NIDS). Enterprise environments routinely face over
10,000 daily alerts [5], yet these alerts remain semantically
fragmented—requiring manual correlation to high-level adver-
sarial behaviors. Studies demonstrate that this manual process
introduces error rates up to 30% [4] and creates significant
operational bottlenecks in Security Operations Centers (SOCs).
To illustrate these challenges, we analyze the DAPT2020
Tuesday dataset’s web vulnerability scanning scenario (Fig-
ure 1). In this attack, adversaries employ automated tools to
probe web servers for injection points (e.g., SQL injection,
command injection, remote file inclusion). The generated
traffic undergoes NIDS analysis, producing malicious network
logs comprising three key components: (1) network metadata
(IP/port, timestamps, protocol types), (2) NIDS alerts (signature-
based detections), and (3) protocol-specific information (e.g.,
HTTP URLs, hostnames).
The transformation from raw logs to TTs involves two critical
semantic transitions: first, converting low-level network traffic
into attack intent, and second, mapping this intent to MITRE
ATT&CK techniques. Traditional approaches exhibit three key
limitations:
①LLM-based rule parsing [14], [15] processes NIDS
detection rules and alert signatures via LLM analysis. While
flexible across rule sets, this method lacks contextual awareness
from actual attack logs, failing to infer true intent or detect
stealthy attacks that evade alerts.
②Static keyword mapping [6], [11] relies on pre-defined
alert-to-TT lookup tables. This approach discards contextual
signals and fails when encountering novel alert keywords or
unlogged attack vectors.
③Machine learning models [8], [9] predict TTs from
alert features but struggle with generalization—performance
degrades for new alert signatures or when attacks bypass
detection.
Opportunities in Context-Aware Analysis. Our key ob-
servation is that these approaches discard the most discrim-
inative signal: the protocol-level attack context embedded
in raw logs. For instance, an HTTP request containing
admin.php?cmd=rm+-rf+/ may evade signature-based
NIDS rules yet clearly indicates command injection. By
contrast, our method (Figure 1-④) processes compressed
log summaries—retaining critical protocol semantics while
reducing data volume—and uses LLM reasoning to directly
infer TTs. This eliminates dependency on NIDS intermediaries,
enabling detection of both alerted and silent attacks.


---

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021
3
②Static keyword mapping table
Keyword
Extraction
Technique
SQL code
T1190
SQL Injection
T1190
…
…
map
Vulnerability Scan
Attacker
Web Server
DAPT2020 - Tuesday
Malicious Scenario: Web Vulnerability Scan
(Ground truth: T1595)
Network
IDS
Detection Rules
(Optional)
Malicious
Network
Logs
Network Metadata
NIDS Alerts
Protocol Info
Network Traffic
①Previous LLM-based approach
LLM
T1190
reason
✘
③ML-based approach
ML model
T1190
predict ✘
Feature
Extraction
④Our approach
Raw log
compression
Abstraction
and inference
T1595
✓
Detect
Output
✘
Attack
Context
Attack
Intent
Unseen
Alerts
Untriggered
Alerts
✘
✘
✘
✓
✘
✘
✘
✘
✘
✘
✓
✓
✓
✓
✓
✘
Alert Keyword
{… "src_ip": "1.2.3.4", "dest_ip": "192.168.1.2", "dest_port": 9000,"proto": "TCP","timestamp": "01:25:10", 
{… "src_ip": "1.2.3.4", "dest_ip": "192.168.1.2", "dest_port": 9000,"proto": "TCP","timestamp": "01:25:20", 
{… "src_ip": "1.2.3.4", "dest_ip": "192.168.1.2", "dest_port": 9000,"proto": "TCP","timestamp": "01:25:25", "alert": {"signature": "ET WEB_SERVER Possible SQL Injection Attempt"} ,"http": {…"url": "/?pid=-1\/**UNION\/**SELECT\/…",…},…}
{… "src_ip": "1.2.3.4", "dest_ip": "192.168.1.2", "dest_port": 9000,"proto": "TCP","timestamp": "01:25:25", "alert": {"signature": "ET WEB_SERVER Possible SQL Injection Attempt"} ,"http": {…"url": "/?pid=-1\/**\/AND\/**\/1=2 \/… ", … },…}
"http": {…"url": "info.php?f=http://cirt.net/rfiinc.txt", …},…}
"http": {…"ref": " () { _; } >_ [$($())] {echo 1: true;}"}, …}
NIDS Alerts
Network Metadata
Protocol Info
Input
Output
TT
Mapping
✓
✓
✓
✓
No alert triggered
Samples
Fig. 1. An example of attack-to-tactic/technique (TT) mapping for web server vulnerability scanning (in the DAPT2020-Tuesday dataset). The attacker probes
for injection points, with traffic analyzed by a NIDS. Traditional methods (rule-based alerts, statistical keyword tables, or ML) and prior LLM-based approaches
rely on alert text or rule parsing. In contrast, our method processes compressed attack context logs through LLM reasoning, enabling TT mapping without
dependency on NIDS alerts or rules.
III. APPROACH OVERVIEW
Mapping raw NIDS logs to adversarial tactics and techniques
(TTs) demands more than syntactic pattern matching; it
requires a nuanced understanding of the behavioral intent
and contextual signals embedded within fragmented, noisy
observations. To bridge this semantic gap, RHINO transforms
unstructured NIDS logs into structured MITRE ATT&CK
mappings through a multi-stage reasoning pipeline that mirrors
human analyst workflows. Figure 2 illustrates the end-to-end
reasoning process, which is divided into four interpretable
modules, each addressing a critical challenge in LLM-based
log analysis.
Preprocessing and Context Preservation. Raw NIDS logs are
inherently verbose and repetitive, often exceeding LLM context
windows while lacking semantic cohesion. The preprocessing
module tackles this by aggregating logs into flow-level sum-
maries, filtering low-information noise (e.g., bulk port scans),
and extracting protocol-specific features (e.g., HTTP methods,
SMB commands). This compression preserves behavioral
signals—such as traffic directionality, packet asymmetries, and
session timing—while reducing input volume by 83.5% in our
experiments. To mitigate information loss, application-layer
fields are statistically sampled to retain representative examples
without overwhelming the model’s token budget.
Behavioral Abstraction via Semantic Parsing. The parsed
flow summaries are then translated into natural language
descriptions that capture adversarial behaviors (e.g., “rapid
sequential SSH login failures from a single IP”). Unlike
traditional classifiers that treat logs as isolated events, this
stage explicitly models network context—such as source-
destination relationships, protocol anomalies, and temporal
patterns—to reconstruct attacker actions as coherent narratives.
These descriptions serve as a bridge between low-level statistics
and high-level reasoning, enabling the system to infer intent
from incomplete or ambiguous observations.
Multi-Role Collaborative Inference.Inspired by human ana-
lyst teams, RHINO employs a partitioned reasoning strategy to
map behaviors to MITRE TTs. First, the LLM acts as a network
analyst, hypothesizing attacker objectives (e.g., “gaining initial
access via credential brute-forcing”). Next, it transitions to a
threat intelligence role, evaluating behavioral evidence against
ATT&CK knowledge to generate candidate techniques (e.g.,
T1110: Brute Force). Crucially, the tactic space is divided
into subsets, and the model performs parallel inference passes
to mitigate bias toward dominant techniques (e.g., reducing
over-prediction of T1078: Valid Accounts by 1.8%). Finally, a
validator role cross-references candidates with official MITRE
definitions, discarding hallucinations (e.g., “T1077: Windows
Admin Shares”) and resolving semantic ambiguities.
Confidence-Aware Refinement. The initial TT candidates
undergo iterative validation to ensure alignment with both
observed behaviors and MITRE’s taxonomy. Each candidate is
scored based on its semantic fit to the behavioral description and
contextual plausibility (e.g., “T1110 is favored over T1078 for
repeated login failures”). This stage reduces invalid predictions
by 5.3% and ranks outputs by confidence, enabling analysts to
prioritize high-likelihood techniques.
IV. DESIGN
The core challenge in mapping NIDS logs to adversarial
TTs lies in bridging the semantic gap between low-level
observations (e.g., FTP login attempts) and high-level attacker


---

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021
4
RHINO Core Components
Abstraction
Output
Final Mapping
Results with score
1. T1190, Exploit Public-facing Appl
ication, Initial Access, 0.9
2. T1595, Active Scanning,
Reconnaissance, 0.7.
3.T1595.002 Vulnerability Scanning,
Reconnaissance, 0.5.
4. T1046, Network Service Discovery,
Discovery, 0.6. 
5. T1204, User Execution, Execution,
0.4.
Environment Extraction
Behavior Interpretation
Abstraction
Module
1
Intent Reasoning
(Attack Analysis)
TT Mapping
Self-Consistency
Consistent
Result
Fusion
Result 1
Result 2
Result N
…
LLM
Inference
Module
2
<Tactic Group #N>
Preliminary 
Mapping Result
…
Preliminary 
Mapping Result
<Tactic Group #2>
Preliminary 
Mapping Result
<Tactic Group #1>
Preliminary 
Mapping Result
Knowledge Base
Result &
Correction
Prompt
Result Check
Retrieve
Refinement
Module
3
Result Verification 
and Correction
TT Scoring
Raw Logs of 
NIDS Alerts
Grouping by
{src_ip, dest_ip, dest_port, proto}
Isolation Forest Classifier
Other Malicious
Log Group
Log Compression & Abstraction
Scanning
Log Group
Preprocessing Module
Log
Group
#1
Log
Group
#2
Log
Group
#N
…
Completed by LLM
Module Output
Intermediate Result
Legend
Fig. 2. A detailed illustration of the RHINO framework, which employs a multi-role instruction approach to construct prompts. When reasoning about attacks,
we first compress raw NIDS logs to identify corresponding network behaviors. These behaviors are then mapped to attack tactics and techniques (TTs). Finally,
the mapped results are compared against standardized TT definitions in MITRE ATT&CK to ensure accuracy and eliminate any invalid TTs.
behaviors (e.g., brute-force password guessing). Traditional
approaches treat this as a classification task, either through rule-
based pattern matching or supervised learning. However, these
methods fail to capture the contextual and sequential reasoning
inherent to human analyst workflows. RHINO addresses this
limitation through a structured, multi-phase reasoning pipeline
that mirrors analytical cognition while leveraging the inferential
capabilities of LLMs. Below, we detail each component of this
pipeline and its role in transforming noisy observations into
validated adversarial tactics and techniques.
A. Preprocessing Module
Raw NIDS logs exhibit three properties that hinder direct
LLM processing: volumetric redundancy (thousands of similar
entries per session), protocol-specific verbosity (excessive
protocol-specific metadata), and behavioral fragmentation
(attack patterns distributed across multiple flows). A typical
credential brute-forcing attempt, for instance, may produce hun-
dreds of FTP log entries documenting retransmissions, failed
handshakes, and authentication attempts. Left unprocessed, this
verbosity would quickly exhaust the context window of even the
most capable language models while obscuring the underlying
attack pattern.
To address this, our preprocessing module implements a
hierarchical compression strategy. NIDS logs are first grouped
by their essential communication attributes—source and desti-
nation IP addresses, destination port, transport protocol, and
application-layer service. This five-tuple grouping deliberately
excludes ephemeral source ports, which typically carry no
semantic value in attack scenarios. Each resulting flow group
is then characterized by statistical features that capture its
behavioral essence: packet and byte counts in both directions,
session duration, and TCP flag distributions. This transforma-
tion reduces a 283,491-entry DDoS trace from CICIDS2017
to a 312-token representation, while retaining its characteristic
pattern of numerous short-lived connections and asymmetric
packet flows.
The module incorporates specialized handling for high-
volume, low-information activities like port scanning. When
a source IP contacts more than fifty distinct destinations—a
strong indicator of scanning behavior—we employ an Isolation
Forest model to separate repetitive probe traffic from potentially
interesting outliers. This approach proved particularly effective
in our evaluation, filtering out 13.9% of flows in the DAPT2020
dataset without compromising attack visibility. For stateful
protocols like HTTP, SMB, and FTP, we enrich the flow repre-
sentations by extracting and strategically sampling application-
layer fields (e.g., HTTP methods, FTP commands). We further
apply binomial sampling [16] to preserve the semantic signal
in fields like HTTP URIs while maintaining manageable input
sizes.
B. Abstraction Module
While the preprocessing module produces efficient numerical
summaries, these representations remain inaccessible to the
semantic reasoning capabilities of language models. The
abstraction module bridges this gap by translating flow statistics
into natural language narratives that capture the security-
relevant aspects of network behavior.
This translation is guided by a carefully constructed prompt
that positions the language model in the role of a network
security analyst. Given a flow summary fi ∈F, the language
model M generates two complementary outputs: ai and di.
The former is a structured enumeration of key attributes (IP
addresses, ports, protocol features), while the latter is a free-
form behavioral description (e.g., “The traffic is directed
from a source IP 172.16.0.1 to a destination IP within a
private network (192.168.10.50)... with a high frequency of
authentication attempts and consistent failures to authenticate
...”). The description di incorporates critical contextual cues that


---

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021
5
inform a human analyst’s assessment—such as traffic direction-
ality (e.g., distinguishing client-initiated requests from server
responses), temporal patterns (e.g., burstiness or periodicity),
and protocol-specific semantics (e.g., interpreting sequences of
SMB commands as potential share enumeration).
This dual-output approach ensures both machine-readability
and human interpretability. The structured metadata anchors
the subsequent reasoning process in observable evidence, while
the narrative description provides the rich contextual fabric
needed for accurate intent inference.
C. Inference Module
Mapping abstracted behaviors to MITRE ATT&CK tech-
niques presents unique challenges. The tactic-technique space
is large and semantically nuanced, with many techniques
exhibiting overlapping or context-dependent definitions. Our
preliminary experiments revealed that conventional prompting
approaches led to two persistent failure modes: hallucination
of non-existent techniques (occurring in 5.3% of test cases
with ChatGPT-4o) and misclassification due to over-reliance
on lexical patterns rather than behavioral context.
The inference module addresses these issues through a
partitioned reasoning strategy, inspired by how human analysts
conduct complex threat assessment. The process begins with the
language model generating the attacker’s intent (e.g., “The log
data points to a brute force attack targeting the FTP service
on the destination IP, with the attacker attempting to gain
unauthorized access by guessing login credentials”) based on
the behavioral narrative—similar to an analyst forming initial
impressions during triage.
Formally, let Bi = (ai, di) denote a behavior description
from the abstraction module. The inference module generates
an attacker intent Ii using the LLM M with an intent-focused
prompt pintent:
Ii = M(pintent, Bi)
These intents then guide a structured exploration of the
MITRE framework, where the fourteen tactics are divided into
five non-overlapping groups to prevent cognitive overload. For
each tactic group (TA)j, the model evaluates how well the
observed behaviors align with constituent techniques using
prompt ptt:
Y(j)
i
= M(ptt, Bi, Ii, (TA)j)
∀j ∈[1, 5]
Here, Yi is a triplet (ti, ci, ri), where ti denotes the
technique, ci its corresponding tactic, and ri the reasoning
justification. This partitioning proved particularly effective at
surfacing less common techniques that might otherwise be
overshadowed by more frequently referenced tactics.
Finally, the module consolidates all partial mappings using
a fusion prompt pfusion:
ˆYi = M(pfusion, Bi, Ii, {Y(j)
i
}5
j=1)
The output ˆYi = [(t1, c1, r1), ..., (tk, ck, rk)] is an unranked
list of up to five tactic-technique pairs, each accompanied by
a justification (e.g., “T1110: The logs show a high number
of failed authentication attempts using ‘USER’ and ‘PASS’
commands, which is indicative of a brute force attack.”).
Our evaluation showed this approach improved technique
prediction accuracy by at most 31.8% compared to monolithic
prompting strategies, while reducing hallucinated outputs to
just 0.6% of cases. The multi-stage, evidence-based reasoning
mirrors the gradual refinement process human analysts employ
when building their understanding of an attack.
D. Refinement Module
The final component of our pipeline addresses a critical
operational requirement: ensuring that all output mappings are
not only plausible but also semantically grounded in both the
observed data and official MITRE definitions. Even technically
valid technique proposals may lack proper contextual fit—for
instance, suggesting T1190 (Exploit Public-facing Application)
for a sequence of requests that are targeting to discover potential
injection points simply because the requests contain the SQL
keyword.
The refinement module implements a two-phase validation
process. First, all candidate techniques are checked against
MITRE’s official taxonomy, filtering out invalid or hallucinated
entries. This step alone eliminated 3.7% of incorrect outputs in
our testing. The remaining candidates then undergo contextual
scoring, where the language model assesses how well each
technique’s definition aligns with both the behavioral narrative
and the original flow evidence.
Formally, let D( ˆYi) denote the set of official MITRE
ATT&CK definitions for each technique in ˆYi. Using an LLM
M with the refinement prompt prefine, we define the relevance
scoring process as:
Si = M(prefine, ˆYi, Bi, D( ˆYi))
The final output, Si = [(t′
1, c′
1, r′
1, s′
1), ..., (t′
k, c′
k, r′
k, s′
k)],
where s′
i is the confidence score, Si is a ranked list ordered
by s′
i, incorporating both contextual consistency and semantic
plausibility.
This scoring produces more than just a ranked list—it
generates auditable justifications that trace the mapping decision
back to specific observations in the source data. For example,
a high-confidence mapping to T1110 (Brute Force) might refer-
ence “the high number of SSH connection attempts with short
durations and timeouts strongly indicates a brute force attack
aimed at guessing valid credentials.” Such interpretability is
crucial for operational trust, enabling security teams to validate
the system’s reasoning against their own expertise.
V. EXPERIMENTS
We present a comprehensive empirical assessment of RHINO,
designed to rigorously evaluate its effectiveness in mapping
network behaviors to MITRE ATT&CK techniques. The
evaluation framework addresses four critical research dimen-
sions through systematic experiments across diverse attack
scenarios, comparative analyses with state-of-the-art baselines,
and detailed component-level ablation studies. All experiments
were conducted on a dedicated evaluation platform equipped


---

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021
6
TABLE I
DISTRIBUTION OF ATTACK CATEGORIES OF THREE DATASETS USED IN OUR EXPERIMENT. DAPT2020 [17] INCLUDES SIMULATED APT ATTACK
PROCESSES, COVERING MULTIPLE STAGES OF THE ATTACK. CICIDS2017 [18] CONTAINS VARIOUS TYPES OF NETWORK INTRUSION SAMPLES, FOCUSING
ON TRADITIONAL INTRUSION DETECTION SCENARIOS. IOT23 [19] PROVIDES VARIOUS TYPES OF MALICIOUS TRAFFIC FROM IOT BOTNETS.
Dataset
# Malicious
Log lines
# IPs
Traffic
Duration (h)
# Flow Instances Corresponding to Each Attack Category
Network Scan
Account Discovery
Directory Bruteforce
Command Injection
SQL Injection
Backdoor
CSRF
7,653
133
9,968
12
55
20
7
Account Bruteforce
Malware Download
Web Vulnerability Scan
Credential Access
DAPT2020
1,287,644
28
96
141
2
2,574
796
FTP-Patator
SSH-Patator
DoS/DDoS
Heartbleed
Web Attack
Portscan
Botnet
CICIDS2017
1,073,698
27
96
3,972
2,961
266,778
11
104
159,066
736
DDoS
C&C
PortScan
FileDownload
Attack
IoT23
4,450,709
1,684,627
72
3,592,851
6,801
3,386,241
11
3,586
with an Intel Core i5-13400 processor (16GB RAM), with each
experimental condition repeated across three independent trials
to ensure statistical reliability.
Specifically, to evaluate RHINO, we focus on answering the
following research questions:
RQ1 (Performance): How does the performance of RHINO
compare with that of baseline methods?
RQ2 (Ablation): How does each module within RHINO
contribute to the overall mapping performance?
RQ3 (Error analysis): What are the common errors in this
task, and how can RHINO mitigate these errors to improve its
overall performance?
RQ4 (Practicality): Is RHINO practical and effective in
real-world mapping task?
A. Evaluation Settings
Datasets. The evaluation leverages three benchmark datasets
(Table I) representing distinct threat paradigms, each selected
for their complementary coverage of modern attack vectors.
The DAPT2020 dataset comprises 1.28 million malicious
flows simulating advanced persistent threats in enterprise
environments, with particular emphasis on multi-stage attack
sequences including initial compromise through web vulner-
ability exploitation, lateral movement via SMB exploitation,
and data exfiltration using FTP. This dataset’s value lies in its
realistic emulation of adversarial tradecraft.
For traditional network intrusion scenarios, we utilize the
CICIDS2017 dataset’s 1.07 million lines of malicious logs
spanning seven attack categories across multiple protocols
(HTTP/S, FTP, SSH). The dataset’s comprehensive coverage
of behavioral anomalies—ranging from volumetric DoS floods
to subtle heartbleed exploits—provides a robust testbed for
evaluating protocol-aware analysis capabilities.
The IoT23 dataset’s 4.45 million lines of logs from IoT
botnet infections (Mirai, Gafgyt variants) were selected to
evaluate performance on constrained-device attack patterns.
We focused on three representative scenarios (corresponding
to 34-1, 48-1, and 60-1) demonstrating complete kill-chains
from device compromise through DDoS payload execution,
with special consideration given to the characteristic irregular
beaconing intervals and high-volume attack traffic peculiar to
IoT threats.
To establish a reliable evaluation framework, we first defined
a ground truth mapping between observed malicious traffic and
MITRE ATT&CK techniques (TTs). Our methodology for de-
riving these mappings followed the labeling approach proposed
by Daniel et al. [14], which we applied to three benchmark
datasets: DAPT2020, CICIDS2017, and IoT23. From these
datasets’ ground truth annotations, we systematically extracted
45 distinct attack labels, each characterizing a unique attack
variant. These labels were then manually correlated with their
corresponding MITRE ATT&CK techniques through careful
analysis of each dataset’s attack descriptions. This process
involved examining behavioral patterns, attack objectives, and
technical procedures documented in the datasets to ensure
accurate technique alignment.
Baselines. Three baseline prompting strategies were imple-
mented with identical input preprocessing pipelines to ensure
fair comparison. The Vanilla prompting approach serves as
our null hypothesis, testing raw LLM capability through
minimal instructions: “Analyze the following network log
summary and identify up to 5 relevant MITRE ATT&CK
Tactic-Technique (TT) pairs.[FLOW SUMMARY]” The Chain-
of-Thought (CoT) baseline enforces explicit reasoning steps
before prediction: “... Step 1: Describe the key elements of
the event. Step 2: Match to possible ATT&CK Tactics and
Techniques. Step 3: Choose up to 5 most relevant TT pairs...”
Our Tree-of-Thought (ToT) implementation follows Yao et
al.’s breadth-first search methodology [20] with three parallel
reasoning paths and majority-vote aggregation.
Metrics. All baseline methods are evaluated under consistent
conditions, using identical preprocessed log summaries as input,
with matching model configurations and input formats to ensure
a fair comparison with our approach. Model performance is
assessed using top-K accuracy, measured at both tactical and
technical levels. For each traffic sample, a prediction is deemed
correct if the ground-truth tactic or technique appears within
the top-1, top-3, or top-5 predictions generated by the model.
The overall accuracy is derived from the proportion of correctly
labeled flow samples in the dataset. Formally, given a scenario
s comprising N flow samples with true labels gi and model
predictions yi, a sample is correctly predicted if its true label
gi is among the top-K predictions. The accuracy is computed
as:
Accuracy(K) = 1
N
N
X
i=1
1(gi ∈{y(i)
1 , y(i)
2 , . . . , y(i)
K }),
where 1(gi ∈y(i)
1 , y(i)
2 , . . . , y(i)
K ) is an indicator function
returning 1 if the condition holds and 0 otherwise.
To mitigate bias introduced by traffic-heavy scenarios (e.g.,
DoS attacks disproportionately influencing results), we employ


---

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021
7
TABLE II
COMPARISON OF MODEL PERFORMANCE ACROSS THE DAPT2020, CICIDS2017, AND IOT23 DATASETS. ACCURACY IS REPORTED FOR TOP-1, TOP-3, AND
TOP-5 PREDICTIONS. BEST RESULTS ARE HIGHLIGHTED IN BOLD, AND SECOND-BEST RESULTS ARE UNDERLINED. METHODS INCLUDE RHINO (OURS),
CHAIN-OF-THOUGHT (COT), TREE-OF-THOUGHT (TOT), AND VANILLA PROMPTING.
Weighted Accuracy (%)
Top 1
Top 3
Top 5
Model
Dataset
Ours
CoT
ToT
Vanilla
Ours
CoT
ToT
Vanilla
Ours
CoT
ToT
Vanilla
DAPT2020
67.99
60.15
29.10
59.91
88.33
62.96
73.81
63.67
97.57
63.08
73.94
64.22
CICIDS2017
98.54
2.62
46.11
2.91
99.56
14.18
46.17
14.36
99.62
25.94
63.86
14.50
IoT23
97.90
99.35
99.55
5.98
99.76
99.96
99.71
5.98
99.82
99.97
99.90
6.09
ChatGPT 4o
Average
88.14
54.04
58.25
22.93
95.89
59.03
73.23
28.01
99.00
63.00
79.24
28.27
DAPT2020
81.66
60.60
44.94
66.75
94.47
78.73
79.89
81.83
94.68
79.24
84.79
81.94
CICIDS2017
81.43
72.55
63.89
2.93
99.23
95.46
64.27
45.28
99.29
96.30
64.70
98.89
IoT23
96.10
37.22
99.79
99.60
98.06
99.89
99.94
99.79
98.14
99.90
99.95
99.84
Claude
Sonnet 4
Average
86.40
56.79
69.54
56.43
97.26
91.36
81.36
75.63
97.37
91.81
83.14
93.56
DAPT2020
69.04
82.47
77.44
71.91
95.17
85.94
93.15
72.48
95.66
88.92
93.94
75.64
CICIDS2017
96.53
25.72
67.37
2.93
99.25
55.73
67.49
20.71
99.26
55.75
90.27
56.08
IoT23
99.78
5.63
5.93
5.49
99.79
5.82
5.94
68.16
99.83
5.83
5.96
99.50
Gemini
2.5 Flash
Average
88.45
37.94
50.24
26.78
98.07
49.16
55.53
53.78
98.25
50.16
63.39
77.07
DAPT2020
65.17
52.56
40.34
52.16
79.77
76.42
80.93
57.68
80.18
79.76
84.88
57.87
CICIDS2017
94.22
39.29
39.13
5.12
99.63
55.94
47.02
5.69
99.73
56.09
58.41
17.16
IoT23
99.76
5.68
68.34
5.62
99.90
5.91
99.77
5.63
99.99
5.96
99.82
37.02
Technique-level
Deepseek V3
Average
86.38
32.51
49.27
20.97
93.10
46.09
75.91
23.00
93.30
47.27
81.04
37.35
DAPT2020
68.00
60.42
32.59
47.16
88.39
63.27
75.27
61.94
97.80
63.66
75.44
62.13
CICIDS2017
99.38
2.62
46.14
2.91
99.56
22.09
46.18
14.49
99.62
33.85
63.87
22.40
IoT23
97.90
99.35
99.56
5.98
99.76
99.98
99.80
6.00
99.77
99.99
99.98
6.10
ChatGPT 4o
Average
88.42
54.13
59.43
18.69
95.91
61.78
73.75
27.48
99.06
65.83
79.77
30.21
DAPT2020
81.82
64.04
45.23
66.80
94.55
79.27
80.21
81.95
94.81
79.44
85.14
82.10
CICIDS2017
99.53
72.55
64.03
2.93
99.65
98.05
64.24
45.71
99.71
98.89
64.67
99.33
IoT23
98.04
37.22
99.80
99.66
99.99
99.90
99.95
99.79
99.99
99.92
99.97
99.84
Claude
Sonnet 4
Average
93.13
57.93
69.68
56.46
98.06
92.40
81.46
75.82
98.18
92.75
83.26
93.76
DAPT2020
70.67
82.09
77.49
78.92
95.62
88.09
89.08
79.87
96.00
90.33
89.92
83.20
CICIDS2017
99.18
50.22
67.41
2.97
99.66
99.01
67.51
9.07
99.68
99.02
91.15
44.44
IoT23
99.79
5.82
5.94
5.77
99.79
6.03
5.96
68.44
99.84
6.06
5.99
99.78
Gemini
2.5 Flash
Average
89.88
46.04
50.28
29.22
98.36
64.38
54.18
52.46
98.50
65.14
62.35
75.81
DAPT2020
65.20
52.51
40.91
22.32
79.82
72.71
79.84
30.75
80.29
73.16
81.79
57.27
CICIDS2017
99.54
41.87
62.01
7.70
99.64
55.89
64.64
10.85
99.74
58.62
76.05
40.44
IoT23
99.76
5.77
68.38
5.72
99.90
6.07
99.82
5.73
99.99
6.20
99.89
37.20
Tactic-level
Deepseek V3
Average
88.17
33.38
57.10
11.91
93.12
44.89
81.43
15.78
93.34
45.99
85.91
44.97
a weighted accuracy metric. This approach assigns scenario-
specific weights to balance contributions across attack cate-
gories, ensuring equitable evaluation. The weighted accuracy
is defined as:
Accuracyweighted(K) =
T
X
s=1
ns
n · Accuracy(K)s,
where ns denotes the number of flow samples for attack
category s, n represents the total malicious flow samples,
and
ns
n acts as the normalization weight. This formulation
guarantees that each attack scenario’s impact on the overall
metric reflects its dataset proportion, yielding a more balanced
assessment.
Beyond conventional top-K accuracy metrics, we introduce
two specialized measures to address specific evaluation re-
quirements. Tactical Consistency evaluates whether predicted
techniques properly align with ground-truth tactical phases
(e.g., ensuring “T1046: Network Service Discovery” maps to
the “Discovery” tactic). The Class-wise F1 metric provides
per-technique performance analysis to identify strengths and
weaknesses across ATT&CK’s heterogeneous technique land-
scape.
B. RQ1: Performance Evaluation
We evaluate the system’s accuracy in mapping malicious
network behaviors to MITRE ATT&CK techniques, com-
paring our multi-stage design against established prompting
strategies—Chain-of-Thought (CoT), Tree-of-Thought (ToT),
and vanilla prompting. All methods process identical inputs,
including flow summaries and semantic behavior descriptions
from the abstraction module. Performance is measured via
top-1, top-3, and top-5 accuracy at both tactic and technique
levels.
Key Findings. As shown in Table II, our method achieves supe-
rior accuracy across three datasets (DAPT2020, CICIDS2017,
IoT23) for four commercially available models: ChatGPT-4o,
Claude Sonnet 4, Google Gemini 2.5 Flash, and DeepSeek
V3. These backbone models were selected to cover a range
of AI architectures and technologies from leading providers,
ensuring a comprehensive evaluation across multiple datasets
and providing an in-depth comparison of state-of-the-art model
performance. All models exhibit comparable performance, yet
all significantly outperform baseline prompting approaches,
demonstrating the architectural robustness and generalizability
of RHINO.
For instance, Gemini 2.5 Flash achieves an average top-1
accuracy of 88.45%, which is 38.21 percentage points higher
than the second-best baseline (ToT at 50.24%), representing a


---

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021
8
T1595 T1190 T1048 T1110 T1046 T1059 T1210 T1105 T1071 T1499 T1498
0.00
0.25
0.50
0.75
1.00
F1 Score
Gemini top-1
Gemini top-5
DeepSeek top-1
DeepSeek top-5
Fig. 3.
Class-wise F1 scores for top-1 and top-5 predictions across two
representative backbone models: Gemini 2.5 Flash (best-performing) and
DeepSeek V3 (worst-performing).
76.05% relative improvement. ChatGPT-4o follows closely
with 88.14% accuracy, outperforming baselines by 29.89
percentage points (51.31% relative). Claude Sonnet 4 and
DeepSeek V3 achieve nearly identical accuracies of 86.40%
and 86.38%, respectively, but their improvements over baselines
vary substantially. Claude outperforms ToT (69.54%) by 16.86
points, a 24.24% relative improvement, whereas DeepSeek
surpasses its best baseline ToT (49.27%) by 37.11 points,
amounting to a 75.32% relative gain. These results highlight
RHINO’s ability to capture nuanced attack patterns and improve
detection coverage.
Tactic-Level Performance. Similar trends are observed at the
tactic level. Across all four models, our approach consistently
outperforms the strongest baseline (ToT). Claude achieves
the highest absolute accuracy (93.13%), with a 23.45-point
gain over ToT. Gemini and DeepSeek V3, despite weaker
baseline performance, exhibit the most substantial improve-
ments: Gemini shows a 39.6-point absolute increase (78.8%
relative), while DeepSeek V3 attains the absolute gain of
31.07 points (54.4% relative). ChatGPT-4o also demonstrates
a notable 28.99-point (48.78% relative) improvement. It is
worth noting that in the IoT23 dataset, baseline prompting
methods occasionally outperform RHINO by ∼3% in isolated
cases. We attribute this to chance alignment: baselines often
default to common tactics (e.g., frequent requests mislabeled
as Reconnaissance), coincidentally matching ground truth. In
contrast, RHINO’s structured reasoning trades marginal losses
in edge cases for consistently higher average accuracy (e.g.,
88.42% for ChatGPT-4o vs. 59.43% for ToT), thereby avoiding
heuristic biases.
Class-wise F1 Analysis. To further dissect performance
across the diverse set of techniques in MITRE ATT&CK, we
evaluate class-wise F1 scores using the One-vs-Rest (OvR)
approach [21]. In this setup, each technique is treated as
an independent binary classification task, where the target
technique is considered the positive class (1) and all others are
grouped as negatives (0). For top-1 predictions, the highest-
scoring candidate is selected; for top-5, the correct technique is
chosen if present among candidates, otherwise the top candidate
is retained. Predictions and ground truth are aggregated across
all datasets, computing precision, recall, and F1 per technique.
Figure 3 presents the resulting class-wise F1 scores for
top-1 and top-5 predictions for two representative models:
Gemini 2.5 Flash (best overall performance) and DeepSeek
V3 (lowest performance). RHINO successfully maps a total of
11 techniques with notable accuracy. Among these, techniques
such as T1595 (Active Scanning), T1110 (Brute Force), T1071
(Application Layer Protocol), T1499 (Endpoint Denial of
Service), and T1498 (Network Denial of Service) achieving
F1 scores above 0.7. These techniques benefit from high-
volume, pattern-driven attacks (e.g., repeated login attempts
for T1110), enabling reliable intent inference from traffic
metadata. Conversely, techniques like T1048 (Exfiltration Over
Alternative Protocol) and T1046 (Network Service Discovery)
yield considerably lower F1 scores. This performance drop
can be attributed to their more subtle and context-dependent
behavioral signatures. For instance, accurately identifying
T1048 often requires inspection of file content or payload,
which is not accessible from metadata alone. Finally, we
observe that top-5 F1 scores consistently surpass top-1 scores
across most techniques, indicating that although the model
may not always rank the correct technique first, it frequently
includes the true technique among its top-five predictions.
Comparison with Related Work. We also compare the
mapping accuracy with the state-of-the-art solution LNR1 [14],
which reasons about NIDS rules while labeling them with
MITRE ATT&CK TTs using LLMs. We do not evaluate static
keyword mapping approaches [6], [11] (Figure 1-②) or machine
learning models [8], [9] (Figure 1-③) due to their coarser
granularity, lack of open-source availability, or unclear training
data provenance, which hinder fair comparison. Following the
descriptions and prompts from [14], we implemented LNR
using ChatGPT-4, which was also evaluated in the original
study, and reran all experiments across the three datasets.
As shown in Table III, LNR achieves an accuracy of 34.92%
on the CICIDS2017 dataset, which is comparable to RHINO,
but performs poorly on the other two datasets. This performance
discrepancy stems from two main issues: first, LNR relies on
Snort and its detection rules, yet 87.1% of malicious flows did
not trigger alerts; second, LNR does not incorporate the context
of malicious flows during the mapping process, resulting in
17.54% of mapping errors. In contrast, RHINO uses malicious
network logs as input, which are independent of detection rules,
and leverages broader contextual information (e.g., source,
behavior) to analyze the attacker’s intent, leading to more
accurate and consistent results.
TABLE III
COMPARISON OF TECHNIQUE-LEVEL WEIGHTED MAPPING ACCURACY
BETWEEN RHINO, BASELINE METHODS AND THE STATE-OF-THE-ART
SOLUTION LNR, ALL USING CHATGPT-4 AS THE BACKBONE MODEL.
Weighted Accuracy (%)
DAPT2020
CICIDS2017
IoT23
Average
CoT
64.30
3.00
35.23
34.18
ToT
57.64
31.62
68.30
52.52
Vanilla
57.47
2.60
2.17
20.74
LNR
0.83
34.92
2.20
12.65
RHINO
66.00
32.26
99.74
66.00
Discussion. In summary, the results validate the effectiveness
1We abbreviate the key words in the title to represent the approach in the
paper.


---

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021
9
TABLE IV
ABLATION STUDY USING CHATGPT-4O ON THE IMPACT OF KEY COMPONENTS IN RHINO: THE ABSTRACTION MODULE, INFERENCE MODULE, AND
REFINEMENT MODULE. THREE VARIANTS ARE TESTED: (1) RHINO-NO-ABSTRACTION (W/O ABS.) (2) RHINO-ALT-CONSISTENCY, WHICH REPLACES
STRUCTURED INFERENCE WITH STANDARD CONSISTENCY DECODING METHODS SUCH AS multi-sampling AND self-debate; AND (3)
RHINO-NO-REFINEMENT (W/O REF.). THE PERFORMANCE METRICS FOR TOP-1, TOP-3, AND TOP-5 ACCURACY ARE REPORTED FOR EACH
CONFIGURATION. RESULTS ARE COLOR-CODED, WITH RED INDICATING PERFORMANCE DEGRADATION AND GREEN INDICATING PERFORMANCE
IMPROVEMENT COMPARED TO THE FULL METHOD OF RHINO.
Weighted Accuracy (%)
Top 1
Top 3
Top 5
Dataset
Ours
w/o
Abs.
Multi
Sampling
Self
Debate
w/o
Ref.
Ours
w/o
Abs.
Multi
Sampling
Self
Debate
w/o
Ref.
Ours
w/o
Abs.
Multi
Sampling
Self
Debate
w/o
Ref.
49.91
63.76
64.40
61.15
90.02
66.09
66.00
82.83
90.90
66.12
69.08
86.04
DAPT2020
67.99
-26.59
-6.23
-5.28
-10.06
88.33
+1.91
-25.19
-25.28
-6.23
97.57
-6.84
-32.23
-29.20
-11.81
3.00
79.20
78.60
99.53
3.06
99.60
79.23
99.60
25.93
99.63
79.23
99.67
CICIDS2017
98.54
-96.95
-19.63
-20.24
+1.00
99.56
-96.92
+0.04
-20.42
+0.04
99.62
-73.97
+0.01
-20.46
+0.05
5.85
68.45
97.88
99.70
6.00
99.84
99.71
99.75
6.01
99.88
99.75
99.76
IoT23
97.90
-94.02
-30.08
-0.02
+1.84
99.76
-93.98
+0.08
-0.05
-0.01
99.82
-93.97
+0.07
-0.06
-0.06
19.59
70.47
80.29
86.79
33.03
88.51
81.65
94.06
40.95
88.54
82.69
95.16
Technique-level
Average
88.14
-77.78
-20.06
-8.91
-1.53
95.89
-65.55
-7.69
-14.85
-1.90
99.00
-58.64
-10.56
-16.48
-3.88
48.49
63.78
64.40
61.34
88.70
66.14
66.03
83.19
89.58
66.28
69.29
86.44
DAPT2020
68.00
-28.69
-6.21
-5.30
-9.80
88.39
+0.34
-25.17
-25.30
-5.89
97.80
-8.40
-24.72
-21.31
-1.82
3.02
81.79
99.45
99.05
3.06
99.61
99.53
99.60
25.93
99.66
99.53
99.68
CICIDS2017
99.38
-96.96
-17.70
+0.08
-0.32
99.56
-96.92
+0.04
-0.03
+0.04
99.62
-73.98
+0.10
-0.03
+0.12
5.86
99.69
97.88
99.70
6.02
99.84
99.71
99.76
6.04
99.90
99.75
99.77
IoT23
97.90
-94.01
+1.84
-0.02
+1.84
99.76
-93.96
+0.08
-0.05
-0.01
99.77
-93.95
+0.19
+0.04
+0.05
19.13
81.75
87.24
86.70
32.59
88.53
88.42
94.18
40.52
88.61
89.52
95.30
Tactic-level
Average
88.42
-78.37
-7.54
-1.34
-1.95
95.91
-66.01
-7.69
-7.80
-1.80
99.06
-59.10
-7.48
-6.53
-0.50
of RHINO in processing complex threats. Its multi-stage
design mitigates the oversimplification risks inherent in baseline
methods, which often rely on heuristic mappings or truncated
context. Baselines, despite excelling in narrow scenarios
(e.g., tactic-level predictions in IoT23), exhibit inconsistency
across datasets, underscoring RHINO’s advantages: reliability,
interpretability, and comprehensive attack analysis.
C. RQ2: Ablation Study
To evaluate the contributions of RHINO’s core compo-
nents—the Abstraction Module, Inference Module, and Re-
finement Module—we conduct an ablation study with three
variants:
• RHINO-No-Abstraction, which bypasses the Abstraction
Module and feeds compressed flow summaries directly to
the reasoning stage;
• RHINO-Alt-Consistency, replacing our structured infer-
ence strategy with standard consistency decoding methods
(e.g., multi-sampling and self-debate); and
• RHINO-No-Refinement, which skips the final reranking
phase and outputs raw predictions from the reasoning
module.
As summarized in Table IV, we report the perfor-
mance of these variants using ChatGPT-4o across three
datasets—DAPT2020, CICIDS2017, and IoT23—in terms of
top-1, top-3, and top-5 accuracy. Detailed results for other
LLMs are provided in the supplemental material. Below, we
discuss the key findings from this study.
Impact of the Abstraction Module. Disabling the Abstraction
Module leads to the most severe performance degradation, with
an average top-1 accuracy drop of 78.37% at the technique
level and 77.78% at the tactic level. Notably, datasets like
CICIDS2017 and IoT23 exhibit over 90% degradation in
some cases. This underscores the module’s critical role in
bridging low-level flow data with high-level intent. For instance,
attacks like DoS lack explicit textual patterns and rely on
subtle indicators (e.g., flow duration and volume). Without
abstraction, the model struggles to contextualize such signals,
often misclassifying them.
Effectiveness of Partitioned Reasoning. Our structured
inference strategy outperforms standard consistency methods
(multi-sampling and self-debate) by about 7–20% in average
accuracy. While baseline methods improve output stability,
they fail to guide the model through complex, multi-step
reasoning—particularly evident in DAPT2020, where top-5
accuracy drops by ∼30% compared to RHINO. By partitioning
the 14 tactics into 5 semantically coherent groups, our approach
narrows the search space, enabling the model to focus on
specific subtasks. This not only improves accuracy but also
ensures better semantic alignment in predictions.
Role of the Refinement Module. While disabling refinement
yields a modest average accuracy decline (1.53% at technique
level of top-1 accuracy), its impact varies by dataset. For
DAPT2020, the absence of refinement causes a significant
10% drop, highlighting its importance in challenging cases. In
contrast, for IoT23 and CICIDS2017—where earlier modules
already achieve high accuracy—the module’s contribution
is less pronounced. Beyond accuracy, refinement enhances
interpretability by providing per-sample confidence scores,
which are invaluable for human-in-the-loop analysis and
forensic applications.
D. RQ3: Error Analysis
This section presents a comprehensive analysis of error
cases in our method, focusing on two main aspects: (1)
mapping errors in technique identification and (2) tactical
consistency in technique-to-tactic associations. These analyses
aim to uncover systemic weaknesses and identify opportunities
for improvement in the model’s reasoning and refinement
processes.
1) Mapping Error Analysis: To quantify the effectiveness
of our method, we performed a manual examination of top-1
mapping errors and compared them with the strongest baseline,
ToT. Errors were identified by contrasting LLM-generated map-
pings with ground-truth malicious behavior descriptions in the


---

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021
10
TABLE V
ERROR RATES (IN PERCENTAGE) OF DIFFERENT ERROR TYPES FOR RHINO
(OURS) AND THE BEST BASELINE METHOD (TOT) USING CHATGPT-4O
ACROSS THREE DATASETS DAPT2020, CICIDS2017, IOT23 AND IN TOTAL.
Error Rate (%)
Dataset
Method
Inference
Error
Technique
Confusion
Over-
inference
Ours
5.29
1.80
5.35
DAPT2020
ToT
14.02
2.72
3.84
Ours
2.76
0
0
CICIDS2017
ToT
10.28
0
0
Ours
1.26
0.05
0
IoT23
ToT
6.89
0
0
Ours
9.31
1.85
5.35
Total
ToT
31.19
2.72
3.84
dataset. Our analysis revealed three primary error categories: (1)
Inference Errors occur when the model misinterprets network
behaviors or attacker intent. For instance, the technique T1071:
Application Layer Protocol (C2 communication) might be
incorrectly mapped to T1046: Network Service Discovery due
to ambiguities in behavioral interpretation. Such errors often
stem from the model’s inability to discern subtle distinctions
in attack semantics. (2) Technique Confusion arises when
semantically similar techniques are conflated. Examples include
T1595: Active Scanning and T1046: Network Service Discov-
ery, which share overlapping behaviors but differ in tactical
objectives. The LLM occasionally overlooks critical metadata
or contextual cues, leading to misclassifications. (3) Over
Inference manifests when the model overemphasizes localized
malicious features while neglecting broader contextual signals.
This is particularly prevalent in logs containing anomalous
but benign patterns (e.g., HTTP status codes 302/404 or SQL
queries) that superficially resemble attack artifacts.
As summarized in Table V, which presents the error rates of
ChatGPT-4o across the DAPT2020, CICIDS2017, and IoT23
datasets, several key observations emerge.
• Inference Accuracy Improvement: Our method reduces
inference errors by 21.88% (absolute) compared to ToT,
demonstrating superior capability in disambiguating attack
intent. This improvement is attributed to the structured
reasoning module, which systematically decomposes be-
havioral patterns and tactical objectives.
• Technique Confusion Mitigation: While our approach
reduces technique confusion errors by 32.21% (relative),
complete elimination remains challenging. Subtle distinc-
tions between techniques (e.g., scanning for reconnais-
sance vs. lateral movement) often require explicit guidance,
which the refinement module partially addresses through
standardized definitions. However, edge cases persist due
to the inherent complexity of attack taxonomies.
• Context-Detail Trade-off: A marginal increase in over-
inference errors (1.51% absolute) was observed, likely
due to the refinement module’s emphasis on tactical scope
narrowing. Although this focus improves precision, it
occasionally leads to overfitting on local features. Despite
this trade-off, our method achieves a net reduction in total
errors.
Collectively, these results underscore our method’s advan-
tages over ToT in accuracy, robustness, and interpretability.
2) Tactical Consistency Analysis: We further evaluated the
alignment between correctly identified techniques and their
associated tactics. For each dataset, we computed the mismatch
rate, which is the proportion of correct technique-to-tactic
mappings that are incorrect. Table VI presents results for the
top-1/3/5 settings across ChatGPT-4o, Claude Sonnet 4, Gemini
2.5 Flash, and DeepSeek V3:
• ChatGPT-4o shows a low total mismatch rate ranging
from 0.05% to 0.99%, indicating occasional tactical mis-
assignments. However, its high technique-level accuracy
ensures minimal operational impact.
• Claude Sonnet 4 maintains nearly perfect consistency,
with no mismatches for top-1/3, except for a minor
mismatch (0.83%) at top-5 on the DAPT2020 dataset,
suggesting its dependable technique-to-tactic alignment.
• Gemini 2.5 Flash Gemini 2.5 Flash demonstrates a total
mismatch rate ranging from 0.33% to 0.51%, with a
particularly high top-1 mismatch rate of 5.16% on the
DAPT2020 dataset. Despite this, Gemini achieves the
highest top-1 accuracy of 88.45%, suggesting that while it
excels in overall accuracy, the model may still encounter
occasional misclassifications on specific data points.
• DeepSeek V3 maintains near-perfect consistency, with no
mismatches at top-1 across all datasets and only minor
mismatches (range from 0.01% to 0.02%) at top-3/5,
demonstrating its precise mapping approach that prioritizes
tactical alignment over extensive coverage.
Claude Sonnet 4 and DeepSeek V3 maintains nearly per-
fect consistency, demonstrating the highest level of tactical
alignment. Meanwhile, ChatGPT-4o shows strong consistency,
slight mismatches are minimal in impact compared to its
superior technique detection. On the other hand, Gemini 2.5
Flash achieves higher accuracy but sacrifices some precision,
which occasionally leads to tactical misassignments. These
results demonstrate the adaptability of our method across
various backbone models, ensuring tactical coherence without
compromising performance.
E. RQ4: Practicality Study
To validate the real-world applicability of our approach, we
integrate our system with an existing CNN+LSTM-based NIDS
framework, evaluating its ability to enhance adversarial network
traffic detection and subsequent attack behavior mapping. We
conduct experiments on two benchmark datasets—CICIDS2017
(diverse attack types) and IoT23 (botnet-focused)—which
reflect realistic attack scenarios. Our study assesses how
effectively our system refines the mapping of attack techniques
and tactics after the NIDS identifies malicious traffic.
Experimental Setup. We deploy the CNN+LSTM NIDS model
from Bamber et al. [22], pretrained on CICIDS2017 and IoT23.
Each dataset is split into 80% training and 20% testing data,
with the model trained for 5 epochs. The NIDS classifies
traffic as benign or malicious; for malicious samples, our
system’s abstraction, inference, and refinement modules map
the behaviors to MITRE ATT&CK techniques and tactics.


---

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021
11
TABLE VI
TACTICAL CONSISTENCY EVALUATION ACROSS THREE DATASETS (DAPT2020, CICIDS2017, IOT23). FOR EACH DATASET, THE TABLE REPORTS THE
NUMBER OF TECHNIQUES CORRECTLY IDENTIFIED (# CORRECT), THE NUMBER OF MISMATCHED TACTICS (# MISMATCHED), AND THE MISMATCH RATE
(REPORTED AS A PERCENTAGE). THE EVALUATION IS PRESENTED FOR TOP-1, TOP-3, AND TOP-5 SETTINGS. THE VALUES FOR # CORRECT, # MISMATCHED,
AND RATE ARE THE AVERAGES FROM THREE INDEPENDENT EXPERIMENTS CONDUCTED ON EACH DATASET.
Top-1
Top-3
Top-5
Model
Dataset
# Correct
# Mismatched
Rate
# Correct
# Mismatched
Rate
# Correct
# Mismatched
Rate
DAPT2020
10,806.67
163.67
1.51%
16,505.00
367.33
2.23%
22,336.33
369.67
1.66%
CICIDS2017
273,385.33
0.00
0.00%
376,053.67
4,970.33
1.32%
376,228.33
4,972.67
1.32%
IoT23
72,994.33
0.00
0.00%
145,676.67
0.00
0.00%
145,680.00
1.33
0.00%
ChatGPT-4o
Total
357,186.33
163.67
0.05%
538,235.33
5,337.67
0.99%
544,244.67
5,343.67
0.98%
DAPT2020
9,707.33
0.00
0.00%
16,652.33
0.00
0.00%
18,185.67
150.33
0.83%
CICIDS2017
225,092.33
0.00
0.00%
347,457.33
0.00
0.00%
350,862.67
0.00
0.00%
IoT23
71,696.67
0.00
0.00%
96,960.33
0.00
0.00%
97,134.67
0.00
0.00%
Claude
Sonnet 4
Total
306,496.33
0.00
0.00%
461,070.00
0.00
0.00%
466,183.00
150.33
0.03%
DAPT2020
8,926.67
460.33
5.16%
18,467.00
463.67
2.51%
18,755.00
463.67
2.47%
CICIDS2017
267,187.33
1,324.00
0.50%
643,048.00
2,310.67
0.36%
652,190.00
3,634.67
0.56%
IoT23
74,401.33
0.00
0.00%
191,186.00
0.00
0.00%
214,609.00
0.00
0.00%
Gemini 2.5
Flash
Total
350,515.33
1,784.33
0.51%
852,701.00
2,774.33
0.33%
885,554.00
4,098.33
0.46%
DAPT2020
7,756.00
0.00
0.00%
10,125.00
1.00
0.01%
10,214.33
1.67
0.02%
CICIDS2017
260,432.00
0.00
0.00%
374,401.00
0.00
0.00%
381,858.67
1.33
0.00%
IoT23
74,418.33
0.00
0.00%
98,075.67
0.00
0.00%
98,145.33
0.00
0.00%
DeepSeek V3
Total
342,606.33
0.00
0.00%
482,601.67
1.00
0.00%
490,218.33
3.00
0.00%
TABLE VII
THE PERFORMANCE METRICS OF THE CNN+LSTM-BASED NIDS ON THE
CICIDS2017 AND IOT23 DATASETS, INCLUDING TRUE POSITIVES (TP),
TRUE NEGATIVES (TN), FALSE POSITIVES (FP), FALSE NEGATIVES (FN),
AND STANDARD EVALUATION METRICS—ACCURACY (AC), PRECISION
(PR), RECALL (RC), AND F1 SCORE.
Dataset
Result Statistics
# TPs
# TNs
# FPs
# FNs
103,150
242,404
49
68
AC (%)
PR (%)
RC (%)
F1 (%)
CICIDS2017
99.97
99.95
99.93
99.94
# TPs
# TNs
# FPs
# FNs
1,398,062
1,575
82
42
AC (%)
PR (%)
RC (%)
F1 (%)
IoT23
99.99
99.99
99.99
99.99
We evaluate NIDS detection performance using standard
metrics: True Positives (TP), True Negatives (TN), False
Positives (FP), False Negatives (FN), Accuracy (AC), Precision
(PR), Recall (RC), and F1 Score. Specifically, a TP occurs
when the system correctly identifies a malicious network flow
based on its feature representation, while a TN represents the
correct classification of a benign flow. Conversely, an FP arises
when the system misclassifies a benign flow as malicious, and
an FN occurs when a malicious flow is erroneously classified
as benign. For attack behavior mapping, we measure top-1,
top-3, and top-5 accuracy for technique and tactic predictions.
Results and Analysis. As shown in Table VII, the NIDS
achieves near-perfect detection on both datasets (99.97%
AC for CICIDS2017; 99.99% for IoT23), demonstrating the
CNN+LSTM model’s robustness. Post-detection, our system
attains 94% top-1 accuracy for technique/tactic mapping on
CICIDS2017 (Figure 4). IoT23 exhibits slightly lower but still
strong performance (>90% top-1), with top-5 tactic accuracy
exceeding 98%, highlighting our method’s adaptability to
specialized attack patterns (e.g., botnets).
These results underscore two key contributions:
• Integration feasibility: Our system seamlessly enhances
NIDS outputs with ATT&CK mappings, adding inter-
pretability without compromising detection efficacy.
Top-1
Top-3
Top-5
0
25
50
75
100
Accuracy (%)
CICIDS2017 - Technique
CICIDS2017 - Tactic
IoT23 - Technique
IoT23 - Tactic
Fig. 4. The top-1, top-3, and top-5 weighted accuracy rates of RHINO in
mapping detected attack behaviors to techniques and tactics for the CICIDS2017
and IoT23 datasets.
• Scalability: Consistent performance across heterogeneous
datasets (general-purpose CICIDS2017 and IoT-specific
IoT23) suggests broader applicability.
This study confirms our approach’s practicality in operational
settings, bridging the gap between detection and actionable
threat intelligence.
VI. DISCUSSION
Token Efficiency vs. Accuracy Trade-off. Our method reveals
a clear trade-off between token consumption and accuracy.
As demonstrated in Figure 5, RHINO achieves significantly
higher accuracy at the expense of increased token usage.
Simpler approaches such as Vanilla and Chain-of-Thought
(CoT) consume fewer tokens but yield lower accuracy, whereas
RHINO improves accuracy by 69.45% (from 18.7% to 88.15%)
compared to Vanilla, despite its higher token cost. This indicates
a fundamental balance between efficiency and performance:
lightweight methods may suffice for latency-sensitive tasks,
while RHINO justifies its additional resource expenditure in
scenarios demanding higher precision and interpretability.
Computational Overhead Justified by Performance Gains.
Regarding computational overhead, RHINO exhibits the longest
inference time (12,768.3s) among the baseline methods.
However, this represents only a 16.97% increase over the
strongest baseline, ToT (10,916.3s), while delivering a 28.65%


---

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021
12
0
5000
10000
15000
20000
25000
Tokens consumption
20
30
40
50
60
70
80
90
100
Top-1 Accuracy (%)
Vanilla
CoT
ToT
Self Debate
Multi Sampling
RHINO
Fig. 5. Cost-effectiveness analysis. Each dot’s size represents the average
token consumption of each method. The y-axis represents the average accuracy
across three datasets.
improvement in average accuracy. This suggests that our
method effectively balances runtime and performance, with
the gains in decision-making quality outweighing the marginal
increase in inference time.
Exclusion of General-Purpose Reasoning LLMs. We de-
liberately excluded general-purpose reasoning LLMs, such
as ChatGPT-o1 or DeepSeek-R1, as backbone models in
our evaluation for two key reasons. First, these models are
not designed to enforce structured execution steps, which
conflicts with the core design principles of our methodology.
Second, their inherent latency and operational costs make them
impractical for multi-step or modular tasks, further highlighting
the need for specialized solutions like RHINO.
VII. RELATED WORK
The mapping of security data to MITRE ATT&CK tactics
and techniques (TTs) is critical for reconstructing adversar-
ial behaviors and understanding advanced threats. Existing
approaches fall into three primary methodological categories:
rule-based systems, learning-based inference models, and LLM-
powered semantic analysis.
Rule-based methods employ predefined mappings, topo-
logical analysis, or static ontologies [6], [11]. For instance,
AttackDynamics [23] constructs attack graphs by correlating
system topology with CAPEC, CWE, and CVE databases.
While these approaches benefit from explicit expert knowledge,
their reliance on manual pattern definitions renders them ineffec-
tive against novel attack techniques or unknown vulnerabilities,
fundamentally limiting their generalizability.
Learning-based approaches [7], [9] address these limita-
tions by inferring TTs from structured observations or system
provenance. SAGE [10] employs rule-based preprocessing
to convert IDS alerts into attack stages before applying
unsupervised sequence modeling to extract multi-stage strate-
gies. ARKAIV [8] maps system logs to tactics and uses
supervised learning to predict data exfiltration outcomes. Recent
advances in provenance graph analysis have shown particular
promise—TREC [24] segments compact subgraphs from large
system provenance data to identify individual APT technique
instances. Through a Siamese neural network architecture and
few-shot learning, TREC overcomes the “needle in a haystack”
challenge of locating sparse attack patterns while addressing the
scarcity of labeled training data. However, these learning-based
methods still face fundamental constraints: SAGE and ARKAIV
operate at the tactical level without fine-grained technique
recognition, while TREC’s dependency on system provenance
graphs limits its applicability to environments where such
detailed audit trails are unavailable.
LLM-based methods have emerged to bridge this semantic
gap by leveraging pretrained language models for TT map-
ping. Daniel et al. [14] employ ChatGPT to annotate Snort
rules with MITRE tactics and techniques, while the RAM
framework [15] uses prompt-chaining to map SIEM queries
to ATT&CK labels. These approaches benefit from LLMs’
broad knowledge base but remain constrained by their input
requirements—they process only curated detection rules rather
than raw observational data, as direct LLM processing of large-
scale logs would be computationally prohibitive. Consequently,
existing implementations rely on rule-based NIDS to perform
initial semantic conversion from raw data to attack labels before
LLM analysis.
Our work introduces a novel synthesis of these paradigms. By
developing a log compression technique that preserves semantic
information, we enable LLMs to analyze raw observational data
without the computational overhead of processing complete
log volumes. This approach eliminates dependency on both
predefined rules (unlike rule-based systems) and labeled
datasets (unlike learning-based methods), while overcoming the
input limitations of current LLM implementations. Through
procedural reasoning, our system bridges the semantic gap
between low-level system events and high-level attacker
behaviors effectively, supporting adaptable TT analysis across
diverse detection paradigms.
VIII. CONCLUSION
RHINO reframes MITRE ATT&CK mapping as a structured
reasoning task, combining context-aware log abstraction, col-
laborative multi-role inference, and definition-aware refinement
to outperform rule-based, learning-based, and monolithic LLM
approaches. Experiments across APT, intrusion, and IoT botnet
scenarios demonstrate >86% top-1 accuracy, with a 4.9%
reduction in hallucinations, while maintaining compatibility
with existing NIDS pipelines. By mirroring human analyst
workflows, RHINO enables reliable, interpretable attack analy-
sis without relying on predefined rules or labeled datasets.
This work advances the state of the art in interpretable
threat analysis, demonstrating that LLMs can excel in complex
security reasoning when guided by structured, human-analogous
workflows. Future directions include extending RHINO to multi-
modal threat intelligence (e.g., logs + provenance graphs) and
optimizing its token efficiency for real-time deployment.
REFERENCES
[1] H.-J. Liao, C.-H. R. Lin, Y.-C. Lin, and K.-Y. Tung, “Intrusion detection
system: A comprehensive review,” Journal of network and computer
applications, vol. 36, no. 1, pp. 16–24, 2013.
[2] J. Koziol, Intrusion detection with Snort.
Sams Publishing, 2003.


---

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021
13
[3] Y. Mirsky, T. Doitshman, Y. Elovici, and A. Shabtai, “Kitsune: an
ensemble of autoencoders for online network intrusion detection,” arXiv
preprint arXiv:1802.09089, 2018.
[4] B. E. Strom, A. Applebaum, D. P. Miller, K. C. Nickels, A. G. Pennington,
and C. B. Thomas, “Mitre att&ck: Design and philosophy,” in Technical
report.
The MITRE Corporation, 2018.
[5] M. Bromiley, “Agentic AI in the SOC: Reducing Alert Fatigue
and Burnout — prophetsecurity.ai,” https://www.prophetsecurity.ai/blog/
agentic-ai-in-the-soc-reducing-alert-fatigue-burnout-attrition, 2025.
[6] A. B. Izzuddin and C. Lim, “Mapping threats in smart grid system using
the mitre att&ck ics framework,” in 2022 IEEE International Conference
on Aerospace Electronics and Remote Sensing Technology (ICARES).
IEEE, 2022, pp. 1–7.
[7] S. M. Milajerdi, R. Gjomemo, B. Eshete, R. Sekar, and V. Venkatakrish-
nan, “Holmes: real-time apt detection through correlation of suspicious
information flows,” in 2019 IEEE symposium on security and privacy
(SP).
IEEE, 2019, pp. 1137–1152.
[8] A. R. Hakim, K. Ramli, M. Salman, B. Pranggono, and E. R. Agustina,
“Predicting data exfiltration using supervised machine learning based on
tactics mapping from threat reports and event logs,” IEEE Access, 2024.
[9] S. Moskal and S. J. Yang, “Translating intrusion alerts to cyberattack
stages using pseudo-active transfer learning (patrl),” in 2021 IEEE
conference on communications and network security (CNS).
IEEE,
2021, pp. 110–118.
[10] A. Nadeem, S. Verwer, S. Moskal, and S. J. Yang, “Alert-driven attack
graph generation using s-pdfa,” IEEE transactions on dependable and
secure computing, vol. 19, no. 2, pp. 731–746, 2021.
[11] Q. Meng, N. Oo, Y. Jiang, H. W. Lim, and B. Sikdar, “Poster: M2ask: A
correlation-based multi-step attack scenario detection framework using
mitre att&ck mapping,” in Proceedings of the 2024 on ACM SIGSAC
Conference on Computer and Communications Security, 2024, pp. 4979–
4981.
[12] Z. Yu, M. Wen, X. Guo, and H. Jin, “Maltracker: A fine-grained npm
malware tracker copiloted by llm-enhanced dataset,” in Proceedings of
the 33rd ACM SIGSOFT International Symposium on Software Testing
and Analysis, 2024, pp. 1759–1771.
[13] Y. Li, C. Huang, S. Deng, M. L. Lock, T. Cao, N. Oo, H. W.
Lim, and B. Hooi, “KnowPhish: Large language models meet
multimodal knowledge graphs for enhancing Reference-Based phishing
detection,” in 33rd USENIX Security Symposium (USENIX Security
24).
Philadelphia, PA: USENIX Association, Aug. 2024, pp. 793–810.
[Online]. Available: https://www.usenix.org/conference/usenixsecurity24/
presentation/li-yuexin
[14] N. Daniel, F. K. Kaiser, A. Dzega, A. Elyashar, and R. Puzis, “Labeling
nids rules with mitre att &ck techniques using chatgpt,” in European
Symposium on Research in Computer Security.
Springer, 2023, pp.
76–91.
[15] P. N. Wudali, M. Kravchik, E. Malul, P. A. Gandhi, Y. Elovici, and
A. Shabtai, “Rule-att&ck mapper (ram): Mapping siem rules to ttps using
llms,” arXiv preprint arXiv:2502.02337, 2025.
[16] D. V. Lindley, “Binomial sampling schemes and the concept of informa-
tion,” Biometrika, vol. 44, no. 1-2, pp. 179–186, 1957.
[17] S. Myneni, A. Chowdhary, A. Sabur, S. Sengupta, G. Agrawal, D. Huang,
and M. Kang, “Dapt 2020-constructing a benchmark dataset for advanced
persistent threats,” in Deployable Machine Learning for Security Defense:
First International Workshop, MLHat 2020, San Diego, CA, USA, August
24, 2020, Proceedings 1.
Springer, 2020, pp. 138–163.
[18] I. Sharafaldin, A. H. Lashkari, A. A. Ghorbani et al., “Toward generating
a new intrusion detection dataset and intrusion traffic characterization.”
ICISSp, vol. 1, pp. 108–116, 2018.
[19] S. Garcia, A. Parmisano, and M. J. Erquiaga, “Iot-23: A labeled dataset
with malicious and benign iot network traffic,” 2020, data set. [Online].
Available: https://doi.org/10.5281/zenodo.4743746
[20] S. Yao, D. Yu, J. Zhao, I. Shafran, T. Griffiths, Y. Cao, and K. Narasimhan,
“Tree of thoughts: Deliberate problem solving with large language models,”
Advances in neural information processing systems, vol. 36, pp. 11 809–
11 822, 2023.
[21] W. Chmielnicki and K. Stapor, “Using the one–versus–rest strategy
with samples balancing to improve pairwise coupling classification,”
International Journal of Applied Mathematics and Computer Science,
vol. 26, 03 2016.
[22] S. S. Bamber, A. V. R. Katkuri, S. Sharma, and M. Angurala, “A
hybrid cnn-lstm approach for intelligent cyber intrusion detection system,”
Computers & Security, vol. 148, p. 104146, 2025.
[23] C. Hankin, P. Malacaria et al., “Attack dynamics: An automatic attack
graph generation framework based on system topology, capec, cwe, and
cve databases,” Computers & Security, vol. 123, p. 102938, 2022.
[24] M. Lv, H. Gao, X. Qiu, T. Chen, T. Zhu, J. Chen, and S. Ji, “Trec: Apt
tactic/technique recognition via few-shot provenance subgraph learning,”
in Proceedings of the 2024 on ACM SIGSAC Conference on Computer
and Communications Security, 2024, pp. 139–152.
