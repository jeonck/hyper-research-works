---
title: 'Li et al. — Reading the Tea Leaves: A Comparative Analysis of Threat Intelligence
  (USENIX Security 2019)'
id: li-et-al-reading-the-tea-leaves-a-comparative-analysis-of-threat-intelligence-us
tags:
- attack-ontology-drift-cti-85bc51
- cti-quality
created: '2026-09-12T13:21:31.940694Z'
source: https://www.usenix.org/conference/usenixsecurity19/presentation/li
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Six feed metrics (volume, differential/exclusive contribution, latency, accuracy,
  coverage); 3 malware feeds shared >40% of entries with a two-year-old snapshot;
  labels like malicious/suspicious loosely defined.
---

## What it is
Li, Dunn, Pearce, McCoy, Voelker & Savage, "Reading the Tea Leaves: A Comparative Analysis of Threat Intelligence," 28th USENIX Security Symposium (USENIX Security '19), pp. 851–867. The most-cited empirical measurement study of threat-intelligence feed quality; the paper that gave the field its working metric vocabulary for feeds.

## What it says bearing on the query
- Formally defines **six metrics** for characterizing threat-intelligence feeds: **volume, differential contribution, exclusive contribution, latency, accuracy, coverage**.
- Applies them across a broad range of **public and commercial sources** (including Facebook ThreatExchange and a paid feed aggregator), grounding quantitative assessments with external measurements to investigate coverage and accuracy qualitatively.
- Longitudinal/staleness result: comparing 2016 and 2018 data, **30 of 43 feeds in 2018 intersected with the data from two years earlier**, and **9 feeds had an intersection rate over 10%**. Three malware feeds (Feodo IP Blacklist, PA Abuse.ch Ransomware, Zeus IP Blacklist) **shared over 40%** of their entries with the two-year-old snapshot — i.e. a large share of "current" C&C indicators were carried-over old entries.
- Reported framing of the labeling problem: feeds **vary significantly in what they capture, few explain collection methodology**, and consumers get **loose labels like "scan", "botnet", "malicious", "suspicious"** that are not consistently defined across producers.

## Bearing on ATT&CK ontology drift
Two loadbearing points for the argument:
1. **Precedent for the method.** This is the template for "measure the artifact, not the vendor's claim": define metrics, run them across versions/sources, and report differential vs. exclusive contribution. The ontology-drift analogue is precisely *differential vs. exclusive contribution across ATT&CK releases* — how much of an apparent growth delta is genuinely new content versus re-labelled/split/renamed existing content. The metric shape already exists in the literature; it has simply never been applied to the *vocabulary* rather than to indicator sets.
2. **Precedent for the pathology.** The "40% of entries are two years old" result and the "loosely defined labels" complaint are the IoC-layer version of the same disease: apparent volume is inflated by bookkeeping, and the label semantics are unstable across producers. Nobody in that line of work extended the question to the TTP layer, where the vocabulary is itself versioned and centrally rewritten.

## Fidelity
Could not read the PDF (usenix.org and the UCSD mirror are behind the blocked proxy). Metric list, the 30/43 and 9-feeds-over-10% and >40% figures, and the loose-label characterization are at summary fidelity from search-result descriptions of the paper. No verbatim quotation asserted; re-verify the exact figures against sec19fall-li_prepub.pdf before citing.
