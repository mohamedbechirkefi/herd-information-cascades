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

## 2026-11-24: Session M2 (core implementation while the freeze is pending)

**Milestone:** M2 core implementation. The protocols remain unfrozen drafts; nothing confirmatory was run.

### Starting state

`git status`: on branch `main`, working tree clean; HEAD `cf2ab2c`.

### Implemented (`src/herd/`)

- `model.py` (typed, validated `Cell` and `Episodes`), `generate.py` (SeedSequence streams per (seed, cell), tie rule excluded from the key, separate coin stream), `rules.py` (independent baseline; Bayesian `complete` public-belief recursion and exact `window-k` recursion; naive imitation; own and coin tie rules; cascade flags; near-tie counting), `metrics.py`, `stats.py` (normal intervals, Student t tail, Wilson, bootstrap, Holm), `reference.py` (exact rational enumeration oracle and analytic anchor), `schema.py` with `schemas/config-v1.json`, `result-v1.json`, `manifest-v1.json`, `provenance.py` (config hash, git revision, versions, platform, peak RSS, protocol gate), `runner.py`, `serialize.py`, `report.py` (CSV and Markdown tables, SVG figures, report.md, report.pdf through pandoc and Typst), `cli.py` (`smoke`, `run`, `report`, `test`).
- Configurations in `experiments/`: `EXP-001-R001..R004.json` (exploratory) and `EXP-002.json`, `EXP-003.json` (confirmatory, refused while unfrozen).

### Commands run and actual outputs

| Command | Output |
|---|---|
| `.venv/bin/python -m pytest -q` (first full run) | `2 failed, 256 passed`: a test with inexact float arithmetic (test fixed), and check C4 failing at $q = 0.5$ (a real finding: the equivalence needs $q > 1/2$; check restricted, proposal P-2) |
| `PYTHONPATH=src uv run --frozen python -m herd.cli test -q` | `259 passed in 18.03s` (before commit `f15c0c2`) |
| `PYTHONPATH=src uv run --frozen python -m herd.cli smoke` | `EXPLORATORY run EXP-001-R001: 18 arms, 12 contrasts, 25 checks (0 failed), 0 failed cells`; runtime 0.07 s |
| `... run --config experiments/EXP-001-R002.json` | 72 arms, 48 contrasts, 61 checks (0 failed); runtime 9.81 s (simulation 5.68 s); peak RSS 123060224 bytes |
| `... run --config experiments/EXP-001-R003.json` | 108 arms, 72 contrasts, 89 checks (0 failed); runtime 22.34 s (simulation 16.24 s); peak RSS 144687104 bytes |
| `... run --config experiments/EXP-001-R004.json` | 24 arms, 16 contrasts, 17 checks (0 failed); runtime 3.26 s |
| `... run --config experiments/EXP-002.json` | `REFUSED: ... EXP-002 protocol is not frozen (registry protocol_sha256 = 'none (recorded at freeze)') ...`, exit code 3 |
| `... report --run results/exploratory/EXP-001-R00N` (N = 1..4) | tables, two SVG figures, report.md and report.pdf per run; PDFs of 4, 10, 12 and 4 pages, text extracted with pypdf, the EXPLORATORY banner present in each |
| First PDF build | long tables were cut at the page end (pandoc wraps Typst tables in unbreakable figures); fixed in commit `7aea99f` with breakable figures; pages inspected as PNG renders |
| `.venv/bin/python -m pytest -q` (after the report fix) | `259 passed` |

### Exploratory measurements (EXP-001, not evidence for any hypothesis)

- Verification: all checks passed in all four runs (C1 analytic anchor, C2 zero information, C3 independent baseline, C4 complete-network equivalence for $q > 1/2$, C5 schema, C6 no near ties; C7 found 0 Bayesian/imitation divergences under `complete` with coin ties).
- Throughput: 0.79 to 0.91 ms per 1,000 agent decisions (all rules). Projected full EXP-002: about 28 s of simulation and 16 s of analysis (five times R002); EXP-003: about 1.7 minutes (five times R003). Both are far below the one-hour budget.
- Seed spread: largest paired SD of a non-degenerate contrast 0.458 (R002) and 0.484 (R003), so the planned 10,000 episodes give a 95% half-width of at most about 0.0095 (planning value 0.01 holds). Between-seed SD of per-seed mean differences over the SD expected from independent episodes: median 0.98 (R002), 1.05 (R003).
- Degenerate cells: all 16 `window-1` contrasts in R002 have zero variance (both social rules equal the baseline exactly); proposal P-1.

### Decisions

D-006 (implementation choices), D-007 (amendment proposals recorded, not applied). Proposals: `research/amendment_proposals.md`.

### Files created or changed

Created: `src/herd/*` and schemas, `tests/*.py`, `experiments/*.json`, `results/exploratory/EXP-001-R001..R004/`, `research/amendment_proposals.md`. Changed: `roadmap.md`, `progress.md`, `research/experiment_registry.csv` (EXP-001 status), `research/experiment_journal.jsonl` (J-0002 to J-0005), `research/decision_log.md`, `research/publication/artifact_manifest.json`, READMEs in `src/`, `tests/`, `results/`, `experiments/`, `CONTRIBUTING.md` (commands appended). Git-ignored: `results/raw/EXP-001-R00N/episodes.npz`.

### Not done

- The 11.3 standalone report for EXP-001 (`research/experiments/EXP-001/report.md`) is left for M3; the generated run reports are its inputs.
- No confirmatory run, no protocol freeze, no push.
- Holm-adjusted or simultaneous intervals are not implemented pending the owner's choice (P-5).

### Outstanding risks

Tie detection relies on a relative tolerance; the exact oracle covers $N \le 9$ only, and the near-tie counter guards larger $N$. The literature review is still abstract-level.

### Next action

Owner: review `research/amendment_proposals.md` (especially P-1, `window-1` degenerate) and freeze the protocols. Then M3: run EXP-002 and EXP-003 under the frozen protocols and write the 11.3 reports.

## 2026-11-24: Session FREEZE (owner-approved amendments and protocol freeze)

**Milestone:** M1 gate. The owner approved the amendments and the freeze on 2026-11-24 (`../_shared/owner-approvals-2026-11-24.md`, HERD section). Nothing confirmatory was run.

### Starting state

`git status`: working tree clean; HEAD `5806678`. `.venv/bin/python -m pytest -q`: `259 passed`.

### Work

- Applied A-1 to A-5 (see `research/protocol.md` section 11; decision D-008) to `research/protocol.md`, the three EXP protocols, `research/feasibility.md` (fallback) and the two confirmatory configs (`window-2` in place of `window-1`).
- Code: `herd.runner.apply_holm` excludes degenerate contrasts from the Holm family (`holm_family = false`, `p_holm = null`); result schema allows a null `p_holm` and the `holm_family` flag; report text explains it; `herd.provenance.config_frozen` makes the run gate also require `research/freeze.json` to list the study protocol hash, the experiment protocol hash and the canonical config hash.
- Tests: Holm family exclusion (hand-computed), a degenerate `window-1` run reported outside Holm, synthetic freeze-record gate (accept, changed config, edited study protocol, missing record, unfrozen registry), `tests/test_freeze.py` (frozen configs pass the gate, six kinds of change refused, record hashes match the files, amendments present in the configs, CLI refuses a changed config with exit code 3). The tests call the gate only; no confirmatory run.
- Commit `c507f05` (amendments, code, tests), then the freeze record `research/freeze.json` (git revision `c507f05`), registry hashes and statuses, README, CITATION.cff and manuscript authorship (C3), roadmap and this entry.

### Commands and outputs

| Command | Output |
|---|---|
| `.venv/bin/python -m pytest -q --ignore=tests/test_freeze.py` (before the freeze record) | `261 passed` |
| `.venv/bin/python -m pytest -q` (after the freeze record and registry) | `278 passed` |
| `shasum -a 256 research/protocol.md` | `f73423c0bfd6f6463b1c1cb0d316e4ddc3942306eafe6793ba866112e72a457c` |

### Next action

M3, scheduled by the coordinator: run EXP-002 and EXP-003 under the frozen v1.0 protocols, then write the 11.3 reports (EXP-001 report included).
