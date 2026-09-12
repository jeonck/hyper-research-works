---
title: Cyber-Attack Technique Classification
id: cyber-attack-technique-classification
tags:
- attack-ontology-drift-cti-85bc51
- pin-rate-survey
created: '2026-09-12T21:32:42.425437Z'
updated: '2026-09-12T21:44:20.476062Z'
source: https://arxiv.org/abs/2411.18755v1
source_domain: arxiv.org
fetched_at: '2026-09-12T21:32:42.424871Z'
fetch_provider: crawl4ai
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'arXiv 2411.18755v1: 0 ATT&CK technique-ID occurrences, below the pin-rate-survey
  inclusion threshold of 3.'
raw_file: raw/cyber-attack-technique-classification.pdf
doi: arXiv:2411.18755v1
---

Cyber-Attack Technique Classification
Using Two-Stage Trained Large Language Models
Weiqiu You
University of Pennsylvania
weiqiuy@seas.upenn.edu
Youngja Park
IBM T.J. Watson Research Center
young_park@us.ibm.com
Abstract
Understanding the attack patterns associated
with a cyberattack is crucial for comprehend-
ing the attacker’s behaviors and implementing
the right mitigation measures. However, major-
ity of the information regarding new attacks is
typically presented in unstructured text, posing
significant challenges for security analysts in
collecting necessary information.
In this paper, we present a sentence classifica-
tion system that can identify the attack tech-
niques described in natural language sentences
from cyber threat intelligence (CTI) reports.
We propose a new method for utilizing aux-
iliary data with the same labels to improve
classification for the low-resource cyberattack
classification task. The system first trains the
model using the augmented training data and
then trains more using only the primary data.
We validate our model using the TRAM data1
and the MITRE ATT&CK framework. Experi-
ments show that our method enhances Macro-
F1 by 5 to 9 percentage points and keeps Micro-
F1 scores competitive when compared to the
baseline performance on the TRAM dataset.
1
Introduction
The rapid growth of cyberattacks, both in numbers
and techniques, presents significant challenges to
companies, often leading to incidents of data theft,
financial losses, and disruptions to critical infras-
tructure. To promptly respond to the cyber threats,
it is vital for security analysts to collect and process
comprehensive information on the threats, includ-
ing the tactics, techniques and procedures (TTPs)
employed in the attacks.
However, much of the information on new cyber
attacks appear in unstructured documents, such as
blogs, news articles and tweets. Although these
cyber-threat intelligence (CTI) reports can provide
valuable insights into the on-going attacks and the
1https://github.com/mitre-attack/tram
evolving threat landscape, collecting relevant in-
formation from a large volume of unstructured re-
ports is very time consuming and labor intensive.
For instance, threat hunters must sift through sev-
eral lengthy documents to understand the attacker’s
TTPs before they can create detection rules and
respond effectively to the attack.
Recently, there have been efforts to auto-
matically extract cybersecurity attack techniques
(TTPs) from CTI reports (Husari et al., 2017; Li
et al., 2022; Legoy et al., 2020; Sauerwein and
Pfohl, 2022; Alam et al., 2023). These existing
tools assign TTP labels to either IoCs (Husari et al.,
2017; Li et al., 2022), short phrases (Alam et al.,
2023), or entire documents (Legoy et al., 2020;
Sauerwein and Pfohl, 2022). These approaches
have limitations. The document-level TTP classi-
fication does not provide actionable insights, e.g.,
how exactly a TTP was used. Security analysts still
must read the documents and find the TTP-related
information manually. The IoC or phrase-level TTP
classification provides partial knowledge and lacks
the contextual information. Further, these methods
typically employ a pipeline system consisting of
several NLP (natural language processing) and ma-
chine learning models. However, the capabilities of
state-of-the-art NLP technologies for cybersecurity
text are still limited. In particular, pipeline-based
approaches can propagate errors where mistakes
from the previous steps negatively impact the per-
formance of subsequent steps. A machine learning
model that is trained end-to-end can address the
error propagation problem.
In this work, we present a novel classifica-
tion model that can classify natural language sen-
tences into their respective TTPs from the MITRE
ATT&CK framework. It is worth noting that gen-
erating a training dataset with a sufficient number
of CTI sentences labeled with TTPs is a highly
challenging task. We propose to solve the data
sparseness in two ways.
arXiv:2411.18755v1  [cs.LG]  27 Nov 2024


---

Technique
TRAM (CTI Report)
MITRE (Description)
Abuse
Elevation
Control
Mechanism
sudo
Adversaries may circumvent mechanisms de-
signed to control elevate privileges to gain
higher-level permissions.
(To bypass UAC) configurable setting for the process to
abuse Other than these, new coding algorithm has been
introduced.
Most modern systems contain native eleva-
tion control mechanisms that are intended to
limit privileges that a user can perform on a
machine.
Access Token
Manipulation
The tokens for each platform are hardcoded within the
sample:November 2016 to January 2017: "Evil New Year"
CampaignIn the early part of 2017, Group123 started the
"Evil New Year" campaign.
Adversaries may modify access tokens to op-
erate under a different user or system security
context to perform actions and bypass access
controls.
The Trojan uses the access token to write the string above
to the first file uploaded to Google drive whose filename
is .txt.
A user can manipulate access tokens to make
a running process appear as though it is the
child of a different process or belongs to
someone other than the user that started the
process.
Access Discovery
This may include information about the currently logged
in user, the hostname, network configuration data, active
connections, process information, local and domain ad-
ministrator accounts, an enumeration of user directories,
and other data.
Adversaries may attempt to get a listing of
accounts on a system or within an environ-
ment.
The PowerShell script collects all possible information on
the user and the network, including snapshots, computer
and user names, emails from registry, tasks in task sched-
uler, system information, AVs registered in the system,
privileges, domain and workgroup information.
This information can help adversaries deter-
mine which accounts exist to aid in follow-on
behavior.
Table 1: Example sentence from CTI data and MITRE ATT&CK data. CTI sentences are extracted from the the
TRAM dataset and contain named entities of specific files and tokens. MITRE data, on the other hand, are general
descriptions of attack techniques, so they are higher level statements of attack techniques’ behaviors.
Firstly, we utilize the TTP descriptions from
MITRE ATT&CK as an additional training data.
MITRE ATT&CK is a knowledge base that con-
tains descriptions of attack tactics, techniques, mit-
igation, software, etc. For each attack technique,
there is a corresponding description of it in the
MITRE knowledge base. We use these descriptions
of attack techniques as additional data to train the
attack technique classification. However, the style
and vocabulary of CTI sentences are very different
from that of the descriptions in MITRE ATT&CK,
as shown in Table ??. In this case, simply adding
the MITRE data to CTI data does not improve the
classification performance. To address this prob-
lem, we introduce a similarity-based data augmen-
tation and a novel two-stage training method. We
first train the classification model using the com-
bined data and then continue training the model
longer using only the CTI data. This two-stage
training allows the model to benefit from the addi-
tional data while minimizing the negative effect of
the out-of-distribution data.
Secondly, we base our classification models on a
large language model (LLM) pretrained with a col-
lection of CTI documents. In recent years, LLMs,
such as BERT (Devlin et al., 2019a), have shown a
superior performance for many NLP applications.
These foundation models are first trained on a large
amount of unlabeled text to gain general seman-
tic knowledge, and then fine-tuned on a relatively
small amount of labeled data to optimize for a spe-
cific task, such as attack technique classification.
We train a BERT model (called CTI-BERT here-
after) using a collection of CTI reports, vulnera-
bility descriptions and security-related academic
publications. Our system leverages the LLM’s abil-
ity to capture the contextual meaning and produces
a higher accuracy than baseline methods.
Our main contributions are the following:
1. We propose a similarity-based two-stage train-
ing pipeline to use selected auxiliary data to
help training with primary data.
2. Our experiments validate the effectiveness
of our method on cyberattack classification,
showing that it improves Macro-F1 scores
significantly while maintaining competitive
Micro-F1 scores.


---

3. We demonstrate how domain-specific LLMs
are very effective in tackling the data sparse-
ness problem.
2
Two-stage Training with LLMs
We aim to build a generic framework for the low-
resourced and imbalanced attack technique clas-
sification task. We solve the problem by utilizing
a small amount of external data. Given a small
primary dataset, DP , and an auxiliary dataset, DA,
our objective is to improve the model’s classifica-
tion performance on DP . We assume that both
primary and auxiliary datasets belong to the same
domain with the same label sets. However, the
writing style and vocabulary in the two datasets
differ significantly, and, thus, simply adding the
auxiliary data to the primary data often deteriorates
the classification results.
We propose a two-stage model training tech-
nique with similarity-based auxiliary data selection
to address the low-resource class-imbalance prob-
lem. Figure 1 shows the high-level architecture of
our approach. We first select part of DA that is
similar to DP and augment the training data with
the selected subset of DA. Then, we fine-tune a
pretrained language model using the augmented
data first and, then, fine-tune the model further in
the second stage only with DP to steer the final
model closer to DP .
2.1
Similarity-based Auxiliary Data
Incorporation on Minority Classes
The simplest way to use auxiliary data would be
to concatenate the two datasets DP and DA. How-
ever, due to the distribution shift, adding auxiliary
data can harm the model’s performance, especially
for the majority classes if the classes already have
some high quality data. To minimize the negative
effect of distribution shift, we augment DP only
for minority classes by adding a subset of DA that
is more similar to DP to training. In this work, we
define a minority class as one having fewer than k
samples.
There are different methods to assess how simi-
lar two sentences are, including minimum-edit dis-
tance (Levenshtein, 1965), cosine similarity (Salton
et al., 1975), dot-product (Salton et al., 1975), etc.
With LLMs, the most widely used method to mea-
sure the sentence similarity is to convert the sen-
tences into their embeddings (i.e., vector represen-
tations) and calculate the cosine similarity between
the sentence embeddings.
We use the embedding-based cosine similarity.
To select similar samples, we use a pretrained lan-
guage model, BERT (Devlin et al., 2019b), to com-
pute the pairwise cosine similarity between DA
c
and DP
c , which represent the auxiliary and primary
data for a class c respectively. For each sentence
sA
i ∈DA
c , its similarity to DP
c is defined as:
Sim(sA
i , DP
c ) = max
sP
j ∈DP
c
cos(h(sA
i ), h(sP
j ))
(1)
where cos(h1, h2)=
h⊺
1h2
||h1||·||h2||, and h(sA
i ) is the
embedding of sA
i . Then, we take the most simi-
lar k −|DP
c | sentences from DA
c to augment DP
c .
This way, we make each minority class have up to k
sentences. We denote the set of sentences selected
based on the similarity to the DP as DA_sim.
2.2
Domain-specific Language Model
Although training on general-domain text data al-
lows BERT to learn the English language, it has
some limitations when we process text in a specific
domain, such as law, medical, and security, etc.
due to their own specific vocabulary. To improve
the performance of security text understanding, we
use a BERT model trained from scratch for the cy-
bersecurity domain using a high quality security
text dataset (Park and You, 2023). The pretraining
dataset contains about 1.2 billion words collected
from various cybersecurity threat intelligence (CTI)
reports covering key security topics such as security
campaigns, malware, threat actors and vulnerabili-
ties. The dataset includes news articles, blogs and
APTnotes2, MITRE datasets on attacks3 and vul-
nerabilities4, academic publications from security
conferences, security textbooks, Wikipedia pages
belonging to the “Computer Security” category.
2.3
Two-stage Model Training
As discussed earlier, simply augmenting the train-
ing data with auxiliary data can deteriorate the per-
formance (see our experiment results in Table 3).
In order to gain back the loss in performance due to
the data distribution shift, we propose a two-stage
training, where we first train a model using both
DP and DA_sim and then train the model more on
DP only. The second stage training can bring the
model closer to DP .
2https://github.com/aptnotes/data
3https://attack.mitre.org/, https://capec.mitre.org/
4https://cve.mitre.org/, https://cwe.mitre.org/


---

Primary Data
DP
Auxiliary Data
DA
Language Model
h
Language Model
h
Sentence Embeddings
eP
1
eP
k
eA
1
eA
n
cosine
similarity
Selected
Auxiliary Data
DA_sim
(a) Cosine-similarity-based Auxiliary Data Selection
Pretrained
Language Model 
h
DP
Intermediate
Model h'
Final
Model hF
DA_sim
Model Training I
Model Training II
DP
(b) Two-stage Model Training
Figure 1: System Overview. For the given primary data (DP ) and auxiliary data (DA), we first select a subset of the
auxiliary samples (DA_sim) based on their similarity with DP . The model training is done using DP and DA_simat
the first stage and then with only DA_simat the second stage.
3
Experiments
We validate our method focusing on the cyber-
attack technique classification task, i.e., classifying
CTI sentences to their attack technique types.
3.1
Data
We use the TRAM5 and MITRE ATT&CK6
datasets as primary and auxiliary data respectively.
The MITRE dataset contains the description for
each attack technique. The TRAM dataset contains
CTI sentences extracted from security news and
technical reports. The sentences are labeled with
the attack techniques from MITRE ATT&CK.
Data Splits and Preprocessing
The original
TRAM dataset has a few limitations. First, it only
has the train and test splits (no validation split), and
the train and test sets are created by duplicating all
examples four times and randomly splitting into a
ratio of 4:1, resulting in many examples appearing
in both splits. Further, MITRE ATT&CK organizes
5https://github.com/center-for-threat-informed-
defense/tram
6https://attack.mitre.org
attack techniques by different targets–Enterprise,
Mobile and Industrial Control Systems, and some
techniques can apply to multiple targets such as
enterprise and mobile. In TRAM, if an attack tech-
nique is used for different targets, they are labeled
as different classes.
For our experiments, we remove all duplicates
from the original train and test splits and combine
the classes with the same name, regardless of the
target systems. Further, to evaluate the model over
all the classes, we remove the classes with fewer
than three examples to make sure that each class
has at least one example in the splits. After these
preprocessing, we obtain 1,491 TRAM sentences
with 73 classes out of the original 264 classes.
We then split the sentences into the train, devel-
opment and test sets in a ratio of 2:1:1. Finally,
we collect the descriptions for the 73 classes from
MITRE, resulting in 2,637 sentences. We use the
pre-processed TRAM data as DP and the MITRE
descriptions as DA.
Data Statistics
Table 2 shows the summary of
our datasets. As we can see, the TRAM data has the
following characteristics: 1) Low-resource: only


---

0
15
30
45
60
75
90
105
Number of Sentences
0
2
4
6
8
10
12
14
Number of Classes
TRAM
0
20
40
60
80 100 120 140
Number of Sentences
0
1
2
3
4
5
Number of Classes
MITRE
Figure 2: Distribution of classes based on the num-
ber of member sentences. The TRAM data is highly
imbalanced, having 14 classes with only 3 sentences
(one each in train, validation and test splits), while the
MITRE data is more balanced, with only 3 classes with
less than 3 sentences.
754 training examples. 2) Unbalanced: 14 classes
have only one sentence in the training split. 3)
Many-classes: 73 classes for this small amount of
training data.
Data Set
DP Train
DP Dev
DP Test
DA
# Sent
754
355
382
2,637
Table 2: Summary of our datasets: 73 classes, 1,491
primary sentences and 2,637 auxiliary sentences.
Figure 2 shows the distribution of class sizes in
MITRE and TRAM. We can see that the MITRE
dataset has a more balanced distribution with few
minority classes, while TRAM has a large number
of classes with only one or a few sentences. Having
only a few sentences makes it hard for the model
to learn to generalize, and thus adding additional
sentences from MITRE can help significantly with
the minority classes.
3.2
Training Details
We fine-tune both the first-stage and second-stage
models for the 73-way multiclass classification.
The classification models are trained for 50 epochs
for each stage, with the batch size of 16 and the
learning rate of 2e-5. After 1,000 warmup steps, the
learning rate is varied according to the formula in
Vaswani et al. (2017). We use the Adam optimizer
with β1 = 0.9, β2 = 0.999, and weight decay of
0.01. The code is implemented using PyTorch and
HuggingFace Transformers7.
We select k = 10 as the threshold cutoff for mi-
nority classes based on preliminary ablations. The
hyper-parameters are selected base on the valida-
tion split of DP (i.e., DP Dev in Table 2). The
experiments are performed on Quadro RTX 6000
or V100 GPUs.
3.3
Baseline Systems
We compare our two-stage classification method
with two baseline methods. The baseline models
are trained once using (1) only the primary data
(DP ) and (2) all of the primary and auxiliary data
(DP +DA). We also compare 2-stage training with
1-stage training for all cases (primary data only, pri-
mary+all auxiliary data, primay+similar auxiliary
data), resulting in 6 different cases.
Furthermore,
we
compare
our
model
with
the
general
domain
BERT
model
(bert-base-uncased)
and
two
other
pre-
trained foundation models for the cybersecurity
domain:
SecBERT (jackaduma, 2022) and
SecureBERT (Aghaei et al., 2023). Similarly to
CTI-BERT, SecBERT8 is a BERT model pre-
trained from scratch using APTnotes, Stucco-data,
CASIE and data from the SemEval-2018 Task-8.
On the other hand, SecureBERT updates the
general-domain RoBERTa model (Liu et al., 2019)
using a security corpus. We fine-tuned these three
baseline models using the same training setup as
described in Section 3.2.
4
Results and Discussion
Table 3 summarizes the results. Note that, for the
DP +DA_sim setting, we augment only minority
classes, which have fewer than 10 sentences, so
that all classes have at least 10 sentences. For each
case, we train five models with five different seeds
and report the average Micro and Macro-F1 scores
7https://github.com/huggingface/transformers
8https://huggingface.co/jackaduma/SecBERT


---

Models
BERT
SecBERT
SecureBERT
CTI-BERT (ours)
Micro Macro Micro Macro Micro Macro Micro Macro
Primary Data Only
(1) DP (baseline 1)
61.2
38.0
63.1
41.6
63.8
43.3
69.1
47.3
(2) DP →DP
61.1
38.5
62.5
42.6
64.6
44.5
67.9
46.5
Augmentation w/ all of auxiliary
(3) DP +DA (baseline 2)
56.0
42.9
59.3
48.0
56.0
43.1
65.7
55.1
(4) DP +DA→DP
61.0
44.9
63.6
50.4
62.9
47.4
70.9
58.0
Augmentation w/ similar auxiliary
(5) DP +DA_sim
59.4
42.4
63.5
48.3
64.0
48.7
70.1
56.8
(6) DP +DA_sim→DP (Proposed) 62.9
44.8
63.8
48.2
65.4
50.2
71.3
56.1
Table 3: Average Micro-F1 and Macro-F1 scores over five runs for different models. ‘→’ indicates two-stage
training. The average standard deviation is 0.014. The best results are highlighted in bold.
Models
BERT
SecBERT
SecureBERT
CTI-BERT (ours)
Micro
Macro
Micro
Macro
Micro
Macro
Micro
Macro
Self Data Augmentation
(a) DP +DP_same→DP
61.6
39.2
63.5
42.7
63.1
41.8
69.1
48.4
(b) DP +DP_swap→DP
61.6
39.2
63.0
42.7
63.1
41.8
69.1
48.4
Using Auxiliary Data
(c) DP +DA_rand→DP
61.6
43.4
63.4
49.1
66.2
49.4
69.0
55.0
(d) DP +DA_sim→DP
62.9
44.8
63.8
48.2
65.4
50.2
71.3
56.1
Table 4: Ablation Results for Minority Class Augmentation. The models augment only minority classes with fewer
than k samples. DP_same oversamples sentences from the same classes ; DP_swap randomly swaps tokens within
each oversampled sentence in DP_same; DA_rand randomly selects examples from DA; DA_sim selects most
similar examples from DA.
over the 5 runs. Micro-F1 shows how accurate the
model is at predicting for all sentences, and Macro-
F1 shows how accurate the model is at predicting
for all classes.
We also perform several ablation studies with
different sampling techniques–oversampling of pri-
mary data and random sampling from auxiliary
data. Further, we compare cases where the auxil-
iary data is incorporated for only minority classes
vs. all classes. The details and the results of the
ablations are shown in Table 4 and 5 respectively.
From these experimental results, we obtain the fol-
lowing findings.
4.1
Auxiliary Data
To evaluate whether adding auxiliary MITRE data
helps with prediction on the primary TRAM data,
we train DP +DA model ((3) in Table 3). We pro-
duce the DP +DA model by simply training with
the combined primary and auxiliary data. The in-
tuition is that, if auxiliary data is in the same dis-
tribution as the primary data, then simply adding it
should already help.
We can see from Table 3 that augmenting TRAM
with MITRE (DP +DA) increases Macro-F1 but
lowers Micro-F1 compared to the results of DP .
MITRE has more evenly distributed data across
classes as shown in Figure 2. The increased Macro-
F1 shows that balanced data helps more classes to
have better performance. However, the fact that
Micro-F1 lowers shows that there is a gap between
the style of DP and DA. This aligns with how DP
contains sentences from CTI reports, while DA
contains sentences from descriptions.
4.2
Two-stage Training
Since simply adding auxiliary MITRE data does
not help, we test the models (4) (DP +DA→DP )
in Table 3 to evaluate if continuing training on
primary data on the model (3) helps. The intuition


---

Models
BERT
SecBERT
SecureBERT
CTI-BERT (ours)
Micro
Macro
Micro
Macro
Micro
Macro
Micro
Macro
(e) DP +DA_randall→DP
60.9
43.6
62.8
49.4
65.3
50.5
69.6
56.8
(f) DP +DA_simall→DP
61.5
43.8
62.4
48.1
64.6
47.5
68.6
53.2
Table 5: Ablation Results for All Class Augmentation. The models augment all classes. DA_randall randomly
selects k examples from each class in DA; DA_simall selects top k similar examples from each class in DA.
(k = 10)
is that, continuing training on only the primary data
might steer the model back to the distribution of
primary data, while keeping the benefit of auxiliary
data on rare classes.
We can see from Table 3 that models (4), com-
pared to models (3), not only gains back Micro-F1,
but also improves more on Macro-F1. This shows
the usefulness of our two-stage training pipeline
in resolving the mismatch between distributions of
TRAM and MITRE.
Moreover, we do a sanity check of whether two-
stage training only benefits from training the model
longer, instead of from auxiliary data. By compar-
ing (4) and (2) in Table 3, we can see that simply
training the model with primary data for longer
does not help with Macro-F1.
4.3
Adding Similar Data to Rare Classes
Since adding MITRE data helps with rare but not
common classes, we ask the question: Can we take
advantage of this and only use it for rare classes?
We add MITRE sentences to these rare classes such
that they have up to k sentences, with rare classes
defined in Section 3.2. In our preliminary experi-
ments, we have tried k = 5, 10, 15 as the threshold,
and k = 10 produced the best Micro and Macro F1
scores on the dev. split, so we use k = 10 for all
our experiments.
Another question lies in how to select the sen-
tences from MITRE to add. A natural way is to add
the sentences that are most similar to TRAM sen-
tences, such that there is less distribution shift. We
use the cosine-similarity-based selection method
described in Section 2.1 to select the most similar
sentences.
We can see from Table 3 that models (6) consis-
tently outperforms (4) in Micro-F1 for all models,
while having competitive Macro-F1. Even for the
one-stage versions, models (5) also outperforms (3)
in Micro-F1 and sometimes Macro-F1. This shows
that selecting more similar data to add to only rare
classes helps the best.
4.4
Rare Classes Only
However, is the performance improvement from
adding similar data, or from adding data to rare
classes, or both? To evaluate if adding auxiliary
data only to rare classes is better than adding to
all classes, we have ablations of models (c) from
Table 4 vs. models (e) from Table 5 and models (d)
from Table 4 vs. models (f) from Table 5. Here,
when we add the examples to all classes, we also
only add up to k = 10 sentences to compare with
the rare class class.
We can see from the comparison between (c) and
(e) that using randomly selected auxiliary data for
only rare classes is better than adding them to all
classes. Similarly, the comparison between (d) and
(f) shows that adding similar auxiliary data for only
rare classes is also better than for all classes.
4.5
Similar vs. Random
To evaluate if selecting similar data is necessary,
we compare with adding randomly selected data
from auxiliary data. The intuition is that, if adding
randomly selected data helps more than adding
data selected by similarity, then there is no need to
select auxiliary data based on similarity.
We can see from (d) vs. (c) in Table 4 and (f)
vs. (e) in Table 5 that selecting similar data helps
Micro and Macro F1s for BERT, but not necessarily
for SecBERT, SecureBERT and CTI-BERT. This
result is surprising to us, but one possible expla-
nation is that security domain foundation models
already have good representations for the security
domain text data. Therefore, they are able to use
random auxiliary data with no worse effectiveness
as similar data. Yet, for a general-domain model
such as BERT, it does not have a good understand-
ing of how sentences in CTI reports relate to the
descriptions of attack techniques. It then need more
supervision from auxiliary data that are more simi-
lar to the primary data.


---

4.6
Auxiliary Data vs. Oversampled Primary
Data
Lastly, to confirm if auxiliary data adds new infor-
mation to primary data, we compare it with simply
oversampling the primary data (see Table 4). We
compare with two oversampling methods: (a) re-
peating sentences and (b) repeating sentences but
with some words swapped within each sentence.
For the auxiliary data, we use both (c) randomly
selected auxiliary data and (d) similarity-based se-
lected auxiliary data. All experiments augment
data only to minority classes. The intuition is that,
if auxiliary data has different information that is
useful for the primary data, then adding it should
produce a better performance than simple data aug-
mentation techniques on just the primary data.
From Table 4, we can see that both adding
similarity-based and adding randomly selected aux-
iliary data boost both Micro and Macro-F1 much
more than data augmentation on primary data alone.
This confirms that we can often benefit from auxil-
iary data even if they are not in the same style as
primary data.
5
Related Work
Attack Technique Classification
Prior work on security information extraction from
threat reports has primarily focused on IoCs and
vulnerabilities (Sabottke et al., 2015; Niakanlahiji
et al., 2019; Shin et al., 2021; Park and Lee,
2022). Recently, several works have proposed vari-
ous methods to automatically extract TTP-related
knowledge from unstructured text.
Rahman and Williams (2022); Bridges et al.
(2017) summarize datasets and methods in CTI
extraction. Tounsi and Rais (2017) define four
CTI categories and discuss existing CTI tools and
research trends. Tuma et al. (2018) review 26 cy-
berthreat analysis methodologies.
Husari et al. extracts threat actions (i.e., TTP)
from the SVO (Subject-Verb-Object) dependency
structure in sentences, where the subject is a mal-
ware instance. The tool considers the object as
a TTP (Husari et al., 2017). Li et al. present
AttacKG which constructs an attack graph by ex-
tracting attack-related entities and entity dependen-
cies from CTI reports. They also construct a tech-
nique template for each attack technique in MITRE
ATT&CK, which is initialized by attack graphs
built upon technique procedure examples from the
MITRE ATT&CK knowledge base. The techniques
used in an attack is determined by aligning the tech-
nique templates with the attack graph built from
CTI reports (Li et al., 2022). Legoy et al. and
Sauerwein and Pfohl explore natural language pro-
cessing (NLP) and machine learning (ML) meth-
ods for automated attack technique classification.
These works take the reference documents listed in
ATT&CK techniques as the labeled training data
and perform a document-level classification, i.e.,
assigning TTP tags to the entire documents (Legoy
et al., 2020; Sauerwein and Pfohl, 2022). Alam
et al. treats the attack technique extraction as a se-
quence tagging task, where the classification model
predicts if each token in the sentence belongs to an
attack pattern. Then, the system takes each contigu-
ous block of attack pattern tokens as a TTP (Alam
et al., 2023).
The difference between ours and the above work
is that these work focus on either a document-level
or IoC-level attack technique extraction, while we
focus on sentence-level classification. Sentence-
level classification is essential for fine-grained anal-
ysis of documents without losing context informa-
tion.
Transfer Learning with Auxiliary Data
Transfer learning is commonly done using unla-
beled data for pretraining. ULMFiT (Howard and
Ruder, 2018) demonstrates the effectiveness of
finetuning pretrained foundation models on down-
stream NLP tasks. BERT (Devlin et al., 2019b)
shows that pretraining on large corpora of text us-
ing masked language modeling and next sentence
prediction helps with downstream tasks that are
finetuned later.
When we do have labeled auxiliary data for trans-
fer learning, we can make better use of them with
specific training pipelines. Li et al. (2020) pro-
poses to use auxiliary data by mixing of auxiliary
data with target data with XMixup (Cross-domain
Mixup) in computer vision. Mixup of data consist
of blending two images together, which is not as
easy to directly use in the text modality. Kung et al.
(2021) is the most similar us and they also use a
two-stage training pipeline. They first select data
samples from auxiliary tasks based on task simi-
larity from pretrained MT-DNN (Multi-Task Deep
Neural Networks), then train MT-DNN model us-
ing the selected samples from auxiliary tasks, and
then finetune the model on the primary task. We,
on the other hand, show that using auxiliary data se-
lected from cosine similarity with primary data of


---

the same class helps for generic single-task models,
without the need for multi-task training.
Data Augmentation
When there is no auxiliary data available, data
augmentation can also help improve the perfor-
mance. Rule-based methods for data augmenta-
tion include token-level perturbation (Wei and Zou,
2019), swapping parts based on dependency trees
(¸Sahin and Steedman, 2018). Wei and Zou (2019)
use token-level pertubation such as insertion, dele-
tion and swap. ¸Sahin and Steedman (2018) swap
parts of sentences base on dependency trees. Xie
et al. (2020) propose to use consistency training to
leverage unsupervised data using supervised data
augmentation methods. Chen et al. (2020) augment
paraphrase identification data by finding paired
nodes in a signed graph data.
Other works like Zhang et al. (2018); Guo et al.
(2020) interpolate between existing examples to
augment data in computer vision or NLP. Oversam-
pling techniques (Chawla et al., 2002; Charte et al.,
2015; Wei and Zou, 2019) mitigate the class imbal-
ance problem and improve the performance for mi-
nority classes. Language models are also used for
data augmentation through back-translation (Sen-
nrich et al., 2016), direct paraphrasing (Kumar
et al., 2019), and replacing tokens by sampling
from a language model’s distribution (Kobayashi,
2018). Back-translation (Sennrich et al., 2016) and
other direct paraphrasing models (Kumar et al.,
2019) can augment data by creasing paraphrases
for sentences in the original dataset. They can also
be used for data augmentation by replacing tokens
by sampling from a language model’s distribution
(Kobayashi, 2018).
We focus on using auxiliary data to augment
primary data. The above traditional data augmenta-
tion methods on a single data source can be used
with our method at the same time.
6
Conclusion
In this paper, we propose a technique using two-
stage training with auxiliary data for attack tech-
nique classification. We demonstrated that adding
selected auxiliary data only to rare classes helps
alleviate the data imbalance issue for the primary
data. The inclusion improves the classification ac-
curacy on rare classes while maintaining compet-
itive accuracy on common classes. Further, we
pretrained our own BERT model, CTI-BERT, and
showcased its effectiveness over existing pretrained
security-domain foundation models.
Although we focused on the cyber-attack classi-
fication task in this paper, our method is general,
model-agnostic, and compatible with any existing
training method. We hope that this work paves the
way for researchers to better utilize auxiliary data
in other domains through the two-stage training
process.
References
Ehsan Aghaei, Xi Niu, Waseem Shadid, and Ehab Al-
Shaer. 2023. SecureBERT: A Domain-Specific Lan-
guage Model for Cybersecurity, pages 39–56.
Md Tanvirul Alam, Dipkamal Bhusal, Youngja Park,
and Nidhi Rastogi. 2023. Looking beyond iocs: Au-
tomatically extracting attack patterns from external
cti. In Proceedings of the 26th International Sympo-
sium on Research in Attacks, Intrusions and Defenses,
RAID ’23, page 92–108. Association for Computing
Machinery.
Robert Bridges, Kelly Huffer, Corinne Jones, Michael
Iannacone, and John Goodall. 2017. Cybersecurity
automated information extraction techniques: Draw-
backs of current methods, and enhanced extractors.
pages 437–442.
Francisco Charte, Antonio J. Rivera, María J. del Je-
sus, and Francisco Herrera. 2015. Mlsmote: Ap-
proaching imbalanced multilabel learning through
synthetic instance generation. Knowledge-Based Sys-
tems, 89:385–397.
Nitesh V. Chawla, Kevin W. Bowyer, Lawrence O. Hall,
and W. Philip Kegelmeyer. 2002. Smote: Synthetic
minority over-sampling technique. J. Artif. Int. Res.,
16(1):321–357.
Hannah Chen, Yangfeng Ji, and David Evans. 2020.
Finding Friends and flipping frenemies: Automatic
paraphrase dataset augmentation using graph theory.
In Findings of the Association for Computational
Linguistics: EMNLP 2020, pages 4741–4751, Online.
Association for Computational Linguistics.
Jacob Devlin, Ming-Wei Chang, Kenton Lee, and
Kristina Toutanova. 2019a. Bert: Pre-training of
deep bidirectional transformers for language under-
standing. ArXiv, abs/1810.04805.
Jacob Devlin, Ming-Wei Chang, Kenton Lee, and
Kristina Toutanova. 2019b. BERT: Pre-training of
deep bidirectional transformers for language under-
standing. In Proceedings of the 2019 Conference of
the North American Chapter of the Association for
Computational Linguistics: Human Language Tech-
nologies, Volume 1 (Long and Short Papers), pages
4171–4186, Minneapolis, Minnesota. Association for
Computational Linguistics.


---

Demi Guo, Yoon Kim, and Alexander Rush. 2020.
Sequence-level mixed sample data augmentation. In
Proceedings of the 2020 Conference on Empirical
Methods in Natural Language Processing (EMNLP),
pages 5547–5552, Online. Association for Computa-
tional Linguistics.
Jeremy Howard and Sebastian Ruder. 2018. Universal
language model fine-tuning for text classification.
In Proceedings of the 56th Annual Meeting of the
Association for Computational Linguistics (Volume 1:
Long Papers), pages 328–339, Melbourne, Australia.
Association for Computational Linguistics.
Ghaith Husari, Ehab Al-Shaer, Mohiuddin Ahmed, Bill
Chu, and Xi Niu. 2017. Ttpdrill: Automatic and
accurate extraction of threat actions from unstruc-
tured text of CTI sources. In Proceedings of the 33rd
Annual Computer Security Applications Conference,
pages 103–115. ACM.
jackaduma. 2022. Secbert. Accessed: 2023-10-10.
Sosuke Kobayashi. 2018. Contextual augmentation:
Data augmentation by words with paradigmatic re-
lations. In Proceedings of the 2018 Conference of
the North American Chapter of the Association for
Computational Linguistics: Human Language Tech-
nologies, Volume 2 (Short Papers), pages 452–457,
New Orleans, Louisiana. Association for Computa-
tional Linguistics.
Ashutosh Kumar, Satwik Bhattamishra, Manik Bhan-
dari, and Partha Talukdar. 2019.
Submodular
optimization-based diverse paraphrasing and its ef-
fectiveness in data augmentation. In Proceedings of
the 2019 Conference of the North American Chap-
ter of the Association for Computational Linguistics:
Human Language Technologies, Volume 1 (Long and
Short Papers), pages 3609–3619, Minneapolis, Min-
nesota. Association for Computational Linguistics.
Po-Nien Kung, Sheng-Siang Yin, Yi-Cheng Chen, Tse-
Hsuan Yang, and Yun-Nung Chen. 2021. Efficient
multi-task auxiliary learning: Selecting auxiliary data
by feature similarity. In Proceedings of the 2021 Con-
ference on Empirical Methods in Natural Language
Processing, pages 416–428, Online and Punta Cana,
Dominican Republic. Association for Computational
Linguistics.
Valentine Legoy, Marco Caselli, Christin Seifert, and
Andreas Peter. 2020. Automated retrieval of att&ck
tactics and techniques for cyber threat reports. CoRR,
abs/2004.14322.
Vladimir I. Levenshtein. 1965. Binary codes capable of
correcting deletions, insertions, and reversals. Soviet
physics. Doklady, 10:707–710.
Xingjian Li, Haoyi Xiong, Haozhe An, Chengzhong
Xu, and Dejing Dou. 2020. Xmixup: Efficient trans-
fer learning with auxiliary samples by cross-domain
mixup.
Zhenyuan Li, Jun Zeng, Yan Chen, and Zhenkai Liang.
2022. Attackg: Constructing technique knowledge
graph from cyber threat intelligence reports. In Com-
puter Security – ESORICS 2022 - 27th European
Symposium on Research in Computer Security, Pro-
ceedings, pages 589–609. Springer Science and Busi-
ness Media Deutschland GmbH.
Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Man-
dar Joshi, Danqi Chen, Omer Levy, Mike Lewis,
Luke Zettlemoyer, and Veselin Stoyanov. 2019.
Roberta: A robustly optimized bert pretraining ap-
proach. arXiv preprint arXiv:1907.11692.
Amirreza Niakanlahiji, Lida Safarnejad, Reginald
Harper, and Bei-Tseng Chu. 2019. Iocminer: Au-
tomatic extraction of indicators of compromise from
twitter. In IEEE International Conference on Big
Data, pages 4747–4754. IEEE.
Youngja Park and Taesung Lee. 2022. Full-stack in-
formation extraction system for cybersecurity intel-
ligence. In Proceedings of the 2022 Conference on
Empirical Methods in Natural Language Processing:
EMNLP 2022 - Industry Track, Abu Dhabi, UAE, De-
cember 7 - 11, 2022, pages 531–539. Association for
Computational Linguistics.
Youngja Park and Weiqiu You. 2023.
A pretrained
language model for cyber threat intelligence. In Pro-
ceedings of the 2023 Conference on Empirical Meth-
ods in Natural Language Processing: Industry Track,
pages 113–122, Singapore. Association for Compu-
tational Linguistics.
Md Rayhanur Rahman and Laurie Williams. 2022.
From threat reports to continuous threat intelligence:
A comparison of attack technique extraction methods
from textual artifacts.
Carl Sabottke, Octavian Suciu, and Tudor Dumitras.
2015. Vulnerability disclosure in the age of social
media: Exploiting twitter for predicting real-world
exploits. In 24th USENIX Security Symposium, pages
1041–1056. USENIX Association.
Gözde Gül ¸Sahin and Mark Steedman. 2018.
Data
augmentation via dependency tree morphing for low-
resource languages. In Proceedings of the 2018 Con-
ference on Empirical Methods in Natural Language
Processing, pages 5004–5009, Brussels, Belgium.
Association for Computational Linguistics.
Gerard Salton, Anita Wong, and Chung-Shu Yang. 1975.
A vector space model for automatic indexing. Com-
mun. ACM, 18:613–620.
Clemens Sauerwein and Alexander Pfohl. 2022. To-
wards automated classification of attackers’ ttps
by combining NLP with ML techniques.
CoRR,
abs/2207.08478.
Rico Sennrich, Barry Haddow, and Alexandra Birch.
2016. Improving neural machine translation models
with monolingual data. In Proceedings of the 54th
Annual Meeting of the Association for Computational


---

Linguistics (Volume 1: Long Papers), pages 86–96,
Berlin, Germany. Association for Computational Lin-
guistics.
Hyejin Shin, WooChul Shim, Saebom Kim, Sol Lee,
Yong Goo Kang, and Yong Ho Hwang. 2021. #twiti:
Social listening for threat intelligence. In WWW ’21:
The Web Conference, pages 92–104. ACM / IW3C2.
Wiem Tounsi and Helmi Rais. 2017. A survey on tech-
nical threat intelligence in the age of sophisticated
cyber attacks. Computers & Security, 72.
Katja Tuma, Gül Çalikli, and Riccardo Scandariato.
2018. Threat analysis of software systems: A system-
atic literature review. J. Syst. Softw., 144:275–294.
Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob
Uszkoreit, Llion Jones, Aidan N Gomez, Ł ukasz
Kaiser, and Illia Polosukhin. 2017. Attention is all
you need. In Advances in Neural Information Pro-
cessing Systems, volume 30. Curran Associates, Inc.
Jason Wei and Kai Zou. 2019. EDA: Easy data augmen-
tation techniques for boosting performance on text
classification tasks. In Proceedings of the 2019 Con-
ference on Empirical Methods in Natural Language
Processing and the 9th International Joint Confer-
ence on Natural Language Processing (EMNLP-
IJCNLP), pages 6382–6388, Hong Kong, China. As-
sociation for Computational Linguistics.
Qizhe Xie, Zihang Dai, Eduard Hovy, Thang Luong,
and Quoc Le. 2020. Unsupervised data augmenta-
tion for consistency training. In Advances in Neural
Information Processing Systems, volume 33, pages
6256–6268. Curran Associates, Inc.
Hongyi Zhang, Moustapha Cisse, Yann N. Dauphin, and
David Lopez-Paz. 2018. mixup: Beyond empirical
risk minimization. In International Conference on
Learning Representations.
