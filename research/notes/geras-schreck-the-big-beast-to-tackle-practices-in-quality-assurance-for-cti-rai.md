---
title: 'Geras & Schreck — The Big Beast to Tackle: Practices in Quality Assurance
  for CTI (RAID 2024)'
id: geras-schreck-the-big-beast-to-tackle-practices-in-quality-assurance-for-cti-rai
tags:
- attack-ontology-drift-cti-85bc51
- cti-quality
created: '2026-09-12T13:21:45.679797Z'
source: https://dl.acm.org/doi/10.1145/3678890.3678903
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: '25 practitioner interviews: organizations recognize the need for CTI quality
  but have no systematic assessment processes — corroborating the Delphi finding that
  no concrete metrics are in operational use.'
---

## What it is
Geras & Schreck, The "Big Beast to Tackle": Practices in Quality Assurance for Cyber Threat Intelligence, *RAID 2024* (27th International Symposium on Research in Attacks, Intrusions and Defenses), Padua, 30 Sep–2 Oct 2024, DOI 10.1145/3678890.3678903. A qualitative practitioner study — the "what do CTI teams actually do about quality" counterpart to the Delphi/metric papers.

## What it says bearing on the query
- Based on **25 interviews with CTI experts**, aimed at understanding how CTI quality is handled in the real world rather than in models.
- Core reported finding: organizations **recognize the need for high-quality intelligence but struggle to establish systematic processes** for assessing and improving it — i.e. QA in CTI is largely ad hoc, personal-judgement-driven, and unstandardized.
- Explicitly positioned as **bridging the gap between theory and practice** in CTI quality measurement; the title phrase ("big beast to tackle") is the practitioners' own framing of quality assurance as an unsolved, oversized problem.

## Bearing on ATT&CK ontology drift
- Independent corroboration (interview evidence, 2024) of the Delphi study's negative result: **there are no concrete, agreed metrics in operational use**. If practitioners have no systematic QA for accuracy and timeliness — the dimensions everyone agrees on — they certainly have no process for detecting that their historical ATT&CK mappings have silently decayed as the framework was re-versioned.
- Useful for motivating the reporting-discipline half of the query: the intervention needed is not merely a metric but a **protocol practitioners can actually run** (pin the ATT&CK version, record the normalization mapping, re-report under a common release). The RAID evidence says any proposal requiring bespoke expert judgement per item will not be adopted.
- **Searched this paper's framing specifically for vocabulary/ontology-versioning QA and found no indication it is among the practices discussed.** Absence here is weakly-evidenced (abstract-level only) and should be confirmed against the full text.

## Fidelity
Could not read full text (ACM DL blocked). The "25 interviews", the RAID 2024 venue/date, and the "recognize the need but struggle to establish systematic processes" finding are at summary fidelity from search-result descriptions of the abstract. No verbatim quotation asserted; the title phrase is quoted only as the published title.
