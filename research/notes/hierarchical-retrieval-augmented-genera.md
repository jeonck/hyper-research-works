---
title: HIERARCHICAL RETRIEVAL AUGMENTED GENERA-
id: hierarchical-retrieval-augmented-genera
tags:
- attack-ontology-drift-cti-85bc51
- pin-rate-survey
created: '2026-09-12T21:34:47.089690Z'
updated: '2026-09-12T21:44:29.003818Z'
source: https://arxiv.org/abs/2604.14166v1
source_domain: arxiv.org
fetched_at: '2026-09-12T21:34:47.089259Z'
fetch_provider: crawl4ai
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'arXiv 2604.14166v1 (2026): uses 7 ATT&CK technique-ID occurrences (without
  sub-techniques); ATT&CK release declaration classified as none.'
raw_file: raw/hierarchical-retrieval-augmented-genera.pdf
doi: arXiv:2604.14166v1
---

HIERARCHICAL RETRIEVAL AUGMENTED GENERA-
TION FOR ADVERSARIAL TECHNIQUE ANNOTATION IN
CYBER THREAT INTELLIGENCE TEXT
Filippo Morbiato, Markus Keller, Priya Nair, Luca Romano
University of Padua Italy
filippo.morbiato@studenti.unipd.it
ABSTRACT
Mapping Cyber Threat Intelligence (CTI) text to MITRE ATT&CK technique IDs
is a critical task for understanding adversary behaviors and automating threat de-
fense. While recent Retrieval-Augmented Generation (RAG) approaches have
demonstrated promising capabilities in this domain, they fundamentally rely on
a flat retrieval paradigm. By treating all techniques uniformly, these methods
overlook the inherent taxonomy of the ATT&CK framework, where techniques
are structurally organized under high-level tactics.
In this paper, we propose
H-TechniqueRAG, a novel hierarchical RAG framework that injects this tactic-
technique taxonomy as a strong inductive bias to achieve highly efficient and
accurate annotation. Our approach introduces a two-stage hierarchical retrieval
mechanism: it first identifies the macro-level tactics (the adversary’s technical
goals) and subsequently narrows the search to techniques within those tactics, ef-
fectively reducing the candidate search space by 77.5%. To further bridge the gap
between retrieval and generation, we design a tactic-aware reranking module and
a hierarchy-constrained context organization strategy that mitigates LLM context
overload and improves reasoning precision. Comprehensive experiments across
three diverse CTI datasets demonstrate that H-TechniqueRAG not only outper-
forms the state-of-the-art TechniqueRAG by 3.8% in F1 score, but also achieves a
62.4% reduction in inference latency and a 60% decrease in LLM API calls. Fur-
ther analysis reveals that our hierarchical structural priors equip the model with
superior cross-domain generalization and provide security analysts with highly
interpretable, step-by-step decision paths.
1
INTRODUCTION
Cyber Threat Intelligence (CTI) serves as the backbone of modern proactive cybersecurity, provid-
ing actionable insights into the tactics, techniques, and procedures (TTPs) deployed by threat actors.
To standardize the description of these behaviors, the MITRE ATT&CK framework has been widely
adopted as the de facto ontology (Strom et al., 2018). It organizes adversary behaviors into a strict
hierarchical taxonomy consisting of 14 high-level tactics (representing the ”why” or the adversary’s
technical goals) and over 200 fine-grained techniques (representing the ”how” or the specific exe-
cution methods). Automatically mapping unstructured CTI reports to these specific technique IDs
is essential for rapid threat analysis, intelligence sharing (often spanning various communication
channels and media (Yi-fan, 2016)), and automated defense deployment (Husari et al., 2017; Rani
et al., 2024).
However, mapping CTI text to the ATT&CK matrix is notoriously challenging due to the heavy
reliance on unstructured natural language, which is often riddled with technical jargon, implicit con-
text, and ambiguous attack descriptions. Traditional rule-based and supervised machine learning
approaches, similar to early manual feature extraction methods in other modalities (Li et al., 2025;
Zhang et al., 2024), struggle to generalize across the rapidly evolving landscape of cyber threats (Sir-
acusano et al., 2023). Recently, the advent of Large Language Models (LLMs) has opened new av-
enues for automated CTI processing (Tihanyi et al., 2024; Zhao et al., 2024), mirroring their broader
success in multimodal intelligence, multi-agent frameworks, and task-oriented systems (Qian et al.,
1
arXiv:2604.14166v1  [cs.CL]  24 Mar 2026


---

2025; Zhang et al., 2025; Si et al., 2023). Yet, relying solely on parametric knowledge via zero-shot
or few-shot prompting often leads to severe hallucinations or misclassifications (AI, 2024). The
primary bottleneck lies in the vast label space: LLMs struggle to distinguish between hundreds of
subtly different techniques without grounding in external, up-to-date knowledge bases.
To mitigate this, Retrieval-Augmented Generation (RAG) (Guu et al., 2020) has emerged as a
dominant paradigm. The current state-of-the-art for CTI-to-ATT&CK mapping, TechniqueRAG
(Lekssays et al., 2025), employs a standard ”flat” retrieval mechanism where all 200+ techniques
are embedded and indexed uniformly. While this significantly improves over zero-shot baselines,
it exhibits a critical architectural flaw: it completely ignores the rich, hierarchical taxonomy of the
ATT&CK framework. This flat paradigm leads to two major issues. First, it suffers from seman-
tic collision during retrieval, techniques belonging to entirely different tactics may share similar
vocabulary (e.g., ”malicious attachments” could trigger techniques in both Initial Access and De-
fense Evasion), confusing the retriever. Second, concatenating a long, unstructured list of retrieved
techniques as context exacerbates the ”lost in the middle” phenomenon in LLMs, an issue especially
critical when aligning influential samples in long contexts (Liu et al., 2024; Si et al., 2025a), severely
degrading the generator’s reasoning capabilities and unnecessarily inflating token costs.
In reality, the ATT&CK hierarchy encodes invaluable domain priors. A human analyst does not
search through 200 techniques simultaneously; rather, akin to global planners operating in complex
long-horizon agent tasks (Si et al., 2025b), they first determine the tactic (e.g., ”the attacker is try-
ing to establish Persistence”) and then evaluate the specific techniques under that umbrella (e.g.,
”Scheduled Task/Job”). Similar to how structured layout constraints and complex instruction map-
ping enhance generative visual models and multi-stage reasoning architectures (Hoxha et al., 2026;
Zhou et al., 2025; Wang et al., 2025), leveraging this hierarchical prior can not only resolve semantic
ambiguity but also exponentially prune the search space.
Motivated by this human-like analytical process, we propose H-TechniqueRAG (Hierarchical Tech-
niqueRAG), a framework that structurally aligns the RAG pipeline with the ATT&CK taxonomy.
Instead of a single flat index, we introduce a two-stage hierarchical retrieval mechanism. Given a
CTI snippet, the model first retrieves the most probable tactics, and then dynamically constrains the
fine-grained technique search strictly within those tactical boundaries. To further ensure robustness,
we introduce a tactic-aware reranking mechanism that leverages technique-tactic co-occurrence pri-
ors, alongside a hierarchical context organization strategy that structures the prompt logically for the
LLM.
In summary, our main contributions are as follows:
• Hierarchical Retrieval Paradigm: We design a two-stage retrieval framework that exploits the
inherent ATT&CK tactic-technique taxonomy. By filtering at the tactic level first, we reduce the
candidate technique space by 77.5%, transforming a dense, noisy retrieval task into a sparse, high-
confidence process.
• Tactic-Aware Reranking: We introduce a hierarchical reranking mechanism that fuses semantic
similarity with domain-specific priors (e.g., historical tactic-technique co-occurrence distributions
and hierarchical consistency constraints), achieving a 3.8% F1 improvement over the SOTA.
• Hierarchy-Constrained Generation: We propose a structured context organization strategy that
groups retrieved techniques under their respective tactics. This explicitly guides the LLM’s rea-
soning process, mitigates context window overload, and slashes LLM inference costs (API calls)
by 60%.
• Extensive Empirical Validation: Comprehensive evaluations across three CTI datasets demon-
strate that H-TechniqueRAG consistently yields superior accuracy, operates 62.4% faster during
inference, and exhibits exceptional cross-domain generalization. Furthermore, our approach in-
herently provides highly interpretable decision paths for security analysts.
2
RELATED WORK
CTI Extraction and TTP Mapping
Extracting threat intelligence from unstructured text has been
a long-standing challenge in cybersecurity. Early approaches relied on rule-based systems and man-
ually crafted patterns (Husari et al., 2017). TTPDrill (Husari et al., 2017) introduced a systematic
2


---

approach for extracting TTPs from threat reports using NLP techniques. TTPXHunter (Rani et al.,
2024) extended this work with machine learning classifiers for technique identification. However,
these approaches require extensive feature engineering and struggle with the diversity of CTI text, a
broad challenge also encountered in complex semantic information extraction from diverse domains
like remote sensing (Zhou et al., 2019). More recently, ThreatPilot (Xu et al., 2024) proposed an
attack-driven extraction framework, but it still relies on traditional NLP pipelines without leveraging
LLMs.
LLMs in Cybersecurity
Large language models have shown remarkable capabilities in various
cybersecurity tasks. CyberMetric (Tihanyi et al., 2024) provided a benchmark for evaluating LLMs
on cybersecurity knowledge, revealing that while LLMs possess substantial domain knowledge,
they struggle with precise technique identification due to the large number of similar techniques
in ATT&CK. Direct zero-shot or few-shot prompting often yields suboptimal results (AI, 2024),
highlighting the need for external knowledge augmentation and efficient context representation, a
principle broadly applicable to efficient generation tasks and semantic reasoning in complex visual
scenarios (Zhou et al., 2026; Li et al., 2024).
Retrieval-Augmented Generation
RAG has become a dominant paradigm for knowledge-
intensive NLP tasks (Guu et al., 2020). Recent work has explored various extensions to improve
retrieval quality and efficiency. TagRAG (Tao et al., 2026) introduced tag-guided hierarchical re-
trieval for general domains, automatically constructing tag hierarchies from data. LeanRAG (Zhang
et al., 2026) combined knowledge graphs with semantic aggregation for hierarchical retrieval. How-
ever, these approaches do not exploit pre-existing domain hierarchies like ATT&CK, requiring ad-
ditional effort to construct hierarchical structures. Our work differs by directly leveraging the well-
defined ATT&CK hierarchy, eliminating the need for hierarchy construction while ensuring domain
alignment. Conceptually, utilizing such structured, association-based alignment priors is similarly
crucial for robust localization and navigation in complex autonomous simulation environments (Li
et al., 2025a;b).
TechniqueRAG and CTI Annotation
TechniqueRAG (Lekssays et al., 2025) represents the cur-
rent state-of-the-art for CTI-to-ATT&CK mapping, using a flat RAG approach where all techniques
are indexed and retrieved uniformly. While effective, this approach ignores the hierarchical structure
of ATT&CK, leading to inefficient retrieval and suboptimal context organization. Our hierarchical
approach addresses these limitations by introducing tactic-level retrieval and tactic-aware reranking.
3
METHODOLOGY
In this section, we present H-TechniqueRAG, a hierarchical retrieval-augmented generation frame-
work for CTI-to-ATT&CK technique annotation. We first formalize the problem, then describe
the four core modules: (1) hierarchical knowledge base construction, (2) two-stage hierarchical
retrieval, (3) hierarchical reranking, and (4) hierarchical generation.
3.1
PRELIMINARY
Task Definition
Given a CTI text segment s ∈S, where S denotes the collection of CTI texts,
our goal is to predict the set of relevant ATT&CK techniques T ∗= {T1, T2, ..., Tk} ⊆T , where
T is the complete set of MITRE ATT&CK techniques (approximately 200 techniques in Enterprise
ATT&CK).
ATT&CK Hierarchy
The MITRE ATT&CK framework organizes techniques into a hierarchical
structure. We formalize this as:
Definition 1 (Tactic-Technique Hierarchy). Let A = {A1, A2, ..., A14} denote the set of 14 tactics
(e.g., Initial Access, Execution). Let T = {T1, T2, ..., Tn} denote the set of n techniques. We define:
• Technique-to-Tactic mapping: ϕ : T →A, which maps each technique to its parent tactic.
• Tactic-to-Technique mapping: ψ : A →2T , which returns all techniques under a tactic,
i.e., ψ(Ai) = {Tj|ϕ(Tj) = Ai}.
3


---

This hierarchy satisfies the completeness property:
14
[
i=1
ψ(Ai) = T ,
ψ(Ai) ∩ψ(Aj) = ∅
∀i̸ = j
(1)
This hierarchical structure encodes valuable domain knowledge—each technique belongs to exactly
one tactic, and techniques under the same tactic often share semantic characteristics.
3.2
MODULE 1: HIERARCHICAL KNOWLEDGE BASE CONSTRUCTION
We construct two separate knowledge bases for tactics and techniques, each with its own embedding
index.
Tactic Knowledge Base
For each tactic Ai ∈A, we construct a rich textual representation by
combining its official description, keywords, and typical adversary behaviors:
hAi = Encoder(desc(Ai) ⊕keywords(Ai) ⊕behaviors(Ai))
(2)
where ⊕denotes text concatenation and Encoder is a pre-trained sentence encoder (we use Sentence-
BERT (Reimers & Gurevych, 2019)). This yields a tactic embedding matrix HA ∈R14×d.
Technique Knowledge Base
For each technique Tj ∈T , we aggregate multiple information
sources:
hTj = Encoder(desc(Tj) ⊕examples(Tj) ⊕detection(Tj))
(3)
where desc(Tj) is the official description, examples(Tj) contains procedure examples, and
detection(Tj) provides detection methods. This produces a technique embedding matrix HT ∈
Rn×d.
Tactic-Technique Co-occurrence Prior
We compute the conditional probability of techniques
given tactics based on historical CTI data:
P(Tj|Ai) =
count(Tj, Ai)
P
Tk∈ψ(Ai) count(Tk, Ai)
(4)
This prior captures domain-specific frequency patterns—for instance, under ”Initial Access”, tech-
niques like ”Phishing” (T1566) appear more frequently than ”Hardware Additions” (T1200).
3.3
MODULE 2: TWO-STAGE HIERARCHICAL RETRIEVAL
Unlike flat retrieval that searches all techniques simultaneously, our hierarchical approach first iden-
tifies relevant tactics, then searches within those tactics.
3.3.1
STAGE 1: TACTIC RETRIEVAL
Given a CTI text s, we first encode it:
hs = Encoder(s)
(5)
We then compute semantic similarity with each tactic:
scoreA(s, Ai) = cos(hs, hAi) =
h⊤
s hAi
∥hs∥∥hAi∥
(6)
We select the top-M tactics as candidates:
CA = Top-M({scoreA(s, Ai)}14
i=1)
(7)
We use M = 3 to balance recall and efficiency. Since there are only 14 tactics, selecting the top
3 provides sufficient coverage (recall > 95% in practice) while significantly pruning the technique
search space.
4


---

3.3.2
STAGE 2: TECHNIQUE-TACTIC JOINT RETRIEVAL
Within each candidate tactic Ai ∈CA, we retrieve relevant techniques using a combined score of
semantic similarity and co-occurrence prior:
scoreT (s, Tj|Ai) = α · cos(hs, hTj) + β · P(Tj|Ai)
(8)
where α + β = 1 balances semantic matching and domain prior. We set α = 0.7, β = 0.3 based on
validation performance.
The final candidate set aggregates techniques from all candidate tactics:
CT =
[
Ai∈CA
Top-KA({scoreT (s, Tj|Ai)}Tj∈ψ(Ai))
(9)
With M = 3 and KA = 15, we retrieve at most |CT | ≤45 techniques, compared to 200+ in flat
retrieval—a 77.5% reduction.
3.4
MODULE 3: HIERARCHICAL RERANKING
The retrieval stage provides initial candidate scores, but may not capture complex inter-
dependencies. We employ a learned reranking model that incorporates hierarchical features.
Hierarchical Feature Construction
For each candidate technique Tj, we construct a feature vec-
tor combining:
fTj = [hTj; hϕ(Tj); scoreA(s, ϕ(Tj)); P(Tj|ϕ(Tj))]
(10)
where hTj is the technique embedding, hϕ(Tj) is the parent tactic embedding, scoreA(s, ϕ(Tj)) is
the tactic retrieval score, and P(Tj|ϕ(Tj)) is the co-occurrence prior.
Reranking Model
We use a simple neural network for reranking:
rerank score(Tj) = w⊤σ(WrfTj + br)
(11)
where σ is ReLU activation, and w, Wr, br are learnable parameters.
Consistency Calibration
To ensure hierarchical consistency, we apply a confidence penalty for
techniques whose parent tactics are not in CA:
confidence(Tj) = rerank score(Tj) × I[ϕ(Tj) ∈CA]
(12)
Fallback Mechanism
If the maximum confidence is below a threshold θ (indicating potential
retrieval failure), we fall back to global retrieval:
Cfallback
T
= Top-K({cos(hs, hTj)}n
j=1)
(13)
This ensures robustness when tactic retrieval fails.
3.5
MODULE 4: HIERARCHICAL GENERATION
The final stage uses an LLM to generate technique predictions based on the hierarchical context.
Hierarchical Context Organization
Unlike flat RAG that concatenates all retrieved content, we
organize the context by tactics:
Given CTI text: "{s}"
Relevant Tactics and Techniques:
[Tactic: {A_i} (Score: {score_A})]
- Technique {T_j}: {desc(T_j)}
...
5


---

[Tactic: {A_k} (Score: {score_A})]
- Technique {T_m}: {desc(T_m)}
...
This organization has two benefits: (1) it structures information hierarchically, making it easier
for the LLM to reason about tactic-technique relationships, and (2) it significantly reduces context
length from approximately 20,000 tokens (200 techniques × 100 tokens each) to about 4,500 tokens
(45 techniques × 100 tokens).
Hierarchy-Constrained Generation
We design the prompt to explicitly leverage the hierarchy:
You are a cybersecurity expert. Based on the hierarchical
ATT&CK knowledge:
1. First, identify which tactics are most relevant
2. Then, select techniques from the candidate set
3. Ensure each predicted technique belongs to one of
the candidate tactics
Output format:
- Tactic: {A_i}
- Techniques: {T_j}, {T_k}
This guides the LLM to follow the hierarchical structure during generation.
3.6
TRAINING OBJECTIVE
We train the encoder and reranking model end-to-end using a multi-task loss:
L = Ltactic + λ1Ltechnique + λ2Lrerank + λ3Lconsistency
(14)
Tactic Retrieval Loss
Ltactic = −
X
Ai∈A∗
log
exp(scoreA(s, Ai))
P
Aj∈A exp(scoreA(s, Aj))
(15)
where A∗= {ϕ(Tj)|Tj ∈T ∗} is the set of true tactics.
Technique Retrieval Loss
Ltechnique = −
X
Tj∈T ∗
log
exp(scoreT (s, Tj|ϕ(Tj)))
P
Tk∈ψ(ϕ(Tj)) exp(scoreT (s, Tk|ϕ(Tj)))
(16)
Reranking Loss
Lrerank = −
X
Tj∈T ∗
log
exp(rerank score(Tj))
P
Tk∈CT exp(rerank score(Tk))
(17)
Consistency Loss
Lconsistency =
1
|CT |
X
Tj∈CT
I[ϕ(Tj) /∈CA] · rerank score(Tj)
(18)
This loss penalizes techniques whose parent tactics are not in the candidate set, encouraging hierar-
chical consistency.
6


---

3.7
COMPLEXITY ANALYSIS
Time Complexity
Tactic retrieval requires computing similarity with 14 tactics: O(|A| · d) =
O(14 · d). Technique retrieval searches within M tactics, each containing approximately |T |/|A|
techniques: O(M · |T |
|A| · d) = O(3 · 15 · d). Total complexity is O(22, 656) for d = 384, compared
to O(76, 800) for flat retrieval—a 70.5% reduction.
Space Complexity
We store embeddings for both tactics and techniques: O((|A| + |T |) · d) =
O(214 · 384). We use FAISS for efficient similarity search with minimal memory overhead.
4
EXPERIMENTS
We conduct comprehensive experiments to evaluate H-TechniqueRAG on three research questions:
• RQ1: How does H-TechniqueRAG compare to state-of-the-art methods in annotation accuracy?
• RQ2: What efficiency gains does hierarchical retrieval provide?
• RQ3: How do individual components contribute to overall performance?
4.1
EXPERIMENTAL SETUP
Datasets
We evaluate on three CTI datasets:
• CTI-RCM (Husari et al., 2017): 1,200 CTI texts with 3,500 technique annotations, collected from
diverse threat reports. We use 80%/10%/10% for train/validation/test.
• MITRE CTI (Strom et al., 2018): 2,800 CTI texts with 8,200 annotations, sourced from MITRE’s
official CTI corpus. This larger dataset tests scalability.
• TRAM (Gao et al., 2024): 450 CTI texts used exclusively for testing cross-domain generalization.
Baselines
We compare with 8 baselines covering traditional methods, LLM-based approaches,
and RAG variants:
• Zero-shot LLM (AI, 2024): Direct prompting of Llama-3-8B without retrieval.
• BERT-NER (Devlin et al., 2019): Fine-tuned BERT for named entity recognition of techniques.
• TTPXHunter (Rani et al., 2024): Traditional NLP pipeline with rule-based extraction.
• CyberMetric-LLM (Tihanyi et al., 2024): LLM with cybersecurity knowledge, no retrieval.
• ThreatPilot (Xu et al., 2024): Attack-driven CTI extraction using LLMs.
• TagRAG (Tao et al., 2026): Hierarchical RAG with automatically constructed tags.
• LeanRAG (Zhang et al., 2026): Knowledge graph-based hierarchical retrieval.
• TechniqueRAG (Lekssays et al., 2025): State-of-the-art flat RAG for CTI annotation.
Evaluation Metrics
We report precision, recall, and F1-score (micro-averaged). Additionally, we
measure MAP@10 (Mean Average Precision at 10) for ranking quality, tactic accuracy for hierar-
chical consistency, inference time in milliseconds, and LLM API call count for cost analysis.
Implementation Details
We use Sentence-BERT (all-MiniLM-L6-v2) as the encoder with em-
bedding dimension d = 384. For LLM generation, we use Llama-3-8B-Instruct. We index em-
beddings with FAISS using IVF (Inverted File Index) for efficient retrieval. Training uses Adam
optimizer with learning rate 1e −4, batch size 32, and early stopping with patience 5. All exper-
iments run on a single NVIDIA A100 40GB GPU. We set hyperparameters M = 3, KA = 15,
α = 0.7, β = 0.3, and θ = 0.3 based on validation performance.
7


---

Table 1:
Main performance comparison across datasets.
Best results in bold, second-best
underlined.
Method
CTI-RCM
MITRE CTI
Avg F1
F1
P
R
MAP@10
F1
P
R
MAP@10
Zero-shot LLM AI (2024)
45.2
48.3
42.5
38.5
42.8
45.1
40.7
35.2
44.0
BERT-NER Devlin et al. (2019)
52.1
55.8
48.9
45.2
49.7
53.2
46.6
42.8
50.9
TTPXHunter Rani et al. (2024)
58.3
62.1
54.9
51.8
55.6
59.4
52.3
48.5
57.0
CyberMetric-LLM Tihanyi et al. (2024)
61.5
65.2
58.2
55.3
58.9
62.7
55.5
52.1
60.2
ThreatPilot Xu et al. (2024)
64.2
67.8
61.0
58.7
61.5
65.2
58.2
55.3
62.9
TagRAG Tao et al. (2026)
66.8
70.1
63.8
61.2
64.1
67.5
61.0
58.5
65.5
LeanRAG Zhang et al. (2026)
67.5
71.2
64.2
62.0
65.0
68.6
61.9
59.2
66.3
TechniqueRAG Lekssays et al. (2025)
68.3
71.8
65.1
63.5
66.0
69.5
62.8
60.8
67.2
H-TechniqueRAG (Ours)
72.1
75.3
69.2
67.8
69.8
72.9
66.9
65.2
71.0
Table 2: Efficiency comparison. Lower is better for all metrics.
Method
Time (ms)
API Calls
Candidates
Memory (MB)
Zero-shot LLM AI (2024)
1,250
1
0
16,000
TechniqueRAG Lekssays et al. (2025)
2,180
5
200
2,400
TagRAG Tao et al. (2026)
2,450
6
180
2,600
LeanRAG Zhang et al. (2026)
2,890
7
150
3,200
H-TechniqueRAG (Ours)
820
2
45
1,800
Table 3: Cross-domain generalization on TRAM test set.
Method
F1
P
R
Tactic Acc
Drop
TechniqueRAG Lekssays et al. (2025)
61.2
64.5
58.2
71.5
-10.4%
TagRAG Tao et al. (2026)
59.8
62.9
57.0
68.9
-8.7%
LeanRAG Zhang et al. (2026)
60.5
63.8
57.6
70.2
-8.7%
H-TechniqueRAG (Ours)
66.3
69.4
63.5
83.2
-4.9%
Table 4: Ablation study on CTI-RCM. All variants degrade from full model.
Variant
F1
MAP@10
Time (ms)
∆F1
Full Model
72.1
67.8
820
–
w/o Hierarchical Retrieval
68.3
63.5
2,180
-3.8%
w/o Tactic-Aware Reranking
70.2
65.6
850
-1.9%
w/o Co-occurrence Prior
71.0
66.5
820
-1.1%
w/o Fallback Mechanism
71.5
67.0
780
-0.6%
w/o Hierarchical Context
69.8
65.0
890
-2.3%
4.2
MAIN RESULTS
Annotation Accuracy
Table 1 presents performance comparison across datasets.
H-
TechniqueRAG achieves the best F1 scores on both CTI-RCM (72.1%) and MITRE CTI (69.8%),
outperforming TechniqueRAG by 3.8% and 3.8% respectively. This improvement stems from two
factors: (1) hierarchical retrieval prunes irrelevant techniques, reducing noise in the candidate set,
and (2) tactic-aware reranking incorporates domain priors for better ranking.
Compared to TagRAG and LeanRAG, which also employ hierarchical structures, H-TechniqueRAG
achieves 5.3% and 4.6% higher F1 respectively. This demonstrates that directly leveraging the well-
defined ATT&CK hierarchy is more effective than automatically constructing hierarchies (TagRAG)
or building knowledge graphs (LeanRAG).
Efficiency Analysis
Table 2 shows that H-TechniqueRAG significantly reduces computational
cost. Inference time decreases by 62.4% (from 2,180ms to 820ms) compared to TechniqueRAG.
8


---

1
2
3
4
5
M (Number of Tactics)
70
75
80
85
90
95
Score (%)
F1 Score
Tactic Recall
0.5
0.6
0.7
0.8
0.9
 (Semantic Weight)
70.0
70.5
71.0
71.5
72.0
F1 Score (%)
0.1
0.2
0.3
0.4
0.5
 (Confidence Threshold)
68
70
72
74
76
78
Score (%)
F1 Score
Precision
10
12
14
16
18
20
K_A (Techniques per Tactic)
70.8
71.0
71.2
71.4
71.6
71.8
72.0
F1 Score (%)
Figure 1: Parameter sensitivity analysis. Red dashed lines indicate optimal values.
This stems from two factors: (1) hierarchical retrieval reduces candidate techniques by 77.5%, and
(2) smaller candidate sets require fewer LLM tokens for context.
LLM API calls reduce from 5 to 2 (60% reduction), directly translating to cost savings. The hier-
archical knowledge base requires less memory (1,800MB vs 2,400MB) due to efficient indexing of
separate tactic and technique collections.
Cross-Domain Generalization
Table 3 evaluates on the held-out TRAM dataset to assess cross-
domain generalization. H-TechniqueRAG shows the smallest performance drop (-4.9%) compared
to TechniqueRAG (-10.4%), demonstrating that hierarchical structure provides domain-invariant
knowledge. Notably, tactic accuracy is significantly higher (83.2% vs 71.5%), indicating that tactic-
level predictions are more robust across domains.
4.3
ABLATION STUDIES
We conduct ablation studies to understand component contributions (Table 4). Removing hierarchi-
cal retrieval (using flat retrieval instead) causes the largest drop (-3.8% F1), confirming it as the core
innovation. This variant also suffers 2.6× longer inference time, highlighting the efficiency benefits.
Removing hierarchical context organization causes -2.3% F1 drop, showing that structured context
helps the LLM reason better than flat concatenation. Tactic-aware reranking contributes -1.9%,
demonstrating the value of hierarchical features. Co-occurrence prior provides moderate improve-
ment (-1.1% without it). Fallback mechanism has smallest impact (-0.6%) but is crucial for robust-
ness in edge cases.
9


---

65
70
75
80
85
90
95
Tactic Accuracy (%)
57.5
60.0
62.5
65.0
67.5
70.0
72.5
75.0
77.5
F1 Score (%)
Pearson r = 0.87
Initial
Access
Execution
Persistence
Privilege
Escalation
Defense
Evasion
Credential
Access
Discovery
Lateral
Movement
60
65
70
75
80
85
90
95
100
Accuracy (%)
T1566
T1059
T1055
T1083
T1078
Techniques
TA1
TA2
TA3
TA4
TA5
Tactics
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
Figure 2: Tactic retrieval analysis: (a) correlation with final F1, (b) per-tactic accuracy, (c) tactic-
technique co-occurrence.
1000
1500
2000
2500
Inference Time (ms)
67
68
69
70
71
72
F1 Score (%)
TechniqueRAG
TagRAG
LeanRAG
H-TechniqueRAG
TechniqueRAG
TagRAG
LeanRAG
H-TechniqueRAG
0
1
2
3
4
5
6
7
API Calls
100
200
300
400
500
CTI Text Length (tokens)
1000
1500
2000
2500
Inference Time (ms)
TechniqueRAG
H-TechniqueRAG
0
25
50
75
100
125
150
175
200
Candidate Size
Figure 3: Efficiency analysis: (a) time-performance trade-off, (b) text length impact, (c) scalability.
Hyperparameter Sensitivity
We analyze the effect of key hyperparameters (Figure 1). For M
(number of tactics), performance peaks at M = 3—smaller values hurt recall while larger values
introduce noise. The semantic weight α performs best at 0.7, suggesting semantic similarity should
dominate over co-occurrence prior. Confidence threshold θ = 0.3 balances precision and recall
optimally. Notably, performance is stable within reasonable ranges (e.g., M ∈[2, 4]), showing
robustness to hyperparameter choices.
4.4
ANALYSIS
Tactic Retrieval Quality
Figure 2 analyzes tactic retrieval performance. We find strong corre-
lation between tactic accuracy and final F1 (Pearson r = 0.87), confirming that accurate tactic
retrieval is crucial for overall performance. Some tactics are easier to identify than others—Initial
Access and Execution have >90% accuracy due to distinctive language patterns, while Persistence
and Defense Evasion are more challenging due to overlapping techniques.
Efficiency-Performance Trade-off
Figure 3 plots inference time vs. F1 for all methods. H-
TechniqueRAG achieves the best trade-off, positioned at the Pareto frontier. The improvement is
especially pronounced for longer CTI texts—hierarchical retrieval’s pruning effect increases with
text complexity, as ambiguous descriptions benefit more from tactic-level disambiguation.
Hierarchical Consistency
Figure 4 (Left) shows that H-TechniqueRAG achieves 93.2% hierar-
chical consistency (predicted techniques’ parent tactics match retrieved tactics), compared to 78.5%
for TechniqueRAG. This consistency provides interpretable decision paths—analysts can understand
why a technique was predicted by examining the tactic-technique relationship.
Scalability
Figure 4 (Right) demonstrates scalability with varying training data sizes.
H-
TechniqueRAG maintains >60% F1 with only 20% training data, outperforming TechniqueRAG
by 8% in this low-data regime. This advantage stems from hierarchical priors that compensate for
10


---

TechniqueRAG
TagRAG
LeanRAG
H-TechniqueRAG
60
65
70
75
80
85
90
95
100
Score (%)
78.5
82.3
84.1
93.2
Hierarchical Consistency
Tactic Accuracy
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1.0
Training Data Ratio
50
55
60
65
70
75
F1 Score (%)
Low-data
advantage
TechniqueRAG
H-TechniqueRAG
Figure 4: (Left) Hierarchical consistency analysis across methods. (Right) Scalability analysis with
varying training data sizes.
Tactic
Misclassification
35%
Technique
Ambiguity
28%
Multi-technique
Miss
22%
Novel
Technique
10%
Text
Vagueness
5%
TechniqueRAG
H-TechniqueRAG
0
20
40
60
80
100
120
140
160
Error Count
37.2%
Reduction
Figure 5: Error distribution and representative cases.
limited training examples—tactic-technique relationships learned from ATT&CK structure provide
strong inductive bias.
Error Analysis
We categorize errors into five types (Figure 5): (1) Tactic Misclassification (35%):
incorrect tactic retrieval leads to wrong technique candidates; (2) Technique Ambiguity (28%): se-
mantically similar techniques are hard to distinguish; (3) Multi-technique Miss (22%): complex
texts contain multiple techniques, but some are missed; (4) Novel Technique (10%): techniques not
covered in ATT&CK; (5) Text Vagueness (5%): insufficient information for any method.
The fallback mechanism mitigates 60% of tactic misclassification errors by falling back to global
retrieval when confidence is low. Technique ambiguity errors could be reduced with more granular
technique descriptions or sub-technique modeling.
5
CONCLUSION
We presented H-TechniqueRAG, a hierarchical retrieval-augmented generation framework for CTI-
to-ATT&CK technique annotation. By explicitly leveraging the tactic-technique hierarchy of the
ATT&CK framework, our approach achieves significant improvements in both accuracy and effi-
ciency. The two-stage hierarchical retrieval reduces the candidate set by 77.5%, while tactic-aware
reranking and hierarchical context organization improve annotation precision. Experiments demon-
strate consistent improvements across multiple datasets with 62.4% faster inference and 60% fewer
LLM calls. The hierarchical approach provides additional benefits beyond performance: inter-
pretable decision paths help analysts understand predictions, and the structured knowledge base
enables easier domain adaptation and incremental updates. Our work demonstrates that domain-
specific hierarchies, when properly leveraged, can significantly enhance RAG systems.
11


---

REFERENCES
Blake Strom, Andy Applebaum, Doug Miller, et al. Finding the tracks of the adversary: The mitre
att&ck framework. MITRE Corporation, 2018.
OU Yi-fan. Communication and operation of tv wechat official account. Journalism and Mass
Communication, 6(12):730–736, 2016.
George Husari, Ehab Al-Shaer, Mohiuddin Ahmed, et al. Ttpdrill: Automatic and accurate extrac-
tion of threat actions from unstructured text of cti sources. In Proceedings of the 33rd Annual
Computer Security Applications Conference, pp. 323–335, 2017.
Nanda Rani, Bikash Saha, Vikas Maurya, and Sandeep Kumar Shukla. Ttpxhunter: Actionable
threat intelligence extraction as ttps from finished cyber threat reports.
Digit. Threat. Res.
Pract., 5(4):37:1–37:19, 2024. doi: 10.1145/3696427. URL https://doi.org/10.1145/
3696427.
Xinjin Li, Yu Ma, Kaisen Ye, Jinghan Cao, Minghao Zhou, and Yeyang Zhou. Hy-facial: Hybrid
feature extraction by dimensionality reduction methods for enhanced facial expression classifica-
tion. arXiv preprint arXiv:2509.26614, 2025.
Xiangyu Zhang, Daijiao Liu, Tianyi Xiao, Cihan Xiao, Tuende Szalay, Mostafa Shahin, Beena
Ahmed, and Julien Epps. Auto-landmark: Acoustic landmark dataset and open-source toolkit for
landmark extraction. arXiv preprint arXiv:2409.07969, 2024.
Giuseppe Siracusano et al. Beyond rule-based systems: A survey of machine learning and natural
language processing in cyber threat intelligence. IEEE Communications Surveys & Tutorials,
2023.
Norbert Tihanyi, Mohamed Amine Ferrag, Ridhi Jain, Tam´as Bisztray, and M´erouane Deb-
bah.
Cybermetric: A benchmark dataset based on retrieval-augmented generation for eval-
uating llms in cybersecurity knowledge.
In IEEE International Conference on Cyber Secu-
rity and Resilience, CSR 2024, London, UK, September 2-4, 2024, pp. 296–302. IEEE, 2024.
doi: 10.1109/CSR61664.2024.10679494. URL https://doi.org/10.1109/CSR61664.
2024.10679494.
Xin Zhao et al. Large language models for cybersecurity: A comprehensive survey. arXiv preprint
arXiv:2405.04760, 2024.
Wenhan Qian, Ziqu Shang, Detang Wen, and Tongran Fu. From perception to reasoning and inter-
action: A comprehensive survey of multimodal intelligence in large language models. Authorea
Preprints, 2025.
Hongwei Zhang, Ji Lu, Yongsheng Du, Yanqin Gao, Lingjun Huang, Baoli Wang, Fang Tan, and
Peng Zou.
Marine: Theoretical optimization and design for multi-agent recursive in-context
enhancement. arXiv preprint arXiv:2512.07898, 2025.
Shuzheng Si, Wentao Ma, Haoyu Gao, Yuchuan Wu, Ting-En Lin, Yinpei Dai, Hangyu Li, Rui
Yan, Fei Huang, and Yongbin Li. SpokenWOZ: A large-scale speech-text benchmark for spoken
task-oriented dialogue agents. In Thirty-seventh Conference on Neural Information Processing
Systems Datasets and Benchmarks Track, 2023. URL https://openreview.net/forum?
id=viktK3nO5b.
Meta AI. Llama 3: Open and efficient foundation language models. arXiv preprint, 2024.
Kelvin Guu, Kenton Lee, Zora Tung, Panupong Pasupat, and Ming-Wei Chang. Retrieval augmented
language model pre-training. In International Conference on Machine Learning, pp. 3929–3938.
PMLR, 2020.
Ahmed Lekssays, Utsav Shukla, Husrev Taha Sencar, and Md. Rizwan Parvez. Techniquerag: Re-
trieval augmented generation for adversarial technique annotation in cyber threat intelligence text.
In Wanxiang Che, Joyce Nabende, Ekaterina Shutova, and Mohammad Taher Pilehvar (eds.),
Findings of the Association for Computational Linguistics, ACL 2025, Vienna, Austria, July 27 -
12


---

August 1, 2025, volume ACL 2025 of Findings of ACL, pp. 20913–20926. Association for Compu-
tational Linguistics, 2025. URL https://aclanthology.org/2025.findings-acl.
1076/.
Nelson F Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, and
Percy Liang. Lost in the middle: How language models use long contexts. Transactions of the
Association for Computational Linguistics, 12:277–294, 2024.
Shuzheng Si, Haozhe Zhao, Gang Chen, Yunshui Li, Kangyang Luo, Chuancheng Lv, Kaikai An,
Fanchao Qi, Baobao Chang, and Maosong Sun.
GATEAU: Selecting influential samples for
long context alignment. In Christos Christodoulopoulos, Tanmoy Chakraborty, Carolyn Rose,
and Violet Peng (eds.), Proceedings of the 2025 Conference on Empirical Methods in Natural
Language Processing, pp. 7380–7411, Suzhou, China, November 2025a. Association for Com-
putational Linguistics. ISBN 979-8-89176-332-6. doi: 10.18653/v1/2025.emnlp-main.375. URL
https://aclanthology.org/2025.emnlp-main.375/.
Shuzheng Si, Haozhe Zhao, Kangyang Luo, Gang Chen, Fanchao Qi, Minjia Zhang, Baobao Chang,
and Maosong Sun. A goal without a plan is just a wish: Efficient and effective global planner train-
ing for long-horizon agent tasks, 2025b. URL https://arxiv.org/abs/2510.05608.
Ardit Hoxha, Besnik Shehu, Erion Kola, and Etem Koklukaya. A survey of generative video models
as visual reasoners. 2026.
Yucheng Zhou, Jiahao Yuan, and Qianning Wang.
Draw all your imagine: A holistic bench-
mark and agent framework for complex instruction-based image generation.
arXiv preprint
arXiv:2505.24787, 2025.
Chenglin Wang, Yucheng Zhou, Qianning Wang, Zhe Wang, and Kai Zhang. Complexbench-edit:
Benchmarking complex instruction-driven image editing via compositional dependencies. In Pro-
ceedings of the 33rd ACM International Conference on Multimedia, pp. 13391–13397, 2025.
Yeyang Zhou, Yixin Chen, Yimin Chen, Shunlong Ye, Mingxin Guo, Ziqi Sha, Heyu Wei, Yanhui
Gu, Junsheng Zhou, and Weiguang Qu. Eagle: An enhanced attention-based strategy by generat-
ing answers from learning questions to a remote sensing image. In International Conference on
Computational Linguistics and Intelligent Text Processing, pp. 558–572. Springer, 2019.
Ming Xu, Hongtai Wang, Jiahao Liu, Xinfeng Li, Zhengmin Yu, Weili Han, Hoon Wei Lim, Jin Song
Dong, and Jiaheng Zhang. Threatpilot: Attack-driven threat intelligence extraction. 2024. URL
https://arxiv.org/abs/2412.10872v2.
Yucheng Zhou, Jihai Zhang, Guanjie Chen, Jianbing Shen, and Yu Cheng. Less is more: Vision
representation compression for efficient video generation with large language models. In Pro-
ceedings of the AAAI Conference on Artificial Intelligence, volume 40, pp. 13826–13834, 2026.
Xiaofan Li, Yifu Zhang, and Xiaoqing Ye.
Drivingdiffusion: layout-guided multi-view driving
scenarios video generation with latent diffusion model. In European Conference on Computer
Vision, pp. 469–485. Springer, 2024.
Wenbiao Tao, Xinyuan Li, Yunshi Lan, and Weining Qian. Tagrag: Tag-guided hierarchical knowl-
edge graph retrieval-augmented generation. CoRR, abs/2601.05254, 2026. doi: 10.48550/ARXIV.
2601.05254. URL https://doi.org/10.48550/arXiv.2601.05254.
Yaoze Zhang, Rong Wu, Pinlong Cai, Xiaoman Wang, Guohang Yan, Song Mao, Ding Wang, and
Botian Shi. Leanrag: Knowledge-graph-based generation with semantic aggregation and hier-
archical retrieval. In Sven Koenig, Chad Jenkins, and Matthew E. Taylor (eds.), Fortieth AAAI
Conference on Artificial Intelligence, Thirty-Eighth Conference on Innovative Applications of
Artificial Intelligence, Sixteenth Symposium on Educational Advances in Artificial Intelligence,
AAAI 2026, Singapore, January 20-27, 2026, pp. 34862–34869. AAAI Press, 2026. doi: 10.
1609/AAAI.V40I41.40789. URL https://doi.org/10.1609/aaai.v40i41.40789.
Xiaofan Li, Zhihao Xu, Chenming Wu, Zhao Yang, Yumeng Zhang, Jiang-Jiang Liu, Haibao Yu,
Xiaoqing Ye, Yuan Wang, Shirui Li, et al. U-vilar: Uncertainty-aware visual localization for au-
tonomous driving via differentiable association and registration. In Proceedings of the IEEE/CVF
International Conference on Computer Vision, pp. 24889–24898, 2025a.
13


---

Xiaofan Li, Chenming Wu, Zhao Yang, Zhihao Xu, Yumeng Zhang, Dingkang Liang, Ji Wan, and
Jun Wang. Driverse: Navigation world model for driving simulation via multimodal trajectory
prompting and motion alignment. In Proceedings of the 33rd ACM International Conference on
Multimedia, pp. 9753–9762, 2025b.
Nils Reimers and Iryna Gurevych.
Sentence-bert: Sentence embeddings using siamese bert-
networks. In Proceedings of the 2019 Conference on Empirical Methods in Natural Language
Processing, pp. 3982–3992, 2019.
Peng Gao, Fei Shao, Xinyu Liu, et al.
Tram: Threat report att&ck mapping.
arXiv preprint
arXiv:2401.02613, 2024.
Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. Bert: Pre-training of deep
bidirectional transformers for language understanding. In Proceedings of the 2019 Conference of
the North American Chapter of the Association for Computational Linguistics: Human Language
Technologies, pp. 4171–4186, 2019.
14
