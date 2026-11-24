<!-- SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0 -->
# EXP-002 protocol: social learning versus independent decisions across signal quality, network and visibility

- **Status:** FROZEN v1.0, 2026-11-24 (owner-approved, G-FREEZE). Draft v0.1 plus the amendments of section 14. Not yet run.
- **Type:** confirmatory once frozen.
- **Depends on:** EXP-001 (smoke and verification) and the M2 verification tests passing.
- **Protocol hash:** the SHA-256 of this file is recorded in `research/experiment_registry.csv` and `research/freeze.json`.
- **Study-level protocol:** `research/protocol.md` (model, definitions). This file is the experiment-specific operationalisation.

## 1. Precise question

For which combinations of signal quality $q$, observation network $G$ and visibility $v$ does using social information (Bayesian or naive vote counting) raise or lower mean decision accuracy relative to ignoring it?

## 2. Mechanism and rationale

Observing predecessors adds information, but once public evidence outweighs any single private signal, agents stop revealing their signals and an informational cascade starts (BHW1992, Banerjee1992; verified abstracts). A cascade can lock in the wrong action. Bayesian agents never lose accuracy individually from extra information, but the group can stop learning. Naive agents who count every observed action as independent evidence over-weight early movers (ER2010, verified abstract), which can make social information harmful. Restricted observation (ADLO2011, CK2004) changes how much early actions propagate.

## 3. Competing explanations

- Accuracy gains may come from information quantity rather than structure: the visibility factor varies quantity within each network.
- Differences may be artefacts of the tie convention or horizon: tested in EXP-003.
- Differences may be implementation errors: verification tests, the analytic anchor and the complete-network equivalence check of the study protocol must pass first.

## 4. Hypotheses

- **H0:** $\Delta_r(c) = 0$ for all $r \in$ {Bayesian, imitation} and all 24 cells $c = (q, G, v)$.
- **H1 (non-directional):** $\Delta_r(c) \neq 0$ for at least one $(r, c)$.
- **Directional expectations:** Bayesian $\Delta \geq 0$ everywhere; imitation $\Delta$ equals Bayesian $\Delta$ under `complete`; imitation $\Delta < 0$ in at least one `window-k` cell at low $q$ ($k \in \{2, 3\}$).
- **Contradicting results:** H1 is not supported if no contrast is Holm-significant (Holm-adjusted p < 0.05 within the family of non-degenerate contrasts) and no degenerate contrast has a non-zero exact difference. A Bayesian $\Delta$ significantly below zero, or any divergence between imitation and Bayesian actions under `complete`, contradicts the model and stops interpretation pending an implementation check.

## 5. Estimand

$\Delta_r(c) = E_e[\mathrm{Acc}_r(e) - \mathrm{Acc}_{\mathrm{ind}}(e)]$, the expected paired difference in episode accuracy (proportion of agents correct) over the distribution of episodes in cell $c$.

## 6. Unit, scope and variables

- **Experimental unit:** episode. **Simulation scope:** $N = 50$ agents, prior $1/2$.
- **Independent variables:** rule (3 levels), $q \in \{0.55, 0.60, 0.70, 0.80\}$, $G \in$ {complete, window-2, window-3}, $v \in \{1.0, 0.5\}$.
- **Dependent variables:** primary, episode accuracy; secondary, cascade probability, wrong-cascade probability, error persistence (longest wrong run, agents), informative-action share, action entropy (bits), last-agent accuracy. Formulas in `research/protocol.md` section 4.
- **Treatment:** Bayesian or imitation rule. **Control and baseline:** independent rule on the same episode.

## 7. Sampling, seeds and sample size

- Master seeds 0 to 9; each seed yields 1,000 episodes per cell; RNG streams derived deterministically from (seed, cell) with numpy `SeedSequence`; all rules share the episode draws (common random numbers).
- 10,000 paired episodes per $(r, c)$. Rationale: 95% half-width of about 0.01 accuracy points at a paired SD of 0.5 (study protocol section 5).

## 8. Fixed compute budget

One local process on the audited machine; target under one hour wall-clock; actual runtime and peak memory recorded in `run_manifest.json`. If the measured EXP-001 throughput implies more than four hours, the owner is asked before the freeze whether to reduce episodes to 5 seeds $\times$ 1,000 (half-width about 0.014).

## 9. Analysis plan

- For each $(r, c)$: mean paired difference, normal-approximation 95% interval, percentile bootstrap check (2,000 resamples over episodes, fixed seed), two-sided paired t-test p-value, Holm adjustment over the non-degenerate contrasts among the 48 (familywise error rate 0.05).
- A structurally degenerate contrast (zero paired variance) has no t statistic; it is excluded from the Holm family and reported as an exact comparison, and the family size is reported (amendment A-3).
- The 95% intervals are unadjusted and describe magnitude; the decision uses Holm-adjusted p-values only. No simultaneous interval is claimed (amendment A-4).
- Per-seed means and the full distribution of episode accuracy for every arm.
- Secondary metrics: means with 95% intervals per arm; no multiplicity adjustment; described as secondary.

## 10. Exclusion and stopping rules

As in `research/protocol.md` section 6: no outcome-based exclusions; failed runs recorded, rerun once with the same seed after a documented fix, otherwise reported missing; fixed sample, no interim analysis.

## 11. Anticipated failure modes

Numerical underflow in likelihoods (use log-likelihood ratios); window recursion indexing errors at the start of the sequence and around hidden actions; tie detection with floating point (compare exact rational log-ratios or use integer signal counts where possible); RNG stream reuse across cells.

## 12. Sensitivity

EXP-003 (tie rule, horizon). Its results are reported alongside EXP-002 and can qualify its interpretation.

## 13. Reproduction commands (planned; the CLI does not exist yet)

```
uv sync --frozen
uv run python -m herd.cli run --config experiments/EXP-002.json
uv run python -m herd.cli report --exp EXP-002
```

## 14. Amendments before freeze (owner-approved 2026-11-24)

Applied to draft v0.1 before the freeze; details and rationale in `research/protocol.md` section 11.

- **A-1.** `window-1` replaced by `window-2` (sections 4 and 6; `experiments/EXP-002.json`).
- **A-2.** The complete-network equivalence is predicted for $q > 1/2$ only; every EXP-002 cell has $q \geq 0.55$, so the check applies to all `complete` cells.
- **A-3.** Structurally degenerate (zero-variance) contrasts are excluded from the Holm family and reported as exact comparisons (section 9).
- **A-4.** Decisions use Holm-adjusted p-values; reported intervals are unadjusted 95% intervals; no simultaneous interval is claimed (sections 4 and 9).
- **A-5.** Planned sample kept: seeds 0 to 9, 1,000 episodes per seed and cell (section 7, unchanged).

The reproduction commands of section 13 are kept as drafted (not part of the approved amendments); the working commands, with the `PYTHONPATH=src` prefix and `report --run`, are in `CONTRIBUTING.md` and `research/freeze.json`.
