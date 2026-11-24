# SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
"""Run provenance: hashes, git revision, versions, platform, peak memory, and the protocol gate."""

from __future__ import annotations

import csv
import hashlib
import json
import platform
import re
import resource
import subprocess
import sys
from pathlib import Path

import numpy as np

from . import RESULT_SCHEMA_VERSION, __version__

REPO_ROOT = Path(__file__).resolve().parents[2]
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def canonical_json(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def config_hash(config: dict) -> str:
    return sha256_text(canonical_json(config))


def git_state(root: Path = REPO_ROOT) -> dict:
    try:
        rev = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
        status = subprocess.run(["git", "-C", str(root), "status", "--porcelain", "--", "src", "pyproject.toml", "uv.lock"],
                                capture_output=True, text=True, check=True).stdout
        return {"revision": rev, "dirty": bool(status.strip())}
    except (OSError, subprocess.CalledProcessError):
        return {"revision": None, "dirty": None}


def cpu_name() -> str:
    if sys.platform == "darwin":
        try:
            return subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"], capture_output=True, text=True,
                                  check=True).stdout.strip()
        except (OSError, subprocess.CalledProcessError):
            pass
    return platform.processor() or "unknown"


def platform_info() -> dict:
    return {"os": f"{platform.system()} {platform.release()}", "machine": platform.machine(), "cpu": cpu_name(),
            "mac_ver": platform.mac_ver()[0] or "n/a"}


def versions() -> dict:
    return {"herd": __version__, "python": platform.python_version(), "numpy": np.__version__,
            "result_schema": RESULT_SCHEMA_VERSION}


def peak_rss_bytes() -> int | None:
    try:
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    except (OSError, ValueError):
        return None
    return int(rss if sys.platform == "darwin" else rss * 1024)


def protocol_frozen(exp_id: str, root: Path = REPO_ROOT) -> tuple[bool, str]:
    """A protocol counts as frozen only if the registry records a SHA-256 for it and the
    protocol file on disk still has that hash."""
    registry = root / "research" / "experiment_registry.csv"
    if not registry.is_file():
        return False, "experiment registry not found"
    with open(registry, newline="", encoding="utf-8") as fh:
        rows = [r for r in csv.DictReader(fh) if r.get("exp_id") == exp_id]
    if not rows:
        return False, f"{exp_id} is not registered"
    row = rows[0]
    recorded = (row.get("protocol_sha256") or "").strip()
    if not SHA256_RE.match(recorded):
        return False, f"{exp_id} protocol is not frozen (registry protocol_sha256 = {recorded!r})"
    path = root / row.get("protocol_path", "")
    if not path.is_file():
        return False, f"protocol file {path} missing"
    actual = sha256_file(path)
    if actual != recorded:
        return False, f"{exp_id} protocol file hash {actual} differs from the frozen hash {recorded}"
    return True, f"{exp_id} protocol frozen at {recorded}"


FREEZE_RECORD = Path("research") / "freeze.json"


def config_frozen(config: dict, root: Path = REPO_ROOT) -> tuple[bool, str]:
    """A confirmatory configuration may run only if the freeze record (research/freeze.json) lists it.

    The record must exist, the study protocol and the experiment protocol on disk must still have the
    hashes it records, and the canonical SHA-256 of the configuration (sorted keys, compact separators)
    must equal the hash recorded for one of the experiment's frozen configurations."""
    path = root / FREEZE_RECORD
    if not path.is_file():
        return False, f"freeze record {FREEZE_RECORD} not found"
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return False, f"freeze record {FREEZE_RECORD} is not valid JSON ({exc})"
    study = record.get("study_protocol") or {}
    study_path = root / study.get("path", "")
    if not SHA256_RE.match(study.get("sha256", "")) or not study_path.is_file():
        return False, "freeze record has no valid study protocol entry"
    if sha256_file(study_path) != study["sha256"]:
        return False, f"study protocol {study['path']} differs from the frozen hash {study['sha256']}"
    exp = (record.get("experiments") or {}).get(config["exp_id"])
    if not exp:
        return False, f"{config['exp_id']} is not in the freeze record"
    proto = root / exp.get("protocol_path", "")
    if not proto.is_file() or sha256_file(proto) != exp.get("protocol_sha256"):
        return False, f"{config['exp_id']} protocol differs from the hash in the freeze record"
    digest = config_hash(config)
    frozen = {c.get("canonical_sha256") for c in exp.get("configs", [])}
    if digest not in frozen:
        return False, f"configuration hash {digest} is not a frozen {config['exp_id']} configuration"
    return True, f"configuration {digest} frozen for {config['exp_id']}"
