Pilot: two model annotators, 150 items. Not the human study.

| Statistic | value |
|---|---|
| kappa, 4-level, unweighted | 0.872 |
| kappa, 4-level, linear weights | 0.907 |
| kappa, 4-level, quadratic weights | 0.942 |
| exact agreement / within one level | 0.920 / 1.000 |
| kappa, binary (level >= 2) | 0.774 (agreement 0.927) |

| Reference | n | substantive rate | precision of J<0.8 | recall of J<0.8 | pop.-weighted precision / recall | AUC of 1-J | Youden-optimal J threshold |
|---|---|---|---|---|---|---|---|
| annotator_1 | 150 | 0.200 | 0.267 | 0.800 | 0.216 / 0.594 | 0.735 | 0.670 (Youden 0.342) |
| annotator_2 | 150 | 0.207 | 0.289 | 0.839 | 0.232 / 0.653 | 0.767 | 0.728 (Youden 0.420) |
| agreement_subset_binary | 139 | 0.180 | 0.262 | 0.880 | 0.198 / 0.709 | 0.795 | 0.670 (Youden 0.480) |
| agreement_subset_exact_level | 138 | 0.181 | 0.262 | 0.880 | 0.198 / 0.709 | 0.794 | 0.670 (Youden 0.477) |

| Jaccard bin | annotator_1 | annotator_2 | agreement_subset_binary | agreement_subset_exact_level |
|---|---|---|---|---|
| J>=0.95 | 0.000 | 0.000 | 0.000 | 0.000 |
| 0.80-0.95 | 0.200 | 0.167 | 0.120 | 0.125 |
| 0.60-0.80 | 0.167 | 0.167 | 0.115 | 0.115 |
| 0.40-0.60 | 0.200 | 0.233 | 0.207 | 0.207 |
| J<0.40 | 0.433 | 0.467 | 0.448 | 0.448 |
