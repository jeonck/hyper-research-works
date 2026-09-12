---
title: 'ARENA: An Architecture for Measuring the'
id: arena-an-architecture-for-measuring-the
tags:
- attack-ontology-drift-cti-85bc51
- pin-rate-survey
created: '2026-09-12T21:32:51.145135Z'
updated: '2026-09-12T21:44:21.148401Z'
source: https://arxiv.org/abs/2606.21377v1
source_domain: arxiv.org
fetched_at: '2026-09-12T21:32:51.144719Z'
fetch_provider: crawl4ai
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'arXiv 2606.21377v1 (2026): uses 5 ATT&CK technique-ID occurrences (with
  sub-techniques); ATT&CK release declaration classified as none.'
raw_file: raw/arena-an-architecture-for-measuring-the.pdf
doi: arXiv:2606.21377v1
---

ARENA: An Architecture for Measuring the
Transferability of Autonomous Cyber Defense
Sidnei Barbieri1, ´Agney Lopes Roth Ferraz1, Wagner Comin Sonaglio1, Gioliano de Oliveira Braga1, Henrique
Curi de Miranda1 and Lourenc¸o Alves Pereira J´unior1
1Computer Science Division, Aeronautics Institute of Technology (ITA), S˜ao Jos´e dos Campos/SP - Brazil
sidneisb@ita.br, roth@ita.br, sonaglio@ita.br, giolianobraga@ita.br, henriquecuri1@proton.me, ljr@ita.br
Abstract— Agentic AI systems powered by Large Language
Models (LLMs) are increasingly used to build autonomous
defense agents, yet evaluating them remains an open challenge.
An agent that succeeds in one environment often degrades
when the same attack runs on a different platform, telemetry
stack, or policy; we call this the agent transferability gap:
success in one environment is not evidence of capability in
the next. We present ARENA, a modular architecture that
decomposes cyber-defense evaluation into four independently
varying layers: attacker emulation, System Under Test (SUT)
generation, a typed agent runtime, and a deterministic policy
verifier, plus a failure taxonomy that attributes degradation to
schema, grounding, budget, or policy. A controlled experiment
reveals the gap: two deterministic agents, indistinguishable under
detection recall, diverge once the telemetry schema changes, and
ARENA attributes the loss to observation semantics rather than
to attack recognition. ARENA makes transferability measurable,
attributable, and reproducible.
Keywords— autonomous agents, transferability, cyber range,
adversary emulation
I. INTRODUCTION
Security Operations Centers (SOCs) process thousands of
alerts a day, yet the median time to contain a breach is
still measured in days, not minutes [1]. That pressure is
moving Large Language Model (LLM) agents into the loop
as autonomous defenders that triage, investigate, and contain
with little human intervention [2]. Each such agent is validated
somewhere, on a benchmark, in a lab, or on one cyber range,
and is then deployed elsewhere. Deployment rests on an
assumption that no one states: that a capability shown in one
environment carries over to the next.
The assumption is fragile. The same attack produces
different observations as the environment changes: Elastic
Common Schema (ECS) JavaScript Object Notation (JSON)
becomes Splunk Common Information Model (CIM) records,
a Windows event log becomes a Linux audit record, and an
enterprise host becomes an Open Radio Access Network (O-
RAN) controller. An agent that learned to read one telemetry
schema can miss the identical attack expressed in another.
When it does, current evaluations remain silent on the ques-
tions that determine whether the agent is safe to deploy:
whether its capability degraded, by how much, at which step
in its reasoning, and why.
So this paper puts one question first: can an autonomous
cyber-defense capability transfer across environments? The
difficulty is structural. Structured Cyber Threat Intelligence
(CTI), such as MITRE ATT&CK encoded in the Structured
Threat Information Expression (STIX) format, constrains but
does not uniquely determine the target environment [3]: one
campaign can be faithfully realized on Linux containers,
Windows virtual machines, or a hybrid cloud, each emitting
different telemetry. The attack intent is fixed; the environment
and the observations it exposes are not. We call the resulting
capability loss the agent transferability gap, and current
practice cannot see it. Static prompt benchmarks divorced
from infrastructure [4] and single-environment ranges both
ask whether an agent worked in one context; neither asks
whether its competence survives a change of context.
Before ARENA, transferability is assumed. An evaluator
who watches an agent fail can report that it failed, not whether
the failure came from a changed telemetry schema, a lost
entity grounding, an exhausted query budget, or a policy the
agent misread. After ARENA, transferability is measured,
attributed, and reproduced: ARENA holds the attack intent
fixed, varies the environment, and records enough of each
run to replay it, so a degradation becomes a number with a
cause rather than an anecdote.
ARENA (Agent Resilience Evaluation Architecture) con-
tributes a decomposition of cyber-range evaluation into four
independently variable subsystems: attacker emulation, Sys-
tem Under Test (SUT) generation, agent runtime, and policy
verification; a failure taxonomy that attributes degradation to
schema, grounding, budget, or policy; and a controlled, repro-
ducible experiment that isolates transferability failures across
platform variants. Enterprise IT is the primary validation case.
Artificial Intelligence Radio Access Network (AI-RAN) over
O-RAN is a deliberate stress case: it changes the environment
and observation semantics more aggressively than any enter-
prise variant, motivating a transferability architecture rather
than a single-domain benchmark.
II. PROBLEM FORMULATION
To measure transferability, we must name what is held fixed
and what is allowed to change between two evaluations of the
same agent. Informally, every evaluation couples five things:
the attack the agent faces, the environment it runs in, what
that environment lets it see, the agent itself, and the rules it
must obey. Today, these are entangled, so when an agent fails,
no one can say which of them caused it. Naming them lets
us hold some fixed and vary others, which is exactly what
current evaluation cannot do.
We make the five precise as a tuple ⟨A, E, O, π, P⟩. The
attack intent A is the behavioral semantics of a campaign ex-
pressed in structured CTI (ATT&CK or FiGHT techniques in
STIX), independent of any concrete host. The environment E
is a concrete System Under Test: operating system, services,
arXiv:2606.21377v1  [cs.CR]  19 Jun 2026


---

Environment A
correlated telemetry
(Elastic, Splunk)
Environment B
normalized telemetry
(osquery)
Same attack, same defense agent
succeeds
fails
Only the telemetry schema changed.
Why different outcomes?
ARENA measures the gap, attributes
a cause, and makes it reproducible.
Fig. 1
THE AGENT TRANSFERABILITY GAP.
topology, and telemetry stack. The observations O are the
telemetry that the environment exposes to the defender; the
same intent on two environments yields different observations,
because ECS JSON, Splunk CIM records, and O-RAN E2
Service Model (E2SM) counters encode the same events in
different schemas. The agent π is a defense policy mapping
observations O to defensive actions, and the operational
policy P is the governance constraints an action must respect.
A defender’s competence is therefore a property of the
whole tuple, not of π alone. Holding the intent A and the
governance P fixed, we vary the environment from ei to ej,
thereby varying the observations it exposes. Transferability
is the degree to which the competence of π survives that
shift, read per exercised dimension: detection, grounding,
resource cost, policy compliance, and, for live SUTs, time-
to-containment. A result that holds for ei and collapses to ej
is the agent transferability gap, made quantitative (Fig. 1).
This framing reorients evaluation. A static benchmark fixes
E and O and measures π on prompts; a single-environment
range fixes one E and varies A. Neither isolates the variable
that matters in deployment, the environment, so neither can
separate a capability intrinsic to π from an artifact of the one
environment it was tuned on. ARENA makes ⟨A, E, O, π, P⟩
explicit, varies E and O while holding A and P fixed,
and attributes each change in transferability to the layer that
produced it. The rest of the paper instantiates each element of
the tuple as an independently configurable layer and defines
the taxonomy that performs the attribution.
Threat model and scope. ARENA targets autonomous
defense against targeted, multi-stage campaigns, the behavior
of an Advanced Persistent Threat (APT) rather than an
opportunistic scan or a single exploit. The attack intent A
is therefore drawn from documented campaigns encoded in
structured CTI: enterprise campaigns from ATT&CK-in-STIX
and, in the AI-RAN domain, telecom campaigns from MITRE
FiGHT. The empirical claim is precise: ARENA quantifies
whether a defender’s competence survives the environmental
changes a campaign traverses and attributes any loss to
a layer. The adversary follows the campaign’s behavioral
semantics while the environment fixes concrete bindings,
such as hosts, credentials, and telemetry schema, making one
intent replayable across SUTs. The evaluation boundary is the
deployed agent and its enforcement mechanism; the physical
layer, model-training supply chain, and human analyst remain
separate objects of study.
III. BACKGROUND
Cyber ranges have evolved from static training environ-
ments for human operators into programmable platforms
capable of automated adversary emulation. Tools such as Apa-
che Caldera [5], originally developed at MITRE, orchestrate
multi-step attack campaigns by executing “abilities” map-
ped to ATT&CK techniques. However, Caldera and similar
platforms assume that the operator manually configures the
target environment and provides the specific parameters (IP
addresses, credentials, file paths) required to map abstract
techniques to executable commands.
Recent measurement work has quantified this gap. The
procedural semantics gap in ATT&CK-in-STIX reveals that
structured technique-to-procedure entries lack the executable
detail needed for fully automated replay [6]. Meanwhile, the
environment semantics gap demonstrates that the overwhel-
ming majority of software objects in public CTI lack version
or Common Platform Enumeration (CPE) pinning, making
automated SUT derivation impossible without analyst inter-
vention [3].
The integration of LLMs into security operations has pro-
gressed along two tracks. Copilot systems, such as Microsoft
Security Copilot, augment human analysts by summarizing
alerts and suggesting investigation steps. Agent systems go
further: they execute closed-loop investigation and contain-
ment without waiting for human approval at each step [2].
Both tracks introduce failure modes absent from traditional
rule-based systems. LLMs can hallucinate IP addresses that
are not present in the telemetry, propose actions against assets
outside their jurisdiction, or violate organizational policies,
such as isolating a production server before collecting forensic
evidence [7].
Static benchmarks test prompt-level reasoning but ignore
infrastructure coupling. Single-environment simulations cap-
ture interactions within a fixed topology. Agent guardrails
usually check only the prompt or tool boundary. None varies
the environment E and the observations O under a fixed intent
A, which is the regime in which the transferability question
of Section II lives.
IV. ARENA ARCHITECTURE
ARENA decomposes the evaluation problem into four
subsystems, each independently configurable. Fig. 2 shows
them with explicit interfaces over a shared artifact store: the
attack intent enters the attacker substrate, the SUT generator
instantiates the environment, the agent runtime emits a typed
action trace, and the policy verifier checks it. Every subsystem
reads and writes versioned artifacts, so any run can be
replayed or audited, and a transferability failure can be traced
to the subsystem that produced it.


---

CTI / STIX bundle
→intent model
Parameter binding
→Caldera adapter
Fixed ∩free region
Provisioning orchestrator
SUT-A/B/C
Win·Elastic, Win·Splunk,
Linux·osquery
Dispatcher →agent
(LLM) + tools
Typed schema +
grounding boundary
task | action | source | data
Deterministic
verifier →verdict
1. Attacker emulation
2. SUT generator
3. Agent runtime
4. Policy verifier
Evaluation engine & versioned artifact store
transferability matrix · failure taxonomy (SF/GF/BE/PV) · immutable, replayable runs
intent A
observations O
action trace
Fig. 2
ARENA MEASUREMENT ARCHITECTURE. THE SHARED STORE RECORDS A TRANSFERABILITY MATRIX AND A FAILURE TAXONOMY: SCHEMA (SF),
GROUNDING (GF), BUDGET (BE), AND POLICY (PV) FAILURES.
Attacker substrate. The first layer converts structured
CTI into executable, multi-host attack workflows. It separates
behavioral extraction, which parses ATT&CK technique IDs
and STIX procedure descriptions into adversary intent, from
parameter binding, which maps that intent to target IPs,
credentials, paths, and other SUT-specific values, and from
workflow compilation, which emits a plan for Caldera or an
equivalent orchestrator [6]. This separation is what makes
the transferability testable: lateral movement over a Server
Message Block (SMB)-class share reflects the same attack
intent whether it runs on Windows SMB or Linux Samba,
while the bindings and telemetry vary with the SUT.
SUT generator. The second layer partitions each environ-
ment specification into a fixed region and a free region [3].
The fixed region contains constraints that the CTI requires,
such as an operating-system family or service class. The
free region contains analyst-controlled choices left unspecified
by CTI, such as telemetry stack, topology, patch level, and
deployment substrate. Varying the free region while pre-
serving the fixed region produces multiple valid SUTs for
the same campaign. A ransomware campaign that requires
Windows domain services, for example, can be detected
with Elastic telemetry, Splunk telemetry, or a Falco/osquery
hybrid. The generator records the deployment modality as
container-feasible (CF), virtual-machine-required (VMR), or
infrastructure-dependent (ID), so the evaluator knows which
results depend on kernel behavior or network segmentation
rather than on the agent alone.
Agent runtime. The third layer provides a controlled exe-
cution boundary for LLM-based defense agents and follows
a manifest-driven architecture [2]. It uses three mechanisms.
Bounded telemetry delivery. The dispatcher delivers a
finite, bounded slice of telemetry to the agent for each
investigation cycle. This prevents the agent from accessing un-
bounded log stores, which would enable hallucination through
pattern-matching on irrelevant data. The telemetry window
size is configurable and recorded as an evaluation parameter.
Typed report schema. The agent must emit a structured
report conforming to a declared JSON schema. The report
contains fields for the identified threat type, affected assets
(by telemetry-grounded identifiers), proposed containment ac-
tions, and confidence indicators. Any report that fails schema
validation is recorded as a schema failure in the failure
taxonomy.
Grounding verification. Before any proposed action is
forwarded to the policy verifier, the enforcement boundary
checks a grounding proof: every referenced asset must resolve,
through an evaluation-time entity table, to evidence in the
telemetry slice delivered to the agent. An action against an
entity present in the slice but unresolved or misattributed
by the agent is a grounding failure. A legitimate entity
absent from the delivered slice but present in the hash-pinned
full rendering is, in fact, a windowing limitation. This is a
deterministic set-membership test over the delivered and full
entity tables, not a post hoc analyst judgment; both tables are
retained so that the attribution can be replayed.
Policy verifier. The fourth layer defines deterministic, pre-
execution verification of agent-proposed action plans [7].
Its policy vocabulary admits mandatory actions, temporal
prohibition-before constraints, and approval-gated actions, as
well as the SOC-defense reading of task alignment, action
alignment, source authorization, and data isolation [8]. Rules
are finite predicates over an ordered trace, so a concrete
checker can emit an auditable verdict without relying on the
evaluated model. The current prototype instantiates one such
predicate, evidence collection before isolating a production
host; richer rule sets remain versioned policy inputs rather
than unimplemented empirical claims. The verifier tags the
plan and records violations without letting the agent grade
itself, so compliance can be compared across SUT configura-
tions.
Failure taxonomy. ARENA classifies degradation into
schema failures (SF), grounding failures (GF), budget exhaus-
tion (BE), and policy violations (PV). SF means the agent’s
report does not conform to the typed output schema. GF
means the agent references an entity that does not resolve to
evidence in its delivered telemetry, rather than a windowing
limitation in which a legitimate entity fell outside the teleme-
try window. BE means the agent exceeds the allowed number
of investigation queries or token budget, and PV means the
proposed plan violates one or more SOC governance rules.
By recording these categories for each agent and SUT variant,


---

ARENA produces a transferability matrix that reveals where
an agent’s chain of reasoning breaks when the environment
changes.
When several checks fail in a single run, ARENA records
the full failure vector and assigns a primary label based on
the first boundary that blocks safe interpretation, in the order
SF, GF, BE, PV. This keeps attribution deterministic while
preserving the co-occurrence for later analysis. A schema-
invalid plan, for instance, is never read further as policy-
compliant or non-compliant.
Response and deception. A defender that only labels
an incident is half a defender, so ARENA scores the full
detect, attribute, and respond loop. The agent must contain
the incident and may, where policy permits, deceive the
adversary by redirecting them to a decoy host or by planting
honeytokens. Because a deceptive action changes what the
adversary observes, the verifier treats it as privileged and gates
it on the source-authorization and data-isolation properties,
while the artifact store records the decoy state so the run
stays reproducible. A benign-only rendering of the same
background runs beside each campaign, so an agent that
aggressively tries to lift its recall pays a false-positive cost.
Response quality, therefore, enters the transferability matrix
alongside detection, which is why an agent can transfer its
detection and still fail to transfer a safe response.
Transferability metric. ARENA’s matrix separates each
exercised dimension rather than collapsing them into an
arbitrary weighted score: detection, grounding, resource cost,
policy compliance, and, for live SUTs, containment latency.
For an agent a and two SUT variants si and sj of the
same campaign, the transferability delta ∆(a, si →sj) is
reported for every dimension exercised by that experiment.
Re-evaluations of agent defenses reach the same conclusion:
effectiveness and utility are distinct axes, and a single number
conflates them [8], [9]. A reference SUT s0 anchors the
comparison, and the failure taxonomy attributes each change
to a layer. The controlled experiment below isolates obser-
vation semantics and therefore reports detection, grounding,
resource, and verifier-calibration outcomes; a live-SUT matrix
adds wall-clock containment.
Cross-domain generality. None of the four layers is speci-
fic to enterprise IT: the attacker substrate, the fixed/free SUT
partition, the typed runtime, and the policy verifier stay the
same when the domain changes; only the CTI source and the
concrete components do. The flagship cross-domain specifica-
tion is AI-RAN over O-RAN. Its open, multi-vendor interfaces
(O1, O2, E2) and the controller split across the service mana-
gement, rApp, and xApp tiers [10] make it the most heteroge-
neous environment a defender can face, so it is the strongest
stress test of transferability rather than a convenient one. The
attacker substrate consumes MITRE FiGHT, the 5G threat
knowledge base, exactly as it consumes ATT&CK: FiGHT-
in-STIX is translated into an O-RAN operation, the analog
of the enterprise round-trip. The defender’s observations be-
come radio key performance indicators (KPIs) and E2SM
counters rather than host logs, which exercises precisely the
observation axis O that the tuple isolates. ORION supplies
the legitimate intent-to-policy control loop the agent must
defend [11], and AutoRAN provisions the stack reproducibly
from declarative automation [12]. The same partition holds
for additional domains, such as 5G Unmanned Aerial Vehicle
TABLE I
CONTROLLED TRANSFERABILITY EXPERIMENT.
Agent
SUT
Det.
Prec.
Grnd.
∆Grnd.
GF
BE
Reference
Elastic
1.00
0.62
1.00
—
0
0
Reference
Splunk
1.00
0.62
1.00
+0.00
0
0
Reference
Osquery
1.00
0.62
0.60
−0.40
2
1
Correlation
Elastic
1.00
0.62
1.00
—
0
0
Correlation
Splunk
1.00
0.62
1.00
+0.00
0
0
Correlation
Osquery
1.00
0.62
1.00
+0.00
0
1
(UAV) command-and-control [13] and federated Unmanned
Traffic Management (UTM) [14]: the attack intent remains
fixed while the environment, observations, and policy vary, so
transfer from enterprise IT to AI-RAN, 5G, or UTM becomes
measurable within a single architecture.
V. EXPERIMENT
We implemented ARENA’s measurement core and execu-
ted a controlled transferability experiment. The fixed attack
intent is a targeted ransomware intrusion with five ATT&CK
stages: spearphishing initial access (T1566.001), PowerShell
execution (T1059.001), file and directory discovery (T1083),
SMB lateral movement (T1021.002), and application-layer
command and control (T1071.001). The campaign contains
11 canonical events: the five malicious stages, three unrelated
background events, and three legitimate PowerShell, disco-
very, and SMB activities that deliberately trigger the same
rules as malicious events. We render this single source of truth
into three SUTs that change only the observation schema:
ECS, where each event is a correlated nested document;
CIM, where each event is a flat record with different field
names; and osquery, a relational view that splits a process
and its connection into rows joined by a process identifier.
The reference agent attributes a technique to the process in
the signal’s record; the correlation agent additionally joins
the process and connection by that identifier. An independent
ARENA instrument performs event-level scoring against the
authoritative entity table, so every number in Table I recom-
putes from recorded artifacts.
In Table I, Det. is malicious-event recall, Prec. is event-
level precision, and Grnd. additionally requires the respon-
sible process, or host when no process exists, to match the
authoritative entity table. Both agents detect all five malicious
stages but reach only 0.62 precision because the context-
insensitive rules also flag the three legitimate lookalikes. This
false-positive cost is stable across schemas and therefore does
not masquerade as transfer loss. On Elastic and Splunk, both
agents ground every malicious event. On osquery, however,
the reference agent’s grounded recall drops to 0.60: lateral
movement and command-and-control remain detected, but
their owning processes are lost across separate rows, resulting
in two grounding failures. The correlation agent rejoins those
rows, restoring grounded recall to 1.00. The oracle grounds
every stage in every schema, proving that osquery contains
the evidence. Both agents still exceed the normalized per-
event read budget on osquery, so the experiment separates
an agent capability defect (GF) from irreducible schema
expansion (BE). Detection recall remains 1.00 throughout;
ARENA exposes a transferability failure that detection alone
cannot observe.


---

The robustness sweep repeats the three legitimate lookalikes
0, 1, 2, and 4 times while leaving all malicious events un-
changed. Precision falls from 1.00 to 0.62, 0.45, and 0.29, as
expected under increasing ambiguity; however, the reference
agent’s osquery grounding delta remains exactly −0.40, and
the correlation agent remains at 0.00. Thus, benign ambiguity
affects detection precision but not the measured transferability
mechanism. The oracle, entity table, canonical campaign, pure
renderers, and exact per-run budget are versioned separa-
tely from the agents, making this result deterministic and
replayable. As an applicability check, the same typed runtime
also evaluated Claude Opus 4.8 (claude-opus-4-8, the
provider’s current Opus model ID [15]) without changing
ground truth or scoring: Det./Grnd. stayed at 1.00/1.00 on
Elastic and 1.00/1.00 on Splunk, then fell to 0.20/0.20 on
osquery with BE=1. This optional run is not a model ranking;
it shows that the instrument can evaluate an actual frontier
LLM while the deterministic agents remain the reproducible
control.
Two calibration experiments bound the remaining attribu-
tions. The budget sweep allows 8, 11, and 16 record reads,
respectively 0.73, 1.00, and 1.45 reads per canonical event.
All SUTs exceed 8, only osquery exceeds 11 (it renders 16
rows), and none exceeds 16. Grounding is invariant across
those thresholds, so BE records a declared resource policy
while GF records an agent capability. Separately, three policy
traces validate the prototype predicate: evidence-then-isolate
on the production host passes, direct isolation of that host
yields PV, and direct isolation of a workstation passes. These
controls exercise both verifier verdicts without implying co-
verage of every rule family.
The three schemas are the measurement, not decoration.
Elastic ECS and Splunk CIM keep process, host, and network
facts correlated within one event while changing field names
and query idioms, so they test transfer across telemetry voca-
bulary; osquery splits those facts into separate rows joined by
an identifier, so it tests transfer across observation structure.
Together, they provide a stronger semantic contrast than
adding another alerting layer on top of Elastic or OpenSearch,
while AI-RAN changes the observation object itself to radio
KPI streams.
Validity controls. The experiment supports a mechanistic
claim: under fixed attack intent, policy, rules, and canonical
events, changing observation structure removes two process-
to-connection links from the reference agent’s local view;
adding exactly that join restores them. The correlation agent
changes one capability, while the oracle proves the availability
of evidence, and the scaled budget separates record expan-
sion from inference failure. Event-level matching prevents
a familiar ATT&CK label on benign activity from being
credited as a true positive, and the ambiguity sweep shows that
false-positive pressure changes precision without changing the
grounding delta. These controls jointly identify the cause of
the observed loss rather than merely correlating it with the
osquery rendering.
AI-RAN over O-RAN is the cross-domain stress case
produced by the same architecture. We compile FiGHT
subtechnique FGT5034.001, O-RAN E2Mgr Unauthorized
Access, into a versioned trial manifest with pinned prove-
nance (repository, commit, checksum, FiGHT status). The
specified substrate is a near-real-time RAN Intelligent Con-
troller (FlexRIC), an open O-RAN near-real-time RIC with
xApp development support [16], hosting the agent over an
srsRAN/OpenAirInterface stack provisioned by AutoRAN;
the fixed intent is a rogue xApp invoking an insufficiently
authorized E2 Manager (E2Mgr) interface, and controlled
variants change xApp authorization, E2 exposure, telemetry
completeness, and per-UE service objectives. Observations
become E2SM Key Performance Measurement (E2SM-KPM)
counters, per-UE throughput and latency, E2 subscriptions,
and xApp control actions, so the defender must hold KPI and
per-UE context that host logs are never required for. This
makes a false healthy state measurable: aggregate KPIs stay
within baseline while a protected user equipment violates its
objective, and any containment must respect the controller’s
near-real-time deadline. The artifact labels this trial specified,
not executed: the enterprise experiment carries the empirical
claim, while the compiled manifest shows that ARENA maps
the same measurement object onto AI-RAN without inventing
results.
ARENA scores two axes that prior evaluations conflate.
The first is benign transfer, the trial above: Does a capability
survive a change of SUT, telemetry, or policy? The second
is adversarial-surface resistance: holding the SUT fixed, does
the enforcement boundary survive injection into the agent’s
context, a poisoned playbook, a misleading tool description,
or a corrupted retrieval entry? The same runtime and verifier
serve both, yet the scorecards stay separate, so a defense can-
not hide weak transfer behind strong injection resistance, nor a
broken tool boundary behind good detection. The governance
the verifier enforces is one organization’s; coalition or cross-
tenant policy needs a richer conflict model, which the artifact
contract already carries as a versioned input rather than a
hidden assumption.
The practical consequence is a sharper evaluation question.
Instead of asking whether an autonomous defender is “good”
in the abstract, ARENA asks which capability was transferred:
attack recognition, entity grounding, budget discipline, policy
compliance, or containment behavior. That separation matters
most in heterogeneous infrastructure. Enterprise telemetry
may change vocabulary; O-RAN telemetry changes the ob-
servation object itself, from host logs to KPI streams, E2SM
counters, xApp actions, and service objectives. A defender
that recognizes the tactic can still lose the entity or policy
context needed to respond safely. The versioned manifest, ora-
cle, entity table, budget sweep, policy verdicts, and AI-RAN
trial specification make the enterprise losses replayable and
the measurement object extensible across agents, campaigns,
and SUTs.
The same decomposition also prevents a common evalua-
tion failure: silently changing several denominators at once.
A new campaign changes the canonical event set and oracle,
but should not change the scoring code. A new SUT changes
the renderer, entity table, and policy bindings, but should not
change attack intent. A new agent changes the manifest and
runtime adapter, but should not change the verifier. A new
governance rule changes the policy version, but should not
change telemetry. This discipline gives reviewers a concrete
audit path for future extensions: when a result changes, the
artifact says whether the changed object was the attacker,
environment, observation, agent, or policy, rather than asking
the reader to infer it from prose. It also makes negative results


---

useful: a failed transfer trial need not be dismissed as a bad
prompt or a misconfigured range. The artifact can indicate
whether the next experiment should improve the correlation,
widen the observation window, alter the policy, or change the
environment generator.
VI. RELATED WORK
Prior work places three design pressures on ARENA:
executable emulation must be tied to real environments, agent
evaluation must measure safety and utility under distribution
shift, and claims about autonomous behavior must remain
auditable.1 Apache Caldera [5] and Atomic Red Team auto-
mate attack execution, CyberBattleSim [18] models abstract
network interaction, and Effects Language (EL) adds executa-
ble graph semantics for repeatable adversary emulation [19].
Industrial platforms (AttackIQ, SCYTHE, Prelude Operator)
and academic ranges such as DETERLab [20] and Emu-
lab [21] provide execution and topology, while policy engines
such as Open Policy Agent (OPA)/Rego motivate declarative
verification. Building on the procedural- and environment-
semantics gaps that measurement work has revealed in public
CTI [3], [6], ARENA differs in the evaluation affordance
it exposes: it systematically varies the SUT under a fixed
attack intent and places the defense agent behind a typed
enforcement boundary.
This distinction matters because execution fidelity and
transferability measurement are different scientific objects. A
range can replay an attack in one topology and still leave
unanswered whether the defender learned the campaign se-
mantics or merely the telemetry conventions of that topology.
An emulation engine can run a technique and still require an
analyst to bind the environment-specific details that decide
what the agent sees. A policy engine can reject an unsafe
action and still say nothing about whether the agent’s detec-
tion degraded when observations changed. ARENA borrows
from all three families but changes the experimental question:
hold the campaign intent and governance fixed, change the
environment and observation semantics, and record which
boundary accounts for any loss.
The closest architectural alternatives also separate at the
artifact boundary. DETERLab and Emulab make topologies
reproducible, but their primary artifact is a network experi-
ment; ARENA’s artifact additionally includes the CTI bundle,
SUT manifest, telemetry schema, entity table, agent manifest,
policy version, and verifier decision record. Caldera and
Atomic Red Team make actions executable, but their primary
question is whether an operation can run; ARENA’s primary
question is whether a defense capability transfers when the
same operation is rendered through another SUT. Runtime
policy systems make enforcement explicit, but ARENA treats
enforcement output as a measurement dimension rather than
merely a guardrail. Industrial breach-and-attack evaluations
such as MITRE Engenuity ATT&CK Evaluations [22] score
detection products against a fixed emulated adversary in
a vendor-chosen environment; ARENA inverts that design,
holding the adversary fixed and varying the environment to
measure transfer. These differences are why ARENA is not
1The literature surveyed in this section was assembled with a reproducible,
versioned venue corpus [17].
another cyber range; it is a measurement architecture for a
failure mode that current ranges do not isolate.
Evaluation work shows why this separation matters. Static
benchmarks such as SECURE [4] measure reasoning but
ignore infrastructure, and even the newest agentic-SOC bench-
marks, such as the Cyber Defense Benchmark [23], evaluate
threat hunting within a single telemetry environment rather
than across multiple environments. Re-evaluations of prompt-
injection defenses [9] and unified platforms [24] reveal the
second pressure: defenses must confront adaptive attacks
and benign utility tasks simultaneously. Broader safety and
trustworthiness studies [25], [26] and offensive-AI syste-
matization with automated safety data pipelines [27], [28]
therefore motivate the reporting choice in ARENA: capability
and policy compliance are measured side by side rather than
collapsed into one scalar.
The agentic attack surface is broader than one prompt chan-
nel. Representative attacks reach the prompt and context win-
dow [29], [30], long-context and order-oblivious settings [31],
[32], web-agent and tool-selection layer [33], [34], multi-
modal channel [35], retrieval store [36]–[38], persistent me-
mory [39], [40], and agent protocol or tool description [41]–
[43]. Detection and traceback [44], [45], sanitization and type-
directed privilege separation [46], [47], and runtime enforce-
ment [48] answer different slices of that surface. However,
each attack and each defense is usually validated in the setting
in which it was introduced. ARENA treats a defense as a
configurable component whose robustness must itself transfer,
turning a catalog of point results into a measurement question.
The evidence that capability fails to transfer across environ-
ments exists in pieces that ARENA unifies into one measure-
ment. Behavioral malware detection degrades when sandbox-
trained models meet real endpoints [49], and HORIZON
shows reliability falling across longer agent trajectories [50].
Task drift, jailbreak detection under distribution shift, and the
research–practice gap in adversarial ML show that context, not
model quality alone, determines outcomes [51]–[53]. Cyber-
specific agents in CTI, malware detection, and fuzzing raise
the same question in operational settings [54]–[56], while
SOC response shows the policy side of the problem [7]; mo-
bile adaptation and O-RAN control extend it to heterogeneous
infrastructure [2], [57], [58]. The O-RAN line is especially
relevant because its control plane is programmable and clo-
sed loop: Polese et al. define the architectural surface [10],
ORION supplies intent-aware orchestration [11], and Auto-
RAN supplies reproducible automation [12]. ATT&CK and
FiGHT provide campaign vocabularies, but the scientific
question is defensive transfer, not offensive automation: an
agent can identify a tactic in one substrate and still lose the
entity, KPI, or policy context needed to respond safely in
another.
VII. CONCLUSION
We presented ARENA, an evaluation architecture with
independently variable attacker emulation, SUT generation,
agent runtime, and policy verification. Its controlled expe-
riment revealed a 0.40 grounding loss that detection recall
missed, attributed it to two missing cross-table joins, and
showed that a correlation-aware agent restores grounding.
Evaluating an agent on a single telemetry representation,


---

therefore, overstates its deployed competence: detection can
remain perfect while grounding silently degrades in response
to a valid operational change. The same layers compile a
pinned FiGHT technique into an auditable AI-RAN trial
specification. ARENA therefore turns transferability from
an assumption into a measured, attributed, and reproducible
property, establishing a simple discipline: success in one
environment is not evidence of capability in the next.
REFERENCES
[1] IBM Security, “Cost of a data breach report 2024,” https://www.ibm.
com/reports/data-breach, 2024, accessed: 2026-06-12.
[2] S. Barbieri, ´A. L. R. Ferraz, L. A. Pereira J´unior, “PocketAgents: A
manifest-driven library of autonomous defense agents,” 2026. [Online].
Available: https://arxiv.org/abs/2605.21694
[3] ——, “AutoSUT: The environment semantics gap in structured
CTI for adversary emulation,” 2026. [Online]. Available: https:
//arxiv.org/abs/2606.08700
[4] N. Kaushik et al., “Benchmarking large language models for cyber-
security advisory,” arXiv preprint arXiv:2405.20441, 2024, SECURE
benchmark.
[5] The Apache Software Foundation, “Apache Caldera: Automated adver-
sary emulation platform (originally MITRE Caldera),” https://caldera.
apache.org/, 2026, accessed: 2026-06-17.
[6]
´A. L. R. Ferraz, S. Barbieri, M. E. de Souza, L. A. Pereira J´unior,
“The procedural semantics gap in structured CTI: A measurement-
driven STIX analysis for APT emulation,” 2026. [Online]. Available:
https://arxiv.org/abs/2512.12078
[7] S. Barbieri, L. V. d. Meneses, ´A. L. R. Ferraz, L. A. Pereira J´unior,
“SOCpilot: Verifying policy compliance for LLM-assisted incident
response,” 2026. [Online]. Available: https://arxiv.org/abs/2605.05501
[8] V. Siu, J. He, K. Montgomery, Z. Wang, N. Gong, C. Wang, D. Song,
“A framework for formalizing llm agent security,” arXiv preprint
arXiv:2603.19469, 2026.
[9] Y. Jia, Z. Shao, Y. Liu, J. Jia, D. Song, N. Z. Gong, “A critical
evaluation of defenses against prompt injection attacks,” arXiv preprint
arXiv:2505.18333, 2025.
[10] M. Polese, L. Bonati, S. D’Oro, S. Basagni, T. Melodia, “Understanding
O-RAN: Architecture, interfaces, algorithms, security, and research
challenges,” 2022. [Online]. Available: https://arxiv.org/abs/2202.01032
[11] G.
d.
S.
Machado,
G.
Z.
Bruno,
A.
Huff,
J.
M.
C.
Brito,
C. B. Both, “ORION: Intent-aware orchestration in Open RAN
for SLA-driven network management,” 2026. [Online]. Available:
https://arxiv.org/abs/2603.03667
[12] S. Maxenti, R. Shirkhani, M. Elkael, L. Bonati, S. D’Oro, T. Melodia,
M.
Polese,
“AutoRAN:
Automated
and
zero-touch
Open
RAN
systems,” 2025. [Online]. Available: https://arxiv.org/abs/2504.11233
[13] W. C. Sonaglio, ´A. L. R. Ferraz, A. E. Melo, M. E. de Souza, G. Noubir,
L. A. Pereira J´unior, “When connectivity is not enough: Cross-layer
attacks on UAV C2 over 5G,” 2026, arXiv:2603.04662.
[14] H. Curi de Miranda, ´A. L. R. Ferraz, W. C. Sonaglio, L. A. Pe-
reira J´unior, “A systematic security testing approach for InterUSS-based
environments,” 2026, arXiv:2605.11339.
[15] Anthropic, “Claude models overview,” https://docs.anthropic.com/en/
docs/about-claude/models/overview, 2026, accessed: 2026-06-18.
[16] OpenAirInterface Alliance, “FlexRIC tutorial: xApp development,”
https://openairinterface.org/flexric-tutorial-xapp-development/,
2026,
accessed: 2026-06-18.
[17] S. Barbieri, ´A. L. R. Ferraz, L. A. Pereira J´unior, “TopVenues: A
reproducible corpus and tooling substrate for cybersecurity literature
reviews,” 2026. [Online]. Available: https://arxiv.org/abs/2606.18320
[18] Microsoft, “CyberBattleSim: An experimentation and research platform
for automated agents in simulated enterprise networks,” https://github.
com/microsoft/CyberBattleSim, 2021, accessed: 2026-06-12.
[19] Suresh K. Damodaran and Paul D. Rowe, “Automated repeatable
adversary threat emulation with effects language (EL),” Digital
Threats: Research and Practice, 2026. [Online]. Available: https:
//doi.org/10.1145/3816043
[20] T. Benzel, “The science of cyber security experimentation: The DETER
project,” in Annual Computer Security Applications Conf. (ACSAC),
2011.
[21] B. White, J. Lepreau, L. Stoller, R. Ricci, S. Guruprasad, M. New-
bold, M. Hibler, C. Barb, A. Joglekar, “An integrated experimental
environment for distributed systems and networks,” in USENIX Symp.
on Operating Systems Design and Implementation (OSDI), 2002.
[22] MITRE
Engenuity,
“ATT&CK
evaluations,”
https://attackevals.
mitre-engenuity.org/, 2026, accessed: 2026-06-18.
[23] A. Chona, I. Kozlov, A. Kumar, “Cyber Defense Benchmark: Agentic
threat hunting evaluation for LLMs in SecOps,” arXiv:2604.19533,
2026.
[24] R. Geng, C. Yin, Y. Wang, Y. Chen, J. Jia, “Piarena: A platform for
prompt injection evaluation,” arXiv preprint arXiv:2604.08499, 2026.
[25] X. Ma, Y. Gao, Y. Wang, R. Wang, X. Wang, Y. Sun, Y. Ding, H. Xu,
Y. Chen, Y. Zhao, H. Huang, Y. Li, Y. Wu, J. Zhang, X. Zheng, Y. Bai,
Y. Li, Z. Wu, X. Qiu, J. Zhang, X. Han, H. Li, J. Sun, C. Wang,
J. Gu, B. Wu, S. Chen, T. Zhang, Y. Liu, M. Gong, T. Liu, S. Pan,
C. Xie, T. Pang, Y. Dong, R. Jia, Y. Zhang, S. Ma, X. Zhang, N. Gong,
C. Xiao, S. Erfani, T. Baldwin, B. Li, M. Sugiyama, D. Tao, J. Bailey,
Y.-G. Jiang, “Safety at scale: a comprehensive survey of large model
and agent safety,” in Foundations and Trends® in Privacy and Security,
2025.
[26] Y. Huang, C. Gao, S. Wu, H. Wang, X. Wang, Y. Zhou, Y. Wang,
J. Ye, J. Shi, Q. Zhang, Y. Li, H. Bao, Z. Liu, T. Guan, D. Chen,
R. Chen, K. Guo, A. Zou, B. H. Kuen-Yew, C. Xiong, E. Stengel-Eskin,
H. Zhang, H. Yin, H. Zhang, H. Yao, J. Yoon, J. Zhang, K. Shu, K. Zhu,
R. Krishna, S. Swayamdipta, T. Shi, W. Shi, X. Li, Y. Li, Y. Hao, Z. Jia,
Z. Li, X. Chen, Z. Tu, X. Hu, T. Zhou, J. Zhao, L. Sun, F. Huang,
O. C. Sasson, P. Sattigeri, A. Reuel, M. Lamparth, Y. Zhao, N. Dziri,
Y. Su, H. Sun, H. Ji, C. Xiao, M. Bansal, N. V. Chawla, J. Pei, J. Gao,
M. Backes, P. S. Yu, N. Z. Gong, P.-Y. Chen, B. Li, D. Song, X. Zhang,
“On the trustworthiness of generative foundation models: Guideline,
assessment, and perspective,” arXiv preprint arXiv:2502.14296, 2025.
[27] S. L. Schr¨oer, G. Apruzzese, S. Human, P. Laskov, H. S. Anderson,
E. W. N. Bernroider, A. Fass, B. Nassi, V. Rimmer, F. Roli, S. Salam,
C. E. A. Shen, A. Sunyaev, T. Wadhwa-Brown, I. Wagner, G. Wang,
“Sok: On the offensive potential of ai,” in 2025 IEEE Conference on
Secure and Trustworthy Machine Learning (SaTML), 2025.
[28] X. Zhou, W. Wang, L. Lu, J. Shi, G. Tie, Y. Xu, L. Chen, P. Zhou, N. Z.
Gong, L. Sun, “Safeagent: Safeguarding llm agents via an automated
risk simulator,” arXiv preprint arXiv:2505.17735, 2025.
[29] Y. Jia, Y. Liu, Z. Shao, J. Jia, N. Gong, “Promptlocate: Localizing
prompt injection attacks,” arXiv preprint arXiv:2510.12252, 2025.
[30] R. Wang, Y. Jia, N. Z. Gong, “Obliinjection: Order-oblivious prompt
injection attack to llm agents with multi-source data,” arXiv preprint
arXiv:2512.09321, 2025.
[31] X. Wang, Y. Liu, Z. Wang, D. Song, N. Gong, “Websentinel: Detecting
and localizing prompt injection attacks for web agents,” arXiv preprint
arXiv:2602.03792, 2026.
[32] J. Shi, Z. Yuan, G. Tie, P. Zhou, N. Z. Gong, L. Sun, “Prompt injection
attack to tool selection in llm agents,” arXiv preprint arXiv:2504.19793,
2025.
[33] R. Geng, Y. Wang, C. Yin, M. Cheng, Y. Chen, J. Jia, “Pisanitizer: Pre-
venting prompt injection to long-context llms via prompt sanitization,”
arXiv preprint arXiv:2511.10720, 2025.
[34] Z. Jiang, Y. Hu, Y. Yang, Y. Cao, N. Z. Gong, “Jailbreaking safeguarded
text-to-image models via large language models,” in Findings of the
Association for Computational Linguistics: EACL, 2026.
[35] P. Chao, A. Robey, E. Dobriban, H. Hassani, G. J. Pappas, E. Wong,
“Jailbreaking black box large language models in twenty queries,” in
2025 IEEE Conference on Secure and Trustworthy Machine Learning
(SaTML), 2025.
[36] W. Zou, R. Geng, B. Wang, J. Jia, “Poisonedrag: Knowledge corruption
attacks to retrieval-augmented generation of large language models,”
USENIX Security Symposium, 2025, arXiv:2402.07867.
[37] R. Geng, Y. Wang, Y. Chen, J. Jia, “Unic-rag: Universal knowledge
corruption attacks to retrieval-augmented generation,” arXiv preprint
arXiv:2508.18652, 2025.
[38] J. Liang, Y. Wang, C. Li, R. Zhu, T. Jiang, N. Gong, T. Wang, “Graphrag
under fire,” arXiv preprint arXiv:2501.14050, 2025.
[39] W. Jin, X. Wang, W. Zou, J. Jia, N. Gong, “Cleanbase: Detecting
malicious documents in rag knowledge database,” arXiv preprint ar-
Xiv:2605.00460, 2026.
[40] D. Feng, W. Cui, Y. Jiang, W. Yu, D. Li, “From static roles to context-
aware decisions: Integrating llms and rag into access control frameworks
for power systems,” in IEEE Access, 2026.
[41] Y. Hu, Y. Jia, M. Li, D. Song, N. Gong, “Maltool: Malicious tool attacks
on llm agents,” arXiv preprint arXiv:2602.12194, 2026.
[42] H. Ye, Z. Zhang, J. Jia, H. Hu, “Trustdesc: Preventing tool poisoning
in llm applications via trusted description generation,” arXiv preprint
arXiv:2604.07536, 2026.
[43] Anonymous, “A2asecbench: A protocol-aware security benchmark for
agent-to-agent multi-agent systems,” OpenReview preprint, 2025.
[44] Z. Cheng, J. Sun, A. Gao, Y. Quan, Z. Liu, X. Hu, M. Fang, “Se-
cure retrieval-augmented generation against poisoning attacks,” arXiv
preprint arXiv:2510.25025, 2025.
[45] B. Zhang, H. Xin, M. Fang, Z. Liu, B. Yi, T. Li, Z. Liu, “Traceback of


---

poisoning attacks to retrieval-augmented generation,” in Proceedings of
the ACM on Web Conference 2025, 2025.
[46] Y. Wang, S. Chen, R. Alkhudair, B. Alomair, D. Wagner, “De-
fending against prompt injection with datafilter,” arXiv preprint ar-
Xiv:2510.19207, 2025.
[47] D. Jacob, E. Alghamdi, Z. Hu, B. Alomair, D. Wagner, “Preventing
prompt injection with type-directed privilege separation,” arXiv preprint
arXiv:2509.25926, 2025.
[48] H. Wang, C. M. Poskitt, J. Sun, “AgentSpec: Customizable runtime
enforcement for safe and reliable llm agents,” arXiv preprint ar-
Xiv:2503.18666, 2025.
[49] Y. Kaya, Y. Chen, M. Botacin, S. Saha, F. Pierazzi, L. Cavallaro,
D. Wagner, T. Dumitras¸, “Ml-based behavioral malware detection is
far from a solved problem,” in 2025 IEEE Conference on Secure and
Trustworthy Machine Learning (SaTML), 2025.
[50] X. J. Wang, H. Bai, Y. Sun, H. Wang, S. Zhang, W. Hu, M. Schroder,
B. Mutlu, D. Song, R. D. Nowak, “The long-horizon task mirage?
diagnosing where and why agentic systems break,” arXiv preprint
arXiv:2604.11978, 2026.
[51] S. Abdelnabi, A. Fay, G. Cherubin, A. Salem, M. Fritz, A. Paverd, “Get
my drift? catching llm task drift with activation deltas,” in 2025 IEEE
Conference on Secure and Trustworthy Machine Learning (SaTML),
2025.
[52] J. Piet, X. Huang, D. Jacob, A. Chow, M. Alrashed, G. Zhao, Z. Hu,
C. Sitawarin, B. Alomair, D. Wagner, “Jailbreaksovertime: Detecting
jailbreak attacks under distribution shift,” in Proceedings of the 18th
ACM Workshop on Artificial Intelligence and Security, 2025.
[53] G. Apruzzese, H. S. Anderson, S. Dambra, D. Freeman, F. Pierazzi,
K. Roundy, ““real attackers don’t compute gradients”: Bridging the gap
between adversarial ml research and practice,” in 2023 IEEE Conference
on Secure and Trustworthy Machine Learning (SaTML), 2023.
[54] Y. Meng, L. Tang, F. Yu, J. Jia, G. Yan, P. Yang, Z. Xi, “Uncovering
vulnerabilities of llm-assisted cyber threat intelligence,” arXiv preprint
arXiv:2509.23573, 2025.
[55] R. Saul, J. Jiang, E. Chia, D. Wagner, “Trident: Improving malware
detection with llms and behavioral features,” arXiv preprint ar-
Xiv:2605.00297, 2026.
[56] A. Wen, N. A. Alzahrani, J. Jiang, A. Joe, K. Shieh, A. Zhang, B. Alo-
mair, D. Wagner, “Seedaichemy: Llm-driven seed corpus generation for
fuzzing,” arXiv preprint arXiv:2511.12448, 2025.
[57] L. Li, X. Yang, W. Wu, H. Wang, T. Ohtsuki, X. Fu, M. Pan, X. Shen,
“Mobillm: Enabling llm fine-tuning on the mobile device via server
assisted side tuning,” arXiv preprint arXiv:2502.20421, 2025.
[58] P. Sharma, H. Wen, V. Yegneswaran, A. Gehani, P. Porras, Z. Lin,
“Mobillm: An agentic ai framework for closed-loop threat mitigation
in 6g open rans,” arXiv preprint arXiv:2509.21634, 2025.
