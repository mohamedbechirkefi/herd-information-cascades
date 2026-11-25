# SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
"""Artifact manifest (master prompt 11.5): maps every run, table, figure and number trace used in the
manuscript and reports to experiment, runs, metric definition, result path, generator, config and
protocol hashes and code revision. Read-only on results; writes research/publication/artifact_manifest.json.

  python -m herd.manifest
"""

from __future__ import annotations

import json
import sys
import time

from .provenance import REPO_ROOT, sha256_file

RUNS = {
    "EXP-001-R001": "results/exploratory/EXP-001-R001", "EXP-001-R002": "results/exploratory/EXP-001-R002",
    "EXP-001-R003": "results/exploratory/EXP-001-R003", "EXP-001-R004": "results/exploratory/EXP-001-R004",
    "EXP-001-R005": "results/exploratory/EXP-001-R005", "EXP-002-R001": "results/EXP-002/EXP-002-R001",
    "EXP-003-R001": "results/EXP-003/EXP-003-R001", "EXP-004-R001": "results/exploratory/EXP-004-R001",
}
PROTOCOLS = {"EXP-001": "research/experiments/EXP-001/protocol.md", "EXP-002": "research/experiments/EXP-002/protocol.md",
             "EXP-003": "research/experiments/EXP-003/protocol.md", "EXP-004": "research/experiments/EXP-004/protocol.md"}
METRIC = ("Delta_r(c) = mean over paired episodes of Acc_r(e) - Acc_ind(e), Acc(e) = share of the N agents with a_i = theta "
          "(proportion); 95% normal interval; Holm-adjusted two-sided paired t-test p within the variation")
FIGURES = {
    "FIG-001": ("EXP-002-R001", "figures/delta.svg", "forest plot of the 48 primary contrasts with 95% intervals"),
    "FIG-002": ("EXP-002-R001", "figures/accuracy_hist.svg", "episode-accuracy histograms per arm"),
    "FIG-003": ("EXP-003-R001", "figures/delta.svg", "forest plot of the 72 sensitivity contrasts"),
    "FIG-004": ("EXP-004-R001", "figures/delta.svg", "forest plot of the 72 exploratory EXP-004-R001 contrasts"),
}
TABLE_METRICS = {
    "TAB-001": METRIC, "TAB-002": "status by the frozen EXP-003 rule (src/herd/robustness.py) plus Delta range, largest Holm p, per-seed signs",
    "TAB-003": "wrong-cascade probability (share of episodes with an agent in a wrong cascade); share of paired episodes with Acc_r < Acc_ind; last-agent paired difference",
    "TAB-004": "paired difference Acc_imitation(e) - Acc_bayesian(e), 95% normal interval; share of episodes that differ",
    "TAB-005": "mean over agents of expected visible observed actions beside Bayesian Delta",
    "TAB-S01": METRIC, "TAB-S02": "status by the frozen EXP-003 rule", "TAB-S03": "status by the frozen EXP-003 rule (exploratory run)",
    "TAB-S04": "secondary metrics per arm, means with 95% intervals",
}
LABELS = {"EXP-001": "exploratory", "EXP-002": "confirmatory", "EXP-003": "confirmatory", "EXP-004": "exploratory"}


def run_entry(run_id: str, path: str) -> dict:
    m = json.loads((REPO_ROOT / path / "run_manifest.json").read_text(encoding="utf-8"))
    exp = run_id[:7]
    return {"artifact_id": run_id, "kind": "run", "label": m["label"], "exp_id": exp, "run_ids": [run_id],
            "result_path": f"{path}/result.json", "result_sha256": sha256_file(REPO_ROOT / path / "result.json"),
            "config_path": m["config_path"], "config_sha256": m["config_sha256"],
            "protocol_path": PROTOCOLS[exp], "protocol_sha256": sha256_file(REPO_ROOT / PROTOCOLS[exp]),
            "code_revision": m["git"]["revision"], "dirty": m["git"]["dirty"],
            "generator": "src/herd/runner.py and src/herd/serialize.py (python -m herd.cli run); report: src/herd/report.py",
            "report": f"research/experiments/{exp}/report.md", "generated_run_report": f"{path}/report.md"}


def build() -> dict:
    from .paper import SOURCES

    runs = {rid: run_entry(rid, p) for rid, p in RUNS.items()}
    arts = list(runs.values())
    for tab, (run_ids, files, gen) in SOURCES.items():
        exps = sorted({r[:7] for r in run_ids})
        if tab in ("TAB-003", "TAB-004", "TAB-005"):
            exps = ["EXP-002", "EXP-004"]
        arts.append({"artifact_id": tab, "kind": "table", "label": "exploratory" if (tab in ("TAB-003", "TAB-004", "TAB-005", "TAB-S03")) else
                     ("mixed: confirmatory rows EXP-003-R001, exploratory rows EXP-004-R001" if tab == "TAB-002" else "confirmatory"),
                     "exp_id": exps, "run_ids": run_ids, "metric": TABLE_METRICS[tab], "source_paths": files,
                     "source_sha256": {f: sha256_file(REPO_ROOT / f) for f in files},
                     "generator": f"src/herd/paper.py ({gen}; python -m herd.paper fill)",
                     "config_sha256": {r: runs[r]["config_sha256"] for r in run_ids},
                     "code_revision": {r: runs[r]["code_revision"] for r in run_ids},
                     "used_in": ["research/paper/manuscript.md" if not tab.startswith("TAB-S") else "research/paper/supplementary.md"]})
    for fig, (rid, rel, desc) in FIGURES.items():
        r = runs[rid]
        arts.append({"artifact_id": fig, "kind": "figure", "label": r["label"], "exp_id": r["exp_id"], "run_ids": [rid],
                     "path": f"{RUNS[rid]}/{rel}", "sha256": sha256_file(REPO_ROOT / RUNS[rid] / rel), "description": desc,
                     "metric": METRIC, "generator": "src/herd/report.py (python -m herd.cli report)",
                     "config_sha256": r["config_sha256"], "code_revision": r["code_revision"],
                     "used_in": ["research/paper/manuscript.md", "research/paper/supplementary.md", r["report"]]})
    derived = "results/exploratory/EXP-004-derived"
    summ = json.loads((REPO_ROOT / derived / "summary.json").read_text(encoding="utf-8"))
    arts.append({"artifact_id": "EXP-004-derived", "kind": "derived analysis", "label": "exploratory", "exp_id": "EXP-004",
                 "run_ids": ["EXP-002-R001", "EXP-003-R001"], "path": derived, "inputs_sha256": summ["inputs_sha256"],
                 "outputs_sha256": summ["outputs_sha256"], "generator": "src/herd/exploratory.py (python -m herd.exploratory)",
                 "protocol_sha256": sha256_file(REPO_ROOT / PROTOCOLS["EXP-004"]), "code_revision": summ["git"]["revision"]})
    arts.append({"artifact_id": "NUMBER-TRACE", "kind": "number trace", "path": "research/publication/number_trace.csv",
                 "sha256": sha256_file(REPO_ROOT / "research/publication/number_trace.csv"),
                 "description": "one row per number printed in the manuscript prose: token, selector into a committed artifact, "
                                "experiment, runs, metric, hashes, claim; verified by python -m herd.audit",
                 "generator": "hand-curated; checked by src/herd/audit.py"})
    return {"schema_version": "1.0.0", "updated": time.strftime("%Y-%m-%d"),
            "status": "M4: confirmatory runs EXP-002-R001 and EXP-003-R001, exploratory runs EXP-001-R001 to R005 and EXP-004-R001, "
                      "manuscript tables and figures; every manuscript number is traced in research/publication/number_trace.csv",
            "artifacts": arts}


def main(argv: list[str] | None = None) -> int:
    out = REPO_ROOT / "research/publication/artifact_manifest.json"
    data = build()
    out.write_text(json.dumps(data, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {out.relative_to(REPO_ROOT)}: {len(data['artifacts'])} artifacts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
