# SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
"""Likelihood and posterior calculations, including the zero-information case."""
import numpy as np
import pytest

from herd.generate import generate_episodes
from herd.model import Cell
from herd.rules import TIE, compare, run_rule

from conftest import make_episodes


def test_public_posterior_complete_network():
    q = 0.6
    out = run_rule("bayesian", make_episodes(1, [1, 1, 1, 1]), Cell(q, "complete", 1.0, 4))
    pp = out.extra["public_posterior"][0]
    assert pp[0] == pytest.approx(0.5)
    assert pp[1] == pytest.approx(q)                                   # one revealed signal
    assert pp[2] == pytest.approx(q * q / (q * q + (1 - q) ** 2))     # two revealed signals = 0.6923...
    assert pp[3] == pytest.approx(pp[2])                               # a cascade action reveals nothing


def test_agent_posteriors_complete_network():
    q = 0.6
    out = run_rule("bayesian", make_episodes(1, [1, 0, 0]), Cell(q, "complete", 1.0, 3))
    post = out.posterior[0]
    assert post[0].tolist() == pytest.approx([1 - q, q])       # no history: posterior = signal likelihood
    assert post[1, 0] == pytest.approx(0.5)                     # one action against one signal: a tie
    assert post[1, 1] == pytest.approx(q * q / (q * q + (1 - q) ** 2))


def test_hidden_actions_carry_no_information():
    out = run_rule("bayesian", make_episodes(1, [1, 1, 0], [[0, 0, 1]]), Cell(0.7, "complete", 0.5, 3))
    assert out.extra["public_posterior"][0].tolist() == pytest.approx([0.5, 0.5, 0.5])


@pytest.mark.parametrize("tie_rule", ["own", "coin"])
def test_window1_predecessor_likelihood_is_q(tie_rule):
    # Under window-1 every predecessor action has accuracy q (by induction), so an agent
    # with a signal agreeing with the observed action has posterior q^2 / (q^2 + (1-q)^2)
    # and a disagreeing one has posterior exactly 1/2.
    q = 0.7
    ep = generate_episodes(Cell(q, "window-1", 1.0, 30, tie_rule), 5, 200)
    out = run_rule("bayesian", ep, Cell(q, "window-1", 1.0, 30, tie_rule))
    prev = out.actions[:, :-1]
    post = out.posterior[:, 1:, :]
    agree1 = post[:, :, 1][prev == 1]
    disagree0 = post[:, :, 0][prev == 1]
    assert np.allclose(agree1, q * q / (q * q + (1 - q) ** 2))
    assert np.allclose(disagree0, 0.5)


@pytest.mark.parametrize("network", ["complete", "window-1", "window-2", "window-3"])
@pytest.mark.parametrize("v", [1.0, 0.5])
@pytest.mark.parametrize("tie_rule", ["own", "coin"])
def test_zero_information_posteriors_and_no_cascades(network, v, tie_rule):
    cell = Cell(0.5, network, v, 25, tie_rule)
    ep = generate_episodes(cell, 11, 300)
    out = run_rule("bayesian", ep, cell)
    assert np.all(out.posterior == 0.5)
    assert not out.cascade.any()
    if tie_rule == "own":
        assert np.array_equal(out.actions, ep.signals)  # every decision is a tie resolved by the own signal


def test_compare_codes_and_tolerance():
    codes, near = compare(np.array([0.3, 0.2, 0.25, 0.0, 0.25 * (1 + 1e-12), 0.25 * (1 + 1e-7)]),
                          np.array([0.2, 0.3, 0.25, 0.0, 0.25, 0.25]))
    assert codes.tolist() == [1, 0, TIE, TIE, TIE, 1]
    assert near == 1
