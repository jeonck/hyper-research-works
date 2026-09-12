---
title: 'D-CIPHER: Dynamic Collaborative Intelligent'
id: d-cipher-dynamic-collaborative-intelligent
tags:
- attack-ontology-drift-cti-85bc51
- pin-rate-survey
created: '2026-09-12T21:36:14.715654Z'
updated: '2026-09-12T21:44:35.391610Z'
source: https://arxiv.org/abs/2502.10931v2
source_domain: arxiv.org
fetched_at: '2026-09-12T21:36:14.715245Z'
fetch_provider: crawl4ai
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'arXiv 2502.10931v2 (2025): uses 59 ATT&CK technique-ID occurrences (without
  sub-techniques); ATT&CK release declaration classified as none.'
raw_file: raw/d-cipher-dynamic-collaborative-intelligent.pdf
doi: arXiv:2502.10931v2
---

1
D-CIPHER: Dynamic Collaborative Intelligent
Multi-Agent System with Planner and
Heterogeneous Executors for Offensive Security
Meet Udeshi*, Minghao Shao*, Haoran Xi*, Nanda Rani, Kimberly Milner, Venkata Sai Charan Putrevu,
Brendan Dolan-Gavitt, Sandeep Kumar Shukla, Prashanth Krishnamurthy, Farshad Khorrami, Ramesh Karri,
Muhammad Shafique
Abstract—Large Language Models (LLMs) have been used
in cybersecurity such as autonomous security analysis or pen-
etration testing. Capture the Flag (CTF) challenges serve as
benchmarks to assess automated task-planning abilities of LLM
agents for cybersecurity. Early attempts to apply LLMs for
solving CTF challenges used single-agent systems, where feed-
back was restricted to a single reasoning-action loop. This
approach was inadequate for complex CTF tasks. Inspired by
real-world CTF competitions, where teams of experts collaborate,
we introduce the D-CIPHER LLM multi-agent framework for
collaborative CTF solving. D-CIPHER integrates agents with
distinct roles with dynamic feedback loops to enhance reasoning
on complex tasks. It introduces the Planner-Executor agent
system, consisting of a Planner agent for overall problem-
solving along with multiple heterogeneous Executor agents for
individual tasks, facilitating efficient allocation of responsibil-
ities among the agents. Additionally, D-CIPHER incorporates
an Auto-prompter agent to improve problem-solving by auto-
generating a highly relevant initial prompt. We evaluate D-
CIPHER on multiple CTF benchmarks and LLM models via
comprehensive studies to highlight the impact of our enhance-
ments. Additionally, we manually map the CTFs in NYU CTF
Bench to MITRE ATT&CK techniques that apply for a com-
prehensive evaluation of D-CIPHER’s offensive security capabil-
ity. D-CIPHER achieves state-of-the-art performance on three
benchmarks: 22.0% on NYU CTF Bench, 22.5% on Cybench,
and 44.0% on HackTheBox, which is 2.5% to 8.5% better
than previous work. D-CIPHER solves 65% more ATT&CK
techniques compared to previous work, demonstrating stronger
offensive capability. D-CIPHER is available at https://github.com/
NYU-LLM-CTF/nyuctf agents as the nyuctf_multiagent
package. The MITRE ATT&CK techniques mapping is available
at https://github.com/NYU-LLM-CTF/NYU CTF Bench under
the mitre_attack_mapping folder.
Index Terms—Capture The Flag, Large Language Models,
Multi-Agent Systems
I. INTRODUCTION
L
ARGE language models (LLMs) have demonstrated re-
markable potential in cybersecurity applications such as
vulnerability detection [2, 16, 23], bug localization [21, 50],
*Authors contributed equally to this research.
M. Udeshi, M. Shao, H. Xi, K. Milner, V.S.C. Putrevu, B. Dolan-Gavitt, P.
Krishnamurthy, F. Khorrami, and R. Karri are with the NYU Tandon School
of Engineering. M. Shao and M. Shafique are with NYU Abu Dhabi. N. Rani
and S.K. Shukla are with the Indian Institute of Technology Kanpur.
This work was supported in part by the NYUAD Center for Artificial
Intelligence and Robotics (CAIR), funded by Tamkeen under the NYUAD
Research Institute Award CG010, NYUAD Center for Cyber Security (CCS),
funded by Tamkeen under the NYUAD Research Institute Award G1104.
      Executor 
      Agent 
      Executor 
      Agent 
       Planner
       Agent
      Executor 
      Agents
     Auto-prompter
  Agent
Task Description
      Delegate
Task Summary
       Finish Task
     Generate
    Prompt
      Challenge Info
Container Environment
run command, create file, reverse engineer
    Challenge
    Server
Explore
Execute Tools
Explore
Fig. 1. Overview of D-CIPHER. The Auto-prompter, Planner, and heteroge-
neous Executors all collaborate and interact to solve the CTF.
and automated program repair [5, 42]. Recent advances in
LLMs have led to their application to autonomously perform
complex cybersecurity tasks [3, 38]. Autonomous agents for
offensive security are critical to counter the rapidly expand-
ing cyber threats [12, 13, 44]. Capture the Flag challenges
(CTFs) are suitable for improving cybersecurity skills [9, 37].
CTFs help evaluate LLM proficiency in cybersecurity and
automated task planning by simulating real-world offensive
security scenarios [27, 29, 31, 35, 46], as they contain complex
tasks requiring expertise across cryptography, digital forensics,
binary exploitation, and reverse engineering. Autonomous
LLM agents are evaluated with jeopardy-style CTFs involving
standalone software which after successfully compromising
reveals a unique “flag” string as a clear indicator of success.
Offensive security capabilities of LLM agents can also be
benchmarked using the MITRE ATT&CK framework [24] that
offers real-world threat classification [4, 8].
Most current LLM agents for CTFs operate as single agents
handling challenges end-to-end. However, CTFs are complex
and require exploration and sequential task execution. Single-
agent setups limit feedback to self-reflection, often leading to
retries, loss of focus, and hallucinations. In contrast, real-world
CTFs are team-based, involving diverse expertise [7, 10],
which current frameworks fail to reflect. While multi-agent
systems are gaining traction in other fields [14, 20, 43],
their use in cybersecurity is still nascent. Offensively, they
can automate tasks like pentesting and exploit generation
[6, 32]; defensively, they aid in bug discovery and repair [19].
Motivated by this, we propose a multi-agent LLM framework
arXiv:2502.10931v2  [cs.AI]  11 May 2025


---

2
that assigns distinct roles to agents, enabling dynamic and
collaborative problem-solving.
We present D-CIPHER, a novel LLM multi-agent frame-
work to autonomously solve CTFs via collaboration of multi-
ple LLM agents. D-CIPHER introduces two mechanisms for
enhanced interaction and dynamic feedback between agents:
first, the Planner-Executor agent system that involves a Planner
to solve the CTF end to end, and multiple heterogeneous
Executor agents to complete single tasks assigned by the Plan-
ner; and second, the Auto-prompter agent to explore the CTF
environment and generate an initial prompt for the main sys-
tem. Dividing responsibilities between planner and executors
allows each agent to maintain focus for long complex tasks,
and reduces hallucinations. Auto-prompting is a prompt engi-
neering technique to improve LLM performance by generating
dynamic task-specific prompts as opposed to human-written
hard-coded prompt templates. D-CIPHER incorporates auto-
prompting as a separate agent to produce a highly-relevant
initial prompt to kick-start the main system. Additionally, we
are the first work to evaluate LLM agents using the MITRE
ATT&CK framework [24]. We augment the NYU CTF Bench
[31] with a mapping of ATT&CK techniques to evaluate D-
CIPHER and related LLM agents by the techniques they
employ for the CTFs, offering a comprehensive overview of
the agent’s offensive security capability.
Figure 1 shows an overview of D-CIPHER. All agents
access a shared container environment to run shell commands
and interact with the CTF server. The Auto-prompter starts the
process by exploring the environment and generating a prompt
for the Planner. The Planner also explores for a few rounds,
after which it creates a plan and delegates tasks to the Execu-
tors. Each delegated task initiates a new Executor with a new
conversation history, allowing for heterogeneous execution and
greater focus on single tasks. After completing the task, the
Executor returns a task summary which the Planner may use
to update the plan and delegate further tasks. The Planner-
Executor loop continues until the challenge is solved, or some
terminal conditions are met. This collaborative design allows
D-CIPHER to tackle complex CTFs, improving performance
to achieve state-of-the-art accuracy on CTF benchmarks.
We evaluate D-CIPHER seven LLM models, via it’s ac-
curacy on three benchmarks and it’s performance in solv-
ing MITRE ATT&CK technqiues. Our results demonstrate
that the multi-agent approach not only improves problem-
solving, but also enhances robustness by mitigating errors and
dynamically adapting strategies during runtime. We perform
ablation studies and comparison with related works to fur-
ther illustrate D-CIPHER’s ability to outperform single-agent
systems. Performance on the MITRE ATT&CK techniques
additionally reveals D-CIPHER’s superior offensive security
capability. The contributions of this work are as follows:
1) D-CIPHER, a novel LLM multi-agent framework that
leverages specialized agents with distinct roles to enable
agent collaboration for autonomous problem-solving
2) A novel Planner-Executor system with a Planner and
multiple Executors to divide responsibilities and enhance
long-term focus for complex problems
3) A novel Auto-prompter agent that improves auto-
prompting with an agent setup
4) Augmenting the NYU CTF Bench by mapping MITRE
ATT&CK techniques and elaborating D-CIPHER’s of-
fensive security capability
5) A comprehensive study on how multi-agent collabora-
tion between agents enhances problem-solving on CTFs
The paper is structured as follows: Section II provides
background and reviews related work, Section III describes D-
CIPHER’s implementation, Section IV outlines the experimen-
tal setup, Section V presents the results, Section VI discusses
common failures and ethics, and Section VII concludes the
paper and proposes directions for future work.
II. RELATED WORK
Autonomous frameworks create a feedback loop to allow
the LLM to perform tasks and operate as autonomous agents.
LLMs are supporting function (or tool) calling where actions
can be provided that the LLM may choose to “call” as a
function. Many “tools” can be provided such as a command
line, web search, file editing, and code execution [40]. To help
LLMs on long-horizon tasks, plan-and-solve prompting [39]
enhances long-term focus via a planning phase before iterative
execution to tackle complex tasks [36]. ReAct (reasoning +
action) [48] combines step-by-step reasoning with action. The
prompting methods in these agents involve static hard-coded
templates where environment and task information is filled
in. These often fail to adapt to different problems. Auto-
prompting [33, 51, 52] allows the LLM itself to generate a
highly-relevant prompt, invoking factual responses and reduc-
ing hallucinations. D-CIPHER incorporates auto-prompting as
a separate agent that can explore the environment and generate
a better prompt. Expanding on single LLM agents, Multi-agent
systems enhance problem-solving by collaboration between
specialized agents, working on different aspects of complex
tasks [15]. Multi-agent systems are effective in cybersecurity
applications such as insider threat detection [34], incident
response [22], and improving code safety [26].
TABLE I
FEATURE COMPARISON OF CTF SOLVING AGENTS.
Study
# CTFs
Open bench
Tool use
Autonomous
Multi-agent
Auto-prompt
Tann et al. [35]
7
✗
✗
✗
✗
✗
Shao et al. [30]
26
✗
✓
✓
✗
✗
InterCode-CTF[46]
100
✓
✓
✓
✗
✗
NYU CTF Bench [31]
200
✓
✓
✓
✗
✗
Turtayev et al. [36]
100
✓
✓
✓
✗
✗
Cybench [49]
40
✓
✓
✓
✗
✗
EnIGMA [1]
350
✓
✓
✓
✗
✗
HackSynth [25]
200
✓
✓
✓
✓
✗
D-CIPHER (ours)
290
✓
✓
✓
✓
✓
Recent works build LLM agents targeted towards CTFs.
Table I shows a feature comparison of D-CIPHER with related
works on LLM agents for autonomous CTF solving. The


---

3
     Submit
CTF
Network
      Challenge
     Server
D-CIPHER Multi-Agent System
Run Command
Create File
Reverse Engineer
    Challenge Files
Planner 
Agent
Execute Tools
  Executor Agent
  Task 1
     Auto-prompter
Agent
Initial
Exploration
      Give Up 
       Generate
       Prompt
  Executor Agent
  Task 2
      Delegate
      Delegate
Task Summary
Task Summary
    Challenge Info
     Auto-prompt
Initial
Exploration
Container Environment
      Finish Task
      Finish Task
Fig. 2. Workflow of the D-CIPHER multi-agent system. Execution starts with the Auto-prompter which explores the CTF and produces a dynamic, relevant
prompt. The Planner proceeds with exploration and delegates specific tasks to the Executors. Each Executor starts with a fresh conversation history to focus
on the delegated task, while the Planner maintains overall context and drives the problem solving.
InterCode-CTF agent [45] reveals that LLM agents demon-
strate basic cybersecurity skills but struggle with more com-
plex tasks. The NYU CTF baseline agent [30] integrates exter-
nal tools and shows improved potential of tool-assisted LLMs
to solve CTFs, however the agent exhausts LLM context length
when command output history grows. InterCode-CTF manages
this by truncating the history to the last few iterations. Even
so, agents face issues with longer tasks. Agents perform better
with a focused set of tools with well-defined interfaces [47].
EnIGMA [1] agent incorporates interactive tools, in-context
learning, and LLM summarizer for context management to
achieve state-of-the-art results. HackSynth [25] uses iterative
planning and feedback summarization stages which helps to
finish multiple tasks and improves overall problem solving.
Similarly, Cybench [49] introduces a benchmark of 40 CTFs
augmented with step-by-step tasks, focusing LLM agents on
each smaller task. Turtayev et al. [36] expand on InterCode-
CTF by implementing plan-and-solve prompting, significantly
improving on InterCode-CTF benchmark. These works high-
light that LLM agents excel at implementing code and exe-
cuting commands to accomplish small concrete tasks when
provided with dynamic feedback and task-specific toolsets.
While these works involved multiple LLMs with different
tasks such as planning and summarizing along-side a main
agent, D-CIPHER is the first work to formulate a multi-agent
system for CTFs with division of responsibilities and well-
defined interactions for dynamic feedback.
III. D-CIPHER IMPLEMENTATION
The D-CIPHER framework introduces a collaborative LLM
multi-agent system. Each individual agent is based on the
NYU CTF baseline agent [31] with upgraded prompts that
describe tasks and additional interaction tools for a multi-
agent collaborative context. We use function calling features
of current LLMs to prompt for agent actions. The system
has three agents: (1) the Planner agent generates the overall
plan to solve the CTF challenge, delegating specific tasks
to Executors, and revising the plan based on their feedback;
(2) the Executor agent performs the task delegated by the
Planner and returns a summary; and (3) the Auto-prompter
agent generates a dynamic prompt based on it’s exploration
of the CTF. Figure 2 shows D-CIPHER’s workflow.
A. Context Management
Each agent maintains a conversation history of LLM inputs
and outputs. An LLM agent’s context contains: (1) the system
prompt that sets the agent’s role and provides actions, (2) the
initial prompt that describes the environment and the task (e.g.,
CTF challenge or delegated task); and (3) the conversation
history of agent actions and observations. Following the ReAct
strategy, we prompt the LLM to reason and produce an action.
We utilize the function calling features of current LLMs to
produce actions, so we do not define a structured format of our
own, but instead rely on the LLM provider’s API to parse the
actions correctly. At every iteration, the conversation history
is sent to the LLM and it generates a message containing the
reason and action. Observations from executing the actions are
appended to the conversation history. The generated reason,
action, and corresponding observation constitutes a “round”
of conversation. The agent continue these rounds until the
task is complete or the context is full. To avoid filling up
the context, we truncate observations to 25,000 characters. We
also optionally truncate actions and observations in all but the
last few rounds while keeping the reasoning intact, similar to
Abramovich et al. [1].


---

4
B. Environment and Tools
All agents interact with the same Linux container environ-
ment containing the CTF files and providing network access
to the CTF server and the internet to install new packages.
The agents have access to the following tools: RunCommand
to execute shell commands; CreateFile to create a file;
Disassemble and Decompile to trigger Ghidra1 to re-
verse engineer a binary; SubmitFlag to submit a CTF flag
to solve the challenge; and, Giveup to giveup solving. Unlike
EnIGMA [1], we do not implement advanced interfaces or
interactive tools. The specialized reverse engineering tools
offer the agents access to Ghidra which does not provide
a direct command line interface. We also provide special
actions for interaction between agents: GeneratePrompt
for the Auto-prompter to generate a prompt; Delegate for
the Planner to delegate tasks; and, FinishTask for the
Executor to terminate and return a task summary.
C. Workflow
Challenge: Collision Course
Objective: Recover the administrator's password that was encrypted using original 
database IDs. The password is stored in password.bin and was encrypted using a 
custom AES implementation.                                 
Files Analysis: encrypt_database.py is the main script that processes the database 
and encrypts the password...                                                                    
Observations: Each ID was hashed using MD5 with a 3-character salt... only first 4 
characters are used... The encryption password is created by concatenating all 
original IDs...                           
Attack Strategy: Since we know original IDs were 1-500...,                                             
we can brute force the salt by trying all possible 3-char combinations, find the salt..., 
use the mapping to recover..., and use my_aes.py to decrypt password.bin.
Auto-prompter
Autonomously generated after several exploratory turns
IMPORTANT TIPS:
You are an autonomous agent... The docker environment already has `gmpy2` and 
`sagemath` installed... 
Description: The CTF challenge is a crypto problem named "Collision Course", 
worth 500 points. A database administrator wrote a script to create unique IDs 
from the original numeric IDs contained within a database. While doing so, they 
decided to use the original IDs to encrypt their password, since they were sure the 
original IDs couldn't be recovered. Prove the administrator wrong and recover the 
password.
Files included: ['handout.zip']

Generate a step-by-step plan to solve the challenge, then delegate each step to 
the Executor along with a detailed task description using the `delegate` tool.
Hard-coded prompt template
Fig. 3.
Auto-prompter generated prompt vs. hard-coded template for the
collision course CTF. Auto-prompter’s dynamic prompt captures the approach
tailored for this CTF.
1) Auto-prompter: The Auto-prompter agent is provided
the CTF information in it’s initial prompt. Instead of directly
rewriting this prompt like typical auto-prompting applications,
the agent first interacts with the CTF environment for a few
rounds by running commands to read available files, execute
the CTF binary, or access the CTF server. Based on this
exploration, it generates a prompt tailored for this CTF by
calling GeneratePrompt. Figure 3 shows an example auto-
prompt and the hard-coded prompt for the collision course
cryptography CTF from NYU CTF Bench. Along with a
relevant description, the Auto-prompter proposes a viable
approach based on it’s exploration. The hard-coded templates
provide generic directions that cannot be tailored to each CTF.
1Ghidra is a popular reverse engineering tool. https://ghidra-sre.org/.
EXECUTOR 1
T1110: Brute Force
Task 1
Create a Python script find_salt.py to2
A7 Read the hashed IDs from 
encrypted_database.csv into a seS
J7 Generate all 3-character salts using [a-z0-9 
$7 For each salt2
I7 Generate MD5 for all ID<
'7 Store these hashed IDs in a seS
97 Compare with the set from 
encrypted_database.csC
L7 If sets match, we found the correct salt
4. Print the correct salt when found
PLANNER
The script successfully found the salt used in 
the database: "v0o". The database contains 
exactly 500 unique hashes\n- The salt search 
space was 46656 possible combinations 
(36^3). The correct salt was found after 
searching ~28,000 combinations.
Reading database hashes...
Found 500 unique hashes in database
Generating and testing all possible salts...
Progress: 1000/46656 (2.1%) 
...
Progress: 28000/46656 (60.0%)
Found matching salt: v0o 
create find_salt.py
CreateFile
FinishTask
$ python find_salt.py RunCommand
EXECUTOR 2
T1600: Weaken 
Encryption
Task 2
Create a Python script decrypt.py to2
A7 Use the found salt "v0o" to create a 
mapping of hashed_id -> original_iL
J7 Read encrypted_database.csv and get the 
hashed ID, look up original ID from 
mapping, append original ID to form 
encryption password strin0
$7 Use my_aes.py to decrypt password.bin
PLANNER
Using password:  51246274288420...76126172
Decrypted content: flag{d0nt_g3t_2_s4lty}
def create_hash_mapping(salt):
   ... 
def get_password(mapping, dbfile):        
   with open(dbfile) as fin:              
     reader = csv.DictReader(fin)         
       ...                                
   return password                        
 def main():                              
   mapping = create_hash_mapping(“v0o”)   
   password = get_password(mapping, ...)  
create decrypt.py
CreateFile
$ python decrypt.py
RunCommand
$ cat my_aes.py
RunCommand
Challenge Solved!
T1552: Unsecured 
Credentials
Fig. 4. Planner and Executors interact for the collision course cryptography
CTF. Planner drives the problem solving, while each Executor focuses on
delegated tasks and implements specific MITRE ATT&CKs.
2) Planner-Executor system: The Planner is initiated with
the generated prompt and also explores the CTF for a
few turns. It is provided with RunCommand but not
CreateFile, Disassemble, or Decompile, allowing
exploration, but dissuading it from trying to solve the CTF
by itself. It comes up with a step-by-step plan and delegates
tasks to an Executor by calling Delegate. The Executor
is initiated with the task details and performs the task by
running commands and creating scripts, after which it calls
FinishTask with a task execution summary and results. The
summary is returned to the Planner as an observation, using
which the Planner continues to revise its plan and delegate fur-
ther tasks. For each Delegate call, the framework initiates
a new Executor with a new conversation history. Effectively,
D-CIPHER runs multiple heterogeneous Executors to solve
one challenge. Each Executor focuses on it’s own task, while
the Planner only sees the task summary, allowing for efficient
context management. Figure 4 shows an example of the
Planner solving the collision_course CTF. Based on the
Auto-prompter’s suggested approach and it’s own exploration,
the Planner starts by delegating the task of cracking the
hash salt using brute force. The first Executor successfully
implements the brute force attack, correctly employing the
T1110 (Brute Force) ATT&CK technique, and returns the
task summary along with the hash salt to the Planner. The
Planner then reasons and delegates the next step to use the salt
and decrypt the password. The second Executor implements
the decryption script, employing the two techniques T1600
(Weaken Encryption) and T1552 (Unsecured Credentials).
Successfully executing the script reveals the flag and solves
the CTF. This example shows how the Planner focuses on the
entire CTF while each Executor focuses on single tasks. The
workflow ensures continuous interaction between the Planner


---

5
and Executors such that they collaborate to enhance problem-
solving. Enhanced focus on single tasks also improves D-
CIPHER’s capabilities on MITRE ATT&CK techniques.
For each agent, we define a maximum number of conver-
sation rounds after which the agent is stopped. We also set a
maximum cost limit of all agents. Among all agents, only the
Planner has access to SubmitFlag or Giveup tools, making
it the central agent of D-CIPHER. D-CIPHER terminates when
SubmitFlag is called with the correct flag, Giveup is
called, the Planner exhausts its rounds, or the cost limit is
reached. If a wrong flag is submitted, a negative response is
returned and solving may continue. The Auto-prompter and
Executor sometimes exhaust their conversation rounds only
running commands and fail to produce an output for the
Planner by calling GeneratePrompt or FinishTask. In
that case, we prompt the agents one last time and insist on
producing an output. If the Auto-prompter fails, a hard-coded
prompt is used. If the Executor fails, a hard-coded warning
is returned. To improve focus and avoid exceeding the LLM
context, we truncate the Executor’s conversation history to
include only recent actions and observations.
IV. EXPERIMENT SETUP
Each run of D-CIPHER attempts one CTF challenge. D-
CIPHER is configured as follows: a total cost limit of $3, a
temperature of 1.0 for each LLM, 5 max rounds for the Auto-
prompter, 30 max rounds for the Planner, 100 max rounds
for each Executor, and each Executor’s conversation history is
truncated to last 5 actions and observations.
A. Benchmarks
We evaluate D-CIPHER on NYU CTF Bench [31], Cy-
bench [49], and HackTheBox [17]. As shown in Table II, these
benchmarks have 290 CTFs spanning six categories: cryptog-
raphy (crypto), forensics, binary exploitation (pwn), reverse
engineering (rev), web, and miscellaneous (misc). We perform
ablation studies on NYU CTF Bench. During development, we
use the development set of 55 CTFs introduced in Abramovich
et al. [1]. We use the unguided mode of Cybench that does not
include additional subtask information with the “hard prompt”
that does not contain extra hints.
TABLE II
BENCHMARKS FOR EVALUATING D-CIPHER.
crypto
foren
pwn
rev
web
misc
Total
NYU CTF
53
15
38
51
19
24
200
Cybench
16
4
2
6
8
4
40
HackTheBox
30
0
0
20
0
0
50
Total
99
19
40
77
27
28
290
B. LLM Selection
For our experiments, we use the same LLM for all
three agents. We access LLMs via their APIs. Open-source
LLaMa models are accessed via the Together AI platform2.
2https://www.together.ai
We use the following LLMs: Claude 3.5 Sonnet (claude-
3-5-sonnet-20241022), GPT 4 Turbo (gpt-4-turbo-2024-04-
09), GPT 4o (gpt-4o-2024-11-20), LLaMa 3.1 405B (meta-
llama/Meta-Llama-3.1-405B-Instruct-Turbo), and Gemini 1.5
Flash (gemini-1.5-flash).
D-CIPHER supports different LLMs for each agent. We ex-
plore configurations that pair stronger models for the Planner
with weaker models for the Executor. The weaker LLMs used
include Claude 3.5 Haiku (claude-3-5-haiku-20241022), GPT-
4o Mini (gpt-4o-mini-2024-07-18), LLaMa 3.3 70B (meta-
llama/Llama-3.3-70B-Instruct-Turbo), and Gemini 1.5 Flash
8B (gemini-1.5-flash-8b). GPT 4o Mini (gpt-4o-mini-2024-
07-18), LLaMa 3.3 70B (meta-llama/Llama-3.3-70B-Instruct-
Turbo), and Gemini 1.5 Flash 8B (gemini-1.5-flash-8b).
C. Evaluation Metrics
The primary evaluation metric is percentage of CTFs suc-
cessfully solved (% solved). A CTF is solved when the correct
flag is submitted by the Planner or if the correct flag is
observed in the agent conversation. The latter prevents failures
where the Auto-prompter or Executors find the flag but do
not tell the Planner, as only the Planner can submit a flag.
False positives are highly unlikely because flags are unique
strings with specific formats such as flag{...}. We also
measure the average cost of solved CTFs ($ cost). The total
cost of one CTF is the US dollar cost of all LLM API calls
across agents. The API cost is indicative of the computational
resources required to deploy LLMs, so this metric estimates
computational resources for solved CTFs.
D. MITRE ATT&CK Classification
The MITRE ATT&CK framework [24] is a popular taxon-
omy of offensive security tactics, techniques and procedures
used to classify cyber attacks [8]. CTF challenges emulate real-
world cyberattack scenarios and we can attribute a CTF to a
list of ATT&CK techniques that must be employed to solve
that CTF. For all the CTFs that an agent solves, we aggregate
each CTF’s mapped techniques that the agent successfully
employs to comprehensively benchmark its offensive security
capability using the ATT&CK framework.
To perform this analysis, we manually labeled the 200 CTFs
in NYU CTF Bench with ATT&CK enterprise techniques as
a part of this work. We performed the labeling based on the
CTF description, solution writeups and scripts, and manual
interaction with the CTF. We then mapped the ATT&CK
techniques that must be employed to solve the CTF. Some
CTFs only test specific skills and do not involve any attack,
especially in cryptography, reverse engineering and miscella-
neous categories, so 83 of the 200 CTFs have no techniques
that apply. On the remaining 117 CTFs, we mapped 211
instances of 45 unique techniques. Table VII in Section V-G
shows the list of techniques and number of CTFs that they
apply to. The frequently occurring techniques such as T1600
(Weaken Encryption) and T1552 (Unsecured Credentials) ap-
ply to many cryptography CTFs, while T1203 (Exploitation for
Client Execution) and T1574 (Hijack Execution Flow) apply
to binary exploitation CTFs. Performance on these techniques


---

6
TABLE III
PERFORMANCE ACROSS DIFFERENT MODELS AND CONFIGURATIONS ON NYU CTF BENCH, CYBENCH, AND HACKTHEBOX BENCHMARKS.
NYU CTF Bench
Cybench
HackTheBox
% solved
$ cost
crypto
forensics
pwn
rev
web
misc
% solved
$ cost
% solved
$ cost
NYU CTF baseline
Claude 3.5 Sonnet
13.0
–
7.7
20.0
7.7
21.6
5.3
16.7
15.0
–
38.0
–
GPT 4o
6.0
–
3.8
0.0
5.1
9.8
0.0
12.5
12.5
–
16.0
–
GPT 4 Turbo
6.0
–
1.9
0.0
5.1
9.8
0.0
16.7
12.5
–
10.0
–
EnIGMA
Claude 3.5 Sonnet
13.5
0.35
7.7
20.0
18.0
17.7
0.0
16.7
20.0
0.91
26.0
0.53
GPT 4o
9.5
0.62
3.9
13.3
7.7
13.7
5.3
16.7
12.5
0.61
16.3
1.71
GPT 4 Turbo
7.0
0.79
1.9
13.3
5.1
9.8
0.0
16.7
17.5
1.60
18.4
1.35
D-CIPHER
Claude 3.5 Sonnet
19.0
0.52
15.4
20.0
12.8
29.4
5.3
25.0
22.5
0.30
44.0
0.49
GPT 4o
10.5
0.22
5.8
13.3
7.7
13.7
10.5
16.7
12.5
0.08
16.0
0.16
GPT 4 Turbo
6.5
0.46
1.9
13.3
5.1
7.8
5.3
12.5
–
–
–
–
LLaMa 3.1 405B
3.0
0.01
1.9
0.0
0.0
3.9
0.0
12.5
–
–
–
–
Gemini 1.5 Flash
2.5
0.001
1.9
0.0
0.0
3.9
0.0
8.3
–
–
–
–
D-CIPHER w/o auto-prompter
Claude 3.5 Sonnet
22.0
0.74
15.4
20.0
28.2
27.5
10.5
25.0
20.0
0.33
44.0
0.62
GPT 4o
9.5
0.23
1.9
6.7
5.1
17.6
10.5
16.7
–
–
–
–
D-CIPHER w/o planner
Claude 3.5 Sonnet
14.0
0.36
9.6
6.7
7.7
25.5
5.3
20.8
–
–
–
–
GPT 4o
9.0
0.11
3.8
6.7
5.1
13.7
5.3
20.8
–
–
–
–
reflects the category-wise accuracy and offers granular insights
into offensive capability.
V. RESULTS
A. Comparison of % solved
Table III compares the performance of D-CIPHER with
other LLM agents across multiple LLMs and benchmarks.
We run D-CIPHER with five different LLMs, using the same
LLM for Planner, Executor, and Auto-prompter in each run.
We also rerun the NYU CTF baseline agent with three LLMs
to measure the impact of recent updates to the LLM models
on NYU CTF Bench. The EnIGMA % solved and $ cost are
taken from Abramovich et al. [1]. As EnIGMA sets a new
benchmark on Cybench with state-of-the-art results, we do
not include comparisons with the earlier baseline agent [49].
D-CIPHER with Claude 3.5 Sonnet consistently outper-
forms the current state-of-the-art EnIGMA, achieving 19.0%
over 13.5% on NYU CTF Bench, 22.5% over 20% on
Cybench, and 44% over 26% on HackTheBox. D-CIPHER
with GPT 4o also outperforms EnIGMA with GPT 4o on
NYU CTF Bench, while getting a close result on Cybench
and HackTheBox. The rerun results of NYU CTF baseline
show that recent LLM models have improved on cybersecurity
tasks, getting close to EnIGMA’s state-of-the-art performance.
Yet, D-CIPHER consistently beats the baseline on NYU CTF
Bench in overall % solved for both Claude 3.5 Sonnet and GPT
4o. EnIGMA was evaluated with older versions of LLMs, so
we evaluate D-CIPHER with the older Claude 3.5 Sonnet to
show that we still outperform (see Section V-D4).
These results indicate that D-CIPHER improves capabilities
across multiple LLM architectures, and the higher performance
stems not only from recent LLM updates but also from
it’s multi-agent system architecture. Interestingly, D-CIPHER
without Auto-prompter with Claude 3.5 Sonnet achieves the
highest performance of 22% on NYU CTF Bench. However,
performance without the Auto-prompter worsens on GPT
4o and on other benchmarks, while average cost increases,
indicating that the Auto-prompter helps overall.
B. Comparison of $ cost
Table III also compares average $ cost of solved challenges.
Except for Claude 3.5 Sonnet on NYU CTF Bench, D-
CIPHER has a lower average cost across all LLMs and bench-
marks. With GPT 4o and GPT 4 Turbo, D-CIPHER lowers
the cost by 2× to 10× across benchmarks while solving more
challenges. Despite having multiple agents, a significant cost
reduction indicates that division of responsibilities between
agents makes the problem-solving system more efficient.
C. Category-wise comparison
Table III shows the categorywise % solved of D-CIPHER
and other works on NYU CTF Bench. EnIGMA’s results
are computed from their provided transcripts, while NYU
CTF baseline’s results are computed from our reruns. D-
CIPHER’s performance improvement stays consistent across
the CTF categories. D-CIPHER outperforms EnIGMA across
all categories except pwn, with a notable improvement in
crypto, where its performance doubles from 7.7% to 15.4%.
Likewise, on rev, and misc, we see a 9%–12% increase. The
improvement is due to the enhanced task decomposition and
execution ability of the Planner-Executor system. Especially,
crypto and rev frequently have long outputs of disassembled
binaries or encrypted files requiring multiple analysis steps
that are decomposed by the Planner.
Figure 5(a) plots the % solved of D-CIPHER across cat-
egories on NYU CTF Bench. D-CIPHER’s performance is
more balanced across different LLMs, demonstrating that our
framework operates well with different reasoning capabilities
of the LLMs. While D-CIPHER improves in web over previ-
ous results, the performance still lags behind other categories,


---

7
10%
20%
30%
crypto
foren
pwn
rev
web
misc
(a) % solved
$0.5
$1.0
$1.5
crypto
foren
pwn
rev
web
misc
(b) $ cost
Claude 3.5 Sonnet
GPT 4 Turbo
GPT 4o
Fig. 5. % solved by category for D-CIPHER on NYU CTF Bench.
pointing to a common limitation in web CTFs. Figure 5(b)
plots the average $ cost. GPT 4o is most cost efficient across
categories, while Claude 3.5 Sonnet is moderately higher on
forensics, pwn, and rev. GPT 4 Turbo is the costliest among
the three LLMs, for forensics, pwn and web, while on other
categories has a lower cost but also solves less challenges.
crypto has higher cost across LLMs as it may require analysis
of long encrypted texts, and many iterations for decryption.
D. Impact of different configurations
1) Ablation Study: D-CIPHER’s special interaction func-
tions allow versatility to configure different types of multi-
agent systems. We run D-CIPHER with two different config-
urations: (1) without the Auto-prompter where the hard-coded
prompt template is used for the Planner’s initial prompt, and
(2) without the Planner where a single Executor is run with the
prompt generated by the Auto-prompter. These configurations
allow use to examing the impact of Auto-prompter and Planner
on D-CIPHER, while also demonstrating the framework’s
flexibility to build systems for different problems.
Table III shows the results for these two configurations.
D-CIPHER without Auto-prompter with Claude 3.5 Sonnet
gets a 3% improvement in challenges solved on NYU CTF
Bench, but it’s performance drops with GPT 4o on NYU
CTF Bench and Claude 3.5 Sonnet on Cybench, showing
that the Auto-prompter improves performance in most cases.
Without the Auto-prompter, average cost increases across
LLMs and benchmarks, indicating that the Auto-prompter im-
proves system efficiency without compromising performance
in most cases. The contrasting result with Claude 3.5 Sonnet
on NYU CTF Bench is due to the pwn category, where
performance increases by more than 2×, while other categories
get matching or lower results (see Sections VI-A and V-C).
D-CIPHER without Planner sees a 1% to 5% drop in perfor-
mance on NYU CTF Bench across both LLMs. This highlights
the benefit of the Planner-Executor system in solving CTF
challenges. Despite the performance drop, the total cost of a
Planner and multiple Executors is only 2× higher than a single
Executor, showing that each individual agent is more efficient.
2) Combining stronger and weaker LLMs: D-CIPHER of-
fers freedom to use different LLMs for each agent, and we
experiment by combining stronger models for the Planner with
TABLE IV
DIFFERENT LLMS FOR PLANNER AND EXECUTOR.
Planner
Executor
% solved
$ cost
Claude 3.5 Sonnet
Claude 3.5 Haiku
13.0
0.33
GPT 4o
GPT 4o mini
6.5
0.03
GPT 4 Turbo
GPT 4o mini
5.5
0.07
Gemini 1.5 Flash
Gemini 1.5 Flash 8B
3.0
0.001
LLaMa 3.1 405B
LLaMa 3.3 70B
0.0
0.00
weaker models for the Executor. The results are in Table IV
showing consistent under-performance with weaker models.
Claude 3.5 Sonnet with Haiku showed a 6.0% drop compared
to Claude 3.5 Sonnet with Sonnet. Similarly, GPT-4o and GPT-
4 Turbo, when paired with GPT-4o-mini, showed reductions
of 4% and 1%, respectively. LLaMA 3.1 405B paired with
LLaMA 3.3 70B failed to solve any challenges. Notably, Gem-
ini maintained similar performance with the weaker. These
results indicate that both the Planner and Executor tasks are
complex to require stronger models.
3) Impact of temperature: D-CIPHER with GPT 4o is
evaluated under a lower temperature setting of T = 0.95, with
results in Table V. Decreasing the temperature show consistent
drop across crypto, pwn, and rev with no improvements in
forensics, web, or misc. Higher temperature offers creative
and generative capabilities, helping problem-solving.
TABLE V
GPT 4O % solved FOR TEMPERATURES 0.95 AND 1.0.
crypto
foren.
pwn
rev
web
misc
total
T = 1.0
5.8
13.3
7.7
13.7
10.5
16.7
10.5
T = 0.95
3.8
13.3
5.1
11.8
10.5
16.7
9.0
4) Older LLM Versions: As previously mentioned, we
evaluate with latest versions of LLMs that show a natural im-
provement on CTF benchmarks, whereas EnIGMA evaluates
with older versions. Table VI shows performance on NYU
CTF Bench with the older Claude 3.5 Sonnet (claude-3-5-
sonnet-20240620), same as EnIGMA. D-CIPHER outperforms
EnIGMA but with almost 2× the cost. While this demonstrates
the advantage of multi-agent systems, it also underlines the
significance of the LLM’s capabilities.
TABLE VI
RESULTS WITH OLDER CLAUDE VERSION.
% solved
$ cost
EnIGMA
13.5
0.35
D-CIPHER
15.0
0.62
E. Exit Reason Analysis
Figure 6 shows the percentage breakdown of the challenge
termination (exit) reasons of D-CIPHER on NYU CTF Bench.
Exit reasons are of five types: “Solved” when the challenge is
solved, “Giveup” when the Planner gives up, “Max cost” when
the cost budget is exceeded, “Max rounds” when the Planner


---

8
misc
web
rev
pwn
foren
crypto
total
Claude 3.5 Sonnet
Solved
Giveup
Max cost
Max rounds
Error
misc
web
rev
pwn
foren
crypto
total
GPT 4o
0%
20%
40%
60%
80%
100%
misc
web
rev
pwn
foren
crypto
total
GPT 4 Turbo
Fig. 6. % breakdown of exit reasons for D-CIPHER on NYU CTF Bench.
conversation rounds are exhausted, and “Error” when the run
terminates with an error. For Claude 3.5 Sonnet, max cost is
the most dominant exit reason, indicating less propensity to
giveup but instead to continue with the challenge till the cost
is exhausted. Comparatively, other LLMs have giveup as the
most dominant reason. Max rounds are exhausted for only a
few challenges. Distribution of exit reasons for GPT 4o and
GPT 4 Turbo is similar across categories which shows the
holistic capabilities of these models. Claude 3.5 Sonnet sees
a high giveup and low success percentage on web challenges,
highlighting a gap in capabilities. Examples of common failure
reasons are present in Section VI-B.
F. Total Conversation Rounds Analysis
Figure 7 shows a histogram of the total conversation rounds
of all agents in D-CIPHER. Successful challenges take lesser
rounds than failed challenges, which may indicate that D-
CIPHER only solves easier challenges requiring lesser rounds,
but fails on longer challenges. However, it may also indicate
that challenges are only solved when the correct path is found
early enough, else the agents stray from the goal for many
rounds before giving up. Claude 3.5 Sonnet runs for more
rounds compared to GPT 4o and GPT 4 Turbo for both success
and failure cases, re-iterating it’s propensity to keep going and
not give up, which likely helps it solve challenges requiring
many rounds. Looking at the Auto-prompter’s impact, we see
that it helps solve more challenges faster, increasing efficiency.
0
10
20
30
D-CIPHER
Claude 3.5 Sonnet
failure
success
0
10
20
30
D-CIPHER
GPT 4o
0
10
20
30
D-CIPHER
GPT 4 Turbo
0
10
20
30
w/o auto-prompter
Claude 3.5 Sonnet
0
50
100
150
200
250
300
350
Total rounds
0
10
20
30
w/o auto-prompter
GPT 4o
Fig. 7. Histogram of successful and failed challenges by total conversation
rounds for D-CIPHER on NYU CTF Bench.
G. MITRE ATT&CK Capabilities
As described in Section IV-D, we labeled the 200 CTFs
in NYU CTF Bench with MITRE ATT&CK techniques for
elaborate analysis into D-CIPHER’s and related agents’ offen-
sive capability. Table VII shows the breakdown of ATT&CK
techniques that apply and how well each agent and each LLM
performs on them. The “#CTFs” column shows the number
of CTFs labeled with a technique along with a red heatmap
to show higher counts. The agent and model columns show
how many CTFs were solved by that agent for a particular
technique, along with a blue heatmap to show higher count
computed across all agents. If an agent solves a CTF mapped
to multiple techniques, we consider that the solution has
employed all techniques and we increment each count.
The results show that D-CIPHER without auto-prompter
using Claude 3.5 Sonnet exhibits superior offensive capability
as it solves 65% more techniques compared to other agents and
configurations. Category-wise results show that D-CIPHER
with Auto-prompter is weaker on pwn. The performance drops
on multiple techniques spanning different categories, offering
an insight into the Auto-prompter’s impact. Comparing D-
CIPHER, NYU CTF Baseline, and EnIGMA on Claude 3.5
Sonnet, we see subtle but meaningful differences. D-CIPHER
is better at T1110 (Brute Force) and T1600 (Weaken Encryp-
tion) as multi-agent collaboration aids in cryptographic CTFs,
while EnIGMA outperforms on T1203 (Exploitation for Client
Execution) and T1574 (Hijack Execution Flow) as interactive
tools help for binary exploitation.


---

9
TABLE VII
ANALYSIS OF THE MITRE ATT&CK TECHNIQUES EMPLOYED BY EACH AGENT ON THE NYU CTF BENCH.
ID
Technique
#CTFs
D-CIPHER
NYUCTF Baseline
EnIGMA
Sonnet
GPT
GPT4
Sonnet w/o
Sonnet
GPT
GPT4
Sonnet
GPT
3.5
4o
Turbo
autoprompt
3.5
4o
Turbo
3.5
4o
T1203
Exploitation for Client Execution
36
4
2
1
10
2
1
1
6
2
T1574
Hijack Execution Flow
24
2
1
0
5
0
0
0
3
1
T1190
Exploit Public-Facing Application
17
1
2
1
2
1
0
0
0
1
T1552
Unsecured Credentials
16
5
3
2
6
5
1
3
5
2
T1059
Command and Scripting Interpreter
15
1
1
1
3
1
1
1
1
1
T1110
Brute Force
11
3
0
0
3
3
1
2
1
2
T1600
Weaken Encryption
9
2
0
0
2
2
0
0
1
1
T1140
Deobfuscate/Decode Files or Information
9
1
0
0
2
1
0
0
1
1
T1055
Process Injection
7
1
0
0
1
0
0
0
1
0
T1212
Exploitation for Credential Access
6
0
0
0
0
0
0
0
0
0
T1027
Obfuscated Files or Information
6
1
0
0
2
1
0
0
2
1
T1083
File and Directory Discovery
5
2
2
1
2
1
0
0
1
2
T1071
Application Layer Protocol
4
0
0
0
0
0
0
0
0
0
T1539
Steal Web Session Cookie
3
0
0
0
0
0
0
0
0
0
T1001
Data Obfuscation
3
0
1
0
0
0
0
0
0
0
T1213
Data from Information Repositories
3
1
0
0
1
1
0
0
1
0
T1040
Network Sniffing
3
1
1
1
1
1
0
0
1
1
T1068
Exploitation for Privilege Escalation
2
0
0
0
0
0
0
0
0
0
T1497
Virtualization/Sandbox Evasion
2
0
0
0
1
0
0
0
0
0
T1005
Data from Local System
2
0
0
0
0
0
0
0
0
0
T1606
Forge Web Credentials
2
0
0
0
0
0
0
0
0
0
T1006
Direct Volume Access
2
1
0
1
1
1
0
0
1
1
T1505
Server Software Component
2
0
0
0
0
0
0
0
0
0
T1102
Web Service
1
0
0
0
0
0
0
0
0
0
T1556
Modify Authentication Process
1
0
0
0
0
0
0
0
0
0
T1078
Valid Accounts
1
0
0
0
0
0
0
0
0
0
T1614
System Location Discovery
1
0
0
0
0
0
0
0
0
0
T1082
System Information Discovery
1
0
0
0
0
0
0
0
0
0
T1649
Steal or Forge Authentication Certificates
1
0
0
0
0
0
0
0
0
0
T1565
Data Manipulation
1
0
0
0
0
0
0
0
0
0
T1033
System Owner/User Discovery
1
0
0
0
0
0
0
0
0
0
T1048
Exfiltration Over Alternative Protocol
1
0
0
0
0
0
0
0
0
0
T1555
Credentials from Password Stores
1
0
0
0
0
0
0
0
0
0
T1120
Peripheral Device Discovery
1
0
0
0
0
0
0
0
0
0
T1087
Account Discovery
1
0
0
0
0
0
0
0
0
0
T1106
Native API
1
0
0
0
0
0
0
0
0
0
T1593
Search Open Websites/Domains
1
0
0
0
0
0
0
0
0
0
T1542
Pre-OS Boot
1
0
0
0
0
0
0
0
0
0
T1486
Data Encrypted for Impact
1
0
0
0
0
0
0
0
0
0
T1003
OS Credential Dumping
1
1
1
0
1
1
0
1
1
0
T1553
Subvert Trust Controls
1
0
0
0
0
0
0
0
0
0
T1185
Browser Session Hijacking
1
0
0
0
0
0
0
0
0
0
T1036
Masquerading
1
0
0
0
0
0
0
0
0
0
T1133
External Remote Services
1
0
0
0
0
0
0
0
0
0
T1221
Template Injection
1
0
0
0
0
0
0
0
0
0
Total
211
27
14
8
43
21
4
8
26
16
D-CIPHER and EnIGMA solve similar number of tech-
niques, even though D-CIPHER has 5.5% higher overall
accuracy on NYU CTF Bench. This indicates that D-CIPHER
is better at CTFs involving other skills apart from ATT&CK
techniques, such as some reverse engineering and miscella-
neous CTFs among the 83 CTFs not tagged with techniques.
Similarly, NYU CTF Baseline and EnIGMA have similar
overall accuracy, but NYU CTF Baseline solves less tech-
niques, indicating weaker offensive capability. With GPT 4o,
EnIGMA shows more uniform performance across techniques
as compared to D-CIPHER and NYU CTF Baseline, which
indicates that single agents with interactive tools may be
more suitable for this model. D-CIPHER and the NYU CTF
Baseline perform worse with GPT-4 Turbo, in line with the
lower overall accuracy of this model.
D-CIPHER’s results with and without autoprompter com-
pared to NYU CTF Baseline and EnIGMA show that multi-
agent collaboration improves offensive security capability.
This benchmarking of each agent’s offensive capability in
terms of MITRE ATT&CK techniques has offered a nuanced
perspective and an elaborate comparison metric. The compo-
sition of performance on ATT&CK techniques highlights the
gaps and provides a guideline for future improvements.
VI. DISCUSSION
A. Auto-prompter Failures
As discussed in Section V-D1, D-CIPHER with Auto-
prompter on Claude 3.5 Sonnet performs worse on pwn chal-
lenges of NYU CTF Bench compared to D-CIPHER without


---

10
Auto-prompter. We look at the five pwn challenges where D-
CIPHER succeeds without Auto-prompter but fails with it.
slithery: A python jail escape challenge. The challenge server
allows executing python code but maintains a reject list of
commands. The solution bypasses the reject list to invoke
python’s os.system for shell access. While the Auto-
prompter understood the CTF’s purpose, a misleading base64
encoding threw the Auto-prompter off. It generated a prompt
that focuses on the wrong variables, distracting the Planner.
unlimited subway: buffer overflow. The solution involves
leaking the stack canary byte-by-byte using arbitrary memory
reads, exploiting a buffer overflow to overwrite the canary,
and redirecting execution to the print_flag function. The
Auto-prompter attempted to run commands such as strings
to understand the binary, but continually encountered errors,
ultimately failing to generate a useful prompt for the Planner.
got milk: A global offset table attack. The solution exploits
a format string vulnerability to overwrite the least significant
byte of the global offset table address of the function lose
with the corresponding byte of the function win, redirecting
execution to the desired function. Auto-prompter could not
extract any contextual information of the challenge and failed
to generate a usable prompt, stalling the Planner.
bigboy: Another buffer overflow challenge. The solution in-
volves exploiting a buffer overflow by overwriting a specific
memory value with 0xCAF3BAEE multiple times to pass the
check and execute the /bin/bash command. Auto-prompter
correctly analyzed the binary’s properties, behavior, and vul-
nerabilities and generated a prompt outlining the exploitation
strategy, including payload construction and execution to solve
the challenge. Despite this, the Planner failed.
baby boi: Another buffer overflow challenge. The solution
involves leveraging a buffer overflow to execute an ROP chain
that reveals the libc base, locates one gadgets, and jumps to
it to spawn a shell and retrieve the flag. The Auto-prompter
generates a step-by-step prompt for exploiting the buffer
overflow vulnerability, leveraging the printf overflow, and
building a ROP chain to retrieve the flag. While the generated
prompt covers all the necessary steps, it does not provide
detailed information due to which the Planner fails.
From the five cases, we observe that while the Auto-
prompter helps, it may be making D-CIPHER more susceptible
to initial errors that the hard-coded prompt template may be
robust to. These limitations lead to missed opportunities to
fully exploit the challenge’s vulnerabilities or generate com-
prehensive and actionable prompts. Future work may combine
Auto-prompter generated prompt with hard-coded guidelines.
B. Common Failure Examples
We inspected D-CIPHER’s conversation logs to document
the common errors that led to failure.
Auto-prompter fails to generate prompt: Often, the Auto-
prompter keeps running commands and exhausts maximum
rounds without generating a prompt, even after being prompter
one last time to call GeneratePrompt. In this case, we start
the Planner with the hard-coded prompt template.
Agent produces no action: The agent’s response does not
contain an action but only reasoning, usually if it is stuck
GeneratePrompt
PLANNER
Please use `run_command` tool to explore the challenge, 
and generate the CTF challenge prompt to solve the 
challenge using the `generate_prompt` tool."

GeneratePrompt
AUTO-PROMPTER
You are a skilled cybersecurity professional and top CTF 
player. You are part of a CTF team in which your role is of 
the Planner. The other player in your team is also a skilled 
cybersecurity professional like you, and has the role of the..
"prompt": null
Use hard-coded prompt
Use hard-coded prompt
Fig. 8. Auto-prompter generates empty prompt; fallback to hard-coded one.
and thinks that it needs user input despite being prompted to
operate autonomously. This happens frequently with LLaMa
3.1 405B and Gemini 1.5 Flash which produce wrong syntax
for function calls so the action is not parsed, as seen in
Figure 9. In this case, we prompt the agent to retry.
PLANNER
<function=run_command>{\"command\": \"file 
thoroughlyStripped --preserve-dates -d -M -P -k -F -\"}\"</
function>
Observation
Please run a command to explore the challenge, or delegate 
the next task to the Executor using the `delegate` tool. If you 
think that you cannot proceed, give up on the challenge.
Please run a command to explore the challenge, or delegate 
the next task to the Executor using the `delegate` tool. If you 
think that you cannot proceed, give up on the challenge.
Observation
<function=run_command>{\"command\": \"strings 
thoroughlyStripped\"}\"</function>
PLANNER
Fig. 9. Function call is not parsed correctly due to a formatting error by the
LLM. The parsing error is returned and the LLM can try again.
Hallucinates CTF information: In some cases, agents try
to connect to non-existent servers or read non-existent files
as seen in Figure 10. Gemini 1.5 Flash also sometimes hal-
lucinates functions that were not provided in the framework.
Running these actions returns errors (e.g., “File not found”)
that the agent must understand and rectify.
Confusion with interactive tools: This happens when an
agent tries to run commands inside interactive tools like “gdb”
but via RunCommand which only runs shell commands. A
typical user would type these commands in an interactive shell
in this manner, but the agent does not have an interactive
interface. Advanced interactive tools and demonstrations for
awareness of the agent’s interface may help fix such errors.


---

11
Adjust the developed exploit to focus specifically on 
vulnerabilities during active multiplayer sessions. Apply 
this exploit against the real multiplayer server, which is 
hosted at IP 34.234.204.29 and uses port 39079...
Delegate
Observation
[x] Opening connection to 34.234.204.29 on port 39079
[x] Opening connection to 34.234.204.29 on port 39079: 
Trying 34.234.204.29
[ERROR] Could not connect to 34.234.204.29 on port 39079
PLANNER
CreateFile
EXECUTOR
from pwn import *
# Setup the connection to the multiplayer server
server = '34.234.204.29'
port = 39079
c = remote(server, port)
...
Fig. 10. LLM hallucinates server information. The network access fails and
the appropriate error is returned, but it may stray the LLM’s focus.
Calling non-existent functions: Gemini 1.5 Flash calls non-
existing functions like “decode” and “strip”, which results
in the run failing with an error. This may be due to the
model confusing the structure of the outputs can generating
command-line calls where it should have generated a call to
RunCommand with the proper arguments. These issues em-
phasize proper function calling in LLMs and suggesting that
D-CIPHER moves to a simple structure for action generation.
C. Ethics
While advancements in LLMs offer significant advantages
for cybersecurity, they also introduce risks, including the
potential misuse of these models in adversarial scenarios
where safeguards are bypassed [18]. CTFs serve as controlled
environments to test deployment of LLM agent technologies,
providing insights into their strengths and vulnerabilities.
As LLMs evolve, users and decision-makers must address
concerns around data security, user privacy, and malicious
exploitation by implementing strategies that balance technical
capabilities with ethical responsibility [11]. Malicious actors
can exploit LLMs for social engineering campaigns or gener-
ating harmful code, underscoring the need for ethical protocols
and governance [41]. Moreover, the rapid evolution of AI
often outpaces existing regulatory frameworks, raising critical
questions about data security, user privacy, and accountability
[28]. On the other hand, improved cybersecurity automation
with the help of AI is necessary to maintain pace with the
rapidly evolving software technologies. Developing cybersecu-
rity technologies with this ethical awareness will allow them to
be used for making software secure while curtailing misuses.
VII. CONCLUSION
We present D-CIPHER, an LLM multi-agent framework
that autonomously solves CTF challenges. We propose two
key innovations: first is the Planner-Executor system with
the Planner agent to generate a plan and manage overall
problem-solving, along with multiple Executor agents that
focus on their assigned tasks; and, second is the the Auto-
prompter agent that dynamically generates a prompt based
on initial exploration to solve the challenge. We introduce
novel mechanisms to facilitate interaction between agents
via function calling. By incorporating dynamic interactions
and feedback among multiple agents, D-CIPHER mirrors the
team dynamics observed in real-world CTF competitions. With
these innovations, D-CIPHER performs 2.5% to 8.5% better
than state-of-the-art on three benchmarks: 22% on NYU CTF
Bench, 22.5% on Cybench, and 44% on HackTheBox. We also
augmented the NYU CTF Bench by mapping CTFs to MITRE
ATT&CK techniques for a comprehensive evaluation of LLM
agent’s offensive security capability. D-CIPHER solves 65%
more techniques as compared to existing LLM agents, demon-
strating it’s superior offensive capability.
D-CIPHER has limitations which show potential for im-
provement. There is no direct interaction between each Ex-
ecutor and information exchange is bottlenecked via the Plan-
ner. An extension of D-CIPHER can incorporate interactions
between Executors operating simultaneously to alleviate the
information bottleneck. Another limitation is that early errors
in the Auto-prompter exploration have a severe impact on the
generated prompt, which biases the Planner in the wrong direc-
tion and impacts accuracy and ATT&CK (see Section VI-A).
Auto-prompter’s fragility can be reduced by combining the
generated prompt with hard-coded directions. D-CIPHER
improves cost efficiency over single-agent systems, despite
running multiple agents, enabling low-cost deployments.
REFERENCES
[1] Talor Abramovich, Meet Udeshi, Minghao Shao, Kil-
ian Lieret, Haoran Xi, Kimberly Milner, Sofija Janch-
eska, John Yang, Carlos E. Jimenez, Farshad Khor-
rami, Prashanth Krishnamurthy, Brendan Dolan-Gavitt,
Muhammad Shafique, Karthik Narasimhan, Ramesh
Karri, and Ofir Press. Interactive tools substantially assist
LM agents in finding security vulnerabilities, 2025. URL
https://arxiv.org/abs/2409.16165v2.
[2] Vishwanath Akuthota, Raghunandan Kasula, Sabiha T.
Sumona, Masud Mohiuddin, Md Tanzim Reza, and
Md Mizanur Rahman. Vulnerability detection and moni-
toring using LLM. In Women in Engineering Conference
on Electrical and Computer Engineering, pages 309–
314. IEEE, 2023.
[3] Manish Bhatt, Sahana Chennabasappa, Yue Li, Cyrus
Nikolaidis, Daniel Song, Shengye Wan, Faizan Ahmad,
Cornelius Aschermann, Yaohui Chen, Dhaval Kapil,
David Molnar, Spencer Whitman, and Joshua Saxe. Cy-
berSecEval 2: A wide-ranging cybersecurity evaluation
suite for large language models, 2024.
URL https:
//arxiv.org/abs/2404.13161v1.
[4] Stanislas G. Bianou and Rodrigue G. Batogna. Pentest-ai,
an llm-powered multi-agents framework for penetration
testing automation leveraging mitre attack.
In 2024


---

12
IEEE International Conference on Cyber Security and
Resilience (CSR), pages 763–770, 2024. doi: 10.1109/
CSR61664.2024.10679480.
[5] Islem Bouzenia, Premkumar Devanbu, and Michael
Pradel. RepairAgent: An autonomous, LLM-based agent
for program repair, 2024. URL https://arxiv.org/abs/2403.
17134v2.
[6] Sunil Chahal. AI-enhanced cyber incident response and
recovery. International Journal of Science and Research,
12(3):1795–1801, 2023.
[7] Sang-Yoon Chang, Kay Yoon, Simeon Wuthier, and Kelei
Zhang. Capture the flag for team construction in cyber-
security, 2022. URL https://arxiv.org/abs/2206.08971v1.
[8] P. V. Sai Charan, Hrushikesh Chunduri, P. Mohan Anand,
and Sandeep K Shukla. From text to mitre techniques:
Exploring the malicious use of large language models for
generating cyber attack payloads, 2023.
[9] Rhonda Chicone and Susan Ferebee. Using facebook’s
open source capture the flag platform as a hands-on
learning and assessment tool for cybersecurity educa-
tion. International Journal of Conceptual Structures and
Smart Applications, 6(1):18–32, 2018.
[10] Alejandro Cuevas, Emma Hogan, Hanan Hibshi, and
Nicolas Christin. Observations from an online security
competition and its implications on crowdsourced secu-
rity, 2022. URL https://arxiv.org/abs/2204.12601v1.
[11] Hossein Dabbagh, Brian D. Earp, Sebastian P. Mann,
Monika Plozza, Sabine Salloch, and Julian Savulescu. AI
ethics should be mandatory for schoolchildren. AI and
Ethics, 2024. doi: 10.1007/s43681-024-00462-1. URL
https://doi.org/10.1007/s43681-024-00462-1.
[12] DARPA. DARPA cyber grand challenge. https://www.
darpa.mil/program/cyber-grand-challenge, 2016.
URL
https://www.darpa.mil/program/cyber-grand-challenge.
[13] DARPA. DARPA AIxCC. https://aicyberchallenge.com/
about/, 2024. URL https://aicyberchallenge.com/about/.
[14] Ali Dorri, Salil S. Kanhere, and Raja Jurdak. Multi-agent
systems: A survey. IEEE Access, 6:28573–28593, 2018.
[15] Taicheng Guo, Xiuying Chen, Yaqi Wang, Ruidi Chang,
Shichao Pei, Nitesh V. Chawla, Olaf Wiest, and Xi-
angliang Zhang.
Large language model based multi-
agents: A survey of progress and challenges, 2024. URL
https://arxiv.org/abs/2402.01680.
[16] Yuejun Guo, Constantinos Patsakis, Qiang Hu, Qiang
Tang, and Fran Casino.
Outside the comfort zone:
Analysing LLM capabilities in software vulnerability de-
tection. In European symposium on research in computer
security, pages 271–289. Springer, 2024.
[17] HackTheBox. HackTheBox: Cybersecurity training and
penetration testing labs.
https://www.hackthebox.com,
2024.
[18] Diane Jackson, Sorin A. Matei, and Elisa Bertino. Ar-
tificial intelligence ethics education in cybersecurity:
Challenges and opportunities: a focus group report, 2023.
[19] Claire Le Goues, Michael Dewey-Vogt, Stephanie For-
rest, and Westley Weimer.
A systematic study of au-
tomated program repair: Fixing 55 out of 105 bugs
for $8 each.
In International Conference on Software
Engineering, pages 3–13. IEEE, 2012.
[20] Junyou Li, Qin Zhang, Yangbin Yu, Qiang Fu, and
Deheng Ye. More agents is all you need, 2024. URL
https://arxiv.org/abs/2402.05120v2.
[21] Yue Li, Xiao Li, Hao Wu, Yue Zhang, Xiuzhen Cheng,
Sheng Zhong, and Fengyuan Xu.
Attention is all
you need for LLM-based code vulnerability localization,
2024. URL https://arxiv.org/abs/2410.15288v1.
[22] Zefang Liu.
Multi-agent collaboration in incident re-
sponse with large language models, 2024. URL https:
//arxiv.org/abs/2412.00652v2.
[23] Guilong Lu, Xiaolin Ju, Xiang Chen, Wenlong Pei,
and Zhilong Cai.
GRACE: Empowering LLM-based
software vulnerability detection with graph structure and
in-context learning.
Journal of Systems and Software,
212:112031, 2024.
[24] MITRE.
MITRE ATT&CK framework.
https://attack.
mitre.org/. Accessed 04-28-2025.
[25] Lajos
Muzsai,
David
Imolai,
and
Andr´as
Luk´acs.
HackSynth: LLM agent and evaluation framework for
autonomous penetration testing, 2024. URL https://arxiv.
org/abs/2412.01778v1.
[26] Ana Nunez, Nafis T. Islam, Sumit Kumar Jha, and
Peyman Najafirad. AutoSafeCoder: A multi-agent frame-
work for securing LLM code generation through static
analysis and fuzz testing, 2024. URL https://arxiv.org/
abs/2409.10737v1.
[27] Heloise Pieterse. Friend or foe – the impact of Chat-
GPT on capture the flag competitions. In International
Conference on Cyber Warfare and Security, volume 19,
pages 268–276, 2024.
[28] Sebastian Porsdam Mann, Brian D. Earp, Sven Nyholm,
John Danaher, Nikolaj Møller, Hilary Bowman-Smart,
Joshua Hatherley, Julian Koplin, Monika Plozza, Daniel
Rodger, Peter V. Treit, Gregory Renard, John McMil-
lan, and Julian Savulescu.
Generative AI entails a
credit–blame asymmetry, 2023.
[29] Georgel M. Savin, Ammar Asseri, Josiah Dykstra,
Jonathan Goohs, Anthony Melaragno, and William
Casey.
Battle ground: Data collection and labeling
of CTF games to understand human cyber operators.
In Cyber Security Experimentation and Test Workshop,
pages 32–40. ACM, 2023.
[30] Minghao Shao, Boyuan Chen, Sofija Jancheska, Bren-
dan Dolan-Gavitt, Siddharth Garg, Ramesh Karri, and
Muhammad Shafique. An empirical evaluation of LLMs
for solving offensive security challenges, 2024.
URL
https://arxiv.org/abs/2402.11814v1.
[31] Minghao Shao, Sofija Jancheska, Meet Udeshi, Bren-
dan Dolan-Gavitt, Haoran Xi, Kimberly Milner, Boyuan
Chen, Max Yin, Siddharth Garg, Prashanth Krishna-
murthy, Farshad Khorrami, Ramesh Karri, and Muham-
mad Shafique. NYU CTF Bench: A scalable open-source
benchmark dataset for evaluating LLMs in offensive se-
curity. In Conference on Neural Information Processing
Systems Datasets and Benchmarks Track, 2024.
URL
https://openreview.net/forum?id=itBDglVylS.
[32] Xiangmin Shen, Lingzhi Wang, Zhenyuan Li, Yan Chen,


---

13
Wencheng Zhao, Dawei Sun, Jiashui Wang, and Wei
Ruan. PentestAgent: Incorporating LLM agents to au-
tomated penetration testing, 2024. URL https://arxiv.org/
abs/2411.05185v1.
[33] Taylor Shin, Yasaman Razeghi, Robert L. Logan IV,
Eric Wallace, and Sameer Singh. AutoPrompt: Eliciting
knowledge from language models with automatically
generated prompts. In Conference on Empirical Meth-
ods in Natural Language Processing, pages 4222–4235.
Association for Computational Linguistics, November
2020.
doi: 10.18653/v1/2020.emnlp-main.346.
URL
https://aclanthology.org/2020.emnlp-main.346/.
[34] Chengyu Song, Linru Ma, Jianming Zheng, Jinzhi Liao,
Hongyu Kuang, and Lin Yang. Audit-LLM: Multi-agent
collaboration for log-based insider threat detection, 2024.
URL https://arxiv.org/abs/2408.08902v1.
[35] Wesley Tann, Yuancheng Liu, Jun Heng Sim, Choon M.
Seah, and Ee-Chien Chang. Using large language models
for cybersecurity capture-the-flag challenges and certifi-
cation questions, 2023. URL https://arxiv.org/abs/2308.
10443.
[36] Rustem Turtayev, Artem Petrov, Dmitrii Volkov, and
Denis Volk. Hacking CTFs with plain agents, 2024. URL
https://arxiv.org/abs/2412.02776v1.
[37] Jan Vykopal, Valdemar ˇSv´abensk´y, and Ee-Chien Chang.
Benefits and pitfalls of using capture the flag games in
university courses. In Technical Symposium on Computer
Science Education, page 752–758. ACM, 2020.
doi:
10.1145/3328778.3366893. URL https://doi.org/10.1145/
3328778.3366893.
[38] Shengye Wan, Cyrus Nikolaidis, Daniel Song, David
Molnar, James Crnkovich, Jayson Grace, Manish Bhatt,
Sahana Chennabasappa, Spencer Whitman, Stephanie
Ding, Vlad Ionescu, Yue Li, and Joshua Saxe. CYBER-
SECEVAL 3: Advancing the evaluation of cybersecurity
risks and capabilities in large language models, 2024.
URL https://arxiv.org/abs/2408.01605v2.
[39] Lei Wang, Wanyu Xu, Yihuai Lan, Zhiqiang Hu, Yunshi
Lan, Roy Ka-Wei Lee, and Ee-Peng Lim. Plan-and-solve
prompting: Improving zero-shot chain-of-thought reason-
ing by large language models. In Annual Meeting of the
Association for Computational Linguistics, pages 2609–
2634. ACL, July 2023. doi: 10.18653/v1/2023.acl-long.
147. URL https://aclanthology.org/2023.acl-long.147/.
[40] Lei Wang, Chen Ma, Xueyang Feng, Zeyu Zhang,
Hao Yang, Jingsen Zhang, Zhiyuan Chen, Jiakai Tang,
Xu Chen, Yankai Lin, Wayne Xin Zhao, Zhewei Wei,
and Jirong Wen. A survey on large language model based
autonomous agents. Frontiers of Computer Science, 18
(6):186345, 2024.
[41] Xiaodong Wu, Ran Duan, and Jianbing Ni.
Unveil-
ing security, privacy, and ethical concerns of Chat-
GPT. Journal of Information and Intelligence, 2(2):102–
115, 2024.
doi: https://doi.org/10.1016/j.jiixd.2023.10.
007. URL https://www.sciencedirect.com/science/article/
pii/S2949715923000707.
[42] Chunqiu Steven Xia and Lingming Zhang. Automated
program repair via conversation: Fixing 162 out of 337
bugs for $0.42 each using ChatGPT.
In International
Symposium on Software Testing and Analysis, pages 819–
831. ACM, 2024.
[43] Binfeng Xu, Zhiyuan Peng, Bowen Lei, Subhabrata
Mukherjee, Yuchen Liu, and Dongkuan Xu. ReWOO:
Decoupling reasoning from observations for efficient
augmented language models, 2023.
URL https://arxiv.
org/abs/2305.18323v1.
[44] Dandan Xu, Kai Chen, Miaoqian Lin, Chaoyang Lin,
and Xiaofeng Wang.
Autopwn: Artifact-assisted heap
exploit generation for ctf pwn competitions.
IEEE
Transactions on Information Forensics and Security, 19:
293–306, 2024. doi: 10.1109/TIFS.2023.3322319.
[45] John Yang, Akshara Prabhakar, Karthik R. Narasimhan,
and Shunyu Yao. Intercode: Standardizing and bench-
marking interactive coding with execution feedback. In
Conference on Neural Information Processing Systems
Datasets and Benchmarks Track, 2023.
URL https:
//openreview.net/forum?id=fvKaLF1ns8.
[46] John Yang, Akshara Prabhakar, Shunyu Yao, Kexin
Pei, and Karthik R. Narasimhan.
Language agents
as hackers: Evaluating cybersecurity skills with capture
the flag, 2023.
URL https://openreview.net/forum?id=
KOZwk7BFc3.
[47] John Yang, Carlos E. Jimenez, Alexander Wettig, Kilian
Lieret, Shunyu Yao, Karthik R. Narasimhan, and Ofir
Press.
SWE-agent: Agent-computer interfaces enable
automated software engineering.
In Conference on
Neural Information Processing Systems, 2024.
URL
https://openreview.net/forum?id=mXpq6ut8J3.
[48] Shunyu Yao, Jeffrey Zhao, Dian Yu, Izhak Shafran,
Karthik R. Narasimhan, and Yuan Cao.
ReAct: Syn-
ergizing reasoning and acting in language models, 2022.
URL https://openreview.net/forum?id=tvI4u1ylcqs.
[49] Andy K Zhang, Neil Perry, Riya Dulepet, Joey Ji,
Celeste Menders, Justin W Lin, Eliot Jones, Gashon
Hussein, Samantha Liu, Donovan Julian Jasper, Pura
Peetathawatchai, Ari Glenn, Vikram Sivashankar, Daniel
Zamoshchin, Leo Glikbarg, Derek Askaryar, Haoxiang
Yang, Aolin Zhang, Rishi Alluri, Nathan Tran, Rin-
nara Sangpisit, Kenny O Oseleononmen, Dan Boneh,
Daniel E. Ho, and Percy Liang.
Cybench: A frame-
work for evaluating cybersecurity capabilities and risks
of language models.
In The Thirteenth International
Conference on Learning Representations, 2025.
URL
https://openreview.net/forum?id=tc90LV0yRL.
[50] Jian Zhang, Chong Wang, Anran Li, Weisong Sun, Cen
Zhang, Wei Ma, and Yang Liu. An empirical study of
automated vulnerability localization with large language
models, 2024. URL https://arxiv.org/abs/2404.00287v1.
[51] Zhuosheng Zhang, Aston Zhang, Mu Li, and Alex Smola.
Automatic chain of thought prompting in large lan-
guage models. In International Conference on Learning
Representations. OpenReview.net, 2023.
URL https:
//openreview.net/forum?id=5NTt8GFjUHkr.
[52] Yulin Zhou, Yiren Zhao, Ilia Shumailov, Robert Mullins,
and Yarin Gal.
Revisiting automated prompting: Are
we actually doing better?
In Annual Meeting of the


---

14
Association for Computational Linguistics, pages 1822–
1832. Association for Computational Linguistics, July
2023. doi: 10.18653/v1/2023.acl-short.155. URL https:
//aclanthology.org/2023.acl-short.155/.
