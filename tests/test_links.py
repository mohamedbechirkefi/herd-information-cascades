# SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
"""Relative Markdown links resolve (M6), and the checker detects broken ones."""

from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("check_links", ROOT / "scripts" / "check_links.py")
check_links = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check_links)


def test_every_relative_link_resolves():
    total, broken = check_links.check(ROOT)
    assert total > 0
    assert broken == []


def test_checker_detects_missing_file_and_anchor(tmp_path):
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    (tmp_path / "b.md").write_text("# Title\n\n## Section two\n", encoding="utf-8")
    (tmp_path / "a.md").write_text(
        "[ok](b.md) [ok anchor](b.md#section-two) [web](https://example.org/x)\n"
        "[bad file](missing.md) [bad anchor](b.md#nowhere) `[in code](missing2.md)`\n"
        "```\n[fenced](missing3.md)\n```\n",
        encoding="utf-8",
    )
    subprocess.run(["git", "add", "a.md", "b.md"], cwd=tmp_path, check=True)
    total, broken = check_links.check(tmp_path)
    assert total == 4
    assert len(broken) == 2
    assert any("missing.md (missing file)" in b for b in broken)
    assert any("b.md#nowhere (missing anchor)" in b for b in broken)


def test_slug_follows_github_rule():
    assert check_links.slug(" 5.1 EXP-001: verification (exploratory)") == "51-exp-001-verification-exploratory"
