<!-- SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0 -->
# HERD: session rules

HERD studies when social information improves binary decisions and when it produces cascades of errors, using simulated agents only. `master_prompt.md` is the authority for this repository. It is never edited.

## 1. Reading order at every session start

Before modifying anything, read in this order:

1. `master_prompt.md` (authority; sections 2, 3, 10 and 11 in particular)
2. `roadmap.md` (milestones, status, blockers)
3. `progress.md` (append-only journal; read the latest entry first)
4. `research/protocol.md` (current protocol status: DRAFT until the owner freezes it)
5. `research/claims_register.csv` (every claim and its evidence)

Then run `git status`, inspect existing files, and never overwrite changes made by the owner. State the current milestone and the next bounded task before working.

## 2. Mandatory requirements (master prompt section 11)

- Maintain the publication tree of section 11.1: `research/experiment_registry.csv`, `research/protocol.md`, `research/claims_register.csv`, `research/paper/` (manuscript.md canonical, manuscript.tex and manuscript.pdf generated), `research/experiments/EXP-NNN/` and `research/publication/`.
- Stable identifiers: experiments `EXP-NNN`, runs `EXP-NNN-RNNN`, figures `FIG-NNN`, claims `CLM-NNN`.
- Register every experiment before confirmatory execution, with purpose, dependency, primary outcome, protocol hash, status, report location and planned analysis.
- Before each experiment, write `research/experiments/EXP-NNN/protocol.md` following section 11.2. Freeze it (version and SHA-256 hash recorded in the registry) only on the owner's approval.
- Every registered experiment gets a standalone report with the twelve sections of 11.3, including failed, null, abandoned and exploratory ones, visibly labelled.
- One integrated manuscript (11.4), 3,000 to 6,000 words where justified. Abstract drafted only after analysis.
- Evidence-to-publication pipeline (11.5): tables and figures generated once from versioned results and reused everywhere; a manifest maps each number to experiment, run, metric, result path, generator script, config hash and code revision; a second review pass challenges the preferred hypothesis.
- Milestone additions (11.6): M0/M1 registry, manuscript skeleton, per-experiment protocols, zero-cost toolchain; M2 versioned output schemas, run manifests and report generators alongside the core; M3 reports generated as experiments finish, provenance captured at run time; M4 evidence audit and manuscript synthesis with contradictory results and sensitivity analysis; M5 demo, paper, reports and articles use identical verified results; M6 compile and inspect PDFs, clean-clone reproduction, owner review checklist.
- Never fabricate a PDF, a placeholder result, a citation, a test count or a passing status.

## 3. Toolchain (zero cost, local)

- Python 3.12.1 at `/usr/local/bin/python3`; dependencies locked in `uv.lock` with `/Users/bechir/research/labs/.tools/py/bin/uv`.
- `uv`, `typst` (Python package 0.15.0), `pypdf` and `pillow` in `/Users/bechir/research/labs/.tools/py/bin/`.
- pandoc 3.6.3 at `/Users/bechir/research/labs/.tools/pandoc`.
- Node 22.23.3 at `/Users/bechir/research/helix/.tools/node/bin`: read-only use; never modify that folder.
- No TeX distribution. PDFs are built as Markdown to Typst with pandoc (pass `-V mainfont="Libertinus Serif"`; the default template leaves the font list empty), compiled with the typst Python package. `manuscript.tex` is generated from Markdown with pandoc and is not compiled locally.

## 4. Rules for all sessions

- **Gates.** Never push, add a remote, create a GitHub repository or publish anything (G-PUBLIC). No paid service of any kind. Never freeze a protocol: freezing is the owner's decision (G-FREEZE). No confirmatory experiment before the owner freezes its protocol. Exploratory runs are allowed and are labelled exploratory.
- **Scope.** Work only inside this repository, except for read-only use of the tools listed above. Do not touch any other folder under `/Users/bechir/research`. Never kill processes you did not start. Never delete anything you did not create in the current session.
- **Truthfulness.** Never fabricate results, citations, test counts or PDFs. Record commands and their actual outputs in `progress.md`. Anything not verified is labelled unverified.
- **Files and style.** New text and code files start with `SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0` as a comment where the format allows; JSON and CSV are covered by `NOTICE.md`. English. No em dashes. Plain, formal register. No e-mail address, personal identifier or secret in any committed file (git author metadata excepted). Refer to the owner as "the owner" (they/them).
- **Licence.** The licence files (`LICENSE`, `NOTICE.md`, `LICENSE_HISTORY.md`, `CLA.md`, `.github/`) are the owner's decision and are not changed. Development commands may be appended to `CONTRIBUTING.md`.
- **Commits.** Local only: `git -c user.name=<owner username> -c user.email=<owner address> commit` with the identity given in `/Users/bechir/research/labs/_shared/M0-brief.md` (the address is never written into a committed file), message ending with a blank line and `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. Run `git status` before and after.
- **Claims boundary.** Synthetic actors do not establish real human irrationality. Simulation results hold only within the model's assumptions.
- **Session end.** Update `progress.md` (dated entry with commands and real outputs), `roadmap.md` statuses and blockers, and `research/decision_log.md` for any decision.
