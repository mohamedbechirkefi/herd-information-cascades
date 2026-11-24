<!-- SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0 -->
# src/

Python package `herd` (M2). Run with `PYTHONPATH=src` from the repository root (decision D-006).

| Module | Role |
|---|---|
| `model.py` | typed and validated `Cell` (q, network, v, N, tie rule) and `Episodes` |
| `generate.py` | seeded episode generation, common random numbers across rules and tie rules |
| `rules.py` | independent baseline, Bayesian (`complete` and exact `window-k`), naive imitation |
| `metrics.py` | per-episode metrics of protocol section 4 |
| `stats.py` | intervals, Student t tail, Wilson, bootstrap, Holm |
| `reference.py` | exact rational enumeration oracle (small N) and the analytic cascade anchor |
| `schema.py`, `schemas/` | versioned JSON schemas (config, result, manifest) and a strict subset validator |
| `provenance.py` | hashes, git revision, versions, platform, peak memory, protocol-freeze gate |
| `runner.py` | config to summaries, contrasts and verification checks |
| `serialize.py` | validated result export, raw arrays, run manifest |
| `report.py` | CSV and Markdown tables, SVG figures, report.md and report.pdf |
| `cli.py` | `smoke`, `run`, `report`, `test` |
