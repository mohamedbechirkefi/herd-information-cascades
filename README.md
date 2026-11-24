<!-- SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0 -->
# HERD: when does social information help, and when does it produce cascades of errors?

**Status: M1 gate passed, 2026-11-24.** The engine, tests and tooling exist. The owner approved the amendments and the protocol is frozen (v1.0, `research/freeze.json`); the confirmatory experiments have not been run. Only exploratory verification and timing runs have been made; there are no findings.

## Question

When does social information improve decisions, and when does it generate cascades of errors? HERD studies this in a simulated sequential decision task: a binary hidden state, private noisy signals and publicly observed choices. It compares agents who decide independently, Bayesian social learners and naive imitators, while varying signal quality, the observation network and action visibility.

## Why it matters

Groups often act on what others did before them. Classic models show that this can lock a group into the wrong choice. A reproducible map of when social information helps or harms, under clearly stated assumptions, is useful for teaching and for designing further studies. All agents are synthetic: the results do not establish anything about real human behaviour.

## What is implemented

The simulation engine (`src/herd/`): the independent baseline, exact Bayesian social learning on complete and window-k networks, naive imitation, metrics, a seeded runner with versioned JSON results and run manifests, a report generator, and a command line. A pytest suite checks it against hand-computed examples, an exact rational enumeration oracle and an analytic cascade formula. Exploratory runs (EXP-001) are in `results/exploratory/`; they are planning measurements, not findings. See `roadmap.md`.

## Research navigation

| Item | Location | Status |
|---|---|---|
| Study protocol | `research/protocol.md` | FROZEN v1.0 (owner-approved 2026-11-24) |
| Feasibility audit | `research/feasibility.md` | done (M0) |
| Literature review | `research/literature_review.md` | initial, non-systematic |
| Experiment registry | `research/experiment_registry.csv` | 3 planned |
| Manuscript | `research/paper/manuscript.md` | skeleton of headings only |
| Claims register | `research/claims_register.csv` | empty (no claims) |

| Experiment | Question | Status |
|---|---|---|
| EXP-001 | Smoke matrix and engine verification (exploratory) | exploratory runs R001 to R004 done; report pending (M3) |
| EXP-002 | Bayesian and imitation rules versus independent decisions over signal quality, network and visibility | frozen, not yet run |
| EXP-003 | Sensitivity of EXP-002 to tie-breaking and horizon | frozen, not yet run |

## Quick start (development environment)

```
/Users/bechir/research/labs/.tools/py/bin/uv sync --frozen
```

Commands (the package runs from `src/`):

```
PYTHONPATH=src uv run --frozen python -m herd.cli test
PYTHONPATH=src uv run --frozen python -m herd.cli smoke
PYTHONPATH=src uv run --frozen python -m herd.cli report --run results/exploratory/EXP-001-R001
```

`run --config experiments/EXP-002.json` runs only while the protocol files and the configuration still have the hashes in `research/freeze.json`; any changed confirmatory configuration is refused.

## Data

Synthetic data only, regenerated from seeds. No external dataset is used or redistributed. See `data/manifest.json`.

## Limitations

See `research/limitations.md`.

## Licence

HERD Source-Available Non-Commercial Research License v1.0 (`LicenseRef-HERD-NC-Research-1.0`). This is a custom licence, not an OSI-approved open-source licence. See `LICENSE` and `NOTICE.md`. Third-party dependencies keep their own licences.

## Citation

See `CITATION.cff`.
