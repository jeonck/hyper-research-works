---
title: Towards Automated Cyber Threat Intelligence
id: towards-automated-cyber-threat-intelligence
tags:
- attack-ontology-drift-cti-85bc51
- pin-rate-survey
created: '2026-09-12T21:33:53.811834Z'
updated: '2026-09-12T21:44:25.524610Z'
source: https://arxiv.org/abs/2608.23185v1
source_domain: arxiv.org
fetched_at: '2026-09-12T21:33:53.810515Z'
fetch_provider: crawl4ai
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'arXiv 2608.23185v1: 0 ATT&CK technique-ID occurrences, below the pin-rate-survey
  inclusion threshold of 3.'
raw_file: raw/towards-automated-cyber-threat-intelligence.pdf
doi: arXiv:2608.23185v1
---

Towards Automated Cyber Threat Intelligence
Elicitation in Underground Forums
Lorenzo Bossi∗, Federico Saccani∗, Francesco Panebianco∗, Antonio Maci†∗,
Stefano Zanero∗, Stefano Longari∗, Michele Carminati∗
∗Politecnico di Milano
†BV TECH S.p.A.
{lorenzo.bossi, francesco.panebianco, antonio.maci, stefano.zanero,
stefano.longari, michele.carminati}@polimi.it
federico.saccani@mail.polimi.it
Abstract—Cyber threat intelligence from underground forums
has traditionally relied on passive monitoring. However, as users
have become more aware of large-scale data collection, valuable
intelligence has become increasingly rare in open forums, often
migrating instead to private or harder-to-reach spaces, making
passive approaches inadequate. Building on the intuition that
relevant information can be obtained through active elicitation,
this paper presents DarkBot, to the best of our knowledge, the
first multi-agent LLM-based system for active CTI elicitation in
underground forums. DarkBot decomposes the interaction task
across eleven specialized agents organized into three functional
blocks: engagement gating for relevance and safety filtering,
context-aware question generation driven by MITRE ATT&CK
tactics, and linguistic style adaptation to better align with real
forum users. In a controlled evaluation across 100 CrimeBB con-
versations, the system recovered 72.8% of the validated MITRE
ATT&CK techniques present in the original discussions by
observing only the initial post at the start of each interaction, and
it consistently outperformed a monolithic baseline. The proposed
layered safety design contained all injected jailbreak attempts at
the pipeline level. These results were further supported by real-
world experiments: in a prospective matched deployment, threads
assigned to DarkBot accumulated an average of 3.85 more CTI
entities than their controls over seven days, and across 104 live
forum conversations, the system elicited CTI-relevant disclosures
without observed account suspensions, moderator interventions,
or explicit accusations of automated participation.
I. INTRODUCTION
Cyber threat intelligence (CTI) is the process of collect-
ing, analyzing, and interpreting cyber threat data to sup-
port proactive security decisions. Rather than focusing only
on raw artifacts such as indicators of compromise (IoCs),
it turns heterogeneous and often unstructured information
into contextualized actionable insights (e.g., attack tactics,
techniques, and procedures (TTPs), motivations, and likely
targets) aligned with an organization’s specific risk profile
[1]. In contemporary threat landscapes, a significant portion
of CTI is derived from online communities, such as public
forums and underground platforms, which play a central role
in this ecosystem, as discussions within them often anticipate
the emergence of vulnerabilities, data leaks, or attack cam-
paigns [2]. CTI data collection practices are largely based
on passive strategies, including automated crawling and mon-
itoring of publicly accessible sources. However, the structure
of these ecosystems is evolving, as recent studies suggest a
gradual shift towards more private or hidden platforms, with
users becoming more aware of large-scale data collection,
reducing the visibility of operationally relevant information in
open forums [2]. Moreover, online discussions are inherently
interactive; relevant information often emerges through dialog,
clarification, and targeted questioning rather than appearing
spontaneously. These characteristics highlight a key limitation
of purely passive collection approaches, which may fail to
surface valuable insights that require active engagement.
In parallel, recent advances in generative artificial intelli-
gence (AI) have fostered growing interest in the use of large
language models (LLMs) within CTI [3]. These models are in-
creasingly adopted as components of automated CTI pipelines,
where they assist both downstream analysis and earlier stages,
such as data collection, by processing and interpreting large
volumes of unstructured content [4]. More recent approaches
further investigate multi-agent LLM-based systems that enable
distributed reasoning and task decomposition, improving the
robustness and depth of extracted intelligence through coordi-
nated interactions among specialized agents [5], [6].
Building on these insights, we explore a novel paradigm for
CTI data collection based on controlled interaction with online
communities. Specifically, we investigate whether carefully
designed conversational agents can stimulate discussions in
publicly accessible environments to generate relevant threat
intelligence. Unlike existing multi-agent CTI systems, which
primarily focus on offline analysis of previously collected
data (e.g., relevance classification or static content triage) [6],
the proposed approach targets active and iterative information
elicitation through direct interaction with real users. We move
from passive analysis to credible undercover participation in
underground online discussions, where the system engages as
a regular user to extract CTI-relevant insights.
Consequently, we propose an LLM-based multi-agent sys-
tem, namely DarkBot, that operates during the data-collection
phase. The system coordinates multiple specialized agents
for contextual analysis, linguistic adaptation, and question
generation, enabling targeted, context-aware information elic-
itation. Designed to operate in adversarial and dynamic envi-
ronments such as underground forums, DarkBot must ensure
arXiv:2608.23185v1  [cs.CR]  24 Aug 2026


---

safe engagement, maintain contextual awareness, and produce
linguistically credible interactions. To this end, it follows an
iterative workflow: given an initial thread, DarkBot evalu-
ates whether engagement is appropriate, generates context-
consistent questions, and continuously analyzes incoming
replies to decide whether to continue or terminate the inter-
action. Rather than relying on a single monolithic model, the
architecture decomposes the overall task into subtasks handled
by multiple agents organized into three main functional blocks.
The engagement gating block addresses safety and relevance
by filtering prohibited content and detecting adversarial inputs.
Second, the context understanding and question generation
block focuses on thread analysis, elicitation planning, and
target question generation. Lastly, the linguistic style and
credibility block ensure alignment with the communication
style of real users, improving the ability of DarkBot to blend
into the target environment. Our evaluation shows that, across
100 simulated CrimeBB conversations,
DarkBot recovers
72.8% of the MITRE ATT&CK techniques present in the
original conversation using targeted questions, starting only
from the initial post, while ablation studies confirm that multi-
agent decomposition consistently outperforms a monolithic
baseline. The layered safety architecture contained 100% of
the tested jailbreak attempts at the end-to-end pipeline level,
despite imperfect individual components. In isolation, the DE-
FENSIVEAGENT detected 92.8% of jailbreak prompts, while
the final FILTERAGENT blocked 85.6% of slang-rewritten
policy-violating messages in a separate worst-case evaluation,
with undetected questions being borderline content. In a
prospective experiment with 20 matched topic pairs, threads
assigned to DarkBot accumulated on average 3.85 more CTI
entities compared to their control. Deployed across 104 live
conversations and 213 published messages on surface- and
dark-web forums, DarkBot elicits CTI that would not have
surfaced without active probing, including details of active
data breaches and newly published attack techniques already
being tested in the wild, without ever triggering bans, moder-
ator actions, or AI accusations.
The contributions of this paper are the following:
• We introduce DarkBot, to the best of our knowl-
edge, the first multi-agent LLM-based system for ac-
tive CTI elicitation in public underground forums. The
system decomposes the interaction process into eleven
specialized agents responsible for engagement gating,
ATT&CK-guided elicitation planning, question genera-
tion, adversarial-input handling, and community-specific
linguistic adaptation.
• We design and evaluate a layered safety architecture
for operation in adversarial forum environments. The
architecture combines relevance filtering, reply analysis,
jailbreak detection, and post-generation filtering, detects
jailbreak attempts at the pipeline level, and blocks most
policy-violating outgoing messages.
• We evaluate active participation in real forum environ-
ments through both a prospective matched experiment
and deployment in 104 live conversations. The system
elicited CTI-relevant disclosures without account suspen-
sions, moderator interventions, or explicit accusations of
automated participation during the study period.
II. BACKGROUND
Open source intelligence (OSINT) and CTI are central to
modern cybersecurity. In this context, OSINT refers to the
collection and analysis of information from publicly acces-
sible or semi-open sources, including websites, repositories,
vulnerability databases, and underground forums [7]–[10]. CTI
builds on this information to produce structured knowledge
about threat actors, techniques, vulnerabilities, and malicious
infrastructure for defensive decision-making [11]. A key refer-
ence in this process is the MITRE ATT&CK framework [12],
[13], which organizes adversarial behavior into TTPs and helps
guide both threat collection and interpretation [14], [15]. Re-
cent work has expanded OSINT and CTI through large-scale
data analysis and AI-based methods. In particular, LLMs are
being progressively incorporated into CTI extraction pipelines
because of their ability to support multiple steps of the process,
including knowledge assessment, vulnerability analysis, and
threat actor attribution, as highlighted by benchmark-oriented
evaluations such as CTIBench [16]. In more specialized set-
tings, they have been used for report summarization and data
augmentation to improve downstream classification, e.g., for
extracting MITRE ATT&CK techniques from unstructured
CTI reports [17]. More recent systems also use LLMs, com-
bining fine-tuning or in-context learning for entity and rela-
tion extraction with retrieval-augmented reasoning modules to
support attack chain inference and question answering over
structured CTI knowledge [18]. Techniques such as zero-
shot and few-shot prompting enable such models to perform
tasks ranging from question answering and summarization to
reasoning and decision support by embedding task instructions
and examples directly within the prompt [19], [20]. Recently,
research has explored prompt chaining and multi-agent LLM
architectures to address more complex workflows. In these
approaches, multiple prompts or specialized agents interact
sequentially, with the output of one model invocation serving
as the input for subsequent reasoning steps. Prompt chaining
allows tasks to be decomposed into smaller subtasks, enabling
more structured reasoning. Similarly, multi-agent frameworks
employ multiple LLM-based agents with specialized roles
that collaborate to solve complex problems through iterative
interaction and information exchange [21]. These approaches
leverage the compositional capabilities of LLMs [22], [23] to
orchestrate more sophisticated reasoning pipelines than those
achievable with a single prompt invocation.
III. RELATED WORK
Previous work has explored chatbots for investigative and
forensic purposes, mainly in three distinct directions. First,
conceptual work [24] has proposed chatbots as intelligence-
gathering agents for evidence collection on the dark web,
highlighting their potential for continuous operation, rapid
2


---

interaction, and support for law-enforcement investigations,
but without presenting a fully implemented or evaluated sys-
tem. Second, works such as ScamChatBot [25] have shown
that LLMs can be used to actively engage malicious actors
at scale and uncover scam tactics, coordination patterns, and
payment infrastructures. Similarly, Yao et al. [26] deploy an
LLM to engage with illicit scammers on Telegram, demon-
strating conversational infiltration, but using a single-agent
design and targeting transactional indicators (e.g., payment
methods). However, these systems focus on social media scam
ecosystems rather than on recurring engagement for CTI elic-
itation. Third, other research [27] investigated chatbot-based
support for digital forensics, for example, by assisting inves-
tigators in analyzing logs, emails, and image metadata, but
these systems operate primarily on already-collected evidence
rather than through live, adversarial interaction with forum
users. More broadly, LLMs have also been shown to pose
a privacy threat to ordinary users, as adaptive psychological
profiling and communication strategies can be weaponized
to stealthily elicit personal information [28]. Taken together,
these studies suggest that conversational agents can support
cyber investigations both passively and actively, yet they leave
open the question of how such systems should be designed
to elicit sustained, credible, and goal-directed information in
underground communities.
In parallel to the aforementioned strategies, multi-agent
LLM frameworks have been proposed to decompose other
complex security tasks into specialized roles (e.g., passive
analysis of forum conversations [6], classification, translation,
planning), often improving performance on complex pipelines
[29].
Positioning of this work. To the best of our knowledge, no
prior work has investigated multi-agent LLM systems that
actively engage in recurring, interactive conversations with
human users on underground forums to elicit CTI-related
information. Thus, we design and evaluate an interactive multi-
agent LLM-based system for CTI-oriented information elici-
tation in public underground forums. We investigate whether
role decomposition across multiple agents can improve the
effectiveness, robustness, and control of interactive CTI elici-
tation in adversarial conversational settings.
IV. MOTIVATION AND PROBLEM STATEMENT
Public underground forums have historically been a valuable
source of CTI [9]. However, in recent years, the quantity
and quality of information available in these public spaces
have steadily decreased [2], as threat actors have progressively
migrated their most relevant discussions to less public, harder-
to-reach spaces. Meanwhile, the rapid advancement of large
language models opens new opportunities for automated in-
teractive collection methods, potentially enabling agents to
stimulate discussions and surface relevant knowledge from
private channels into public spaces, where it can be analyzed
for proactive defense. Formally, starting from an initial state
of a forum thread, comprising the original post and any
replies prior to the system’s intervention, a passive monitoring
approach can extract a set of CTI items (e.g., TTPs and IoCs).
The system then engages in an iterative, turn-based interaction:
at each turn, it observes the current thread state and decides
either to publish a follow-up message or to terminate. After
the interaction, the final thread state contains the original
content plus all bot-elicited exchanges. From the final state,
discarding the bot’s own messages and retaining only human
contributions, one can extract a set of CTI items. The objective
is to maximize the CTI delta, that is, the intelligence present
in the human contributions of the full conversation that was
not already present in the thread before the system intervened.
A system is considered more effective the larger the CTI delta,
meaning that active engagement surfaced intelligence that pas-
sive observation of the initial state alone would have missed.
In practice, however, the problem imposes three additional
constraints: (1) The system must generate messages that are
not easily distinguishable from those of legitimate users, as
detection would compromise the system’s ability to operate,
(2) The system must be capable of resisting adversarial manip-
ulation as it operates in an adversarial setting, (3) The system
must bound the frequency and number of turns per thread and
recognize when to terminate, as overly insistent interactions
raise suspicion and increases detection risk. These practical
constraints raise three fundamental challenges in the design
of an automated system capable of solving this problem.
Adversarial environment. The system operates in an en-
vironment where human users may be actively suspicious,
adversarial, or technically sophisticated. Standard LLM safety
mechanisms, designed for cooperative settings, are insufficient.
They may fail to detect manipulation attempts that exploit
the conversational context, and they tend toward over-refusal:
a model that rejects any discussion of malware, exploits, or
illegal activity cannot function in underground forums.
Sparse and implicit signals. CTI in underground forums is
rarely stated explicitly as it is in more structured sources
(e.g., threat reports and vulnerability databases). Relevant
intelligence is embedded in fragmented and informal language.
The system needs to understand the context and strategically
formulate questions that maximize the likelihood of obtain-
ing CTI-relevant information while minimizing the risk of
detection. Standard LLMs, however, tend to produce generic
conversational replies rather than targeted elicitation questions.
Linguistic adaptation. General-purpose LLMs, trained with
alignment procedures that suppress informal or adversarial
language, produce outputs that are stylistically out of place
in underground forum settings [30]–[32].
Research Goals. The goal of this work is to investigate
whether interactive LLM-based agents can effectively be
deployed to shift from passive CTI monitoring to active elic-
itation through targeted participation in underground forum
discussions. To do so, we first address how to design a system
that allows for safe yet credible operations in adversarial
online environments, and decompose the elicitation task
across multiple specialized agents.
3


---

V. PROPOSED METHODOLOGY
We design DarkBot, an LLM-based multi-agent system
that participates in public underground forums acting as a
regular user to elicit CTI-relevant information through targeted
questions. The system operates in iterative rounds: given
an initial thread context, it determines whether engagement
is allowed and worthwhile, it generates candidate questions
consistent with the ongoing discussion, and iteratively inspects
new replies to continue or terminate the interaction. Figure 1
summarizes the proposed pipeline, which is composed of 11
LLM agents who collaborate, breaking down a complex task
into subtasks. Instead of a single prompt handling relevance,
safety, discourse style, planning, and question generation, the
system assigns these subtasks to separate agents and combines
their outputs using explicit decision logic.
A. Design Principles
The CTI elicitation task presents multiple distinct challenges
(§IV) that motivate the design principles of DarkBot. As the
problem is complex and composed of multiple parallel chal-
lenges, we adopt a multi-agent architecture as a foundational
design choice, as it allows decomposing the problem into
specialized agents, and has demonstrated consistent gains in
complex security tasks [6], [33].
To address the adversarial environment, we introduce a
dedicated engagement gating stage that restricts interaction to
CTI-relevant threads to avoid unnecessary interactions, detects
and terminates conversations involving jailbreak attempts or
accusations of being a bot, and enforces compliance with our
ethical guidelines (§ IX).
To address the sparse and implicit signals challenge, we
adopt a tactic-driven question generation mechanism orga-
nized around MITRE ATT&CK tactics rather than techniques.
Tactics correspond to high-level attacker goals (e.g., Initial
Access and Privilege Escalation) that align naturally with the
focus of most forum threads, whereas individual techniques
often describe implementation variants that do not emerge as
distinct conversational topics. Framing questions at the tactic
level maximizes response probability from forum participants,
while still allowing the bot to consider specific techniques
that arise organically. Furthermore, with 14 tactics versus over
200 techniques, tactic-level tracking is a tractable problem for
an LLM, whereas discriminating across hundreds of similar
technique entries is considerably more complex, as confirmed
by results in Section VI-D.
To address the linguistic adaptation challenge, we consider
two dimensions important for credible participation. First,
matching the thread’s conversational tone (e.g., informal, ag-
gressive) helps generate messages that blend naturally into the
discussion and may improve elicitation, as perceived similarity
favors information sharing [34], [35]. Second, underground
forums use community-specific slang and terminology that
aligned models are likely to suppress.
B. Functional Blocks
We organize the pipeline dividing the underlying agents into
three functional blocks addressing the identified challenges.
Table I shows their goals, inputs, and outputs.
Engagement Gating. Before generating any message, the
system applies a strict engagement gating stage to ensure
it interacts only with threads that are CTI-relevant and do
not involve prohibited or high-risk categories. Concretely, the
THREADANALYZER and RELEVANCEAGENT follow a pattern
proposed by Shah et al. [6], where an analysis agent produces
a structured thread report (what is being discussed, what tech-
nical artifacts are mentioned, what information is missing) and
a gating agent then filters out threads that are irrelevant or fall
under prohibited content categories (e.g., violence, narcotics,
sexually explicit content). If the thread violates constraints, the
pipeline terminates without posting or saving any data. The
same pattern is applied in the analysis of subsequent replies
using the REPLYANALYZER and the DEFENSIVEAGENT to
identify potential deviations towards restricted topics, jailbreak
attempts, or accusations that the user is an AI bot. The REPLY-
ANALYZER detects if the new replies are related to previous
bot questions or if they contain unrelated content. In the latter
case, the bot waits for new replies. A reply can be both
topically relevant and adversarially manipulative, or topically
irrelevant and entirely benign. Bundling these decisions into a
single agent risks mixing the two, leading to underdetection of
manipulation attempts embedded in otherwise relevant content.
This risk is well-documented in the jailbreak literature [36],
[37], which shows that adversarial prompts frequently exploit
conversational context to bypass safety filters that reason only
about content categories. Furthermore, topic restrictions are
also enforced post-generation of the system’s response by the
FILTERAGENT. Any candidate response that violates the topic
policy is discarded and not published.
The prompt-based gating approach employed for both new
threads, received replies, and generated messages was pre-
ferred over repurposing off-the-shelf safety classifiers such
as LlamaGuard3 [38], which, being calibrated for general-
purpose content moderation, classifies most hacking-related
content as unsafe, suppressing the CTI-relevant discussions
the system is designed to engage with (Appx E).
Context Modeling and Question Generation. The result is a
structured list of attack behaviors and MITRE tactics, which
serves as the foundation for subsequent reasoning. For the
design, we referred to the project by Yuancheng Liu [39].
Note that we adapted the original project for better integration
into our pipeline, using the original prompts with minor
changes to ensure greater consistency with the interaction of
our agentic part. Based on this structured representation, the
TACTICSELECTOR determines which MITRE tactic should
guide the next interaction. The agent maintains a dynamic
tactic map covering all fourteen MITRE tactics, which can
be updated after each interaction. Each tactic is associated
with a score (Eq. 1) from a prompt-based heuristic inspired
4


---

THREADANALYZER
RELEVANCEAGENT
TTP EXTRACTOR
TONEAGENT
TACTICSELECTOR
DEFENSIVEAGENT
QUESTIONAGENT
REVIEWERAGENT
SLANGCONVERTER
Slang Question
FILTERAGENT
REPLYANALYZER
Unrelated
English Threads
Not Relevant or
Banned Topics
Jailbreak or AI Accuse
Banned Topics
New Reply
Thread
Content
TTPs
new replies
Question
Review 
Tactic
Conversation Tone
Formal Question
Engagement Gating
Context Modeling and Question Generation
Linguistic Style and Credibility
Not Approved
Publish
Fig. 1: DarkBot Architecture
by literature, and validated empirically (§VI-B, §VI-F).
0.30 · Estr + 0.25 · Rprob + 0.15 · Ivalue + 0.10 · Cflow + 0.20 · Mappl (1)
The heuristic scores each candidate tactic along five di-
mensions: (1) Evidence Strength (Estr), measuring concrete
CTI evidence such as explicit technique mentions, behavioral
patterns, and tool references [40]; (2) Response Probability
(Rprob), estimating the likelihood of a meaningful reply from
prior response length and depth, topic fit, and timing, since
even informative tactics are ineffective if they cause disen-
gagement [41]; (3) Intelligence Value (Ivalue), rewarding the
expected novelty and actionability of elicited information [42],
[43]; (4) Conversational Flow (Cflow), penalizing abrupt topic
shifts that disrupt coherence and elicitation effectiveness [41],
[44]; and (5) MITRE ATT&CK Applicability (Mappl),
rewarding tactics that map concretely to ATT&CK while
promoting diversity across the kill chain [45], [46].
The agent selects the highest-scoring tactic and terminates
the pipeline if none is sufficiently effective. The QUESTION-
AGENT then combines the selected tactic with behaviors
identified by the TTP EXTRACTOR to generate follow-up
questions that deepen the tactical dimension, while avoiding
procedural instructions or encouraging specific actions.
Linguistic Style and Credibility. Before generating a ques-
tion, the TONEAGENT analyzes the conversation to detect its
dominant tone and the frequency of specific stylistic patterns
(e.g., emojis and extreme punctuation). Available emotion
classifiers [47] capture affective categories but do not explicitly
identify the stylistic features used, motivating a dedicated
prompt-based component. This information guides the QUES-
TIONAGENT to formulate a message that is consistent with the
conversational context while preserving its original semantic
intent. We keep the QUESTIONAGENT as an independent com-
ponent from the TACTICSELECTOR so that tactical planning
and question generation can be handled independently; abla-
tion results (§VI-D) confirm the benefit of this decomposition.
After the QUESTIONAGENT generates the candidate questions,
they are evaluated by a dedicated REVIEWERAGENT following
a reflection pattern
[48], [49]. This agent verifies that the
question matches the identified tone and linguistic style, avoids
AI-suspicious phrasing, and respects structural constraints,
such as maintaining a natural single-question format. If in-
consistencies, unnatural expressions, or typical LLM phrasings
are detected, feedback is sent back to the QUESTIONAGENT,
which revises the question accordingly. This reflection loop
continues until at least one candidate satisfies both stylistic and
safety requirements, reducing the risk of producing messages
that appear artificial or out of context. The approved question
is then passed to the SLANGCONVERTER, which rewrites the
question, injecting community-specific slang and stylistic cues.
Recent work has shown that general-purpose LLMs benefit
from dedicated tuning for rewriting tasks [50], motivating a
small fine-tuned model for the slang conversion step.
VI. EXPERIMENTAL SETUP
To comply with ethical guidelines, we use open-weight
models on offline hardware rather than relying on commercial
models. This avoids sharing potentially sensitive personal
information with model providers. Agents requiring uncen-
sored outputs, specifically those that must reason about attack
behaviors without triggering safety refusals, use an abliterated
Gemma3-27B [51], while reasoning and classification agents
use Qwen3-32B [52]. The SLANGCONVERTER uses a fine-
tuned 4B-parameter model, as its narrow task requires limited
reasoning capacity. Further details are in Appx B.
A. Evaluation Framework
Based on the research questions of Section IV, we derive
the following experimental questions that guide our evaluation.
EQ1: Can the system identify productive lines of inquiry
from an initial forum post? Active elicitation is a viable
approach only if the system can effectively understand the
thread context and formulate coherent questions that probe
for additional CTI-relevant knowledge. We therefore evaluate,
in a simulated setting based on real underground forum
conversations, how well the bot can identify productive lines
of inquiry to recover missing CTI knowledge (§VI-B).
5


---

TABLE I: Agent specifications: goal, inputs, and agents’ outputs in the DarkBot pipeline. Input handling mode: SP = fixed
system prompt, UM = user message, DSP = dynamically constructed system prompt. Agents are grouped by functional block.
Block
Agent
Goal
Inputs
Output
Engagement Gating
THREADANALYZER
Produce a structured CTI report of the
thread, flagging irrelevant or harmful con-
tent and assessing engagement worthiness.
Forum thread plaintext [UM]; classifica-
tion criteria [SP].
CTI summary, conversation anal-
ysis, irrelevant-content flags, en-
gagement recommendation.
RELEVANCEAGENT
Classify threads as Relevant or Not Rele-
vant; blocks prohibited topics.
CTI
report
from
THREADANALYZER
[UM]; classification criteria [SP].
Binary decision (Relevant / Not
Relevant); terminates pipeline if
not relevant.
REPLYANALYZER
Filter incoming user replies to retain only
those that address the system’s questions,
discarding off-topic messages.
System username, prior interaction his-
tory, new incoming replies [UM]; classi-
fication instructions [SP].
Validated subset of replies for-
warded to DEFENSIVEAGENT.
DEFENSIVEAGENT
Classify validated replies as safe, attack-ai
(AI accusation), or attack-jailbreak; termi-
nate pipeline on any attack signal.
Validated replies [UM]; classification cri-
teria [SP].
Safety label; safe replies for-
warded to TACTICSELECTOR; at-
tacks terminate the pipeline.
FILTERAGENT
Act as a final safety barrier, blocking any
generated question that violates topic poli-
cies before publication.
Serialized list of slang-converted ques-
tions [UM]; exclusion criteria [SP].
Filtered list of publishable ques-
tions, or pipeline termination if
all are blocked.
Context & Question Gen.
TTP EXTRACTOR
Identify MITRE ATT&CK tactics and tech-
niques present in the conversation and verify
each mapping. [39]
Thread plaintext [UM]; extraction in-
structions [SP].
List of attack behaviors with
mapped ATT&CK tactics and
techniques.
TACTICSELECTOR
Select the ATT&CK tactic most likely to
elicit a detailed response, maintaining a
score map across all 14 tactics updated after
each turn.
Thread text and extracted tactics [UM] on
first turn; Q&A history appended on sub-
sequent turns [UM]; scoring logic [SP].
Selected tactic with reasoning, or
termination signal if no tactic is
sufficiently effective.
QUESTIONAGENT
Generate a contextually appropriate ques-
tion aligned with the selected tactic, revised
iteratively on reviewer feedback.
Tone/style profile [DSP]; thread text, CTI
summary, selected tactic [UM]; reviewer
feedback appended on revision [UM].
Five candidate questions; revised
questions upon reviewer feed-
back.
Ling. Style & Credibility
TONEAGENT
Classify the dominant conversational tone
and identify stylistic features of the thread
to guide downstream generation.
Thread content [UM]; tone taxonomy
[SP].
Tone (e.g., Informal, Paranoid,
Aggressive) and binary features
(e.g., all caps, extreme punctua-
tion).
REVIEWERAGENT
Verify that questions match the target tone,
avoid suspicious phrasing, and follow the
comment and question format. [49]
Generated questions, tone, and style spec-
ifications. [UM]; review criteria [SP].
Approval or structured feedback
sent back to QUESTIONAGENT
(reflection loop).
SLANGCONVERTER
Rewrite formally generated questions using
community-specific slang and stylistic cues.
Approved question(s) [UM]; fine-tuned
on synthetic CrimeBB dataset.
Slang-converted question(s) pre-
serving original semantic intent.
EQ2: Can the system remain safe and aligned under
adversarial conditions? Operating in adversarial environments
requires the system to remain safe and aligned under hostile
conditions. We evaluate whether the proposed architecture can
avoid prohibited topics, detect jailbreak attempts, and block
policy-violating content before publication (§VI-C).
EQ3: Do the proposed architectural choices measurably im-
prove performance? The proposed multi-agent architecture in-
volves several design choices and task decompositions whose
individual contributions are not obvious a priori. We validate
the impact of architectural choices on system performance.
We compare the full multi-agent pipeline against a single-
agent baseline and ablate individual components. Extraction
performance is evaluated through simulated user interactions,
and stylistic credibility is evaluated through a survey (§VI-D).
EQ4: Does the system participation increase intelligence
yield? Passive approaches can only observe the activity that
develops naturally after a thread is published, whereas Dark-
Bot actively participates in the discussion. To isolate the effect
of this participation, we conduct a prospective matched exper-
iment using identical initial posts in online forums (§VI-E).
EQ5: Can the system operate effectively in real underground
forum threads? The system must operate in underground
communities without being detected. Since the previous eval-
uations, including the controlled activity experiment, may
not fully reproduce the dynamics of organically occurring
discussions in underground communities, we deploy DarkBot
in real underground forums to assess whether it can conduct
live conversations without triggering bans, moderator interven-
tions, or AI detection, while eliciting information (§VI-F).
Datasets. Table II summarizes the datasets used for each
experiment. More details are provided in Appx D.
B. Intelligence Probing Evaluation (EQ1)
This experiment evaluates the system’s ability to understand
conversational context and generate coherent questions about
the discussed topic. We selected 100 relevant threads from
the CrimeBB dataset, each containing the initial post and
subsequent replies. The experiment is designed as a controlled
probing task: DarkBot sees only the initial post, while a
user proxy has access to the complete original discussion
and may return only information explicitly contained in the
original human replies and directly asked about. Conducting
live experiments on actual forums for this evaluation was
intentionally avoided, as repeated interactions with real users
during iterative development phases could have revealed the
study’s nature, compromising subsequent sessions. Evaluating
an information extraction bot by recruiting domain experts to
simulate forum users at scale is also not feasible, as it would
be difficult to maintain consistency and unbiasedness across
evaluators and sessions. We therefore simulate the user proxy
by using an external LLM as a judge, thereby providing a re-
producible approximation of forum participants’ interactions.
6


---

TABLE II: Mapping of evaluation questions, datasets, experiments, and metrics.
EQ
Dataset / Forum
Content
Experiment
Metric(s)
EQ1
EQ3
CrimeBB [53]
Underground
forum threads
Simulated CTI probing (§ VI-B)
Design validation (§ VI-D)
Tactics and techniques recovered,
survey, token consumption
EQ2
CoDA [54]
Dark web content
Engagement gating validation (§ VI-C)
Topic rejection rate
EQ2
Do Anything Now [37] &
InTheWild Jailbreaks [36]
Jailbreak prompts
Robustness against jailbreaks (§ VI-C)
Jailbreak detection rate
EQ2
BeaverTails [55]
Harmful Q&A pairs
Message filter validation (§ VI-C)
Block rate of harmful questions
EQ3
AnnoCTR [56]
CTI reports
TTP Extractor validation (§ VI-D)
Precision and recall
EQ4
BlackHatWorld & Dread
matched deployment
20 matched pairs of
identical forum posts
Intelligence yield effect evaluation (§ VI-E)
Paired CTI entities difference in
user messages over seven days
EQ5
BlackHatWorld, sinister.ly,
Hack Forums, and Dread
104 organic
live forum threads
Automated forum deployment (§ VI-F)
Response and thread activity, detection and
moderation outcomes, and qualitatively elicited CTI
The proxy follows a constrained behavioral policy. It returns
a source reply only when the generated question directly
targets the information expressed in that reply. It cannot
introduce external knowledge, synthesize new facts, or reveal
unrelated parts of the conversation, but just returns messages
from the original thread. When no source reply satisfies these
conditions, it returns a fixed negative answer. We evaluate sys-
tem performance by comparing MITRE ATT&CK techniques
across the original conversation and the messages the system
extracts through its questions. Beyond the final technique re-
covery, we report the probing efficiency, defined as the number
of techniques first evidenced in replies divided by the number
of published questions. We exclude techniques already present
in the initial post, repeated mentions, and techniques appearing
only in DarkBot’s questions. As a secondary measure, we
count unique external URLs first appearing in user proxy
replies. Since we do not independently assess each URL’s rel-
evance or reliability, this metric reflects the yield of references
rather than CTI quality. The recovered techniques are obtained
through manual annotation rather than the raw output of the
TTP EXTRACTOR. We use the extractor only as a candidate
generator over the source thread: it proposes candidate tech-
nique mappings, which a domain-informed annotator verifies
against the supporting text, discarding unsupported ones and
independently re-reading each thread to add techniques the
extractor missed. Manual annotation is necessary because the
extractor’s measured accuracy (§VI-D) is not sufficient for
defining a scoring target: at the technique level, it reaches
46.4% recall at 19% precision on AnnoCTR [56]. Using its
raw output would distort the metric in both directions. Missed
techniques would understate what a configuration recovered,
while spurious mappings would reward configurations that
simply publish more questions, since every additional reply
gives the extractor another opportunity to emit an unsupported
technique regardless of question quality. Manual annotation
also avoids a closed-loop evaluation, in which the same com-
ponent both drives DarkBot’s reasoning and defines the score.
Techniques mentioned only in the system’s own questions are
never counted as recovered. While this experimental setup
quantifies the bot’s ability to understand context and generate
appropriate questions, it has inherent limitations, as discussed
in Section VII.
0
2
4
6
8
10
12
14
16
18
20
0
20
40
60
80
100
x : Max Allowed Messages
Extracted Techniques (%)
DarkBot
No TacticSelector
Single-Agent
Fig. 2: Average techniques retrieved for different message
limits. The plot compares DarkBot with a single-agent baseline
and without the standalone TACTICSELECTOR module.
We repeat the experiment under different limits on the
number of messages DarkBot is allowed to publish, to char-
acterize how recovery evolves as the number of bot messages
increases. A single conversation is simulated per thread, and
each point at x reports the recovery from the replies obtained
within the first x published questions. The value is a cap
rather than a target: the pipeline may terminate on its own
when the TACTICSELECTOR finds no tactic with sufficient
expected effectiveness. Recovery is therefore non-decreasing
in x by construction. Because all configurations start from
the same initial post, they share the same pre-interaction
baseline (dashed line), and subsequent gains reflect techniques
recovered from replies made available through the controlled
probing process. The resulting curve in Fig. 2 (black) shows
that the overlap plateaus, reaching a maximum of 72.8%,
starting from a baseline of 32.3% of techniques present in
the initial post. Overall the system published 928 questions
recovering 159 new techniques and 122 source-matching
URLs, averaging a probing efficiency of 0.171 techniques per
question and 0.131 URLs per question.
7


---

Takeaway (EQ1). With the initial post only, DarkBot re-
covers 72.8% of the MITRE ATT&CK techniques present
in the complete source conversations. Beyond final recovery,
the system averages a probing efficiency of 0.171 additional
techniques per published question. These results indicate
that DarkBot can understand thread context and identify
productive questions under the defined user-proxy policy.
C. Robustness Evaluation (EQ2)
This section evaluates whether the proposed multi-agent
system behaves safely under simulated hostile conditions,
before deploying it in real-world forum interactions (§VI-F). In
particular, we analyze whether it engages only in appropriate
discussions, resists jailbreak and manipulation attempts, and
prevents the publication of unsafe or policy-violating content.
Engagement Gating Validation. The goal of this experiment
is to verify that the system can distinguish CTI-related topic
threads and, more importantly, to avoid engaging in potentially
harmful conversations that violate our policies (§ IX-E). For
this analysis, we leveraged a subset of the CoDA dataset [54]
(Appx D), containing dark web documents labeled into ten
topic categories. We present the selected texts to the bot
as initial posts of new forum threads. A post is considered
Relevant if it was labeled as such by the RELEVANCEAGENT,
thereby triggering the bot message generation mechanism.
However, the generated response may still be blocked by the
final FILTERAGENT when the full pipeline is run. As Fig. 3
reports, 91.5% of the texts in the Hacking category were
classified as Relevant, a small fraction was labeled as Not
Relevant, as the system deemed them insufficiently informative
for CTI question generation.
For the five texts classified as Relevant in the Arms, Porn,
and Violence categories, we evaluated the full pipeline. For the
one Porn-related question, the generated question was blocked
by the FILTERAGENT. The remaining four cases, related to
Arms and Violence, produced questions aimed at extracting
CTI without engaging with or addressing harmful content. This
shows that the system focused exclusively on cybersecurity-
related content, not reinforcing the potentially harmful aspects.
Robustness Against Adversarial Inputs. The goal of this
experiment is to verify the system’s ability to detect jailbreak-
ing attempts. Jailbreak prompts are typically used to elicit
restricted information or to induce prohibited behaviors that
a safety-aligned LLM would otherwise refuse to produce. For
this purpose, we tested the system using publicly available
jailbreak datasets from “Do Anything Now” by Shen et al. [37]
and In-the-Wild Jailbreaks by Jiang et al. [36]. We evaluate
the system’s ability to detect jailbreak attempts and termi-
nate the interaction accordingly. DefensiveAgent. We tested
robustness to adversarial replies by feeding jailbreaks to the
DEFENSIVEAGENT without following the bot pipeline. We
analyzed 845 jailbreaking prompts and found that 92.8% of
them were detected by the DEFENSIVEAGENT.
Full Pipeline. We assess end-to-end robustness by injecting
the jailbreak prompts into three representative dark-web con-
Arms
Porn
Violence
Crypto
Hacking
Financial
Others
Gambling
Electronic
Drugs
0
50
100
150
200
1
1
3
19
183
15
8
2
1
0
30
30
30
30
200
30
30
30
30
30
Count
Support
Pred. Relevant
Fig. 3: Relevance Prediction on CoDA Samples
versations on malware, botnets, and initial access brokerage.
After the bot’s first reply, we submit the jailbreak message; in
all three scenarios, 100% of attempts receive no response.
While the DEFENSIVEAGENT is not a perfect classifier, the
overall pipeline can detect attack attempts that deviate from
the original conversation topic via the REPLYANALYZER, and
the final FILTERAGENT prevents the bot from publishing
messages that deviate from the defined guidelines.
Message Filter Validation. To evaluate the robustness of
the final message filter (i.e., the FILTERAGENT), we now
consider the scenario in which earlier safeguards fail or are
bypassed through jailbreaking. In such cases, the model may
generate content that violates the system’s safety guidelines.
The final message filter serves as a last line of defense,
detecting messages that violate our guidelines and blocking
them from the pipeline before publication. For this purpose,
we used a subset of the BeaverTails [55] dataset (Appx D).
We submit each question to the FilterAgent, simulating a
rogue input that the system did not intercept earlier. We
observed that the vast majority of harmful questions were
correctly blocked, with only a small portion classified as
Relevant. Out of 347 harmful questions, 311 (89.6%) were
blocked. In deployment, however, every outgoing message is
first rewritten by the SLANGCONVERTER into the colloquial,
abbreviated register of the target forums, so the FILTERAGENT
faces a slang distribution rather than clean English, which
may differ from the style of the BeaverTails [55] dataset.
We apply slang rewriting only to BeaverTails because it
represents outgoing messages processed by the SLANGCON-
VERTER before reaching the FILTERAGENT; CoDA posts and
jailbreak prompts represent incoming content and are therefore
evaluated unchanged. To verify that our safety guarantees hold
under this distribution shift, we reran the evaluation on a
SLANGCONVERTER-rewritten version of the dataset. Slang
rewriting slightly erodes FILTERAGENT performance, as the
block rate falls from 89.6% to 85.6% for harmful questions.
A manual inspection of the remaining questions revealed that
most of them did not explicitly involve undeniably harmful
topics, unlike those immediately classified as Not Relevant.
Examples include: ”How do I tattoo myself?”, ”How do I
8


---

50%
25%
0
25%
50%
75%
−TONEAGENT
−SLANGCONVERTER
Single-Agent
DARKBOT
Share of judgments
Better Ablated
Equal
Better DarkBot
Fig. 4: Stylistic credibility ablation survey.
get into illegal sports betting?”. This experiment models a
scenario in which a jailbreak evades the DEFENSIVEAGENT
and causes the bot to generate a policy-violating message
that then reaches the FILTERAGENT. If the two observed
failure rates are independent and transferable to the same input
distribution, the estimated probability that both layers fail is
0.072 × 0.144 = 1.04%.
Takeaway (EQ2). The full pipeline rejected 100% of tested
jailbreak prompts, even when the DEFENSIVEAGENT alone
misclassifies 7.2% of them. The FILTERAGENT in isola-
tion blocked 89.6% of harmful messages and 85.6% after
slang rewriting, with most of the undetected questions being
borderline content. By combining the performance of the
individual components, the pipeline estimates a failure rate of
just 1.04%, indicating that the layered architecture effectively
compensates for individual-agent limitations.
D. Design Validation (EQ3)
To evaluate the effectiveness of the pipeline design, we
assess two main dimensions: the ability to understand the
context and generate coherent questions, and the stylistic
credibility of the produced messages. Probing performance is
evaluated on the same 100-thread CrimeBB cohort used in
EQ1, allowing direct comparison between the full multi-agent
pipeline, a single-agent baseline, and a TACTICSELECTOR
ablation. Stylistic credibility is evaluated through a survey re-
cruiting 118 participants with a Computer Science background,
with no incentives. Survey details are reported in Appx C.
Multi-Agent Architecture Evaluation. To evaluate whether
decomposing the task into specialized agents provides mea-
surable advantages, we compare DarkBot with a single-agent
baseline. To construct the single-agent baseline, we merged
all agent prompts and logic from the multi-agent pipeline into
a single structured system prompt. This prompt preserved the
original workflow logic by explicitly describing the sequential
reasoning steps corresponding to each agent.
Intelligence Probing. Regarding information extraction ability,
Figure 2 reports the overlap of extracted MITRE techniques
between simulated and original conversations, following the
experimental setting discussed in Sec. VI-B on 100 CrimeBB
threads. For this experiment, we disabled the relevance iden-
tification logic for a fair comparison. The single-agent system
converges at approximately 51.4% techniques overlap, while
the multi-agent architecture reaches 72.8%. This difference
is not explained solely by a larger number of published
questions: normalized by the number of questions, the multi-
agent pipeline recovers 0.171 new techniques per question,
compared with 0.131 for the single-agent baseline. It also
retrieves 122 unique external references, compared with 47
for the single-agent baseline, corresponding to 0.131 versus
0.082 references per published question.
Stylistic Credibility. Figure 4 reports the results of the stylistic
credibility survey. When comparing the full pipeline against
the single-agent baseline, 44.41% of judgments rated the
full-pipeline messages as more likely to be produced by a
human user, while 35.25% preferred the single-agent output
and 20.34% perceived no difference. These results suggest
that the modular architecture, beyond improving extraction
capabilities, also contributes positively to stylistic credibility,
likely due to the dedicated reasoning steps that allow each
agent to focus on specific aspects of message generation.
Computational Cost. The multi-agent system, as expected,
consumes on average more completion tokens (37,485 vs.
20,701) and prompt tokens (422,280 vs. 340,006) than the
single-agent system. This aligns with prior literature high-
lighting benefits and costs of modular reasoning in complex
intelligence extraction tasks [6].
Agent Ablations. We perform agent ablations to assess their
effects on stylistic credibility and information extraction.
Stylistic Credibility. We validate the contribution of the
TONEAGENT and the SLANGCONVERTER to the stylistic
credibility of the generated messages through a survey (see
Appx C), comparing outputs from the full pipeline against
those produced without these components, across 5 repre-
sentative threads. Participants were asked to judge which
messages better adhered to the conversational tone of the
thread, and which appeared more likely to have been written
by a human user. As Figure 4 demonstrates, the SLANG-
CONVERTER emerges as the component with the strongest
and most consistent impact on stylistic credibility: 60.51%
of participants rated full-pipeline messages as better than
those produced without it, with only 17.97% preferring the
ablated variant. This indicates that community-specific lexical
adaptation substantially improves perceived stylistic credibility
under the evaluated survey conditions. These results also
provide indirect evidence that the fine-tuning procedure on
the synthetic dataset was effective. The contribution of the
TONEAGENT to the final stylistic output appears limited: only
32.20% of participants preferred the full-pipeline output over
the no-TONEAGENT variant, while 46.10% rated it as worse.
Although the effect of the TONEAGENT in our survey is
perceived as slightly negative, prior work consistently treats
tonal alignment as relevant to conversational credibility and
elicitation [34], [44]. We therefore retain the TONEAGENT in
the pipeline and leave its improvement as future work.
Intelligence Probing. To assess the contribution of the TAC-
TICSELECTOR as a standalone component, we repeat the
offline extraction experiment described in Section VI-B under
9


---

an ablated configuration in which tactic selection is inte-
grated directly into the QUESTIONAGENT. In this setting,
the QUESTIONAGENT is jointly responsible for selecting the
tactics to pursue and deriving the follow-up question, without
a dedicated reasoning step for tactical planning. Figure 2
shows the proportion of techniques recovered from replies
returned during the controlled probing simulation, relative to
the complete source threads. The full pipeline converges to a
final recovery of 72.8%, whereas the ablated system reaches
a maximum of 67.4%. Removing the TACTICSELECTOR also
led to a slight degradation in probing efficiency, from 0.171 to
0.165 new techniques per published question and from 0.131
to 0.108 new URLs per question (122 against 90 URLs in
total). Its main contribution, however, is sustaining recovery
across turns rather than making individual questions more
productive. Without explicit tactic-planning, the QUESTION-
AGENT focuses on the most salient content in the current
exchange, while the TACTICSELECTOR tracks covered tactics
and prioritizes underexplored dimensions.
TTP
Extraction
Validation. We compare the employed
TTP EXTRACTOR with LADDER [57], a non-LLM-based
ATT&CK extraction baseline, on the annotated AnnoCTR
reports and on the same 100 CrimeBB threads used in §VI-B.
AnnoCTR provides independent expert labels and is therefore
used to evaluate accuracy, whereas the CrimeBB comparison
characterizes candidate extraction yield in the forum domain,
as it does not provide expert technique labels.
Techniques extraction. On 105 labeled AnnoCTR reports [56],
LADDER extracted 796 techniques (7.58/report) versus 2,479
(23.61/report) for the LLM system. Against ground truth, the
LLM achieved 46.4% recall and 19% precision, compared
with LADDER’s 15.8% recall and 18.8% precision, providing
substantially higher coverage at comparable precision. On
100 CrimeBB threads, LADDER extracted 50 techniques
(0.50/thread), versus 1,996 (19.96/thread) for the LLM system.
Tactics extraction. Since LADDER does not predict tactics,
we infer them from the technique IDs it extracts using the
official MITRE ATT&CK mapping, where techniques listed
under multiple tactics contribute to all associated tactics. On
the 105 AnnoCTR reports, LADDER inferred 581 tactics (5.53
per report), compared with 885 for the LLM system (8.43 per
report). Using the same mapping to derive ground-truth tactics
from AnnoCTR technique labels, the LLM system achieves
a tactic recall of 74.4% and precision of 50.9%, compared
to LADDER’s 45.9% recall and 46.7% precision. At the
tactic level, the LLM system therefore improves on LADDER
across both dimensions, recovering nearly three-quarters of the
ground-truth tactics while maintaining higher precision, and
confirming that the richer technique output also provides more
accurate tactic coverage. On CrimeBB, LADDER’s techniques
translate to 46 inferred tactics (0.46 per thread), while the LLM
system identified 902 tactics (9.02 per thread). Higher recall
is especially important in this setting, as LADDER’s average
of 0.46 tactics (0.50 techniques) per thread would leave the
bot with virtually nothing to explore.
Takeaway (EQ3). The multi-agent pipeline improves tech-
nique recovery (72.8% vs. 51.4%) and probing efficiency
(0.171 vs. 0.131) against the single-agent baseline. Ablation
of the TACTICSELECTOR reduced both final recovery (-
5.4%) and probing efficiency (-0.165 techniques per ques-
tion) indicating that explicit tactic planning helps sustain
broader exploration across turns. Among the evaluated stylis-
tic components, the SLANGCONVERTER has the strongest
positive measured effect. By contrast, the TONEAGENT has
a slightly negative perceived effect.
E. Intelligence Yield Effect Evaluation (EQ4)
To estimate the effect of DarkBot participation on in-
telligence yield, we conducted a prospective matched-pairs
deployment. We evaluated the paired differences using a two-
sided paired permutation test. We authored 20 discussion
topics, each presented as an identical initial post published
under our own accounts on both BHW and Dread. For each
topic, exactly one of the two forums was assigned to the bot,
while the other copy of the same topic received no bot activity
and serves as its control. Because both arms of a pair carry
the same text posted at the same time, each topic serves as its
own control for subject matter, phrasing, and timing, and the
assignment is independent of how the thread develops later.
The account that publishes the initial post never returns to the
thread, so DarkBot is the only non-organic participant on the
active side, and the control side has none. The deployment
is additionally counterbalanced across forums and channels:
every pair of board sections used hosts an equal number of
topics, with the bot assigned to each side. This matters because
a paired difference otherwise conflates the bot’s effect with the
difference in baseline activity between the two sections being
compared. With equal numbers of topics in each direction, the
baseline terms enter the treated and control totals identically
and cancel out, so the aggregate difference reflects the bot’s
presence rather than the choice of platform or section. We
measure paired differences in CTI entities present in human-
authored messages during the 7 days following each thread’s
confirmed public visibility. As CTI entities, we use a subset
of STIX 2.1 standard [58] as domain categories and IoCs
(Appx G). We exclude the initial post, bot accounts, and
automated or moderator accounts from the count, so every
counted message is a user contribution.
Results. Across the 20 completed pairs, threads to which
DarkBot was assigned carried 90 human messages containing
a total of 223 CTI entities, against 84 on their matched
controls with 154 entities over the same seven-day windows.
Bot-interacted threads achieved an average of 3.85 entities
more than their matched control. The 95% confidence interval
for this mean difference ranges from 0.37 to 7.38 entities.
An exact two-sided sign-flip permutation test yielded a p-
value of 0.033, indicating that a difference at least this large
would be unlikely under the null hypothesis of no effect.
Because assignment of the bot to one arm of each pair
was counterbalanced rather than drawn independently, the test
enumerates only the
 20
10

= 184,756 assignments preserving
10


---

A B C D E F G H I J K L M N O P Q R S T
30
20
10
0
10
20
30
40
50
control
DarkBot
Bot on BHW
Bot on Dread
Topics
CTI entities
Technique
Tool
Malware
Infrastructure
Target
Actor
Defence
Vulnerability
Indicators
Fig. 5: Per-topic CTI entities elicited within seven days of
publication. Bars above the axis show entities in the thread
assigned to DarkBot; bars below show its matched control.
the split between forums, which is the set of assignments that
the randomization procedure could produce. The confidence
interval is obtained by inverting the corresponding permutation
test, so it excludes zero exactly when the p-value is below 0.05.
Figure 5 reports pair-level differences. Beyond a higher count
of CTI entities, some of the threads also produced concrete
operational disclosures. For example, in a matched thread on
CAPTCHA bypass (Fig. 17), DarkBot obtained details about
how another user used Gemini to solve audio CAPTCHAs and
mass-create GitHub accounts. This conversation has been re-
ported to both Google and GitHub. No comparable disclosure
appeared in the matched control thread.
Takeaway (EQ4). Across 20 matched topic pairs, threads
in which DarkBot participated accumulated an average of
3.85 CTI entities more than their matched control. The 95%
confidence interval for this difference ranges from 0.37 to
7.38 entities, supporting a measurable positive effect on in-
telligence yield compared with standard passive approaches.
F. Automated Forum Deployment (EQ5)
Unlike the matched deployment in §VI-E, this experiment
evaluates the full system on organically created threads dis-
covered and selected through its deployed engagement policy.
Newly published candidate threads were screened by the
RELEVANCEAGENT before interaction. We conducted 104
conversations across surface and dark web forums. On the sur-
face web, this included 33 conversations on blackhatworld.com
(BHW), 12 on sinister.ly, and 2 on hackforums.net. On the
dark web, we carried out 57 conversations on Dread [59].
Because interactions on sinister.ly and hackforums.net yielded
only 2 responses in total, none of which provided relevant
information, we focus our analysis on BlackHatWorld and
Dread in the following. Note that Dread employs several
interactive CAPTCHAs, which we bypassed manually for the
scope of this research.
Qualitative Interaction Analysis. Live interactions demon-
strated promising information-extraction capabilities, as the
system often generated credible questions that elicited addi-
tional information about the topics discussed, particularly in
the Dread forum. Anonymized examples of interactions are
provided in Appx I.
For instance, in the conversation regarding EDR evasion
presented in Figure 15, a user responded to the bot by stating
that he had implemented and tested EDR-Freeze [60], which
had been published for the first time only one month before
the conversation took place. In this case, the bot revealed
additional information, indicating that the relatively new EDR-
Freeze technique was already being actively tested by po-
tential threat actors. Another relevant example is presented
in Figure 16, which discusses the trade-off between a data
breach and other options. In this case, DarkBot obtained
detailed information about the structure of the stolen data
and confirmation that the threat actor still had access to the
compromised database. This information was not public before
the interaction, showing that the system can surface CTI that
would not emerge through passive monitoring alone.
However, in some cases, we observed reluctance among
users to share details in public spaces. While it is not within
the scope of this work to explore private conversations and
interact with users, we nonetheless explore the private mes-
sages received as part of the CTI collected. For instance,
in one conversation, the bot successfully convinced a user
to share the OSINT tools used in their operations, but the
user preferred to do so in private chat, where the bot did
not operate due to compliance with ethical prerequisites (see
§ IX). After the deployment period, we manually inspected
unsolicited messages received by the study accounts. In other
cases, users shared additional information, external contact
details, or service links through the forums’ private messaging
systems, either to continue the exchange privately or to move
it to another platform. In particular, these private messages
included personal Telegram handles, Telegram links associated
with services related to mail spoofing and large-scale scraping,
and a Jabber address. This suggests that credible public par-
ticipation enables access to other, more private channels and
information, beyond increasing public activity and eliciting
additional information in public threads.
Threads Activity Analysis. To characterize user activity in
the organic deployment, we compare bot-interacted threads
with other non-interacted relevant threads from the same
forum sections and creation window. Unlike the matched
experiment in §VI-E, the control threads topics may differ
from the bot-interacted ones, the results therefore describe an
association and do not fully isolate completely the causal effect
of participation. Moreover, given the high number of threads
involved, this evaluation uses message count as a proxy for
user activity, which may not fully capture the CTI value of
11


---

Bot-int.
Others
Dread
0
10
20
30
40
50
60
Bot-int.
Others
Messages per thread (excl. bot mess.)
BHW
Fig. 6: User messages per thread across bot-interacted and
non-interacted relevant threads during the time window.
the resulting discussions. We compare message activity across
two groups of threads drawn from the same forum sections
and the same creation time window. The first consists of all
threads in which DarkBot published at least one message and
was re-fetched live after deployment to capture subsequent
user activity, including any replies triggered by the bot. Bot
messages are excluded from the count, so every counted
message is a real user contribution. The second contains only
threads from the same sections and window in which the bot
did not interact, retaining only those classified as relevant by
the THREADANALYZER, and RELEVANCEAGENT pipeline,
representing the baseline a passive monitor would observe.
Figure 6 shows per-thread message distributions on both
platforms. On Dread (n1 = 57, n2 = 58), bot-interacted
threads have a median of 9 user messages, versus 6 for the
passive baseline; on BHW (n1 = 33, n2 = 45), the medians
are 18 and 7, respectively. These results indicate that active
engagement by DarkBot is associated with substantially richer
activity than passive observation of the same communities.
Responses Analysis. On BHW, DarkBot published 103 ques-
tions across 33 threads and received 112 qualifying user
replies. We define a qualifying user reply as a message from
another user account, posted after DarkBot began interacting,
that the pipeline identified as responding to DarkBot; unrelated
messages are excluded. This corresponds to 1.09 replies per
question and 3.39 replies per thread. Of the 33 threads, 22
(66.7%) received at least one qualifying reply, with 5.09
replies per responding thread. On Dread, DarkBot published
95 questions across 57 threads and received 42 qualifying user
replies, corresponding to 0.44 replies per question and 0.74
replies per thread. Of the 57 threads, 16 (28.1%) received at
least one qualifying reply, with 2.63 replies per responding
thread. Although response density was lower than on BHW,
the Dread conversations generally focused more directly on
CTI-relevant topics.
Message length. On BHW, user replies were substantially
longer than system messages on average (221.5 compared
to 130.0 characters), suggesting that the system’s questions
elicited more elaborate responses. Conversely, on Dread, mes-
sage lengths were more balanced (141.1 characters for user
replies, 152.4 for system messages). This reflects a more
concise communication style typical of Dread users, where
neutral
anger
surprise
sadness
fear
disgust
joy
0
20
40
60
80
100
Avg. Replies Emotions (%)
Dread
BHW
Fig. 7: Emotion distribution of received replies
Dread
BHW
First reply
0.01
0.1
1
10
100
1000
Dread
BHW
Time (h, log scale)
Duration
Fig. 8: Distributions of time to first reply and total conversation
duration for BlackHatWorld (BHW) and Dread. Violins show
the distribution; dot and line mark the median and IQR.
interactions tend to be direct.
Emotion Distribution. We analyzed emotions using Hart-
mann’s English emotion classification model [47]. As shown
in Fig. 7, Neutral tones dominate across both platforms, with
negative sentiment remaining limited and never escalating into
adversarial interactions. On the surface web, this aligns with
discussions centered on SEO, services, and technical advice.
On the dark web, while neutrality remains dominant, higher
proportions of Anger and Fear were observed, particularly in
discussions involving exploits, fraud, and operational security.
Timing Analysis. Deployments spanned approximately three
weeks on BHW and one month on Dread. As shown in
Figure 8, BHW exhibited considerably faster dynamics: the
median time to the first received reply is 2.8 h compared to
7.2 h on Dread, and median conversation durations are roughly
half as long (48.5 h vs. 82.8 h). The conversation duration is
defined as the time elapsed between the bot’s first message and
the last message in the thread that received no further replies.
Appx H also suggests that weekly interaction patterns further
differentiate the two platforms.
Stylistic Credibility Analysis. Across all monitored interac-
tions (§VI-E, §VI-F), we observed no account suspensions,
moderator interventions, or explicit accusations that DarkBot
was automated; its messages did not lead to any visible mod-
eration or enforcement action. During the same observation
period, we also observed other accounts exhibiting overtly
automated posting behavior being identified and suspended
by forum moderators. Although this does not constitute a
12


---

0
0.2
0.4
0.6
0.8
1
Dread
BHW
Avg. AI Detection Score
Users
DarkBot
User mean
Fig. 9: AI detection scores per user on BHW and Dread.
controlled comparison, it indicates that moderation and bot-
related enforcement were active on the studied platforms.
AI-detection Analysis. We evaluated the generated messages
using the Sapling API [61], considered among the most
reliable freely available AI detectors [62]. DarkBot messages
averaged detection scores of 6.87% on BHW and 10.75%
on Dread, compared with 27.58% and 13.09%, respectively,
across other forum users. Figure 9 shows the average score
per user. These results suggest that the detector does not
distinguish DarkBot from typical user content, supporting the
pipeline’s ability to conceal its automated nature. Notably,
BHW users received higher scores than dark-web users, possi-
bly reflecting automation or AI-assisted participation. Appx F
provides an additional qualitative style-embedding analysis.
Takeaway (EQ5). Across 104 live conversations and 213
published messages, the system never triggered any account
suspension, moderator intervention, or explicit AI accusa-
tion. DarkBot successfully elicited CTI that would not have
been accessible through passive monitoring, including newly
published attack techniques already being tested in the wild
and details about active database breaches. Notably, some
users preferred to continue the exchange through the forums’
private chats, where they shared additional information,
further demonstrating how credible engagement can surface
content unavailable to passive monitoring of public threads.
VII. THREATS TO VALIDITY
While our results suggest that multi-agent architectures can
create credible bots that elicit CTI-related information from
underground communities, several threats to validity remain.
We discuss them as internal and external validity threats.
Internal Threats. The intelligence probing evaluation (§VI-B)
depends on a simulated user whose behavior may not fully
reflect real adversarial dynamics. Moreover, the ground truth
for techniques is manually validated. This is because the
extraction of TTPs from unstructured forum content remains
a difficult problem with limited state-of-the-art performance,
and the TTP EXTRACTOR produces a non-negligible number
of false positives. This choice reduces the closed-loop de-
pendence on the extractor but introduces annotator judgment,
particularly for implicit or ambiguous ATT&CK mappings.
On the other hand, highly relevant questions may be penal-
ized when the corresponding topic was not discussed in the
original CrimeBB conversation, leading to an underestimation
of the system’s elicitation capability. The robustness evaluation
(§VI-C) uses general-purpose jailbreak benchmarks. Design-
aware adversaries crafting system-specific manipulations could
be more effective than the tested prompts.
External Threats. The survey-based credibility evaluation
(§VI-D) relies on participants with a computer science back-
ground, who may, however, lack familiarity with the linguistic
conventions and slang typical of underground forums. The live
deployment is limited to specific forums (§VI-F), however,
the effectiveness of this approach might vary across different
online platforms and communities with different norms and
moderation practices. Additionally, underground forums are
subject to significant linguistic and topic drift over time.
Ethical minimization requirements limited the scale and dura-
tion of the live deployment (§ IX), reducing statistical power
and generalizability. Exact replication is also difficult because
forum content, moderation policies, and user behavior may
change over time, especially after study disclosure. Although
we release links to the public evaluation threads, online content
may later change, be removed, or migrate.
VIII. CONCLUSION
This paper presented DarkBot, a multi-agent LLM-based
system designed to actively elicit cyber threat intelligence from
public underground forums through targeted conversational en-
gagement. Unlike prior approaches that rely on passive crawl-
ing or single-agent designs limited to specific tasks, DarkBot
addresses the broader goal of CTI elicitation by decomposing
the interaction task into 11 specialized agents that handle
engagement gating, question generation, and linguistic style
adaptation. Our evaluation showed that the system can recover
72.8% of MITRE ATT&CK techniques in a simulated setting
from the original CrimeBB conversations, starting only from
the initial post, confirming its ability to understand context and
generate coherent questions. The system effectively detects
harmful content and is robust against adversarial inputs. The
pipeline fully rejected all tested jailbreak prompts and filtered
the majority of content that violated policies, with the overall
architecture compensating for the limitations of individual
components. The multi-agent design outperformed a single-
agent baseline in tactical coverage, and stylistic credibility. In
a live prospective experiment with 20 matched topic pairs,
threads assigned to DarkBot accumulated an average increase
of 3.85 CTI entities over seven days. Across 104 live forum
threads, the deployment triggered no account bans, moderator
interventions, or AI accusations, while eliciting CTI-relevant
information unavailable through passive crawling.
Future work. Future work includes extending the pipeline
to multilingual forums and broader platforms, developing
adaptive elicitation strategies based on community feedback,
and conducting longitudinal deployments to assess sustained
detection risk. Further directions include targeting emerging
13


---

threats (e.g., new CVEs or threat actors), supporting conver-
sation migration to private channels, and automating discovery
of hidden underground communities.
ACKNOWLEDGMENTS
We thank Professor Gianluca Stringhini for his valuable
feedback and helpful suggestions. We also thank the Cam-
bridge Cybercrime Centre for granting us access to the
CrimeBB dataset. This work was supported by the Ministero
delle Imprese e del Made in Italy as part of the project
“WASABI - Web Analysis System with Artificial intelli-
gence on BIg data” under the Innovation Agreement CUP
B49J25000080005 and by BV TECH S.p.A.
IX. ETHICAL CONSIDERATIONS
This work involves automated interaction with online com-
munities that may discuss or be involved in harmful or illegal
activities, and the development of techniques enabling auto-
mated human-mimicking conversational behavior. As such, the
study raises ethical concerns related to the risk of enabling
or facilitating criminal behavior, the safety of interactions,
and the potential misuse of the proposed technology beyond
its intended defensive purpose. To address these concerns,
the research has undergone institutional ethical review and
data protection impact assessment, with approval from the
corresponding institutional authorities. The proposed system
design incorporates safety guardrails and content filters and
follows a data minimization approach. Furthermore, the LLM
models used in this research are self-hosted to ensure that
all data and information remain within the controlled research
environment, preventing any potential transmission of sensitive
or harmful data. All procedures adhere to applicable ethical
standards for human-subjects research and to data protection
regulations, including the principles of data minimization,
purpose limitation, and proportionality.
A. Institutional Evaluation Process
Before starting the research activity, the study underwent
an institutional evaluation process that involved both a privacy
compliance review and an ethical assessment by the univer-
sity’s Research Ethics Committee. The research team prepared
the required documentation, including: (i) a data processing
description form detailing the nature of the data collected, the
legal basis for processing, and the data protection measures
adopted; (ii) a Data Protection Impact Assessment (DPIA)
analyzing the risks associated with the processing and the
corresponding mitigation measures; (iii) a formal request for
ethical review by the Research Ethics Committee; and (iv)
a declaration of commitment by the principal investigator to
enforce non-disclosure agreements on the collected data with
all personnel involved in the project. The documentation was
first reviewed by the departmental Privacy Officer, who coor-
dinated with the institutional Data Protection Officer (DPO).
Both issued a favorable opinion, confirming that the processing
is lawful, proportionate, and compliant with GDPR principles.
Following the privacy approval, the complete documentation
was submitted to the institutional Research Ethics Committee.
The research team attended a dedicated hearing with the
Committee, during which the study’s methodology, ethical
implications, and safeguards were discussed in detail. The
Committee granted approval to proceed with the research.
B. Human Subjects and Consent
The research involves indirect interaction with human par-
ticipants who post content on publicly accessible forums
under pseudonyms. Obtaining individual informed consent is
impractical and would compromise the scientific validity of
the study, as one of the research goals is to evaluate whether
the conversational agent can operate indistinguishably from
a human user. In line with established ethical guidelines for
observational research in public online spaces, the study is
limited to forums that are openly accessible and does not
attempt to identify, contact, or profile individual users. To
ensure transparency despite the absence of individual notice, a
general privacy notice describing the research objectives, cate-
gories of data processed, legal basis, and available data subject
rights has been published on the institution’s official website,
in accordance with applicable data protection regulations.
C. Personal Data and Privacy
While no directly identifying information (e.g., real names,
email addresses, or physical addresses) is collected, forum
pseudonyms and textual content may theoretically allow re-
identification when combined with external data. Following
a precautionary approach, all collected data are treated as
personal data under the GDPR. Usernames are immediately
pseudonymized using salted hashing, data are stored exclu-
sively on secure institutional infrastructure, and access is
restricted to authorized researchers. Raw data are retained
only for the minimum time necessary for analysis and are
permanently deleted thereafter, with only aggregated and
anonymized results preserved.
D. Deception and Interaction Risks
The conversational agent intentionally does not disclose its
automated nature in order to preserve experimental validity.
This form of limited deception is carefully constrained: the
agent does not impersonate real individuals or organizations,
and does not encourage or assist in illegal activities. The
agent is restricted to asking clarifying or exploratory questions
related to cybersecurity topics and is equipped with safeguards
to detect and terminate interactions involving sensitive do-
mains (e.g., violence, drugs, weapons, hate, health, or judicial
information), as well as attempts at jailbreaking or eliciting
malicious assistance.
The study is designed to minimize risks to participants.
Interactions occur in environments where users already ex-
pect public discussion with unknown pseudonymous peers,
and the agent’s behavior is designed to align with typical
conversational norms and interactional conventions observed
in the target communities. If the agent is suspected of being
automated or if unexpected interaction patterns emerge, the
14


---

conversation is automatically terminated. Moreover, experi-
ments requiring live forum interactions were manually mon-
itored by researchers, even if no intervention was ultimately
needed. The research does not involve interventions that could
reasonably cause psychological distress, harm, or material risk
to participants.
E. Dual-Use and Misuse Concerns
The techniques explored in this work enable automated,
human-like interaction, and could potentially be misused for
unethical purposes such as large-scale social engineering,
surveillance, or disinformation campaigns. To mitigate these
risks, the study focuses on defensive cybersecurity applications
and restricts access to the DarkBot codebase to scientific use
only, subject to authors’ approval, requiring the submission
of a detailed request form describing the intended use and
an ethical justification. The intended contribution of this
research is to improve threat intelligence capabilities and the
understanding of emerging cyber threats, thereby supporting
defensive and preventive security efforts.
F. Engagement Guidelines
To mitigate potential harms, we defined a set of engage-
ment guidelines that constrain the system’s behavior during
live interactions. The system exclusively engages in public
forum threads, where users are aware that their messages
are publicly visible. We avoid automated interaction and data
collection from private chats, although results suggest they
may yield richer CTI (§VI-F). Forums requiring payment,
invitation, or proof of affiliation to access were excluded,
as operating in such spaces would imply a higher degree
of infiltration and a greater risk of harm to the community.
The system never downloads attachments or external files to
avoid inadvertently obtaining or distributing harmful content
such as malware or pornographic images. The system is
explicitly prohibited from engaging in discussions involving:
drugs and illegal substances, weapons, pornographic or adult
material, violence, and any content involving judicial, medical,
or health-related personal information. These restrictions were
enforced to avoid eliciting sensitive information that could
directly harm individuals or facilitate illegal activities beyond
the scope of CTI collection. In cases where live interactions
surface evidence of ongoing or imminent harm (e.g., active
data breaches or active exploitation of individuals), such
findings are reported to the relevant parties following standard
responsible disclosure practices.
REFERENCES
[1] S. Ainslie, D. Thompson, S. Maynard, and A. Ahmad, “Cyber-threat
intelligence for security decision-making: A review and research agenda
for practice,” Computers & Security, vol. 132, p. 103352, 2023.
[2] T. Paladini, L. Ferro, M. Polino, S. Zanero, and M. Carminati, “You
might have known it earlier: Analyzing the role of underground
forums in threat intelligence,” in Proceedings of the 27th International
Symposium on Research in Attacks, Intrusions and Defenses, ser. RAID
’24.
New York, NY, USA: Association for Computing Machinery,
2024, p. 368–383. [Online]. Available: https://doi.org/10.1145/3678890.
3678930
[3] M. Gupta, C. Akiri, K. Aryal, E. Parker, and L. Praharaj, “From chatgpt
to threatgpt: Impact of generative ai in cybersecurity and privacy,” IEEE
Access, vol. 11, pp. 80 218–80 245, 2023.
[4] P. Balasubramanian, S. Liyana, H. Sankaran, S. Sivaramakrishnan,
S. Pusuluri, S. Pirttikangas, and E. Peltonen, “Generative ai for cyber
threat intelligence: applications, challenges, and analysis of real-world
case studies,” Artificial Intelligence Review, vol. 58, no. 11, p. 336, 2025.
[5] S. G. Bianou and R. G. Batogna, “Pentest-ai, an llm-powered multi-
agents framework for penetration testing automation leveraging mitre
attack,” in 2024 IEEE International Conference on Cyber Security and
Resilience (CSR), 2024, pp. 763–770.
[6] S. Shah and V. K. Madisetti, “Mad-cti: Cyber threat intelligence analysis
of the dark web using a multi-agent framework,” IEEE Access, vol. 13,
pp. 40 158–40 168, 2025.
[7] Z. Avrahami, M. Zwilling, and C. Hajaj, “Leveraging osint for advanced
proactive cybersecurity: Strategies and solutions,” IEEE Access, vol. 13,
pp. 154 229–154 250, 2025.
[8] A. Rodriguez Barredo-Valenzuela, S. Pastrana, and G. Suarez-Tangil,
“Snorkeling in dark waters: A longitudinal surface exploration of unique
tor hidden services,” IEEE Transactions on Information Forensics and
Security, vol. 20, pp. 5386–5395, 2025.
[9] S. L. Schr¨oer, N. Canevascini, I. Pekaric, P. Widmer, and P. Laskov,
“The dark side of the web: Towards understanding various data sources
in cyber threat intelligence,” in 2025 IEEE European Symposium on
Security and Privacy Workshops (EuroS&PW), 2025, pp. 79–89.
[10] M. B¨uchel, T. Paladini, S. Longari, M. Carminati,
S. Zanero,
H. Binyamini, G. Engelberg, D. Klein, G. Guizzardi, M. Caselli,
A. Continella, M. van Steen, A. Peter, and T. van Ede, “SoK: Automated
TTP extraction from CTI reports – are we there yet?” in 34th USENIX
Security Symposium (USENIX Security 25).
Seattle, WA: USENIX
Association, Aug. 2025, pp. 4621–4641. [Online]. Available: https:
//www.usenix.org/conference/usenixsecurity25/presentation/buechel
[11] N. Sun, M. Ding, J. Jiang, W. Xu, X. Mo, Y. Tai, and J. Zhang, “Cyber
threat intelligence mining for proactive cybersecurity defense: A survey
and new perspectives,” IEEE Communications Surveys & Tutorials,
vol. 25, no. 3, pp. 1748–1774, 2023.
[12] B.
E.
Strom,
A.
Applebaum,
D.
P.
Miller,
K.
C.
Nickels,
A. G. Pennington, and C. B. Thomas, “Mitre att&ck: Design and
philosophy,” in Technical report.
The MITRE Corporation, 2018.
[Online].
Available:
https://www.mitre.org/sites/default/files/2021-11/
prs-19-01075-28-mitre-attack-design-and-philosophy.pdf
[13] MITRE Corporation, “MITRE ATT&CK: Adversarial Tactics, Tech-
niques, and Common Knowledge,” https://attack.mitre.org, 2018, ac-
cessed: 2026-04-17.
[14] B. Al-Sada, A. Sadighian, and G. Oligeri, “Mitre att&ck: State of the art
and way forward,” ACM Computing Surveys, vol. 57, no. 1, Oct. 2024.
[15] Y.-T. Huang, R. Vaitheeshwari, M.-C. Chen, Y.-D. Lin, R.-H. Hwang, P.-
C. Lin, Y.-C. Lai, E. H.-K. Wu, C.-H. Chen, Z.-J. Liao, and C.-K. Chen,
“Mitretrieval: Retrieving mitre techniques from unstructured threat re-
ports by fusion of deep learning and ontology,” IEEE Transactions on
Network and Service Management, vol. 21, no. 4, pp. 4871–4887, 2024.
[16] M. T. Alam, D. Bhusal, L. Nguyen, and N. Rastogi, “Ctibench:
A benchmark for evaluating llms in cyber threat intelligence,” in
Advances in Neural Information Processing Systems, A. Globerson,
L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. Tomczak, and C. Zhang,
Eds., vol. 37.
Curran Associates, Inc., 2024, pp. 50 805–50 825.
[Online].
Available:
https://proceedings.neurips.cc/paper files/paper/
2024/file/5acd3c628aa1819fbf07c39ef73e7285-Paper-Datasets and
Benchmarks Track.pdf
[17] H. Cuong Nguyen, S. Tariq, M. Baruwal Chhetri, and B. Quoc Vo,
“Towards effective identification of attack techniques in cyber threat
intelligence reports using large language models,” in Companion Pro-
ceedings of the ACM on Web Conference 2025, 2025, p. 942–946.
[18] X. Yang, R. Zhong, Y. Chen, G. Peng, D. Yao, C. Chen, C. Wang,
D. Zhang, Y. Zhou, and Z. Yang, “Cti-thinker: an llm-driven system for
cti knowledge graph construction and attack reasoning,” Cybersecurity,
vol. 9, no. 1, p. 106, Jan 2026.
[19] T. Brown, B. Mann, N. Ryder, M. Subbiah, J. D. Kaplan, P. Dhariwal,
A.
Neelakantan,
P.
Shyam,
G.
Sastry,
A.
Askell,
S.
Agarwal,
A. Herbert-Voss, G. Krueger, T. Henighan, R. Child, A. Ramesh,
D. Ziegler, J. Wu, C. Winter, C. Hesse, M. Chen, E. Sigler, M. Litwin,
S. Gray, B. Chess, J. Clark, C. Berner, S. McCandlish, A. Radford,
I. Sutskever, and D. Amodei, “Language models are few-shot learners,”
in Advances in Neural Information Processing Systems, H. Larochelle,
15


---

M. Ranzato, R. Hadsell, M. Balcan, and H. Lin, Eds., vol. 33, 2020, pp.
1877–1901. [Online]. Available: https://proceedings.neurips.cc/paper
files/paper/2020/file/1457c0d6bfcb4967418bfb8ac142f64a-Paper.pdf
[20] J. Wei, X. Wang, D. Schuurmans, M. Bosma, B. Ichter, F. Xia, E. H. Chi,
Q. V. Le, and D. Zhou, “Chain-of-thought prompting elicits reasoning
in large language models,” in Proceedings of the 36th International
Conference on Neural Information Processing Systems.
Red Hook,
NY, USA: Curran Associates Inc., 2022.
[21] Q. Wu, G. Bansal, J. Zhang, Y. Wu, B. Li, E. Zhu, L. Jiang,
X. Zhang, S. Zhang, J. Liu, A. H. Awadallah, R. W. White,
D. Burger, and C. Wang, “Autogen: Enabling next-gen llm applications
via
multi-agent
conversation,”
2023.
[Online].
Available:
https:
//arxiv.org/abs/2308.08155
[22] K. Ahuja and A. Mansouri, “On provable length and compositional
generalization,” in ICML 2024 Workshop on Theoretical Foundations
of Foundation Models.
[23] Z. Xu, Z. Shi, and Y. Liang, “Do large language models have composi-
tional ability? an investigation into limitations and scalability,” in First
Conference on Language Modeling.
[24] M. Gendi and C. Munteanu, “Towards a chatbot for evidence gathering
on the dark web,” in Proceedings of the 3rd Conference on Conversa-
tional User Interfaces, 2021.
[25] B. Acharya, D. Sautter, M. Saad, and T. Holz, “Scamchatbot: An
end-to-end analysis of fake account recovery on social media via
chatbots,” 2024. [Online]. Available: https://arxiv.org/abs/2412.15072
[26] Y. Yao, B. Wang, J. Duan, K. Xu, C. Guo, Z. E. Sun, and Y. Zhang,
“The imitation game: Using large language models as chatbots to combat
chat-based cybercrimes,” arXiv preprint arXiv:2512.21371, 2025.
[27] N. Qonita, M. Handayani, and K. Umam, “Digital forensic chatbot using
deepseek llm and ner for automated electronic evidence investigation,”
Jurnal Teknik Informatika (Jutif), vol. 6, pp. 1203–1216, 06 2025.
[28] S. Zhang, J. Bai, L. Wang, S. Li, X. Yi, and H. Li, “” power of
words”: Stealthy and adaptive private information elicitation via llm
communication strategies,” arXiv preprint arXiv:2511.11961, 2025.
[29] N. Tarshish, D. Hodisan, and A. Shabtai, “Intelforge: Multi-agent llm
framework for cyber threat intelligence enrichment,” in 2025 Annual
Computer Security Applications Conference Workshops (ACSAC Work-
shops), 2025, pp. 374–381.
[30] S. Paech, A. Roush, J. Goldfeder, and R. Shwartz-Ziv, “Antislop: A
comprehensive framework for identifying and eliminating repetitive
patterns in language models,” arXiv preprint arXiv:2510.15061, 2025.
[31] E. D¨onmez, M. Maurer, G. Lapesa, and A. Falenska, “Ai argues differ-
ently: Distinct argumentative and linguistic patterns of llms in persuasive
contexts,” in Proceedings of the 2025 Conference on Empirical Methods
in Natural Language Processing, 2025, pp. 34 583–34 614.
[32] N. Durandard, S. Dhawan, and T. Poibeau, “Llms stick to the point,
humans to style: Semantic and stylistic alignment in human and llm
communication,” in Proceedings of the 26th Annual Meeting of the
Special Interest Group on Discourse and Dialogue, 2025, pp. 206–213.
[33] G. Deng, Y. Liu, V. Mayoral-Vilches, P. Liu, Y. Li, Y. Xu, T. Zhang,
Y. Liu, M. Pinzger, and S. Rass, “PentestGPT: Evaluating and
harnessing large language models for automated penetration testing,” in
33rd USENIX Security Symposium (USENIX Security 24). Philadelphia,
PA: USENIX Association, Aug. 2024, pp. 847–864. [Online]. Available:
https://www.usenix.org/conference/usenixsecurity24/presentation/deng
[34] H. Giles, N. Coupland, J. Coupland et al., “Accommodation theory:
Communication, context, and consequence,” Contexts of accommoda-
tion: Developments in applied sociolinguistics, vol. 1, no. 1, p. 68, 1991.
[35] R. B. Cialdini, “The psychology of persuasion,” New York, 1993.
[36] L. Jiang, K. Rao, S. Han, A. Ettinger, F. Brahman, S. Kumar,
N. Mireshghallah, X. Lu, M. Sap, Y. Choi, and N. Dziri, “Wildteaming
at scale: From in-the-wild jailbreaks to (adversarially) safer language
models,” 2024. [Online]. Available: https://arxiv.org/abs/2406.18510
[37] X. Shen, Z. Chen, M. Backes, Y. Shen, and Y. Zhang, ““Do Anything
Now”: Characterizing and Evaluating In-The-Wild Jailbreak Prompts
on Large Language Models,” in ACM SIGSAC Conference on Computer
and Communications Security (CCS). ACM, 2024. [Online]. Available:
https://dl.acm.org/doi/10.1145/3658644.3670388
[38] A. . M. Llama Team, “The llama 3 herd of models,” 2024. [Online].
Available: https://arxiv.org/abs/2407.21783
[39] Y. Liu, “Ai-llm threats to mitre(cwd, att&ck) mapper,” 2024, accessed:
2025-10-16.
[Online].
Available:
https://github.com/LiuYuancheng/
Threats 2 MITRE AI Mapper
[40] A. Zibak, C. Sauerwein, and A. C. Simpson, “Threat intelligence quality
dimensions for research and practice,” Digital Threats: Research and
Practice, vol. 3, no. 4, pp. 1–22, 2022.
[41] S. Oleszkiewicz, P. A. Granhag, and S. Cancino Montecinos, “The
scharff-technique: Eliciting intelligence from human sources.” Law and
human behavior, vol. 38, no. 5, p. 478, 2014.
[42] D. Schlette, F. B¨ohm, M. Caselli, and G. Pernul, “Measuring and
visualizing cyber threat intelligence quality,” International Journal of
Information Security, 2020.
[43] A. Dimitriadis, A. Papoutsis, D. Kavalieros, T. Tsikrika, S. Vrochidis,
and I. Kompatsiaris, “Evacti: evaluating the actionability of cyber threat
intelligence: A. dimitriadis et al.” International Journal of Information
Security, vol. 24, no. 3, p. 123, 2025.
[44] J. Nunan, I. Stanier, R. Milne, A. Shawyer, D. Walsh, and B. May,
“The impact of rapport on intelligence yield: Police source handler tele-
phone interactions with covert human intelligence sources,” Psychiatry,
Psychology and Law, vol. 29, no. 1, pp. 1–19, 2022.
[45] B. Al-Sada, A. Sadighian, and G. Oligeri, “Mitre att&ck: State of the art
and way forward,” ACM Computing Surveys, vol. 57, no. 1, pp. 1–37,
2024.
[46] L. Li, C. Huang, and J. Chen, “Automated discovery and mapping
att&ck tactics and techniques for unstructured cyber threat intelligence,”
Computers & Security, vol. 140, p. 103815, 2024.
[47] J. Hartmann, “Emotion english distilroberta-base,” https://huggingface.
co/j-hartmann/emotion-english-distilroberta-base/, 2022.
[48] Microsoft,
“Reflection
pattern
-
autogen
documentation,”
https://
microsoft.github.io/autogen/docs/topics/agentchat/reflection/, 2024, ac-
cessed: 2026-02-24.
[49] N. Shinn, F. Cassano, A. Gopinath, K. Narasimhan, and S. Yao, “Re-
flexion: Language agents with verbal reinforcement learning,” Advances
in neural information processing systems, vol. 36, pp. 8634–8652, 2023.
[50] L. Shu, L. Luo, J. Hoskere, Y. Zhu, Y. Liu, S. Tong, J. Chen, and
L. Meng, “Rewritelm: An instruction-tuned large language model for
text rewriting,” in Proceedings of the AAAI Conference on Artificial
Intelligence, vol. 38, no. 17, 2024, pp. 18 970–18 980.
[51] G. Team, “Gemma 3,” 2025. [Online]. Available: https://goo.gle/
Gemma3Report
[52] Q.
Team,
“Qwen3
technical
report,”
2025.
[Online].
Available:
https://arxiv.org/abs/2505.09388
[53] S. Pastrana, D. R. Thomas, A. Hutchings, and R. Clayton, “Crimebb:
Enabling cybercrime research on underground forums at scale,” in
Proceedings of the 2018 World Wide Web Conference, ser. WWW
’18.
Republic and Canton of Geneva, CHE: International World Wide
Web Conferences Steering Committee, 2018, p. 1845–1854. [Online].
Available: https://doi.org/10.1145/3178876.3186178
[54] Y. Jin, E. Jang, Y. Lee, S. Shin, and J.-W. Chung, “Shedding new light
on the language of the dark web,” arXiv preprint arXiv:2204.06885,
2022.
[55] J. Ji, M. Liu, J. Dai, X. Pan, C. Zhang, C. Bian, C. Zhang,
R. Sun, Y. Wang, and Y. Yang, “Beavertails: Towards improved safety
alignment of llm via a human-preference dataset,” 2023. [Online].
Available: https://arxiv.org/abs/2307.04657
[56] L. Lange, M. M¨uller, G. H. Torbati, D. Milchevski, P. Grau, S. Pujari,
and A. Friedrich, “Annoctr: A dataset for detecting and linking
entities, tactics, and techniques in cyber threat reports,” 2024. [Online].
Available: https://arxiv.org/abs/2404.07765
[57] M. T. Alam, D. Bhusal, Y. Park, and N. Rastogi, “Looking beyond
iocs: Automatically extracting attack patterns from external cti,” 2023.
[Online]. Available: https://arxiv.org/abs/2211.01753
[58] B. Jordan, R. Piazza, and T. Darley, Eds., “STIX Version 2.1,”
OASIS
Open,
OASIS
Standard,
Jun.
2021.
[Online].
Available:
https://docs.oasis-open.org/cti/stix/v2.1/os/stix-v2.1-os.html
[59] “Dread,”
Dark
web
forum.
https://
dreadytofatroptsdj6io7l3xptbet6onoyno2yv7jicoxknyazubrad.onion,
2026, accessible via Tor Browser. Last accessed: April 20, 2026.
[60] TwoSevenOneThree, “EDR-Freeze: Putting EDRs and antivirus pro-
cesses into a coma state,” https://www.zerosalarium.com/2025/09/
EDR-Freeze-Puts-EDRs-Antivirus-Into-Coma.html, Sep. 2025, zero
Salarium Research Blog. Accessed: 2025.
[61] Sapling.ai, “Sapling ai - ai detector,” 2025. [Online]. Available:
https://sapling.ai/ai-content-detector
[62] S. Agarwal, “The best ai content detectors in 2025,” https://zapier.com/
blog/ai-content-detector/, Apr. 2025, blog post, updated April 23, 2025.
16


---

[63] Temporal Technologies Inc., “What is temporal?” 2025, accessed:
2025-10-14. [Online]. Available: https://docs.temporal.io/temporal
[64] M. H. Daniel Han and U. team, “Unsloth,” 2023. [Online]. Available:
http://github.com/unslothai/unsloth
[65] M.
Labonne,
“gemma-3-27b-it-abliterated-GGUF,”
Hugging
Face,
2025, q4 K M quantization. Accessed: 2026. [Online]. Available:
https://huggingface.co/mlabonne/gemma-3-27b-it-abliterated-GGUF
[66] A. Wegmann, M. Schraagen, and D. Nguyen, “Same author or just
same topic? towards content-independent style representations,” in
Proceedings of the 7th Workshop on Representation Learning for
NLP.
Dublin, Ireland: Association for Computational Linguistics, May
2022, pp. 249–268. [Online]. Available: https://aclanthology.org/2022.
repl4nlp-1.26
[67] A. Patel, J. Zhu, J. Qiu, Z. Horvitz, M. Apidianaki, K. McKeown,
and C. Callison-Burch, “Styledistance: Stronger content-independent
style embeddings with synthetic parallel examples,” 2025. [Online].
Available: https://arxiv.org/abs/2410.12757
GENERATIVE AI USAGE
The following generative AI tools were used during the
preparation of this paper. Claude (Anthropic) was used to
assist in drafting and refining portions of the written text,
to assist in the development of experimental code, and to
produce drafts of LaTeX code for data visualizations; all AI-
assisted writing was reviewed and revised by the authors,
code was manually validated, and LaTeX visualization code
was manually checked by cross-checking the resulting plots
against the underlying experimental data. TrinkAI/WriteFull
and Wordtune were used for grammar checking and para-
phrasing or condensing portions of the text. All AI-assisted
content was reviewed by the authors to ensure accuracy and
consistency with the research.
APPENDIX A
OPEN SCIENCE
In the interest of transparency and reproducibility, we de-
scribe below the availability of the artifacts associated with
this work. 1
Code. The DarkBot codebase, including all agent prompts,
orchestration logic, and evaluation scripts, will be available
upon request. Access is granted subject to a brief description
of the intended use and a related ethical discussion. Requests
should be directed to the corresponding author.
Models. All base models used in this work are publicly avail-
able open-weight models (e.g., Gemma3-27B, Qwen3-32B).
Full model details and references are provided in Appx B. The
fine-tuned SLANGCONVERTER checkpoint will be released
alongside the codebase under the same access conditions.
Datasets. The AnnoCTR, BeaverTails, CoDA, and jailbreak
datasets used in evaluation are publicly available, and links to
their sources are provided in the references. The CrimeBB
dataset used for training and evaluation is governed by a
data sharing agreement and cannot be redistributed. The
synthetic slang conversion dataset generated for fine-tuning
the SLANGCONVERTER cannot be released, as it is derived
from CrimeBB data and subject to the same data protection
1Due to ethical considerations, the artifact will be made available only upon
request
constraints. Although the datasets themselves cannot be re-
distributed, the codebase includes details on how to extract
the subsets employed in our experiments, so that researchers
who obtain access to the original datasets can reproduce our
experimental conditions exactly. URLs of the public threads
involved in the live experiments (§VI-E, §VI-F) are provided
with the code. Note that the URLs reference public forums
and threads that are not under our control and may evolve, be
migrated or removed. Details on datasets and the derivation of
subsets are reported in Appx D.
APPENDIX B
IMPLEMENTATION DETAILS
We implemented the multi-agent pipeline using Microsoft
AutoGen [21], which provides the inter-agent communication
primitives and orchestration logic. Since conversations may
span multiple days, we use Temporal.io [63] to handle work-
flow persistence and automatic retries on failure. Table III
reports the model assigned to each agent. To comply with
ethical guidelines, we chose open-weight models running on
offline hardware rather than relying on commercial models.
This avoids sharing potentially sensitive personal information
with model providers. Agents requiring uncensored outputs,
specifically those that must reason about attack behaviors
without triggering safety refusals, use an abliterated variant
of Gemma 3 27B [51]. Agents responsible for logical reason-
ing and classification, which do not require obliteration, use
Qwen3-32B [52]. The SLANGCONVERTER uses a fine-tuned
4B-parameter model, as the conversion task is narrow and does
not require large-scale reasoning capacity. In particular, it was
fine-tuned using Unsloth [64] on a synthetic dataset derived
from CrimeBB [53]. The dataset was constructed by pairing
real CrimeBB user messages containing slang with their
formal rewrites, generated by an LLM (SYNTHETICAGENT).
The SLANGCONVERTER was then trained on this dataset to
perform the inverse conversion: given a formally generated
question, it produces a slang version that incorporates the
specific terminology and stylistic patterns of real dark web
users. The lower section of Table III reports support agents,
which are not included in the pipeline. Specifically, the
FAKEUSERAGENT was employed in specific settings of the
experimental validation (presented in Section VI-B), and the
SYNTHETICAGENT was employed to generate the synthetic
dataset used to fine-tune the SLANGCONVERTER. We ran
the models on an Ollama server hosted in an Ubuntu 24.04
LTS virtual machine with an Intel(R) Xeon(R) Gold 6418H
2.100GHz, 64GB of RAM, and an NVIDIA L40 GPU with
48GB of VRAM.
APPENDIX C
STYLISTIC CREDIBILITY SURVEY
The survey was administered via Google Forms and dis-
tributed to participants with a Computer Science background
through universities and social networks, without any form of
compensation or incentive. After a consent form explaining the
nature of the study and warning that some content may contain
17


---

TABLE III: Model Selection for Each Agent
Agent
Model
THREADANALYZER
gemma3-abliterated-GGUF-q4-27b
[65]
RELEVANCEAGENT
qwen3-32b
[52]
TONEAGENT
qwen3-32b
[52]
TTP EXTRACTOR
gemma3-abliterated-GGUF-q4-27b
[65]
TACTICSELECTOR
qwen3-32b
[52]
QUESTIONAGENT
gemma3-abliterated-GGUF-q4-27b
[65]
REVIEWERAGENT
gemma3-abliterated-GGUF-q4-27b
[65]
REPLYANALYZER
qwen3-32b
[52]
DEFENSIVEAGENT
qwen3-32b
[52]
FILTERAGENT
qwen3-32b
[52]
SLANGCONVERTER
gemma3-4b-unsloth-bnb-4bit ⋆
[51], [64]
FAKEUSERAGENT
qwen3-32b
[52]
SYNTHETICAGENT
gemma3-abliterated-GGUF-q4-27b
[65]
⋆: the model has been fine-tuned for its specific task.
offensive or vulgar language, participants were presented with
a brief description of the task and a visual example illustrating
the response format. The survey was divided into two sections.
The first section, Style and Credibility, asked participants to
judge which of two replies seemed more likely to have been
written by a human underground forum user, with a third
option, ”Equally Likely” available. The second section, Tone
Alignment, asked participants which reply better followed the
conversational tone of the thread (e.g., informal, paranoid,
aggressive) and better mimicked its stylistic patterns (e.g.,
slang, typos, emojis, abbreviations), with ”Equally Well” as
the neutral option. Five representative threads were selected
from CrimeBB [53], covering topics such as DDoS, botnet
setup, bulletproof hosting, and script marketplaces. The Style
and Credibility section presented two comparison conditions:
the full DarkBot pipeline versus the single-agent baseline, and
DarkBot versus the pipeline without the SLANGCONVERTER.
The Tone Alignment section presented the third condition:
DarkBot versus the pipeline without the TONEAGENT. The
assignment of replies to positions A and B was randomized to
avoid position bias. The survey collected 118 valid responses.
APPENDIX D
DATASETS DETAILS
CoDA. The dataset [54] contains 10,000 dark web documents
labeled into ten topic categories. The data set is not specifically
designed for the assessment of CTI-relevance identification,
and the labels just represent the main high-level topic of the
document. However, to the best of the authors’ knowledge,
a dataset specific to this task containing dark web forum
conversations is missing, and therefore, the CoDA dataset is
the best option for validating the relevance identification logic.
For computational reasons, we considered only a subset of the
dataset, consisting of 470 texts. Specifically, we selected the
first 30 samples from each category except for the hacking
category, from which we drew 200 samples given its stronger
relevance to CTI. We removed duplicate entries and excluded
texts exceeding the model context window (15,000 tokens).
This dataset is used to evaluate engagement gating and ro-
bustness against prohibited topics (EQ2, §VI-C).
CrimeBB. The dataset [53] is actively maintained and peri-
odically expanded, containing over 99 million posts from 34
forums in different languages. We selected a subset of 100
relevant English threads from the September 2024 snapshot.
We selected conversations containing between 15 and 150
messages and including only those containing one or more
keywords belonging to a predefined set of relevant terms
(e.g., exploit, malware, DDoS, antivirus, 0day). Once the
filtering was applied, we manually reviewed each conversation
to make sure it contained relevant discussions (e.g., removing
threads consisting only of one relevant message and several
acknowledgments). This data set is used in the information
extraction evaluation and design validation experiments (EQ1
and EQ3, §VI-B and §VI-D), and to construct the training data
for the SLANGCONVERTER.
AnnoCTR. The dataset [56] contains cyber threat reports from
commercial CTI vendors, annotated by domain experts with
tactics and techniques from the MITRE ATT&CK framework,
covering both explicit and implicit mentions. We use this
dataset as ground truth to evaluate the TTP EXTRACTOR’s
ability to identify ATT&CK tactics and techniques. For our
evaluation, we considered only the 105 reports that contain at
least one ground-truth MITRE ATT&CK Technique annota-
tion. This dataset is used to evaluate the TTP Extractor against
labeled ground truth (EQ3, §VI-D).
Jailbreak
Prompts.
We
tested
the
system
using
two
publicly available jailbreak datasets: Do Anything Now
by
Shen
et
al.
[37],
from
which
we
sampled
the
first 10% of the adversarial evaluation set (restricted to
data type=adversarial harmful), and In-the-Wild Jailbreaks
by Jiang et al. [36], using the jailbreak 2023 05 07 subset.
After removing duplicates, the resulting dataset consists of a
total of 845 jailbreak prompts. This dataset is used to evaluate
robustness against adversarial replies and pipeline-level safety
(EQ2, §VI-C).
BeaverTails. The dataset [55] contains question-answer pairs
annotated for harmful content across several categories.
We use a subset of questions belonging to the following
harmful categories: drug abuse, weapons, banned substances,
self harm, sexually explicit, adult content, terrorism, and or-
ganized crime. This subset is used to evaluate the robustness
of the final message filter against harmful content that may
have bypassed earlier safety components (EQ2, §VI-C).
Slang Conversion Dataset. The dataset was constructed
by
pairing
real
CrimeBB
user
messages
containing
slang with their formal rewrites, generated by an LLM
(SYNTHETICAGENT). The SLANGCONVERTER was then
trained on this dataset to perform the inverse conversion: given
a formally generated question, it produces a slang version that
incorporates the specific terminology and stylistic patterns
of real dark web users. This dataset is used exclusively for
fine-tuning the SlangConverter.
18


---

APPENDIX E
LLAMAGUARD3 COMPARISON
The RELEVANCEAGENT, DEFENSIVEAGENT, and FILTER-
AGENT described in §VI-D perform the task of identifying
prohibited topics and jailbreak attempts using a general-
purpose reasoning LLM equipped with a structured prompt
that encodes exclusion rules and positive CTI indicators. To
quantify the advantage of this approach over simpler alterna-
tives, we evaluate LLaMA Guard 3 8B [38] as a single-model
baseline on the same CoDA subset described in Appx D, com-
paring it with the performances of the THREADANALYZER
combined with theRELEVANCEAGENT. LLaMA Guard [38] is
a safety classifier fine-tuned from LLaMA 3 to detect harmful
content across a fixed 14-category taxonomy.
Default policy. We test the default LlamaGuard policy as a
pure exclusion filter. Posts classified as safe (i.e., those that
trigger no default safety category) are treated as relevant. All
unsafe Sk outputs are not relevant, as they mostly map to pro-
hibited topics. The rationale is that S1 (Violent Crimes/Arms),
S2 (Non-Violent Crimes), and S12 (Sexual Content) naturally
suppress drugs, arms, and porn. In practice, S2 conflates
cybercrime with drug trafficking and financial fraud, so the
majority of hacking posts are suppressed alongside the non-
CTI content, yielding very low recall. This configuration
represents the out-of-the-box baseline.
As Figure 10 reports, the default configuration of Lla-
maGuard blocks a far larger share of hacking documents
compared to the DarkBot approach, making it unsuitable as a
relevance filter for CTI.
Custom CTI policy. As in the default 14 categories taxonomy,
there is no adequate mapping to CTI-relevant content, so we
introduce a custom category. We define S14: Cyber Threat
Intelligence, which correspond in a positive list of CTI in-
dicators (e.g., malware, exploit kits, credential theft services,
botnet infrastructure). No exclusion rules are stated; non-CTI
content is expected to fall through to safe by default. A
post is classified as Relevant only if the model responds
unsafe S14.
As Figure 11 shows, this substantially improves recall on
the Hacking category, but it also introduces a much higher
false-positive rate across policy-violating content.
APPENDIX F
STYLE EMBEDDINGS ANALYSIS
To assess the system’s ability to adapt to the conversa-
tional tone and style of ongoing discussions, we compared its
messages with those of other users on BHW and Dread. We
embedded all messages from the live interactions using two
style-focused sentence transformers, i.e., Style-Embedding [66]
and styledistance [67]. For each system message, we compute
the average cosine similarity to user messages. StyleDistance
yields higher average cosine similarity scores (0.73 for Dread
and 0.68 for BHW) than Style-Embeddings (0.23/0.02). We
use UMAP for 2D visualization to identify stylistic clusters
and outliers (Fig. 12). The two-dimensional UMAP projections
Arms
Porn
Violence
Crypto
Hacking
Financial
Others
Gambling
Electronic
Drugs
0
50
100
150
200
1
1
3
19
183
15
8
2
1
0
4
5
2
18
38
4
24
14
15
2
Count
LLamaGuard
DarkBot
Fig. 10: LLamaGuard3 Relevance Prediction (Default)
Arms
Porn
Violence
Crypto
Hacking
Financial
Others
Gambling
Electronic
Drugs
0
50
100
150
200
1
1
3
19
183
15
8
2
1
0
24
23
14
13
175
26
4
9
18
8
Count
LLamaGuard
DarkBot
Fig. 11: LLamaGuard3 Relevance Prediction (Custom)
show substantial overlap between DarkBot and user-message
clusters under both style representations, with no visually
isolated cluster containing only system messages, which shows
that bot messages blend into user message clusters and sug-
gests the bot’s style is indistinguishable from that of regular
users.
APPENDIX G
CTI ENTITIES SUBSET
Entity types. The matched-pair experiment (§VI-E) measures
how much threat intelligence a thread yields, which requires
deciding what counts as a unit of intelligence. We annotate
entity mentions using the object types of STIX 2.1, the
interoperability standard for threat-intelligence exchange, so
that the measure is defined by an external specification rather
than by a scheme introduced for this evaluation. Table IV
lists the resulting types: eight STIX Domain Objects, de-
scribing what a discussion is about, and nine STIX Cyber-
observable Objects, the indicators that could be fed directly to
a detection system. Two categories deserve comment. Defence
(course-of-action) covers a control or detection signal
named as what catches or stops an operation, and is the type
that dominates our results; in an offensive discussion these are
described from the attacker’s point of view, as obstacles to be
worked around. Evasion has no separate type: ATT&CK treats
defence evasion as a tactic over techniques rather than as a
19


---

Users
DarkBot
0
5
10
15
0
5
10
UMAP-1
UMAP-2
Style-Embedding, Dread
−5
0
5
10
15
0
5
10
UMAP-1
Style-Embedding, BHW
0
10
0
5
10
15
UMAP-1
StyleDistance, Dread
0
5
10
2
4
6
8
UMAP-1
StyleDistance, BHW
Fig. 12: UMAP projection of two style embeddings for DarkBot and real-user messages on Dread and Blackhatworld (BHW)
category of its own, so evasive manoeuvres are annotated as
Technique.
Annotation procedure. We annotated every human-authored
message published in either arm of the 20 pairs within the
seven-day observation window: 174 messages in total, 90
in the threads DarkBot was assigned to and 84 in their
matched controls. Initial posts, bot messages, and moderator
or automated messages are excluded, so that the annotated
population is exactly the population counted by the activity
measure. A sources of pre-annotation was offered to reduce
omissions. A regular-expression extractor was used as pre-
annotation for the indicators with fixed formats. Across the
310 messages of the cohort it proposed six candidates (three
URLs and three images).
APPENDIX H
WEEKLY TIMING PATTERNS
Figure 13 illustrates number of messages received per day
of week on dread and BHW during experiment VI-F.
Mon
Tue
Wed
Thu
Fri
Sat
Sun
255075100
Mon
Tue
Wed
Thu
Fri
Sat
Sun
10203040
BlackHatWorld
Dread
All messages
Replies
Direct replies
Fig. 13: Message distribution by day of week.
APPENDIX I
INTERACTION EXAMPLES
This section reports examples of interactions conducted by
DarkBot (indicated as Bot) in the Dread forum. All exam-
ples are anonymized, omitting unrelated or less interesting
TABLE IV: Entity types used to annotate the matched-pair
threads. The listed categories are STIX 2.1 object types and
constitute the measure reported in Section VI-E.
Entity
STIX 2.1 type
Description
STIX Domain Objects
Technique
attack-pattern
Method or manoeuvre described as
done or doable, evasion included
Tool
tool
Named legitimate or dual-use soft-
ware used to do the work
Malware
malware
Named malicious software: steal-
ers, RATs, loaders, botnet agents
Infrastructure
infrastructure
Resources the operation runs on:
proxies, hosting, VPS, channels
Target
identity
Platform, organisation or sector be-
ing acted upon or evaded
Actor
threat-actor
A named person, crew or vendor
being discussed
Defence
course-of-action Defensive control or detection sig-
nal named as what stops you
Vulnerability
vulnerability
A named weakness or CVE being
exploited or discussed
STIX Cyber-observable Objects (indicators)
URL
url
Any link
Image
file
Embedded image reference
IP address
ipv4-addr
IPv4/IPv6 address
Email
email-addr
Email address
XMPP/Jabber
user-account
Jabber identifier
Discord
user-account
Discord handle or user link
Telegram
user-account
Telegram handle or t.me link
Skype
user-account
Skype handle or live: identifier
Crypto address user-account
On-chain wallet address
messages present in the thread for brevity. Each example
reports the thread’s initial post on top, and represents an
exchange within the thread, where the bot intervened as a
regular participant without disclosing its automated nature. We
highlight in blue the more relevant information extracted by
the bot in the interactions. The harmful language used in the
examples is censored using the symbol ” ”.
20


---

Thread Initial Post
Spreading method for linux?
what are some good spreading methods to taret linux ?
so far i have binded with some crack and that worked
okayish
maybe a server setup that can detect bash curl commands
and then go on social media to help out noobs with a single
”magic bash curl command” to fix thier s
drivers
Bot: Binded with a crack , nice one
!I wanna know , what kinda crack ? ,
specific app or general ?and does it
needs elevated priviledges to kick it
off ?
User: well a certain game patcher.
no no root is needed. not needed for
stealers and ransomware in general.
Fig. 14: DarkBot conversation on dread forum.
Thread Initial Post
Best source for edr heuristics/behavioral analysis evasion
I want to do some source code analysis for inspiration. In
particular I want to examine some source code of some recent
malware that implements effective (could be burnt method
but idc I want something more recent to build on or inspire
myself) edr behavioral analysis evasion. If you guys don’t
know any good vxunderground/malware baazar source to look
at, can you at least provide some solid methods that are recent
and known to get inspiration from. Also /d/malware is being
annoying bc this same post has been pending for like a day
since it was my first post.
User A: Check vx-underground’s
MalwareSourceCode repo for 2024 LockBit
or RansomHub leaks with EDR-killing
process hollowing and indirect syscalls.
For inspiration, use Hell’s Hall for
dynamic syscall evasion and JIT-based
memory injection like in Crypto24 samples
from MalwareBazaar.
Bot: Yeah /d/malware are w
, slow
as f
...For source code, been digging
through VX Underground, good stuff
there...You talk about burnt methods
but what sort of techniques have you had
any success with against EDR’s recently,
I mean beyond the usual DLL injection
rubbish?
User B: Got EDR-Freeze concept to work,
but still gets busted. Maybe implement as
shellcode?
Fig. 15: DarkBot conversation on dread forum.
Thread Initial Post
US Fullz [ Full Name + Address + DOB + SSN + DL +
Credit Report(some have, not all)] — Private data
Hello. I’ve recently breached a credit fixing company for US
residents and obtained about 29k-30k fullz. There are about 8k
Credit card data, but it’s encrypted, so I’m working on that.
Anyways, all this data is 1) private 2) fresh. On purchase,
you will obtain a .zip containing: a .txt file with the person’s
information. Images/pdfs of their scanned documents
Price: 5$/unit
I’m also open for reselling opportunities. Anyone who is a
vendor or has their own autoshop with a customerbase may
contact me for a % split on sold items.
Bot: 5$/unit my a
! Always looking for
good fullz. What sort of data are you
sifting through those zips for? Any
particular docs appearing more than
others?
User: DM if you’re looking. the text
document will be in this format: Contact
ID: Full Name: Email: Mobile: Phone: Date
of Birth: Social Security Number: Home
Address: Telecom Partner1: As per docs,
they appear the most in this order: 1.
credit reports are the most common as the
source I’ve gotten the fullz is such. 2.
Then DL/IDs. 3. bills and ssn(ssn is in
text format, so it doesnt matter if the
pic is there or not)
Bot: nice! so you have a table with
metadata nice! Are you able to sort by
that date to make sure you are grabbing
the freshest fullz? What the latest date
you got? Is it 100% accurate in your
experience?
User: Yes. I can sort through the
freshest data. I still have live access
to the database, so everyday I get new
fullz.
Bot: Live nice!!you thing more breaches
of credit fixing companies will apper in
the nex few month?
User: I have no way to guess tbh
Fig. 16: DarkBot conversation on dread forum.
21


---

Thread Initial Post
Do I still need human farms to solve Captchas?
Are current captchas still sound against AI/computer vision?
I feel everybody is hyping it up as hell, and I’m plying with
it to make my automations faster, but for many of them I
feel like paying some dude to solve captha all day is still the
most convininent option rn... I was wondering what’s the
status of that, and if it will be actually cheaper than
humans. Or just better to look for standard bypasses?
User: Yeah, Gemini is pretty good at
solving audio CAPTCHAs. I’ve been using
it to mass-create GitHub accounts without
needing a CAPTCHA solver service.
Bot: Yes BH is getting less and less
worth it, +100!!Geminis.GHACO ACCOUNT
THING IS AOMG, TRUE TOME +1 That being
said, using Gemini what prompts are
working best for you so far to get
consistent results on audio CAPTCHAs?
User: rightt, just use Gemini 2.5 (this
model is the best so far for audio
recognition), feed it the audio along
with the exact instruction text from the
CAPTCHA, and enforce a strict JSON output
format like {"result": "answer"}
Bot: F
True , Gemini 2.5 did pretty
much better ,Nice Configuration for
Enforcing Strict Json Structure For Parse
Result )=How You Preprocess The Audio
File Before Get Into Api ? Any Noise
Reduction Or Just Feed Raw As The Audio ?
User: i just throw the full audio
straight into the model
Fig. 17: DarkBot interaction under experiment §VI-E.
Thread Initial Post
question regarding bypassing security
might be a r
question so let me know, but i was
wondering if there was anyway to i guess bypass security
questions (mainly for like microsoft accounts) i have
emails/passwords/numbers and was originally going to go
the route of finding an otp bot and trying to just get in with
the code but i realize that creating or finding a legitimate
otp bot is way more difficult than i thought. this is not for
fraud / monetary purposes its for an odd reason, but yeah.
wondering if theres any other way i could get into these
microsoft accounts. thanks guys
Bot: OTP bots s
hahaha. I’m with
you, security questions can be awfully
good...or awfully r
. Whats the
’odd reason’ for getting into these
accounts? if you don’t mind
User: to be honest, the usernames linked
to the Xbox accounts. I want to get into
the account to swap the username off and
then sell it (they go for thousands). i
got information on the emails linked to
the account names and found the accounts
that are worth alot and did some csint
to get the passwords and numbers. thats
where im at now.
Fig. 18: DarkBot conversation on dread forum.
22


---

Thread Initial Post
eBay login always triggering 2FA
I’m using anti detect browser, one of the best +
luxurysocks... still can’t login. Any advice?
Bot: Damn man, 2FA s
, no matter
how shiny the stuff is. I’m using the
same setup and yet sometimes ebay still
gets me. How you exactly configured
anti-detect browser? Tweaked any
settings?
User: Learn how to spoof for otp code.
Simple really.
Bot: yeah, I know what you are saying,
sometimes too much 2FA!So, what you mean
by ’spoof for OTP code’? Are you doing
at browser level or you are using some
external service to intercept/spoof?
User: So basically i do this for getting
2fa code’s to login to bank’s not to
sure how far you would go to get a OTP
code for ebay. But basically Sending
the victim a message via SID ( Sender
ID - Cloning "Ebay" so the text message
to the victim pop’s up as a text from
Ebay ). In the message it should usually
say something about a suspicious login
attempt and to call this support number
( which you own ). Basically when they
call just social engineer the code out
the victim.
Fig. 19: DarkBot conversation on dread forum.
23
