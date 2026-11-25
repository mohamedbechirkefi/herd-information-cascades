<!-- SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0 -->
# HERD roadmap

Target: five focused development days (planning estimate). Status values: done, in progress, planned, blocked. Nothing is marked done unless its acceptance criteria were checked.

| Milestone | Depends on | Priority | Effort | Status | Blockers |
|---|---|---|---|---|---|
| M0 Bootstrap and feasibility | none | P0 | 0.25 day | done (2026-11-24), pending the owner's review of scope and cost | none |
| M1 Research and preregistration | M0 | P0 | 0.25 day | done (2026-11-24): M1 gate passed, protocols frozen v1.0 with the owner-approved amendments A-1 to A-5 (`research/freeze.json`) | full-text checks of BHW1992, CK2004, ER2010 remain open (literature, not the freeze) |
| M2 Core implementation | M1 draft (implementation may proceed before the freeze) | P0 | 1.5 days | done (2026-11-24) for the code, tests and tooling; proposals P-1 to P-6 answered and applied at the freeze | none |
| M3 Experiments | M1 freeze, M2 | P0 | 1 day | done (2026-11-25): EXP-002 and EXP-003 frozen matrices complete, reports written | none |
| M4 Interpretation | M3 | P0 | 1 day | done (2026-11-25): confounder inspection, exploratory EXP-004, evidence audit (88 of 88 traced numbers verified), manuscript v1.0 and second review pass; gate holds | the EXP-004 standalone report was refused by the session's write tool and is handed to the coordinator to write; BHW1992, CK2004, ER2010 full texts still unread (abstract-level citations, marked) |
| M5 Interactive experience | M3 results (M4 for final labels) | P1 | 0.75 day | planned | M4 for final labels |
| M6 Release candidate | M4, M5 | P0 | 0.25 day | planned | owner approval for any publication (G-PUBLIC) |

## M0 Bootstrap and feasibility

- **Deliverables:** control files (section 2 of the master prompt), feasibility audit, source and licence audit, budget, scope, exclusions and fallback; section 11.1 tree initialised.
- **11.6 additions:** experiment registry, manuscript skeleton, per-experiment draft protocols; zero-cost local publication toolchain confirmed.
- **Acceptance:** the owner can understand the question, the cost (zero) and the exclusions from `README.md`, `research/feasibility.md` and `research/protocol.md`; `uv.lock` exists; local commit made.

## M1 Research and preregistration

- **Deliverables:** evidence review, formal model, baselines, protocol, fixture manifest.
- **11.6 additions:** freeze the confirmatory protocols (EXP-002, EXP-003) before execution, recording version and SHA-256 in the registry; EXP-001 remains exploratory.
- **Acceptance:** the owner has frozen the protocols; hashes recorded; full texts of the key sources checked against the model details; exploratory results visibly separated.
- **Status (2026-11-24):** M1 gate passed. The owner approved the amendments (window-2 replaces window-1; anchor and equivalence for $q > 1/2$; zero-variance contrasts outside the Holm family; Holm-adjusted p-values with unadjusted intervals; planned sample kept). Protocol v1.0 frozen; hashes in `research/freeze.json` and the registry. Full-text checks of the key sources remain open.

## M2 Core implementation

- **Deliverables:** independent baseline first, then Bayesian (`complete`, then `window-k`) and imitation rules; episode generator with `SeedSequence` streams; metrics; experiment runner; CLI (`smoke`, `run`, `report`, `test`).
- **11.6 additions:** versioned JSON result schema with validation, run manifests (runtime, peak memory, OS, CPU, package versions, git revision, config), report generators, all built alongside the core.
- **Acceptance:** unit tests for likelihood calculations, the zero-information case and the independent baseline; analytic cascade anchor; exact enumeration reference for small $N$; complete-network equivalence test; invalid-input tests; all run with actual counts recorded.
- **Status (2026-11-24):** met. 259 tests pass (`progress.md`, M2 entry), including exhaustive differential tests against the exact rational oracle for `complete`, `window-1`, `window-2` and `window-3`, both tie rules and four visibility patterns; the analytic anchor holds as an exact rational identity for $N = 1..8$; CLI, schemas, manifests and the report generator work end to end on four exploratory runs (EXP-001-R001 to R004, all checks passed). Findings for the owner: `window-1` is degenerate (P-1) and the complete-network equivalence needs $q > 1/2$ (P-2), see `research/amendment_proposals.md`. The 11.3 report for EXP-001 is deferred to M3.

## M3 Experiments

- **Deliverables:** EXP-001 smoke and verification; EXP-002 and EXP-003 under the frozen protocols; raw machine-readable results, plots and uncertainty.
- **11.6 additions:** individual reports generated as each experiment finishes; failed runs and deviations recorded; provenance captured at run time.
- **Acceptance:** complete planned matrix or documented failure; no silently dropped runs.
- **Status (2026-11-25):** met. Smoke run EXP-001-R005 on exploratory seeds (25/25 checks); EXP-002-R001 (48/48 contrasts, 61/61 checks, 0 failed cells) and EXP-003-R001 (72/72 contrasts, 89/89 checks, 0 failed cells) ran once each with the frozen configs at revision `50fbdb1`; no run failed or was dropped. 11.3 reports: `research/experiments/EXP-00N/report.md` (N = 1, 2, 3). Raw results and SHA-256 manifests committed. Post-run reporting-layer additions recorded in D-010.

## M4 Interpretation

- **Deliverables:** confounder inspection, sensitivity analysis (EXP-003), expected versus observed, claims register, limitations.
- **11.6 additions:** finish experiment reports and evidence audit; synthesise the manuscript, including contradictory results and the sensitivity analysis; second review pass that challenges the preferred hypothesis.
- **Acceptance:** each numerical claim maps to result ID, config and figure; each external claim to a verified source; unsupported claims removed or qualified.
- **Status (2026-11-25):** met. Every manuscript prose number has a row in `research/publication/number_trace.csv` (result path, run, metric, config and protocol hash, revision) verified by `python -m herd.audit`; every claim CLM-001 to CLM-015 maps to a result ID, config hash, table or figure and manuscript section; every external claim maps to a source opened at abstract or metadata level and is marked so; unsupported phrases removed or qualified (evidence audit F-2 to F-8). Exploratory EXP-004 closes limitations 9 to 11 descriptively without changing a frozen verdict. Pending outside the gate: `research/experiments/EXP-004/report.md`, handed to the coordinator.

## M5 Interactive experience

- **Deliverables:** static page with an animated decision cascade and the accuracy distribution; playground with reset, seed and scenario controls; published results separated from sandbox runs.
- **11.6 additions:** demo, paper, reports and articles use identical verified results, labels and scope.
- **Acceptance:** offline after initial load, responsive, keyboard usable, reduced-motion option, no fabricated data, no runtime service.

## M6 Release candidate

- **Deliverables:** clean clone, locked install, tests, smoke reproduction, demo build, manifest and link checks, secret and licence scan, publication drafts.
- **11.6 additions:** compile and visually inspect manuscript and report PDFs (pandoc to Typst); verify references, cross-links, equations and figures; owner review checklist.
- **Acceptance:** actual command outputs recorded; verified facts only; the owner approves any publication. Nothing is pushed or published without approval.

## Cut order if the five-day target is threatened

EXP-003 horizon variation, then the `window-3` network, then demo polish. Controls, the tie-rule sensitivity and scientific reporting are never cut.
