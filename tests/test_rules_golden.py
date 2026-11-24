# SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
"""Hand-computed golden examples (derivations in the comments)."""
import numpy as np
import pytest

from herd.model import Cell
from herd.rules import run_rule

from conftest import make_episodes

F, T = False, True


# Complete network, v = 1, own-signal ties, q = 0.6, theta = 1. The public signal
# difference d starts at 0; an informative action moves it by one; |d| >= 2 is a cascade.
@pytest.mark.parametrize("rule", ["bayesian", "imitation"])
@pytest.mark.parametrize("signals,visible,actions,cascade", [
    # d: 0 -> 1 -> 2; agents 3 to 5 herd on 1 whatever their signal.
    ([1, 1, 0, 0, 0], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [F, F, T, T, T]),
    # d: 0 -> 1 -> 0 (tie, own signal) -> -1 -> 0 (tie) -> 1: nobody herds.
    ([1, 0, 0, 1, 1], [1, 1, 1, 1, 1], [1, 0, 0, 1, 1], [F, F, F, F, F]),
    # wrong cascade: d reaches -2 after two wrong signals.
    ([0, 0, 1, 1, 1], [1, 1, 1, 1, 1], [0, 0, 0, 0, 0], [F, F, T, T, T]),
    # agent 2 hidden: d stays 1, agent 3 (s = 0) ties and follows its signal, d -> 0 -> -1.
    ([1, 1, 0, 0, 0], [1, 0, 1, 1, 1], [1, 1, 0, 0, 0], [F, F, F, F, F]),
])
def test_complete_network_golden(rule, signals, visible, actions, cascade):
    ep = make_episodes(1, signals, visible)
    out = run_rule(rule, ep, Cell(0.6, "complete", 1.0, 5))
    assert out.actions[0].tolist() == actions
    assert out.cascade[0].tolist() == cascade


def test_complete_coin_tie_uses_coin():
    # agent 2 has d = 1 and s = 0: a tie, resolved by its coin (1), not by its signal (0).
    ep = make_episodes(1, [1, 0, 0], coins=[[0, 1, 0]])
    out = run_rule("bayesian", ep, Cell(0.6, "complete", 1.0, 3, "coin"))
    assert out.actions[0, 1] == 1
    out_own = run_rule("bayesian", ep, Cell(0.6, "complete", 1.0, 3, "own"))
    assert out_own.actions[0, 1] == 0


@pytest.mark.parametrize("signals,actions,cascade", [
    # window-3 imitation: lead over the last three visible actions.
    ([1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1], [F, F, T, T, T, T]),
    # a4 sees (1,0,0): lead -1, s=0 -> 0, s=1 -> tie: not a cascade; a5 sees (0,0,0): cascade.
    ([1, 0, 0, 0, 1, 1], [1, 0, 0, 0, 0, 0], [F, F, F, F, T, T]),
])
def test_imitation_window3_golden(signals, actions, cascade):
    out = run_rule("imitation", make_episodes(1, signals), Cell(0.6, "window-3", 1.0, 6))
    assert out.actions[0].tolist() == actions
    assert out.cascade[0].tolist() == cascade


def test_independent_baseline_copies_signals_and_never_cascades():
    rng = np.random.default_rng(0)
    sig = rng.integers(0, 2, size=(20, 9))
    ep = make_episodes(rng.integers(0, 2, size=20), sig, rng.random((20, 9)) < 0.5)
    for net in ("complete", "window-1", "window-3"):
        out = run_rule("independent", ep, Cell(0.8, net, 0.5, 9))
        assert np.array_equal(out.actions, sig)
        assert not out.cascade.any()
