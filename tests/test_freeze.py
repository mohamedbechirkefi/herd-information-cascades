# SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
"""The protocol freeze (owner-approved 2026-11-24): research/freeze.json, the registry hashes and the run gate.

These tests call the gate only. No confirmatory run is executed by the test suite."""
import hashlib
import json

import pytest

from herd.cli import main
from herd.provenance import REPO_ROOT, config_frozen, config_hash, protocol_frozen
from herd.runner import ProtocolGateError, gate

FROZEN_CONFIGS = ["experiments/EXP-002.json", "experiments/EXP-003.json"]


def _load(rel):
    return json.loads((REPO_ROOT / rel).read_text())


@pytest.mark.parametrize("rel", FROZEN_CONFIGS)
def test_frozen_confirmatory_configs_pass_the_gate(rel):
    # The gate only; no confirmatory run is executed by the test suite.
    cfg = _load(rel)
    assert protocol_frozen(cfg["exp_id"])[0]
    ok, reason = config_frozen(cfg)
    assert ok, reason
    assert "frozen" in gate(cfg)


@pytest.mark.parametrize("rel", FROZEN_CONFIGS)
@pytest.mark.parametrize("mutation", [
    {"episodes_per_seed": 999}, {"seeds": list(range(9))}, {"networks": ["complete", "window-1", "window-3"]},
    {"q": [0.55]}, {"bootstrap": {"resamples": 2000, "seed": 1}}, {"description": "edited"},
])
def test_changed_confirmatory_configs_are_refused(rel, mutation):
    cfg = {**_load(rel), **mutation}
    with pytest.raises(ProtocolGateError, match="not a frozen"):
        gate(cfg)  # gate only: a refused config never reaches the simulation


def test_freeze_record_hashes_match_the_files():
    record = json.loads((REPO_ROOT / "research" / "freeze.json").read_text())
    assert hashlib.sha256((REPO_ROOT / record["study_protocol"]["path"]).read_bytes()).hexdigest() == record["study_protocol"]["sha256"]
    for exp_id in ("EXP-002", "EXP-003"):
        exp = record["experiments"][exp_id]
        assert hashlib.sha256((REPO_ROOT / exp["protocol_path"]).read_bytes()).hexdigest() == exp["protocol_sha256"]
        for c in exp["configs"]:
            assert hashlib.sha256((REPO_ROOT / c["path"]).read_bytes()).hexdigest() == c["file_sha256"]
            assert config_hash(_load(c["path"])) == c["canonical_sha256"]


def test_frozen_configs_carry_the_approved_amendments():
    for rel in FROZEN_CONFIGS:
        cfg = _load(rel)
        assert cfg["networks"] == ["complete", "window-2", "window-3"]  # A-1
        assert cfg["seeds"] == list(range(10)) and cfg["episodes_per_seed"] == 1000  # A-5
        assert cfg["label"] == "confirmatory"


def test_cli_run_refuses_changed_confirmatory_config(capsys, tmp_path):
    for rel in FROZEN_CONFIGS:
        cfg = {**_load(rel), "episodes_per_seed": 10}
        path = tmp_path / "changed.json"
        path.write_text(json.dumps(cfg))
        assert main(["run", "--config", str(path)]) == 3
        assert "REFUSED" in capsys.readouterr().err
