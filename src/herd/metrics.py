# SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
"""Per-episode metrics (protocol section 4). Every metric returns an (E,) array."""

from __future__ import annotations

import numpy as np

from .model import ModelError

METRICS = {
    "accuracy": "proportion of agents with a_i = theta (0 to 1)",
    "cascade_any": "1 if at least one agent is in a cascade (0 or 1)",
    "wrong_cascade_any": "1 if at least one agent is in a cascade on the wrong action (0 or 1)",
    "longest_wrong_run": "length of the longest run of consecutive incorrect actions (agents)",
    "informative_share": "share of agents not in a cascade (0 to 1)",
    "action_entropy_bits": "binary entropy of the within-episode action frequency (bits)",
    "last_agent_accuracy": "1 if a_N = theta (0 or 1)",
}


def longest_run(mask: np.ndarray) -> np.ndarray:
    """Longest run of consecutive True values along axis 1."""
    if mask.ndim != 2:
        raise ModelError("mask must be 2-D")
    run = np.zeros(mask.shape[0], dtype=np.int64)
    best = np.zeros(mask.shape[0], dtype=np.int64)
    for i in range(mask.shape[1]):
        run = np.where(mask[:, i], run + 1, 0)
        best = np.maximum(best, run)
    return best


def binary_entropy_bits(p: np.ndarray) -> np.ndarray:
    p = np.asarray(p, dtype=float)
    if np.any((p < 0) | (p > 1)):
        raise ModelError("probabilities must lie in [0, 1]")
    with np.errstate(divide="ignore", invalid="ignore"):
        h = -(p * np.log2(p) + (1 - p) * np.log2(1 - p))
    return np.where((p == 0) | (p == 1), 0.0, h)


def episode_metrics(theta: np.ndarray, actions: np.ndarray, cascade: np.ndarray) -> dict[str, np.ndarray]:
    if actions.ndim != 2 or cascade.shape != actions.shape or theta.shape != (actions.shape[0],):
        raise ModelError("shape mismatch between theta (E,), actions (E, N) and cascade (E, N)")
    if actions.shape[1] < 1:
        raise ModelError("episodes must have at least one agent")
    correct = actions == theta[:, None]
    wrong = ~correct
    return {
        "accuracy": correct.mean(axis=1),
        "cascade_any": cascade.any(axis=1).astype(float),
        "wrong_cascade_any": (cascade & wrong).any(axis=1).astype(float),
        "longest_wrong_run": longest_run(wrong).astype(float),
        "informative_share": 1.0 - cascade.mean(axis=1),
        "action_entropy_bits": binary_entropy_bits(actions.mean(axis=1)),
        "last_agent_accuracy": correct[:, -1].astype(float),
    }
