# SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0
"""Build the publication PDFs and manuscript.tex (M6).

  .venv/bin/python scripts/build_pdfs.py             manuscript, supplementary and experiment-report PDFs, manuscript.tex
  .venv/bin/python scripts/build_pdfs.py --keep-typ  also keep the intermediate .typ files (for page rendering)

The run reports under results/ are part of the frozen results and are built by `herd.cli report`, not here.
PDFs: Markdown -> Typst with pandoc, compiled with the typst Python package (decision D-003).
manuscript.tex: generated from Markdown with pandoc; not compiled locally (no TeX distribution).
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from herd.report import PANDOC, build_pdf  # noqa: E402

AUTHOR = "Mohamed Bechir Kefi"  # owner-approved author line (common decision C3)
TARGETS = [ROOT / "research/paper/manuscript.md", ROOT / "research/paper/supplementary.md",
           *sorted((ROOT / "research/experiments").glob("EXP-*/report.md"))]


def build_tex(md: Path) -> Path:
    tex = md.with_suffix(".tex")
    subprocess.run([PANDOC, md.name, "-s", "-o", tex.name], cwd=md.parent, check=True)
    tex.write_text("% SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0\n% Generated from manuscript.md by scripts/build_pdfs.py; do not edit.\n"
                   + tex.read_text(encoding="utf-8"), encoding="utf-8")
    return tex


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--keep-typ", action="store_true")
    args = parser.parse_args(argv)
    for md in TARGETS:
        pdf = build_pdf(md, keep_typ=args.keep_typ, author=AUTHOR, page_numbers=True)
        print(f"wrote {pdf.relative_to(ROOT)} ({pdf.stat().st_size} bytes)")
    tex = build_tex(ROOT / "research/paper/manuscript.md")
    print(f"wrote {tex.relative_to(ROOT)} ({tex.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
