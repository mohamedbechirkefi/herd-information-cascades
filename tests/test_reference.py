# SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
"""Differential tests against exact rational enumeration, and the analytic cascade anchor."""
from fractions import Fraction

import numpy as np
import pytest

from herd.generate import generate_episodes
from herd.model import Cell, ModelError
from herd.reference import ExactModel, analytic_no_cascade_probability, analytic_wrong_cascade_probability
from herd.rules import bayesian_window, run_rule

from conftest import exhaustive_episodes

VIS_PATTERNS = [(1, 1, 1, 1, 1), (1, 0, 1, 1, 0), (0, 1, 1, 0, 1), (0, 0, 0, 0, 0)]


@pytest.mark.parametrize("network", ["complete", "window-1", "window-2", "window-3"])
@pytest.mark.parametrize("tie_rule", ["own", "coin"])
@pytest.mark.parametrize("rule", ["bayesian", "imitation", "independent"])
@pytest.mark.parametrize("q", [Fraction(3, 5), Fraction(11, 20), Fraction(4, 5)])
def test_engine_matches_exact_enumeration(network, tie_rule, rule, q):
    for vis in VIS_PATTERNS:
        n = len(vis)
        ep = exhaustive_episodes(n, vis, with_coins=(tie_rule == "coin"))
        out = run_rule(rule, ep, Cell(float(q), network, 1.0, n, tie_rule))
        ref = ExactModel(q, network, tuple(bool(x) for x in vis), tie_rule, rule)
        for e in range(ep.n_episodes):
            actions, flags = ref.play(tuple(int(x) for x in ep.signals[e]), tuple(int(x) for x in ep.coins[e]))
            assert tuple(out.actions[e]) == actions, (vis, e)
            assert tuple(out.cascade[e]) == flags, (vis, e)


@pytest.mark.parametrize("q", [Fraction(11, 20), Fraction(3, 5), Fraction(7, 10), Fraction(4, 5)])
@pytest.mark.parametrize("n", [1, 2, 3, 4, 5, 6, 7, 8])
def test_analytic_anchor_exact(q, n):
    ref = ExactModel(q, "complete", (True,) * n)
    p = ref.expectation(lambda th, s, a, f: int(any(fl and ai != th for fl, ai in zip(f, a))))
    assert p == analytic_wrong_cascade_probability(q, n)


@pytest.mark.parametrize("q", [Fraction(3, 5), Fraction(4, 5)])
def test_no_cascade_probability_exact(q):
    for m in range(0, 4):
        n = 2 * m + 1  # agent 2m+1 is the first that can be in a cascade
        ref = ExactModel(q, "complete", (True,) * n)
        p = ref.expectation(lambda th, s, a, f: int(not f[-1]))
        assert p == analytic_no_cascade_probability(q, m)


def test_analytic_anchor_rejects_zero_information():
    with pytest.raises(ModelError):
        analytic_wrong_cascade_probability(Fraction(1, 2), 10)


@pytest.mark.parametrize("v", [1.0, 0.5])
@pytest.mark.parametrize("tie_rule", ["own", "coin"])
def test_window_recursion_with_full_window_equals_complete(v, tie_rule):
    # window-(N-1) observes every predecessor: the generic recursion must equal the public-belief recursion.
    n = 8
    cell = Cell(0.6, "complete", v, n, tie_rule)
    ep = generate_episodes(cell, 2, 400)
    a = run_rule("bayesian", ep, cell)
    b = bayesian_window(ep, Cell(0.6, f"window-{n - 1}", v, n, tie_rule), n - 1)
    assert np.array_equal(a.actions, b.actions)
    assert np.array_equal(a.cascade, b.cascade)
    assert np.allclose(a.posterior, b.posterior)


@pytest.mark.parametrize("q", [Fraction(11, 20), Fraction(4, 5)])
@pytest.mark.parametrize("network", ["complete", "window-2", "window-3"])
def test_bayesian_agents_individually_at_least_as_accurate_as_signals(q, network):
    # Invariant: each Bayesian agent maximises its own expected accuracy, so P(a_i = theta) >= q.
    n = 6
    ref = ExactModel(q, network, (True,) * n)
    for i in range(n):
        acc = ref.expectation(lambda th, s, a, f, i=i: int(a[i] == th))
        assert acc >= q


def test_complete_network_equivalence_bayesian_imitation_own_ties():
    for v in (1.0, 0.5, 0.2):
        for q in (0.55, 0.8):
            cell = Cell(q, "complete", v, 50)
            ep = generate_episodes(cell, 4, 500)
            assert np.array_equal(run_rule("bayesian", ep, cell).actions, run_rule("imitation", ep, cell).actions)


@pytest.mark.parametrize("v", [1.0, 0.5])
@pytest.mark.parametrize("q", [0.55, 0.7])
def test_window1_is_degenerate_under_own_signal_ties(v, q):
    # Finding recorded for the owner: with binary signals and own-signal ties, every window-1
    # comparison is a tie, so Bayesian and imitation agents both act on their own signal.
    cell = Cell(q, "window-1", v, 50)
    ep = generate_episodes(cell, 9, 500)
    for rule in ("bayesian", "imitation"):
        out = run_rule(rule, ep, cell)
        assert np.array_equal(out.actions, ep.signals)
        assert not out.cascade.any()


def test_exact_model_rejects_large_or_invalid_inputs():
    with pytest.raises(ModelError):
        ExactModel(Fraction(3, 5), "complete", (True,) * 12)
    with pytest.raises(ModelError):
        ExactModel(0.6, "complete", (True,) * 3)
    with pytest.raises(ModelError):
        ExactModel(Fraction(3, 5), "complete", (True,) * 3, tie_rule="x")


def test_complete_network_equivalence_does_not_hold_at_zero_information():
    # At q = 1/2 Bayesian agents always tie and follow their signal; imitators still herd.
    cell = Cell(0.5, "complete", 1.0, 20)
    ep = generate_episodes(cell, 4, 200)
    assert np.array_equal(run_rule("bayesian", ep, cell).actions, ep.signals)
    assert run_rule("imitation", ep, cell).cascade.any()
