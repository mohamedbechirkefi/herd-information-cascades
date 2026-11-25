# SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
"""M5 consistency (master prompt 11.6): the demo shows the same numbers as the paper.

1. Re-running the export in memory reproduces the committed demo/public/data/results.json byte for byte.
2. Every ``display`` and ``interval_display`` string in it appears verbatim in the manuscript, or in its
   generated supplementary appendix, or is one of the documented exceptions below.
3. The sandbox fixture of the TypeScript port is reproduced by the Python engine.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
MANUSCRIPT = (REPO / "research/paper/manuscript.md").read_text(encoding="utf-8")
SUPPLEMENTARY = (REPO / "research/paper/supplementary.md").read_text(encoding="utf-8")

# Display strings that are not printed in research/paper/manuscript.md or supplementary.md.
# Each is reproduced from a committed result file by the export, which the identity test checks.
DOCUMENTED_EXCEPTIONS = {
    "Wilson 99% [0.3958, 0.4211]": "C1 check of EXP-002-R001 at q = 0.55: interval text from the check detail in "
                                   "results/EXP-002/EXP-002-R001/result.json (tables/checks.csv); the manuscript prints the point value only",
    "Wilson 99% [0.2980, 0.3218]": "as above, q = 0.60",
    "Wilson 99% [0.1459, 0.1646]": "as above, q = 0.70",
    "Wilson 99% [0.0539, 0.0661]": "as above, q = 0.80",
}


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, REPO / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def export():
    return _load("export_demo_data", "scripts/export_demo_data.py")


def _displays(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ("display", "interval_display"):
                if v is not None:
                    yield f"{path}.{k}", v
            else:
                yield from _displays(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from _displays(v, f"{path}[{i}]")


def test_committed_results_json_is_a_fresh_export(export):
    committed = (REPO / "demo/public/data/results.json").read_text(encoding="utf-8")
    assert export.serialize(export.build()) == committed


def test_export_is_deterministic(export):
    assert export.serialize(export.build()) == export.serialize(export.build())


def test_every_display_string_is_in_the_paper(export):
    data = export.build()
    where = {"manuscript": 0, "supplementary": 0, "exception": 0}
    missing = []
    used_exceptions = set()
    for path, text in _displays(data):
        assert isinstance(text, str) and text, path
        if text in MANUSCRIPT:
            where["manuscript"] += 1
        elif text in SUPPLEMENTARY:
            where["supplementary"] += 1
        elif text in DOCUMENTED_EXCEPTIONS:
            where["exception"] += 1
            used_exceptions.add(text)
        else:
            missing.append((path, text))
    assert not missing, missing
    assert used_exceptions == set(DOCUMENTED_EXCEPTIONS), "stale documented exception"
    assert where["manuscript"] > 0


def test_every_experiment_is_exported_with_status_verdict_and_claims(export):
    data = export.build()
    registry = (REPO / "research/experiment_registry.csv").read_text(encoding="utf-8").splitlines()[1:]
    ids = sorted(line.split(",")[0] for line in registry if line)
    assert [e["id"] for e in data["experiments"]] == ids
    claims = {line.split(",")[0] for line in (REPO / "research/claims_register.csv").read_text(encoding="utf-8").splitlines()[1:] if line}
    exported = {c for e in data["experiments"] for c in e["claim_ids"]}
    assert exported == claims
    for e in data["experiments"]:
        assert e["status"] and e["verdict"]


def test_sources_are_hashed_and_no_timestamp(export):
    data = export.build()
    assert all(len(s["sha256"]) == 64 for s in data["sources"])
    text = export.serialize(data)
    assert "created_utc" not in text and "T00:" not in text
    assert len(data["contrast_map"]) == 48 + 72 + 72


def test_sandbox_fixture_matches_the_python_engine():
    fixture = _load("export_sandbox_fixture", "scripts/export_sandbox_fixture.py")
    committed = (REPO / "demo/src/fixtures/engine_fixture.json").read_text(encoding="utf-8")
    assert fixture.serialize(fixture.build()) == committed
