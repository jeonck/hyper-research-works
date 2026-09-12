# Codebook: does the description change alter what the technique identifier denotes?

You will read pairs of MITRE ATT&CK technique descriptions. Each pair is the
same technique identifier (for example T1110) in two consecutive major releases,
release A (earlier) and release B (later). Your task is to judge, for each pair,
how much the **meaning** of the technique changed between A and B: does the
identifier still denote the same adversary behaviour, with the same boundaries?

You are rating meaning, not text volume. A long rewrite that says the same
thing is a low level. A one-sentence change that moves a boundary is a high
level. Do not count words, do not diff mechanically, read both descriptions and
ask what an analyst who tagged an observation with this identifier under
release A would have meant, and whether that observation is still correctly
tagged under release B.

## The scale

| Level | Name | The test |
|---|---|---|
| 0 | Cosmetic or editorial | The set of behaviours the identifier covers is identical, and no reader would learn anything new about the behaviour from B. Typography, whitespace, citation additions or renames, link retargeting, reordering of existing sentences, removal of non-descriptive boilerplate (detection guidance, platform lists, data-source lists) that does not describe the behaviour. |
| 1 | Clarification, scope unchanged | B explains the same behaviour better, or in more detail, or with new examples, tools, background or context, but every behaviour covered by A is still covered by B and nothing new is covered. An observation tagged under A would be tagged the same way under B, and the reverse. |
| 2 | Scope change | B adds, removes, narrows or broadens the behaviours the identifier covers. Some observations correctly tagged under A would no longer be tagged with this identifier under B, or some observations not covered under A now are. The core behaviour is recognisably the same one, but its boundary moved. |
| 3 | Redefinition | The identifier now denotes a different behaviour. The mechanism, the object acted on, or the purpose that defined the technique under A has been replaced, so that the core of what A described is no longer what B describes. A reader holding only B would not recover A's definition from it. |

## Decision rules

1. **Judge the boundary, not the length.** Ask: is there an observation that
   would be tagged with this identifier under A but not under B, or the reverse?
   If no, the level is 0 or 1. If yes, the level is 2 or 3.
2. **0 versus 1.** Level 1 requires that B tells the reader something about the
   behaviour that A did not (a new example, a new tool, a mechanism explained,
   a new platform illustrated as an instance of the same behaviour). If B only
   re-words, re-orders, re-cites or strips non-behavioural boilerplate, it is 0.
3. **1 versus 2.** New examples of the same behaviour are level 1. New
   *kinds* of behaviour, or the deletion of a kind of behaviour that A included,
   are level 2. Ask whether the new or removed material would have been
   correctly tagged with this identifier under A. If it would have been, the
   example merely illustrates the existing scope (level 1). If it would not
   have been, the scope moved (level 2). Adding a new platform or environment
   (cloud, containers, SaaS) as a place where the same behaviour occurs is
   usually level 2 if A's text confined the behaviour to another environment
   and level 1 if A was environment-neutral.
4. **2 versus 3.** Level 2 keeps the core: the same mechanism, object and
   purpose are still at the centre of B, with the edge moved. Level 3 replaces
   the core: the central mechanism, object or purpose of A is gone or demoted
   to an aside, and B is organised around something else. A renamed technique
   is a hint toward 3, not a rule. A technique whose text was split into
   sub-techniques, leaving a general parent, is 2 (narrowed or generalised),
   not 3, as long as the parent still denotes the family A described.
5. **Removed material.** Text removed from A counts as narrowing only if it
   described a behaviour that was covered. Removed detection guidance,
   mitigation guidance, platform lists, data-source lists, citations, and
   removed examples of behaviours that B still covers, do not narrow scope.
6. **Ignore everything you know about the releases.** Do not use the release
   numbers, the technique identifier, or your memory of ATT&CK to infer what
   MITRE intended. Rate the two texts in front of you.
7. **When torn between two levels,** choose the lower one and say why in the
   rationale. Disagreements are adjudicated afterward; a recorded reason is
   more useful than a guessed high level.
8. **Empty or near-empty description on one side.** If A or B is empty or a
   single sentence and the other side is substantive, judge what the identifier
   denotes on each side from what is there. A one-line statement of the same
   behaviour against a long treatment of it is 1, not 3.

## Worked examples

Each example is an item in the sample you will annotate, so you can check the
full texts. Excerpts are quoted; they are not the whole description.

### Level 0

**A075, "Shared Modules"** (T1129). The only change is that a space before a
citation marker is removed: `Win32 API. (Citation: Wikipedia Windows Library
Files)` becomes `Win32 API.(Citation: Wikipedia Windows Library Files)`. Nothing
about the behaviour is different. Level 0.

**A039, "Exfiltration Over Alternative Protocol"** (T1048). Release A ends with
a block that begins `Detection: Analyze network data for uncommon data flows
...` and continues with `Platforms: Linux, macOS, Windows Data Sources: User
interface, Process monitoring ...`. Release B drops that block and keeps the
behavioural text unchanged. More than half of the words are gone, but the
removed words are detection guidance and platform metadata, not a description
of adversary behaviour (rule 5). Level 0. This is the case that makes rule 1
matter: a large textual change that changes no meaning.

### Level 1

**A085, "Brute Force"** (T1110). B keeps A's definition and appends a
paragraph: `Brute forcing credentials may take place at various points during
a breach. For example, adversaries may attempt to brute force access to Valid
Accounts within a victim environment leveraging knowledge gathered from other
post-compromise behaviors ...`. This is context about when the behaviour
occurs and what it combines with. Every observation that was brute force under
A is brute force under B and nothing new is brute force. Level 1.

**A090, "Windows Management Instrumentation"** (T1047). B adds background (`WMI
is designed for programmers and is the infrastructure for management data and
operations on Windows systems`), an example command (`wmic.exe Shadowcopy
Delete`), a note that `wmic.exe` is deprecated, and mentions COM APIs as
another way to reach WMI. All of this illustrates or explains abuse of WMI,
the behaviour A already covered. Level 1. The added shadow-copy example is an
instance of executing a command through WMI, not a new kind of behaviour.

### Level 2

**A071, "Software Deployment Tools"** (T1072). A covers `third-party software
suites installed within an enterprise network, such as administration,
monitoring, and deployment systems`, with examples SCCM, HBSS, Altiris. B
re-centres the technique on `centralized software suites ... in an enterprise
network or cloud environment`, adds `AWS Systems Manager, Microsoft Intune,
Azure Arc, and GCP Deployment Manager`, adds `SaaS-based configuration
management services` that can run commands on cloud-hosted instances, and
mentions integration into CI/CD pipelines. An observation of an adversary
using a SaaS configuration manager to run commands on cloud instances would
not have been tagged T1072 from A's text; it is from B's. The core (abusing
enterprise-wide deployment tooling for lateral movement and execution) is the
same; the boundary broadened. Level 2.

**A046, "Time Based Evasion" to "Time Based Checks"** (T1497.003). A covers
two things: using time to detect a sandbox, and delaying execution (sleep
calls, scheduled tasks, ping loops, API hammering) to outlast automated
analysis. B removes the delaying behaviours entirely and keeps only the
checks (`enumerating time-based properties, such as uptime or the system
clock`, `GetTickCount`, `GetSystemTimeAsFileTime`). An observation of malware
sleeping for ten minutes before detonating was covered under A and is not
covered under B. The core that remains (time as a sandbox indicator) was
already central in A, so this is a narrowing, not a replacement. Level 2.

### Level 3

**A031, "DLL Side-Loading"** (T1574.002). Under A, side-loading is defined by
`hijacking the library manifest used to load DLLs`: the adversary exploits
`vague references in the library manifest of a program by replacing a
legitimate library with a malicious one`, and the vulnerability is located in
`Windows Side-by-Side (WinSxS) manifests`. Under B, the manifest mechanism is
gone; side-loading is now `planting then invoking a legitimate application
that executes their payload(s)` by `positioning both the victim application
and malicious payload(s) alongside each other`. The object acted on (a
manifest versus a co-located legitimate executable) and the mechanism changed.
An analyst who tagged a WinSxS manifest abuse as T1574.002 under A, and one who
tagged a dropped legitimate EXE plus malicious DLL under B, mean different
things by the identifier. Level 3.

**A045, "Exploitation for Defense Evasion" to "Exploitation for Stealth"**
(T1211). Under A, the technique is exploiting a vulnerability `to bypass
security features`, with the paradigm case being `defensive security software
that can be used to disable or circumvent them`, targeted after Security
Software Discovery. Under B, the purpose is `to evade detection by hiding
activity, suppressing logging, or operating within trusted or unmonitored
components`, and B states explicitly `Rather than directly disabling defenses,
adversaries may use exploitation to circumvent monitoring and logging
mechanisms`. Disabling security software, the core of A, is moved outside the
technique. The identifier now denotes exploitation whose purpose is
concealment rather than exploitation whose purpose is defeating a control.
Level 3. Contrast with A046: here the centre moved, there the edge moved.

## Recording your answer

For each item write one line: `item_id,level,rationale`, where level is 0, 1,
2 or 3 and the rationale is one sentence naming the boundary that did or did
not move. Rate every item. Do not skip, do not leave blanks, do not use half
levels.
