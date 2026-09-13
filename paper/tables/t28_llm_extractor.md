| Model (digest) | Prompt condition | Emitted IDs (distinct) | Live at v19.2 | Stale, resolvable | Stale, unresolvable | Fabricated | Other-domain | Home release (share live) |
|---|---|---|---|---|---|---|---|---|
| gemma3:4b (a2af6cc3eb7f) | unspecified | 908 (105) | 0.831 | 0.109 | 0.000 | 0.057 | 0.002 | v10.1 (0.64) |
| gemma3:4b (a2af6cc3eb7f) | latest | 901 (118) | 0.820 | 0.120 | 0.000 | 0.058 | 0.002 | v18.1 (0.64) |
| gemma3:4b (a2af6cc3eb7f) | era_pinned | 899 (109) | 0.819 | 0.122 | 0.000 | 0.056 | 0.003 | v18.1 (0.62) |
| gemma3:4b (a2af6cc3eb7f) | legacy_pinned | 882 (95) | 0.840 | 0.137 | 0.001 | 0.022 | 0.000 | v18.1 (0.73) |
| llama3.2:3b (a80c4f17acd5) | unspecified | 1193 (61) | 0.845 | 0.137 | 0.000 | 0.017 | 0.001 | v6.3 (0.64) |
| llama3.2:3b (a80c4f17acd5) | latest | 1198 (64) | 0.826 | 0.128 | 0.000 | 0.046 | 0.000 | v6.3 (0.66) |
| llama3.2:3b (a80c4f17acd5) | era_pinned | 1185 (58) | 0.833 | 0.149 | 0.000 | 0.019 | 0.000 | v6.3 (0.74) |
| llama3.2:3b (a80c4f17acd5) | legacy_pinned | 1161 (45) | 0.841 | 0.158 | 0.000 | 0.002 | 0.000 | v6.3 (0.96) |

| Model | Condition | Gold set (release, n) | Emitted share live at gold release | micro-F1 naive | micro-F1 normalized | sample-F1 naive → normalized | Gain [95% CI] | Items passing naive → normalized |
|---|---|---|---|---|---|---|---|---|
| gemma3:4b | unspecified | tram (v13.0, 150) | 0.833 | 0.043 | 0.046 | 0.041 → 0.043 | +0.002 [+0.000, +0.004] | 5 → 7 |
| gemma3:4b | unspecified | ctibench (v14.0, 47) | 0.890 | 0.023 | 0.023 | 0.022 → 0.023 | +0.001 [+0.000, +0.002] | 0 → 0 |
| gemma3:4b | unspecified | rcatt (v6.3, 50) | 0.185 | 0.017 | 0.062 | 0.023 → 0.064 | +0.041 [+0.014, +0.072] | 0 → 1 |
| gemma3:4b | latest | tram (v13.0, 150) | 0.861 | 0.047 | 0.050 | 0.044 → 0.050 | +0.005 [+0.001, +0.011] | 8 → 9 |
| gemma3:4b | latest | ctibench (v14.0, 47) | 0.899 | 0.027 | 0.027 | 0.026 → 0.026 | +0.001 [+0.000, +0.003] | 0 → 0 |
| gemma3:4b | latest | rcatt (v6.3, 50) | 0.205 | 0.030 | 0.081 | 0.033 → 0.080 | +0.047 [+0.019, +0.082] | 0 → 1 |
| gemma3:4b | era_pinned | tram (v13.0, 150) | 0.843 | 0.050 | 0.054 | 0.048 → 0.054 | +0.006 [+0.001, +0.012] | 9 → 11 |
| gemma3:4b | era_pinned | ctibench (v14.0, 47) | 0.898 | 0.019 | 0.019 | 0.018 → 0.019 | +0.001 [+0.000, +0.003] | 0 → 0 |
| gemma3:4b | era_pinned | rcatt (v6.3, 50) | 0.222 | 0.017 | 0.072 | 0.021 → 0.071 | +0.050 [+0.022, +0.085] | 0 → 1 |
| gemma3:4b | legacy_pinned | tram (v13.0, 150) | 0.877 | 0.048 | 0.049 | 0.050 → 0.051 | +0.001 [+0.000, +0.002] | 11 → 12 |
| gemma3:4b | legacy_pinned | ctibench (v14.0, 47) | 0.898 | 0.031 | 0.031 | 0.031 → 0.031 | +0.000 [+0.000, +0.000] | 0 → 0 |
| gemma3:4b | legacy_pinned | rcatt (v6.3, 50) | 0.215 | 0.013 | 0.048 | 0.015 → 0.044 | +0.029 [+0.008, +0.057] | 0 → 1 |
| llama3.2:3b | unspecified | tram (v13.0, 150) | 0.831 | 0.000 | 0.005 | 0.000 → 0.004 | +0.004 [+0.000, +0.011] | 0 → 0 |
| llama3.2:3b | unspecified | ctibench (v14.0, 47) | 0.851 | 0.026 | 0.027 | 0.024 → 0.024 | +0.000 [+0.000, +0.000] | 0 → 0 |
| llama3.2:3b | unspecified | rcatt (v6.3, 50) | 0.798 | 0.029 | 0.040 | 0.020 → 0.031 | +0.011 [+0.000, +0.027] | 0 → 0 |
| llama3.2:3b | latest | tram (v13.0, 150) | 0.837 | 0.000 | 0.002 | 0.000 → 0.002 | +0.002 [+0.000, +0.007] | 0 → 0 |
| llama3.2:3b | latest | ctibench (v14.0, 47) | 0.838 | 0.034 | 0.034 | 0.031 → 0.031 | +0.000 [+0.000, +0.000] | 0 → 0 |
| llama3.2:3b | latest | rcatt (v6.3, 50) | 0.695 | 0.021 | 0.028 | 0.011 → 0.015 | +0.005 [+0.000, +0.013] | 0 → 0 |
| llama3.2:3b | era_pinned | tram (v13.0, 150) | 0.832 | 0.000 | 0.002 | 0.000 → 0.002 | +0.002 [+0.000, +0.007] | 0 → 0 |
| llama3.2:3b | era_pinned | ctibench (v14.0, 47) | 0.825 | 0.038 | 0.038 | 0.037 → 0.037 | +0.000 [+0.000, +0.000] | 0 → 0 |
| llama3.2:3b | era_pinned | rcatt (v6.3, 50) | 0.817 | 0.021 | 0.027 | 0.011 → 0.016 | +0.005 [+0.000, +0.015] | 0 → 0 |
| llama3.2:3b | legacy_pinned | tram (v13.0, 150) | 0.828 | 0.000 | 0.002 | 0.000 → 0.002 | +0.002 [+0.000, +0.007] | 0 → 0 |
| llama3.2:3b | legacy_pinned | ctibench (v14.0, 47) | 0.812 | 0.015 | 0.019 | 0.016 → 0.019 | +0.003 [+0.000, +0.009] | 0 → 0 |
| llama3.2:3b | legacy_pinned | rcatt (v6.3, 50) | 0.996 | 0.029 | 0.030 | 0.017 → 0.017 | +0.000 [+0.000, +0.001] | 0 → 0 |

Prompt sensitivity (gemma3:4b, unspecified condition, TRAM subset):

| Prompt | n | Live share | Stale share | Fabricated share | micro-F1 naive |
|---|---|---|---|---|---|
| p0 | 60 | 0.811 | 0.107 | 0.083 | 0.052 |
| p1 | 60 | 0.840 | 0.112 | 0.048 | 0.042 |
| p2 | 60 | 0.865 | 0.099 | 0.036 | 0.057 |
