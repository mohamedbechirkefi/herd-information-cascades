<!-- SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0 -->
# HERD: when does social information help, and when does it produce cascades of errors?

**Status (2026-11-25): independent research manuscript / preprint draft, not peer-reviewed.** Milestones M0 to M4 are done and M5 (interactive page) is in this repository. The confirmatory experiments EXP-002 and EXP-003 ran once each under protocols frozen with the owner's approval on 2026-11-24; EXP-001 and EXP-004 are exploratory. The owner approved the manuscript title and its funding, competing-interest and AI-use statements on 2026-11-25; the owner's full-text review of the manuscript is pending (M6). Nothing has been published. Simulation with synthetic agents only.

## Question

When does social information improve binary decisions, and when does it generate cascades of errors? HERD studies this in a simulated sequential decision task: a binary hidden state, private noisy signals of precision $q$ and publicly observed choices. It compares agents who decide independently, exact Bayesian social learners and naive vote-counting imitators, while varying signal precision, the observation network (complete history, last two or last three predecessors) and action visibility.

## Why it matters

Groups often act on what others did before them. Classic models show that this can lock a group into the wrong choice. A reproducible map of when social information helps or harms, under clearly stated assumptions, is useful for teaching and for designing further studies. All agents are synthetic: the results establish nothing about real human behaviour.

## Key findings (within the model)

From `research/paper/manuscript.md` v1.0, *Higher average accuracy, frequent locked-in errors: a simulation study of Bayesian and naive social learning*. Differences are on the proportion scale (0.01 is one accuracy point), with unadjusted 95% intervals.

- **Confirmatory (EXP-002).** All 48 paired contrasts against the independent baseline were positive and Holm-significant, from +0.0059 [0.0048, 0.0070] to +0.1439 [0.1375, 0.1504]; 46 exceeded the protocol's practical threshold of 0.01. The pre-stated expectation that naive imitation would lower accuracy in some restricted network at low precision was **contradicted**.
- **Cascades of errors.** The same rules produced wrong cascades in up to 0.868 of episodes (imitation, $q = 0.55$, window-3, $v = 0.5$).
- **Confirmatory sensitivity (EXP-003).** No sign reversed under coin-flip ties or horizons of 10 and 200 agents, but coin ties shrank every gain (to 0.0036 to 0.0494) and two contrasts lost significance ($q = 0.55$, window-3, $v = 1$: Bayesian 0.0082 [-0.0013, 0.0176], imitation 0.0079 [-0.0015, 0.0174]); by the frozen rule these two conclusions are convention-dependent.
- **Exploratory (EXP-004, post hoc).** The social group ends below the independent baseline on the same episode in a share of episodes between 0.050 and 0.425. This does not change any frozen verdict.

A positive mean gain over many groups does not mean that any given group gains. Limitations: `research/limitations.md`.

## Interactive page (M5)

![The HERD sandbox after a run: the first episode shown agent by agent, where the first two private signals were wrong and every later Bayesian agent followed them into a wrong cascade, above the accuracy distributions of the sandbox run. The page labels it as sandbox output, not a research result.](docs/demo.png)

*Screenshot of the sandbox section (seed 1, default settings). Sandbox output is produced in the browser and is not a research result.*

`demo/` is a static page (TypeScript, React, Vite; no runtime service) with the published results drawn from `demo/public/data/results.json`, which `scripts/export_demo_data.py` writes from committed results only: a forest plot of every contrast with its interval for EXP-002, EXP-003 and EXP-004, the episode-accuracy distribution of every EXP-002 cell, the assumptions, method and limitations, and a sandbox. The sandbox runs a TypeScript port of the decision rules, tested against the Python engine on a fixture (identical actions and cascade flags), with its own random generator. The page runs offline after the first load and collects nothing. Demo URL: to be added after the owner approves publication.

```
cd demo && npm ci && npm run build && npm run preview
```

## What is implemented

The simulation engine (`src/herd/`): the independent baseline, exact Bayesian social learning on complete and window-k networks, naive imitation, metrics, a seeded runner with versioned JSON results and run manifests, a report generator, an evidence audit and a command line. A pytest suite checks it against hand-computed examples, an exact rational enumeration oracle and an analytic cascade formula.

## Research navigation

| Item | Location | Status |
|---|---|---|
| Manuscript | `research/paper/manuscript.md`, `research/paper/supplementary.md` | v1.0 (M4); title and statements owner-approved 2026-11-25; full-text owner review pending; no PDF yet (M6) |
| Study protocol | `research/protocol.md` | frozen v1.0 (owner-approved 2026-11-24) |
| Experiment registry | `research/experiment_registry.csv` | 4 experiments |
| Claims register | `research/claims_register.csv` | CLM-001 to CLM-015 |
| Evidence audit | `research/publication/evidence_audit.md`, `number_trace.csv`, `artifact_manifest.json` | 88 of 88 traced numbers verified |
| Limitations | `research/limitations.md` | 15 items |
| Owner review checklist | `research/publication/author_review.md` | open (owner only) |

| Experiment | Question | Type | Status | Report |
|---|---|---|---|---|
| EXP-001 | Smoke matrix and engine verification | exploratory | complete; all checks passed in 5 runs | `research/experiments/EXP-001/report.md` |
| EXP-002 | Bayesian and imitation rules versus independent decisions over signal precision, network and visibility | confirmatory | complete; H1 supported, imitation expectation contradicted | `research/experiments/EXP-002/report.md` |
| EXP-003 | Sensitivity of EXP-002 to tie-breaking and horizon | confirmatory | complete; 70 of 72 robust, 2 convention-dependent | `research/experiments/EXP-003/report.md` |
| EXP-004 | Post-hoc sensitivity and distributional checks | exploratory, post hoc | complete | `research/experiments/EXP-004/report.md` |

## Quick start

```
/Users/bechir/research/labs/.tools/py/bin/uv sync --frozen --all-groups
.venv/bin/python -m pytest -q
PYTHONPATH=src .venv/bin/python -m herd.cli smoke
```

## Full reproduction

```
PYTHONPATH=src .venv/bin/python -m herd.cli run --config experiments/EXP-002.json
PYTHONPATH=src .venv/bin/python -m herd.cli run --config experiments/EXP-003.json
PYTHONPATH=src .venv/bin/python -m herd.cli run --config experiments/EXP-004-R001.json
PYTHONPATH=src .venv/bin/python -m herd.cli report --run <run folder>
PYTHONPATH=src .venv/bin/python -m herd.paper check
PYTHONPATH=src .venv/bin/python -m herd.audit
.venv/bin/python scripts/export_demo_data.py --check
```

`run` refuses a confirmatory configuration whose protocol or configuration no longer has the hashes in `research/freeze.json`. More commands: `CONTRIBUTING.md`.

## Architecture

Model and episode generation (`model.py`, `generate.py`), decision rules (`rules.py`), metrics and statistics (`metrics.py`, `stats.py`), runner and serialisation (`runner.py`, `serialize.py`, `schema.py`), reports and evidence pipeline (`report.py`, `tables.py`, `paper.py`, `audit.py`, `manifest.py`), exact oracle (`reference.py`). The demo reads only the exported JSON file and fails closed if it is malformed.

## Data

Synthetic data only, regenerated from seeds. No external dataset is used or redistributed. See `data/manifest.json`.

## Licence

HERD Source-Available Non-Commercial Research License v1.0 (`LicenseRef-HERD-NC-Research-1.0`). This is a custom licence, not an OSI-approved open-source licence. See `LICENSE` and `NOTICE.md`. Third-party dependencies keep their own licences.

## Citation

Mohamed Bechir Kefi. *Higher average accuracy, frequent locked-in errors: a simulation study of Bayesian and naive social learning.* Independent research manuscript / preprint draft, not peer-reviewed, 2026. Repository URL: to be added after the owner approves publication. See `CITATION.cff`. An AI system was used as a research and development assistant and is not an author.
