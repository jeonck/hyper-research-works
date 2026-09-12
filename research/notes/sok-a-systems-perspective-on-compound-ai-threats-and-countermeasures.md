---
title: 'SoK: A Systems Perspective on Compound AI Threats and Countermeasures'
id: sok-a-systems-perspective-on-compound-ai-threats-and-countermeasures
tags:
- attack-ontology-drift-cti-85bc51
- pin-rate-survey
created: '2026-09-12T21:36:32.662863Z'
updated: '2026-09-12T21:44:36.527947Z'
source: https://arxiv.org/abs/2411.13459v1
source_domain: arxiv.org
fetched_at: '2026-09-12T21:36:32.662470Z'
fetch_provider: crawl4ai
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'arXiv 2411.13459v1: 0 ATT&CK technique-ID occurrences, below the pin-rate-survey
  inclusion threshold of 3.'
raw_file: raw/sok-a-systems-perspective-on-compound-ai-threats-and-countermeasures.pdf
doi: arXiv:2411.13459v1
---

SoK: A Systems Perspective on Compound AI Threats and Countermeasures
Sarbartha Banerjee∗†,
Prateek Sahu∗†,
Mulong Luo†,
Anjo Vahldiek-Oberwagner‡,
Neeraja J. Yadwadkar†,
and Mohit Tiwari†§
†The University of Texas at Austin
‡Intel Labs
§Symmetry Systems
Abstract—Large language models (LLMs) used across enter-
prises often use proprietary models and operate on sensitive
inputs and data. The wide range of attack vectors identified in
prior research—targeting various software and hardware com-
ponents used in training and inference—makes it extremely
challenging to enforce confidentiality and integrity policies.
As we advance towards constructing compound AI infer-
ence pipelines that integrate multiple large language models
(LLMs), the attack surfaces expand significantly. Attackers
now focus on the AI algorithms as well as the software and
hardware components associated with these systems. While
current research often examines these elements in isolation, we
find that combining cross-layer attack observations can enable
powerful end-to-end attacks with minimal assumptions about
the threat model. Given, the sheer number of existing attacks
at each layer, we need a holistic and systemized understanding
of different attack vectors at each layer.
This SoK discusses different software and hardware attacks
applicable to compound AI systems and demonstrates how
combining multiple attack mechanisms can reduce the threat
model assumptions required for an isolated attack. Next, we
systematize the ML attacks in lines with the Mitre Att&ck
framework to better position each attack based on the threat
model. Finally, we outline the existing countermeasures for
both software and hardware layers and discuss the necessity
of a comprehensive defense strategy to enable the secure and
high-performance deployment of compound AI systems.
Index Terms—Machine Learning, Security
1. Introduction
AI-powered applications like chatbots [1]–[3], and ML
tools like autonomous driving [4] and OCR [5], have be-
come widespread due to advances in neural networks and
transformers. Recent developments in large language models
(LLMs) with billions of parameters support tasks like pro-
gram and image generation. These production-ready models
train on massive data, often containing sensitive information,
and utilize proprietary architectures running on expensive
compute resources, making them targets for adversaries.
Literature in ML security and privacy have explored several
attacks [6]–[10] and developed efficient defenses [11]–[15],
∗Sarbartha Banerjee and Prateek Sahu are equal contributors.
Models
Vector DB
Databricks
Elastic
Tools
NumPy
Packages
RDMA
cuDf
Libraries
Framework
Langchain
Haystack
 Hardware 
Compute
TPU
Network
Infiniband
 Software 
 Application 
Application
6. Misclassify
Object
Software
Hardware
DDR5
4. Bitflip in 
GPU
1. Prompt 
Injection
2. Triggers
Bug
3. Hammers
DRAM
Memory
HBM
DDR5
7. Leak Data
5. Incorrect 
Computation
Figure 1. Application, software and hardware layers for compound AI.
Example shows cross-layer components can be exploited to leak data.
but many focus individually on algorithms or platforms,
ignoring the complex interactions in modern AI systems.
A recent study [16] also highlighted that privacy-preserving
models can leak data when deployed alongside other soft-
ware components, challenging existing security guarantees.
Emerging compound AI systems [17] are created by
integrating multiple AI models with numerous software
components, all deployed across distributed hardware. Fig-
ure 1-left provides a cross-stack view of a compound AI
system: The application layer comprises of multiple AI
models, vectorized databases for knowledge storage, and
associated tools used by AI agent models. The software
layer includes frameworks like Langchain [18] to design
AI pipelines, packages like Pytorch [19] to design models,
and libraries like cuDNN [20] to interface with devices.
Finally, the hardware layer comprises of compute units like
CPUs, GPUs, and TPUs along with memory and network
components. While literature have proposed attacks across
different AI/ML models and systems, vulnerabilities and
attack surfaces across different components in these layers
can be composed to create new attack vectors or relax the
threat model assumptions for existing attacks.
The complexity of layered software, distrustful entities,
and diverse hardware creates a broad attack surface, high-
lighting the need for a systematization of existing literature.
The volume of proposed attacks and defenses across differ-
ent stack layers makes it challenging to grasp threat models
and associated defenses. Heterogeneous hardware – CPUs,
GPUs, ASICs, FPGAs – introduces further risks, including
arXiv:2411.13459v1  [cs.CR]  20 Nov 2024


---

Multimodal 
Embeddings
LLM Agent
Search Query
Generation
Vector DB
Web
Draft
Generation
MoE Router
E1
E2
En
...
Aggregator
Compliance
Grounding
Multimodal 
Decoding
1. Query Pre-processing
2. Retrieval
3. Generation
4. Query Post-processing
Output
Query
Clip
VisualBERT
Chain of Thought
Zero-shot-react
BM25
ColBERT
Plaid
Dessert
Mixtral
ST-MoE
GPT
T5
Guardrails
SG Fact checker
DeepFloyd
DiffusionGPT
Figure 2. A Compound AI Pipeline begins with Query pre-processing to refine the input query and feed to an LLM agent. The agent extracts
knowledge in the Retrieval stage, generates a draft response, and fills information generated from MoE experts in the Generation step. This
response goes through compliance and fact checks Query post-processing step to finally generate a multi-modal output.
digital and physical side-channel attacks, that could expose
sensitive data or model parameters. Device ownership be-
tween cloud and edge deployments, adds complexity to
the trust landscape, expanding the overall attack surface.
Figure 1-right enumerates an example of how complex
cross-layer observations can lead to an end-to-end attack. An
attacker performs a prompt injection attack that can exploit a
software library bug, eventually triggering repeated memory
access to adjacent memory rows containing model param-
eters. Repeated access can result in Rowhammer [21], that
changes the weights tensors due to bit-flips. These tampered
weights can change the model prediction and misclassify
objects which eventually generates incorrect response.
However, no prior work has systematized the impact
of vulnerabilities in system software (e.g., frameworks,
packages, libraries) or hardware (e.g., side-channels, fault
injection) in a heterogeneous deployment platforms. We
categorize these as system attacks and focus on organizing
them with a view to the complex threat models emerging
from compound AI systems. Algorithmic attacks [6], [7],
[9], [22], that target ML algorithms and training data in the
application layers, are well-studied by prior SoKs [23]–[25].
Our work also explores attacks at the software and the hard-
ware layers that attackers can use for composing cross-layer
widgets to perform an end-to-end attack. Understanding
the threat model assumptions and attacker capabilities can
inform system designers of cross-stack attack composition
as well as define defense mechanisms at the software and
hardware layer. This also informs algorithm designers of
system and hardware impacts, and help build robust models.
In this paper, we focus on different types of system
attacks and defenses in a compound AI system. Specifically,
we make the following contributions –
1) We explore a range of software, and hardware vulnera-
bilities, as well as the defenses impacting AI models and
study how they affect compound AI pipelines. To the best
of our knowledge, this is the first effort to methodically
categorize system attacks and defenses for AI systems.
2) We focus on the cross-stack vulnerabilities introduced
by the emergence of compound AI pipelines in this
domain and systematize existing attacks and vulner-
abilities in a well-known cyber-security framework –
Mitre Att&ck [26]. This can be used a foundation
for threat model developments and methodologies for
individual defenses.
3) We explore case-studies which utilize cross-stack vulner-
abilities to mount an end-to-end attack. We discuss the
learning and gaps of current security practices and bring
out open research questions that will drive us to build
better and safer AI applications.
The rest of the paper is organized as follows. Section 2
introduces emerging compound AI pipelines and related
AI/ML security literature. Section 3 discusses the assets,
trust entities and threat models under study. Section 4 and
Section 5 explores various software and hardware attacks
and defenses of existing AI/ML systems. Section 6 works
on systematizing the attacks in a well formed framework
and explores new attack paths that are possible within
the paradigm of modern compound AI pipelines. Finally,
Section 7 addresses key learning and gaps of current security
practices before concluding in section 8.
2. Background
Language models are popular for next token prediction,
given an input prompt. With the prolific use of accelerated
hardware (GPUs, TPUs [27] etc.), such models have grown
to billions of parameters with the capability to understand
complex structures and provide high accuracy responses –
making large language models (LLMs).
Compound AI: The growing demands of LLMs and their
widespread use bring new system and design challenges.
Modern AI inference pipelines often involve multiple ML
and LLM models working together, from prompt engineer-
ing to token generation and AI-safety checks. The com-
plexity increases with the use of multi-modal inputs (e.g.,
Gemini [2]) and fine-tuned mixtures of experts (e.g., GitHub
Copilot [28], Amazon Q Developer [29], MistralAI [30]),
resulting in Compound AI systems [17].
These pipelines integrate diverse software and ML/LLM
components to optimize resource usage and improve accu-
racy. In a typical workflow shown in fig. 2, a user query,
potentially containing text, images, and videos, is processed
to generate embedded context [31]. Optimizations like few-
shot training or chain-of-thought reasoning are applied, and


---

Reconnaissance/
Resource Development
Initial Access/
Execution
Defense Evasion/
Privilege Escalation 
Collection/ 
Exfiltration (Impact)
Remote
Software 
Access
Privileged
Software 
Access
Digital
Hardware
access
Physical
Hardware 
access
Crafted Input Query
Malicious Vector Entry
Malicious Package/ Driver Config.
Training Data Poisoning
Orchestrate Victim Colocation
Enable Performance Counters
Hardware Isolation Primitive Config.
Connect Bus Monitor
Insert Hardware Trojan
Setup Noise Injection Device
Directed/Repeated Model Query
Install Malicious Package
Access Control Violation
Malicious Device Migration
Contend with Victim Resources
Locate Critical Memory Address
Access Adjacent Memory Bits
Start Executing Target Models 
Guardrail Model Bypass
Grounding Evasion
Evade Tenant Boundary
Delay Response or System Crash
Snoop Victim behavior
Bypass ECC
Extract Secret Data
Tamper Output Response
Degrade Model Performance
Privilege Escalation (C,I,A)
Biased or Unsafe Output (I)
Extract Victim Private Data (C)
Denial-of-Service (A)
Extract Model Architecture (C)
Generate Misinformation (I)
Extract Timing Side-Channel (C)
Bitflip Attack (I)
Misclassification (I)
Extract Private User Input/Response (C)
Threat
Model
Figure 3. Positioning each attack widget in the Mitre Attack framework. The different colors specify the attacker capability ranging from remote
access (weakest adversary) to physical access (strongest adversary). The attack steps through different steps. The impact denotes the security
policy violation [C = Confidentiality, I = Integrity, A = Availability]
facts may be retrieved using a Retrieval Augmented Gener-
ator (RAG) [3]. The query is then sent to an LLM for token
generation, often using a mixture-of-experts approach. Once
generated, responses undergo grounding and safety checks
before being presented back to the user. This complex-
ity requires sophisticated software orchestration to manage
model batching, data transfer, and resource allocation across
heterogeneous platforms, going beyond traditional GPU or
accelerators to meet time-sensitive user needs.
Algorithmic Attacks and Defenses: Existing ML attacks
primarily target vulnerabilities in the algorithm itself, re-
gardless of the deployment environment. Such attacks in-
clude membership inference, model extraction, and data
poisoning, among others and are classified as algorithmic
attacks in our document. Membership inference attacks [6]
aim to determine if specific data were part of a model’s
training set, risking exposure of sensitive private information
to the public. Techniques like machine unlearning [14] can
defend against these attacks. Model extraction attacks [7],
[8] seek to replicate a model’s architecture and param-
eters, which are valuable intellectual properties requiring
significant computational resources. Thus, it is important to
prevent model extraction [13]. Data poisoning attacks [9]
involve injecting corrupted data into the training set, either
reducing overall model accuracy or targeting specific predic-
tions. Data augmentation [15] is a defense strategy against
such attacks. These attacks rely solely on model inputs and
outputs during training or inference, without considering
side-channel data tied to the deployment environment. They
are distinct from system attacks we categorize in this work.
3. Threat Model Categorization
The diversity of machine learning deployments demands
a broad and adaptable threat model. Software and hardware
defenses often depend on different threat models, complicat-
ing the evaluation of an attack’s relevance in a given context.
Moreover, studies vary in their focus on secret assets and
their assumptions about trusted entities.
To address this, we first align the AI/ML attack land-
scape with the Mitre Att&ck framework [32], providing a
structured approach to understand threat models. We then
introduce various assets within a compound AI system, and
identify the trusted entities in these deployments.
3.1. MITRE ATT&CK Framework
MITRE ATT&CK [32] is a knowledge base that mod-
els cyber adversary behavior using various real-world ob-
servations. This framework reflects the various phases of
an adversary’s attack lifecycle and the platforms they are
known to target. We align the system and hardware attacks
on AI/ML systems to the MITRE framework to enable
threat model development and explore defense methodolo-
gies in AI applications. Figure 3 translates various attacks
seen across literature and Common Vulnerability and Ex-
posure(CVE) databases as as techniques across different
categories from the framework:
1) Reconnaissance and Initial Access lists the techniques
used by an attacker to identify and locate a victim model
or target device to mount an attack. For example, poison-
ing of training data or exploiting co-location patterns [33]
on cloud allows attackers to target specific applications
or models.
2) Resource Development lists down methodologies an
attacker utilizes to prepare for an exploit. These might in-
clude employing shared memory regions with victim [34]
and exploiting access control violations.
3) Privilege Escalation and Execution enumerates meth-
ods for adversaries to realize an attack. These methods
can be software or hardware contention [35], [36], and
passing illegal prompts that lead to system errors or
confused deputy [37] issues.


---

4) Collection and Exfiltration identifies the types of met-
rics or data that an attack might expose, revealing sen-
sitive information (e.g., performance counters, power
traces, execution time) or causing service-level disrup-
tions (e.g., misclassification, Denial of Service).
5) Impact lists down the confidentiality, integrity and avail-
ability aspects of an attack result as seen in the “Collec-
tion and Exfiltration” techniques.
3.2. Threat Models
We divide the attacker’s scope into categories that we
define here as four threat models. In fig. 3, we enumerate
techniques in increasing order of threat model severity.
Darker colored rows indicate a higher privilege adversary,
with attacks having a higher severity impact.
Remote software access describes a threat model where an
adversary only has remote access to a compound AI sys-
tem. This is typical for cloud-hosted applications providing
API access to AI applications. Here, the attacker is least-
privileged since she can only influence execution indirectly
(e.g. resource contention) or leak data via prompt injection.
Privileged software access involves an adversary with
elevated software control, such as root access to an OS,
hypervisors, or firmware. This includes untrusted system ad-
ministrators in a public cloud environment and users exploit-
ing privilege escalation vulnerabilities in AI pipelines. An
adversary can monitor execution via system traces, device
drivers, or disrupt operations by manipulating schedulers.
Digital hardware access includes adversaries that can issue
system commands for observing hardware metrics (e.g., per-
formance counters) or launch covert-channel attacks to leak
information like model weights and layer architecture. This
threat model is common in public cloud environments where
attackers co-locate malicious workloads with AI pipelines.
Physical hardware access represents the most privileged
adversary, with full physical access to hardware running
AI inference. This is common in edge ML deployments
where devices running sensitive models are controlled by
untrusted owners, allowing potent attacks like cold-boot,
memory dumps, or access to debug ports.
3.3. Secret Assets
Secret assets refer to confidential information that at-
tackers aim to exploit. Each component of a compound AI
system possesses distinct secret assets, as outlined below:
Model training data A compound AI system is composed
of multiple large language models (LLMs). These models
are trained on extensive datasets, some of which include
private or confidential information. Furthermore, fine-tuning
these models is often carried out using proprietary data.
Prior work [16] leaked confidential information including
user ssh key, user name, credit card info, address etc.
from training data. Membership inference attacks determine
whether specific information was included in the training
data. Lastly, certain attacks analyze the distribution of the
training data and use it to compromise the inference process.
Data poisoning attacks can either skew a model’s de-
cisions or diminish its overall effectiveness. Such attacks
are more challenging to be detected in multi-modal training
due to adversarial noise – highlighting the importance of
integrity in training data.
AI model IPs LLMs contain billions of parameters and
takes significant training resources, making them lucrative
attack targets. Attackers have tried to violate confidentiality
of ML models by extracting the weights, architecture and
hyperparameters. The model architecture can be private
for proprietary foundation models and confidential adapters
for fine-tuned models. Similarly, model hyperparameters
including learning rate, and others are lucrative for attack-
ers. Additionally, the semantic relationships between tokens
in an embedding model are confidential, as attackers can
exploit this information to carry out membership inference
attacks. The integrity of the model data is equally important.
Altering model hyperparameters can degrade model accu-
racy, while tampering with model weights may lead to mis-
classifications or the spread of misinformation.
Knowledge database The LLM models leverage recent
knowledge from vector databases, which are constantly
being populated with new information. The integrity of
the vector database is critical for generating relevant and
correct information. Similarly, the vector DBs should not
be susceptible to availability attacks like denial-of-service,
which can generate stale response.
Inference data User queries to a compound AI system can
contain sensitive information like medical records, person-
ally identifiable information(PIIs) or financial documents.
For such private data a user would like to ensure confiden-
tiality from the software, model owners and other tenants of
the compound AI application.
3.4. Trust Entities
The relationship between different trust entities plays
key role in defining a threat model. The entities include:
Hardware manufacturer has access to the hardware de-
sign and the manufacturing supply chain. Hardware Tro-
jans introduce backdoors that can be used to exploit CIA
guarantees for all assets. Since, a lot of ML systems are
designed on FPGAs, the role of hardware manufacturer
includes the FPGA manufacturer and the hardware design
bitstream owner.
Platform owner refers to a cloud-service provider or an
admin of the hosted hardware. A platform owner multiplexes
different model run on the same hardware to improve the
resource utilization of the cluster. A platform owner or a
hypervisor admin can have access to privileged software like
devise drivers or have physical access to hardware to mount
various snooping/physical attacks.
Training data owner refers to owner of private data that
is used in training an ML model. Although modern LLMs
are typically trained on a large corpus of public data, many
expert models are then fine-tuned by training on private and
sensitive data (e.g. medical images, financial documents).


---

Algorithmic attacks [6] have been shown to divulge training
data using membership inference attacks.
Model owner refers to an owner of an ML model where the
model weights, layer architecture and the hyperparameters
could be private and sensitive information. Model owners
are susceptible to information leakage via algorithmic at-
tacks [7], [8] and from distrusted co-located tenants via side-
channels [38], [39].
Inference data owner is a client side user who provides
data for inference to the AI/ML application. Similar to
training data, these inputs can be sensitive and contain PIIs
which an user would want to keep confidential from other
users and tenants on the platform.
Software developers refer to owners of third-party services
and framework components that are associated with an
end-to-end ML/AI application. Bugs and vulnerabilities can
enable attackers to gain unrestricted access to the runtime
service or the ability to mount man-in-the-middle attacks to
leak sensitive information.
4. Software vulnerabilities and defenses
Design of compound AI systems involve a development
stage followed by a deployment stage that involve a wide
variety of software frameworks, packages and libraries. The
development stage focuses on model training, knowledge in-
tegration and designing of LLM pipelines that are built using
frameworks like Langchain [18] and HuggingFace [40] and
model compilation packages(Tensorflow [41], Pytorch [19]).
Vulnerabilities like trojans, misconfigured access control
of databases, and buggy libraries and drivers can lead to
privilege escalation and initial access into systems that are
leveraged to mount sophisticated attacks. Verification of
large codebases in compound AI systems are unfeasible
because of the computational difficulty involved in with ex-
tensive repositories and models. Additionally the challenge
of accurately modeling the interactions between libraries and
continuous evolution of such deployments make it imprac-
tical to rely only on software verifications.
The deployment stage relies on various data storage
(Apache Spark [42], Hadoop [43] and Snowflake [44]) and
model orchestration (BentoML [45], Kubernetes [46]) to de-
ploy AI pipelines across heterogeneous platforms that utilize
device libraries and packages (Pyyaml [47], CuDNN [20])
to provide optimized executions. Vulnerabilities and lack
of safeguards across the software stack and device drivers
can leak to black-box attacks like prompt injection and
membership inference, or model tampering and model fin-
gerprinting attacks that violate the confidentiality, integrity
and availability of compound AI systems.
4.1. Attacks
We searched the CVE database to report several vulnera-
bilities across different components (Frameworks, Packages
and Libraries) of the compound AI stack in table 1. The
columns categorize the attacks based on the attackers’ mo-
tive, which includes violating data confidentiality, integrity,
and availability (C,I,A) of the system. The last two columns
enable the attacker to either run arbitrary code in the victim
machine, or performing privilege escalation. These attacks
enable the attacker to collect victim information including
access to system logs, scheduling processes, linking mali-
cious libraries, or introduce ransomware. These capabilities
often lead to model hijack and tampering attacks. We de-
scribe each of the attack types in detail.
Data Confidentiality An attacker can leak asset classes
including model weights and hyperparameters (layer archi-
tecture, learning coefficient, temperature etc.), input query,
training data and documents in the vector database. The
common weaknesses leading to data confidentiality violation
include (1) Buffer out-of-bound reads (OOB Read); (2) Use-
after-free memory errors; (3) Backdoor introduced by mali-
cious packages; and (4) System bugs leading to insufficient
access control. The first column in table 1 lists several CVEs
leading to data confidentiality violation, with the green
boxes needing privileged system access. The main causes of
information leakage are insufficient access control leading
to active or stale data leakage from registers and memory.
Software bugs or malicious packages trigger memory safety
errors and The majority of compound AI software is written
in Python and C++ which are not type safe languages, and
hence lacking compiler protections.
Data Integrity Data integrity is essential to prevent mis-
classification in edge deployments and the spread of mis-
information in complex RAG systems. The common weak-
nesses include (1) Buffer out-of-bound writes (OOB Writes)
by an attacker into victim memory. (2) Access control
violations enable an unprivileged attacker to gain access
to victim data while cleartext writes in databases enable
admin to change document contents. (3) Directory traversal
enables attackers to gain write access to model files while
memory corruption on compression libraries (Python zlib)
either tampering or deleting sensitive data.
Crash/Denial-of-Service System or platform availability
can be restricted with system crashes or denial-of-service
(DoS) attacks as shown in the third column of table 1.
The system crashes are triggered with unexpected behav-
ior including: (1) Heap overflow attacks leading to kernel
panic; or (2) System exceptions specifically in floating point
units(FPE) or integer overflows leading to system crash.
The DoS attacks include (1) An attacker taking over the
entire system or model resource preventing other tenants
from accessing the model; (2) An attacker can also target
the Kubernetes orchestration to prevent other tenants from
accessing a compute node. (3) Creating DoS by engaging the
system in a complex regular expression (ReDoS) is shown
in NLTK framework. System availability is important in
mission critical applications (autonomous vehicles, industry
quality-check installations) or real-time usecases (Chatbots).
Code execution Several compound AI systems are de-
ployed in a large cloud infrastructure. A code execution
vulnerability can be exploited to reveal system configura-
tion or identity. Moreover, arbitrary code can interfere with
system robustness or trigger inaccessible tools inside the
AI pipeline. (1) Arbitrary code execution (ACE) enables


---

TABLE 1. LIST OF SOFTWARE COMPONENTS WITH VULNERABILITIES IN COMPOUND AI FRAMEWORKS, PACKAGES AND UNDERLYING
LIBRARIES.■REQUIRES A PRIVILEGED ATTACKER WHILE ■REFERS TO DOS ATTACKS.
Data Confidentiality
Data Integrity
Crash/DoS
Code Execution
Privilege Escalation
Frameworks
Langchain - SQL Injection
CVE-2023-36189
ChatGPT - Integrity
CVE-2024-40594
NLTK - ReDoS
CVE-2021-43854
Haystack - ACE
CVE-2024-41950
Langchain - SSRF
CVE-2024-3095
LLama - OOB Read
CVE-2024-42478
LLama - OOB Write
CVE-2024-42479
LLama - Heap Ovf.
CVE-2024-42479
HuggingFace - RCE
CVE-2024-3568
Langflow - ACL Violation
CVE-2024-7297
HuggingFace - Access Control
CVE-2023-2800
Rasa - Directory Trvsl
CVE-2021-42556
Mxnet - Resource Hog
CVE-2022-24294
LLamaindex - Bug/RCE
CVE-2024-3271
Ollama - ACL Violation
CVE-2024-28224
Packages
Pytorch - OOB Read
CVE-2024-31584
MLFlow - ACL Violation
CVE-2024-4263
Snowflake - Arbit. input
CVE-2022-42965
Pytorch - Cmd Injection
CVE-2022-0845
Pytorch - API Bug
CVE-2024-5480
TensorFlow - Use-after-free
CVE-2021-41220
TensorFlow - OOB Write
CVE-2022-41894
TensorFlow - FP Exception
CVE-2023-27579
Snowflake - Cmd. Injection
CVE-2023-34230
Hadoop - ACL Violation
CVE-2023-26031
Pytorch - Malicious Pkg.
CVE-2022-30877
Spark - Cleartext Store
CVE-2019-10099
Kubernetes - Bug
CVE-2022-3172
BentoML - RCE
CVE-2024-2912
Kubernetes - API Bug
CVE-2023-1260
Libraries
OpenCL - Use-after-free
CVE-2023-4969
Py zlib - Mem Corrupt
CVE-2018-25032
Scipy - Heap Ovf.
CVE-2022-48560
Pyyaml - RCE
CVE-2021-4118
OneAPI - Library Bug
CVE-2024-21766
CuDNN - Use-after-free
CVE-2021-37652
SQLite - OOB Write
CVE-2020-35527
Mlnx OS - IPfilter config
CVE-2024-0101
Redis - Integer Ovf.
CVE-2023-41056
Py Urllib - Inp. Validation
CVE-2023-24329
Cuda - OOB Read
CVE-2023-25513
vGPU Drv - OOB Write
CVE-2023-31035
Firmware - Config Error
CVE-2023-31035
vGPU Drv - OOB Write
CVE-2023-31035
Torchserve - Directory Trvsl
CVE-2023-48299
attackers to convert non-executable memory regions into
malicious scripts. (2) Remote code execution (RCE) attacks
perform the same on a remote system and is even more
catastrophic. (3) Command injection attacks are able to
query secret datatypes by inserting a command. For instance,
victim database entries are deleted by inserting delete()
command in a Snowflake database. (4) The OOB write
vulnerability in the vGPU driver [48] flips device config-
uration enabling an attacker to perform unauthorized code
execution, leading to device hijack.
Privilege escalation The green boxes in table 1 requires
attackers to have a privileges system access. However, a non-
privileged attacker can mount privilege escalation attack to
become the root user of the system. The privilege escalation
vulnerabilities include: (1) Access control (ACL) violations
in software frameworks and packages pose significant risks.
Many of these frameworks, packages, or libraries include
kernel modules, allowing attackers to exploit ACL violations
or API bugs to gain privileged access. (2) Directory traversal
or the lack of input validation is exploited by attackers
with blackbox access to access privileged data structures.
(3) Server side request forgery (SSRF) is used by a remote
attacker to gain unauthorized system access and we found
one such CVE in Langchain [49].
4.2. Defenses
The complex software stack in a compound AI system
is riddled with vulnerabilities at all levels as discussed
in section 4.1. While many of the frameworks, libraries
and packages might have individual safety nets, it is clearly
insufficient to protect against different vulnerability classes.
Moreover, the active development and the sheer size of
the codebase makes it infeasible for formal verification
techniques [50] or even high-coverage fuzzing methods [51].
A key observation though is that, some vulnerabilities like
buffer overflow, use-after-free, and memory errors etc. can
be thwarted with existing defenses. However, certain other
attacks like victim co-location, input validation or instal-
lation of malicious package catalyze certain algorithmic
or hardware attacks. In this section, we propose defenses
against direct software vulnerabilities as well as mandate
certain software practices to prevent leveraging system soft-
ware in performing algorithmic and hardware attacks.
Software supply-chain defenses Protecting the software
supply-chain is a first-line defense against the listed vulner-
abilities. The Compound AI software stack incorporates nu-
merous dependencies sourced from a wide range of vendors.
Prior work [52] proposes user credential and role validation
to prevent package tampering.
The second challenge is the authentication of package
registry. The attacker registers several malicious packages
with similar names to trick the victim. Prior work [53]
employs administrative safeguards as well as remove unused
dependencies to protect against these attacks. Amalfi [54]
uses ML classifiers to test package reproducibility from
source code to automatically detect malicious packages.
Access control policies Declaration of variables with an
appropriate access modifier such as private, public
and protected as provided by languages like Python,
C++ and Java is necessary to avoid secret data leakage and
tampering due to improper access control policies. Secret
variables should always be declared as private to prevent
access from different class methods. Code review and in-
formation flow tracking compiler passes [55]–[57] can help
prevent secret data leakage from training datasets, model
parameters and knowledge vector database. Fine-grained
identity and access management policies (IAM) should also
be validated [58] for datasets, model and other resources.
Input queries and retrieved context should undergo input
validation to prevent privilege escalation attacks. Input vali-
dation should verify token lengths, detect malicious regular
expressions, and sanitize retrieval commands. Exhaustive
testing of the trained model eliminates unknown behavior
when presented with crafted inputs. Safeguards should be
placed at different compound AI components both on the
client and server side to prevent access control attacks.


---

Memory safety We discovered several CVEs for different
types of buffer overflow attacks, dangling pointers and use-
after-free errors. Illegal memory accesses lead to confiden-
tiality, integrity and availability concerns. While defenses
are proposed for these well-known problems, the deploy-
ment scale and the active development leads to these errors.
There is an urgent need to shift the software backend
from C,C++ to memory safe languages like Rust. The
software community is developing critical packages [59]
and linux OS [60] in Rust language to ensure memory
safety. Running compound AI systems in a sandbox environ-
ment [61]–[64] reduces the risk of privilege escalation and
DoS attacks, which are particularly catastrophic in cloud
deployments. Existing memory safety protections including
address-space-linear randomization (ASLR), stack canaries
and use-after-free protections should be enabled for all
production systems. Memory tagging techniques like CC,
Cheri [65] and Morpheus [66] isolate data from different
security domains and are implemented in latest Intel and
arm processors to deter memory safety errors.
Node resiliency and check-pointing Training of founda-
tional models take place in vast distributed systems with
hundreds of GPUs and terabytes of storage. Orchestration
frameworks are used for compute scheduling and efficient
data movement. This frameworks should be fault tolerant
and be able to deal with node crashes. For instance, orches-
tration frameworks can migrate computations away from
specific nodes [67] based on system’s health to prevent large
scale infrastructure failures. The ML model should be check-
pointed at regular and frequent intervals to ensure minimal
loss during a large scale failure. Moreover, efficient log
collection and forensic analysis is required for root causing
the failure. Omnilog [68] collects Linux audit logs efficiently
and ensure log integrity after system compromise. Recent
works have employed machine learning techniques to find
malicious attack signatures for faster attack detection.
4.3. Key Takeaways
Takeaway 1: Safeguarding the software supply chain:
The compound AI software stack contains a large number
of software packages from multiple vendors. This creates
a distributed attack surface enabling an attacker to inject a
malicious package or software backdoors to extract secret
data. Software supply chain defenses should validate the
developer, leverage packages from well-known sources to
ensure secret data confidentiality and integrity protection.
Takeaway 2: Design with type-safe languages: A ma-
jority of data leakage and privilege escalation attacks are a
result of improper access control policies and memory safety
errors. Memory- and type-safe languages like rust should be
used to prevent these attacks.
Takeaway 3: Software defenses for heterogeneous plat-
forms: Many software defenses (e.g. ASLR, stack canary)
found on CPU environments are crucial on platforms like
GPUs, ML accelerators [27] and even DPUs [69] since rise
in AI deployments have exposed these platforms to threat
models similar to CPU systems.
Takeaway 4: System wide software health monitors
Small errors in multiple software components can cause
a catastrophic system failure. Hence, system-wide software
monitors should be deployed in the orchestration layer to
monitor the health of each deployed node. Resource hogging
or access control violations should be detected proactively
to minimize system impact.
5. Hardware vulnerabilities and defenses
Beyond the algorithmic and software attacks, an at-
tacker can mount direct, side-channel and bit-flip attacks
in hardware. These attacks can be performed both during
training and query inference in a compound AI system.
We define direct attacks as those in which the attacker
gains unauthorized access to read or manipulate confidential
data directly from storage, memory, interconnect or on-
device buffers. A timing attack is a side-channel attack
where the attacker extracts victim secret data from execution
timing variation. An attacker can use hardware performance
monitors, or high-resolutions timers to extract fine-grained
victim execution timing. A power attack extracts power
signatures to infer victim execution. Bitflip and injection
attack tampers secret data. A bitflip attack is non-invasive,
while an injection attack requires hardware physical access.
In this section, we will first enlist different attacks
performed on ML systems to extract different assets in-
cluding training data privacy, model parameters and hyper-
parameters, and user inference input. Next, we will discuss
hardware defense mechanisms deployed to protect confi-
dentiality and integrity of ML execution, with a final key
takeaway section summarizing the main design trends and
their mapping to the attack vectors.
5.1. Attacks
We categorize existing hardware attacks into different
attack categories. It includes attacks on heterogeneous hard-
ware including CPUs, GPUs and ML accelerators. We cate-
gorize the hardware components into memory, interconnect
and compute components as shown in
table 2. Memory
attacks encapsulate data leakage and tampering in main
memory. Interconnect attacks cover leakage from mem-
ory bus and I/O interconnect. Compute attacks encompass
micro-architectural attack on on-chip memory, buffers and
processing units. The attacker can either perform hardware
attacks remotely (digital attacks) or require physical system
access (physical attacks).
Digital attacks include timing side-channels and resource
utilization attacks while physical attacks include power and
fault injection attacks that require device physical access to
snoop signals or tamper with execution.
Memory and storage attacks Memories are used to store
proprietary ML models and secret user data. CPUs, GPUs
and accelerators are typically connected to DDR rams, SD
rams or an HBM storage. Attackers target data stored in
these memory components in order to compromise its con-
fidentiality and integrity. Direct attacks dump secret data


---

Component
Attack Type
Channel
Asset
Breach
Memory
Boot attacks [70], [71]
Direct
Mv, I
C
Bank Conflict [72], [73]
Timing
Ma
C
NVleak [74]
Ma
C
Rowhammer [75]–[77]
Bitflip
Mv, I
I
Rambleed [78], [79]
Mv, I, T
C
PiM/PnM attacks [80]–[82]
Power
Mv, I
C
Laser attacks [83]–[85]
Injection
Mv, I
I
Interconnect
Bus hijack [86]–[88]
Direct
Mv, I, T
C,I
Access pattern [10], [89]–[92]
Ma
C
Perf. Counters [93]–[95]
Ma
C
Sparsity [96], [97]
Timing
Mv
C
Contention [98], [99]
Ma
C
Fingerprinting [93], [100], [101]
Ma
C
HW Trojan [102]
Bitflip
Mv, I, T
I
TDC with RO [103]
Power
Ma
C
Voltage Virus [104]
Injection
Mv, I
I
Compute
Spad use-after-free [11], [105]
Direct
Mv, I, T
C,I
Cache Attacks [39], [106]–[108]
Timing
Mv, T, I
I
Exec. Time [109]–[112]
Ma, Mv
I
HW Trojan [113]
Bitflip
Mv, T, I
I
Fingerprinting [114], [115]
Power
Ma
C
Laser [116]
Injection
Mv, T, I
I
TABLE 2. LIST OF ATTACKS IN DIFFERENT HARDWARE COMPONENTS. ASSET CLASSES INCLUDE MODEL WEIGHTS (Mv), MODEL
ARCHITECTURE (Ma), TRAINING DATA (T ) AND PRIVATE QUERY (I).
stored as plaintext from memory. Boot attacks exploit the
cell retention of volatile memories across reboots to leak
secret data, violating confidentiality of model parameters
(Mv), secret user inputs (I) and training data (T). Tim-
ing attacks retrieve model architecture (Ma) by recording
the timing difference between row buffer hits and misses.
NVLeak [74] attack leaks secret vector database knowledge
stored in persistent storage. Bitflip attacks like Rowham-
mer [21] and Rowpress [117] can flip model parameters
to reduce model performance. Many large models are re-
silient to bitflip attacks, especially for early layer bitflips.
However, these attacks can be used to tamper user input
queries leading to either mis-classification or model hallu-
cination. Rambleed attacks use rowhammer to leak secret
data from adjacent rows. This can also be used to infer
user queries, as well as targeted training data and model
parameters. Despite rowhammer mitigations [118] in latest
generations of memory, recent work [117] demonstrated
rowhammer in HBM memories widely used in latest GPUs.
Power attacks are demonstrated on processing-in-memory
(PiM) and processing-near-memory (PnM) devices, which
are gaining popularity due to data transfer minimization.
Specifically RRAM PiMs emit power signatures based on
layer architecture. PnM access pattern is also used to infer
confidential DNA sequence input. Finally, laser is used inject
faults in memory, which can poison training data samples
or tamper model parameters during inference.
Interconnect attacks The next attack surface is on the
memory bus and I/O interconnect. This is widely used to
data transfer between the compute units like CPUs, GPUs
and accelerators and memory and storage blocks like DRAM
and nvme drives. Direct attacks include bus hijack by either
connecting a malicious device over the PCIe or using a bus
monitor. Bus hijack attacks can be used to either read secret
data during transfer or perform a man-in-the-middle attack
to tamper input queries or ML models. The interconnect
is widely used across heterogeneous compute units in a
compound AI system, making it lucrative for attackers.
Hijacking the interconnect enables the attacker to control
the decisions taken by the LLM agent and emit malicious
response. Demand access pattern extracted from memory
bus is also used to infer model layer architecture. Finally,
several performance counters reveal read/write data volumes
to fingerprint service usage or layer connections in a ML
model. While, performance counters are mostly disabled in
production systems, CSPs can use them for analytics, lead-
ing to application and service fingerprinting attacks. Timing
attacks include leakage from data-driven optimizations like
model sparsity. Prior work [97] uses AXI bus monitors to re-
veal sparsity ratio from data volume. Bus contention [90] is
used to snoop network traffic, revealing model architecture.
Finally, bus utilization is used to fingerprint model layer
dimensions. Hardware Trojan tampers model parameters to
misclassify ML inference. Physical side-channels include
ring oscillators to snoop power consumption, which is used
as a proxy to infer model dimensions. These attacks reveal
model architecture, which is then used to perform member-
ship inference or model extraction attacks with white-box
assumption. Voltage viruses [104] can be used to tamper
with model inference in multi-tenant FPGA deployments.
Compute attacks On-chip microarchitectural sharing of
multiple tenants expose several attack vectors. Sesame [11]
observed several attacks for resource sharing in multi-tenant
accelerators. These include sharing of compute blocks and
use-after-free attacks in a spatially shared scratchpad. Timing
attacks include CPU and GPU caches. Cachetelepathy [39]
leveraged prime+probe and flush+reload attacks to leak ML
model architecture. Similar attacks were demonstrated in
GPU caches as well. Moreover, compute execution time
is inferred from EM emission [109] and from floating-
point unit [112] and used to fingerprint different layer types
and dimensions. These works also use novel algorithms to


---

efficiently reverse engineer the model architecture. Bitflip
attacks are used to tamper the bias buffer [113], which
leads to model mis-classification. Misclassification in the
LLM agent can lead to incorrect response and trigger in-
correct tools for query inference. Prior work [115] used
power channel and magnetic signals to fingerprint layers
by targeting the GEMM module. Finally, fault injection in
control queues can violate dependency queues in a DAE
design. This triggers model computation before the data is
ready in scratchpad leading to incorrect model response.
5.2. Defenses
Prior works has proposed several defense mechanisms to
protect secret data from the attacks discussed in section 5.1.
Some of the defenses target specific micro-architectural
components like caches, scratchpad and compute units,
while others strive to design isolated execution systems.
Memory and storage defenses Several prior defenses con-
sidered offchip memory and storage outside of their trust
boundary and proposed confidentiality and integrity protec-
tion. Direct attacks are thwarted by encrypting data in mem-
ory [119], [120] and storage [121], preventing attackers from
reading out plaintext secret. Other works [122], [123] intro-
duced data integrity primitives with authenticated encryption
blocks to prevent bitflip attacks. However, data integrity
protection incurs latency and memory bandwidth overheads.
Efforts to reduce the memory traffic overhead includes Mor-
phable counters [124] that optimize the memory traffic by
storing the message authentication code (MAC) in the ECC
storage, while MGX [125] eliminates the need for loading
replay counters by generating them in the processor. Other
works [118], [126]–[128] propose Rowhammer and other
bitflip mitigation in memory. Timing channels are prevented
by restructuring the data structures to prevent bank con-
flicts or defenses in memory controller [129]–[132]. Finally,
power side channels are defended with masking and hiding
techniques [133], while injection attacks can be prevented
with use of data integrity blocks.It is important to monitor
health of SSDs since these are used as storage buckets for
training data and knowledge databases. RL-Watchdog [134]
introduces a reinforcement learning technique to detect SSD
failures, while NVMensure [135] computes checksum to
prevent data poisoning attacks during ML training.
Interconnect defenses IO information (including address,
data, and timing) can leak information [89]. ORAM [136]
is a general way of protecting address and data from leak-
ing information by obfuscating the address and the data
content. However, its high performance overhead prevents
practical adoption. Practical secure accelerators perform en-
crypted data transfer to prevent direct attacks [125], [137].
Bus hijack attacks can be prevented by securing DMA
transfers with IOMMU [138] and RDMA protocol with
sRDMA [139]. Performance counters should be disabled
with hardware fuses in production systems to prevent mali-
cious hypervisors to snoop application data. Trusted execu-
tion environments like Intel TDX [119], Nvidia CC [140], or
Arm Trustzone [141] ensure that performance counters are
disabled during trusted execution. The timing channel with
IO [99] is not protected either by ORAM or encrypted data
transfer. There are currently no defenses to prevent sparsity
data volume attacks. However, structured sparsity deployed
in Nvidia Ampere GPUs [142] can reduce the data leakage
granularity. The contention and fingerprinting attacks can
be mitigated by memory traffic shaping [12], [143], [144].
This introduces high bandwidth utilization of ML acceler-
ators, which is optimized by obsidian [145]. Bitflip attacks
with hardware trojans can be prevented by protecting the
hardware supply chain [146]. Introducing hardware trojans
is easier in accelerator ASIC and FPGA implementations
making it pertinent to verify FPGA bitstreams and attest
accelerators to prevent bitflip due to malicious hardware.
Compute defenses The compute block defenses include on-
chip memory, buffers and the processing unit. On-chip mem-
ory like cache and scratchpad leaks confidential information
about the model or the input data via timing channel or
power side channel. Cache timing side-channels is a well-
studied problem with two types of defenses: Randomized
cache designs like ScatterCache [147] and others [148],
[149] insert secret data in random cache sets, while set
partitioning approaches like DAWG [150] and others [151],
[152] isolate cache ways. Both of these techniques can
defend against neural network-specific attacks like [39].
Sesame [11] proposed scratchpad and on-chip buffer par-
titioning for ML tenants to protect against timing attacks.
Apart from memory structures, logical units and gates
are also vulnerable to various physical and digital side-
channels since compute logic are often optimized for spe-
cialized operand data. These optimizations are exploited
to leak sensitive model weights and input data via timing
measurements and power usages. Power and EM variation
can be measured by direct external physical equipments,
while timing variations can be captured by both digital and
physical probes. Power side-channels can be defended by
specialized hardware unit that minimizes power variations
[153] or by obfuscating power signals using hardware masks
similar to Bomanet [154]. Luo [155] proposed power side-
channel mitigation combating voltage virus droop [104] in
multi-tenant accelerators by reducing clock frequency with
DVFS. Signal jamming techniques [156] are used to evade
EM based fingerprinting [157] attacks.
Several digital side-channels use performance counters
and high-resolution timers to exploit optimized data-paths
that leak model architecture or secret data values. Since
trusted execution environments [119], [140] are also suscep-
tible to such vulnerabilities, they disable performance coun-
ters during confidential computation to mitigate side-channel
analysis. Timing attacks can also be combated by elimi-
nating high-resolution timers in production systems [158]
or obfuscating timing measurement [159]. Constant-timing
hardware [160]–[162] provide microarchitectural mitigation
by enforcing timing invariability in ALUs and removing
operand data specific optimizations. Intel DOIT [163] and
ARM DIT [164] in recent processors provide in specific
instructions that enforce constant time executions and do not
involve any data driven micro-architectural optimizations.


---

5.3. Key Takeaways
Takeaway 1: Protecting the hardware supply chain:
Safeguarding the hardware supply chain is essential to pre-
vent insertion of Hardware Trojans to leak secrets. Since, a
lot of AI applications leverage multi-tenant FPGA accelera-
tors, authenticating the bitstream is critical in preventing this
powerful attack. Security verification of hardware micro-
architecture [165] is critical to prevent side-channel attacks.
Takeaway 2: Avoiding data-driven optimizations: Tim-
ing variations in data-driven optimizations leak secret data.
Data pruning in memory bus [89], sparse computation [97]
and cache data compression [166] can leak secret data. Such
features should be disabled during secure computation.
Takeaway 3: Optimizing hardware security primitives:
The challenge of high performance overheads in adopting
obfuscation techniques can be addressed by adoption of
domain-specific [125] and state-space exploration [145],
[167]. However, these optimizations should not result in new
side-channels. Emerging architectures like PiM and PnM
can help reduce memory traffic and data movement latency.
Takeaway 4: Creation of a hardware design template
Computation, data movement and storage are the important
primitives in a compound AI system. TEEs with side-
channel protections [11] can perform isolated execution,
link encryption in I/O bus protects data confidentiality and
reliable storage prevents data tampering. Each hardware
deployment should be follow a design template having a
combination TEE compute unit, encrypted switches and reli-
able storage blocks, similar to the recent Nvidia confidential
compute deployment [168].
6. Cross-Layer Attacks
Section 4 and 5 explore software and hardware vul-
nerabilities, along with available defenses for various threat
models within a compound AI system. Here, we focus on
cross-layer attacks, where adversaries exploit both software
and hardware vulnerabilities to breach data security. In sec-
tion 6.1, we discuss existing cross-layer attacks that com-
bine algorithmic, software, and hardware methods. We also
highlight the potential severity of these attacks in modern
compound AI systems, which are increasingly reliant on
heterogeneous hardware and diverse software stacks.
As AI ecosystems evolve, the scope of these attacks must
be reconsidered, especially since many traditional CPU-side
attacks are being adapted to violate confidentiality, integrity,
and availability in the AI/ML domain. Effective security
cannot be achieved in isolation – reliable protection requires
a holistic approach that encompasses both ML algorithms
and secure platform design, considering the entire system
for threat modeling and defenses.
6.1. Cross-layer attacks in AI model deployments
Systematizing a framework for existing proposed at-
tacks, across the the application stack allows us to envision
how algorithmic attacks can be combined with software and
EM/Power
Observation
Performance 
Counters
Model
Extraction 
Attack
(Sec. 6.1.1)
Snoop Victim
Behavior
Extract Model
Architecture (C)
Directed 
Model Query
Build 
Shadow Models
Model 
Weights (C)
Reconnaissance/
Resource Dev
Initial Access/
Execution
Defense Evasion/
Privilege Escalation 
Collection/ 
Exfiltration (Impact)
Critical Bit 
Exploration
Adjacent Row
Data Fill
Rowhammer
Bitflip
Misclassification
(I)
Laser Fault
Injection
Malicious Package
Insertion
Timing
Measurement
Victim Colocation
Misinformation
(I)
SQL Injection 
(RAG DB)
Directed 
Model Query
Access Malicious
Vector Entry
Train 
Shadow Models
Extract Model
Architecture (C)
Attack
Bitflip
Attack
(Sec. 6.1.2)
Timing
Attack
(Sec. 6.1.3)
Knowledge
Tampering
(Sec. 6.1.4)
Figure 4. Three attack cases which leverages cross-stack vulnerabilities
to mount powerful attacks. We map different attack techniques to the
MITRE framework.
hardware vulnerabilities to achieve higher efficacy. Many
system attacks, especially those targeting hardware physical
and digital channels, only protect part of the assets like
model architecture or model weights. On the other hand,
algorithmic attacks often make assumptions (e.g. whitebox
or greybox) that are only feasible after partial model infor-
mation extraction from system attacks.
Here we are presenting four cases that leverage both sys-
tem and algorithmic techniques to mount powerful attacks.
Each attack is mapped to MITRE techniques, as illustrated
in fig. 4, allowing for a clear classification of attack lifecy-
cles. Such a mapping aids system designers in understanding
the stages of an attack and selecting appropriate defense
mechanisms to mitigate these threats. We discuss more on
defense methodologies and quantifying attack techniques
in section 7.2.
6.1.1 Performing model extraction: An attacker with
hardware physical access can extract model weights using
coldboot attacks to directly read memory contents. However,
attaining physical access to MLaaS deployments is infeasi-
ble. The model extraction attacks in MLaaS threat models
comprise to two steps: (I) Extract model layer architecture
(filter matrix dimensions); (II) Train a duplicate model with
same accuracy. Digital attacks like Deepsniffer [93] and oth-
ers [89], [90] monitor hardware utilization to reveal model
architecture, while physical attacks like DeepEM [157] and
others [114] use EM and power channels.
Subsequently, an attacker can perform an algorithmic
attack with whitebox assumptions. The attacker creates a
number of shadow models and train them on the repeated
query response of the victim model. Ultimately, one of the
shadow models will achieve the same level of accuracy as
the victim model, resulting in a successful model extraction
attack. This attack requires only remote query access to the
victim model. This approach can also be used to perform
membership inference attacks with a different asset target.
While model extraction attacks target model parameter con-
fidentiality (Mv), membership inference declassifies training
data (T). In this example, we see how hardware attacks can


---

transform weaker threat model assumptions of algorithmic
attacks into a more realistic threat model.
6.1.2 Bitflip for model degradation: While bit-flip attacks
can be executed through various system attack methods,
their impact varies significantly depending on the targeted
bits. The effectiveness of such attacks can be amplified by
following these steps: (I) Identify the critical model bits
that misclassify a specific class or degrades model accuracy.
Proflip [169] and TBT [170], for instance explores the
sensitive bits in a ML model. (II) Mount a Deephammer [75]
attack to flip the specific bits for maximum impact. An
attacker with physical access can also perform Laser fault
injection [83] to flip critical model bits. This approach high-
lights how algorithmic attacks can serve as reconnaissance
tools, identifying critical bits to enhance the effectiveness
of conventional bit-flip attacks.
6.1.3 Covert channel for hardware timing attack: Hard-
ware timing attacks like layer fingerprinting [109], [112]
and cache side-channels [39], [106] are particularly effective
when the attacker knows the start and end points of each
layer’s execution. This helps eliminate noisy data collection
from these side-channels. An attacker can extract model
architecture with only remote digital access, making this
attack relevant in cloud MLaaS deployments. This attack
can be performed in two stages: (I) A malicious software
package can be inserted in the software supply chain to
trigger an interrupt at the compute start of each layer. (II)
This covert channel can be intercepted by an attacker to
reset or collect timing information for layer fingerprinting.
The supply-chain attack denoises the timing attack data col-
lection by the digital attacker for more precise fingerprinting.
Moreover, a compromised orchestration framework can aid
victim colocation exclusively with the attacker to eliminate
system noise from other processes.
6.1.4 Tamper knowledge database to spread misinforma-
tion: RAG models can generate recent content by retrieving
from an updated knowledge database. ConfusedPilot [37]
shows how an attacker can spread misinformation by tam-
pering the knowledge database. The key assumption is that
an attacker can add malicious entries in the knowledge
database. However, this might not be true for enterprise
databases with administrator gate-keeping. Software attack
can evade this assumption with the following attack flow:
(I) An SQL injection attack [171] can insert malicious
knowledge in the vector database. Such an attack was shown
on Langchain framework (listed in table 1) which is widely
used in designing RAG pipeline and can be launched by
an unprivileged attacker. (II) After tampering the database,
the ConfusedPilot algorithmic attack can be deployed to
tamper content generation integrity or RAG availability. This
attack exemplifies how a specific threat model assumption
in an algorithmic attack can be generalized with cross-layer
attacks. Mapping these attacks to the Mitre framework help
replace threat model assumptions in the reconnaissance and
resource development stages with system attacks.
6.2. Emerging cross-layer attacks on compound AI
systems
In this section, we will qualitatively discuss new cross-
layer attacks possible on the compound AI system. Specif-
ically, we showcase how an adversary can extract partial
information from different compound AI stages (shown
in fig. 2 to design an end-to-end attack. Carlini [16] al-
ready showcased a purely algorithmic attack where a LLM
model trained with differential privacy (DP) leaks training
data violating privacy when deployed as a component in a
compound AI system. This seminal work shows how a safe
training DP budget is violated, when a LLM is used as a
part of a larger system.
Generation accuracy degradation: Data poisoning and
other approaches are shown to degrade model accuracy or
cause misclassification. However, a compound AI system
includes a grounding block (shown in fig. 2) in query post-
processing to fact-check the generated content. This prevents
model hallucination and the effectiveness of isolated data
poisoning. An attacker with physical access can still gener-
ate a degraded response and bypass the grounding block to
perform an attack.
The reconnaissance step starts with finding the physical
address of the multiplexer logic in the MoE router. This
can be performed by dumping device memory contents with
memory safety vulnerabilities (use-after-free or OOB read)
or by a hardware boot attack [70]. The initial access stage
involves installing a malicious grounding block to bypass the
fact checking logic. Next, the attacker mounts a rowhammer
attack to alter the MoE router expert selection for a victim
query. This generates a degraded response which evades
fact-check with a malicious grounding component complet-
ing the attack. This attack requires hardware physical access,
but is able to use cross-layer attacks to emit a degraded
response despite query post-processing.
Leak private data from generated program snippet:
Compound AI tools like Github Copilot [28] are widely
used to generate program snippets. Tampering the generated
program is lucrative as it can be used to extract user private
data used as program inputs, manipulate the desired output
or crash a user system.
This attack starts by redirecting the LLM agent into
a malicious program generator. This can be performed by
modifying the function call address with a OOB write in
the LLM agent. The malicious program generator can add
covert channel attack widgets in the generated code. When
the victim executes the generated code snippet, it triggers
the covert channel enabling the attacker to leak secret data
with cache [35] and other hardware timing [172] attacks.
Leak model parameters with Hardware Trojan: Com-
pound AI system is composed of multiple proprietary LLMs.
We showcase the model extraction attack by an attacker with
physical access. The reconnaissance step includes insertion
of an FPGA accelerator in the orchestration pool with a
Hardware Trojan to extract model weights. The privileged
attacker hijacks the software orchestrator to redirect the
execution of the target model into the accelerator.


---

Once the target model is scheduled in the malicious ac-
celerator, the trojan extracts model parameters by snooping
on the memory interconnect hardware channel. This attack
can be generalized to leak any component in the compound
AI system, including the retrieval output, LLM agent model,
the MoE experts or the compliance and grounding LLMs.
Privilege escalation attack to control hardware: The
privilege escalation attack is showcased as a software attack
in section 4.1. However, the diverse software supply chain
in a compound AI stack makes it more compelling. The
ever-increasing use of packages and libraries make it more
prone to bugs and malicious package inclusions. This attack
is powerful as the attack only needs query access to perform
privilege escalation. SSRF attacks in Langchain [49] or ac-
cess control violations in Langflow [173] and Ollama [174]
increases the attacker capability. Mounting privilege escala-
tion attack in the initial access sets the stage for better con-
trol of the deployment platform. It enables a non-privileged
attacker to toggle performance counters leading to hardware
attacks or control the victim execution to colocate with the
attacker or trigger DoS attacks.
7. Discussion
In this SoK, we classify attacks on AI systems into three
categories: algorithmic, software, and hardware attacks. We
also demonstrate how cross-layer vulnerabilities can either
amplify certain attacks or enable a less capable adversary
to carry them out. In this section, we first highlight the key
takeaways from this exercise in section 7.1. These learning
help in designing a more holistic compound AI platform,
that is robust at every level of stack. Next, stress the need
of qualitatively and quantitatively analyze attack vectors
in section 7.2. Since, systems have a diverse threat model
assumption, understanding the severity of individual vul-
nerability is necessary to understand the severity of attacks
and work towards quantifiable defenses. Finally, we discuss
various open research challenges in designing robust AI
systems in section 7.3.
7.1. Key Takeaways
Takeaway 1: The potency of cross-layer attacks: The
vulnerabilities in algorithmic, software and hardware equip
an attacker with different attack widgets. These widgets can
be sequenced to launch an end-to-end attack on a compound
AI system with minimal threat model assumptions. Multiple
ownership of the hardware platforms and the software sup-
ply chain makes it challenging to propose a single defense.
Software and hardware defenses are needed at every stage
of the training and inference of compound AI pipelines.
Takeaway 2: The need for a holistic attack categoriza-
tion: Given the diverse asset and threat model categories
for isolated attacks, there is a need for a holistic attack
categorization. We propose using the Mitre Att&ck frame-
work to position different attacks based on the threat model,
the leaked asset and the overall impact. While isolated
attacks like few bitflips may be harmless in attacking a
billion parameter model, it can be lethal if paired with an
algorithmic attack to flip a few critical bits. A severity score
should be assigned to isolated attacks based on the threat
model, the type of leaked asset and the overall impact on a
large system like in compound AI.
Takeaway 3: Identifying the critical attack targets: The
reconnaissance step enables the attacker to identify critical
stack component that should be targeted for a specific secret
asset. For instance, knowledge databases and grounding
blocks are the critical components, if the attacker wants to
degrade response accuracy or spread misinformation. An at-
tacker with physical access should flip bits at the later stages,
as compound AI system is robust enough to correct early
stage bitflip in many cases. The LLM agent plays a crucial
role in determining the compound AI’s response pathway,
making it a high-value target for control-flow hijacking.
Targeted model extraction and membership inference attacks
needs to be directed at specific IPs. A malicious orchestrator
can enable an attacker to colocate with the target component
or deploy it in a specific node. These insights enable the
attacker to collect noise free data during exfiltration stages
to perform efficient attacks.
Takeaway 4: Re-evaluation of existing defense mech-
anisms: Many of the defense mechanisms are focused on
a specific security policy and are deployed for a specific
hardware platform. For instance, buffer overflow and mem-
ory safety protections are implemented in CPUs. However,
compound AI systems are deployed in a heterogeneous
hardware. Such protections should either be triaged to GPUs
and accelerators, or devices should come with a defense
capability metadata verified during attestation. This can help
the software orchestrator to schedule sensitive components
only to the secure systems. Moreover, supply chain defenses
are becoming super important and challenging, given the
dynamism of capability development in the compound AI
systems. Security policies of every software and hardware
components should be designed based on first principle.
7.2. Need for Quantitative and Qualitative Metric
The cybersecurity and software industries have utilized
quantification metrics, such as CVEs, to assess the severity
of attacks and vulnerabilities. While hardware vulnerabilities
lack this quantification, metrics like channel capacity and
leakage bit-rate have been proposed in the literature [175],
[176] to evaluate side and covert channels. Weaknesses in
both software and hardware are categorized under Com-
mon Weakness Enumeration (CWE) metrics, enabling the
community to identify and mitigate security violations be-
fore exploitation. However, a classification mechanism for
AI/ML attacks across the stack is currently lacking. Critical
vulnerabilities in the components of compound AI systems
can jeopardize the entire system’s security guarantees. Al-
though some groups are advocating for this issue [177], we
lack significant outcomes. Rapid emergence of AI inference
pipelines highlights the necessity of developing standardized
metrics to categorize and quantify attacks at each layer.


---

We also call for a severity scoring system based on the
sensitivity of targeted assets and the capabilities required
by potential attackers. For example, while both model pa-
rameters and architectures are proprietary, leaking model
parameters poses a greater sensitivity risk than model ar-
chitecture. Additionally, different types of hyperparameters
vary in their criticality regarding model accuracy, which
must be factored into severity assessments. Beyond asset
sensitivity, classifying threat models and attacker capabili-
ties, plays a crucial role in determining attack potency. For
instance, vulnerabilities exploitable by remote adversaries
have a broader attack ”blast radius” than those requiring
physical access. Similarly, an algorithmic attack with white-
box access is typically less potent than one requiring only
black-box access. This work, organizes existing attacks into
a recognized framework that aids in classifying AI vulnera-
bilities. Extending the framework with quantifiable measures
is an open research question we aim to address in future.
7.3. Building a Robust Compound AI System
Here we explore best practices for designing secure com-
pound AI systems that aim at cross layer vulnerabilities and
employ defenses at the algorithm, software, and hardware.
Cross-stack alignment of security requirements: Modern
AI pipelines handle sensitive data from multiple distrustful
entities, complicating security enforcement. Privacy policies
from end-users and security requirements from model own-
ers often lack clear alignment with software and hardware
layers, making it challenging to maintain consistent security
guarantees. Establishing clear trust relationships between
data owners and entities, along with specifying privacy
requirements in multi-tenant environments, is crucial for de-
signing robust AI systems. We identify the definition of trust
relationships and the creation of a security framework that
can effectively translate user policies into system guarantees
as key open research questions for future work.
Factoring DP budget in a compound AI system: Differ-
ential privacy (DP) [178] is a mathematical tool to quantify
the privacy budget. DP stochastic gradient descent [179]
is already used to train LLMs. However, the DP privacy
budget should account for other components in the com-
pound AI pipeline. The compositional nature of DP that the
total privacy budget equals the sum of privacy budget of
each component makes it convenient to quantify the privacy
for complex systems like compound AI system. DP-based
framework for quantifying privacy leakage and providing
guidance towards protecting layer-designs in a compound
AI systems is an open area for future studies.
Cross-layer IFC for compound AI: Information flow con-
trol (IFC) can help prevent data leakage in compound AI
systems by tagging confidential data in vector databases,
restricting sensitive information from reaching malicious
entities. Prior work has applied IFC to control expert access
in MoE models [180], and this approach can be extended to
compound AI systems. Enforcing IFC early in the pipeline
limits data leakage, while memory safety measures protect
against access control evasion and code injection. Metadata
like ownership and permissions on database entries can
enable fine-grain access control for sensitive data. Current
IFC methods focus on algorithms but overlook system-level
attacks. Cross-layer IFC, including hardware and software
[12], [181], [182] and full-system verification [183], offers
stronger security and is a promising direction for AI security.
Private Attested AI Services: Recent AI service offerings
Apple’s Private Cloud Compute (PCC) [184] and Edgeless
System’s Continuum AI [185] start a trend to place AI ser-
vices into a highly confined environment. In addition, these
systems offer users attestation evidence of the environment
which increases trust into these systems. Confidential com-
puting (CC) like Intel TDX [119] provides the foundation to
provide this evidence to remote parties and in combination
with trusted supply chains [52] can further strengthen the
trust in the entire deployment. CC furthermore reduces the
reliance on a trustworthy infrastructure provider, when the
trusted execution environment is implemented by a 3rd party
(unlike Apple’s PCC).
Identifying critical model parameters: Recent studies
[126], [169], [170] have demonstrated that some ML model
parameters are more critical than others. For instance, mul-
tiplexer bits in a MoE router or bits in a RAG indexing
algorithm can significantly increase misclassification risks
in a compound AI system. Similar analyses are needed for
other components, including LLM agents, to identify key
parameters. Quantifying critical parameters is essential for
designing defense mechanisms and differential privacy bud-
gets. Such a study should also include a sensitivity analysis
of random bit flips to assess their impact on model accuracy,
helping specify toleration threshold for deployments
8. Conclusion
This SoK systemizes the software and hardware vulnera-
bilities to forecast cross-layer vulnerabilities in a compound
AI stack. While existing attacks and defenses have diverse
threat models, we strive to systemize them using a well-
known Mitre Att&ck framework. Arranging attack widgets
according to the assumed threat model and target assets help
clarify the flow of an attack sequence. It further sets the
stage for quantitatively scoring the potency of different vul-
nerabilities. This paper highlights the risk of system attacks
in the software and hardware of machine learning systems.
This SoK lays the foundation for future advancements in
both attack and defense strategies, expanding focus beyond
algorithmic attacks to include vulnerabilities across software
and hardware stack layers.
9. Acknowledgment
We thank Carlos Rozas, Mona Vij, Cory Cornelius, Scott
Constable, Mic Bowman, Nageen Himayat, Jose Vicarte,
Marius Arvinte, Fangfei Liu, Sebastian Szyller and other
Intel SPR team members for the regular discussions and
valuable feedback. This work was supported in part by ACE,
one of the seven centers in JUMP 2.0, a Semiconductor Re-
search Corporation (SRC) program sponsored by DARPA.


---

References
[1]
ChatGPT, “Chatgpt.” https://chatgpt.com/.
[2]
Gemini, “Gemini.” https://gemini.google.com/app.
[3]
Copilot, “Copilot.” https://copilot.microsoft.com/.
[4]
Tesla, “Autopilot and full self-driving (supervised) — tesla support.”
https://www.tesla.com/support/autopilot.
[5]
Textract, “Ocr software, data extraction tool - amazon textract - aws.”
https://aws.amazon.com/textract/.
[6]
R. Shokri, M. Stronati, C. Song, and V. Shmatikov, “Membership
inference attacks against machine learning models,” in 2017 IEEE
symposium on security and privacy (SP), pp. 3–18, IEEE, 2017.
[7]
F. Tram`er, F. Zhang, A. Juels, M. K. Reiter, and T. Ristenpart,
“Stealing machine learning models via prediction {APIs},” in 25th
USENIX security symposium (USENIX Security 16), pp. 601–618,
2016.
[8]
S. Milli, L. Schmidt, A. D. Dragan, and M. Hardt, “Model recon-
struction from model explanations,” in Proceedings of the Confer-
ence on Fairness, Accountability, and Transparency, pp. 1–9, 2019.
[9]
Z. Tian, L. Cui, J. Liang, and S. Yu, “A comprehensive survey on
poisoning attacks and countermeasures in machine learning,” ACM
Computing Surveys, vol. 55, no. 8, pp. 1–35, 2022.
[10]
S. Chandrasekar, S.-K. Lam, and S. Thambipillai, “Dnn model theft
through trojan side-channel on edge fpga accelerator,” in Interna-
tional Symposium on Applied Reconfigurable Computing, pp. 146–
158, Springer, 2023.
[11]
S. Banerjee, P. Ramrakhyani, S. Wei, and M. Tiwari, “Sesame:
Software defined enclaves to secure inference accelerators with
multi-tenant execution,” arXiv preprint arXiv:2007.06751, 2020.
[12]
S. Banerjee, S. Wei, P. Ramrakhyani, and M. Tiwari, “Triton:
Software-defined threat model for secure multi-tenant ml inference
accelerators,” in Proceedings of the 12th International Workshop
on Hardware and Architectural Support for Security and Privacy,
pp. 19–28, 2023.
[13]
M. Juuti, S. Szyller, S. Marchal, and N. Asokan, “Prada: protecting
against dnn model stealing attacks,” in 2019 IEEE European Sym-
posium on Security and Privacy (EuroS&P), pp. 512–527, IEEE,
2019.
[14]
L. Bourtoule, V. Chandrasekaran, C. A. Choquette-Choo, H. Jia,
A. Travers, B. Zhang, D. Lie, and N. Papernot, “Machine un-
learning,” in 2021 IEEE Symposium on Security and Privacy (SP),
pp. 141–159, IEEE, 2021.
[15]
E. Borgnia, V. Cherepanova, L. Fowl, A. Ghiasi, J. Geiping,
M. Goldblum, T. Goldstein, and A. Gupta, “Strong data augmenta-
tion sanitizes poisoning and backdoor attacks without an accuracy
tradeoff,” in ICASSP 2021-2021 IEEE International Conference on
Acoustics, Speech and Signal Processing (ICASSP), pp. 3855–3859,
IEEE, 2021.
[16]
E. Debenedetti, G. Severi, N. Carlini, C. A. Choquette-Choo,
M. Jagielski, M. Nasr, E. Wallace, and F. Tram`er, “Privacy side
channels in machine learning systems,” in 33rd USENIX Security
Symposium (USENIX Security 24), pp. 6861–6848, 2024.
[17]
M. Zaharia, O. Khattab, L. Chen, J. Q. Davis, H. Miller, C. Potts,
J. Zou, M. Carbin, J. Frankle, N. Rao, and A. Ghodsi, “The shift
from models to compound ai systems.” https://bair.berkeley.edu/bl
og/2024/02/18/compound-ai-systems/, 2024.
[18]
Langchain, “Langchain framework.” https://www.langchain.com/.
[19]
pyTorch, “Pytorch.” https://pytorch.org/.
[20]
Nvidia, “Cuda® deep neural network library.” https://developer.nv
idia.com/cudnn.
[21]
O. Mutlu and J. S. Kim, “Rowhammer: A retrospective,” IEEE
Transactions on Computer-Aided Design of Integrated Circuits and
Systems, vol. 39, no. 8, pp. 1555–1571, 2019.
[22]
V. Hartmann, A. Suri, V. Bindschaedler, D. Evans, S. Tople, and
R. West, “Sok: Memorization in general-purpose large language
models,” arXiv preprint arXiv:2310.18362, 2023.
[23]
N. Papernot, P. McDaniel, A. Sinha, and M. P. Wellman, “Sok:
Security and privacy in machine learning,” in 2018 IEEE European
symposium on security and privacy (EuroS&P), pp. 399–414, IEEE,
2018.
[24]
A. Dionysiou and E. Athanasopoulos, “Sok: Membership inference
is harder than previously thought,” Proceedings on Privacy Enhanc-
ing Technologies, 2023.
[25]
S. V. Dibbo, “Sok: Model inversion attack landscape: Taxonomy,
challenges, and future roadmap,” in 2023 IEEE 36th Computer
Security Foundations Symposium (CSF), pp. 439–456, IEEE, 2023.
[26]
Mitre, “Mitre attack framework.” https://attack.mitre.org/.
[27]
N. P. Jouppi, C. Young, N. Patil, D. Patterson, G. Agrawal, R. Bajwa,
S. Bates, S. Bhatia, N. Boden, A. Borchers, et al., “In-datacenter
performance analysis of a tensor processing unit,” in Proceedings of
the 44th annual international symposium on computer architecture,
pp. 1–12, 2017.
[28]
Github, “Github copilot.” https://github.com/features/copilot.
[29]
Amazon, “Amazon q developer.” https://aws.amazon.com/q/develop
er/.
[30]
Mistral, “Mistral ai.” https://mistral.ai/news/mixtral-of-experts/.
[31]
M. Ali and S. Khan, “Clip-decoder: Zeroshot multilabel classifica-
tion using multimodal clip aligned representations,” in Proceedings
of the IEEE/CVF International Conference on Computer Vision,
pp. 4675–4679, 2023.
[32]
B. E. Strom, A. Applebaum, D. P. Miller, K. C. Nickels, A. G. Pen-
nington, and C. B. Thomas, “Mitre att&ck: Design and philosophy,”
in Technical report, The MITRE Corporation, 2018.
[33]
Z. N. Zhao, A. Morrison, C. W. Fletcher, and J. Torrellas, “Ev-
erywhere all at once: Co-location attacks on public cloud faas,” in
Proceedings of the 29th ACM International Conference on Architec-
tural Support for Programming Languages and Operating Systems,
Volume 1, ASPLOS ’24, (New York, NY, USA), p. 133–149, Asso-
ciation for Computing Machinery, 2024.
[34]
P. Vila, B. K¨opf, and J. F. Morales, “Theory and practice of finding
eviction sets,” in 2019 IEEE Symposium on Security and Privacy
(SP), pp. 39–54, IEEE, 2019.
[35]
Y. Yarom and K. Falkner, “Flush+ reload: A high resolution, low
noise, l3 cache side-channel attack,” in 23rd USENIX security sym-
posium (USENIX security 14), pp. 719–732, 2014.
[36]
C. Percival, “Cache missing for fun and profit,” 2005.
[37]
A. RoyChowdhury, M. Luo, P. Sahu, S. Banerjee, and M. Tiwari,
“Confusedpilot: Confused deputy risks in rag-based llms,” 2024.
[38]
W. Hua, Z. Zhang, and G. E. Suh, “Reverse engineering convo-
lutional neural networks through side-channel information leaks,”
in Proceedings of the 55th Annual Design Automation Conference,
pp. 1–6, 2018.
[39]
M. Yan, C. W. Fletcher, and J. Torrellas, “Cache telepathy: Lever-
aging shared resource attacks to learn dnn architectures,” in 29th
USENIX Security Symposium (USENIX Security 20), pp. 2003–2020,
2020.
[40]
Huggingface, “Hugging face.” https://huggingface.co/.
[41]
Google, “Google tensorflow.” https://www.tensorflow.org/.
[42]
Apache, “Apache spark.” https://spark.apache.org/.
[43]
Apache, “Apache hadoop.” https://hadoop.apache.org/.
[44]
Snowflake, “Snowflake.” https://www.snowflake.com/en/.
[45]
BentoML, “Bentoml.” https://www.bentoml.com/.
[46]
Kubernetes, “Kubernetes.” https://kubernetes.io/.


---

[47]
Pyyaml, “Pyyaml package.” https://pypi.org/project/PyYAML/.
[48]
Mitre, “Cve-2023-31035.” https://cve.mitre.org/cgi-bin/cvename.cgi
?name=CVE-2023-31035, 2023.
[49]
Mitre, “Cve-2024-3095.” https://cve.mitre.org/cgi-bin/cvename.cgi
?name=CVE-2024-3095, 2024.
[50]
O. Hasan and S. Tahar, “Formal verification methods,” in Encyclope-
dia of Information Science and Technology, Third Edition, pp. 7162–
7170, IGI global, 2015.
[51]
K. Kim, D. R. Jeong, C. H. Kim, Y. Jang, I. Shin, and B. Lee, “Hfl:
Hybrid fuzzing on the linux kernel.,” in NDSS, 2020.
[52]
E. Abu Ishgair, M. S. Melara, and S. Torres-Arias, “Sok: A defense-
oriented evaluation of software supply chain security,” arXiv e-
prints, pp. arXiv–2405, 2024.
[53]
P. Ladisa, H. Plate, M. Martinez, and O. Barais, “Sok: Taxonomy
of attacks on open-source software supply chains,” in 2023 IEEE
Symposium on Security and Privacy (SP), pp. 1509–1526, IEEE,
2023.
[54]
A. Sejfia and M. Sch¨afer, “Practical automated detection of ma-
licious npm packages,” in Proceedings of the 44th International
Conference on Software Engineering, pp. 1681–1692, 2022.
[55]
T. Runge, M. Servetto, A. Potanin, and I. Schaefer, “Immutability
and encapsulation for sound oo information flow control,” ACM
Transactions on Programming Languages and Systems, vol. 45,
no. 1, pp. 1–35, 2023.
[56]
M. Dalton, H. Kannan, and C. Kozyrakis, “Raksha: a flexible
information flow architecture for software security,” ACM SIGARCH
Computer Architecture News, vol. 35, no. 2, pp. 482–493, 2007.
[57]
W. Crichton, M. Patrignani, M. Agrawala, and P. Hanrahan, “Mod-
ular information flow through ownership,” in Proceedings of the
43rd ACM SIGPLAN International Conference on Programming
Language Design and Implementation, pp. 1–14, 2022.
[58]
L. Wutschitz, B. K¨opf, A. Paverd, S. Rajmohan, A. Salem, S. Tople,
S. Zanella-B´eguelin, M. Xia, and V. R¨uhle, “Rethinking privacy
in machine learning pipelines from an information flow control
perspective,” 2023.
[59]
“Rust ai engine.” https://rust-ml.github.io/book/.
[60]
S. K. Panter and N. U. Eisty, “Rusty linux: Advances in rust for
linux kernel development,” arXiv preprint arXiv:2407.18431, 2024.
[61]
A. Vahldiek-Oberwagner, E. Elnikety, N. O. Duarte, M. Samm-
ler, P. Druschel, and D. Garg, “Erim: Secure, efficient in-process
isolation with memory protection keys,” in 28th USENIX Security
Symposium, 2019.
[62]
A. Bhattacharyya, F. Hofhammer, Y. Li, S. Gupta, A. Sanchez,
B. Falsafi, and M. Payer, “Securecells: A secure compartmentalized
architecture,” in 2023 IEEE Symposium on Security and Privacy
(SP), 2023.
[63]
S. Narayan, C. Disselkoen, T. Garfinkel, N. Froyd, E. Rahm,
S. Lerner, H. Shacham, and D. Stefan, “Retrofitting fine grain isola-
tion in the firefox renderer,” in 29th USENIX Security Symposium,
2020.
[64]
S. Narayan, T. Garfinkel, M. Taram, J. Rudek, D. Moghimi, E. John-
son, C. Fallin, A. Vahldiek-Oberwagner, M. LeMay, R. Sahita,
D. Tullsen, , and D. Stefan, “Going beyond the limits of sfi:
Flexible and secure hardware-assisted in-process isolation with hfi,”
in Proceedings of the Conference on Architectural Support for
Programming Languages and Operating Systems (ASPLOS), 2023.
[65]
R. N. Watson, J. Woodruff, P. G. Neumann, S. W. Moore, J. An-
derson, D. Chisnall, N. Dave, B. Davis, K. Gudka, B. Laurie, S. J.
Murdoch, R. Norton, M. Roe, S. Son, and M. Vadera, “Cheri: A
hybrid capability-system architecture for scalable software compart-
mentalization,” in 2015 IEEE Symposium on Security and Privacy,
pp. 20–37, 2015.
[66]
M. Gallagher, L. Biernacki, S. Chen, Z. B. Aweke, S. F. Yitbarek,
M. T. Aga, A. Harris, Z. Xu, B. Kasikci, V. Bertacco, S. Malik,
M. Tiwari, and T. Austin, “Morpheus: A vulnerability-tolerant secure
architecture based on ensembles of moving target defenses with
churn,” in Proceedings of the Twenty-Fourth International Confer-
ence on Architectural Support for Programming Languages and Op-
erating Systems, ASPLOS ’19, (New York, NY, USA), p. 469–484,
Association for Computing Machinery, 2019.
[67]
S. Singh, C. H. Muntean, and S. Gupta, “Boosting microservice
resilience: An evaluation of istio’s impact on kubernetes clusters
under chaos,” in 2024 9th International Conference on Fog and
Mobile Edge Computing (FMEC), pp. 245–252, IEEE, 2024.
[68]
V. Gandhi, S. Banerjee, A. Agrawal, A. Ahmad, S. Lee, and
M. Peinado, “Rethinking system audit architectures for high event
coverage and synchronous log availability,” in 32nd USENIX Secu-
rity Symposium (USENIX Security 23), pp. 391–408, 2023.
[69]
Nvidia, “Nvidia bluefield dpu.” https://www.nvidia.com/en-us/netw
orking/products/data-processing-unit/.
[70]
Y.-S. Won, J.-Y. Park, D.-G. Han, and S. Bhasin, “Practical cold
boot attack on iot device-case study on raspberry pi,” in 2020 IEEE
International Symposium on the Physical and Failure Analysis of
Integrated Circuits (IPFA), pp. 1–4, IEEE, 2020.
[71]
Y. Jiang, S. Wang, R. Figueiredo, and Y. Jin, “Warm-boot attack
on modern drams,” in 2023 Design, Automation & Test in Europe
Conference & Exhibition (DATE), pp. 1–2, IEEE, 2023.
[72]
P. Pessl, D. Gruss, C. Maurice, M. Schwarz, and S. Mangard,
“Drama: Exploiting dram addressing for cross-cpu attacks,” in 25th
USENIX security symposium (USENIX security 16), pp. 565–581,
2016.
[73]
V. van der Veen and B. Gras, “Dramaqueen: Revisiting side channels
in dram,” 2023.
[74]
Z. Wang, M. Taram, D. Moghimi, S. Swanson, D. Tullsen, and
J. Zhao, “Nvleak:off-chip side-channel attacks via non-volatile mem-
ory systems,” in 32nd USENIX Security Symposium (USENIX Secu-
rity 23), pp. 6771–6788, 2023.
[75]
F. Yao, A. S. Rakin, and D. Fan, “Deephammer: Depleting the
intelligence of deep neural networks through targeted chain of bit
flips,” in 29th USENIX Security Symposium (USENIX Security 20),
pp. 1463–1480, 2020.
[76]
S. Li, X. Wang, M. Xue, H. Zhu, Z. Zhang, Y. Gao, W. Wu, and
X. S. Shen, “Yes, one-bit-flip matters! universal dnn model inference
depletion with runtime code fault injection,” in Proceedings of the
33th USENIX Security Symposium, 2024.
[77]
A. S. Rakin, Z. He, and D. Fan, “Bit-flip attack: Crushing neural net-
work with progressive bit search,” in Proceedings of the IEEE/CVF
International Conference on Computer Vision, pp. 1211–1220, 2019.
[78]
A. Kwong, D. Genkin, D. Gruss, and Y. Yarom, “Rambleed: Reading
bits in memory without accessing them,” in 2020 IEEE Symposium
on Security and Privacy (SP), pp. 695–711, IEEE, 2020.
[79]
A. S. Rakin, M. H. I. Chowdhuryy, F. Yao, and D. Fan, “Deepsteal:
Advanced model extractions leveraging efficient weight stealing in
memories,” in 2022 IEEE symposium on security and privacy (SP),
pp. 1157–1174, IEEE, 2022.
[80]
Z. Wang, F.-h. Meng, Y. Park, J. K. Eshraghian, and W. D. Lu, “Side-
channel attack analysis on in-memory computing architectures,”
IEEE Transactions on Emerging Topics in Computing, vol. 12, no. 1,
pp. 109–121, 2023.
[81]
Z. Wang, Y. Wu, Y. Park, S. Yoo, X. Wang, J. K. Eshraghian,
and W. D. Lu, “Powergan: A machine learning approach for power
side-channel attack on compute-in-memory accelerators,” Advanced
Intelligent Systems, vol. 5, no. 12, p. 2300313, 2023.
[82]
K.
Kanellopoulos,
F.
Bostanci,
A.
Olgun,
A.
G.
Yaglikci,
I. E. Yuksel, N. M. Ghiasi, Z. Bingol, M. Sadrosadati, and
O. Mutlu, “Amplifying main memory-based timing covert and side
channels using processing-in-memory operations,” arXiv preprint
arXiv:2404.11284, 2024.


---

[83]
Y. Liu, L. Wei, B. Luo, and Q. Xu, “Fault injection attack on deep
neural network,” in 2017 IEEE/ACM International Conference on
Computer-Aided Design (ICCAD), pp. 131–138, IEEE, 2017.
[84]
G. Li, S. K. S. Hari, M. Sullivan, T. Tsai, K. Pattabiraman,
J. Emer, and S. W. Keckler, “Understanding error propagation in
deep learning neural network (dnn) accelerators and applications,” in
Proceedings of the International Conference for High Performance
Computing, Networking, Storage and Analysis, pp. 1–12, 2017.
[85]
N. Narayanan, Z. Chen, B. Fang, G. Li, K. Pattabiraman, and
N. Debardeleben, “Fault injection for tensorflow applications,” IEEE
Transactions on Dependable and Secure Computing, vol. 20, no. 4,
pp. 2677–2695, 2022.
[86]
ufrisk, “pcileech.” https://github.com/ufrisk/pcileech, 2017.
[87]
A. T. Markettos, C. Rothwell, B. F. Gutstein, A. Pearce, P. G.
Neumann, S. W. Moore, and R. N. M. Watson, “Thunderclap:
Exploring vulnerabilities in operating system iommu protection via
dma from untrustworthy peripherals,” in Proceedings 2019 Network
and Distributed System Security Symposium, NDSS 2019, Internet
Society, 2019.
[88]
S. Huang, X. Peng, H. Jiang, Y. Luo, and S. Yu, “New security
challenges on machine learning inference engine: Chip cloning and
model reverse engineering,” arXiv preprint arXiv:2003.09739, 2020.
[89]
W. Hua, Z. Zhang, and G. E. Suh, “Reverse engineering convo-
lutional neural networks through side-channel information leaks,”
in Proceedings of the 55th Annual Design Automation Conference,
pp. 1–6, 2018.
[90]
S. Banerjee, S. Wei, P. Ramrakhyani, and M. Tiwari, “Bandwidth
utilization side-channel on ml inference accelerators,” arXiv preprint
arXiv:2110.07157, 2021.
[91]
M. Chen, “Hmtt.” https://asg.ict.ac.cn/hmtt/, 2019.
[92]
Y. Zhu, Y. Cheng, H. Zhou, and Y. Lu, “Hermes attack: Steal dnn
models with lossless inference accuracy,” in 30th USENIX Security
Symposium (USENIX Security 21), 2021.
[93]
X. Hu, L. Liang, S. Li, L. Deng, P. Zuo, Y. Ji, X. Xie, Y. Ding,
C. Liu, T. Sherwood, et al., “Deepsniffer: A dnn model extraction
framework based on learning architectural hints,” in Proceedings of
the Twenty-Fifth International Conference on Architectural Support
for Programming Languages and Operating Systems, pp. 385–399,
2020.
[94]
H. Naghibijouybari, A. Neupane, Z. Qian, and N. Abu-Ghazaleh,
“Rendered insecure: Gpu side channel attacks are practical,” in
Proceedings of the 2018 ACM SIGSAC conference on computer and
communications security, pp. 2139–2153, 2018.
[95]
J. Wei, Y. Zhang, Z. Zhou, Z. Li, and M. A. Al Faruque, “Leaky
dnn: Stealing deep-learning model secret with gpu context-switching
side-channel,” in 2020 50th Annual IEEE/IFIP International Con-
ference on Dependable Systems and Networks (DSN), pp. 125–137,
IEEE, 2020.
[96]
D. Yang, P. J. Nair, and M. Lis, “Huffduff: Stealing pruned dnns
from sparse accelerators,” in Proceedings of the 28th ACM In-
ternational Conference on Architectural Support for Programming
Languages and Operating Systems, Volume 2, pp. 385–399, 2023.
[97]
S. Krithivasan, S. Sen, and A. Raghunathan, “Sparsity turns adver-
sarial: Energy and latency attacks on deep neural networks,” IEEE
Transactions on Computer-Aided Design of Integrated Circuits and
Systems, vol. 39, no. 11, pp. 4129–4141, 2020.
[98]
Y. Zhang, R. Nazaraliyev, S. B. Dutta, N. Abu-Ghazaleh, A. Mar-
quez, and K. Barker, “Beyond the bridge: Contention-based covert
and side channel attacks on multi-gpu interconnect,” arXiv preprint
arXiv:2404.03877, 2024.
[99]
M. Tan, J. Wan, Z. Zhou, and Z. Li, “Invisible probe: Timing attacks
with pcie congestion side-channel,” in 2021 IEEE Symposium on
Security and Privacy (SP), pp. 322–338, IEEE, 2021.
[100] V. Duddu, D. Samanta, D. V. Rao, and V. E. Balas, “Steal-
ing neural networks via timing side channels,” arXiv preprint
arXiv:1812.11720, 2018.
[101] Y. Sun, G. Jiang, X. Liu, P. He, and S.-K. Lam, “Layer sequence
extraction of optimized dnns using side-channel information leaks,”
IEEE Transactions on Computer-Aided Design of Integrated Circuits
and Systems, 2024.
[102] X. Hu, Y. Zhao, L. Deng, L. Liang, P. Zuo, J. Ye, Y. Lin, and Y. Xie,
“Practical attacks on deep neural networks by memory trojaning,”
IEEE Transactions on Computer-Aided Design of Integrated Circuits
and Systems, vol. 40, no. 6, pp. 1230–1243, 2020.
[103] S. Tian, S. Moini, A. Wolnikowski, D. Holcomb, R. Tessier, and
J. Szefer, “Remote power attacks on the versatile tensor accelerator
in multi-tenant fpgas,” in 2021 IEEE 29th Annual International
Symposium on Field-Programmable Custom Computing Machines
(FCCM), pp. 242–246, IEEE, 2021.
[104] S. Majumdar and R. Teodorescu, “Voltage noise-based adversarial
attacks on machine learning inference in multi-tenant fpga accelera-
tors,” in 2024 IEEE International Symposium on Hardware Oriented
Security and Trust (HOST), pp. 80–85, IEEE, 2024.
[105] S.-O. Park, O. Kwon, Y. Kim, S. K. Cha, and H. Yoon, “Mind control
attack: Undermining deep learning with gpu memory exploitation,”
Computers & Security, vol. 102, p. 102115, 2021.
[106] S. Hong, M. Davinroy, Y. Kaya, S. N. Locke, I. Rackow, K. Kulda,
D. Dachman-Soled, and T. Dumitras¸, “Security analysis of deep
neural networks operating in the presence of cache side-channel
attacks,” arXiv preprint arXiv:1810.03487, 2018.
[107] Y. Liu and A. Srivastava, “Ganred: Gan-based reverse engineer-
ing of dnns via cache side-channel,” in Proceedings of the 2020
ACM SIGSAC Conference on Cloud Computing Security Workshop,
pp. 41–52, 2020.
[108] S. B. Dutta, H. Naghibijouybari, A. Gupta, N. Abu-Ghazaleh,
A. Marquez, and K. Barker, “Spy in the gpu-box: Covert and side
channel attacks on multi-gpu systems,” in Proceedings of the 50th
Annual International Symposium on Computer Architecture, pp. 1–
13, 2023.
[109] L. Batina, S. Bhasin, D. Jap, and S. Picek, “Csinn: Reverse engi-
neering of neural network architectures through electromagnetic side
channel,” in 28th USENIX Security Symposium (USENIX Security
19), pp. 515–532, 2019.
[110] G. Takatoi, T. Sugawara, K. Sakiyama, and Y. Li, “Simple electro-
magnetic analysis against activation functions of deep neural net-
works,” in Applied Cryptography and Network Security Workshops:
ACNS 2020 Satellite Workshops, AIBlock, AIHWS, AIoTS, Cloud
S&P, SCI, SecMT, and SiMLA, Rome, Italy, October 19–22, 2020,
Proceedings 18, pp. 181–197, Springer, 2020.
[111] P. Horvath, L. Chmielewski, L. Weissbart, L. Batina, and Y. Yarom,
“Barracuda: Bringing electromagnetic side channel into play to steal
the weights of neural networks from nvidia gpus,” arXiv preprint
arXiv:2312.07783, 2023.
[112] G. Dong, P. Wang, P. Chen, R. Gu, and H. Hu, “Floating-point
multiplication timing attack on deep neural network,” in 2019 IEEE
International Conference on Smart Internet of Things (SmartIoT),
pp. 155–161, IEEE, 2019.
[113] P. Li and R. Hou, “Int-monitor: a model triggered hardware trojan in
deep learning accelerators,” The Journal of Supercomputing, vol. 79,
no. 3, pp. 3095–3111, 2023.
[114] Y. Xiang, Z. Chen, Z. Chen, Z. Fang, H. Hao, J. Chen, Y. Liu,
Z. Wu, Q. Xuan, and X. Yang, “Open dnn box by power side-
channel attack,” IEEE Transactions on Circuits and Systems II:
Express Briefs, vol. 67, no. 11, pp. 2717–2721, 2020.
[115] M. M´endez Real and R. Salvador, “Physical side-channel attacks on
embedded neural networks: A survey,” Applied Sciences, vol. 11,
no. 15, p. 6790, 2021.


---

[116] Y. Liu, L. Wei, B. Luo, and Q. Xu, “Fault injection attack on deep
neural network,” in 2017 IEEE/ACM International Conference on
Computer-Aided Design (ICCAD), pp. 131–138, IEEE, 2017.
[117] H. Luo, A. Olgun, A. G. Ya˘glıkc¸ı, Y. C. Tu˘grul, S. Rhyner, M. B.
Cavlak, J. Lindegger, M. Sadrosadati, and O. Mutlu, “Rowpress:
Amplifying read disturbance in modern dram chips,” in Proceedings
of the 50th Annual International Symposium on Computer Architec-
ture, pp. 1–18, 2023.
[118] A. Saxena, G. Saileshwar, P. J. Nair, and M. Qureshi, “Aqua:
Scalable rowhammer mitigation by quarantining aggressor rows at
runtime,” in 2022 55th IEEE/ACM International Symposium on
Microarchitecture (MICRO), pp. 108–123, IEEE, 2022.
[119] TDX, “Intel trust domain extensions.” https://www.intel.com/conten
t/www/us/en/developer/tools/trust-domain-extensions/overview.htm
l, 2021.
[120] AMD-SEV, “Amd secure encrypted virtualizations.” https://www.
amd.com/en/developer/sev.html, 2018.
[121] R. Zhou, Z. Ai, J. Hu, Q. Liu, Q. Zhou, X. Wang, H. Jiang, and K.-C.
Li, “Data integrity checking for iscsi with dm-verity,” in Advanced
Technologies, Embedded and Multimedia for Human-centric Com-
puting: HumanCom and EMC 2013, pp. 691–697, Springer, 2014.
[122] V. Costan, “Intel sgx explained,” IACR Cryptol, EPrint Arch, 2016.
[123] S. Gueron, “Memory encryption for general-purpose processors,”
IEEE Security & Privacy, vol. 14, no. 6, pp. 54–62, 2016.
[124] G. Saileshwar, P. J. Nair, P. Ramrakhyani, W. Elsasser, J. A.
Joao, and M. K. Qureshi, “Morphable counters: Enabling compact
integrity trees for low-overhead secure memories,” in 2018 51st
Annual IEEE/ACM International Symposium on Microarchitecture
(MICRO), pp. 416–427, IEEE, 2018.
[125] W. Hua, M. Umar, Z. Zhang, and G. E. Suh, “Mgx: Near-zero
overhead memory protection for data-intensive accelerators,” in Pro-
ceedings of the 49th Annual International Symposium on Computer
Architecture, pp. 726–741, 2022.
[126] J. Wang, Z. Zhang, M. Wang, H. Qiu, T. Zhang, Q. Li, Z. Li,
T. Wei, and C. Zhang, “Aegis: Mitigating targeted bit-flip attacks
against deep neural networks,” in 32nd USENIX Security Symposium
(USENIX Security 23), pp. 2329–2346, 2023.
[127] M. Qureshi, A. Rohan, G. Saileshwar, and P. J. Nair, “Hydra: En-
abling low-overhead mitigation of row-hammer at ultra-low thresh-
olds via hybrid tracking,” in Proceedings of the 49th Annual Inter-
national Symposium on Computer Architecture, pp. 699–710, 2022.
[128] J. Woo, G. Saileshwar, and P. J. Nair, “Scalable and secure row-
swap: Efficient and safe row hammer mitigation in memory sys-
tems,” in 2023 IEEE International Symposium on High-Performance
Computer Architecture (HPCA), pp. 374–389, IEEE, 2023.
[129] Y. Wang, A. Ferraiuolo, and G. E. Suh, “Timing channel protection
for a shared memory controller,” in 2014 IEEE 20th International
Symposium on High Performance Computer Architecture (HPCA),
pp. 225–236, IEEE, 2014.
[130] A. Ferraiuolo, Y. Wang, D. Zhang, A. C. Myers, and G. E. Suh,
“Lattice priority scheduling: Low-overhead timing-channel protec-
tion for a shared memory controller,” in 2016 IEEE International
Symposium on High Performance Computer Architecture (HPCA),
pp. 382–393, IEEE, 2016.
[131] W. Xiong, L. Ke, D. Jankov, M. Kounavis, X. Wang, E. Northup,
J. A. Yang, B. Acun, C.-J. Wu, P. T. P. Tang, et al., “Secndp: Secure
near-data processing with untrusted memory,” in 2022 IEEE Inter-
national Symposium on High-Performance Computer Architecture
(HPCA), pp. 244–258, IEEE, 2022.
[132] A. Shafiee, A. Gundu, M. Shevgoor, R. Balasubramonian, and
M. Tiwari, “Avoiding information leakage in the memory controller
with fixed service policies,” in Proceedings of the 48th International
Symposium on Microarchitecture, pp. 89–101, 2015.
[133] B.
Sapui,
J.
Krautter,
M.
Mayahinia,
A.
Jafari,
D.
Gnad,
S. Meschkov, and M. B. Tahoori, “Power side-channel attacks
and countermeasures on computation-in-memory architectures and
technologies,” in 2023 IEEE European Test Symposium (ETS), pp. 1–
6, IEEE, 2023.
[134] J. Y. Ha, S. Lee, H. Y. Yeom, and Y. Son, “{RL-Watchdog}: A
fast and predictable {SSD} liveness watchdog on storage systems,”
in 2024 USENIX Annual Technical Conference (USENIX ATC 24),
pp. 1083–1100, 2024.
[135] T. Krauß, R. G¨otz, and A. Dmitrienko, “Security of nvme offloaded
data in large-scale machine learning,” in European Symposium on
Research in Computer Security, pp. 143–163, Springer, 2023.
[136] S. Devadas, M. van Dijk, C. W. Fletcher, L. Ren, E. Shi, and
D. Wichs, “Onion oram: A constant bandwidth blowup oblivious
ram,” in Theory of Cryptography: 13th International Conference,
TCC 2016-A, Tel Aviv, Israel, January 10-13, 2016, Proceedings,
Part II 13, pp. 145–174, Springer, 2016.
[137] W. Hua, M. Umar, Z. Zhang, and G. E. Suh, “Guardnn: secure
accelerator architecture for privacy-preserving deep learning,” in
Proceedings of the 59th ACM/IEEE Design Automation Conference,
pp. 349–354, 2022.
[138] IOMMU, “Intel iommu.” https://www.intel.com/content/dam/develo
p/external/us/en/documents/intel-whitepaper-using-iommu-for-dma
-protection-in-uefi-820238.pdf, 2014.
[139] K. Taranov, B. Rothenberger, A. Perrig, and T. Hoefler, “{sRDMA}–
efficient {NIC-based} authentication and encryption for remote di-
rect memory access,” in 2020 USENIX Annual Technical Conference
(USENIX ATC 20), pp. 691–704, 2020.
[140] T. Computing, “Nvidia trusted computing solutions.” https://docs.n
vidia.com/nvtrust/index.html, 2021.
[141] ARM, “Arm trustzone.” https://www.arm.com/technologies/trustzo
ne-for-cortex-a, 2014.
[142] Nvidia, “Structured sparsity in the nvidia ampere architecture.” https:
//developer.nvidia.com/blog/structured-sparsity-in-the-nvidia-amper
e-architecture-and-applications-in-search-engines/, 2023.
[143] Y. Zhou, S. Wagh, P. Mittal, and D. Wentzlaff, “Camouflage: Mem-
ory traffic shaping to mitigate timing attacks,” in 2017 IEEE Inter-
national Symposium on High Performance Computer Architecture
(HPCA), pp. 337–348, IEEE, 2017.
[144] P. W. Deutsch, Y. Yang, T. Bourgeat, J. Drean, J. S. Emer, and
M. Yan, “Dagguise: mitigating memory timing side channels,” in
Proceedings of the 27th ACM International Conference on Architec-
tural Support for Programming Languages and Operating Systems,
pp. 329–343, 2022.
[145] S. Banerjee, S. Wei, P. Ramrakhyani, and M. Tiwari, “Obsidian:
Cooperative state-space exploration for performant inference on
secure ml accelerators,” arXiv preprint arXiv:2409.02817, 2024.
[146] B. Halak, Hardware supply chain security: Threat modelling, emerg-
ing attacks and countermeasures. Springer Nature, 2021.
[147] M. Werner, T. Unterluggauer, L. Giner, M. Schwarz, D. Gruss, and
S. Mangard, “{ScatterCache}: thwarting cache attacks via cache
set randomization,” in 28th USENIX Security Symposium (USENIX
Security 19), pp. 675–692, 2019.
[148] Q. Tan, Z. Zeng, K. Bu, and K. Ren, “Phantomcache: Obfuscating
cache conflicts with localized randomization.,” in NDSS, 2020.
[149] M. K. Qureshi, “New attacks and defense for encrypted-address
cache,” in Proceedings of the 46th International Symposium on
Computer Architecture, pp. 360–371, 2019.
[150] V. Kiriansky, I. Lebedev, S. Amarasinghe, S. Devadas, and J. Emer,
“Dawg: A defense against cache timing attacks in speculative exe-
cution processors,” in 2018 51st Annual IEEE/ACM International
Symposium on Microarchitecture (MICRO), pp. 974–987, IEEE,
2018.


---

[151] D. Townley, K. Arıkan, Y. D. Liu, D. Ponomarev, and O. Ergin,
“Composable cachelets: Protecting enclaves from cache side-channel
attacks,” in 31st USENIX Security Symposium (USENIX Security
22), pp. 2839–2856, 2022.
[152] D. Sanchez and C. Kozyrakis, “Vantage: Scalable and efficient
fine-grain cache partitioning,” in Proceedings of the 38th annual
international symposium on Computer architecture, pp. 57–68, 2011.
[153] A. Dubey, R. Cammarota, and A. Aysu, “Maskednet: The first
hardware inference engine aiming power side-channel protection,” in
2020 IEEE International Symposium on Hardware Oriented Security
and Trust (HOST), pp. 197–208, IEEE, 2020.
[154] A. Dubey, R. Cammarota, and A. Aysu, “Bomanet: Boolean masking
of an entire neural network,” in Proceedings of the 39th International
Conference on Computer-Aided Design, pp. 1–9, 2020.
[155] Y. Luo and X. Xu, “A quantitative defense framework against
power attacks on multi-tenant fpga,” in Proceedings of the 39th
international conference on computer-aided design, pp. 1–9, 2020.
[156] Y. Yao, J. Zhao, Z. Li, X. Cheng, and L. Wu, “Jamming and
eavesdropping defense scheme based on deep reinforcement learning
in autonomous vehicle networks,” IEEE Transactions on Information
Forensics and Security, vol. 18, pp. 1211–1224, 2023.
[157] H. Yu, H. Ma, K. Yang, Y. Zhao, and Y. Jin, “Deepem: Deep neural
networks model recovery through em side-channel information leak-
age,” in 2020 IEEE International Symposium on Hardware Oriented
Security and Trust (HOST), pp. 209–218, IEEE, 2020.
[158] B. C. Vattikonda, S. Das, and H. Shacham, “Eliminating fine grained
timers in xen,” in Proceedings of the 3rd ACM workshop on Cloud
computing security workshop, pp. 41–46, 2011.
[159] R. Martin, J. Demme, and S. Sethumadhavan, “Timewarp: Rethink-
ing timekeeping and performance monitoring mechanisms to mit-
igate side-channel attacks,” ACM SIGARCH computer architecture
news, vol. 40, no. 3, pp. 118–129, 2012.
[160] K. v. Gleissenthall, R. G. Kıcı, D. Stefan, and R. Jhala, “Iodine:
Verifying constant-time execution of hardware,” in 28th USENIX
Security Symposium (USENIX Security 19), pp. 1411–1428, 2019.
[161] K. Sakiyama, L. Batina, N. Mentens, B. Preneel, and I. Ver-
bauwhede, “Small-footprint alu for public-key processors for per-
vasive security,” in Workshop on RFID Security, vol. 12, 2006.
[162] G. E. Suh, D. Clarke, B. Gassend, M. Van Dijk, and S. Devadas,
“Aegis: Architecture for tamper-evident and tamper-resistant pro-
cessing,” in ACM International Conference on Supercomputing 25th
Anniversary Volume, pp. 357–368, 2003.
[163] “Data operand independent timing isa guidance.” https://www.intel.
com/content/www/us/en/developer/articles/technical/software-secur
ity-guidance/best-practices/data-operand-independent-timing-isa-g
uidance.html.
[164] “Arm architecture registers for future architecture technologies.” ht
tps://developer.arm.com/documentation/ddi0601/2020-12/AArch6
4-Registers/DIT--Data-Independent-Timing.
[165] M. Ghaniyoun, K. Barber, Y. Xiao, Y. Zhang, and R. Teodorescu,
“Teesec: Pre-silicon vulnerability discovery for trusted execution
environments,” in Proceedings of the 50th Annual International
Symposium on Computer Architecture, pp. 1–15, 2023.
[166] M. Minkin and B. Kasikci, “Zipchannel: Cache side-channel vulner-
abilities in compression algorithms,” in 2024 54th Annual IEEE/IFIP
International Conference on Dependable Systems and Networks
(DSN), pp. 223–237, IEEE, 2024.
[167] K. Lee, M. Yan, J. Emer, and A. Chandrakasan, “Secureloop: Design
space exploration of secure dnn accelerators,” in Proceedings of the
56th Annual IEEE/ACM International Symposium on Microarchitec-
ture, pp. 194–208, 2023.
[168] C. Computing, “Confidential computing deployment guide.” https:
//docs.nvidia.com/cc-deployment-guide-tdx.pdf, 2024.
[169] H. Chen, C. Fu, J. Zhao, and F. Koushanfar, “Proflip: Targeted trojan
attack with progressive bit flips,” in Proceedings of the IEEE/CVF
International Conference on Computer Vision, pp. 7718–7727, 2021.
[170] A. S. Rakin, Z. He, and D. Fan, “Tbt: Targeted neural network attack
with bit trojan,” in Proceedings of the IEEE/CVF Conference on
Computer Vision and Pattern Recognition, pp. 13198–13207, 2020.
[171] Mitre, “Cve-2023-36189.” https://cve.mitre.org/cgi-bin/cvename.cgi
?name=CVE-2023-36189, 2023.
[172] T. Nakai, D. Suzuki, and T. Fujino, “Timing black-box attacks:
Crafting adversarial examples through timing leaks against dnns on
embedded devices,” IACR Transactions on Cryptographic Hardware
and Embedded Systems, pp. 149–175, 2021.
[173] Mitre, “Cve-2024-7297.” https://cve.mitre.org/cgi-bin/cvename.cgi
?name=CVE-2024-7297, 2024.
[174] Mitre, “Cve-2024-28224.” https://cve.mitre.org/cgi-bin/cvename.cgi
?name=CVE-2024-28224, 2024.
[175] C. Hunger, M. Kazdagli, A. Rawat, A. Dimakis, S. Vishwanath,
and M. Tiwari, “Understanding contention-based channels and using
them for defense,” in 2015 IEEE 21st International Symposium on
High Performance Computer Architecture (HPCA), pp. 639–650,
IEEE, 2015.
[176] T. Bourgeat, J. Drean, Y. Yang, L. Tsai, J. Emer, and M. Yan, “Casa:
End-to-end quantitative security analysis of randomly mapped
caches,” in 2020 53rd Annual IEEE/ACM International Symposium
on Microarchitecture (MICRO), pp. 1110–1123, IEEE, 2020.
[177] “Cwe - cwe/capec wgs & sigs.” https://cwe.mitre.org/community/
working groups.html#ai wg.
[178] C. Dwork, “Differential privacy,” in International colloquium on
automata, languages, and programming, pp. 1–12, Springer, 2006.
[179] F. Boenisch, C. M¨uhl, A. Dziedzic, R. Rinberg, and N. Papernot,
“Have it your way: Individualized privacy assignment for dp-sgd,”
Advances in Neural Information Processing Systems, vol. 36, 2024.
[180] T. Tiwari, S. Gururangan, C. Guo, W. Hua, S. Kariyappa, U. Gupta,
W. Xiong, K. Maeng, H.-H. S. Lee, and G. E. Suh, “Information flow
control in machine learning through modular model architecture,” in
33rd USENIX Security Symposium (USENIX Security 24), pp. 6921–
6938, 2024.
[181] A. Ferraiuolo, M. Zhao, A. C. Myers, and G. E. Suh, “Hyperflow:
A processor architecture for nonmalleable, timing-safe information
flow security,” in Proceedings of the 2018 ACM SIGSAC Conference
on Computer and Communications Security, pp. 1583–1600, 2018.
[182] M. Tiwari, J. K. Oberg, X. Li, J. Valamehr, T. Levin, B. Hardekopf,
R. Kastner, F. T. Chong, and T. Sherwood, “Crafting a usable
microkernel, processor, and i/o system with strict and provable
information flow security,” ACM SIGARCH Computer Architecture
News, vol. 39, no. 3, pp. 189–200, 2011.
[183] A. Erbsen, S. Gruetter, J. Choi, C. Wood, and A. Chlipala, “In-
tegration verification across software and hardware for a simple
embedded system,” in Proceedings of the 42nd ACM SIGPLAN
International Conference on Programming Language Design and
Implementation, pp. 604–619, 2021.
[184] Apple, “Private cloud compute: A new frontier for ai privacy in the
cloud.” https://security.apple.com/blog/private-cloud-compute/.
[185] Edgeless, “The confidential genai service.” https://www.edgeless.s
ystems/products/continuum.
