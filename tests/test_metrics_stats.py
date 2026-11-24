# SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
import math

import numpy as np
import pytest

from herd.metrics import binary_entropy_bits, episode_metrics, longest_run
from herd.model import ModelError
from herd.stats import (betainc_reg, bootstrap_mean_interval, holm, mean_interval, paired_contrast,
                        t_two_sided_p, wilson_interval)


def test_episode_metrics_golden():
    theta = np.array([1, 0])
    actions = np.array([[1, 0, 0, 1, 0], [0, 0, 0, 0, 0]])
    cascade = np.array([[False, False, True, False, True], [False, False, True, True, True]])
    m = episode_metrics(theta, actions, cascade)
    assert m["accuracy"].tolist() == [0.4, 1.0]
    assert m["cascade_any"].tolist() == [1.0, 1.0]
    assert m["wrong_cascade_any"].tolist() == [1.0, 0.0]
    assert m["longest_wrong_run"].tolist() == [2.0, 0.0]
    assert m["informative_share"].tolist() == [0.6, 0.4]
    assert m["action_entropy_bits"][0] == pytest.approx(-(0.4 * math.log2(0.4) + 0.6 * math.log2(0.6)))
    assert m["action_entropy_bits"][1] == 0.0
    assert m["last_agent_accuracy"].tolist() == [0.0, 1.0]


def test_metric_inputs_validated():
    with pytest.raises(ModelError):
        episode_metrics(np.array([1]), np.zeros((2, 3)), np.zeros((2, 3), bool))
    with pytest.raises(ModelError):
        binary_entropy_bits(np.array([1.2]))
    with pytest.raises(ModelError):
        longest_run(np.zeros(3, bool))


def test_t_distribution_known_values():
    assert t_two_sided_p(2.228138852, 10) == pytest.approx(0.05, abs=1e-6)
    assert t_two_sided_p(12.7062047, 1) == pytest.approx(0.05, abs=1e-6)
    assert t_two_sided_p(1.959963985, 1e7) == pytest.approx(0.05, abs=1e-5)
    assert t_two_sided_p(0.0, 5) == pytest.approx(1.0)
    assert betainc_reg(2.0, 3.0, 0.4) == pytest.approx(0.5248, abs=1e-4)
    with pytest.raises(ModelError):
        t_two_sided_p(1.0, 0)


def test_wilson_interval():
    lo, hi = wilson_interval(50, 100, 1.959963984540054)
    assert lo == pytest.approx(0.4038, abs=1e-4) and hi == pytest.approx(0.5962, abs=1e-4)
    assert wilson_interval(0, 10)[0] == 0.0
    with pytest.raises(ModelError):
        wilson_interval(11, 10)


def test_paired_contrast_and_degenerate_case():
    rng = np.random.default_rng(1)
    x = rng.integers(0, 4, 500) / 4.0  # dyadic values: the difference is exact
    c = paired_contrast(x + 0.25, x)
    assert c["degenerate"] and c["mean"] == 0.25 and c["p_value"] == 0.0
    z = paired_contrast(x, x)
    assert z["degenerate"] and z["p_value"] == 1.0 and z["ci_low"] == z["ci_high"] == 0.0
    y = x + rng.normal(0.05, 0.2, 500)
    c = paired_contrast(y, x, bootstrap_resamples=500, bootstrap_seed=3)
    assert c["ci_low"] < c["mean"] < c["ci_high"]
    assert abs(c["boot_ci_low"] - c["ci_low"]) < 0.01 and abs(c["boot_ci_high"] - c["ci_high"]) < 0.01
    with pytest.raises(ModelError):
        paired_contrast(x, x[:10])


def test_bootstrap_deterministic():
    x = np.arange(100.0)
    assert bootstrap_mean_interval(x, 300, 5) == bootstrap_mean_interval(x, 300, 5)


def test_mean_interval_requires_two_points():
    with pytest.raises(ModelError):
        mean_interval(np.array([1.0]))


def test_holm_hand_computed():
    assert holm([0.01, 0.04, 0.03, 0.005]) == pytest.approx([0.03, 0.06, 0.06, 0.02])
    assert holm([0.5, 0.9]) == pytest.approx([1.0, 1.0])
    with pytest.raises(ModelError):
        holm([0.1, 1.2])
