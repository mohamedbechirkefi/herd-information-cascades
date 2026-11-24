# SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
import numpy as np
import pytest

from herd.generate import generate_episodes
from herd.model import Cell, Episodes, ModelError, parse_network
from herd.rules import run_rule, signal_likelihood


@pytest.mark.parametrize("kwargs", [
    dict(q=0.49, network="complete", v=1.0, n_agents=5),
    dict(q=1.0, network="complete", v=1.0, n_agents=5),
    dict(q=float("nan"), network="complete", v=1.0, n_agents=5),
    dict(q=True, network="complete", v=1.0, n_agents=5),
    dict(q=0.6, network="complete", v=1.5, n_agents=5),
    dict(q=0.6, network="complete", v=-0.1, n_agents=5),
    dict(q=0.6, network="complete", v=1.0, n_agents=0),
    dict(q=0.6, network="complete", v=1.0, n_agents=2.5),
    dict(q=0.6, network="ring", v=1.0, n_agents=5),
    dict(q=0.6, network="window-0", v=1.0, n_agents=5),
    dict(q=0.6, network="complete", v=1.0, n_agents=5, tie_rule="random"),
])
def test_cell_rejects_invalid_inputs(kwargs):
    with pytest.raises(ModelError):
        Cell(**kwargs)


def test_parse_network():
    assert parse_network("complete") is None
    assert parse_network("window-1") == 1
    assert parse_network("window-12") == 12
    for bad in ("window-", "window-01", "Complete", 3):
        with pytest.raises(ModelError):
            parse_network(bad)


def test_episodes_validation():
    good = dict(theta=np.array([0, 1], np.int8), signals=np.zeros((2, 3), np.int8),
                visible=np.ones((2, 3), bool), coins=np.zeros((2, 3), np.int8))
    Episodes(**good)
    with pytest.raises(ModelError):
        Episodes(**{**good, "signals": np.full((2, 3), 2, np.int8)})
    with pytest.raises(ModelError):
        Episodes(**{**good, "visible": np.ones((2, 3), np.int8)})
    with pytest.raises(ModelError):
        Episodes(**{**good, "coins": np.zeros((2, 4), np.int8)})
    with pytest.raises(ModelError):
        Episodes(**{**good, "theta": np.array([0, 1, 1], np.int8)})


def test_rule_rejects_mismatched_horizon():
    cell = Cell(0.6, "complete", 1.0, 4)
    ep = generate_episodes(Cell(0.6, "complete", 1.0, 5), 0, 3)
    with pytest.raises(ModelError):
        run_rule("bayesian", ep, cell)
    with pytest.raises(ModelError):
        run_rule("majority", generate_episodes(cell, 0, 3), cell)


def test_generation_is_deterministic_and_seed_sensitive():
    cell = Cell(0.7, "window-3", 0.5, 30)
    a = generate_episodes(cell, 7, 50)
    b = generate_episodes(cell, 7, 50)
    c = generate_episodes(cell, 8, 50)
    assert np.array_equal(a.signals, b.signals) and np.array_equal(a.visible, b.visible) and np.array_equal(a.coins, b.coins)
    assert not np.array_equal(a.signals, c.signals)


def test_common_random_numbers_across_tie_rules():
    own = generate_episodes(Cell(0.55, "complete", 0.5, 50, "own"), 3, 100)
    coin = generate_episodes(Cell(0.55, "complete", 0.5, 50, "coin"), 3, 100)
    for name in ("theta", "signals", "visible", "coins"):
        assert np.array_equal(getattr(own, name), getattr(coin, name))


def test_generation_invalid_inputs():
    cell = Cell(0.6, "complete", 1.0, 5)
    for bad in (0, -1, 2.5, True):
        with pytest.raises(ModelError):
            generate_episodes(cell, 0, bad)
    for bad in (-1, 1.5, True):
        with pytest.raises(ModelError):
            generate_episodes(cell, bad, 10)


def test_generated_signal_accuracy_and_visibility_rates():
    ep = generate_episodes(Cell(0.7, "complete", 0.5, 100), 1, 2000)
    acc = (ep.signals == ep.theta[:, None]).mean()
    assert abs(acc - 0.7) < 0.005
    assert abs(ep.visible.mean() - 0.5) < 0.005
    assert np.all(generate_episodes(Cell(0.7, "complete", 1.0, 10), 1, 50).visible)


def test_signal_likelihood():
    assert signal_likelihood(1, 1, 0.7) == 0.7
    assert signal_likelihood(0, 1, 0.7) == pytest.approx(0.3)
    assert signal_likelihood(0, 0, 0.7) == 0.7
    with pytest.raises(ModelError):
        signal_likelihood(2, 1, 0.7)
    with pytest.raises(ModelError):
        signal_likelihood(1, 1, 0.4)
