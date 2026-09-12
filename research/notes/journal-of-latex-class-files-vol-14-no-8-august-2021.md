---
title: JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021
id: journal-of-latex-class-files-vol-14-no-8-august-2021
tags:
- attack-ontology-drift-cti-85bc51
- pin-rate-survey
created: '2026-09-12T21:32:21.846366Z'
updated: '2026-09-12T21:44:19.867945Z'
source: https://arxiv.org/abs/2512.09485v1
source_domain: arxiv.org
fetched_at: '2026-09-12T21:32:21.838735Z'
fetch_provider: crawl4ai
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'arXiv 2512.09485v1: 0 ATT&CK technique-ID occurrences, below the pin-rate-survey
  inclusion threshold of 3.'
raw_file: raw/journal-of-latex-class-files-vol-14-no-8-august-2021.pdf
doi: arXiv:2512.09485v1
---

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021
1
Advancing LLM-Based Security Automation with Customized Group
Relative Policy Optimization for Zero-Touch Networks
Xinye Cao, Graduate Student Member, IEEE, Yihan Lin, Guoshun Nan, Member, IEEE, Qinchuan Zhou,
Yuhang Luo, Yurui Gao, Zeliang Zhang, Haolang Lu, Qimei Cui, Senior Member, IEEE,
Yanzhao Hou, Member, IEEE, Xiaofeng Tao, Senior Member, IEEE, Tony Q.S. Quek, Fellow, IEEE
Abstract—Zero-Touch Networks (ZTNs) represent a transfor-
mative paradigm toward fully automated and intelligent net-
work management, providing the scalability and adaptability
required for the complexity of sixth-generation (6G) networks.
However, the distributed architecture, high openness, and deep
heterogeneity of 6G networks expand the attack surface and
pose unprecedented security challenges. To address this, security
automation aims to enable intelligent security management across
dynamic and complex environments, serving as a key capability
for securing 6G ZTNs. Despite its promise, implementing security
automation in 6G ZTNs presents two primary challenges: 1)
automating the lifecycle from security strategy generation to
validation and update under real-world, parallel, and adversarial
conditions, and 2) adapting security strategies to evolving threats
and dynamic environments. This motivates us to propose SecLoop
and SA-GRPO. SecLoop constitutes the first fully automated
framework that integrates large language models (LLMs) across
the entire lifecycle of security strategy generation, orchestration,
response, and feedback, enabling intelligent and adaptive de-
fenses in dynamic network environments, thus tackling the first
challenge. Furthermore, we propose SA-GRPO, a novel security-
aware group relative policy optimization algorithm that itera-
tively refines security strategies by contrasting group feedback
collected from parallel SecLoop executions, thereby addressing
the second challenge. Extensive real-world experiments on five
benchmarks, including 11 MITRE ATT&CK processes and over
20 types of attacks, demonstrate the superiority of the proposed
SecLoop and SA-GRPO. We will release our platform to the
community, facilitating the advancement of security automation
towards next generation communications.
Index Terms—Security automation, LLM, GRPO, zero-touch
networks, 6G.
This work was supported in part by the National Natural Science Foun-
dation of China under Grant 62471064; in part by the National Research
Foundation, Singapore and Infocomm Media Development Authority under
its Communications and Connectivity Bridging Funding Initiative; in part by
the Beijing Natural Science Foundation Program (No.L232002); in part by
Beijing University of Posts and Telecommunications (BUPT) Excellent Ph.
D. Students Foundation under Grant CX20252013; and in part by Beijing
Natural Science Foundation under Grant QY25332. Any opinions, findings
and conclusions or recommendations expressed in this material are those of
the author(s) and do not reflect the views of National Research Foundation,
Singapore. (Xinye Cao and Yihan Lin contributed equally to this work.)
(Corresponding authors: Guoshun Nan; Tony Q.S. Quek.)
Xinye Cao, Yihan Lin, Guoshun Nan, Qinchuan Zhou, Yuhang Luo,
Yurui Gao, Zeliang Zhang, Haolang Lu, Qimei Cui, Yanzhao Hou, Xiaofeng
Tao are with National Engineering Research Center for Mobile Network
Technologies, Beijing University of Posts and Telecommunications, China. (e-
mail: caoxinye@bupt.edu.cn; linjhs@bupt.edu.cn; nanguo2021@bupt.edu.cn;
kevinlvrain@bupt.edu.cn;
lyh eddiemurphy@bupt.edu.cn;
gaoyu-
rui813@bupt.edu.cn;
2023211490@bupt.cn;
lhl 2507@bupt.edu.cn;
cuiqimei@bupt.edu.cn; houyanzhao@bupt.edu.cn; taoxf.bupt@gmail.com).
Tony Q.S. Quek is with the Singapore University of Technology and
Design, Singapore 487372, and also with the Department of Electronic
Engineering, Kyung Hee University, Yongin 17104, South Korea (e-mail:
tonyquek@sutd.edu.sg).
Fig. 1.
Illustration of various attacks in zero-touch networks. Zero-touch
networks introduce the software defined network (SDN) framework and
automated management. The openness of 6G ZTN is accompanied with
various attacks, such as DDoS, SQL injection, and man-in-the-middle (MITM)
attacks.
I. INTRODUCTION
A. Background
W
ITH the commercialization of 5G, research efforts
have rapidly shifted toward the exploration of 6G
networks. According to the 6G vision recommendation [1]
released by the ITU-R, security has been identified as one
of the fundamental design principles of 6G networks, while
the deep integration of artificial intelligence (AI) and com-
munication [2]–[4] is considered among the six representative
usage scenarios. Zero-touch networks [5]–[7] have emerged as
a key solution for achieving fully automated network opera-
tions, offering essential capabilities such as self-configuration,
self-monitoring, self-healing, and self-optimization. ZTNs are
expected to play a pivotal role in 6G networks by addressing
the growing demand for virtualized network functions [8] and
aligning with the trend toward software-defined and automated
architectures [9]. The primary objective of ZTNs is to execute
various network management and control tasks autonomously,
without the need for human intervention.
6G ZTNs, as illustrated in Figure 1, expand the attack
surface due to the open architectures, distributed networks,
and heterogeneous environments, thereby increasing the com-
plexity of threat detection and mitigation [10], [11]. For
instance, adversaries may launch distributed denial-of-service
(DDoS) attacks to disrupt communication services, or SQL
arXiv:2512.09485v1  [cs.CR]  10 Dec 2025


---

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021
2
injections to affect sensitive user information [12]. Traditional
protection mechanisms [13], [14] are insufficient to cope
with these emerging threats, highlighting the urgent need
for intelligent, adaptive, and context-aware security solutions
to ensure resilient and efficient defense in next generation
communication systems. LLMs [15]–[19], as a transformative
technology in the field of artificial intelligence, are reshaping
the landscape of network security. With their advanced natu-
ral language understanding and autonomous decision-making
capabilities, LLMs significantly enhance the effectiveness of
threat detection, analysis, and mitigation in next generation
communication systems.
B. Motivation
The security vulnerabilities exposed by the openness and
heterogeneity of 6G and ZTNs call for a fundamental re-
thinking of network security architecture to defend diverse
and evolving threats in dynamic environments [20], [21]. Cur-
rent security orchestration, automation, and response (SOAR)
platforms [22]–[24] largely rely on handcrafted rule sets or
template-based response strategies. However, such approaches
often fail to cope with advanced persistent threats, multi-
stage attacks, or highly obfuscated adversarial behaviors. Fur-
thermore, most systems only generate recommended strate-
gies, lacking direct executability and seamless integration
with diverse security tools, hindering practical deployment. In
summary, existing security approaches for 6G ZTNs face two
fundamental challenges:
1) Automating the lifecycle from security strategy gen-
eration to validation and update: Conventional security au-
tomation systems are often limited to strategy generation [22],
[25], [26] or tool invocation [27], [28], lacking a complete
and automated workflow. They require substantial manual
intervention and offer limited adaptability. In contrast, a fully
autonomous end-to-end security system must seamlessly coor-
dinate attack simulation, environment configuration, strategy
generation, tool execution, and feedback-driven refinement.
Achieving such integration poses significant challenges for the
intelligence of the system in the real world.
2) Adapting security strategies to evolving threats and
dynamic environments: Traditional approaches often rely
on supervised learning [29]–[31], which demands experts to
annotate data that is costly and difficult to maintain. Moreover,
static datasets fail to capture the dynamic characteristics of
real-world attacks, leading to poor generalization for evolving
threats and zero-day attacks. To enable adaptive and robust
defense, it is essential to develop learning mechanisms with
minimal supervision and continuously refine strategies based
on real-time feedback from heterogeneous environments.
C. Our Method
The aforementioned issues motivate us to propose SecLoop
and SA-GRPO. A group of security strategies generated by
SA-GRPO is deployed across parallel real-world environments
instantiated by SecLoop and is iteratively refined based on
feedback. We outline six high-level design principles for
SecLoop and SA-GRPO to tackle the two challenges.
1) Learnable: The system should possess the ability to con-
tinuously learn from diverse and evolving network conditions.
2) Adaptive: To ensure resilience in rapidly changing environ-
ments, the system must dynamically respond to diverse threat
intelligence and adjust defensive strategies accordingly.
3) Practical: Generated strategies should be practical and
tightly aligned with the execution capabilities of the underlying
defense infrastructure.
4) Automatic: The system must support full automation
across the security lifecycle, from threat simulation to strategy
execution and feedback refinement, eliminating the need for
manual intervention.
5) Efficient: To accelerate learning and improve responsive-
ness, the system should support parallel execution of candidate
strategies in realistic environments, enabling fast validation
and feedback cycles.
6) Pluggable: Given the heterogeneity of network infrastruc-
tures and evolving security tools, the system should maintain
a modular architecture, allowing flexible integration and re-
placement of components.
Keeping the above goals in mind, we design and implement
SecLoop, an end-to-end security automation framework that
enables strategy generation, execution, and feedback across
real-world environments. SecLoop supports parallel deploy-
ment of diverse security strategies in isolated, virtualized
environments and integrates LLMs as intelligent decision
agents. These agents interact with streaming alerts from in-
trusion detection systems (IDS) and trigger responses through
orchestrated security tools. To optimize decision-making under
limited supervision, we further propose SA-GRPO, a security-
aware group relative policy optimization algorithm. SA-GRPO
generates a group of candidate strategies and deploys them
concurrently in SecLoop environments. Feedback collected
during execution is used to iteratively refine the policy through
reinforcement learning. Through customized rewards, includ-
ing format, execution, evaluation, and penalty, SA-GRPO can
be tailored to security-specific scenarios. Extensive experi-
ments on five benchmarks over 20 types of attack demonstrate
the effectiveness of our proposed framework. Our code is
publicly available1.
D. Main Contributions
The main contributions of this paper are threefold:
❶LLM Agent Empowered Security System: We design and
implement SecLoop, the first end-to-end security strategy gen-
eration, orchestration, response, and feedback system, enabling
adaptation of defensive strategies against evolving cyberthreats
in 6G zero-touch networks. Integrated with native LLM and
automated real-world BATTLE-FIELD (Blue And red Team
Tactical Learning Environments For Intrusion, ExpLoitation,
and Defense), SecLoop supports comprehensive attack simu-
lation encompassing the ATT&CK process, provides a robust
environment for fine-tuning LLMs and validating security
algorithms under realistic adversarial conditions.
❷Security-Aware GRPO: We propose SA-GRPO, a security-
aware group relative policy optimization algorithm that refines
1https://github.com/caoxinye/SecLoop


---

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021
3
security strategies through iterative feedback from parallel
BATTLE-FIELD. SA-GRPO eliminates the need for high-
quality labeled data, adapting to the real world. To further
tailor the optimization process to security-specific tasks, we
design a customized reward function from four complementary
perspectives, including format check, simulation execution,
attack evaluation, and reasoning verification.
❸Extensive Experiments: We conduct extensive experiments
on four public benchmarks to show the effectiveness of the
proposed SA-GRPO, yielding a state-of-the-art defense for the
next generation networks. We also build a more comprehensive
dataset on the SecLoop, and such a dataset can serve as a
benchmark for security orchestration. Furthermore, we con-
duct 21 types of cyberattacks, including advanced and zero-
day attacks, on real-world tests to demonstrate the practical
potential of SA-GRPO. Finally, we provide three case studies
of heterogeneous edge devices to visually demonstrate the
detailed work procedure of the proposed SA-GRPO.
E. Related Work
1) Security Orchestration: Security orchestration has been
widely applied in programmable network architectures such
as software-defined networking (SDN) [32], [33] and net-
work functions virtualization (NFV) [34], [35] to achieve
automated and scalable security management. The zero-touch
network and service management (ZSM) proposed by ETSI
is regarded as a new paradigm to achieve fully automated
network management [5]. In this framework, the security
orchestration center (SOC) is deeply integrated to support
real-time policy enforcement, intent analysis, and dynamic de-
ployment of cross-domain security services [5], [7], [36]. The
existing research also systematically explores the convergence
trends and security challenges of key technologies such as
SDN, NFV, Multi-Access Edge Computing (MEC), and O-
RAN in 5G and B5G [36], [37]. Although SOC provides a
complete automated management framework, current research
still mostly focuses on the automation of the deployment of
security functions [38]. To the best of our knowledge, we
are the first to build a fully automated end-to-end security
automation framework with native LLMs.
2) Security Strategy Optimization: Reinforcement learning
(RL) has been widely adopted for optimizing security strate-
gies. Q-learning [39] enables adaptive threshold tuning for
replay attack mitigation, and Double Q-learning [40] enhances
stability in edge-based intrusion detection via CyberRL.
DQN [41] was applied in the APT Rivalry Game framework
to optimize the timing of defense responses. PPO [42] further
supports attack path planning in dynamic Active Directory
graphs, while defenders optimize edge-blocking decisions
using value-based evaluations. Hierarchical approaches such
as HMARL employ Q-Tabular and PPO [43] across different
layers to enable multi-agent collaborative defense. SAC [44]
has been used in the RUDOLF framework to learn adaptive
traffic obfuscation strategies in Tor, and DDPG-MIX [45]
has been adopted in Double Oracle games to compute ro-
bust alert prioritization under adversarial conditions. Despite
recent progress, existing RL-based approaches often rely on
static datasets and struggle to generalize or adapt in com-
plex environments. To address this, we propose SA-GRPO,
a security-aware RL algorithm that iteratively refines policies
by contrasting feedback from parallel executions of real-world
testbeds, enabling more adaptive strategy generation.
F. Paper Organization and Notations
The remainder of the paper is organized as follows. Section
II presents the architecture of the proposed SecLoop. Section
III describes our proposed SA-GRPO algorithm. Section IV
shows the experimental settings and discusses results com-
pared with different baselines. Section V gives some insightful
discussions. Finally, conclusions are drawn in Section VI.
II. OUR PROPOSED SECLOOP SYSTEM
SecLoop is an advanced and automated security framework
designed to address the dynamic and evolving security chal-
lenges in 6G ZTNs. As illustrated in Figure 3, the system
consists of three key modules: the parallel BATTLE-FIELD,
the SOC, and LLM-guided strategy optimization. These com-
ponents work together to provide a fully integrated, end-
to-end solution for security strategy generation, execution,
response, and continuous feedback. Figure 2 and Section
II-A describe the mapping relationship between the proposed
SecLoop and the ZSM architecture. The details of the SOC
and the overall system workflow are introduced in Section
II-B, while the specifics of the parallel BATTLE-FIELD are
discussed in Section II-C. The SA-GRPO algorithm, which
drives the LLM-guided strategy optimization, is explained
in detail in Section III. Additionally, Section II-D provides
the construction process and details related to the training
dataset. Through the interaction of these modules, SecLoop
enhances its response to evolving threats while minimizing
manual intervention.
A. Correspondence with the ETSI ZSM Framework
As illustrated in Figure 2, we establish a correspondence
between the SecLoop framework and the ETSI ZSM [46]
framework. The right side of the figure depicts the ZSM frame-
work, which is composed of managed infrastructure resources,
management domain, dataset services, management functions,
domain integration fabric, and cross-domain integration fabric.
The core components of our SecLoop framework correspond
to different logical functions within the ZSM’s management
functions, forming the loop illustrated in the left half of
the figure. These components are: parallel BATTLE-FIELD,
policy execution validator, LLM-based agent, and security
orchestration center, which correspond respectively to the
ZSM framework’s domain data collection, domain analytics,
domain intelligence, and domain orchestration. These compo-
nents collaborate to form a complete observe, orient, decide,
act (OODA) automation loop where the parallel BATTLE-
FIELD collects data, the validator analyzes the situation, the
agent generates policies, and the orchestration center executes
them. This design clearly demonstrates a dynamic and adaptive
zero-touch management process, validating the architectural
feasibility and practical integration capability of the scheme.


---

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021
4
Management Functions
Domain Integration Fabric
Cross-Domain Integration Fabric
Dataset
Services
Parallel 
BATTLE-FIELD
Security Orchestration 
Center
LLM-Based 
Agent
Policy Execution 
Validator
Observe
Orient
Decide
Act
Knowledge
Parallel 
BATTLE-FIELD
Policy Execution 
Validator
LLM-Based Agent
Security 
Orchestration Center
AutoAttack
Dataset
Control
Managed Resource
Feedback
Data
Security Strategy
Response
Data
Data
Data
Data
Domain Managed Infrastructure Resources
...
IP Tables
Suricata
Powershell
Management Domain
Fig. 2. Illustration of our framework mapped to ETSI ZSM. Data from the Parallel BATTLE-FIELD is fed into the policy execution validator. The analysis
results from the validator are then delivered to the LLM-Based Agent, which generates strategic strategies. These strategies are executed by the SOC, and the
final results are continuously monitored and recollected by the Parallel BATTLE-FIELD for subsequent cycles, constituting a closed-loop framework.
B. System Framework
As illustrated in Figure 3, the SecLoop framework begins
by collecting attack alerts from the environments. These alerts
are then processed and summarized into structured language
descriptions, which serve as prompts for the LLM-based agent.
Based on the input attack descriptions and the list of tools
available in the current environments, the LLM agent generates
a group of security strategies. Each strategy includes the tools
to be invoked and their specific parameters in response to
ongoing attacks. These strategies are fed into the red/blue
team controller of the SOC, which automates the generation
and parallel execution of BATTLE-FIELD. Each environment
corresponds to a specific security strategy. Once the strategy
is executed, the corresponding response from the environment
is sent back to the policy execution validator in the SOC to
generate feedback. The reward, based on strategies, feedback,
and attack alerts, is used for model gradient updates. The
LLM agent then refines the strategies iteratively to yield more
optimal responses. We present the mathematical modeling of
the entire SecLoop process below.
1) Data Collection and Log Preprocessing: First, for a
set of attacks in the current environment, the n attack alerts
collected by the IDS are represented as a set
L = {L1, . . . , Li, . . . , Ln},
(1)
where each Li denotes an individual attack alert. Each Li ∈L
is associated with specific attributes such as timestamp, attack
type, and severity, forming a multi-dimensional feature space
that can be used for further processing and analysis. These
raw logs are typically noisy, repetitive, and heterogeneous
in format. The summarizer module Sr then extracts key
event information, compresses redundant data, and outputs
standardized m attack summaries, denoted as
C = Sr(L) = {C1, . . . , Ci, . . . , Cm},
(2)
where each Ci represents a structured alert summary.
2) Security Strategy Generation: The summarized threat
information S, along with the current list of available tools
TA = {T1, T2, . . . , Tk}
(3)
and the environment description E, are then formatted as
prompt templates and input into the LLM based on Qwen2.5-
7B-Instruct with fine-tuning. The concatenated input prompt
is represented as
P = [C, TA, E].
(4)
The LLM processes the input prompt P through a function
LLM, which generates a group of security strategies
S = LLM(P) = {S1, S2, . . . , Sg}.
(5)
Here, each strategy Si is a vector that includes the tool call
list T i
C to be invoked along with the associated parameters for
mitigating the detected attacks.
T i
C = {t1, t2, . . . , tl},
T i
C ⊆Si,
(6)
where tj represents each tool involved in the strategy Si and
l is the number of tools in the tool call list T i
C.
3) Simulation Verification and Multi-Dimensional Eval-
uation: The generated security strategies Si are fed into the
SOC via API interfaces for processing by the blue team con-
troller (BTC) and red team controller (RTC). These controllers
automate the generation of a set of parallel BATTLE-FIELD
environments using infrastructure-as-code (IaC) templates de-
fined by Vagrant, each consisting of virtual machines (VMs)
representing the red and blue teams. Specifically, the red team
environment is implemented using a red team virtual machine


---

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021
5
Reward
Format 
LLM-Guided Strategy Optimization
AutoAttack
Dataset
You are a cybersecurity expert ...Tool list:{tool_list},  
Alert summary:{alert_summary}
Prompt
Red Team
Controller
Blue Team
Controller
Policy Execution Validator
Security Strategies Execution Result
Attack Execution Evaluation
Service Availability Status
Security Orchestration Center
...
Tool Call List
MITRE  ATT&CK; Attack Chain
Reconn-
aissance
Red VM
Blue VM
Windows 
Firewall
ENV 1
Blue VM
Red VM
ENV 2
Blue VM
Red VM
ENV n
Blue VM
Red VM
Parallel BATTLE-FIELD
LLM-Based 
Agent
Tool Call List
Feedback
Response
Windows 
Firewall
IP Tables
Powershell
Suricata
Security Strategies
Gradient 
Update
Framework of Our Proposed SecLoop
1
...
2
3
4
5
6
Control
Execution 
Evaluation
Penalty
IP Tables
Sysctl
Powershell
Suricata
...
Initial 
Access
Execution
Persiste-
nce
...
Credential   
Access
Fig. 3. Illustration of our proposed SecLoop. The system inputs are attack alerts from the AutoAttack dataset, which is fed into the LLM-based agent. LLM
agent generates a group of strategies, which are then input into the SOC for execution. The red team controller and blue team controller automatically generate
parallel BATTLE-FIELD environments to carry out the corresponding tool invocations. The response of BATTLE-FIELD is processed by the policy execution
validator to generate feedback values, which are passed to the SA-GRPO reward function. SA-GRPO iteratively optimizes and updates the model parameters.
(RVM), while the blue team environment is represented by a
blue team virtual machine (BVM).
Ek = (ERVM, EBVM)
(7)
represents the k-th parallel execution environment, where
ERVM and EBVM denote the red and blue team virtual ma-
chines, respectively. The BATTLE-FIELD environment is de-
fined as:
EBVM = BTC(Sk),
for each
Sk ∈S,
(8)
ERVM = RTC(Sk),
for each
Sk ∈S,
(9)
where Sk is the security strategy assigned to the environment
EBVM, and the execution is governed by the orchestrated
interaction between the RVM and BVM.
After the execution of each strategy Si, the corresponding
response RSi = {rsexe(Si), rsattack(Si), rsservice(Si)} from the
environment is sent back to the policy execution validator in
the SOC. This response consists of three key components: 1)
security strategies execution result rsexe(Si), 2) attack execu-
tion evaluation rsattack(Si), and 3) service availability status
rsservice(Si). These components provide essential feedback for
assessing the effectiveness of the executed strategies.
As for the security strategy execution result, the success
of each tool is represented as fexe(tj) ∈{0, 1}, where the
number 1 indicates successful execution and the number 0
indicates failure. The overall execution result rsexe(Si) is the
average success rate of all tools in T i
C:
rsexe(Si) = 1
l
l
X
j=1
fexe(tj),
tj ∈T i
C.
(10)
To evaluate the success of the attack execution, we divide
the attack process into multiple stages, each corresponding to
a specific step in the attack chain. These stages are derived
from the dataset. Pi = {p1, p2, . . . , pm} represents the set of
stages for the attack process associated with strategy Si, and
pj ∈Pi represents the j-th stage of the attack. The success of
each attack stage is represented as fexe(pj) ∈{0, 1}, where
the number 1 indicates successful execution and the number
0 indicates failure. The overall execution result rsattack(Si) is
the average success rate of all attack stages in Pi:
rsattack(Si) = 1
m
m
X
j=1
fexe(pj),
pj ∈Pi.
(11)
The service availability status evaluates the impact of exe-
cuting the strategy Si on the availability of network services,
taking into account the effects in both the blue team and red
team environments. After executing the strategy, the service
availability status is represented as rsservice(Si) ∈{0, 1},
where the number 1 indicates that the service is available and
unaffected by the attack, and the number 0 indicates that the
service is disrupted or unavailable due to the attack.
rsservice(Si) = fservice(EBVM, ERVM, Si).
(12)
Here, fservice is a function that assesses the availability of
services in the blue and red team environments after the
execution of strategy Si. The feedback is then represented as:
Fi = rsexe(Si) + rsattack(Si) + rsservice(Si).
(13)
4) Feedback Optimization and Model Update: The cus-
tomized reward function in the SA-GRPO algorithm consists
of four key components: format check, simulation execution,


---

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021
6
attack evaluation, and reasoning verification. The format check
evaluates the format correctness of the security strategies S,
while simulation execution and attack evaluation reflect the de-
gree to which the attack and defense strategies are executed in
the environments, based on feedback F. Reasoning verification
assesses how well the strategy aligns with the attack descrip-
tion L, ensuring that the generated strategy matches the attack
scenario. These components collectively determine the overall
reward Reward(Si, Fi, L), which guides the optimization of
strategies. The output of SA-GRPO is the gradient update ∆θ
for model parameter adjustment. Particularly, our proposed
SA-GRPO algorithm, which integrates strategies comparison
and a multi-dimensional reward function mechanism, enables
the model to maintain high-quality responses while avoiding
over-defense. This process can be triggered periodically or on
demand, enabling the dynamic evolution of LLMs.
C. Parallel BATTLE-FIELD
Our BATTLE-FIELD is the core evaluation engine within
the SecLoop framework, designed to construct a highly realis-
tic, automated, and reusable cyber attack-defense simulation
environment. The primary objective of this module is to
provide a closed-loop validation platform for the security
strategies under conditions closely resembling real-world cy-
berattacks. BATTLE-FIELD employs a red-blue confrontation
mechanism, incorporating three key roles: attack simulation
(Red Team), defence strategy (Blue Team), and evaluation. It
simulates attack behaviors while executing defensive actions
and quantitatively evaluates the effectiveness of the strategies.
To enable rapid deployment and environment reproducibil-
ity, BATTLE-FIELD leverages Vagrant to implement an
Infrastructure-as-Code management mechanism. Vagrant al-
lows users to define virtual network topologies through declar-
ative configuration files, including host operating system types,
IP address allocations, service configurations, and software
installation scripts. With this capability, BATTLE-FIELD can
automatically clone a complete experimental environment be-
fore each evaluation task begins, ensuring that comparisons
between different strategies are conducted under identical or
similar conditions. All virtual machine instances run on the
VMware platform, utilizing its efficient resource scheduling
and network isolation mechanisms to guarantee the indepen-
dence and security of each experimental unit.
1) Attack Simulation: In terms of attack simulation,
BATTLE-FIELD utilizes a custom-developed, lightweight
platform as the red team’s automated attack engine. This
engine is built upon the MITRE ATT&CK framework and is
capable of automatically generating multi-stage attack chains
based on predefined tactics and techniques. By loading dif-
ferent plugins and parameterized action profiles, the system
can simulate typical attack behaviors such as initial access,
privilege escalation, persistence, lateral movement, and data
exfiltration. Moreover, our engine supports the development
of dynamic and randomized attack modules. This allows
researchers to design specific attack paths tailored to real-
world scenarios, thereby enhancing the diversity and realism
of the simulations and mitigating the risk of overfitting to a
static attack configuration.
2) Defense Strategy: During a complete evaluation cycle,
after the LLM-Guided Strategy Optimization submits the gen-
erated security policies to the SOC, the blue team controller
first applies the corresponding mitigation measures on the
blue team hosts located on BATTLE-FIELD based on the
policy content, such as closing ports, updating firewall rules,
and isolating suspicious hosts. Subsequently, the red team
controller launches the predefined attack sequence using the
automated attack engine and records key events during the
attack process, such as successful compromise points and
blocked attack locations. Meanwhile, the blue team controller
monitors the system availability of the blue team hosts to
comprehensively assess both the defensive effectiveness and
side effects of the strategy.
3) Evaluation: After completion, the policy execution
validator will collect all the report information, including
the blue team’s security strategies execution result, the red
team’s attack execution evaluation, and the blue team’s service
availability status, and then parse this report information to
calculate the corresponding values and feed them back to the
reward, which serves as the signal source for the execution
reward and evaluation reward of the SA-GRPO algorithm,
promoting the continuous improvement of the strategy model.
D. Dataset Construction
We construct the AutoAttack dataset, which combines attack
alerts with required automated environment configurations.
This dataset is primarily designed for automating the replay
of attack processes for BATTLE-FIELD, rather than for su-
pervised model training with labeled data. The proposed Au-
toAttack integrates alert logs and real traffic, encompassing the
automated replay of over 20 attack scenarios of 11 ATT&CK
processes, such as zero-day exploits. Our AutoAttack provides
the necessary attack information inputs for LLMs.
1) Environment configuration for batch red-blue virtual
machine pairing implemented by Vagrant: The Vagrant tool
is employed to create and configure the red and blue team
virtual machines, allowing reproducible deployment of attack
environments. All Vagrant-managed environments are defined
and deployed through code, aligning with an Infrastructure-
as-Code paradigm using provisioning scripts. This design
encapsulates virtual machine configuration, network topol-
ogy construction, and attack chain initialization into version-
controllable artifacts such as shell and Python scripts. By
avoiding manual configurations through GUI tools, this code-
centric approach mitigates the risk of environment drift and
enables reproducible and parameterized scenario generation.
2) Attack modules and MITRE ATT&CK tactical map-
ping: The MITRE ATT&CK framework offers a structured
taxonomy of adversarial tactics and techniques derived from
real-world observations, serving as a standardized reference
for describing attacker behaviors and organizing threat intelli-
gence. Our approach integrates automated simulation of real-
world cybersecurity incidents with synthetic network security
event generation to map attack modules to MITRE ATT&CK
tactics. Automated simulations replicate complex attack be-
haviors, including nmap scanning, password cracking via


---

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021
7
TABLE I
ATTACK STAGES AND MITRE ATT&CK TACTICAL MAPPING
MITRE ATT&CK
Tactical Stages
Attack Means
Reconnaissance
Port scanning through fscan/nmap
Initial Access
Redis unauthorized vulnerability written
to webshell Trojan, CVE-2025-29927
Execution
File upload and write to webshell Trojan,
Deserialization attack,
CVE-2024-23897, CVE-2025-24813
Persistence
Preliminary webshell Trojan Writing
Complete Logic for webshell Control Trojan,
CVE-2024-2961
Credential Access
XSS (Cross Site Script),
Cross Site Request Forgery, etc.
Discovery
SQL injection, LFI/RFI, SSRF,
CVE-2024-23897, CVE-2025-30208
Lateral Movement
Blasting Windows account passwords
by CrackMapExec through SMB protocol
Collection
C2 Trojan collects information from
Blue Team’s target drone
Command and Control
C2 Trojan was activated and went live
on the blue team’s target machine
Exfiltration
Transmitting sensitive information of
the target drone through C2
Impact
Man in the middle attacks in the form of
DNS hijacking, DoS/DDoS Attacks
SMB protocols. Synthetic traffic generation models browser-
based XSS attacks and non-standard command-and-control
(C2) patterns. This dual methodology ensures comprehensive
alignment between attack modules and MITRE ATT&CK
tactics, as detailed in Table I.
To address zero-day threats lacking public exploits, we
developed a specialized synthetic event synthesis module. By
analyzing technical disclosures and historical CVE data (e.g.,
CVE-2024-2961, CVE-2024-23897), we reconstruct high-
impact vulnerability exploitation scenarios. Synthetic alerts
emulate behavioral signatures of middleware services common
to industrial and communication networks while evading rule-
based detection. This enables evaluation of the SOAR strategy
generalization against emerging, unseen threats.
3) Automated Attack Orchestration: We have developed
a custom, lightweight automated attack engine for adversary
emulation, built upon the MITRE ATT&CK framework. Gov-
erned by the red team controller, this engine automatically
orchestrates multi-stage attack chains by loading various plu-
gins and parameterized action profiles. It simulates a wide
range of APT behaviors and executes them in the red-team
VM to conduct realistic, threat-based stress tests on the blue-
team VM. A key feature is its support for dynamic and ran-
domized attack modules, which enhances simulation realism
and mitigates the risk of overfitting to static configurations.
This system effectively bridges theoretical ATT&CK structures
with scalable and dynamic adversary emulation, overcoming
the limitations of traditional human-computer interaction.
To reflect the operational characteristics of communication
network environments, we apply a filtering mechanism to
exclude techniques with limited relevance to network traffic
analysis, such as Resource Development and Privilege Esca-
lation, and instead focus on failure-prone defense scenarios
frequently encountered in the communication field.
III. SA-GRPO ALGORITHM DESIGN
A. Workflow of SA-GRPO
Traditional supervised fine-tuning (SFT) methods rely heav-
ily on a high-quality labeled dataset and bring significant GPU
memory consumption. In contrast, the GRPO algorithm lever-
ages the comparative results of a group of outputs, enabling
more efficient learning from diverse scenarios without requir-
ing extensive labeled datasets. Based on GRPO, we propose
SA-GRPO, a security-aware group relative policy optimiza-
tion algorithm tailored specifically for security automation
of SecLoop. As shown in Figure 4, SA-GRPO updates the
policy model by maximizing the SA-GRPO objective, which
is computed using an estimator of the advantage based on
the relative rewards of outputs within each group. Detailed
procedures for our proposed SA-GRPO are outlined below.
Algorithm 1 Our Proposed SA-GRPO
Input: initial Policy Model πθ, Reward Model R, Task
Prompts D, Hyperparameters ϵlow, ϵhigh
for step = 1, ..., M do
Db ∼D
πθold ←πθ
for each question q ∈Db do
{oi}G
i=1 ∼πθold(·|q)
end for
for each oi do
{ri}G
i=1 ←{R(q, oi)}G
i=1
ˆAi,t ←ri −mean({ri}G
i=1)
end for
for SA-GRPO iteration = 1, . . . , µ do
πθ ←arg max
θ
JSA−GRPO(θ)
end for
end for
Output: πθ
SA-GRPO introduces a policy model πθ, a reward model,
a group of task prompts D and hyperparameters such as
ϵlow, ϵhigh. For each subsequent step, SA-GPRO samples a
batch Db from D and updates the former policy model. Then
it samples a group of outputs {oi}G
i=1 for each question q
when using old policy πθold and optimizes the policy via the
following objective:
JSA−GRPO(θ) = E(q,a)∼D, {oi}G
i=1∼πθold(·|q)
"
1
G
G
X
i=1
|oi|
X
t=1
min

γi,t(θ) ˆAi,t, clipi,t(θ) ˆAi,t
#
,
(14)
where (q, a) is a question-answer pair from the data distribu-
tion D, and {oi}G
i=1 are G outputs sampling for each question-
answer pair (q, a); clipi,t(θ) is a clip operation for importance
sampling ratio γi,t(θ), where
clipi,t(θ) = clip
 γi,t(θ), 1 −εlow, 1 + εhigh

,
(15)
where εlow and εhigh are respectively hyperparameters within
the lower and upper bound of the clipping range of the


---

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021
8
Policy
Model
Group
Computaion
Evaluation
: Original GRPO
  : Our SA-GRPO 
Reward
Penalty
BATTLE-FIELD
Format
Execution
Fig. 4. Illustration of our proposed SA-GRPO algorithm. A group of outputs is sampled from the policy model, each assigned a reward computed with four
customized reward functions. The group relative advantage is estimated for each output, and the policy model is updated by maximizing the objective function.
importance sampling ratio γi,t(θ) for the i-th output at the
t-th token, where
γi,t(θ) =
πθ(oi,t | q, oi,<t)
πθold(oi,t | q, oi,<t),
(16)
where πθ(oi,t | q, oi,<t) is the probability of i-th object at
t-th token under the conditions of question q and object oi
when using updated policy πθ while πθold(oi,t | q, oi,<t) is
the probability when using old policy πθold; SA-GRPO then
computes ˆAi,t which is an estimator of the advantage at time
step t for each output oi, where
ˆAi,t = R(q, oi) −mean({R(q, oi)}G
i=1).
(17)
Given the reward function R, ˆAi,t is calculated based on the
relative rewards of the outputs inside each group.
B. Reward Modules Design
1) Format Reward: The format reward evaluates the struc-
tural correctness of the outputs generated by the LLM, specif-
ically assessing whether they adhere to the expected format
(JSON). The score is assigned on a scale from 0 to 1,
with a score of 1 indicating complete conformity to the
predefined structure. Only outputs that achieve the full score
of 1 are eligible to proceed to the subsequent reward module.
Otherwise, the response advances to the final penalty stage.
To automate format verification and ensure consistency, we
employ regular expressions as the validation mechanism. The
format reward function Rformat takes outputs oi of LLM as
inputs which is defined as:
Rformat(oi) =
(
1,
if re(oi) = true
0,
if re(oi) = false ,
(18)
where re(oi) is a function based on regular expressions that
validates the format of oi.
2) Execution Reward: The execution reward assesses the
ability of the LLM-generated instructions to execute correctly
within our BATTLE-FIELD. The reward is conducted on a
scale from 0 to 1, where a score of 1 is assigned only if
the instruction is executed without error. Instructions that fail
execution advance to the final penalty stage. To ensure robust
execution verification and maintain consistency, the reward
module is closely integrated with the BATTLE-FIELD. The
execution reward function can be defined as Rexec, which takes
outputs from LLM as inputs oi where
Rexec(oi) =
(
1,
if E(oi) = true
0,
if E(oi) = false ,
(19)
where E(oi) is a function that verifies the executable instruc-
tions in oi.
3) Evaluation Reward: The Evaluation Reward measures
the effectiveness of LLM-generated instructions in defending
against and mitigating attacks within the BATTLE-FIELD.
This reward is quantified on a scale from 0 to 1, where a
score of 1 indicates the absence of warning alarms following
the execution of the provided instructions. Lower scores are
assigned based on the degree to which the instructions suc-
cessfully enhance the environment’s defensive and mitigation
capabilities. Subsequently, the instructions proceed to the final
penalty assessment stage. To ensure rigorous validation of
execution outcomes, the reward module is tightly integrated
with the BATTLE-FIELD platform. The evaluation reward
function can be defined as Reva, which takes outputs from
LLM as inputs oi where
Reva(oi) = WBATTLE−FIELD(oi) ∈[0, 1],
(20)
where WBATTLE−FIELD(oi) is a function based on BATTLE-
FIELD that evaluates the defensive and mitigation capabilities
of instructions in oi.
4) Penalty: To prevent the excessive processing of instruc-
tions generated by the LLM, we introduce a penalty module
designed to mitigate potential biases and enhance the overall
robustness of our system. An automated LLM-based expert is
employed to evaluate the generated instructions, ensuring their
validity and appropriateness. This approach effectively avoids
extreme or overly harsh operations, thereby maintaining bal-
anced and reliable system performance. The penalty function
can be defined as P(oi) which takes outputs from LLM as
inputs oi where
P(oi) = 1 −WLLM(oi), WLLM(oi) ∈[0, 1],
(21)
where WLLM(oi) is a function based on an LLM-based expert
that evaluates the rationality of instructions in oi.


---

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021
9
IV. EXPERIMENTS
A. Experimental Setup
1) Configuration of LLM Training: The experimental
setup of the SecLoop framework is designed to support dis-
tributed training, high-fidelity simulation, and efficient policy
validation. The training node is deployed on a CentOS Stream
8 server equipped with 8 NVIDIA A800 GPUs, 256GB
DDR4 memory, and 10TB NVMe SSD storage. This node
runs PyTorch 2.3 and HuggingFace Transformers, with model
architecture based on Qwen2.5-7B-Instruct. Multi-GPU com-
munication is accelerated via NCCL libraries, while Slurm
manages job scheduling.
2) Configuration of LLM Evaluation: The evaluation node
operates on an Ubuntu 22.04 server with 1 NVIDIA A100
GPU (80GB HBM2e), 64GB DDR4 memory, and 1TB NVMe
SSD. This node executes security policies generated by the
training node, hosts a lightweight communication middleware.
3) Configuration of BATTLE-FIELD: The BATTLE-
FIELD simulation environment is hosted on a Windows 11 Pro
machine (Intel Core i7-14700F, 64GB DDR4 memory) inte-
grated with Vagrant 2.4.3 and VMware Workstation Pro 17.5.
This setup enables dynamic cloning of red-team and blue-team
virtual machines through Infrastructure-as-Code templates.
4) Configuration of Policy Execution Validator: The red
team controller and the blue team controller are deployed on
separate Ubuntu 22.04 servers, each of which has 16GB of
memory and a 512GB NVMe SSD. The red team controller
coordinates our self-developed attack agent to execute the
specified attack strategy. The blue team controller performs
defensive actions. Their execution results will be fed back to
the policy execution validator. The policy execution validator
resides in a WSL2 subsystem on the Windows 11 host, running
Ubuntu 22.04 with 64GB of memory.
5) Configuration of Real-World Test: For real-world de-
ployment testing, we evaluated SecLoop on a set of embedded
edge devices, including four Jetson AGX Orin 64GB and four
Jetson ORIN NX 16GB. Each Jetson AGX Orin 64GB features
a 2048-core NVIDIA Ampere GPU with 64 Tensor Cores
and a 12-core Arm Cortex-A78AE CPU, while the Jetson
ORIN NX features a 1024-core GPU and a 6-core CPU. In
addition, we included a Windows 11 laptop with 16GB RAM
and an Ubuntu 22.04 desktop machine with 64GB RAM in
our evaluation, further demonstrating the framework’s cross-
platform compatibility and adaptability across heterogeneous
hardware environments.
B. Datasets
The attack datasets CIC-IDS2017 [47], CIC-IDS2018 [48],
UNSW-NB15 [49], and CCDC-2018 [50], which are widely
used in the current field of network security, are respectively
collected for network attack data in different scenarios. CIC-
IDS2017 and CIC-IDS2018 mainly collect attack traffic in the
conventional network environment, including various attack
types such as DDoS, DoS, penetration attacks, brute-force
cracking, and Web attacks; UNSW-NB15 covers nine types
of modern cyber attacks, such as missed strike attacks, worm
spread, and Shellcode injection. CCDC-2018 is based on a
real offensive and defensive exercise environment and records
multi-stage compound attacks such as phishing attacks, mal-
ware spread, and lateral penetration.
We also construct corresponding attack environments in
BATTLE-FIELD based on the datasets, enabling faithful re-
play of attacks and accurate evaluation of generated outputs.
In comparison with baseline reinforcement learning algo-
rithms such as PPO and KTO, we incorporate Reinforcement
Learning from Human Feedback (RLHF). In this approach,
domain experts are engaged to annotate the training dataset
with human preferences, which are subsequently leveraged to
generate human-guided rewards during the training phase.
C. Baselines
We compare the function of our proposed SecLoop with
various baselines, including TENNISON [51], JESS [52],
Virtual IoT HoneyNets [53], OntoCSD [22], APIRO [27], AG-
AEGM [25], SSAE-SVM [54], IoT-DPS [55], RAG-IR [56],
IRCopilot [57], and ReAct-LLM [58]. TENNISON employs
adaptive distributed strategies against DoS/DDoS/scanning via
multi-level detection and orchestration. JESS uses three-stage
mitigation (Nominal-Preparatory-Active) with joint entropy
analysis for DNS/NTP attacks. Virtual IoT HoneyNets deploy
policy-driven honeypots with real-time monitoring for IoT
botnets/zero-days. OntoCSD combines CBR reasoning with
OWL/SWRL threat modeling for credential attacks/phishing.
APIRO integrates NLP-based API recommendations with het-
erogeneous toolsets for data breach mitigation. AG-AEGM
evaluates defenses through attack graph analysis and evolu-
tionary game theory. SSAE-SVM employs entropy analysis
plus deep learning (SSAE/SVM) for hybrid attack detection.
IoT-DPS utilizes lightweight LLMs to enable real-time de-
tection and automatic response to abnormal traffic and attack
behaviors in IoT networks. RAG-IR dynamically integrates
LLMs with CTI to achieve automated, context-aware security
alert enhancement and response strategy generation. IRCopilot
applies LLMs to the automation of event response throughout
the entire lifecycle. React-LLM is an autonomous network
event response system based on the ReAct (Reasoning +
Acting) framework and LLMs. Our system uniquely automates
strategy validation through integrated response-feedback loops
in security orchestration.
We compare the performance of our proposed SecLoop
with state-of-the-art baselines, including xNIDS [59] and
SAGE [60]. xNIDS transfers the results of deep learning-based
intrusion detection systems to actionable responses. SAGE
utilizes an unsupervised S-PDFA model to compress intrusion
alerts into attack graphs for strategy generation. Different from
baselines, SecLoop can generate defense strategies that enable
automation tool execution in diverse environments.
The proposed SA-GRPO is compared with several re-
inforcement learning approaches, including GRPO [61],
KTO [62], DQN [63], DDQN [64], and PPO [65]. PPO uses a
clipped surrogate objective to constrain policy updates within
a proximal region of the previous policy. KTO maximizes
the utility of generations instead of maximizing the log-
likelihood of preferences. DQN learns off-policy Q-values


---

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021
10
TABLE II
COMPARISONS OF SECURITY AUTOMATION SYSTEMS
Scheme
Strategy
Generation
Automated Security
Orchestration
Response
Feedback
ATT&CK Stages
TENNISON [51]
✓
✓
✓
✓
2, 3, 4, and 6
JESS [52]
✓
×
✓
×
1, 2, and 13
Virtual IoT HoneyNets [53]
✓
✓
✓
×
1, 2, 3, 4, 5, 6, and 13
OntoCSD [22]
✓
✓
✓
×
1, 2, 4, 5, 6, 9, and 13
APIRO [27]
✓
×
✓
×
1, 2, 3, 4, 5, 9, and 13
AG-AEGM [25]
✓
✓
✓
×
1, 2, 3, 4, 5, 6, 7, 9, 10, and 13
SSAE-SVM [54]
✓
×
×
×
13
IoT-DPS [55]
✓
✓
✓
×
1, 7, 8, 11, and 13
RAG-IR [56]
✓
✓
✓
×
2, 3, 5, 6, 7, 8, 9, 10, 11, and 12
IRCopilot [57]
✓
✓
✓
✓
3, 4, 5, and 6
ReAct-LLM [58]
✓
✓
✓
×
1, 2, 7, and 8
SecLoop(Ours)
✓
✓
✓
✓
1, 2, 3, 4, 7, 8, 9, 10, 11, 12, and 13
The numbers 1-13 correspond to the ATT&CK tactical stages: Reconnaissance, Initial Access, Execution, Persistence, Privilege Escalation, Defense Evasion,
Credential Access, Discovery, Lateral Movement, Collection, Command and Control, Exfiltration, and Impact.
(a)
(b)
(c)
(d)
(e)
(f)
Fig. 5.
Performance comparisons and ablation studies of our proposed SecLoop and SA-GRPO. (a), (b), and (c) compare the accuracy of SecLoop and
SA-GRPO against multiple baselines on five benchmarks. (d), (e), and (f) evaluate the accuracy of SecLoop and SA-GRPO in the real-world testbed.
with replay and a target network for discrete actions, but tends
to overestimate. DDQN decouples selection and evaluation
to reduce bias and stabilize training. Unlike PPO and KTO,
GRPO adopts a group-relative advantage estimation approach.
Specifically, our proposed SA-GRPO algorithm is a redesign
of GRPO tailored for SecLoop, which eliminates the division
by the standard deviation, excludes the KL divergence term,
and adopts the Clip-Higher [66] strategy.
D. Metrics
To evaluate the accuracy of different methods, we trans-
form the generated responses into executable strategies for
BATTLE-FIELD and execute them within our simulation
environment. A strategy is considered correct if it can be
successfully executed in the blue team environment, effectively
defends against the red team’s attacks, and does not cause any
disruption to the blue team’s system. The accuracy is then
calculated as the ratio of correct responses to the total number.
E. Performance
This section presents extensive experiments to evaluate
the effectiveness of the proposed SecLoop and SA-GRPO
methods, along with key observations and conclusions.
❶Comparisons of Our Proposed SecLoop System:
As shown in Table II, we compare our proposed SecLoop
in multiple dimensions, including security strategy genera-
tion, automated security orchestration, response, feedback,
and ATT&CK process completeness. It is evident that the
SecLoop system achieves an end-to-end security automation
loop. While existing systems demonstrate certain capabilities
in strategy generation, many lack a fully integrated automated
security orchestration process. Several systems do not support
closed-loop feedback, limiting their capacity for iterative im-
provement and adaptation to new threats. In particular, we
introduce a qualitative classification and statistical analysis
method based on the MITRE ATT&CK framework, which
expands attack detection from a single dimension to tactical-


---

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021
11
(a)
(b)
(c)
Fig. 6. Performance comparisons and ablation study of the proposed SecLoop
and SA-GRPO. (a) compare the proposed SecLoop with state-of-the-art
LLMs, (b) is the ablation study of reward functions of our SA-GRPO, and
(c) demonstrates the impact of group size during training of our SA-GRPO.
level association analysis. Furthermore, our SecLoop system
achieves the highest level of ATT&CK process completeness.
We also compare the advancement of our system, SecLoop,
in terms of functional coverage, decision-making intelligence,
and adaptation capability. In terms of functional coverage,
most existing systems focus on specific stages of the security
process, such as threat detection, policy generation, or policy
optimization, whereas SecLoop achieves a complete closed
loop from threat perception to policy self-optimization. Re-
garding decision-making intelligence, most existing security
systems rely on manual configuration and rule-driven methods.
In contrast, SecLoop automatically generates relevant scripts
through the LLM to invoke security tools and employs SA-
GRPO to achieve self-optimization of security decisions. Any
manual intervention in these core modules would create a
significant bottleneck, degrading the system into a traditional,
slow-response security model. Compared with other systems,
SecLoop can not only generate safety strategies but also
invoke tools to execute strategies in different environments,
which demonstrates a higher level of intelligence. Finally, with
respect to adaptation capability, compared to existing systems,
SecLoop not only demonstrates stronger generalization across
heterogeneous devices and dynamic environments but also
adapts to various attack types, effectively reducing the cost
of manual operations.
We compare the performance of our proposed SecLoop
with two representative baselines on five benchmarks, as
shown in Figure 5(a). Experimental results show that Se-
cLoop consistently outperforms existing methods across all
test datasets, achieving average accuracy improvements of
41.6% over xNIDS and 50.0% over SAGE, respectively.
Figure 6(a) presents a comparison of the performance of
SecLoop with state-of-the-art LLMs, including Grok 3 Beta,
Gemini 2.5 Pro Preview, and GPT-4.1, across five benchmark
datasets. Notably, our SecLoop with 7B parameters consis-
tently outperforms these large-parameter LLMs, achieving
average accuracy improvements of 66.9% over Grok 3 Beta,
32.9% over Gemini 2.5 Pro Preview, and 1.2% over GPT-4.1.
❷Comparisons of Our Proposed SA-GRPO Algorithm:
To validate the effectiveness of our proposed SA-GRPO,
we compare SA-GRPO with reinforcement learning algo-
rithms, including DQN, DDQN, PPO, KTO, and GRPO, on
five benchmarks. As illustrated in Figure 5(b), SA-GRPO
significantly outperforms other algorithms, showing average
accuracy gains of 26.7% over DQN, 22.7% over DDQN,
18.6% over PPO, 14.7% over KTO, and 10.3% over GRPO,
respectively. Furthermore, we conduct an ablation study of SA-
GRPO, as shown in Figure 5(c). The results reveal substantial
improvements in accuracy across all tasks after fine-tuning,
with an average increase of 30.4%. This demonstrates SA-
GRPO’s superior performance and stronger generalization
capability against diverse attack scenarios.
Figure 6(b) presents an ablation study that investigates the
impact of different rewards on the overall performance of SA-
GRPO. We observe varying degrees of performance degrada-
tion when any of the rewards is removed. Specifically, the
execution and evaluation rewards lead to the most significant
impact on SA-GRPO, with an average decrease of 26.9%
compared to the original SA-GRPO. This indicates that the
feedback from environments plays a critical role in guiding
the model toward strategy generation. Disabling the penalty
reward also results in a notable decline of 10.0%, preventing
destructive outputs and ensuring the security of our automated
system. In contrast, the absence of the format reward causes
the smallest performance drop at 3.1%, because it mainly
focuses on accelerating the training process of the model.
Figure 6(c) presents a sensitivity analysis on the impact
of the group size, a key hyperparameter in our SA-GRPO
algorithm. The results demonstrate a clear positive trend: as
the group size increases, the model’s average accuracy across
all datasets steadily improves. This improvement is attributed
to the core mechanism of group relative policy optimization; a
larger group provides a wider and more diverse sample of can-
didate policies for each prompt, which allows for a more robust
and lower-variance estimation of the advantage signal used for
the policy update. However, this performance gain comes at
the cost of increased computational overhead, as the number
of generations and subsequent reward calculations scales with
the group size. Considering this trade-off between performance
and computational efficiency, we selected a group size of 7 for
our primary experiments, as it delivered substantial accuracy
gains while maintaining a manageable training cost.


---

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021
12
TABLE III
PERFORMANCE COMPARISON OF THE STRATEGY ON DIFFERENT
HARDWARE PLATFORMS
Platform
Tensor
Performance
VRAM
(MiB)
Time
cost (s)
Accuracy
(%)
Simulation
Environment
1248 TOPS
15410
0.74
92.71
Edge
Devices
275 TOPS
17868
48.19
91.35
❸Real-World Experiments: To evaluate the deployment
capability of SecLoop in resource-constrained environments,
we conduct real-world tests on an NVIDIA Jetson edge device.
The corresponding results are presented in Figures 5(d)(e)(f).
In Figure 5(d), we deploy the model trained via SecLoop to
the Jetson device and also implement the two representative
baseline methods for comparative purposes. In the real-world
test of SecLoop, we found that SecLoop still outperforms
the other methods in terms of response accuracy under edge
computing conditions, with average accuracy improvements
of 41.6% over xNIDS and 50.8% over SAGE. This indicates
that in the real-world environment, the performance of our
SecLoop is similar to that of the simulation environment.
Figure 5(e) shows the performance of different reinforce-
ment learning algorithms on the edge device, including PPO,
KTO, GRPO, and our proposed SA-GRPO. The results reaf-
firm that SA-GRPO continues to outperform other algorithms
even in resource-constrained environments, achieving average
accuracy gains of 18.4% over PPO, 16.4% over KTO, and
11.2% over GRPO. Moreover, the ablation study of SA-
GRPO in the real-world situation demonstrates minor distinc-
tion from simulation environments, as shown in Figure 5(f).
These findings further prove SA-GRPO’s adaptability and high
performance under resource-constrained conditions.
Table III presents a performance comparison of our pro-
posed method on two different hardware platforms: a high-
performance simulation environment and resource-constrained
edge devices. The simulation environment, with a tensor
performance of 1248 TOPS, utilizes 15410 MiB of VRAM,
achieves the lowest time cost of 0.74 seconds, and an accuracy
of 92.71%. In contrast, the edge device, which operates under
more limited computational resources with a tensor perfor-
mance of 275 TOPS, has a measured peak memory usage of
17868 MiB, exhibits a higher time cost of 48.19 seconds, but
still maintains a high accuracy of 91.35%. Notably, the slightly
higher memory consumption on edge devices is because of
the unified memory system adopted by the edge platform and
differences in optimization levels. This demonstrates that while
the edge platform will increase time consumption, it maintains
a high level of accuracy, highlighting the adaptability and ro-
bustness of our method across diverse hardware environments.
F. Case Study
As illustrated in Figure 7, we visualize three case studies
to demonstrate the effectiveness of our proposed SecLoop and
SA-GRPO in three heterogeneous environments of real-world
testbeds. For each scenario, we set up an attacker and multiple
victim devices. The LLM-Based Agent collects the alerts sent
by the victim devices and generates corresponding security
strategies. These strategies guide the devices in activating
security tools to mitigate diverse attacks.
In the first case, we used four edge devices (Jetson ORIN
NX 16GB) as victim devices and a Jetson AGX Orin 64GB
as the attacker. The LLM-based agent, deployed on the Jet-
son AGX Orin 64GB, generates strategies and orchestrates
security. In this scenario, the attacker launches various attacks
on the victim devices, including SQL injection, DoS, XSS,
and SSRF. The collected alerts and prompts are fed into the
model to generate executable security strategies. For example,
on the victim devices, we deployed a web service with an
SQL injection vulnerability that accepts unsanitized user input.
Sensitive information is sent back to the attacker’s platform
through cross-protocol communication. When the model re-
ceives the “SQL Injection Attempt” alert, it outputs strategies
like blocking IP and restraining other ongoing processes,
effectively defending the system against the attack.
In the second case, we deployed three Jetson ORIN NX edge
devices as victims and a Jetson AGX Orin edge device as the
attacker. The LLM-based agent, running on a host machine,
handles strategy generation and security orchestration. The
attacker targets the three victim devices with attacks such as
Command&Control, Nmap Scanning, and Redis Unauthorized
Write. Attack validation occurs in three stages: 1) establishing
a reverse TCP connection with netcat to test file writeability,
2) executing “whoami” to verify privilege escalation, 3) using
“curl” to trigger the WebShell and verify attack chain integrity.
When the model detects the “Redis Unauthorized Access”
alert, it generates defense strategies such as blocking IP,
enhancing SSH service security, and restraining other ongoing
processes to mitigate the attack.
In the third case, we deployed two Jetson ORIN NX
devices and a laptop as victim devices, with a host acting
as the attacker. The LLM-based agent, deployed on a Jetson
AGX Orin, generates strategies and orchestrates security. The
attacker targets the victims with different attacks, including
CVE-2025-24813, SMB-Brute Force, and CVE-2024-2961.
The alerts and prompts are processed by the model to generate
executable security strategies. Attack verification occurs in
three stages: 1) monitoring Tomcat logs to confirm file path;
2) using the JMX protocol to validate malicious class loading;
3) using the ps command to detect injected commands. Upon
receiving the “Tomcat RCE Attempt - InvokerTransformer”
alert, the model outputs strategies like blocking IP, restraining
other ongoing processes, and hardening kernel configuration
to mitigate the attack.
V. DISCUSSIONS
So far, we have shown the superiority of our proposed
SecLoop and SA-GRPO over five benchmarks. In this section,
we take the next step to highlight some interesting observations
and future work, including the adaptivity, generalization, and
self-evolution of the proposed SecLoop and SA-GRPO.
A. Adaptivity of Our Proposed SA-GRPO to Various Attacks
For the ATT&CK process, we have implemented the auto-
mated generation and environment replay of over 20 different


---

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021
13
Prompt
Alerts
Model Inputs
Real-World Testbed
Outputs
OUTPUT #1 (SQL Injection)
OUTPUT #2 (DoS)
OUTPUT #3 (XSS)
OUTPUT #4 (SSRF)
OUTPUT #1 (Redis Unauth)
OUTPUT #2 (Nmap)
OUTPUT #3 (C2)
OUTPUT #1 (CVE-2025-24813)
OUTPUT #2 (SMB-Brute Force)
OUTPUT #3 (CVE-2024-2961)
Prompt
Alerts
Prompt
Alerts
ALERT #1 (SQL Injection)
ALERT #2 (DoS)
ALERT #3 (XSS)
ALERT #4 (SSRF)
ALERT #1 (Redis Unauth)
ALERT #2 (Nmap)
ALERT #3 (C2)
ALERT #1 (CVE-2025-24813)
ALERT #2 (SMB-Brute Force)
ALERT #3 (CVE-2024-2961)
Time range: 
2025-03-26 22:03:28 to 
2025-03-26 22:03:58, 
detected 180 times 
'SQL Injection 
Attempt' attack, 
source IP: 
192.168.75.142, target: 
192.168.75.129:80, risk 
level: 1
...
Time range: 
2025-03-27 16:17:55 
to 2025-03-27 
16:18:03, detected 77 
times 'Redis 
Unauthorized Access' 
attack, source IP: 
192.168.75.213, 
target: 
192.168.75.166:6379, 
risk level: 4
Time range: 
2025-03-27 08:17:47 to 
2025-03-27 08:18:17, 
detected 31 times 
'Tomcat RCE Attempt - 
InvokerTransformer' 
attack, source IP: 
192.168.75.137, target: 
192.168.75.208:8082, 
risk level: 5
...
Case  1
Case 2
Case 3
[ { "tool": "block_ip", "params": {...} },
  { "tool": "enforce_apparmor", "params": {...} },
  { "tool": "deploy_hids", "params": {...} },
  { "tool": "patch_vulnerabilities", "params": {...} },
   ... ]
[ { "tool": "block_ip", "params": {...} },
  { "tool": "secure_sshd", "params": {...} },
  { "tool": "enforce_apparmor", "params": {...} },
  { "tool": "deploy_hids", "params": {...} },
   ... ]
[ { "tool": "block_ip", "params": {...} },
  { "tool": "enforce_apparmor", "params": {...} },
  { "tool": "deploy_hids", "params": {...} },
  { "tool": "harden_kernel", "params": {...} },
   ... ]
Attacker 
Device 1
Device 2
Device 3
Device 4
LLM-Based 
Agent
Attacker 
Device 3
Device 1
Device 2
LLM-Based 
Agent
LLM-Based 
Agent
Attacker 
Device 3
Device 2
Device 1
Nmap
You are a cybersecurity 
analyst ... Based on the 
following IDS detection 
summary, please 
select ... response tools 
from the provided list. 
Aim to use multiple 
tools in a coordinated 
manner to effectively 
address the detected 
threat. 
Available tools:
{tool_list}
IDS detection summary:
{alert_summary}
{env_description}
{tool_call_list_example}
You are a cybersecurity 
analyst ... Based on the 
following IDS detection 
summary, please 
select ... response tools 
from the provided list. 
Aim to use multiple 
tools in a coordinated 
manner to effectively 
address the detected 
threat. 
Available tools:
{tool_list}
IDS detection summary:
{alert_summary}
{env_description}
{tool_call_list_example}
You are a cybersecurity 
analyst ... Based on the 
following IDS detection 
summary, please 
select ... response tools 
from the provided list. 
Aim to use multiple 
tools in a coordinated 
manner to effectively 
address the detected 
threat. 
Available tools:
{tool_list}
IDS detection summary:
{alert_summary}
{env_description}
{tool_call_list_example}
LLM-Based       
Agent
LLM-Based       
Agent
LLM-Based       
Agent
Fig. 7. Case study of the proposed SecLoop. At the top of this figure, three heterogeneous real-world environments composed of various embedded devices,
a host, and a laptop. The workflow indicates that the attacker attempts to attack multiple devices. Subsequently, our LLM-based agent summarizes alerts and
generates corresponding in-depth security strategies. Available security tools on the devices will be invoked to deal with the diverse attacks.
attacks as listed in Table I. The mitigation tools and exe-
cution methods required for these attacks vary significantly.
Our proposed SA-GRPO algorithm is capable of identifying
the appropriate tools for various attacks and automatically
invoking them, demonstrating its practicality in real-world
environments. This approach advances automated network
security mitigation and reduces the cost of manual operations.
B. Generalization of Our Proposed SA-GRPO to Heteroge-
neous Environments
Communication security scenarios often involve heteroge-
neous devices and dynamic environments, which offer high
demands on the model’s generalization capability. We test the
SA-GRPO model in three different heterogeneous real-world
environments and found that it achieved an accuracy rate of
over 91% as shown in Figure 5(e), demonstrating the model’s
potential for practical deployment.
C. Self-Evolving of Our Proposed SecLoop
Due to the dynamic nature of environments and software
version updates, tool invocation presents significant chal-
lenges, requiring continuous updates and evolution of the
model. In the future, we plan to conduct in-depth research
into the self-evolution mechanism of LLMs, leveraging online
feedback from actual environments to drive the self-adaptation
of the SecLoop system’s security capabilities and minimize
potential adverse impacts such as over-defense. Additionally,
we will explore the collaboration between large and small
models to reduce system resource consumption and latency.
By implementing dynamic task allocation and knowledge
distillation techniques, we aim to significantly reduce resource
consumption and latency, thereby enhancing the system’s suit-
ability for resource-constrained deployment scenarios without
compromising security effectiveness.
D. Fault Tolerance and Proactive Threat Discovery
To enhance the system for production-grade deployment,
our future work will also focus on developing robust fault
tolerance and proactive defense capabilities. We plan to ex-
plore a “Guardian Model” framework, where an independent
monitoring model performs real-time risk assessment on the
strategies generated by the main agent, intervening to prevent
high-risk actions. Concurrently, we will investigate integrating
formal verification methods to logically validate strategies
against predefined security invariants before execution. Fur-
thermore, we aim to evolve SecLoop from a reactive system
to one capable of proactive threat discovery by incorporating
advanced techniques, such as program analysis and fuzz
testing, to autonomously identify potential vulnerabilities.


---

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021
14
VI. CONCLUSION
In this work, we address the pressing security challenges
posed by the dynamic, open, and heterogeneous nature of 6G
Zero-Touch Networks by introducing SecLoop and SA-GRPO.
SecLoop provides a fully automated, end-to-end security au-
tomation framework that integrates LLMs across the entire
lifecycle of strategy generation, orchestration, execution, and
feedback, enabling intelligent and adaptive defense in real-
world adversarial environments. Building on this foundation,
SA-GRPO serves as a novel group-based reinforcement learn-
ing algorithm that optimizes security strategies without relying
on high-quality labeled data, leveraging parallel execution and
feedback-driven refinement. Experimental results demonstrate
the effectiveness of our approach in heterogeneous network
scenarios. We believe that SecLoop and SA-GRPO offer a
practical and extensible foundation for intelligent security
automation in ZTNs. In the future, we plan to explore online
self-evolution of the proposed SecLoop system.
APPENDIX A
HYPERPARAMETER CONFIGURATIONS
To ensure the reproducibility of our work, this sec-
tion provides a detailed breakdown of the hyperparame-
ter configurations used for training our model with the
SA-GRPO algorithm. Our experiments are based on the
Qwen2.5-7B-Instruct model. We utilized the Deep-
Speed ZeRO-2 strategy for distributed training across 8 GPUs,
optimizing for computational efficiency with a bfloat16
mixed-precision setup.
Table IV summarizes these key hyperparameters and
algorithm-specific configurations used in our model training
and optimization strategy.
APPENDIX B
TIME COMPLEXITY ANALYSIS
In this section, we provide a formal theoretical analysis of
the SecLoop framework’s complexity in terms of time, mes-
sages, and communication rounds. The analysis is presented
for the two primary operational phases: the training phase and
the inference (deployment) phase. We define the following
variables for our analysis: B denotes the batch size of prompts,
G is the group size (number of generations per prompt), Lp
is the length of the input prompt sequence, Lc is the length
of the generated completion (policy) sequence, dmodel is the
hidden dimension of the model, P is the total number of
model parameters, Nenv is the number of parallel BATTLE-
FIELD environments, and Tsim is the time required for a single
BATTLE-FIELD simulation.
A. Complexity Analysis of the Training Phase
During the training phase, the system optimizes the model’s
policy through iterative steps. Each training step comprises
three core stages: policy generation, parallel evaluation, and
policy update.
1) Time Complexity of Policy Generation: The objective
of this stage is to generate G candidate policies for each of
TABLE IV
KEY HYPERPARAMETERS, DESCRIPTIONS, AND CONFIGURATIONS
Hyper
Parameter
Description
Value
G
Number of response samples gen-
erated per query for group-relative
advantage estimation; controls di-
versity and stability of policy up-
dates.
7
εlow
Lower bound for clipping the prob-
ability ratio γi,t(θ) in the surrogate
objective; avoids overly conserva-
tive updates.
0.2
εhigh
Upper bound for clipping γi,t(θ);
limits aggressive updates to pro-
mote stability and prevent large
policy shifts.
0.28
reward weights
Weights for each reward function.
1
α
Controls the mix between the cur-
rent policy and the previous refer-
ence policy during updates.
0.6
β
Coefficient
for
KL
divergence
penalty, controlling the regulariza-
tion against the reference policy for
stable fine-tuning.
0
Learning Rate
Step size for updating policy pa-
rameters during optimization.
3e−6
ref model sync
steps
Determines how frequently the cur-
rent policy is synchronized with the
reference policy.
512
torch dtype
Mixed-precision
training
using
bfloat16
for
computational
efficiency.
bfloat16
num train epochs
Total number of training epochs.
1
per device train
batch size
Batch size per GPU.
4
gradient accu-
mulation steps
Gradient accumulation steps.
1
the B prompts. The time complexity is derived from the first
principles of the Transformer architecture.
First, the complexity of a single forward pass for a sequence
of length L is dominated by the self-attention mechanism
(O(L2 · dmodel)) and the feed-forward network (O(L · d2
model)).
Thus, the total complexity is given by:
Tsingle pass(L) = O(L2 · dmodel + L · d2
model).
(22)
During autoregressive generation with a KV cache, a policy
of length Lc is generated from a prompt of length Lp. This in-
volves a Prefill operation on the prompt to compute and cache
KV vectors, with a complexity of Tprefill = Tsingle pass(Lp).
Subsequently, a Decoding loop generates tokens sequentially.
The complexity to generate the i-th token is approximately
O((Lp + i) · d2
model). Therefore, the total decoding complexity
for Lc tokens is the sum over all generated tokens:
Lc
X
i=1
O((Lp + i −1) · d2
model),
(23)
which is approximately:
O(Lc · (Lp + Lc) · d2
model).
(24)
For a total batch size of N = B · G, we extend the above
complexity to the entire batch. This yields the total time


---

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021
15
complexity formula for the policy generation stage:
Tgeneration =O

B · G ·
 L2
p · dmodel + Lp · d2
model
+ Lc · (Lp + Lc) · d2
model

.
(25)
2) Complexity of Parallel Evaluation in BATTLE-
FIELD: The B × G generated policies are distributed among
Nenv parallel BATTLE-FIELD environments for evaluation.
• Time Complexity: For a single simulation, the time
complexity is:
O(Tsim ×
B × G
Nenv

).
(26)
• Messages and Rounds: This stage constitutes the main
external communication overhead. Within one training
step, there is one core interaction: the trainer sends all
policies to the BATTLE-FIELD server, and the server
returns the corresponding scores. The number of logical
messages is proportional to the total number of policies,
i.e., O(B · G).
3) Time Complexity of Policy Update: This stage is
a standard backpropagation process, with a computational
cost proportional to the forward pass. The complexity of
one backpropagation pass is proportional to the product of
the batch size, sequence length, and the number of model
parameters. For a total batch size of N = B · G and a total
sequence length of L = Lp + Lc, the time complexity for the
policy update stage is Tupdate = O(B · G · (Lp + Lc) · P).
B. Complexity Analysis of the Inference (Deployment) Phase
During deployment for autonomous response, the analysis
focuses on the end-to-end response time for a single event.
1) Time Complexity: The total response time Tresponse is the
sum of three sequential stages: Tresponse = Tinfer+Tcomm+Texec.
• Policy Generation (Tinfer): For a single inference pass
where B = 1 and G = 1, the generation time is:
Tinfer =O(L2
alert · dmodel + Lalert · d2
model+
Lpolicy · (Lalert + Lpolicy) · d2
model).
(27)
• Communication Latency (Tcomm): The delay from send-
ing the policy over the network.
• Execution Latency (Texec): The time required for secu-
rity tools to execute on the target system.
2) Messages and Rounds: The communication model
during inference is a fixed 2-round interaction protocol for
a single, decisive action:
• Round 1: The sensor/IDS sends 1 alert message to the
LLM Agent.
• Round 2: The LLM Agent sends 1 policy directive to
the execution endpoint.
This framework is extensible to handle complex incidents
requiring iterative reasoning. In such cases, the protocol can
be expanded to 2n rounds, where n is the number of steps
in the response plan. After each action, the execution result
serves as a new observation, initiating a subsequent 2-round
cycle for the next-step decision.
REFERENCES
[1] C.-X. Wang, X. You, X. Gao, X. Zhu, Z. Li, C. Zhang, H. Wang,
Y. Huang, Y. Chen, H. Haas et al., “On the Road to 6G: Visions,
Requirements, Key Technologies, and Testbeds,” IEEE Communications
Surveys & Tutorials, vol. 25, no. 2, pp. 905–974, 2023.
[2] F. Jiang, C. Pan, L. Dong, K. Wang, M. Debbah, D. Niyato, and
Z. Han, “A Comprehensive Survey of Large AI Models for Future
Communications: Foundations, Applications and Challenges,” arXiv
preprint arXiv:2505.03556, 2025.
[3] F. Zhu, X. Wang, X. Li, M. Zhang, Y. Chen, C. Huang, Z. Yang, X. Chen,
Z. Zhang, R. Jin et al., “Wireless Large AI Model: Shaping the AI-Native
Future of 6G and Beyond,” arXiv preprint arXiv:2504.14653, 2025.
[4] Q. Cui, X. You, N. Wei, G. Nan, X. Zhang, J. Zhang, X. Lyu, M. Ai,
X. Tao, Z. Feng et al., “Overview of AI and Communication for 6G Net-
work: Fundamentals, Challenges, and Future Research Opportunities,”
Science China Information Sciences, vol. 68, no. 7, p. 171301, 2025.
[5] L. Yang, S. Naser, A. Shami, S. Muhaidat, L. Ong, and M. Debbah, “To-
wards Zero Touch Networks: Cross-Layer Automated Security Solutions
for 6G Wireless Networks,” IEEE Transactions on Communications,
2025.
[6] A. Masaracchia, V. Sharma, M. Fahim, O. A. Dobre, and T. Q. Duong,
“Digital Twin for Open RAN: Toward Intelligent and Resilient 6G Radio
Access Networks,” IEEE Communications Magazine, vol. 61, no. 11, pp.
112–118, 2023.
[7] M. El Rajab, L. Yang, and A. Shami, “Zero-touch Networks: Towards
Next-Generation Network Automation,” Computer Networks, vol. 243,
p. 110294, 2024.
[8] K. Wang, K. Yang, H.-H. Chen, and L. Zhang, “Computation Diversity
in Emerging Networking Paradigms,” IEEE Wireless Communications,
vol. 24, no. 1, pp. 88–94, 2017.
[9] K. Wang, K. Yang, and C. S. Magurawalage, “Joint Energy Minimiza-
tion and Resource Allocation in C-RAN with Mobile Cloud,” IEEE
Transactions on Cloud Computing, vol. 6, no. 3, pp. 760–770, 2016.
[10] V.-L. Nguyen, P.-C. Lin, B.-C. Cheng, R.-H. Hwang, and Y.-D. Lin,
“Security and Privacy for 6G: A Survey on Prospective Technologies
and Challenges,” IEEE Communications Surveys & Tutorials, vol. 23,
no. 4, pp. 2384–2428, 2021.
[11] Y. Chen, M. Cui, D. Wang, Y. Cao, P. Yang, B. Jiang, Z. Lu, and B. Liu,
“A Survey of Large Language Models for Cyber Threat Detection,”
Computers & Security, p. 104016, 2024.
[12] M. M. Salim, S. Rathore, and J. H. Park, “Distributed Denial of
Service Attacks and Its Defenses in IoT: A Survey,” The Journal of
Supercomputing, vol. 76, pp. 5320–5363, 2020.
[13] A. K. Abasi, M. Aloqaily, B. Ouni, M. Guizani, M. Debbah, and
F. Karray, “A Survey on Securing 6G Wireless Communications Based
Optimization Techniques,” in 2023 International Wireless Communica-
tions and Mobile Computing (IWCMC).
IEEE, 2023, pp. 216–223.
[14] M. A. Ferrag, O. Friha, B. Kantarci, N. Tihanyi, L. Cordeiro, M. Debbah,
D. Hamouda, M. Al-Hawawreh, and K.-K. R. Choo, “Edge Learning
for 6G-enabled Internet of Things: A Comprehensive Survey of Vul-
nerabilities, Datasets, and Defenses,” IEEE Communications Surveys &
Tutorials, vol. 25, no. 4, pp. 2654–2713, 2023.
[15] X. Cao, G. Nan, H. Guo, H. Mu, L. Wang, Y. Lin, Q. Zhou, J. Li, B. Qin,
Q. Cui et al., “Exploring LLM-Based Multi-Agent Situation Awareness
for Zero-Trust Space-Air-Ground Integrated Network,” IEEE Journal on
Selected Areas in Communications, 2025.
[16] M. A. Ferrag, A. Battah, N. Tihanyi, R. Jain, D. Maimut¸, F. Alwahedi,
T. Lestable, N. S. Thandi, A. Mechri, M. Debbah et al., “SecureFalcon:
Are We There Yet in Automated Software Vulnerability Detection with
LLMs?” IEEE Transactions on Software Engineering, 2025.
[17] F. Jiang, Y. Peng, L. Dong, K. Wang, K. Yang, C. Pan, D. Niyato, and
O. A. Dobre, “Large Language Model Enhanced Multi-Agent Systems
for 6G Communications,” IEEE Wireless Communications, 2024.
[18] M. A. Ferrag, M. Ndhlovu, N. Tihanyi, L. C. Cordeiro, M. Debbah,
and T. Lestable, “Revolutionizing Cyber Threat Detection with Large
Language Models,” arXiv preprint arXiv:2306.14263, pp. 195–202,
2023.
[19] F. Jiang, L. Dong, S. Tu, Y. Peng, K. Wang, K. Yang, C. Pan,
and D. Niyato, “Personalized Wireless Federated Learning for Large
Language Models,” arXiv preprint arXiv:2404.13238, 2024.
[20] Y. Zheng, Z. Li, X. Xu, and Q. Zhao, “Dynamic Defenses in Cyber Se-
curity: Techniques, Methods and Challenges,” Digital Communications
and Networks, vol. 8, no. 4, pp. 422–435, 2022.
[21] M. Khan and L. Ghafoor, “Adversarial Machine Learning in the Context
of Network Security: Challenges and Solutions,” Journal of Computa-
tional Intelligence and Robotics, vol. 4, no. 1, pp. 51–63, 2024.


---

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021
16
[22] D. Wu, J. Chen, R. Xie, and K. Chen, “OntoCSD: An Ontology-based
Security Model for an Integrated Solution of Cyberspace Defense,”
Frontiers of Information Technology & Electronic Engineering, vol. 25,
no. 9, pp. 1209–1225, 2024.
[23] U. Bartwal, S. Mukhopadhyay, R. Negi, and S. Shukla, “Security
Orchestration, Automation, and Response Engine for Deployment of
Behavioural Honeypots,” in 2022 IEEE Conference on Dependable and
Secure Computing (DSC).
IEEE, 2022, pp. 1–8.
[24] N. S. Chahal, P. Bali, and P. K. Khosla, “A Proactive Approach to Assess
Web Application Security through the Integration of Security Tools in
a Security Orchestration Platform,” Computers & Security, vol. 122, p.
102886, 2022.
[25] L. Liu, C. Tang, L. Zhang, and S. Liao, “A Generic Approach for
Network Defense Strategies Generation Based on Evolutionary Game
Theory,” Information Sciences, vol. 677, p. 120875, 2024.
[26] S. Y. Enoch, C. Y. Moon, D. Lee, M. K. Ahn, and D. S. Kim, “A
Practical Framework for Cyber Defense Generation, Enforcement and
Evaluation,” Computer Networks, vol. 208, p. 108878, 2022.
[27] Z. T. Sworna, C. Islam, and M. A. Babar, “APIRO: A Framework for
Automated Security Tools API Recommendation,” ACM Transactions
on Software Engineering and Methodology, vol. 32, no. 1, pp. 1–42,
2023.
[28] Z. T. Sworna, M. A. Babar, and A. Sreekumar, “IRP2API: Automated
Mapping of Cyber Security Incident Response Plan to Security Tools’
APIs,” in 2023 IEEE International Conference on Software Analysis,
Evolution and Reengineering (SANER).
IEEE, 2023, pp. 546–557.
[29] N. Yan, K. Wang, K. Zhi, C. Pan, K. K. Chai, and H. V. Poor, “Secure
and Private Over-the-air Federated Learning: Biased and Unbiased
Aggregation Design,” IEEE Transactions on Wireless Communications,
2025.
[30] E. E. Abdallah, A. F. Otoom et al., “Intrusion Detection Systems
using Supervised Machine Learning Techniques: A survey,” Procedia
Computer Science, vol. 201, pp. 205–212, 2022.
[31] O. Faker and E. Dogdu, “Intrusion Detection Using Big Data and
Deep Learning Techniques,” in Proceedings of the 2019 ACM Southeast
conference, 2019, pp. 86–93.
[32] R. Dungarani and S. N. Gujjar, “SDN Security: Taming the Wild West
of Network Automation,” in 2024 IEEE International Conference on
Blockchain and Distributed Systems Security (ICBDS).
IEEE, 2024,
pp. 1–13.
[33] A. M. Zarca, D. Garcia-Carrillo, J. B. Bernabe, J. Ortiz, R. Marin-
Perez, and A. Skarmeta, “Managing AAA in NFV/SDN-enabled IoT
scenarios,” in 2018 Global Internet of Things Summit (GIoTS).
IEEE,
2018, pp. 1–7.
[34] A. Robles-Enciso, J. M. Bernab´e Murcia, A. Molina Zarca, and
A. Skarmeta Gomez, “Dynamic Multi-Method Allocation for Intent-
based Security Orchestration,” Journal of Network and Systems Man-
agement, vol. 33, no. 1, pp. 1–28, 2025.
[35] C. Basile, F. Valenza, A. Lioy, D. R. Lopez, and A. P. Perales,
“Adding Support for Automatic Enforcement of Security Policies in
NFV Networks,” IEEE/ACM Transactions on Networking, vol. 27, no. 2,
pp. 707–720, 2019.
[36] S. Batewela, M. Liyanage, E. Zeydan, M. Ylianttila, and P. Ranaweera,
“Security Orchestration in 5G and Beyond Smart Network Technolo-
gies,” IEEE Open Journal of the Computer Society, 2025.
[37] I. Parvez, A. Rahmati, I. Guvenc, A. I. Sarwat, and H. Dai, “A Survey on
Low Latency Yowards 5G: RAN, Core Network and Caching Solutions,”
IEEE Communications Surveys & Tutorials, vol. 20, no. 4, pp. 3098–
3130, 2018.
[38] M. B¨ohme, E. Bodden, T. Bultan, C. Cadar, Y. Liu, and G. Scan-
niello, “Software Security Analysis in 2030 and Beyond: A Research
Roadmap,” ACM Transactions on Software Engineering and Methodol-
ogy, 2024.
[39] Y. Yu, W. Yang, W. Ding, and J. Zhou, “Reinforcement Learning
Solution for Cyber-Physical Systems Security Against Replay Attacks,”
IEEE Transactions on Information Forensics and Security, vol. 18, pp.
2583–2595, 2023.
[40] M. A. Issa, H. Chen, J. Wang, and M. Imani, “CyberRL: Brain-Inspired
Reinforcement Learning for Efficient Network Intrusion Detection,”
IEEE Transactions on Computer-Aided Design of Integrated Circuits
and Systems, 2024.
[41] L. Zhang, T. Zhu, F. Hussain, D. Ye, and W. Zhou, “A Game-Theoretic
Method for Defending Against Advanced Persistent Threats in Cyber
Systems,” IEEE Transactions on Information Forensics and Security,
2023.
[42] D. Goel, K. Moore, M. Guo, D. Wang, M. Kim, and S. Camtepe,
“Optimizing Cyber Defense in Dynamic Active Directories through
Reinforcement Learning,” in European Symposium on Research in
Computer Security.
Springer, 2024, pp. 332–352.
[43] Y. Tang, J. Sun, H. Wang, J. Deng, L. Tong, and W. Xu, “A Method
of Network Attack-Defense Game and Collaborative Defense Decision-
Making Based on Hierarchical Multi-Agent Reinforcement Learning,”
Computers & Security, vol. 142, p. 103871, 2024.
[44] M. Jiang, B. Cui, J. Fu, T. Wang, L. Yao, and B. K. Bhargava,
“RUDOLF: An Efficient and Adaptive Defense Approach Against
Website Fingerprinting Attacks Based on Soft Actor-Critic Algorithm,”
IEEE Transactions on Information Forensics and Security, 2024.
[45] L. Tong, A. Laszka, C. Yan, N. Zhang, and Y. Vorobeychik, “Finding
Needles in a Moving Haystack: Prioritizing Alerts with Adversarial
Reinforcement Learning,” in Proceedings of the AAAI Conference on
Artificial Intelligence, vol. 34, no. 01, 2020, pp. 946–953.
[46] ETSI, “Zero-Touch Network and Service Management (ZSM); Refer-
ence Architecture, ETSI GS ZSM 002, v1.1.1,” Aug 2019.
[47] A. Rosay, E. Cheval, F. Carlier, and P. Leroux, “Network Intrusion
Detection: A Comprehensive Analysis of CIC-IDS2017,” in 8th In-
ternational Conference on Information Systems Security and Privacy.
SCITEPRESS-Science and Technology Publications, 2022, pp. 25–36.
[48] J. L. Leevy and T. M. Khoshgoftaar, “A Survey and Analysis of Intrusion
Detection Models Based on CSE-CIC-IDS2018 Big Data,” Journal of
Big Data, vol. 7, pp. 1–19, 2020.
[49] N. Moustafa and J. Slay, “UNSW-NB15: A Comprehensive Data Set
for Network Intrusion Detection Systems (UNSW-NB15 Network Data
Set),” in 2015 military communications and information systems confer-
ence (MilCIS).
IEEE, 2015, pp. 1–6.
[50] T. M. Cover, ELEMENTS OF INFORMATION THEORY.
John Wiley
& Sons, 1999.
[51] L. Fawcett, S. Scott-Hayward, M. Broadbent, A. Wright, and N. Race,
“Tennison: A Distributed SDN Framework for Scalable Network Se-
curity,” IEEE Journal on Selected Areas in Communications, vol. 36,
no. 12, 2018.
[52] K. Kalkan, L. Altay, G. G¨ur, and F. Alag¨oz, “JESS: Joint Entropy-Based
DDoS Defense Scheme in SDN,” IEEE Journal on Selected Areas in
Communications, vol. 36, no. 10, pp. 2358–2372, 2018.
[53] A. M. Zarca, J. B. Bernabe, A. Skarmeta, and J. M. A. Calero, “Virtual
IoT HoneyNets to Mitigate Cyberattacks in SDN/NFV-enabled IoT
Networks,” IEEE Journal on Selected Areas in Communications, vol. 38,
no. 6, pp. 1262–1277, 2020.
[54] Z. Long and W. Jinsong, “A Hybrid Method of Entropy and SSAE-SVM
Based DDoS Detection and Mitigation Mechanism in SDN,” Computers
& Security, vol. 115, p. 102604, 2022.
[55] Y. Otoum, A. Asad, and A. Nayak, “LLM-Based Threat Detec-
tion and Prevention Framework for IoT Ecosystems,” arXiv preprint
arXiv:2505.00240, 2025.
[56] A. Tellache, A. A. Korba, A. Mokhtari, H. Moldovan, and Y. Ghamri-
Doudane, “Advancing Autonomous Incident Response: Leveraging
LLMs and Cyber Threat Intelligence,” arXiv preprint arXiv:2508.10677,
2025.
[57] X. Lin, J. Zhang, G. Deng, T. Liu, X. Liu, C. Yang, T. Zhang, Q. Guo,
and R. Chen, “IRCopilot: Automated Incident Response with Large
Language Models,” arXiv preprint arXiv:2505.20945, 2025.
[58] S. Baral, S. Saha, and A. Haque, “Autonomous Cyber Incident Response
Using Reasoning and Action,” in 2025 International Wireless Communi-
cations and Mobile Computing (IWCMC). IEEE, 2025, pp. 1392–1397.
[59] F. Wei, H. Li, Z. Zhao, and H. Hu, “{xNIDS}: Explaining Deep
Learning-based Network Intrusion Detection Systems for Active In-
trusion Responses,” in 32nd USENIX Security Symposium (USENIX
Security 23), 2023, pp. 4337–4354.
[60] A. Nadeem, S. Verwer, S. Moskal, and S. J. Yang, “Enabling Visual
Analytics via Alert-driven Attack Graphs,” in ACM SIGSAC Conference
on Computer and Communications Security. Association for Computing
Machinery (ACM), 2021, pp. 2420–2422.
[61] Z. Shao, P. Wang, Q. Zhu, R. Xu, J. Song, X. Bi, H. Zhang,
M. Zhang, Y. Li, Y. Wu et al., “Deepseekmath: Pushing the Limits
of Mathematical Reasoning in Open Language Models,” arXiv preprint
arXiv:2402.03300, 2024.
[62] K. Ethayarajh, W. Xu, N. Muennighoff, D. Jurafsky, and D. Kiela,
“Model Alignment as Prospect Theoretic Optimization,” in Forty-first
International Conference on Machine Learning, 2024.
[63] V. Mnih, K. Kavukcuoglu, D. Silver, A. Graves, I. Antonoglou, D. Wier-
stra, and M. Riedmiller, “Playing atari with deep reinforcement learn-
ing,” arXiv preprint arXiv:1312.5602, 2013.
[64] H. Van Hasselt, A. Guez, and D. Silver, “Deep Reinforcement Learning
with Double Q-Learning,” in Proceedings of the AAAI conference on
artificial intelligence, vol. 30, no. 1, 2016.


---

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021
17
[65] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proxi-
mal Policy Optimization Algorithms,” arXiv preprint arXiv:1707.06347,
2017.
[66] Q. Yu, Z. Zhang, R. Zhu, Y. Yuan, X. Zuo, Y. Yue, T. Fan, G. Liu,
L. Liu, X. Liu et al., “DAPO: An Open-Source LLM Reinforcement
Learning System at Scale,” arXiv preprint arXiv:2503.14476, 2025.
Xinye Cao (Graduate Student Member, IEEE) re-
ceived the B.E. degree in electronic and information
engineering from Central China Normal University
(CCNU), Wuhan, China, in 2020. She is currently
pursuing the Ph.D. degree in cyberspace security
with the National Engineering Research Center for
Mobile Network Technologies, Beijing University
of Posts and Telecommunications (BUPT). Her re-
search interests include large AI model for future
wireless communication systems and wireless com-
munication security.
Yihan Lin is currently pursuing the bachelor’s
degree with the Beijing University of Posts and
Telecommunications (BUPT), Beijing, China. He is
working as a Research Intern with the National
Engineering Research Center for Mobile Network
Technologies, BUPT. His research interests include
wireless communications security and software se-
curity.
Guoshun Nan (Member, IEEE) is a full professor
at National Engineering Research Center for Mobile
Network Technologies, Beijing University of Posts
and Telecommunications, Beijing, China. He has
broad interest in multimodal learning, large language
models, and 6G network security, and has published
more than 30 papers in top-tier journals and con-
ferences including IEEE TPAMI, IEEE JSAC, IEEE
TMC, IEEE TIFS, NeurIPS, ICML, CVPR, ICCV,
ACL, etc. He also serves as a reviewer for these
communities.
Qinchuan Zhou is currently pursuing the bachelor’s
degree with the Beijing University of Posts and
Telecommunications (BUPT), Beijing, China. He is
working as a Research Intern with the National
Engineering Research Center for Mobile Network
Technologies, BUPT. His research interests encom-
pass computer vision and large language model
based multi-agent architectures.
Yuhang Luo is currently pursuing the bachelor’s de-
gree with Beijing University of Posts and Telecom-
munications (BUPT), Beijing, China. He is working
as a Research Intern with the National Engineering
Research Center for Mobile Network Technologies,
BUPT. His research interests include penetration
testing, vulnerability mining, WEB security, and
firewall security.
Yurui Gao is currently pursuing the bachelor’s de-
gree with Beijing University of Posts and Telecom-
munications (BUPT), Beijing, China. She is working
as a Research Intern with the National Engineering
Research Center for Mobile Network Technologies,
BUPT. Her research interests include large language
model security, software security, and program anal-
ysis.
Zeliang Zhang is currently pursuing the bache-
lor’s degree with Beijing University of Posts and
Telecommunications (BUPT), Beijing, China. He is
working as a Research Intern with the National
Engineering Research Center for Mobile Network
Technologies, BUPT. His research interests include
cybersecurity and large language model.
Haolang Lu (Graduate Student Member, IEEE)
received the B.E. degree in cyberspace security from
Beijing University of Posts and Telecommunications
(BUPT), Beijing, China, in 2024. He is currently
pursuing the Ph.D. degree with the Graduate College
for Engineers, BUPT. His research interests include
artificial intelligence security and interpretability.


---

JOURNAL OF LATEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021
18
Qimei Cui (M’09–SM’15) received the B.E. and
M.S. degrees in electronic engineering from Hunan
University, Changsha, China, in 2000 and 2003,
respectively, and the Ph.D. degree in information and
communications engineering from the Beijing Uni-
versity of Posts and Telecommunications (BUPT),
Beijing, China, in 2006. She has been a Full Pro-
fessor with the School of Information and Commu-
nication Engineering, BUPT, since 2014. She was a
visiting Professor with the Department of Electronic
Engineering, University of Notre Dame, IN, USA,
in 2016. Her research interests include B5G/6G wireless communications,
mobile computing and IoT. She serves as a Technical Program Chair of the
APCC 2018, and a Track Chair of IEEE/CIC ICCC 2018, and a Workshop
Chair of WPMC 2016. She also serves as a Technical Program Committee
Member of several international conferences, such as the IEEE ICC, the IEEE
WCNC, the IEEE PIMRC, the IEEE ICCC, the WCSP 2013, and the IEEE
ISCIT 2012. She won the Best Paper Award at the IEEE ISCIT 2012, the IEEE
WCNC 2014, and the WCSP 2019, and the Honorable Mention Demo Award
at the ACM MobiCom 2009, and the Young Scientist Award at the URSI
GASS 2014. She serves as Editor of SCIENCE CHINA Information Science
, and Guest Editor of the EURASIP Journal on Wireless Communications
and Networking and International Journal of Distributed Sensor Networks
and Journal of Computer Networks and Comm.
Yanzhao Hou (Member, IEEE) received the Ph.D.
degree from the Beijing University of Posts and
Telecommunications (BUPT), Beijing, China, in
2014. He is currently with the National Engineering
Research Center for Mobile Network Technologies,
BUPT. His current research interests include wire-
less federated learning, AI-driven wireless communi-
cations and trial systems. He received the Best Demo
Award in IEEE APCC2018.
Xiaofeng Tao received the B.S. degree in electrical
engineering from Xi’an Jiaotong University, Xi’an,
China, in 1993, and the M.S. and Ph.D. degrees in
telecommunication engineering from Beijing Uni-
versity of Posts and Telecommunications(BUPT),
Beijing, China, in 1999 and 2002, respectively. He
is a Professor in BUPT, a Fellow of the Institution
of Engineering and Technology, and Chair of the
IEEE ComSoc Beijing Chapter. He has authored
or co-authored over 200 papers and three books
in wireless communication areas. He focuses on
5G/B5G research.
Tony Q.S. Quek (S’98-M’08-SM’12-F’18) received
the B.E. and M.E. degrees in electrical and electron-
ics engineering from the Tokyo Institute of Technol-
ogy in 1998 and 2000, respectively, and the Ph.D.
degree in electrical engineering and computer sci-
ence from the Massachusetts Institute of Technology
in 2008. Currently, he is the Associate Provost (AI
& Digital Innovation) and Cheng Tsang Man Chair
Professor with Singapore University of Technology
and Design (SUTD). He also serves as the Director
of the Future Communications R&D Programme,
and the ST Engineering Distinguished Professor. He is a co-founder of
Silence Laboratories and NeuroRAN. His current research topics include
wireless communications and networking, network intelligence, non-terrestrial
networks, open radio access network, AI-RAN, and 6G.
Dr. Quek was honored with the 2008 Philip Yeo Prize for Outstanding
Achievement in Research, the 2012 IEEE William R. Bennett Prize, the
2015 SUTD Outstanding Education Awards – Excellence in Research, the
2016 IEEE Signal Processing Society Young Author Best Paper Award,
the 2017 CTTC Early Achievement Award, the 2017 IEEE ComSoc AP
Outstanding Paper Award, the 2020 IEEE Communications Society Young
Author Best Paper Award, the 2020 IEEE Stephen O. Rice Prize, the 2020
Nokia Visiting Professor, the 2022 IEEE Signal Processing Society Best Paper
Award, the 2024 IIT Bombay International Award For Excellence in Research
in Engineering and Technology, the IEEE Communications Society WTC
Recognition Award 2024, and the Public Administration Medal (Bronze). He
is an IEEE Fellow, a WWRF Fellow, an AIIA Fellow, and a Fellow of the
Academy of Engineering Singapore.
