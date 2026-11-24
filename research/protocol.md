<!-- SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0 -->
# HERD study protocol

**Status: DRAFT v0.1 (2026-11-24). Not frozen. Awaiting the owner's review and freeze (G-FREEZE).** No confirmatory experiment may run under this draft. Any run before the freeze is exploratory and labelled as such.

Per-experiment protocols: `research/experiments/EXP-001/protocol.md` (smoke, exploratory), `research/experiments/EXP-002/protocol.md` (main comparison), `research/experiments/EXP-003/protocol.md` (sensitivity). Feasibility audit: `research/feasibility.md`.

## 1. Research question

When does social information improve binary decisions, and when does it generate cascades of errors?

Operational form: in a sequential binary decision task with a hidden state, private noisy signals and publicly observed choices, how does the mean decision accuracy of agents who use social information (Bayesian social learners; naive vote-counting imitators) differ from that of agents who ignore it (independent baseline), as a function of signal quality, observation network and action visibility?

## 2. Formal model

- Hidden state $\theta \in \{0, 1\}$, drawn once per episode with $P(\theta = 1) = 1/2$.
- Agents $i = 1, \dots, N$ act once, in a fixed order.
- Private signal $s_i \in \{0, 1\}$, conditionally independent given $\theta$, with $P(s_i = \theta \mid \theta) = q$, $q \in [1/2, 1)$. $q = 1/2$ is the zero-information case.
- Action $a_i \in \{0, 1\}$; payoff 1 if $a_i = \theta$, else 0.
- Visibility: each action is publicly recorded with probability $v$, independently of everything else. The record shows which positions are hidden, so the realised visibility pattern is common knowledge. Hidden actions are seen by no one.
- Observation network $G$: agent $i$ observes the visible actions among the predecessor set $O_i$:
  - `complete`: $O_i = \{1, \dots, i-1\}$ (the setting of Bikhchandani, Hirshleifer and Welch, 1992);
  - `window-k`: $O_i = \{i-k, \dots, i-1\} \cap \{1, \dots\}$, with $k \in \{1, 3\}$ ($k = 1$ is the single-predecessor setting studied by Celen and Kariv, 2004).
- Decision rules (one rule per arm; populations are homogeneous within an arm):
  - **Independent (baseline):** $a_i = s_i$.
  - **Bayesian:** $a_i = \mathbb{1}[P(\theta = 1 \mid s_i, h_i) > 1/2]$, where $h_i$ is the observed history and all agents are commonly known to be Bayesian. Ties ($= 1/2$) follow the own signal (primary rule). Posteriors are computed exactly: for `complete`, by the public-belief recursion over visible actions; for `window-k`, by a forward recursion over the $2^{k}$ possible observed windows, $P(w_i \mid \theta)$, using the predecessors' deterministic decision tables. The likelihood ratio of one signal is $q/(1-q)$.
  - **Imitation (naive vote counting):** $a_i = \mathbb{1}[n_1 - n_0 + (2 s_i - 1) > 0]$, where $n_1, n_0$ count observed actions; ties follow the own signal. Every observed action is treated as one independent signal of the same precision as the agent's own, which is the naive inference error discussed by Eyster and Rabin (2010).
- Analytic anchor (for verification, not a result): for Bayesian agents, `complete`, $v = 1$, own-signal tie rule, the probability that a cascade on the wrong action eventually starts is $(1-q)^2 / (q^2 + (1-q)^2)$, and the probability that no cascade has started after $2m$ agents is $(2q(1-q))^m$. These follow from the random walk of the public signal difference, which is absorbed at $\pm 2$. They are derived in this protocol and will be checked by a test (M2) and by EXP-001.
- Pre-stated structural prediction (not a result): under `complete` with any $v$, the imitation rule and the Bayesian rule produce identical actions on every episode, because both act on their own signal while the observed lead is at most one and herd once it reaches two. Any difference in this setting indicates an implementation error. The two rules can differ under `window-k`.

## 3. Hypotheses (EXP-002, primary)

Let $\mathrm{Acc}_r(e)$ be the episode-level accuracy of rule $r$ in episode $e$ (definition in section 4) and $\Delta_r(c) = E[\mathrm{Acc}_r - \mathrm{Acc}_{\mathrm{ind}}]$ for cell $c = (q, G, v)$, estimated on matched episodes.

- **H0:** $\Delta_r(c) = 0$ for every social rule $r \in \{\text{Bayesian}, \text{imitation}\}$ and every cell $c$.
- **H1 (non-directional):** $\Delta_r(c) \neq 0$ for at least one $(r, c)$; the answer to the research question is the map of signs and magnitudes of $\Delta_r(c)$ over the grid, each with a Holm-adjusted 95% confidence interval.
- **Pre-stated directional expectations** (reported as expectations, tested by the same intervals): Bayesian $\Delta > 0$ in every cell with $q > 1/2$ (each Bayesian agent maximises its own expected accuracy given strictly more information); imitation $\Delta$ is non-positive in some `window-k` cells at low $q$. A Bayesian $\Delta$ significantly below zero contradicts theory and triggers the stopping rule for an implementation check before any interpretation.
- **Disconfirmation:** H1 is not supported if every Holm-adjusted interval contains zero. The directional expectation for imitation is contradicted if imitation $\Delta$ is significantly positive in every cell.

## 4. Operational definitions and metrics

All metrics are computed per episode, then averaged over episodes. Units are stated.

- **Primary metric: episode accuracy** $\mathrm{Acc}(e) = \frac{1}{N} \sum_{i=1}^{N} \mathbb{1}[a_i = \theta]$ (proportion, 0 to 1). Direction: higher is better. Justification: it directly measures whether decisions improve, it is defined identically for all rules, and it is the welfare quantity in the cited models. Primary contrast: paired difference against the independent baseline on the same episode.
- **Secondary metrics:**
  - *Cascade agent*: agent $i$ is in a cascade if its action would be identical under both values of $s_i$, given what it observed (counterfactual evaluation of the same rule). Independent agents are never in a cascade.
  - *Cascade probability* (proportion of episodes): at least one agent is in a cascade.
  - *Wrong-cascade probability* (proportion of episodes): at least one agent is in a cascade on the wrong action ($a_i \neq \theta$). This is the "cascade of errors" quantity.
  - *Error persistence* (agents): length of the longest run of consecutive incorrect actions in the episode.
  - *Information diversity*: share of agents whose action is informative (not in a cascade), proportion; plus the binary entropy (bits) of the within-episode action frequency, descriptive only.
  - *Last-agent accuracy* (proportion): $\mathbb{1}[a_N = \theta]$, for comparison with the asymptotic learning literature.

## 5. Design

- **Experimental unit:** an episode, i.e. one draw of $(\theta, s_1..s_N, \text{visibility pattern})$ played out by $N$ agents. Episodes are independent.
- **Matching (common random numbers):** within a seed and episode index, all three rules receive the same $\theta$, signals and visibility pattern. Comparisons are paired at the episode level.
- **Factors (full matrix, EXP-002):** rule $\in$ {independent, Bayesian, imitation} $\times$ $q \in \{0.55, 0.60, 0.70, 0.80\}$ $\times$ $G \in$ {complete, window-1, window-3} $\times$ $v \in \{1.0, 0.5\}$ = 72 arms, 24 cells. $N = 50$.
- **Seeds:** 10 independent master seeds (0 to 9), each producing 1,000 episodes per cell: 10,000 episodes per arm. Seeds are RNG streams and replication checks; per-seed means are reported. The inferential unit is the episode.
- **Sample-size rationale:** episode accuracy lies in [0, 1], so a paired difference has standard deviation at most 1, and in practice at most about 0.5 for bimodal cascade outcomes. With 10,000 paired episodes the standard error is at most 0.005 at SD 0.5, giving a 95% half-width of about 0.01 (one accuracy point) before multiplicity adjustment. This is the smallest effect treated as practically meaningful. The cost estimate is in `research/feasibility.md`.
- **Uncertainty method:** for each $(r, c)$, the mean paired difference with a normal-approximation 95% interval at the episode level, checked against a percentile bootstrap over episodes (2,000 resamples, fixed seed). Holm adjustment across the 48 primary contrasts (2 rules $\times$ 24 cells), with two-sided paired t-test p-values. Effect sizes are reported as absolute differences in accuracy points, with raw distributions (histograms of episode accuracy) for every arm.
- **Controls:** the independent rule is the baseline; the zero-information case $q = 1/2$ and the analytic anchor of section 2 are verification controls (EXP-001, tests).
- **Compute budget:** fixed in advance at one local machine, single process allowed, wall-clock target under one hour for EXP-002; the actual runtime is recorded.

## 6. Exclusion and stopping rules

- No episode is excluded on the basis of its outcome.
- A run that fails schema validation or raises an error is recorded as failed, rerun once with the same seed after a fix is documented, and reported as missing if it fails again. No failed run is silently dropped.
- Fixed sample size. No optional stopping or interim looks at outcomes.
- Stop and investigate (no interpretation) if any verification test fails, if Bayesian accuracy is significantly below independent accuracy in any cell, or if the imitation and Bayesian rules diverge under `complete`.

## 7. Smoke matrix (EXP-001, exploratory)

Rules all three; $q \in \{0.5, 0.6, 0.8\}$; $G \in$ {complete, window-1}; $v = 1.0$; $N = 20$; 2 seeds $\times$ 200 episodes. Purpose: toolchain, schema, timing and verification checks only. Its numbers are never used as evidence for H1.

## 8. Sensitivity analysis (EXP-003)

The main interpretation could be invalidated if the sign of $\Delta$ depends on arbitrary modelling conventions. EXP-003 reruns the EXP-002 cells for $q \in \{0.55, 0.70\}$ with:

1. **Tie rule:** ties broken by a fair coin instead of the own signal (the convention of Bikhchandani, Hirshleifer and Welch, 1992).
2. **Horizon:** $N \in \{10, 200\}$ instead of 50, since averaging over agents weights early, informative actions differently.

The main interpretation is considered fragile if any Holm-significant sign in EXP-002 reverses or loses significance under either variation; this is reported as a finding, not hidden.

## 9. Confounders and competing explanations

- Accuracy averaged over agents mixes early (pre-cascade) and late behaviour; addressed by reporting last-agent accuracy and the horizon sensitivity.
- Tie conventions change cascade onset; addressed by EXP-003.
- Differences between networks can arise from the amount of information rather than its structure; the visibility factor varies information quantity within a network.
- Implementation errors can mimic effects; addressed by the analytic anchor, the zero-information case and the structural equivalence check.

## 10. Claims boundary

Synthetic actors do not establish real human irrationality. The rules are stylised; the Bayesian rule assumes common knowledge of rationality and of the network. Results hold only within these assumptions.

## 11. Amendments

None. Any amendment after the freeze will be dated, justified and kept separate from the frozen analysis.
