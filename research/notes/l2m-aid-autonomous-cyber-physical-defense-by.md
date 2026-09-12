---
title: 'L2M-AID: Autonomous Cyber-Physical Defense by'
id: l2m-aid-autonomous-cyber-physical-defense-by
tags:
- attack-ontology-drift-cti-85bc51
- pin-rate-survey
created: '2026-09-12T21:33:47.891062Z'
updated: '2026-09-12T21:44:25.016946Z'
source: https://arxiv.org/abs/2510.07363v2
source_domain: arxiv.org
fetched_at: '2026-09-12T21:33:47.890545Z'
fetch_provider: crawl4ai
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'arXiv 2510.07363v2 (2025): uses 4 ATT&CK technique-ID occurrences (without
  sub-techniques); ATT&CK release declaration classified as none.'
raw_file: raw/l2m-aid-autonomous-cyber-physical-defense-by.pdf
doi: arXiv:2510.07363v2
---

L2M-AID: Autonomous Cyber-Physical Defense by
Fusing Semantic Reasoning of Large Language
Models with Multi-Agent Reinforcement Learning
Tianxiang Xu1†, Zhichao Wen2†, Xinyu Zhao 3, Jun Wang4, Yan Li5, Chang Liu6*
1Peking University, Beijing, China
2RWTH Aachen University, Aachen, Germany
3University of Texas at Austin, Austin, USA
4Wuhan University, Wuhan, China
5Thales Group, Ottawa, Canada
6Chinese Medical Information and Big Data Association, Beijing, China
Abstract—The increasing integration of Industrial IoT (IIoT)
exposes critical cyber-physical systems to sophisticated, multi-
stage attacks that elude traditional defenses lacking contextual
awareness. This paper introduces L2M-AID, a novel frame-
work for Autonomous Industrial Defense using LLM-empowered,
Multi-agent reinforcement learning. L2M-AID orchestrates a
team of collaborative agents, each driven by a Large Language
Model (LLM), to achieve adaptive and resilient security. The
core innovation lies in the deep fusion of two AI paradigms:
we leverage an LLM as a semantic bridge to translate vast,
unstructured telemetry into a rich, contextual state representa-
tion, enabling agents to reason about adversary intent rather
than merely matching patterns. This semantically-aware state
empowers a Multi-Agent Reinforcement Learning (MARL) al-
gorithm, MAPPO, to learn complex cooperative strategies. The
MARL reward function is uniquely engineered to balance security
objectives (threat neutralization) with operational imperatives,
explicitly penalizing actions that disrupt physical process stability.
To validate our approach, we conduct extensive experiments
on the benchmark SWaT dataset and a novel synthetic dataset
generated based on the MITRE ATT&CK for ICS framework.
Results demonstrate that L2M-AID significantly outperforms
traditional IDS, deep learning anomaly detectors, and single-agent
RL baselines across key metrics, achieving a 97.2% detection
rate while reducing false positives by over 80% and improving
response times by a factor of four. Crucially, it demonstrates
superior performance in maintaining physical process stability,
presenting a robust new paradigm for securing critical national
infrastructure.
Index Terms—cyber-physical systems security, multi-agent rein-
forcement learning, large language models, autonomous defense,
semantic reasoning
I. INTRODUCTION
The fourth industrial revolution is catalyzing a profound
convergence of Operational Technology (OT) and Information
Technology (IT), forging hyper-connected Industrial IoT (IIoT)
† These authors contributed equally to this work
* Corresponding author: Chang Liu (cryyu1478@outlook.com)
0For any commercial use or derivative works, please contact the
IEEE Copyrights Office at copyrights@ieee.org.
ecosystems that promise unprecedented efficiency gains but
simultaneously introduce a perilous new attack surface [1].
The dissolution of the traditional air-gap has interwoven once-
isolated industrial control systems (ICS) with enterprise net-
works, exposing critical infrastructure to sophisticated cyber-
physical threats where digital intrusions inflict tangible phys-
ical damage [2]. Seminal events like the Stuxnet worm’s
sabotage of nuclear centrifuges [3] and the Mirai botnet’s
weaponization of IoT devices [4] are not mere historical
footnotes, but harbingers of a reality where securing these
deeply coupled systems demands a fundamental rethinking of
our defense posture. Confronted with this landscape, existing
security paradigms are proving critically inadequate. Signature-
based Intrusion Detection Systems (SIDS) are inherently blind
to the zero-day exploits that characterize modern APTs [5],
while Anomaly-based Intrusion Detection Systems (AIDS)
face a fundamental paradox in IIoT. The very predictability
of industrial processes, which simplifies baseline modeling, is
now being exploited by adversaries to orchestrate “low-and-
slow” attacks that mimic legitimate traffic to evade detection
[6], [7]. This underscores a critical flaw: current systems
are sophisticated pattern recognizers but lack genuine intent
understanding. They can flag a statistical anomaly but cannot
discern the malicious intent behind a sequence of seemingly
benign actions, a deficiency exacerbated by the operational
constraints of resource-limited and often unpatchable legacy
systems [8].
To transcend these limitations, we advocate for a paradigm
shift from passive detection to proactive, autonomous defense,
driven by breakthroughs in artificial intelligence. The advent
of Large Language Models (LLMs) offers a transformative
capability, evolving them from mere language processors into
powerful reasoning engines capable of synthesizing vast, het-
erogeneous data streams—from cryptic system logs to open-
source threat intelligence—into a coherent, causal understand-
ing of an unfolding security event [9], [10]. However, in
arXiv:2510.07363v2  [cs.AI]  14 Oct 2025


---

the distributed fabric of IIoT, a monolithic intelligence is a
bottleneck and a single point of failure. This necessitates a
Multi-Agent System (MAS) architecture, where a decentralized
team of specialized agents can offer scalable and resilient de-
fense [11]. This paper introduces L2M-AID, a framework that
materializes this vision. Our central thesis is that a deep fusion
of the high-level semantic reasoning of LLMs with the low-
level, adaptive control of Multi-Agent Reinforcement Learning
(MARL) can bridge the chasm between understanding and
action. L2M-AID orchestrates a hierarchical team of LLM-
empowered agents, trained collectively via the MAPPO algo-
rithm under a Centralized Training, Decentralized Execution
(CTDE) paradigm [12]. Crucially, our MARL formulation is
tailored for the cyber-physical domain, with a reward function
meticulously engineered to balance the dual objectives of threat
neutralization and the preservation of physical process stability.
The primary contributions of this work are threefold:
1) A Novel Hierarchical Multi-Agent Framework: We
design and propose L2M-AID, a role-based, hierarchical
agent architecture that synergistically fuses LLM-driven
semantic reasoning with MARL-based adaptive control,
creating a novel solution for autonomous cyber-physical
defense.
2) A Context-Aware MARL Formulation for IIoT: We
introduce a formal MARL model where the state space is
semantically enriched by LLM-generated contextual em-
beddings, and the reward function explicitly co-optimizes
for security efficacy and physical process stability, bridg-
ing the gap between cyber defense and operational safety.
3) Comprehensive Empirical Validation and Generaliza-
tion: We conduct rigorous experiments on the benchmark
SWaT dataset and a novel synthetic attack dataset derived
from the MITRE ATT&CK for ICS framework, demon-
strating that L2M-AID achieves superior performance
and generalization against a spectrum of baselines.
II. RELATED WORK
This section critically reviews three core research domains
integral to our work: intrusion detection in Industrial Control
Systems (ICS), the application of Large Language Models in
cybersecurity, and Multi-Agent Reinforcement Learning for
network defense. By analyzing the trajectory and inherent
limitations within each domain, we delineate the research
chasm that motivates the novel architectural fusion presented
in our L2M-AID framework.
A. The Evolution and Stalemate in ICS Intrusion Detection
Research in ICS intrusion detection has progressed from
static techniques to sophisticated data-driven models, yet a
fundamental gap in contextual understanding persists. The
complexity of these environments necessitates validation on
high-fidelity datasets sourced from specialized testbeds like
SWaT [13]. Early defense strategies centered on graphical
model-based approaches for anomaly detection [14], which,
Strategic Layer
Tactical Layer
Strategic Orchestrator Agent
• Threat Correlation & Analysis
• Task Decomposition & Delegation
• Situational Awareness
• LLM-powered Reasoning
🧠 LLM
Network Monitoring Agent
• IIoT Protocol Analysis
• Traffic Anomaly Detection
• Real-time Monitoring
Host Analysis Agent
• System Log Analysis
• Process Monitoring
• File System Changes
Threat Intelligence Agent
• IoC Investigation
• External CTI Queries
• Intelligence Synthesis
Mitigation Agent
• Automated Response
• Network Isolation
• Alert Generation
IIoT Environment
• PLCs, HMIs, SCADA
• Sensors & Actuators
• Industrial Networks
👁️
🔍
🧩
🛡️
MARL Training (MAPPO)
Fig. 1.
The hierarchical architecture of L2M-AID, illustrating the strategic
Orchestrator Agent and the tactical Monitoring, Analysis, and Mitigation
Agents. The solid lines represent the primary data and command flow, while
the dashed lines indicate the broadcast of the LLM-generated contextual state
embedding (Lt).
while precise, lacked flexibility against novel attacks. The
field then advanced towards machine learning, with hybrid
algorithms combining techniques like vector quantization and
one-class SVMs showing promise [15]. This was followed by
the rise of deep learning, which demonstrated strong capa-
bilities in omni-directional SCADA intrusion detection [16]
and specialized architectures like 1D-CNN autoencoders for
specific cyber-physical tasks like leakage detection [17].
Despite the increasing sophistication of machine learning
applications in ICS security [18], these models largely function
as reactive pattern recognizers. Their core limitation is that
they operate on raw or statistically-derived features, lacking
the context to interpret the logical sequence of an attack.
They can identify that a state is anomalous, but not why it is
malicious in the context of a broader campaign, such as those
cataloged in the MITRE ATT&CK for ICS framework [19].
This semantic gap is the primary reason for their struggles with
high false positive rates and their inability to counter attackers
who adeptly mimic legitimate operational behavior.
B. LLMs as Semantic Bridges for Cyber Threat Intelligence
Large Language Models (LLMs) have emerged as a powerful
solution to this semantic gap, introducing a paradigm of high-
level reasoning to cybersecurity. Their primary application
lies in automating the cognitive labor of human analysts,
demonstrating profound capabilities in performing advanced
malicious log analysis [20] and extracting structured TTPs
from unstructured threat intelligence [9]. This has naturally led
to their integration with SOAR platforms to automate incident
response, where LLMs can triage alerts and suggest actions
based on predefined playbooks [21]. The latest evolution of
this trend is the development of “generative agents”—LLM-
powered autonomous entities capable of complex, interactive
behavior and planning [22].


---

C. MARL for Adaptive Control and the Research Chasm
Multi-Agent Reinforcement Learning (MARL) provides a
robust framework for translating cognitive understanding into
decentralized, adaptive control. Situated within the fully coop-
erative paradigm as outlined in recent reviews [23], MARL
has gained prominence in network defense, with extensive
studies exploring its applications in communication networks
[24], including MARL-based intrusion detection systems [25]
and reinforcement learning for fine-grained tasks such as
feature selection [26]. The architectural evolution of multi-
agent systems has been further advanced through formalization
of AI agent communication protocols that ensure resilient
coordination [27]. These developments collectively enhance
MARL’s stability and practicality, especially with algorithms
like PPO proving effective in complex cooperative environ-
ments [29]. Despite these advances, a fundamental gap persists
between two powerful yet disconnected paradigms: LLMs
excel in high-level symbolic reasoning but lack adaptive learn-
ing, while MARL offers dynamic sub-symbolic control yet
struggles with semantically rich state spaces [28]. The core
innovation of L2M-AID is bridging this divide through a neuro-
symbolic fusion where the LLM acts as a dynamic “state
shaper” and “reward interpreter” for the MARL algorithm.
The LLM transforms raw, high-dimensional telemetry into
semantically contextualized representations, enabling MARL
agents to learn coordinated, context-aware strategies. In return,
MARL provides the continuous adaptation that LLMs lack,
forming a unified, intelligent defense framework capable of
both reasoning and autonomous control.
III. METHODOLOGY
This section delineates the architectural design and theo-
retical underpinnings of the L2M-AID framework. We first
present the hierarchical multi-agent architecture engineered
for autonomous cyber defense. Subsequently, we provide a
rigorous mathematical formalization of the defense problem as
a cooperative multi-agent reinforcement learning task, detailing
our novel state representation and reward structure. Finally,
we describe the learning algorithm adopted to derive optimal
collaborative defense policies.
A. Hierarchical Multi-Agent Architecture
L2M-AID adopts a hierarchical, distributed multi-agent ar-
chitecture inspired by the functional structure of a Security
Operations Center (SOC). The system separates high-level rea-
soning from low-level execution through two layers: a Strate-
gic Orchestrator Agent and a set of Tactical Agents. The
Orchestrator, powered by a security-domain fine-tuned LLM,
serves as the cognitive core—correlating multi-source alerts,
assessing threats, planning strategic responses, and maintaining
situational awareness through adaptive reasoning. The Tactical
layer comprises specialized agents that sense, analyze, and
act within the IIoT environment: the Network Monitoring
Agent inspects industrial protocols and detects anomalies,
the Host Analysis Agent interprets logs to uncover stealthy
activities, the Threat Intelligence Agent enriches alerts via
internal and external intelligence, and the Mitigation Agent
executes safe, pre-authorized responses. Together, these agents
form a continuous perceive–reason–act cycle that transforms
raw telemetry into contextual understanding and coordinated
defensive actions.
B. Formalization as a Cooperative MARL Task
We formalize the autonomous defense problem as a Decen-
tralized Partially Observable Markov Decision Process (Dec-
POMDP), defined by M = ⟨S, A, P, R, O, Ω, n, γ⟩, where
each agent i observes only oi
t ∈O, a partial view of the
global state st ∈S. This models real IIoT environments where
centralized state observation is infeasible.
1) State and Observation Space (S, O): The global state st
represents the complete IIoT environment at timestep t. Each
agent i perceives a multi-modal local observation:
oi
t = ⟨N i
t , Hi
t, Pi
t, Ci
t, Lt⟩
(1)
where N i
t and Hi
t encode network and host telemetry; Pi
t con-
tains critical physical process variables (pressure, temperature);
and Ci
t buffers inter-agent messages.
Our key contribution is Lt, a shared contextual embed-
ding generated by the Orchestrator’s LLM through periodic
synthesis of aggregated alerts. This dense vector encodes
high-level semantic concepts (e.g., ”reconnaissance detected”,
”lateral movement in progress”) and is broadcast to all agents,
enriching local observations with global context. This mecha-
nism provides implicit coordination, enabling agents to align
behaviors despite partial observability—a fundamental Dec-
POMDP challenge.
2) Action Space (A): The joint action space A = ×n
i=1Ai
comprises discrete, finite action sets per agent. Each Ai is
role-specific to ensure operational safety—e.g., the Mitigation
Agent is restricted to reversible containment operations.
3) Reward Function Engineering (R): We engineer a shared
global reward R(s, a) for joint action a = (a1, . . . , an) that
balances security efficacy with operational constraints:
R(s, a) = wsecRsecurity(s, a) + wprocRprocess(s, a)
+ wcostRcost(a)
(2)
Rsecurity rewards threat neutralization and penalizes missed de-
tections; Rprocess enforces operational safety through penalties
for deviations from safe bounds; Rcost encourages efficiency
via minor action and false positive penalties. The weights
(wsec, wproc, wcost) encode domain-specific risk tolerance, en-
abling customized defense policies.
C. Learning Algorithm: MAPPO with Centralized Training
To solve this Dec-POMDP, we employ Multi-Agent Prox-
imal Policy Optimization (MAPPO), an algorithm that has
demonstrated superior performance and stability in complex
cooperative multi-agent settings [29]. PPO’s core mechanism,


---

PERCEIVE
REASON
ACT
Network Traffic
• Modbus/TCP Packets
• DNP3 Communications
• Industrial Protocols
Host Systems
• System Logs
• Process Activities
• File Changes
Physical Process
• Sensor Readings
• Actuator States
• Control Variables
Network Monitor
• Deep Packet Inspection
• Protocol Analysis
• Anomaly Detection
Threat Intel
• IoC Verification
• CTI Enrichment
• Context Building
Multi-Source Alerts
🚨 Network Anomaly
⚠️ Suspicious Process
🔍 Threat Intelligence
📊 Process Deviation
Strategic Orchestrator
LLM-Powered Reasoning Engine
🧠 LLM
Core
Alert Correlation
• Multi-source fusion
• Pattern recognition
• Timeline analysis
Semantic Reasoning
• Intent analysis
• Attack chain modeling
• Impact assessment
Response Strategy
📋 Action Plan
🎯 Target Selection
⚖️ Risk Assessment
🔄 Feedback Loop
Tactical Commands
🛡️ Isolate Host
🚫 Block Traffic
🔔 Alert Operators
📝 Generate Report
Mitigation Agent
Autonomous Response Executor
Network Actions
• Firewall Rules
• Port Isolation
• Traffic Redirection
System Actions
• Process Termination
• Service Quarantine
• Alert Generation
Execution Results
✅ Threat Neutralized
🔒 System Secured
📈 Process Stability
📊 Performance Metrics
Learning Feedback
🎯 Policy Updates
📖 Knowledge Base
🔄 Model Refinement
📚 Experience Replay
t = 0-5s
t = 5-15s
t = 15-30s
👁️
🧠
⚡
Host Analyzer
• Log Parsing
• Behavioral Analysis
• Event Correlation
Fig. 2. The operational data and decision pipeline of L2M-AID. Tactical agents convert raw data into alerts, which the Orchestrator correlates and reasons
upon to formulate a strategy, finally commanding the Mitigation Agent to act.
the clipped surrogate objective, prevents excessively large
policy updates, which is crucial for stable learning in the non-
stationary environment characteristic of multi-agent systems.
The objective for each agent i’s policy πθi is given by:
L(θi) = Et
h
min(rt(θi) ˆAt, clip(rt(θi), 1 −ϵ, 1 + ϵ) ˆAt)
i
(3)
where rt(θi) =
πθi(at|ot)
πθi,old(at|ot) is the probability ratio and ˆAt is
the estimated advantage function.
We adopt the Centralized Training for Decentralized Execu-
tion (CTDE) paradigm. During the centralized training phase,
we introduce a centralized critic that has access to the global
state s (or the full set of observations {o1, . . . , on}), enabling
it to learn an accurate joint-action value function V (s). This
global perspective provides a stable and informative learning
signal that effectively addresses the credit assignment problem
and mitigates the non-stationarity arising from concurrently
learning policies. For decentralized execution, once the training
converges, the centralized critic is discarded. Each agent i
then operates autonomously in the deployment environment,
executing its learned policy πθi based solely on its local
observation history. This decoupling ensures that the deployed
system is scalable, robust, and maintains a low-latency re-
sponse capability, as it eliminates the need for a centralized
controller at runtime.
IV. EXPERIMENTAL EVALUATION
To rigorously assess the efficacy and cyber-physical safety
of the L2M-AID framework, we conducted a series of com-
prehensive experiments. This section details the experimental
setup, including the evaluation datasets and our novel synthetic
attack generation methodology. We then specify the implemen-
tation details, the baseline models against which L2M-AID is
benchmarked, and the metrics used for performance evaluation.
Finally, we present and analyze the quantitative results, includ-
ing a crucial ablation study, and provide a qualitative case study
to illustrate the framework’s operational intelligence.
TABLE I
KEY HYPERPARAMETER CONFIGURATION
Category
Parameter
Value
MAPPO Algorithm
Actor Learning Rate (αactor)
5e-4
Critic Learning Rate (αcritic)
5e-4
Discount Factor (γ)
0.99
GAE Lambda (λ)
0.95
PPO Clip Parameter (ϵ)
0.2
Training Epochs
10
Neural Network
Actor/Critic Network
3-layer MLP
Architecture
Activation Function
ReLU
LLM Parameters
Base Model
Llama-3-8B-Instruct
Temperature
0.2
Top-p
0.9
Reward Weights
Security Weight (wsec)
1.0
Process
Stability
Weight
(wproc)
2.0
Cost Weight (wcost)
0.1
A. Evaluation Datasets and Methodology
Our evaluation leverages an offline replay methodology,
where the defense framework processes datasets chronolog-
ically. At each timestep, agents make decisions based on
their current observations, and the efficacy of these actions is
evaluated against ground-truth labels. This approach enables
a deterministic and reproducible assessment of the agents’
learned policies.
1) SWaT Benchmark Dataset: The primary evaluation is
performed on the Secure Water Treatment (SWaT) dataset, a
widely recognized gold-standard benchmark for ICS security
research [13]. Generated from a fully operational, industrial-
scale water treatment testbed, the dataset provides eleven days
of continuous sensor and actuator data, synchronized with
network traffic captures. This period includes seven days of
normal operations and four days featuring 36 distinct multi-
stage cyber-physical attacks, complete with precise tempo-
ral ground-truth labels. The high fidelity of SWaT and its
integration of both cyber and physical data are crucial for


---

Detection
Rate
Precision
Response
Speed
Process
Stability
Generalization
Efficiency
20%
40%
60%
80%
100%
Overall Performance Profile
L2M-AID
Best Baseline
L2M-AID
w/o LLM
Single
PPO
LSTM-AE
60
70
80
90
100
Detection Rate (%)
Detection Performance
SWaT
Synthetic
L2M-AID
w/o LLM
Single
PPO
LSTM-AE
0
2
4
6
8
10
FPR (%)
False Positive Rate
SWaT
Synthetic
L2M-AID
w/o LLM
Single PPO
0
100
200
300
Response Time (s)
MTTR Distribution
L2M-AID
w/o LLM
Single
PPO
LSTM-AE
0
2
4
6
8
10
PSI Score
Process Stability
SWaT
Synthetic
0
20
40
60
80
100
120
Training Epochs
0.0
0.2
0.4
0.6
0.8
1.0
1.2
Normalized Reward
L2M-AID
converged
Single PPO
converged
w/o LLM
converged
Training Convergence Comparison
L2M-AID
Single-Agent PPO
L2M-AID (w/o LLM)
Reconnaissance
Lateral Movement
Data Manipulation
Process Impact
L2M-AID
w/o LLM
Single PPO
LSTM-AE
98%
97%
96%
97%
90%
87%
85%
88%
92%
90%
89%
91%
85%
82%
78%
74%
Detection Rate by Attack Type (%)
70
75
80
85
90
95
100
Detection Rate (%)
L2M-AID Performance Dashboard - Complete Experimental Results
Fig. 3.
Comprehensive performance dashboard for L2M-AID and baseline
models. The radar chart provides a holistic view of normalized performance
across five key axes. Bar and box plots detail performance on SWaT and
Synthetic datasets for Detection Rate, False Positive Rate (FPR), Mean
Time to Respond (MTTR), and Process Stability Index (PSI). The line chart
compares training convergence speeds, and the heatmap breaks down detection
performance by attack category.
validating L2M-AID’s core competency in defending cyber-
physical processes.
2) Synthetic Attack Dataset with Conditional GANs: To
evaluate generalization against zero-day threats, we developed
a synthetic dataset generation pipeline that transcends static
benchmark limitations. Our four-stage methodology synthe-
sizes physically-consistent attack scenarios derived from threat
intelligence: 1) We establish benign operational baselines from
seven days of normal SWaT data, extracting temporal patterns
and cross-sensor correlations. 2) We formalize adversarial
behavior as an attack graph based on MITRE ATT&CK
for ICS [19], where vertices represent tactics and weighted
edges encode transition probabilities. 3) Treating this graph
as an HMM, we perform probabilistic traversals to generate
diverse TTP sequences absent from original SWaT attacks
[30]. 4) We employ a conditional TimeGAN [31] to inject
attacks while preserving physical consistency—the generator
learns normal process dynamics and uses TTP sequences
as conditioning inputs to guide anomaly injection. Crucially,
our approach ensures physical coupling: when manifesting
TTP T0831 ”Manipulation of Control” on sensor ‘LIT101‘,
correlated sensors like ‘FIT101‘ exhibit consistent deviations
based on hydraulic constraints. This physics-aware synthesis
yields realistic, stealthy attacks that respect process dynamics,
providing a rigorous generalization testbed.
B. Implementation Details and Baselines
L2M-AID was implemented using PyTorch with the Mi-
crosoft AutoGen framework [10] providing agent communi-
cation infrastructure. The reasoning core employs Llama-3-
8B-Instruct [32], fine-tuned on a domain-specific corpus of
cybersecurity reports, ICS protocol specifications, and MITRE
ATT&CK for ICS TTPs to enhance security-specific reasoning.
The MARL component utilizes EPyMARL with hyperparam-
eters detailed in Table I. We evaluate against four baselines
representing distinct defense paradigms:
1) Signature-based IDS (Snort): Traditional network de-
fense using Emerging Threats rules supplemented with
SCADA-specific signatures.
2) Unsupervised Anomaly Detection (LSTM-AE): State-
of-the-art deep learning model detecting statistical devi-
ations without semantic understanding.
3) Single-Agent DRL (PPO): Monolithic PPO agent ob-
serving the flattened state vector with unified action
space, testing whether multi-agent decomposition pro-
vides advantages.
4) L2M-AID (w/o LLM): Ablation variant removing the
LLM-generated contextual embedding (Lt) to isolate
semantic reasoning contributions.
C. Evaluation Metrics
Performance is assessed using a suite of metrics that
capture both security effectiveness and operational impact.
We use standard security metrics including Detection Rate
(DR) (TP/(TP + FN)) and False Positive Rate (FPR)
(FP/(FP + TN)). To measure responsiveness, we report the
Mean Time to Respond (MTTR), calculated as the average
duration from the onset of a malicious event to the execution of
a correct mitigation action. Critically, to quantify the impact on
the physical process, we introduce the Process Stability Index
(PSI), a metric defined as the inverse of the Root Mean Square
Error between key physical variables and their safe operational
setpoints during a security event. A higher PSI value signifies
less deviation from the safe state and thus better operational
safety.
PSI =


v
u
u
t
1
T · K
T
X
t=1
K
X
k=1
(P obs
t,k −P setpoint
k
)2


−1
(4)
Here, T is the event duration, K is the number of monitored
physical variables, P obs
t,k is the observed value, and P setpoint
k
is
the safe setpoint.
D. Results and Analysis
1) Overall Performance and Training Dynamics: Table II
and Figure 3 demonstrate L2M-AID’s superiority. On the
SWaT dataset, L2M-AID achieves 97.2%±1.5 detection rate
while maintaining 0.9%±0.2 false positive rate. This low FPR
results from the LLM’s semantic contextualization, effectively
distinguishing genuine threats from benign operational anoma-
lies that plague unsupervised methods. The framework’s rapid
response capability is evidenced by its MTTR of 28.6±4.1
seconds—four times faster than Single-Agent PPO. Training
convergence analysis shows L2M-AID reaches higher final
rewards and stabilizes around epoch 80, indicating efficient


---

Detection
Rate
False
Positive
Rate
Process
Stability
0
10
20
30
40
50
60
70
80
Improvement (%)
+9.5%
+63.3%
+72.3%
(a) LLM Contribution to Performance
DR (%)
FPR (%)
MTTR (s)
PSI
0
20
40
60
80
100
Normalized Performance
(b) Multi-Agent vs Single-Agent Architecture
Multi-Agent (L2M-AID)
Single-Agent PPO
0
200
400
600
800
1000
Training Episodes
0
1
2
3
Reward Value
(c) Reward Function Component Evolution
Security (w=1.0)
Process Stability (w=2.0)
Cost (w=0.1)
Total Reward
L2M-AID Component Analysis
Fig. 4.
Component analysis of L2M-AID. (a) Performance improvement
percentage gained from including the LLM, showing its dominant impact
on reducing false positives and maintaining process stability. (b) Normalized
performance comparison between the Multi-Agent (L2M-AID) and Single-
Agent architectures. (c) Evolution of the constituent parts of the global
reward function during training, demonstrating the successful co-optimization
of security and process stability.
learning through structured multi-agent decomposition. The
framework maintains robust detection across all attack stages,
from initial Reconnaissance (98% DR) to final Process Impact
(97% DR).
TABLE II
OVERALL PERFORMANCE COMPARISON ON THE SWAT DATASET (MEAN
± STD. DEV. OVER 5 RUNS)
Model
DR (%)
FPR (%)
MTTR (s)
PSI
Snort
41.7±2.1
0.1±0.05
–
1.8±0.3
LSTM-AE
88.9±3.5
5.6±0.8
–
3.5±0.6
Single-Agent PPO
91.2±2.8
3.1±0.5
125.4±15.2
4.2±0.7
L2M-AID
97.2±1.5
0.9±0.2
28.6±4.1
8.9±1.1
2) Component Contribution and Generalization: Ablation
studies (Figure 4, Table III) dissect the framework’s perfor-
mance drivers. The LLM’s semantic reasoning contribution
is substantial: 9.5% DR improvement, but more critically,
63.3% false positive reduction and 72.3% process stability
enhancement. This validates our core hypothesis that the LLM
acts as a powerful semantic filter, dramatically improving au-
tonomous action quality and safety. The multi-agent paradigm’s
superiority over monolithic approaches is confirmed—L2M-
AID outperforms Single-Agent PPO across all metrics, par-
ticularly in reducing FPR and MTTR while improving PSI,
demonstrating that role specialization enables effective dis-
tributed threat handling. Reward engineering analysis (Figure
4(c)) shows agents successfully maximize the Process Stability
component (w = 2.0) while optimizing Security (w = 1.0),
confirming the reward structure guides policies toward both
security and operational safety. These design choices enable
excellent generalization: L2M-AID maintains 94.5% DR and
8.1 PSI on challenging synthetic zero-day attacks, significantly
exceeding all baselines.
TABLE III
ABLATION STUDY ON SYNTHETIC DATASET
Model Variant
DR (%)
FPR (%)
PSI
L2M-AID (Full)
94.5
1.8
8.1
L2M-AID (w/o LLM)
86.3
4.9
4.7
Single-Agent PPO
83.1
5.5
3.9
LSTM-AE
72.4
9.2
2.6
E. Qualitative Case Study
To provide qualitative insight, we analyzed the framework’s
behavior during a synthetic multi-stage attack involving re-
connaissance (T0819), data manipulation (T0846), and pro-
cess impairment (T0831). The LSTM-AE baseline flagged an
anomaly on the target sensor (LIT-301) late in the attack
chain but provided no actionable context. In stark contrast,
L2M-AID exhibited intelligent, coordinated behavior. The Net-
work and Host agents detected early, low-level indicators.
The Orchestrator agent received these disparate alerts and,
using its LLM core, reasoned that the sequence of events was
strongly indicative of an ”Impair Process Control” campaign.
It then generated a high-level strategic goal and commanded
the Mitigation Agent to isolate the specific PLC controlling the
affected subsystem. The entire perceive-reason-act cycle was
completed in under 30 seconds, preempting a physical overflow
event. This case vividly illustrates L2M-AID’s ability to move
beyond mere anomaly detection to achieve a genuine, context-
aware understanding of adversary intent and execute a precise,
autonomous response.
V. CONCLUSION AND FUTURE OUTLOOK
This paper presented L2M-AID, an autonomous defense
framework that fuses Large Language Models (LLMs) with
Multi-Agent Reinforcement Learning (MARL) to tackle dy-
namic cyber-physical threats in Industrial IoT. By orchestrating
hierarchical LLM-empowered agents, the framework automates
the entire security operations lifecycle, where LLMs serve as
semantic bridges transforming raw telemetry into contextual
knowledge for MARL agents to learn cooperative defense
strategies. Experiments demonstrated clear superiority over
baselines in detection accuracy, response efficiency, false pos-
itive reduction, and Process Stability Index (PSI), confirm-
ing its ability to harmonize cyber defense with operational
safety. Looking ahead, key research directions include bridging
the simulation-to-reality gap, strengthening resilience against
adversarial AI (e.g., prompt injection, data poisoning), and
enhancing explainability of MARL decisions. Future efforts
will pursue adversarial self-play with AI-driven Red Teams,
hierarchical MARL for long-term strategy, and generative
LLM explanations to build trusted, explainable, and resilient
autonomous security systems.


---

REFERENCES
[1] L. D. Xu, E. L. Xu, and L. Li, “Industry 4.0: a survey on technologies,
applications and open research issues,” Journal of Industrial Information
Integration, vol. 10, pp. 1–25, 2018.
[2] M. A. Ferrag, L. Maglaras, S. Moschoyiannis, and H. Janicke, “Deep
learning for cyber security intrusion detection: Approaches, datasets, and
comparative study,” Journal of Information Security and Applications,
vol. 50, p. 102419, 2020.
[3] R. Langner, “Stuxnet: Dissecting a cyberwarfare weapon,” IEEE Security
& Privacy, vol. 9, no. 3, pp. 49–51, 2011.
[4] M. Antonakakis, T. April, M. Bailey, et al., “Understanding the Mirai bot-
net,” in Proceedings of the 26th USENIX Security Symposium (USENIX
Security 17), pp. 1093–1110, 2017.
[5] A. Khraisat, I. Gondal, P. Vamplew, and J. Kamruzzaman, “Survey
of intrusion detection systems: techniques, datasets and challenges,”
Cybersecurity, vol. 2, no. 1, pp. 1–22, 2019.
[6] Y. Hu, A. Yang, H. Li, Y. Sun, and L. Sun, “A survey of intrusion detec-
tion on industrial control systems,” International Journal of Distributed
Sensor Networks, vol. 14, no. 8, p. 1550147718794615, 2018.
[7] J. Giraldo, D. Urbina, A. Cardenas, et al., “A survey of physics-based
attack detection in cyber-physical systems,” ACM Computing Surveys
(CSUR), vol. 51, no. 4, pp. 1–36, 2018.
[8] S. Ghosh and S. Sampalli, “A survey of security in SCADA networks:
Current issues and future challenges,” IEEE Access, vol. 7, pp. 135812–
135831, 2019.
[9] G. d. J. C. da Silva and C. B. Westphall, “A survey of large language
models in cybersecurity,” arXiv preprint arXiv:2402.16968, 2024.
[10] Q. Wu, G. Bansal, J. Zhang, et al., “Autogen: Enabling next-gen
LLM applications via multi-agent conversations,” in arXiv preprint
arXiv:2308.08155, 2023.
[11] S. Oesch, A. Chaulagain, B. Weber, et al., “Towards a high fidelity train-
ing environment for autonomous cyber defense agents,” in Proceedings of
the 17th Cyber Security Experimentation and Test Workshop, pp. 91–99,
2024.
[12] R. Lowe, Y. I. Wu, A. Tamar, et al., “Multi-agent actor-critic for mixed
cooperative-competitive environments,” Advances in Neural Information
Processing Systems, vol. 30, 2017.
[13] A. P. Mathur and N. O. Tippenhauer, “SWaT: A water treatment testbed
for research and training on ICS security,” in 2016 International Work-
shop on Cyber-Physical Systems for Smart Water Networks (CySWater),
pp. 31–36, 2016.
[14] Q. Lin, S. Adepu, S. Verwer, and A. Mathur, “TABOR: A graphical
model-based approach for anomaly detection in industrial control sys-
tems,” in Proceedings of the 2018 Asia Conference on Computer and
Communications Security, pp. 525–536, 2018.
[15] J. Pang, X. Pu, and C. Li, “A hybrid algorithm incorporating vector
quantization and one-class support vector machine for industrial anomaly
detection,” IEEE Transactions on Industrial Informatics, vol. 18, no. 12,
pp. 8786–8796, 2022.
[16] J. Gao, L. Gan, F. Buschendorf, et al., “Omni SCADA intrusion detection
using deep learning algorithms,” IEEE Internet of Things Journal, vol.
8, no. 2, pp. 951–961, 2020.
[17] H. M. Tornyeviadzi and R. Seidu, “Leakage detection in water distribu-
tion networks via 1D CNN deep autoencoder for multivariate SCADA
data,” Engineering Applications of Artificial Intelligence, vol. 122, p.
106062, 2023.
[18] B. Madupati, “Machine Learning for Cybersecurity in Industrial Control
Systems (ICS),” Available at SSRN 5076696, 2022.
[19] O. Alexander, M. Belisle, and J. Steele, “MITRE ATT&CK for industrial
control systems: Design and philosophy,” The MITRE Corporation:
Bedford, MA, USA, vol. 29, pp. 21–85, 2020.
[20] M. Boffa, I. Drago, M. Mellia, et al., “LogPr´ecis: Unleashing language
models for automated malicious log analysis,” Computers & Security,
vol. 141, p. 103805, 2024.
[21] S. Guduru, “Autonomous cyber defense: LLM-Powered incident response
with LangChain and SOAR integration,” Journal ID, vol. 9471, p. 1297,
2025.
[22] J. S. Park, J. O’Brien, C. J. Cai, et al., “Generative agents: Interactive
simulacra of human behavior,” in Proceedings of the 36th Annual ACM
Symposium on User Interface Software and Technology, pp. 1–22, 2023.
[23] A. Oroojlooy and D. Hajinezhad, “A review of cooperative multi-agent
deep reinforcement learning,” Applied Intelligence, vol. 53, no. 11, pp.
13677–13722, 2023.
[24] H. Kheddar, D. W. Dawoud, A. I. Awad, et al., “Reinforcement-learning-
based intrusion detection in communication networks: A review,” IEEE
Communications Surveys & Tutorials, 2024.
[25] A. Tellache, A. Mokhtari, A. A. Korba, and Y. Ghamri-Doudane, “Multi-
agent reinforcement learning-based network intrusion detection system,”
in NOMS 2024-2024 IEEE Network Operations and Management Sym-
posium, pp. 1–9, 2024.
[26] K. Ren, Y. Zeng, Y. Zhong, et al., “MAFSIDS: a reinforcement learning-
based intrusion detection model for multi-agent feature selection net-
works,” Journal of Big Data, vol. 10, no. 1, p. 137, 2023.
[27] Y. Yang, H. Chai, Y. Song, et al., “A survey of AI agent protocols,” arXiv
preprint arXiv:2504.16736, 2025.
[28] Y.-F. Hsu and M. Matsuoka, “A deep reinforcement learning approach
for anomaly network intrusion detection system,” in 2020 IEEE 9th
International Conference on Cloud Networking (CloudNet), pp. 1–6,
2020.
[29] C. Yu, A. Velu, E. Vinitsky, et al., “The surprising effectiveness of
PPO in cooperative multi-agent games,” Advances in Neural Information
Processing Systems, vol. 35, 2022.
[30] S. Choi, J.-H. Yun, and B.-G. Min, “Probabilistic attack sequence
generation and execution based on MITRE ATT&CK for ICS datasets,”
in Proceedings of the 14th Cyber Security Experimentation and Test
Workshop, pp. 41–48, 2021.
[31] J. Yoon, D. Jarrett, and M. Van der Schaar, “Time-series generative ad-
versarial networks,” Advances in Neural Information Processing Systems,
vol. 32, 2019.
[32] A. Dubey, A. Jauhri, A. Pandey, et al., “The LLaMA 3 herd of models,”
arXiv e-prints, p. arXiv–2407, 2024.
