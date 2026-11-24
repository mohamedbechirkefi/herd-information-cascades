# SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
"""Typed model objects: a simulation cell and a batch of episodes.

Units: probabilities are dimensionless proportions in [0, 1]; agent indices are
0-based in code and 1-based in the protocol text; ``n_agents`` counts agents.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

import numpy as np

NETWORK_PATTERN = re.compile(r"^(complete|window-([1-9][0-9]*))$")
TIE_RULES = ("own", "coin")
RULES = ("independent", "bayesian", "imitation")


class ModelError(ValueError):
    """Raised for invalid model inputs (explicit error path)."""


def parse_network(network: str) -> int | None:
    """Return the window size k for ``window-k``, or None for ``complete``."""
    if not isinstance(network, str):
        raise ModelError(f"network must be a string, got {type(network).__name__}")
    match = NETWORK_PATTERN.match(network)
    if match is None:
        raise ModelError(f"unknown network {network!r}; expected 'complete' or 'window-k' with k >= 1")
    return None if match.group(2) is None else int(match.group(2))


@dataclass(frozen=True)
class Cell:
    """One cell of the design: signal quality, network, visibility, horizon and tie rule.

    q: probability that a private signal equals the hidden state, 1/2 <= q < 1.
    network: 'complete' or 'window-k'.
    v: probability that an action is publicly visible, 0 <= v <= 1.
    n_agents: number of agents per episode, >= 1.
    tie_rule: 'own' (ties follow the own signal) or 'coin' (fair coin).
    """

    q: float
    network: str
    v: float
    n_agents: int
    tie_rule: str = "own"

    def __post_init__(self) -> None:
        for name in ("q", "v"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not np.isfinite(value):
                raise ModelError(f"{name} must be a finite number, got {value!r}")
        if not 0.5 <= self.q < 1.0:
            raise ModelError(f"q must satisfy 0.5 <= q < 1, got {self.q}")
        if not 0.0 <= self.v <= 1.0:
            raise ModelError(f"v must satisfy 0 <= v <= 1, got {self.v}")
        if isinstance(self.n_agents, bool) or not isinstance(self.n_agents, (int, np.integer)) or self.n_agents < 1:
            raise ModelError(f"n_agents must be an integer >= 1, got {self.n_agents!r}")
        if self.tie_rule not in TIE_RULES:
            raise ModelError(f"tie_rule must be one of {TIE_RULES}, got {self.tie_rule!r}")
        parse_network(self.network)

    @property
    def window(self) -> int | None:
        return parse_network(self.network)

    def seed_key(self) -> str:
        """Canonical text identifying the episode distribution (tie rule excluded on purpose,
        so that tie-rule variations share episode draws)."""
        return f"q={self.q!r};network={self.network};v={self.v!r};N={int(self.n_agents)}"

    def as_dict(self) -> dict:
        return {"q": float(self.q), "network": self.network, "v": float(self.v),
                "n_agents": int(self.n_agents), "tie_rule": self.tie_rule}


@dataclass(frozen=True)
class Episodes:
    """A batch of E episodes with N agents each.

    theta: (E,) hidden states in {0, 1}.
    signals: (E, N) private signals in {0, 1}.
    visible: (E, N) booleans, True when agent i's action is publicly recorded.
    coins: (E, N) fair-coin outcomes in {0, 1}, used only to break ties under tie_rule='coin'.
    """

    theta: np.ndarray
    signals: np.ndarray
    visible: np.ndarray
    coins: np.ndarray

    def __post_init__(self) -> None:
        theta, signals, visible, coins = self.theta, self.signals, self.visible, self.coins
        for name, arr in (("theta", theta), ("signals", signals), ("visible", visible), ("coins", coins)):
            if not isinstance(arr, np.ndarray):
                raise ModelError(f"{name} must be a numpy array")
        if theta.ndim != 1:
            raise ModelError("theta must have shape (E,)")
        if signals.ndim != 2 or signals.shape[0] != theta.shape[0]:
            raise ModelError("signals must have shape (E, N) with E = len(theta)")
        if visible.shape != signals.shape or coins.shape != signals.shape:
            raise ModelError("visible and coins must have the same shape as signals")
        if visible.dtype != np.bool_:
            raise ModelError("visible must be boolean")
        for name, arr in (("theta", theta), ("signals", signals), ("coins", coins)):
            if arr.size and not np.isin(arr, (0, 1)).all():
                raise ModelError(f"{name} must contain only 0 and 1")

    @property
    def n_episodes(self) -> int:
        return int(self.theta.shape[0])

    @property
    def n_agents(self) -> int:
        return int(self.signals.shape[1])
