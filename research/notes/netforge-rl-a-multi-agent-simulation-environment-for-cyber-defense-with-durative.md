---
title: 'NetForge RL: A Multi-Agent Simulation Environment for Cyber Defense with Durative'
id: netforge-rl-a-multi-agent-simulation-environment-for-cyber-defense-with-durative
tags:
- attack-ontology-drift-cti-85bc51
- pin-rate-survey
created: '2026-09-12T21:33:41.246851Z'
updated: '2026-09-12T21:44:24.608709Z'
source: https://arxiv.org/abs/2604.09523v3
source_domain: arxiv.org
fetched_at: '2026-09-12T21:33:41.241680Z'
fetch_provider: crawl4ai
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'arXiv 2604.09523v3 (2026): uses 5 ATT&CK technique-ID occurrences (with
  sub-techniques); ATT&CK release declaration classified as none.'
raw_file: raw/netforge-rl-a-multi-agent-simulation-environment-for-cyber-defense-with-durative.pdf
doi: arXiv:2604.09523v3
---

NetForge RL: A Multi-Agent Simulation Environment for Cyber Defense with Durative
Actions
Igor Jankowski
igorjankowwski@gmail.com
Training reinforcement-learning agents for cyber defense requires an environment that reflects
the operational setting: noisy, partial observations, several defenders coordinating across a network,
and an adaptive adversary realized through self-play. We present NetForge RL, a multi-agent
environment for this setting on procedurally generated enterprise and operational-technology (OT)
networks. A red agent compromises hosts with partial observability; three zone-split blue agents
defend from synthetic SIEM telemetry, Windows/Sysmon event logs encoded into dense embeddings
rather than a ground-truth state vector. The environment follows the PettingZoo parallel API with
fixed-shape observations and MITRE ATT&CK-mapped actions, ships five scenarios with named
difficulty presets and a held-out evaluation split, and replays deterministically under a seed. A JAX
backend vectorizes a reduced transition core, reaching 2.5 × 105 environment-steps/s at batch 4096
on CPU, as a fast surrogate for training-loop iteration. Alongside the environment we provide
reference baselines (scripted, a JAX IPPO trainer, and a self-play tournament), six diagnostic probes
that each measure one defensive skill, and an evaluation runner reporting 95% confidence intervals.
We describe the reproducibility engineering behind the environment and include a responsible-use
statement.
I.
INTRODUCTION
Cyber defense is a sequential decision problem under
partial observation, and a multi-agent one: several defend-
ers act across separate network zones against an attacker
that adapts [1]. It also exercises aspects of RL that toy
benchmarks omit: observations are partial and noisy,
credit is assigned over long horizons, objectives are asym-
metric, and the action space is large and grounded in real
tactics [2].
A cyber-RL environment must offer (i) a standard RL
API, (ii) observations based on the telemetry a defender
actually sees, (iii) throughput high enough for MARL
sample budgets, and (iv) reproducible replay under a
seed; existing open-source environments meet some but
not all (Section II).
We introduce NetForge RL to address these gaps
(Figure 1), covering the four requirements (i)–(iv) and
adding evaluation tooling on top:
• (i)
A
standard
multi-agent
API.
The
PettingZoo [3] parallel interface with Gymna-
sium [4] spaces, fixed-shape observations, and
per-agent action masks, checked by PettingZoo’s
parallel_api_test.
• (ii) Synthetic SOC telemetry. Blue agents read
SIEM logs (Windows/Sysmon XML) encoded into
an embedding; blue agents never see a ground-truth
array. A stochastic benign-traffic generator adds
background noise so alert volume alone is uninfor-
mative.
• (iii) A vectorized backend. A JAX [5] kernel
runs a reduced transition core under jax.vmap/jit,
verified against a NumPy reference; it is a through-
put surrogate with a coarser observation than
the Python engine (Section V), and we report
environment-steps and agent-steps separately.
• (iv) Reproducibility. Per-episode RNGs, reseeded
telemetry, and deterministic timestamps make re-
wards and observations replay under a seed, guarded
by a golden-trajectory test.
• Evaluation tooling. Scripted, JAX IPPO, and
self-play baselines reported with 95% confidence
intervals, and six probes that score distinct defensive
capabilities.
Our contribution is the environment and its evaluation
tooling; training reference RL policies to convergence
across all scenarios is future work (Section IX). Section VII
states the environment’s scope and what it does not yet
model.
II.
RELATED WORK AND POSITIONING
Cyber-defense RL environments.
Open-source
cyber-RL environments cluster into a few families. Attack-
graph abstractions model an attacker traversing a network
from structured state: NASim [6] is a compact single-
agent POMDP with one-hot features, and CyberBat-
tleSim [7] an abstract single-agent attack graph, since
extended to continuous embedding spaces [8] and to mul-
tiple operation agents [9]. Operations gyms such as Cy-
bORG [10] and its CAGE challenges [11] provide curated,
turn-based red/blue tasks with structured observations.
Emulation frameworks such as CSLE [12] run scenarios
on real virtualized infrastructure for high fidelity, trad-
ing away throughput. Separately, ns3-gym [13] wraps a
network simulator as a Gym environment for networking
research rather than defense.
arXiv:2604.09523v3  [cs.LG]  15 Jul 2026


---

2
Agents
red + 3 blue zones
Action registry
instantiate, mask,
cost, duration
Event queue
resolve at t+d
Conflict resolver
defensive priority
Global
state
SIEM logger
+ benign traffic
Sysmon/Win events
Observations
+ rewards
LogEncoder
TF-IDF →SVD
act
apply
encode
observe
FIG. 1. The NetForge execution loop. Each step instantiates masked actions, queues them with per-action durations, resolves
simultaneous red/blue effects, applies state deltas, synthesizes SIEM telemetry (mixed with benign-traffic noise), encodes it, and
returns fixed-shape observations and rewards to the agents.
Few of these combine a native multi-agent API, obser-
vations built from log telemetry rather than ground-truth
state, and a batched backend fast enough for modern
sample budgets. NetForge combines them (Table I). The
table reports capabilities, not quality: each environment
has strengths NetForge lacks, for instance CybORG’s
curated task designs and CSLE’s emulation fidelity.
Accelerated backends and MARL benchmarks.
Executing the transition function on accelerators via
JAX [5] yields large sample budgets, as Brax shows for
rigid-body physics [14]. NetForge applies this to a cyber-
defense transition core while keeping a Python engine
(event queue, telemetry, command-list effects) for single-
environment rollouts. Our evaluation conventions follow
cooperative MARL benchmarks such as SMAC [15]: fixed-
shape observations, per-agent action masks, and results
reported as distributions over seeds.
III.
ENVIRONMENT DESIGN
NetForge RL models a red team compromising a gener-
ated network and a zone-split blue team detecting, isolat-
ing, and remediating hosts.
A.
Agents, Formulation, and API
The environment is a partially observable, general-
sum
stochastic
game
with
a
fixed
set
of
four
agents: red_operator, blue_dmz, blue_internal, and
blue_restricted.
It implements the PettingZoo
ParallelEnv contract: reset(seed) returns per-agent
observations and infos, and step(actions) returns per-
agent observations, rewards, terminations, truncations,
and infos. Each blue agent owns a topological zone (DMZ,
internal/corporate, restricted/secure) and receives SIEM
telemetry filtered to that zone plus a shared blue channel;
the red agent operates under partial observability, seeing
only hosts it has discovered. Listing 1 shows a complete
rollout.
Each
agent’s
action
space
is
MultiDiscrete([32, 100]):
the
first
component
selects one of up to 32 action types, the second a target
host index among 100 slots. The action_mask is the
Listing 1. A full PettingZoo rollout of NetForge RL.
import numpy as np
from netforge_rl.environment.parallel_env \
import NetForgeRLEnv
env = NetForgeRLEnv(
{"scenario_type": "ransomware",
"max_ticks": 200})
obs, infos = env.reset(seed=0)
while env.agents:
actions = {}
for a in env.agents:
m = obs[a]["action_mask"] # 32 types|100 targets
actions[a] = np.array([
np.random.choice(np.flatnonzero(m[:32])),
np.random.choice(np.flatnonzero(m[32:]))])
obs, rewards, terms, truncs, infos = \
env.step(actions)
flat concatenation of a 32-bit type mask and a 100-bit
target mask (Table II). The observation space is a Dict
with fixed shapes so neural policies need no per-topology
reshaping (Table II). We pad the topology to exactly
100 host slots, of which 15–30 are active, avoiding a
variable-size representation.
Padding slots sit on the
reserved, non-routable 169.254.0.0/16 subnet.
The
per-step action_mask zeroes any action targeting a
padding slot, so an agent cannot act on padding and
need not learn the address range. Padding features are
constant and shift with the active set under churn: they
cost observation width but leak no episode-specific signal,
and we exclude them from all reported metrics.
B.
Synthetic SIEM Telemetry
Rather than exposing ground-truth compromise flags,
NetForge renders each consequential interaction as a
realistic Windows Event / Sysmon XML record (e.g.,
EventID 4624 logon, 4625 failed logon, Sysmon 1 pro-
cess creation, Sysmon 10 LSASS access). A SIEMLogger
buffers these into a rolling window, and a LogEncoder
converts them into a dense R128 embedding: a character n-
gram TF-IDF vectorizer projected by Truncated SVD and
L2-normalized. Treating each record as character n-grams
keeps the encoder agnostic to log schema and portable
to real, semi-structured log streams, at the cost of not


---

3
TABLE I. Positioning of NetForge RL relative to representative open-source cyber-RL environments. “Multi-agent” means a
native multi-agent RL API; “SIEM-like obs” means the observation is encoded log telemetry, not a raw state vector; “Vectorized
backend” means a batched/accelerator execution path.
Environment
Multi-agent API SIEM-like obs Procedural topo. Vectorized backend Standard RL API
NASim [6]
No
No
Partial
No
Gym
CyberBattleSim [7]
No
No
Yes
No
Gym
C-CyberBattleSim [8]
No
No
Yes
No
Gym
CybORG / CAGE [10]
Limited
No
Partial
No
Gym-like
CSLE [12]
Limited
Partial
Yes
No
Gym-like
NetForge RL (ours)
Yes
Yes
Yes
Partial (JAX core)
PettingZoo
TABLE II. Per-agent observation dictionary (fixed shapes).
Blue agents receive an additional blue_comm channel carrying
shared situational awareness.
Key
Shape
Meaning
obs
R256
Local host/zone features
action_mask
{0, 1}132 Legal types (32) + targets (100)
siem_embedding R128
Mean of recent zone SIEM logs
adj_matrix
R10000
Flattened 100×100 reachability
delta_t
R1
Normalized time since last step
blue_comm
R100
Shared blue awareness (blue only)
Event XML
4624
LogEncoder
TF-IDF→SVD
Zone window
last 8 logs
siem_emb
∈R128
ingest
encode
pool
FIG. 2. The SIEM observation pipeline. Actions emit Win-
dows/Sysmon event logs, which are encoded and zone-filtered
into a fixed-size embedding. A stochastic benign-traffic gener-
ator adds background events to the same buffer.
exploiting the categorical field structure a schema-aware
encoder could. Blue agents observe the mean embed-
ding of the eight most recent logs in their zone, forcing
log-based reasoning over telemetry (Figure 2).
Benign-traffic generator (false positives).
To
prevent the degenerate policy of isolating every host,
a stochastic benign-traffic generator injects background
events (logins, decoy traffic) into the SIEM buffer each
tick. Because these flow through the same pipeline as
adversarial events, the defender must learn to discriminate
true indicators from noise rather than thresholding on
volume. These events are written straight to the SIEM
buffer as telemetry; they do not pass through the event
queue (Section III C).
C.
Action Taxonomy and Durative Timing
Actions are grounded in the MITRE ATT&CK cor-
pus [16]. Each agent belongs to exactly one team (red or
blue), and a single action registry exposes every registered
action to that team’s live agents. The blue repertoire
spans detection, containment, remediation, and deception
(monitoring, endpoint analysis, EDR deployment, honey-
TABLE III. Representative actions with MITRE mappings,
energy cost, and duration in ticks.
Red gains and pivots
privilege; blue detects, contains, and remediates. Red rows cite
ATT&CK techniques; blue rows cite ATT&CK Mitigations
(M) or D3FEND defensive techniques (D3-).
Action
Team ATT&CK Cost Dur. Effect
DiscoverNetworkServices Red
T1046
2
3
Port scan; enables exploit
ExploitRemoteService
Red
T1210
5
5
RCE (User)
ExploitEternalBlue
Red
T1210
4
6
SMB RCE
DumpLSASS
Red
T1003.001
1
2
Steal cred. tokens
PassTheTicket
Red
T1550.003
1
1
Token-gated pivot
Monitor
Blue
M1047
2
2
Alert on elevated hosts
Analyze
Blue
M1049
1
1
Reveal IoCs (needs EDR)
IsolateHost
Blue
M1030
1
1
Sever host, drop sessions
DeployHoneytoken
Blue
D3-DUC
5
1
Plant deceptive creds
RotateKerberos
Blue
M1015
50
4
Global token flush
tokens) alongside the red attack actions; a reachability
test verifies that every registered action is instantiable by
some agent. In total the environment registers 20 red and
16 blue action types (Table III lists representatives). Each
red action carries its ATT&CK technique, so an episode
reports which techniques the attacker actually exercised
and the fraction of the mapped taxonomy it covered.
Actions have durations and are queued: an action
started at tick t with duration d resolves at t + d, and a
blue isolation of a host aborts an in-flight red action tar-
geting it (Figure 3). An action emits its SIEM telemetry
when it resolves, not when it is submitted, so an in-flight
action is not yet visible; a defender pre-empts an exploit
through earlier resolved signals such as the reconnaissance
that precedes it, not by observing the exploit mid-flight.
This gives actions their durative, delayed-effect character
while keeping the API a standard per-step interface (the
normalized time gap is exposed as delta_t). Each agent
may have at most one action in flight: submitting a new
one is blocked until the previous action resolves, so red
and blue bandwidth are both bounded by the same mech-
anism. A conflict resolver grants defensive priority when
red and blue effects land on the same tick.
D.
Token-Gated Routing
Reachability is not free: the state engine enforces zone-
based routing gated on a stolen access token.
Enter-
ing the Secure subnet requires the red agent to hold


---

4
tick
0
1
2
3
4
5
6
ExploitRemoteService (d=5)
aborted
IsolateHost
isolation cancels
the in-flight exploit
Red
Blue
FIG. 3. Durative timing. A red exploit submitted at t=0 (du-
ration 5) would resolve at t=5, but a blue isolation submitted
at t=2 matures one tick later and cancels the in-flight exploit
at t=3, so the earlier-maturing action wins and timing decides
the outcome.
Internet
DMZ
Web/Mail
Corporate
DC (tokens)
Secure
PII/OT [token]
ingress
pivot
token
FIG. 4. Token-gated routing. Traversal into the Secure zone
requires a cryptographic token the red team must steal and
can lose to a blue key rotation.
an Enterprise_Admin_Token, which must be stolen
(via DumpLSASS) and used (via PassTheTicket); a blue
RotateKerberos flushes stolen tokens and revokes that
mobility (Figure 4, abstracted; see Section VII), so reach-
ing the Secure zone takes a multi-step attack chain.
E.
Scenarios and Procedural Topologies
NetForge ships five scenario families that differ in ob-
jective and reward structure: ransomware (mass compro-
mise/encryption), apt_espionage (stealthy persistence
and exfiltration), cloud_hybrid (protect a Secure zone),
iot_grid (protect grid controllers), and ot_stuxnet (pre-
vent physical PLC destruction).
Topologies
are
generated
procedurally
by
NetworkGenerator:
3–5 subnets,
per-host OS/ser-
vice/CVE/credential profiles, decoys, and an optional
OT subnet.
Training draws from arbitrary seeds;
setting evaluation_mode=True draws from a disjoint
held-out seed pool (offset 1000) that is never seen during
training, giving a clean train/generalization split, and
a frozen 20-seed evaluation suite fixes the reporting
set. Difficulty is exposed as three named presets (easy,
medium, hard) that vary network size, SIEM telemetry
delay, and dynamic topology churn (host arrival, DHCP
reallocation), so difficulty and the evaluation split are
reproducible and documented. A curriculum wrapper
additionally advances difficulty by a reward threshold for
non-stationarity studies.
F.
Reward Function Design
Every scenario shares one reward shape and differs only
in its weights. Each step, an agent’s reward is a shared
action-cost penalty (proportional to the action’s energy
cost) plus a team-specific sum of weighted terms, each
tied to a discrete state transition, for example a privi-
lege gain, a correct or a false-positive isolation, a decoy
deployment, or a kinetic-destruction event. Transitions
are read through the same iter_host_deltas helper as
the metrics (Section IV). The weights themselves are a
plain lookup table per scenario and per team: ransomware
blue, for instance, earns +5 for correctly isolating a com-
promised host and −2 for isolating a clean one, while
the OT-safety scenarios (ot_stuxnet, iot_grid) score a
PLC’s kinetic destruction as +104 to red and −104 to
blue. The ±104 term belongs to the shared shape but its
weight is zero in every non-OT scenario, so catastrophic
physical outcomes dominate the return only where a PLC
exists. Because the weights are data, the environment-
specification generator emits them verbatim (Section X).
Raw rewards are not comparable across scenarios, since
each defines its own scale; a tanh-normalized reward in
[−1, 1] is provided for cross-scenario reporting.
IV.
REPRODUCIBILITY AND DETERMINISM
Benchmark validity depends on two properties: rewards
must be independent of internal effect encodings, and
episodes must replay identically under a seed.
Encoding-invariant rewards. An action can express
its effect as a state delta or as a command list; rewards
and metrics must not depend on which. Both forms are
read through one normalization pass, and a test asserts
that the two encodings of a privilege gain score identically.
The JAX backend omits command-list effects, so the
question does not arise there (Section V).
Seeded replay. Every source of randomness is per-
episode and seed-derived: a per-episode RNG drives all
stochastic actions, each stateful component is reseeded on
reset(seed), and log timestamps advance from a seeded
epoch, never the wall clock. Observations, embeddings,
infos, and rewards therefore replay bit-for-bit for a fixed
seed and differ across seeds. A golden-trajectory finger-
print and a full observable-stream hash guard this, the
latter also checking that two environments interleaved in
one process stay independent. The suite (342 tests) covers
the PettingZoo API contract, reward-encoding invariance,
seeded replay, per-scenario termination, and JAX/NumPy
parity, and gates continuous integration.
V.
JAX BACKEND
The Python engine runs one environment per instance.
For the sample budgets MARL needs, NetForge provides a


---

5
states
B×
vmap(step)
jit on device
next
+ reward
FIG. 5. The vectorized backend maps one jit-compiled transi-
tion across a batch of B environment states (stacked cards)
with jax.vmap, producing the next states and rewards without
leaving the accelerator.
JAX-vectorized backend that implements a reduced tran-
sition core (host privilege/status, reachability, scenario
rewards, action masks) as pure functions under jax.vmap
and jax.jit (Figure 5), verified against a NumPy refer-
ence by a trajectory-level parity test. The JAX core keeps
the Python engine’s action-timing semantics: each agent
has one action in flight and cannot submit another until
it resolves, and a Blue IsolateHost that matures on a
tick cancels a still-pending Red action on the same host,
with same-tick ties favoring Blue. It does not replicate
the Python engine’s event-driven tick-skipping: the vec-
torized backend advances one tick per step() rather than
jumping to the next event, a fixed-cadence rendition of
the same timing. In place of the full SIEM text pipeline
(synthesized Windows/Sysmon XML through TF-IDF),
a pure, jit-compatible function computes a per-host
alert scalar in [0, 1] directly from host state (compromise,
privilege, honeytoken, decoy, EDR coverage). The JAX
backend thus does not produce the R128 siem_embedding
of Table II at all; each host instead carries a single alert
value. The two backends thus agree on host state, reacha-
bility, reward, and action timing, but not on tick cadence
or on the shape and meaning of the observation. The JAX
core is therefore for throughput iteration on the train-
ing machinery (debugging a loop, estimating a compute
budget), not for developing observation-dependent policy
behavior: policies do not transfer between backends, and
full-fidelity results in this paper use the Python engine.
We report throughput distinguishing environment-steps
(one batched transition) from agent-steps (environment-
steps × number of agents), because conflating them in-
flates numbers by the agent count. On a single laptop-
class CPU (6 cores/12 threads, no GPU; Figure 6), the
JAX core reaches 2.5 × 105 environment-steps/s and
1.0×106 agent-steps/s at batch 4096. The single-instance
Python engine, which additionally runs the SIEM text
pipeline, event queue, and command-list effects, sustains
≈144 environment-steps/s on the same machine. Because
the two backends do different work per step, we report
each as the cost of its own execution path rather than a
speedup of one over the other; these numbers characterize
scaling on commodity CPU hardware.
1
64
256
1024
4096
102
104
106
298
17k
63k
203k
249k
batch size B
env-steps/s (log)
FIG. 6.
JAX-backend environment-step throughput (log
scale) versus batch size on a single laptop-class CPU
(6 cores/12 threads, no GPU), 50 steps with 2 warmup it-
erations. Throughput rises from ≈300 env-steps/s at B=1 to
2.5 × 105 at B=4096 as the fixed compilation amortizes over
more environments. The single-instance Python engine, which
runs the full SIEM text pipeline, event queue, and command-
list effects, sustains ≈144 env-steps/s on the same machine
(Section V).
VI.
METRICS, BASELINES, AND
DIAGNOSTICS
Metrics. Beyond episodic return, the environment
reports operational metrics in the info dictionary, all
computed over active hosts only (padding excluded): SLA
uptime, count of compromised and isolated hosts, mean
time to containment (MTTC), detection rate, total exfil-
trated data, a deception-efficacy ratio (the fraction of red
actions that struck a decoy or honeytoken), and ATT&CK
technique coverage. These let a study distinguish surgical
defense from the degenerate failure mode where an agent
minimizes compromise by destroying network utility.
Reference baselines. We provide mask-aware ran-
dom and rule-based heuristic red/blue policies, a scripted
kill-chain attacker, a JAX IPPO trainer, and a bench-
mark runner (python -m benchmarks.run_benchmark)
that sweeps scenarios and seeds and reports each met-
ric as a mean with a 95% confidence interval, with
a train-vs-held-out generalization-gap mode.
Because
ExploitRemoteService requires a prior service-discovery
action on its target, a naive heuristic red that fires ex-
ploits without reconnaissance never compromises any-
thing, and the benchmark looks deceptively quiet. A
scripted kill-chain that recons before exploiting and ex-
pands its foothold across zones produces a non-trivial
operating point (Table IV). We also include a JAX IPPO
trainer whose entire rollout (environment step, observa-
tion, policy, and advantage estimation) runs on-device;
a committed 40-iteration run on ransomware (≈246k
environment-steps, about a minute on CPU) improves
mean blue reward from 0.13 to 0.71. Because this run is
on the JAX surrogate with its scalar alert signal, it con-
firms only that the mechanics and rewards are learnable
there, not that a policy can master the full R128 SIEM
telemetry of the Python engine. A self-play tournament


---

6
TABLE IV. Scripted red baselines against a heuristic blue
defender (10 seeds, 150 ticks; active hosts only). A recon-free
heuristic attacker never lands an exploit; the kill-chain attacker
compromises hosts and suppresses SLA, giving the benchmark
a non-trivial operating point.
Red policy
Mean compromised SLA uptime
Random
≈0.0
≈100%
Heuristic (no recon)
0.0
100%
Kill-chain (recon+pivot)
2.3
90.4%
rates every red and blue policy on a single Elo ladder via
a fractional update: each match’s Elo score is Blue’s mean
SLA uptime as a continuous share in [0, 1] rather than a
discrete win/loss, with Red scored as the complementary
share. These baseline implementations serve as functional
demonstrations rather than state-of-the-art benchmark
evaluations.
Diagnostics. Because aggregate return hides why a
policy succeeds or fails, NetForge ships a suite of six di-
agnostic probes, each isolating one defensive capability:
memory (act on a foothold planted at reset), attention
(find one true alert amid heavy noise), temporal reasoning
(contain an intrusion under a delayed SIEM feed), preci-
sion (avoid isolating clean hosts), safety (protect an OT
host from kinetic destruction), and generalization (contain
a target while the topology churns). Each probe returns
a score in [0, 1], and a capability card aggregates the suite
across seeds into a per-policy radar chart (Figure 7), giv-
ing a per-capability profile of each policy instead of one
scalar.
Each probe stresses a specific channel and is not a
trivial integration check: the Attention probe plants the
one true indicator among equal-severity decoy alerts, the
Temporal probe delays telemetry by a fixed number of
ticks, and every probe penalizes false-positive isolations,
not only rewards correct ones. Because the policies key on
the SIEM alert stream, these stresses bite. The reference
heuristic contains clearly-signalled footholds (memory,
safety, generalization) but drops to 0.50 on attention,
where the decoys draw false-positive isolations, and to 0.79
on temporal, where the delayed feed sets back its response.
The random policy scores near zero except on precision,
where inaction is safe, and partly on generalization, where
a chance isolation occasionally lands. The suite thus ranks
policies by how well they act on degraded telemetry.
VII.
LIMITATIONS
NetForge is a simulation and its dynamics have not been
validated against real network telemetry or live red-team
engagements; results do not transfer to operational sys-
tems without further study. Exploit success is abstracted,
not executed. The trainer’s demonstration is a single-
scenario learning curve, not a multi-seed, multi-scenario
sweep, and the six probes are validated mainly against
Memory
Attention
Temporal
Precision
Safety
General.
0.5
1
Heuristic blue
Random
FIG. 7.
Validating the diagnostic probes (5 seeds):
per-
capability scores for a SIEM-reading heuristic and a random
defender. The two profiles separate along most axes (preci-
sion excepted, where inaction alone scores well), showing the
probes distinguish a competent policy from a trivial one; the
card is meant to profile trained policies (future work), not to
rank these two.
scripted policies so far. Several mechanics are deliberate
abstractions: the benign-traffic generator writes to the
SIEM buffer directly, so its noise bypasses the action-
duration and preemption mechanics; RotateKerberos re-
vokes routing to already-held Secure hosts, an abstraction
of a real ticket rotation that invalidates future authenti-
cation without severing a live session; the fixed 100-slot
encoding pads the 100×100 reachability matrix to 104
mostly-zero entries for 15–30 active hosts, wasteful for
dense policies; and the generator’s benign background
is a simple template mix that a text encoder can partly
separate by vocabulary, so adversarially-matched noise
remains future work (Section IX).
VIII.
RESPONSIBLE USE
NetForge trains attacker as well as defender policies
but contains no operational exploit code and cannot act
on real systems: exploit outcomes are CVSS-weighted
probabilities over vulnerability flags, and CVE identifiers
are abstract labels, so trained red policies confer no real-
world offensive capability. Users must not connect the
environment to production infrastructure, and a datasheet
documents its generation, intended uses, and limitations.
IX.
FUTURE WORK
• Stronger baselines. A multi-seed, multi-scenario
sweep of IPPO, MAPPO, and an LLM SOC agent


---

7
with confidence intervals across all five scenarios,
replacing the current single-scenario curve, and val-
idating the six diagnostic probes on trained and
LLM policies rather than scripted baseline only.
• Continuous-time architectures. CT-GMARL,
an ODE-RNN graph architecture for multi-agent
defense over dynamic network topologies, modelling
the environment’s durative, event-driven timing di-
rectly rather than through the fixed-cadence, fixed-
shape encoding used here.
• A richer environment. More scenario and topol-
ogy variety, an expanded diagnostic-probe suite, a
frozen versioned benchmark specification, graph or
sparse-matrix observations to replace the padded ad-
jacency, and GPU/TPU-scale throughput alongside
the current CPU numbers.
• Comparison with real networks. Validating the
simulated dynamics against real network telemetry
or a red-team engagement (closing the gap named
in Section VII), and a quantitative related-work
comparison in place of the qualitative positioning
in Table I.
X.
AVAILABILITY
NetForge RL is open source at https://github.
com/reforcemind/NetForge_RL, with documentation at
https://reforcemind.github.io/NetForge_RL/. The
package
installs
via
pip,
exposes
the
PettingZoo
API shown in Listing 1,
ships the JAX backend,
benchmark scripts, and documentation, and includes
the automated test suite that gates continuous in-
tegration.
An environment-specification generator
(benchmarks/env_spec.py) emits a machine-readable de-
scription of the agents, spaces, observability model, termi-
nation conditions, and reward decomposition to support
reproducible comparison.
[1] R. Lowe, Y. Wu, A. Tamar, J. Harb, P. Abbeel, and
I. Mordatch, in Advances in Neural Information Process-
ing Systems (NeurIPS), Vol. 30 (2017).
[2] A. Applebaum, D. Miller, B. Strom, C. Korban, and
R. Wolf, in Proceedings of the 32nd Annual Conference
on Computer Security Applications (ACSAC) (2016) pp.
363–373.
[3] J. Terry, B. Black, N. Grammel, M. Jayakumar, A. Hari,
R. Sullivan, L. S. Santos, C. Dieffendahl, C. Horsch,
R. Perez-Vicente, et al., in Advances in Neural Informa-
tion Processing Systems, Vol. 34 (2021) pp. 15032–15043.
[4] M. Towers, A. Kwiatkowski, J. Terry, J. U. Balis, et al.,
arXiv preprint arXiv:2407.17032 (2024).
[5] J. Bradbury, R. Frostig, P. Hawkins, M. J. Johnson,
C. Leary, D. Maclaurin, G. Necula, A. Paszke, J. Van-
derPlas, S. Wanderman-Milne, and Q. Zhang, JAX: com-
posable transformations of Python+NumPy programs,
http://github.com/jax-ml/jax (2018).
[6] J. Schwartz and H. Kurniawati, NASim:
Network
attack
simulator,
https://networkattacksimulator.
readthedocs.io/ (2019).
[7] Microsoft Defender Research Team, Cyberbattlesim,
https://github.com/microsoft/CyberBattleSim
(2021).
[8] F. Terranova, A. Lahmadi, and I. Chrisment, in Interna-
tional Symposium on Research in Attacks, Intrusions and
Defenses (RAID) (2025).
[9] T. Kunz, C. Fisher, J. La Novara-Gsell, C. Nguyen, and
L. Li, in International Conference on Computational Sci-
ence and Computational Intelligence (CSCI) (2023).
[10] M. Standen, D. Bowman, J. Richer, et al., arXiv preprint
arXiv:2108.09118 (2021).
[11] TTCP CAGE Working Group, CAGE Challenge 2, Tech.
Rep. (TTCP, 2022).
[12] K. Hammar and R. Stadler, CSLE: A framework for
building self-learning cyber-security systems, https://
github.com/Kim-Hammar/csle (2023).
[13] P.
Gawłowicz
and
A.
Zubow,
arXiv
preprint
arXiv:1810.03943 (2018).
[14] C. D. Freeman, E. Frey, A. Raichuk, S. Girgin, I. Mor-
datch, and O. Bachem, arXiv preprint arXiv:2106.13281
(2021).
[15] M. Samvelyan, T. Rashid, C. S. de Witt, G. Farquhar,
N. Nardelli, T. G. J. Rudner, C.-M. Hung, P. H. S.
Torr, J. Foerster, and S. Whiteson, arXiv preprint
arXiv:1902.04043 (2019).
[16] B. E. Strom, A. Applebaum, D. P. Miller, K. C. Nickels,
A. G. Pennington, and C. B. Thomas, MITRE ATT&CK:
Design and Philosophy, Tech. Rep. (The MITRE Corpo-
ration, 2018).
