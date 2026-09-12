---
title: 'BEACON: Behavior-Anchored Cross-Source Knowledge Graph'
id: beacon-behavior-anchored-cross-source-knowledge-graph
tags:
- attack-ontology-drift-cti-85bc51
- pin-rate-survey
created: '2026-09-12T21:34:35.000843Z'
updated: '2026-09-12T21:44:28.361423Z'
source: https://arxiv.org/abs/2608.28394v1
source_domain: arxiv.org
fetched_at: '2026-09-12T21:34:35.000370Z'
fetch_provider: crawl4ai
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'arXiv 2608.28394v1 (2026): uses 23 ATT&CK technique-ID occurrences (without
  sub-techniques); ATT&CK release declaration classified as exact_release.'
raw_file: raw/beacon-behavior-anchored-cross-source-knowledge-graph.pdf
doi: arXiv:2608.28394v1
---

BEACON: Behavior-Anchored Cross-Source Knowledge Graph
Construction for Cyber Threat Intelligence
Changze Li
changzeli@vt.edu
Virginia Tech
Blacksburg, United States
Yutong Cheng
yutongcheng@vt.edu
Virginia Tech
Blacksburg, United States
Tsania Camila Finnisa
111202214241@mhs.dinus.ac.id
Dian Nuswantoro University
Jepara, Indonesia
Qian Cui
cuiqia@amazon.com
Amazon
Seattle, United States
Wei Ding
dingwe@amazon.com
Amazon
Seattle, United States
Peng Gao
penggao@vt.edu
Virginia Tech
Blacksburg, United States
Abstract
Cyber threat intelligence (CTI) is foundational to modern cyber de-
fense, yet much of it resides in unstructured reports whose volume
and heterogeneity far exceed manual analysis, motivating research
on automatically constructing knowledge graphs from CTI reports.
However, most existing approaches extract partial information
within a single report, leaving the cross-source setting unexplored,
where the same threat is given unrelated names. Our key insight
is that attack behaviors, once mapped to MITRE ATT&CK (a stan-
dardized catalog of attack techniques maintained by experts), can
anchor the rest of a report. Attack behaviors are the adversarial
actions a report describes, while contextual entities (e.g., threat
actors, campaigns, and affected products) and Indicators of Com-
promise (IoCs; e.g., IP addresses) are their participants and traces.
Attaching them to these anchors places every per-report graph in
one canonical space, where overlapping techniques become the
signal that aligns unrelated names.
We realize this insight in BEACON, an LLM-driven framework
for cross-source CTI knowledge graph construction. Its first stage
extracts each report into a graph under a propose-then-verify para-
digm, grounding candidates in report evidence and official ATT&CK
definitions, to suppress LLM misclassification and hallucination.
Its second stage merges these graphs with a hierarchical alignment
strategy that applies signals in decreasing order of determinism,
from character-level and semantic similarity to overlapping tech-
nique neighborhoods, iterating as merges pool neighborhoods. No
existing benchmark links entities to technique anchors or provides
cross-source alignment ground truth. We therefore construct and re-
lease two human-annotated datasets from 34 sources: to our knowl-
edge the largest for report-level CTI extraction (8,395 elements) and
the first for cross-source consolidation (3,487). On them, BEACON
outperforms all baselines by at least 23% and 9%, respectively.
1
Introduction
Cyber threat intelligence (CTI) is evidence-based knowledge about
existing and emerging cyber threats [30], and it is foundational to
modern cyber defense, shifting organizations from reactive incident
response to proactive threat anticipation. Much of this knowledge
resides in natural-language reports that security vendors publish
independently and continuously [19, 28, 36, 44]. Reports mainly
describe three kinds of information: (1) Contextual entities represent
high-level context about the campaign, such as threat actors, cam-
paigns, malware families, and affected products. (2) Attack behaviors
are mid-level tactics, techniques, and procedures (TTPs) [43] per-
formed by the adversary. MITRE ATT&CK [43] standardizes attack
behaviors into a taxonomy of techniques curated and maintained by
security experts. Each technique-level entry, or TTP, has a unique
ID, such as T1190 for exploiting a public-facing application and
T1566 for phishing. (3) Indicators of Compromise (IoCs) represent
low-level traces of the attack procedures, such as IP addresses, file
hashes, and CVE identifiers.
These reports differ in wording, naming conventions, and level of
detail, and their volume and heterogeneity far exceed the capacity
of manual analysis. This motivates a growing line of work that
organizes this knowledge into graphs for large-scale querying [6, 13,
16], but two major limitations remain. First, existing methods
cover only part of the information in a CTI report, and fall
into two research focuses. One maps attack behavior descriptions
in natural language to ATT&CK techniques, but leaves out the
surrounding contextual entities and IoCs [5, 28, 40]. The other
extracts contextual entities and IoCs as relation triplets in each
report’s own wording, without mapping behaviors to ATT&CK
techniques or capturing their relations to them [6, 13, 29, 52]. No
existing work extracts both into one structure. Recent work turns to
large language models (LLMs) for their stronger natural-language
processing capability [6, 52, 54], but three properties of CTI make
extraction difficult for them. The same entity can play different
roles in different contexts: Gmail can be an affected product or
the tool used to send phishing emails, and Microsoft can be the
affected vendor or the report’s own publisher, which should not
be extracted. ATT&CK contains hundreds of techniques whose
definitions differ only in fine-grained details: lateral movement
through remote services is T1021 [48] with legitimate access but
T1210 [49] through a vulnerability. And LLM outputs are generated
rather than retrieved from the text, so extracted information may
not exist in the source. These properties make LLM-based extraction
suffer from misclassification and hallucination [3, 31, 46].
Second, no existing method reliably constructs a knowledge
graph across reports from different CTI sources. Vendors in-
dependently report on the same threat under different naming
conventions, and no single report contains all aliases used across
sources [7, 39]. For instance, three reports on an Oracle E-Business
Suite campaign name the same threat actor Cl0p [10], Clop [23],
1
arXiv:2608.28394v1  [cs.CR]  28 Aug 2026


---

Li et al.
and Graceful Spider [20] (Figure 1, left): the first two differ by a
character, while the third is entirely unrelated. Most existing work
deduplicates entities within a single report [6], and the few multi-
report attempts rely on embedding similarity [52], which cannot
align unrelated names such as Cl0p and Graceful Spider. While
LLMs can match entities from context, comparing all entity pairs
across reports is costly, and LLMs can incorrectly merge distinct
entities that appear in related narratives. For example, reports that
describe Oracle E-Business Suite also mention the actor’s earlier
MOVEit campaign as background [10, 23], and an LLM compar-
ing reports can incorrectly merge the two campaigns because they
share the same actor and context.
In this work, we aim to construct one knowledge graph from CTI
reports across sources, which covers all three kinds of information
and reliably merges nodes that refer to the same real-world entity.
Our key insight is that attack behaviors, a central component of
CTI reports, can be mapped to ATT&CK techniques, however a
source words them, while contextual entities and IoCs describe
the participants and traces of these behaviors [28, 40]. Attaching
entities to ATT&CK techniques as anchors therefore captures the re-
lationships that existing methods leave unextracted, and unifies the
per-report graphs in a shared canonical space, giving entities with
unrelated names an additional domain-specific signal for alignment.
We build on this insight with BEACON (BEhavior-Anchored
CONsolidation of CTI reports), an LLM-driven two-stage frame-
work that constructs one knowledge graph across different CTI
sources (Figure 1). To suppress misclassification and hallucination,
we design a propose-then-verify paradigm. The first stage, space-
anchoring, extracts each report into a graph in which contextual
entities and IoCs attach to ATT&CK technique anchors. Since attack
behaviors mapping to techniques in narratives are interleaved, the
LLM first decomposes each report into atomic behaviors grounded
in report evidence. It then proposes multiple candidate techniques
for each atomic behavior to expand the coverage among hundreds
of fine-grained definitions, and verifies each candidate against its
official ATT&CK definition. Under the same propose-then-verify
paradigm, contextual entities and IoCs are extracted and attached
to the technique anchors when their evidence overlaps.
For the second stage, consolidation, we design a hierarchical
alignment strategy that merges the per-report graphs by applying
merging signals in decreasing order of determinism, with each level
building on the merges above it and every merge verified by the
LLM against report evidence. To cover naming divergence from
a single character to entirely unrelated names, it matches entities
from character-level and semantic similarity to a signal that only
the anchored space makes available: the overlap of their ATT&CK
technique neighborhoods, the sets of techniques they attach to.
Since entities sharing multiple attack behaviors are likely the same,
the neighborhood level can match entities with unrelated names,
and iterates as each merge pools its members’ neighborhoods and
exposes new candidates.
No existing benchmark links entities to technique anchors or pro-
vides cross-source alignment ground truth. We therefore construct
and release two new datasets: BEACON-Single, which contains
150 reports from 15 publishers with 8,395 nodes and edges in total,
and to our knowledge is the largest human-annotated benchmark
for report-level CTI extraction; and BEACON-Group, which or-
ganizes 100 reports from 31 publishers into 33 groups covering
the same threat, and is the first benchmark for cross-source CTI
consolidation. Both datasets are carefully curated through dual ex-
pert annotation with senior adjudication. BEACON outperforms
all baselines on both tasks, by at least 23% on extraction and 9%
on consolidation. On the hardest cases, entities that appear un-
der differently spelled or entirely unrelated names across sources,
BEACON outperforms all baselines by at least 27%. Ablation exper-
iments show that ATT&CK technique neighborhoods are critical
for aligning these hard entities.
2
Related Work
2.1
CTI Extraction
Evolving CTI standards such as STIX [34], MITRE ATT&CK [43],
and OpenCTI [11] provide shared vocabularies for representing
and exchanging threat knowledge, yet the CTI community often
distributes intelligence as natural-language reports. Bridging this
gap, one line of work reconstructs attack behaviors from report
text and maps them to ATT&CK techniques [1, 3, 4, 15, 17, 21, 24–
26, 28, 33, 36, 54]. Early methods rely on rule-guided NLP or super-
vised classifiers [17, 24, 28, 36], but such pipelines struggle with
natural-language variability and transfer poorly as threats evolve.
Later works leverage pretrained language models such as BERT [9],
either embedding report text and TTP definitions into a shared
space for semantic comparison [1, 21, 33] or mapping text to TTP
IDs end-to-end [4, 26]. They handle variation better but remain
bound to pretrained backbones and labeled data. Recent work turns
to LLMs [3], with TechniqueRAG [25] reranking candidate tech-
niques with an instruction-tuned LLM before mapping with a fine-
tuned one and AttacKG+ [54] expanding triplets into temporal
behavior graphs, whose entities carry no relation to the mapped
techniques. Haque et al. aggregate predicted TTP IDs into campaign-
level sets [15], confirming the value of multi-report settings while
leaving entities unaligned. Across this line, extraction focuses on
attack behaviors, and contextual entities and IoCs are not extracted
or not attached to the mapped techniques, while BEACON extracts
both and attaches them to the mapped techniques.
Another line of work targets contextual information. These meth-
ods extract the named participants of an attack, such as threat actors,
malware families, and affected organizations, and their relations
into a graph. Early systems use rule-based and unsupervised NLP
techniques [37], while recent work extracts ontology-constrained
relation triplets end-to-end with LLMs [6, 53]. Systems such as
CTINexus [6] and CTI-Thinker [52] extract MITRE ATT&CK tech-
nique IDs only when the report explicitly writes out the ID, such
as T1190, as a string. Behaviors that the report describes in natu-
ral language without naming an ID are therefore not mapped to
techniques. LADDER extracts both TTPs and contextual entities,
but its ontology only connects each TTP to malware, so the graph
cannot capture the relations between other types of entities and
attack behaviors [1]. Across this line, extraction focuses on contex-
tual entities and IoCs alone, without mapping attack behaviors to
techniques or capturing their relations with ATT&CK techniques.
Moreover, both lines are limited to single reports, while BEACON
2


---

BEACON: Behavior-Anchored Cross-Source Knowledge Graph Construction for Cyber Threat Intelligence
Cl0p
SOCRadar
Cl0p
exfiltrate data via MOVEit
CVE-2025-61882
Clop
   Security Week
Clop
deploy web shell quietly
md5: 9b7a2e3f0c1d4b77
Graceful Spider
      The Hacker News
Graceful spider
abuse legitimate tools
IP: 103.27.12.88
/OA_HTML/SyncServlet
Contextual
Entity
IoC
Cl0p
EBS
⚓
T1190
⚓
T1588
CVE-2025-61882
CVE-2025-61884
CVE-2025-61882
/OA_HTML/SyncServlet
Graceful 
Spider
EBS
⚓
T1190
⚓
T1588
CVE-2025-61884
CVE-2025-61882
Clop
EBS
⚓
T1190
⚓
T1566
Cl0p
Telegram
EBS
TAXXX
CVE-2025-61882
 ⚓
 T1486
⚓
T1588
TTP
Anchor
⚓
 T1190
⚓
 T1566
⚓
T1059
⚓
 TXXXX
CVE-2025-61884
� Node Record
● SOCRadar ● SecurityWeek 
● The Hacker News
Cl0p · Clop · Graceful Spider
Sentence 23: Cl0p used pre-
auth REC ... +2
Report-Level Graphs
Consolidated Graph
Consolidation
by shared technique 
neighborhoods
●●●
●●●
●●●
●●●
●●
●●●
●●●
CTI Reports
Merge
Shared 
TTPs
Anchored 
Extraction
Contextual 
entity
TTP Anchor
IoC
Figure 1: From heterogeneous reports to one consolidated graph. Left: three major CTI sources, SOCRadar [42], The Hacker
News [47], and SecurityWeek [41], cover the same campaign and name its actor Cl0p [10], Graceful Spider [23], and Clop [20].
Middle: the space-anchoring stage extracts each report into a graph in which contextual entities (circles) and IoCs (rectangles)
attach to ATT&CK technique anchors (hexagons). Right: the consolidation stage merges nodes that refer to the same entity,
where shared technique neighborhoods align the unrelated name. The colored dots inside a node mark its source reports, and
the merged actor node keeps every alias, source, and evidence sentence in its record.
constructs one graph from reports across sources that covers all
three kinds of information.
2.2
Cross-Source Linking and Alignment
Classical entity matching compares names, textual fields, and at-
tributes across sources using similarity functions and binary clas-
sifiers that judge whether two records match [2, 8], but performs
poorly when name and attribute overlap is absent. Neural entity
matching encodes records into learned representations for pair-
wise comparison [12, 18, 27, 32], yet textual semantics alone cannot
reliably identify the same entity when the two records differ signif-
icantly. For example, “Twitter” and “X” refer to the same product,
but no embedding can relate the new name to the old one until
sufficient training data about the renaming appears. When entities
are connected in graphs, structure offers an additional matching
signal [22, 45]. Most recently, entity matching uses LLMs to judge
whether two records refer to the same entity [51], but these judg-
ments still rest on the same textual evidence.
In CTI, a few existing approaches try to address the entity align-
ment problem. CTINexus [6] limits entity alignment to single-
report deduplication, and CTI-Thinker [52], though aligning across
sources, relies on encoder embeddings and cosine-similarity thresh-
olds. Both approaches fail on CTI naming conventions. Threat enti-
ties are often given unrelated codewords, such as Wicked Panda
and Brass Typhoon for the same actor, which are distant in both
semantics and spelling, so neither embedding nor string similarity
can match them. Threat entities can also be given alphanumeric
labels, such as APT41 and TA415, which carry no semantics for em-
beddings to compare and share few characters for string similarity
to match. String similarity can further incorrectly merge two labels
when their spellings are nearly identical, such as APT41 and APT40.
Naming conventions also differ across vendors. For example, Mandi-
ant tracks the actor above as APT41, while Microsoft names it Brass
Typhoon in its own weather-themed scheme. Aligning this actor
across sources therefore requires matching APT41 with Brass Ty-
phoon, names from two unrelated naming schemes, which neither
exact-name nor similarity-based matching can handle. BEACON
instead aligns entities by their shared ATT&CK technique neigh-
borhoods, a signal that is consistent across sources and independent
of naming conventions.
3
Methodology
Figure 2 gives an overview of BEACON, an LLM-driven framework
that runs in two stages. The first stage, space-anchoring, extracts
each of the CTI reports {𝑟1, . . . ,𝑟𝑛} into a graph in which contextual
entities and IoCs attach to ATT&CK technique anchors. The second
stage, consolidation, merges nodes that refer to the same real-world
3


---

Li et al.
xN
TXXXX
TXXXX
TXXXX
Contextual Entity Proposal
Atomic behavior Proposal
IoC Proposal
Evidence Check Candidate Verification
TXXXX
TXXXX
TXXXX
TXXXX
TXXXX
Locate Evidence
TXXXX
TXXXX
Example[.]com
Evidence Check
TXXXX
TXXXX
TXXXX
Clop
TXXXX
TXXXX TXXXX
Clop
TXXXX TXXXX TXXXX
TTP Proposal
Normalization
Candidate Verification
Anchored Attachment
Stage 1 · Space Anchoring (per report)
T1190
Example.com
ID & Normalized Match 
Exact Names & Type Rules 
Jaro-
Winkler
Normalized 
Levenshtein 
Distance
3-gram 
Jaccard
3-gram 
cosine
Dist+1
◉Cosine
1
2
3
4
Threat Actor:  1
2
Campaign: 
4
1
2
MalwareFamily: 
Organization: 
1
2
3
4
1
2
......
Deterministic Matching
Similarity-based Matching (Contextual Entities Only)
Character Channel
Embedding Channel
Technique-Neighborhood Channel
Node Level
Cluster Level
Two-Level Verification
Stage 2 · Consolidation Stage
Iterative 
Closure xN
Each type combines a subset of 
the measures
Embedding
Similarity
 Search
Final Graph
Extracted Graph (per report)
Candidate cluster
TXXXXtoken-weighted 
window scoring
exact match check
exact match check
Shared Technique 
neighborhoods
Candidate Verification
Official ATT&CK 
Technique Definition
Same-Sentence Attachment
Central-entity Attachment
If Clop is 
central 
entity...
Evidence
Evidence
Report
False[.]com
Clop
ZeusBot
Clop
ZeusBot
Example[.]com
False[.]com
Clop
Example[.]com
Example.com
Example.com
CVE-example
Clop
Non-entity
Marketing Blurb
Security Advice
Report Metadata
Example[.]com
CVE-example
Graceful 
Spider
Graceful 
Spider
TXXXX
TXXXX
Evidence
Evidence
APT41
APT40
Clop
Clop
T1190
Example.com
Report
LLM
Clop
Clop
Example.com
Example.com
Four Character-Level Similarity Measures
Figure 2: The BEACON pipeline. Stage 1 turns each report into an anchored graph along three tracks: the LLM proposes
contextual entities, atomic behaviors, and IoCs, and every proposal is grounded in report evidence. Atomic behaviors are
located to evidence spans by token-weighted window scoring, and their candidate techniques are verified against official
ATT&CK definitions. IoCs are normalized before a final review. Candidate edges are then proposed between verified nodes by
same-sentence attachment, each confirmed by the LLM, and report-central entities are additionally paired with every anchor.
Stage 2 consolidates the per-report graphs: deterministic matching merges identical technique IDs, normalized IoC forms, and
exact names, and the remaining contextual entities enter three candidate channels: character similarity with per-type measures,
embedding similarity, and shared technique neighborhoods. Every candidate cluster passes node-level and cluster-level LLM
verification, and the neighborhood channel iterates until no new merge is accepted.
entity across reports, producing one consolidated graph𝐺∗that cov-
ers all three kinds of information. To suppress misclassification and
hallucination, both stages follow a propose-then-verify paradigm,
where every proposal is verified before entering the graph.
3.1
Space-Anchoring Stage
The anchoring stage extracts a CTI report 𝑟into a graph 𝐺=
(𝑉𝑎∪𝑉𝑐∪𝑉𝑜, 𝐸) with three types of nodes: technique anchors 𝑉𝑎,
mapped to an ATT&CK technique; contextual entities 𝑉𝑐, typed
as ThreatActor, Campaign, MalwareFamily, Tool, Organization,
Product, Location, or Sector; and IoCs 𝑉𝑜, typed as IP addresses,
domains, URLs, emails, file paths, Registry keys, file hashes, CVEs,
mutexes, or AES keys. The edge design follows two properties of
CTI reports. First, attack behaviors are a central component of CTI
reports, where contextual entities and IoCs enter the narrative as
their participants and traces [28, 40]. Second, attack behaviors can
be reliably mapped to MITRE ATT&CK, however a source words
them. Therefore, every edge in 𝐸connects a contextual entity or
IoC to a technique anchor, which gives the consolidation stage
a domain-specific signal for cross-source alignment. These node
types and edges form the predefined ontology of BEACON.
3.1.1
Behavior Grounding. BEACON maps the attack behaviors
in report 𝑟to ATT&CK techniques in four steps. First, since CTI
reports describe attacks as continuous narratives, where actions
that map to different techniques appear without clear boundaries,
the LLM decomposes the report into a list of atomic behaviors.
We define an atomic behavior 𝑏as one adversarial action, such
as exploiting one public-facing service or dropping one payload,
matching the granularity at which ATT&CK defines individual
techniques. Each atomic behavior is a single brief sentence, phrased
in the report’s own verbs and technical terms, with technical strings
such as domains and file paths kept unchanged.
Second, to ground every atomic behavior in report evidence,
BEACON uses a deterministic locator without relying on the LLM
4


---

BEACON: Behavior-Anchored Cross-Source Knowledge Graph Construction for Cyber Threat Intelligence
to identify evidence locations. Locating evidence requires the out-
put to match the report text exactly, while LLM outputs are gen-
erated rather than retrieved from the text, so generated evidence
is not guaranteed to exist in the report. A deterministic locator
instead guarantees that every evidence span is taken from the re-
port, avoiding this form of hallucination. The locator employs a
scoring-based mechanism that scores every bounded window of
consecutive sentences by the tokens shared with 𝑏, weighting each
match inversely to its frequency in the report so that rare terms
dominate. Before scoring, the locator stems the behavior and ev-
ery report sentence, and removes stopwords and the report’s most
frequent tokens, which carry little behavior-specific information.
Matched two- and three-word phrases receive an additional bonus,
since phrase matches are less likely to be coincidental than single-
token matches. The highest-scoring window becomes the evidence
span 𝑠(𝑏). If multiple windows share the same score, the locator
keeps only the shortest one to keep the later verification focused.
Third, since ATT&CK contains hundreds of techniques with
fine-grained definitional differences and a single candidate can eas-
ily miss the correct one, the LLM reads 𝑏together with 𝑠(𝑏) and
proposes multiple candidate ATT&CK techniques. The proposal
is responsible for recall, so the candidate techniques only need to
be relevant to the evidence. Candidates that do not exist in the
ATT&CK version BEACON uses are removed to suppress hallu-
cination. For example, the LLM can propose a revoked ATT&CK
technique that its training data still contains.
Fourth, BEACON verifies the remaining candidates against their
official definitions in the MITRE ATT&CK catalog, through an LLM-
as-a-judge mechanism [55]. The LLM receives the atomic behavior,
its evidence span, and each candidate’s official ATT&CK name
and definition, and judges each candidate separately. To keep the
scores consistent across judgments, the LLM assigns confidence
at predefined levels. Higher levels require the evidence to satisfy
more of the technique’s definition. To keep the judgment within
the evidence and prevent weak evidence from passing, we instruct
the LLM not to infer from its own knowledge and require conser-
vative scoring when the evidence is ambiguous. Candidates whose
confidence exceeds a threshold become anchors, each supported by
evidence within the report and carrying the official ATT&CK ID of
its technique, such as T1190, which is shared across all reports.
3.1.2
Contextual Entity and IoC Extraction. Since the LLM can miss
entities when it reads a long report in one pass, BEACON splits the
report into overlapping windows of consecutive sentences, so that
entities at window boundaries have enough context to be extracted.
The LLM then extracts contextual entity and IoC candidates with
types from each window, according to the predefined ontology.
Unlike an atomic behavior, which is rephrased by the LLM, a con-
textual entity or IoC is an exact substring of the report. BEACON
therefore lets the LLM specify the evidence sentences of each candi-
date directly, since an incorrect specification can be easily checked
by string matching. Since the candidates are LLM outputs and can
differ from the report text in characters such as letter case, BEACON
applies word-level matching to candidates that fail the exact check,
which normalizes the candidate and each sentence and accepts a
sentence if its word-set Jaccard overlap with the candidate exceeds
a threshold. To prevent an incorrect location from removing a real
entity, BEACON searches the rest of the window in the same way
if all named sentences fail both checks. Candidates found nowhere
in the report are removed as a form of hallucination.
To reduce duplicate verification, contextual entities and IoCs are
normalized and deduplicated first. Since IoC spellings are stable but
often obfuscated by type-specific conventions, a per-type determin-
istic normalizer converts each IoC into a normalized form, such as
removing the square brackets in a domain written as example[.]com.
IoCs with identical normalized forms then merge directly. Contex-
tual entities have no external standard form, so BEACON only low-
ercases names, removes extra spaces, and merges exact type–name
duplicates, leaving the remaining cases to the consolidation stage.
After deduplicating, BEACON verifies contextual entities and IoC
candidates. The same contextual entity can play different roles in
different contexts, so whether a candidate passes and matches its
type depends on its own evidence. The LLM checks each contextual
candidate separately, confirming that it matches its type definition
in the ontology, that it is a specific entity rather than a generic
description like “a popular website”, and that it is neither market-
ing language, nor defensive advice, nor report metadata such as
authors and publication dates. When uncertain, the LLM rejects
the candidate. IoC candidates instead have standardized forms after
normalization, so the LLM reviews them in one pass against the
full report, reporting only values to refuse or types to correct.
3.1.3
Anchored Attachment. Since there is no explicit relation be-
tween entities and ATT&CK techniques to extract like the triplets,
BEACON adds all edges after nodes. Verifying every entity–technique
pair with the LLM is costly, so BEACON proposes candidate edges
to reduce the pairs to verify. Since an entity that participates in
a behavior tends to be described near that behavior in the report,
BEACON proposes a candidate edge wherever the entity’s and the
anchor’s evidence span share at least one sentence. The LLM re-
ceives both spans and the anchor’s ATT&CK definition, and judges
whether the entity participates in that behavior. A candidate is
accepted only when the shared sentences describe the relation ex-
plicitly or support it directly. It is rejected when the entity and the
behavior merely appear in the same sentence or belong to the same
report topic, so that co-occurrence alone does not produce an edge.
A report often names its central entity, a threat actor, malware
family, or campaign, without repeating it in every behavior de-
scription. The evidence spans of these behaviors therefore never
contain the entity, and the edges between the central entity and its
behaviors are missed. BEACON therefore treats ThreatActor, Cam-
paign, and MalwareFamily as report-central types and processes
entities of these types in two passes. The LLM first judges, based
on the report text and the ATT&CK techniques with their MITRE
ATT&CK definitions, whether the entity is the central subject of
the report, that is, whether the report describes the behaviors as
performed by this entity. Co-occurrence with behaviors, shared
topics, or ambiguous evidence is not sufficient for this judgment.
Entities that pass this check are then paired with every technique
anchor in the report, and each pairing goes through the same ver-
ification process. Through these edges, every entity is linked to
anchors that carry official ATT&CK technique IDs shared across
all reports.
5


---

Li et al.
3.2
Consolidation Stage
Given the report-level graphs {𝐺1, . . . ,𝐺𝑛} extracted from CTI re-
ports, the consolidation stage merges the nodes that refer to the
same real-world entity and outputs one consolidated graph 𝐺∗. We
design a hierarchical alignment strategy that applies alignment
signals in decreasing order of determinism, and each merge pro-
posed by a later signal runs on the graph already merged by earlier
signals. The LLM thus judges a smaller set of ambiguous names,
reducing both cost and the chance of misclassification and halluci-
nation. Nodes merged by earlier signals also combine the evidence
of their members, giving the LLM richer context when it verifies
the candidates from less deterministic signals.
Deterministic Matching. Since the anchoring stage has given each
technique anchor its official ATT&CK ID, two anchors merge when
they carry the same ID. Two IoCs merge when they share a type
and their values are identical after per-type normalization. For a
few IoC types, identical strings do not reliably indicate the same
real-world entity, so BEACON keeps IoCs of these types unmerged.
For example, a mutex name, the name a program assigns to a lock,
can be reused by unrelated programs. Contextual entities with the
same type and normalized name merge directly. For threat actor
names in the same numbered naming scheme (a prefix such as APT,
UNC, FIN [14] or TA [38] followed by a number), BEACON applies
an additional type-specific normalization such as removing case
and leading-zero differences, and two names merge when both the
prefix and the number match. Every merged node keeps the source
report of each member (Figure 1, right), so any merged node can
be traced back to the sentences and sources that support it.
Similarity-based Matching. Since multiple vendors independently
report on the same threat under different naming conventions, the
names of the same entity can remain different even after normal-
ization, so contextual entities require more than deterministic rules.
There are three more candidate proposal channels, and each chan-
nel uses one alignment signal to propose candidate pairs. The pairs
from all channels are combined into per-type connected compo-
nents as candidate clusters that the LLM later verifies.
The character channel targets spelling variations such as “Cl0p”
versus “Clop”. Since entity types differ in the string patterns of
their names, the channel uses four measures, each suited to a differ-
ent pattern: Jaro–Winkler for short names that differ near the end,
such as a trailing version digit; Normalized Levenshtein for names
that differ by a few characters, such as Cl0p and Clop; Trigram
Cosine for multi-word names, since its score remains high when
words are inserted or reordered; and Trigram Jaccard, a stricter
overlap measure that ignores repetition, for short names where
repeated substrings inflate similarity. Each entity type is scored by
a weighted subset of the four measures, with its own normalization
before scoring. For example, campaign names remove the “Oper-
ation" prefix and are scored by trigram cosine, Jaro–Winkler, and
normalized Levenshtein. A pair becomes a candidate when its score
exceeds a threshold. The channel uses a higher threshold when
names are short, as short names are more likely to be similar by co-
incidence. Two additional rules handle CTI naming patterns where
character similarity can be misleading. First, threat actor pairs in
the same numbered naming scheme but with different numbers
are excluded from scoring, since names like APT41 and APT40 are
nearly identical in spelling but never the same entity. Second, a
short all-letter name is paired with any multi-word name whose
initials spell it, such as IRS and Internal Revenue Service, which
captures acronym pairs that the four measures miss.
The embedding channel handles entities whose names have char-
acter similarity too low for the character channel but may still be
semantically related, such as “Clop ransomware group” and “Cl0p”
for the same actor. A text-embedding model encodes each entity
name, and a pair becomes a candidate when its embedding cosine
similarity exceeds a threshold. To avoid comparing all pairs within
a type, the channel computes similarity only for name pairs with
basic lexical overlap: an identical normalized name, a shared word,
or a trigram Jaccard or Jaro–Winkler score above a low threshold.
Entities with numbered naming schemes are excluded from this
channel, since different numbers always indicate different entities,
a rule that embedding similarity can violate.
The technique-neighborhood channel targets entities with unre-
lated names, which neither the character nor the embedding chan-
nel can propose, such as Graceful Spider and Cl0p for the same actor.
It relies on the structure built in the anchoring stage. For each entity
𝑣, the channel collects its ATT&CK technique neighborhoods 𝑁𝑎(𝑣)
that 𝑣attaches to. Since entities sharing multiple attack behaviors
are likely the same entity, two entities become a candidate pair
when their neighborhoods share at least two ATT&CK techniques.
This channel runs last, since earlier merges combine member neigh-
borhoods and expose candidates that previously shared too few
ATT&CK techniques.
Every candidate cluster proposed by the three channels goes
through LLM verification. The LLM receives each member’s name,
type, source report, and evidence spans, and gives confidence judg-
ments at predefined levels on two granularities. Since a candidate
cluster can contain a few members that do not belong while the
rest are correct, a node-level judgment removes members that do
not fit the cluster while keeping the rest of the cluster valid. Since a
candidate cluster is a connected component of pairwise candidates,
it can contain names that were never proposed as a pair. That is, if
A pairs with B and B with C, all three enter one cluster even when
A and C are distinct entities. A cluster-level judgment therefore
decides whether all members refer to one real-world entity.
Iterative Closure. A merge combines the ATT&CK technique
neighborhoods of its members, so entities that previously shared too
few techniques can then become candidates through the technique-
neighborhood channel. To align the entities that only become candi-
dates after earlier merges, the channel iterates until no new merge
passes verification. Since merging creates no new names, every
pair the character and embedding channels could match was al-
ready available initially, so these channels do not iterate. Combining
neighborhoods also increases the overlap between unrelated en-
tities, but overlap only produces candidates, and every candidate
passes the same LLM verification before it is accepted. The iteration
always stops, since each round either merges nodes or, when no
candidate passes verification, leaves the neighborhoods unchanged
so that no new candidate can be proposed.
6


---

BEACON: Behavior-Anchored Cross-Source Knowledge Graph Construction for Cyber Threat Intelligence
4
Evaluation
4.1
Evaluation Setup
Datasets. We construct and release two datasets, BEACON-
Single for report-level extraction and BEACON-Group for cross-
source consolidation. Each instance is independently labeled by two
expert annotators, and disagreements are adjudicated by a senior
annotator. To our knowledge, BEACON-Single is the largest human-
annotated dataset for report-level CTI extraction, and BEACON-
Group is the first for cross-source CTI consolidation.
BEACON-Single contains 150 reports from 15 publishers, with
4,966 annotated node instances and 3,429 edge instances. BEACON-
Group organizes 100 reports from 31 publishers into 33 groups,
where each group covers the same or closely related threats. The
gold-standard consolidation merges the 2,908 report-level nodes
into 1,950 consolidated nodes, of which 528 combine nodes from
multiple reports, and the 2,278 edges into 1,537.
Research questions. Our evaluation answers three questions:
• RQ1: does the space-anchoring stage accurately extract all
three node types and their edges?
• RQ2: does the consolidation stage correctly align entities
across sources?
• RQ3: how much do verification in the space-anchoring stage
and each similarity-based channel in the consolidation stage
contribute?
Baselines. For RQ1 we compare five systems covering both lines
of CTI extraction. From the line focusing on contextual information,
CTINexus extracts ontology-constrained relation triplets end-to-
end with an LLM. From the line focusing on behaviors, AttacKG+
uses an LLM to construct temporal behavior graphs and map them
to ATT&CK techniques; SoK-NER is a rule- and resource-based
ATT&CK matching pipeline; and SIGMERGE-TTP is a supervised
BERT-based multi-subsequence classifier over a fixed ATT&CK
label set, whose recall upper bound on our dataset is 98.72%. The
step-guided LLM uses the same model, input, and target ontology
as BEACON, but produces all outputs in one guided call without the
anchoring pipeline. For RQ2 the baselines cover the three alignment
signals without technique anchors. CTINexus clusters entities of
the same type whose embedding similarity exceeds a threshold.
Since its released implementation deduplicates within one report,
we pool the report-level nodes of all reports in a group into one
input, so that it deduplicates across them. ComEM uses an LLM to
judge candidate pairs retrieved by lexical similarity and to select
the best match among the remaining candidates. GA-MGM applies
general-domain structural matching, jointly aligning all graphs
of a group using fixed text similarities and graph topology. All
baseline outputs are converted to our ontology by deterministic
rules without access to the gold annotations.
Metrics. All results are reported as micro precision, recall, and F1.
For RQ1, a predicted node or edge is correct when it matches a gold
node or edge of the same type in the same report, under one-to-one
matching. For RQ2, we score the final clusters in merge-link units: a
cluster of size 𝑘contributes 𝑘−1 links, and a predicted cluster 𝑃that
overlaps a gold cluster𝐺contributes max(|𝑃∩𝐺|−1, 0) correct links.
This metric rewards partially recovered clusters, penalizes over-
merging, and avoids the quadratic weight that pairwise counting
gives to large clusters. Overall consolidation results aggregate all
three node types. All consolidation systems take the same gold
report-level nodes as input, so RQ2 measures alignment quality
independently of extraction quality.
Implementation. Every system that requires an LLM uses GPT-
4o [35]. All systems use the same ATT&CK v17.1 snapshot, and
all thresholds were tuned once on a small held-out development
set and then fixed. Each reported number comes from a single run
per configuration, and we quantify sampling uncertainty with 95%
percentile bootstrap confidence intervals (10,000 resamples over
reports for RQ1 and over groups for RQ2) and paired bootstrap
tests for the main comparisons.
4.2
Results
4.2.1
RQ1: Anchoring-Stage Extraction. Table 1 reports the space-
anchoring results. BEACON achieves the best F1 on all five output
types (78.7% overall, 95% CI [77.4, 79.9]) and exceeds every baseline
on each type by at least 23%. The step-guided LLM, the one base-
line that covers all five outputs, shares BEACON’s model, so this
advantage comes from the pipeline of the space-anchoring stage
rather than from the model.
Technique anchors. For BEACON, TTP extraction measures the
quality of the technique anchors that the consolidation stage builds
on. SIGMERGE-TTP has high recall but much lower precision, be-
cause the classifier, trained on official ATT&CK text, assigns too
many techniques to the broader behavior descriptions in real re-
ports. AttacKG+ achieves the best F1 among the baselines but is
limited by its multi-step pipeline, where triplet rewriting and tactic–
technique labeling each lose information and accumulate errors.
The step-guided LLM has the lowest recall, as it completes all extrac-
tion in one long guided call and misses many behaviors. BEACON’s
advantage is concentrated in recall (84.60), since decomposing the
report into atomic behaviors allows multiple candidate techniques
to be proposed for each behavior separately, while verification
accepts a candidate only when its evidence span supports the tech-
nique’s ATT&CK definition.
Contextual entities and IoCs. CTINexus and AttacKG+ extract
entities only when they appear in relation triplets, so entities with-
out an explicit relation are not extracted. BEACON instead attaches
entities to technique anchors without requiring entity–entity rela-
tions, which explains its higher recall on both contextual entities
and IoCs. The difference is largest for CTINexus, whose IoC recall
is 14.04, since IoCs usually appear in lists rather than in sentences
describing relations, so a triplet extractor rarely finds a relation
that includes them. AttacKG+ extracts only attack-relevant triplets,
which further limits the range of contextual entities it covers, and
part of its low IoC score comes from IoC types that partially overlap
with ours. The step-guided LLM misses entities for the same reason
it misses behaviors. On IoCs, the step-guided LLM has higher pre-
cision but extracts conservatively and misses over half of the gold
IoCs, while BEACON’s F1 comes from deterministic normalization
and filtering.
7


---

Li et al.
Contextual entity
TTP
IoC
Ctx–TTP
IoC–TTP
Method
P
R
F1
P
R
F1
P
R
F1
P
R
F1
P
R
F1
CTINexus [6]
40.93
31.26
35.45
–
–
–
41.81
14.04
21.02
–
–
–
–
–
–
AttacKG+ [54]
22.85
24.82
23.80
54.70
44.99
49.37
9.99
24.48
14.19
–
–
–
–
–
–
SoK-NER [3]
–
–
–
26.61
31.34
28.78
–
–
–
–
–
–
–
–
–
SIGMERGE-TTP [4]
–
–
–
42.06
52.72
46.79
–
–
–
–
–
–
–
–
–
Step-guided LLM
73.23
34.64
47.03
68.22
27.57
39.27
88.65
42.98
57.89
39.91
11.07
17.33
38.69
17.09
23.70
BEACON (Ours)
90.66
68.08
77.77
72.51
84.60
78.09
83.68
79.32
81.44
59.10
62.64
60.82
56.68
45.56
50.52
Table 1: RQ1 space-anchoring extraction: micro precision, recall, and F1 (%) for the three node types and two edge types. Best in
bold, second-best underlined. “–” marks outputs that a baseline does not natively produce.
Contextual entity
IoC
Method
P
R
F1
P
R
F1
GA-MGM [50]
31.42
45.51
37.17
10.06
56.67
17.09
ComEM [51]
62.01
68.27
64.99
26.26
86.67
40.31
CTINexus [6]
85.17
82.85
84.00
32.61
100.00
49.18
BEACON (Ours)
98.59
89.74
93.96
100.00
96.67
98.31
Table 2: RQ2 consolidation-stage micro precision, recall, and
F1 (%) for contextual entities and IoCs. Best in bold, second-
best underlined.
Anchored edges. Edges are the hardest output, as a correct edge
requires two correct endpoints and verified evidence for their rela-
tion. The step-guided LLM is the only baseline that produces edges
of these types, since SoK-NER and SIGMERGE-TTP extract tech-
niques alone, and CTINexus and AttacKG+ do not relate entities to
techniques. IoC–TTP edges are the harder of the two, because IoCs
in lists rarely share a sentence with a behavior’s evidence span, so
fewer candidate edges are proposed.
4.2.2
RQ2: Cross-Source Consolidation.
Full consolidation. Table 2 reports the consolidation results. BEA-
CON achieves the best F1 on both node types (93.96 and 98.31) and
exceeds every baseline by at least 9%. Technique anchors, which
account for 304 of the 958 gold merge-link units, merge determin-
istically by shared technique IDs and are therefore excluded from
the comparison. CTINexus aligns entities by embedding similarity,
which incorrectly merges IoCs with similar strings (32.61 precision,
compared with BEACON’s 100 under deterministic matching) and
cannot propose aliases with unrelated names. ComEM cannot pro-
pose such candidates either, and the LLM cannot judge a pair that is
not proposed, which limits recall. Its precision is low because both
its BM25 blocking and its Flan-T5 match ranking prefer candidates
with overlapping context, and its selector rarely chooses the no-
match option, so distinct entities from one campaign are merged.
Its IoC alignment applies no CTI-specific normalization and relies
on the model’s own knowledge of IoC formats, which results in
a low F1 (40.31). GA-MGM aligns graphs by text similarity and
graph topology, but it expects dense graphs where entities connect
directly to each other, while the report graphs in this task are sparse,
with edges only between entities and technique anchors, so it loses
both precision and recall. Overall, shared technique neighborhoods
are the one structural signal that holds across sources, and gives
BEACON its additional, domain-specific alignment advantage.
Residual alignment. Table 3 evaluates the 220 gold contextual-
entity alignment units that deterministic rules cannot align, entities
Method
P
R
F1
CTINexus [6]
55.88
51.82
53.77
ComEM [51]
39.66
75.00
51.89
GA-MGM [50]
10.16
30.91
15.30
BEACON (Ours)
95.12
70.91
81.25
Table 3: RQ2 residual alignment: micro precision, recall, and
F1 (%) on the 220 gold contextual-entity alignment units that
deterministic rules cannot align. Best in bold, second best
underlined.
whose names differ in spelling or are entirely unrelated across
sources. A unit is kept when its members share neither the same
normalized name nor the same type–name pair, so the filter removes
only units whose names already match, which every compared sys-
tem aligns correctly. BEACON retains 81.25 F1 on this subset (95%
CI [72.9, 87.3]), while CTINexus drops to 53.77 ([45.5, 61.8]), as
the remaining cases concentrate on the aliases that differ most
across sources. The two intervals do not overlap, and the paired
difference is +27.5 F1 (𝑝< 10−4). Embedding similarity still aligns
roughly half of these units, but it cannot align names that are se-
mantically unrelated. ComEM achieves 51.89 F1, with the highest
recall in the table (75.00) but low precision (39.66), since its selector
merges nearly every proposed candidate. GA-MGM drops to 15.30,
as both of its signals fail on this subset. Its text similarities cannot
match unrelated names, while names in the same numbered naming
scheme look similar and are proposed as matches. With no rule
that excludes such pairs and no verification against report evidence,
these proposals become merges, which explains its precision of
10.16. Its graph topology signal does not help on these sparse report
graphs either. On this subset, the technique-neighborhood channel
is essential. Removing it drops F1 from 81.25 to 64.85, since candi-
dates proposed from shared technique neighborhoods and verified
against report evidence align the entities that both character and
embedding similarity miss.
Error analysis. Figure 3 shows the contextual-entity errors under
the merge-link metric, where missed merges are about ten times
more common than false merges. Over half of the missed alignments
come from entities whose names are entirely unrelated, such as
SPIKEDWINE and APT29, and whose technique neighborhoods
share too few techniques, so none of the three channels can propose
the pair. Nearly half of the remaining missed alignments involve
abbreviations and spelling variants, but their main cause is the LLM
8


---

BEACON: Behavior-Anchored Cross-Source Knowledge Graph Construction for Cyber Threat Intelligence
30
15
0
15
30
FN  ←  Error count  →  FP
Unrelated names
Spelling variant
Same-scheme
Shared techniques
Cross-lingual
Near-identical split
FN
FP
Figure 3: Contextual-entity error analysis under the merge-
link metric. Missed merges (FN) are shown on the left, and
false merges (FP) on the right.
Removed component
Scope
ΔP
ΔR
ΔF1
w/o Entity review
Ctx
−14.06
+7.67
−1.59
w/o TTP verification
TTP
−42.78
+8.54
−33.02
w/o IoC filtering
IoC
−24.75
+11.76
−9.88
w/o Edge confirmation
Ctx–TTP
−15.42
+2.71
−8.46
w/o Edge confirmation
IoC–TTP
−14.02
+4.11
−4.62
Table 4: RQ3: Space-anchoring verification ablation. Each row
removes one verification component and reports the change
in micro P/R/F1 (%) on the output type that the component
applies to, relative to full BEACON (Table 1).
verification, which is conservative and rejects candidates with weak
supporting evidence, as with the pair IRS and Internal Revenue
Service, proposed by the character channel but rejected. On the
false-merge side, most cases merge similar names or names in the
same numbered naming scheme, such as Storm-1175 with Storm-
0506. The exclusion rule covers a fixed list of prefixes that does not
include Storm, showing that the naming schemes in CTI are too
diverse to enumerate. The remaining false merges combine two
actors that share techniques but are different entities, as with Black
Basta and Cactus.
4.2.3
RQ3: Component Attribution.
Anchoring verification. Table 4 reports the ablation of each veri-
fication component in the space-anchoring stage. Every removal
raises recall but lowers precision more, so verification suppresses
misclassification and hallucination at a smaller cost in recall. TTP
verification has the largest effect, confirming the value of verifying
candidate techniques against official ATT&CK definitions. Entity
review has the most balanced effect, leaving F1 nearly unchanged.
IoC filtering changes both precision and recall substantially, as
IoCs such as paths and IPs are easy to extract by format but not
all of them are attack-related, so the filter removes many unrelated
ones while occasionally removing valid ones. Removing edge con-
firmation lowers precision substantially on both edge types, which
shows that many candidate edges proposed from shared sentences
reflect co-occurrence rather than participation.
Consolidation channels. Table 5 reports the ablation of each pro-
posal component in the consolidation stage. The full configuration
Contextual entity
Overall
Configuration
P
R
F1
F1
w/o char measures
98.39
88.30
93.07
95.52
w/o char rules
98.74
88.14
93.14
95.56
w/o embedding
99.03
81.57
89.46
93.30
w/o neighborhood
99.42
81.89
89.81
93.52
Full BEACON
98.59
89.74
93.96
96.07
Table 5: RQ3 consolidation-stage ablations using micro met-
rics (%). Each row removes one candidate proposal compo-
nent. Best in bold, second-best underlined.
achieves the best contextual and overall F1, and every removal
lowers recall while leaving precision nearly unchanged, since the
channels only propose candidates and the same LLM verification
decides every merge. The embedding and neighborhood channels
contribute the most to recall, by similar amounts. The neighbor-
hood channel aligns the entities with unrelated names, which the
embedding channel cannot propose. The two character-level com-
ponents contribute less, as their easy cases are already resolved
by deterministic normalization and their harder cases partially by
the embedding channel. Precision is highest when the neighbor-
hood channel is removed (99.42), indicating that the neighborhood
channel proposes the least reliable candidates of the three.
5
Conclusion
We identified that existing approaches to constructing knowledge
graphs from CTI reports extract only partial information and leave
the cross-source setting unexplored. We proposed BEACON based
on the insight that attack behaviors can be reliably mapped to
MITRE ATT&CK, while contextual entities and IoCs describe their
participants and traces. The space-anchoring stage attaches con-
textual entities and IoCs to ATT&CK technique anchors, placing
per-report graphs in one canonical space. The consolidation stage
merges them by signals applied in decreasing order of determinism,
where the shared technique neighborhoods are critical for aligning
entities with unrelated names. To suppress misclassification and
hallucination, both stages follow a propose-then-verify paradigm
grounded in report evidence. On two human-annotated datasets
that we construct and release, BEACON outperforms all baselines.
Ethical Considerations
BEACON supports defensive threat analysis by organizing publicly
available CTI reports and grounding behaviors in public MITRE
ATT&CK definitions. It generates no attack procedures, exploit
code, or operational instructions beyond what the source reports
already disclose, and therefore introduces limited dual-use risk be-
yond the original public sources. The datasets are built from publicly
released reports and contain no private telemetry or undisclosed
victim data. Victim-related information is retained only where
the source report publicly discloses it and the schema requires
it. Annotators were informed of the research use of their work
and compensated accordingly. Released materials preserve source
attribution and comply with the original publishers’ access terms,
with redistribution-restricted text provided as metadata and derived
annotations.
9


---

Li et al.
References
[1] Md Tanvirul Alam, Dipkamal Bhusal, Youngja Park, and Nidhi Rastogi. 2023.
Looking Beyond IoCs: Automatically Extracting Attack Patterns from External
CTI. In Proceedings of the 26th International Symposium on Research in Attacks,
Intrusions and Defenses (RAID ’23). 92–108.
[2] Mikhail Bilenko and Raymond J. Mooney. 2003. Adaptive Duplicate Detection
Using Learnable String Similarity Measures. In Proceedings of the Ninth ACM
SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD
’03). 39–48.
[3] Marvin Büchel, Tommaso Paladini, Stefano Longari, Michele Carminati, Stefano
Zanero, Hodaya Binyamini, Gal Engelberg, Dan Klein, Giancarlo Guizzardi,
Marco Caselli, Andrea Continella, Maarten van Steen, Andreas Peter, and Thijs
van Ede. 2025. SoK: Automated TTP Extraction from CTI Reports–Are We There
Yet?. In 34th USENIX Security Symposium (USENIX Security ’25). 4621–4641.
[4] Yongxin Cai, Jing Qiu, Qingming Li, Du Cheng, and Lei Chen. 2026. From Texts to
Rules: Generating Sigma Rules with Large Language Models from Cyber Threat
Reports. In 35th USENIX Security Symposium (USENIX Security ’26).
[5] Wenrui Cheng, Tiantian Zhu, Tieming Chen, Qixuan Yuan, Jie Ying, Hongmei
Li, Chunlin Xiong, Mingda Li, Mingqi Lv, and Yan Chen. 2025. CRUcialG: Recon-
struct Integrated Attack Scenario Graphs by Cyber Threat Intelligence Reports.
IEEE Transactions on Dependable and Secure Computing 22, 6 (2025), 6345–6360.
doi:10.1109/TDSC.2025.3584826
[6] Yutong Cheng, Osama Bajaber, Saimon Amanuel Tsegai, Dawn Song, and Peng
Gao. 2025. CTINexus: Automatic cyber threat intelligence knowledge graph
construction using large language models. In 2025 IEEE 10th European Symposium
on Security and Privacy (EuroS&P ’25). 923–938.
[7] Yutong Cheng, Yang Liu, Changze Li, Dawn Song, and Peng Gao. 2026. CTI-
Connect: A Benchmark for Retrieval-Augmented LLMs over Heterogeneous
Cyber Threat Intelligence. In Proceedings of the 32nd ACM SIGKDD Conference
on Knowledge Discovery and Data Mining V.2 (KDD ’26). 8741–8752.
[8] William W. Cohen and Jacob Richman. 2002. Learning to Match and Cluster
Large High-Dimensional Data Sets for Data Integration. In Proceedings of the
Eighth ACM SIGKDD International Conference on Knowledge Discovery and Data
Mining (KDD ’02). 475–480.
[9] Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. 2019. BERT:
Pre-training of Deep Bidirectional Transformers for Language Understanding. In
Proceedings of the 2019 Conference of the North American Chapter of the Association
for Computational Linguistics: Human Language Technologies, Volume 1 (Long
and Short Papers) (NAACL-HLT ’19). 4171–4186.
[10] Yağmur Ernalbant. 2025. Cl0p’s Oracle EBS Zero-Day Campaign: What We Know
So Far. https://socradar.io/blog/cl0p-oracle-ebs-zeroday-campaign/. SOCRadar,
published November 21, 2025; updated November 24, 2025.
[11] Filigran. 2026. OpenCTI Documentation. Online documentation. Accessed:
2026-05-16. https://docs.opencti.io/latest/
[12] Cheng Fu, Xianpei Han, Jiaming He, and Le Sun. 2020. Hierarchical Matching
Network for Heterogeneous Entity Resolution. In Proceedings of the Twenty-Ninth
International Joint Conference on Artificial Intelligence (IJCAI ’20). 3665–3671.
[13] Peng Gao, Xiaoyuan Liu, Edward Choi, Sibo Ma, Xinyu Yang, and Dawn Song.
2024. ThreatKG: An AI-Powered System for Automated Open-Source Cyber
Threat Intelligence Gathering and Management. In Proceedings of the 1st ACM
Workshop on Large AI Systems and Models with Privacy and Safety Analysis
(LAMPS ’24). 1–12.
[14] Google Cloud. [n. d.]. Mandiant Victim Notification Program. Google Cloud
Security Resources. Accessed: 2026-08-21. https://cloud.google.com/security/
resources/insights/mandiant-victim-notification-program
[15] Md Nazmul Haque, Sivana Hamer, Brandon Wroblewski, Md Rayhanur Rah-
man, and Laurie Williams. 2026. Beyond Single Reports: Evaluating Automated
ATT&CK Technique Extraction in Multi-Report Campaign Settings.
arXiv
preprint arXiv:2604.07470 (2026).
[16] Aidan Hogan, Eva Blomqvist, Michael Cochez, Claudia d’Amato, Gerard De Melo,
Claudio Gutierrez, Sabrina Kirrane, José Emilio Labra Gayo, Roberto Navigli,
Sebastian Neumaier, et al. 2021. Knowledge graphs. Comput. Surveys 54, 4 (2021),
1–37.
[17] Ghaith Husari, Ehab Al-Shaer, Mohiuddin Ahmed, Bill Chu, and Xi Niu. 2017.
TTPDrill: Automatic and Accurate Extraction of Threat Actions from Unstruc-
tured Text of CTI Sources. In Proceedings of the 33rd Annual Computer Security
Applications Conference (ACSAC ’17). 103–115.
[18] Xuhui Jiang, Yinghan Shen, Zhichao Shi, Chengjin Xu, Wei Li, Zixuan Li, Jian
Guo, Huawei Shen, and Yuanzhuo Wang. 2024. Unlocking the Power of Large
Language Models for Entity Alignment. In Proceedings of the 62nd Annual Meeting
of the Association for Computational Linguistics (Volume 1: Long Papers) (ACL ’24).
7566–7583.
[19] Christopher S. Johnson, Mark L. Badger, David A. Waltermire, Julie Snyder,
and Clem Skorupka. 2016. Guide to Cyber Threat Information Sharing. NIST
Special Publication 800-150. National Institute of Standards and Technology.
doi:10.6028/NIST.SP.800-150
[20] Eduard Kovacs. 2025. Nearly 30 Alleged Victims of Oracle EBS Hack Named
on Cl0p Ransomware Site. https://www.securityweek.com/nearly-30-alleged-
victims-of-oracle-ebs-hack-named-on-cl0p-ransomware-site/. SecurityWeek,
November 10, 2025.
[21] Udesh Kumarasinghe, Ahmed Lekssays, Husrev Taha Sencar, Sabri Boughorbel,
Charitha Elvitigala, and Preslav Nakov. 2024. Semantic Ranking for Automated
Adversarial Technique Annotation in Security Text. In Proceedings of the 19th
ACM Asia Conference on Computer and Communications Security (ASIA CCS ’24).
49–62.
[22] Simon Lacoste-Julien, Konstantina Palla, Alex Davies, Gjergji Kasneci, Thore
Graepel, and Zoubin Ghahramani. 2013. SiGMa: Simple Greedy Matching for
Aligning Large Knowledge Bases. In Proceedings of the 19th ACM SIGKDD Interna-
tional Conference on Knowledge Discovery and Data Mining (KDD ’13). 572–580.
[23] Ravie Lakshmanan. 2025. CL0P-Linked Hackers Breach Dozens of Organizations
Through Oracle Software Flaw. https://thehackernews.com/2025/10/cl0p-linked-
hackers-breach-dozens-of.html. The Hacker News, October 10, 2025.
[24] Valentine Legoy, Marco Caselli, Christin Seifert, and Andreas Peter. 2020. Auto-
mated Retrieval of ATT&CK Tactics and Techniques for Cyber Threat Reports.
In 1st Cyber Threat Intelligence Symposium (CTI ’20).
[25] Ahmed Lekssays, Utsav Shukla, Husrev Taha Sencar, and Md Rizwan Parvez. 2025.
TechniqueRAG: Retrieval Augmented Generation for Adversarial Technique
Annotation in Cyber Threat Intelligence Text. In Findings of the Association for
Computational Linguistics: ACL 2025 (Findings of ACL ’25). 20913–20926.
[26] Lingzi Li, Cheng Huang, and Junren Chen. 2024. Automated Discovery and
Mapping ATT&CK Tactics and Techniques for Unstructured Cyber Threat Intel-
ligence. Computers & Security 140 (2024), 103815.
[27] Yuliang Li, Jinfeng Li, Yoshihiko Suhara, AnHai Doan, and Wang-Chiew Tan.
2020. Deep entity matching with pre-trained language models. arXiv preprint
arXiv:2004.00584 (2020).
[28] Zhenyuan Li, Jun Zeng, Yan Chen, and Zhenkai Liang. 2022. AttacKG: Construct-
ing technique knowledge graph from cyber threat intelligence reports. In 27th
European Symposium on Research in Computer Security (ESORICS ’22). 589–609.
[29] Francesco Marchiori, Mauro Conti, and Nino Vincenzo Verde. 2023. STIXnet: A
Novel and Modular Solution for Extracting All STIX Objects in CTI Reports. In
Proceedings of the 18th International Conference on Availability, Reliability and
Security (ARES ’23). 1–11.
[30] Vasileios Mavroeidis and Siri Bromander. 2017. Cyber threat intelligence model:
an evaluation of taxonomies, sharing standards, and ontologies within cyber
threat intelligence. In 2017 European Intelligence and Security Informatics Confer-
ence (EISIC ’17). 91–98.
[31] Emanuele Mezzi, Fabio Massacci, and Katja Tuma. 2025. Large Language Models
Are Unreliable for Cyber Threat Intelligence. In 20th International Conference on
Availability, Reliability and Security (ARES ’25). 343–364.
[32] Sidharth Mudgal, Han Li, Theodoros Rekatsinas, AnHai Doan, Youngchoon Park,
Ganesh Krishnan, Rohit Deep, Esteban Arcaute, and Vijay Raghavendra. 2018.
Deep Learning for Entity Matching: A Design Space Exploration. In Proceedings
of the 2018 International Conference on Management of Data (SIGMOD ’18). 19–34.
[33] Tu Nguyen, Nedim Šrndić, and Alexander Neth. 2024.
Noise Contrastive
Estimation-Based Matching Framework for Low-Resource Security Attack Pat-
tern Recognition. In Findings of the Association for Computational Linguistics:
EACL 2024 (Findings of EACL ’24). 355–373.
[34] OASIS Cyber Threat Intelligence Technical Committee. 2021. STIX Version 2.1.
OASIS Standard. OASIS Open. https://docs.oasis-open.org/cti/stix/v2.1/os/stix-
v2.1-os.html
[35] OpenAI. 2024. GPT-4o System Card. arXiv preprint arXiv:2410.21276 (2024).
[36] Vittorio Orbinato, Mariarosaria Barbaraci, Roberto Natella, and Domenico Cotro-
neo. 2022. Automatic mapping of unstructured cyber threat intelligence: An
experimental study: (Practical Experience Report). In 2022 IEEE 33rd International
Symposium on Software Reliability Engineering (ISSRE ’22). 181–192.
[37] Youngja Park and Taesung Lee. 2022. Full-Stack Information Extraction System
for Cybersecurity Intelligence. In Proceedings of the 2022 Conference on Empirical
Methods in Natural Language Processing: Industry Track (EMNLP ’22 Industry
Track). 531–539.
[38] Proofpoint Threat Research Team. 2025. Call It What You Want: Threat Actor De-
livers Highly Targeted Multistage Polyglot Malware. Proofpoint Threat Insight.
Accessed: 2026-08-21. https://www.proofpoint.com/us/blog/threat-insight/call-
it-what-you-want-threat-actor-delivers-highly-targeted-multistage-polyglot
[39] Aakanksha Saha, James Mattei, Jorge Blasco, Lorenzo Cavallaro, Daniel Votipka,
and Martina Lindorfer. 2025. Expert Insights into Advanced Persistent Threats:
Analysis, Attribution, and Challenges. In 34th USENIX Security Symposium
(USENIX Security ’25). 2185–2204.
[40] Kiavash Satvat, Rigel Gjomemo, and V. N. Venkatakrishnan. 2021. Extractor:
Extracting attack behavior from threat reports. In 2021 IEEE European Symposium
on Security and Privacy (EuroS&P ’21). 598–615.
[41] SecurityWeek. 2026. SecurityWeek. Accessed: 2026. https://www.securityweek.
com/
[42] SOCRadar. 2026. SOCRadar Blog. Accessed: 2026. https://socradar.io/blog/
10


---

BEACON: Behavior-Anchored Cross-Source Knowledge Graph Construction for Cyber Threat Intelligence
[43] Blake E. Strom, Andy Applebaum, Doug P. Miller, Kathryn C. Nickels, Adam G.
Pennington, and Cody B. Thomas. 2020. MITRE ATT&CK: Design and Philosophy.
Technical Report. The MITRE Corporation. https://www.mitre.org/sites/default/
files/2021-11/prs-19-01075-28-mitre-attack-design-and-philosophy.pdf
[44] Manuel Suarez-Roman, Francesco Marchiori, Mauro Conti, and Juan Tapiador.
2026. The CTI Echo Chamber: Fragmentation, Overlap, and Vendor Specificity in
Twenty Years of Cyber Threat Reporting. arXiv preprint arXiv:2602.17458 (2026).
[45] Fabian M. Suchanek, Serge Abiteboul, and Pierre Senellart. 2011. PARIS: Proba-
bilistic Alignment of Relations, Instances, and Schema. Proceedings of the VLDB
Endowment 5, 3 (2011), 157–168.
[46] Yufei Tao, Adam Hiatt, Erik Haake, Antonie J. Jetter, and Ameeta Agrawal. 2024.
When Context Leads but Parametric Memory Follows in Large Language Models.
In Proceedings of the 2024 Conference on Empirical Methods in Natural Language
Processing (EMNLP ’24). 4034–4058.
[47] The Hacker News. 2026.
The Hacker News.
Accessed: 2026.
https://
thehackernews.com/
[48] The MITRE Corporation. 2025. Remote Services (T1021). MITRE ATT&CK.
Version 1.6, accessed August 22, 2026. https://attack.mitre.org/techniques/T1021/
[49] The MITRE Corporation. 2026. Exploitation of Remote Services (T1210). MITRE
ATT&CK. Version 1.2, accessed August 22, 2026.
https://attack.mitre.org/
techniques/T1210/
[50] Runzhong Wang, Junchi Yan, and Xiaokang Yang. 2020. Graduated Assignment
for Joint Multi-Graph Matching and Clustering with Application to Unsupervised
Graph Matching Network Learning. In Advances in Neural Information Processing
Systems 33 (NeurIPS ’20). 19908–19919.
[51] Tianshu Wang, Xiaoyang Chen, Hongyu Lin, Xuanang Chen, Xianpei Han,
Le Sun, Hao Wang, and Zhenyu Zeng. 2025. Match, Compare, or Select? An
Investigation of Large Language Models for Entity Matching. In Proceedings
of the 31st International Conference on Computational Linguistics (COLING ’25).
96–109.
[52] Xiuzhang Yang, Ruijie Zhong, Yuling Chen, Guojun Peng, Di Yao, Chaofan
Chen, Chenyang Wang, Dongni Zhang, Yilin Zhou, and Zixuan Yang. 2026. CTI-
Thinker: An LLM-Driven System for CTI Knowledge Graph Construction and
Attack Reasoning. Cybersecurity 9, 1 (2026), 106.
[53] Bowen Zhang and Harold Soh. 2024. Extract, Define, Canonicalize: An LLM-
based Framework for Knowledge Graph Construction. In Proceedings of the 2024
Conference on Empirical Methods in Natural Language Processing (EMNLP ’24).
9820–9836.
[54] Yongheng Zhang, Tingwen Du, Yunshan Ma, Xiang Wang, Yi Xie, Guozheng
Yang, Yuliang Lu, and Ee-Chien Chang. 2025. AttacKG+: Boosting attack graph
construction with large language models. Computers & Security 150 (2025),
104220.
[55] Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu,
Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric P. Xing, Hao Zhang,
Joseph E. Gonzalez, and Ion Stoica. 2023. Judging LLM-as-a-Judge with MT-
Bench and Chatbot Arena. In Advances in Neural Information Processing Systems
36 (NeurIPS ’23). 46595–46623.
11
