---
title: 'Virkud et al. (USENIX Sec 2024): EDR vendors disagree on ATT&CK labels within
  a single pinned version'
id: virkud-et-al-usenix-sec-2024-edr-vendors-disagree-on-attck-labels-within-a-singl
tags:
- attack-ontology-drift-cti-85bc51
- critique
created: '2026-09-12T13:21:27.913486Z'
source: https://www.usenix.org/conference/usenixsecurity24/presentation/virkud
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Same-behaviour detection rules from different vendors carry disjoint ATT&CK
  technique labels at a fixed ATT&CK v11 — a synchronic labelling-noise floor that
  may dominate cross-version drift.
---

## What it is
Peer-reviewed USENIX Security 2024 paper (Virkud, Inam, Riddle, Liu, Wang, Bates, Univ. of Illinois), with an artifact-evaluated (Available/Functional/Reproduced) code+data release. It analyses how three open detection rulesets — Splunk `security_content`, Elastic `detection-rules`, SigmaHQ — apply ATT&CK labels, against ATT&CK **v11** (the repo's `data/techniques.csv` is explicitly pinned to v11, snapshots taken October 2022).

## The criticism it makes
Two prongs, both hostile to ATT&CK-based analytics:
1. **Coverage is not a meaningful security metric.** Many techniques are *unrealizable* as detection rules, and "coverage of an ATT&CK technique does not consistently imply coverage of the same real-world threats." Reported coverage is inflated by low-severity rules; filtering to high-risk rules roughly halves it (to ~25-26%, per secondary summaries of the paper — I did not read the paper PDF itself).
2. **RQ3: "How consistently is ATT&CK applied?"** The authors cluster rules from different vendors that detect the *same* threat entity (37 entities had rules from >=2 products) and compare the ATT&CK labels attached.

## Strength of evidence
Strong, and I verified the core disagreement claim directly from the released artifact (cloned to `/home/user/ext/edr-attack`, notebook `code/RQ3 Analysis.ipynb` cell outputs). Two verbatim examples from the notebook outputs:
- **CVE-2021-4034 (PwnKit)**: Elastic rule `e69` is labelled `['Hijack Execution Flow (T1574)', 'Exploitation for Privilege Escalation (T1068)']`; Splunk rule `s489` for the same CVE is labelled `['Exploitation for Privilege Escalation (T1068)']`.
- **Named-pipe impersonation / Meterpreter `getsystem`**: Elastic `e479` is labelled `['Access Token Manipulation (T1134)']`; Splunk `s229`, describing the same `cmd.exe /c echo ... > \\.\Pipe\...` behaviour, is labelled `['Command and Scripting Interpreter (T1059)', 'Windows Command Shell (T1059.003)', 'Windows Service (T1543.003)', 'Create or Modify System Process (T1543)']` — **zero technique overlap** for the same behaviour.

## For or against the thesis
**Cuts both ways, and the "against" direction is the sharper one.**
- *For*: it establishes that ATT&CK labels attached to the same artefact are not stable across labellers, so any analytic whose ground truth is an ATT&CK label inherits that instability — exactly the validity problem the thesis is about.
- *Against (the strong rebuttal)*: this disagreement is measured **within one pinned ATT&CK version (v11)**. It is a *synchronic* labelling-noise floor that has nothing to do with version churn. If two vendors describing the same behaviour can share zero techniques at a fixed version, then the variance contributed by cross-version ontology drift may be a second-order term sitting on top of a much larger first-order human-mapping variance. A thesis that attributes analytic non-comparability primarily to *drift* must first bound this synchronic noise floor and show drift variance exceeds it — otherwise it is measuring the wrong drift.
- Methodologically it is also a rebuttal-by-example of the "everyone ignores versions" framing: the authors *did* pin a version and state it, which is precisely the reporting discipline the thesis wants to prescribe. It was already normal practice in a top-tier 2024 paper.

## Fidelity
High for the RQ3 label-disagreement examples (read directly from the released notebook outputs in the cloned artifact). Medium for the coverage percentages (25-26% figure comes from a web-search synthesis of the paper, not from the PDF, which I could not fetch — egress blocked). Paper PDF: https://www.usenix.org/system/files/usenixsecurity24-virkud.pdf ; artifact: https://github.com/avirkud/endpoint-detection-mitreattack
