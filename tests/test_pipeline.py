# SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
"""Integration: config -> run -> validated result and manifest -> report; protocol gate; schema."""
import copy
import hashlib
import json

import pytest

from herd.model import ModelError
from herd.provenance import REPO_ROOT, config_frozen, config_hash, protocol_frozen
from herd.report import build_report
from herd.runner import ProtocolGateError, apply_holm, gate, run
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


def _synthetic_freeze(tmp_path):
    for exp in ("EXP-009",):
        (tmp_path / "research" / "experiments" / exp).mkdir(parents=True)
    study = tmp_path / "research" / "protocol.md"
    study.write_text("study protocol\n")
    proto = tmp_path / "research" / "experiments" / "EXP-009" / "protocol.md"
    proto.write_text("frozen protocol\n")
    digest = hashlib.sha256(proto.read_bytes()).hexdigest()
    (tmp_path / "research" / "experiment_registry.csv").write_text(
        f"exp_id,protocol_path,protocol_sha256\nEXP-009,research/experiments/EXP-009/protocol.md,{digest}\n")
    cfg = {**copy.deepcopy(BASE), "exp_id": "EXP-009", "run_id": "EXP-009-R001", "label": "confirmatory",
           "output_dir": "results/EXP-009/x"}
    record = {"study_protocol": {"path": "research/protocol.md", "sha256": hashlib.sha256(study.read_bytes()).hexdigest()},
              "experiments": {"EXP-009": {"protocol_path": "research/experiments/EXP-009/protocol.md",
                                          "protocol_sha256": digest,
                                          "configs": [{"canonical_sha256": config_hash(cfg)}]}}}
    (tmp_path / "research" / "freeze.json").write_text(json.dumps(record))
    return cfg, study, proto


def test_freeze_record_gate_with_synthetic_root(tmp_path):
    cfg, study, proto = _synthetic_freeze(tmp_path)
    assert config_frozen(cfg, tmp_path)[0]
    assert "frozen" in gate(cfg, tmp_path)
    changed = {**cfg, "episodes_per_seed": 41}
    with pytest.raises(ProtocolGateError, match="not a frozen"):
        gate(changed, tmp_path)
    study.write_text("study protocol edited after freeze\n")
    ok, reason = config_frozen(cfg, tmp_path)
    assert not ok and "study protocol" in reason
    (tmp_path / "research" / "freeze.json").unlink()
    ok, reason = config_frozen(cfg, tmp_path)
    assert not ok and "not found" in reason


def test_gate_refuses_when_registry_unfrozen_even_with_freeze_record(tmp_path):
    cfg, _, proto = _synthetic_freeze(tmp_path)
    (tmp_path / "research" / "experiment_registry.csv").write_text(
        "exp_id,protocol_path,protocol_sha256\nEXP-009,research/experiments/EXP-009/protocol.md,none\n")
    with pytest.raises(ProtocolGateError, match="not frozen"):
        gate(cfg, tmp_path)


def _contrast(variation, p, degenerate=False):
    return {"variation": variation, "p_value": p, "degenerate": degenerate}


def test_holm_family_excludes_degenerate_contrasts():
    cs = [_contrast("a", 0.01), _contrast("a", 1.0, degenerate=True), _contrast("a", 0.04), _contrast("a", 0.03),
          _contrast("a", 0.005), _contrast("b", 0.02), _contrast("b", 0.0, degenerate=True)]
    apply_holm(cs)
    a = [c for c in cs if c["variation"] == "a"]
    # family of variation a: four non-degenerate p-values, hand-computed Holm as in test_holm_hand_computed
    assert [c["p_holm"] for c in a if c["holm_family"]] == pytest.approx([0.03, 0.06, 0.06, 0.02])
    assert a[1]["holm_family"] is False and a[1]["p_holm"] is None
    b = [c for c in cs if c["variation"] == "b"]
    assert b[0]["p_holm"] == pytest.approx(0.02) and b[1]["holm_family"] is False and b[1]["p_holm"] is None


def test_degenerate_contrast_in_a_run_is_reported_outside_holm():
    # window-1 with own-signal ties is degenerate (amendment A-1): an exploratory run must flag it
    cfg = {**copy.deepcopy(BASE), "q": [0.7], "networks": ["window-1"], "visibility": [1.0]}
    res = run(cfg).result
    assert res["contrasts"] and all(c["degenerate"] for c in res["contrasts"])
    assert all(c["holm_family"] is False and c["p_holm"] is None for c in res["contrasts"])
    rows = __import__("herd.report", fromlist=["contrast_rows"]).contrast_rows(res)
    assert all(r["holm_family"] is False for r in rows)


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
