# SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
"""Write the engine fixture that the demo's TypeScript port is tested against.

Episodes are drawn with the research engine's own generator (``herd.generate``) and every
decision rule of ``herd.rules`` is applied to them; the fixture stores the inputs (state,
signals, visibility, coins) and the engine's outputs (actions, cascade flags, per-episode
metrics). ``demo/src/engine.test.ts`` feeds the same inputs to the port and requires identical
actions and cascade flags and metrics and paired contrasts (mean and normal 95% interval) within 1e-12. Compute: well under a second, one process.

  .venv/bin/python scripts/export_sandbox_fixture.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from herd.generate import generate_episodes  # noqa: E402
from herd.metrics import episode_metrics  # noqa: E402
from herd.model import Cell  # noqa: E402
from herd.rules import run_rule  # noqa: E402
from herd.stats import mean_interval  # noqa: E402

OUT = REPO / "demo" / "src" / "fixtures" / "engine_fixture.json"
SEED = 7
EPISODES = 16
N_AGENTS = 12
METRICS = ["accuracy", "cascade_any", "wrong_cascade_any", "longest_wrong_run", "informative_share",
           "action_entropy_bits", "last_agent_accuracy"]


def bits(row) -> str:
    return "".join("1" if int(x) else "0" for x in row)


def build() -> dict:
    cells = []
    grid = [(q, net, v, tie) for q in (0.5, 0.55, 0.7) for net in ("complete", "window-1", "window-2", "window-3")
            for v in (1.0, 0.5) for tie in ("own", "coin")]
    for q, net, v, tie in grid:
        cell = Cell(q=q, network=net, v=v, n_agents=N_AGENTS, tie_rule=tie)
        ep = generate_episodes(cell, SEED, EPISODES)
        rules = {}
        for rule in ("independent", "bayesian", "imitation"):
            out = run_rule(rule, ep, cell)
            m = episode_metrics(ep.theta, out.actions, out.cascade)
            rules[rule] = {"actions": [bits(r) for r in out.actions], "cascade": [bits(r) for r in out.cascade],
                           "metrics": {k: [float(x) for x in m[k]] for k in METRICS}}
        acc = {r: [float(x) for x in rules[r]["metrics"]["accuracy"]] for r in rules}
        contrasts = {}
        for r in ("bayesian", "imitation"):
            d = mean_interval([a - b for a, b in zip(acc[r], acc["independent"])])
            contrasts[r] = {"mean": d["mean"], "ci_low": d["ci_low"], "ci_high": d["ci_high"]}
        cells.append({"q": q, "network": net, "v": v, "n_agents": N_AGENTS, "tie_rule": tie,
                      "theta": [int(t) for t in ep.theta], "signals": [bits(r) for r in ep.signals],
                      "visible": [bits(r) for r in ep.visible], "coins": [bits(r) for r in ep.coins], "rules": rules, "contrasts": contrasts})
    return {"description": "Inputs and outputs of the HERD Python engine (herd.generate, herd.rules, herd.metrics) "
                           f"for {len(cells)} cells, seed {SEED}, {EPISODES} episodes of {N_AGENTS} agents each.",
            "seed": SEED, "cells": cells}


def serialize(data: dict) -> str:
    return json.dumps(data, separators=(",", ":")) + "\n"


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(serialize(build()), encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)} ({OUT.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
