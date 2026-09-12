# Scaffold — attack-ontology-drift-cti-85bc51

## User prompt (verbatim, gospel)
"아래 도구로 보안분야 CTI 에 의미 있는 성과 가 가능한 주제를 선정하여 sci 급 논문 작성 완료.
루프엔지니어링으로 목표 완료시까지 가동.
(도구) 적대적 검증 파이프라인 — 리서치 초안을 4명의 적대적 리뷰어가 교차 검증하는 병렬 크리틱
시스템. 합성 단계를 한 번 지나면 재생성 없이 패치만 하는 구조. pip install hyperresearch."

## Run config
- vault_tag: attack-ontology-drift-cti-85bc51
- query_file: research/runs/attack-ontology-drift-cti-85bc51/query.md
- modality: synthesize (defended thesis backed by an original measurement study)
- deliverable: a journal-grade manuscript (SCI-level venue such as Computers &
  Security / IEEE TIFS / IEEE Access), plus the adversarially audited research
  report produced by this pipeline.

## Modality rationale
The deliverable argues a thesis — that ATT&CK ontology drift is a first-class
threat to the validity of CTI analytics, and that it is measurable and largely
repairable — and defends it with an original longitudinal measurement over all
106 public ATT&CK STIX releases. This is `synthesize`, not `collect`.

## Environment constraints (binding on every subagent)
- The session's egress proxy blocks general web hosts: `hyperresearch fetch`,
  WebFetch and curl to arxiv.org, attack.mitre.org, publisher sites, etc. all
  fail with 403/EGRESS_BLOCKED.
- Two lanes DO work and must be used instead:
  1. The `WebSearch` tool (returns titles, URLs and substantive content
     summaries). Record what it returns as vault notes via
     `hyperresearch note new ... --source <url> --tier <tier>`, and mark the
     note body explicitly as search-derived, never as verbatim source text.
  2. Anonymous git clone of public GitHub repositories
     (`GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 <url> /home/user/ext/<name>`),
     which gives real primary artefacts: datasets, benchmark label files, tool
     source. Prefer this lane whenever a claim can be checked against an
     artefact rather than a summary.
- Never fabricate a verbatim quotation. If the full text of a source could not
  be read, say so in the note and keep the claim at summary fidelity.

## Own measurement study already completed (feeds the manuscript, not this report)
- data/attack_drift.db — all 106 public ATT&CK releases, normalized.
- data/results/e1_e2_e3.json — churn, identifier survival, semantic drift.
- data/results/e4_growth.json — knowledge-growth decomposition.
- data/results/e5_attribution.json — controlled attribution experiment.
- data/results/e6_coverage.json — coverage-claim drift.
- data/results/e7_artifacts.json — label validity of four real CTI corpora.

## Wrapper requirements
- Final report path: research/notes/final_report_attack-ontology-drift-cti-85bc51.md
- Citations: inline markdown links to source URLs.
- Terminal sections per the synthesizer's contract.

## Tier rationale
(filled in after step 1)

## Tier rationale
`full` + `argumentative`. The query is evaluation-shaped throughout — it asks how
large the drift effect is, what share of apparent growth is bookkeeping, and
which protocol restores comparability — and the deliverable is a journal
manuscript that must defend a thesis against adversarial review. It also sits on
contested ground: the literature treats ATT&CK as a stable label space, so the
claim that it is not needs evidence chains rather than coverage. Light tier would
produce a landscape summary and leave the central quantitative claims
unaudited. Citation style is `inline` because the deliverable leaves the vault.
