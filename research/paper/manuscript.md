<!-- SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0 -->
<!-- Status: independent research manuscript / preprint draft, not peer-reviewed. Version 1.0 (M4, 2026-11-25), revised after the second review pass (`research/publication/review_pass_2.md`). Tables between GENERATED markers are written by `python -m herd.paper fill` from committed results; do not edit them by hand. -->
# Higher average accuracy, frequent locked-in errors: a simulation study of Bayesian and naive social learning

**Status:** independent research manuscript / preprint draft, not peer-reviewed. Version 1.0, 2026-11-25. Working title until M4: *How groups can become confidently wrong*. The M4 title was approved by the owner on 2026-11-25 (decision log D-012).

## Author and affiliation metadata

Mohamed Bechir Kefi. No affiliation. (Approved by the owner on 2026-11-24, common decision C3.)

## Abstract

Sequential social learning can raise decision accuracy or lock a group into an error. We simulated binary decisions with a hidden state, private signals of precision $q$ and publicly observed actions, and compared exact Bayesian social learners and naive vote-counting imitators with agents who ignore social information, on matched episodes. The confirmatory study (EXP-002, frozen protocol) crossed four signal precisions, three observation networks (complete history, last two or last three predecessors) and two visibility levels, with 10,000 paired episodes of 50 agents per contrast. All 48 contrasts were positive and Holm-significant, from +0.0059 (95% CI 0.0048 to 0.0070) to +0.1439 (0.1375 to 0.1504) on the proportion scale; 46 exceeded the protocol's practical threshold of 0.01. A pre-stated expectation that this naive rule would lower accuracy in some restricted network at low precision was contradicted. The same rules produced wrong cascades in up to 0.87 of episodes. A frozen sensitivity analysis (EXP-003) found no sign reversal under coin-flip tie-breaking or horizons of 10 and 200 agents, but coin ties shrank every gain (to 0.0036 to 0.0494) and removed significance for two contrasts, so the magnitudes are specific to the own-signal convention. Exploratory checks extend the sign robustness to the untested precisions and show that the social group ends below the independent baseline in a share of episodes between 0.05 and 0.43. Within this stylised model, social information raises accuracy on average over groups while frequently leaving a group worse off than independent agents; nothing here concerns real people.

## Keywords

information cascades; social learning; herding; Bayesian learning; naive inference; simulation study

## 1. Introduction

When people decide in sequence and can see what others chose, each choice carries information about the private evidence behind it. Using that information can make later decisions better informed. It can also stop learning altogether: once the public evidence outweighs any single private signal, each agent follows the crowd regardless of its own signal, so later actions reveal nothing, and the crowd can settle on the wrong action. This is the informational cascade described by Bikhchandani, Hirshleifer and Welch (1992) and Banerjee (1992). Whether observing others helps or harms on balance depends on how agents interpret what they see, how much of the history they see, and how reliable their own information is.

The research question of this study is: **when does social information improve binary decisions, and when does it generate cascades of errors?** We answer it within a fully specified simulation model, not for real people. The gap we address is narrow. Analytic results exist for the classic complete-history model, and naive inference has been studied analytically (Eyster and Rabin, 2010), but we are not aware of a matched-episode comparison that places an exact Bayesian rule and a naive counting rule against the same independent baseline across signal precision, recent-window observation networks and partial visibility, reports error-cascade metrics next to accuracy, and tests the result against modelling conventions in a protocol frozen before execution. Our literature search was non-systematic, so we make no novelty claim.

**Hypotheses.** H0: for each social rule and each cell (precision, network, visibility), the expected paired difference in episode accuracy against the independent baseline is zero. H1 (non-directional): at least one difference is non-zero. Pre-stated directional expectations: the Bayesian difference is non-negative everywhere; the two social rules act identically under the complete network; naive imitation lowers accuracy in at least one restricted-network cell at low precision.

**Contributions.**

1. A verified simulation engine with exact Bayesian posteriors for complete and recent-window observation networks under partial visibility, checked against a closed-form cascade probability and an independent exact rational oracle (Sections 3 and 4.2).
2. A confirmatory map of 48 paired accuracy contrasts (EXP-002), with all secondary cascade metrics (Section 5.2).
3. A frozen sensitivity analysis of the tie-breaking convention and the horizon (EXP-003), plus a labelled exploratory extension and distributional analysis (EXP-004) (Sections 5.3 and 5.4).
4. A full evidence trail: frozen protocols with hashes, per-experiment reports, raw per-episode outputs and an artifact manifest (Section 10).

## 2. Related work

All sources below were checked at the level of bibliographic metadata and abstract on 2026-11-24 (records listed in `research/literature_review.md`). On 2026-11-25 (M6) freely available full texts were read for Bikhchandani, Hirshleifer and Welch (1992), and working-paper versions for Acemoglu et al., Celen and Kariv, Eyster and Rabin and Weizsacker; each statement below was checked against them (pages and sections in `research/publication/evidence_audit.md`, section 3). Statements about Banerjee (1992), Smith and Sorensen (2000), Golub and Jackson (2010) and Anderson and Holt (1997) remain limited to what their abstracts say.

**Informational cascades.** Bikhchandani, Hirshleifer and Welch (1992) define an informational cascade as a situation in which it is optimal to follow predecessors regardless of one's own information, and use it to explain localised conformity and the fragility of mass behaviour. Banerjee (1992) shows that optimising agents who observe predecessors herd and that the equilibrium is inefficient. Our `complete` network with full visibility and Bayesian agents is this setting; we use it as an analytic anchor and a replication target, not as a contribution.

**Pathologies and networks.** Smith and Sorensen (2000) show that with heterogeneous preferences "confounded learning" can arise besides herds; our populations are homogeneous, so this mechanism is excluded. Acemoglu, Dahleh, Lobel and Ozdaglar (2011) study sequential learning over stochastic observation networks and give conditions on "expansion in observations" for learning with unbounded private beliefs; our binary signals give bounded beliefs, and our networks are deterministic recent windows chosen so that exact posteriors can be computed. Celen and Kariv (2004) study Bayesian sequential decisions in which each agent observes only the immediate predecessor's action (checked against the authors' working-paper version); our `window-k` networks with $k \geq 2$ do not include that case.

**Naive inference.** Eyster and Rabin (2010) study naive agents who treat predecessors' actions as reflecting only private information; according to their abstract such agents over-weight early movers, herd on wrong actions with positive probability and can be worse off from observing others. Our imitation rule is a simplified operationalisation of that idea (each observed action counts as one independent signal); it is not a replication of their model, and our results neither confirm nor contradict theirs. Golub and Jackson (2010) concern repeated averaging (DeGroot) rather than one-shot sequential choices and are related work only.

**Human subjects.** Laboratory studies (Anderson and Holt, 1997; the meta-analysis of 13 experiments by Weizsacker, 2008, working paper) examine whether people cascade and whether they follow others when they should. We study synthetic agents only and make no claim about human behaviour.

**Positioning.** Replication: the complete-network Bayesian anchor. Extension: exact Bayesian posteriors for recent-window networks with partial, commonly known visibility, compared on matched episodes with a naive rule. Original to this study within the limits of our search: the frozen-protocol sensitivity analysis of the paired contrast map.

## 3. Background and formal model

**Task.** A hidden state $\theta \in \{0, 1\}$ is drawn with probability 1/2. Agents $i = 1, \dots, N$ act once, in order. Agent $i$ receives a private binary signal $s_i$ with $P(s_i = \theta \mid \theta) = q$, $q \in [1/2, 1)$, independent across agents given $\theta$, and chooses $a_i \in \{0, 1\}$ with payoff $\mathbb{1}[a_i = \theta]$.

**Visibility and networks.** Each action is publicly recorded with probability $v$, independently; which positions are hidden is common knowledge, and hidden actions are seen by no one. Agent $i$ observes the visible actions of its predecessor set $O_i$: `complete`, $O_i = \{1, \dots, i-1\}$; `window-k`, $O_i = \{i-k, \dots, i-1\}$, $k \in \{2, 3\}$.

**Rules.** Each arm has a homogeneous population.

- Independent (baseline): $a_i = s_i$.
- Bayesian: $a_i = \mathbb{1}[P(\theta = 1 \mid s_i, h_i) > 1/2]$, where $h_i$ is the observed history and all agents are commonly known to be Bayesian; ties follow the own signal. Under `complete` the posterior is computed by the public-belief recursion over visible actions; under `window-k` by a forward recursion over the $2^k$ possible observed windows conditional on $\theta$, using the predecessors' decision tables. The likelihood ratio of one signal is $q/(1-q)$.
- Imitation (naive vote counting): $a_i = \mathbb{1}[n_1 - n_0 + (2s_i - 1) > 0]$, where $n_1$ and $n_0$ count observed actions; ties follow the own signal.

**Analytic anchor.** For Bayesian agents under `complete`, $v = 1$, own-signal ties and $q > 1/2$, the public signal difference is a random walk absorbed at $\pm 2$: from 0, the next two informative actions reach $+2$ with probability $q^2$, $-2$ with probability $(1-q)^2$, and return to 0 with probability $2q(1-q)$. The probability that a wrong cascade has started by agent $N$ is therefore

$$P_{\text{wrong}}(N) = \frac{(1-q)^2}{q^2 + (1-q)^2}\left(1 - (2q(1-q))^{m}\right), \qquad m = \lfloor (N-1)/2 \rfloor .$$

Under the same conditions, the imitation rule takes the same action as the Bayesian rule on every episode, because both follow their own signal while the observed lead is at most one and herd once it reaches two. These two properties are verification targets, not results.

**Metrics.** Episode accuracy $\mathrm{Acc}(e) = \frac{1}{N}\sum_i \mathbb{1}[a_i = \theta]$ (proportion) is the primary metric. An agent is in a cascade if its action would be the same under both values of its own signal, given what it observed. Secondary metrics: cascade probability and wrong-cascade probability (share of episodes with at least one agent in a cascade, respectively in a cascade on the wrong action), longest run of consecutive wrong actions (agents), informative-action share, action entropy (bits) and last-agent accuracy. The estimand is $\Delta_r(c) = E_e[\mathrm{Acc}_r(e) - \mathrm{Acc}_{\mathrm{ind}}(e)]$ for rule $r$ and cell $c = (q, G, v)$.

**Complexity.** The window recursion costs $O(N \cdot 2^k)$ per decision table and episode; at the sizes used, a full confirmatory run takes seconds (Section 5).

## 4. Methods

### 4.1 Design and controls

- **EXP-001 (exploratory, verification).** Smoke matrix: three rules, $q \in \{0.5, 0.6, 0.8\}$, networks `complete` and `window-1`, $v = 1$, $N = 20$, 2 seeds $\times$ 200 episodes; checks C1 to C6 (analytic anchor, zero information, independent baseline, complete-network equivalence, schema, no near ties). Five runs: R001 to R004 before the freeze, R005 immediately before the confirmatory runs.
- **EXP-002 (confirmatory).** Three rules $\times$ $q \in \{0.55, 0.60, 0.70, 0.80\}$ $\times$ $G \in$ {complete, window-2, window-3} $\times$ $v \in \{1, 0.5\}$: 72 arms, 24 cells, 48 contrasts; $N = 50$; master seeds 0 to 9, 1,000 episodes per seed and cell, so 10,000 paired episodes per contrast.
- **EXP-003 (confirmatory sensitivity).** The EXP-002 design on $q \in \{0.55, 0.70\}$ under V1 (coin-flip ties, $N = 50$), V2 (own-signal ties, $N = 10$) and V3 (own-signal ties, $N = 200$). Frozen interpretation rule: an EXP-002 Holm-significant contrast whose sign reverses or which loses Holm significance under any variation is reported as convention-dependent.
- **EXP-004 (exploratory, post hoc, M4).** The EXP-003 design on the remaining $q \in \{0.60, 0.80\}$ (run EXP-004-R001, seeds 0 to 9), and descriptive analyses of the committed per-episode outputs: share of episodes below the baseline, last-agent paired difference, paired imitation-minus-Bayesian difference and observation quantity.
- **Controls.** The independent rule on the same episode is the baseline for every contrast. Common random numbers: within a seed and cell, all rules receive the same $\theta$, signals and visibility pattern; coin flips use a separate stream.

### 4.2 Implementation and verification

The engine (`src/herd/`) is written in Python 3.12.1 with numpy 2.3.4 as its only runtime dependency. An exact rational oracle (`src/herd/reference.py`) enumerates every state, signal and coin profile for $N \leq 9$, derives each decision from the posterior definition, and shares no code with the engine; it is the reference of the differential tests. Ties are detected with a relative tolerance of $10^{-9}$, and comparisons with a relative gap in $(10^{-9}, 10^{-6}]$ are counted as near ties (check C6). The unit suite had 278 tests at the frozen revision, 281 after the confirmatory runs and 289 after the M4 additions (evidence audit and exploratory analyses). Every run ran its verification checks: EXP-002-R001 passed 61 of 61, EXP-003-R001 89 of 89, EXP-004-R001 89 of 89.

### 4.3 Statistical analysis

For each contrast: the mean paired difference with a normal-approximation 95% interval at the episode level, checked against a percentile bootstrap (2,000 resamples, fixed seed); a two-sided paired t-test; Holm adjustment within each experiment or variation over its non-degenerate contrasts at familywise 0.05. A contrast with zero paired variance would be reported as an exact comparison outside the Holm family; none occurred. The reported intervals are unadjusted and describe magnitude; decisions use the Holm-adjusted p-values only. Secondary metrics are described with 95% intervals and no multiplicity adjustment. EXP-004 quantities are descriptive with unadjusted normal intervals and no p-values. The inferential unit is the episode; per-seed means are reported as replication checks.

### 4.4 Protocol registration and reproducibility

The study protocol and the EXP-002 and EXP-003 protocols were frozen at v1.0 on 2026-11-24 with the owner's approval, after amendments A-1 to A-5 made before any confirmatory value was seen (A-1 replaced the degenerate `window-1` network by `window-2`; A-2 restricted the anchor and the equivalence check to $q > 1/2$; A-3 and A-4 fixed the treatment of zero-variance contrasts and the meaning of the intervals; A-5 kept the sample). The freeze was internal to the repository (SHA-256 hashes in `research/freeze.json` and `research/experiment_registry.csv`, enforced by a run gate); it was not registered with an external registry. Exploratory values of the primary contrast from runs EXP-001-R001 to R004 were seen before the freeze and are disclosed in `research/freeze.json`. EXP-002 and EXP-003 ran once each, at code revision `50fbdb1`, with no failed cell or dropped run. EXP-004 was designed after all confirmatory results were seen and is exploratory throughout.

## 5. Results

### 5.1 EXP-001: verification (exploratory)

All checks passed in all five runs (R001 25 of 25, R002 61 of 61, R003 89 of 89, R004 17 of 17, R005 25 of 25). Under `window-1`, both social rules reproduced the independent baseline exactly, which motivated amendment A-1. In the confirmatory runs, the analytic anchor C1 held at every precision: the analytic values 0.4010, 0.3077, 0.1552 and 0.0588 lie inside the Wilson 99% intervals of the observed wrong-cascade shares 0.4084, 0.3098, 0.1550 and 0.0597 ($q = 0.55$, 0.60, 0.70, 0.80; EXP-002-R001). Bayesian and imitation actions were identical on all 10,000 episodes of each of the 8 complete-network cells (C4).

### 5.2 EXP-002: social information and mean accuracy (confirmatory)

All 48 contrasts were non-degenerate (Holm family $m = 48$), positive and Holm-significant; the largest Holm-adjusted p-value was $3.1 \times 10^{-14}$. Every contrast was positive in each of the 10 seeds. The normal and bootstrap intervals differed by at most 0.0006. Table 1 gives every contrast; Figure 1 (`results/EXP-002/EXP-002-R001/figures/delta.svg`) plots them with their intervals, and Figure 2 (`results/EXP-002/EXP-002-R001/figures/accuracy_hist.svg`) shows the episode-accuracy distribution of every arm.

**Table 1 (TAB-001).** EXP-002-R001: mean paired difference in episode accuracy against the independent baseline (proportion scale; 0.01 is one accuracy point), with unadjusted 95% normal intervals; 10,000 paired episodes per contrast, $N = 50$, own-signal ties. All 48 are Holm-significant (Holm-adjusted p at most $3.1 \times 10^{-14}$). Source: `results/EXP-002/EXP-002-R001/result.json`.

<!-- BEGIN GENERATED TAB-001 -->
| q | Network | v | Bayesian Delta [95% CI] | Imitation Delta [95% CI] |
|---|---|---|---|---|
| 0.55 | complete | 1 | 0.0380 [0.0290, 0.0470] | 0.0380 [0.0290, 0.0470] |
| 0.55 | complete | 0.5 | 0.0400 [0.0317, 0.0483] | 0.0400 [0.0317, 0.0483] |
| 0.55 | window-2 | 1 | 0.0386 [0.0295, 0.0477] | 0.0386 [0.0295, 0.0477] |
| 0.55 | window-2 | 0.5 | 0.0091 [0.0067, 0.0114] | 0.0059 [0.0048, 0.0070] |
| 0.55 | window-3 | 1 | 0.0424 [0.0335, 0.0514] | 0.0448 [0.0360, 0.0536] |
| 0.55 | window-3 | 0.5 | 0.0195 [0.0151, 0.0239] | 0.0131 [0.0109, 0.0152] |
| 0.6 | complete | 1 | 0.0836 [0.0752, 0.0921] | 0.0836 [0.0752, 0.0921] |
| 0.6 | complete | 0.5 | 0.0783 [0.0705, 0.0861] | 0.0783 [0.0705, 0.0861] |
| 0.6 | window-2 | 1 | 0.0617 [0.0529, 0.0705] | 0.0617 [0.0529, 0.0705] |
| 0.6 | window-2 | 0.5 | 0.0225 [0.0203, 0.0247] | 0.0132 [0.0122, 0.0142] |
| 0.6 | window-3 | 1 | 0.0824 [0.0739, 0.0909] | 0.0907 [0.0824, 0.0990] |
| 0.6 | window-3 | 0.5 | 0.0349 [0.0306, 0.0392] | 0.0274 [0.0253, 0.0295] |
| 0.7 | complete | 1 | 0.1344 [0.1277, 0.1412] | 0.1344 [0.1277, 0.1412] |
| 0.7 | complete | 0.5 | 0.1216 [0.1153, 0.1280] | 0.1216 [0.1153, 0.1280] |
| 0.7 | window-2 | 1 | 0.0992 [0.0918, 0.1066] | 0.0992 [0.0918, 0.1066] |
| 0.7 | window-2 | 0.5 | 0.0337 [0.0317, 0.0356] | 0.0212 [0.0202, 0.0221] |
| 0.7 | window-3 | 1 | 0.1335 [0.1268, 0.1402] | 0.1439 [0.1375, 0.1504] |
| 0.7 | window-3 | 0.5 | 0.0636 [0.0600, 0.0673] | 0.0466 [0.0448, 0.0484] |
| 0.8 | complete | 1 | 0.1317 [0.1272, 0.1362] | 0.1317 [0.1272, 0.1362] |
| 0.8 | complete | 0.5 | 0.1251 [0.1209, 0.1293] | 0.1251 [0.1209, 0.1293] |
| 0.8 | window-2 | 1 | 0.1086 [0.1033, 0.1139] | 0.1086 [0.1033, 0.1139] |
| 0.8 | window-2 | 0.5 | 0.0363 [0.0349, 0.0378] | 0.0235 [0.0228, 0.0243] |
| 0.8 | window-3 | 1 | 0.1342 [0.1298, 0.1386] | 0.1394 [0.1353, 0.1436] |
| 0.8 | window-3 | 0.5 | 0.0704 [0.0678, 0.0731] | 0.0526 [0.0513, 0.0540] |
<!-- END GENERATED TAB-001 -->

The gain grows with $q$ up to $q = 0.7$ and then levels off under `complete` and `window-3` with full visibility. Halving visibility shrinks the gain sharply in the window networks (Bayesian, $q = 0.7$: window-2 from 0.0992 to 0.0337) but only slightly under `complete` (0.1344 to 0.1216). The smallest effect is the imitation contrast at $q = 0.55$, window-2, $v = 0.5$: +0.0059 [0.0048, 0.0070]. The expectation that imitation would lower accuracy in at least one window cell at low precision is therefore contradicted for this rule and this grid. Statistical significance is not practical size: the protocol (section 5) names 0.01 as the smallest practically meaningful effect, and 2 of the 48 contrasts are below it (imitation +0.0059 and Bayesian +0.0091, both at $q = 0.55$, window-2, $v = 0.5$).

**Cascades of errors.** The same rules that raise mean accuracy produce frequent wrong cascades (Table 3, first column): 0.408 of episodes for both social rules at $q = 0.55$, complete, $v = 1$, and up to 0.868 for imitation at $q = 0.55$, window-3, $v = 0.5$. At $q = 0.55$, complete, $v = 1$, the longest run of wrong actions averages 20.07 agents of 50 for Bayesian agents against 4.41 for the baseline. Under partial visibility in the window networks, wrong-cascade probabilities are high while accuracy still improves (they reach 0.868 at $q = 0.55$), because the metric counts an episode once even if the cascade is later broken.

### 5.3 EXP-003: sensitivity to tie rule and horizon (confirmatory)

No contrast was degenerate (Holm family $m = 24$ per variation). Of the 72 comparisons, 70 were robust, none reversed sign, and 2 lost significance (Table 2, rows EXP-003-R001). Both are at $q = 0.55$, window-3, $v = 1$ under coin ties: Bayesian $\Delta = 0.0082$ [$-0.0013$, 0.0176] and imitation 0.0079 [$-0.0015$, 0.0174], Holm-adjusted p 0.18, against 0.0424 and 0.0448 in EXP-002. By the frozen rule these two EXP-002 conclusions are convention-dependent. Coin ties reduced all 24 gains, by more than half in 16 of them; horizons changed magnitudes but not significance (Bayesian, $q = 0.7$, complete, $v = 1$: 0.0957 at $N = 10$, 0.1344 at $N = 50$, 0.1452 at $N = 200$).

**Table 2 (TAB-002).** Robustness of the EXP-002 contrasts under the three variations, by the frozen EXP-003 rule. Rows EXP-003-R001 are confirmatory; rows EXP-004-R001 are exploratory and post hoc. "Compared" counts EXP-002 Holm-significant contrasts in the variation's grid; Delta range and largest Holm p are over the variation's 24 contrasts; the last column counts contrasts positive in every seed. Sources: the two `robustness_vs_EXP-002-R001.csv` tables and the runs' `result.json`.

<!-- BEGIN GENERATED TAB-002 -->
| Source | Label | Variation | q values | Compared | Robust | Lost significance | Sign reversed | Delta range | Largest Holm p | Positive in all 10 seeds |
|-------|------------|-----------|-----|---------|------|----------|--------|-----------|------|-------|
| EXP-003-R001 | confirmatory | V1 (N=50, coin ties) | 0.55, 0.70 | 24 | 22 | 2 | 0 | 0.0036 to 0.0494 | 0.18 | 13 of 24 |
| EXP-003-R001 | confirmatory | V2 (N=10, own ties) | 0.55, 0.70 | 24 | 24 | 0 | 0 | 0.0074 to 0.0957 | 7.2e-08 | 22 of 24 |
| EXP-003-R001 | confirmatory | V3 (N=200, own ties) | 0.55, 0.70 | 24 | 24 | 0 | 0 | 0.0068 to 0.1572 | 7.3e-13 | 24 of 24 |
| EXP-004-R001 | exploratory | V1 (N=50, coin ties) | 0.60, 0.80 | 24 | 24 | 0 | 0 | 0.0083 to 0.0600 | 1.7e-06 | 19 of 24 |
| EXP-004-R001 | exploratory | V2 (N=10, own ties) | 0.60, 0.80 | 24 | 24 | 0 | 0 | 0.0108 to 0.0999 | < 1e-15 | 24 of 24 |
| EXP-004-R001 | exploratory | V3 (N=200, own ties) | 0.60, 0.80 | 24 | 24 | 0 | 0 | 0.0120 to 0.1476 | < 1e-15 | 24 of 24 |
<!-- END GENERATED TAB-002 -->

### 5.4 EXP-004: exploratory extensions (post hoc)

**Untested precisions.** Applied to $q \in \{0.60, 0.80\}$, the same three variations left all 72 comparisons robust (Table 2, rows EXP-004-R001). Coin ties again reduced every gain, to between 0.27 and 0.63 of its EXP-002 value. This extends the sign robustness of EXP-003 in an exploratory way; it does not change the confirmatory EXP-003 verdict.

**Distribution of outcomes.** Table 3 reports, per cell, the share of episodes in which the social rule ends below the independent baseline on the same episode. It ranges from 0.050 to 0.425; at $q = 0.55$ it lies between 0.371 and 0.425 in every cell. With full visibility it coincides, to three decimals, with the wrong-cascade probability. The last agent's paired gain is positive in all 48 contrasts, with 95% intervals excluding zero (from 0.0067 to 0.1595).

**Table 3 (TAB-003).** EXP-002-R001, by cell, Bayesian (B) and imitation (I). Wrong-cascade probability: share of episodes with at least one agent in a wrong cascade (secondary metric, confirmatory run). Share below baseline: share of the 10,000 paired episodes with $\mathrm{Acc}_r(e) < \mathrm{Acc}_{\mathrm{ind}}(e)$ (EXP-004, exploratory). Last-agent Delta: paired difference in the last agent's accuracy (EXP-004, exploratory). Sources: `result.json`; `results/exploratory/EXP-004-derived/q2_distribution.csv`.

<!-- BEGIN GENERATED TAB-003 -->
| q | Network | v | Wrong-cascade probability, B / I | Share of episodes below baseline, B / I (exploratory) | Last-agent Delta, B / I (exploratory) |
|---|---|---|---|---|---|
| 0.55 | complete | 1 | 0.408 / 0.408 | 0.408 / 0.408 | 0.0442 / 0.0442 |
| 0.55 | complete | 0.5 | 0.402 / 0.402 | 0.402 / 0.402 | 0.0435 / 0.0435 |
| 0.55 | window-2 | 1 | 0.409 / 0.409 | 0.409 / 0.409 | 0.0453 / 0.0453 |
| 0.55 | window-2 | 0.5 | 0.829 / 0.842 | 0.412 / 0.371 | 0.0166 / 0.0067 |
| 0.55 | window-3 | 1 | 0.404 / 0.400 | 0.404 / 0.400 | 0.0425 / 0.0467 |
| 0.55 | window-3 | 0.5 | 0.774 / 0.868 | 0.425 / 0.402 | 0.0226 / 0.0187 |
| 0.6 | complete | 1 | 0.310 / 0.310 | 0.310 / 0.310 | 0.0907 / 0.0907 |
| 0.6 | complete | 0.5 | 0.305 / 0.305 | 0.305 / 0.305 | 0.1014 / 0.1014 |
| 0.6 | window-2 | 1 | 0.334 / 0.334 | 0.334 / 0.334 | 0.0615 / 0.0615 |
| 0.6 | window-2 | 0.5 | 0.750 / 0.763 | 0.347 / 0.305 | 0.0175 / 0.0111 |
| 0.6 | window-3 | 1 | 0.311 / 0.300 | 0.311 / 0.300 | 0.0909 / 0.1023 |
| 0.6 | window-3 | 0.5 | 0.691 / 0.786 | 0.371 / 0.336 | 0.0356 / 0.0294 |
| 0.7 | complete | 1 | 0.155 / 0.155 | 0.155 / 0.155 | 0.1433 / 0.1433 |
| 0.7 | complete | 0.5 | 0.157 / 0.157 | 0.157 / 0.157 | 0.1356 / 0.1356 |
| 0.7 | window-2 | 1 | 0.196 / 0.196 | 0.196 / 0.196 | 0.1116 / 0.1116 |
| 0.7 | window-2 | 0.5 | 0.551 / 0.556 | 0.252 / 0.218 | 0.0453 / 0.0261 |
| 0.7 | window-3 | 1 | 0.156 / 0.142 | 0.156 / 0.142 | 0.1453 / 0.1595 |
| 0.7 | window-3 | 0.5 | 0.475 / 0.562 | 0.252 / 0.225 | 0.0578 / 0.0428 |
| 0.8 | complete | 1 | 0.060 / 0.060 | 0.060 / 0.060 | 0.1413 / 0.1413 |
| 0.8 | complete | 0.5 | 0.058 / 0.058 | 0.058 / 0.058 | 0.1395 / 0.1395 |
| 0.8 | window-2 | 1 | 0.087 / 0.087 | 0.087 / 0.087 | 0.1170 / 0.1170 |
| 0.8 | window-2 | 0.5 | 0.303 / 0.306 | 0.155 / 0.135 | 0.0372 / 0.0240 |
| 0.8 | window-3 | 1 | 0.057 / 0.050 | 0.057 / 0.050 | 0.1318 / 0.1388 |
| 0.8 | window-3 | 0.5 | 0.248 / 0.300 | 0.144 / 0.129 | 0.0733 / 0.0538 |
<!-- END GENERATED TAB-003 -->

**Imitation against Bayesian.** Table 4 gives the paired difference between the two social rules in the window networks. Under half visibility imitation is below Bayesian in all 8 cells (by 0.0032 to 0.0178). Under window-3 with full visibility imitation is above Bayesian at $q = 0.6$, 0.7 and 0.8 (by 0.0052 to 0.0104), and the interval includes zero at $q = 0.55$. Under window-2 with full visibility the two rules gave the same actions on every episode, which the protocol did not predict.

**Table 4 (TAB-004).** EXP-002-R001 window cells: paired difference in episode accuracy, imitation minus Bayesian, with unadjusted 95% normal intervals, and the share of episodes in which the two accuracies differ (EXP-004, exploratory; no multiplicity control). Source: `results/exploratory/EXP-004-derived/q3_imitation_minus_bayesian.csv`.

<!-- BEGIN GENERATED TAB-004 -->
| q | Network | v | Imitation minus Bayesian [95% CI] | Share of episodes where the rules differ |
|---|---|---|---|---|
| 0.55 | window-2 | 1 | 0.0000 [0.0000, 0.0000] | 0.000 |
| 0.55 | window-2 | 0.5 | -0.0032 [-0.0050, -0.0014] | 0.834 |
| 0.55 | window-3 | 1 | 0.0024 [-0.0020, 0.0068] | 0.125 |
| 0.55 | window-3 | 0.5 | -0.0064 [-0.0100, -0.0028] | 0.932 |
| 0.6 | window-2 | 1 | 0.0000 [0.0000, 0.0000] | 0.000 |
| 0.6 | window-2 | 0.5 | -0.0093 [-0.0110, -0.0076] | 0.829 |
| 0.6 | window-3 | 1 | 0.0083 [0.0043, 0.0123] | 0.108 |
| 0.6 | window-3 | 0.5 | -0.0075 [-0.0110, -0.0040] | 0.928 |
| 0.7 | window-2 | 1 | 0.0000 [0.0000, 0.0000] | 0.000 |
| 0.7 | window-2 | 0.5 | -0.0125 [-0.0140, -0.0110] | 0.798 |
| 0.7 | window-3 | 1 | 0.0104 [0.0075, 0.0134] | 0.074 |
| 0.7 | window-3 | 0.5 | -0.0170 [-0.0200, -0.0140] | 0.900 |
| 0.8 | window-2 | 1 | 0.0000 [0.0000, 0.0000] | 0.000 |
| 0.8 | window-2 | 0.5 | -0.0128 [-0.0139, -0.0117] | 0.697 |
| 0.8 | window-3 | 1 | 0.0052 [0.0034, 0.0070] | 0.040 |
| 0.8 | window-3 | 0.5 | -0.0178 [-0.0200, -0.0156] | 0.813 |
<!-- END GENERATED TAB-004 -->

**Observation quantity.** Table 5 orders the networks by the mean expected number of visible observed actions per agent. Among the four window cells, the Bayesian gain increases with that quantity at every $q$; from window-3 at $v = 1$ to complete at $v = 1$, the quantity rises about 8.5 times while the gain changes by less than 0.005.

**Table 5 (TAB-005).** Mean over agents of the expected number of visible observed actions ($v(i-1)$ for complete, $v\min(k, i-1)$ for window-$k$, $N = 50$) beside the EXP-002 Bayesian contrast (EXP-004, exploratory, descriptive). Source: `results/exploratory/EXP-004-derived/q4_quantity.csv`.

<!-- BEGIN GENERATED TAB-005 -->
| Network | v | Mean expected observed actions per agent | Bayesian Delta, q = 0.55 | Bayesian Delta, q = 0.60 | Bayesian Delta, q = 0.70 | Bayesian Delta, q = 0.80 |
|---|---|---|---|---|---|---|
| window-2 | 0.5 | 0.97 | 0.0091 | 0.0225 | 0.0337 | 0.0363 |
| window-3 | 0.5 | 1.44 | 0.0195 | 0.0349 | 0.0636 | 0.0704 |
| window-2 | 1 | 1.94 | 0.0386 | 0.0617 | 0.0992 | 0.1086 |
| window-3 | 1 | 2.88 | 0.0424 | 0.0824 | 0.1335 | 0.1342 |
| complete | 0.5 | 12.25 | 0.0400 | 0.0783 | 0.1216 | 0.1251 |
| complete | 1 | 24.50 | 0.0380 | 0.0836 | 0.1344 | 0.1317 |
<!-- END GENERATED TAB-005 -->

### 5.5 Expected versus observed

**Table 6.** Every pre-stated prediction and its verdict under the frozen rule. EXP-004 made no predictions.

| Experiment | Prediction (source) | Observation | Verdict under the frozen rule |
|---|---|---|---|
| EXP-001 | Checks C1 to C6 pass (EXP-001 protocol section 4) | All checks passed in all 5 runs | Verification passed (exploratory; licenses EXP-002) |
| EXP-002 | H1: at least one contrast non-zero (study protocol section 3) | 48 of 48 Holm-significant, all positive; 2 below the 0.01 practical threshold | H0 rejected for all 48; H1 supported |
| EXP-002 | Bayesian $\Delta \geq 0$ in every cell | All 24 Bayesian contrasts positive, smallest 0.0091 | Consistent; stopping rule not triggered |
| EXP-002 | Imitation and Bayesian identical under `complete` | 0 differing episodes in 8 cells of 10,000 | Confirmed (C4) |
| EXP-002 | Imitation $\Delta < 0$ in at least one `window-k` cell at low $q$ | Smallest imitation contrast +0.0059 [0.0048, 0.0070], Holm-significant | Contradicted |
| EXP-002 | Analytic anchor C1 at each $q$ | Analytic value inside the Wilson 99% interval of the observed share at all 4 $q$ | Passed |
| EXP-003 | H0 (robustness): every EXP-002 significant sign holds under V1, V2, V3 | 70 of 72 robust, 0 reversed, 2 lost significance | H1 of EXP-003 holds for 2 contrasts; both convention-dependent |
| EXP-003 | Analytic anchor C1 under V2 and V3 | Inside the 99% intervals | Passed |

## 6. Discussion

**What the evidence supports.** Within the model, observing predecessors raised mean accuracy against the independent baseline in every cell, for both an exact Bayesian rule and a naive counting rule, and the sign of that gain did not depend on the tie convention or on the horizon in any comparison. The mechanism is the one the cascade literature describes: early informative actions aggregate several signals, so agents who follow them are more often right than their own signal alone; but once the public lead reaches two, agents stop revealing their signals and the group stops learning. The analytic anchor ties the complete-network results to that mechanism exactly. Two qualifications apply to "in every cell": the gain is below the protocol's practical threshold of 0.01 in 2 of the 48 contrasts, and its magnitude depends strongly on the tie convention (Section 5.3).

**What the evidence does not show.** It does not show that observing others helps a given group, that naive inference is harmless in general, or that network structure rather than the quantity of observed information drives the differences between networks. Each of these would need a different estimand or design (Section 9).

**How groups become confidently wrong.** The average gain conceals a split outcome. At the lowest precision, about four in ten episodes end with the social group below what independent agents would have achieved on the same signals, and in those episodes most agents follow a wrong cascade for a long run. The positive mean says that social information is beneficial on average over many groups; it does not say that any given group benefits. A distributional estimand (for example, the probability that a group ends worse than independent agents) answers a different question from the preregistered one, and our numbers for it are exploratory.

**Competing explanations.** The protocol named four. (1) *Averaging over agents mixes early and late behaviour:* the last-agent gain is positive in every contrast, and horizons of 10 and 200 agents keep every sign and every significance, so the sign of the result does not come from the averaging. (2) *Tie conventions:* coin ties keep every sign but shrink every gain, by more than half in most contrasts; the magnitudes in Table 1 belong to the own-signal convention. (3) *Information quantity rather than structure:* within the window networks the gain follows the quantity of observed actions, but the complete network gains no more than window-3 with full visibility despite many more observed actions, consistent with cascades blocking further information; quantity and structure are confounded in this grid, so the data cannot separate them. (4) *Implementation error:* the analytic anchor, the zero-information case, the complete-network equivalence and the exact oracle all pass; the oracle covers $N \leq 9$ only, so a window-network error that appears only at larger $N$ cannot be excluded.

**The contradicted expectation.** We expected naive imitation to lose accuracy in some restricted network at low precision, following the idea that naive agents over-weight early movers. It did not, in any cell. Two features of our rule explain why this need not conflict with the theory: under the complete network it is action-equivalent to the Bayesian rule, and in recent-window networks each agent counts at most three actions, so the over-weighting it can produce is bounded. The exploratory comparison of the two rules shows small, visibility-dependent differences in both directions. The result says that this particular naive rule does not make social information harmful on average in this grid; it says nothing about other naive rules or about the richer setting of Eyster and Rabin (2010).

## 7. Limitations and threats to validity

- **Synthetic agents.** The agents follow stylised rules. Nothing here establishes real human rationality or irrationality, or behaviour on any platform or in any population.
- **Model scope.** Binary state, binary symmetric signals, one action per agent, homogeneous populations, common knowledge of rules, network and visibility pattern. Heterogeneous preferences, where confounded learning arises, are excluded.
- **Network family.** Only complete histories and recent windows of two or three predecessors; conclusions about "networks" are limited to these.
- **Imitation rule.** One simple naive rule.
- **Metric and convention dependence.** Episode accuracy averages over agents and depends on $N$; magnitudes depend strongly on the tie rule; two contrasts are convention-dependent under the frozen rule.
- **Partly tested robustness.** The confirmatory sensitivity analysis covered $q \in \{0.55, 0.70\}$; the extension to $q \in \{0.60, 0.80\}$ is exploratory.
- **Mean versus distribution.** The preregistered estimand is a mean; distributional results are exploratory.
- **Statistics.** p-values are tiny because samples are large; magnitudes carry the message. Intervals are unadjusted. No correction across experiments or variations was planned.
- **Verification coverage.** The exact oracle stops at $N \leq 9$; the analytic anchor covers only the complete network with full visibility.
- **Literature.** The review is non-systematic and abstract-level.
- **Reproducibility is not validity.** Exact reruns show computational reproducibility only.

## 8. Ethics and responsible research

The study uses synthetic data only; no personal data, human subjects or external datasets are involved, so no ethics approval was needed and none is claimed. The main misuse risk is over-reading: simulation results about stylised agents could be cited as evidence that real crowds are rational or irrational, or that social media "makes people wrong". They are not such evidence. Any extension to human subjects would require an owner-approved ethics review and appropriate safeguards.

## 9. Conclusion and future work

In a stylised model of sequential binary decisions, using social information raised mean decision accuracy over independent decisions in all 24 cells tested, for both exact Bayesian learners and naive vote counters, and the sign of the gain survived changes of tie rule and horizon. The size of the gain depends strongly on the tie convention (from 0.0059 to 0.1439 under own-signal ties, from 0.0036 to 0.0494 under coin ties in the confirmatory sensitivity grid), two low-precision contrasts are not established under coin ties, and in many episodes the social group locks onto the wrong action and ends below independent agents. Feasible extensions, each requiring a new frozen protocol: a preregistered distributional estimand; a planned paired comparison of naive and Bayesian rules in restricted networks; stronger over-weighting rules and heterogeneous populations; and exact oracle checks at larger $N$.

## 10. Data and code availability

All code, configurations, frozen protocols, raw per-episode outputs (confirmatory runs), result files, run manifests, generated reports and figures are in this repository (public URL: to be added after the owner approves publication). Environment: `uv sync --frozen` from `uv.lock` (Python 3.12.1, numpy 2.3.4). Reproduction: `PYTHONPATH=src .venv/bin/python -m herd.cli run --config experiments/EXP-002.json` (and `EXP-003.json`, `EXP-004-R001.json`), then `herd.cli report --run <run folder>`; derived analyses `python -m herd.exploratory`; manuscript tables `python -m herd.paper fill`. Every number in this manuscript is mapped to its source in `research/publication/artifact_manifest.json`.

## 11. Funding, competing interests and AI assistance

No funding was received. The author declares no competing interests. An AI system (Claude, Anthropic) was used as a research and development assistant: it wrote code, tests, configurations, experiment reports and drafts of this manuscript under the author's direction. The owner approved the protocol freezes, the amendments and every decision listed in `research/decision_log.md`. Every number was generated by the committed code from committed results and checked by an automated trace against the result files (`research/publication/evidence_audit.md`). AI review is internal quality control, not peer review. The author reviews the final text before any publication.

## References

All entries were verified at the level of bibliographic metadata and abstract (accessed 2026-11-24 unless stated). Full texts read on 2026-11-25: Bikhchandani, Hirshleifer and Welch (published version); Acemoglu et al., Celen and Kariv, Eyster and Rabin and Weizsacker (working-paper versions, listed in `research/publication/evidence_audit.md`). The others: abstract only.

- Acemoglu, D., Dahleh, M. A., Lobel, I. and Ozdaglar, A. (2011). Bayesian learning in social networks. *Review of Economic Studies*, 78(4), 1201-1236. https://doi.org/10.1093/restud/rdr004
- Anderson, L. R. and Holt, C. A. (1997). Information cascades in the laboratory. *American Economic Review*, 87(5), 847-862. https://ideas.repec.org/a/aea/aecrev/v87y1997i5p847-62.html
- Banerjee, A. V. (1992). A simple model of herd behavior. *Quarterly Journal of Economics*, 107(3), 797-817. https://doi.org/10.2307/2118364
- Bikhchandani, S., Hirshleifer, D. and Welch, I. (1992). A theory of fads, fashion, custom, and cultural change as informational cascades. *Journal of Political Economy*, 100(5), 992-1026. https://doi.org/10.1086/261849 (title checked against the Crossref record on 2026-11-25)
- Celen, B. and Kariv, S. (2004). Observational learning under imperfect information. *Games and Economic Behavior*, 47(1), 72-86. https://ideas.repec.org/a/eee/gamebe/v47y2004i1p72-86.html (content checked against the authors' working-paper version)
- Eyster, E. and Rabin, M. (2010). Naive herding in rich-information settings. *American Economic Journal: Microeconomics*, 2(4), 221-243. https://doi.org/10.1257/mic.2.4.221
- Golub, B. and Jackson, M. O. (2010). Naive learning in social networks and the wisdom of crowds. *American Economic Journal: Microeconomics*, 2(1), 112-149. https://doi.org/10.1257/mic.2.1.112
- Smith, L. and Sorensen, P. (2000). Pathological outcomes of observational learning. *Econometrica*, 68(2), 371-398. https://ideas.repec.org/a/ecm/emetrp/v68y2000i2p371-398.html
- Weizsacker, G. (2008). Do we follow others when we should? A simple test of rational expectations. Working paper, ESRC Centre for Economic Learning and Social Evolution, University College London. https://researchonline.lse.ac.uk/id/eprint/4945

## Supplementary appendix

`research/paper/supplementary.md`: the complete experimental matrix, the full EXP-002 contrast table (TAB-S01) and secondary metrics (TAB-S04), the full robustness tables of EXP-003 (TAB-S02) and EXP-004 (TAB-S03), configurations and hashes, deviations and owner decisions, and links to every experiment report.
