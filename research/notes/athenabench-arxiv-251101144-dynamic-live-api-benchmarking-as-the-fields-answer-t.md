---
title: 'AthenaBench (arXiv 2511.01144): dynamic live-API benchmarking as the field''s
  answer to CTIBench staleness'
id: athenabench-arxiv-251101144-dynamic-live-api-benchmarking-as-the-fields-answer-t
tags:
- attack-ontology-drift-cti-85bc51
- cti-benchmarks
created: '2026-09-12T13:21:06.173976Z'
source: https://arxiv.org/abs/2511.01144
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: AthenaBench explicitly diagnoses CTIBench as static-knowledge-limited and
  regenerates items from live MITRE ATT&CK and NVD APIs, fixing currency but removing
  any stable release identifier, and scores lowest exactly on the two ATT&CK-bookkeeping-exposed
  tasks (RMS 32.6, TAA 39.0).
---

# AthenaBench (arXiv:2511.01144) — the "dynamic benchmark" answer to CTIBench staleness

## What it is
Workshop paper (WAITI 2025) by Md Tanvirul Alam, Dipkamal Bhusal, Salman Ahmad, Nidhi Rastogi, Peter Worth — an explicit revision of CTIBench by largely the same authors. Repo: https://github.com/Athena-Software-Group/athenabench.

## What it says bearing on the query
AthenaBench is positioned as a fix for a defect the authors attribute to their own prior benchmark: CTIBench suffers from **static knowledge**, because its tasks are derived from fixed corpora, and in a fast-moving domain such benchmarks "risk becoming outdated and misaligned with the evolving cyber threat landscape." The stated remedies are (a) an improved dataset-creation pipeline, (b) **duplicate removal in the vulnerability datasets to reduce contamination risk**, (c) refined evaluation metrics, (d) a new **risk-mitigation-strategy (RMS)** task, and (e) generation of benchmark samples from **live CTI sources and APIs including MITRE ATT&CK and the NVD API**, so tasks stay current with minimal human supervision.

Headline result: proprietary LLMs lead overall but remain weak on the reasoning-heavy tasks — **threat-actor attribution and risk mitigation** — with open-source models further behind. The repo's own results table shows TAA topping out at 39.0 (GPT-5) and RMS F1 at 32.6 (GPT-5), against CKT 92.0 — i.e. the two tasks most exposed to ATT&CK's Groups/Mitigations bookkeeping are exactly the two where measured capability is lowest.

## Why this matters for an ontology-drift argument
This is the strongest existing acknowledgement in the LLM-CTI benchmark literature that ATT&CK-derived benchmarks decay. But the chosen fix is **currency, not comparability**: pulling items from a live ATT&CK API means each regeneration silently redefines the label space, so two AthenaBench runs months apart are no more comparable than CTIBench-vs-AthenaBench. Nothing in the paper's described design pins or reports a release identifier, and the released repo carries none (verified by grep). The gap this leaves open — *declare the release, diff the releases, re-score under a common label space* — is precisely the normalization-protocol contribution the research query asks about.

## Citable claims
- AthenaBench explicitly diagnoses CTIBench's ATT&CK/NVD-derived tasks as **static-knowledge-limited** and prone to going stale.
- Its remedy is live-API regeneration from MITRE ATT&CK + NVD, plus duplicate removal framed as **contamination reduction**.
- Reported best-model scores (repo README, full benchmark): CKT 92.0, ATE 76.2, RCM 71.6, VSP 85.4, **RMS 32.6, TAA 39.0**.

## Fidelity
**Summary fidelity.** arxiv.org is blocked by the egress proxy, so I did not read the PDF/HTML full text; the paper's positioning above is reconstructed from search-result snippets plus the repo README. No sentence here should be treated as a verbatim quotation from the paper. The score table and repo-derived statistics are ground truth from the cloned repository.
