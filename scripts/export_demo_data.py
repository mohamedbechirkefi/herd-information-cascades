# SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
"""Export the published results for the M5 demo page (demo/public/data/results.json).

Reads committed results only (result.json files, robustness tables, EXP-004 derived tables),
plus the claims register, the experiment registry, the artifact manifest and the limitations
file. Writes the shared template schema ``lab-demo-results`` 1.0.0, with HERD-specific
top-level extensions (``title``, ``run_revisions``, ``contrast_map``, ``cells``).

Every ``display`` and ``interval_display`` string uses the formatting of the generators that
print the manuscript and supplementary tables (``herd.paper`` and ``herd.tables``), so the page
shows the same text as the documents; ``tests/test_demo_export.py`` checks this verbatim.
No timestamps are written, so the output is a pure function of the committed inputs.

  .venv/bin/python scripts/export_demo_data.py          # write the file
  .venv/bin/python scripts/export_demo_data.py --check  # exit 1 if the committed file is stale
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "demo" / "public" / "data" / "results.json"

R1 = [f"results/exploratory/EXP-001-R00{i}" for i in range(1, 6)]
R2 = "results/EXP-002/EXP-002-R001"
R3 = "results/EXP-003/EXP-003-R001"
R4 = "results/exploratory/EXP-004-R001"
D4 = "results/exploratory/EXP-004-derived"
CLAIMS = "research/claims_register.csv"
REGISTRY = "research/experiment_registry.csv"
MANIFEST = "research/publication/artifact_manifest.json"
LIMITATIONS = "research/limitations.md"
NETWORKS = ["complete", "window-2", "window-3"]
RULE_NAMES = {"independent": "Independent", "bayesian": "Bayesian", "imitation": "Imitation"}
UNIT_DELTA = "proportion (paired difference in episode accuracy; 0.01 is one accuracy point)"
VARIATION_LABELS = {"main": "EXP-002 (N=50, own ties)", "V1": "V1 (N=50, coin ties)",
                    "V2": "V2 (N=10, own ties)", "V3": "V3 (N=200, own ties)"}


class ExportError(RuntimeError):
    """Raised when a committed input is missing or inconsistent (the export fails closed)."""


def _read(rel: str) -> bytes:
    path = REPO / rel
    if not path.is_file():
        raise ExportError(f"missing committed input {rel}")
    return path.read_bytes()


class Inputs:
    """Reads each input once and records its SHA-256."""

    def __init__(self) -> None:
        self.hashes: dict[str, str] = {}

    def raw(self, rel: str) -> bytes:
        data = _read(rel)
        self.hashes[rel] = hashlib.sha256(data).hexdigest()
        return data

    def json(self, rel: str) -> dict:
        return json.loads(self.raw(rel).decode("utf-8"))

    def csv(self, rel: str) -> list[dict]:
        return list(csv.DictReader(self.raw(rel).decode("utf-8").splitlines()))

    def text(self, rel: str) -> str:
        return self.raw(rel).decode("utf-8")


def f4(x: float) -> str:
    return f"{x:.4f}"


def ci4(lo: float, hi: float) -> str:
    return f"[{lo:.4f}, {hi:.4f}]"


def ci_d(lo: float, hi: float, d: int) -> str:
    return f"[{lo:.{d}f}, {hi:.{d}f}]"


def estimate(label: str, value: float, lo, hi, level, unit: str, display: str, interval_display) -> dict:
    return {"label": label, "estimate": float(value), "ci_low": None if lo is None else float(lo),
            "ci_high": None if hi is None else float(hi), "ci_level": level, "unit": unit,
            "display": display, "interval_display": interval_display}


def cell_label(q: float, net: str, v: float) -> str:
    return f"q = {q:g}, {net}, v = {v:g}"


def holm_sig(c: dict) -> bool:
    return bool(c["holm_family"] and c["p_holm"] is not None and c["p_holm"] < 0.05)


def cell_key(c: dict) -> tuple:
    cell = c["cell"]
    return (cell["q"], NETWORKS.index(cell["network"]), -cell["v"])


def claim_map(rows: list[dict]) -> dict[str, list[str]]:
    """Experiment id -> claim ids, from the result_id column of the claims register."""
    out: dict[str, list[str]] = {f"EXP-00{i}": [] for i in range(1, 5)}
    for r in rows:
        rid = r["result_id"]
        exps = {"EXP-004"} if "derived, EXP-004" in rid else set(re.findall(r"(EXP-\d{3})-R\d{3}", rid))
        if not exps:
            raise ExportError(f"claim {r['claim_id']} has no result id")
        for e in sorted(exps):
            out[e].append(r["claim_id"])
    return out


def strip_md(text: str) -> str:
    """Plain text for the page: drop bold markers, backticks and simple inline math."""
    t = text.replace("**", "").replace("`", "")
    t = re.sub(r"\$([^$]*)\$", lambda m: m.group(1), t)
    for a, b in ((r"\leq", "<="), (r"\in", "in"), (r"\{", "{"), (r"\}", "}"), (r"\dots", "...")):
        t = t.replace(a, b)
    return re.sub(r"\s+", " ", t).strip()


def limitations(text: str) -> list[str]:
    items = re.findall(r"^\d+\.\s+(.*)$", text, flags=re.M)
    if not items:
        raise ExportError("no numbered limitation found")
    return [strip_md(i) for i in items]


def contrast_rows(res: dict, exp_id: str, label: str, robustness: dict | None) -> list[dict]:
    rows = []
    for c in sorted(res["contrasts"], key=lambda c: (c["variation"], cell_key(c), c["rule"])):
        cell = c["cell"]
        if c["metric"] != "accuracy" or c["control"] != "independent":
            raise ExportError(f"unexpected contrast in {res['run_id']}")
        status = "Holm-significant" if holm_sig(c) else "not Holm-significant"
        if robustness is not None:
            r = robustness[(c["variation"], c["rule"], cell["q"], cell["network"], cell["v"])]
            if abs(float(r["delta"]) - c["mean"]) > 1e-12:
                raise ExportError(f"robustness table disagrees with {res['run_id']}")
            status = r["status"]
        rows.append({
            "run_id": res["run_id"], "exp_id": exp_id, "label": label, "variation": c["variation"],
            "variation_label": VARIATION_LABELS[c["variation"]], "rule": c["rule"], "q": cell["q"],
            "network": cell["network"], "v": cell["v"], "n_agents": cell["n_agents"], "tie_rule": cell["tie_rule"],
            "estimate": c["mean"], "ci_low": c["ci_low"], "ci_high": c["ci_high"], "ci_level": 0.95,
            "display": f4(c["mean"]), "interval_display": ci4(c["ci_low"], c["ci_high"]),
            "holm_significant": holm_sig(c), "status": status,
        })
    return rows


def robustness_index(rows: list[dict]) -> dict:
    return {(r["variation"], r["rule"], float(r["q"]), r["network"], float(r["v"])): r for r in rows}


def build() -> dict:
    inp = Inputs()
    runs1 = [inp.json(f"{d}/result.json") for d in R1]
    res2, res3, res4 = (inp.json(f"{d}/result.json") for d in (R2, R3, R4))
    man = {d: inp.json(f"{d}/run_manifest.json") for d in R1 + [R2, R3, R4]}
    rob3 = robustness_index(inp.csv(f"{R3}/tables/robustness_vs_EXP-002-R001.csv"))
    rob4 = robustness_index(inp.csv(f"{R4}/tables/robustness_vs_EXP-002-R001.csv"))
    q2 = {(float(r["q"]), r["network"], float(r["v"]), r["rule"]): r
          for r in inp.csv(f"{D4}/q2_distribution.csv") if r["variation"] == "main"}
    q3 = [r for r in inp.csv(f"{D4}/q3_imitation_minus_bayesian.csv") if r["variation"] == "main" and r["network"] != "complete"]
    derived = inp.json(f"{D4}/summary.json")
    claims = inp.csv(CLAIMS)
    registry = {r["exp_id"]: r for r in inp.csv(REGISTRY)}
    manifest = inp.json(MANIFEST)
    lims = limitations(inp.text(LIMITATIONS))
    cmap = claim_map(claims)

    for d, m in man.items():
        if m["git"]["dirty"]:
            raise ExportError(f"{d} was produced from a dirty tree")
    listed = {a["result_path"] for a in manifest["artifacts"] if a.get("result_path")}
    for d in R1 + [R2, R3, R4]:
        if f"{d}/result.json" not in listed:
            raise ExportError(f"{d}/result.json is not in the artifact manifest")
    for res in runs1 + [res2, res3, res4]:
        if res["failures"]:
            raise ExportError(f"{res['run_id']} has failed cells")

    # ---- EXP-001 (exploratory verification) ----
    est1 = []
    for res in runs1:
        n, k = len(res["checks"]), sum(c["passed"] for c in res["checks"])
        est1.append(estimate(f"{res['run_id']}: verification checks passed", k, None, None, None, "checks",
                             f"{k} of {n}", None))
    all_pass1 = all(e["estimate"] == len(r["checks"]) for e, r in zip(est1, runs1))
    exp1 = {
        "id": "EXP-001", "title": registry["EXP-001"]["title"], "status": "exploratory, complete",
        "verdict": "Verification passed (exploratory; licenses EXP-002)" if all_pass1 else "Verification failed",
        "estimates": est1, "claim_ids": cmap["EXP-001"], "report_path": "research/experiments/EXP-001/report.md",
        "notes": ["Exploratory by design: its numbers are never evidence for a study hypothesis.",
                  "Under window-1, both social rules reproduced the independent baseline exactly, which motivated amendment A-1.",
                  "Check counts are exact; they carry no sampling interval."],
    }

    # ---- EXP-002 (confirmatory) ----
    con2 = contrast_rows(res2, "EXP-002", "confirmatory", None)
    n_sig = sum(r["holm_significant"] for r in con2)
    n_pos = sum(r["estimate"] > 0 for r in con2)
    below = [r for r in con2 if r["estimate"] < 0.01]
    imit_neg = [r for r in con2 if r["rule"] == "imitation" and r["network"] != "complete" and r["estimate"] < 0 and r["holm_significant"]]
    est2 = [estimate(f"{RULE_NAMES[r['rule']]}, {cell_label(r['q'], r['network'], r['v'])}", r["estimate"], r["ci_low"],
                     r["ci_high"], 0.95, UNIT_DELTA, r["display"], r["interval_display"]) for r in con2]
    for c in sorted((c for c in res2["checks"] if c["id"] == "C1"), key=lambda c: c["cell"]["q"]):
        m = re.search(r"(\d+)/(\d+) episodes.*Wilson 99% \[([0-9.]+), ([0-9.]+)\]", c["detail"])
        if m is None:
            raise ExportError("unexpected C1 detail text")
        est2.append(estimate(f"Check C1, q = {c['cell']['q']:g}: observed wrong-cascade share (analytic value {c['expected']:.4f})",
                             c["observed"], float(m.group(3)), float(m.group(4)), 0.99, "proportion of episodes",
                             f4(c["observed"]), f"Wilson 99% [{m.group(3)}, {m.group(4)}]"))
    checks2 = sum(c["passed"] for c in res2["checks"])
    exp2 = {
        "id": "EXP-002", "title": registry["EXP-002"]["title"],
        "status": f"confirmatory, complete (run EXP-002-R001; 0 failed cells; {checks2} of {len(res2['checks'])} checks passed)",
        "verdict": (f"H0 rejected for all {n_sig} of {len(con2)} contrasts ({n_pos} positive); H1 supported. "
                    "Pre-stated expectation that imitation lowers accuracy in a window-k cell at low q: "
                    + ("contradicted." if not imit_neg else "supported.")),
        "estimates": est2, "claim_ids": cmap["EXP-002"], "report_path": "research/experiments/EXP-002/report.md",
        "notes": [f"{len(con2) - len(below)} of the {len(con2)} contrasts exceed the protocol's practical threshold of 0.01; "
                  f"{len(below)} are below it (both at q = 0.55, window-2, v = 0.5)." if all(r["q"] == 0.55 and r["network"] == "window-2" and r["v"] == 0.5 for r in below) else "",
                  "Intervals are unadjusted 95% normal intervals at the episode level; decisions use Holm-adjusted p-values.",
                  "Each contrast pairs 10,000 episodes of 50 agents; own-signal ties."],
    }
    exp2["notes"] = [n for n in exp2["notes"] if n]

    # ---- EXP-003 (confirmatory sensitivity) ----
    con3 = contrast_rows(res3, "EXP-003", "confirmatory", rob3)
    status3 = {s: sum(r["status"] == s for r in con3) for s in ("robust", "lost significance", "sign reversed")}
    lost = [r for r in con3 if r["status"] != "robust"]
    est3 = [estimate("Robust comparisons (same sign, Holm-significant), all three variations", status3["robust"], None, None, None,
                     f"of {len(con3)} comparisons", f"{status3['robust']} of {len(con3)}", None)]
    for r in lost:
        est3.append(estimate(f"{RULE_NAMES[r['rule']]}, {cell_label(r['q'], r['network'], r['v'])}, {r['variation_label']} ({r['status']})",
                             r["estimate"], r["ci_low"], r["ci_high"], 0.95, UNIT_DELTA, r["display"], r["interval_display"]))
    for r in con3:
        if r["rule"] == "bayesian" and r["q"] == 0.7 and r["network"] == "complete" and r["v"] == 1.0 and r["variation"] in ("V2", "V3"):
            est3.append(estimate(f"Bayesian, {cell_label(r['q'], r['network'], r['v'])}, {r['variation_label']} (horizon example)",
                                 r["estimate"], r["ci_low"], r["ci_high"], 0.95, UNIT_DELTA, r["display"], r["interval_display"]))
    exp3 = {
        "id": "EXP-003", "title": registry["EXP-003"]["title"],
        "status": f"confirmatory, complete (run EXP-003-R001; 0 failed cells; {sum(c['passed'] for c in res3['checks'])} of {len(res3['checks'])} checks passed)",
        "verdict": (f"{status3['robust']} of {len(con3)} comparisons robust, {status3['sign reversed']} reversed, "
                    f"{status3['lost significance']} lost significance: by the frozen rule, "
                    + (f"{len(lost)} EXP-002 conclusions are convention-dependent." if lost else "no EXP-002 conclusion is convention-dependent.")),
        "estimates": est3, "claim_ids": cmap["EXP-003"], "report_path": "research/experiments/EXP-003/report.md",
        "notes": ["Loss of significance is not evidence of a zero effect.",
                  "Coin-flip ties reduced every gain in this grid; the EXP-002 magnitudes belong to the own-signal tie convention."],
    }

    # ---- EXP-004 (exploratory, post hoc) ----
    con4 = contrast_rows(res4, "EXP-004", "exploratory", rob4)
    robust4 = sum(r["status"] == "robust" for r in con4)
    est4 = [estimate(f"Q1: robust comparisons at q = 0.60 and 0.80 (V1 to V3, of {len(con4)}), by the EXP-003 rule applied post hoc", robust4,
                     None, None, None, f"of {len(con4)} comparisons", str(robust4), None)]
    q3.sort(key=lambda r: (float(r["q"]), NETWORKS.index(r["network"]), -float(r["v"])))
    for r in q3:
        est4.append(estimate(f"Q3: imitation minus Bayesian, {cell_label(float(r['q']), r['network'], float(r['v']))}",
                             float(r["imitation_minus_bayesian"]), float(r["ci_low"]), float(r["ci_high"]), 0.95,
                             "proportion (paired difference in episode accuracy)", f4(float(r["imitation_minus_bayesian"])),
                             ci4(float(r["ci_low"]), float(r["ci_high"]))))
    sb = [float(r["share_below_baseline"]) for r in q2.values() if r["rule"] != "independent"]
    est4.append(estimate("Q2: smallest share of episodes below the independent baseline", min(sb), None, None, None,
                         "proportion of episodes (descriptive, no interval computed)", f"{min(sb):.3f}", None))
    est4.append(estimate("Q2: largest share of episodes below the independent baseline", max(sb), None, None, None,
                         "proportion of episodes (descriptive, no interval computed)", f"{max(sb):.3f}", None))
    if abs(min(sb) - derived["q2_exp002"]["share_below_baseline_min"]) > 1e-12:
        raise ExportError("q2 distribution disagrees with the EXP-004 summary")
    exp4 = {
        "id": "EXP-004", "title": registry["EXP-004"]["title"], "status": "exploratory, post hoc, complete",
        "verdict": ("No frozen rule (exploratory; designed after the confirmatory results were seen). "
                    f"The EXP-003 rule applied post hoc: {robust4} of {len(con4)} comparisons robust. It changes no frozen verdict."),
        "estimates": est4, "claim_ids": cmap["EXP-004"], "report_path": "research/experiments/EXP-004/report.md",
        "notes": ["Exploratory and post hoc: none of these numbers is evidence for H1 of EXP-002 or EXP-003.",
                  "Q3 intervals are unadjusted 95% normal intervals with no multiplicity control."],
    }

    # ---- Extension: per-cell data for the distribution view (EXP-002 main arms) ----
    cells = []
    arms = {(a["cell"]["q"], a["cell"]["network"], a["cell"]["v"], a["rule"]): a for a in res2["arms"] if a["variation"] == "main"}
    for q, net, v in sorted({(k[0], k[1], k[2]) for k in arms}, key=lambda k: (k[0], NETWORKS.index(k[1]), -k[2])):
        out_arms = []
        for rule in ("independent", "bayesian", "imitation"):
            a = arms[(q, net, v, rule)]
            m = a["metrics"]
            h = a["accuracy_histogram"]
            if sum(h["counts"]) != a["n_episodes"]:
                raise ExportError("histogram counts do not sum to the episode count")
            arm = {
                "rule": rule, "n_episodes": a["n_episodes"], "edges": h["edges"], "counts": h["counts"],
                "accuracy": estimate("Mean episode accuracy", m["accuracy"]["mean"], m["accuracy"]["ci_low"], m["accuracy"]["ci_high"],
                                     0.95, "proportion", f"{m['accuracy']['mean']:.3f}",
                                     ci_d(m["accuracy"]["ci_low"], m["accuracy"]["ci_high"], 3)),
                "wrong_cascade": estimate("Wrong-cascade probability", m["wrong_cascade_any"]["mean"], m["wrong_cascade_any"]["ci_low"],
                                          m["wrong_cascade_any"]["ci_high"], 0.95, "proportion of episodes",
                                          f"{m['wrong_cascade_any']['mean']:.3f}",
                                          ci_d(m["wrong_cascade_any"]["ci_low"], m["wrong_cascade_any"]["ci_high"], 3)),
                "longest_wrong_run": estimate("Mean longest run of wrong actions", m["longest_wrong_run"]["mean"],
                                              m["longest_wrong_run"]["ci_low"], m["longest_wrong_run"]["ci_high"], 0.95, "agents",
                                              f"{m['longest_wrong_run']['mean']:.2f}",
                                              ci_d(m["longest_wrong_run"]["ci_low"], m["longest_wrong_run"]["ci_high"], 2)),
                "share_below_baseline": None,
            }
            if rule != "independent":
                d = q2[(q, net, v, rule)]
                arm["share_below_baseline"] = estimate(
                    "Share of episodes below the independent baseline (exploratory, EXP-004)", float(d["share_below_baseline"]),
                    None, None, None, "proportion of episodes (descriptive, no interval computed)", f"{float(d['share_below_baseline']):.3f}", None)
            out_arms.append(arm)
        cells.append({"q": q, "network": net, "v": v, "n_agents": 50, "arms": out_arms})

    revisions = []
    for d in R1 + [R2, R3, R4]:
        m = man[d]
        revisions.append({"run_id": m["run_id"], "exp_id": m["exp_id"], "label": m["label"],
                          "code_revision": m["git"]["revision"], "result_path": f"{d}/result.json"})
    revisions.append({"run_id": "EXP-004-derived", "exp_id": "EXP-004", "label": "exploratory",
                      "code_revision": derived["git"]["revision"], "result_path": f"{D4}/summary.json"})

    if man[R2]["git"]["revision"] != man[R3]["git"]["revision"]:
        raise ExportError("confirmatory runs were produced at different revisions")

    return {
        "schema": "lab-demo-results",
        "schema_version": "1.0.0",
        "project": "HERD",
        "question": "When does social information improve binary decisions, and when does it generate cascades of errors?",
        "status_label": ("Independent research manuscript / preprint draft, not peer-reviewed (v1.0, 2026-11-25). "
                         "Simulation with synthetic agents only. EXP-002 and EXP-003 are confirmatory (protocols frozen 2026-11-24); "
                         "EXP-001 and EXP-004 are exploratory. The owner's full-text review of the manuscript is pending."),
        "code_revision": man[R2]["git"]["revision"],
        "sources": [{"path": p, "sha256": h} for p, h in sorted(inp.hashes.items())],
        "experiments": [exp1, exp2, exp3, exp4],
        "assumptions": assumptions(res2, res3),
        "limitations": lims,
        "title": "Higher average accuracy, frequent locked-in errors: a simulation study of Bayesian and naive social learning",
        "run_revisions": revisions,
        "contrast_map": con2 + con3 + con4,
        "cells": cells,
    }


def assumptions(res2: dict, res3: dict) -> list[dict]:
    c2, c3 = res2["config"], res3["config"]
    src2, src3 = "experiments/EXP-002.json (frozen v1.0)", "experiments/EXP-003.json (frozen v1.0)"
    var2 = c2["variations"][0]
    return [
        {"name": "Hidden state", "value": "binary, each value with prior probability 1/2", "source": "manuscript section 3"},
        {"name": "Private signal", "value": "binary, equal to the hidden state with probability q, independent across agents given the state", "source": "manuscript section 3"},
        {"name": "Signal precision q (EXP-002)", "value": ", ".join(f"{q:.2f}" for q in c2["q"]), "source": src2},
        {"name": "Observation networks", "value": "complete history; last k predecessors (window-k), k in {2, 3}", "source": src2},
        {"name": "Visibility v", "value": ", ".join(f"{v:g}" for v in c2["visibility"]) + " (each action publicly recorded with probability v; the pattern is common knowledge)", "source": src2},
        {"name": "Agents per episode N (EXP-002)", "value": str(var2["n_agents"]), "source": src2},
        {"name": "Tie rule (EXP-002)", "value": "ties follow the own signal", "source": src2},
        {"name": "Sensitivity variations (EXP-003)", "value": "; ".join(f"{v['id']}: N = {v['n_agents']}, {v['tie_rule']} ties" for v in c3["variations"]), "source": src3},
        {"name": "Seeds and episodes", "value": f"master seeds {c2['seeds'][0]} to {c2['seeds'][-1]}, {c2['episodes_per_seed']:,} episodes per seed and cell", "source": src2},
        {"name": "Common random numbers", "value": "within a seed and cell, every rule sees the same state, signals and visibility pattern", "source": "manuscript section 4.1"},
        {"name": "Rules", "value": "independent (baseline): follow the own signal; Bayesian: exact posterior, all agents commonly known to be Bayesian; imitation: count observed actions as independent signals", "source": "manuscript section 3"},
        {"name": "Smallest practically meaningful effect", "value": "0.01 on the proportion scale (stated in the sample-size rationale, not a decision rule)", "source": "research/protocol.md section 5"},
        {"name": "Multiplicity", "value": "Holm adjustment at familywise 0.05 within each experiment or variation; intervals unadjusted", "source": "research/protocol.md section 5 (amendment A-4)"},
    ]


def serialize(data: dict) -> str:
    return json.dumps(data, indent=1, ensure_ascii=False) + "\n"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="export_demo_data")
    p.add_argument("--check", action="store_true", help="fail if the committed file differs from a fresh export")
    a = p.parse_args(argv)
    text = serialize(build())
    if a.check:
        same = OUT.is_file() and OUT.read_text(encoding="utf-8") == text
        print("results.json is up to date" if same else "results.json is stale")
        return 0 if same else 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    data = json.loads(text)
    print(f"wrote {OUT.relative_to(REPO)}: {len(data['experiments'])} experiments, "
          f"{sum(len(e['estimates']) for e in data['experiments'])} estimates, {len(data['contrast_map'])} contrasts, "
          f"{len(data['cells'])} cells, {len(data['sources'])} sources")
    return 0


if __name__ == "__main__":
    sys.exit(main())
