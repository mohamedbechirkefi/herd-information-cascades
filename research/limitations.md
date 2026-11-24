<!-- SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0 -->
# Limitations (living document)

Status at M0: no experiment has been run, so these are anticipated limitations of the design, not observed ones.

1. **Synthetic agents only.** The agents follow stylised rules. Results do not establish real human irrationality or rationality, and say nothing about any real platform or population.
2. **Model scope.** Binary state, binary symmetric signals, a single action per agent, homogeneous populations within an arm, and common knowledge of rules and network for the Bayesian agents. Heterogeneous preferences (where confounded learning can arise) are excluded.
3. **Network family.** Only the complete history and recent-window networks are studied, because exact Bayesian inference is tractable there. General random graphs are excluded; conclusions about "networks" are limited to these structures.
4. **Imitation rule.** Naive vote counting is one simple heuristic among many; other imitation rules can behave differently, as the degenerate pure-copy rule shows.
5. **Metric choice.** Episode accuracy averages over agents and depends on the horizon $N$; this is probed by EXP-003 but not eliminated.
6. **Literature base.** The M0 review is non-systematic and relies largely on abstracts.
7. **Reproducibility versus validity.** Exact reruns demonstrate computational reproducibility, not real-world validity.
