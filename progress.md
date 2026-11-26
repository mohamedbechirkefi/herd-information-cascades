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

## 2026-11-24: Session RATIFY (owner's second-round decisions)

**Milestone:** records only, before M3. Nothing confirmatory was run.

### Work

- The owner answered "Approve all" (`../_shared/owner-approvals-2026-11-24b.md`); the HERD item ratifies the freeze-time choices A-3 (zero-variance contrasts outside the Holm family) and A-4 (unadjusted 95% intervals, decisions on Holm-adjusted p-values). Recorded as D-009 and as R-1 in `research/freeze.json` (`ratifications`).
- No protocol, config or code changed; all frozen hashes unchanged. No other second-round item applies to HERD.

### Next action

M3, scheduled by the coordinator: run EXP-002 and EXP-003 under the frozen v1.0 protocols.

## 2026-11-25: Session M3 (confirmatory experiments)

**Milestone:** M3, started on the owner's "Start next" (2026-11-25) under the coordinator's M3 brief. Gate met: complete planned matrices, no failed or dropped run.

### Pre-run checks

- `git status --porcelain`: empty at `eded9b8`. `shasum -a 256` of `research/protocol.md`, `research/experiments/EXP-00{1,2,3}/protocol.md`, `experiments/EXP-002.json`, `experiments/EXP-003.json` and `herd.provenance.config_hash` of both configs: all equal to `research/freeze.json`.
- `../.tools/py/bin/uv sync --frozen --all-groups --all-extras`: "Audited 6 packages". No editable install (`import herd` fails without `PYTHONPATH=src`). `.venv/bin/python -m pytest -q`: 278 passed.
- Data: synthetic only (`data/manifest.json`); nothing to rebuild.
- Smoke run EXP-001-R005 (`experiments/EXP-001-R005.json`, smoke matrix on exploratory seeds 100 and 101): 25 checks, 0 failed, 0.05 s. Known-case metric and statistics tests (`tests/test_metrics_stats.py`, `tests/test_reference.py`): 132 passed. Journal J-0006. Committed as `50fbdb1`, the provenance revision of both confirmatory runs.

### Confirmatory runs (one process, `nice -n 10`)

- `PYTHONPATH=src nice -n 10 .venv/bin/python -m herd.cli run --config experiments/EXP-002.json`: "CONFIRMATORY run EXP-002-R001: 72 arms, 48 contrasts, 61 checks (0 failed), 0 failed cells; runtime 8.73 s"; exit 0. Journal J-0007.
- `PYTHONPATH=src nice -n 10 .venv/bin/python -m herd.cli run --config experiments/EXP-003.json`: "CONFIRMATORY run EXP-003-R001: 108 arms, 72 contrasts, 89 checks (0 failed), 0 failed cells; runtime 19.47 s"; exit 0. Journal J-0008.
- `herd.cli report --run` for both runs; `herd.robustness`: "72 comparisons: {'robust': 70, 'lost significance': 2}".

### Results (frozen analysis)

- EXP-002: Holm family 48 (no degenerate contrast); all 48 contrasts positive and Holm-significant; range +0.0059 [0.0048, 0.0070] to +0.1439 [0.1375, 0.1504]. H1 supported; the imitation directional expectation is contradicted.
- EXP-003: 70 of 72 comparisons robust, none reverses sign; under coin ties the two contrasts at q = 0.55, window-3, v = 1 lose significance (Holm p 0.18): convention-dependent.
- Reports: `research/experiments/EXP-001/report.md`, `EXP-002/report.md`, `EXP-003/report.md`. Claims CLM-001 to CLM-009. Limitations 8 to 11. Decision D-010.

### Post-run additions (no estimate changed; D-010)

- `src/herd/report.py`: figure captions now carry the run label (they said "Exploratory." for every run); test added; run reports regenerated.
- `src/herd/robustness.py` (EXP-003 rule) and `src/herd/tables.py` (report tables), with tests.
- Confirmatory raw arrays committed; `results/EXP-00N/SHA256SUMS` (`shasum -a 256 -c` passes for all 10 and 11 files).

### Tests

`.venv/bin/python -m pytest -q`: 281 passed (278 before plus 3 new).

### Next action

M4: evidence audit, manuscript synthesis with the EXP-003 caveat and the contradicted imitation expectation, second review pass challenging the preferred hypothesis.

## 2026-11-25: Session M4 (interpretation, evidence audit and manuscript)

**Milestone:** M4, under the coordinator's M4 brief (owner: "Approve all recommendations, push then next", 2026-11-25). No owner follow-up of 2026-11-25 is specific to HERD. No confirmatory rerun; no frozen protocol, config or seed changed.

### Work

- **Confounder inspection and sensitivity.** Competing explanations of the study protocol section 9 and EXP-002 section 3 checked against committed results (`research/publication/evidence_audit.md` section 5). Gaps closed by a cheap exploratory experiment, EXP-004 (protocol committed first at `3831429`; D-011):
  - `PYTHONPATH=src nice -n 10 .venv/bin/python -m herd.cli run --config experiments/EXP-004-R001.json`: "EXPLORATORY run EXP-004-R001: 108 arms, 72 contrasts, 89 checks (0 failed), 0 failed cells; runtime 20.50 s (simulation 13.61 s, 0.145 ms per 1000 decisions), peak RSS 305086464 bytes"; exit 0. Journal J-0009.
  - `herd.robustness --reference results/EXP-002/EXP-002-R001 --sensitivity results/exploratory/EXP-004-R001`: "72 comparisons: {'robust': 72}".
  - `PYTHONPATH=src .venv/bin/python -m herd.exploratory --out results/exploratory/EXP-004-derived` (at `f2c91ff`): share below baseline 0.0496 to 0.4252; last-agent delta 0.0067 to 0.1595, 48 of 48 intervals exclude zero; imitation minus Bayesian: 11 of 24 intervals exclude zero, complete cells all zero. Journal J-0010.
- **Expected versus observed:** manuscript Table 6.
- **Claims register:** CLM-001 to CLM-015, with result ID, config hash, table or figure, manuscript section and trace IDs; CLM-002 and CLM-009 unit wording corrected.
- **Evidence audit:** `src/herd/audit.py`, `src/herd/paper.py`, `src/herd/manifest.py`; `research/publication/number_trace.csv` (88 rows), `artifact_manifest.json` (23 artifacts), `evidence_audit.md` (findings F-1 to F-8), `claims_audit.md`. EXP-002 and EXP-003 reports edited with dated notes (units, one unsourced phrase, CK2004 and BHW1992 tie convention marked unverified); no number changed. BHW1992 title checked against Crossref.
- **Manuscript:** `research/paper/manuscript.md` v1.0 (about 4,860 words of prose before the references, abstract 247 words, title revised) and `research/paper/supplementary.md`; 9 generated tables.
- **Second review pass:** `research/publication/review_pass_2.md`; six challenges, four of which led to manuscript changes (tie-convention magnitudes, mean versus group outcome and title, practical threshold, scope of the imitation result).
- **Records:** limitations 9 to 11 updated and 12 to 15 added; D-011; registry row EXP-004; roadmap M4 done.
- **Refused file.** The write tool refused `research/experiments/EXP-004/report.md` (the twelve-section 11.3 report of EXP-004). Per the brief it was not written by other means; its full text is returned to the coordinator. The generated run report `results/exploratory/EXP-004-R001/report.md` exists.

### Checks

| Command | Output |
|---|---|
| `PYTHONPATH=src .venv/bin/python -m herd.audit` | `trace: 88 rows, 88 verified, 0 failed`; `coverage: 0 manuscript prose numbers without a trace row`; `report tables: all generated rows present verbatim`; `all generated tables match the result files` |
| `shasum -a 256 -c results/EXP-002/SHA256SUMS results/EXP-003/SHA256SUMS` | 21 OK, 0 failed |
| `.venv/bin/python -m pytest -q` | `289 passed` (281 before plus 4 in `tests/test_exploratory.py` and 4 in `tests/test_audit.py`) |

### Next action

The coordinator writes `research/experiments/EXP-004/report.md` from the returned text; then M5 (interactive page) with the M4 labels. Open for the owner: review of the revised title, the manuscript and the AI-assistance statement; the full texts of BHW1992, CK2004 and ER2010 remain unread.

## 2026-11-25: M4 done (coordinator)

The M4 session composed the file(s) the write tool refused from committed results; the coordinator wrote them after checking that every decimal number appears in a committed file. With the manuscript, evidence audit and second review pass already committed, the M4 gate holds. M4 is **done**.

## 2026-11-25: Post-M4 owner decisions applied (items 1 and 2)

**Authority.** Owner, 2026-11-25, "Approve all" (post-M4) (`../_shared/owner-approvals-2026-11-25c.md`). Decision D-012.

**Changes.**
- Item 1: the M4 title is approved; the manuscript status line records the approval (one sentence added, no line added).
- Item 2: the funding, competing-interest and AI-use wording of manuscript section 11 is recorded as owner-approved (D-012). No wording changed.

**Commands and actual outputs.**

| Command | Output |
|---|---|
| `.venv/bin/python -m pytest -q` | `289 passed` |
| `PYTHONPATH=src .venv/bin/python -m herd.audit` | `trace: 88 rows, 88 verified, 0 failed`; `coverage: 0 manuscript prose numbers without a trace row`; `report tables: all generated rows present verbatim`; `all generated tables match the result files` |
| `PYTHONPATH=src .venv/bin/python -m herd.paper check` | `all generated tables match the result files` |

No `manuscript.tex` or PDF exists in this repository yet; both are left to M6.

### Owner placeholders for M5

1. `research/paper/manuscript.md` section 10: "public URL: to be added after the owner approves publication". The owner supplies the repository URL at release.
2. `research/publication/author_review.md`: every item of the owner review checklist is open and can be completed only by the owner.

No other placeholder needing an owner-only fact was found in the manuscript, supplementary, `README.md` or `CITATION.cff`. Observed but outside this session's items: `README.md` still describes the M4 interpretation and the EXP-001 report as pending (stale status text, for M5).

**Next action.** M5 (interactive page) with the M4 labels.

## 2026-11-25: Session M5 (interactive experience)

**Milestone:** M5, under the coordinator's M5 brief. Authority: owner, 2026-11-25, "Next" (`../_shared/owner-approvals-2026-11-25d.md`), with the master prompt's default stack (TypeScript, React, Vite) pinned from the shared template. No frozen protocol, config, seed or result changed; no confirmatory run; nothing pushed. Decisions D-013 and D-014.

### Work

- `demo/` copied from `labs/_shared/demo-template/` (without `node_modules`; `.npmrc`, `package.json` and `package-lock.json` unchanged); `npm ci --prefer-offline`: "added 53 packages".
- `scripts/export_demo_data.py` writes `demo/public/data/results.json`: 4 experiments, 81 estimates, 192 contrasts, 24 cells, 25 hashed sources, no timestamp. Extensions validated fail-closed in `demo/src/results.ts`.
- `scripts/export_sandbox_fixture.py` writes `demo/src/fixtures/engine_fixture.json` (48 cells, seed 7, 16 episodes of 12 agents; 0.2 s).
- Page (`demo/src/App.tsx`, `charts.tsx`, `Sandbox.tsx`, `engine.ts`, `simulate.ts`, `sandbox.worker.ts`, `style.css`): overview with status label; forest plot of every contrast with intervals (EXP-002, EXP-003 V1 to V3, EXP-004 V1 to V3), hollow same-size marks for contrasts that are not significant or lost significance; one panel per experiment; EXP-002 accuracy distributions; assumptions; method and limitations; sandbox with an animated cascade replay, scenario, rule, q, network, visibility, ties, N, episodes and seed controls, Run, Cancel, Reset and an animation switch.
- `tests/test_demo_export.py` (6 tests): fresh export identity, determinism, every display string in the manuscript or supplementary or a documented exception (4 C1 interval texts), every registered experiment and claim exported, hashed sources, sandbox fixture reproduced by the Python engine.
- Text alignment: `README.md`, `CITATION.cff`, `articles/medium.md` and `articles/linkedin.md` (new drafts), `articles/README.md`, `demo/README.md`, `CONTRIBUTING.md` (commands appended). Every decimal number in README, CITATION.cff and the two articles was checked to appear in the manuscript, supplementary, claims register or limitations (script output: no missing number besides `cff-version` 1.2).
- Manuscript section 5.1 and Table 6: C1 wording corrected (D-014); no number changed.
- `docs/demo.png` (95,908 bytes): sandbox section after a run, seed 1, default settings.
- Screenshots inspected with the Read tool (desktop light, desktop dark, mobile, sandbox after a run on desktop and on mobile in dark mode). Fixed during inspection: a select overflowing at 360 px (two places), table regions inside closed `details` counted as focusable (content now rendered only when open), spacing of the cascade marker in the strip.

### Commands and actual outputs

| Command | Output |
|---|---|
| `.venv/bin/python scripts/export_demo_data.py --check` | `results.json is up to date` |
| `.venv/bin/python -m pytest -q` | `295 passed` (289 before plus 6 in `tests/test_demo_export.py`) |
| `PYTHONPATH=src .venv/bin/python -m herd.audit` | `trace: 88 rows, 88 verified, 0 failed`; `coverage: 0 manuscript prose numbers without a trace row`; `report tables: all generated rows present verbatim`; `all generated tables match the result files` |
| `cd demo && npm test` | `Test Files 3 passed (3)`, `Tests 69 passed (69)` (engine port 51, results validator 14, sandbox simulation 4) |
| `npm run build` | `✓ built`; `dist/assets/index-*.js` 251.92 kB, worker 5.36 kB |
| `node tools/a11y_check.mjs dist` on a copy of `dist` with a malformed `results.json` | `FAIL results render (no fail-closed panel): 0 experiment panels`, `A11Y-CHECK FAIL (2)` (fail-closed confirmed) |

`node tools/a11y_check.mjs dist --screenshots <scratchpad>/herd/shots`, full output:

```
PASS results render (no fail-closed panel): 4 experiment panels
PASS text contrast, light scheme (WCAG AA)
PASS text contrast, dark scheme (WCAG AA)
PASS keyboard reaches every focusable element: 30 reached of 30
PASS visible focus indicator
PASS no horizontal page scroll at 360 px: overflow 0px
PASS reduced motion: no running animations: 0 running
PASS no request leaves the local origin
PASS offline after first load: results stay, sandbox runs: Sandbox run complete (seed 1, 500 episodes of 30 agents): Bayesian minus indepen
A11Y-CHECK PASS
```

The checker is the template's, unchanged apart from its SPDX line.

### Gate

M5 gate holds: offline after the initial load, responsive at 360 px, usable with the keyboard, reduced-motion option, no fabricated data, no runtime service. M5 **done**.

### Owner placeholders remaining

Repository URL and demo URL ("to be added after the owner approves publication") in the manuscript section 10, README, CITATION.cff, articles, page footer and `demo/README.md`; the owner review checklist (`research/publication/author_review.md`, all boxes open). Author line, affiliation, funding and competing interests are owner-approved (C3, D-012).

### Next action

M6: clean-clone reproduction, PDFs, link and licence scans, owner review checklist; the owner's full-text review of the manuscript (including the D-014 wording edit).

## 2026-11-25: Session M6 (release candidate)

**Milestone:** M6, under the coordinator's M6 brief. Authority: owner, 2026-11-25, "Next" (second) (`../_shared/owner-approvals-2026-11-25e.md`). Nothing pushed, tagged or released; no frozen protocol, config, seed or result changed; no confirmatory run. Decision D-015. Commits `802145d` (work) and the records commit that follows it.

### Work

- Clean clones (two, both deleted): full results in `research/publication/reproducibility_report.md`.
- PDFs: `scripts/build_pdfs.py` (new) with an extended `build_pdf` (metadata title, author, page numbers, no creation date). Built `research/paper/manuscript.pdf` (13 pages, 284,401 bytes), `supplementary.pdf` (19 pages), `research/experiments/EXP-001/report.pdf` (3), `EXP-002` (13), `EXP-003` (20), `EXP-004` (5), and `manuscript.tex`. Pages rendered to PNG at 60 to 80 ppi in scratch and read: all 13 manuscript pages, the first page of each report, table pages of EXP-002, EXP-003 and the supplementary. Fixed: overlapping cells in manuscript Table 2 and in the EXP-001 execution-record table. Metadata (pypdf): title and author set in all 6, 0 e-mail addresses, 0 local paths. Two builds gave the same MD5.
- References: 9 of 9 cited and resolved. Full texts (free, legal) read: BHW1992 (published), ADLO2011, CK2004, ER2010, W2008wp (working-paper versions); abstract only: Banerjee1992, SS2000 (MIT DSpace copy refused with HTTP 429), GJ2010 (three-page author version only), AH1997; unverified: 0. F-5 resolved: BHW1992 section II.A, p. 996, coin-flip tie convention; footnote 13, p. 1000, "indifferent individuals adopt" in the general model. Manuscript section 2 and reference note, CK2004 sentence, EXP-002 and EXP-003 reports (dated notes), `research/limitations.md` item 13 and `research/publication/evidence_audit.md` section 3.1 updated. No number changed.
- Links and numbers: `scripts/check_links.py` and `tests/test_links.py` (3 tests); `tests/test_public_numbers.py` (README, CITATION.cff and articles against the paper).
- Scans: 0 e-mail addresses, 0 keys or tokens, 0 private-key headers, 0 `.env` files in tracked files. Home-directory paths removed from `README.md`, `demo/README.md`, `CONTRIBUTING.md`, `src/herd/report.py`. *Note on this journal:* earlier entries of this file contain two lines with absolute tool paths (M0 entry); they are left as recorded (append-only), as are 6 lines in `CLAUDE.md` and 4 in `research/feasibility.md`.
- `research/publication/dependency_licences.md`: 6 Python, 53 npm packages; no flag (notes: lightningcss MPL-2.0 build-only; pandoc GPL-2.0-or-later as a local tool).
- `CITATION.cff`: `version: 0.1.0-rc1`; `date-released` already absent, left absent; structural check against CFF 1.2.0 keys and types passed; `preferred-citation.title` equals the manuscript title.
- `data/manifest.json`: stale generator status corrected.
- `demo/public/data/results.json` re-exported (source hashes of the edited limitations file changed; no number changed).
- `research/publication/author_review.md`: 0 ticked boxes found, none ticked; section "Prepared for the owner (M6, 2026-11-25)" added with reading paths, open decisions and 11 placeholder locations. `release_checklist.md`: items 1 to 11 ticked with evidence; the two owner items open.

### Commands and actual outputs (working repository)

| Command | Output |
|---|---|
| `.venv/bin/python -m pytest -q -p no:cacheprovider` | `299 passed` |
| `PYTHONPATH=src .venv/bin/python -m herd.audit` | `trace: 88 rows, 88 verified, 0 failed`; `coverage: 0 manuscript prose numbers without a trace row`; `report tables: all generated rows present verbatim`; `all generated tables match the result files` |
| `PYTHONPATH=src .venv/bin/python -m herd.paper fill` | `research/paper/manuscript.md: 5 generated tables`; `research/paper/supplementary.md: 4 generated tables` |
| `.venv/bin/python scripts/export_demo_data.py --check` | `results.json is up to date` |
| `.venv/bin/python scripts/check_links.py` | `links: 49 Markdown files, 21 relative links, 0 broken` |
| `cd demo && npm test` | `Test Files 3 passed (3)`, `Tests 69 passed (69)` |
| `npm run build`; `node tools/a11y_check.mjs dist` | `✓ built`; `A11Y-CHECK PASS` |
| `shasum -a 256 -c results/EXP-002/SHA256SUMS`, `results/EXP-003/SHA256SUMS` | 10 OK, 11 OK |
| artifact manifest check (23 artifacts) | 79 paths exist; 16 file hashes and 8 canonical config hashes match |

### Status

M6: release candidate prepared, awaiting owner review and G-PUBLIC. Not done until the owner signs off `research/publication/author_review.md`.

### Next action

The owner's review: `research/publication/author_review.md` (section "Prepared for the owner"), then a G-PUBLIC decision.

## 2026-11-26: Owner answers of 2026-11-26 applied (wording and configuration)

**Authority:** owner, 2026-11-26, decision sheet (`../_shared/owner-decision-sheet-2026-11-26.md`, `../_shared/owner-approvals-2026-11-26.md`), applied under the coordinator's brief `../_shared/OWNER-ANSWERS-brief.md`. Decision D-016. No push, no deploy, no box of `author_review.md` ticked. No result, analysis, figure, configuration, seed, frozen protocol, protocol hash or checksummed output changed. `git status` was clean at the start.

### Work

- A1, B1, B2: repository and demo URLs filled (`CITATION.cff` with `repository-code`, `README.md`, `demo/README.md`, both articles, manuscript section 10, page footer in `demo/src/App.tsx`); out-of-date "nothing published" sentences corrected. `demo/wrangler.jsonc` added (assets only, `./dist`). Footer text wraps (`overflow-wrap: anywhere` in `demo/src/style.css`).
- B3: author line "Mohamed Bechir Kefi, independent researcher" in the manuscript, the four experiment reports (identification section only), `CITATION.cff` (`affiliation`), README, articles and page footer. B7: `CITATION.cff` `title` set to the manuscript title.
- B8, B13, R-HERD-1: `release_checklist.md` gains a dated status update, a version note and "Release notes (draft)".
- B9: home paths replaced in `CLAUDE.md` and `research/feasibility.md`; 2 lines remain in this journal's M0 entry (listed in `reproducibility_report.md`).
- `author_review.md`: placeholder list updated (none remain), section "Owner answers recorded (2026-11-26)" added; 0 boxes ticked.

### Commands and actual outputs

| Command | Output |
|---|---|
| `.venv/bin/python scripts/build_pdfs.py` | manuscript.pdf (284490 bytes), supplementary.pdf (587481), EXP-001 to EXP-004 report.pdf, manuscript.tex; supplementary.pdf unchanged byte for byte (its source did not change) |
| typst PNG render (70 ppi, scratch) of manuscript pages 1, 12, 13 and EXP-002 report page 1 | read: author line, section 10 URLs and section 11 statements render correctly, no overlap; pypdf: author line found on page 1 of all four reports; metadata author "Mohamed Bechir Kefi" |
| `.venv/bin/python -m pytest -q -p no:cacheprovider` | `299 passed in 7.73s` |
| `PYTHONPATH=src .venv/bin/python -m herd.audit` | `trace: 88 rows, 88 verified, 0 failed`; `coverage: 0 manuscript prose numbers without a trace row`; `all generated tables match the result files` |
| `.venv/bin/python scripts/export_demo_data.py --check` | `results.json is up to date` |
| `.venv/bin/python scripts/check_links.py` | `links: 49 Markdown files, 21 relative links, 0 broken` |
| `cd demo && npm test` | `Test Files 3 passed (3)`, `Tests 69 passed (69)` |
| `npm run build`; `node tools/a11y_check.mjs dist` | `✓ built in 169ms`; 9 PASS lines including "no request leaves the local origin", `A11Y-CHECK PASS` |
| `git ls-files \| xargs grep -n "/Users/"` | 2 lines, both in `progress.md` (M0 entry) |

### Next action

The owner: B15 (articles), B16 (full-text review and sign-off of `research/publication/author_review.md`), B18 (release). The coordinator deploys the demo from `demo/dist` with `demo/wrangler.jsonc`.
