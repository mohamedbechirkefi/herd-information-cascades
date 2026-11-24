# SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
"""Seeded episode generation with common random numbers.

Streams are derived from (master seed, cell) with numpy SeedSequence. The tie rule
is not part of the key, and coin flips use their own child stream, so that every
rule and every tie-rule variation sees the same hidden states, signals and
visibility pattern for a given (seed, cell, episode index).
"""

from __future__ import annotations

import hashlib

import numpy as np

from .model import Cell, Episodes, ModelError

STREAM_NAMES = ("theta", "signals", "visibility", "coins")


def _spawn_key(cell: Cell) -> tuple[int, ...]:
    digest = hashlib.sha256(cell.seed_key().encode("utf-8")).digest()
    return tuple(int.from_bytes(digest[i : i + 4], "big") for i in range(0, 16, 4))


def streams(cell: Cell, master_seed: int) -> dict[str, np.random.Generator]:
    if isinstance(master_seed, bool) or not isinstance(master_seed, (int, np.integer)) or master_seed < 0:
        raise ModelError(f"master_seed must be a non-negative integer, got {master_seed!r}")
    root = np.random.SeedSequence(entropy=int(master_seed), spawn_key=_spawn_key(cell))
    children = root.spawn(len(STREAM_NAMES))
    return {name: np.random.Generator(np.random.PCG64(child)) for name, child in zip(STREAM_NAMES, children)}


def generate_episodes(cell: Cell, master_seed: int, n_episodes: int) -> Episodes:
    """Draw ``n_episodes`` episodes for ``cell``. Deterministic in (cell, master_seed, n_episodes)."""
    if isinstance(n_episodes, bool) or not isinstance(n_episodes, (int, np.integer)) or n_episodes < 1:
        raise ModelError(f"n_episodes must be an integer >= 1, got {n_episodes!r}")
    g = streams(cell, master_seed)
    e, n = int(n_episodes), int(cell.n_agents)
    theta = (g["theta"].random(e) < 0.5).astype(np.int8)
    correct = g["signals"].random((e, n)) < cell.q
    signals = np.where(correct, theta[:, None], 1 - theta[:, None]).astype(np.int8)
    visible = g["visibility"].random((e, n)) < cell.v
    coins = (g["coins"].random((e, n)) < 0.5).astype(np.int8)
    return Episodes(theta=theta, signals=signals, visible=visible, coins=coins)
