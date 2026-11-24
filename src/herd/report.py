# SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
"""Report generator: tables (CSV and Markdown), SVG figures, report.md and report.pdf.

Every number is read from a validated result.json; nothing is typed in by hand.
PDFs are built as Markdown -> Typst with pandoc (-V mainfont="Libertinus Serif") and
compiled with the typst Python package (decision D-003).
"""

from __future__ import annotations

import csv
import json
import math
import os
import subprocess
from pathlib import Path
from xml.sax.saxutils import escape

from .serialize import read_result
from .stats import Z95

PANDOC = os.environ.get("HERD_PANDOC", "/Users/bechir/research/labs/.tools/pandoc")
TYPST_PYTHON = os.environ.get("HERD_TYPST_PYTHON", "/Users/bechir/research/labs/.tools/py/bin/python")
RULE_COLOURS = {"independent": "#6b6b6b", "bayesian": "#1f5f8b", "imitation": "#b5562b"}
FONT = "Libertinus Serif, Georgia, serif"


def cell_label(cell: dict) -> str:
    return f"q={cell['q']:g}, {cell['network']}, v={cell['v']:g}"


def _fmt(x, digits=4):
    if x is None:
        return "n/a"
    if isinstance(x, float):
        return f"{x:.{digits}f}"
    return str(x)


def arm_rows(res: dict) -> list[dict]:
    rows = []
    for a in res["arms"]:
        c = a["cell"]
        row = {"variation": a["variation"], "rule": a["rule"], "q": c["q"], "network": c["network"], "v": c["v"],
               "n_agents": c["n_agents"], "tie_rule": c["tie_rule"], "n_episodes": a["n_episodes"]}
        for m, s in a["metrics"].items():
            row[f"{m}_mean"] = s["mean"]
            row[f"{m}_ci_low"] = s["ci_low"]
            row[f"{m}_ci_high"] = s["ci_high"]
        row["near_ties"] = a["near_ties"]
        row["runtime_s"] = a["runtime_s"]
        rows.append(row)
    return rows


def contrast_rows(res: dict) -> list[dict]:
    rows = []
    for c in res["contrasts"]:
        cell = c["cell"]
        seeds = c["per_seed_mean"]
        seed_sd = _sd(seeds)
        rows.append({"variation": c["variation"], "rule": c["rule"], "q": cell["q"], "network": cell["network"],
                     "v": cell["v"], "n_agents": cell["n_agents"], "tie_rule": cell["tie_rule"], "n": c["n"],
                     "delta_mean": c["mean"], "ci_low": c["ci_low"], "ci_high": c["ci_high"],
                     "boot_ci_low": c.get("boot_ci_low"), "boot_ci_high": c.get("boot_ci_high"),
                     "paired_sd": c["sd"], "p_value": c["p_value"], "p_holm": c["p_holm"], "degenerate": c["degenerate"],
                     "n_seeds": len(seeds), "seed_mean_sd": seed_sd,
                     "projected_half_width_10000": Z95 * c["sd"] / math.sqrt(10000)})
    return rows


def _sd(xs):
    if len(xs) < 2:
        return None
    m = sum(xs) / len(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def svg_delta(res: dict, path: Path) -> str:
    """Forest plot of paired accuracy differences with 95% intervals."""
    cons = res["contrasts"]
    if not cons:
        return ""
    lo = min(c["ci_low"] for c in cons)
    hi = max(c["ci_high"] for c in cons)
    lo, hi = min(lo, 0.0), max(hi, 0.0)
    pad = 0.05 * (hi - lo or 1)
    lo, hi = lo - pad, hi + pad
    row_h, left, width, top = 16, 290, 380, 40
    height = top + row_h * len(cons) + 50
    x = lambda val: left + (val - lo) / (hi - lo) * width  # noqa: E731
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{left + width + 30}" height="{height}" '
             f'font-family="{FONT}" font-size="11">',
             f'<rect width="100%" height="100%" fill="#ffffff"/>',
             f'<text x="10" y="18" font-size="13">Paired accuracy difference vs independent (proportion), 95% interval</text>',
             f'<line x1="{x(0):.1f}" y1="{top - 6}" x2="{x(0):.1f}" y2="{height - 40}" stroke="#999" stroke-dasharray="3,3"/>']
    for i, c in enumerate(cons):
        y = top + i * row_h + row_h / 2
        col = RULE_COLOURS[c["rule"]]
        label = f"{c['variation']}: {cell_label(c['cell'])}, N={c['cell']['n_agents']}, {c['cell']['tie_rule']}, {c['rule']}"
        parts.append(f'<text x="10" y="{y + 4:.1f}">{escape(label)}</text>')
        parts.append(f'<line x1="{x(c["ci_low"]):.1f}" y1="{y:.1f}" x2="{x(c["ci_high"]):.1f}" y2="{y:.1f}" stroke="{col}" stroke-width="2"/>')
        parts.append(f'<circle cx="{x(c["mean"]):.1f}" cy="{y:.1f}" r="3" fill="{col}"/>')
    yb = height - 34
    parts.append(f'<line x1="{left}" y1="{yb}" x2="{left + width}" y2="{yb}" stroke="#333"/>')
    for k in range(5):
        val = lo + k * (hi - lo) / 4
        parts.append(f'<line x1="{x(val):.1f}" y1="{yb}" x2="{x(val):.1f}" y2="{yb + 4}" stroke="#333"/>')
        parts.append(f'<text x="{x(val):.1f}" y="{yb + 16}" text-anchor="middle">{val:.3f}</text>')
    parts.append(f'<text x="{left}" y="{height - 4}">blue: Bayesian; orange: imitation. n episodes per contrast as in the table.</text>')
    parts.append("</svg>")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(parts) + "\n", encoding="utf-8")
    return path.name


def svg_histograms(res: dict, path: Path, max_cells: int = 24) -> str:
    """Small multiples: distribution of episode accuracy per rule, one panel per cell."""
    groups: dict[tuple, list[dict]] = {}
    for a in res["arms"]:
        key = (a["variation"], json.dumps(a["cell"], sort_keys=True))
        groups.setdefault(key, []).append(a)
    keys = list(groups)[:max_cells]
    cols = 4
    pw, ph, gap = 170, 110, 26
    rows = math.ceil(len(keys) / cols)
    W, H = cols * (pw + gap) + 20, rows * (ph + gap + 14) + 50
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="{FONT}" font-size="9">',
             '<rect width="100%" height="100%" fill="#ffffff"/>',
             '<text x="10" y="16" font-size="12">Episode accuracy distributions (share of episodes per bin of width 0.05)</text>']
    for idx, key in enumerate(keys):
        arms = groups[key]
        ox = 10 + (idx % cols) * (pw + gap)
        oy = 34 + (idx // cols) * (ph + gap + 14)
        cell = arms[0]["cell"]
        parts.append(f'<text x="{ox}" y="{oy + 8}">{escape(key[0] + ": " + cell_label(cell))}</text>')
        top = oy + 14
        parts.append(f'<rect x="{ox}" y="{top}" width="{pw}" height="{ph - 14}" fill="none" stroke="#ccc"/>')
        ymax = max(max(c / max(1, sum(a["accuracy_histogram"]["counts"])) for c in a["accuracy_histogram"]["counts"]) for a in arms) or 1
        for a in arms:
            counts = a["accuracy_histogram"]["counts"]
            total = max(1, sum(counts))
            nb = len(counts)
            pts = []
            for b, cnt in enumerate(counts):
                yv = top + (ph - 14) * (1 - (cnt / total) / ymax)
                x0 = ox + pw * b / nb
                x1 = ox + pw * (b + 1) / nb
                pts.append(f"{x0:.1f},{yv:.1f} {x1:.1f},{yv:.1f}")
            parts.append(f'<polyline fill="none" stroke="{RULE_COLOURS[a["rule"]]}" stroke-width="1.3" points="{" ".join(pts)}"/>')
        parts.append(f'<text x="{ox}" y="{top + ph - 2}">0</text><text x="{ox + pw - 6}" y="{top + ph - 2}">1</text>')
    parts.append(f'<text x="10" y="{H - 6}">grey: independent; blue: Bayesian; orange: imitation. Horizontal axis: episode accuracy 0 to 1.</text>')
    parts.append("</svg>")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(parts) + "\n", encoding="utf-8")
    return path.name


def md_table(rows: list[dict], cols: list[tuple[str, str]], digits: int = 4) -> str:
    head = "| " + " | ".join(h for _, h in cols) + " |"
    sep = "|" + "|".join("---" for _ in cols) + "|"
    body = ["| " + " | ".join(_fmt(r.get(k), digits) for k, _ in cols) + " |" for r in rows]
    return "\n".join([head, sep] + body)


def build_markdown(res: dict, manifest: dict | None, figs: dict) -> str:
    label = res["label"].upper()
    lines = [f"<!-- SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0 -->",
             f"# {res['run_id']} ({label}): generated run report", ""]
    if res["label"] == "exploratory":
        lines += ["**EXPLORATORY RUN. Not evidence for any study hypothesis.** The study protocol is an unfrozen draft; "
                  "these numbers serve planning and verification only (master prompt section 3).", ""]
    lines += [f"- Experiment: {res['exp_id']}; run: {res['run_id']}; created (UTC): {res['created_utc']}",
              f"- Description: {res['config']['description']}",
              f"- Config SHA-256: `{res['config_sha256']}`",
              f"- Seeds: {res['config']['seeds']}; episodes per seed and cell: {res['config']['episodes_per_seed']}",
              f"- Result schema: {res['schema_version']}"]
    if manifest:
        lines += [f"- Code revision: `{manifest['git']['revision']}` (dirty: {manifest['git']['dirty']})",
                  f"- Platform: {manifest['platform']['cpu']}, {manifest['platform']['os']}; Python {manifest['versions']['python']}, numpy {manifest['versions']['numpy']}",
                  f"- Wall-clock runtime: {manifest['runtime_s']:.2f} s; peak resident memory: {manifest['peak_rss_bytes']} bytes"]
    t = res["timing"]
    lines += [f"- Simulation time: {t['simulation_s']:.2f} s for {t['agent_decisions']} agent decisions "
              f"({t['seconds_per_1000_decisions'] * 1000:.3f} ms per 1,000 decisions); analysis time {t['analysis_s']:.2f} s", ""]
    checks = res["checks"]
    lines += ["## Verification checks", ""]
    if checks:
        failed = [c for c in checks if not c["passed"]]
        lines += [f"{len(checks)} checks, {len(checks) - len(failed)} passed, {len(failed)} failed.", ""]
        crow = [{"id": c["id"], "name": c["name"], "cell": cell_label(c["cell"]) if "cell" in c else "all",
                 "rule": c.get("rule", ""), "passed": "pass" if c["passed"] else "FAIL",
                 "observed": c.get("observed"), "expected": c.get("expected")} for c in checks]
        lines += [md_table(crow, [("id", "Check"), ("name", "Name"), ("cell", "Cell"), ("rule", "Rule"),
                                  ("passed", "Result"), ("observed", "Observed"), ("expected", "Expected")]), ""]
    else:
        lines += ["No verification checks were requested in this configuration.", ""]
    lines += ["## Failed cells", ""]
    lines += [("None." if not res["failures"] else "\n".join(f"- {f['variation']} {cell_label(f['cell'])} seed {f['seed']}: {f['error']}" for f in res["failures"])), ""]
    lines += ["## Paired accuracy differences against the independent baseline", "",
              "Mean paired difference in episode accuracy (proportion of agents correct), normal-approximation 95% interval at the "
              "episode level, Holm adjustment within each variation. `seed SD` is the standard deviation of the per-seed mean "
              "differences; `hw@10k` is the 95% half-width that the observed paired SD implies at 10,000 episodes.", ""]
    crow = contrast_rows(res)
    for r in crow:
        r["cell"] = f"{r['variation']}: q={r['q']:g}, {r['network']}, v={r['v']:g}, N={r['n_agents']}, {r['tie_rule']}"
    lines += [md_table(crow, [("cell", "Cell"), ("rule", "Rule"), ("n", "n"), ("delta_mean", "Delta"), ("ci_low", "CI low"),
                              ("ci_high", "CI high"), ("paired_sd", "paired SD"), ("seed_mean_sd", "seed SD"),
                              ("p_holm", "p (Holm)"), ("projected_half_width_10000", "hw@10k")]), ""]
    if figs.get("delta"):
        lines += [f"![Forest plot of paired accuracy differences with 95% intervals for every contrast in {res['run_id']}. "
                  f"Exploratory.]({figs['delta']})", "",
                  f"*Figure: paired accuracy difference (proportion) against the independent baseline, points are means and bars "
                  f"95% normal intervals over episodes; the dashed line marks zero. Source: {res['run_id']}/result.json.*", ""]
    lines += ["## Arms", "", "Means over episodes with 95% intervals in the CSV table `tables/arms.csv`.", ""]
    arow = arm_rows(res)
    for r in arow:
        r["cell"] = f"{r['variation']}: q={r['q']:g}, {r['network']}, v={r['v']:g}, N={r['n_agents']}, {r['tie_rule']}"
    lines += [md_table(arow, [("cell", "Cell"), ("rule", "Rule"), ("n_episodes", "n"), ("accuracy_mean", "Accuracy"),
                              ("cascade_any_mean", "Cascade"), ("wrong_cascade_any_mean", "Wrong cascade"),
                              ("longest_wrong_run_mean", "Longest wrong run"), ("informative_share_mean", "Informative"),
                              ("last_agent_accuracy_mean", "Last agent")], 3), ""]
    if figs.get("hist"):
        lines += [f"![Small multiples of episode-accuracy histograms for each cell and rule in {res['run_id']}. Exploratory.]({figs['hist']})", "",
                  "*Figure: distribution of episode accuracy, share of episodes per bin of width 0.05; grey independent, blue Bayesian, "
                  "orange imitation.*", ""]
    lines += ["## Metric definitions", ""] + [f"- `{k}`: {v}" for k, v in res["metric_definitions"].items()] + [""]
    return "\n".join(lines)


def build_pdf(md_path: Path) -> Path:
    typ = md_path.with_suffix(".typ")
    pdf = md_path.with_suffix(".pdf")
    subprocess.run([PANDOC, md_path.name, "-s", "-V", "mainfont=Libertinus Serif", "-V", "papersize=a4", "-o", typ.name],
                   cwd=md_path.parent, check=True)
    subprocess.run([TYPST_PYTHON, "-c", "import sys, typst; typst.compile(sys.argv[1], output=sys.argv[2], root=sys.argv[3])",
                    typ.name, pdf.name, "."], cwd=md_path.parent, check=True)
    typ.unlink()
    return pdf


def build_report(run_dir: Path, pdf: bool = True) -> list[Path]:
    res = read_result(run_dir / "result.json")
    manifest_path = run_dir / "run_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else None
    written = []
    write_csv(run_dir / "tables" / "arms.csv", arm_rows(res))
    write_csv(run_dir / "tables" / "contrasts.csv", contrast_rows(res))
    write_csv(run_dir / "tables" / "checks.csv", [{k: (json.dumps(v) if isinstance(v, dict) else v) for k, v in c.items()} for c in res["checks"]])
    written += [run_dir / "tables" / n for n in ("arms.csv", "contrasts.csv", "checks.csv")]
    figs = {}
    if res["contrasts"]:
        svg_delta(res, run_dir / "figures" / "delta.svg")
        figs["delta"] = "figures/delta.svg"
        written.append(run_dir / "figures" / "delta.svg")
    svg_histograms(res, run_dir / "figures" / "accuracy_hist.svg")
    figs["hist"] = "figures/accuracy_hist.svg"
    written.append(run_dir / "figures" / "accuracy_hist.svg")
    md = run_dir / "report.md"
    md.write_text(build_markdown(res, manifest, figs), encoding="utf-8")
    written.append(md)
    if pdf:
        written.append(build_pdf(md))
    return written
