<!-- SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0 -->
# tests/

pytest suite (M2). Run with `uv run --frozen pytest` or `PYTHONPATH=src uv run --frozen python -m herd.cli test`.

- `test_model.py`: input validation, deterministic seeding, common random numbers.
- `test_rules_golden.py`: hand-computed examples for the complete network, coin ties, window-3 imitation and the independent baseline.
- `test_likelihood.py`: public and private posteriors, hidden actions, window-1 likelihoods, the zero-information case, tie tolerance.
- `test_reference.py`: exhaustive differential tests against the exact rational oracle; analytic anchor as an exact identity; window-(N-1) equals complete; Bayesian agents individually at least as accurate as their signal; complete-network equivalence and its failure at q = 1/2; window-1 degeneracy.
- `test_properties.py`: invariants (cascade agents ignore their signal, determinism, metric bounds, zero visibility, state relabelling symmetry).
- `test_metrics_stats.py`: metric golden values, t distribution, Wilson, Holm, bootstrap, degenerate contrasts.
- `test_pipeline.py`: config to result to report, invalid configurations, the protocol-freeze gate, fail-closed result reading.
