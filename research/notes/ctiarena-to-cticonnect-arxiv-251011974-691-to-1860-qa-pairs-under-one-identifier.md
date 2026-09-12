---
title: 'CTIArena to CTIConnect (arXiv 2510.11974): 691 to 1,860 QA pairs under one
  identifier, same 9-task taxonomy'
id: ctiarena-to-cticonnect-arxiv-251011974-691-to-1860-qa-pairs-under-one-identifier
tags:
- attack-ontology-drift-cti-85bc51
- cti-benchmarks
created: '2026-09-12T13:21:53.902711Z'
source: https://arxiv.org/abs/2510.11974
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: 'One arXiv record carries two benchmark identities: CTIArena v1 with 691
  QA pairs and CTIConnect v2 (KDD 26) with 1,860 expert-verified pairs over the same
  9 tasks and 5 sources, a 2.7x growth from re-verification rather than new adversary
  intelligence, and a citation hazard mirroring ATT&CK''s own version instability.'
---

# CTIArena → CTIConnect (arXiv:2510.11974): the heterogeneous-CTI benchmark, and its own version instability

## What it is
One arXiv record, two identities. **v1 = "CTIArena: Benchmarking LLM Knowledge and Reasoning Across Heterogeneous Cyber Threat Intelligence"** (also on OpenReview, id E0AekM35XF); **v2 = "CTIConnect: A Benchmark for Retrieval-Augmented LLMs over Heterogeneous Cyber Threat Intelligence"**, accepted to **KDD '26** (Jeju, 9–13 Aug 2026). Peng Gao's lab (Virginia Tech); repo https://github.com/peng-gao-lab/CTIArena; project page https://cticonnect.github.io/.

## What it says bearing on the query
Both versions map the CTI-analysis landscape into **nine representative tasks across three categories**, spanning multiple heterogeneous authoritative sources that analysts must integrate (ATT&CK among them). The stated gap it fills: no prior benchmark evaluates LLMs in a **retrieval-augmented** setting with an evaluation harness granting access to the heterogeneous domain-knowledge sources analysts actually use.

The benchmark's own size changed materially between versions: **691 expert-grounded QA pairs (v1, CTIArena)** → **1,860 expert-verified QA pairs over 9 tasks and 5 heterogeneous CTI sources (v2, CTIConnect)**. That is a ~2.7× growth in a benchmark that kept the same task taxonomy, under a renamed identity, on the same arXiv id.

## Why this is directly on-topic
1. It is the strongest current evidence that **CTI benchmark "growth" is often bookkeeping rather than new intelligence** — a 691→1,860 jump with an unchanged 9-task structure, achieved by expansion and re-verification of the same source pool, not by the discovery of new adversary behaviour.
2. **Citation hazard**: two different numbers (691 vs 1,860) and two different names (CTIArena vs CTIConnect) live behind one identifier. Any paper reporting "CTIArena scores" without stating the version is unreproducible — the same instability the query alleges for ATT&CK, reproduced at the benchmark layer.
3. Its RAG framing shifts the failure mode: with retrieval over live ATT&CK, a model's score depends on **which ATT&CK snapshot the retriever indexed**, making the version pin a property of the harness, not the dataset.

## Citable claims
- CTIArena (v1): **691** high-quality QA pairs, 9 tasks, 3 categories, heterogeneous multi-source CTI, billed as the first benchmark for heterogeneous CTI under knowledge-augmented settings.
- CTIConnect (v2, KDD '26): **1,860** expert-verified QA pairs, **9 tasks, 5 heterogeneous CTI sources**, retrieval-augmented evaluation harness.
- Same arXiv id 2510.11974 carries both; the rename and the 2.7× size change are not distinguishable from a bare citation.

## Fidelity
**Summary fidelity throughout.** arxiv.org, openreview.net and people.cs.vt.edu are egress-blocked; the GitHub repo `peng-gao-lab/CTIArena` could not be cloned anonymously from this session (git asked for credentials) and is not reachable via the session's repo allowlist, so **I did not inspect its label files** and cannot state how its ATT&CK labels were built or whether it pins a release version. The 691/1,860/9-task/5-source figures come from search-result snippets of the two versions and are not verified verbatim quotations. Resolving the label-construction question for this benchmark is an open gap for a later batch with network access.
