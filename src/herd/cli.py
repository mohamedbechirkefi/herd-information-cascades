# SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
"""Command line: smoke, run, report, test.

  python -m herd.cli smoke                    exploratory EXP-001 smoke matrix
  python -m herd.cli run --config FILE        run a configuration (confirmatory refused while unfrozen)
  python -m herd.cli report --run DIR         tables, figures, report.md and report.pdf from a result
  python -m herd.cli test                     the pytest suite
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

from .provenance import REPO_ROOT

SMOKE_CONFIG = "experiments/EXP-001-R001.json"


def _run(config_path: str) -> int:
    from .runner import ProtocolGateError, run
    from .serialize import write_run

    path = (REPO_ROOT / config_path) if not Path(config_path).is_absolute() else Path(config_path)
    config = json.loads(path.read_text(encoding="utf-8"))
    started = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    t0 = time.perf_counter()
    try:
        output = run(config)
    except ProtocolGateError as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 3
    runtime = time.perf_counter() - t0
    rel = str(path.resolve().relative_to(REPO_ROOT)) if path.resolve().is_relative_to(REPO_ROOT) else str(path)
    manifest = write_run(output, rel, started, runtime, command=" ".join(["herd.cli"] + sys.argv[1:]))
    res = output.result
    failed = [c for c in res["checks"] if not c["passed"]]
    print(f"{res['label'].upper()} run {res['run_id']}: {len(res['arms'])} arms, {len(res['contrasts'])} contrasts, "
          f"{len(res['checks'])} checks ({len(failed)} failed), {len(res['failures'])} failed cells")
    print(f"runtime {runtime:.2f} s (simulation {res['timing']['simulation_s']:.2f} s, "
          f"{res['timing']['seconds_per_1000_decisions'] * 1e3:.3f} ms per 1000 decisions), "
          f"peak RSS {manifest['peak_rss_bytes']} bytes")
    print(f"wrote {res['config']['output_dir']}/result.json and run_manifest.json")
    for c in failed:
        print(f"FAILED CHECK {c['id']} {c['name']} {c.get('cell')}: {c['detail']}")
    return 1 if (failed or res["failures"]) else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="herd", description="HERD simulation study (synthetic agents only)")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("smoke", help=f"run the exploratory smoke matrix ({SMOKE_CONFIG})")
    p_run = sub.add_parser("run", help="run a configuration file")
    p_run.add_argument("--config", required=True)
    p_rep = sub.add_parser("report", help="build tables, figures and a report from a run directory")
    p_rep.add_argument("--run", required=True, help="directory holding result.json")
    p_rep.add_argument("--no-pdf", action="store_true")
    sub.add_parser("test", help="run the pytest suite (extra arguments are passed to pytest)")
    args, extra = parser.parse_known_args(argv)
    if extra and args.command != "test":
        parser.error(f"unrecognized arguments: {' '.join(extra)}")
    if args.command == "smoke":
        return _run(SMOKE_CONFIG)
    if args.command == "run":
        return _run(args.config)
    if args.command == "report":
        from .report import build_report

        run_dir = Path(args.run)
        run_dir = run_dir if run_dir.is_absolute() else REPO_ROOT / run_dir
        paths = build_report(run_dir, pdf=not args.no_pdf)
        for p in paths:
            print(f"wrote {p}")
        return 0
    if args.command == "test":
        return subprocess.call([sys.executable, "-m", "pytest", *extra], cwd=REPO_ROOT)
    return 2


if __name__ == "__main__":
    sys.exit(main())
