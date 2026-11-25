# SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
"""Check that every relative link in the tracked Markdown files resolves (M6).

  .venv/bin/python scripts/check_links.py

A link `[text](target)` or `[text](target#anchor)` is checked when the target is not a URL
(http, https, mailto). The target must exist relative to the Markdown file; an anchor must match
a heading of the target file under GitHub's slug rule. Code spans and fenced code are skipped.
Exit status 0 when every link resolves, 1 otherwise.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)|!\[[^\]]*\]\(([^)\s]+)\)")
FENCE = re.compile(r"^(```|~~~)")
SKIP = ("http://", "https://", "mailto:")


def markdown_files(root: Path = ROOT) -> list[Path]:
    out = subprocess.run(["git", "ls-files", "*.md"], cwd=root, capture_output=True, text=True, check=True).stdout
    return [root / line for line in out.splitlines() if line and (root / line).exists()]


def slug(heading: str) -> str:
    text = re.sub(r"[`*_]", "", heading.strip().lower())
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def anchors(path: Path) -> set[str]:
    seen: dict[str, int] = {}
    result = set()
    in_fence = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
        if in_fence or not line.startswith("#"):
            continue
        s = slug(line.lstrip("#"))
        n = seen.get(s, 0)
        result.add(s if n == 0 else f"{s}-{n}")
        seen[s] = n + 1
    return result


def links(path: Path) -> list[tuple[int, str]]:
    found = []
    in_fence = False
    for no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        line = re.sub(r"`[^`]*`", "", line)
        for m in LINK.finditer(line):
            target = m.group(1) or m.group(2)
            if not target.startswith(SKIP):
                found.append((no, target))
    return found


def check(root: Path = ROOT) -> tuple[int, list[str]]:
    total, broken = 0, []
    for md in markdown_files(root):
        for no, target in links(md):
            total += 1
            file_part, _, anchor = target.partition("#")
            dest = md if not file_part else (md.parent / file_part).resolve()
            where = f"{md.relative_to(root)}:{no}: {target}"
            if not dest.exists():
                broken.append(f"{where} (missing file)")
            elif anchor and dest.suffix == ".md" and anchor.lower() not in anchors(dest):
                broken.append(f"{where} (missing anchor)")
    return total, broken


def main() -> int:
    total, broken = check()
    for b in broken:
        print(f"BROKEN {b}")
    files = len(markdown_files())
    print(f"links: {files} Markdown files, {total} relative links, {len(broken)} broken")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
