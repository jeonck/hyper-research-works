---
title: Who Shares What? An Empirical Analysis of Security Conference Content
id: who-shares-what-an-empirical-analysis-of-security-conference-content
tags:
- attack-ontology-drift-cti-85bc51
- pin-rate-survey
created: '2026-09-12T21:35:44.554129Z'
updated: '2026-09-12T21:44:32.894383Z'
source: https://arxiv.org/abs/2404.17989v2
source_domain: arxiv.org
fetched_at: '2026-09-12T21:35:44.552709Z'
fetch_provider: crawl4ai
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'arXiv 2404.17989v2: 0 ATT&CK technique-ID occurrences, below the pin-rate-survey
  inclusion threshold of 3.'
raw_file: raw/who-shares-what-an-empirical-analysis-of-security-conference-content.pdf
doi: arXiv:2404.17989v2
---

Who Shares What? An Empirical Analysis of Security Conference Content
Across Academia and Industry
LUKAS WALTER, CLEMENS SAUERWEIN, AND DANIEL W. WOODS
Security conferences are important venues for information sharing, where academics and practitioners share knowledge about new
attacks and state-of-the-art defenses. Despite their importance, researchers have not systematically examined who shares information
and which security topics are discussed. To address this gap, our paper characterizes the speakers, sponsors, and topics presented
at prestigious academic and industry security conferences. We compile a longitudinal dataset containing 9,728 abstracts and 1,686
sponsors across four academic and six industry conferences. Our findings show limited information sharing between industry and
academia. Conferences vary significantly in how equitably talks and authorship are distributed across individuals. The topics of
academic and industry abstracts display consistent coverage of techniques within the MITRE ATT&CK framework. Top-tier academic
conferences, as well as DEFCON and Black Hat, address the governance, response, and recovery functions of the NIST Cybersecurity
Framework inconsistently. Commercial information security and insurance conferences (RSA, Gartner, Advisen and NetDiligence)
more consistently cover the framework. Prevention and detection were the most common topics in the sample period, with no clear
temporal trends.
CCS Concepts: • Security and privacy →Economics of security and privacy; Social aspects of security and privacy; • Social
and professional topics →Computing industry.
ACM Reference Format:
Lukas Walter, Clemens Sauerwein, and Daniel W. Woods. 2026. Who Shares What? An Empirical Analysis of Security Conference
Content Across Academia and Industry. Digit. Threat. Res. Pract. 1, 1 (January 2026), 30 pages. https://doi.org/10.1145/3788676
1
Introduction
Information security knowledge is produced by both academic and industry researchers. However, these two communi-
ties differ in their norms and values, including what constitutes “rigorous” research and the role of peer review. Despite
these differences, both academic and industry researchers value the exchange of knowledge that occurs when experts
convene to present and discuss findings at conferences.
For many professionals in both academia and industry, these events represent important venues for professional
development and community engagement. Attendees often travel internationally and spend significant amounts on
registration fees and related expenses. Although some of these activities are not directly related to formal knowledge
exchange (e.g., hallway discussions and informal extracurricular activities), most participants devote time to listening
to presentations that convey insights into novel attacks, mitigation techniques, lessons learned, and emerging security
concepts.
Despite the substantial investment of time and resources by attendees and their employers, security conferences
have not been systematically studied as part of the security information sharing ecosystem [1–3]. To our knowledge,
no prior research has analyzed the speakers or topics featured at industry conferences. Existing studies on academic
security conferences have primarily focused on bibliometrics [4, 5] and evaluation methodologies [6, 7]. This research
Lukas Walter: University of Innsbruck, Austria; E-mail: lukwalter7@gmail.com
Clemens Sauerwein: University of Innsbruck, Austria; E-mail: clemens.sauerwein@uibk.ac.at
Daniel W. Woods: University of Edinburgh, United Kingdom; E-mail: daniel.woods@ed.ac.uk.
© 2026 Copyright held by the owner/author(s).
Manuscript submitted to ACM
Manuscript submitted to ACM
1
arXiv:2404.17989v2  [cs.CR]  15 Jan 2026


---

2
Lukas Walter, Clemens Sauerwein, and Daniel W. Woods
gap is significant because conferences influence which security topics receive attention, thereby shaping the direction
of research and practice. While conferences provide a platform for selected researchers to present their work, low
acceptance rates necessarily exclude many others.1
To address the research gap, our study characterizes information sharing at leading academic and industry security
conferences by posing the following research questions:
RQ1: Who speaks at security conferences?
RQ2: About which topics?
RQ3: How does this vary by conference and over time?
We collected a dataset containing titles, abstracts, and author or speaker information from four academic and six
industry conferences held between 2014 and 2022. To analyze thematic content, we classified abstracts as offensive,
defensive, or neutral (for theoretical work). Offensive talks were mapped to the MITRE ATT&CK Framework2, and
defensive talks to the NIST Cybersecurity Framework3.
Our contributions are as follows:
RQ1: Among academic conferences, NDSS exhibits the most equitable distribution of speakers, whereas ACM CCS
shows the least. Cross-participation between academic, industry, and insurance conferences is rare. We found no
evidence that sponsorship significantly affects speaker selection at industry conferences.
RQ2: Defensive talks are more common than offensive talks at all conferences except DEFCON. Defensive talks focus
on protective technology, detection, and response. Offensive talks are more evenly distributed across offensive
security categories in MITRE ATT&CK.
RQ3: The distribution of topics remains relatively stable over time. Compared among conferences, DEFCON covers
similar topics to academic conferences. RSA and Gartner emphasize on governance, while cyber insurance
conferences focus on incident response.
Data: The dataset compiled for this study was made publicly available to support replication and further analysis [8].
The remainder of this paper is structured as follows. Section 2 discusses related work in the field of information sharing.
Section 3 describes the research methodology. Section 4 presents the empirical results. Section 5 discusses the limitations
of the study. Section 6 outlines the implications of our findings and provides recommendations. Section 7 concludes the
paper.
2
Related Work
Defenders use and share various forms of security information to better calibrate their defensive posture to the threat
landscape [9, 10]. Most research focuses on sharing real-time technical indicators [2], which we review in Section 2.1.
Other communication channels through which defenders acquire and disseminate security knowledge are discussed in
Section 2.2.
2.1
Information Sharing
The two most common forms of security information sharing are threat intelligence (TI) and vulnerability management.
A range of schema and standards have been introduced to facilitate sharing [11], including MAEC, OVAL, XCCDF,
1The acceptance rates at top-tier academic conferences like IEEE Security and Privacy, USENIX Security, ACM CCS, and NDSS range from 5–20%
depending on the year. Industry conferences like Black Hat, DEFCON and RSA do not report acceptance rates.
2https://attack.mitre.org/ (accessed 19 October 2025)
3https://www.nist.gov/cyberframework (accessed 19 October 2025)
Manuscript submitted to ACM


---

Who Shares What? An Empirical Analysis of Security Conference Content Across Academia and Industry
3
CPE, CVE, and CVSS. Governments have passed regulations to support information sharing [12], funded Computer
Emergency Response Teams (CERTs) to coordinate vulnerability disclosure [13], and directly shared threat intelligence4.
Commercial providers also offer threat intelligence and surrounding services [14–17]. The associated platforms provide
information enrichment and analysis functions to obtain targeted and actionable threat intelligence [16, 18–20].
Recent empirical studies have questioned the quality of threat intelligence. Li et al. [21] find little overlap between
different TI feeds and cannot identify a way to distinguish quality, which confirms findings from other studies [22, 23].
Expert interviews with TI practitioners reveal processes to evaluate quality are informal [24], which is to be expected
given this remains an open research challenge [25]. Encouragingly, a study of threat intelligence during COVID-19
found evidence that collaboration, in the form of aggregating commercial TI feeds, improved coverage of threats [23].
In the area of vulnerability management, bug bounty programs have proliferated, run both independently by
vendors [26] and on platforms like HackerOne [27]. Empirical evaluations support the efficacy of bug bounty programs
over internal testing [28, 29], even though they follow similar processes [30]. Recent work has shown bug hunters in
China organize into teams, in part to facilitate information sharing [31]. However, many firms do not patch even when
the vulnerability is known and the patch is available [32, 33]. This has motivated research into understanding expert
users who apply patches [34, 35], and notifications that nudge firms towards patching [36–38].
The sheer volume of information shared about security vulnerabilities has created a prioritization challenge, making
it difficult for defenders to identify which issues merit attention [39, 40]. Information overload similarly affects threat
intelligence [24]. This motivates research exploring online advice and knowledge sharing that may be easier for the
recipients to digest than technical indicators.
2.2
Advice and Knowledge Sharing
Online forums are often used to solve security and privacy problems [41, 42], including by developers [43]. In some
cases, this involves copying insecure code snippets directly from the forum post [44]. This has motivated research into
how to nudge developers towards better choices [45].
Online security advice targeted at the general public is also widely available [46]. An analysis of over a thousand
sources of advice reveals that the specific recommendations are actionable and comprehensible, albeit with room for
improvement [47]. However, the sources recommended 374 unique behaviors, which leads to information overload [47].
Some users address the quality issue by looking to trusted sources [46].
Conferences address this issue by curating the agenda, via peer review in academia. Research into what information
is shared at these conferences has been small-scale. For example, Carver et al. [6] identify which evaluation method
(e.g., proof or empirical) was used by each paper in the 2015 IEEE Security and Privacy proceedings. This study was
extended to cover the 2016 ACM CCS proceedings [7]. A bibliometric analysis was conducted of around 30,000 academic
computer security papers [4], focusing on statistics like the number of words, authors, and citations in each paper.
We are not aware of analysis of industry conferences, even though practitioner conferences have tens of thousands
of attendees (e.g. 45k at RSA). Across both academia and industry, it remains unclear who speaks/publishes at security
conferences (RQ1), about which topics (RQ2), and how this changes over time and conferences (RQ3).
4https://www.cisa.gov/known-exploited-vulnerabilities-catalog (accessed 19 October 2025)
Manuscript submitted to ACM


---

4
Lukas Walter, Clemens Sauerwein, and Daniel W. Woods
Fig. 1. Two-stage classification process. In the first stage, GPT-based natural language processing is used to classify abstracts. In the
second stage, both GPT and cosine similarity are applied to map abstracts to cybersecurity frameworks.
3
Methodology
We focused on prestigious security conferences, as they exerted the greatest influence within both academia and
industry. Each talk can be analyzed as a video recording, via the associated paper, or metadata such as the abstract
and title. While full academic papers contained the most comprehensive information, their industry equivalents (e.g.,
white papers) were not consistently available. Similarly, video recordings of talks were inconsistently published, and
automated transcription remained imperfect. For these reasons, we relied on abstracts and titles, which were consistently
available across both domains.
Section 3.1 describes our corpus of conference abstracts. Section 3.2 explains the natural language processing (NLP)
techniques used to classify talks. Section 3.3 outlines our validation strategy. Section 3.4 discusses ethical considerations
and open science. Figure 1 provides a high-level overview of our research design.
3.1
Data Collection
Conferences. For academia, we focused on top-tier computer security conferences [48]: USENIX Security, IEEE
S&P, ACM CCS, and NDSS. Cryptography-specific venues were excluded because their focus did not align with
the frameworks considered (see Section 3.2). Journals were also excluded, as the absence of in-person presentations
undermines the comparability with industry conferences.
For industry, we conducted a structured web search for articles featuring the ‘top security conferences’. Only Black
Hat, DEFCON and RSA were consistently included across all identified lists. For example, the SANS Institute hosts
influential topic-specific conferences (e.g. Threat Intelligence or Network Security), but no specific event is consistently
included as the flagship event. We consider these seven conferences to be the most prestigious computer security
conferences.
To diversify our sample, we included Gartner Security - given its influence over procurement decisions - and two
leading cyber insurance conferences (Advisen and NetDiligence). Cyber insurance is increasingly used by firms to
manage cybersecurity risk [49]. Its inclusion offers an informative comparison, particularly because the insurance
community’s roots lay in finance rather than IT. Table 1 displays the conferences in our sample, along with some simple
statistics.
Data Extraction. The dataset used in this study was collected exclusively from publicly available sources, without
reliance on institutional subscriptions or paywalled materials. Data was retrieved directly from official conference
Manuscript submitted to ACM


---

Who Shares What? An Empirical Analysis of Security Conference Content Across Academia and Industry
5
Conference
Sample Window
Type
Talks per year
Characters in title
Words per abstract
𝜇
𝜎
𝜇
𝜎
𝜇
𝜎
Black Hat
2014 - 2022
industry (InfoSec)
252
53.83
54.82
26.43
170.98
99.16
RSA
2017 - 2022
industry (InfoSec)
338.33
34.98
55.69
17.18
75.75
26.98
DEFCON
2014 - 2022
industry (InfoSec)
92.22
32.19
56.10
25.75
176.72
77.72
Gartner Security
2022
industry (InfoSec)
321.0
0.0
68.07
19.38
66.85
20.38
Advisen
2014 - 2022
industry (Insurance)
10.0
4.92
38.81
17.62
58.67
22.25
NetDiligence
2019 - 2022
industry (Insurance)
25.0
6.22
51.50
20.35
36.76
27.36
USENIX Security
2014 - 2022
academic
132.78
68.33
72.30
22.40
184.12
62.10
IEEE S&P
2014 - 2022
academic
82.22
34.08
69.77
21.42
222.52
63.53
ACM CCS
2014 - 2022
academic
166.33
34.47
67.99
21.44
186.21
82.81
NDSS
2014 - 2022
academic
73.0
15.80
72.11
19.79
186.54
82.22
Table 1. Conference metadata. Descriptive statistics showing the mean (𝜇) and standard deviation (𝜎) across all years for the number
of talks per year, title length in characters, and abstract length.
Conference
Sponsors
𝜇
𝜎
Notes
Black Hat
179.0
54.29
RSA
75.0
0.0
contains data only from year 2022.
DEFCON
0
0
Gartner Security
N/A
N/A
sponsor data was not available
Advisen
18.13
5.95
year 2020 is missing.
NetDiligence
56.50
15.32
USENIX Security
15.22
3.33
IEEE S&P
14.67
6.22
ACM CCS
13.87
3.33
year 2018 is missing.
NDSS
10.14
3.27
only years from 2016 - 2022
Table 2. Sponsorship data. Mean (𝜇) and standard deviation (𝜎) of the number of sponsors per conference. Notes indicate data-specific
limitations.
Conference
Gini Index
1
1/N
Black Hat
0.234
0.381
RSA
0.288
0.441
DEFCON
0.179
0.382
Gartner Security
0.328
0.427
Advisen/Zywave
0.244
0.383
NetDiligence
0.159
0.269
USENIX Security
0.284
0.417
IEEE S&P
0.280
0.380
ACM CCS
0.325
0.451
NDSS
0.209
0.376
Table 3. Speaker distribution equality. The Gini index is calculated for the total number of talks per individual across all years. The
two columns report Gini index values under different normalization factors (1 and 1/N).
websites or openly accessible conference proceedings using web content mining techniques. We extracted freely
available metadata, including titles, author names, abstracts, and sponsor lists, as published on conference or publisher
landing pages. Consequently, no special permissions were required from conference organizers or authors. A semi-
automated process was employed to extract information on speakers, affiliations, titles, abstracts, and dates. For
academic venues, we included keynotes and paper presentations for which an abstract was available, excluding poster
sessions. For industry conferences, we considered all talks with an abstract listed in the conference agenda and omitted
Manuscript submitted to ACM


---

6
Lukas Walter, Clemens Sauerwein, and Daniel W. Woods
non-technical sessions such as networking events or welcome remarks. The resulting dataset comprises 9,728 talks
(5,639 industry; 4,089 academic) and 1,686 sponsor entries, of which 451 corresponded to academic and 371 to cyber
insurance conferences.
3.2
Data Analysis
The analysis for RQ1 involved calculating descriptive statistics about the distribution of talks, speakers, and sponsors.
To address RQ2, we applied natural language processing (NLP) methods to classify abstracts according to established
cybersecurity frameworks (Figure 1). This deductive approach mapped textual content to structured taxonomies of
offensive and defensive security practices. Two key decisions guided this analysis: (i) the selection of frameworks and
(ii) the choice of NLP techniques.
Choice of Framework The chosen frameworks would ideally be: (i) comprehensive, (ii) widely recognized in practice,
and (iii) freely accessible. The first criterion ensures us to meaningfully map more abstracts to the framework, which
would not be possible with a digital forensics standard. The second criterion makes our results easier to understand,
since some readers will always be familiar with the categories in the framework. The final criterion enables others to
replicate our work.
For offensive frameworks, we considered MITRE ATT&CK and Cyber Kill Chain framework. ATT&CK framework
offers greater depth, satisfying the first criterion. For defensive frameworks, we evaluated NIST Cybersecurity Framework
(CSF), ISO 27001 and CIS Critical Security Controls. We excluded ISO 27001 due to licensing costs. CIS standard was
excluded because NIST CSF is broader, including governance. Although the choice of framework is important, mappings
between frameworks are widely available5.
NLP Techniques We implemented a two-stage classification process. For the first classification phase, we used
OpenAI’s gpt-3.5-turbo model to classify abstracts as offensive, defensive, or neutral using the following minimal
zero-shot prompt:
“Is this text cybersecurity offensive or defensive (just answer one word, namely: offensive, defensive or
neutral)? <abstract>”
Minimal prompting reduced output variation and improved scalability, as more detailed prompts in pilot tests led to
longer, less consistent, and more ambiguous responses. Neutral talks, which comprise a minority (17%) of the corpus,
are not further classified, as they can not be clearly mapped to either frameworks (see Table 4). They are mentioned
solely for completeness.
For the second stage of the classification, we referred to the official documentation of each standard to establish
themes and sub-themes. For MITRE ATT&CK Framework, we used the 14 tactics as themes and the 196 techniques
as sub-themes. For NIST Cybersecurity Framework, we used the 22 categories as themes and the 98 sub-categories
as sub-themes. We estimated the similarity between each abstract and the corresponding (sub) theme using two NLP
techniques: cosine similarity and a Large Language Model (LLM).
To calculate cosine similarity, we preprocessed text by removing stop words (NLTK stopword list) and lemmatized
terms using WordNetLemmatizer. Texts were represented as embeddings via SentenceTransformer (stsb-mpnet-base-v2)
and compared to framework categories using cosine similarity. This process was applied to both NIST CSF and MITRE
ATT&CK hierarchies.
5For example, CIS Controls v8 mapped to NIST CSF is available here: https://www.cisecurity.org/insights/white-papers/cis-controls-v8-mapping-to-nist-
csf (accessed 19 October 2025)
Manuscript submitted to ACM


---

Who Shares What? An Empirical Analysis of Security Conference Content Across Academia and Industry
7
Talk
Cosine Similarity
gpt-3.5-turbo
Category NIST CSF ATT&CK NIST CSF
ATT&CK
Offensive
0.298
0.452
0.160
0.286
Defensive
0.317
0.411
0.135
0.236
Neutral
0.266
0.342
0.149
0.155
Table 4. Average similarity between talk categories and cybersecurity frameworks, computed using GPT-based classification and
cosine similarity techniques.
For the Large Language Model, we used OpenAI’s gpt-3.5-turbo model using the following zero-shot prompt:
“What are the MITRE ATT&CK tactics that can be identified in the following text. Only return the tactics
which are identified: <abstract>”
A similar prompt was used for the NIST CSF categories. Each theme was queried individually, producing binary (0/1)
outputs per talk. To calculate aggregate similarity to each theme, we took the average across all talks in a specific
sub-sample.
3.3
Validation
Validation was difficult because there is no existing ground truth mapping for abstract talks to cybersecurity frameworks.
Further, frameworks are high-level with blurry boundaries between categories. We employed a three-pronged validation
approach to address these issues, consisting of: (i) human annotation, (ii) cross-method agreement, and (iii) theoretical
consistency.
For human annotation, we manually labeled 264 abstracts and compared these to GPT classification. The model
achieved a 92.4% concordance with the human annotators. Based on the selected sample (𝑛= 264) from the total
population of 𝑁= 9, 728 abstracts, a 95% confidence interval for true population concordance was determined at ±3.16
percentage points. This calculation incorporated the Finite Population Correction (FPC) to accurately reflect the known,
finite size of the total abstract population.
For the cross-method agreement, we compared the topic classifications across NLP techniques. Because cosine
similarity produced continuous values, we applied a threshold to align the number of positive (1) and negative (0)
classifications. We set the threshold such that both GPT and cosine similarity would have the same number of 0s and 1s.
Otherwise the scores could be perfectly aligned, but appear to disagree purely due to setting different thresholds. For
the ATT&CK and NIST Cybersecurity framework categories, the two techniques agreed for 67% and 81% of the abstracts
respectively. This ranged across individual categories, from a low of 52% up to 95% (see Table 5). The categories with
high accuracy are partly driven by the class imbalance as so few defensive abstracts cover Maintenance (from NIST
CSF) or Resource Development (from MITRE ATT&CK).
For the theoretical consistency, we examined whether offensive and defensive talks displayed similarity patterns.
It might be expected that offensive or defensive talks display the highest similarity to the offensive or defensive
frameworks, while neutral talks would exhibit low similarity to both frameworks. Table 4 compares the performance of
the two classification techniques in aligning with our labeling of abstracts as offensive, defensive, or neutral. Specifically,
it presents the average similarity scores between each category of talk and the corresponding cybersecurity frameworks.
The results show that the cosine similarity scores display the expected ranking: defensive talks exhibit the highest
similarity to the NIST CSF (0.317), and offensive talks align most closely with the ATT&CK framework (0.452). However,
this is not true for OpenAI’s gpt-3.5-turbo model, as offensive talks display higher similarity to both frameworks, and
defensive talks display the lowest similarity to NIST CSF.
Manuscript submitted to ACM


---

8
Lukas Walter, Clemens Sauerwein, and Daniel W. Woods
ATT&CK Tactic
Agree
NIST CSF Function
Agree
Credential Access
0.63
Asset Management
0.95
Execution
0.52
Business Environment
0.95
Impact
0.70
Governance
0.90
Persistence
0.56
Risk Assessment
0.84
Privilege Escalation
0.65
Risk Management Strategy
0.93
Lateral Movement
0.79
Supply Chain Risk Mgmt
0.93
Defense Evasion
0.57
Identity Mgmt and Access Control 0.86
Exfiltration
0.71
Awareness and Training
0.90
Discovery
0.52
Data Security
0.90
Collection
0.54
Info. Prot. Processes and Proc.
0.94
Resource Dev.
0.98
Maintenance
0.95
Reconnaissance
0.90
Protective Technology
0.58
Command & Control 0.73
Anomalies and Events
0.65
Initial Access
0.56
Security Continuous Monitoring
0.84
Detection Processes
0.62
Response Planning
0.66
Communications (Respond)
0.78
Analysis
0.67
Mitigation
0.67
Improvements (Respond)
0.65
Recovery Planning
0.79
Improvements (Recover)
0.79
Communications (Recover)
0.81
Mean
0.67
Mean
0.81
Table 5. Agreement between NLP techniques. Fraction of abstracts per category for which the GPT and cosine similarity classifications
are consistent.
Summary These three validation tests indicates that our mapping captures meaningful signal, albeit with considerable
noise - unsurprising given the subjective nature of the task. The GPT method reliably classifies talks as offensive,
defensive or neutral. However, the agreement between NLP techniques is disappointing.
Disagreement results from a mixture of errors/hallucinations and also differences in approach. Cosine similarity
focuses on keywords and phrases used in the descriptions of each framework. This can lead to false positives when
these words are used in a different context, while also leading to false negatives when abstracts use different words
with the same meaning. On the other hand, the GPT method captures how words and phrases are used in the dataset,
which is mainly user-submitted data from the Internet, which is vulnerable to context drift.
Going forward, we will report on aggregate results from OpenAI’s gpt-3.5-turbo as it is a robust, widely used, and
well-documented LLM variant. Aggregating the classifications helps mitigate random errors as these should cancel out.
However, it does not mitigate systemic bias associated with GPT, which we discuss in Section 5. In the Appendix, we
display supplementary figures based on an ensemble model, which outputs an equal weighting of the GPT and cosine
similarity techniques.
3.4
Open Science & Ethics
We release our corpus of titles, abstracts, speakers, and sponsors in an open source repository, as well as our analysis
scripts [8]. We hope this allows other researchers to extend this research project. We discuss these directions in Section 6.
Our primary ethical consideration is the use of personal data—such as author names and affiliations—which we
process and analyze. As this information is already publicly available and tied to individuals’ voluntary participation in
public events, we believe the privacy risks are minimal. While obtaining affirmative consent from all speakers would be
impractical, we acknowledge the concern and have taken care to handle the data responsibly. We believe the value
of this work for open science justifies the approach, though future collaborations with conference organizers could
further strengthen ethical alignment.
Manuscript submitted to ACM


---

Who Shares What? An Empirical Analysis of Security Conference Content Across Academia and Industry
9
Fig. 2. Number of talks presented at each conference from 2014 to 2022.
Fig. 3. Top sponsors of academic conferences aggregated over time (2014–2022). Numbers above the bars indicate sponsorship tier of
each sponsor.
4
Results
This section presents the results of our analysis on the composition of talks and sponsors at each conference (Section 4.1),
speakers (Section 4.2), and abstract topics (Section 4.3).
4.1
Conference Statistics
RSA and Black Hat had the most talks across the sample period (see Figure 2). Volatility in the size of Black Hat since 2019
is driven by the conference introducing/discontinuing sessions like Day Zero, CISO Summit, and Sponsored Workshops.
The academic conferences display the highest rates of growth, as noted by Balzarotti [5]. USENIX Security doubled in
size from 2019 to 2021. The industry conferences do not display the same growth trend. Insurance conferences had the
fewest talks, with the absolute number remaining stable over time. This is perhaps surprising given the market grew by
over 360% between 2015 and 2021 [50].
Manuscript submitted to ACM


---

10
Lukas Walter, Clemens Sauerwein, and Daniel W. Woods
Fig. 4. Relationship between speaker slots and sponsor slots at the Black Hat conference (2014–2022). Each point represents a
company, with the x-axis showing speaker slots and the y-axis showing sponsor slots.
The academic conferences all had the longest abstracts in terms of word count. This should be considered an imperfect
proxy for information content, especially given many conferences have a word limit. Table 1 shows that IEEE S&P
displays the highest average at 223 words. Abstracts at Black Hat and DEFCON had a similar word count to ACM CCS,
NDSS, and USENIX Security. These five conferences have a mean word count of between 170 and 190, which makes
sense given original research is often presented at Black Hat and DEFCON. The conferences (RSA, NetDiligence, and
Advisen) with the lowest word counts place less emphasis on research. There was less variance in the length of titles,
both within and between conferences.
Black Hat has the most sponsors with an average of 197 per year (see Table 2). It is followed by RSA (75), NetDiligence
(57), and Advisen (18). We were unable to find comprehensive sponsorship data for Gartner. The academic conferences
all have between 10 and 16 sponsors per year. DEFCON does not accept sponsors. Conferences with fewer sponsors
typically had longer abstracts.
The academic conferences are sponsored by a mixture of public and private sources (see Figure 3). Large global
technology companies, along with the National Science Foundation, support all four conferences in a similar proportion.
Information security (InfoSec) vendors tend to support specific conferences. Non-profits like the EFF, the FreeBSD
Foundation, and DMTF only sponsor USENIX Security.
Although we could not collect information on the price of sponsorship, the numbers on top of the bars in Figure 3
represent the average sponsor tier of that company, where 1 is the highest. This shows that the non-profits like EFF are
consistently in lower tiers, while BigTech companies tend to be in the higher tiers. However, the US-based National
Science Foundation is most consistently a tier one sponsor. No other country has an equivalent research institution that
consistently sponsors these conferences.
The industry conferences are mainly sponsored by InfoSec vendors, with large technology companies sponsoring
less frequently. This can be seen in Figure 19 in the Appendix. The analysis of sponsors of industry conferences is
less comprehensive because of gaps in the data. The insurance conferences contain a wide range of sponsors (see
Figure 19 in the Appendix). These include not just insurance companies, but also law firms, digital forensics providers,
communications consultants, and data analytics firms. This is likely because these firms receive work from insurers [51].
To probe whether sponsorship influences the number of talks, we analyze the only industry security conference for
which we had longitudinal sponsor information, namely Black Hat. Across all years, the conference had 592 unique
Manuscript submitted to ACM


---

Who Shares What? An Empirical Analysis of Security Conference Content Across Academia and Industry
11
sponsors and 1493 unique affiliation across speakers, which had an intersection of just 219. This means that 85% of the
speakers’ affiliated organizations never sponsored the conference, and 63% of sponsors did not have an affiliated speaker
at Black Hat. Figure 4 shows the relationship between number of times an organization sponsored Black Hat and the
number of affiliated talks. The two outliers are Microsoft and Google, who respectively had 61 and 55 affiliated talks.
4.2
Speaker Statistics
This subsection examines the distribution of abstracts among specific individuals. At industry conferences, the individual
typically presents at the conference, sometimes joint with others. However, just one author typically presents at academic
conferences. We consider each type of talk separately to account for this, using “author” as the terms for individuals
associated with academic talks. Throughout we assume that each unique name corresponds to a single unique person.
Figure 6 shows there is minimal overlap of speakers between industry, academic, and insurance conferences. For this
reason, we proceed by analyzing each type of conference separately.
Figure 5 displays the individuals with the most associations with talks, weighted by 1
𝑛where 𝑛is the number of
authors on a paper or individuals on a panel. Patrick Wardle is a dramatic outlier with 33 talks including more than ten
talks at each of Black Hat and DEFCON. The rest of the top 30 industry information security speakers gave between
10 and 15 talks across all four conferences. Some industry speakers presented exclusively at one conference, such as
Patrick Hevesi at Gartner. No other Top 30 speaker gave a talk at Gartner. The top insurance speaker had seven talks in
total and just 19 speakers gave more than three talks.
Turning to the academic talks, the top authors have over fifty publications, although rarely as a single author.
Academics are more likely to publish at multiple conferences than industry speakers. For example, all the top 30 authors
have presented at IEEE Security and Privacy, USENIX Security and ACM CCS, although some authors did not present
at NDSS. This kind of analysis raises the question of how speaking slots are distributed among participants.
Table 3 displays the Gini index for each conference. A score of 0 means all speakers gave the same number of talks,
while a score of 1 means one individual gave all talks. Academic conferences are similarly equal to industry conferences
when publications count as 1
𝑛where 𝑛is the number of co-authors/co-panelists, whereas academic conferences appear
considerably less equal when each publications counts as 1 (see Table 3). This corrects for academics who make small
contributions to high 𝑛papers. Both metrics agree that NDSS is the most equal academic conference, while ACM CCS
is the least.
4.3
Content of Talks
We now explore the topics of abstracts. Figure 7 shows that defensive talks are more common than offensive and neutral
talks at all conferences apart from DEFCON, which is explicitly set up for hackers to present their research. At DEFCON,
64% of the talks were offensive and just 15% (20%) of the talks were defensive (neutral). Across both cyber insurance
conferences, just 1% of talks were classified as offensive, whereas 55% of insurance talks were neutral and 44% were
defensive. The academic conferences all accepted more defensive work than offensive, and some even accepted more
neutral than offensive talks.
4.3.1
Defensive Talks. Figure 8 shows that the similarity of talks across areas of NIST CSF has remained relatively stable
over time. There is a slight trend of increasing abstracts about risk assessment and governance, as well as decreasing
similarity to protective technology. This is generally true when considering trends in topics at individual conferences,
and we display some such figures in the Appendix. For this reason, we proceed by analyzing the abstracts aggregated
Manuscript submitted to ACM


---

12
Lukas Walter, Clemens Sauerwein, and Daniel W. Woods
Fig. 5. Number of talks per individual for the 30 most frequent speakers from 2014 to 2022 across industry, academic, and insurance
conferences.
Manuscript submitted to ACM


---

Who Shares What? An Empirical Analysis of Security Conference Content Across Academia and Industry
13
Fig. 6. Overlap of speakers across conference types. The Venn diagram shows intersections among industry, InfoSec, and insurance
venues during 2014–2022.
Fig. 7. Distribution of offensive, defensive, and neutral talks at each conference from 2014 to 2022.
Fig. 8. Similarity score of defensive talks mapped to the NIST Cybersecurity Framework over time (2014–2022).
across all years. The NIST Cybersecurity Framework is divided into five core functions: Identify, Protect, Detect,
Respond and Recover.
Manuscript submitted to ACM


---

14
Lukas Walter, Clemens Sauerwein, and Daniel W. Woods
Fig. 9. Similarity score of DEFCON defensive talks mapped to the NIST Cybersecurity Framework over time (2014–2022).
Before analyzing the aggregate data, there is one exception to the general lack of a temporal trend in topics. Figure 9
shows how DEFCON displayed a considerable temporal shift towards Detection and Response functions of NIST CSF.
This could be evidence of the conference’s commercialization, which is an ongoing topic of discussion. The equivalent
figures for other conferences can be found in the Appendix.
Identify. The identify function comprises the first six rows in Figure 10. Broadly speaking, Identify covers how
organizations make security decisions. Both industry InfoSec and insurance talks address these topics more than the
academic talks. The insurance conferences and Gartner display high similarity to Risk Assessment, which captures the
likelihood and impact of different security incidents, and Governance, which cover the process of establishing a security
policy. It is also notable that the research-oriented industry information security conferences (DEFCON and Black Hat)
display less similarity to Identify. Notably, there is low similarity to the final two sections: Risk Management Strategy
involves understanding the firm’s meta-reasoning like the assumptions and risk tolerance of the firm, meanwhile Supply
Chain Risk Management involves assessing the risk of external firms. Academics study this area when they conduct
threat modeling [52, 53].
Researchers should not dismiss the Identify function as ‘non-technical’ and outside the scope of computer security.
Many of the Identify tasks can be solved using technical data. For example, a recent SoK on asset discovery highlights
how Asset Management can be approached using network measurements [54]. Similarly, Risk Assessment is analogous
to cyber incident prediction, which has been studied as a machine learning problem based on technical indicators and
published at top-tier venues [55, 56].
Protect. The protect function covers the next six rows in Figure 10. Broadly speaking, Protect describes technical
controls and organizational processes that directly prevent incidents from occurring. Of these six categories, all
conferences had the most similarity to Protective Technology. Figure 11 displays cosine similarity to each sub-category
of Protective Technology. The two sub-categories with the highest similarity concern system hardening (PR.PT-3) and
network security (PR.PT-4). The next two subcategories concern audits and logging (PR.PT-1), and removable media
(PR.PT-2). Finally, resilience mechanisms like fail-safe and load balancing (PR.PT-5) display the lowest similarity.
Academic talks display some similarity to Identity Management and Access Control. This include the evergreen
research topic that is passwords [57, 58]. The Awareness and Training category received more coverage in the industry
talks relative to the academic talks [59]. Academic research related to this may instead be presented at conferences
focusing on Human-Computer Interaction like SOUPS and Chi [60].
Manuscript submitted to ACM


---

Who Shares What? An Empirical Analysis of Security Conference Content Across Academia and Industry
15
Fig. 10. Similarity score of defensive talks mapped to the NIST Cybersecurity Framework over time (2014–2022).
Fig. 11. Cosine similarity score for talks within the Protective Technology function of the NIST Cybersecurity Framework from 2014 to
2022.
The remaining three categories had low similarity. Maintenance had the lowest similarity across all of the defensive
categories. This finding supports the observation that researchers often overlook maintenance even though it is crucial
to successful operations [61]. The Information Protection Processes and Procedures category consists of procedures to
ensure availability like back-ups, recovery plans and so on. Industry talks more frequently cover these topics. Low
similarity to Data Security was perplexing given this is so core to computer security. The first two sub-categories
of Data Security, namely data at rest and in transit, are core academic topics. However, the other sub-categories are
organizational procedures that tend not to be covered at academic conferences.
Detect. The next three rows concern network monitoring and incident detection. Broadly speaking, all of the
industry conferences displayed moderate similarity to Security Continuous Monitoring, Anomalies and Events, and
Detection Processes. These three categories respectively correspond to: what monitoring technology is in place; how
anomalies are identified and responded to; and the surrounding organizational processes like testing, communication,
and improvement. NDSS displays higher similarity than the other academic conferences to all three Detect categories,
Manuscript submitted to ACM


---

16
Lukas Walter, Clemens Sauerwein, and Daniel W. Woods
Fig. 12. Similarity score of offensive talks mapped to the MITRE ATT&CK framework over time (2014–2022).
which likely results from the conference’s focus on network security. Across the five NIST Cybersecurity framework
functions, the abstracts were most consistently similar to Detect.
Respond. The respond function comprises the next five rows, which are broadly the steps taken to investigate and
contain an incident. This does not capture coordinated response, such as botnet take downs [62]. Abstracts were most
similar to Response Planning, which involves establishing incident response procedures before the incident occurs.
The talks also displayed reasonable similarity to Mitigation, which involves actions to contain and resolve an incident,
and also Improvements, which is about extracting lessons learned from incidents. This is perhaps surprising given the
consensus that the security community struggles to extract lessons from incidents [63].
There was low similarity with the Analysis category, which includes forensic investigations and vulnerability
disclosure policies, especially at academic conferences. This could be because researchers present at specialist venues
like Digital Investigation [64]. There was relatively low similarity to Communications, which involves coordinating with
internal and external stakeholders like law enforcement, especially at academic conferences.
Much like with Detect, NDSS displays higher similarity to than the other academic conferences. The insurance
conferences, especially NetDilligence, display remarkably high similarity to all five categories. The high level of similarity
holds even for Communications despite the other conferences largely ignoring this topic, which supports the theme that
insurers have a different perspective on security.
Recover. The final function comprises three categories that all happen post-incident, which all have equivalent
categories in the Response function. All conferences show less similarity to the Recover category. This suggests conference
talks are more focused on short-term tasks like containing the incident than the long-term goal of restoring the victim
to previous function, which is the goal of Recover. The Advisen conference displays the most similarity, which makes
sense given recovery is the goal of insurance.
4.3.2
Offensive Talks. We mapped offensive talks to the MITRE ATT&CK framework. This consists of 14 tactics and
each tactic has multiple techniques. Gartner, Advisen and NetDilligence are not displayed due to a lack of offensive
talks.
Manuscript submitted to ACM


---

Who Shares What? An Empirical Analysis of Security Conference Content Across Academia and Industry
17
Fig. 13. Similarity score of offensive talks mapped to the MITRE ATT&CK framework across conferences.
Much like with defensive talks, Figure 12 displays no clear temporal trend in which offensive tactics are covered by
conference abstracts. There is, however, a subtle trend towards Impact. We group the 14 tactics into temporal categories:
Pre-compromise, First Compromise, Expansion, and Outcome.
Pre-Compromise. The Reconnaissance and Resource Development tactics involve collecting information and other
resources (e.g. acquiring exploits) before the attack is launched. Resource development is the tactic that the conferences
are least similar to. Reconnaissance, which involves techniques like active scanning and gathering information on the
victim’s network, is also very rarely covered by talks. These tactics may be infrequently discussed because they are
non-technical.
First Compromise. The next four tactics concern how the attacker compromises the first system on a network.
Initial Access describes the entry vector into the network, which includes different types of phishing and account
compromises. The industry talks conferences display moderate similarity to Initial Access. USENIX Security abstracts
are most similar to this among the academic conferences. This breaks from the trend that NDSS talks were most similar
to the NIST Cybersecurity Framework out of the academic conferences.
Execution describes tactics that attackers use to run malicious code on the victim’s systems. The industry talks display
the most similarity to this category, in particular the Black Hat talks. The academic talks are highly similar to this
category, but it is not the highest. Figure 14 displays the similarity of the tactics within Execution.
Persistence describes how attackers maintain access across events like the user rebooting, switching user or any other
interruption. It is discussed most often at DEFCON, with Black Hat talks the second most similar. The other conferences
display relatively low similarity. This suggests that academic researchers are most concerned by the initial vulnerability,
and not how the adversary maintains access to the system.
Privilege Escalation techniques allow an attacker to gain more permissions to access files and other system resources.
This technique shows a similar pattern to Persistence, in which academic talks display low similarity relative to industry
conferences. USENIX Security talks have the most similarity out of the academic conferences.
Expansion. The next three steps concern how the attacker moves through a victim’s network. Defense Evasion
concerns how the adversary avoids detection. The talks display a high similarity to this and also Discovery, which
Manuscript submitted to ACM


---

18
Lukas Walter, Clemens Sauerwein, and Daniel W. Woods
Fig. 14. Cosine similarity score for talks classified under the Execution technique category of MITRE ATT&CK framework across
conferences.
concerns how the adversary collects information about the victim’s network. Unlike the previous tactics, the academic
talks display higher similarity to both than the industry talks.
Credential Access involves stealing account names and passwords, such as via keylogging. The conference talks
are only moderately similar to this, with academic talks showing more similarity than industry. The conference talks
display low similarity to the third tactic in this category, namely Lateral Movement. It covers how the adversary moves
through the victim’s network.
Outcome. These tactics concern what was achieved by the compromise, although these techniques could also be
used to expand access. Collection concerns identifying and gathering data on the victim network. It is the tactic in this
category with the highest similarity to the conference talks. Meanwhile, Exfiltration concerns how the data is stolen
from the network, which has reasonably low similarity to the conference talks.
The Command and Control tactic involves establishing communication channels to maintain control over the infected
systems. This has moderate similarities across both industry and academia. The NDSS conference displays the highest
similarity, again because this is fundamentally a problem of distributed computing, albeit an illegal one. Finally, the
Impact technique concerns an effort to “manipulate, interrupt, or destroy your systems and data”, which would involve
ransomware for example. The academic talks display higher similarity to this category, although it is moderate-high for
all conferences apart from RSA.
5
Threats to Validity and Limitations
Our study has several limitations that affect the interpretation and generalizability of the results.
Threats to External Validity (Generalizability) Missing Data: Our comparative longitudinal study was impacted
by changes in reporting and missing data. We could not collect some years of talks due to data unavailability.
Our longitudinal dataset is affected by occasional missing years or incomplete sponsor information, particularly
for some industry conferences. For example, the RSA conference was created in 1991 but we could only extract the
program from 2017 onward. Similarly, there was a lot of missing sponsorship information, which led to a long list
of exceptions to the sponsors column in Table 2. These omissions mean that 13 of the 74 expected conference-year
sponsorship data points (approximately 17.6%) are missing from the analysis. This lack of data systematically biases
Manuscript submitted to ACM


---

Who Shares What? An Empirical Analysis of Security Conference Content Across Academia and Industry
19
aggregate statistics toward the better-documented conferences and limits the completeness of the longitudinal trend
analysis. Future releases of our dataset will incorporate missing years as additional data become publicly available.
Threats to Construct Validity (Measurement) Real Names: Counting authors can be complex because two unique
names may correspond to the same individual (e.g. Emma Jones and Emma Q. Jones), and one name may correspond to
multiple individuals (e.g. Emma Jones from New York and Emma Jones from California). Additionally, some authors
may use pseudonyms rather than their real names. For simplicity, we counted unique names as unique people. We
considered using affiliations to distinguish between two unique individuals with the same name, but researchers switch
institutions too often for this to be reliable.
Similar issues are present for company names. Company names are inconsistently abbreviated (Hewlett Packard vs
HP), subsidiaries and even departments are listed (e.g. both Microsoft Corporation and Microsoft Research were listed
as sponsors), and some companies change names (e.g. Facebook to Meta). We fixed such issues manually where we
could, but we likely missed instances for less well known companies. This fragmentation is estimated to affect less than
2% of total unique entities after manual correction, primarily impacting measures of speaker concentration and sponsor
overlap but not materially changing overall long-term trends.
Classification: Mapping abstracts to categories from security frameworks is challenging because: (i) the task is
inherently subjective; (ii) the categories are high-level with fuzzy boundaries; (iii) abstracts typically focus on specific
technological systems; and (iv) even state-of-the-art LLMs are known to have errors, let alone the version we used that
is now far from state-of-the-art. These factors help to explain why the agreement between the two NLP techniques (see
Section 3.3) was disappointing. Ultimately, we focused on the LLM-based mapping because it was the best available
technique at the time of the initial analysis and it captures how language is used in real discussions in the LLM’s
training set. This was also confirmed by the results of manual annotation: 264 abstracts (2.7% of the corpus) were
validated, achieving a 92.4% agreement (95% CI ±3.1 pp) and a Cohen’s kappa coefficient of 0.89 with human annotators.
However, residual errors and category ambiguities are still possible. This can be contrasted against the cosine similarity
approach, which is trained on a bag-of-words extracted from official documents. However, it is not unreasonable to
prefer a different mapping, such as using another NLP technique or another cybersecurity framework. To enable this,
we open-source our data and analysis scripts [8].
Conference Coverage: Our comparative analysis (RQ3) would have been more interesting if we collected data from
more conferences and also went further back in time. For example, the FIRST Conference on Computer Security Incident
Handling would likely have covered more topics related to Respond, but from a more technical perspective than the
insurance conferences. The core challenge to adding more data is that we could only semi-automated our scrapers in
order to ensure data quality, and had to create a new parser for each conference. This made it costly to add additional
conferences and also to scrape further back in time. Again, we hope that open-sourcing our data and analysis will allow
future work to extend our work by adding new conferences.
Threats to Internal Validity (Causality): Our results are descriptive, not causal. While we discuss possible
explanations for observed patterns (e.g., topic prevalence or speaker concentration), these should not be interpreted as
evidence of causation. Since our study is based on descriptive data, we explicitly avoid making causal claims to prevent
threats to internal validity.
6
Discussion
This section discusses the results and how our framing assumptions influenced the analysis.
Manuscript submitted to ACM


---

20
Lukas Walter, Clemens Sauerwein, and Daniel W. Woods
Speakers Academic conferences display greater information sharing across venues than industry. Many industry
speakers present at only one conference, and speakers rarely cross the insurance–InfoSec line (see Figure 6). It is unclear
whether industry conferences would benefit from more cross-pollination. The call for broader information sharing is
appealing, however it could be that more efficient communication is enabled by the shared language and assumptions
within each community.
A common question is whether sponsorship buys influence [65]. Conferences with more sponsors have fewer
words per abstract, which could be interpreted as sponsored conferences involving less complex talks. However, the
relationship between sponsorship and speaker selection appears limited. For example, at Black Hat — the event with
the largest number of sponsors — 63% of sponsors never had an affiliated talk, and 85% of speakers’ organizations never
sponsored the conference. Nevertheless, sponsorship patterns raise concerns for academic conferences. Despite focusing
on privacy, two of the five most frequent sponsors of academic conferences directly profit from behavioral advertising.
The relationship between BigTech companies and researchers has been called into question by other researchers [66].
A similar question is whether it is a problem that a small number of speakers/authors hold the majority of influence.
For illustrative purposes, we can compare the Gini index for conferences (see Table 3) to the index of income inequality
in specific countries. The distribution of talks across speakers is typically around 0.37–0.44, which is close to the post-tax
distribution of income in relatively unequal societies like the US (0.375) and Mexico (0.42). All prestigious industry and
academic talks have higher inequality than Germany (0.296).6 Inequality in academic talks is not necessarily a cause
for concern. Scientific conferences should provide a platform for the ‘best’ science, and that likely means the ‘best’
scientists will present more often. However, an unequal distribution can also result from a narrow perspective of what
constitutes ‘high-quality’ research. Among academic venues, ACM CCS displayed the highest inequality across both
Gini computation approaches.
Topics Expanding the topical diversity of academic security conferences could mitigate inequality by allowing
new researchers to present alternative perspectives. Some areas - particularly the Identify function within the NIST
Cybersecurity Framework - remain underrepresented. Understanding current security management practices [67] could
inspire technical approaches to management problems. For instance, Asset Management can be inferred from network
traffic [68]; Risk Assessment can be framed as ML prediction [55]; and Governance can involve technical audits [69, 70].
Turning to offensive talks, their distribution is much more even across the techniques in MITRE ATT&CK, spanning
both academic and industry conferences. The one exception is information gathering that occurs pre-compromise,
which is rarely discussed at conferences. Preventing resource development is perhaps better conducted by governments,
such as by disrupting criminal markets for exploits [71]. The lack of offensive talks at insurance conferences raises the
question of whether there is a sufficient understanding of attacker operations.
Variance Insurance-focused events are clear outliers: they emphasize management and resilience rather than
technical controls or attacker techniques. This confirms the finding that insurers are more focused on post-incident
response than pre-incident mitigation [72]. Within MITRE ATT&CK mappings, the only offensive conference (DEFCON)
is comparatively focused on how compromise was achieved (execution, persistence and initial access), while the academic
conferences focus on activities that take place after compromise.
Over time, there appears to be a gradual shift towards the Identify function and away from Protective Technology and
Detect functions. This trend contradicts the prediction of Schneier that the 2010s would be the decade of response [73].
6All figures sourced from the OECD using post-tax income: https://stats.oecd.org (accessed 19 October 2025)
Manuscript submitted to ACM


---

Who Shares What? An Empirical Analysis of Security Conference Content Across Academia and Industry
21
Instead, there appears to be a subtle shift to security management. However, the apparent declines should not be
overstated, as the ‘declining’ categories remain the most frequently discussed in absolute terms.
Assumptions In mapping abstracts to cybersecurity frameworks, we imply that there should be balanced coverage
across framework categories. Our core assumption is that a broader range of speakers and topics implies a healthier
research ecosystem. While diversity has known benefits, specialization also drives depth and innovation. This tension
reflects the classic explore–exploit trade-off, where the objective — maximizing global security knowledge — remains
undefined. We acknowledge that reasonable readers may disagree with our emphasis on explore.
More fundamentally, it is unclear whether encouraging specific lines of work is appropriate, especially given the
sources of those frameworks. This has the potential to impinge on academic freedom. Although we explained why
ATT&CK and NIST CSF were the best among the alternatives (see Section 3), it is entirely unclear whether they are
‘good enough’ in terms of granularity, completeness and so on. This may be actively contested by some.
Future Work We focused on speakers but did not consider listeners/readers. Doing so is crucial to understanding
the impact of conference presentations. Collecting this information risks introducing some form of surveillance that
undermines the privacy of attendees. One privacy-preserving approach is to scrape the number of views that uploaded
video recordings received and to study the comments. Alternatively, an (imperfect) academic proxy for impact on
readers is citation count, but the industry equivalent requires more sophisticated research designs.
To address the limitations described in Section 5, future work should add extra conferences and map abstract to
different security frameworks and compare the results. Further, a qualitative study collecting data from conference
organizers could explore hidden dynamics, such as negotiations with industry sponsors. This would provide insights
into unseen details like what sponsors demand from academic conferences. Gaining access to industry conference
organizers is considerably more difficult.
7
Conclusion
Security conferences are an important but understudied channel by which knowledge and information is shared. Our
paper built a longitudinal dataset of talks at 10 prestigious conferences across industry and academia. We characterized
who speaks at these conferences (RQ1), about which topics (RQ2), and how this compares across conferences and over
time (RQ3). To answer the latter two research questions, we mapped conference abstracts to cybersecurity frameworks
using two NLP techniques, which show moderate agreement.
The results show academics moved freely between the big four venues, but just 5% of academic authors also
presented at InfoSec or Insurance conferences. The equivalent figure was 4% for insurance speakers, and 7% for InfoSec
speakers. This suggests there is limited information sharing across academia, InfoSec and insurance; a potential area
for improvement. We also showed there is an unequal distribution of talks across speakers, with this inequality varying
across conferences. In terms of sponsors, academic conference are dominated by BigTech firms, whereas InfoSec
conference sponsors are predominantly cybersecurity vendors. Unequal distribution of speaking time or sponsorship
sources can be a sign that parties have the power to influence which security topics are studied and which solutions are
adopted.
Defensive talks were more common than offensive and neutral ones at all conferences, except for DEFCON, where
offensive topics dominated due to its hacker-focused nature. This allows us to quantify the balance of offensive and
defensive papers at academic conferences, which have been criticized for focusing on attack papers [74]. Offensive
abstracts are distributed evenly across the categories of MITRE ATT&CK, apart from Reconnaissance and Resource
Manuscript submitted to ACM


---

22
Lukas Walter, Clemens Sauerwein, and Daniel W. Woods
Development. Defensive abstracts focused on Protective Technology and categories related to monitoring. Academic
conferences are less likely to focus on the Identify and Recover functions from the NIST Cybersecurity Framework.
These findings support a more nuanced understanding of security information sharing, in which success should
be evaluated with regards to specific channels and institutions. Researchers have been disappointed by the quality of
information shared via online sources [43, 44] and threat intelligence feeds [21, 24, 75]. However, there is more success
when it comes to vulnerability management. Bug bounties incentivize the discovery of new information [27, 28]. Further,
information about fixes is widely available, the problem lies in acting on the information by installing patches [32, 33].
Our results suggest security conferences should be considered a success story, closer to patch management than threat
intelligence sharing. This is perhaps not surprising given attendees, sponsors and research founders invest considerable
resources in attending and sponsoring these conferences. An interesting follow-on study would speak to conference
organizers to enrich our quantitative analysis with qualitative insights about the unobservable aspects of conference
organization.
Going forward, organizers of prestigious conferences should ensure there is a range of speakers and topics. To increase
diversity of speakers, program committees could explore proposals like: (i) reserving slots for authors/institutions
who have not presented before; and (ii) introducing a maximum number of submissions per individual (implemented
by USENIX Security, for example). To increase topic diversity, conferences could edit the call for papers to address
under-studied topics according to our results, and possibly lower the bar for acceptance for these topics—a policy not
unlike special issues for journals. We only raise these policies as provocations, acknowledging such policies will be
argued to be in tension with the principle of meritocracy. Nevertheless, we hope our article can prompt discussions
among program committees.
References
[1] Florian Skopik, Giuseppe Settanni, and Roman Fiedler. A problem shared is a problem halved: A survey on the dimensions of collective cyber
defense through security information sharing. Computers & Security, 60:154–176, 2016.
[2] Stefan Laube and Rainer Böhme. Strategic aspects of cyber risk information sharing. ACM Computing Surveys, 50(5):1–36, 2017.
[3] Scott Ainslie, Dean Thompson, Sean Maynard, and Atif Ahmad. Cyber-threat intelligence for security decision-making: A review and research
agenda for practice. Computers & Security, page 103352, 2023.
[4] Steffen Wendzel, Cédric Lévy-Bencheton, and Luca Caviglione. Not all areas are equal: analysis of citations in information security research.
Scientometrics, 122(1):267–286, 2020.
[5] Davide Balzarotti. System security circus 2022. https://www.s3.eurecom.fr/~balzarot/security-circus/circus_stats.html, 2022. Accessed: 2025-10-10.
[6] Jeffrey C Carver, Morgan Burcham, Sedef Akinli Kocak, Ayse Bener, Michael Felderer, Matthias Gander, Jason King, Jouni Markkula, Markku Oivo,
Clemens Sauerwein, et al. Establishing a baseline for measuring advancement in the science of security: an analysis of the 2015 IEEE security &
privacy proceedings. In Proceedings of the Symposium and Bootcamp on the Science of Security, pages 38–51, 2016.
[7] Morgan Burcham, Mahran Al-Zyoud, Jeffrey C Carver, Mohammed Alsaleh, Hongying Du, Fida Gilani, Jun Jiang, Akond Rahman, Özgür Kafalı,
Ehab Al-Shaer, et al. Characterizing scientific reporting in security literature: An analysis of ACM CCS and IEEE S&P papers. In Proceedings of the
Hot Topics in Science of Security: Symposium and Bootcamp, pages 13–23, 2017.
[8] Lukas Walter, Clemens Sauerwein, and Daniel Woods. Infosec.pptx: A longitudinal dataset of talks and sponsors at academic and industry security
conferences (2014–2022), April 2024. Available online at: https://doi.org/10.5281/zenodo.15989593.
[9] Jeb Webb, Atif Ahmad, Sean B Maynard, and Graeme Shanks. A situation awareness model for information security risk management. Computers &
security, 44:1–15, 2014.
[10] Atif Ahmad, Sean B Maynard, Kevin C Desouza, James Kotsias, Monica T Whitty, and Richard L Baskerville. How can organizations develop
situation awareness for incident response: A case study of management practice. Computers & Security, 101:102122, 2021.
[11] Panos Kampanakis. Security automation and threat information-sharing options. IEEE Security & Privacy, 12(5):42–51, 2014.
[12] Agnes Yang, Young Jin Kwon, and Sang-Yong Tom Lee. The impact of information sharing legislation on cybersecurity industry. Industrial
Management & Data Systems, 120(9):1777–1794, 2020.
[13] Rebecca Slayton and Brian Clarke. Trusting infrastructure: The emergence of computer security incident response, 1989–2005. Technology and
Culture, 61(1):173–206, 2020.
Manuscript submitted to ACM


---

Who Shares What? An Empirical Analysis of Security Conference Content Across Academia and Industry
23
[14] Thomas D Wagner, Khaled Mahbub, Esther Palomar, and Ali E Abdallah. Cyber threat intelligence sharing: Survey and research directions. Computers
& Security, 87:101589, 2019.
[15] Clemens Sauerwein, Christian Sillaber, Andrea Mussmann, and Ruth Breu. Threat intelligence sharing platforms: An exploratory study of software
vendors and research perspectives. In Wirtschaftsinformatik 2017, 2017.
[16] Sarah Brown, Joep Gommers, and Oscar Serrano. From cyber security information sharing to threat management. In Proceedings of the 2nd ACM
workshop on information sharing and collaborative security, pages 43–49, 2015.
[17] Clemens Sauerwein, Irdin Pekaric, Michael Felderer, and Ruth Breu. An analysis and classification of public information security data sources used
in research and practice. Computers & security, 82:140–155, 2019.
[18] Clemens Sauerwein, Daniel Fischer, Milena Rubsamen, Guido Rosenberger, Dirk Stelzer, and Ruth Breu. From threat data to actionable intelligence:
an exploratory analysis of the intelligence cycle implementation in cyber threat intelligence sharing platforms. In Proceedings of the 16th International
Conference on Availability, Reliability and Security, pages 1–9, 2021.
[19] Luc Dandurand and Oscar Serrano Serrano. Towards improved cyber security information sharing. In 2013 5th International Conference on Cyber
Conflict (CYCON 2013), pages 1–16. IEEE, 2013.
[20] David Chismon and Martyn Ruks. Threat intelligence: Collecting, analysing, evaluating. MWR InfoSecurity Ltd, 3(2):36–42, 2015.
[21] Vector Guo Li, Matthew Dunn, Paul Pearce, Damon McCoy, Geoffrey M Voelker, and Stefan Savage. Reading the tea leaves: A comparative analysis
of threat intelligence. In Proc. of the 28th USENIX Security Symposium, pages 851–867, 2019.
[22] Kurt Thomas, Rony Amira, Adi Ben-Yoash, Ori Folger, Amir Hardon, Ari Berger, Elie Bursztein, and Michael Bailey. The abuse sharing economy:
Understanding the limits of threat exchanges. In Research in Attacks, Intrusions, and Defenses: 19th International Symposium, RAID 2016, Paris, France,
September 19-21, 2016, Proceedings 19, pages 143–164. Springer, 2016.
[23] Xander Bouwman, Victor Le Pochat, Pawel Foremski, Tom Van Goethem, Carlos H Gañán, Giovane Moura, Samaneh Tajalizadehkhoob, Wouter
Joosen, and Michel van Eeten. Helping hands: Measuring the impact of a large threat intelligence sharing community. In Proc. of the 31st USENIX
Security Symposium, pages 1149–1165, 2022.
[24] Xander Bouwman, Harm Griffioen, Jelle Egbers, Christian Doerr, Bram Klievink, and Michel van Eeten. A different cup of TI? the added value of
commercial threat intelligence. In Proc. of the 30th USENIX Security Symposium, pages 433–450, 2020.
[25] Adam Zibak, Clemens Sauerwein, and Andrew C Simpson. Threat intelligence quality dimensions for research and practice. Digital Threats: Research
and Practice, 3(4):1–22, 2022.
[26] Mingyi Zhao, Aron Laszka, and Jens Grossklags. Devising effective policies for bug-bounty platforms and security vulnerability discovery. Journal
of Information Policy, 7:372–418, 2017.
[27] Kiran Sridhar and Ming Ng. Hacking for good: Leveraging HackerOne data to develop an economic model of bug bounties. Journal of Cybersecurity,
7(1):tyab007, 2021.
[28] Matthew Finifter, Devdatta Akhawe, and David Wagner. An empirical study of vulnerability rewards programs. In Presented as part of the 22nd
USENIX Security Symp., pages 273–288. USENIX, 2013.
[29] Mingyi Zhao, Jens Grossklags, and Peng Liu. An empirical study of web vulnerability discovery ecosystems. In Proc. of the 22nd ACM SIGSAC
Conference on Computer and Communications Security, pages 1105–1117. ACM, 2015.
[30] Daniel Votipka, Rock Stevens, Elissa Redmiles, Jeremy Hu, and Michelle Mazurek. Hackers vs. testers: A comparison of software vulnerability
discovery processes. In 2018 IEEE Symposium on Security and Privacy (SP), pages 374–391. IEEE, 2018.
[31] Yangheran Piao, Temima Hrle, Daniel W Woods, and Ross Anderson. Study club, labor union or start-up? characterizing teams and collaboration in
the bug bounty ecosystem. In 2025 IEEE Symposium on Security and Privacy (SP), pages 539–558. IEEE, 2025.
[32] Stefan Frei, Martin May, Ulrich Fiedler, and Bernhard Plattner. Large-scale vulnerability analysis. In Proceedings of the SIGCOMM workshop on
Large-scale attack defense, pages 131–138, 2006.
[33] Frank Li and Vern Paxson. A large-scale empirical study of security patches. In Proceedings of the 2017 ACM SIGSAC Conference on Computer and
Communications Security, pages 2201–2215, 2017.
[34] Frank Li, Lisa Rogers, Arunesh Mathur, Nathan Malkin, and Marshini Chetty. Keepers of the machines: Examining how system administrators
manage software updates for multiple machines. In Fifteenth Symposium on Usable Privacy and Security (SOUPS 2019), pages 273–288, 2019.
[35] Arunesh Mathur, Josefine Engel, Sonam Sobti, Victoria Chang, and Marshini Chetty. "they keep coming back like zombies": Improving software
updating interfaces. In Twelfth Symposium on Usable Privacy and Security (SOUPS 2016), pages 43–58, 2016.
[36] Ben Stock, Giancarlo Pellegrino, Christian Rossow, Martin Johns, and Michael Backes. Hey, you have a problem: On the feasibility of large-scale
web vulnerability notification. In Proc. of the USENIX Security Symp., pages 1015–1032. USENIX, 2016.
[37] Frank Li, Zakir Durumeric, Jakub Czyz, Mohammad Karami, Michael Bailey, Damon McCoy, Stefan Savage, and Vern Paxson. You’ve got vulnerability:
Exploring effective vulnerability notifications. In Proc. of the USENIX Security Symp., pages 1033–1050. USENIX, 2016.
[38] Orçun Çetin, Carlos Gañán, Lisette Altena, Samaneh Tajalizadehkhoob, and Michel Van Eeten. Tell me you fixed it: Evaluating vulnerability
notifications via quarantine networks. In 2019 IEEE European Symposium on Security and Privacy (EuroS&P), pages 326–339. IEEE, 2019.
[39] Jay Jacobs, Sasha Romanosky, Idris Adjerid, and Wade Baker. Improving vulnerability remediation through better exploit prediction. Journal of
Cybersecurity, 6(1):tyaa015, 2020.
[40] Stephanie de Smale, Rik van Dijk, Xander Bouwman, Jeroen van der Ham, and Michel van Eeten. No one drinks from the firehose: How organizations
filter and prioritize vulnerability information. In 2023 IEEE Symposium on Security and Privacy (SP), 2023.
Manuscript submitted to ACM


---

24
Lukas Walter, Clemens Sauerwein, and Daniel W. Woods
[41] Jingjie Li, Kaiwen Sun, Brittany Skye Huff, Anna Marie Bierley, Younghyun Kim, Florian Schaub, and Kassem Fawaz. “it’s up to the consumer to be
smart”: Understanding the security and privacy attitudes of smart home users on reddit. In IEEE Symposium on Security and Privacy (SP)(SP), pages
380–396. IEEE Computer Society Los Alamitos, CA, 2023.
[42] Mohammad Tahaei, Kami Vaniea, and Naomi Saphra. Understanding privacy-related questions on stack overflow. In Proceedings of the 2020 CHI
conference on human factors in computing systems, pages 1–14, 2020.
[43] Yasemin Acar, Michael Backes, Sascha Fahl, Doowon Kim, Michelle L Mazurek, and Christian Stransky. You get where you’re looking for: The
impact of information sources on code security. In 2016 IEEE Symposium on Security and Privacy (SP), pages 289–305. IEEE, 2016.
[44] Felix Fischer, Konstantin Böttinger, Huang Xiao, Christian Stransky, Yasemin Acar, Michael Backes, and Sascha Fahl. Stack overflow considered
harmful? the impact of copy&paste on android application security. In 2017 IEEE Symposium on Security and Privacy (SP), pages 121–136. IEEE, 2017.
[45] Felix Fischer, Huang Xiao, Ching-Yu Kao, Yannick Stachelscheid, Benjamin Johnson, Danial Razar, Paul Fawkesley, Nat Buckley, Konstantin Böttinger,
Paul Muntean, and Jens Grossklags. Stack overflow considered helpful! deep learning security nudges towards stronger cryptography. In 28th
USENIX Security Symposium (USENIX Security 19), pages 339–356, 2019.
[46] Elissa M Redmiles, Amelia R Malone, and Michelle L Mazurek. I think they’re trying to tell me something: Advice sources and selection for digital
security. In 2016 IEEE Symposium on Security and Privacy (SP), pages 272–288. IEEE, 2016.
[47] Elissa M Redmiles, Noel Warford, Amritha Jayanti, Aravind Koneru, Sean Kross, Miraida Morales, Rock Stevens, and Michelle L Mazurek. A
comprehensive quality evaluation of security and privacy advice on the web. In 29th USENIX Security Symposium (USENIX Security 20), pages
89–108, 2020.
[48] Ananta Soneji, Faris Bugra Kokulu, Carlos Rubio-Medrano, Tiffany Bao, Ruoyu Wang, Yan Shoshitaishvili, and Adam Doupé. “flawed, but like
democracy we don’t have a better system”: The experts’ insights on the peer review process of evaluating security papers. In 2022 IEEE Symposium
on Security and Privacy (SP), pages 1845–1862. IEEE, 2022.
[49] Savino Dambra, Leyla Bilge, and Davide Balzarotti. SoK: Cyber insurance—Technical challenges and a system security roadmap. In Proc. of the
Symp. on Security and Privacy, pages 293–309. IEEE, 2020.
[50] National
Association
of
Insurance
Commissioners
Staff.
Report
on
the
cybersecurity
insurance
market.
https://content.naic.org/sites/default/files/cmte-c-cyber-supplement-report-2022-for-data-year-2021.pdf, 2021. Accessed: 2025-10-10.
[51] Daniel W Woods, Rainer Böhme, Josephine Wolff, and Daniel Schwarcz. Lessons lost: Incident response in the age of cyber insurance and breach
attorneys. In Proceedings of the 32nd USENIX Security Symposium, 2023.
[52] Harjot Kaur, Carson Powers, Ronald E Thompson III, Sascha Fahl, and Daniel Votipka. “threat modeling is very formal, it’s very technical, and also
very hard to do correctly”: Investigating threat modeling practices in open-source software projects. In 34th USENIX Security Symposium (USENIX
Security’25), 2025.
[53] Warda Usman and Daniel Zappala. Sok: A framework and guide for human-centered threat modeling in security and privacy research. In 2025 IEEE
Symposium on Security and Privacy (SP), pages 2697–2715. IEEE, 2025.
[54] Mathew Vermeer, Jonathan West, Alejandro Cuevas, Shuonan Niu, Nicolas Christin, Michel Van Eeten, Tobias Fiebig, Carlos Ganán, and Tyler
Moore. Sok: A framework for asset discovery: Systematizing advances in network measurements for protecting organizations. In 2021 IEEE European
Symposium on Security and Privacy (EuroS&P), pages 440–456. IEEE, 2021.
[55] Yang Liu, Armin Sarabi, Jing Zhang, Parinaz Naghizadeh, Manish Karir, Michael Bailey, and Mingyan Liu. Cloudy with a chance of breach:
Forecasting cyber security incidents. In Proc. of the USENIX Sec. Symp., pages 1009–1024. USENIX, 2015.
[56] Leyla Bilge, Yufei Han, and Matteo Dell’Amico. Riskteller: Predicting the risk of cyber incidents. In Proc. of the Conference on Computer and
Communications Security, pages 1299–1311. ACM, 2017.
[57] Robert Morris and Ken Thompson. Password security: A case history. Communications of the ACM, 22(11):594–597, 1979.
[58] Joseph Bonneau, Cormac Herley, Paul C Van Oorschot, and Frank Stajano. The quest to replace passwords: A framework for comparative evaluation
of web authentication schemes. In 2012 IEEE symposium on security and privacy, pages 553–567. IEEE, 2012.
[59] Grant Ho, Ariana Mirian, Elisa Luo, Khang Tong, Euyhyun Lee, Lin Liu, Christopher A Longhurst, Christian Dameff, Stefan Savage, and Geoffrey M
Voelker. Understanding the efficacy of phishing training in practice. In 2025 IEEE Symposium on Security and Privacy (SP), pages 37–54. IEEE, 2025.
[60] Simson Garfinkel and Heather Richter Lipford. Usable security: History, themes, and challenges. Synthesis Lectures on Information Security, Privacy,
and Trust, 5(2):1–124, 2014.
[61] Benjamin Collier, Richard Clayton, Alice Hutchings, and Daniel Thomas. Cybercrime is (often) boring: maintaining the infrastructure of cybercrime
economies. In Workshop on the Economics of Information Security, 2020.
[62] Anh V Vu, Ben Collier, Daniel R Thomas, John Kristoff, Richard Clayton, and Alice Hutchings. Assessing the aftermath: the effects of a global
takedown against ddos-for-hire services. In Proceedings of the USENIX Security Symposium (USENIX Security), 2025.
[63] Rob Knake, Adam Shostack, and Tarah Wheeler. Learning from cyber incidents: Adapting aviation safety models to cybersecurity. Harvard Belfer
Center, 2021.
[64] Simson L Garfinkel. Digital forensics research: The next 10 years. Digital Investigation, 7:S64–S73, 2010.
[65] Daniel W Drezner. The ideas industry. Oxford University Press, 2017.
[66] Mohamed Abdalla and Moustafa Abdalla. The grey hoodie project: Big tobacco, big tech, and the threat on academic integrity. In Proceedings of the
2021 AAAI/ACM Conference on AI, Ethics, and Society, pages 287–297, 2021.
Manuscript submitted to ACM


---

Who Shares What? An Empirical Analysis of Security Conference Content Across Academia and Industry
25
[67] Jonas Hielscher, Uta Menges, Simon Parkin, Annette Kluge, and M Angela Sasse. “employees who don’t accept the time security takes are not aware
enough”: The ciso view of human-centred security. In 32st USENIX Security Symposium (USENIX Security 23), Boston, MA, 2023.
[68] Louis F DeKoven, Audrey Randall, Ariana Mirian, Gautam Akiwate, Ansel Blume, Lawrence K Saul, Aaron Schulman, Geoffrey M Voelker, and
Stefan Savage. Measuring security practices and how they impact security. In Proc. of the Internet Measurement Conference, pages 36–49. ACM, 2019.
[69] Sazzadur Rahaman, Gang Wang, and Danfeng Yao. Security certification in payment card industry: Testbeds, measurements, and recommendations.
In Proc. of the Conf. on Computer and Communications Security, pages 481–498. ACM, 2019.
[70] Samin Yaseer Mahmud, Akhil Acharya, Benjamin Andow, William Enck, and Bradley Reaves. Cardpliance: PCI DSS compliance of android
applications. In 29th USENIX Security Symposium, pages 1517–1533, 2020.
[71] Luca Allodi, Marco Corradin, and Fabio Massacci. Then and now: On the maturity of the cybercrime markets the lesson that black-hat marketeers
learned. IEEE Trans. on Emerging Topics in Computing, 4(1):35–46, 2015.
[72] Josephine Wolff. Cyberinsurance Policy: Rethinking Risk in an Age of Ransomware, Computer Fraud, Data Breaches, and Cyberattacks. MIT Press, 2022.
[73] Bruce Schneier. The future of incident response. IEEE Security & Privacy, 12(5):96–96, 2014.
[74] Cormac Herley and Paul C Van Oorschot. SoK: Science, security and the elusive goal of security as a scientific pursuit. In Proc. of the Symp. on
Security and Privacy, pages 99–120. IEEE, 2017.
[75] XB Bouwman, AM Ethembabaoglu, B Hermans, C Hernandez Ganan, and MJG van Eeten. Can iocs impose cost? the effects of publishing threat
intelligence on adversary behavior. In ACM Conference on Computer and Communications Security. ACM, 2025.
Manuscript submitted to ACM


---

26
Lukas Walter, Clemens Sauerwein, and Daniel W. Woods
Appendix: Supplementary Figures and Tables
Fig. 15. Mean similarity score (averaged across GPT-based and cosine similarity measures) for defensive talks mapped to the NIST
Cybersecurity Framework.
Fig. 16. Mean similarity score (averaged across GPT-based and cosine similarity measures) for offensive talks mapped to the MITRE
ATT&CK Framework.
Manuscript submitted to ACM


---

Who Shares What? An Empirical Analysis of Security Conference Content Across Academia and Industry
27
Fig. 17. Similarity score of Black Hat defensive talks mapped to the NIST Cybersecurity Framework from 2014 to 2022.
Fig. 18. Similarity score of IEEE S&P defensive talks mapped to the NIST Cybersecurity Framework from 2014 to 2022.
Manuscript submitted to ACM


---

28
Lukas Walter, Clemens Sauerwein, and Daniel W. Woods
Fig. 19. Top sponsors of InfoSec and cyber insurance conferences aggregated over 2014–2022. Numbers above the bars indicate each
sponsor’s mean sponsorship tier. Note: sponsor data for some InfoSec conferences were incomplete.
Fig. 20. Similarity score of USENIX Security defensive talks mapped to the NIST Cybersecurity Framework from 2014 to 2022.
Manuscript submitted to ACM


---

Who Shares What? An Empirical Analysis of Security Conference Content Across Academia and Industry
29
Fig. 21. Similarity score of Black Hat offensive talks mapped to the MITRE ATT&CK Framework from 2014 to 2022.
Fig. 22. Similarity score of DEFCON offensive talks mapped to the MITRE ATT&CK Framework from 2014 to 2022.
Fig. 23. Similarity score of IEEE S&P offensive talks mapped to the MITRE ATT&CK Framework from 2014 to 2022.
Manuscript submitted to ACM


---

30
Lukas Walter, Clemens Sauerwein, and Daniel W. Woods
Fig. 24. Similarity score of USENIX Security offensive talks mapped to the MITRE ATT&CK Framework from 2014 to 2022.
Manuscript submitted to ACM
