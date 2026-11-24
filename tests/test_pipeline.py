# SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
"""Integration: config -> run -> validated result and manifest -> report; protocol gate; schema."""
import copy
import hashlib
import json

import pytest

from herd.cli import main
from herd.model import ModelError
from herd.provenance import REPO_ROOT, protocol_frozen
from herd.report import build_report
from herd.runner import ProtocolGateError, run
from herd.schema import SchemaError, errors, load_schema, validate
from herd.serialize import read_result, write_run

BASE = {
    "config_version": "1", "exp_id": "EXP-001", "run_id": "EXP-001-R900", "label": "exploratory",
    "description": "test configuration", "rules": ["independent", "bayesian", "imitation"],
    "q": [0.5, 0.7], "networks": ["complete", "window-2"], "visibility": [1.0, 0.5],
    "variations": [{"id": "t", "tie_rule": "own", "n_agents": 9}], "seeds": [0, 1], "episodes_per_seed": 40,
    "bootstrap": {"resamples": 50, "seed": 1}, "verification": True,
    "output_dir": "results/exploratory/test", "raw_dir": "results/raw/test",
}


def test_run_end_to_end(tmp_path):
    out = run(copy.deepcopy(BASE))
    res = out.result
    assert len(res["arms"]) == 2 * 2 * 2 * 3
    assert len(res["contrasts"]) == 2 * 2 * 2 * 2
    assert res["failures"] == []
    ids = {c["id"] for c in res["checks"]}
    assert {"C1", "C2", "C3", "C4", "C5", "C6"} <= ids
    assert all(c["passed"] for c in res["checks"] if c["id"] in ("C2", "C4", "C5", "C6"))
    manifest = write_run(out, "experiments/test.json", "2026-11-24T00:00:00Z", 1.0, "test", root=tmp_path)
    run_dir = tmp_path / BASE["output_dir"]
    assert read_result(run_dir / "result.json")["run_id"] == "EXP-001-R900"
    assert manifest["config_sha256"] == res["config_sha256"]
    with pytest.raises(FileExistsError):
        write_run(out, "experiments/test.json", "x", 1.0, "test", root=tmp_path)
    written = build_report(run_dir, pdf=False)
    assert (run_dir / "report.md").read_text().count("EXPLORATORY RUN") == 1
    assert any(p.name == "delta.svg" for p in written)


def test_run_is_reproducible():
    a = run(copy.deepcopy(BASE)).result
    b = run(copy.deepcopy(BASE)).result
    strip = lambda r: [(x["rule"], x["metrics"]["accuracy"]["mean"]) for x in r["arms"]]  # noqa: E731
    assert strip(a) == strip(b)
    assert [c["mean"] for c in a["contrasts"]] == [c["mean"] for c in b["contrasts"]]


@pytest.mark.parametrize("mutation", [
    {"label": "final"}, {"q": [0.4]}, {"networks": ["star"]}, {"rules": []}, {"seeds": [-1]},
    {"episodes_per_seed": 1}, {"extra_key": 1}, {"run_id": "R1"},
    {"output_dir": "results/somewhere"},  # exploratory output must be in an exploratory folder
    {"rules": ["bayesian", "imitation"]},  # baseline missing
])
def test_invalid_configs_rejected(mutation):
    cfg = {**copy.deepcopy(BASE), **mutation}
    with pytest.raises((SchemaError, ModelError)):
        run(cfg)


def test_confirmatory_config_refused_while_unfrozen(tmp_path):
    cfg = {**copy.deepcopy(BASE), "exp_id": "EXP-002", "run_id": "EXP-002-R001", "label": "confirmatory",
           "output_dir": "results/EXP-002/x"}
    with pytest.raises(ProtocolGateError):
        run(cfg)  # the real registry: EXP-002 is a draft
    frozen, reason = protocol_frozen("EXP-002")
    assert not frozen and "not frozen" in reason


def test_protocol_gate_with_synthetic_registry(tmp_path):
    (tmp_path / "research" / "experiments" / "EXP-009").mkdir(parents=True)
    proto = tmp_path / "research" / "experiments" / "EXP-009" / "protocol.md"
    proto.write_text("frozen protocol\n")
    digest = hashlib.sha256(proto.read_bytes()).hexdigest()
    reg = tmp_path / "research" / "experiment_registry.csv"
    reg.write_text("exp_id,protocol_path,protocol_sha256\n"
                   f"EXP-009,research/experiments/EXP-009/protocol.md,{digest}\n"
                   "EXP-010,research/experiments/EXP-009/protocol.md,none\n")
    assert protocol_frozen("EXP-009", tmp_path)[0]
    assert not protocol_frozen("EXP-010", tmp_path)[0]
    assert not protocol_frozen("EXP-011", tmp_path)[0]
    proto.write_text("edited after freeze\n")
    ok, reason = protocol_frozen("EXP-009", tmp_path)
    assert not ok and "differs" in reason


def test_cli_run_refuses_confirmatory_config(capsys):
    assert main(["run", "--config", "experiments/EXP-002.json"]) == 3
    assert "REFUSED" in capsys.readouterr().err
    assert main(["run", "--config", "experiments/EXP-003.json"]) == 3


def test_shipped_configs_are_valid():
    schema = load_schema("config-v1.json")
    for path in sorted((REPO_ROOT / "experiments").glob("*.json")):
        validate(json.loads(path.read_text()), schema)


def test_schema_validator_subset():
    schema = {"type": "object", "required": ["a"], "additionalProperties": False,
              "properties": {"a": {"type": "integer", "minimum": 0}, "b": {"enum": ["x"]}}}
    assert errors({"a": 1}, schema) == []
    assert errors({"a": -1}, schema)
    assert errors({"a": 1, "c": 2}, schema)
    assert errors({"b": "x"}, schema)
    assert errors({"a": True}, schema)
    with pytest.raises(SchemaError):
        errors({}, {"oneOf": []})
    with pytest.raises(SchemaError):
        read_result_from = load_schema("missing.json")  # noqa: F841


def test_result_reader_fails_closed(tmp_path):
    p = tmp_path / "result.json"
    p.write_text(json.dumps({"schema_version": "1.0.0", "kind": "herd-result"}))
    with pytest.raises(SchemaError):
        read_result(p)
    good = run(copy.deepcopy(BASE)).result
    bad = copy.deepcopy(good)
    bad["contrasts"][0]["p_holm"] = 1.5
    p.write_text(json.dumps(bad))
    with pytest.raises(SchemaError):
        read_result(p)
