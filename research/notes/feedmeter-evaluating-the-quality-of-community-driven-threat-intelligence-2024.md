---
title: FeedMeter — Evaluating the Quality of Community-Driven Threat Intelligence
  (2024)
id: feedmeter-evaluating-the-quality-of-community-driven-threat-intelligence-2024
tags:
- attack-ontology-drift-cti-85bc51
- cti-quality
created: '2026-09-12T13:21:45.414904Z'
source: https://www.scitepress.org/Papers/2024/123576/123576.pdf
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Continuous-monitoring platform scoring feeds on eight descriptive metrics;
  normalization means cross-producer format harmonization, not cross-version vocabulary
  harmonization.
---

## What it is
"FeedMeter: Evaluating the Quality of Community-Driven Threat Intelligence," SCITEPRESS conference paper (2024), https://www.scitepress.org/Papers/2024/123576/123576.pdf. An operational platform for continuous feed-quality monitoring, i.e. the "make it a running service" descendant of the measurement papers.

## What it says bearing on the query
- FeedMeter **collects, normalizes and aggregates** threat-intelligence feeds and **continuously monitors them using eight descriptive metrics** that approximate feed quality.
- The framing is explicitly about *community-driven* (open/crowd-sourced) intelligence, where no vendor SLA exists and quality must be inferred from observable feed behaviour over time.
- It represents the state of the art in *automated, continuous* quality assessment: quality as a monitored time series rather than a one-off audit.

## Bearing on ATT&CK ontology drift
- Strengthens the **absence finding**: even the most operationally mature, continuously-running quality instrumentation in this literature defines its eight metrics over *feed content behaviour* (volume, churn, overlap, latency, and similar descriptive statistics). It **normalizes** feeds — but normalization here means format/field harmonization across producers at a single point in time, **not harmonization across versions of a controlled vocabulary**.
- Conceptually, FeedMeter is the closest architectural template for what a drift-aware instrument would look like: a continuously-running monitor that emits a per-release quality/stability time series. The proposed contribution differs in what is monitored — the **knowledge base's own ontology** (technique adds/deprecations/revocations/splits/tactic reassignments/description rewrites) rather than the indicator stream flowing through it.

## Fidelity
Could not read the PDF (SCITEPRESS blocked). "Eight descriptive metrics", "collects, normalizes and aggregates", and the community-driven framing are at summary fidelity from search-result description. **The individual eight metrics are NOT enumerated here because I could not read them** — do not assert their identity without opening the paper. No verbatim quotation asserted.
