# SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
"""Invariant tests on random episodes."""
import numpy as np
import pytest

from herd.generate import generate_episodes
from herd.metrics import episode_metrics
from herd.model import Cell, Episodes
from herd.rules import run_rule

CELLS = [Cell(q, net, v, 15, tie) for q in (0.55, 0.8) for net in ("complete", "window-2", "window-3")
         for v in (1.0, 0.5) for tie in ("own", "coin")]


@pytest.mark.parametrize("cell", CELLS, ids=lambda c: c.seed_key() + c.tie_rule)
@pytest.mark.parametrize("rule", ["bayesian", "imitation"])
def test_cascade_agent_action_does_not_depend_on_own_signal(cell, rule):
    ep = generate_episodes(cell, 21, 60)
    out = run_rule(rule, ep, cell)
    rng = np.random.default_rng(0)
    for _ in range(40):
        e, i = int(rng.integers(ep.n_episodes)), int(rng.integers(ep.n_agents))
        flipped = ep.signals.copy()
        flipped[e, i] = 1 - flipped[e, i]
        out2 = run_rule(rule, Episodes(ep.theta, flipped, ep.visible, ep.coins), cell)
        assert np.array_equal(out.actions[e, :i], out2.actions[e, :i])  # the past does not change
        if out.cascade[e, i]:
            assert out.actions[e, i] == out2.actions[e, i]
        elif cell.tie_rule == "own":
            assert out.actions[e, i] != out2.actions[e, i]  # outside a cascade, own-tie agents reveal their signal


@pytest.mark.parametrize("cell", CELLS[:6], ids=lambda c: c.seed_key())
def test_outputs_are_binary_deterministic_and_metrics_bounded(cell):
    ep = generate_episodes(cell, 3, 80)
    for rule in ("independent", "bayesian", "imitation"):
        a = run_rule(rule, ep, cell)
        b = run_rule(rule, ep, cell)
        assert np.array_equal(a.actions, b.actions) and np.array_equal(a.cascade, b.cascade)
        assert set(np.unique(a.actions)) <= {0, 1}
        m = episode_metrics(ep.theta, a.actions, a.cascade)
        for name in ("accuracy", "cascade_any", "wrong_cascade_any", "informative_share", "action_entropy_bits", "last_agent_accuracy"):
            assert np.all((m[name] >= 0) & (m[name] <= 1))
        assert np.all((m["longest_wrong_run"] >= 0) & (m["longest_wrong_run"] <= cell.n_agents))
        assert np.all(m["wrong_cascade_any"] <= m["cascade_any"])


def test_zero_visibility_makes_social_rules_independent():
    cell = Cell(0.7, "complete", 0.0, 20)
    ep = generate_episodes(cell, 1, 100)
    for rule in ("bayesian", "imitation"):
        assert np.array_equal(run_rule(rule, ep, cell).actions, ep.signals)
    cell3 = Cell(0.7, "window-3", 0.0, 20)
    ep3 = generate_episodes(cell3, 1, 100)
    assert np.array_equal(run_rule("bayesian", ep3, cell3).actions, ep3.signals)


def test_symmetry_under_relabelling_of_states():
    # Swapping 0 and 1 in theta, signals and coins swaps every action (own and coin ties).
    for cell in (Cell(0.6, "window-3", 0.5, 20, "coin"), Cell(0.6, "complete", 0.5, 20, "own")):
        ep = generate_episodes(cell, 8, 100)
        flip = Episodes((1 - ep.theta).astype(np.int8), (1 - ep.signals).astype(np.int8), ep.visible, (1 - ep.coins).astype(np.int8))
        for rule in ("bayesian", "imitation"):
            assert np.array_equal(run_rule(rule, ep, cell).actions, 1 - run_rule(rule, flip, cell).actions)
