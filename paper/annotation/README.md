# Annotation instrument: does a description change alter what the identifier denotes?

This directory ships the human-annotation study that validates the paper's
substantial-rewrite rule (token Jaccard below 0.8), ready to run.

| File | Contents |
|---|---|
| `codebook.md` | the four-level ordinal scale (0 cosmetic, 1 clarification, 2 scope change, 3 redefinition), decision rules and worked examples |
| `sample_150.csv` | 150 identifier-stable technique pairs across consecutive Enterprise major releases, stratified into five Jaccard bins of 30; the annotator-facing file carries no similarity value |
| `sample_150_key.csv` | the bin, Jaccard and structured-field flags per item; not shown to annotators |
| `pilot_annotator_1.csv`, `pilot_annotator_2.csv` | the blind pilot: two language-model annotators (Claude Sonnet, Claude Opus), codebook and sample only, no key, no hypothesis |

## Protocol

1. Two annotators with CTI experience read `codebook.md` and annotate every
   item independently, blind to the Jaccard value and to each other, writing
   `item_id,level,rationale`.
2. Agreement is reported as Cohen's kappa on the four-level scale (unweighted
   and quadratic-weighted) and on the binarised scale, level 2 or 3 =
   substantive.
3. Disagreements are adjudicated by discussion to a single level; the
   adjudicated set is the reference.
4. Concordance of the paper's rule with the reference: precision and recall of
   J < 0.8 for "substantive", AUC of 1 − J, the Youden-optimal threshold, and
   the substantive rate within each Jaccard bin. Precision and recall are also
   re-weighted to the population of edited pairs, since the sample is
   stratified.

`code/36_semantic_validation.py` computes all of step 4 from whatever
`pilot_annotator_{1,2}.csv` (or human files renamed to those paths) are present.
