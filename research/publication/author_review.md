<!-- SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0 -->
# Owner review checklist. Completed by the owner only.

- [ ] Authorship and affiliation metadata approved
- [ ] Protocol freezes approved (EXP-001 to EXP-003), with hashes
- [ ] Claims and limitations reviewed
- [ ] AI assistance disclosure reviewed
- [ ] Licence and data statements reviewed
- [ ] Publication approved (repository, preprint, articles)

## Prepared for the owner (M6, 2026-11-25)

No box above was ticked by an agent at any milestone (checked at M6: 0 ticked boxes), so nothing was unticked. Only the owner ticks these boxes.

### What to read for each item

1. **Authorship and affiliation metadata.** `research/paper/manuscript.md`, "Author and affiliation metadata"; `CITATION.cff` (`authors`, `preferred-citation`); `README.md`, citation section. The author line "Mohamed Bechir Kefi" with "No affiliation" was approved on 2026-11-24 (common decision C3) and replaced on 2026-11-26 by "Mohamed Bechir Kefi, independent researcher" (decision sheet item B3, D-016); the PDFs carry the author name in their metadata.
2. **Protocol freezes (EXP-001 to EXP-003), with hashes.** `research/freeze.json`; `research/experiment_registry.csv`; `research/decision_log.md`, D-008 and D-009. EXP-002 and EXP-003 are frozen at v1.0; EXP-001 is exploratory by design and EXP-004 is exploratory and not frozen.
3. **Claims and limitations.** `research/paper/manuscript.pdf` (13 pages; sections 5 to 7), `research/claims_register.csv`, `research/limitations.md`, `research/publication/claims_audit.md`, `research/publication/review_pass_2.md`, and the four experiment reports `research/experiments/EXP-00N/report.pdf`. The wording correction D-014 and the M6 reference edits (D-015, item 3) are part of this review.
4. **AI assistance disclosure.** `research/paper/manuscript.md`, section 11; `CITATION.cff`, `message`; the identification section of each experiment report.
5. **Licence and data statements.** `LICENSE`, `NOTICE.md`, `CLA.md` (unchanged by agents); `data/manifest.json`; `research/publication/dependency_licences.md` (no flagged dependency); manuscript section 10.
6. **Publication approval.** `research/publication/release_checklist.md`, `research/publication/reproducibility_report.md`, `articles/medium.md`, `articles/linkedin.md`, `demo/README.md`.

### Open decisions for this repository

- Publication: the repository was pushed and has been public since 2026-11-25, and demo hosting on Cloudflare Workers was approved on 2026-11-26 (B2). The release, tag, DOI, preprint and article posting are not decided (B15, B18).
- The owner has not yet signed off any box of this checklist, so M6 is not done.
- The owner's full-text review of the manuscript, including the D-014 wording correction and the M6 reference qualifications (D-015), is pending.
- The repository URL and the demo URL are now filled (B1, B2, 2026-11-26).
- At the release `CITATION.cff` `version` becomes `0.1.0` and `date-released` the release day (B8, 2026-11-26); until then `0.1.0-rc1` and no `date-released`.
- The committed run-report PDFs under `results/` predate the M6 builder and have no title in their metadata; rebuilding them would change committed result folders, so whether to rebuild them was left to the owner (D-015); on 2026-11-26 the owner kept them as they are (R-HERD-1).
- Funding ("No funding was received.") and competing interests ("The author declares no competing interests.") were approved (D-012) and confirmed on 2026-11-26 (B4); the author line and affiliation were settled on 2026-11-26 (B3).

### Remaining owner placeholders (file and line)

None (updated 2026-11-26). The 11 placeholder locations listed at M6 (repository URL in `CITATION.cff`, `README.md`, `articles/linkedin.md`, `articles/medium.md`, `research/paper/manuscript.md` and the page footer in `demo/src/App.tsx`; demo URL in `README.md`, `articles/linkedin.md`, `articles/medium.md`, `demo/README.md` and the page footer) were filled with https://github.com/mohamedbechirkefi/herd-information-cascades and https://herd-information-cascades.kefimohamedbechir.workers.dev (D-016).

## Owner answers recorded (2026-11-26)

Source: owner, 2026-11-26, decision sheet (`../_shared/owner-decision-sheet-2026-11-26.md`, answers in `../_shared/owner-approvals-2026-11-26.md`, relative to the labs folder). Applied in decision D-016. No box above is ticked by an agent.

- **A1.** Out-of-date "nothing published" and "local and unpublished" sentences corrected in `README.md`, `CITATION.cff` and `release_checklist.md`; append-only records unchanged.
- **B1.** Repository URL filled; `CITATION.cff` has `repository-code`.
- **B2.** Demo URL filled; `demo/wrangler.jsonc` added (static assets from `./dist`, no Worker script); deployment is the coordinator's.
- **B3.** Author line "Mohamed Bechir Kefi, independent researcher" (manuscript: "Mohamed Bechir Kefi. Independent researcher; no institutional affiliation."; `CITATION.cff` `affiliation: "Independent researcher"`; experiment reports, README, articles, demo footer). The frozen protocols are not edited. `pyproject.toml` has no authors field.
- **B4.** Funding and competing-interest statements confirmed as printed; there was no placeholder or "to be confirmed" mark.
- **B5.** Not applicable (the AI-use statement was already approved, D-012).
- **B6, B7.** The manuscript title was already approved (D-012); `CITATION.cff` `title` now equals the manuscript title, like `preferred-citation.title`.
- **B8.** Recorded in `release_checklist.md`.
- **B9.** Home paths scrubbed from `CLAUDE.md` and `research/feasibility.md`; what remains is listed in `reproducibility_report.md`.
- **B10.** Committed PDFs stay and will be attached to the release.
- **B11.** Not applicable (no HERD figure was listed).
- **B13.** Release-note sentence on build and check tools added to `release_checklist.md`.
- **B14.** Source-level labels (full text, abstract only) accepted as stated in the manuscript.
- **R-HERD-1.** The run-report PDFs under `results/` are kept as they are (release-note sentence added).

Still open: B15 (article drafts and titles, before any posting), B16 (the owner's full-text review of the manuscript and the sign-off of this checklist), B18 (release, tag, optional DOI or preprint). No freeze is pending in this repository (EXP-002 and EXP-003 frozen; EXP-001 and EXP-004 exploratory by design).
