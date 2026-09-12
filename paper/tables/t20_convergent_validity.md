**all identifier-stable pairs** (n = 8359, J<0.8 in 518)

| Reference signal | base rate | agreement | kappa | precision of J<0.8 | recall of J<0.8 | AUC of 1-J | Youden-optimal J threshold |
|---|---|---|---|---|---|---|---|
| major_bump | 0.038 | 0.916 | 0.112 | 0.124 | 0.204 | 0.622 | 0.994 (Youden 0.236) |
| any_bump | 0.233 | 0.775 | 0.155 | 0.566 | 0.150 | 0.681 | 1.000 (Youden 0.364) |
| tactic_changed | 0.028 | 0.915 | 0.018 | 0.041 | 0.090 | 0.522 | 0.994 (Youden 0.047) |
| platform_changed | 0.067 | 0.895 | 0.131 | 0.195 | 0.180 | 0.646 | 0.978 (Youden 0.295) |
| name_changed | 0.007 | 0.941 | 0.133 | 0.081 | 0.677 | 0.927 | 0.988 (Youden 0.799) |
| structured_changed | 0.099 | 0.873 | 0.142 | 0.268 | 0.169 | 0.627 | 0.994 (Youden 0.247) |

| Metric | AUC for major version bump | AUC for structured-field change | Spearman rho with token Jaccard |
|---|---|---|---|
| jaccard | 0.622 | 0.627 | n/a |
| seqmatch | 0.632 | 0.627 | 0.973 |
| char3_jaccard | 0.629 | 0.627 | 0.974 |
| sentence_jaccard | 0.632 | 0.626 | 0.964 |
| tfidf_cosine | 0.630 | 0.629 | 0.980 |

**pairs with an edited description** (n = 1358, J<0.8 in 518)

| Reference signal | base rate | agreement | kappa | precision of J<0.8 | recall of J<0.8 | AUC of 1-J | Youden-optimal J threshold |
|---|---|---|---|---|---|---|---|
| major_bump | 0.094 | 0.619 | 0.057 | 0.124 | 0.504 | 0.569 | 0.637 (Youden 0.179) |
| any_bump | 0.641 | 0.409 | -0.108 | 0.566 | 0.336 | 0.516 | 0.952 (Youden 0.185) |
| tactic_changed | 0.036 | 0.613 | 0.009 | 0.041 | 0.429 | 0.478 | 0.520 (Youden 0.156) |
| platform_changed | 0.175 | 0.593 | 0.037 | 0.195 | 0.426 | 0.595 | 0.970 (Youden 0.219) |
| name_changed | 0.043 | 0.638 | 0.075 | 0.081 | 0.724 | 0.751 | 0.830 (Youden 0.408) |
| structured_changed | 0.232 | 0.591 | 0.064 | 0.268 | 0.441 | 0.593 | 0.924 (Youden 0.174) |

| Metric | AUC for major version bump | AUC for structured-field change | Spearman rho with token Jaccard |
|---|---|---|---|
| jaccard | 0.569 | 0.593 | n/a |
| seqmatch | 0.602 | 0.603 | 0.943 |
| char3_jaccard | 0.564 | 0.586 | 0.986 |
| sentence_jaccard | 0.602 | 0.566 | 0.602 |
| tfidf_cosine | 0.583 | 0.623 | 0.946 |
