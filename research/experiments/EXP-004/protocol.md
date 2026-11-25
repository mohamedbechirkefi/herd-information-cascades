<!-- SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0 -->
# EXP-004 protocol: post-hoc sensitivity and distributional checks (EXPLORATORY, M4)

**EXPLORATORY AND POST HOC. Written on 2026-11-25, after the confirmatory results of EXP-002 and EXP-003 were seen. Nothing in this experiment is preregistered, nothing here changes or replaces a frozen verdict, and none of its numbers is evidence for H1 of EXP-002 or EXP-003.**

- **Status:** v1.0, 2026-11-25, exploratory. Not frozen and not submitted for freezing.
- **Depends on:** EXP-002-R001 and EXP-003-R001 (committed results), code revision `d36b08c`.
- **Authority:** the coordinator's M4 brief (`../_shared/M4-brief.md`, task 1): new computation is allowed when cheap and clearly labelled exploratory, kept in `results/exploratory/`, at most 2 workers.
- **Protocol hash:** recorded in `research/experiment_registry.csv` (exploratory; not a confirmatory protocol).

## 1. Precise questions

- **Q1 (untested robustness, limitation 9).** Do the 24 EXP-002 contrasts at $q \in \{0.60, 0.80\}$, which EXP-003 did not cover, keep their sign and Holm significance under the three EXP-003 variations (V1 coin ties, $N = 50$; V2 $N = 10$; V3 $N = 200$)?
- **Q2 (mean versus distribution, limitation 10).** In what share of episodes does a social rule end below the independent baseline on the same episode, and how does the last agent's paired accuracy difference compare with the episode-mean difference?
- **Q3 (imitation versus Bayesian, limitation 11).** How large, with 95% intervals, are the paired imitation-minus-Bayesian differences in episode accuracy that EXP-002 reported only as differences of two contrasts?
- **Q4 (information quantity versus structure, protocol section 9).** Does the social-learning gain order by the expected number of observed actions, or do cells with very different observation quantity give similar gains?

## 2. Mechanism and rationale

Q1 closes the gap stated in the EXP-003 report (section 9). Q2 and Q3 address the bimodality and the exploratory rule difference noted in the EXP-002 report. Q4 inspects the competing explanation of protocol section 9 that "differences between networks can arise from the amount of information rather than its structure".

## 3. Competing explanations

Monte Carlo error (addressed by 10,000 paired episodes per contrast); post-hoc selection of comparisons (addressed by reporting every cell of each question, with no cell chosen after seeing it, and by labelling everything exploratory); implementation error (addressed by the same in-run checks C1 to C7 as EXP-003).

## 4. Design

- **Q1, new simulation, run EXP-004-R001.** Exactly the EXP-003 design (three rules, networks complete, window-2, window-3, $v \in \{1, 0.5\}$, variations V1, V2, V3, 1,000 episodes per seed and cell, bootstrap 2,000 resamples with seed 20261124, verification checks on) on the complementary values $q \in \{0.60, 0.80\}$. Master seeds 0 to 9, so that each episode draw matches the EXP-002 episode of the same seed and cell (streams are keyed by seed, $q$, network, $v$ and $N$; see `research/freeze.json`, C4). These seeds were already used by the confirmatory runs, so nothing held out is consumed. Configuration `experiments/EXP-004-R001.json`, output `results/exploratory/EXP-004-R001/`. Analysis: the frozen EXP-003 rule as implemented in `src/herd/robustness.py` (unchanged), against EXP-002-R001. Holm within each variation over its non-degenerate contrasts (family of 24), as in EXP-003.
- **Q2 and Q3, derived from committed raw arrays.** No new simulation. From `results/raw/EXP-002-R001/episodes.npz` and `results/raw/EXP-003-R001/episodes.npz`: for every social-rule contrast, the share of episodes with $\mathrm{Acc}_r(e) < \mathrm{Acc}_{\mathrm{ind}}(e)$, $= $ and $>$, and the paired last-agent difference with a normal 95% interval; for every cell, the paired difference $\mathrm{Acc}_{\mathrm{imit}}(e) - \mathrm{Acc}_{\mathrm{bayes}}(e)$ with a normal 95% interval and the share of episodes in which the two rules differ. No multiplicity adjustment and no p-value: these are descriptive.
- **Q4, derived from committed estimates.** The expected number of visible observed actions of agent $i$ is $v(i-1)$ under `complete` and $v \min(k, i-1)$ under `window-k`; its mean over $i = 1..N$ is tabulated beside $\Delta_r(c)$ from EXP-002-R001. Descriptive only.
- **Code:** `src/herd/exploratory.py` (Q2 to Q4), written for this experiment, with tests on hand-built arrays.

## 5. Sample size and budget

Q1: 10,000 paired episodes per contrast and variation, about 1.6 times EXP-003 (higher $q$ ends cascades sooner but the agent count is the same); one process, under one minute expected. Q2 to Q4: seconds. Workers: one.

## 6. Exclusions and stopping

No episode excluded. A failed verification check in R001 is reported as a finding and stops interpretation of R001. R001 is run once; any rerun is recorded.

## 7. What would contradict the main reading

For Q1: any sign reversal or loss of Holm significance at $q \in \{0.60, 0.80\}$ would extend the set of convention-dependent contrasts. For Q2: a share of episodes below baseline that is large compared with the mean gain would show that the positive mean conceals frequent harm at the group level. For Q4: gains that order by expected observation quantity alone would favour the quantity explanation over structure.

## 8. Reproduction commands

```
PYTHONPATH=src .venv/bin/python -m herd.cli run --config experiments/EXP-004-R001.json
PYTHONPATH=src .venv/bin/python -m herd.cli report --run results/exploratory/EXP-004-R001
PYTHONPATH=src .venv/bin/python -m herd.robustness --reference results/EXP-002/EXP-002-R001 --sensitivity results/exploratory/EXP-004-R001
PYTHONPATH=src .venv/bin/python -m herd.exploratory --out results/exploratory/EXP-004-derived
```
