<!-- SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0 -->
# Progress journal (append-only)

## 2026-11-24: Session M0 (with M1 drafts)

**Milestone:** M0 bootstrap and feasibility; M1 protocol drafts.

### Starting state

`git status`: on branch `main`, working tree clean. One commit (`e8015cf`): master prompt and the owner's licence package.

### Commands run and actual outputs

| Command | Output |
|---|---|
| `sysctl -n machdep.cpu.brand_string hw.ncpu hw.memsize` | `Apple M1 Pro`, `10`, `17179869184` |
| `sw_vers` | macOS 15.3.1, build 24D70 |
| `df -h /Users/bechir/research/labs` | 460Gi size, 311Gi used, 128Gi available |
| `/usr/local/bin/python3 --version` | Python 3.12.1 |
| `.tools/py/bin/uv --version` | uv 0.9.5 (d5f39331a 2025-10-21) |
| `.tools/py/bin/typst --version` | no such file: typst is a Python package here, not a binary |
| `.tools/py/bin/python -c "import typst, pypdf, PIL"` | typst 0.15.0, pypdf 6.20.0, pillow 11.3.0 |
| `.tools/pandoc --version` | pandoc 3.6.3 (Mach-O arm64) |
| `/Users/bechir/research/helix/.tools/node/bin/node --version` | v22.23.3 |
| `git --version` | git version 2.42.1 |
| `which tex pdflatex xelatex` | not found (all three) |
| Toolchain smoke (exploratory, scratch directory): pandoc Markdown to Typst, typst compile | first attempt `TypstError: font fallback list must not be empty`; with `-V mainfont="Libertinus Serif"`: 1 page PDF, text extracted |
| `uv lock --python /usr/local/bin/python3` | `Resolved 8 packages`; uv.lock written (numpy 2.3.4, pytest 8.4.2, colorama 0.4.6, iniconfig 2.3.1, packaging 26.3, pluggy 1.7.0, pygments 2.21.0) |
| `uv sync --frozen` | installed the locked packages into `.venv` (git-ignored) |
| `uv run --frozen python -c "import numpy"` | numpy 2.3.4 |
| `uv run --frozen pytest` | `collected 0 items`, `no tests ran` (no tests exist yet) |

Literature and data searches: WebSearch and WebFetch; sources opened are listed with URLs in `research/literature_review.md`. The publisher page for BHW1992 at doi.org returned HTTP 403; the IDEAS record was used instead. PyPI JSON was read for numpy 2.3.4 (uploaded 2025-10-15) and pytest 8.4.2 (uploaded 2025-09-04).

### Decisions

D-001 licence (owner), D-002 synthetic data only, D-003 toolchain without TeX, D-004 draft protocol design choices, D-005 dependencies. See `research/decision_log.md`.

### Files created or changed

Created: `CLAUDE.md`, `roadmap.md`, `progress.md`, `README.md`, `CITATION.cff`, `pyproject.toml`, `uv.lock`, `data/manifest.json`, `research/` (decision_log, literature_review, protocol, feasibility, limitations, claims_register.csv, experiment_journal.jsonl, experiment_registry.csv, paper/manuscript.md skeleton, paper/figures/README.md, publication checklists and artifact manifest, experiments/EXP-001..003/protocol.md), READMEs in `results/`, `src/`, `tests/`, `experiments/`, `demo/`, `articles/`. Changed: `CONTRIBUTING.md` (development commands appended).

### Not done

No code, no tests, no experiments (by design). Section 11.1 files that would require results (`manuscript.tex`, `references.bib`, `supplementary.md`, `manuscript.pdf`, per-experiment `report.md`, `config.json`, `run_manifest.json`, `metrics.csv`, `reproduction.md`) were not created, to avoid placeholder artefacts. Full texts of the key papers were not read.

### Outstanding risks

Exact Bayesian `window-k` recursion is the main implementation risk; throughput is unmeasured. The literature review is abstract-level.

### Next action

Owner: review and freeze (or amend) the draft protocols. Meanwhile, M2: implement the independent baseline, the Bayesian `complete` rule and the verification tests.
