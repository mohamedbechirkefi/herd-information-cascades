<!-- SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0 -->
# EXP-001 protocol: smoke matrix and engine verification (exploratory)

- **Status:** DRAFT v0.1, 2026-11-24. Exploratory by design: its numbers are never evidence for the study hypotheses. Not executed.
- **Depends on:** M2 core engine and unit tests.
- **Protocol hash:** recorded in `research/experiment_registry.csv` when the owner freezes the study protocol.

## 1. Precise question

Does the engine reproduce known analytic quantities and structural properties, produce schema-valid outputs for every rule, network and visibility level, and run fast enough for the EXP-002 budget?

## 2. Mechanism and rationale

The Bayesian `complete` model is analytically tractable (BHW1992 setting): the public signal difference is a random walk absorbed at $\pm 2$ under the own-signal tie rule. This gives exact targets against which the simulator can be checked before any comparison is interpreted.

## 3. Competing explanations for a mismatch

Implementation error; Monte Carlo error; an error in the analytic derivation itself (the derivation is written out in the report and checked by hand).

## 4. Hypotheses (verification checks, each with a pass criterion)

1. **Analytic anchor.** Bayesian, `complete`, $v = 1$: the observed share of episodes with a wrong cascade by agent $N$ matches $\frac{(1-q)^2}{q^2 + (1-q)^2}\left(1 - (2q(1-q))^{m}\right)$ with $m = \lfloor (N-1)/2 \rfloor$, within its 99% binomial interval. Derivation (to be repeated in the report): from a public difference of 0, the next two informative actions reach $+2$ with probability $q^2$, $-2$ with probability $(1-q)^2$ and return to 0 with probability $2q(1-q)$; the first cascading agent is agent $2j+1$ after $j$ such pairs, so a cascade agent exists by agent $N$ only if $j \leq m$. The M2 reference function computes the same quantity by exact enumeration for small $N$ as an independent check.
2. **Zero information** ($q = 1/2$): all rules have expected accuracy $1/2$; Bayesian agents' posteriors equal $1/2$ for every history; no cascades are recorded for Bayesian agents (every tie follows the own signal).
3. **Independent baseline:** mean accuracy matches $q$ within its 99% binomial interval; cascade share is exactly zero.
4. **Equivalence:** Bayesian and imitation actions are identical on every episode under `complete`.
5. **Schema:** every output validates against the versioned result schema.

A failed check is a finding: it is recorded, and EXP-002 does not start until it is resolved.

## 5. Estimands, unit and variables

Unit: episode. Smoke matrix: rules all three; $q \in \{0.5, 0.6, 0.8\}$; $G \in$ {complete, window-1}; $v = 1.0$; $N = 20$; 2 seeds $\times$ 200 episodes per cell. Metrics as in `research/protocol.md` section 4, plus runtime per 1,000 agent decisions.

## 6. Sample size and budget

400 episodes per arm, 36 arms: sufficient for the binomial checks at the 99% level to detect gross errors (half-width about 0.06 on a proportion), not for estimating effects. Budget: a few minutes locally.

## 7. Uncertainty, exclusions, stopping

Exact or Wilson binomial intervals for checks 1 and 3; checks 2, 4 and 5 are exact. No exclusions. Stop at the first failed check and diagnose.

## 8. Anticipated failure modes

Off-by-one in cascade onset; ties mis-detected through floating point; RNG streams not shared across rules.

## 9. Reproduction commands (planned)

```
uv run python -m herd.cli smoke
```
