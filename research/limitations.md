<!-- SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0 -->
# Limitations (living document)

Status at M0: anticipated limitations of the design. Items 8 to 11 were added at M3 (2026-11-25), after the confirmatory runs EXP-002-R001 and EXP-003-R001. Items 9 to 11 were updated and items 12 to 15 added at M4 (2026-11-25).

1. **Synthetic agents only.** The agents follow stylised rules. Results do not establish real human irrationality or rationality, and say nothing about any real platform or population.
2. **Model scope.** Binary state, binary symmetric signals, a single action per agent, homogeneous populations within an arm, and common knowledge of rules and network for the Bayesian agents. Heterogeneous preferences (where confounded learning can arise) are excluded.
3. **Network family.** Only the complete history and recent-window networks are studied, because exact Bayesian inference is tractable there. General random graphs are excluded; conclusions about "networks" are limited to these structures.
4. **Imitation rule.** Naive vote counting is one simple heuristic among many; other imitation rules can behave differently, as the degenerate pure-copy rule shows.
5. **Metric choice.** Episode accuracy averages over agents and depends on the horizon $N$; this is probed by EXP-003 but not eliminated.
6. **Literature base.** The M0 review is non-systematic and relies largely on abstracts.
7. **Reproducibility versus validity.** Exact reruns demonstrate computational reproducibility, not real-world validity.
8. **Tie convention matters for magnitude.** Coin-flip ties shrank every social-learning gain in the EXP-003 grid (by more than half in 16 of 24 contrasts) and removed Holm significance at $q = 0.55$, window-3, $v = 1$ (EXP-003). The EXP-002 magnitudes are specific to the own-signal tie rule.
9. **Robustness only partly tested.** EXP-003 covers $q \in \{0.55, 0.70\}$; the robustness of the 24 EXP-002 contrasts at $q \in \{0.60, 0.80\}$ is untested by a confirmatory analysis. M4 update: the exploratory, post-hoc run EXP-004-R001 found all 72 comparisons at these $q$ robust (CLM-010); this does not make them confirmatory.
10. **Mean versus distribution.** The primary estimand is a mean paired difference. Episode accuracy is bimodal under social learning, and wrong cascades are frequent (up to 0.87 of episodes in EXP-002), so a positive mean does not say that every group gains. No distributional estimand was preregistered. M4 update: exploratory analysis puts the share of episodes in which the social group ends below the baseline at 0.050 to 0.425 (CLM-011).
11. **Imitation versus Bayesian not tested.** Differences between the two social rules in the window networks (EXP-002) are exploratory; no planned test compares them directly. M4 update: exploratory paired intervals are in CLM-013 (no multiplicity control).
12. **Practical size.** Two Holm-significant EXP-002 contrasts (+0.0059 and +0.0091, $q = 0.55$, window-2, $v = 0.5$) are below the 0.01 effect the protocol calls the smallest practically meaningful (CLM-014); under coin ties 5 of 48 contrasts are below it.
13. **Unverified literature detail.** The protocols attribute coin-flip tie-breaking to BHW1992; this was not checked against the full text (publisher page inaccessible). The frozen protocols are not edited; reports and manuscript do not rely on the attribution.
14. **Verification coverage of the window code.** The exact oracle covers $N \leq 9$ and the analytic anchor only the complete network with $v = 1$; a window-network error that appears only at larger $N$ cannot be excluded, and it would move both social rules together.
15. **Quantity versus structure not separable.** In this grid the window networks have both less and differently placed information than the complete network; the design cannot attribute network differences to structure (EXP-004 Q4, CLM-015).
