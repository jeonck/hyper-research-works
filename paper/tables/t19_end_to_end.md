| Gold set (release, items) | System | Scoring | micro-F1 | sample-F1 | Items passing | Verdict flips naive→normalized (fail→pass / pass→fail) |
|---|---|---|---|---|---|---|
| rcatt (v6.3, n=1490) | S1 (rcATT-era, v6.3) | naive | 0.241 | 0.142 | 178 |  |
| rcatt (v6.3, n=1490) | S1 (rcATT-era, v6.3) | normalized | 0.243 | 0.164 | 211 | 38 / 5 |
| rcatt (v6.3, n=1490) | S2 (TRAM-era, v13.0) | naive | 0.043 | 0.056 | 79 |  |
| rcatt (v6.3, n=1490) | S2 (TRAM-era, v13.0) | normalized | 0.064 | 0.112 | 164 | 85 / 0 |
| rcatt (v6.3, n=1490) | S2 (TRAM-era, v13.0) | vocab_matched | 0.067 | 0.103 | 148 |  |
| tram (v13.0, n=17177) | S1 (rcATT-era, v6.3) | naive | 0.021 | 0.011 | 192 |  |
| tram (v13.0, n=17177) | S1 (rcATT-era, v6.3) | normalized | 0.050 | 0.027 | 466 | 274 / 0 |
| tram (v13.0, n=17177) | S1 (rcATT-era, v6.3) | vocab_matched | 0.077 | 0.109 | 1875 |  |
| tram (v13.0, n=17177) | S2 (TRAM-era, v13.0) | naive | 0.698 | 0.635 | 11553 |  |
| tram (v13.0, n=17177) | S2 (TRAM-era, v13.0) | normalized | 0.700 | 0.636 | 11569 | 16 / 0 |
| ctibench (v14.0, n=47) | S1 (rcATT-era, v6.3) | naive | 0.013 | 0.011 | 0 |  |
| ctibench (v14.0, n=47) | S1 (rcATT-era, v6.3) | normalized | 0.013 | 0.032 | 1 | 1 / 0 |
| ctibench (v14.0, n=47) | S1 (rcATT-era, v6.3) | vocab_matched | 0.016 | 0.033 | 1 |  |
| ctibench (v14.0, n=47) | S2 (TRAM-era, v13.0) | naive | 0.019 | 0.018 | 0 |  |
| ctibench (v14.0, n=47) | S2 (TRAM-era, v13.0) | normalized | 0.020 | 0.040 | 1 | 1 / 0 |
| ctibench (v14.0, n=47) | S2 (TRAM-era, v13.0) | vocab_matched | 0.020 | 0.040 | 1 |  |

| Gold set | Order under naive | Order under normalized | Order changes? |
|---|---|---|---|
| rcatt | S1 (rcATT-era, v6.3) > S2 (TRAM-era, v13.0) | S1 (rcATT-era, v6.3) > S2 (TRAM-era, v13.0) | no |
| tram | S2 (TRAM-era, v13.0) > S1 (rcATT-era, v6.3) | S2 (TRAM-era, v13.0) > S1 (rcATT-era, v6.3) | no |
| ctibench | S2 (TRAM-era, v13.0) > S1 (rcATT-era, v6.3) | S2 (TRAM-era, v13.0) > S1 (rcATT-era, v6.3) | no |

| Layer (publisher folder) | Declares release | Distinct techniques | Live interval | Dead at v19.2 | Kept / merged-away / demoted / dropped | Catalogue share authored → naive → normalized |
|---|---|---|---|---|---|---|
| Cisco Talos (20210811-Cisco-Talos) | no | 15 | v7.0–v16.1 | 3 (0.20) | 15 / 1 / 1 / 0 | 3.5% → 1.7% → 2.0% |
| Cisco Talos (20211028-Cisco-Talos) | no | 15 | v7.0–v18.1 | 2 (0.13) | 15 / 1 / 1 / 0 | 3.5% → 1.9% → 2.0% |
| Rapid7 (20200922-Rapid7) | no | 28 | v7.0–v18.1 | 3 (0.11) | 28 / 2 / 2 / 0 | 6.5% → 3.6% → 3.7% |
| layer (samples) | 17 | 211 | v17.0–v18.1 | 16 (0.08) | 211 / 2 / 8 / 0 | 31.1% → 28.0% → 30.0% |
| MITRE Engenuity (20220223-MITRE-Engenuity) | no | 15 | v7.0–v18.1 | 1 (0.07) | 15 / 0 / 0 / 0 | 3.5% → 2.0% → 2.2% |
| Cisco Talos (20220426-Cisco-Talos) | no | 19 | v8.0–v16.1 | 1 (0.05) | 19 / 0 / 0 / 0 | 3.6% → 2.6% → 2.7% |
| Cisco Talos (20220726-Cisco-Talos) | no | 19 | v8.0–v16.1 | 1 (0.05) | 19 / 0 / 0 / 0 | 3.6% → 2.6% → 2.7% |
| Sophos (20210518-Sophos) | no | 62 | none (mixed) | 3 (0.05) | 61 / 1 / 1 / 1 | n/a → 8.5% → 8.6% |
| FireEye Mandiant - M-Trends 2021 (20210413-FireEye-Mandiant) | no | 211 | v8.2–v16.1 | 6 (0.03) | 211 / 2 / 2 / 0 | 39.8% → 29.4% → 30.0% |
| McAfee (20210421-McAfee) | no | 39 | v7.0–v16.1 | 1 (0.03) | 39 / 0 / 0 / 0 | 9.1% → 5.5% → 5.6% |
| *Bear APTs (samples) | 17 | 126 | v7.0–v18.1 | 3 (0.02) | 126 / 0 / 2 / 0 | 29.4% → 17.6% → 18.1% |
| McAfee (20211001-McAfee) | no | 66 | v7.0–v16.1 | 1 (0.02) | 66 / 0 / 0 / 0 | 15.4% → 9.3% → 9.5% |
