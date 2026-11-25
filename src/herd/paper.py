# SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
"""Manuscript and supplementary tables, generated once from committed results (master prompt 11.5).

Each table sits in the Markdown between the markers
  <!-- BEGIN GENERATED TAB-NNN -->  and  <!-- END GENERATED TAB-NNN -->
`fill` rewrites the text between the markers from the result files; `check` fails if any table in the
documents differs from what the result files give (a stale table).

  python -m herd.paper fill
  python -m herd.paper check
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

from .provenance import REPO_ROOT
from .serialize import read_result
from .tables import contrasts_table, robustness_table, secondary_table

R2 = "results/EXP-002/EXP-002-R001"
R3 = "results/EXP-003/EXP-003-R001"
R4 = "results/exploratory/EXP-004-R001"
D4 = "results/exploratory/EXP-004-derived"
DOCUMENTS = ["research/paper/manuscript.md", "research/paper/supplementary.md"]
NETWORKS = ["complete", "window-2", "window-3"]

# Artifact provenance for the manifest: table id -> (run ids, source files, generator function name).
SOURCES = {
    "TAB-001": (["EXP-002-R001"], [f"{R2}/result.json"], "tab_primary"),
    "TAB-002": (["EXP-003-R001", "EXP-004-R001"], [f"{R2}/result.json", f"{R3}/result.json", f"{R4}/result.json",
                f"{R3}/tables/robustness_vs_EXP-002-R001.csv", f"{R4}/tables/robustness_vs_EXP-002-R001.csv"], "tab_sensitivity"),
    "TAB-003": (["EXP-002-R001"], [f"{R2}/result.json", f"{D4}/q2_distribution.csv"], "tab_distribution"),
    "TAB-004": (["EXP-002-R001"], [f"{D4}/q3_imitation_minus_bayesian.csv"], "tab_rule_difference"),
    "TAB-005": (["EXP-002-R001"], [f"{D4}/q4_quantity.csv"], "tab_quantity"),
    "TAB-S01": (["EXP-002-R001"], [f"{R2}/result.json"], "contrasts_table"),
    "TAB-S02": (["EXP-003-R001"], [f"{R3}/tables/robustness_vs_EXP-002-R001.csv"], "robustness_table"),
    "TAB-S03": (["EXP-004-R001"], [f"{R4}/tables/robustness_vs_EXP-002-R001.csv"], "robustness_table"),
    "TAB-S04": (["EXP-002-R001"], [f"{R2}/result.json"], "secondary_table"),
}


def _res(path: str) -> dict:
    return read_result(REPO_ROOT / path / "result.json")


def _csv(path: str) -> list[dict]:
    with open(REPO_ROOT / path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _ci(m: float, lo: float, hi: float, d: int = 4) -> str:
    return f"{m:.{d}f} [{lo:.{d}f}, {hi:.{d}f}]"


def _p(x: float) -> str:
    return "< 1e-15" if x < 1e-15 else f"{x:.2g}"


def _cells(res: dict) -> list[tuple]:
    return sorted({(c["cell"]["q"], c["cell"]["network"], c["cell"]["v"]) for c in res["contrasts"]},
                  key=lambda k: (k[0], NETWORKS.index(k[1]), -k[2]))


def tab_primary() -> str:
    res = _res(R2)
    by = {(c["cell"]["q"], c["cell"]["network"], c["cell"]["v"], c["rule"]): c for c in res["contrasts"]}
    out = ["| q | Network | v | Bayesian Delta [95% CI] | Imitation Delta [95% CI] |", "|---|---|---|---|---|"]
    for q, net, v in _cells(res):
        b, i = by[(q, net, v, "bayesian")], by[(q, net, v, "imitation")]
        out.append(f"| {q:g} | {net} | {v:g} | {_ci(b['mean'], b['ci_low'], b['ci_high'])} | {_ci(i['mean'], i['ci_low'], i['ci_high'])} |")
    return "\n".join(out)


def tab_sensitivity() -> str:
    out = ["| Source | Label | Variation | q values | Compared | Robust | Lost significance | Sign reversed | Delta range | Largest Holm p | Positive in all 10 seeds |",
           "|---|---|---|---|---|---|---|---|---|---|---|"]
    for run, label, rob in ((R3, "confirmatory", f"{R3}/tables/robustness_vs_EXP-002-R001.csv"),
                            (R4, "exploratory", f"{R4}/tables/robustness_vs_EXP-002-R001.csv")):
        res, rows = _res(run), _csv(rob)
        for var in sorted({c["variation"] for c in res["contrasts"]}):
            cs = [c for c in res["contrasts"] if c["variation"] == var]
            rr = [r for r in rows if r["variation"] == var]
            cell = cs[0]["cell"]
            qs = ", ".join(f"{q:.2f}" for q in sorted({c["cell"]["q"] for c in cs}))
            st = {s: sum(r["status"] == s for r in rr) for s in ("robust", "lost significance", "sign reversed")}
            lo, hi = min(c["mean"] for c in cs), max(c["mean"] for c in cs)
            allpos = sum(all(x > 0 for x in c["per_seed_mean"]) for c in cs)
            out.append(f"| {res['run_id']} | {label} | {var} (N={cell['n_agents']}, {cell['tie_rule']} ties) | {qs} | {len(rr)} | "
                       f"{st['robust']} | {st['lost significance']} | {st['sign reversed']} | {lo:.4f} to {hi:.4f} | "
                       f"{_p(max(c['p_holm'] for c in cs))} | {allpos} of {len(cs)} |")
    return "\n".join(out)


def tab_distribution() -> str:
    res = _res(R2)
    arms = {(a["cell"]["q"], a["cell"]["network"], a["cell"]["v"], a["rule"]): a for a in res["arms"] if a["variation"] == "main"}
    dist = {(float(r["q"]), r["network"], float(r["v"]), r["rule"]): r for r in _csv(f"{D4}/q2_distribution.csv")
            if r["variation"] == "main"}
    out = ["| q | Network | v | Wrong-cascade probability, B / I | Share of episodes below baseline, B / I (exploratory) | Last-agent Delta, B / I (exploratory) |",
           "|---|---|---|---|---|---|"]
    for q, net, v in _cells(res):
        wc = " / ".join(f"{arms[(q, net, v, r)]['metrics']['wrong_cascade_any']['mean']:.3f}" for r in ("bayesian", "imitation"))
        sb = " / ".join(f"{float(dist[(q, net, v, r)]['share_below_baseline']):.3f}" for r in ("bayesian", "imitation"))
        la = " / ".join(f"{float(dist[(q, net, v, r)]['delta_last_agent']):.4f}" for r in ("bayesian", "imitation"))
        out.append(f"| {q:g} | {net} | {v:g} | {wc} | {sb} | {la} |")
    return "\n".join(out)


def tab_rule_difference() -> str:
    rows = [r for r in _csv(f"{D4}/q3_imitation_minus_bayesian.csv") if r["variation"] == "main" and r["network"] != "complete"]
    rows.sort(key=lambda r: (float(r["q"]), NETWORKS.index(r["network"]), -float(r["v"])))
    out = ["| q | Network | v | Imitation minus Bayesian [95% CI] | Share of episodes where the rules differ |", "|---|---|---|---|---|"]
    for r in rows:
        out.append(f"| {float(r['q']):g} | {r['network']} | {float(r['v']):g} | "
                   f"{_ci(float(r['imitation_minus_bayesian']), float(r['ci_low']), float(r['ci_high']))} | {float(r['share_episodes_differ']):.3f} |")
    return "\n".join(out)


def tab_quantity() -> str:
    rows = [r for r in _csv(f"{D4}/q4_quantity.csv") if r["rule"] == "bayesian"]
    qs = sorted({float(r["q"]) for r in rows})
    keys = sorted({(r["network"], float(r["v"]), float(r["mean_expected_observed_actions"])) for r in rows}, key=lambda k: k[2])
    out = ["| Network | v | Mean expected observed actions per agent | " + " | ".join(f"Bayesian Delta, q = {q:.2f}" for q in qs) + " |",
           "|---|---|---|" + "---|" * len(qs)]
    for net, v, e in keys:
        d = {float(r["q"]): float(r["delta"]) for r in rows if r["network"] == net and float(r["v"]) == v}
        out.append(f"| {net} | {v:g} | {e:.2f} | " + " | ".join(f"{d[q]:.4f}" for q in qs) + " |")
    return "\n".join(out)


def generators() -> dict:
    return {
        "TAB-001": tab_primary, "TAB-002": tab_sensitivity, "TAB-003": tab_distribution,
        "TAB-004": tab_rule_difference, "TAB-005": tab_quantity,
        "TAB-S01": lambda: contrasts_table(_res(R2)),
        "TAB-S02": lambda: robustness_table(REPO_ROOT / R3 / "tables/robustness_vs_EXP-002-R001.csv"),
        "TAB-S03": lambda: robustness_table(REPO_ROOT / R4 / "tables/robustness_vs_EXP-002-R001.csv"),
        "TAB-S04": lambda: secondary_table(_res(R2)),
    }


BLOCK = re.compile(r"(<!-- BEGIN GENERATED (TAB-[A-Z0-9]+) -->\n)(.*?)(<!-- END GENERATED \2 -->)", re.S)


def render(text: str, gens: dict) -> str:
    return BLOCK.sub(lambda m: m.group(1) + gens[m.group(2)]() + "\n" + m.group(4), text)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="herd.paper")
    p.add_argument("mode", choices=["fill", "check"])
    a = p.parse_args(argv)
    gens, stale = generators(), []
    for doc in DOCUMENTS:
        path = REPO_ROOT / doc
        text = path.read_text(encoding="utf-8")
        new = render(text, gens)
        ids = [m.group(2) for m in BLOCK.finditer(text)]
        if a.mode == "fill":
            path.write_text(new, encoding="utf-8")
            print(f"{doc}: {len(ids)} generated tables ({', '.join(ids)})")
        elif new != text:
            stale.append(doc)
    if a.mode == "check":
        print("stale tables in: " + ", ".join(stale) if stale else "all generated tables match the result files")
        return 1 if stale else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
