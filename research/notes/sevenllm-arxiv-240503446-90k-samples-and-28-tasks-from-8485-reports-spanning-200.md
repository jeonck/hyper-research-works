---
title: 'SEvenLLM (arXiv 2405.03446): 90k samples and 28 tasks from 8,485 reports spanning
  2004-present, with no ATT&CK label spine'
id: sevenllm-arxiv-240503446-90k-samples-and-28-tasks-from-8485-reports-spanning-200
tags:
- attack-ontology-drift-cti-85bc51
- cti-benchmarks
created: '2026-09-12T13:23:19.238529Z'
source: https://arxiv.org/abs/2405.03446
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Largest LLM-CTI benchmark in this batch, built from 6,706 English plus 1,779
  Chinese curated reports into ~90,000 instruction samples over an unversioned 28-task
  taxonomy with no external referent; a clean case of dataset growth by task multiplication,
  and its ATT&CK labelling status could not be established.
---

# SEvenLLM (arXiv:2405.03446) — bilingual multi-task CTI benchmark built without an ATT&CK label spine

## What it is
*SEvenLLM: Benchmarking, Eliciting, and Enhancing Abilities of Large Language Models in Cyber Threat Intelligence* (2024). Produces **SEvenLLM-Instruct** (instruction corpus) and **SEvenLLM-Bench** (evaluation set).

## What it says bearing on the query
Construction: over ten thousand cybersecurity incident pages were harvested from leading domestic (Chinese) and international vendors covering incidents from **2004 to the present**, from which **6,706 English and 1,779 Chinese high-quality reports** were curated as seeds. A pipeline auto-selects tasks from a task pool and converts raw report text into supervised question/response corpora. SEvenLLM-Instruct contains **~90,000 samples**; training uses a **multi-task objective over 28 tasks**. SEvenLLM-Bench is bilingual and multi-task over **28 CTI tasks (13 understanding, 15 generation)**, evaluated via MCQ and query-answer items.

## Why it matters here — mostly as a contrast case
SEvenLLM is the largest-scale LLM-CTI benchmark in this batch, and it is built on a **vendor-report corpus with an auto-generated task taxonomy**, not on an ATT&CK-derived label spine. Consequences for the research question:

1. **Its labels are LLM/pipeline-derived from report text**, so they are not exposed to ATT&CK renumbering — but they are exposed to a worse problem: a **28-task taxonomy with no external referent**, meaning no other benchmark's scores are comparable to it at all, and the taxonomy itself is unversioned.
2. **The 2004-to-present span is a hidden drift trap.** A corpus spanning 20+ years of reporting is scored against a single contemporary task/label convention. Terminology, actor naming, and technique vocabulary all shifted across that span; a 2004 report and a 2024 report are not annotated under the same conceptual regime even if the annotation pipeline is identical.
3. **It shows the "growth" ambiguity vividly.** ~90,000 instruction samples and 28 tasks derived from 8,485 curated reports is an ~10× expansion factor — genuine adversary intelligence content is the 8,485 reports; the rest is task-format multiplication. This is a clean instance of the query's "apparent growth vs bookkeeping" distinction, at the dataset layer rather than the ontology layer.

## Citable claims
- Seed corpus: **6,706 English + 1,779 Chinese** curated high-quality reports (from >10,000 harvested incident pages), incidents from **2004 onward**.
- **SEvenLLM-Instruct ≈ 90,000 samples**; multi-task objective over **28 tasks**.
- **SEvenLLM-Bench**: bilingual, **28 CTI tasks — 13 understanding, 15 generation**; MCQ + query-answer item formats.

## Fidelity
**Summary fidelity.** arxiv.org and openreview.net are egress-blocked; all figures come from search-result snippets, not full text, and none is a verified verbatim quotation. Critically for this batch's assignment: **I could not establish whether SEvenLLM assigns any ATT&CK technique labels at all, nor whether it pins an ATT&CK release version.** No public GitHub repo for it could be cloned anonymously from this session (two candidate owner/name guesses failed to resolve). This remains an open gap.
