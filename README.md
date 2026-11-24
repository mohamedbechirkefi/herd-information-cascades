<!-- SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0 -->
# HERD: when does social information help, and when does it produce cascades of errors?

**Status: M0 (bootstrap and feasibility), 2026-11-24.** No experiment has been run. There are no findings. The study protocol is a draft awaiting the owner's freeze.

## Question

When does social information improve decisions, and when does it generate cascades of errors? HERD studies this in a simulated sequential decision task: a binary hidden state, private noisy signals and publicly observed choices. It compares agents who decide independently, Bayesian social learners and naive imitators, while varying signal quality, the observation network and action visibility.

## Why it matters

Groups often act on what others did before them. Classic models show that this can lock a group into the wrong choice. A reproducible map of when social information helps or harms, under clearly stated assumptions, is useful for teaching and for designing further studies. All agents are synthetic: the results do not establish anything about real human behaviour.

## What is implemented

Nothing yet beyond the control files, the draft protocol and the dependency lockfile. See `roadmap.md`.

## Research navigation

| Item | Location | Status |
|---|---|---|
| Study protocol | `research/protocol.md` | DRAFT v0.1, not frozen |
| Feasibility audit | `research/feasibility.md` | done (M0) |
| Literature review | `research/literature_review.md` | initial, non-systematic |
| Experiment registry | `research/experiment_registry.csv` | 3 planned |
| Manuscript | `research/paper/manuscript.md` | skeleton of headings only |
| Claims register | `research/claims_register.csv` | empty (no claims) |

| Experiment | Question | Status |
|---|---|---|
| EXP-001 | Smoke matrix and engine verification (exploratory) | planned, protocol draft |
| EXP-002 | Bayesian and imitation rules versus independent decisions over signal quality, network and visibility | planned, protocol draft |
| EXP-003 | Sensitivity of EXP-002 to tie-breaking and horizon | planned, protocol draft |

## Quick start (development environment)

```
/Users/bechir/research/labs/.tools/py/bin/uv sync --frozen
```

Experiment commands will be added in M2.

## Data

Synthetic data only, regenerated from seeds. No external dataset is used or redistributed. See `data/manifest.json`.

## Limitations

See `research/limitations.md`.

## Licence

HERD Source-Available Non-Commercial Research License v1.0 (`LicenseRef-HERD-NC-Research-1.0`). This is a custom licence, not an OSI-approved open-source licence. See `LICENSE` and `NOTICE.md`. Third-party dependencies keep their own licences.

## Citation

See `CITATION.cff`.
