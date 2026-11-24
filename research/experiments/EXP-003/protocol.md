<!-- SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0 -->
# EXP-003 protocol: sensitivity of the EXP-002 contrasts to the tie rule and the horizon

- **Status:** FROZEN v1.0, 2026-11-24 (owner-approved, G-FREEZE). Draft v0.1 plus the amendments of section 8. Not yet run.
- **Type:** confirmatory sensitivity analysis once frozen.
- **Depends on:** EXP-002 (same engine revision and analysis code).
- **Protocol hash:** recorded in `research/experiment_registry.csv` and `research/freeze.json`.

## 1. Precise question

Do the signs and Holm significance of the EXP-002 contrasts $\Delta_r(c)$ survive (a) coin-flip tie-breaking instead of own-signal tie-breaking and (b) horizons $N = 10$ and $N = 200$ instead of $N = 50$?

## 2. Mechanism and rationale

Under coin-flip ties, which is the convention of BHW1992, an agent with a balanced posterior acts at random, so cascades can start one agent earlier and early actions carry less information. Averaging accuracy over $N$ agents weights pre-cascade agents (whose accuracy is close to $q$) by about $1/N$; a short horizon can hide the cost of a wrong cascade and a long one can amplify it. Either convention could, in principle, reverse a conclusion drawn from EXP-002.

## 3. Hypotheses

- **H0 (robustness):** for every $(r, c)$ that is Holm-significant in EXP-002, the sign of $\Delta_r(c)$ is the same under each variation.
- **H1:** at least one sign reverses or loses significance under a variation.
- **Interpretation rule (fixed in advance):** if H1 holds for any contrast, the EXP-002 conclusion for that contrast is reported as convention-dependent.

## 4. Design

- Cells: $q \in \{0.55, 0.70\}$ $\times$ $G \in$ {complete, window-2, window-3} $\times$ $v \in \{1.0, 0.5\}$ = 12 cells, 3 rules.
- Variations: V1 tie = coin, $N = 50$; V2 tie = own signal, $N = 10$; V3 tie = own signal, $N = 200$.
- Seeds 0 to 9, 1,000 episodes per cell, common random numbers; the coin flips use a separate stream so the episode draws match EXP-002.
- Estimand, metrics, uncertainty method (normal-approximation interval, bootstrap check, Holm over the non-degenerate contrasts among the 24 of each variation, degenerate contrasts reported as exact comparisons) and exclusion and stopping rules as in EXP-002.

## 5. Sample size and budget

10,000 paired episodes per contrast and variation, as in EXP-002. The $N = 200$ variation costs about four times the agents per episode; total volume about 1.5 times EXP-002 (planning estimate).

## 6. Anticipated failure modes

The coin-flip Bayesian decision tables become stochastic; the `window-k` recursion must then carry action probabilities rather than deterministic tables. Unit tests for the stochastic case are required before running.

## 7. Reproduction commands (planned)

```
uv run python -m herd.cli run --config experiments/EXP-003.json
uv run python -m herd.cli report --exp EXP-003
```

## 8. Amendments before freeze (owner-approved 2026-11-24)

Applied to draft v0.1 before the freeze; details and rationale in `research/protocol.md` section 11.

- **A-1.** `window-1` replaced by `window-2` (section 4; `experiments/EXP-003.json`).
- **A-2.** The complete-network equivalence is predicted for $q > 1/2$ and own-signal ties only; under coin ties (V1) the divergence is recorded as a diagnostic without prediction.
- **A-3.** Within each variation, structurally degenerate (zero-variance) contrasts are excluded from the Holm family and reported as exact comparisons (section 4).
- **A-4.** Holm-significance means a Holm-adjusted p-value below 0.05 within the variation's family; intervals are unadjusted 95% intervals.
- **A-5.** Planned sample kept: seeds 0 to 9, 1,000 episodes per seed and cell.
