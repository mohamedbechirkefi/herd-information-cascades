# SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
"""Exact reference implementations for verification (small N only).

ExactModel enumerates every hidden state, every private-signal profile and every
coin profile with rational arithmetic (fractions.Fraction). Each agent's decision is
derived from the definition of the posterior, P(theta | s_i, observed visible
predecessor actions), by summing over all predecessor profiles. It shares no code with
the vectorised engine in rules.py and serves as the differential-test oracle.
"""

from __future__ import annotations

import itertools
from fractions import Fraction

from .model import ModelError, parse_network

TIE = -1


def observer_sets(network: str, n_agents: int) -> list[tuple[int, ...]]:
    """Predecessor sets O_i (0-based) for each agent."""
    k = parse_network(network)
    out = []
    for i in range(n_agents):
        lo = 0 if k is None else max(0, i - k)
        out.append(tuple(range(lo, i)))
    return out


def analytic_wrong_cascade_probability(q: Fraction | float, n_agents: int):
    """P(at least one agent in a wrong cascade among agents 1..N): Bayesian, complete, v=1,
    own-signal ties, q > 1/2. Equals (1-q)^2 / (q^2 + (1-q)^2) * (1 - (2q(1-q))^m),
    m = floor((N-1)/2). Exact for Fraction input."""
    if not (q > Fraction(1, 2) and q < 1):
        raise ModelError("the analytic anchor requires 1/2 < q < 1 (at q = 1/2 no cascade forms)")
    if n_agents < 1:
        raise ModelError("n_agents must be >= 1")
    m = (n_agents - 1) // 2
    r = 2 * q * (1 - q)
    return (1 - q) ** 2 / (q ** 2 + (1 - q) ** 2) * (1 - r ** m)


def analytic_no_cascade_probability(q: Fraction | float, pairs: int):
    """P(no cascade has started after 2m agents) = (2q(1-q))^m, same setting."""
    if pairs < 0:
        raise ModelError("pairs must be >= 0")
    return (2 * q * (1 - q)) ** pairs


class ExactModel:
    """Exact model for one (q, network, visibility pattern, tie rule, rule)."""

    def __init__(self, q: Fraction, network: str, visible: tuple[bool, ...], tie_rule: str = "own",
                 rule: str = "bayesian", max_agents: int = 9):
        if not isinstance(q, Fraction) or not (Fraction(1, 2) <= q < 1):
            raise ModelError("q must be a Fraction with 1/2 <= q < 1")
        if tie_rule not in ("own", "coin"):
            raise ModelError("tie_rule must be 'own' or 'coin'")
        if rule not in ("bayesian", "imitation", "independent"):
            raise ModelError("unknown rule")
        n = len(visible)
        if n < 1 or n > max_agents:
            raise ModelError(f"exact enumeration supports 1..{max_agents} agents")
        self.q, self.network, self.visible, self.tie_rule, self.rule, self.n = q, network, tuple(visible), tie_rule, rule, n
        self.obs = observer_sets(network, n)
        # tables[i][observed] = (code for s=0, code for s=1)
        self.tables: list[dict[tuple, tuple[int, int]]] = []
        self.posteriors: list[dict[tuple, tuple[Fraction, Fraction]]] = []
        for i in range(n):
            self._build_table(i)

    # -- definitions -------------------------------------------------------------------
    def p_signal(self, s: int, theta: int) -> Fraction:
        return self.q if s == theta else 1 - self.q

    def observed(self, i: int, actions: tuple[int, ...]) -> tuple:
        return tuple((j, actions[j]) for j in self.obs[i] if self.visible[j])

    def act(self, i: int, s: int, coin: int, actions: tuple[int, ...]) -> int:
        codes = self.tables[i][self.observed(i, actions)]
        code = codes[s]
        if code == TIE:
            return s if self.tie_rule == "own" else coin
        return code

    def play(self, signals, coins=None) -> tuple[tuple[int, ...], tuple[bool, ...]]:
        """Actions and cascade flags for one profile."""
        coins = coins if coins is not None else (0,) * self.n
        actions: tuple[int, ...] = ()
        flags = []
        for i in range(self.n):
            c0, c1 = self.tables[i][self.observed(i, actions)]
            flags.append(c0 == c1 and c0 != TIE)
            actions = actions + (self.act(i, signals[i], coins[i], actions),)
        return actions, tuple(flags)

    def _profiles(self, length: int):
        coin_space = itertools.product((0, 1), repeat=length) if self.tie_rule == "coin" else [(0,) * length]
        coin_list = list(coin_space)
        coin_weight = Fraction(1, 2 ** length) if self.tie_rule == "coin" else Fraction(1)
        for sig in itertools.product((0, 1), repeat=length):
            for coins in coin_list:
                yield sig, coins, coin_weight

    def _prefix_actions(self, sig, coins) -> tuple[int, ...]:
        actions: tuple[int, ...] = ()
        for j in range(len(sig)):
            actions = actions + (self.act(j, sig[j], coins[j], actions),)
        return actions

    def _build_table(self, i: int) -> None:
        like = {0: {}, 1: {}}
        for theta in (0, 1):
            for sig, coins, cw in self._profiles(i):
                w = cw
                for s in sig:
                    w *= self.p_signal(s, theta)
                acts = self._prefix_actions(sig, coins)
                o = self.observed(i, acts)
                like[theta][o] = like[theta].get(o, Fraction(0)) + w
        table, post = {}, {}
        for o in set(like[0]) | set(like[1]):
            l1, l0 = like[1].get(o, Fraction(0)), like[0].get(o, Fraction(0))
            codes, posts = [], []
            for s in (0, 1):
                if self.rule == "independent":
                    codes.append(s)
                    posts.append(Fraction(1, 2))
                    continue
                if self.rule == "imitation":
                    lead = sum(2 * a - 1 for _, a in o) + (2 * s - 1)
                    codes.append(TIE if lead == 0 else int(lead > 0))
                    posts.append(Fraction(1, 2))
                    continue
                a, b = self.p_signal(s, 1) * l1, self.p_signal(s, 0) * l0
                codes.append(TIE if a == b else int(a > b))
                posts.append(a / (a + b) if a + b > 0 else Fraction(1, 2))
            table[o] = (codes[0], codes[1])
            post[o] = (posts[0], posts[1])
        self.tables.append(table)
        self.posteriors.append(post)

    # -- exact expectations --------------------------------------------------------------
    def expectation(self, fn) -> Fraction:
        """E[fn(theta, signals, actions, flags)] over theta ~ Bernoulli(1/2), signals, coins."""
        total = Fraction(0)
        for theta in (0, 1):
            for sig, coins, cw in self._profiles(self.n):
                w = Fraction(1, 2) * cw
                for s in sig:
                    w *= self.p_signal(s, theta)
                actions, flags = self.play(sig, coins)
                total += w * fn(theta, sig, actions, flags)
        return total
