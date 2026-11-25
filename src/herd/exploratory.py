# SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
"""EXP-004 derived analyses (EXPLORATORY, post hoc, M4). Never evidence for a frozen hypothesis.

Reads committed per-episode arrays and committed result.json files; changes no frozen estimate.

  Q2  distribution of paired episode outcomes (social rule versus independent) and the paired
      last-agent difference, for every social-rule contrast of EXP-002-R001 and EXP-003-R001;
  Q3  paired imitation-minus-Bayesian difference in episode accuracy, for every cell;
  Q4  mean expected number of visible observed actions per agent beside Delta (EXP-002-R001);
  plus a summary of the EXP-004-R001 robustness table and of the coin-tie shrinkage.

  python -m herd.exploratory --out results/exploratory/EXP-004-derived
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from pathlib import Path

import numpy as np

from .provenance import REPO_ROOT, git_state, sha256_file
from .serialize import read_result
from .stats import mean_interval

LABEL = "exploratory (EXP-004, post hoc, M4); not evidence for any frozen hypothesis"
SOURCES = {
    "EXP-002-R001": ("results/EXP-002/EXP-002-R001/result.json", "results/raw/EXP-002-R001/episodes.npz"),
    "EXP-003-R001": ("results/EXP-003/EXP-003-R001/result.json", "results/raw/EXP-003-R001/episodes.npz"),
}


def parse_key(key: str) -> dict:
    """'main|q=0.55|complete|v=1.0|N=50|own|bayesian|accuracy' -> fields."""
    var, q, net, v, n, tie, rule, metric = key.split("|")
    return {"variation": var, "q": float(q[2:]), "network": net, "v": float(v[2:]), "n_agents": int(n[2:]),
            "tie_rule": tie, "rule": rule, "metric": metric}


def cell_prefix(key: str) -> str:
    return "|".join(key.split("|")[:6])


def outcome_shares(treat: np.ndarray, control: np.ndarray) -> dict:
    """Share of episodes where treat is below, equal to and above control (exact float comparison of
    proportions with the same denominator N, so equality is exact)."""
    t, c = np.asarray(treat, float), np.asarray(control, float)
    n = t.size
    return {"n": n, "share_below": float(np.sum(t < c)) / n, "share_equal": float(np.sum(t == c)) / n,
            "share_above": float(np.sum(t > c)) / n}


def paired(treat: np.ndarray, control: np.ndarray) -> dict:
    d = np.asarray(treat, float) - np.asarray(control, float)
    m = mean_interval(d)
    return {"mean": m["mean"], "ci_low": m["ci_low"], "ci_high": m["ci_high"], "sd": m["sd"],
            "share_differ": float(np.mean(d != 0))}


def distribution_rows(raw: dict, run_id: str) -> list[dict]:
    rows = []
    for key in sorted(raw.keys()):
        f = parse_key(key)
        if f["metric"] != "accuracy" or f["rule"] == "independent":
            continue
        pre = cell_prefix(key)
        acc, acc0 = raw[key], raw[f"{pre}|independent|accuracy"]
        last, last0 = raw[f"{pre}|{f['rule']}|last_agent_accuracy"], raw[f"{pre}|independent|last_agent_accuracy"]
        sh = outcome_shares(acc, acc0)
        dm = paired(acc, acc0)
        dl = paired(last, last0)
        rows.append({"run_id": run_id, **{k: f[k] for k in ("variation", "q", "network", "v", "n_agents", "tie_rule", "rule")},
                     "n": sh["n"], "delta_accuracy": dm["mean"], "share_below_baseline": sh["share_below"],
                     "share_equal_baseline": sh["share_equal"], "share_above_baseline": sh["share_above"],
                     "delta_last_agent": dl["mean"], "delta_last_agent_ci_low": dl["ci_low"],
                     "delta_last_agent_ci_high": dl["ci_high"]})
    return rows


def rule_difference_rows(raw: dict, run_id: str) -> list[dict]:
    rows = []
    for key in sorted(raw.keys()):
        f = parse_key(key)
        if f["metric"] != "accuracy" or f["rule"] != "imitation":
            continue
        pre = cell_prefix(key)
        d = paired(raw[key], raw[f"{pre}|bayesian|accuracy"])
        rows.append({"run_id": run_id, **{k: f[k] for k in ("variation", "q", "network", "v", "n_agents", "tie_rule")},
                     "n": int(raw[key].size), "imitation_minus_bayesian": d["mean"], "ci_low": d["ci_low"],
                     "ci_high": d["ci_high"], "share_episodes_differ": d["share_differ"]})
    return rows


def expected_observed(network: str, v: float, n_agents: int) -> float:
    """Mean over agents i = 1..N of the expected number of visible observed actions."""
    i = np.arange(1, n_agents + 1)
    if network == "complete":
        k = i - 1
    elif network.startswith("window-"):
        k = np.minimum(int(network.split("-")[1]), i - 1)
    else:
        raise ValueError(f"unknown network {network}")
    return float(v * k.mean())


def quantity_rows(res: dict) -> list[dict]:
    rows = []
    for c in res["contrasts"]:
        cell = c["cell"]
        rows.append({"run_id": res["run_id"], "q": cell["q"], "network": cell["network"], "v": cell["v"], "rule": c["rule"],
                     "mean_expected_observed_actions": expected_observed(cell["network"], cell["v"], cell["n_agents"]),
                     "delta": c["mean"], "ci_low": c["ci_low"], "ci_high": c["ci_high"]})
    return sorted(rows, key=lambda r: (r["q"], r["rule"], r["mean_expected_observed_actions"]))


def shrink_summary(robustness_csvs: list[Path]) -> dict:
    out = {}
    for p in robustness_csvs:
        with open(p, newline="", encoding="utf-8") as fh:
            rows = [r for r in csv.DictReader(fh)]
        v1 = [r for r in rows if r["variation"] == "V1"]
        status: dict[str, int] = {}
        for r in rows:
            status[r["status"]] = status.get(r["status"], 0) + 1
        out[str(p)] = {"comparisons": len(rows), "status_counts": status, "v1_contrasts": len(v1),
                       "v1_below_reference": sum(float(r["delta"]) < float(r["ref_delta"]) for r in v1),
                       "v1_below_half_reference": sum(float(r["delta"]) < 0.5 * float(r["ref_delta"]) for r in v1),
                       "v1_ratio_min": min(float(r["delta"]) / float(r["ref_delta"]) for r in v1),
                       "v1_ratio_max": max(float(r["delta"]) / float(r["ref_delta"]) for r in v1)}
    return out


def write_csv(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="herd.exploratory")
    p.add_argument("--out", required=True)
    a = p.parse_args(argv)
    out = REPO_ROOT / a.out
    if (out / "summary.json").exists():
        raise SystemExit(f"{a.out} already holds results; outputs are never overwritten")
    dist, diff, inputs = [], [], {}
    for run_id, (res_path, raw_path) in SOURCES.items():
        inputs[res_path] = sha256_file(REPO_ROOT / res_path)
        inputs[raw_path] = sha256_file(REPO_ROOT / raw_path)
        with np.load(REPO_ROOT / raw_path) as z:
            raw = {k: z[k] for k in z.files}
        dist += distribution_rows(raw, run_id)
        diff += rule_difference_rows(raw, run_id)
    res2 = read_result(REPO_ROOT / SOURCES["EXP-002-R001"][0])
    qty = quantity_rows(res2)
    rob = [REPO_ROOT / "results/EXP-003/EXP-003-R001/tables/robustness_vs_EXP-002-R001.csv",
           REPO_ROOT / "results/exploratory/EXP-004-R001/tables/robustness_vs_EXP-002-R001.csv"]
    for r in rob:
        inputs[str(r.relative_to(REPO_ROOT))] = sha256_file(r)
    write_csv(dist, out / "q2_distribution.csv")
    write_csv(diff, out / "q3_imitation_minus_bayesian.csv")
    write_csv(qty, out / "q4_quantity.csv")
    main_dist = [r for r in dist if r["variation"] == "main"]
    summary = {
        "label": LABEL, "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "git": git_state(),
        "command": "python -m herd.exploratory " + " ".join(argv if argv is not None else sys.argv[1:]),
        "inputs_sha256": inputs,
        "q2_exp002": {"contrasts": len(main_dist),
                      "share_below_baseline_min": min(r["share_below_baseline"] for r in main_dist),
                      "share_below_baseline_max": max(r["share_below_baseline"] for r in main_dist),
                      "last_agent_delta_min": min(r["delta_last_agent"] for r in main_dist),
                      "last_agent_delta_max": max(r["delta_last_agent"] for r in main_dist),
                      "last_agent_ci_excludes_zero": sum(r["delta_last_agent_ci_low"] > 0 for r in main_dist)},
        "q3_exp002": {"cells": sum(r["variation"] == "main" for r in diff),
                      "complete_cells_all_zero": all(r["imitation_minus_bayesian"] == 0 and r["share_episodes_differ"] == 0
                                                     for r in diff if r["variation"] == "main" and r["network"] == "complete"),
                      "ci_excludes_zero": sum((r["ci_low"] > 0 or r["ci_high"] < 0) for r in diff if r["variation"] == "main")},
        "robustness": {str(Path(k).relative_to(REPO_ROOT)): v for k, v in shrink_summary(rob).items()},
    }
    for name in ("q2_distribution.csv", "q3_imitation_minus_bayesian.csv", "q4_quantity.csv"):
        summary.setdefault("outputs_sha256", {})[name] = sha256_file(out / name)
    (out / "summary.json").write_text(json.dumps(summary, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: summary[k] for k in ("q2_exp002", "q3_exp002", "robustness")}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
