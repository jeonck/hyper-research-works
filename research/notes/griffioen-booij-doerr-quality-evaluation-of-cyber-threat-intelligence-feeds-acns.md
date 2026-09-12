---
title: Griffioen, Booij & Doerr — Quality Evaluation of Cyber Threat Intelligence
  Feeds (ACNS 2020)
id: griffioen-booij-doerr-quality-evaluation-of-cyber-threat-intelligence-feeds-acns
tags:
- attack-ontology-drift-cti-85bc51
- cti-quality
created: '2026-09-12T13:21:45.150716Z'
source: https://link.springer.com/chapter/10.1007/978-3-030-57878-7_14
status: draft
type: note
tier: institutional
content_type: paper
deprecated: false
summary: Independent measurement of feed timeliness/coverage/accuracy; establishes
  that a consumer's threat landscape is an artifact of source selection — but uses
  no vocabulary-stability axis.
---

## What it is
Griffioen, Booij & Doerr, "Quality Evaluation of Cyber Threat Intelligence Feeds," *Applied Cryptography and Network Security* (ACNS 2020), Springer LNCS, DOI 10.1007/978-3-030-57878-7_14. A measurement study of open/commercial feed quality, companion in spirit to the USENIX "Tea Leaves" work (a related preprint on the authors' site is titled around feed timeliness).

## What it says bearing on the query
- Evaluates CTI feeds along quality axes centred on **timeliness, coverage, and accuracy/false positives**, arguing that feed consumers cannot take vendor claims at face value and need independent, repeatable measurement.
- Contributes to the now-standard finding that feeds differ sharply in **what they capture and how quickly**, with limited overlap between sources, so a consumer's measured "threat landscape" is largely an artifact of which feeds they subscribed to.
- Part of the cluster of work establishing that **CTI evaluation practice lacks standardized, comprehensive, quantifiable quality metrics** (a framing repeated by later work such as the automated dynamic assessment line).

## Bearing on ATT&CK ontology drift
- Supplies the second independent precedent (with Li et al. 2019) that **quality in CTI is established empirically by re-measuring the same construct across time and sources**, and that apparent content is sensitive to the measurement frame.
- Again: the quality axes used are *timeliness / coverage / accuracy / FP rate*. None of them is a **vocabulary-stability** axis. The unit of analysis is the indicator, and the label set applied to indicators is treated as given.
- Its "the consumer's landscape is an artifact of source selection" conclusion has a direct ontology analogue: **an analytic's measured technique landscape is an artifact of the ATT&CK release it was computed against** — a claim that, as far as this batch's searching found, nobody has stated or quantified in the feed-quality literature.

## Fidelity
Could not read full text (Springer, ACM and the cyber-threat-intelligence.com PDF all blocked). Claims are at summary fidelity from search-result descriptions and the surrounding literature's characterization of this paper. **No verbatim quotation asserted, and no specific numeric result from this paper is claimed** — the substantive numbers should be pulled from the PDF directly if this source is to carry weight in a submission.
