# SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
"""Result serialisation: validated JSON summary, per-episode raw arrays and the run manifest."""

from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

from . import MANIFEST_SCHEMA_VERSION
from .provenance import REPO_ROOT, git_state, peak_rss_bytes, platform_info, sha256_file, versions
from .runner import RunOutput
from .schema import load_schema, validate


def _rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def read_result(path: Path) -> dict:
    """Load and validate a result file (fail closed on malformed input)."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    validate(data, load_schema("result-v1.json"))
    return data


def write_run(output: RunOutput, config_path: str, started_utc: str, runtime_s: float, command: str,
              root: Path = REPO_ROOT) -> dict:
    cfg = output.result["config"]
    out_dir = root / cfg["output_dir"]
    raw_dir = root / cfg["raw_dir"]
    if out_dir.exists() and (out_dir / "result.json").exists():
        raise FileExistsError(f"{_rel(out_dir)} already holds a result; use a new run_id (raw results are never overwritten)")
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)
    validate(output.result, load_schema("result-v1.json"))
    result_path = out_dir / "result.json"
    result_path.write_text(json.dumps(output.result, indent=1, sort_keys=False) + "\n", encoding="utf-8")
    raw_path = raw_dir / "episodes.npz"
    np.savez_compressed(raw_path, **{k: v for k, v in output.raw.items()})
    outputs = [
        {"path": _rel(result_path), "sha256": sha256_file(result_path), "bytes": result_path.stat().st_size, "committed": True},
        {"path": _rel(raw_path), "sha256": sha256_file(raw_path), "bytes": raw_path.stat().st_size, "committed": False},
    ]
    manifest = {
        "schema_version": MANIFEST_SCHEMA_VERSION, "kind": "herd-run-manifest",
        "run_id": cfg["run_id"], "exp_id": cfg["exp_id"], "label": cfg["label"],
        "config_path": config_path, "config_sha256": output.result["config_sha256"], "seeds": cfg["seeds"],
        "git": git_state(root), "versions": versions(), "platform": platform_info(),
        "started_utc": started_utc, "finished_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "runtime_s": float(runtime_s), "peak_rss_bytes": peak_rss_bytes(), "outputs": outputs, "command": command,
    }
    validate(manifest, load_schema("manifest-v1.json"))
    (out_dir / "run_manifest.json").write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
    return manifest
