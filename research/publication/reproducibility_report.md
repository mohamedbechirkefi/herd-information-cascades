<!-- SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0 -->
# Reproducibility report (M6, 2026-11-25)

Clean-clone reproduction of the release candidate, with the commands run and their actual outputs. Two clones were made, each with `git clone -q <repository> <scratch>/clone` (a local clone of HEAD, no network), and each was deleted at the end.

## Environment

- Machine: Apple M1 Pro, macOS 15.3.1 (Darwin 24.3.0).
- Python 3.12.1; dependencies from `uv.lock` with uv 0.9.5: numpy 2.3.4 (runtime), pytest 8.4.2, iniconfig 2.3.1, pluggy 1.7.0, packaging 26.3, Pygments 2.21.0 (test group). Full list with licences: `dependency_licences.md`.
- Node 22.23.3 (demo); npm packages from `demo/package-lock.json` (53 packages).
- PDF toolchain: pandoc 3.6.3 and the typst Python package 0.15.0 from the shared local `.tools` folder.

## Clone 1: HEAD `4cd8c92` (M5 state), started 2026-11-25T19:17:16Z

| Command (in the clone) | Actual output |
|---|---|
| `uv sync --frozen --all-groups --all-extras` | environment created; a second run: `Audited 6 packages` |
| `.venv/bin/python -m pytest -q -p no:cacheprovider` | `295 passed in 24.30s` |
| `PYTHONPATH=src .venv/bin/python -m herd.cli smoke` (after moving the committed EXP-001-R001 result aside) | `EXPLORATORY run EXP-001-R001: 18 arms, 12 contrasts, 25 checks (0 failed), 0 failed cells`; exit 0 |
| field-by-field comparison with the committed `results/exploratory/EXP-001-R001/result.json` | 42 differing leaves, excluding `created_utc` and `timing`: 18 `runtime_s`, 12 `holm_family`, 12 `p_holm`; every arm metric, contrast estimate, interval and check identical (exact float equality) |
| `herd.cli run --config experiments/EXP-001-R005.json` (committed result moved aside) | `EXPLORATORY run EXP-001-R005: 18 arms, 12 contrasts, 25 checks (0 failed), 0 failed cells`; 18 differing leaves, all `runtime_s` |
| `cmp` of the regenerated raw arrays with the working repository's | `results/raw/EXP-001-R001/episodes.npz` and `results/raw/EXP-001-R005/episodes.npz` byte-identical |
| `cd demo && npm ci --prefer-offline` | `added 53 packages in 510ms` |
| `npm test` | `Test Files 3 passed (3)`, `Tests 69 passed (69)` |
| `npm run build` | `✓ built in 387ms`; `dist/assets/index-*.js` 252.00 kB |
| `node tools/a11y_check.mjs dist` | 9 PASS lines, `A11Y-CHECK PASS` |
| `scripts/export_demo_data.py` and `scripts/export_sandbox_fixture.py`, then `git status --short` | `wrote demo/public/data/results.json: 4 experiments, 81 estimates, 192 contrasts, 24 cells, 25 sources`; `wrote demo/src/fixtures/engine_fixture.json (268393 bytes)`; 0 status lines (deterministic) |
| `herd.audit`; `herd.paper check` | `trace: 88 rows, 88 verified, 0 failed`; `coverage: 0 manuscript prose numbers without a trace row`; `all generated tables match the result files` |

**Smoke tolerance and reading.** The tolerance is exact equality for every estimate, interval, check and raw array; run times are excluded. The EXP-001-R001 differences are not a failure: R001 was produced at `f15c0c24`, before amendment A-3 at the freeze (degenerate contrasts excluded from the Holm family, D-008 and D-009), so its committed file predates the `holm_family` field; the current code fills `holm_family` and `p_holm` as the frozen protocol requires. EXP-001-R005, the smoke run on the frozen tree, reproduced exactly. Decision D-015, item 7.

## Findings in clone 1 and fixes (working repository)

No command failed. Findings from the other M6 checks, fixed in the working repository and committed in `802145d`:

1. Manuscript Table 2 and the EXP-001 report's execution-record table had overlapping cells in the PDF: column widths set (D-015, item 2).
2. `data/manifest.json` described the generator as not implemented: corrected (D-015, item 5).
3. Absolute home-directory paths in `README.md`, `demo/README.md`, `CONTRIBUTING.md` and `src/herd/report.py`: removed (D-015, item 5).
4. The PDF builder set no metadata title: added (D-015, item 1).

## Clone 2: HEAD `802145d` (after the fixes), started 2026-11-25T19:30:54Z

| Command (in the clone) | Actual output |
|---|---|
| `uv sync --frozen --all-groups --all-extras` | `Installed 6 packages in 43ms` |
| `.venv/bin/python -m pytest -q -p no:cacheprovider` | `299 passed in 10.15s` (295 plus 3 link tests and 1 public-number test) |
| `.venv/bin/python scripts/check_links.py` | `links: 49 Markdown files, 21 relative links, 0 broken` |
| `herd.audit`; `herd.paper check` | `trace: 88 rows, 88 verified, 0 failed`; `coverage: 0 manuscript prose numbers without a trace row`; `report tables: all generated rows present verbatim`; `all generated tables match the result files` |
| `herd.cli run --config experiments/EXP-001-R005.json` (committed result moved aside) | `EXPLORATORY run EXP-001-R005: 18 arms, 12 contrasts, 25 checks (0 failed), 0 failed cells`; 18 differing leaves, all `runtime_s`; raw arrays byte-identical (`cmp`) |
| `herd.cli smoke` (EXP-001-R001) | `18 arms, 12 contrasts, 25 checks (0 failed)`; same 42 differing leaves as in clone 1 (runtimes and the post-A-3 Holm fields) |
| `scripts/export_demo_data.py`, `scripts/export_sandbox_fixture.py`, `git status --short` | 0 status lines (deterministic) |
| `scripts/build_pdfs.py` (with `HERD_PANDOC` and `HERD_TYPST_PYTHON` pointing at the shared tools, since the clone has no neighbouring `.tools` folder), then `git status --short` | 6 PDFs and `manuscript.tex` written; 0 status lines (the committed PDFs and `manuscript.tex` rebuild byte for byte) |
| `cd demo && npm ci --prefer-offline`; `npm test`; `npm run build`; `node tools/a11y_check.mjs dist` | `added 53 packages`; `Tests 69 passed (69)`; `✓ built`; `A11Y-CHECK PASS` |

## Integrity checks (working repository)

| Check | Actual output |
|---|---|
| `shasum -a 256 -c results/EXP-002/SHA256SUMS` and `results/EXP-003/SHA256SUMS` (from the repository root) | 10 OK and 11 OK, 0 failures |
| `run_manifest.json` outputs present on disk, SHA-256 recomputed | 16 checked, 0 mismatches |
| `artifact_manifest.json`: 23 artifacts | 79 referenced paths, all exist; 16 file hashes match; 8 configuration hashes match the canonical hash (`herd.provenance.config_hash`) |
| `data/manifest.json` | no external dataset and no file hashes to check (synthetic data only); generator status corrected |

## Not reproduced

The confirmatory runs EXP-002-R001 and EXP-003-R001 and the exploratory EXP-004-R001 were not re-run at M6 (no confirmatory run is allowed in M6; their committed results and raw arrays are verified by hash above). Their full reproduction commands are in `README.md`.

## Home-directory paths (owner decision sheet item B9, 2026-11-26)

On 2026-11-26 the absolute home-directory paths were removed from the editable files that still had them: `CLAUDE.md` (6 lines, now paths relative to the repository such as `../.tools/` and "the research root" in words) and `research/feasibility.md` (4 lines, tool locations now relative to the repository). No command, script or source default used them; the PDF builder already resolves the shared tools relative to the repository (D-015, item 1). The history is not rewritten, so earlier commits keep the old text.

What remains in tracked files, and why: 2 lines in `progress.md` (the M0 entry of 2026-11-24, a `df -h` and a `node --version` command as run), kept because the journal is append-only. No frozen protocol, decision log, checksummed result file, run log or licence file contains such a path (scan of all tracked files with `grep -n "/Users/"`).
