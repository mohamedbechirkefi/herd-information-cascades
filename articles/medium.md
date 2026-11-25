<!-- SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0 -->
<!-- Draft for Medium (M5, 2026-11-25). Not published; publication is the owner's decision. Every number is copied from research/paper/manuscript.md v1.0, whose numbers are traced to committed results (research/publication/number_trace.csv). -->

# Higher average accuracy, frequent locked-in errors: what a simulation says about following the crowd

*Draft. A simulation study with synthetic agents; nothing here is a finding about real people. Not peer-reviewed.*

Imagine a queue of people, each deciding between two options. Each has a private hint that is right a little more often than not, and each can see what some of the people before them chose. Should they follow the crowd or their own hint?

Following others can help: an early choice carries information about the hint behind it. It can also stop learning altogether. Once the visible lead in favour of one option outweighs any single hint, everyone after that point follows the crowd whatever their own hint says, so their choices reveal nothing new, and the crowd can settle on the wrong answer. Economists call this an informational cascade (Bikhchandani, Hirshleifer and Welch, 1992; Banerjee, 1992).

## The question

When does social information improve binary decisions, and when does it generate cascades of errors? I studied this inside a fully specified simulation, not with people.

## What was simulated

- A hidden state, 0 or 1, equally likely. Each agent receives a private binary signal that matches the state with probability $q$ (the signal precision).
- Agents act once, in order. Each action is publicly visible with probability $v$. An agent sees either the complete history or only the last two or three predecessors.
- Three kinds of agents: **independent** agents who follow their own signal (the baseline), **Bayesian** agents who compute the exact posterior from what they see, and **imitators** who count each observed action as one independent signal (a simple naive rule).
- Every rule faced the same hidden states, signals and visibility patterns, so each comparison is paired on identical episodes.

The confirmatory study (EXP-002) crossed four signal precisions, three networks and two visibility levels: 48 contrasts, each with 10,000 paired episodes of 50 agents. Its protocol, including the analysis, was frozen before the run, and the run was made once.

## Visual explanation

The interactive page in `demo/` replays a single episode agent by agent: the private signal, the social agent's action and what an independent agent would have done. In the episode shown with the sandbox's default settings (seed 1), two early wrong signals push the visible lead to two and every later Bayesian agent follows the wrong action, even those holding the right signal. The page also shows, for every cell of the study, the distribution of episode accuracy: under social learning it is split between groups that end mostly right and groups that end mostly wrong. Demo link: to be added after the owner approves publication.

*Figure (`docs/demo.png`): the sandbox after a run, showing one episode agent by agent above the accuracy distribution of the run. Alt text: a row of agents in which, after two wrong early signals, every Bayesian agent's action is wrong, above two histograms in which the independent group is spread around one half and the Bayesian group is concentrated at zero and at one. Sandbox output, not a research result.*

## What was measured

**Social information raised mean accuracy in every cell tested.** All 48 contrasts were positive and Holm-significant, from +0.0059 (95% CI 0.0048 to 0.0070) to +0.1439 (0.1375 to 0.1504) on the proportion scale, where 0.01 is one accuracy point. Two of the 48 were below the protocol's practical threshold of 0.01.

**A prediction failed.** I expected the naive imitation rule to lower accuracy in some restricted network at low precision. It did not, in any cell: the smallest imitation contrast was +0.0059 [0.0048, 0.0070]. This says that this particular naive rule did not make social information harmful on average in this grid, not that naive inference is harmless in general.

**The same rules often locked groups into errors.** Wrong cascades occurred in 0.408 of episodes for both social rules at $q = 0.55$ with the complete history and full visibility, and in up to 0.868 of episodes for imitation at $q = 0.55$, window-3, $v = 0.5$. In an exploratory analysis, the social group ended below independent agents on the same signals in between 0.050 and 0.425 of episodes.

**The size of the gain depends on a modelling convention.** A frozen sensitivity analysis (EXP-003) changed how agents break exact ties. Under coin-flip ties no gain changed sign, but every gain shrank (to 0.0036 to 0.0494), and two low-precision contrasts lost significance (Bayesian 0.0082, 95% CI -0.0013 to 0.0176; imitation 0.0079, -0.0015 to 0.0174). By the rule fixed in advance, those two conclusions are convention-dependent.

The positive mean is a statement about many groups on average. It does not say that any given group benefits from watching the others.

## Limitations

- The agents are stylised rules. Nothing here establishes real human rationality or irrationality.
- Binary states and signals, one action per agent, homogeneous populations and only two kinds of network were studied.
- One simple imitation rule was tested; others can behave differently.
- The magnitudes depend strongly on the tie convention, and the distributional results are exploratory.
- Exact reruns show computational reproducibility, not real-world validity.

The full list is in `research/limitations.md`.

## Reproducibility

Code, frozen protocols, configurations, raw per-episode outputs, run manifests, per-experiment reports and the manuscript are in the repository, with a trace from every manuscript number to its source. Repository link: to be added after the owner approves publication.

An AI system (Claude, Anthropic) was used as a research and development assistant: it wrote code, tests, reports and drafts under my direction. It is not an author.
