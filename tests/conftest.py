# SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
import itertools

import numpy as np
import pytest

from herd.model import Episodes


def make_episodes(theta, signals, visible=None, coins=None) -> Episodes:
    signals = np.atleast_2d(np.asarray(signals, dtype=np.int8))
    theta = np.asarray(np.atleast_1d(theta), dtype=np.int8)
    if visible is None:
        visible = np.ones(signals.shape, dtype=bool)
    visible = np.atleast_2d(np.asarray(visible, dtype=bool))
    if visible.shape[0] == 1 and signals.shape[0] > 1:
        visible = np.tile(visible, (signals.shape[0], 1))
    coins = np.zeros(signals.shape, dtype=np.int8) if coins is None else np.atleast_2d(np.asarray(coins, dtype=np.int8))
    return Episodes(theta=theta, signals=signals, visible=visible, coins=coins)


def exhaustive_episodes(n, visible, with_coins=False) -> Episodes:
    th, sg, cs = [], [], []
    coin_space = list(itertools.product((0, 1), repeat=n)) if with_coins else [(0,) * n]
    for t in (0, 1):
        for s in itertools.product((0, 1), repeat=n):
            for c in coin_space:
                th.append(t)
                sg.append(s)
                cs.append(c)
    return make_episodes(th, sg, [visible], cs)


@pytest.fixture
def episodes_factory():
    return make_episodes
