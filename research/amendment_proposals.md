<!-- SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0 -->
# Proposed amendments to the draft protocol (for the owner, before the freeze)

**Status: proposals only (2026-11-24, M2 session).** None of these has been applied to `research/protocol.md` or to the per-experiment protocols. Adopting, changing or rejecting them is the owner's decision at the freeze (G-FREEZE). Each proposal cites the exploratory evidence or the test that motivated it. Exploratory numbers are planning measurements, not findings.

## P-1: the `window-1` network is degenerate under binary signals and own-signal ties

- **Observation.** With binary signals of accuracy $q$ and ties resolved by the own signal, every `window-1` agent faces a tie whenever its signal disagrees with the observed action: the predecessor's action has accuracy exactly $q$ (by induction from agent 1), so its likelihood ratio equals that of the own signal. Bayesian and imitation agents therefore both act on their own signal, and their actions equal the independent baseline on every episode. $\Delta \equiv 0$ exactly in all 8 `window-1` cells (16 of the 48 primary contrasts have zero variance).
- **Evidence.** Unit tests `tests/test_reference.py::test_window1_is_degenerate_under_own_signal_ties` and `tests/test_likelihood.py::test_window1_predecessor_likelihood_is_q`; exact enumeration agrees (`test_engine_matches_exact_enumeration`); exploratory run EXP-001-R002 (all 16 `window-1` contrasts degenerate). Under coin ties (EXP-003 V1) the actions differ from the baseline, but the expected difference is zero by the same symmetry.
- **Proposal.** Replace `window-1` by `window-2` in EXP-002 and EXP-003 (non-degenerate: no zero-variance contrast in EXP-001-R004, cost similar to `window-1`), or keep `window-1` only as a labelled analytic null control outside the Holm family. In either case, change the fallback in `research/feasibility.md` section 8 ("reduce the network factor to {complete, window-1}") to {complete, window-2}, since the current fallback would leave a single informative network.

## P-2: the complete-network equivalence holds only for $q > 1/2$

- **Observation.** The structural prediction (protocol section 2; EXP-001 check 4) says that Bayesian and imitation actions coincide under `complete`. At $q = 1/2$ it fails: every Bayesian comparison is a tie (posterior 1/2), so Bayesian agents follow their signal, while imitators still count observed actions and herd. The EXP-001 smoke matrix includes $q = 0.5$ with `complete`, so check 4 as written would fail there.
- **Evidence.** First integration test of the M2 session (69 of 80 test episodes differed at $q = 0.5$); `tests/test_reference.py::test_complete_network_equivalence_does_not_hold_at_zero_information`. For $q > 1/2$ the equivalence held on every episode of every exploratory run (C4) and in the exact enumeration tests.
- **Proposal.** State the prediction and check 4 for $q > 1/2$ only. The runner already applies it only for $q > 1/2$.

## P-3: the analytic anchor is defined only for $q > 1/2$

- **Observation.** The formula $(1-q)^2/(q^2+(1-q)^2)\,(1-(2q(1-q))^m)$ gives 1/4 at $q = 1/2$ for large $N$, but no cascade forms at $q = 1/2$ (all ties).
- **Evidence.** The exact enumeration matches the formula as an exact rational identity for $q \in \{11/20, 3/5, 7/10, 4/5\}$ and $N = 1..8$ (`test_analytic_anchor_exact`), and the function refuses $q = 1/2$.
- **Proposal.** Restrict EXP-001 check 1 explicitly to $q \in \{0.6, 0.8\}$ in the smoke matrix.

## P-4: zero-variance contrasts and the multiplicity family

- **Observation.** A structurally degenerate contrast (all paired differences exactly 0) has no t statistic. The implementation reports it as an exact zero with $p = 1$ and keeps it in the Holm family, which makes Holm slightly more conservative for the other contrasts.
- **Proposal.** Decide at the freeze whether structurally degenerate contrasts are excluded from the Holm family and reported as exact comparisons (master prompt section 11.3, item 8). If P-1 is adopted, no degenerate contrast is expected in EXP-002.

## P-5: "Holm-adjusted 95% confidence interval"

- **Observation.** The study protocol (section 3) mentions Holm-adjusted intervals. Holm's procedure adjusts p-values; it does not define simultaneous intervals directly. The implementation reports unadjusted normal 95% intervals, the bootstrap check, raw and Holm-adjusted p-values.
- **Proposal.** Either state that the decision rule uses Holm-adjusted p-values with unadjusted 95% intervals for magnitude, or add Bonferroni-adjusted intervals (95% simultaneous over the family) as the conservative interval. The runner can add the second option in a few lines once the owner chooses.

## P-6: sample size and compute budget (planning values confirmed)

- **Observation (exploratory, EXP-001-R002 and R003).** The largest episode-level paired SD among non-degenerate contrasts was 0.458 (R002, EXP-002 shape) and 0.484 (R003, EXP-003 shape), below the planning value of 0.5; at 10,000 episodes this implies a 95% half-width of at most about 0.009 to 0.0095, consistent with the planned 0.01. The ratio of the observed between-seed SD of per-seed means to the SD expected from independent episodes had median 0.98 (R002) and 1.05 (R003). Projected runtime of the full EXP-002 matrix is about 0.5 minute of simulation plus about 0.3 minute of analysis on the audited machine (five times R002), and about 1.7 minutes for EXP-003 (five times R003).
- **Proposal.** Keep 10 seeds of 1,000 episodes per cell. The four-hour contingency in EXP-002 section 8 (reduce to 5 seeds) is not needed; the owner may instead consider more episodes, but the planned precision already meets the stated target.
