# SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
"""Decision rules: independent (baseline), Bayesian social learning and naive imitation.

All functions are pure: they take an Episodes batch and a Cell and return a RuleOutput.
Agent decisions are coded as 1, 0 or TIE (-1) before tie resolution. An agent is in a
cascade when its action would be the same, deterministically, under both values of its
own signal given what it observed (protocol section 4).

Bayesian inference is exact up to floating point:
- complete network: public-belief recursion over visible actions;
- window-k network: forward recursion over the 2^k joint states of the last k actions,
  conditional on each hidden state value, using the predecessors' decision tables.
Ties are detected with a relative tolerance TIE_TOL; comparisons whose relative gap lies
between TIE_TOL and NEAR_TIE_BAND are counted as near ties and reported, so that a
tolerance problem cannot pass silently.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .model import Cell, Episodes, ModelError

TIE = -1
TIE_TOL = 1e-9
NEAR_TIE_BAND = 1e-6


@dataclass
class RuleOutput:
    actions: np.ndarray  # (E, N) int8
    cascade: np.ndarray  # (E, N) bool
    posterior: np.ndarray | None = None  # (E, N, 2) P(theta=1 | s, observation) for s = 0, 1 (Bayesian only)
    near_ties: int = 0
    extra: dict = field(default_factory=dict)


def signal_likelihood(s: int, theta: int, q: float) -> float:
    """P(s | theta) for a binary signal of accuracy q."""
    if s not in (0, 1) or theta not in (0, 1):
        raise ModelError("s and theta must be 0 or 1")
    if not 0.5 <= q < 1.0:
        raise ModelError(f"q must satisfy 0.5 <= q < 1, got {q}")
    return q if s == theta else 1.0 - q


def compare(a: np.ndarray, b: np.ndarray) -> tuple[np.ndarray, int]:
    """Decision codes for posterior weights a = P(s|1)L1 and b = P(s|0)L0.

    Returns (codes, near_tie_count): 1 if a > b, 0 if a < b, TIE if equal within TIE_TOL
    relative to max(a, b) (including the unreachable case a = b = 0).
    """
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    scale = np.maximum(a, b)
    gap = np.abs(a - b)
    tie = gap <= TIE_TOL * scale
    codes = np.where(tie, TIE, np.where(a > b, 1, 0)).astype(np.int8)
    near = (~tie) & (gap <= NEAR_TIE_BAND * scale)
    return codes, int(near.sum())


def resolve(codes: np.ndarray, signal: np.ndarray, coin: np.ndarray, tie_rule: str) -> np.ndarray:
    """Turn decision codes into actions."""
    if tie_rule == "own":
        breaker = signal
    elif tie_rule == "coin":
        breaker = coin
    else:
        raise ModelError(f"unknown tie_rule {tie_rule!r}")
    return np.where(codes == TIE, breaker, codes).astype(np.int8)


def prob_action_one(code: np.ndarray, s: int, tie_rule: str) -> np.ndarray:
    """P(a = 1 | decision code, signal s) for an agent with that decision code."""
    tie_value = float(s) if tie_rule == "own" else 0.5
    return np.where(code == 1, 1.0, np.where(code == 0, 0.0, tie_value))


def cascade_flags(code0: np.ndarray, code1: np.ndarray) -> np.ndarray:
    """In cascade: deterministic and identical action under both signal values."""
    return (code0 == code1) & (code0 != TIE)


def _posterior(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    total = a + b
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(total > 0, a / np.where(total > 0, total, 1.0), 0.5)


def independent(ep: Episodes, cell: Cell) -> RuleOutput:
    """Baseline: a_i = s_i. Never in a cascade."""
    _check(ep, cell)
    return RuleOutput(actions=ep.signals.astype(np.int8).copy(), cascade=np.zeros(ep.signals.shape, dtype=bool))


def imitation(ep: Episodes, cell: Cell) -> RuleOutput:
    """Naive vote counting: a_i = 1[n1 - n0 + (2 s_i - 1) > 0], ties per tie rule."""
    _check(ep, cell)
    e, n = ep.signals.shape
    k = cell.window
    actions = np.zeros((e, n), dtype=np.int8)
    cascade = np.zeros((e, n), dtype=bool)
    contrib = np.zeros((e, n), dtype=np.int64)  # visible (2a - 1), 0 if hidden
    for i in range(n):
        lo = 0 if k is None else max(0, i - k)
        lead = contrib[:, lo:i].sum(axis=1)
        code0 = np.sign(lead - 1).astype(np.int8)
        code1 = np.sign(lead + 1).astype(np.int8)
        code0 = np.where(code0 == 0, TIE, np.where(code0 > 0, 1, 0)).astype(np.int8)
        code1 = np.where(code1 == 0, TIE, np.where(code1 > 0, 1, 0)).astype(np.int8)
        s = ep.signals[:, i]
        code = np.where(s == 1, code1, code0)
        a = resolve(code, s, ep.coins[:, i], cell.tie_rule)
        actions[:, i] = a
        cascade[:, i] = cascade_flags(code0, code1)
        contrib[:, i] = np.where(ep.visible[:, i], 2 * a.astype(np.int64) - 1, 0)
    return RuleOutput(actions=actions, cascade=cascade)


def bayesian(ep: Episodes, cell: Cell) -> RuleOutput:
    """Bayesian social learning, dispatched on the network."""
    k = cell.window
    if k is None:
        return bayesian_complete(ep, cell)
    return bayesian_window(ep, cell, k)


def bayesian_complete(ep: Episodes, cell: Cell) -> RuleOutput:
    """Public-belief recursion for the complete network."""
    _check(ep, cell)
    e, n = ep.signals.shape
    q = float(cell.q)
    ps = {(s, t): (q if s == t else 1.0 - q) for s in (0, 1) for t in (0, 1)}
    pub1 = np.full(e, 0.5)
    pub0 = np.full(e, 0.5)
    actions = np.zeros((e, n), dtype=np.int8)
    cascade = np.zeros((e, n), dtype=bool)
    posterior = np.zeros((e, n, 2))
    public_posterior = np.zeros((e, n))
    near_total = 0
    for i in range(n):
        public_posterior[:, i] = pub1 / (pub1 + pub0)
        a0, b0 = ps[(0, 1)] * pub1, ps[(0, 0)] * pub0
        a1, b1 = ps[(1, 1)] * pub1, ps[(1, 0)] * pub0
        code0, n0 = compare(a0, b0)
        code1, n1 = compare(a1, b1)
        near_total += n0 + n1
        posterior[:, i, 0] = _posterior(a0, b0)
        posterior[:, i, 1] = _posterior(a1, b1)
        s = ep.signals[:, i]
        a = resolve(np.where(s == 1, code1, code0), s, ep.coins[:, i], cell.tie_rule)
        actions[:, i] = a
        cascade[:, i] = cascade_flags(code0, code1)
        # Likelihood of the observed action under each state, for observers.
        p1_t1 = ps[(0, 1)] * prob_action_one(code0, 0, cell.tie_rule) + ps[(1, 1)] * prob_action_one(code1, 1, cell.tie_rule)
        p1_t0 = ps[(0, 0)] * prob_action_one(code0, 0, cell.tie_rule) + ps[(1, 0)] * prob_action_one(code1, 1, cell.tie_rule)
        like1 = np.where(a == 1, p1_t1, 1.0 - p1_t1)
        like0 = np.where(a == 1, p1_t0, 1.0 - p1_t0)
        vis = ep.visible[:, i]
        new1 = np.where(vis, pub1 * like1, pub1)
        new0 = np.where(vis, pub0 * like0, pub0)
        total = new1 + new0
        if np.any(total <= 0):
            raise FloatingPointError("public belief collapsed to zero mass")
        pub1, pub0 = new1 / total, new0 / total
    return RuleOutput(actions=actions, cascade=cascade, posterior=posterior, near_ties=near_total,
                      extra={"public_posterior": public_posterior})


def bayesian_window(ep: Episodes, cell: Cell, k: int) -> RuleOutput:
    """Forward recursion over the joint law of the last k actions, given theta.

    State index x encodes the last k actions with bit j = action at position i - k + j
    (bit 0 is the oldest). Positions before the first agent are padded as hidden zeros.
    """
    _check(ep, cell)
    if isinstance(k, bool) or not isinstance(k, (int, np.integer)) or k < 1:
        raise ModelError(f"window size must be an integer >= 1, got {k!r}")
    if k > 16:
        raise ModelError("window recursion limited to k <= 16 (2^k states)")
    e, n = ep.signals.shape
    q = float(cell.q)
    size = 1 << k
    ps = {(s, t): (q if s == t else 1.0 - q) for s in (0, 1) for t in (0, 1)}
    joint = np.zeros((e, 2, size))  # P(last k actions = x | theta)
    joint[:, :, 0] = 1.0
    vis_pad = np.concatenate([np.zeros((e, k), dtype=bool), ep.visible], axis=1)
    act_pad = np.zeros((e, n + k), dtype=np.int64)
    actions = np.zeros((e, n), dtype=np.int8)
    cascade = np.zeros((e, n), dtype=bool)
    posterior = np.zeros((e, n, 2))
    rows = np.arange(e)
    near_total = 0
    for i in range(n):
        # Likelihood of the visible part of each window state: marginalise hidden bits.
        marg = joint.reshape((e, 2) + (2,) * k)
        for j in range(k):
            hidden = ~vis_pad[:, i + j]
            if not hidden.any():
                continue
            axis = 2 + (k - 1 - j)
            summed = np.broadcast_to(marg.sum(axis=axis, keepdims=True), marg.shape)
            mask = hidden.reshape((e,) + (1,) * (k + 1))
            marg = np.where(mask, summed, marg)
        marg = marg.reshape((e, 2, size))
        l1, l0 = marg[:, 1, :], marg[:, 0, :]
        a0, b0 = ps[(0, 1)] * l1, ps[(0, 0)] * l0
        a1, b1 = ps[(1, 1)] * l1, ps[(1, 0)] * l0
        code0, _ = compare(a0, b0)  # (E, S)
        code1, _ = compare(a1, b1)
        # Realised window state.
        x = np.zeros(e, dtype=np.int64)
        for j in range(k):
            x |= act_pad[:, i + j] << j
        c0, c1 = code0[rows, x], code1[rows, x]
        # Near ties are counted only at realised states, where they affect play.
        near_total += compare(a0[rows, x], b0[rows, x])[1] + compare(a1[rows, x], b1[rows, x])[1]
        posterior[:, i, 0] = _posterior(a0[rows, x], b0[rows, x])
        posterior[:, i, 1] = _posterior(a1[rows, x], b1[rows, x])
        s = ep.signals[:, i]
        a = resolve(np.where(s == 1, c1, c0), s, ep.coins[:, i], cell.tie_rule)
        actions[:, i] = a
        cascade[:, i] = cascade_flags(c0, c1)
        act_pad[:, i + k] = a
        # Transition of the joint law: append agent i's action, drop the oldest.
        pa0 = prob_action_one(code0, 0, cell.tie_rule)
        pa1 = prob_action_one(code1, 1, cell.tie_rule)
        p1 = np.stack([ps[(0, 0)] * pa0 + ps[(1, 0)] * pa1, ps[(0, 1)] * pa0 + ps[(1, 1)] * pa1], axis=1)  # (E, 2, S)
        to_one = (joint * p1).reshape(e, 2, size // 2, 2).sum(axis=3)
        to_zero = (joint * (1.0 - p1)).reshape(e, 2, size // 2, 2).sum(axis=3)
        new = np.zeros_like(joint)
        new[:, :, : size // 2] = to_zero
        new[:, :, size // 2 :] = to_one
        joint = new
    return RuleOutput(actions=actions, cascade=cascade, posterior=posterior, near_ties=near_total)


RULE_FUNCTIONS = {"independent": independent, "bayesian": bayesian, "imitation": imitation}


def run_rule(rule: str, ep: Episodes, cell: Cell) -> RuleOutput:
    if rule not in RULE_FUNCTIONS:
        raise ModelError(f"unknown rule {rule!r}; expected one of {sorted(RULE_FUNCTIONS)}")
    return RULE_FUNCTIONS[rule](ep, cell)


def _check(ep: Episodes, cell: Cell) -> None:
    if not isinstance(ep, Episodes) or not isinstance(cell, Cell):
        raise ModelError("expected an Episodes batch and a Cell")
    if ep.n_agents != cell.n_agents:
        raise ModelError(f"episodes have {ep.n_agents} agents but the cell specifies {cell.n_agents}")
