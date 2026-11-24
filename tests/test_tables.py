# SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
"""Report tables are generated from a result, one row per contrast and per arm."""

import copy

from herd.runner import run
from herd.tables import contrasts_table, secondary_table
from test_pipeline import BASE


def test_tables_have_one_row_per_contrast_and_arm():
    res = run(copy.deepcopy(BASE)).result
    assert len(contrasts_table(res).splitlines()) == 2 + len(res["contrasts"])
    assert len(secondary_table(res).splitlines()) == 2 + len(res["arms"])
    assert "n/a" in contrasts_table(res)  # degenerate q=0.5 contrasts sit outside the Holm family
