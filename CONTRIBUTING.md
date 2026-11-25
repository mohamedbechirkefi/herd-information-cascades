<!-- SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0 -->
# Contributing to HERD

HERD is an independent, source-available research project maintained by Mohamed Bechir Kefi: collective decision-making.

Technical suggestions, bug reports, reproducibility results, corrections and Pull Requests are welcome. The project is available for non-commercial research under the HERD Source-Available Non-Commercial Research License v1.0 ([LICENSE](LICENSE)); it is not OSI-approved open-source software.

## 1. Before you start

For major changes, open an Issue first. Read `master_prompt.md`, `research/protocol.md` and `research/claims_register.csv`: frozen protocols are never changed silently, and every reported number must trace to a result file.

## 2. Pull Request requirements

- Your contribution is original or appropriately licensed, and you have the right to submit it.
- No credentials, secrets, confidential information or personal data.
- Relevant tests are included and pass; you report what you actually ran.
- Third-party dependencies and data sources are identified with their licenses.
- New files carry the header `SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0` where the format allows.
- You accept the Contributor License Agreement before your contribution is merged.

## 3. Contributor License Agreement

A recorded acceptance of [CLA.md](CLA.md) is required before merging copyrightable contributions. When you open a Pull Request, the "CLA Assistant" check comments on it; read the CLA, then post this exact comment:

    I have read the HERD CLA v1.0 and I hereby sign it

The check records your public GitHub username and account ID, the date and the PR. You sign once. If the check does not update, comment `recheck`. Checking a box is not a signature; the comment is.

The CLA lets the maintainer use, modify, distribute, relicense and commercially exploit accepted contributions. You keep the copyright in your original contributions.

## 4. Governance

Mohamed Bechir Kefi is the project owner and lead maintainer, and the only person who can change the protected `main` branch. The maintainer decides the research direction, protocol freezes, claims, releases and licensing.

## 5. Privacy and disclosure

Never commit an e-mail address, a name or any other personal identifier in code, logs, fixtures or results. Report security issues privately through GitHub's private vulnerability reporting.

## 6. Development commands

- Install the locked environment: `uv sync --frozen` (uv 0.9.5; Python 3.12).
- Refresh the lockfile after an approved dependency change: `uv lock` (resolution is limited by `exclude-newer` in `pyproject.toml`).
- Run the tests (once they exist, M2): `uv run pytest`.
- Command line (M2; the package is run from `src/`):
  - `PYTHONPATH=src uv run --frozen python -m herd.cli smoke` (exploratory EXP-001 smoke matrix)
  - `PYTHONPATH=src uv run --frozen python -m herd.cli run --config experiments/<file>.json` (confirmatory configurations are refused while the protocol is unfrozen)
  - `PYTHONPATH=src uv run --frozen python -m herd.cli report --run results/exploratory/<run_id>` (needs pandoc and the typst Python package; `--no-pdf` skips the PDF; paths via `HERD_PANDOC` and `HERD_TYPST_PYTHON`)
  - `PYTHONPATH=src uv run --frozen python -m herd.cli test`
  - `PYTHONPATH=src uv run --frozen python -m herd.robustness --reference results/EXP-002/EXP-002-R001 --sensitivity results/EXP-003/EXP-003-R001` (EXP-003 decision rule)
  - `PYTHONPATH=src uv run --frozen python -m herd.tables contrasts|secondary --run <run dir>` (11.3 report tables)
  - `PYTHONPATH=src uv run --frozen python -m herd.exploratory --out results/exploratory/EXP-004-derived` (EXP-004 derived analyses, exploratory; refuses an existing output)
  - `PYTHONPATH=src uv run --frozen python -m herd.paper fill|check` (manuscript and supplementary tables from committed results; `check` fails on a stale table)
  - `PYTHONPATH=src uv run --frozen python -m herd.audit` (evidence audit: number trace, coverage, report tables)
  - `PYTHONPATH=src uv run --frozen python -m herd.manifest` (writes `research/publication/artifact_manifest.json`)
  - `.venv/bin/python scripts/export_demo_data.py` (writes `demo/public/data/results.json` from committed results; `--check` fails if it is stale)
  - `.venv/bin/python scripts/export_sandbox_fixture.py` (writes `demo/src/fixtures/engine_fixture.json`, the Python-engine fixture for the demo's TypeScript port)
- Demo (M5; Node 22): `cd demo && npm ci && npm test && npm run build && npm run preview`; accessibility and offline check `node tools/a11y_check.mjs dist --screenshots <folder>`.
