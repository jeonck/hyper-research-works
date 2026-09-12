---
title: 'Case study: the ATT&CK v19.0 revocation wave'
id: case-study-the-attck-v190-revocation-wave
tags:
- attack-ontology-drift-cti-85bc51
- measurement
created: '2026-09-12T13:21:28.408176Z'
source: https://github.com/mitre-attack/attack-stix-data
status: draft
type: note
tier: ground_truth
content_type: dataset
deprecated: false
summary: v19.0 revoked 17 live techniques including the T1562 family, hitting 52 of
  168 group profiles
---

# Case study — the ATT&CK v19.0 revocation wave

Fidelity: PRIMARY ARTEFACT (computed from the v18.1 and v19.2 STIX bundles).

Between v18.1 and v19.2, 17 techniques that were live were revoked and replaced:

| revoked | name | replaced by | `uses` edges at v18.1 | usage rank |
|---|---|---|---|---|
| T1070.001 | Clear Windows Event Logs | T1685.005 | 40 | 98 of 599 |
| T1070.002 | Clear Linux or Mac System Logs | T1685.006 | 8 | 272 of 599 |
| T1562 | Impair Defenses | T1685 | 5 | 354 of 599 |
| T1562.001 | Disable or Modify Tools | T1685 | 110 | 33 of 599 |
| T1562.002 | Disable Windows Event Logging | T1685.001 | 6 | 324 of 599 |
| T1562.003 | Impair Command History Logging | T1690 | 10 | 253 of 599 |
| T1562.004 | Disable or Modify System Firewall | T1686 | 45 | 92 of 599 |
| T1562.006 | Indicator Blocking | T1685 | 10 | 247 of 599 |
| T1562.007 | Disable or Modify Cloud Firewall | T1686.001 | 1 | 580 of 599 |
| T1562.008 | Disable or Modify Cloud Logs | T1685.002 | 2 | 470 of 599 |
| T1562.009 | Safe Mode Boot | T1688 | 7 | 285 of 599 |
| T1562.010 | Downgrade Attack | T1689 | 3 | 430 of 599 |
| T1562.011 | Spoof Security Alerting | T1685.003 | 0 | None of 599 |
| T1562.012 | Disable or Modify Linux Audit System | T1685.004 | 1 | 561 of 599 |
| T1562.013 | Disable or Modify Network Device Firewall | T1686.002 | 2 | 488 of 599 |
| T1656 | Impersonation | T1684.001 | 12 | 234 of 599 |
| T1672 | Email Spoofing | T1684.002 | 0 | None of 599 |

Blast radius measured on the v18.1 graph:

- group→technique edges referencing a revoked identifier: 84
- software→technique edges: 155
- mitigations: 47
- detection relationships: 17
- groups whose technique profile loses at least one identifier: 52 of 168

This is the counter-example to the claim that ATT&CK identifier churn ended with
the v7.0 sub-technique restructuring. It happened in the most recent release, and
it landed on one of the most heavily referenced technique families in the
knowledge base.