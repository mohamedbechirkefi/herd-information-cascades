<!-- SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0 -->
# EXP-001 report: smoke matrix and engine verification (EXPLORATORY)

**EXPLORATORY EXPERIMENT. Its numbers are never evidence for any study hypothesis.**

## 1. Identification

- **Experiment:** EXP-001 (exploratory by design). **Runs:** EXP-001-R001 to R004 (M2, 2026-11-24, before the freeze) and EXP-001-R005 (M3, 2026-11-25, pre-confirmatory smoke run).
- **Report version:** 1.0, 2026-11-25. **Status:** complete; all verification checks passed in all five runs.
- **Authorship:** Mohamed Bechir Kefi, independent researcher. An AI system was used as a research and development assistant and is not an author.
- **Protocol:** `research/experiments/EXP-001/protocol.md` v1.0 (exploratory), SHA-256 `f40252ceb8e3a7106df06a144da117aad44a730ac6057e4d0477659dbb1987ff`.
- **Code revisions:** R001 to R004 at `f15c0c24f83fa84cf7707602660509573ba30b2b`; R005 at `eded9b82ff9a7b64471ae6e66d127cbc83a9b5e3` (the frozen tree, clean).

## 2. Executive summary

- **Question.** Does the engine reproduce known analytic quantities and structural properties, produce schema-valid outputs, and run fast enough for the EXP-002 budget?
- **Method.** The smoke matrix of the study protocol section 7 (three rules, $q \in \{0.5, 0.6, 0.8\}$, {complete, window-1}, $v = 1$, $N = 20$, 2 seeds $\times$ 200 episodes) with checks C1 to C6, plus three throughput and seed-spread probes on the EXP-002 and EXP-003 matrix shapes at one fifth of the episodes (R002 to R004, seeds 100 to 109).
- **Outcome.** Every check passed in every run (R001 25/25, R002 61/61, R003 89/89, R004 17/17, R005 25/25). R001 to R004 motivated amendment A-1 (`window-1` degenerate) and confirmed the planning SD for A-5. R005 confirmed the frozen engine before the confirmatory runs.
- **Principal caveat.** Binomial checks at 400 episodes detect gross errors only. R001 used master seeds 0 and 1 (at $N = 20$ only, so no episode coincides with a confirmatory episode); its exploratory contrast values were seen before the freeze and are disclosed in `research/freeze.json` (C4).

## 3. Rationale and literature

The Bayesian `complete` model with own-signal ties is analytically tractable (BHW1992 setting): the public signal difference is a random walk absorbed at $\pm 2$, which gives exact targets for the simulator before any comparison is interpreted (`research/literature_review.md`).

## 4. Hypotheses (verification checks)

1. C1 analytic anchor ($q > 1/2$, Bayesian, complete, $v = 1$, own ties): the share of episodes with a wrong cascade by agent $N$ matches $\frac{(1-q)^2}{q^2 + (1-q)^2}(1 - (2q(1-q))^m)$, $m = \lfloor (N-1)/2 \rfloor$, within its Wilson 99% interval.
2. C2 zero information ($q = 1/2$): mean accuracy 1/2 for all rules; Bayesian posteriors exactly 1/2 and no Bayesian cascades.
3. C3 independent baseline: agent accuracy $q$ (Wilson 99%), no cascades.
4. C4 equivalence ($q > 1/2$, complete, own ties): Bayesian and imitation actions identical on every episode.
5. C5 schema validity; C6 no near ties in Bayesian comparisons.

A failed check would stop EXP-002.

## 5. Methodology

Model, rules and generator as in EXP-002 (`src/herd/`). Synthetic data only. Hardware: Apple M1 Pro, 16 GB, macOS 15.3.1; Python 3.12.1, numpy 2.3.4. Configurations `experiments/EXP-001-R00N.json` (N = 1 to 5). Seeds: R001 0 and 1; R002 to R004 100 to 109; R005 100 and 101 (disjoint from the confirmatory seeds 0 to 9).

## 6. Implementation verification

The checks are the experiment. In addition, the unit suite (278 tests at the frozen revision, 281 after this session) includes the exact rational oracle for $N \leq 9$, golden decision tables and known-case tests of every metric and statistic (episode metrics, Student t tails, Wilson interval, paired contrast and degenerate case, bootstrap, Holm). On 2026-11-25 the known-case subset (`tests/test_metrics_stats.py`, `tests/test_reference.py`) gave 132 passed.

## 7. Execution record

| Run | Config SHA-256 (prefix) | Revision | Started (UTC) | Wall-clock (s) | Checks | Failed cells |
|----------|--------------|--------|----------------|--------|------|------|
| EXP-001-R001 | 6bb119865235b1f0 | f15c0c24 | 2026-11-24T16:06:49Z | 0.07 | 25/25 | 0 |
| EXP-001-R002 | e18b052ab500b99a | f15c0c24 | 2026-11-24T16:06:53Z | 9.81 | 61/61 | 0 |
| EXP-001-R003 | 0f01eecc86cd6251 | f15c0c24 | 2026-11-24T16:07:04Z | 22.34 | 89/89 | 0 |
| EXP-001-R004 | 7e64cd6f93ffe4db | f15c0c24 | 2026-11-24T16:07:27Z | 3.26 | 17/17 | 0 |
| EXP-001-R005 | 0c1bfeb60beb150c | eded9b82 | 2026-11-24T23:30:59Z | 0.05 | 25/25 | 0 |

Commands: `PYTHONPATH=src .venv/bin/python -m herd.cli run --config experiments/EXP-001-R00N.json` and `herd.cli report --run results/exploratory/EXP-001-R00N` (R001 also through `herd.cli smoke`). Journal entries J-0002 to J-0006 in `research/experiment_journal.jsonl`. No run failed or was dropped. Deviation: R005 is not named in the protocol; it repeats the smoke matrix on exploratory seeds, as the M3 brief requires before confirmatory runs.

## 8. Results

R005 (pre-confirmatory) check details: C1 at $q = 0.6$: 123/400 wrong-cascade episodes, Wilson 99% [0.2516, 0.3697]; at $q = 0.8$: 21/400, [0.0304, 0.0892]; both intervals contain the analytic value. C2: all rules within the 99% interval around 1/2; maximum $|$posterior $- 1/2| = 0$; no Bayesian cascade agent. C3: independent agent accuracy inside its Wilson 99% interval in all 6 cells, no cascade. C4: 0 of 400 episodes differ at $q = 0.6$ and $q = 0.8$. C5 valid. C6: no near ties. Throughput: 0.160 ms per 1,000 agent decisions. Full tables per run in `results/exploratory/EXP-001-R00N/report.md`.

The R001 to R004 findings that shaped the freeze: under `window-1`, both social rules reproduced the independent baseline exactly (16 degenerate contrasts in R002), which motivated A-1; the largest non-degenerate paired SD (0.4704 in R004) confirmed the planning SD of 0.5 used for A-5.

## 9. Interpretation

The engine reproduces the analytic anchor, the zero-information case, the independent baseline and the complete-network equivalence, and its outputs are schema-valid. These results license running EXP-002 and EXP-003; they are not evidence about H1.

## 10. Threats to validity

Small samples (400 episodes per arm in the smoke matrix) detect only gross errors; the C1 anchor covers only the `complete`, $v = 1$, own-tie setting; `window-k` correctness at $N > 9$ rests on the recursion's agreement with the oracle at small $N$.

## 11. Conclusion and next experiment

Verification passed; EXP-002 and EXP-003 were run on 2026-11-25 (their own reports).

## 12. Reproduction appendix

Environment: `../.tools/py/bin/uv sync --frozen --all-groups --all-extras`. Runs and reports: commands in Section 7. Results: `results/exploratory/EXP-001-R00N/` (result.json, run_manifest.json with SHA-256 of each output, tables, figures, report); raw arrays `results/raw/EXP-001-R00N/episodes.npz` are git-ignored and regenerable.
