<!-- SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0 -->
<!-- Supplementary appendix of research/paper/manuscript.md. Status: independent research manuscript / preprint draft, not peer-reviewed. Tables between GENERATED markers are written by `python -m herd.paper fill` from committed results. -->
# Supplementary appendix

## S1. Experiments, runs and reports

| Experiment | Type | Runs | Protocol (SHA-256 prefix) | Configuration (canonical SHA-256 prefix) | Code revision | Report |
|---|---|---|---|---|---|---|
| EXP-001 | exploratory (verification) | EXP-001-R001 to R004 (2026-11-24), R005 (2026-11-25) | f40252ceb8e3a710 | R001 6bb119865235b1f0; R002 e18b052ab500b99a; R003 0f01eecc86cd6251; R004 7e64cd6f93ffe4db; R005 0c1bfeb60beb150c | R001 to R004 `f15c0c2`; R005 `eded9b8` | `research/experiments/EXP-001/report.md` |
| EXP-002 | confirmatory | EXP-002-R001 (2026-11-25) | 36fbb89207fe9900 (frozen v1.0) | 26e7cef89deddbb8 | `50fbdb1` | `research/experiments/EXP-002/report.md` |
| EXP-003 | confirmatory sensitivity | EXP-003-R001 (2026-11-25) | fd0b7c9e361f196c (frozen v1.0) | 12ebfabeef1fca01 | `50fbdb1` | `research/experiments/EXP-003/report.md` |
| EXP-004 | exploratory, post hoc (M4) | EXP-004-R001 (2026-11-25); derived analyses | e14989310901286f (not frozen) | 9269dee899844d05 | R001 `3831429`; derived `f2c91ff` | `research/experiments/EXP-004/report.md` |

Study protocol: `research/protocol.md` v1.0, SHA-256 `f73423c0bfd6f6463b1c1cb0d316e4ddc3942306eafe6793ba866112e72a457c`. Full hashes: `research/freeze.json`, `research/experiment_registry.csv` and each run's `run_manifest.json`. No run failed, was dropped or was rerun.

## S2. Complete experimental matrix

| Experiment | Rules | q | Networks | v | N | Tie rule | Seeds x episodes | Paired episodes per contrast |
|---|---|---|---|---|---|---|---|---|
| EXP-001 smoke (R001, R005) | independent, Bayesian, imitation | 0.5, 0.6, 0.8 | complete, window-1 | 1 | 20 | own | 2 x 200 | 400 |
| EXP-002 | independent, Bayesian, imitation | 0.55, 0.60, 0.70, 0.80 | complete, window-2, window-3 | 1, 0.5 | 50 | own | 10 x 1,000 | 10,000 |
| EXP-003 V1 | as EXP-002 | 0.55, 0.70 | as EXP-002 | 1, 0.5 | 50 | coin | 10 x 1,000 | 10,000 |
| EXP-003 V2 | as EXP-002 | 0.55, 0.70 | as EXP-002 | 1, 0.5 | 10 | own | 10 x 1,000 | 10,000 |
| EXP-003 V3 | as EXP-002 | 0.55, 0.70 | as EXP-002 | 1, 0.5 | 200 | own | 10 x 1,000 | 10,000 |
| EXP-004-R001 V1, V2, V3 | as EXP-003 | 0.60, 0.80 | as EXP-002 | 1, 0.5 | 50, 10, 200 | coin, own, own | 10 x 1,000 | 10,000 |

EXP-001-R002 to R004 were throughput and seed-spread probes on the EXP-002 and EXP-003 matrix shapes at one fifth of the episodes (seeds 100 to 109); see the EXP-001 report. Master seeds: confirmatory 0 to 9; exploratory 100 to 109 except EXP-001-R001 (seeds 0 and 1 at $N = 20$, no episode in common with a confirmatory episode) and EXP-004-R001 (seeds 0 to 9, chosen after the confirmatory runs so that its episodes match EXP-002).

## S3. Deviations, amendments and owner decisions

- **Amendments before the freeze (owner-approved 2026-11-24):** A-1 `window-1` replaced by `window-2`; A-2 anchor and equivalence restricted to $q > 1/2$; A-3 zero-variance contrasts outside the Holm family, reported exactly; A-4 decisions on Holm-adjusted p-values, unadjusted 95% intervals; A-5 sample kept (`research/protocol.md` section 11; D-008). A-3 and A-4 options were chosen by the AI assistant at the freeze and ratified by the owner (D-009, R-1).
- **Disclosure C4:** exploratory primary-contrast values from EXP-001-R001 to R004 were seen before the freeze (`research/freeze.json`).
- **Execution deviations:** none in EXP-002 or EXP-003. Reporting-layer changes after the runs, changing no estimate: figure captions in the run report generator, the EXP-003 rule implemented in `src/herd/robustness.py` after the runs, the report-table printer (D-010). The protocols' `report --exp` reproduction command does not exist; `report --run` was used.
- **EXP-001-R005:** not named in the EXP-001 protocol; added by the M3 brief as a pre-confirmatory smoke run (D-010).
- **EXP-004 (M4):** designed and run after all confirmatory results were seen, under the coordinator's M4 brief; exploratory throughout (D-011).
- **Owner decisions of 2026-11-25** (`../_shared/owner-approvals-2026-11-25.md` and `-25b.md`): none is specific to this project; the owner's instruction "Approve all recommendations, push then next" started M4.

## S4. Full EXP-002 contrasts (TAB-S01)

Columns as in the EXP-002 report section 8.1. Source: `results/EXP-002/EXP-002-R001/result.json`.

<!-- BEGIN GENERATED TAB-S01 -->
| Variation | q | Network | v | Rule | n | Delta | 95% CI | Bootstrap 95% CI | Holm p | Holm-significant |
|---|---|---|---|---|---|---|---|---|---|---|
| main (N=50, own) | 0.55 | complete | 1 | bayesian | 10000 | 0.0380 | [0.0290, 0.0470] | [0.0287, 0.0469] | < 1e-15 | yes |
| main (N=50, own) | 0.55 | complete | 1 | imitation | 10000 | 0.0380 | [0.0290, 0.0470] | [0.0287, 0.0469] | < 1e-15 | yes |
| main (N=50, own) | 0.55 | complete | 0.5 | bayesian | 10000 | 0.0400 | [0.0317, 0.0483] | [0.0317, 0.0484] | < 1e-15 | yes |
| main (N=50, own) | 0.55 | complete | 0.5 | imitation | 10000 | 0.0400 | [0.0317, 0.0483] | [0.0317, 0.0484] | < 1e-15 | yes |
| main (N=50, own) | 0.55 | window-2 | 1 | bayesian | 10000 | 0.0386 | [0.0295, 0.0477] | [0.0297, 0.0482] | < 1e-15 | yes |
| main (N=50, own) | 0.55 | window-2 | 1 | imitation | 10000 | 0.0386 | [0.0295, 0.0477] | [0.0297, 0.0482] | < 1e-15 | yes |
| main (N=50, own) | 0.55 | window-2 | 0.5 | bayesian | 10000 | 0.0091 | [0.0067, 0.0114] | [0.0068, 0.0114] | 3.1e-14 | yes |
| main (N=50, own) | 0.55 | window-2 | 0.5 | imitation | 10000 | 0.0059 | [0.0048, 0.0070] | [0.0048, 0.0069] | < 1e-15 | yes |
| main (N=50, own) | 0.55 | window-3 | 1 | bayesian | 10000 | 0.0424 | [0.0335, 0.0514] | [0.0334, 0.0511] | < 1e-15 | yes |
| main (N=50, own) | 0.55 | window-3 | 1 | imitation | 10000 | 0.0448 | [0.0360, 0.0536] | [0.0361, 0.0532] | < 1e-15 | yes |
| main (N=50, own) | 0.55 | window-3 | 0.5 | bayesian | 10000 | 0.0195 | [0.0151, 0.0239] | [0.0151, 0.0239] | < 1e-15 | yes |
| main (N=50, own) | 0.55 | window-3 | 0.5 | imitation | 10000 | 0.0131 | [0.0109, 0.0152] | [0.0109, 0.0152] | < 1e-15 | yes |
| main (N=50, own) | 0.6 | complete | 1 | bayesian | 10000 | 0.0836 | [0.0752, 0.0921] | [0.0747, 0.0921] | < 1e-15 | yes |
| main (N=50, own) | 0.6 | complete | 1 | imitation | 10000 | 0.0836 | [0.0752, 0.0921] | [0.0747, 0.0921] | < 1e-15 | yes |
| main (N=50, own) | 0.6 | complete | 0.5 | bayesian | 10000 | 0.0783 | [0.0705, 0.0861] | [0.0707, 0.0861] | < 1e-15 | yes |
| main (N=50, own) | 0.6 | complete | 0.5 | imitation | 10000 | 0.0783 | [0.0705, 0.0861] | [0.0707, 0.0861] | < 1e-15 | yes |
| main (N=50, own) | 0.6 | window-2 | 1 | bayesian | 10000 | 0.0617 | [0.0529, 0.0705] | [0.0523, 0.0701] | < 1e-15 | yes |
| main (N=50, own) | 0.6 | window-2 | 1 | imitation | 10000 | 0.0617 | [0.0529, 0.0705] | [0.0523, 0.0701] | < 1e-15 | yes |
| main (N=50, own) | 0.6 | window-2 | 0.5 | bayesian | 10000 | 0.0225 | [0.0203, 0.0247] | [0.0203, 0.0247] | < 1e-15 | yes |
| main (N=50, own) | 0.6 | window-2 | 0.5 | imitation | 10000 | 0.0132 | [0.0122, 0.0142] | [0.0122, 0.0142] | < 1e-15 | yes |
| main (N=50, own) | 0.6 | window-3 | 1 | bayesian | 10000 | 0.0824 | [0.0739, 0.0909] | [0.0738, 0.0908] | < 1e-15 | yes |
| main (N=50, own) | 0.6 | window-3 | 1 | imitation | 10000 | 0.0907 | [0.0824, 0.0990] | [0.0826, 0.0993] | < 1e-15 | yes |
| main (N=50, own) | 0.6 | window-3 | 0.5 | bayesian | 10000 | 0.0349 | [0.0306, 0.0392] | [0.0304, 0.0392] | < 1e-15 | yes |
| main (N=50, own) | 0.6 | window-3 | 0.5 | imitation | 10000 | 0.0274 | [0.0253, 0.0295] | [0.0252, 0.0294] | < 1e-15 | yes |
| main (N=50, own) | 0.7 | complete | 1 | bayesian | 10000 | 0.1344 | [0.1277, 0.1412] | [0.1277, 0.1414] | < 1e-15 | yes |
| main (N=50, own) | 0.7 | complete | 1 | imitation | 10000 | 0.1344 | [0.1277, 0.1412] | [0.1277, 0.1414] | < 1e-15 | yes |
| main (N=50, own) | 0.7 | complete | 0.5 | bayesian | 10000 | 0.1216 | [0.1153, 0.1280] | [0.1154, 0.1278] | < 1e-15 | yes |
| main (N=50, own) | 0.7 | complete | 0.5 | imitation | 10000 | 0.1216 | [0.1153, 0.1280] | [0.1154, 0.1278] | < 1e-15 | yes |
| main (N=50, own) | 0.7 | window-2 | 1 | bayesian | 10000 | 0.0992 | [0.0918, 0.1066] | [0.0918, 0.1063] | < 1e-15 | yes |
| main (N=50, own) | 0.7 | window-2 | 1 | imitation | 10000 | 0.0992 | [0.0918, 0.1066] | [0.0918, 0.1063] | < 1e-15 | yes |
| main (N=50, own) | 0.7 | window-2 | 0.5 | bayesian | 10000 | 0.0337 | [0.0317, 0.0356] | [0.0317, 0.0357] | < 1e-15 | yes |
| main (N=50, own) | 0.7 | window-2 | 0.5 | imitation | 10000 | 0.0212 | [0.0202, 0.0221] | [0.0203, 0.0221] | < 1e-15 | yes |
| main (N=50, own) | 0.7 | window-3 | 1 | bayesian | 10000 | 0.1335 | [0.1268, 0.1402] | [0.1269, 0.1400] | < 1e-15 | yes |
| main (N=50, own) | 0.7 | window-3 | 1 | imitation | 10000 | 0.1439 | [0.1375, 0.1504] | [0.1377, 0.1505] | < 1e-15 | yes |
| main (N=50, own) | 0.7 | window-3 | 0.5 | bayesian | 10000 | 0.0636 | [0.0600, 0.0673] | [0.0600, 0.0672] | < 1e-15 | yes |
| main (N=50, own) | 0.7 | window-3 | 0.5 | imitation | 10000 | 0.0466 | [0.0448, 0.0484] | [0.0448, 0.0485] | < 1e-15 | yes |
| main (N=50, own) | 0.8 | complete | 1 | bayesian | 10000 | 0.1317 | [0.1272, 0.1362] | [0.1273, 0.1361] | < 1e-15 | yes |
| main (N=50, own) | 0.8 | complete | 1 | imitation | 10000 | 0.1317 | [0.1272, 0.1362] | [0.1273, 0.1361] | < 1e-15 | yes |
| main (N=50, own) | 0.8 | complete | 0.5 | bayesian | 10000 | 0.1251 | [0.1209, 0.1293] | [0.1208, 0.1291] | < 1e-15 | yes |
| main (N=50, own) | 0.8 | complete | 0.5 | imitation | 10000 | 0.1251 | [0.1209, 0.1293] | [0.1208, 0.1291] | < 1e-15 | yes |
| main (N=50, own) | 0.8 | window-2 | 1 | bayesian | 10000 | 0.1086 | [0.1033, 0.1139] | [0.1034, 0.1139] | < 1e-15 | yes |
| main (N=50, own) | 0.8 | window-2 | 1 | imitation | 10000 | 0.1086 | [0.1033, 0.1139] | [0.1034, 0.1139] | < 1e-15 | yes |
| main (N=50, own) | 0.8 | window-2 | 0.5 | bayesian | 10000 | 0.0363 | [0.0349, 0.0378] | [0.0348, 0.0378] | < 1e-15 | yes |
| main (N=50, own) | 0.8 | window-2 | 0.5 | imitation | 10000 | 0.0235 | [0.0228, 0.0243] | [0.0227, 0.0243] | < 1e-15 | yes |
| main (N=50, own) | 0.8 | window-3 | 1 | bayesian | 10000 | 0.1342 | [0.1298, 0.1386] | [0.1297, 0.1386] | < 1e-15 | yes |
| main (N=50, own) | 0.8 | window-3 | 1 | imitation | 10000 | 0.1394 | [0.1353, 0.1436] | [0.1352, 0.1436] | < 1e-15 | yes |
| main (N=50, own) | 0.8 | window-3 | 0.5 | bayesian | 10000 | 0.0704 | [0.0678, 0.0731] | [0.0677, 0.0732] | < 1e-15 | yes |
| main (N=50, own) | 0.8 | window-3 | 0.5 | imitation | 10000 | 0.0526 | [0.0513, 0.0540] | [0.0514, 0.0539] | < 1e-15 | yes |
<!-- END GENERATED TAB-S01 -->

## S5. EXP-002 secondary metrics (TAB-S04)

Means with 95% intervals over 10,000 episodes per arm; descriptive, no multiplicity adjustment. Longest wrong run in agents; other columns are proportions. Source: `results/EXP-002/EXP-002-R001/result.json`.

<!-- BEGIN GENERATED TAB-S04 -->
| Variation | q | Network | v | Rule | Accuracy | Wrong cascade | Longest wrong run | Informative share | Last agent |
|---|---|---|---|---|---|---|---|---|---|
| main | 0.55 | complete | 1 | independent | 0.550 [0.549, 0.552] | 0.000 [0.000, 0.000] | 4.41 [4.38, 4.44] | 1.000 [1.000, 1.000] | 0.547 [0.538, 0.557] |
| main | 0.55 | complete | 1 | bayesian | 0.588 [0.579, 0.597] | 0.408 [0.399, 0.418] | 20.07 [19.61, 20.53] | 0.079 [0.078, 0.080] | 0.592 [0.582, 0.601] |
| main | 0.55 | complete | 1 | imitation | 0.588 [0.579, 0.597] | 0.408 [0.399, 0.418] | 20.07 [19.61, 20.53] | 0.079 [0.078, 0.080] | 0.592 [0.582, 0.601] |
| main | 0.55 | complete | 0.5 | independent | 0.550 [0.549, 0.551] | 0.000 [0.000, 0.000] | 4.39 [4.36, 4.42] | 1.000 [1.000, 1.000] | 0.554 [0.545, 0.564] |
| main | 0.55 | complete | 0.5 | bayesian | 0.590 [0.581, 0.598] | 0.402 [0.392, 0.412] | 18.71 [18.29, 19.13] | 0.158 [0.156, 0.161] | 0.598 [0.588, 0.607] |
| main | 0.55 | complete | 0.5 | imitation | 0.590 [0.581, 0.598] | 0.402 [0.392, 0.412] | 18.71 [18.29, 19.13] | 0.158 [0.156, 0.161] | 0.598 [0.588, 0.607] |
| main | 0.55 | window-2 | 1 | independent | 0.550 [0.549, 0.552] | 0.000 [0.000, 0.000] | 4.41 [4.38, 4.44] | 1.000 [1.000, 1.000] | 0.546 [0.536, 0.555] |
| main | 0.55 | window-2 | 1 | bayesian | 0.589 [0.580, 0.598] | 0.409 [0.399, 0.419] | 20.32 [19.85, 20.79] | 0.060 [0.060, 0.061] | 0.591 [0.581, 0.601] |
| main | 0.55 | window-2 | 1 | imitation | 0.589 [0.580, 0.598] | 0.409 [0.399, 0.419] | 20.32 [19.85, 20.79] | 0.060 [0.060, 0.061] | 0.591 [0.581, 0.601] |
| main | 0.55 | window-2 | 0.5 | independent | 0.550 [0.549, 0.551] | 0.000 [0.000, 0.000] | 4.41 [4.38, 4.44] | 1.000 [1.000, 1.000] | 0.546 [0.536, 0.556] |
| main | 0.55 | window-2 | 0.5 | bayesian | 0.559 [0.556, 0.562] | 0.829 [0.822, 0.836] | 8.31 [8.21, 8.41] | 0.691 [0.689, 0.694] | 0.563 [0.553, 0.572] |
| main | 0.55 | window-2 | 0.5 | imitation | 0.556 [0.554, 0.558] | 0.842 [0.835, 0.849] | 5.93 [5.88, 5.98] | 0.839 [0.838, 0.841] | 0.553 [0.543, 0.562] |
| main | 0.55 | window-3 | 1 | independent | 0.550 [0.548, 0.551] | 0.000 [0.000, 0.000] | 4.41 [4.38, 4.44] | 1.000 [1.000, 1.000] | 0.554 [0.544, 0.563] |
| main | 0.55 | window-3 | 1 | bayesian | 0.592 [0.583, 0.601] | 0.404 [0.394, 0.413] | 19.87 [19.41, 20.33] | 0.080 [0.079, 0.081] | 0.596 [0.587, 0.606] |
| main | 0.55 | window-3 | 1 | imitation | 0.594 [0.585, 0.604] | 0.400 [0.390, 0.409] | 19.45 [19.00, 19.90] | 0.099 [0.097, 0.101] | 0.600 [0.591, 0.610] |
| main | 0.55 | window-3 | 0.5 | independent | 0.549 [0.548, 0.551] | 0.000 [0.000, 0.000] | 4.39 [4.36, 4.42] | 1.000 [1.000, 1.000] | 0.547 [0.537, 0.556] |
| main | 0.55 | window-3 | 0.5 | bayesian | 0.569 [0.564, 0.574] | 0.774 [0.765, 0.782] | 12.63 [12.43, 12.83] | 0.438 [0.435, 0.441] | 0.569 [0.559, 0.579] |
| main | 0.55 | window-3 | 0.5 | imitation | 0.563 [0.560, 0.565] | 0.868 [0.861, 0.875] | 8.34 [8.25, 8.43] | 0.665 [0.663, 0.667] | 0.565 [0.556, 0.575] |
| main | 0.6 | complete | 1 | independent | 0.600 [0.598, 0.601] | 0.000 [0.000, 0.000] | 3.85 [3.83, 3.88] | 1.000 [1.000, 1.000] | 0.600 [0.590, 0.609] |
| main | 0.6 | complete | 1 | bayesian | 0.683 [0.675, 0.692] | 0.310 [0.301, 0.319] | 15.38 [14.95, 15.82] | 0.077 [0.076, 0.078] | 0.690 [0.681, 0.699] |
| main | 0.6 | complete | 1 | imitation | 0.683 [0.675, 0.692] | 0.310 [0.301, 0.319] | 15.38 [14.95, 15.82] | 0.077 [0.076, 0.078] | 0.690 [0.681, 0.699] |
| main | 0.6 | complete | 0.5 | independent | 0.601 [0.599, 0.602] | 0.000 [0.000, 0.000] | 3.84 [3.81, 3.86] | 1.000 [1.000, 1.000] | 0.593 [0.584, 0.603] |
| main | 0.6 | complete | 0.5 | bayesian | 0.679 [0.671, 0.687] | 0.305 [0.296, 0.314] | 14.53 [14.13, 14.93] | 0.154 [0.152, 0.157] | 0.695 [0.686, 0.704] |
| main | 0.6 | complete | 0.5 | imitation | 0.679 [0.671, 0.687] | 0.305 [0.296, 0.314] | 14.53 [14.13, 14.93] | 0.154 [0.152, 0.157] | 0.695 [0.686, 0.704] |
| main | 0.6 | window-2 | 1 | independent | 0.601 [0.600, 0.602] | 0.000 [0.000, 0.000] | 3.86 [3.83, 3.88] | 1.000 [1.000, 1.000] | 0.605 [0.595, 0.614] |
| main | 0.6 | window-2 | 1 | bayesian | 0.663 [0.654, 0.672] | 0.334 [0.325, 0.343] | 16.68 [16.23, 17.13] | 0.059 [0.058, 0.059] | 0.666 [0.657, 0.675] |
| main | 0.6 | window-2 | 1 | imitation | 0.663 [0.654, 0.672] | 0.334 [0.325, 0.343] | 16.68 [16.23, 17.13] | 0.059 [0.058, 0.059] | 0.666 [0.657, 0.675] |
| main | 0.6 | window-2 | 0.5 | independent | 0.601 [0.600, 0.603] | 0.000 [0.000, 0.000] | 3.86 [3.84, 3.89] | 1.000 [1.000, 1.000] | 0.596 [0.586, 0.605] |
| main | 0.6 | window-2 | 0.5 | bayesian | 0.624 [0.621, 0.626] | 0.750 [0.742, 0.759] | 7.07 [6.97, 7.16] | 0.691 [0.689, 0.694] | 0.613 [0.604, 0.623] |
| main | 0.6 | window-2 | 0.5 | imitation | 0.614 [0.613, 0.616] | 0.763 [0.755, 0.772] | 5.19 [5.14, 5.23] | 0.837 [0.836, 0.839] | 0.607 [0.597, 0.616] |
| main | 0.6 | window-3 | 1 | independent | 0.600 [0.598, 0.601] | 0.000 [0.000, 0.000] | 3.87 [3.84, 3.89] | 1.000 [1.000, 1.000] | 0.598 [0.588, 0.607] |
| main | 0.6 | window-3 | 1 | bayesian | 0.682 [0.673, 0.691] | 0.311 [0.302, 0.320] | 15.46 [15.02, 15.89] | 0.076 [0.075, 0.077] | 0.689 [0.680, 0.698] |
| main | 0.6 | window-3 | 1 | imitation | 0.690 [0.682, 0.699] | 0.300 [0.291, 0.309] | 14.79 [14.36, 15.22] | 0.094 [0.092, 0.095] | 0.700 [0.691, 0.709] |
| main | 0.6 | window-3 | 0.5 | independent | 0.601 [0.600, 0.602] | 0.000 [0.000, 0.000] | 3.86 [3.83, 3.89] | 1.000 [1.000, 1.000] | 0.606 [0.596, 0.615] |
| main | 0.6 | window-3 | 0.5 | bayesian | 0.636 [0.631, 0.640] | 0.691 [0.682, 0.700] | 10.84 [10.64, 11.04] | 0.431 [0.428, 0.434] | 0.641 [0.632, 0.651] |
| main | 0.6 | window-3 | 0.5 | imitation | 0.628 [0.626, 0.631] | 0.786 [0.778, 0.794] | 7.18 [7.09, 7.26] | 0.656 [0.654, 0.659] | 0.635 [0.626, 0.645] |
| main | 0.7 | complete | 1 | independent | 0.700 [0.699, 0.701] | 0.000 [0.000, 0.000] | 2.93 [2.91, 2.95] | 1.000 [1.000, 1.000] | 0.702 [0.693, 0.711] |
| main | 0.7 | complete | 1 | bayesian | 0.835 [0.828, 0.841] | 0.155 [0.148, 0.162] | 8.00 [7.65, 8.34] | 0.069 [0.068, 0.070] | 0.845 [0.838, 0.852] |
| main | 0.7 | complete | 1 | imitation | 0.835 [0.828, 0.841] | 0.155 [0.148, 0.162] | 8.00 [7.65, 8.34] | 0.069 [0.068, 0.070] | 0.845 [0.838, 0.852] |
| main | 0.7 | complete | 0.5 | independent | 0.701 [0.700, 0.702] | 0.000 [0.000, 0.000] | 2.93 [2.91, 2.95] | 1.000 [1.000, 1.000] | 0.708 [0.699, 0.717] |
| main | 0.7 | complete | 0.5 | bayesian | 0.823 [0.816, 0.829] | 0.157 [0.150, 0.164] | 7.93 [7.61, 8.25] | 0.138 [0.136, 0.140] | 0.843 [0.836, 0.850] |
| main | 0.7 | complete | 0.5 | imitation | 0.823 [0.816, 0.829] | 0.157 [0.150, 0.164] | 7.93 [7.61, 8.25] | 0.138 [0.136, 0.140] | 0.843 [0.836, 0.850] |
| main | 0.7 | window-2 | 1 | independent | 0.700 [0.699, 0.701] | 0.000 [0.000, 0.000] | 2.96 [2.93, 2.98] | 1.000 [1.000, 1.000] | 0.693 [0.684, 0.702] |
| main | 0.7 | window-2 | 1 | bayesian | 0.799 [0.791, 0.807] | 0.196 [0.188, 0.203] | 9.91 [9.53, 10.29] | 0.056 [0.055, 0.056] | 0.804 [0.797, 0.812] |
| main | 0.7 | window-2 | 1 | imitation | 0.799 [0.791, 0.807] | 0.196 [0.188, 0.203] | 9.91 [9.53, 10.29] | 0.056 [0.055, 0.056] | 0.804 [0.797, 0.812] |
| main | 0.7 | window-2 | 0.5 | independent | 0.700 [0.699, 0.701] | 0.000 [0.000, 0.000] | 2.95 [2.93, 2.97] | 1.000 [1.000, 1.000] | 0.690 [0.681, 0.699] |
| main | 0.7 | window-2 | 0.5 | bayesian | 0.734 [0.731, 0.736] | 0.551 [0.542, 0.561] | 5.09 [5.01, 5.18] | 0.682 [0.679, 0.685] | 0.736 [0.727, 0.744] |
| main | 0.7 | window-2 | 0.5 | imitation | 0.721 [0.719, 0.723] | 0.556 [0.546, 0.566] | 3.87 [3.83, 3.91] | 0.827 [0.826, 0.829] | 0.716 [0.708, 0.725] |
| main | 0.7 | window-3 | 1 | independent | 0.701 [0.699, 0.702] | 0.000 [0.000, 0.000] | 2.94 [2.92, 2.96] | 1.000 [1.000, 1.000] | 0.699 [0.690, 0.708] |
| main | 0.7 | window-3 | 1 | bayesian | 0.834 [0.827, 0.841] | 0.156 [0.149, 0.163] | 8.02 [7.68, 8.37] | 0.069 [0.068, 0.069] | 0.844 [0.837, 0.851] |
| main | 0.7 | window-3 | 1 | imitation | 0.845 [0.838, 0.851] | 0.142 [0.135, 0.149] | 7.37 [7.04, 7.70] | 0.081 [0.079, 0.082] | 0.858 [0.851, 0.865] |
| main | 0.7 | window-3 | 0.5 | independent | 0.701 [0.700, 0.702] | 0.000 [0.000, 0.000] | 2.93 [2.91, 2.95] | 1.000 [1.000, 1.000] | 0.706 [0.697, 0.715] |
| main | 0.7 | window-3 | 0.5 | bayesian | 0.764 [0.761, 0.768] | 0.475 [0.465, 0.485] | 6.96 [6.79, 7.12] | 0.422 [0.418, 0.425] | 0.763 [0.755, 0.772] |
| main | 0.7 | window-3 | 0.5 | imitation | 0.747 [0.745, 0.750] | 0.562 [0.553, 0.572] | 4.91 [4.83, 4.98] | 0.640 [0.637, 0.642] | 0.748 [0.740, 0.757] |
| main | 0.8 | complete | 1 | independent | 0.800 [0.799, 0.801] | 0.000 [0.000, 0.000] | 2.18 [2.16, 2.19] | 1.000 [1.000, 1.000] | 0.799 [0.791, 0.807] |
| main | 0.8 | complete | 1 | bayesian | 0.932 [0.927, 0.937] | 0.060 [0.055, 0.064] | 3.26 [3.04, 3.49] | 0.059 [0.058, 0.059] | 0.940 [0.936, 0.945] |
| main | 0.8 | complete | 1 | imitation | 0.932 [0.927, 0.937] | 0.060 [0.055, 0.064] | 3.26 [3.04, 3.49] | 0.059 [0.058, 0.059] | 0.940 [0.936, 0.945] |
| main | 0.8 | complete | 0.5 | independent | 0.801 [0.799, 0.802] | 0.000 [0.000, 0.000] | 2.16 [2.14, 2.18] | 1.000 [1.000, 1.000] | 0.802 [0.795, 0.810] |
| main | 0.8 | complete | 0.5 | bayesian | 0.926 [0.921, 0.930] | 0.058 [0.054, 0.063] | 3.30 [3.09, 3.50] | 0.117 [0.116, 0.119] | 0.942 [0.937, 0.946] |
| main | 0.8 | complete | 0.5 | imitation | 0.926 [0.921, 0.930] | 0.058 [0.054, 0.063] | 3.30 [3.09, 3.50] | 0.117 [0.116, 0.119] | 0.942 [0.937, 0.946] |
| main | 0.8 | window-2 | 1 | independent | 0.799 [0.798, 0.800] | 0.000 [0.000, 0.000] | 2.17 [2.16, 2.19] | 1.000 [1.000, 1.000] | 0.796 [0.788, 0.804] |
| main | 0.8 | window-2 | 1 | bayesian | 0.908 [0.903, 0.913] | 0.087 [0.081, 0.092] | 4.54 [4.27, 4.80] | 0.051 [0.051, 0.052] | 0.913 [0.908, 0.919] |
| main | 0.8 | window-2 | 1 | imitation | 0.908 [0.903, 0.913] | 0.087 [0.081, 0.092] | 4.54 [4.27, 4.80] | 0.051 [0.051, 0.052] | 0.913 [0.908, 0.919] |
| main | 0.8 | window-2 | 0.5 | independent | 0.801 [0.799, 0.802] | 0.000 [0.000, 0.000] | 2.18 [2.16, 2.19] | 1.000 [1.000, 1.000] | 0.801 [0.793, 0.808] |
| main | 0.8 | window-2 | 0.5 | bayesian | 0.837 [0.835, 0.839] | 0.303 [0.294, 0.312] | 3.20 [3.13, 3.26] | 0.671 [0.668, 0.673] | 0.838 [0.831, 0.845] |
| main | 0.8 | window-2 | 0.5 | imitation | 0.824 [0.823, 0.825] | 0.306 [0.297, 0.315] | 2.64 [2.61, 2.68] | 0.811 [0.810, 0.813] | 0.825 [0.817, 0.832] |
| main | 0.8 | window-3 | 1 | independent | 0.801 [0.800, 0.802] | 0.000 [0.000, 0.000] | 2.16 [2.15, 2.18] | 1.000 [1.000, 1.000] | 0.812 [0.804, 0.819] |
| main | 0.8 | window-3 | 1 | bayesian | 0.935 [0.931, 0.940] | 0.057 [0.052, 0.061] | 3.12 [2.90, 3.34] | 0.059 [0.058, 0.059] | 0.943 [0.939, 0.948] |
| main | 0.8 | window-3 | 1 | imitation | 0.940 [0.936, 0.944] | 0.050 [0.045, 0.054] | 2.81 [2.60, 3.01] | 0.065 [0.064, 0.066] | 0.950 [0.946, 0.955] |
| main | 0.8 | window-3 | 0.5 | independent | 0.800 [0.798, 0.801] | 0.000 [0.000, 0.000] | 2.18 [2.16, 2.20] | 1.000 [1.000, 1.000] | 0.805 [0.797, 0.813] |
| main | 0.8 | window-3 | 0.5 | bayesian | 0.870 [0.867, 0.873] | 0.248 [0.240, 0.257] | 3.86 [3.74, 3.99] | 0.401 [0.398, 0.404] | 0.878 [0.872, 0.885] |
| main | 0.8 | window-3 | 0.5 | imitation | 0.852 [0.851, 0.854] | 0.300 [0.291, 0.309] | 2.98 [2.92, 3.03] | 0.608 [0.606, 0.610] | 0.859 [0.852, 0.866] |
<!-- END GENERATED TAB-S04 -->

## S6. EXP-003 robustness, all 72 comparisons (TAB-S02, confirmatory)

Source: `results/EXP-003/EXP-003-R001/tables/robustness_vs_EXP-002-R001.csv`.

<!-- BEGIN GENERATED TAB-S02 -->
| Variation | q | Network | v | Rule | EXP-002 Delta | Variation Delta | 95% CI | Holm p | Status |
|---|---|---|---|---|---|---|---|---|---|
| V1 (N=50, coin) | 0.55 | complete | 1 | bayesian | 0.0380 | 0.0148 | [0.0054, 0.0243] | 0.012 | robust |
| V1 (N=50, coin) | 0.55 | complete | 1 | imitation | 0.0380 | 0.0148 | [0.0054, 0.0243] | 0.012 | robust |
| V1 (N=50, coin) | 0.55 | complete | 0.5 | bayesian | 0.0400 | 0.0136 | [0.0046, 0.0226] | 0.013 | robust |
| V1 (N=50, coin) | 0.55 | complete | 0.5 | imitation | 0.0400 | 0.0136 | [0.0046, 0.0226] | 0.013 | robust |
| V1 (N=50, coin) | 0.55 | window-2 | 1 | bayesian | 0.0386 | 0.0176 | [0.0081, 0.0270] | 0.0024 | robust |
| V1 (N=50, coin) | 0.55 | window-2 | 1 | imitation | 0.0386 | 0.0195 | [0.0101, 0.0289] | 0.00051 | robust |
| V1 (N=50, coin) | 0.55 | window-2 | 0.5 | bayesian | 0.0091 | 0.0049 | [0.0021, 0.0078] | 0.006 | robust |
| V1 (N=50, coin) | 0.55 | window-2 | 0.5 | imitation | 0.0059 | 0.0036 | [0.0015, 0.0057] | 0.0065 | robust |
| V1 (N=50, coin) | 0.55 | window-3 | 1 | bayesian | 0.0424 | 0.0082 | [-0.0013, 0.0176] | 0.18 | lost significance |
| V1 (N=50, coin) | 0.55 | window-3 | 1 | imitation | 0.0448 | 0.0079 | [-0.0015, 0.0174] | 0.18 | lost significance |
| V1 (N=50, coin) | 0.55 | window-3 | 0.5 | bayesian | 0.0195 | 0.0142 | [0.0093, 0.0191] | 1.9e-07 | robust |
| V1 (N=50, coin) | 0.55 | window-3 | 0.5 | imitation | 0.0131 | 0.0106 | [0.0072, 0.0140] | 9.8e-09 | robust |
| V1 (N=50, coin) | 0.7 | complete | 1 | bayesian | 0.1344 | 0.0494 | [0.0411, 0.0576] | < 1e-15 | robust |
| V1 (N=50, coin) | 0.7 | complete | 1 | imitation | 0.1344 | 0.0494 | [0.0411, 0.0576] | < 1e-15 | robust |
| V1 (N=50, coin) | 0.7 | complete | 0.5 | bayesian | 0.1216 | 0.0476 | [0.0397, 0.0555] | < 1e-15 | robust |
| V1 (N=50, coin) | 0.7 | complete | 0.5 | imitation | 0.1216 | 0.0476 | [0.0397, 0.0555] | < 1e-15 | robust |
| V1 (N=50, coin) | 0.7 | window-2 | 1 | bayesian | 0.0992 | 0.0344 | [0.0259, 0.0428] | 2.2e-14 | robust |
| V1 (N=50, coin) | 0.7 | window-2 | 1 | imitation | 0.0992 | 0.0413 | [0.0329, 0.0496] | < 1e-15 | robust |
| V1 (N=50, coin) | 0.7 | window-2 | 0.5 | bayesian | 0.0337 | 0.0181 | [0.0156, 0.0207] | < 1e-15 | robust |
| V1 (N=50, coin) | 0.7 | window-2 | 0.5 | imitation | 0.0212 | 0.0147 | [0.0128, 0.0165] | < 1e-15 | robust |
| V1 (N=50, coin) | 0.7 | window-3 | 1 | bayesian | 0.1335 | 0.0469 | [0.0387, 0.0552] | < 1e-15 | robust |
| V1 (N=50, coin) | 0.7 | window-3 | 1 | imitation | 0.1439 | 0.0481 | [0.0399, 0.0563] | < 1e-15 | robust |
| V1 (N=50, coin) | 0.7 | window-3 | 0.5 | bayesian | 0.0636 | 0.0284 | [0.0240, 0.0328] | < 1e-15 | robust |
| V1 (N=50, coin) | 0.7 | window-3 | 0.5 | imitation | 0.0466 | 0.0279 | [0.0249, 0.0309] | < 1e-15 | robust |
| V2 (N=10, own) | 0.55 | complete | 1 | bayesian | 0.0380 | 0.0305 | [0.0237, 0.0373] | < 1e-15 | robust |
| V2 (N=10, own) | 0.55 | complete | 1 | imitation | 0.0380 | 0.0305 | [0.0237, 0.0373] | < 1e-15 | robust |
| V2 (N=10, own) | 0.55 | complete | 0.5 | bayesian | 0.0400 | 0.0192 | [0.0142, 0.0242] | 4.1e-13 | robust |
| V2 (N=10, own) | 0.55 | complete | 0.5 | imitation | 0.0400 | 0.0192 | [0.0142, 0.0242] | 4.1e-13 | robust |
| V2 (N=10, own) | 0.55 | window-2 | 1 | bayesian | 0.0386 | 0.0254 | [0.0181, 0.0327] | 5.7e-11 | robust |
| V2 (N=10, own) | 0.55 | window-2 | 1 | imitation | 0.0386 | 0.0254 | [0.0181, 0.0327] | 5.7e-11 | robust |
| V2 (N=10, own) | 0.55 | window-2 | 0.5 | bayesian | 0.0091 | 0.0085 | [0.0054, 0.0116] | 7.2e-08 | robust |
| V2 (N=10, own) | 0.55 | window-2 | 0.5 | imitation | 0.0059 | 0.0074 | [0.0053, 0.0094] | 9.8e-12 | robust |
| V2 (N=10, own) | 0.55 | window-3 | 1 | bayesian | 0.0424 | 0.0326 | [0.0259, 0.0393] | < 1e-15 | robust |
| V2 (N=10, own) | 0.55 | window-3 | 1 | imitation | 0.0448 | 0.0313 | [0.0248, 0.0377] | < 1e-15 | robust |
| V2 (N=10, own) | 0.55 | window-3 | 0.5 | bayesian | 0.0195 | 0.0132 | [0.0089, 0.0175] | 4.8e-09 | robust |
| V2 (N=10, own) | 0.55 | window-3 | 0.5 | imitation | 0.0131 | 0.0105 | [0.0071, 0.0139] | 4.8e-09 | robust |
| V2 (N=10, own) | 0.7 | complete | 1 | bayesian | 0.1344 | 0.0957 | [0.0902, 0.1011] | < 1e-15 | robust |
| V2 (N=10, own) | 0.7 | complete | 1 | imitation | 0.1344 | 0.0957 | [0.0902, 0.1011] | < 1e-15 | robust |
| V2 (N=10, own) | 0.7 | complete | 0.5 | bayesian | 0.1216 | 0.0606 | [0.0565, 0.0648] | < 1e-15 | robust |
| V2 (N=10, own) | 0.7 | complete | 0.5 | imitation | 0.1216 | 0.0606 | [0.0565, 0.0648] | < 1e-15 | robust |
| V2 (N=10, own) | 0.7 | window-2 | 1 | bayesian | 0.0992 | 0.0831 | [0.0771, 0.0891] | < 1e-15 | robust |
| V2 (N=10, own) | 0.7 | window-2 | 1 | imitation | 0.0992 | 0.0831 | [0.0771, 0.0891] | < 1e-15 | robust |
| V2 (N=10, own) | 0.7 | window-2 | 0.5 | bayesian | 0.0337 | 0.0236 | [0.0209, 0.0263] | < 1e-15 | robust |
| V2 (N=10, own) | 0.7 | window-2 | 0.5 | imitation | 0.0212 | 0.0172 | [0.0154, 0.0191] | < 1e-15 | robust |
| V2 (N=10, own) | 0.7 | window-3 | 1 | bayesian | 0.1335 | 0.0924 | [0.0869, 0.0979] | < 1e-15 | robust |
| V2 (N=10, own) | 0.7 | window-3 | 1 | imitation | 0.1439 | 0.0893 | [0.0840, 0.0946] | < 1e-15 | robust |
| V2 (N=10, own) | 0.7 | window-3 | 0.5 | bayesian | 0.0636 | 0.0388 | [0.0352, 0.0424] | < 1e-15 | robust |
| V2 (N=10, own) | 0.7 | window-3 | 0.5 | imitation | 0.0466 | 0.0329 | [0.0300, 0.0358] | < 1e-15 | robust |
| V3 (N=200, own) | 0.55 | complete | 1 | bayesian | 0.0380 | 0.0505 | [0.0410, 0.0599] | < 1e-15 | robust |
| V3 (N=200, own) | 0.55 | complete | 1 | imitation | 0.0380 | 0.0505 | [0.0410, 0.0599] | < 1e-15 | robust |
| V3 (N=200, own) | 0.55 | complete | 0.5 | bayesian | 0.0400 | 0.0432 | [0.0339, 0.0525] | < 1e-15 | robust |
| V3 (N=200, own) | 0.55 | complete | 0.5 | imitation | 0.0400 | 0.0432 | [0.0339, 0.0525] | < 1e-15 | robust |
| V3 (N=200, own) | 0.55 | window-2 | 1 | bayesian | 0.0386 | 0.0354 | [0.0259, 0.0449] | 7.3e-13 | robust |
| V3 (N=200, own) | 0.55 | window-2 | 1 | imitation | 0.0386 | 0.0354 | [0.0259, 0.0449] | 7.3e-13 | robust |
| V3 (N=200, own) | 0.55 | window-2 | 0.5 | bayesian | 0.0091 | 0.0106 | [0.0093, 0.0118] | < 1e-15 | robust |
| V3 (N=200, own) | 0.55 | window-2 | 0.5 | imitation | 0.0059 | 0.0068 | [0.0062, 0.0073] | < 1e-15 | robust |
| V3 (N=200, own) | 0.55 | window-3 | 1 | bayesian | 0.0424 | 0.0462 | [0.0368, 0.0557] | < 1e-15 | robust |
| V3 (N=200, own) | 0.55 | window-3 | 1 | imitation | 0.0448 | 0.0549 | [0.0455, 0.0643] | < 1e-15 | robust |
| V3 (N=200, own) | 0.55 | window-3 | 0.5 | bayesian | 0.0195 | 0.0202 | [0.0176, 0.0228] | < 1e-15 | robust |
| V3 (N=200, own) | 0.55 | window-3 | 0.5 | imitation | 0.0131 | 0.0154 | [0.0143, 0.0166] | < 1e-15 | robust |
| V3 (N=200, own) | 0.7 | complete | 1 | bayesian | 0.1344 | 0.1452 | [0.1383, 0.1522] | < 1e-15 | robust |
| V3 (N=200, own) | 0.7 | complete | 1 | imitation | 0.1344 | 0.1452 | [0.1383, 0.1522] | < 1e-15 | robust |
| V3 (N=200, own) | 0.7 | complete | 0.5 | bayesian | 0.1216 | 0.1391 | [0.1322, 0.1460] | < 1e-15 | robust |
| V3 (N=200, own) | 0.7 | complete | 0.5 | imitation | 0.1216 | 0.1391 | [0.1322, 0.1460] | < 1e-15 | robust |
| V3 (N=200, own) | 0.7 | window-2 | 1 | bayesian | 0.0992 | 0.1033 | [0.0956, 0.1110] | < 1e-15 | robust |
| V3 (N=200, own) | 0.7 | window-2 | 1 | imitation | 0.0992 | 0.1033 | [0.0956, 0.1110] | < 1e-15 | robust |
| V3 (N=200, own) | 0.7 | window-2 | 0.5 | bayesian | 0.0337 | 0.0347 | [0.0337, 0.0357] | < 1e-15 | robust |
| V3 (N=200, own) | 0.7 | window-2 | 0.5 | imitation | 0.0212 | 0.0219 | [0.0214, 0.0224] | < 1e-15 | robust |
| V3 (N=200, own) | 0.7 | window-3 | 1 | bayesian | 0.1335 | 0.1436 | [0.1366, 0.1506] | < 1e-15 | robust |
| V3 (N=200, own) | 0.7 | window-3 | 1 | imitation | 0.1439 | 0.1572 | [0.1505, 0.1639] | < 1e-15 | robust |
| V3 (N=200, own) | 0.7 | window-3 | 0.5 | bayesian | 0.0636 | 0.0681 | [0.0661, 0.0702] | < 1e-15 | robust |
| V3 (N=200, own) | 0.7 | window-3 | 0.5 | imitation | 0.0466 | 0.0486 | [0.0476, 0.0495] | < 1e-15 | robust |
<!-- END GENERATED TAB-S02 -->

## S7. EXP-004-R001 robustness at q = 0.60 and 0.80, all 72 comparisons (TAB-S03, EXPLORATORY)

Post hoc; not part of the frozen sensitivity analysis. Source: `results/exploratory/EXP-004-R001/tables/robustness_vs_EXP-002-R001.csv`.

<!-- BEGIN GENERATED TAB-S03 -->
| Variation | q | Network | v | Rule | EXP-002 Delta | Variation Delta | 95% CI | Holm p | Status |
|---|---|---|---|---|---|---|---|---|---|
| V1 (N=50, coin) | 0.6 | complete | 1 | bayesian | 0.0836 | 0.0294 | [0.0202, 0.0386] | 3.4e-09 | robust |
| V1 (N=50, coin) | 0.6 | complete | 1 | imitation | 0.0836 | 0.0294 | [0.0202, 0.0386] | 3.4e-09 | robust |
| V1 (N=50, coin) | 0.6 | complete | 0.5 | bayesian | 0.0783 | 0.0222 | [0.0133, 0.0310] | 1.7e-06 | robust |
| V1 (N=50, coin) | 0.6 | complete | 0.5 | imitation | 0.0783 | 0.0222 | [0.0133, 0.0310] | 1.7e-06 | robust |
| V1 (N=50, coin) | 0.6 | window-2 | 1 | bayesian | 0.0617 | 0.0246 | [0.0154, 0.0338] | 6.4e-07 | robust |
| V1 (N=50, coin) | 0.6 | window-2 | 1 | imitation | 0.0617 | 0.0289 | [0.0197, 0.0381] | 4.9e-09 | robust |
| V1 (N=50, coin) | 0.6 | window-2 | 0.5 | bayesian | 0.0225 | 0.0117 | [0.0089, 0.0145] | 2.3e-15 | robust |
| V1 (N=50, coin) | 0.6 | window-2 | 0.5 | imitation | 0.0132 | 0.0083 | [0.0062, 0.0104] | 6.7e-14 | robust |
| V1 (N=50, coin) | 0.6 | window-3 | 1 | bayesian | 0.0824 | 0.0275 | [0.0183, 0.0367] | 2.6e-08 | robust |
| V1 (N=50, coin) | 0.6 | window-3 | 1 | imitation | 0.0907 | 0.0245 | [0.0154, 0.0337] | 6.4e-07 | robust |
| V1 (N=50, coin) | 0.6 | window-3 | 0.5 | bayesian | 0.0349 | 0.0133 | [0.0085, 0.0180] | 2.8e-07 | robust |
| V1 (N=50, coin) | 0.6 | window-3 | 0.5 | imitation | 0.0274 | 0.0140 | [0.0106, 0.0173] | 2.5e-15 | robust |
| V1 (N=50, coin) | 0.8 | complete | 1 | bayesian | 0.1317 | 0.0520 | [0.0453, 0.0588] | < 1e-15 | robust |
| V1 (N=50, coin) | 0.8 | complete | 1 | imitation | 0.1317 | 0.0520 | [0.0453, 0.0588] | < 1e-15 | robust |
| V1 (N=50, coin) | 0.8 | complete | 0.5 | bayesian | 0.1251 | 0.0562 | [0.0498, 0.0626] | < 1e-15 | robust |
| V1 (N=50, coin) | 0.8 | complete | 0.5 | imitation | 0.1251 | 0.0562 | [0.0498, 0.0626] | < 1e-15 | robust |
| V1 (N=50, coin) | 0.8 | window-2 | 1 | bayesian | 0.1086 | 0.0528 | [0.0460, 0.0595] | < 1e-15 | robust |
| V1 (N=50, coin) | 0.8 | window-2 | 1 | imitation | 0.1086 | 0.0576 | [0.0509, 0.0643] | < 1e-15 | robust |
| V1 (N=50, coin) | 0.8 | window-2 | 0.5 | bayesian | 0.0363 | 0.0185 | [0.0164, 0.0206] | < 1e-15 | robust |
| V1 (N=50, coin) | 0.8 | window-2 | 0.5 | imitation | 0.0235 | 0.0143 | [0.0127, 0.0159] | < 1e-15 | robust |
| V1 (N=50, coin) | 0.8 | window-3 | 1 | bayesian | 0.1342 | 0.0595 | [0.0529, 0.0661] | < 1e-15 | robust |
| V1 (N=50, coin) | 0.8 | window-3 | 1 | imitation | 0.1394 | 0.0600 | [0.0534, 0.0666] | < 1e-15 | robust |
| V1 (N=50, coin) | 0.8 | window-3 | 0.5 | bayesian | 0.0704 | 0.0349 | [0.0313, 0.0385] | < 1e-15 | robust |
| V1 (N=50, coin) | 0.8 | window-3 | 0.5 | imitation | 0.0526 | 0.0323 | [0.0298, 0.0348] | < 1e-15 | robust |
| V2 (N=10, own) | 0.6 | complete | 1 | bayesian | 0.0836 | 0.0520 | [0.0455, 0.0586] | < 1e-15 | robust |
| V2 (N=10, own) | 0.6 | complete | 1 | imitation | 0.0836 | 0.0520 | [0.0455, 0.0586] | < 1e-15 | robust |
| V2 (N=10, own) | 0.6 | complete | 0.5 | bayesian | 0.0783 | 0.0348 | [0.0301, 0.0396] | < 1e-15 | robust |
| V2 (N=10, own) | 0.6 | complete | 0.5 | imitation | 0.0783 | 0.0348 | [0.0301, 0.0396] | < 1e-15 | robust |
| V2 (N=10, own) | 0.6 | window-2 | 1 | bayesian | 0.0617 | 0.0461 | [0.0389, 0.0532] | < 1e-15 | robust |
| V2 (N=10, own) | 0.6 | window-2 | 1 | imitation | 0.0617 | 0.0461 | [0.0389, 0.0532] | < 1e-15 | robust |
| V2 (N=10, own) | 0.6 | window-2 | 0.5 | bayesian | 0.0225 | 0.0150 | [0.0120, 0.0180] | < 1e-15 | robust |
| V2 (N=10, own) | 0.6 | window-2 | 0.5 | imitation | 0.0132 | 0.0108 | [0.0088, 0.0128] | < 1e-15 | robust |
| V2 (N=10, own) | 0.6 | window-3 | 1 | bayesian | 0.0824 | 0.0555 | [0.0490, 0.0621] | < 1e-15 | robust |
| V2 (N=10, own) | 0.6 | window-3 | 1 | imitation | 0.0907 | 0.0552 | [0.0489, 0.0614] | < 1e-15 | robust |
| V2 (N=10, own) | 0.6 | window-3 | 0.5 | bayesian | 0.0349 | 0.0226 | [0.0184, 0.0267] | < 1e-15 | robust |
| V2 (N=10, own) | 0.6 | window-3 | 0.5 | imitation | 0.0274 | 0.0212 | [0.0179, 0.0245] | < 1e-15 | robust |
| V2 (N=10, own) | 0.8 | complete | 1 | bayesian | 0.1317 | 0.0981 | [0.0941, 0.1022] | < 1e-15 | robust |
| V2 (N=10, own) | 0.8 | complete | 1 | imitation | 0.1317 | 0.0981 | [0.0941, 0.1022] | < 1e-15 | robust |
| V2 (N=10, own) | 0.8 | complete | 0.5 | bayesian | 0.1251 | 0.0645 | [0.0614, 0.0677] | < 1e-15 | robust |
| V2 (N=10, own) | 0.8 | complete | 0.5 | imitation | 0.1251 | 0.0645 | [0.0614, 0.0677] | < 1e-15 | robust |
| V2 (N=10, own) | 0.8 | window-2 | 1 | bayesian | 0.1086 | 0.0861 | [0.0816, 0.0906] | < 1e-15 | robust |
| V2 (N=10, own) | 0.8 | window-2 | 1 | imitation | 0.1086 | 0.0861 | [0.0816, 0.0906] | < 1e-15 | robust |
| V2 (N=10, own) | 0.8 | window-2 | 0.5 | bayesian | 0.0363 | 0.0270 | [0.0250, 0.0291] | < 1e-15 | robust |
| V2 (N=10, own) | 0.8 | window-2 | 0.5 | imitation | 0.0235 | 0.0198 | [0.0184, 0.0212] | < 1e-15 | robust |
| V2 (N=10, own) | 0.8 | window-3 | 1 | bayesian | 0.1342 | 0.0999 | [0.0959, 0.1039] | < 1e-15 | robust |
| V2 (N=10, own) | 0.8 | window-3 | 1 | imitation | 0.1394 | 0.0981 | [0.0942, 0.1020] | < 1e-15 | robust |
| V2 (N=10, own) | 0.8 | window-3 | 0.5 | bayesian | 0.0704 | 0.0466 | [0.0438, 0.0494] | < 1e-15 | robust |
| V2 (N=10, own) | 0.8 | window-3 | 0.5 | imitation | 0.0526 | 0.0399 | [0.0376, 0.0422] | < 1e-15 | robust |
| V3 (N=200, own) | 0.6 | complete | 1 | bayesian | 0.0836 | 0.0971 | [0.0882, 0.1059] | < 1e-15 | robust |
| V3 (N=200, own) | 0.6 | complete | 1 | imitation | 0.0836 | 0.0971 | [0.0882, 0.1059] | < 1e-15 | robust |
| V3 (N=200, own) | 0.6 | complete | 0.5 | bayesian | 0.0783 | 0.0861 | [0.0773, 0.0948] | < 1e-15 | robust |
| V3 (N=200, own) | 0.6 | complete | 0.5 | imitation | 0.0783 | 0.0861 | [0.0773, 0.0948] | < 1e-15 | robust |
| V3 (N=200, own) | 0.6 | window-2 | 1 | bayesian | 0.0617 | 0.0575 | [0.0483, 0.0667] | < 1e-15 | robust |
| V3 (N=200, own) | 0.6 | window-2 | 1 | imitation | 0.0617 | 0.0575 | [0.0483, 0.0667] | < 1e-15 | robust |
| V3 (N=200, own) | 0.6 | window-2 | 0.5 | bayesian | 0.0225 | 0.0191 | [0.0179, 0.0203] | < 1e-15 | robust |
| V3 (N=200, own) | 0.6 | window-2 | 0.5 | imitation | 0.0132 | 0.0120 | [0.0115, 0.0125] | < 1e-15 | robust |
| V3 (N=200, own) | 0.6 | window-3 | 1 | bayesian | 0.0824 | 0.0887 | [0.0797, 0.0976] | < 1e-15 | robust |
| V3 (N=200, own) | 0.6 | window-3 | 1 | imitation | 0.0907 | 0.1022 | [0.0934, 0.1110] | < 1e-15 | robust |
| V3 (N=200, own) | 0.6 | window-3 | 0.5 | bayesian | 0.0349 | 0.0403 | [0.0377, 0.0428] | < 1e-15 | robust |
| V3 (N=200, own) | 0.6 | window-3 | 0.5 | imitation | 0.0274 | 0.0280 | [0.0268, 0.0291] | < 1e-15 | robust |
| V3 (N=200, own) | 0.8 | complete | 1 | bayesian | 0.1317 | 0.1391 | [0.1345, 0.1437] | < 1e-15 | robust |
| V3 (N=200, own) | 0.8 | complete | 1 | imitation | 0.1317 | 0.1391 | [0.1345, 0.1437] | < 1e-15 | robust |
| V3 (N=200, own) | 0.8 | complete | 0.5 | bayesian | 0.1251 | 0.1347 | [0.1302, 0.1393] | < 1e-15 | robust |
| V3 (N=200, own) | 0.8 | complete | 0.5 | imitation | 0.1251 | 0.1347 | [0.1302, 0.1393] | < 1e-15 | robust |
| V3 (N=200, own) | 0.8 | window-2 | 1 | bayesian | 0.1086 | 0.1155 | [0.1102, 0.1209] | < 1e-15 | robust |
| V3 (N=200, own) | 0.8 | window-2 | 1 | imitation | 0.1086 | 0.1155 | [0.1102, 0.1209] | < 1e-15 | robust |
| V3 (N=200, own) | 0.8 | window-2 | 0.5 | bayesian | 0.0363 | 0.0397 | [0.0389, 0.0405] | < 1e-15 | robust |
| V3 (N=200, own) | 0.8 | window-2 | 0.5 | imitation | 0.0235 | 0.0249 | [0.0246, 0.0253] | < 1e-15 | robust |
| V3 (N=200, own) | 0.8 | window-3 | 1 | bayesian | 0.1342 | 0.1424 | [0.1380, 0.1468] | < 1e-15 | robust |
| V3 (N=200, own) | 0.8 | window-3 | 1 | imitation | 0.1394 | 0.1476 | [0.1434, 0.1518] | < 1e-15 | robust |
| V3 (N=200, own) | 0.8 | window-3 | 0.5 | bayesian | 0.0704 | 0.0727 | [0.0711, 0.0742] | < 1e-15 | robust |
| V3 (N=200, own) | 0.8 | window-3 | 0.5 | imitation | 0.0526 | 0.0537 | [0.0530, 0.0544] | < 1e-15 | robust |
<!-- END GENERATED TAB-S03 -->

## S8. Figures

| ID | File | Content | Source run |
|---|---|---|---|
| FIG-001 | `results/EXP-002/EXP-002-R001/figures/delta.svg` | Forest plot of the 48 EXP-002 contrasts with 95% intervals | EXP-002-R001 |
| FIG-002 | `results/EXP-002/EXP-002-R001/figures/accuracy_hist.svg` | Episode-accuracy histograms for every EXP-002 arm | EXP-002-R001 |
| FIG-003 | `results/EXP-003/EXP-003-R001/figures/delta.svg` | Forest plot of the 72 EXP-003 contrasts | EXP-003-R001 |
| FIG-004 | `results/exploratory/EXP-004-R001/figures/delta.svg` | Forest plot of the 72 EXP-004-R001 contrasts (exploratory) | EXP-004-R001 |

All figures are generated by `src/herd/report.py` from the run's `result.json` and raw arrays.
