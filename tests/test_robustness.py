# SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
"""EXP-003 decision rule on hand-built contrasts."""

from herd.robustness import compare, convention_dependent


def _c(rule, delta, p_holm, variation="main", q=0.55, net="window-3", v=1.0, family=True):
    return {"variation": variation, "rule": rule, "mean": delta, "ci_low": delta - 0.01, "ci_high": delta + 0.01,
            "p_holm": p_holm, "holm_family": family,
            "cell": {"q": q, "network": net, "v": v, "n_agents": 50, "tie_rule": "own"}}


def test_statuses():
    ref = {"contrasts": [_c("bayesian", 0.04, 1e-9), _c("imitation", 0.04, 1e-9), _c("bayesian", 0.01, 0.2, net="complete")]}
    sen = {"contrasts": [
        _c("bayesian", 0.03, 0.001, variation="V1"),
        _c("imitation", 0.008, 0.18, variation="V1"),
        _c("bayesian", -0.02, 0.001, variation="V2"),
        _c("imitation", 0.0, None, variation="V2", family=False),
        _c("bayesian", 0.5, 1e-9, variation="V1", net="complete"),  # not significant in the reference: skipped
    ]}
    rows = compare(ref, sen)
    st = {(r["variation"], r["rule"]): r["status"] for r in rows}
    assert st == {("V1", "bayesian"): "robust", ("V1", "imitation"): "lost significance",
                  ("V2", "bayesian"): "sign reversed", ("V2", "imitation"): "sign reversed"}
    assert convention_dependent(rows) == [("bayesian", 0.55, "window-3", 1.0), ("imitation", 0.55, "window-3", 1.0)]
