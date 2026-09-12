---
title: 'Beyond Single Reports: Evaluating Automated ATT&CK'
id: beyond-single-reports-evaluating-automated-attck
tags:
- attack-ontology-drift-cti-85bc51
- ttp-extraction
- measurement
created: '2026-09-12T17:43:38.300115Z'
updated: '2026-09-12T21:34:13.372463Z'
source: https://arxiv.org/pdf/2604.07470
source_domain: arxiv.org
fetched_at: '2026-09-12T17:43:38.299281Z'
fetch_provider: crawl4ai
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'Haque et al. (ASE 26, arXiv 2604.07470, full text): 29 extraction methods
  replicated on 90 reports from SolarWinds/XZ Utils/Log4j; aggregation lifts F1 about
  26%, best F1 78.6%/54.9%; 33.3% of FPs are semantically similar techniques and 40-79.2%
  share a tactic; gold labels from CTIfecta with no ATT&CK release declared.'
raw_file: raw/beyond-single-reports-evaluating-automated-attck.pdf
doi: arXiv:2604.07470
---

Beyond Single Reports: Evaluating Automated ATT&CK
Technique Extraction in Multi-Report Campaign Settings
Md Nazmul Haque
mhaque4@ncsu.edu
North Carolina State University
Raleigh, North Carolina, USA
Sivana Hamer
sahamer@ncsu.edu
North Carolina State University
Raleigh, North Carolina, USA
Brandon Wroblewski
bnwroble@ncsu.edu
North Carolina State University
Raleigh, North Carolina, USA
Md Rayhanur Rahman
mdrayhanur.rahman@ua.edu
University of Alabama
Tuscaloosa, Alabama, USA
Laurie Williams
lawilli3@ncsu.edu
North Carolina State University
Raleigh, North Carolina, USA
Abstract
Large-scale cyberattacks, referred to as campaigns, are docu-
mented across multiple CTI reports from diverse sources, with
some providing a high-level overview of attack techniques
and others providing technical details. Extracting attack tech-
niques from reports is essential for organizations to identify
the controls required to protect against attacks. Manually ex-
tracting techniques at scale is impractical. Existing automated
methods focus on single reports, leaving many attack tech-
niques and their controls undetected, resulting in a fragmented
view of campaign behavior. The goal of this study is to aid se-
curity researchers in extracting attack techniques and controls
from a campaign by replicating and comparing the performance
of the state-of-the-art ATT&CK technique extraction methods
in a multi-report campaign setting compared to prior single-
report evaluations. We conduct an empirical study of 29 meth-
ods to extract attack techniques, spanning entity recognition
(NER), encoder-based classification, and decoder-based LLM
approaches. Our study analyzes 90 CTI reports across three
major attack campaigns, SolarWinds, XZ Utils, and Log4j, us-
ing both quantitative performance metrics and their impact
on controls. Our results show that aggregating multiple CTI
reports improves the F1 score by ≈26% over single-report
analysis, with most approaches reaching performance satura-
tion after 5–15 reports. Despite these gains, extraction perfor-
mance remains limited, with maximum F1 scores of 78.6% for
SolarWinds and 54.9% for XZ Utils. Moreover, up to 33.3% of
misclassifications involve semantically similar techniques that
share tactics and overlap in descriptions. The misclassification
has a disproportionate effect on control coverage. Reports that
are longer and include technical details consistently perform
better, even though their readability scores are low. Based on
the findings, we advocate that researchers move beyond single-
report evaluations and instead use our performance saturation
and control coverage metrics to evaluate technique-extraction
methods in multi-report campaigns.
1
Introduction
Cyber Threat Intelligence (CTI) reports are a key source for
understanding cyber attacks, capturing attack techniques (e.g.,
credential dumping), identifying exploited vulnerabilities, and
recommending controls to mitigate the attack [9, 33]. With
the global cost of cyberattacks projected to reach $12.2 tril-
lion annually by 2031 [8], organizations increasingly rely on
CTI to anticipate, detect, and respond to cyber threats [13].
Large-scale cyber attacks are often structured as attack cam-
paigns, defined as coordinated sequences of attack techniques
targeting specific organizations or sectors over time [46]. As a
result, multiple CTI reports are often published for the same
campaign by different sources [26]. For example, the Solar-
Winds campaign is documented by organizations, ranging
from government agencies such as CISA to independent se-
curity researchers and incident response teams. While these
sources describe the same campaign, they do so from differ-
ent perspectives: one report may focus on high-level strategic
goals, while another provides a granular forensic analysis of a
specific malware payload [26].
At the same time, according to an IBM survey, organizations
receive an average of 60,000 security blog posts per month [31].
As the volume and complexity of CTI reports grow, the timely
extraction and structuring of attack techniques becomes criti-
cal for anticipating and responding to threats [2]. To structure
the information, the MITRE ATT&CK framework [45] has
emerged as the de facto standard. For example, phishing is
an attack technique mapped to ATT&CK ID T1566. Organiza-
tions extract attack techniques from CTI reports and map them
to ATT&CK techniques and use the resulting intelligence to
anticipate, detect, and respond to attacks [45, 60]. However,
manually mapping CTI reports to MITRE ATT&CK framework
is a time-consuming and error-prone task [10, 13], motivating
automated extraction approaches.
Prior works have proposed different automated approaches
on single-report datasets, including rule-based Named Entity
Recognition (NER) [23, 30, 38, 40, 58], encoder-based classifica-
tion [17, 29, 47, 50, 53], and decoder-based LLM approaches [13,
14, 18, 21, 59]. However, all these approaches use custom
datasets and settings, which makes them incomparable. Büchel
et al. [10] conducted a systematic comparison with a unified
dataset and evaluation framework to directly compare the per-
formance of different approaches. Even the best-performing
1
arXiv:2604.07470v1  [cs.SE]  8 Apr 2026


---

ASE ’26, October 12–16, 2026 , Munich, Germany
Haque et al.
approach on single-report datasets achieves a maximum F1-
score of 72.5%, leaving a substantial portion of ATT&CK tech-
niques undetected. And when an ATT&CK technique is missed,
the corresponding controls, defined as recommended actions
that protect against specific ATT&CK techniques, may also be
missed, leaving the organization exposed to undetected threats.
While prior work refers to controls as “mitigations” or “tasks,”
we use the term “controls” consistently. As such, the perfor-
mance of the current extraction method, considering a single
report, is insufficient for practical use. Moreover, a recent study
has demonstrated that aggregating reports of related incidents
improves automated methods for understanding software vul-
nerabilities [3], suggesting that a similar aggregation strategy
may benefit multi-report analyses of the same campaign. Prior
work also notes that individual CTI reports may cover different
aspects of the same campaign, with one report complement-
ing another in describing attack techniques and campaign
behavior [26]. Aggregating multiple reports for a campaign
would help automated methods more accurately identify the
ATT&CK techniques. Hence, accurately capturing ATT&CK
techniques also improves coverage of the controls that protect
against them.
The goal of this study is to aid security researchers in ex-
tracting attack techniques and controls from a campaign by
replicating and comparing the performance of the state-of-the-
art ATT&CK technique extraction methods in a multi-report
campaign setting compared to prior single-report evaluations.
In this study, we address the following research questions.
RQ 1. How do existing automated attack technique extrac-
tion methods perform at the campaign level, having multiple
reports compared to a single report?
RQ 2. Which attack techniques are most frequently missed or
misclassified by existing methods, and does semantic similarity
between ATT&CK technique descriptions contribute to these
errors?
RQ 3. What is the impact of automated attack technique ex-
traction performance on the coverage of mitigation controls?
RQ 4. How many CTI reports are required for automated ap-
proaches to reach performance saturation as additional reports
are incorporated?
RQ 5. What characteristics of CTI reports enable existing
attack technique extraction approaches to perform better?
To answer the research questions, we conduct a concep-
tual replication [16] and extension [12] of Büchel et al. [10].
We evaluate the same 29 state-of-the-art automated extrac-
tion methods spanning three approaches (NER, encoder-based
classification, and decoder-based LLM) in a campaign-level,
multi-report setting. Rather than evaluating each CTI report
in isolation, as prior benchmarks do, we aggregate predictions
across multiple reports describing the same attack campaign
to assess extraction performance at the campaign level. We
conduct this evaluation on a dataset of 90 CTI reports drawn
from three high-profile campaigns: SolarWinds, XZ Utils, and
Log4j [26].
We found that aggregating multiple CTI reports improves
ATT&CK technique coverage compared to single-report eval-
uations by ≈26%. Our error analysis reveals that 33.3% of mis-
classifications occur between semantically similar ATT&CK
techniques, with approximately 79.2% of these errors involv-
ing techniques that share the same tactic (e.g., Defense Eva-
sion, Discovery). We further observe that extraction errors
propagate to downstream controls to mitigate the attack tech-
niques, where the best-performing method correctly covers
only 77.1% of the ground-truth controls.Finally, we found that
most approaches reach performance saturation after incorpo-
rating 10–15 CTI reports, with technically dense reports from
sources such as MITRE and CISA consistently contributing
the most to extraction performance.
The main contributions of this study are as follows: 1 A
campaign-level replication study of existing automated extrac-
tion methods across multiple CTI reports of the same cam-
paign. 2 Metrics for evaluating the performance of automated
CTI extraction approaches at the control level, quantifying
both technique coverage and missed controls. 3 Empirical
saturation thresholds quantifying the minimum number of
CTI reports required for automated extraction approaches to
reach performance saturation across attack campaigns. 4 A
characterization of the textual and structural report properties
that maximize ATT&CK technique extraction performance,
providing actionable guidance for cost-effective CTI collection
and curation. 5 A systematic characterization of the ATT&CK
techniques most frequently missed or misclassified by existing
methods to determine whether semantic overlap drives these
errors.
The rest of the paper is organized as follows: § 2 provides
the review of the background and related works, § 3 describes
the overall methodology of our study, § 4 and § 5 discuss the
results and discussions and § 6 and § 7 discuss the threats to
validity and conclude our paper, respectively.
2
Background and Related Work
Existing automated extraction of ATT&CK techniques from
CTI reports can be broadly categorized into three extraction
approaches [10, 29]: 1 Named Entity Recognition (NER), 2
encoder-based classification, and 3 decoder-based LLM.
1 Named-Entity Recognition (NER): NER-based ap-
proach treats ATT&CK technique extraction as a token-level
sequence labeling task, identifying explicit attack techniques
within CTI reports and then applying rule-based or machine
learning techniques to map extracted phrases to ATT&CK tech-
niques. A typical NER pipeline includes five components for
extracting relevant tokens: tokenization [62], POS tagging [44],
lemmatization [4, 49], related-word detection [19], and pars-
ing [35]. For example, Husari et al. proposed TTPDril, which
used tokenization, POS tagging, and BM25 TF-IDF method to
extract relevant information from the CTI reports [30]. Simi-
larly, Rahman et al. applied BM25 TF-IDF with subject-verb-
object tuple extraction [51]. AttacKG [38] constructs knowl-
edge graphs using NER by extracting attack-relevant entities.
2


---

Beyond Single Reports: Evaluating Automated ATT&CK Technique Extraction in Multi-Report Campaign Settings ASE ’26, October 12–16, 2026 , Munich, Germany
2 Encoder-based classification: Encoder-based classi-
fication approach formulates attack technique extraction as
a multi-class or multi-label text classification task. Instead of
identifying specific keywords or tokens, individual sentences
are mapped to one or more ATT&CK techniques. Most of
the existing literature uses either BERT- or RoBERTa-based
pretrained encoder models to extract ATT&CK techniques.
For instance, researchers [15, 53, 54] use different variants of
BERT-based models [1, 6, 7, 32, 52]. MITREtrieval [29] uses a
RoBERTa-based model [42]. While prior work evaluates both
variants on individual reports, our study evaluates them at the
campaign level, aggregating predictions across multiple CTI
reports for the same attack campaign.
3 Decoder-based LLM: Decoder-based LLM approach
uses LLM to generate attack technique predictions directly
from CTI text, typically through instruction-following or prompt-
based generation. Instead of relying on predefined labels or
token-level supervision, decoder-based LLMs synthesize expla-
nations, infer latent adversarial behaviors, and map narrative
descriptions to corresponding ATT&CK techniques. Instead of
classifying raw text into predefined ATT&CK techniques from
a given prompt, the decoder-based LLM approach generates
raw text, which is then post-processed using regular expres-
sions to extract ATT&CK techniques [59]. These approaches
often leverage few-shot prompting (FSP) [14, 20, 21, 36] or
retrieval-augmented generation (RAG) [13, 14, 18, 64] to im-
prove extraction from large or complex CTI reports. Several
studies also employ supervised fine-tuning (SFT) [13, 20, 21] to
adapt LLMs to domain-specific CTI data. For example, AECR
fine-tuned a 6-billion-parameter model to outperform larger
general-purpose models and reduce hallucinations using a
linear classification head [13]. In contrast, other works, such
as CTINexus [14] and IntelEX [64], combine generative LLMs
with multi-agent or RAG-like architectures to improve entity
relationship extraction and precision. AttacKG+ [65] uses a
four-stage generative LLM pipeline to extract TTPs and entity
relationships to build a knowledge graph. Anandayuvaraj et
al. propose an LLM-based pipeline that collects and groups
news articles describing the same software failure incident [3].
While both works aggregate information across multiple docu-
ments, their focus is on software incident analysis rather than
campaign-level ATT&CK technique extraction.
3
Study Design
We employ a conceptual replication [16] and extension de-
sign [12] to evaluate existing automated ATT&CK technique
extraction methods. A conceptual replication tests the same
research phenomenon as prior work but in a different context.
In this study, we evaluate the same 29 methods with settings
across three approaches (§ 3.2) studied by Büchel et al. [10],
but move from a single-report evaluation to a campaign-level,
multi-report dataset. An extension design builds on the repli-
cated study by introducing additional research questions that
go beyond the scope of the original. We extend the evalu-
ation to analyze the causes of misclassification (RQ 2), the
Dataset Selection
CTIfecta (106 Reports) →Filtered Dataset (90 Reports)
+ External Training Data (AnnoCTR & MITRE Samples)
Sec 3.1
Prediction Approaches
• NER Pipeline
•
Encoder Models
•
Decoder LLMs
(Ablation study)
(BERT, RoBERTa)
(Prompt, SFT)
Sec 3.2
Performance Evaluation
Campaign-Level Aggregation (Precision, Recall, F1-score)
Sec 3.3
RQ1
Misclassification Analysis
Embeddings & t-SNE
Sec 3.4
RQ2
Mitigation Gap
P-SSCRM Mapping
Sec 3.5
RQ3
Performance Saturation
# CTI reports (Greedy appr.)
Sec 3.6
RQ4
CTI Characteristics
Qualitative & Quantitative
Sec 3.7
RQ5
Figure 1: Overview of the experimental workflow.
downstream impact of controls (RQ 3), performance satura-
tion (RQ 4), and report characteristics (RQ 5), none of which
were addressed in the original study.
We provide an overview of our study design in Figure 1.
We first select a dataset of multiple CTI reports for the same
campaign (§3.1) and state-of-the-art methods under three ap-
proaches (§3.2. Next, we evaluate their campaign-level perfor-
mance (§ 3.3). We then extract the misclassified and missed
ATT&CK techniques and investigate the factors behind them(§ 3.4)
and quantify how those errors propagate into gaps in control
coverage(§ 3.5). Finally, we examine how performance evolves
as the number of CTI reports increases (§ 3.6) and characterize
the CTI reports that influence performance (§ 3.7).
3.1
Dataset Selection
To evaluate our research questions, we separate our training
and testing data into two distinct datasets. Initially, we con-
sidered the CTIfecta dataset by Hamer et al. [26] for both
purposes, as it provides multiple reports from the three attack
campaigns required for our evaluation. However, more than
65% (55 of 82) of its ATT&CK techniques appear at most 5
times across the entire dataset, resulting in a long-tail distri-
bution. Training directly on the long-tail CTIfecta data risks
severe overfitting, bias toward majority classes, and poor gen-
eralization. Moreover, to the best of our knowledge, no other
public campaign-level CTI dataset currently exists. Conse-
quently, relying solely on CTIfecta for training would necessi-
tate significant methodological interventions—such as transfer
learning from domain-specific foundational models [1, 41] or
advanced data augmentation [22, 56]. We therefore use the
AnnoCTR dataset for training and fine-tuning (discussed in
the next paragraph), reserving CTIfecta strictly for testing and
evaluation.
3


---

ASE ’26, October 12–16, 2026 , Munich, Germany
Haque et al.
Training dataset. For training or fine-tuning, we lever-
age the AnnoCTR dataset [37]. Because MITRE ATT&CK
technique definitions are standardized and independent of
campaign-specific context, the model learns relevant concepts
while generalizing beyond specific campaigns. We selected
AnnoCTR for its broader coverage (118 techniques) compared
with alternatives such as TRAM (50 techniques) [15]. How-
ever, 17 MITRE ATT&CK techniques present in our testing
data were not covered in AnnoCTR. To ensure complete label
coverage, we collected additional samples for each missing
technique directly from the MITRE ATT&CK website, using
the technique descriptions provided in the official ATT&CK
knowledge base. In the AnnoCTR dataset, minority classes
occur 1-5 times, with a mean of 2.02 samples per class. We
selected 3 samples per missing technique, consistent with the
mean representation of minority classes in AnnoCTR, yielding
51 additional training samples in total.
Testing dataset. For testing, we use the CTIfecta dataset
[26], comprising 106 CTI reports spanning three attack cam-
paigns—SolarWinds, XZ Utils, and Log4j—with 30, 31, and 45
reports per campaign, respectively, authored by a range of
organizations, including security vendors, government agen-
cies, and incident response teams. For example, the Solarwinds
attack campaign includes government directives (e.g., CISA
ED21-01 (https://tinyurl.com/bdf9z568)and in-depth industry
forensic whitepapers (https://tinyurl.com/nz78pj2e). Together,
these reports encompass 114 unique MITRE ATT&CK tech-
niques. We selected CTIfecta for its unique emphasis on depth
over breadth. Unlike existing datasets (e.g., TRAM [15], An-
noCTR [37], and TTPHunter [53]) that prioritize broad, single-
source coverage of disjoint attack campaigns, CTIfecta aggre-
gates diverse reports describing the same attack campaigns.
This multi-view structure enables cross-report aggregation,
capturing the semantic variability and reporting inconsisten-
cies that broader single-report datasets miss. Since our ob-
jective is to automatically extract adversarial activities and
map them to ATT&CK techniques, we filter the dataset using
inclusion and exclusion criteria. We retain only reports that
contain at least one ATT&CK technique and exclude reports
that explicitly reference ATT&CK technique identifiers in the
text to avoid trivial mappings. After filtering, our final dataset
comprises 90 CTI reports (21 SolarWinds, 28 XZ Utils, and 41
Log4j) that cover 82 unique attack techniques.
3.2
Selected Methods of Three Approaches
To evaluate existing approaches for mapping CTI reports of a
campaign to ATT&CK techniques, we replicate the 29 state-of-
the-art methods evaluated by Büchel et al. [10], spanning three
approaches: named entity recognition (NER), encoder-based
classification, and decoder-based LLM. We preserve the origi-
nal configurations, hyperparameters, and model architectures
as reported in [10]. A summary of all 29 methods, including
their configurations, is presented in Table 1.
For NER, the full pipeline comprises five syntactic and
semantic components. To assess the contribution of each com-
ponent, we conduct an ablation study by systematically dis-
abling one module at a time and measuring the resulting per-
formance degradation relative to the full pipeline. Notably,
the NER approach is rule- and pattern-driven and does not
require model training. For encoder-based classification, 15
methods are evaluated, grouped into two categories based on
model architecture: BERT-based and RoBERTa-based variants.
For decoder-based LLMs, we evaluate eight methods cate-
gorized as: prompt-based and weight-based configurations.
Within each category, four methods are considered: (i) zero-
shot prompting using only the CTI report text (RAW), (ii) few-
shot prompting with five randomly labeled examples (FSP),
(iii) RAG supplying the top five most relevant ATT&CK tech-
niques based on cosine similarity of the given CTI text as
context (RAG), and (iv) a combination of few-shot prompting
and RAG (FSP+RAG).
3.3
Effectiveness of Extraction Methods
We first obtain predictions from each automated method for
every individual report. We then aggregate the predictions to
the campaign level (e.g., SolarWinds) by taking the union of
all ATT&CK techniques predicted across reports describing
the same attack campaign. For example, the SolarWinds cam-
paign comprises 21 CTI reports: if one method predicts {T1078,
T1027} for one report and {T1027, T1195} for another report,
the aggregated campaign-level prediction for these two re-
ports is {T1078, T1027, T1195}. We apply the same aggregation
across all 21 reports in the SolarWinds campaign to obtain the
full set of predicted campaign-level techniques. Finally, we
evaluate the aggregated predictions against the complete set
of ground-truth techniques annotated across all 21 reports in
the SolarWinds campaign (§ 3.1) in the CTIfecta dataset.
We evaluate the methods’ effectiveness using precision,
recall, and F1 Score. Precision measures the proportion of pre-
dicted techniques that are correct, recall captures the propor-
tion of ground-truth techniques successfully identified, and
the F1-score represents their harmonic mean. We report macro-
averaged values, treating each technique equally regardless of
its frequency in the dataset.
3.4
Misclassification and Missed ATT&CK
Techniques Analysis
We identify missed and misclassified ATT&CK techniques by
quantitatively analyzing false negatives (FNs) and false pos-
itives (FPs) at the method level for each approach. We then
investigate whether semantic similarity between ATT&CK
technique descriptions contributes to misclassifications and
missed techniques. Techniques with similar official descrip-
tions may be misclassified by models that rely on textual repre-
sentations. To empirically examine whether a misclassification
is attributable to semantic overlap in the ATT&CK technique
description, we compute text embeddings [55] for the descrip-
tions of all predicted and ground-truth techniques and then
4


---

Beyond Single Reports: Evaluating Automated ATT&CK Technique Extraction in Multi-Report Campaign Settings ASE ’26, October 12–16, 2026 , Munich, Germany
Table 1: Summary of the 29 Evaluated Methods Across Three Extraction Approaches, with Model Architectures and
Training Configurations Used in the Study.
Approach
(#methods)
Category
Methods
Configuration & Metadata
NER (6)
Rule-based
full,
base,
no_lemma,
no_parsing,
no_pos,
no_related_words
Ablation study; Syntactic/Semantic Pipeline (Rule-
based, no training)
Encoder-based
Classification
(15)
BERT-based
CySecBERT, SciBERT-{c, uc}, CyBERT, TRAM, Se-
cureBERT, SecBERT, bert-base-{c, uc}, DarkBERT
{c}=cased, {uc}=uncased;
{b}=base, {l}=large; Multi-label classification head;
Activation: Sigmoid; LR: 2×10−5; Batch Size: 16
RoBERTa-based
SecRoBERTa, roberta-{b, l}, xlm-roberta-{b, l}
Decoder-based
LLM (8)
Prompt-based
(Zero/Few-shot)
RAW [57], FSP, RAG, FSP+RAG
LLM: Llama-3.1-8B-Instruct [24]; RAG Embedding:
Qwen2-7B-Instruct [39]; RAG Context: Top-5 retrieved
techniques; PEFT: LoRA [28] (16-bit); LR: 1×10−5
(Emb), 2×10−5; Training: 3 Epochs, Batch Size 4
Weight-based
(SFT)
SFT-RAW, SFT-FSP, SFT-RAG, SFT-FSP+RAG
calculate cosine similarities [48] for every possible pair of
these techniques.
Following prior work [11], we apply a similarity threshold
(𝛿≥0.7) to identify similar pairs and report the percentage
of FPs and FNs whose descriptions fall above the threshold.
Finally, to visually represent the relationships, we project the
embeddings into a two-dimensional space using t-SNE [61],
where points that are close together indicate higher semantic
similarity between their technique descriptions.
3.5
ATT&CK Technique to Control Mapping
Some organizations want to understand attacker technique
trends so they can prioritize the adoption of controls to protect
against them. Within the CTIfecta dataset, each attack cam-
paign is mapped to a ground-truth set of ATT&CK techniques
and their corresponding controls. If an automated method fails
to extract a required ATT&CK technique, the corresponding
controls may also be missed, leaving the organization exposed
to undetected vulnerabilities. To assess the impact of extraction
errors, we map each predicted and ground-truth ATT&CK tech-
nique to its corresponding Proactive Software Supply Chain
Risk Management (P-SSCRM) controls [63]. The P-SSCRM
framework unifies 73 controls (referred to as tasks) across 10
government and industry standards. We use P-SSCRM rather
than native MITRE mitigations because it aligns with the
standards practitioners consult and provides broader cross-
standard coverage with actionable guidance.
Baseline Mapping. We use the ATT&CK technique to
P-SSCRM mapping data published by Hamer et al. [26] as
our baseline. Their original dataset contains 4,453 candidate
mappings of ATT&CK techniques to control pairs spanning
198 attack techniques. Of these, 97 techniques were mapped
using triangulation across four distinct mapping strategies. We
considered these 97 techniques as confirmed baseline mapping.
Extended Manual Mapping Protocol. The above map-
ping dataset also provides individual outputs for each strat-
egy across all techniques. We leverage both the confirmed
mappings and the available strategy outputs to support our
mapping process. Our evaluation dataset contains 82 unique
ATT&CK techniques (§ 3.1), of which 44 are covered by the
confirmed baseline mappings. The remaining 38 out of 82
techniques, therefore, require additional mapping for our anal-
ysis. In addition, we found 6 ATT&CK techniques from the
automated methods’ prediction that are not covered by the
confirmed baseline mappings. Consequently, 38+6=44 tech-
niques were manually mapped to extend the baseline dataset
for this study. For the 44 techniques not covered by the con-
firmed baseline mappings, we analyzed 437 candidate tech-
nique–to–control pairs available in the baseline dataset. We
performed the mapping in two phases. In the first phase, we
applied a filtering criterion to prioritize higher-confidence
candidate pairs: a pair was retained only if it achieved agree-
ment between the manual review strategy and at least one
of the three automated mapping strategies reported in the
baseline dataset. In the second phase, two co-authors inde-
pendently evaluated the remaining pairs by cross-referencing
the MITRE ATT&CK technique descriptions and mitigation
strategies against the objectives, descriptions, and assessment
questions of the corresponding P-SSCRM controls. This in-
dependent review process resulted in 26 inter-rater disagree-
ments, which were resolved by the third author.
Impact Measurement. With the complete mapping estab-
lished, we derive two sets of controls for each attack campaign:
one from the ground-truth ATT&CK techniques annotated in
the CTI reports, and another one from the ATT&CK techniques
predicted by each automated method. Inspired by Hamer et al.
[26], we use metrics to calculate the errors of automated mis-
classifications on mapped controls. First, for each attack cam-
paign, we calculate if each control is: 1 Matched controls:
Controls present in both the ground truth and predicted sets.
2 Missed controls: Ground truth controls absent from
the predicted set, resulting from missed attack techniques. 3
Unnecessary controls: Invalid predicted controls absent
from the ground truth set, resulting from wrong attack tech-
nique predictions. Finally, we calculate control coverage as
the percentage of matched controls divided by the sum of
matched and unnecessary controls.
5


---

ASE ’26, October 12–16, 2026 , Munich, Germany
Haque et al.
3.6
Performance Saturation Analysis
Since no single CTI report captures the full scope of an attack
campaign, aggregating reports is essential, but it raises the
practical question of how many are needed before informa-
tion extraction saturates. To identify the minimum number
of reports required for performance saturation, we perform
a greedy, incremental evaluation for each attack campaign,
adding the most informative reports first. Inspired by the
concept of code saturation [27] (the point at which no new
techniques have been identified), we track the discovery of
techniques as more reports are incorporated. For each cam-
paign, we rank CTI reports by their true-positive contribution,
defined as the number of techniques each report correctly
identifies. If multiple reports contribute the same number of
techniques, we resolve the tie by ordering them alphabeti-
cally by their file names. We then incrementally add reports in
descending order of contribution. After each addition, we cal-
culate the cumulative evaluation metrics (precision, recall, and
F1-score) against a fixed ground-truth reference set containing
all attack techniques for that campaign (§ 3.3).
To identify when additional reports provide limited benefit,
prior work [25] recommends ≤0.05, and we adopt it to define
performance saturation as the point at which improvements
in evaluation metrics fall below this threshold. The number
of reports at this point represents the minimum required to
achieve maximum performance.
3.7
CTI Report Characteristic Analysis
To examine which characteristics of CTI reports influence the
automated extraction of ATT&CK techniques, we select the
best-performing method from each of the three approaches
based on the highest campaign-level recall (§ 3.3). We hy-
pothesize that reports that include more ATT&CK techniques
provide more descriptions of a campaign. We then group re-
ports for each campaign based on the recall saturation point
(identified in § 3.6). Reports that appear prior to the saturation
point and contribute the majority of the true positives are
designated as pre-segment reports, while reports added after
the saturation point are designated as post-segment reports.
Then, for each CTI report in the two groups, we extract the
following features as characteristics to analyze which charac-
teristics influence the automated methods to prioritize reports
in the pre-segment: 1 Word Count: The total number of
words in a report. 2 Sentence Count: The total number
of sentences in a report. 3 Readability Score: The Flesch
Reading Ease score [34], ranging from 1 to 100, where higher
values indicate greater readability. 4 Vendor: The publishing
organization of the report. We hypothesize that some vendors
document CTI reports better than others. 5 Publication
date: The publication date of a report.
Finally, we statistically compare pre-saturation and post-
saturation reports to determine whether their characteristics
differ significantly. For all numeric and ordinal metrics, we
apply the Mann–Whitney U test [43] due to the non-normal
distribution of report characteristics and unequal group sizes.
0
20
40
60
80
100
F1-Score
W_RAW
W_FSP
W_FSP+RAG
W_RAG
FSP+RAG
FSP
RAG
RAW
CySecBERT
SecRoBERTa
tram_multi
scibert_uncased
SecureBERT
roberta-base
DarkBERT
scibert_cased
xlm-roberta-base
SecBERT
bert_uncased
bert-cased
roberta-large
cybert
xlm-roberta-large
no_lemma
base
no_related_words
no_parsing
full
no_pos
Method
63.9
64.5
50.4
51.2
56.0
61.3
56.5
63.5
43.9
58.9
36.3
54.0
45.0
63.0
39.8
58.5
66.2
41.2
55.1
32.4
59.7
38.1
60.6
39.7
64.3
43.5
56.0
35.2
60.8
40.3
59.1
41.5
55.4
37.9
59.3
42.1
58.2
41.6
58.4
43.7
62.4
47.7
57.5
43.3
59.6
45.6
58.4
59.5
55.9
59.0
58.5
67.0
52.9
63.4
57.7
68.2
55.9
68.2
NER
Encoder-based Classification
Decoder-based LLM
Improvement
Decline
Single Report
Multiple Report
Figure 2: Impact of multi-report on ATT&CK technique
extraction. Each dumbbell represents a method’s perfor-
mance shift from Single Report (•) to Multiple Reports (•).
Green lines(—) indicate an improvement with multiple
reports, while red lines (—) indicate a decline.
To quantify the magnitude of differences, we report Cliff’s
delta (𝛿) as a non-parametric effect size measure. We exclude
the vendor from the statistical test because it is a nominal
categorical variable with no inherent ordering. Instead, we an-
alyze vendor distributions descriptively by comparing vendor
frequencies across pre- and post-saturation report sets.
4
Results
RQ 1: How do existing automated attack
technique extraction methods perform at the
campaign level, having multiple reports
compared to a single report?
To answer RQ 1, we replicate 29 methods from the three ap-
proaches mentioned in Table 1 in Buchel et al. [10] on the
campaign with multiple reports and compare them with the
prior single report with respect to precision, recall, and F1-
score. As we have three campaigns and prior studies have two
datasets of single reports, we are averaging the three cam-
paigns’ performance and the two single reports’ performance,
and then comparing the performance between single- and
multiple-report campaigns. To determine the performance dif-
ference, we performed the Mann-Whitney U test [43], and to
measure the effect, we performed Cliff’s delta (Δ). We com-
pared the performance of methods within each approach using
the median, as some methods exhibit skewed performance
distributions, making the median a more robust measure to
minimize the influence of outliers. The results of the F1-score
are shown in Figure 2, and precision and recall are provided
in the replication package.
All eight decoder-based LLM methods demonstrate consis-
tent performance improvements on the multi-report campaign
6


---

Beyond Single Reports: Evaluating Automated ATT&CK Technique Extraction in Multi-Report Campaign Settings ASE ’26, October 12–16, 2026 , Munich, Germany
dataset. The median F1-score increases from 47.67 to 60.12,
corresponding to a relative improvement of 26.1%. This gain
is accompanied by improvements in precision (66.80 →72.10,
+7.9%) and, more notably, recall (43.98 →56.50, +28.5%). The
improvement is statistically significant (𝑝≤0.001) with a large
effect size (Cliff’s Δ = +0.656), indicating an advantage of the
multi-report setting.
All six NER methods also demonstrate consistent improve-
ments on the multi-report campaign dataset, although the
magnitude of improvement is more moderate compared to the
decoder-based LLM approach. The median F1-score increases
from 56.80 to 65.21, corresponding to a relative improvement
of 14.8%. This improvement is accompanied by gains in preci-
sion (55.90 →59.00, +5.5%) and recall (60.00 →64.40, +7.3%).
The observed improvements are associated with very large
effect sizes, with Cliff’s Δ = +1.00, indicating a strong and
consistent advantage of the multi-report setting.
In contrast to decoder-based LLM and NER approaches, all
fifteen encoder-based classification methods demonstrate con-
sistent performance degradation on the multi-report campaign
dataset. The median F1-score decreases from 59.34 to 41.54,
corresponding to a relative decline of 30.0%. This decline is
accompanied by decreases in precision (58.50 →56.10, -4.1%)
and, more severely, recall (61.90 →39.68, -35.9%). The decline
is statistically significant (𝑝≤0.001) with a large negative
effect size (Cliff’s Δ = -1.00).
RQ 1: Overall, our results show that NER and decoder-
based LLM approaches achieve better performance on multi-
reports, whereas the encoder-based classification approach
achieves better performance on a single report. No single
method dominates uniformly across all three campaigns.
SolarWinds
Log4j
XZ Utils
Attack
T1190
T1059
T1566
T1027
T1071
T1105
T1573
T1195
T1036
T1055
MITRE ATT&CK technique
15
15
15
15
15
15
15
15
15
15
14
15
14
15
14
15
12
14
15
11
15
14
13
13
13
12
12
12
11
13
11.0
11.5
12.0
12.5
13.0
13.5
14.0
14.5
15.0
METHODS_FP count
(a) Classification (15 methods)
SolarWinds
Log4j
XZ Utils
Attack
T1190
T1140
T1218
T1041
T1036
T1132
T1082
T1105
T1027
T1059
MITRE ATT&CK technique
8
8
8
8
8
8
8
7
8
8
8
7
8
8
7
8
8
7
8
8
7
8
7
7
8
7
7
7
7
7
7.0
7.2
7.4
7.6
7.8
8.0
METHODS_FP count
(b) LLM (8 methods)
Figure 3: Comparison of false positive (FP) across dif-
ferent approaches of Solarwinds, XZ Utils, and Log4j
attacks. Rows correspond to specific MITRE ATT&CK
techniques, columns represent the attack, and cell values
indicate the number of methods incorrectly predicting
that technique. There are no FPs for the NER approach.
RQ 2: Which attack techniques are most
frequently missed or misclassified by existing
methods, and does semantic similarity
between ATT&CK technique descriptions
contribute to these errors?
To answer RQ 2, we evaluate false positives (FPs) for misclassi-
fied techniques and false negatives (FNs) for missed techniques.
Figures 3 and 4 present the top 10 misclassified and missed
attack techniques across SolarWinds, Log4J, and XZ Utils (de-
tailed counts are available in our replication package). Building
on the embedding analysis described in § 3.4, we examine these
errors to determine how semantic overlap within the MITRE
ATT&CK technique description drives misclassification.
False Positive (FP) analysis: From Figure 3, we observe
that most existing methods consistently misclassify certain at-
tack techniques. For example, T1190: Exploit Public-Facing Ap-
plication, T1059: Command and Scripting Interpreter, and T1566:
Phishing are wrongly predicted by all 15 encoder-based classi-
fication methods, while T1190 and T1140: Deobfuscate/Decode
Files or Information are misclassified by all 8 decoder-based
LLM methods. To understand what drives these consistent er-
rors, we quantitatively analyzed the best-performing method
(SFT RAG). Applying our cosine similarity threshold (≥0.7) re-
veals that a substantial percentage of FPs share high semantic
similarity with the actual ground truth: 33.3% (5/15) for Solar-
Winds, 19.2% (5/26) for XZ Utils, and 12.5% (3/24) for Log4j.
In the t-SNE projection (Figure 5), these highly similar pairs
correspond to the highlighted clusters (dotted blue circled
pairs). For example, T1587: Develop Capabilities is confused
with T1588: Obtain Capabilities, as both describe preparatory
adversarial behaviors. Similarly, T1219: Remote Access Software
maps closely to T1021: Remote Services. Furthermore, these
misclassifications frequently occur within the same tactical
boundaries. Across SolarWinds, XZ Utils, and Log4j, 40.0%
(6/15), 50.0% (13/26), and 79.2% (19/24) of FPs, respectively,
share at least one tactic with their nearest ground-truth tech-
nique, with Defense Evasion and Discovery being the most
frequently shared tactics across all three attacks.
False Negative (FN) analysis: We observe a similar pat-
tern for FNs, where specific ground-truth techniques are con-
sistently missed by existing methods, as shown in Figure 4.
To understand the drivers behind these missed techniques,
we similarly analyze the best-performing method (SFT-RAG)
with a cosine similarity threshold (≥0.7) and reveal that a
notable portion of missed techniques exhibit high semantic
similarity to the incorrectly predicted labels: 20.0% (2/10) for
SolarWinds, 6.7% (1/15) for XZ Utils, and 33.3% (2/6) for Log4j.
In the t-SNE projection (Figure 5), these missed ground-truth
techniques closely cluster near the predicted ones (dotted red
circled pairs). For instance, T1550: Use Alternate Authentication
Material is often missed in favor of T1606: Forge Web Cre-
dentials. Additionally, we observed instances (dotted yellow
circled pair) where an incorrect prediction maps closely to an
FN, such as the confusion between T1090 (FP) and T1665 (FN).
Furthermore, 70.0% (7/10), 73.3% (11/15), and 33.3% (2/6) of FNs
7


---

ASE ’26, October 12–16, 2026 , Munich, Germany
Haque et al.
SolarWinds
Log4j
XZ Utils
Attack
T1195
T1105
T1027
T1199
T1140
T1548
T1553
T1573
T1562
T1072
MITRE ATT&CK technique
6
6
6
6
6
6
6
6
6
6
6
6
6
6
6
6
0
6
6
0
6
6
0
6
6
0
6
6
0
6
0
1
2
3
4
5
6
METHODS_FN count
(a) NER (6 methods)
SolarWinds
Log4j
XZ Utils
Attack
T1195
T1199
T1548
T1021
T1587
T1027
T1105
T1036
T1210
T1505
MITRE ATT&CK technique
15
15
15
15
15
15
15
15
15
15
13
15
15
13
13
9
15
14
15
8
14
13
4
15
0
15
15
0
15
15
0
2
4
6
8
10
12
14
METHODS_FN count
(b) Encoder-based classification (15 meth.)
SolarWinds
Log4j
XZ Utils
Attack
T1199
T1573
T1587
T1195
T1548
T1105
T1027
T1622
T1021
T1553
MITRE ATT&CK technique
8
8
8
8
6
8
7
8
6
5
6
8
6
5
8
7
4
7
5
8
5
8
0
8
5
4
7
8
0
8
0
1
2
3
4
5
6
7
8
METHODS_FN count
(c) Decoder-based LLM (8 methods)
Figure 4: Comparison of false negative across different approaches of Solarwinds, Log4j, and XZ Utils. Rows correspond
to techniques, columns represent campaign, and cell values indicate #methods failing to detect that technique.
10
8
6
4
2
0
t-SNE Component 1
14
12
10
8
6
t-SNE Component 2
T1480
T1098
T1564
T1114
T1606
T1072
T1133
T1124
T1622
T1482
T1007
T1665
T1001
T1484
T1033
T1219
T1499
T1571
T1190
T1496
T1556
T1203
T1486
T1090
T1056
T1588
T1543
T1105
T1036
T1102
T1608
T1016
T1550
T1071
T1589
T1553
T1041
T1560
T1140
T1552
T1573
T1012
T1057
T1053
T1119
T1110
T1027
T1083
T1587
T1518
T1049
T1562
T1070
T1021
T1195
T1082
T1078
T1132
T1568
T1005
T1497
T1218
T1199
T1567
T1059
T1112
T1548
True Positive
False Positive
False Negative
Figure 5: T-SNE projection of ATT&CK technique de-
scriptions, illustrating the semantic similarity between
ground-truth techniques from the SolarWinds campaign
and predictions from the SFT-RAG method.
in SolarWinds, XZ Utils, and Log4J, respectively, share at least
one tactic with their nearest predicted technique, a higher rate
than observed for FPs, with Defense Evasion, Discovery, and
Persistence being the most frequently shared tactics across all
three attacks.
RQ 2: Both misclassified and missed techniques cluster near
their ground-truth counterparts in the embedding space, ac-
counting for up to 33.3% of FPs and FNs. These errors are
further compounded by shared tactics, with up to 79.2% of
FPs and 73.3% of FNs sharing at least one MITRE tactic with
the nearest ground-truth technique.
RQ 3: What is the impact of automated
attack technique extraction performance on
the coverage of mitigation controls?
To answer RQ 3, we first analyze the quantitative performance
of mitigation control coverage across the three automated ex-
traction approaches on the SolarWinds, XZ Utils, and Log4j
datasets. We then qualitatively group the persistently missed
Table 2: Missed controls and mitigation coverage by ap-
proach. Format: Missed Controls (Coverage%). Higher cov-
erage indicates better performance. Total ground-truth
controls are shown in column headers.
Approach
Method
SolarWinds (35)
XZ Utils (32)
Log4j (38)
NER
base
20 (42.9%)
23 (28.1%)
36 (5.3%)
full
19 (45.7%)
21 (34.4%)
33 (13.2%)
no_lemma
20 (42.9%)
23 (28.1%)
36 (5.3%)
no_parsing
19 (45.7%)
21 (34.4%)
36 (5.3%)
no_pos
19 (45.7%)
21 (34.4%)
33 (13.2%)
no_related_words
19 (45.7%)
21 (34.4%)
33 (13.2%)
Encoder-based
classification
CySecBERT
23 (34.3%)
24 (25.0%)
22 (42.1%)
DarkBERT
25 (28.6%)
24 (25.0%)
22 (42.1%)
SecBERT
24 (31.4%)
24 (25.0%)
22 (42.1%)
SecRoBERTa
25 (28.6%)
32 (0.0%)
32 (15.8%)
SecureBERT
23 (34.3%)
24 (25.0%)
22 (42.1%)
bert-base-cased
22 (37.1%)
24 (25.0%)
20 (47.4%)
bert-base-uncased
24 (31.4%)
24 (25.0%)
22 (42.1%)
cybert
23 (34.3%)
24 (25.0%)
21 (44.7%)
roberta-base
25 (28.6%)
24 (25.0%)
23 (39.5%)
roberta-large
22 (37.1%)
24 (25.0%)
22 (42.1%)
scibert_scivocab_cased
25 (28.6%)
24 (25.0%)
22 (42.1%)
scibert_scivocab_uncased
25 (28.6%)
24 (25.0%)
22 (42.1%)
tram_multi_label_model
25 (28.6%)
24 (25.0%)
22 (42.1%)
xlm-roberta-base
25 (28.6%)
24 (25.0%)
22 (42.1%)
xlm-roberta-large
24 (31.4%)
24 (25.0%)
22 (42.1%)
Decoder-based
LLM
prompt_FSP
23 (34.3%)
22 (31.3%)
19 (50.0%)
prompt_RAG + FSP
10 (71.4%)
18 (43.8%)
15 (60.5%)
prompt_RAG
8 (77.1%)
8 (75.0%)
11 (71.1%)
prompt_Raw
11 (68.6%)
21 (34.4%)
11 (71.1%)
weight_SFT Raw
23 (34.3%)
24 (25.0%)
23 (39.5%)
weight+prompt_SFT FSP
15 (57.1%)
20 (37.5%)
14 (63.2%)
weight+prompt_SFT RAG + FSP
8 (77.1%)
17 (46.9%)
9 (76.3%)
weight+prompt_SFT RAG
14 (60.0%)
23 (28.1%)
8 (78.9%)
controls into the P-SSCRM framework groups to identify sys-
temic extraction gaps. Table 2 presents the number of missed
controls and mitigation coverage for each method across the
three attack campaigns. The names of the missed mitigation
controls are provided in the replication package.
Overall, decoder-based LLM methods achieve the high-
est mitigation coverage (77.1%) across all attack campaigns,
whereas NER and encoder-based classification methods miss
the majority of ground-truth controls. For example, the best
NER method (full) achieves 45.7% coverage on SolarWinds
but drops to 13.2% on Log4j, missing 33 of 38 ground-truth
controls. Similarly, the 15 evaluated encoder-based methods
show limited effectiveness, with coverage ranging from 0.0%
to 47.4% (bert-base-cased on Log4j). In contrast, decoder-
based LLM substantially improves coverage, particularly when
combined with RAG. The prompt_RAG method performs best,
8


---

Beyond Single Reports: Evaluating Automated ATT&CK Technique Extraction in Multi-Report Campaign Settings ASE ’26, October 12–16, 2026 , Munich, Germany
achieving 77.1% coverage on SolarWinds and 75.0% on XZ Utils
(both missing 8 controls), while maintaining 71.1% coverage
on Log4j (11 missed controls).
Despite the relative success of decoder-based LLMs com-
pared to NER and classification, failures to map certain controls
reveal critical gaps in the Governance (G), Deployment (D),
and Environment (E) groups of the P-SSCRM framework. Even
the best-performing prompt_RAG method misses controls in
the G, D, and E groups. For example, operational environment
controls (E.3.3, E.3.4, E.3.6, E.3.7), intrusion monitoring (D.2.1),
and supplier management (G.3.4) are consistently omitted by
all 29 evaluated methods across the three attack campaigns.
RQ 3: While decoder-based LLMs with RAG significantly
outperform NER and encoder-based methods, achieving up
to 77.1% mitigation coverage, all 29 evaluated methods exhibit
systemic gaps in the Governance (G), Deployment (D), and
Environment (E) domains of the P-SSCRM framework.
RQ 4: How many CTI reports are required for
automated approaches to reach performance
saturation as additional reports are
incorporated?
To answer RQ 4, we used a greedy incremental evaluation
strategy described in § 3.6. Figure 6 shows cumulative per-
formance (precision, recall, F1) as additional CTI reports are
incorporated, following the incremental evaluation procedure
described in subsection 3.6.
For Precision, NER reaches saturation after a single CTI
report across all three attack campaigns, achieving maximum
precision (1.0). In contrast, encoder-based classification and
decoder-based LLM approaches reach saturation between 11
and 25 reports, with the Log4j campaign requiring 25 reports
with LLMs. At saturation, both approaches stabilize with a
precision range of 0.4 to 0.8.
For Recall, all approaches rise steeply within the first 5 to
10 reports, with most saturating after 10 to 15 reports. How-
ever, decoder-based LLMs on Log4j and XZ Utils campaigns
continue to improve until 22 to 30 reports. At saturation, LLMs
achieve the highest recall across campaigns—0.87 for Log4j,
0.85 for XZ Utils, and 0.75 for SolarWinds. NER achieves mod-
erate recall, ranging from 0.75 for Log4j to 0.35 for XZ Utils,
while encoder-based classification achieves the lowest recall,
ranging from 0.5 for Log4j to 0.33 for XZ Utils.
For F1-score, saturation typically occurs after 5 to 13 CTI
reports, depending on the extraction approach and attack cam-
paign. No single approach consistently dominates across all
campaigns. For example, in the Log4j campaign, NER achieves
the best F1 score and reaches saturation after 5 to 10 reports,
outperforming both encoder-based classification and decoder-
based LLM approaches. In contrast, for the XZ Utils and So-
larWinds campaigns, the decoder-based LLM performs best,
saturating after 6 to 13 reports. Despite these improvements,
the maximum F1-score for the XZ Utils campaign (≈0.53) re-
mains lower than even the lowest F1 score observed for the
Log4j campaign (≈0.61).
RQ 4: While all approaches generally saturate within 5–15
CTI reports, the optimal approach at saturation depends on
the performance metric and attack campaign. NER achieves
perfect precision after a single report, whereas decoder-based
LLM achieves the highest recall but requires up to 30 reports.
Table 3: Cliff’s Δ comparing pre- vs. post-saturation re-
port characteristics. *** 𝑝<0.001, ** 𝑝<0.01, * 𝑝<0.05, ns =
not significant.
Campaign
App.
Words
Sents. Readab.
Days
SolarWinds
NER
0.84***
0.76**
0.16ns -0.30ns
Class.
0.89*** 0.89***
0.28ns -0.28ns
LLM
0.94*** 0.88***
0.12ns -0.21ns
Log4j
NER
0.68**
0.62*
-0.54ns
0.47*
Class.
0.95*** 1.00***
-0.23ns
0.62**
LLM
0.73***
0.64**
-0.32ns
0.20ns
XZ Utils
NER
0.31ns
0.24ns
-0.05ns -0.28ns
Class.
0.76***
0.61**
0.39*
0.46*
LLM
0.48*
0.53*
0.26ns
0.30ns
RQ 5: What characteristics of CTI reports
enable existing attack technique extraction
approaches to perform better?
To answer RQ 5, for each attack campaign and the best-performing
method from each approach, we compare pre-segment and
post-segment reports across five features using the Mann-
Whitney U test, testing whether pre-segment reports score
higher than post-segment reports, with effect sizes reported
as Cliff’s Delta (described in § 3.6). Table 3 summarizes the
results and the exact numbers for each feature of CTI reports
in the supplementary materials.
Report Length (Word Count and Sentence Count). Pre-
segment reports have a significantly higher number of word
and sentence counts than post-segment reports across all three
approaches for SolarWinds and Log4j. XZ Utils follows the
same trend except for NER (Δ = 0.31, 𝑝= 0.131), where the
two groups show comparable lengths. Readability. Readabil-
ity shows no consistent directional difference between pre-
segment and post-segment reports. Cliff’s Δ ranges from −0.54
to 0.39 across campaigns and approaches, with the mix of posi-
tive and negative values indicating the absence of a systematic
trend. The only statistically significant result is XZ Utils under
encoder-based classification (Δ = 0.39, 𝑝= 0.040).
Publication Date. Publication date shows no consistent
directional pattern across campaigns. For Log4j, pre-segment
reports under NER and encoder-based classification have sig-
nificantly more days since disclosure (Δ = 0.47 and 0.62, 𝑝<
0.05), but this pattern does not hold for decoder-based LLM.
For SolarWinds, delta values are negative across all three ap-
proaches, indicating no advantage for earlier or later reports.
Vendor. Pre-segment reports are consistently dominated by
government cybersecurity agencies and established commer-
cial CTI vendors. For the SolarWinds campaign, CISA and
9


---

ASE ’26, October 12–16, 2026 , Munich, Germany
Haque et al.
0
5
10
15
20
25
30
35
40
Number of CTI Reports
0.0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1.0
Precision
0
5
10
15
20
25
30
35
40
Number of CTI Reports
0.0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1.0
Recall
0
5
10
15
20
25
30
35
40
Number of CTI Reports
0.0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1.0
F1 Score
NER - SolarWinds
NER - XZ Utils
NER - Log4j
Classification - SolarWinds
Classification - XZ Utils
Classification - Log4j
LLM - SolarWinds
LLM - XZ Utils
LLM - Log4j
Figure 6: Performance comparison of NER, Encoder-based classification, and decoder-based LLM approaches across
different number of CTI reports. The distinct lines, distinguished by color and marker style, represent the combinations
of the three approaches evaluated across the SolarWinds, XZ Utils, and Log4j attack campaigns.
Google account for ≈60% of pre-segment reports across all
three approaches, while post-segment reports are largely com-
posed of SolarWinds’ own disclosures and secondary sources.
For Log4j, CISA and Apache collectively represent ≈65% pre-
segment reports, whereas post-segment reports span over a
dozen vendors, including Openwall mailing list posts and Fe-
dora. We see the same pattern for XZ Utils.
RQ 5: CTI reports that are longer, contain technical con-
tent, and are from certain vendors consistently enable higher
ATT&CK technique extraction performance. In contrast, read-
ability and publication date show no consistent correlation
with technique extraction performance.
5
Discussion
Security researchers should aggregate CTI reports from
multiple sources rather than relying on a single report
for ATT&CK technique extraction. Our results from RQ 1
show that no single CTI report captures the full ATT&CK
techniques of an attack campaign, and aggregating predictions
across multiple reports consistently improves technique cov-
erage on NER and decoder-based LLM approaches. From RQ 4,
we also observe that saturation is typically reached within 5
to 15 reports with a threshold value of 0.005 in most cases,
suggesting that analysts do not need to collect every available
report. However, for the XZ Utils campaign, we found that the
LLM saturates after 22 reports, with a threshold of 0.001. From
RQ 5, we found that overall, more than 60% of the pre-segment
reports are come from the government agencies (e.g., CISA)
or established commercial CTI vendors (e.g., Google, Apache).
Security practitioners should select extraction approaches
based on their analysis goals. Results from RQ 1 show that
NER achieves perfect precision but the lowest recall, while
decoder-based LLMs achieve the highest F1-score and recall.
Such tradeoffs have direct implications for different security
roles. For example, Security Operations Center (SOC) ana-
lysts and incident responders, who prioritize reducing false
alerts and investigation overhead, may prefer NER. In con-
trast, threat intelligence analysts and detection engineers, who
prioritize comprehensive technique coverage to understand
attacker behavior, may prefer LLM-based extraction despite
higher false-positive rates.
Security analysts should prioritize CTI reports with
rich technical content over readability. Our RQ 5 shows
that report length and technical details have a significant effect
on extraction performance, while the readability score has no
significant effect. Readability scores penalize the inclusion of
hashes, IP addresses, and domain-specific technical terms due
to the long, complex, and unknown tokens they contain. So, a
lower readability score may indicate a higher concentration of
technical details rather than poor writing. Analysts curating
CTI corpora should therefore favor longer, technically detailed
reports, even if they appear harder to read.
Researchers should complement ATT&CK technique
extraction with mitigation-level analysis to better char-
acterize attack campaigns. RQ 3 shows that the best-performing
automated extraction method achieves ≈90% ATT&CK tech-
nique coverage. However, mapping these predicted techniques
to P-SSCRM controls reveals that only 77% of the required
controls are covered. This demonstrates that even a relatively
small number of missed ATT&CK techniques (≈10%) can gen-
erate substantial gaps in control coverage (≈23%), highlighting
the importance of analyzing both ATT&CK techniques and
associated controls to fully characterize attack campaigns.
6
Threats to Validity
Construct validity. Mapping ATT&CK techniques to P-SSCRM
controls introduces potential subjectivity. We mitigate this
by extending the four independent mapping strategies pro-
posed by Hamer et al. [26] with three additional independent
manual mappings to provide diverse perspectives and conver-
gence. Internal validity. Training on AnnoCTR and testing
on CTIfecta introduces potential distributional differences and
10


---

Beyond Single Reports: Evaluating Automated ATT&CK Technique Extraction in Multi-Report Campaign Settings ASE ’26, October 12–16, 2026 , Munich, Germany
missing technique coverage. We mitigate this by augment-
ing the training data with MITRE ATT&CK-derived samples
for techniques absent in AnnoCTR, preserving the long-tail
distribution, and by leveraging domain-specific transfer learn-
ing [1, 41] and data augmentation [22, 56] to improve cross-
dataset generalization. External validity. Our findings may
not generalize to other types of attack campaigns beyond Solar-
Winds, Log4j, and XZ Utils. Additionally, the dataset is limited
to CTI reports collected for these three campaigns, which is
mitigated by the dataset authors [26] through three sampling
strategies designed to achieve theoretical saturation [5].
7
Conclusion
We evaluated 29 state-of-the-art ATT&CK technique extrac-
tion methods spanning three approaches using multiple CTI
reports from the SolarWinds, Log4j, and XZ Utils campaigns.
We found that aggregating multiple reports gives better per-
formance than a single report, with most approaches reaching
performance saturation within 10 to 15 reports. Reports that
are longer and include more technical details contributed the
most to the saturation. Despite the improvement, performance
remains limited; ≈33.3% of misclassifications occur between
techniques sharing the same MITRE tactic. Furthermore, ex-
traction errors disproportionately propagate into controls: the
best-performing method misses only 10% of ATT&CK tech-
niques but results in a 23% gap in controls. Future work should
explore campaign-level multiple reports with technical details
and evaluate multi-modal extraction pipelines that process
command traces alongside plain text, evaluating them against
both ATT&CK techniques and control identification.
8
Data availability
We release the dataset and replication package at https://
figshare.com/s/9ad0a0a0aa4d390b7241.
References
[1] Ehsan Aghaei, Xi Niu, Waseem Shadid, and Ehab Al-Shaer. 2022. Secure-
bert: A domain-specific language model for cybersecurity. In international
conference on security and privacy in communication systems. Springer,
39–56.
[2] Bader Al-Sada, Alireza Sadighian, and Gabriele Oligeri. 2024. MITRE
ATT&CK: State of the art and way forward. Comput. Surveys 57, 1 (2024),
1–37.
[3] Dharun Anandayuvaraj, Matthew Campbell, Arav Tewari, and James C
Davis. 2024. FAIL: Analyzing software failures from the news using LLMs.
In Proceedings of the 39th IEEE/ACM International Conference on Automated
Software Engineering. 506–518.
[4] Vimala Balakrishnan and Ethel Lloyd-Yemoh. 2014. Stemming and lemma-
tization: A comparison of retrieval performances. Lecture notes on software
engineering 2, 3 (2014), 262.
[5] Sebastian Baltes and Paul Ralph. 2022. Sampling in software engineering
research: A critical review and guidelines. Empirical Software Engineering
27, 4 (2022), 94.
[6] Markus Bayer, Philipp Kuehn, Ramin Shanehsaz, and Christian Reuter.
2024. Cysecbert: A domain-adapted language model for the cybersecurity
domain. ACM Transactions on Privacy and Security 27, 2 (2024), 1–20.
[7] Iz Beltagy, Kyle Lo, and Arman Cohan. 2019. SciBERT: A pretrained
language model for scientific text. In Proceedings of the 2019 conference on
empirical methods in natural language processing and the 9th international
joint conference on natural language processing (EMNLP-IJCNLP). 3615–
3620.
[8] David Braue. 2025. Cybercrime To Cost The World 12.2 Trillion Annually
By 2031. https://cybersecurityventures.com/official-cybercrime-report-
2025/ Accessed: March 25, 2026.
[9] Matt Bromiley. 2016. Threat intelligence: What it is, and how to use it
effectively. SANS Institute InfoSec Reading Room 15 (2016), 172.
[10] Marvin Büchel, Tommaso Paladini, Stefano Longari, Michele Carminati,
Stefano Zanero, Hodaya Binyamini, Gal Engelberg, Dan Klein, Giancarlo
Guizzardi, Marco Caselli, et al. 2025. {SoK}: Automated {TTP} Extrac-
tion from {CTI} Reports–Are We There Yet?. In 34th USENIX Security
Symposium (USENIX Security 25). 4621–4641.
[11] Tristan JB Cann, Ben Dennes, Travis Coan, Saffron O’Neill, and Hywel TP
Williams. 2025. Using semantic similarity to measure the echo of strategic
communications. EPJ Data Science 14, 1 (2025), 20.
[12] Jeffrey C Carver. 2010. Towards reporting guidelines for experimental
replications: A proposal. In 1st international workshop on replication in
empirical software engineering, Vol. 1. 1–4.
[13] Minghao Chen, Kaijie Zhu, Bin Lu, Ding Li, Qingjun Yuan, and Yuefei Zhu.
2025. AECR: Automatic attack technique intelligence extraction based on
fine-tuned large language model. Computers & Security 150 (2025), 104213.
[14] Yutong Cheng, Osama Bajaber, Saimon Amanuel Tsegai, Dawn Song, and
Peng Gao. 2024. CTINEXUS: leveraging optimized LLM in-context learning
for constructing cybersecurity knowledge graphs under data scarcity. arXiv
preprint arXiv:2410.21060 (2024).
[15] MITRE Corporation. 2023. Threat Report ATT&CK Mapping (TRAM)
Dataset. https://github.com/center-for-threat-informed-defense/tram. Ac-
cessed: 2025-10-09.
[16] Alan R Dennis and Joseph S Valacich. 2015. A replication manifesto. AIS
Transactions on Replication Research 1, 1 (2015), 1.
[17] LLC MITRE Engenuity. 2023. Threat report att&ck mapper (tram).
[18] Reza Fayyazi, Rozhina Taghdimi, and Shanchieh Jay Yang. 2024. Advanc-
ing TTP analysis: Harnessing the power of large language models with
retrieval augmented generation. In 2024 Annual Computer Security Appli-
cations Conference Workshops (ACSAC Workshops). IEEE, 255–261.
[19] Christiane Fellbaum. 1998. WordNet: An electronic lexical database. MIT
press.
[20] Yu Fengrui and Yanhui Du. 2024. Few-shot learning of TTPs classification
using large language models.
[21] Romy Fieblinger, Md Tanvirul Alam, and Nidhi Rastogi. 2024. Actionable
cyber threat intelligence using knowledge graphs and large language mod-
els. In 2024 IEEE European symposium on security and privacy workshops
(EuroS&PW). IEEE, 100–111.
[22] Lingyu Gao, Debanjan Ghosh, and Kevin Gimpel. 2023. The benefits of
label-description training for zero-shot text classification. In Proceedings
of the 2023 conference on empirical methods in natural language processing.
13823–13844.
[23] Peng Gao, Fei Shao, Xiaoyuan Liu, Xusheng Xiao, Zheng Qin, Fengyuan
Xu, Prateek Mittal, Sanjeev R Kulkarni, and Dawn Song. 2021. Enabling
efficient cyber threat hunting with cyber threat intelligence. In 2021 IEEE
37th International Conference on Data Engineering (ICDE). IEEE, 193–204.
[24] Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey,
Abhishek Kadian, Ahmad Al-Dahle, Aiesha Letman, Akhil Mathur, Alan
Schelten, Alex Vaughan, et al. 2024. The llama 3 herd of models. arXiv
preprint arXiv:2407.21783 (2024).
[25] Greg Guest, Emily Namey, and Mario Chen. 2020. A simple method to
assess and report thematic saturation in qualitative research. PloS one 15,
5 (2020), e0232076.
[26] Sivana Hamer, Jacob Bowen, Md Nazmul Haque, Robert Hines, Chris
Madden, and Laurie Williams. 2026. Closing the Chain: How to reduce
your risk of being SolarWinds, Log4j, or XZ Utils. In 2026 IEEE/ACM 48th
International Conference on Software Engineering (ICSE). IEEE.
[27] Monique M Hennink, Bonnie N Kaiser, and Vincent C Marconi. 2017. Code
saturation versus meaning saturation: how many interviews are enough?
Qualitative health research 27, 4 (2017), 591–608.
[28] Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi
Li, Shean Wang, Liang Wang, Weizhu Chen, et al. 2022. Lora: Low-rank
adaptation of large language models. Iclr 1, 2 (2022), 3.
[29] Yi-Ting Huang, R Vaitheeshwari, Meng-Chang Chen, Ying-Dar Lin, Ren-
Hung Hwang, Po-Ching Lin, Yuan-Cheng Lai, Eric Hsiao-Kuang Wu,
Chung-Hsuan Chen, Zi-Jie Liao, et al. 2024. MITREtrieval: Retrieving
MITRE techniques from unstructured threat reports by fusion of deep
learning and ontology. IEEE Transactions on Network and Service Manage-
ment 21, 4 (2024), 4871–4887.
[30] Ghaith Husari, Ehab Al-Shaer, Mohiuddin Ahmed, Bill Chu, and Xi Niu.
2017. Ttpdrill: Automatic and accurate extraction of threat actions from
unstructured text of cti sources. In Proceedings of the 33rd annual computer
security applications conference. 103–115.
[31] IBM. 2016. IBM Watson to Tackle Cybercrime. https://uk.newsroom.ibm.
com/2016-May-10-IBM-Watson-to-Tackle-Cybercrime Accessed: March
11


---

ASE ’26, October 12–16, 2026 , Munich, Germany
Haque et al.
18, 2026.
[32] Youngjin Jin, Eugene Jang, Jian Cui, Jin-Woo Chung, Yongjae Lee, and
Seungwon Shin. 2023. Darkbert: A language model for the dark side of
the internet. In Proceedings of the 61st annual meeting of the association for
computational linguistics (volume 1: long papers). 7515–7533.
[33] Chris Johnson, Lee Badger, David Waltermire, Julie Snyder, Clem Skorupka,
et al. 2016.
Guide to cyber threat information sharing.
NIST special
publication 800, 150 (2016), 35.
[34] J Peter Kincaid, Robert P Fishburne Jr, Richard L Rogers, and Brad S
Chissom. 1975. Derivation of new readability formulas (automated read-
ability index, fog count and flesch reading ease formula) for navy enlisted
personnel. Technical Report.
[35] Sandra Kübler, Ryan T. McDonald, and Joakim Nivre. 2009. Dependency
Parsing. Synthesis Lectures on Human Language Technologies. Morgan &
Claypool Publishers.
[36] Udesh Kumarasinghe, Ahmed Lekssays, Husrev Taha Sencar, Sabri
Boughorbel, Charitha Elvitigala, and Preslav Nakov. 2024. Semantic rank-
ing for automated adversarial technique annotation in security text. In
Proceedings of the 19th ACM Asia conference on computer and communica-
tions security. 49–62.
[37] Lukas Lange, Marc Müller, Ghazaleh Haratinezhad Torbati, Dragan
Milchevski, Patrick Grau, Subhash Pujari, and Annemarie Friedrich. 2024.
Annoctr: A dataset for detecting and linking entities, tactics, and tech-
niques in cyber threat reports. arXiv preprint arXiv:2404.07765 (2024).
[38] Zhenyuan Li, Jun Zeng, Yan Chen, and Zhenkai Liang. 2022. AttacKG:
Constructing technique knowledge graph from cyber threat intelligence
reports. In European symposium on research in computer security. Springer,
589–609.
[39] Zehan Li, Xin Zhang, Yanzhao Zhang, Dingkun Long, Pengjun Xie, and
Meishan Zhang. 2023. Towards general text embeddings with multi-stage
contrastive learning. arXiv preprint arXiv:2308.03281 (2023).
[40] Xiaojing Liao, Kan Yuan, XiaoFeng Wang, Zhou Li, Luyi Xing, and Raheem
Beyah. 2016. Acing the ioc game: Toward automatic discovery and analysis
of open-source cyber threat intelligence. In Proceedings of the 2016 ACM
SIGSAC conference on computer and communications security. 755–766.
[41] Ling-Hsuan Lin and Shun-Wen Hsiao. 2022. Attack tactic identification
by transfer learning of language model. arXiv preprint arXiv:2209.00263
(2022).
[42] Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Mandar Joshi, Danqi Chen,
Omer Levy, Mike Lewis, Luke Zettlemoyer, and Veselin Stoyanov. 2019.
Roberta: A robustly optimized bert pretraining approach. arXiv preprint
arXiv:1907.11692 (2019).
[43] Thomas W MacFarland and Jan M Yates. 2016. Mann–whitney u test. In
Introduction to nonparametric statistics for the biological sciences using R.
Springer, 103–132.
[44] Christopher D Manning. 2011. Part-of-speech tagging from 97% to 100%:
is it time for some linguistics?. In International conference on intelligent
text processing and computational linguistics. Springer, 171–189.
[45] MITRE. 2026. MITRE ATT&CK™Framework. https://attack.mitre.org/.
Last accessed: 2026-02-24.
[46] MITRE Corporation. 2024. ATT&CK Campaigns. https://attack.mitre.org/
campaigns/ Accessed: March 18, 2026.
[47] Vittorio Orbinato, Mariarosaria Barbaraci, Roberto Natella, and Domenico
Cotroneo. 2022. Automatic mapping of unstructured cyber threat intelli-
gence: An experimental study:(practical experience report). In 2022 IEEE
33rd International symposium on software reliability engineering (ISSRE).
IEEE, 181–192.
[48] Fabian Pedregosa, Gaël Varoquaux, Alexandre Gramfort, Vincent Michel,
Bertrand Thirion, Olivier Grisel, Mathieu Blondel, Peter Prettenhofer, Ron
Weiss, Vincent Dubourg, et al. 2011. Scikit-learn: Machine learning in
Python. the Journal of machine Learning research 12 (2011), 2825–2830.
[49] Joël Plisson, Nada Lavrac, Dunja Mladenic, et al. 2004. A rule based
approach to word lemmatization. In Proceedings of IS, Vol. 3. 83–86.
[50] Fariha Ishrat Rahman, Sadaf Md Halim, Anoop Singhal, and Latifur Khan.
2024. Alert: A framework for efficient extraction of attack techniques
from cyber threat intelligence reports using active learning. In IFIP Annual
Conference on Data and Applications Security and Privacy. Springer, 203–
220.
[51] Md Rayhanur Rahman and Laurie Williams. 2022. From threat reports to
continuous threat intelligence: a comparison of attack technique extraction
methods from textual artifacts. arXiv preprint arXiv:2210.02601 (2022).
[52] Priyanka Ranade, Aritran Piplai, Anupam Joshi, and Tim Finin. 2021. Cy-
bert: Contextualized embeddings for the cybersecurity domain. In 2021
IEEE international conference on big data (Big Data). IEEE, 3334–3342.
[53] Nanda Rani, Bikash Saha, Vikas Maurya, and Sandeep Kumar Shukla. 2023.
TTPHunter: Automated extraction of actionable intelligence as TTPs from
narrative threat reports. In Proceedings of the 2023 australasian computer
science week. 126–134.
[54] Nanda Rani, Bikash Saha, Vikas Maurya, and Sandeep Kumar Shukla. 2024.
Ttpxhunter: Actionable threat intelligence extraction as ttps from finished
cyber threat reports. Digital Threats: Research and Practice 5, 4 (2024),
1–19.
[55] Nils Reimers and Iryna Gurevych. 2019. Sentence-bert: Sentence embed-
dings using siamese bert-networks. In Proceedings of the 2019 conference
on empirical methods in natural language processing and the 9th interna-
tional joint conference on natural language processing (EMNLP-IJCNLP).
3982–3992.
[56] Álvaro Ruiz-Ródenas, Jaime Pujante Sáez, Daniel García-Algora, Mario Ro-
dríguez Béjar, Jorge Blasco, and José Luis Hernández-Ramos. 2025. Syn-
thCTI: LLM-Driven Synthetic CTI Generation to enhance MITRE Tech-
nique Mapping. Future Generation Computer Systems (2025), 108232.
[57] Pranab Sahoo, Ayush Kumar Singh, Sriparna Saha, Vinija Jain, Samrat
Mondal, and Aman Chadha. 2024. A systematic survey of prompt engi-
neering in large language models: Techniques and applications. arXiv
preprint arXiv:2402.07927 1 (2024).
[58] Kiavash Satvat, Rigel Gjomemo, and VN Venkatakrishnan. 2021.
Ex-
tractor: Extracting attack behavior from threat reports. arXiv preprint
arXiv:2104.08618 (2021).
[59] Giuseppe Siracusano, Davide Sanvito, Roberto Gonzalez, Manikantan
Srinivasan, Sivakaman Kamatchi, Wataru Takahashi, Masaru Kawakita,
Takahiro Kakumaru, and Roberto Bifulco. 2023. Time for action: Auto-
mated analysis of cyber threat intelligence in the wild. arXiv preprint
arXiv:2307.10214 (2023).
[60] Wiem Tounsi. 2019. What is cyber threat intelligence and how is it evolv-
ing? Cyber-Vigilance and Digital Trust: Cyber Security in the Era of Cloud
Computing and IoT (2019), 1–49.
[61] Laurens Van der Maaten and Geoffrey Hinton. 2008. Visualizing data using
t-SNE. Journal of machine learning research 9, 11 (2008).
[62] Jonathan J Webster and Chunyu Kit. 1992. Tokenization as the initial phase
in NLP. In COLING 1992 volume 4: The 14th international conference on
computational linguistics.
[63] Laurie Williams, Sammy Migues, Jamie Boote, and Ben Hutchison. 2024.
Proactive Software Supply Chain Risk Management Framework (P-
SSCRM). arXiv preprint arXiv:2404.12300 (2024).
[64] Ming Xu, Hongtai Wang, Jiahao Liu, Yun Lin, Chenyang Xu Yingshi Liu,
Hoon Wei Lim, and Jin Song Dong. 2024. Intelex: A llm-driven attack-level
threat intelligence extraction framework. arXiv e-prints (2024), arXiv–
2412.
[65] Yongheng Zhang, Tingwen Du, Yunshan Ma, Xiang Wang, Yi Xie,
Guozheng Yang, Yuliang Lu, and Ee-Chien Chang. 2025. AttacKG+: Boost-
ing attack graph construction with large language models. Computers &
Security 150 (2025), 104220.
12
