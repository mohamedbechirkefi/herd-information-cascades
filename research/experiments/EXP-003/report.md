<!-- SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0 -->
# EXP-003 report: sensitivity of the EXP-002 contrasts to the tie rule and the horizon

## 1. Identification

- **Experiment:** EXP-003 (confirmatory sensitivity). **Run:** EXP-003-R001 (the only run; no rerun).
- **Date:** executed 2026-11-25 (local time; 2026-11-24T23:31:45Z to 23:32:05Z UTC). Report version 1.0, 2026-11-25.
- **Status:** complete. Full frozen matrix executed, 0 failed cells, 89 of 89 verification checks passed.
- **Authorship:** Mohamed Bechir Kefi (no affiliation). An AI system was used as a research and development assistant and is not an author.
- **Protocol:** `research/experiments/EXP-003/protocol.md` v1.0, SHA-256 `fd0b7c9e361f196c62b0af093503b25b757e814c42557314489bcee899045db5`; study protocol v1.0, SHA-256 `f73423c0bfd6f6463b1c1cb0d316e4ddc3942306eafe6793ba866112e72a457c`.
- **Configuration:** `experiments/EXP-003.json`, canonical SHA-256 `12ebfabeef1fca01b598cc0026c22a2cd1b30be6ad39b96386decc8f0ee8584a` (file SHA-256 `36da498387a4378d5ba3052642f8f4d598b0d0d1d508b9446a8f34b603f2557d`), as recorded in `research/freeze.json`.
- **Code revision:** `50fbdb1af8db41c1569013166365f17379dd05bd` (tree clean at run time), the same revision as EXP-002.

## 2. Executive summary

- **Question.** Do the signs and Holm significance of the EXP-002 contrasts survive (V1) coin-flip tie-breaking instead of own-signal tie-breaking and horizons (V2) $N = 10$ and (V3) $N = 200$ instead of $N = 50$?
- **Method.** The EXP-002 design on 12 cells ($q \in \{0.55, 0.70\}$ $\times$ {complete, window-2, window-3} $\times$ $v \in \{1, 0.5\}$), three rules, seeds 0 to 9, 1,000 episodes per seed and cell, under each of the three variations; Holm within each variation over its non-degenerate contrasts; the frozen interpretation rule compares each EXP-002 Holm-significant contrast with the same contrast under each variation.
- **Outcome.** No contrast was degenerate (Holm family $m = 24$ in each variation). Of the 72 comparisons (24 EXP-002 contrasts $\times$ 3 variations), 70 are robust (same sign, Holm-significant), none reverses sign, and 2 lose significance: under V1 (coin ties), $q = 0.55$, window-3, $v = 1$, Bayesian $\Delta = 0.0082$ (95% CI [-0.0013, 0.0176], Holm p = 0.18) and imitation $\Delta = 0.0079$ ([-0.0015, 0.0174], Holm p = 0.18), against 0.0424 and 0.0448 in EXP-002. H1 of EXP-003 holds for these two contrasts, which are therefore reported as convention-dependent; the other 22 EXP-002 contrasts in this grid are robust to all three variations.
- **Principal caveat.** Coin-flip ties reduce every social-learning gain (V1 effects range from 0.0036 to 0.0494, against 0.0059 to 0.1439 for the same cells in EXP-002). The loss of significance is not evidence that the effect is zero.

## 3. Rationale and literature

Under coin-flip ties, which the protocol describes as the convention of BHW1992 (a model detail beyond the abstract, not verified against the full text; M4 audit, 2026-11-25), an agent with a balanced posterior acts at random, so cascades can start one agent earlier and early actions carry less information. Averaging accuracy over $N$ agents weights pre-cascade agents by about $1/N$, so a short horizon can hide the cost of a wrong cascade and a long one can amplify it. Either convention could reverse a conclusion drawn from EXP-002 (EXP-003 protocol section 2; references in `research/literature_review.md`; full texts of BHW1992 not yet checked).

## 4. Hypotheses and operational definitions

- **H0 (robustness):** for every $(r, c)$ that is Holm-significant in EXP-002, the sign of $\Delta_r(c)$ is the same under each variation.
- **H1:** at least one sign reverses or loses significance under a variation.
- **Interpretation rule (fixed in advance):** if H1 holds for any contrast, the EXP-002 conclusion for that contrast is reported as convention-dependent.
- **Operationalisation of the rule** (`src/herd/robustness.py`, written after the runs, see Section 7): for each EXP-002 contrast with Holm-adjusted p below 0.05 and each variation containing its cell, "robust" if the sign of the mean paired difference is unchanged and the variation's contrast is Holm-significant (Holm-adjusted p below 0.05 within the variation's family, A-4); "sign reversed" if the sign changes; "lost significance" otherwise.
- **Estimand, metrics, control and uncertainty:** as in EXP-002 (paired accuracy difference against the independent baseline; normal 95% interval with bootstrap check; Holm within each variation).

## 5. Methodology

- **Model and rules:** as in EXP-002. Under coin ties, a Bayesian agent with posterior exactly 1/2 and an imitator with a zero count act on a fair coin drawn from a separate stream, so the episode draws ($\theta$, signals, visibility) match EXP-002 for the same seed and cell.
- **Data:** synthetic only; common random numbers across rules.
- **Variations:** V1 coin ties, $N = 50$; V2 own-signal ties, $N = 10$; V3 own-signal ties, $N = 200$.
- **Hardware and software:** Apple M1 Pro, 16 GB, macOS 15.3.1; Python 3.12.1, numpy 2.3.4; one process under `nice -n 10`.
- **Budget:** planned about 1.5 times EXP-002; actual 19.47 s wall-clock, peak resident memory 280 MB.
- **Statistical plan (frozen):** as in EXP-002, per variation.

## 6. Implementation verification

- Tests before the run: 278 passed; after the session's additions: 281 passed. The pre-confirmatory smoke run EXP-001-R005 passed 25 of 25 checks.
- In-run checks (89, all passed): C1 analytic anchor under own ties (V2: 0.3740 and 0.1479 against 0.3769 and 0.1503; V3: 0.3989 and 0.1522 against 0.4010 and 0.1552; all inside Wilson 99% intervals); C3 independent baseline (36 cells); C4 complete-network equivalence under own ties (8 cells, 0 differing episodes); C5 schema; C6 no near ties (36 cells); C7 diagnostic under coin ties (no prediction, amendment A-2): 0 of 10,000 episodes differ between Bayesian and imitation actions in each of the 4 V1 `complete` cells.
- The stochastic coin-tie case of the `window-k` recursion is covered by unit tests against the exact rational oracle (`tests/test_reference.py`), which enumerates coin profiles for $N \leq 9$.

## 7. Execution record

- **Commands:**
  - `PYTHONPATH=src nice -n 10 .venv/bin/python -m herd.cli run --config experiments/EXP-003.json` (exit status 0)
  - `PYTHONPATH=src .venv/bin/python -m herd.cli report --run results/EXP-003/EXP-003-R001`
  - `PYTHONPATH=src .venv/bin/python -m herd.robustness --reference results/EXP-002/EXP-002-R001 --sensitivity results/EXP-003/EXP-003-R001` (output "72 comparisons: {'robust': 70, 'lost significance': 2}")
  - `PYTHONPATH=src .venv/bin/python -m herd.tables contrasts --run results/EXP-003/EXP-003-R001` and `herd.tables robustness --csv results/EXP-003/EXP-003-R001/tables/robustness_vs_EXP-002-R001.csv`
- **Run gate:** passed. **Run:** EXP-003-R001, seeds 0 to 9.
- **Sample counts:** 108 arms $\times$ 10,000 episodes; 72 contrasts of 10,000 paired episodes; 93,600,000 agent decisions. No failed cell, no dropped run, no excluded episode.
- **Deviations from the frozen protocol:** none in the execution or the estimates. The EXP-003 decision rule was stated in the protocol but had no implementation before the run; `src/herd/robustness.py` was written after both runs to apply it mechanically, with a unit test on hand-built contrasts (D-010). It reads the frozen estimates and Holm p-values and computes nothing new; the only operational choice is that "loses significance" means "not Holm-significant in the variation's family", which is the protocol's own definition (A-4). The figure-caption fix of the run report generator (D-010) also applies here.

## 8. Results

### 8.1 Robustness of the EXP-002 contrasts (frozen interpretation rule)

Holm family size $m = 24$ in each variation (no degenerate contrast). 70 robust, 0 sign reversed, 2 lost significance. Largest Holm-adjusted p-value per variation: V1 0.18, V2 $7.2 \times 10^{-8}$, V3 $7.3 \times 10^{-13}$. Per-seed signs: every V3 contrast is positive in all 10 seeds; V2: 22 contrasts in 10 seeds and 2 in 9; V1: 13 in 10 seeds, 1 in 9, 7 in 8 and 3 in 7.

Figure: `results/EXP-003/EXP-003-R001/figures/delta.svg` (forest plot, 72 contrasts with 95% intervals); distributions in `figures/accuracy_hist.svg`. Machine-readable table: `results/EXP-003/EXP-003-R001/tables/robustness_vs_EXP-002-R001.csv`.

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

### 8.2 All contrasts

| Variation | q | Network | v | Rule | n | Delta | 95% CI | Bootstrap 95% CI | Holm p | Holm-significant |
|---|---|---|---|---|---|---|---|---|---|---|
| V1 (N=50, coin) | 0.55 | complete | 1 | bayesian | 10000 | 0.0148 | [0.0054, 0.0243] | [0.0054, 0.0239] | 0.012 | yes |
| V1 (N=50, coin) | 0.55 | complete | 1 | imitation | 10000 | 0.0148 | [0.0054, 0.0243] | [0.0054, 0.0239] | 0.012 | yes |
| V1 (N=50, coin) | 0.55 | complete | 0.5 | bayesian | 10000 | 0.0136 | [0.0046, 0.0226] | [0.0051, 0.0225] | 0.013 | yes |
| V1 (N=50, coin) | 0.55 | complete | 0.5 | imitation | 10000 | 0.0136 | [0.0046, 0.0226] | [0.0051, 0.0225] | 0.013 | yes |
| V1 (N=50, coin) | 0.55 | window-2 | 1 | bayesian | 10000 | 0.0176 | [0.0081, 0.0270] | [0.0078, 0.0274] | 0.0024 | yes |
| V1 (N=50, coin) | 0.55 | window-2 | 1 | imitation | 10000 | 0.0195 | [0.0101, 0.0289] | [0.0100, 0.0290] | 0.00051 | yes |
| V1 (N=50, coin) | 0.55 | window-2 | 0.5 | bayesian | 10000 | 0.0049 | [0.0021, 0.0078] | [0.0020, 0.0076] | 0.006 | yes |
| V1 (N=50, coin) | 0.55 | window-2 | 0.5 | imitation | 10000 | 0.0036 | [0.0015, 0.0057] | [0.0014, 0.0056] | 0.0065 | yes |
| V1 (N=50, coin) | 0.55 | window-3 | 1 | bayesian | 10000 | 0.0082 | [-0.0013, 0.0176] | [-0.0015, 0.0178] | 0.18 | no |
| V1 (N=50, coin) | 0.55 | window-3 | 1 | imitation | 10000 | 0.0079 | [-0.0015, 0.0174] | [-0.0015, 0.0177] | 0.18 | no |
| V1 (N=50, coin) | 0.55 | window-3 | 0.5 | bayesian | 10000 | 0.0142 | [0.0093, 0.0191] | [0.0093, 0.0192] | 1.9e-07 | yes |
| V1 (N=50, coin) | 0.55 | window-3 | 0.5 | imitation | 10000 | 0.0106 | [0.0072, 0.0140] | [0.0073, 0.0141] | 9.8e-09 | yes |
| V1 (N=50, coin) | 0.7 | complete | 1 | bayesian | 10000 | 0.0494 | [0.0411, 0.0576] | [0.0414, 0.0572] | < 1e-15 | yes |
| V1 (N=50, coin) | 0.7 | complete | 1 | imitation | 10000 | 0.0494 | [0.0411, 0.0576] | [0.0414, 0.0572] | < 1e-15 | yes |
| V1 (N=50, coin) | 0.7 | complete | 0.5 | bayesian | 10000 | 0.0476 | [0.0397, 0.0555] | [0.0398, 0.0559] | < 1e-15 | yes |
| V1 (N=50, coin) | 0.7 | complete | 0.5 | imitation | 10000 | 0.0476 | [0.0397, 0.0555] | [0.0398, 0.0559] | < 1e-15 | yes |
| V1 (N=50, coin) | 0.7 | window-2 | 1 | bayesian | 10000 | 0.0344 | [0.0259, 0.0428] | [0.0262, 0.0427] | 2.2e-14 | yes |
| V1 (N=50, coin) | 0.7 | window-2 | 1 | imitation | 10000 | 0.0413 | [0.0329, 0.0496] | [0.0331, 0.0496] | < 1e-15 | yes |
| V1 (N=50, coin) | 0.7 | window-2 | 0.5 | bayesian | 10000 | 0.0181 | [0.0156, 0.0207] | [0.0156, 0.0205] | < 1e-15 | yes |
| V1 (N=50, coin) | 0.7 | window-2 | 0.5 | imitation | 10000 | 0.0147 | [0.0128, 0.0165] | [0.0127, 0.0164] | < 1e-15 | yes |
| V1 (N=50, coin) | 0.7 | window-3 | 1 | bayesian | 10000 | 0.0469 | [0.0387, 0.0552] | [0.0384, 0.0551] | < 1e-15 | yes |
| V1 (N=50, coin) | 0.7 | window-3 | 1 | imitation | 10000 | 0.0481 | [0.0399, 0.0563] | [0.0397, 0.0562] | < 1e-15 | yes |
| V1 (N=50, coin) | 0.7 | window-3 | 0.5 | bayesian | 10000 | 0.0284 | [0.0240, 0.0328] | [0.0239, 0.0326] | < 1e-15 | yes |
| V1 (N=50, coin) | 0.7 | window-3 | 0.5 | imitation | 10000 | 0.0279 | [0.0249, 0.0309] | [0.0247, 0.0308] | < 1e-15 | yes |
| V2 (N=10, own) | 0.55 | complete | 1 | bayesian | 10000 | 0.0305 | [0.0237, 0.0373] | [0.0238, 0.0375] | < 1e-15 | yes |
| V2 (N=10, own) | 0.55 | complete | 1 | imitation | 10000 | 0.0305 | [0.0237, 0.0373] | [0.0238, 0.0375] | < 1e-15 | yes |
| V2 (N=10, own) | 0.55 | complete | 0.5 | bayesian | 10000 | 0.0192 | [0.0142, 0.0242] | [0.0143, 0.0245] | 4.1e-13 | yes |
| V2 (N=10, own) | 0.55 | complete | 0.5 | imitation | 10000 | 0.0192 | [0.0142, 0.0242] | [0.0143, 0.0245] | 4.1e-13 | yes |
| V2 (N=10, own) | 0.55 | window-2 | 1 | bayesian | 10000 | 0.0254 | [0.0181, 0.0327] | [0.0184, 0.0328] | 5.7e-11 | yes |
| V2 (N=10, own) | 0.55 | window-2 | 1 | imitation | 10000 | 0.0254 | [0.0181, 0.0327] | [0.0184, 0.0328] | 5.7e-11 | yes |
| V2 (N=10, own) | 0.55 | window-2 | 0.5 | bayesian | 10000 | 0.0085 | [0.0054, 0.0116] | [0.0054, 0.0118] | 7.2e-08 | yes |
| V2 (N=10, own) | 0.55 | window-2 | 0.5 | imitation | 10000 | 0.0074 | [0.0053, 0.0094] | [0.0053, 0.0095] | 9.8e-12 | yes |
| V2 (N=10, own) | 0.55 | window-3 | 1 | bayesian | 10000 | 0.0326 | [0.0259, 0.0393] | [0.0260, 0.0396] | < 1e-15 | yes |
| V2 (N=10, own) | 0.55 | window-3 | 1 | imitation | 10000 | 0.0313 | [0.0248, 0.0377] | [0.0249, 0.0379] | < 1e-15 | yes |
| V2 (N=10, own) | 0.55 | window-3 | 0.5 | bayesian | 10000 | 0.0132 | [0.0089, 0.0175] | [0.0089, 0.0175] | 4.8e-09 | yes |
| V2 (N=10, own) | 0.55 | window-3 | 0.5 | imitation | 10000 | 0.0105 | [0.0071, 0.0139] | [0.0072, 0.0139] | 4.8e-09 | yes |
| V2 (N=10, own) | 0.7 | complete | 1 | bayesian | 10000 | 0.0957 | [0.0902, 0.1011] | [0.0902, 0.1010] | < 1e-15 | yes |
| V2 (N=10, own) | 0.7 | complete | 1 | imitation | 10000 | 0.0957 | [0.0902, 0.1011] | [0.0902, 0.1010] | < 1e-15 | yes |
| V2 (N=10, own) | 0.7 | complete | 0.5 | bayesian | 10000 | 0.0606 | [0.0565, 0.0648] | [0.0564, 0.0650] | < 1e-15 | yes |
| V2 (N=10, own) | 0.7 | complete | 0.5 | imitation | 10000 | 0.0606 | [0.0565, 0.0648] | [0.0564, 0.0650] | < 1e-15 | yes |
| V2 (N=10, own) | 0.7 | window-2 | 1 | bayesian | 10000 | 0.0831 | [0.0771, 0.0891] | [0.0773, 0.0891] | < 1e-15 | yes |
| V2 (N=10, own) | 0.7 | window-2 | 1 | imitation | 10000 | 0.0831 | [0.0771, 0.0891] | [0.0773, 0.0891] | < 1e-15 | yes |
| V2 (N=10, own) | 0.7 | window-2 | 0.5 | bayesian | 10000 | 0.0236 | [0.0209, 0.0263] | [0.0210, 0.0263] | < 1e-15 | yes |
| V2 (N=10, own) | 0.7 | window-2 | 0.5 | imitation | 10000 | 0.0172 | [0.0154, 0.0191] | [0.0155, 0.0191] | < 1e-15 | yes |
| V2 (N=10, own) | 0.7 | window-3 | 1 | bayesian | 10000 | 0.0924 | [0.0869, 0.0979] | [0.0870, 0.0979] | < 1e-15 | yes |
| V2 (N=10, own) | 0.7 | window-3 | 1 | imitation | 10000 | 0.0893 | [0.0840, 0.0946] | [0.0840, 0.0946] | < 1e-15 | yes |
| V2 (N=10, own) | 0.7 | window-3 | 0.5 | bayesian | 10000 | 0.0388 | [0.0352, 0.0424] | [0.0353, 0.0423] | < 1e-15 | yes |
| V2 (N=10, own) | 0.7 | window-3 | 0.5 | imitation | 10000 | 0.0329 | [0.0300, 0.0358] | [0.0301, 0.0358] | < 1e-15 | yes |
| V3 (N=200, own) | 0.55 | complete | 1 | bayesian | 10000 | 0.0505 | [0.0410, 0.0599] | [0.0411, 0.0597] | < 1e-15 | yes |
| V3 (N=200, own) | 0.55 | complete | 1 | imitation | 10000 | 0.0505 | [0.0410, 0.0599] | [0.0411, 0.0597] | < 1e-15 | yes |
| V3 (N=200, own) | 0.55 | complete | 0.5 | bayesian | 10000 | 0.0432 | [0.0339, 0.0525] | [0.0344, 0.0522] | < 1e-15 | yes |
| V3 (N=200, own) | 0.55 | complete | 0.5 | imitation | 10000 | 0.0432 | [0.0339, 0.0525] | [0.0344, 0.0522] | < 1e-15 | yes |
| V3 (N=200, own) | 0.55 | window-2 | 1 | bayesian | 10000 | 0.0354 | [0.0259, 0.0449] | [0.0261, 0.0442] | 7.3e-13 | yes |
| V3 (N=200, own) | 0.55 | window-2 | 1 | imitation | 10000 | 0.0354 | [0.0259, 0.0449] | [0.0261, 0.0442] | 7.3e-13 | yes |
| V3 (N=200, own) | 0.55 | window-2 | 0.5 | bayesian | 10000 | 0.0106 | [0.0093, 0.0118] | [0.0093, 0.0119] | < 1e-15 | yes |
| V3 (N=200, own) | 0.55 | window-2 | 0.5 | imitation | 10000 | 0.0068 | [0.0062, 0.0073] | [0.0062, 0.0073] | < 1e-15 | yes |
| V3 (N=200, own) | 0.55 | window-3 | 1 | bayesian | 10000 | 0.0462 | [0.0368, 0.0557] | [0.0365, 0.0557] | < 1e-15 | yes |
| V3 (N=200, own) | 0.55 | window-3 | 1 | imitation | 10000 | 0.0549 | [0.0455, 0.0643] | [0.0456, 0.0642] | < 1e-15 | yes |
| V3 (N=200, own) | 0.55 | window-3 | 0.5 | bayesian | 10000 | 0.0202 | [0.0176, 0.0228] | [0.0176, 0.0228] | < 1e-15 | yes |
| V3 (N=200, own) | 0.55 | window-3 | 0.5 | imitation | 10000 | 0.0154 | [0.0143, 0.0166] | [0.0142, 0.0165] | < 1e-15 | yes |
| V3 (N=200, own) | 0.7 | complete | 1 | bayesian | 10000 | 0.1452 | [0.1383, 0.1522] | [0.1382, 0.1522] | < 1e-15 | yes |
| V3 (N=200, own) | 0.7 | complete | 1 | imitation | 10000 | 0.1452 | [0.1383, 0.1522] | [0.1382, 0.1522] | < 1e-15 | yes |
| V3 (N=200, own) | 0.7 | complete | 0.5 | bayesian | 10000 | 0.1391 | [0.1322, 0.1460] | [0.1325, 0.1461] | < 1e-15 | yes |
| V3 (N=200, own) | 0.7 | complete | 0.5 | imitation | 10000 | 0.1391 | [0.1322, 0.1460] | [0.1325, 0.1461] | < 1e-15 | yes |
| V3 (N=200, own) | 0.7 | window-2 | 1 | bayesian | 10000 | 0.1033 | [0.0956, 0.1110] | [0.0955, 0.1106] | < 1e-15 | yes |
| V3 (N=200, own) | 0.7 | window-2 | 1 | imitation | 10000 | 0.1033 | [0.0956, 0.1110] | [0.0955, 0.1106] | < 1e-15 | yes |
| V3 (N=200, own) | 0.7 | window-2 | 0.5 | bayesian | 10000 | 0.0347 | [0.0337, 0.0357] | [0.0336, 0.0358] | < 1e-15 | yes |
| V3 (N=200, own) | 0.7 | window-2 | 0.5 | imitation | 10000 | 0.0219 | [0.0214, 0.0224] | [0.0214, 0.0224] | < 1e-15 | yes |
| V3 (N=200, own) | 0.7 | window-3 | 1 | bayesian | 10000 | 0.1436 | [0.1366, 0.1506] | [0.1365, 0.1509] | < 1e-15 | yes |
| V3 (N=200, own) | 0.7 | window-3 | 1 | imitation | 10000 | 0.1572 | [0.1505, 0.1639] | [0.1500, 0.1640] | < 1e-15 | yes |
| V3 (N=200, own) | 0.7 | window-3 | 0.5 | bayesian | 10000 | 0.0681 | [0.0661, 0.0702] | [0.0660, 0.0702] | < 1e-15 | yes |
| V3 (N=200, own) | 0.7 | window-3 | 0.5 | imitation | 10000 | 0.0486 | [0.0476, 0.0495] | [0.0476, 0.0495] | < 1e-15 | yes |

### 8.3 Secondary metrics (descriptive, means with 95% intervals over 10,000 episodes)

| Variation | q | Network | v | Rule | Accuracy | Wrong cascade | Longest wrong run | Informative share | Last agent |
|---|---|---|---|---|---|---|---|---|---|
| V1 | 0.55 | complete | 1 | independent | 0.550 [0.549, 0.552] | 0.000 [0.000, 0.000] | 4.41 [4.38, 4.44] | 1.000 [1.000, 1.000] | 0.547 [0.538, 0.557] |
| V1 | 0.55 | complete | 1 | bayesian | 0.565 [0.555, 0.575] | 0.434 [0.424, 0.444] | 21.63 [21.15, 22.11] | 0.053 [0.052, 0.053] | 0.566 [0.556, 0.576] |
| V1 | 0.55 | complete | 1 | imitation | 0.565 [0.555, 0.575] | 0.434 [0.424, 0.444] | 21.63 [21.15, 22.11] | 0.053 [0.052, 0.053] | 0.566 [0.556, 0.576] |
| V1 | 0.55 | complete | 0.5 | independent | 0.550 [0.549, 0.551] | 0.000 [0.000, 0.000] | 4.39 [4.36, 4.42] | 1.000 [1.000, 1.000] | 0.554 [0.545, 0.564] |
| V1 | 0.55 | complete | 0.5 | bayesian | 0.564 [0.554, 0.573] | 0.434 [0.425, 0.444] | 21.09 [20.63, 21.54] | 0.107 [0.105, 0.108] | 0.566 [0.556, 0.575] |
| V1 | 0.55 | complete | 0.5 | imitation | 0.564 [0.554, 0.573] | 0.434 [0.425, 0.444] | 21.09 [20.63, 21.54] | 0.107 [0.105, 0.108] | 0.566 [0.556, 0.575] |
| V1 | 0.55 | window-2 | 1 | independent | 0.550 [0.549, 0.552] | 0.000 [0.000, 0.000] | 4.41 [4.38, 4.44] | 1.000 [1.000, 1.000] | 0.546 [0.536, 0.555] |
| V1 | 0.55 | window-2 | 1 | bayesian | 0.568 [0.558, 0.577] | 0.431 [0.422, 0.441] | 21.53 [21.05, 22.00] | 0.049 [0.048, 0.049] | 0.569 [0.559, 0.578] |
| V1 | 0.55 | window-2 | 1 | imitation | 0.570 [0.560, 0.579] | 0.429 [0.420, 0.439] | 21.40 [20.92, 21.87] | 0.050 [0.050, 0.050] | 0.571 [0.561, 0.580] |
| V1 | 0.55 | window-2 | 0.5 | independent | 0.550 [0.549, 0.551] | 0.000 [0.000, 0.000] | 4.41 [4.38, 4.44] | 1.000 [1.000, 1.000] | 0.546 [0.536, 0.556] |
| V1 | 0.55 | window-2 | 0.5 | bayesian | 0.555 [0.552, 0.558] | 0.887 [0.881, 0.894] | 10.04 [9.92, 10.15] | 0.657 [0.654, 0.660] | 0.552 [0.543, 0.562] |
| V1 | 0.55 | window-2 | 0.5 | imitation | 0.553 [0.551, 0.556] | 0.908 [0.902, 0.913] | 8.26 [8.19, 8.34] | 0.799 [0.798, 0.801] | 0.551 [0.542, 0.561] |
| V1 | 0.55 | window-3 | 1 | independent | 0.550 [0.548, 0.551] | 0.000 [0.000, 0.000] | 4.41 [4.38, 4.44] | 1.000 [1.000, 1.000] | 0.554 [0.544, 0.563] |
| V1 | 0.55 | window-3 | 1 | bayesian | 0.558 [0.548, 0.567] | 0.442 [0.432, 0.451] | 21.98 [21.50, 22.46] | 0.053 [0.053, 0.054] | 0.558 [0.549, 0.568] |
| V1 | 0.55 | window-3 | 1 | imitation | 0.558 [0.548, 0.567] | 0.442 [0.432, 0.452] | 21.94 [21.46, 22.42] | 0.058 [0.057, 0.059] | 0.558 [0.548, 0.568] |
| V1 | 0.55 | window-3 | 0.5 | independent | 0.549 [0.548, 0.551] | 0.000 [0.000, 0.000] | 4.39 [4.36, 4.42] | 1.000 [1.000, 1.000] | 0.547 [0.537, 0.556] |
| V1 | 0.55 | window-3 | 0.5 | bayesian | 0.564 [0.558, 0.569] | 0.807 [0.799, 0.815] | 14.48 [14.26, 14.70] | 0.392 [0.389, 0.395] | 0.562 [0.552, 0.572] |
| V1 | 0.55 | window-3 | 0.5 | imitation | 0.560 [0.556, 0.564] | 0.887 [0.881, 0.893] | 11.30 [11.17, 11.43] | 0.592 [0.590, 0.594] | 0.557 [0.548, 0.567] |
| V1 | 0.7 | complete | 1 | independent | 0.700 [0.699, 0.701] | 0.000 [0.000, 0.000] | 2.93 [2.91, 2.95] | 1.000 [1.000, 1.000] | 0.702 [0.693, 0.711] |
| V1 | 0.7 | complete | 1 | bayesian | 0.749 [0.741, 0.758] | 0.248 [0.239, 0.256] | 12.46 [12.04, 12.88] | 0.051 [0.050, 0.051] | 0.752 [0.744, 0.761] |
| V1 | 0.7 | complete | 1 | imitation | 0.749 [0.741, 0.758] | 0.248 [0.239, 0.256] | 12.46 [12.04, 12.88] | 0.051 [0.050, 0.051] | 0.752 [0.744, 0.761] |
| V1 | 0.7 | complete | 0.5 | independent | 0.701 [0.700, 0.702] | 0.000 [0.000, 0.000] | 2.93 [2.91, 2.95] | 1.000 [1.000, 1.000] | 0.708 [0.699, 0.717] |
| V1 | 0.7 | complete | 0.5 | bayesian | 0.749 [0.741, 0.757] | 0.245 [0.237, 0.254] | 12.12 [11.73, 12.52] | 0.102 [0.100, 0.103] | 0.754 [0.746, 0.763] |
| V1 | 0.7 | complete | 0.5 | imitation | 0.749 [0.741, 0.757] | 0.245 [0.237, 0.254] | 12.12 [11.73, 12.52] | 0.102 [0.100, 0.103] | 0.754 [0.746, 0.763] |
| V1 | 0.7 | window-2 | 1 | independent | 0.700 [0.699, 0.701] | 0.000 [0.000, 0.000] | 2.96 [2.93, 2.98] | 1.000 [1.000, 1.000] | 0.693 [0.684, 0.702] |
| V1 | 0.7 | window-2 | 1 | bayesian | 0.734 [0.726, 0.743] | 0.264 [0.255, 0.273] | 13.24 [12.81, 13.67] | 0.047 [0.047, 0.047] | 0.736 [0.727, 0.745] |
| V1 | 0.7 | window-2 | 1 | imitation | 0.741 [0.733, 0.750] | 0.256 [0.248, 0.265] | 12.87 [12.45, 13.29] | 0.048 [0.048, 0.049] | 0.744 [0.735, 0.752] |
| V1 | 0.7 | window-2 | 0.5 | independent | 0.700 [0.699, 0.701] | 0.000 [0.000, 0.000] | 2.95 [2.93, 2.97] | 1.000 [1.000, 1.000] | 0.690 [0.681, 0.699] |
| V1 | 0.7 | window-2 | 0.5 | bayesian | 0.718 [0.715, 0.721] | 0.697 [0.687, 0.706] | 6.80 [6.71, 6.90] | 0.653 [0.650, 0.656] | 0.720 [0.711, 0.728] |
| V1 | 0.7 | window-2 | 0.5 | imitation | 0.715 [0.712, 0.717] | 0.726 [0.718, 0.735] | 5.70 [5.64, 5.76] | 0.793 [0.792, 0.795] | 0.714 [0.705, 0.722] |
| V1 | 0.7 | window-3 | 1 | independent | 0.701 [0.699, 0.702] | 0.000 [0.000, 0.000] | 2.94 [2.92, 2.96] | 1.000 [1.000, 1.000] | 0.699 [0.690, 0.708] |
| V1 | 0.7 | window-3 | 1 | bayesian | 0.748 [0.739, 0.756] | 0.250 [0.241, 0.258] | 12.55 [12.13, 12.97] | 0.050 [0.050, 0.051] | 0.750 [0.742, 0.759] |
| V1 | 0.7 | window-3 | 1 | imitation | 0.749 [0.740, 0.757] | 0.248 [0.240, 0.257] | 12.46 [12.04, 12.87] | 0.054 [0.053, 0.055] | 0.752 [0.743, 0.760] |
| V1 | 0.7 | window-3 | 0.5 | independent | 0.701 [0.700, 0.702] | 0.000 [0.000, 0.000] | 2.93 [2.91, 2.95] | 1.000 [1.000, 1.000] | 0.706 [0.697, 0.715] |
| V1 | 0.7 | window-3 | 0.5 | bayesian | 0.729 [0.725, 0.734] | 0.598 [0.588, 0.608] | 9.46 [9.26, 9.65] | 0.384 [0.381, 0.387] | 0.727 [0.719, 0.736] |
| V1 | 0.7 | window-3 | 0.5 | imitation | 0.729 [0.725, 0.732] | 0.684 [0.675, 0.693] | 7.40 [7.29, 7.51] | 0.580 [0.578, 0.582] | 0.728 [0.719, 0.737] |
| V2 | 0.55 | complete | 1 | independent | 0.551 [0.548, 0.554] | 0.000 [0.000, 0.000] | 2.47 [2.45, 2.50] | 1.000 [1.000, 1.000] | 0.547 [0.537, 0.557] |
| V2 | 0.55 | complete | 1 | bayesian | 0.581 [0.573, 0.589] | 0.374 [0.365, 0.383] | 3.71 [3.63, 3.79] | 0.384 [0.379, 0.389] | 0.597 [0.588, 0.607] |
| V2 | 0.55 | complete | 1 | imitation | 0.581 [0.573, 0.589] | 0.374 [0.365, 0.383] | 3.71 [3.63, 3.79] | 0.384 [0.379, 0.389] | 0.597 [0.588, 0.607] |
| V2 | 0.55 | complete | 0.5 | independent | 0.552 [0.549, 0.555] | 0.000 [0.000, 0.000] | 2.48 [2.46, 2.51] | 1.000 [1.000, 1.000] | 0.558 [0.548, 0.568] |
| V2 | 0.55 | complete | 0.5 | bayesian | 0.571 [0.565, 0.578] | 0.280 [0.271, 0.289] | 3.20 [3.14, 3.26] | 0.631 [0.625, 0.637] | 0.591 [0.581, 0.601] |
| V2 | 0.55 | complete | 0.5 | imitation | 0.571 [0.565, 0.578] | 0.280 [0.271, 0.289] | 3.20 [3.14, 3.26] | 0.631 [0.625, 0.637] | 0.591 [0.581, 0.601] |
| V2 | 0.55 | window-2 | 1 | independent | 0.550 [0.547, 0.553] | 0.000 [0.000, 0.000] | 2.48 [2.46, 2.50] | 1.000 [1.000, 1.000] | 0.548 [0.539, 0.558] |
| V2 | 0.55 | window-2 | 1 | bayesian | 0.575 [0.566, 0.584] | 0.415 [0.405, 0.424] | 4.02 [3.94, 4.11] | 0.299 [0.297, 0.302] | 0.584 [0.574, 0.594] |
| V2 | 0.55 | window-2 | 1 | imitation | 0.575 [0.566, 0.584] | 0.415 [0.405, 0.424] | 4.02 [3.94, 4.11] | 0.299 [0.297, 0.302] | 0.584 [0.574, 0.594] |
| V2 | 0.55 | window-2 | 0.5 | independent | 0.553 [0.550, 0.556] | 0.000 [0.000, 0.000] | 2.45 [2.43, 2.48] | 1.000 [1.000, 1.000] | 0.550 [0.541, 0.560] |
| V2 | 0.55 | window-2 | 0.5 | bayesian | 0.561 [0.557, 0.566] | 0.289 [0.280, 0.298] | 2.91 [2.87, 2.96] | 0.799 [0.795, 0.803] | 0.557 [0.548, 0.567] |
| V2 | 0.55 | window-2 | 0.5 | imitation | 0.560 [0.556, 0.564] | 0.270 [0.261, 0.279] | 2.76 [2.72, 2.79] | 0.871 [0.868, 0.873] | 0.556 [0.546, 0.566] |
| V2 | 0.55 | window-3 | 1 | independent | 0.551 [0.548, 0.554] | 0.000 [0.000, 0.000] | 2.48 [2.45, 2.50] | 1.000 [1.000, 1.000] | 0.556 [0.547, 0.566] |
| V2 | 0.55 | window-3 | 1 | bayesian | 0.583 [0.575, 0.592] | 0.371 [0.362, 0.381] | 3.69 [3.61, 3.77] | 0.388 [0.383, 0.393] | 0.602 [0.592, 0.611] |
| V2 | 0.55 | window-3 | 1 | imitation | 0.582 [0.574, 0.590] | 0.340 [0.331, 0.350] | 3.54 [3.46, 3.62] | 0.445 [0.439, 0.450] | 0.603 [0.593, 0.612] |
| V2 | 0.55 | window-3 | 0.5 | independent | 0.552 [0.549, 0.555] | 0.000 [0.000, 0.000] | 2.47 [2.44, 2.49] | 1.000 [1.000, 1.000] | 0.550 [0.540, 0.559] |
| V2 | 0.55 | window-3 | 0.5 | bayesian | 0.565 [0.560, 0.571] | 0.339 [0.330, 0.348] | 3.18 [3.13, 3.24] | 0.675 [0.670, 0.681] | 0.574 [0.564, 0.583] |
| V2 | 0.55 | window-3 | 0.5 | imitation | 0.563 [0.557, 0.568] | 0.320 [0.310, 0.329] | 3.05 [3.00, 3.10] | 0.752 [0.748, 0.757] | 0.568 [0.558, 0.577] |
| V2 | 0.7 | complete | 1 | independent | 0.701 [0.698, 0.703] | 0.000 [0.000, 0.000] | 1.68 [1.66, 1.69] | 1.000 [1.000, 1.000] | 0.703 [0.694, 0.711] |
| V2 | 0.7 | complete | 1 | bayesian | 0.796 [0.790, 0.803] | 0.148 [0.141, 0.155] | 1.76 [1.70, 1.82] | 0.343 [0.339, 0.347] | 0.843 [0.836, 0.850] |
| V2 | 0.7 | complete | 1 | imitation | 0.796 [0.790, 0.803] | 0.148 [0.141, 0.155] | 1.76 [1.70, 1.82] | 0.343 [0.339, 0.347] | 0.843 [0.836, 0.850] |
| V2 | 0.7 | complete | 0.5 | independent | 0.697 [0.694, 0.700] | 0.000 [0.000, 0.000] | 1.70 [1.68, 1.71] | 1.000 [1.000, 1.000] | 0.700 [0.691, 0.709] |
| V2 | 0.7 | complete | 0.5 | bayesian | 0.758 [0.752, 0.763] | 0.127 [0.120, 0.133] | 1.78 [1.74, 1.83] | 0.585 [0.579, 0.590] | 0.807 [0.799, 0.815] |
| V2 | 0.7 | complete | 0.5 | imitation | 0.758 [0.752, 0.763] | 0.127 [0.120, 0.133] | 1.78 [1.74, 1.83] | 0.585 [0.579, 0.590] | 0.807 [0.799, 0.815] |
| V2 | 0.7 | window-2 | 1 | independent | 0.702 [0.699, 0.705] | 0.000 [0.000, 0.000] | 1.68 [1.66, 1.70] | 1.000 [1.000, 1.000] | 0.693 [0.684, 0.702] |
| V2 | 0.7 | window-2 | 1 | bayesian | 0.785 [0.778, 0.792] | 0.187 [0.179, 0.195] | 2.02 [1.95, 2.08] | 0.279 [0.277, 0.281] | 0.813 [0.805, 0.820] |
| V2 | 0.7 | window-2 | 1 | imitation | 0.785 [0.778, 0.792] | 0.187 [0.179, 0.195] | 2.02 [1.95, 2.08] | 0.279 [0.277, 0.281] | 0.813 [0.805, 0.820] |
| V2 | 0.7 | window-2 | 0.5 | independent | 0.699 [0.696, 0.701] | 0.000 [0.000, 0.000] | 1.69 [1.67, 1.71] | 1.000 [1.000, 1.000] | 0.707 [0.698, 0.716] |
| V2 | 0.7 | window-2 | 0.5 | bayesian | 0.722 [0.718, 0.726] | 0.147 [0.140, 0.154] | 1.86 [1.83, 1.90] | 0.785 [0.780, 0.789] | 0.737 [0.729, 0.746] |
| V2 | 0.7 | window-2 | 0.5 | imitation | 0.716 [0.712, 0.719] | 0.138 [0.131, 0.145] | 1.81 [1.79, 1.84] | 0.857 [0.854, 0.860] | 0.725 [0.716, 0.733] |
| V2 | 0.7 | window-3 | 1 | independent | 0.698 [0.696, 0.701] | 0.000 [0.000, 0.000] | 1.69 [1.67, 1.71] | 1.000 [1.000, 1.000] | 0.701 [0.692, 0.710] |
| V2 | 0.7 | window-3 | 1 | bayesian | 0.791 [0.784, 0.797] | 0.155 [0.148, 0.162] | 1.83 [1.77, 1.89] | 0.340 [0.336, 0.344] | 0.836 [0.828, 0.843] |
| V2 | 0.7 | window-3 | 1 | imitation | 0.788 [0.781, 0.794] | 0.141 [0.134, 0.148] | 1.77 [1.71, 1.83] | 0.382 [0.377, 0.387] | 0.836 [0.829, 0.843] |
| V2 | 0.7 | window-3 | 0.5 | independent | 0.700 [0.697, 0.703] | 0.000 [0.000, 0.000] | 1.69 [1.67, 1.71] | 1.000 [1.000, 1.000] | 0.707 [0.698, 0.716] |
| V2 | 0.7 | window-3 | 0.5 | bayesian | 0.739 [0.734, 0.744] | 0.161 [0.153, 0.168] | 1.87 [1.83, 1.91] | 0.662 [0.657, 0.667] | 0.766 [0.758, 0.775] |
| V2 | 0.7 | window-3 | 0.5 | imitation | 0.733 [0.729, 0.737] | 0.147 [0.140, 0.154] | 1.83 [1.79, 1.86] | 0.737 [0.733, 0.741] | 0.752 [0.744, 0.760] |
| V3 | 0.55 | complete | 1 | independent | 0.550 [0.549, 0.550] | 0.000 [0.000, 0.000] | 6.11 [6.08, 6.14] | 1.000 [1.000, 1.000] | 0.557 [0.547, 0.566] |
| V3 | 0.55 | complete | 1 | bayesian | 0.600 [0.591, 0.610] | 0.399 [0.389, 0.408] | 79.46 [77.56, 81.35] | 0.020 [0.020, 0.020] | 0.601 [0.592, 0.611] |
| V3 | 0.55 | complete | 1 | imitation | 0.600 [0.591, 0.610] | 0.399 [0.389, 0.408] | 79.46 [77.56, 81.35] | 0.020 [0.020, 0.020] | 0.601 [0.592, 0.611] |
| V3 | 0.55 | complete | 0.5 | independent | 0.550 [0.549, 0.551] | 0.000 [0.000, 0.000] | 6.12 [6.09, 6.15] | 1.000 [1.000, 1.000] | 0.542 [0.532, 0.551] |
| V3 | 0.55 | complete | 0.5 | bayesian | 0.593 [0.584, 0.603] | 0.405 [0.395, 0.414] | 79.53 [77.67, 81.39] | 0.040 [0.039, 0.040] | 0.595 [0.586, 0.605] |
| V3 | 0.55 | complete | 0.5 | imitation | 0.593 [0.584, 0.603] | 0.405 [0.395, 0.414] | 79.53 [77.67, 81.39] | 0.040 [0.039, 0.040] | 0.595 [0.586, 0.605] |
| V3 | 0.55 | window-2 | 1 | independent | 0.550 [0.549, 0.551] | 0.000 [0.000, 0.000] | 6.13 [6.09, 6.16] | 1.000 [1.000, 1.000] | 0.550 [0.540, 0.559] |
| V3 | 0.55 | window-2 | 1 | bayesian | 0.586 [0.576, 0.595] | 0.414 [0.404, 0.424] | 82.67 [80.76, 84.59] | 0.015 [0.015, 0.015] | 0.586 [0.576, 0.596] |
| V3 | 0.55 | window-2 | 1 | imitation | 0.586 [0.576, 0.595] | 0.414 [0.404, 0.424] | 82.67 [80.76, 84.59] | 0.015 [0.015, 0.015] | 0.586 [0.576, 0.596] |
| V3 | 0.55 | window-2 | 0.5 | independent | 0.550 [0.549, 0.550] | 0.000 [0.000, 0.000] | 6.12 [6.08, 6.15] | 1.000 [1.000, 1.000] | 0.555 [0.546, 0.565] |
| V3 | 0.55 | window-2 | 0.5 | bayesian | 0.560 [0.559, 0.562] | 0.999 [0.999, 1.000] | 14.90 [14.78, 15.02] | 0.674 [0.672, 0.675] | 0.562 [0.553, 0.572] |
| V3 | 0.55 | window-2 | 0.5 | imitation | 0.557 [0.556, 0.558] | 1.000 [0.999, 1.000] | 8.82 [8.76, 8.87] | 0.835 [0.834, 0.836] | 0.560 [0.551, 0.570] |
| V3 | 0.55 | window-3 | 1 | independent | 0.550 [0.549, 0.551] | 0.000 [0.000, 0.000] | 6.13 [6.09, 6.16] | 1.000 [1.000, 1.000] | 0.553 [0.544, 0.563] |
| V3 | 0.55 | window-3 | 1 | bayesian | 0.596 [0.587, 0.606] | 0.403 [0.393, 0.413] | 80.23 [78.33, 82.14] | 0.020 [0.020, 0.020] | 0.597 [0.587, 0.607] |
| V3 | 0.55 | window-3 | 1 | imitation | 0.605 [0.595, 0.614] | 0.394 [0.384, 0.403] | 78.20 [76.32, 80.09] | 0.025 [0.024, 0.025] | 0.606 [0.597, 0.616] |
| V3 | 0.55 | window-3 | 0.5 | independent | 0.550 [0.549, 0.551] | 0.000 [0.000, 0.000] | 6.15 [6.11, 6.18] | 1.000 [1.000, 1.000] | 0.551 [0.541, 0.560] |
| V3 | 0.55 | window-3 | 0.5 | bayesian | 0.570 [0.567, 0.573] | 0.995 [0.993, 0.996] | 28.96 [28.67, 29.26] | 0.388 [0.387, 0.390] | 0.570 [0.560, 0.580] |
| V3 | 0.55 | window-3 | 0.5 | imitation | 0.565 [0.564, 0.567] | 1.000 [0.999, 1.000] | 14.23 [14.13, 14.34] | 0.646 [0.645, 0.647] | 0.559 [0.549, 0.569] |
| V3 | 0.7 | complete | 1 | independent | 0.700 [0.699, 0.701] | 0.000 [0.000, 0.000] | 4.09 [4.07, 4.11] | 1.000 [1.000, 1.000] | 0.702 [0.693, 0.711] |
| V3 | 0.7 | complete | 1 | bayesian | 0.845 [0.838, 0.852] | 0.152 [0.145, 0.159] | 30.67 [29.27, 32.07] | 0.017 [0.017, 0.018] | 0.848 [0.841, 0.855] |
| V3 | 0.7 | complete | 1 | imitation | 0.845 [0.838, 0.852] | 0.152 [0.145, 0.159] | 30.67 [29.27, 32.07] | 0.017 [0.017, 0.018] | 0.848 [0.841, 0.855] |
| V3 | 0.7 | complete | 0.5 | independent | 0.700 [0.699, 0.701] | 0.000 [0.000, 0.000] | 4.08 [4.06, 4.10] | 1.000 [1.000, 1.000] | 0.703 [0.694, 0.712] |
| V3 | 0.7 | complete | 0.5 | bayesian | 0.839 [0.832, 0.846] | 0.156 [0.149, 0.163] | 31.26 [29.88, 32.64] | 0.035 [0.034, 0.035] | 0.844 [0.837, 0.851] |
| V3 | 0.7 | complete | 0.5 | imitation | 0.839 [0.832, 0.846] | 0.156 [0.149, 0.163] | 31.26 [29.88, 32.64] | 0.035 [0.034, 0.035] | 0.844 [0.837, 0.851] |
| V3 | 0.7 | window-2 | 1 | independent | 0.701 [0.700, 0.701] | 0.000 [0.000, 0.000] | 4.09 [4.07, 4.11] | 1.000 [1.000, 1.000] | 0.696 [0.686, 0.705] |
| V3 | 0.7 | window-2 | 1 | bayesian | 0.804 [0.796, 0.812] | 0.195 [0.187, 0.202] | 39.08 [37.53, 40.62] | 0.014 [0.014, 0.014] | 0.805 [0.798, 0.813] |
| V3 | 0.7 | window-2 | 1 | imitation | 0.804 [0.796, 0.812] | 0.195 [0.187, 0.202] | 39.08 [37.53, 40.62] | 0.014 [0.014, 0.014] | 0.805 [0.798, 0.813] |
| V3 | 0.7 | window-2 | 0.5 | independent | 0.700 [0.699, 0.701] | 0.000 [0.000, 0.000] | 4.10 [4.08, 4.12] | 1.000 [1.000, 1.000] | 0.702 [0.693, 0.710] |
| V3 | 0.7 | window-2 | 0.5 | bayesian | 0.735 [0.733, 0.736] | 0.961 [0.957, 0.964] | 10.39 [10.28, 10.51] | 0.664 [0.662, 0.665] | 0.735 [0.726, 0.743] |
| V3 | 0.7 | window-2 | 0.5 | imitation | 0.722 [0.721, 0.723] | 0.965 [0.962, 0.969] | 6.14 [6.10, 6.18] | 0.822 [0.821, 0.822] | 0.718 [0.709, 0.727] |
| V3 | 0.7 | window-3 | 1 | independent | 0.700 [0.700, 0.701] | 0.000 [0.000, 0.000] | 4.09 [4.07, 4.11] | 1.000 [1.000, 1.000] | 0.699 [0.690, 0.708] |
| V3 | 0.7 | window-3 | 1 | bayesian | 0.844 [0.837, 0.851] | 0.154 [0.147, 0.161] | 30.94 [29.54, 32.35] | 0.017 [0.017, 0.017] | 0.846 [0.839, 0.853] |
| V3 | 0.7 | window-3 | 1 | imitation | 0.858 [0.851, 0.864] | 0.139 [0.132, 0.146] | 28.08 [26.74, 29.43] | 0.020 [0.020, 0.021] | 0.861 [0.854, 0.868] |
| V3 | 0.7 | window-3 | 0.5 | independent | 0.700 [0.699, 0.701] | 0.000 [0.000, 0.000] | 4.09 [4.07, 4.11] | 1.000 [1.000, 1.000] | 0.701 [0.692, 0.710] |
| V3 | 0.7 | window-3 | 0.5 | bayesian | 0.768 [0.766, 0.770] | 0.906 [0.900, 0.912] | 18.52 [18.24, 18.79] | 0.375 [0.373, 0.377] | 0.772 [0.764, 0.780] |
| V3 | 0.7 | window-3 | 0.5 | imitation | 0.748 [0.747, 0.750] | 0.967 [0.963, 0.970] | 9.57 [9.48, 9.66] | 0.622 [0.621, 0.623] | 0.752 [0.743, 0.760] |

### 8.4 Runtime

19.47 s wall-clock (simulation 12.88 s, 0.138 ms per 1,000 agent decisions; analysis 5.04 s); peak resident memory 280,002,560 bytes.

## 9. Interpretation

- **Measured.** No sign of an EXP-002 contrast reverses under any variation. Changing the horizon (V2, V3) changes magnitudes but leaves every contrast Holm-significant; the longer horizon enlarges the gain at $q = 0.7$ with full visibility (for example Bayesian, complete: 0.1452 at $N = 200$ against 0.1344 at $N = 50$ and 0.0957 at $N = 10$).
- **Tie rule.** Coin-flip ties shrink every gain, by more than half in 16 of the 24 contrasts (Bayesian, $q = 0.7$, complete, $v = 1$: 0.0494 against 0.1344). This is consistent with the mechanism of the protocol: a tied agent's action no longer reveals its signal, so cascades start earlier on less information. At $q = 0.55$, window-3, $v = 1$ the remaining gain is under one accuracy point and its interval includes zero.
- **Verdict under the frozen rule.** H1 of EXP-003 holds for two contrasts (Bayesian and imitation, $q = 0.55$, window-3, $v = 1$): the EXP-002 conclusion for these two contrasts is convention-dependent (it holds under own-signal ties, and is not established under coin ties). For the remaining 22 EXP-002 contrasts in the EXP-003 grid, H0 (robustness) is retained under all three variations. The 24 EXP-002 contrasts at $q \in \{0.60, 0.80\}$ were not part of the EXP-003 grid and their robustness is untested.
- **Not equivalence.** "Lost significance" does not show that the coin-tie effect is zero; the 95% intervals ([-0.0013, 0.0176] and [-0.0015, 0.0174]) include effects of up to about 1.8 points.

## 10. Threats to validity

- **Internal:** the coin-tie engine path is verified by the oracle only for $N \leq 9$; C7 is a diagnostic, not a check.
- **Construct:** the robustness rule tracks sign and significance only, not magnitude; large magnitude changes (for example under coin ties) are reported but not judged by the rule.
- **Statistical:** each variation has its own Holm family of 24; no correction across variations or across experiments was planned. The 72 robustness comparisons are a deterministic classification of frozen estimates, not new tests.
- **External:** as in EXP-002; synthetic homogeneous agents only.

## 11. Conclusion and next experiment

The main EXP-002 finding (social information raises mean accuracy against the independent baseline) keeps its sign under every variation tested, and keeps Holm significance in 70 of 72 comparisons. Its size depends strongly on the tie convention, and at low signal quality in the window-3 network with full visibility the gain is not established under coin-flip ties. A follow-up would need a new preregistered protocol: coin ties across the full EXP-002 grid ($q = 0.60, 0.80$ included), and an equivalence or minimum-effect test if the size of the coin-tie gain matters.

## 12. Reproduction appendix

- **Environment:** `../.tools/py/bin/uv sync --frozen --all-groups --all-extras`; test with `.venv/bin/python -m pytest`.
- **Data manifest:** `data/manifest.json` (synthetic only).
- **Run:** `PYTHONPATH=src .venv/bin/python -m herd.cli run --config experiments/EXP-003.json` (needs a fresh output folder).
- **Report, figures and tables:** `herd.cli report --run results/EXP-003/EXP-003-R001`, `herd.robustness` and `herd.tables` commands as in Section 7.
- **Raw results:** `results/EXP-003/EXP-003-R001/result.json` (SHA-256 `f74a37667153b0dc12ab8d3c0df6af74476cde9a9994fd4ea3d090760b5c7367`), `results/raw/EXP-003-R001/episodes.npz` (SHA-256 `a72e02c67175a82fde47e59189b72c878072010f8248fce80bdbcd7ef728d1ac`), `run_manifest.json`; every file hash in `results/EXP-003/SHA256SUMS`.
- **Expected tolerance:** deterministic for a given numpy version; timing fields differ between reruns.
- **References:** `research/literature_review.md`.
