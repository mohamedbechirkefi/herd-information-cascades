<!-- SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0 -->
# demo/: HERD interactive page (M5)

A static page built from the shared lab template (TypeScript, React and Vite, pinned versions, `package-lock.json`). It has no backend and no runtime service, loads nothing from another host, collects no visitor data and runs offline after the first load. Demo URL: to be added after the owner approves publication.

## What it shows

- **Overview** with the status label of the manuscript (v1.0, not peer-reviewed, owner's full-text review pending).
- **Published results**, read from `public/data/results.json`: a forest plot of every paired accuracy contrast with its unadjusted 95% interval (EXP-002 confirmatory; EXP-003 V1 to V3 confirmatory; EXP-004 V1 to V3 exploratory), and one panel per registered experiment (EXP-001 to EXP-004) with status, verdict under the frozen rule, estimates with intervals, report and claim ids. Contrasts that are not Holm-significant or lost significance are drawn at the same size as the others, hollow, and labelled in text.
- **Accuracy distribution** of every EXP-002 cell for the three rules, from the histograms in `results/EXP-002/EXP-002-R001/result.json`, with the wrong-cascade probability, the mean longest wrong run and (exploratory) the share of episodes below the baseline.
- **Assumptions** (labelled as assumptions or design settings), **method and limitations**, run revisions and source hashes.
- **Sandbox**: an animated decision cascade (one episode, agent by agent) and the accuracy distribution of a visitor run, with scenario, rule, q, network, visibility, tie rule, N, episodes and seed controls, plus Run, Cancel, Reset and an animation switch that defaults to off under reduced motion. It runs in a Web Worker, bounded to 2,000 episodes of at most 100 agents.

Measured results, sandbox output and assumptions are labelled differently and never mixed. The page fails closed: if `results.json` is missing or malformed, no number is shown.

## Data and fidelity

- `public/data/results.json` is written by `../scripts/export_demo_data.py` from committed results only. Every `display` and `interval_display` string appears verbatim in `research/paper/manuscript.md` or its supplementary appendix, except four documented interval texts of the C1 check; `tests/test_demo_export.py` checks this and that the committed file is a fresh export.
- The sandbox engine (`src/engine.ts`) is a port of `herd.rules`, `herd.metrics` and `herd.stats.mean_interval`. `src/engine.test.ts` compares it with the Python engine on `src/fixtures/engine_fixture.json` (48 cells covering q = 0.5, 0.55, 0.7, networks complete and window-1 to window-3, v = 1 and 0.5, own and coin ties; 16 episodes of 12 agents each), written by `../scripts/export_sandbox_fixture.py`. Tolerance: identical actions and cascade flags; metrics and paired contrasts within 1e-12. The random draws are not the research engine's (mulberry32 instead of numpy PCG64), so no sandbox seed reproduces a research episode.

## Commands

Node 22 (the version used is recorded in `progress.md`).

```
cd demo && npm ci && npm run build && npm run preview
npm test
node tools/a11y_check.mjs dist --screenshots <folder>
```

`tools/a11y_check.mjs` checks, over the Chrome DevTools Protocol, that the results render, text contrast in light and dark schemes, keyboard reach and visible focus, no horizontal scroll at 360 px, no running animation under reduced motion, no request to another origin, and that the page and the sandbox work after the network is cut.
