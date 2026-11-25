# SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
"""Every decimal number in the README, CITATION.cff and the article drafts appears in the paper (M6).

The demo is covered by tests/test_demo_export.py. Version fields of CITATION.cff are excluded.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ["research/paper/manuscript.md", "research/paper/supplementary.md",
           "research/claims_register.csv", "research/limitations.md"]
PUBLIC = ["README.md", "CITATION.cff", *sorted(str(p.relative_to(ROOT)) for p in (ROOT / "articles").glob("*.md"))]
NUMBER = re.compile(r"(?<![\w.-])[+-]?(\d+(?:[.,]\d+)+)")


def _text(rel: str) -> str:
    text = (ROOT / rel).read_text(encoding="utf-8")
    if rel == "CITATION.cff":
        text = "\n".join(line for line in text.splitlines() if not re.match(r"^(cff-)?version:", line))
    return text


def test_public_numbers_appear_in_the_paper():
    pool = set(re.findall(r"\d+(?:[.,]\d+)+", " ".join((ROOT / s).read_text(encoding="utf-8") for s in SOURCES)))
    missing = {rel: sorted({n for n in NUMBER.findall(_text(rel)) if n not in pool}) for rel in PUBLIC}
    assert {k: v for k, v in missing.items() if v} == {}
    assert sum(len(NUMBER.findall(_text(rel))) for rel in PUBLIC) > 0
