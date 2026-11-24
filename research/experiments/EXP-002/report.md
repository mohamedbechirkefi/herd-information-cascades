<!-- SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0 -->
# EXP-002 report: social learning versus independent decisions across signal quality, network and visibility

## 1. Identification

- **Experiment:** EXP-002 (confirmatory). **Run:** EXP-002-R001 (the only run; no rerun).
- **Date:** executed 2026-11-25 (local time; 2026-11-24T23:31:31Z to 23:31:41Z UTC). Report version 1.0, 2026-11-25.
- **Status:** complete. Full frozen matrix executed, 0 failed cells, 61 of 61 verification checks passed.
- **Authorship:** Mohamed Bechir Kefi (no affiliation). An AI system was used as a research and development assistant and is not an author.
- **Protocol:** `research/experiments/EXP-002/protocol.md` v1.0, SHA-256 `36fbb89207fe9900366ae5a6d1e4d3654548564bde02ab536c3e2c7b1c0d0d7b`; study protocol `research/protocol.md` v1.0, SHA-256 `f73423c0bfd6f6463b1c1cb0d316e4ddc3942306eafe6793ba866112e72a457c`.
- **Configuration:** `experiments/EXP-002.json`, canonical SHA-256 `26e7cef89deddbb8a9d5bcdc95ae1b785f42e086a6b0e4b885731153312e9796` (file SHA-256 `278993cc19e4de08e0a4eb10479d11457f0138b81ad1ac0a4013c4b495363b51`), both as recorded in `research/freeze.json`.
- **Code revision:** `50fbdb1af8db41c1569013166365f17379dd05bd` (tree clean at run time; `dirty: false` in the run manifest).

## 2. Executive summary

- **Question.** For which combinations of signal quality $q$, observation network $G$ and visibility $v$ does using social information raise or lower mean decision accuracy relative to ignoring it?
- **Method.** Simulated sequential binary decisions, $N = 50$ agents, three homogeneous rules (independent baseline, exact Bayesian social learner, naive vote-counting imitator) on common random numbers, 24 cells ($q \in \{0.55, 0.60, 0.70, 0.80\}$ $\times$ {complete, window-2, window-3} $\times$ $v \in \{1, 0.5\}$), 10 seeds $\times$ 1,000 episodes = 10,000 paired episodes per contrast. Primary contrast: paired difference in episode accuracy against the independent baseline; two-sided paired t-tests, Holm over the non-degenerate contrasts.
- **Outcome.** All 48 contrasts were non-degenerate, so the Holm family has $m = 48$. All 48 are positive and Holm-significant (largest Holm-adjusted p-value $3.1 \times 10^{-14}$). Effects range from +0.0059 accuracy points (imitation, $q = 0.55$, window-2, $v = 0.5$; 95% CI [0.0048, 0.0070]) to +0.1439 (imitation, $q = 0.70$, window-3, $v = 1$; [0.1375, 0.1504]). H1 is supported. The pre-stated expectation that imitation would lose accuracy in some `window-k` cell at low $q$ is contradicted: imitation is significantly positive in every cell.
- **Principal caveat.** Social learning raised mean accuracy while producing frequent wrong cascades (for example 0.41 of episodes for both social rules at $q = 0.55$, complete, $v = 1$). The positive average hides a bimodal distribution of episode outcomes. EXP-003 shows that two contrasts ($q = 0.55$, window-3, $v = 1$) lose significance under coin-flip ties. All findings hold only inside this stylised model with synthetic agents.

## 3. Rationale and literature

Observing predecessors adds information, but once public evidence outweighs one private signal, agents stop revealing their signals and an informational cascade starts (Bikhchandani, Hirshleifer and Welch, 1992, BHW1992; Banerjee, 1992; verified abstracts or metadata, see `research/literature_review.md`). A cascade can lock in the wrong action. Naive agents who count observed actions as independent signals over-weight early movers (Eyster and Rabin, 2010, ER2010, verified abstract), which might make social information harmful. Restricted observation (Acemoglu, Dahleh, Lobel and Ozdaglar, 2011; Celen and Kariv, 2004) changes how far early actions propagate. The gap addressed here is a paired, exact-posterior comparison of the two social rules against the same independent baseline across a grid of signal quality, recent-window networks and partial visibility, with the error-cascade metrics reported next to accuracy. The full texts of BHW1992, CK2004 and ER2010 have not been checked (open literature item in `roadmap.md`).

## 4. Hypotheses and operational definitions

- **Estimand:** $\Delta_r(c) = E_e[\mathrm{Acc}_r(e) - \mathrm{Acc}_{\mathrm{ind}}(e)]$, with $\mathrm{Acc}(e) = \frac{1}{N}\sum_i \mathbb{1}[a_i = \theta]$ (proportion, 0 to 1).
- **H0:** $\Delta_r(c) = 0$ for both social rules and all 24 cells. **H1:** $\Delta_r(c) \neq 0$ for at least one $(r, c)$.
- **Directional expectations (pre-stated):** Bayesian $\Delta \geq 0$ everywhere; imitation $\Delta$ equals Bayesian $\Delta$ under `complete`; imitation $\Delta < 0$ in at least one `window-k` cell at low $q$.
- **Disconfirmation:** H1 is not supported if no contrast is Holm-significant and no degenerate contrast has a non-zero exact difference. A significantly negative Bayesian $\Delta$, or any Bayesian and imitation divergence under `complete`, stops interpretation. The imitation expectation is contradicted if imitation $\Delta$ is significantly positive in every cell (study protocol section 3).
- **Secondary metrics** (descriptive, 95% intervals, no multiplicity adjustment): cascade probability, wrong-cascade probability, longest wrong run (agents), informative-action share, action entropy (bits), last-agent accuracy. Definitions in `research/protocol.md` section 4.
- **Control:** the independent rule ($a_i = s_i$) on the same episode.

## 5. Methodology

- **Model:** hidden state $\theta \in \{0,1\}$ with prior 1/2; private binary signals of precision $q$; each action publicly recorded with probability $v$, the visibility pattern common knowledge; agent $i$ observes visible actions in $O_i$ (complete history or the last $k$ positions). Bayesian posteriors are exact (public-belief recursion for `complete`, forward recursion over the $2^k$ window states for `window-k`), own-signal tie rule. Imitation: $a_i = \mathbb{1}[n_1 - n_0 + (2s_i - 1) > 0]$, ties to the own signal. Code: `src/herd/rules.py`, `src/herd/model.py`, `src/herd/generate.py`.
- **Data:** synthetic only (C1); episodes drawn from numpy `SeedSequence` streams keyed by (master seed, cell); all rules share each episode (common random numbers). No external data.
- **Parameters and seeds:** as in Section 2; master seeds 0 to 9; bootstrap 2,000 resamples, seed 20261124.
- **Hardware and software:** Apple M1 Pro, 16 GB, macOS 15.3.1 (Darwin 24.3.0); Python 3.12.1, numpy 2.3.4, result schema 1.0.0; one process run under `nice -n 10`.
- **Budget:** planned under one hour; actual 8.73 s wall-clock, peak resident memory 158 MB.
- **Statistical plan (frozen):** per contrast, mean paired difference with a normal-approximation 95% interval at the episode level, percentile bootstrap check, two-sided paired t-test, Holm adjustment over the non-degenerate contrasts among 48 (familywise 0.05); degenerate contrasts would be exact comparisons outside the family (A-3); intervals are unadjusted (A-4).

## 6. Implementation verification

- **Test suite before the run:** 278 passed (`.venv/bin/python -m pytest`, revision `eded9b8`). After the session's additions: 281 passed.
- **Pre-confirmatory smoke run** EXP-001-R005 (exploratory seeds 100 and 101): 25 of 25 checks passed (see the EXP-001 report).
- **In-run checks (61, all passed):** C1 analytic wrong-cascade anchor for Bayesian, complete, $v = 1$ at each $q$ (observed 0.4084, 0.3098, 0.1550, 0.0597 against analytic 0.4010, 0.3077, 0.1552, 0.0588, all inside Wilson 99% intervals); C3 independent accuracy equals $q$ with zero cascades (24 cells); C4 Bayesian and imitation actions identical on all 10,000 episodes of each of the 8 `complete` cells; C5 schema validity; C6 no near ties in Bayesian comparisons (24 cells).
- **Faithfulness:** the C4 equivalence and C1 anchor confirm that the Bayesian rule and the imitation rule are implemented as specified in the `complete` setting; the `window-k` recursion is checked against the exact rational oracle in the unit tests ($N \leq 9$).

## 7. Execution record

- **Commands:**
  - `PYTHONPATH=src nice -n 10 .venv/bin/python -m herd.cli run --config experiments/EXP-002.json` (exit status 0)
  - `PYTHONPATH=src .venv/bin/python -m herd.cli report --run results/EXP-002/EXP-002-R001`
  - `PYTHONPATH=src .venv/bin/python -m herd.tables contrasts --run results/EXP-002/EXP-002-R001` (Section 8 tables)
- **Run gate:** passed (registry and `research/freeze.json` hashes matched the files on disk).
- **Run:** EXP-002-R001, config hash as in Section 1, seeds 0 to 9, data manifest `data/manifest.json` (synthetic only).
- **Sample counts:** 72 arms $\times$ 10,000 episodes; 48 contrasts of 10,000 paired episodes each; 36,000,000 agent decisions. No failed cell, no dropped run, no excluded episode.
- **Deviations from the frozen protocol:** none in the execution or analysis. Two reporting-layer changes, made after the run and changing no estimate: the generated run report's figure captions said "Exploratory." for every run (fixed in `src/herd/report.py`, reports regenerated; D-010); the reproduction command of the protocol's section 13 (`report --exp`) does not exist and `report --run` was used, as already recorded at the freeze.

## 8. Results

### 8.1 Primary contrasts

Holm family size $m = 48$ (no degenerate contrast). All 48 contrasts positive and Holm-significant. Every contrast is positive in all 10 seeds. The normal and bootstrap intervals differ by at most 0.0006.

Figure: `results/EXP-002/EXP-002-R001/figures/delta.svg` (forest plot of all 48 contrasts with 95% intervals). Episode-accuracy distributions per arm: `results/EXP-002/EXP-002-R001/figures/accuracy_hist.svg`.

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

### 8.2 Secondary metrics (descriptive, means with 95% intervals over 10,000 episodes)

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

### 8.3 Runtime

8.73 s wall-clock (simulation 4.79 s, 0.133 ms per 1,000 agent decisions; analysis 3.32 s); peak resident memory 158,318,592 bytes.

## 9. Interpretation

- **Measured.** In every one of the 24 cells, both social rules raised mean episode accuracy over the independent baseline, by between 0.6 and 14.4 accuracy points (relative to a baseline of $q$, between about 1% and 21%). The gain grows with $q$ up to $q = 0.7$ and then levels off under `complete` and `window-3` with full visibility. Halving visibility shrinks the gain sharply in the window networks (for example Bayesian, $q = 0.7$: window-2 from 0.0992 to 0.0337) but only slightly under `complete` (0.1344 to 0.1216).
- **Against the pre-stated expectations.** Bayesian $\Delta \geq 0$ everywhere: consistent (no Bayesian contrast below zero, so the stopping rule was not triggered). Imitation equals Bayesian under `complete`: confirmed exactly (C4). Imitation $\Delta < 0$ in some `window-k` cell at low $q$: contradicted; the smallest imitation effect is +0.0059 [0.0048, 0.0070] and is still Holm-significant. Under this model, naive vote counting did not make social information harmful on average.
- **Cascades of errors coexist with the average gain.** Wrong-cascade probabilities for the social rules range up to 0.87 (imitation, $q = 0.55$, window-3, $v = 0.5$), and the longest wrong run of Bayesian agents averages about 20 of 50 agents at $q = 0.55$ under full visibility, against about 4.4 for the baseline. The accuracy histograms are bimodal: social information makes most episodes much better and a substantial minority much worse. A positive mean difference is therefore not a statement that social information helps every group.
- **Exploratory observation (not a planned test).** Imitation and Bayesian differ only in the window networks. Under window-3 with $v = 1$ the imitation gain exceeds the Bayesian gain by 0.002 to 0.010 points; under window-2 with $v = 1$ the two rules give the same contrast; in both window networks with $v = 0.5$ the imitation gain is lower by 0.003 to 0.018 points. No paired imitation-versus-Bayesian test was planned, so these differences carry no inferential claim; they suggest that the individually optimal rule need not maximise group accuracy, which is a known theme of the cascade literature and a candidate for a new preregistered experiment.
- **Alternatives.** Information quantity rather than structure: visibility varies quantity within each network, and the gain depends on both, so neither explanation is excluded. Tie convention and horizon: tested in EXP-003, where two contrasts ($q = 0.55$, window-3, $v = 1$) lose significance under coin ties and none reverses sign. Implementation error: guarded by C1 to C6 and the oracle tests.
- **Verdict under the frozen rule.** H0 is rejected for all 48 contrasts at familywise 0.05; H1 is supported. The directional expectation for imitation is contradicted.

## 10. Threats to validity

- **Internal:** a shared implementation error could move both social rules together; the C1 anchor, C4 equivalence and the rational oracle reduce but cannot remove this risk for the `window-k` code at $N = 50$ (the oracle stops at $N \leq 9$).
- **Construct:** episode accuracy averages over agents and depends on $N$; wrong-cascade "any agent" counts an episode once even if the cascade is broken later (possible under partial visibility and window networks), which explains why wrong-cascade probabilities exceed 0.8 while accuracy improves.
- **Statistical:** 48 tests corrected by Holm; normal intervals agree with the bootstrap; episodes are independent by construction. The p-values are extremely small because the sample is large; magnitudes, not p-values, carry the substantive message.
- **External:** synthetic, homogeneous agents with common knowledge of rules, binary symmetric signals and recent-window networks only. Nothing here establishes real human rationality or irrationality, or behaviour on any real platform.

## 11. Conclusion and next experiment

Within this model, using social information raised mean decision accuracy against the independent baseline in all 24 cells and for both rules, while producing frequent and long cascades of errors in individual episodes. The expected harm from naive imitation in restricted networks at low signal quality did not appear. Follow-ups that would need a new preregistered protocol: a planned paired comparison of imitation against Bayesian in the window networks; imitation rules with stronger over-weighting; heterogeneous populations; a distributional estimand (probability that a group ends worse than the baseline).

## 12. Reproduction appendix

- **Environment:** `../.tools/py/bin/uv sync --frozen --all-groups --all-extras` (Python 3.12.1, numpy 2.3.4, pytest 8.4.2; `uv.lock`). Test: `.venv/bin/python -m pytest` (281 passed at the session's final revision).
- **Data manifest:** `data/manifest.json` (synthetic only; no external dataset).
- **Run:** `PYTHONPATH=src .venv/bin/python -m herd.cli run --config experiments/EXP-002.json` (needs a fresh output folder; existing results are never overwritten).
- **Report and figures:** `PYTHONPATH=src .venv/bin/python -m herd.cli report --run results/EXP-002/EXP-002-R001`; tables: `PYTHONPATH=src .venv/bin/python -m herd.tables contrasts|secondary --run results/EXP-002/EXP-002-R001`.
- **Raw results:** `results/EXP-002/EXP-002-R001/result.json` (SHA-256 `86171fe73d39a30468a0b9e2fed8c2c4d1f16d808a635a259aaa94f56bc48a29`), `results/raw/EXP-002-R001/episodes.npz` (per-episode metrics, SHA-256 `d3b1c7192803f0dd15adf41f9a1d0799dba840210f25f9e205b304085f8be07d`), `run_manifest.json`; every file hash in `results/EXP-002/SHA256SUMS`.
- **Expected tolerance:** the run is deterministic for a given numpy version; a rerun on the same stack should reproduce `result.json` estimates exactly (timing fields differ).
- **References:** see `research/literature_review.md` (BHW1992, Banerjee1992, CK2004, ER2010, ADLO2011; metadata and abstracts verified, full texts not yet checked).
