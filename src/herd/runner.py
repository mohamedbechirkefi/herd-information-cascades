# SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
"""Experiment runner: config -> episodes -> rules -> metrics -> summaries, contrasts and checks.

Serialisation is in serialize.py; this module returns plain dictionaries and arrays.
"""

from __future__ import annotations

import itertools
import time
from dataclasses import dataclass
from fractions import Fraction

import numpy as np

from . import RESULT_SCHEMA_VERSION
from .generate import generate_episodes
from .metrics import METRICS, episode_metrics
from .model import Cell, ModelError
from .provenance import REPO_ROOT, config_frozen, config_hash, protocol_frozen
from .reference import analytic_wrong_cascade_probability
from .rules import run_rule
from .schema import load_schema, validate
from .stats import Z99, holm, mean_interval, paired_contrast, wilson_interval

HIST_BINS = 20


class ProtocolGateError(RuntimeError):
    """Raised when a confirmatory configuration is run while its protocol is not frozen."""


@dataclass
class RunOutput:
    result: dict
    raw: dict  # name -> array, per-episode records


def load_config(config: dict) -> dict:
    validate(config, load_schema("config-v1.json"))
    rules = config["rules"]
    if len(set(rules)) != len(rules):
        raise ModelError("rules must be distinct")
    if "independent" not in rules and len(rules) > 1:
        raise ModelError("the independent baseline must be included when social rules are compared")
    ids = [v["id"] for v in config["variations"]]
    if len(set(ids)) != len(ids):
        raise ModelError("variation ids must be distinct")
    if config["label"] == "exploratory" and "exploratory" not in config["output_dir"]:
        raise ModelError("exploratory output_dir must contain 'exploratory' to keep it separate")
    if config["label"] == "confirmatory" and "exploratory" in config["output_dir"]:
        raise ModelError("confirmatory output must not be written to an exploratory folder")
    return config


def gate(config: dict, root=REPO_ROOT) -> str:
    """Refuse confirmatory configs while the protocol is unfrozen. Returns the gate message."""
    if config["label"] != "confirmatory":
        return "exploratory configuration: protocol gate not required"
    frozen, reason = protocol_frozen(config["exp_id"], root)
    if not frozen:
        raise ProtocolGateError(f"refusing to run confirmatory configuration: {reason}. Freezing is the owner's decision (G-FREEZE).")
    ok, why = config_frozen(config, root)
    if not ok:
        raise ProtocolGateError(f"refusing to run confirmatory configuration: {why}. Freezing is the owner's decision (G-FREEZE).")
    return f"{reason}; {why}"


def apply_holm(contrasts: list[dict]) -> None:
    """Holm adjustment within each variation (amendment A-3, owner-approved 2026-11-24).

    A structurally degenerate contrast (every paired difference identical, so zero variance) has no
    test statistic. It is excluded from the Holm family and reported as an exact comparison:
    holm_family = False and p_holm = None. The family of a variation is its non-degenerate contrasts.
    """
    for variation in {c["variation"] for c in contrasts}:
        group = [c for c in contrasts if c["variation"] == variation]
        family = [c for c in group if not c["degenerate"]]
        for c in group:
            c["holm_family"] = not c["degenerate"]
            c["p_holm"] = None
        for c, adj in zip(family, holm([c["p_value"] for c in family])):
            c["p_holm"] = adj


def cells(config: dict):
    for variation in config["variations"]:
        for q, net, v in itertools.product(config["q"], config["networks"], config["visibility"]):
            yield variation["id"], Cell(q=float(q), network=net, v=float(v), n_agents=int(variation["n_agents"]),
                                        tie_rule=variation["tie_rule"])


def run(config: dict, root=REPO_ROOT) -> RunOutput:
    config = load_config(config)
    gate(config, root)
    rules = config["rules"]
    seeds = config["seeds"]
    n_ep = config["episodes_per_seed"]
    arms, contrasts, checks, failures, per_cell_timing = [], [], [], [], []
    raw: dict[str, np.ndarray] = {}
    decisions = 0
    sim_total = 0.0
    t_analysis = 0.0
    for variation, cell in cells(config):
        per_rule = {r: {m: [] for m in METRICS} for r in rules}
        per_rule_seed_mean = {r: {m: [] for m in METRICS} for r in rules}
        per_rule_near = {r: 0 for r in rules}
        per_rule_time = {r: 0.0 for r in rules}
        extra = {"actions": {r: [] for r in rules}, "posterior_dev": [], "bayes_cascades": 0,
                 "agents_correct_ind": 0, "agents_total": 0, "independent_cascades": 0}
        cell_ok = True
        for seed in seeds:
            try:
                ep = generate_episodes(cell, seed, n_ep)
                for r in rules:
                    t0 = time.perf_counter()
                    out = run_rule(r, ep, cell)
                    per_rule_time[r] += time.perf_counter() - t0
                    mets = episode_metrics(ep.theta, out.actions, out.cascade)
                    for m in METRICS:
                        per_rule[r][m].append(mets[m])
                        per_rule_seed_mean[r][m].append(float(mets[m].mean()))
                    per_rule_near[r] += out.near_ties
                    extra["actions"][r].append(out.actions)
                    if r == "bayesian":
                        extra["posterior_dev"].append(float(np.max(np.abs(out.posterior - 0.5))))
                        extra["bayes_cascades"] += int(out.cascade.sum())
                    if r == "independent":
                        extra["agents_correct_ind"] += int((out.actions == ep.theta[:, None]).sum())
                        extra["agents_total"] += int(out.actions.size)
                        extra["independent_cascades"] += int(out.cascade.sum())
                decisions += len(rules) * n_ep * cell.n_agents
            except Exception as exc:  # recorded, never silently dropped
                failures.append({"variation": variation, "cell": cell.as_dict(), "seed": int(seed),
                                 "error": f"{type(exc).__name__}: {exc}"})
                cell_ok = False
                break
        cell_seconds = sum(per_rule_time.values())
        sim_total += cell_seconds
        per_cell_timing.append({"variation": variation, "cell": cell.as_dict(), "seconds": cell_seconds,
                                "episodes": n_ep * len(seeds)})
        if not cell_ok:
            continue
        t1 = time.perf_counter()
        pooled = {r: {m: np.concatenate(per_rule[r][m]) for m in METRICS} for r in rules}
        tag = f"{variation}|q={cell.q}|{cell.network}|v={cell.v}|N={cell.n_agents}|{cell.tie_rule}"
        for r in rules:
            edges = np.linspace(0.0, 1.0, HIST_BINS + 1)
            counts, _ = np.histogram(pooled[r]["accuracy"], bins=edges)
            arms.append({
                "variation": variation, "rule": r, "cell": cell.as_dict(), "n_episodes": int(pooled[r]["accuracy"].size),
                "seeds": [int(s) for s in seeds],
                "metrics": {m: mean_interval(pooled[r][m]) for m in METRICS},
                "per_seed": {m: per_rule_seed_mean[r][m] for m in METRICS},
                "accuracy_histogram": {"edges": [float(x) for x in edges], "counts": [int(c) for c in counts]},
                "near_ties": int(per_rule_near[r]), "runtime_s": float(per_rule_time[r]),
            })
            for m in METRICS:
                raw[f"{tag}|{r}|{m}"] = pooled[r][m]
        if "independent" in rules:
            for r in [x for x in rules if x != "independent"]:
                c = paired_contrast(pooled[r]["accuracy"], pooled["independent"]["accuracy"],
                                    config["bootstrap"]["resamples"], config["bootstrap"]["seed"])
                seed_means = [a - b for a, b in zip(per_rule_seed_mean[r]["accuracy"], per_rule_seed_mean["independent"]["accuracy"])]
                c.update({"variation": variation, "rule": r, "control": "independent", "cell": cell.as_dict(),
                          "metric": "accuracy", "per_seed_mean": seed_means})
                contrasts.append(c)
        if config["verification"]:
            checks.extend(_checks(variation, cell, rules, pooled, extra, per_rule_near))
        t_analysis += time.perf_counter() - t1
    apply_holm(contrasts)
    result = {
        "schema_version": RESULT_SCHEMA_VERSION, "kind": "herd-result",
        "run_id": config["run_id"], "exp_id": config["exp_id"], "label": config["label"],
        "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "config": config, "config_sha256": config_hash(config),
        "metric_definitions": dict(METRICS),
        "arms": arms, "contrasts": contrasts, "checks": checks, "failures": failures,
        "timing": {"simulation_s": sim_total, "analysis_s": t_analysis, "agent_decisions": int(decisions),
                   "seconds_per_1000_decisions": (1000.0 * sim_total / decisions) if decisions else 0.0,
                   "per_cell": per_cell_timing},
    }
    schema = load_schema("result-v1.json")
    if config["verification"]:
        validate(result, schema)
        result["checks"].append({"id": "C5", "name": "result validates against result-v1 schema", "passed": True,
                                 "observed": "valid", "expected": "valid",
                                 "detail": "validated before export; validated again after this entry was added"})
    validate(result, schema)
    return RunOutput(result=result, raw=raw)


def _checks(variation, cell, rules, pooled, extra, near) -> list[dict]:
    out = []
    base = {"variation": variation, "cell": cell.as_dict()}
    n_ep = pooled[rules[0]]["accuracy"].size
    if "bayesian" in rules and cell.network == "complete" and cell.v == 1.0 and cell.tie_rule == "own" and cell.q > 0.5:
        k = int(pooled["bayesian"]["wrong_cascade_any"].sum())
        expected = float(analytic_wrong_cascade_probability(Fraction(str(cell.q)), cell.n_agents))
        lo, hi = wilson_interval(k, n_ep, Z99)
        out.append({**base, "id": "C1", "name": "analytic wrong-cascade anchor (Bayesian, complete, v=1)", "rule": "bayesian",
                    "passed": bool(lo <= expected <= hi), "observed": k / n_ep, "expected": expected,
                    "detail": f"{k}/{n_ep} episodes with a wrong cascade; Wilson 99% [{lo:.4f}, {hi:.4f}]"})
    if cell.q == 0.5:
        for r in rules:
            s = mean_interval(pooled[r]["accuracy"], Z99)
            out.append({**base, "id": "C2", "name": "zero information: mean accuracy 1/2", "rule": r,
                        "passed": bool(s["ci_low"] <= 0.5 <= s["ci_high"]), "observed": s["mean"], "expected": 0.5,
                        "detail": f"episode-level normal 99% [{s['ci_low']:.4f}, {s['ci_high']:.4f}], n={s['n']}"})
        if "bayesian" in rules:
            dev = max(extra["posterior_dev"]) if extra["posterior_dev"] else 0.0
            ok = dev <= 1e-12 and extra["bayes_cascades"] == 0
            out.append({**base, "id": "C2", "name": "zero information: Bayesian posteriors 1/2 and no cascades", "rule": "bayesian",
                        "passed": bool(ok), "observed": dev, "expected": 0.0,
                        "detail": f"max |posterior - 1/2| = {dev:.3e}; Bayesian cascade agents = {extra['bayes_cascades']}"})
    if "independent" in rules:
        k, n = extra["agents_correct_ind"], extra["agents_total"]
        lo, hi = wilson_interval(k, n, Z99)
        ok = lo <= cell.q <= hi and extra["independent_cascades"] == 0
        out.append({**base, "id": "C3", "name": "independent baseline: agent accuracy q, no cascades", "rule": "independent",
                    "passed": bool(ok), "observed": k / n, "expected": float(cell.q),
                    "detail": f"{k}/{n} correct agent decisions, Wilson 99% [{lo:.4f}, {hi:.4f}]; cascade agents = {extra['independent_cascades']}"})
    # The equivalence is predicted for q > 1/2 only: at q = 1/2 every Bayesian comparison is a tie,
    # while imitators still count observed actions (finding F-2 of the M2 session).
    if {"bayesian", "imitation"} <= set(rules) and cell.network == "complete" and cell.q > 0.5:
        a_b = np.concatenate(extra["actions"]["bayesian"])
        a_i = np.concatenate(extra["actions"]["imitation"])
        diff_ep = int(np.any(a_b != a_i, axis=1).sum())
        if cell.tie_rule == "own":
            out.append({**base, "id": "C4", "name": "complete network: Bayesian and imitation actions identical", "rule": "bayesian,imitation",
                        "passed": diff_ep == 0, "observed": diff_ep, "expected": 0,
                        "detail": f"{diff_ep} of {a_b.shape[0]} episodes differ"})
        else:
            out.append({**base, "id": "C7", "name": "complete network, coin ties: Bayesian vs imitation divergence (diagnostic, no prediction)",
                        "rule": "bayesian,imitation", "passed": True, "observed": diff_ep, "expected": None,
                        "detail": f"{diff_ep} of {a_b.shape[0]} episodes differ; the equivalence is predicted only under own-signal ties"})
    if "bayesian" in rules:
        out.append({**base, "id": "C6", "name": "no near ties in Bayesian comparisons", "rule": "bayesian",
                    "passed": near["bayesian"] == 0, "observed": near["bayesian"], "expected": 0,
                    "detail": "comparisons with relative gap in (1e-9, 1e-6] at realised states"})
    return out
