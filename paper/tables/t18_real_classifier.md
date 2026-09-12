| Train -> test | Model / gold vocab | Condition | micro-F1 | micro-P | micro-R | macro-F1 | sample-F1 | Gold labels (instances, distinct) |
|---|---|---|---|---|---|---|---|---|
| rcatt -> tram (n=17177) | v6.3 / v13.0 | naive | 0.021 | 0.235 | 0.011 | 0.012 | 0.011 | 17809, 509 |
| rcatt -> tram (n=17177) | v6.3 / v13.0 | normalized | 0.050 | 0.574 | 0.026 | 0.039 | 0.027 | 17793, 499 |
| rcatt -> tram (n=17177) | v6.3 / v13.0 | vocab_matched | 0.077 | 0.805 | 0.041 | 0.085 | 0.109 | 16242, 235 |
| rcatt -> tram (n=17177) | v6.3 / v13.0 | ceiling_matched | 0.755 | 0.778 | 0.734 | 0.415 | 0.708 | 16242, 235 |
| rcatt -> tram (n=17177) | v6.3 / v13.0 | ceiling_native | 0.698 | 0.738 | 0.663 | 0.270 | 0.635 | 17809, 509 |
| rcatt -> ctibench (n=47) | v6.3 / v14.0 | naive | 0.013 | 0.286 | 0.007 | 0.002 | 0.011 | 299, 84 |
| rcatt -> ctibench (n=47) | v6.3 / v14.0 | normalized | 0.013 | 0.286 | 0.007 | 0.002 | 0.032 | 292, 77 |
| rcatt -> ctibench (n=47) | v6.3 / v14.0 | vocab_matched | 0.016 | 0.286 | 0.008 | 0.003 | 0.033 | 251, 61 |
| tram -> rcatt (n=1490) | v13.0 / v6.3 | naive | 0.043 | 0.370 | 0.023 | 0.021 | 0.056 | 6235, 215 |
| tram -> rcatt (n=1490) | v13.0 / v6.3 | normalized | 0.064 | 0.529 | 0.034 | 0.042 | 0.112 | 5906, 199 |
| tram -> rcatt (n=1490) | v13.0 / v6.3 | vocab_matched | 0.067 | 0.599 | 0.035 | 0.051 | 0.103 | 6235, 215 |
| tram -> rcatt (n=1490) | v13.0 / v6.3 | ceiling_matched | 0.241 | 0.429 | 0.167 | 0.100 | 0.142 | 6235, 215 |
| tram -> rcatt (n=1490) | v13.0 / v6.3 | ceiling_native | 0.241 | 0.429 | 0.167 | 0.100 | 0.142 | 6235, 215 |
| tram -> ctibench (n=47) | v13.0 / v14.0 | naive | 0.019 | 0.250 | 0.010 | 0.016 | 0.018 | 299, 84 |
| tram -> ctibench (n=47) | v13.0 / v14.0 | normalized | 0.020 | 0.250 | 0.010 | 0.018 | 0.040 | 292, 77 |
| tram -> ctibench (n=47) | v13.0 / v14.0 | vocab_matched | 0.020 | 0.250 | 0.010 | 0.018 | 0.040 | 292, 77 |

| Train -> test | Contrast | micro-F1 delta [95% CI] | p (Holm) | sample-F1 delta [95% CI] | p (Holm) |
|---|---|---|---|---|---|
| rcatt -> tram | vocabulary | +0.057 [+0.052, +0.062] | 0.0025 | +0.098 [+0.093, +0.102] | 0.0025 |
| rcatt -> tram | norm_gain | +0.029 [+0.026, +0.033] | 0.0025 | +0.016 [+0.014, +0.018] | 0.0025 |
| rcatt -> tram | data_drift | +0.678 [+0.670, +0.685] | 0.0025 | +0.600 [+0.592, +0.607] | 0.0025 |
| rcatt -> tram | total | +0.734 [+0.728, +0.741] | 0.0025 | +0.697 [+0.691, +0.704] | 0.0025 |
| rcatt -> tram | granularity | -0.057 [-0.060, -0.053] | 0.0025 | -0.073 [-0.077, -0.069] | 0.0025 |
| rcatt -> ctibench | vocabulary | +0.002 [+0.000, +0.006] | 0.552 | +0.022 [+0.000, +0.065] | 0.572 |
| rcatt -> ctibench | norm_gain | +0.000 [+0.000, +0.002] | 0.901 | +0.021 [+0.000, +0.064] | 0.718 |
| tram -> rcatt | vocabulary | +0.024 [+0.019, +0.030] | 0.0025 | +0.047 [+0.037, +0.058] | 0.0025 |
| tram -> rcatt | norm_gain | +0.021 [+0.017, +0.026] | 0.0025 | +0.056 [+0.046, +0.067] | 0.0025 |
| tram -> rcatt | data_drift | +0.174 [+0.150, +0.196] | 0.0025 | +0.039 [+0.021, +0.058] | 0.0025 |
| tram -> rcatt | total | +0.198 [+0.175, +0.221] | 0.0025 | +0.086 [+0.069, +0.103] | 0.0025 |
| tram -> rcatt | granularity | +0.000 [+0.000, +0.000] | 1 | +0.000 [+0.000, +0.000] | 1 |
| tram -> ctibench | vocabulary | +0.000 [+0.000, +0.002] | 1 | +0.021 [+0.000, +0.064] | 1 |
| tram -> ctibench | norm_gain | +0.000 [+0.000, +0.002] | 1 | +0.021 [+0.000, +0.064] | 1 |

| Train -> test | Projection | Distinct: input / kept / collapsed-to-parent / reverted / merged-away / dropped / demoted |
|---|---|---|
| rcatt -> tram | normalized_predictions | 84 / 81 / 0 / 0 / 4 / 3 / 37 |
| rcatt -> tram | normalized_gold | 509 / 509 / 0 / 0 / 19 / 0 / 8 |
| rcatt -> tram | backprojected_gold | 509 / 118 / 135 / 116 / 134 / 140 / 0 |
| rcatt -> ctibench | normalized_predictions | 3 / 3 / 0 / 0 / 0 / 0 / 1 |
| rcatt -> ctibench | normalized_gold | 84 / 77 / 0 / 0 / 0 / 7 / 0 |
| rcatt -> ctibench | backprojected_gold | 84 / 58 / 0 / 3 / 0 / 23 / 0 |
| tram -> rcatt | normalized_predictions | 126 / 126 / 0 / 0 / 6 / 0 / 2 |
| tram -> rcatt | normalized_gold | 215 / 207 / 0 / 0 / 15 / 8 / 88 |
| tram -> rcatt | backprojected_predictions | 126 / 56 / 24 / 41 / 14 / 5 / 0 |
| tram -> ctibench | normalized_predictions | 10 / 10 / 0 / 0 / 0 / 0 / 0 |
| tram -> ctibench | normalized_gold | 84 / 77 / 0 / 0 / 0 / 7 / 0 |
| tram -> ctibench | backprojected_gold | 84 / 77 / 0 / 0 / 0 / 7 / 0 |
