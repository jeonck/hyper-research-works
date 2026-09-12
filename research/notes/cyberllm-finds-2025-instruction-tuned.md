---
title: 'CyberLLM-FINDS 2025: Instruction-Tuned'
id: cyberllm-finds-2025-instruction-tuned
tags:
- attack-ontology-drift-cti-85bc51
- pin-rate-survey
created: '2026-09-12T21:35:14.696693Z'
updated: '2026-09-12T21:44:30.853782Z'
source: https://arxiv.org/abs/2601.06779v1
source_domain: arxiv.org
fetched_at: '2026-09-12T21:35:14.696315Z'
fetch_provider: crawl4ai
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'arXiv 2601.06779v1 (2026): uses 15 ATT&CK technique-ID occurrences (with
  sub-techniques); ATT&CK release declaration classified as none.'
raw_file: raw/cyberllm-finds-2025-instruction-tuned.pdf
doi: arXiv:2601.06779v1
---

CyberLLM-FINDS 2025: Instruction-Tuned
Fine-tuning of Domain-Specific LLMs with
Retrieval-Augmented Generation and Graph
Integration for MITRE Evaluation
Vasanth Iyer1, Leonardo Bobadilla2, S. S. Iyengar2
1Department of Computer Science, Grambling State University, Louisiana, USA.
2Florida International University, Florida, USA.
Large Language Models (LLMs) such as Gemma-2B have demonstrated remarkable proficiency in
various NLP tasks. However, general-purpose models lack deep domain expertise in cybersecurity.
This research presents a methodology for fine-tuning the Gemma-2B model into a domain-specific
cybersecurity LLM. We outline the dataset preparation, domain fine-tuning process, synthetic data
generation, and implications for real-world cybersecurity applications. The results indicate improved
translation of threat events from Chain-of-Thought tuning to Instruction-Level tuning within the
cybersecurity domain, including threat detection, forensic investigation, and attack analysis.
Further experimentation reveals that domain-specific fine-tuning introduces challenges in prompt
length distribution, diverging from patterns in general-purpose models. Uneven prompt lengths
complicate the model’s ability to optimize its context window usage, effectively constraining local
inference to 200–400 tokens—despite support for 2048. One-shot prompts resembling chain-of-thought
reasoning paired with quantized weights performed best. Due to these context window constraints,
we employed a hybrid method: cloud-based LLMs generated synthetic datasets, which were then
used to fine-tune locally hosted, resource-efficient models.
To extend the evaluation, we introduce a Retrieval-Augmented Generation (RAG) pipeline and
graph-based reasoning framework. This enables structured alignment with MITRE ATT&CK tech-
niques using STIX-based threat intelligence, improving recall in multi-hop and long-context scenarios.
The graph modules encode entity-neighborhood context and tactic chains, helping mitigate lim-
itations of short prompt windows. Results show enhanced model alignment with TTP coverage,
validating our graph-augmented LLM’s utility in cybersecurity CTI applications.
1 Introduction
Instruction tuning [1] is a critical step in adapting large language models (LLMs) like Gemma-2B
to domain-specific tasks. It involves fine-tuning the model [3],[4][9],[10],[11],[12] on diverse examples
framed as natural language instructions across multiple task types. As illustrated in Figure 4, this
process enables the model to learn reasoning patterns from tasks such as commonsense inference,
translation, and classification, so it can generalize to new tasks like natural language inference—even
those it hasn’t seen during training. This transferability is essential in cybersecurity [6], where LLMs
must respond accurately to structured threats like MITRE ATT&CK [13] techniques without explicit
task retraining.
1
arXiv:2601.06779v1  [cs.CR]  11 Jan 2026


---

2 Related Work
Several works have explored fine-tuning [3] large language models for domain-specific applications.
Research in medical, legal, and financial domains has shown that adapting LLMs to specialized
datasets [17] improves their accuracy. Prior cybersecurity-focused AI models [6], such as OpenAI’s
GPT-3 [15] for threat analysis and IBM Watson for security, highlight the potential of LLMs in this
domain. However, challenges such as dataset availability, hallucinations, and security risks remain.
3 Methodology
Table 1 Size of Popular Language Models
(Non-Embedding Parameters)
Model
Year
# Parameters
(billions, non-embedding)
BERT Large
2018
0.34
T5
2019
11
GPT-3
2020
175
PaLM
2022
540
Gemma-2B
2023
2
DeepSeek-7B
2023
7
LLaMA
2023
65
Large models typically are trained with lots of data and have many parameters making it chal-
lenging to train from scratch in a research environment. So we will explore the current state of the
art foundation models which can then be fine tuned to our domain of interest. The criteria for the
comparison are the size of the LLMs and context size. Table 1 has parameters which are weights and
biases ranging from 0.3 billion to 540 billion parameters. The Table 1 also shows that the researchers
have recently been able to train better models with less number of parameters making it easier for
fine tuning for the final tasks. In the initial steps we like to optimize memory for efficient tuning
and we next evaluate how the number of parameters has an effect on prompting [1] accuracy as
illustrated in Figure 1 We categorize prompts [1] as follows: Zero-shot i.e. without training data,
one-shot with one example and few-shots with few examples as described in the prompts below.
User Query
Explain Zero-Shot Prompting using MITRE ATT&CK framework.
Model Response
Zero-shot prompting means that the model is asked to classify or reason with no prior example pro-
vided.
Prompt:
Classify the MITRE ATT&CK technique based on the following activity:
"The attacker executed a PowerShell script to download and run a malicious payload."
Answer:
Expected Output:
Tactic: Execution
Technique: T1059 - Command and Scripting Interpreter
Sub-technique: T1059.001 - PowerShell
User Query
Show a one-shot prompting example using MITRE ATT&CK.
2


---

100
100.3
100.7
101
101.3
0
10
20
30
40
50
60
70
Zero-shot One-shot
Few-shot
Natural Language Prompt
No Prompt
Number of Examples in Context (K)
Accuracy (%)
Effect of Prompting Across Model Sizes
175B Params (Prompt)
175B Params (No Prompt)
13B Params (Prompt)
13B Params (No Prompt)
1.3B Params (Prompt)
1.3B Params (No Prompt)
Fig. 1 Comparison of model accuracy across parameter sizes and prompting strategies as a function of the number of
in-context examples. Prompted models consistently outperform non-prompted models, especially in few-shot regimes.
Model Response
One-shot prompting provides a single example before asking the model to perform a similar task.
Prompt:
Classify the MITRE ATT&CK technique based on the following activity.
Example:
"The attacker used a phishing email with a malicious attachment to gain initial
access."
Answer:
Tactic: Initial Access
Technique: T1566 - Phishing
Sub-technique: T1566.001 - Spearphishing Attachment
Now classify this:
"The attacker executed a PowerShell script to download and run a malicious
payload."
Answer:
Expected Output:
Tactic: Execution
Technique: T1059 - Command and Scripting Interpreter
Sub-technique: T1059.001 - PowerShell
3


---

User Query
Show a few-shot prompting example using MITRE ATT&CK.
Model Response
Few-shot prompting provides multiple examples to help the model generalize better.
Prompt:
Classify the MITRE ATT&CK technique based on the following activities.
Example 1:
"The attacker used a phishing email with a malicious attachment to gain initial
access."
Answer:
Tactic: Initial Access
Technique: T1566 - Phishing
Sub-technique: T1566.001 - Spearphishing Attachment
Answer:
Expected Output:
Tactic: Execution
Technique: T1059 - Command and Scripting Interpreter
Sub-technique: T1059.001 - PowerShell
Table 2: Summary of locally trainable large language mod-
els (LLMs) with fewer than 2 billion parameters. These models
are selected based on their ability to fit within standard GPU
memory constraints (e.g., 24GB) and support fine-tuning for
domain-specific tasks such as cybersecurity reasoning.
Model
Params (B)
Year
Highlights
Gemma-2B
2
2024
Google’s lightweight open model for on-
device and fine-tuning tasks
TinyLLaMA-1.1B
1.1
2023
Minimal resource LLaMA-based model
for mobile/IoT research
Phi-2
2.7
2023
Microsoft’s model designed for reason-
ing, aligned with on-device use
DeepSeek-1.3B
1.3
2024
DeepSeek’s small model for fast, local
inference
StableLM-3B
3
2023
Stability AI’s open model designed for
transparency and edge use
RedPajama-3B
3
2023
Open LLaMA-style model trained on
reproducible public datasets
Figure 1 illustrates the relationship between prompting accuracy and the number of in-context
examples. As the number of examples increases from zero-shot to few-shot, the model’s performance
improves, making fewer errors and demonstrating better generalization. Additionally, models with
larger parameter counts exhibit stronger zero-shot generalization capabilities.
Our training pipeline Figures 2,3 consists of two main stages: (1) the construction of domain-
specific datasets 3 and (2) the fine-tuning of language models. To address resource constraints, we
leverage large language models (LLMs) to generate synthetic datasets and utilize smaller, locally
runnable LLMs—typically with reduced precision—for fine-tuning. Specifically, we select native LLMs
with fewer than 2 billion parameters, as summarized in Table 2, to ensure compatibility with our
available GPU memory. In this work, we focus on domain adaptation using Google’s recently released
Gemma-2B model.
4


---

Initial Evaluation
Gemma-2B
Initial Evaluation
Train Dataset
Fine-Tuned Gemma-2B
Initial Fine-Tuning
Question Generation
Answer Generation
Dataset Expansion
Synthetic Dataset
Fine-Tuned Gemma-2B
Synthetic
Continued Fine-Tuning
Fig. 2 Finetuning LLM
Initial Evaluation
Gemma-2B
Initial Evaluation
Domain Dataset
Fine-Tuned Gemma-2B
Initial Fine-Tuning
Question Generation
Answer Generation
Dataset Expansion
Synthetic Dataset
Fine-Tuned Gemma-2B
Synthetic
Continued Fine-Tuning
Fig. 3 Domain Finetuning LLM
3.1 Dataset Collection
To develop a cybersecurity-specific expert model, we construct a domain-specific dataset based on the
MITRE ATT&CK framework and use it to fine-tune the language model, as illustrated in Figure 2.
MITRE ATT&CK organizes adversarial behavior using well-defined Tactics and Techniques, provid-
ing a structured taxonomy that supports effective generalization during fine-tuning. The prompts
used for this task are generated using a chain-of-thought prompting approach, enabling the model
to reason through sequential steps aligned with the structure of ATT&CK.
3.2 Technique T# in the MITRE ATT&CK Framework
This section provides an overview of Technique #’s as defined in the MITRE ATT&CK framework,
including its associated tactics, use cases, and adversary behaviors. The technique is often leveraged
by threat actors to achieve [specific objective].
3.3 Understanding Vulnerability T#
Vulnerability X is a [type of flaw] that affects [systems/applications]. It allows attackers to [describe
action, e.g., escalate privileges, exfiltrate data, etc.]. This subsection explains the technical working
of the vulnerability, including how it is exploited and its presence in known threat campaigns.
3.4 Mitigation Strategies for Vulnerability T#
To reduce the risk associated with Vulnerability X, organizations can implement several mitigation
strategies:
• Apply security patches and updates regularly.
• Use network segmentation and access controls.
• Employ endpoint detection and response (EDR) tools.
• Monitor for known indicators of compromise (IoCs).
A typical technique and its description is shown in Table 3.
Aspect
Description
MITRE Technique
Txxxx – Technique X
Vulnerability Type
e.g., Buffer Overflow
Exploitable By
e.g., Remote attackers, malware
Mitigation
Patching, EDR, segmentation, etc.
Table 3 Example: Technique and Vulnerability Description.
4 Synthetic Data Generation
In cybersecurity, high-quality labeled data is scarce, often sensitive, and typically imbalanced toward
benign activity. This presents a significant barrier to effectively fine-tuning large language models
5


---

Fig. 4
Workflow for generating synthetic cybersecurity data using large LLMs. The process produces instruction-
format samples that encode attack behaviors, supporting Chain-of-Thought prompting and enabling small models to
reason over structured threat intelligence such as MITRE’s Pyramid of Pain, which ranks the difficulty of detecting
and disrupting various attacker artifacts.
(LLMs) for security-specific reasoning tasks. To address this, we introduce a synthetic data generation
[3] framework as illustrated in Figure 4. By leveraging the structured nature of the MITRE ATT&CK
framework, we use LLMs to generate instruction-style examples that simulate a wide variety of attack
tactics, techniques, and procedures (TTPs). This pipeline enables the creation of logs [14], [16] for rare
or hard-to-collect threats, supports diverse prompting styles (e.g., zero-shot, one-shot, few-shot), and
allows for balanced datasets that improve fine-tuning efficiency and model generalization. Crucially,
it also provides a privacy-preserving and legally compliant alternative to real-world security logs.
4.1 Instruction Tuning Process
We perform fine-tuning across multiple tasks at the instruction level. Instruction tuning enables large
language models (LLMs) to specialize in domain-specific reasoning by learning from natural lan-
guage examples aligned with real-world tasks. In the context of cybersecurity, we leverage structured
knowledge from the MITRE ATT&CK framework—such as techniques like T1059 and T1547, tactics
including Execution, Persistence, and Lateral Movement, and contextual formats like logs, alerts,
threat reports, and playbooks—to construct a diverse and targeted training corpus. As illustrated
in Figure 4, our approach combines domain adaptation with synthetic data generation to support
instruction-level fine-tuning at scale.
Synthetic datasets offer the advantage of complete control over coverage and balance. They allow
us to generate labeled examples for every ATT&CK technique, including rare or underrepresented
behaviors that are seldom encountered in enterprise environments. For instance, we can simulate
advanced scenarios such as T1003.001 – LSASS Dumping using PowerShell-based indicators
that may not naturally appear in historical logs. This ensures comprehensive coverage across tactics,
sub-techniques, and platforms, including Windows, Linux, and macOS.
Additionally, synthetic logs as in Table 4 can be tailored to varying levels of complexity. We design
some examples with clean and distinct attack signatures to support basic classification tasks, while
others contain obfuscated patterns or mixed signals to train models for reasoning under uncertainty.
This form of data augmentation enables models to engage in chain-of-thought prompting—reasoning
through multi-step sequences to correctly identify attacker behavior and map it to a specific tactic
or technique.
An equally important benefit of using synthetic data is its safety and compliance. Since no real
personal or organizational identifiers are involved, this method avoids the legal and ethical risks
6


---

Synthetic Log
Instruction
Model Output
"2024-04-15 10:22:11" user:
SYSTEM ran: "powershell -enc
..."
What MITRE ATT&CK technique does
this log indicate?
Tactic: Execution
Technique: T1059.001 – PowerShell
Zeek conn.log: 192.168.1.100 →
10.0.0.10 TCP 3389
Explain what this log suggests and map
it to MITRE ATT&CK.
Indicates use of RDP for Lateral
Movement.
Tactic: Lateral Movement
Technique: T1021.001 – Remote Desktop
Protocol
Table 4 ATT&CK Prompts Enhanced with Synthetic Data Logs.
associated with handling real logs, such as violations of privacy regulations like GDPR or HIPAA.
Furthermore, it mitigates the model’s dependence on the biases of any single SOC dataset, promoting
better generalization.
Finally, our framework supports the generation of diverse prompt formats for instruction tuning.
We create examples suitable for zero-shot learning (where no prior examples are given), one-shot
prompts (with a single reference example), and few-shot configurations (featuring multiple labeled
examples followed by a query). This variety improves the model’s ability to generalize across different
log structures and behavioral patterns. Together, these design choices result in a balanced and task-
relevant training set that significantly enhances the model’s performance in detecting and reasoning
about cyber threats.
4.2 Model Evaluation
The model was evaluated on:
• Accuracy in answering MITRE ATT&CK queries
• Performance on cybersecurity question-answering tasks
• Effectiveness in analyzing threat logs
• Comparison with general-purpose LLMs
The first of the four evaluation criteria pertains to domain adaptation. Our 2B-parameter model
demonstrated effective fine-tuning and successfully answered Chain-of-Thought-style queries aligned
with the MITRE ATT&CK framework. In contrast, the remaining three criteria—focused on instruc-
tion tuning and its extension through synthetic data generation—exhibited lower performance. This
was primarily due to the baseline accuracy of models under 2 billion parameters, which remained
below 20%, as illustrated in Figure 1. Due to reduced task accuracy and inadequate alignment with
instruction-based tasks, we leveraged larger, cloud-hosted LLMs exceeding 175 billion parameters to
generate synthetic instruction datasets. These models, achieving over 50% accuracy in instruction-
following tasks, exhibited stronger generalization capabilities. The generated synthetic data was then
used to re-train the smaller, local models [2], enhancing their ability to respond to instruction-level
prompts.
5 Results and Discussion
5.1 RAG vs Graph-based Retrieval Evaluation on MITRE Queries
To assess how retrieval augmentation impacts fine-tuned CyberLLMs for MITRE ATT&CK-
style queries, we conducted a detailed comparison between pure RAG, Graph+LLM, and
GraphRAG+GNN pipelines. These methods were tested using an automated LLM Judge scoring
system across 5 dimensions: relevance, completeness, accuracy, specificity, and clarity. The scripts
and dataset used are available in Github[5].
The results demonstrate that the hybrid GraphRAG+GNN architecture outperforms pure Graph
traversal while matching or exceeding RAG in several categories. Specifically:
• GraphRAG+GNN achieved the highest overall score (8.00), with improvements in Accuracy
and Specificity.
7


---

Table 5 LLM Judge Evaluation for 5 MITRE ATT&CK Queries
Approach
Relevance
Complete.
Accuracy
Specif.
Clarity
Avg. Score
Pure RAG
8.2
7.9
7.8
7.6
8.0
7.87
Graph + LLM
7.5
7.0
7.3
6.8
7.2
7.16
GraphRAG + GNN
8.0
7.8
8.2
7.9
8.1
8.00
• Pure RAG led in Clarity and speed, winning 3 out of 5 head-to-head evaluations.
• Graph+LLM trailed slightly in average score due to broader but less focused responses.
These findings suggest that combining structured graph context with lightweight GNN-based
node scoring enhances LLM interpretability and retrieval quality on MITRE-style queries.
Table 6 summarizes viable local LLM training configurations in Figure 5 using current-generation
NVIDIA hardware. In our experiments, we utilized a 24GB GPU* for fine-tuning. The domain-specific
MITRE ATT&CK dataset consisted of 2,398 prompt-response pairs (5). To accommodate GPU
memory constraints, the batch size was set to 4. However, attempts to use the default token lengths of
1,024 to 2,048 tokens resulted in parser errors at this batch size. We found that a token length of 397
(5)—combined with dynamic padding for variable-length prompts—enabled stable training across
all epochs. This constraint, however, significantly limited training to 1–2 shot prompting scenarios.
The results of 1–2 shot prompting are presented in Figure 7, with the maximum token out-
put length configured to 200 tokens, as shown in Figure 6. The generated responses demonstrate
meaningful domain adaptation and interpretable accuracy in the cybersecurity context. However, to
comprehensively assess model performance, further evaluation is required. In future work, we plan to
compare the fine-tuned model against other standard LLM baselines using an automated LLM-based
judge framework to ensure consistent and objective scoring across tasks.
GPU Memory Range
Typical Training Config
Notes / Recommendations
8–16GB GPUs
(e.g., RTX 3060, 4060, 3090,
T4)
• Token limit: 2048–3072
• Batch size: 2–4
• Use fp16 or bf16
• Enable gradient checkpointing
• FlashAttention can reduce memory
cost
• Ideal for instruction tuning with 1–2
shot prompts
24–32GB GPUs
(e.g., RTX 4090, A5000, V100) • Token limit: 4096–8192
• Batch size: 4–8+
• Supports long CoT prompts
• Can fine-tune with 4–6 shot examples
• Ideal for multi-turn logs or threat rea-
soning
• Combine synthetic logs with multi-
step output
24GB GPUs∗
(e.g., RTX 4090)
• Token limit: 397
• Batch size: 4
• Used 4-bit quantized [2] weights and
16-bit arithmetic
• Can fine-tune with 1–2 shot examples
• Ideal for domain fine-tuning locally
Table 6
∗Configuration shown was used during both training and evaluation.
6 Acknowledgments
Support for this research was provided by the Army Research Office under Grant Number W911NF-
21-1-0264. The authors would like to thank Dr. Igor Ternovskiy, for valuable discussions on the use
of synthetic data to better approximate domain-specific distributions for fine-tuning large language
models. Additional support was provided by the National Science Foundation under Grant Number
HBCU-EiR-2101181 and DOE Building Training and Assessment Centers Grants Program for work
on developing AI deep learning techniques using explainable AI. Portions of this work also contributed
8


---

Fig. 5 Instruction-tuning workflow using domain-adapted synthetic data. The pipeline integrates structured prompts
derived from the MITRE ATT&CK framework and Chain-of-Thought prompting strategies. The model is fine-tuned
with a mixture of zero-shot, one-shot, and few-shot examples to support reasoning and classification across cyberse-
curity tasks.
9


---

Fig. 6 Model inference results for domain-specific instruction prompts. Each output is constrained to a maximum of
200 tokens, reflecting the token limit applied during inference for consistency across prompt evaluations. The responses
demonstrate how the fine-tuned model interprets MITRE ATT&CK-aligned queries, illustrating task comprehension
and reasoning within the token constraint.
10


---

Fig. 7 Example of instruction-level fine-tuning with 1–2 shot prompting using synthetic data. The prompt contains
a real-world cybersecurity scenario aligned to MITRE ATT&CK, followed by a response from the fine-tuned model.
This illustrates the model’s ability to generalize and explain attack techniques based on few-shot learning with padded
token limits.
to the development of introductory AI courses, supported by a grant from the Google TensorFlow
team.
We gratefully acknowledge the contributions and mentorship of our former Co-Principal Investi-
gator, Dr. Y.B. Reddy, whose guidance and dedication were instrumental in the early stages of this
research. Dr. Reddy passed away recently, and we respectfully dedicate this work to his memory.
11


---

References
[1] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao.
ReAct: Synergizing Reasoning and Acting in Language Models. arXiv preprint arXiv:2210.03629,
2023. Available at: https://arxiv.org/abs/2210.03629.
[2] T. Dettmers, A. Pagnoni, A. Holtzman, and L. Zettlemoyer. QLoRA: Efficient Finetuning
of Quantized LLMs, arXiv preprint arXiv:2305.14314, 2023. Available: https://arxiv.org/abs/
2305.14314
[3] V.Iyer, I. Utilizing Transfer Learning and Graph Matching Spatial Attentions from using
CARLA Pre-Trained Models.. (Future Technology Conference, UK, Nov 2024.).
[4] V. Iyer and A. Mehmood. Multi-Object On-Line Tracking as an Ill-Posed Problem: Ensemble
Deep Learning at the Edge for Spatial Re-identification. In: Arai, K. (eds) Intelligent Computing.
SAI 2022. Lecture Notes in Networks and Systems, vol 507. Springer, Cham, 2022. Available at:
https://doi.org/10.1007/978-3-031-10464-0 13.
[5] Vasanth A. Iyer, “MITRE GNN Analysis: Graph-Augmented Retrieval and Evaluation for Cyber
Threat Intelligence,” GitHub repository, 2026. Available: https://github.com/viyer-research/
mitre-gnn-analysis (accessed Jan. 2026).
[6] S. G. Aarella, S. Agarwal, S. P. Mohanty, E. Kougianos, V. Iyer, and B. Rout. iPUF: A Novel
Security-by-Design Paradigm to Mitigate Data Manipulation and External Attacks in Cyber-
Physical Systems. Presented by IEEE. Available at: https://par.nsf.gov/biblio/10581950.
[7] Vasanth Iyer, and Asif Mehmood, ”Metadata learning of non visual features: cooccurrence
overlap function for rectangular regions and ground truth data”
[8] Iyer, Vasanth Shetty, Sachin,”Virtual Sensor Tracking using Byzantine Fault Tolerance and
Predictive outlier Model for Complex Tasks Recognition”
[9] V.Iyer, S.Shetty,Virtual sensor tracking using byzantine fault tolerance and predictive outlier
model for complex tasks recognition
[10] V. Iyer, A. Aved, T. B. Howlett, J. T. Carlo, B. Abayowa, Autoencoder versus pre-trained
CNN networks: deep-features applied to accelerate computationally expensive object detection
in real-time video streams
[11] V. Iyer, A. Aved, T. B. Howlett, J. T. Carlo, A. Mehmood, N. Pissinou, S. S. Iyengar, Fast
multi-modal reuse: co-occurrence pre-trained deep learning models
[12] V. Iyer, A. Mehmood, Metadata learning of non-visual features: co-occurrence overlap function
for rectangular regions and ground truth data, in: M. S. Alam (Ed.), Pattern Recognition and
Tracking XXXI, Vol. 11400, International Society for Optics and Photonics, SPIE, 2020, pp. 34
– 42.
[13] MITRE ATT&CK Framework, https://attack.mitre.org/
[14] Zeek Network Security Monitor, https://zeek.org/
[15] OpenAI, https://openai.com/
[16] IBM Watson for Cybersecurity, https://www.ibm.com/security/artificial-intelligence
[17] Ghiasi and G. Cui, Y. and Srinivas, A. and Qian R., and Lin and T. and Cubuk, E. and Le,
and Q. Zoph and B. Simple Copy-Paste is a Strong Data Augmentation Method for Instance
Segmentation., CoRR,(2020)
12
