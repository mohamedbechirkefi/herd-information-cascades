# SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
"""Markdown tables for the 11.3 experiment reports, generated from a run's result.json (never typed by hand).

  python -m herd.tables contrasts --run results/EXP-002/EXP-002-R001
  python -m herd.tables secondary --run results/EXP-002/EXP-002-R001
  python -m herd.tables robustness --csv results/EXP-003/EXP-003-R001/tables/robustness_vs_EXP-002-R001.csv
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from .serialize import read_result


def _p(x) -> str:
    if x is None:
        return "n/a"
    x = float(x)
    return "< 1e-15" if x < 1e-15 else f"{x:.2g}"


def contrasts_table(res: dict) -> str:
    out = ["| Variation | q | Network | v | Rule | n | Delta | 95% CI | Bootstrap 95% CI | Holm p | Holm-significant |",
           "|---|---|---|---|---|---|---|---|---|---|---|"]
    for c in res["contrasts"]:
        cell = c["cell"]
        sig = "yes" if (c["holm_family"] and c["p_holm"] is not None and c["p_holm"] < 0.05) else "no"
        out.append(f"| {c['variation']} (N={cell['n_agents']}, {cell['tie_rule']}) | {cell['q']:g} | {cell['network']} | {cell['v']:g} | "
                   f"{c['rule']} | {c['n']} | {c['mean']:.4f} | [{c['ci_low']:.4f}, {c['ci_high']:.4f}] | "
                   f"[{c['boot_ci_low']:.4f}, {c['boot_ci_high']:.4f}] | {_p(c['p_holm'])} | {sig} |")
    return "\n".join(out)


def secondary_table(res: dict) -> str:
    out = ["| Variation | q | Network | v | Rule | Accuracy | Wrong cascade | Longest wrong run | Informative share | Last agent |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    for a in res["arms"]:
        cell, m = a["cell"], a["metrics"]

        def f(k, d=3):
            return f"{m[k]['mean']:.{d}f} [{m[k]['ci_low']:.{d}f}, {m[k]['ci_high']:.{d}f}]"

        out.append(f"| {a['variation']} | {cell['q']:g} | {cell['network']} | {cell['v']:g} | {a['rule']} | {f('accuracy')} | "
                   f"{f('wrong_cascade_any')} | {f('longest_wrong_run', 2)} | {f('informative_share')} | {f('last_agent_accuracy')} |")
    return "\n".join(out)


def robustness_table(path: Path) -> str:
    out = ["| Variation | q | Network | v | Rule | EXP-002 Delta | Variation Delta | 95% CI | Holm p | Status |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            p = None if r["p_holm"] in ("", "None") else float(r["p_holm"])
            out.append(f"| {r['variation']} (N={r['n_agents']}, {r['tie_rule']}) | {float(r['q']):g} | {r['network']} | {float(r['v']):g} | "
                       f"{r['rule']} | {float(r['ref_delta']):.4f} | {float(r['delta']):.4f} | "
                       f"[{float(r['ci_low']):.4f}, {float(r['ci_high']):.4f}] | {_p(p)} | {r['status']} |")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="herd.tables")
    p.add_argument("kind", choices=["contrasts", "secondary", "robustness"])
    p.add_argument("--run")
    p.add_argument("--csv")
    a = p.parse_args(argv)
    if a.kind == "robustness":
        print(robustness_table(Path(a.csv)))
        return 0
    res = read_result(Path(a.run) / "result.json")
    print(contrasts_table(res) if a.kind == "contrasts" else secondary_table(res))
    return 0


if __name__ == "__main__":
    sys.exit(main())
