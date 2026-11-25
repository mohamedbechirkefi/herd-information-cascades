# SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
"""EXP-004 derived analyses (exploratory) on hand-built arrays."""

import numpy as np
import pytest

from herd.exploratory import (distribution_rows, expected_observed, outcome_shares, parse_key,
                              rule_difference_rows)

PRE = "main|q=0.55|window-2|v=1.0|N=4|own"


def _raw():
    acc = {"independent": [0.5, 0.75, 0.25, 1.0], "bayesian": [0.75, 0.75, 0.0, 1.0], "imitation": [0.75, 1.0, 0.0, 1.0]}
    last = {"independent": [0, 1, 0, 1], "bayesian": [1, 1, 0, 1], "imitation": [1, 1, 0, 0]}
    raw = {}
    for r in acc:
        raw[f"{PRE}|{r}|accuracy"] = np.array(acc[r])
        raw[f"{PRE}|{r}|last_agent_accuracy"] = np.array(last[r], dtype=float)
    return raw


def test_parse_key():
    f = parse_key("V1|q=0.7|complete|v=0.5|N=50|coin|bayesian|accuracy")
    assert f == {"variation": "V1", "q": 0.7, "network": "complete", "v": 0.5, "n_agents": 50, "tie_rule": "coin",
                 "rule": "bayesian", "metric": "accuracy"}


def test_outcome_shares():
    s = outcome_shares(np.array([0.2, 0.5, 0.9, 0.5]), np.array([0.5, 0.5, 0.5, 0.1]))
    assert s == {"n": 4, "share_below": 0.25, "share_equal": 0.25, "share_above": 0.5}


def test_distribution_and_rule_difference():
    rows = {r["rule"]: r for r in distribution_rows(_raw(), "EXP-X")}
    b = rows["bayesian"]
    assert b["share_below_baseline"] == 0.25 and b["share_equal_baseline"] == 0.5 and b["share_above_baseline"] == 0.25
    assert b["delta_accuracy"] == pytest.approx(0.0)
    assert b["delta_last_agent"] == pytest.approx(0.25)
    d = rule_difference_rows(_raw(), "EXP-X")
    assert len(d) == 1
    assert d[0]["imitation_minus_bayesian"] == pytest.approx(0.0625)
    assert d[0]["share_episodes_differ"] == 0.25


def test_expected_observed():
    assert expected_observed("complete", 1.0, 4) == pytest.approx(1.5)  # (0+1+2+3)/4
    assert expected_observed("window-2", 0.5, 4) == pytest.approx(0.5 * (0 + 1 + 2 + 2) / 4)
    with pytest.raises(ValueError):
        expected_observed("ring", 1.0, 4)
