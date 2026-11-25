<!-- SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0 -->
# EXP-004 report: post-hoc sensitivity and distributional checks (EXPLORATORY)

**EXPLORATORY AND POST HOC. Designed on 2026-11-25 after the confirmatory results were seen. It changes no frozen verdict, and none of its numbers is evidence for H1 of EXP-002 or EXP-003.**

## 1. Identification

- **Experiment:** EXP-004 (exploratory, M4). **Run:** EXP-004-R001 (new simulation, once, no rerun). **Derived analyses:** `results/exploratory/EXP-004-derived/` (no simulation; computed from committed EXP-002-R001 and EXP-003-R001 outputs).
- **Date:** 2026-11-25 (R001: 2026-11-25T01:19:46Z to 01:20:07Z UTC). Report version 1.0, 2026-11-25.
- **Status:** complete. R001 ran its full matrix: 0 failed cells, 89 of 89 verification checks passed.
- **Authorship:** Mohamed Bechir Kefi (no affiliation). An AI system was used as a research and development assistant and is not an author.
- **Protocol:** `research/experiments/EXP-004/protocol.md` v1.0 (exploratory, not frozen), SHA-256 `e14989310901286f06a108de2234224f7ce013fdf219e6d170e5044c873ca219`, committed at `3831429` before R001 ran.
- **Configuration:** `experiments/EXP-004-R001.json`, canonical SHA-256 `9269dee899844d0595693bf088efcdb7ddd179de3f3cbd202e905a585dcf0e66` (file SHA-256 `fd27019f78884c6aaf448df7e5ab83ea413828060de075b035e221b8926b0cc8`).
- **Code revisions:** R001 at `3831429e2589fbeec183b04e367f39bb78e98d2a` (clean tree; engine identical to the confirmatory revision `50fbdb1`, since only records and configs changed in between); derived analyses at `f2c91ff154bdaed9a444d81041e8c59d2060b725` (clean tree; adds `src/herd/exploratory.py`).

## 2. Executive summary

- **Questions.** Q1: does the EXP-003 robustness result extend to the EXP-002 cells at $q \in \{0.60, 0.80\}$ that EXP-003 did not cover? Q2: how often does a social rule end an episode below the independent baseline, and what is the last agent's paired gain? Q3: how large are the paired imitation-minus-Bayesian differences? Q4: does the gain order by the quantity of observed actions?
- **Method.** Q1: the EXP-003 design rerun on $q \in \{0.60, 0.80\}$ (seeds 0 to 9, so the episode draws match EXP-002), with the unchanged frozen rule of `src/herd/robustness.py`. Q2 to Q4: descriptive statistics on the committed per-episode arrays and estimates.
- **Outcome.** Q1: 72 of 72 comparisons robust (no sign reversal, no loss of Holm significance); coin ties again shrink every gain (V1 at 0.27 to 0.63 times the EXP-002 value; below half in 17 of 24). Q2: in EXP-002, a social rule ends below the baseline on the same episode in between 0.050 and 0.425 of episodes, depending on the cell; with full visibility this share equals the wrong-cascade probability to three decimals. The last agent's paired gain is positive in all 48 contrasts with 95% intervals that exclude zero (0.0067 to 0.1595). Q3: imitation is below Bayesian in all 8 half-visibility window cells (by 0.0032 to 0.0178), above it in 3 of 4 window-3 full-visibility cells (by 0.0052 to 0.0104; the fourth interval includes zero), and identical on every episode in the 4 window-2 full-visibility cells. Q4: among window cells the gain increases with the expected number of observed actions, but the complete network, with 4 to 9 times more observed actions than window-3 at full visibility, gives about the same gain.
- **Principal caveat.** Every comparison is post hoc and unadjusted; the intervals describe magnitude only.

## 3. Rationale and literature

EXP-003 left the robustness of half of the EXP-002 contrasts untested (EXP-003 report, section 9). The primary estimand of EXP-002 is a mean, and its report noted bimodal episode outcomes and an exploratory difference between the two social rules. The protocol named information quantity as a competing explanation for network differences (study protocol section 9). References: `research/literature_review.md` (BHW1992 and ER2010 abstracts only).

## 4. Hypotheses and operational definitions

No hypothesis is tested. Definitions:

- **Q1:** status per EXP-002 contrast and variation by the frozen EXP-003 rule (robust, lost significance, sign reversed); Holm within each variation over its 24 non-degenerate contrasts.
- **Q2:** share of episodes with $\mathrm{Acc}_r(e) < \mathrm{Acc}_{\mathrm{ind}}(e)$ (proportion of 10,000 paired episodes); last-agent paired difference $E[\mathbb{1}[a_N^r = \theta] - \mathbb{1}[a_N^{\mathrm{ind}} = \theta]]$ with a normal 95% interval.
- **Q3:** $E[\mathrm{Acc}_{\mathrm{imit}}(e) - \mathrm{Acc}_{\mathrm{bayes}}(e)]$ with a normal 95% interval, and the share of episodes in which the two episode accuracies differ.
- **Q4:** mean over agents $i = 1..N$ of the expected number of visible observed actions, $v(i-1)$ under `complete` and $v \min(k, i-1)$ under `window-k`.

## 5. Methodology

- **R001:** model, rules, statistics and hardware as in EXP-003 (Apple M1 Pro, 16 GB, macOS 15.3.1, Python 3.12.1, numpy 2.3.4; one process under `nice -n 10`). 12 cells ($q \in \{0.60, 0.80\}$ $\times$ 3 networks $\times$ 2 visibility levels) $\times$ 3 rules $\times$ 3 variations, 10,000 episodes per arm.
- **Derived analyses:** `src/herd/exploratory.py`, with tests on hand-built arrays (`tests/test_exploratory.py`, 4 tests). Inputs and their SHA-256 are listed in `results/exploratory/EXP-004-derived/summary.json`.
- **Budget:** R001 20.50 s wall-clock, peak resident memory 305 MB; derived analyses a few seconds. One worker.

## 6. Implementation verification

- R001 in-run checks, 89 of 89 passed: C1 analytic anchor under own ties (V2: 0.2999 and 0.0605 against 0.2914 and 0.0582; V3: 0.3010 and 0.0589 against 0.3077 and 0.0588; all inside Wilson 99% intervals), C3 (36 cells), C4 (8 cells), C5, C6 (36 cells), C7 diagnostic (0 of 10,000 episodes differ in each of the 4 V1 `complete` cells).
- The derived module was tested on hand-built arrays with known shares, differences and observation counts.

## 7. Execution record

- **Commands:**
  - `PYTHONPATH=src nice -n 10 .venv/bin/python -m herd.cli run --config experiments/EXP-004-R001.json`: "EXPLORATORY run EXP-004-R001: 108 arms, 72 contrasts, 89 checks (0 failed), 0 failed cells; runtime 20.50 s"; exit 0.
  - `PYTHONPATH=src .venv/bin/python -m herd.cli report --run results/exploratory/EXP-004-R001`
  - `PYTHONPATH=src .venv/bin/python -m herd.robustness --reference results/EXP-002/EXP-002-R001 --sensitivity results/exploratory/EXP-004-R001`: "72 comparisons: {'robust': 72}".
  - `PYTHONPATH=src .venv/bin/python -m herd.exploratory --out results/exploratory/EXP-004-derived`
- **Sample counts:** R001 108 arms $\times$ 10,000 episodes, 72 contrasts, 93,600,000 agent decisions. Derived: 48 EXP-002 contrasts and 72 EXP-003 contrasts (Q2), 24 EXP-002 cells and 36 EXP-003 cells (Q3), 48 EXP-002 contrasts (Q4). No failed or dropped run, no excluded episode.
- **Deviations:** none from this exploratory protocol. The raw arrays of R001 (`results/raw/EXP-004-R001/`) are git-ignored like all exploratory raw arrays and are regenerated by the command above.

## 8. Results

### 8.1 Q1: robustness at q = 0.60 and 0.80 (exploratory)

72 robust, 0 lost significance, 0 sign reversed. Largest Holm-adjusted p per variation: V1 $1.7 \times 10^{-6}$, V2 and V3 below $10^{-15}$. Positive in all 10 seeds: V1 19 of 24 contrasts (the other 5 in 9 seeds), V2 and V3 24 of 24. Full table: manuscript supplementary TAB-S03 and `results/exploratory/EXP-004-R001/tables/robustness_vs_EXP-002-R001.csv`; generated run report `results/exploratory/EXP-004-R001/report.md`.

### 8.2 Q2: distribution of paired outcomes (EXP-002, exploratory)

Manuscript TAB-003 and `results/exploratory/EXP-004-derived/q2_distribution.csv`. Share of episodes below the baseline: 0.050 (imitation, $q = 0.8$, window-3, $v = 1$) to 0.425 (Bayesian, $q = 0.55$, window-3, $v = 0.5$). At $q = 0.55$ it is between 0.371 and 0.425 in every cell. Last-agent paired gain: 0.0067 [0.0012, 0.0122] (imitation, $q = 0.55$, window-2, $v = 0.5$) to 0.1595 [0.1482, 0.1708] (imitation, $q = 0.7$, window-3, $v = 1$); 48 of 48 intervals exclude zero.

### 8.3 Q3: imitation minus Bayesian (EXP-002, exploratory)

Manuscript TAB-004 and `q3_imitation_minus_bayesian.csv`. Complete network: identical on every episode (as C4). Window-2, $v = 1$: identical on every episode in all 4 cells (not predicted by the protocol). Half visibility: imitation lower in all 8 window cells, from $-0.0032$ [$-0.0050$, $-0.0014$] to $-0.0178$ [$-0.0200$, $-0.0156$]. Window-3, $v = 1$: imitation higher at $q = 0.6$, 0.7 and 0.8 (0.0083, 0.0104, 0.0052, intervals excluding zero) and 0.0024 [$-0.0020$, 0.0068] at $q = 0.55$. 11 of the 24 EXP-002 cells have intervals that exclude zero.

### 8.4 Q4: observation quantity (EXP-002 estimates, exploratory)

Manuscript TAB-005 and `q4_quantity.csv`. Mean expected observed actions per agent: window-2 $v = 0.5$ 0.97, window-3 $v = 0.5$ 1.44, window-2 $v = 1$ 1.94, window-3 $v = 1$ 2.88, complete $v = 0.5$ 12.25, complete $v = 1$ 24.50. Within these four window cells, the Bayesian gain increases with the quantity at every $q$. From window-3 $v = 1$ to complete $v = 1$ the quantity rises about 8.5 times while the gain changes by less than 0.005 (for example $q = 0.7$: 0.1335 and 0.1344).

### 8.5 Runtime

R001: 20.50 s (simulation 13.61 s, 0.145 ms per 1,000 agent decisions), peak resident memory 305,086,464 bytes.

## 9. Interpretation

- **Q1.** The pattern of EXP-003 extends to the higher signal qualities: signs and Holm significance hold under all three variations, and coin ties shrink every gain. The set of contrasts that the frozen rule classifies as convention-dependent stays the two found by EXP-003. This does not alter any frozen verdict: the EXP-003 verdict is the confirmatory one, and this run is exploratory.
- **Q2.** The positive mean gain coexists with a large minority of episodes in which the group does worse than independent agents would on the same signals: about 4 in 10 episodes at $q = 0.55$. With full visibility these are exactly the wrong-cascade episodes. The gain is therefore a statement about averages over episodes, not about every group. The last-agent result answers the protocol's first confounder: the sign of the gain does not come from averaging early, pre-cascade agents with late ones.
- **Q3.** The direction of the difference between the two social rules depends on visibility in the window networks. Under partial visibility the naive rule loses a little against the Bayesian rule, which fits the idea that treating observed actions as independent is costly when the observer cannot tell how much of the history was hidden; under full window-3 visibility the naive rule gains a little, which shows that the individually optimal rule is not necessarily the group-optimal one. These are post-hoc observations without multiplicity control.
- **Q4.** Observation quantity explains the ordering among window cells but not the complete-network results: beyond about three observed actions, more observation does not raise the gain, which is consistent with the cascade mechanism (once a cascade starts, further actions carry no new information). Quantity and structure are confounded in this grid (the window cells have both less and differently placed information), so the data cannot separate them.

## 10. Threats to validity

- **Statistical:** post hoc, many unadjusted comparisons; selection of questions after seeing results (each question reports every cell, so no cell was selected).
- **Construct:** "below baseline" compares two episode accuracies on the same signals; it is a paired, per-episode notion and not a probability that a real group is harmed. The quantity measure is an expectation, not the realised number of observed actions.
- **Internal:** as EXP-003; the window recursion is verified against the rational oracle only for $N \leq 9$.
- **External:** synthetic homogeneous agents only.

## 11. Conclusion and next experiment

Exploratory evidence supports reading the EXP-002 result as "higher mean accuracy with frequent group-level losses", robust in sign to the tie and horizon conventions across all four signal qualities, with sizes that depend strongly on the tie rule. A new preregistered experiment could test a distributional estimand (share of episodes below baseline) and the paired imitation-versus-Bayesian difference.

## 12. Reproduction appendix

- Environment: `../.tools/py/bin/uv sync --frozen --all-groups --all-extras`; tests `.venv/bin/python -m pytest`.
- Commands: Section 7 (R001 needs a fresh output folder; the derived command refuses an existing `summary.json`).
- Outputs: `results/exploratory/EXP-004-R001/` (`result.json`, `run_manifest.json`, tables, figures, generated report); `results/exploratory/EXP-004-derived/` (`q2_distribution.csv`, `q3_imitation_minus_bayesian.csv`, `q4_quantity.csv`, `summary.json` with input and output SHA-256).
- Tolerance: deterministic for a given numpy version; timing fields differ.
