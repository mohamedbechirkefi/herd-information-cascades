# SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
"""Evidence audit (number trace, coverage, report tables) and generated manuscript tables."""

import pytest

from herd import audit, paper


def test_token_value_precision():
    assert audit.token_value("0.0059") == pytest.approx((0.0059, 0.00005), rel=1e-6)
    v, tol = audit.token_value("3.1 \\times 10^{-14}")
    assert v == pytest.approx(3.1e-14) and tol == pytest.approx(0.05e-14, rel=1e-6)
    assert audit.token_value("48") == (48.0, pytest.approx(0.5))


def test_filters_and_fields():
    rows = [{"a": "1", "b": "x", "c": "0.2"}, {"a": "2", "b": "y", "c": "-0.1"}, {"a": "3", "b": "x", "c": "0.5"}]
    assert len(audit._filter(rows, "b=x")) == 2
    assert len(audit._filter(rows, "b!=x")) == 1
    assert len(audit._filter(rows, "a>1,c<0.4")) == 1
    assert len(audit._filter(rows, "?float(c)>0 or float(a)==2")) == 3
    assert audit._get({"x": 2.0, "y": 0.5}, "=x*y") == 1.0
    with pytest.raises(ValueError):
        audit._agg([1, 2], None)


def test_selector_detects_wrong_token():
    sel = "contrast|results/EXP-002/EXP-002-R001|rule=imitation,q=0.55,network=window-2,v=0.5|mean"
    value = audit.resolve(sel)
    for tok, ok in (("0.0059", True), ("0.0058", False), ("0.006", True), ("0.0060", False)):
        t, tol = audit.token_value(tok)
        assert (abs(value - t) <= tol) is ok


def test_repository_audit_passes():
    trace, bad = audit.check_trace()
    assert len(trace) > 50 and bad == []
    assert audit.check_coverage(trace) == []
    assert audit.check_report_tables() == []
    assert paper.main(["check"]) == 0
