# SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
"""EXP-003 decision rule (frozen protocol v1.0, EXP-003 section 3), applied to two result files.

For every contrast (rule, q, network, v) that is Holm-significant in the reference run (EXP-002), and for
every variation of the sensitivity run (EXP-003) that contains the same cell, the contrast is
'robust' if it keeps its sign and stays Holm-significant, 'sign reversed' if the sign of the mean
paired difference flips, and 'lost significance' if the sign holds but the contrast is no longer
Holm-significant (or is degenerate). A contrast that is not 'robust' under any variation is reported as
convention-dependent. This module only reads result.json files; it changes no estimate.

  python -m herd.robustness --reference results/EXP-002/EXP-002-R001 --sensitivity results/EXP-003/EXP-003-R001
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from .serialize import read_result

ALPHA = 0.05


def _key(c: dict) -> tuple:
    return (c["rule"], float(c["cell"]["q"]), c["cell"]["network"], float(c["cell"]["v"]))


def _sign(x: float) -> int:
    return (x > 0) - (x < 0)


def holm_significant(c: dict) -> bool:
    return bool(c.get("holm_family")) and c.get("p_holm") is not None and c["p_holm"] < ALPHA


def compare(reference: dict, sensitivity: dict) -> list[dict]:
    ref = {}
    for c in reference["contrasts"]:
        ref[_key(c)] = c
    rows = []
    for c in sensitivity["contrasts"]:
        r = ref.get(_key(c))
        if r is None or not holm_significant(r):
            continue
        same_sign = _sign(c["mean"]) == _sign(r["mean"])
        sig = holm_significant(c)
        status = "robust" if (same_sign and sig) else ("sign reversed" if not same_sign else "lost significance")
        rows.append({
            "variation": c["variation"], "rule": c["rule"], "q": c["cell"]["q"], "network": c["cell"]["network"],
            "v": c["cell"]["v"], "n_agents": c["cell"]["n_agents"], "tie_rule": c["cell"]["tie_rule"],
            "ref_delta": r["mean"], "ref_p_holm": r["p_holm"],
            "delta": c["mean"], "ci_low": c["ci_low"], "ci_high": c["ci_high"], "p_holm": c["p_holm"],
            "same_sign": same_sign, "holm_significant": sig, "status": status,
        })
    return rows


def convention_dependent(rows: list[dict]) -> list[tuple]:
    return sorted({(r["rule"], r["q"], r["network"], r["v"]) for r in rows if r["status"] != "robust"})


def write_csv(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()) if rows else ["status"])
        w.writeheader()
        w.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="herd.robustness")
    p.add_argument("--reference", required=True, help="run directory of the reference run (EXP-002)")
    p.add_argument("--sensitivity", required=True, help="run directory of the sensitivity run (EXP-003)")
    a = p.parse_args(argv)
    ref = read_result(Path(a.reference) / "result.json")
    sen = read_result(Path(a.sensitivity) / "result.json")
    rows = compare(ref, sen)
    out = Path(a.sensitivity) / "tables" / f"robustness_vs_{ref['run_id']}.csv"
    write_csv(rows, out)
    counts: dict[str, int] = {}
    for r in rows:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    print(f"{len(rows)} comparisons: {counts}")
    for k in convention_dependent(rows):
        print(f"convention-dependent: rule={k[0]} q={k[1]} {k[2]} v={k[3]}")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
