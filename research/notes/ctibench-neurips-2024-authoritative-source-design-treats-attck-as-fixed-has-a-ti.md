---
title: 'CTIBench (NeurIPS 2024): authoritative-source design treats ATT&CK as fixed,
  has a time-controlled split for CVEs but none for ATT&CK'
id: ctibench-neurips-2024-authoritative-source-design-treats-attck-as-fixed-has-a-ti
tags:
- attack-ontology-drift-cti-85bc51
- cti-benchmarks
created: '2026-09-12T13:21:53.634510Z'
source: https://proceedings.neurips.cc/paper_files/paper/2024/file/5acd3c628aa1819fbf07c39ef73e7285-Paper-Datasets_and_Benchmarks_Track.pdf
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: CTIBench justifies its ATT&CK/NVD/CWE sourcing on reproducibility grounds
  while treating those versioned ontologies as fixed; it builds a 2021 time-controlled
  comparison split for CVE data but no equivalent for its 60-item ATT&CK task, and
  reports persistent LLM knowledge gaps specifically in ATT&CK.
---

# CTIBench (NeurIPS 2024 D&B, Spotlight) — the reference LLM-CTI benchmark

## What it is
Alam, Bhusal, Nguyen, Rastogi, *CTIBench: A Benchmark for Evaluating LLMs in Cyber Threat Intelligence*, NeurIPS 2024 Datasets & Benchmarks track (Spotlight), arXiv:2406.07599, proceedings PDF at proceedings.neurips.cc. The de-facto reference point that later LLM-CTI benchmarks (AthenaBench, CTIArena/CTIConnect, CTI-REALM) position against.

## What it says bearing on the query
Five task families: CTI knowledge MCQ, CVE→CWE root-cause mapping, CVSS severity prediction, **ATT&CK technique extraction (CTI-ATE)**, and **threat-actor attribution (CTI-TAA)**. The design principle the authors state is a commitment to publicly available *authoritative* sources — MITRE ATT&CK, NVD, CWE, FIRST CVSS — justified on grounds of **relevance, reproducibility and coverage**. That is the crux for this research query: authoritativeness is treated as equivalent to reproducibility, when in fact each of those sources is a **versioned, mutating ontology**, and the benchmark inherits whatever release happened to be live at scrape time.

The paper's own headline finding is the one that ontology drift predicts: LLMs show promise but have **persistent knowledge gaps in rapidly evolving domains like MITRE ATT&CK** (alongside CVSS overestimation and weak complex reasoning). The authors read this as a model-capability gap; it is at minimum partly a **label-space/version mismatch** between what the model absorbed in pretraining and the particular ATT&CK release frozen into the benchmark's prompts.

A methodologically telling design choice: CTI-RCM ships a **CTI-RCM-2021 comparison split** (1,000 items) alongside the main 1,000-item CTI-RCM split, explicitly to compare across time periods. So the authors already recognised temporal comparability as a problem *for CVE data* — and built a time-controlled split for it — while doing nothing equivalent for the ATT&CK-labelled tasks.

## Citable claims
- CTIBench = 4,610 released examples over 5 task families; the ATT&CK-labelled task is **60 items (1.3%)** while CVE/CWE/CVSS tasks are 4,000 items (87%).
- Stated source-selection rationale: authoritative public sources (ATT&CK, NVD, CWE, FIRST CVSS) chosen for relevance, reproducibility, coverage.
- Stated finding: persistent LLM knowledge gaps in rapidly evolving domains, MITRE ATT&CK named specifically.
- The benchmark has a time-controlled comparison split for **CVE** data (CTI-RCM-2021) but **none** for ATT&CK.
- Cited as: Advances in NeurIPS 37, pp. 50805–50825, 2024.

## Fidelity
**Mixed.** Repository-level facts (task counts, file layout, the 2021 split, the citation block) are ground truth from the cloned repo at `/home/user/ext/cti-bench`. The paper's stated design rationale and headline findings are at **summary fidelity** from search-result snippets — arxiv.org, proceedings.neurips.cc and dl.acm.org are egress-blocked in this environment, so I did not read the full text and no phrase here is a verified verbatim quotation. See the companion note on `cti-ate.tsv` for the measured label forensics.
