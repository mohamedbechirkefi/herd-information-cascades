<!-- SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0 -->
# Release checklist (M6). Nothing is checked at M0.

**Status (2026-11-25, M6):** release candidate prepared (`CITATION.cff` version `0.1.0-rc1`), awaiting the owner's review and G-PUBLIC. Items 1 to 11 were verified in the M6 session; items 12 and 13 belong to the owner. Evidence: `reproducibility_report.md`, `progress.md` (M6 entry), decision D-015.

**Update (2026-11-26):** the repository has been public at https://github.com/mohamedbechirkefi/herd-information-cascades since 2026-11-25 (pushed by the coordinator on the owner's word), so everything committed in it is public. No release, tag, DOI or preprint exists. The owner's answers of 2026-11-26 (owner, 2026-11-26, decision sheet) were applied in decision D-016. The interactive page is to be hosted at https://herd-information-cascades.kefimohamedbechir.workers.dev (Cloudflare Workers static assets, free plan, deployed by the coordinator). Item 13 below is about the release (B18), which the owner has not yet decided.

- [x] Clean clone into a separate directory. Evidence: two local clones of HEAD (`4cd8c92`, then `802145d`) in the session scratch folder, deleted afterwards.
- [x] `uv sync --frozen` succeeds from `uv.lock`. Evidence: `uv sync --frozen --all-groups --all-extras`, `Installed 6 packages` (clone 2).
- [x] Test suite run; actual counts and output recorded in `progress.md`. Evidence: `299 passed` in clone 2 and in the working repository; demo `Tests 69 passed (69)`.
- [x] Smoke reproduction (EXP-001) matches recorded results within tolerance. Evidence: EXP-001-R005 identical apart from run times, raw arrays byte-identical; EXP-001-R001 identical in every metric, with the post-A-3 Holm fields explained (D-015, item 7).
- [x] Demo builds and works offline after initial load. Evidence: `npm run build` `✓ built`; `node tools/a11y_check.mjs dist`, `A11Y-CHECK PASS` including "offline after first load" (both clones and the working repository).
- [x] `data/manifest.json` and every result manifest verified. Evidence: SHA256SUMS 21 of 21 OK; 16 run-manifest outputs; artifact manifest 79 paths, 16 file hashes, 8 canonical configuration hashes, 0 failures.
- [x] All links and cross-references checked. Evidence: `scripts/check_links.py`, 21 relative links in 49 Markdown files, 0 broken (test `tests/test_links.py`); 370 back-quoted path mentions surveyed, the 20 that do not resolve are patterns (`EXP-NNN`, `R00N`), journal context or external hosts; 9 of 9 references cited and resolved; public-number test `tests/test_public_numbers.py` passes.
- [x] Secret, personal-identifier and licence scan clean. Evidence: 215 tracked and new files scanned; 0 e-mail addresses (apart from the commit-trailer address quoted in `CLAUDE.md` section 4), 0 tokens or keys, 0 private-key headers, 0 `.env` files; home-directory paths removed from 4 current files, 12 lines left in `CLAUDE.md` (6), `research/feasibility.md` (4) and `progress.md` (2) (tool locations; records not rewritten, D-015 item 5); `dependency_licences.md`: 6 Python and 53 npm packages, no flag; SPDX header on every new file whose format allows it.
- [x] Manuscript and report PDFs compiled and visually inspected. Evidence: `scripts/build_pdfs.py`; manuscript 13 pages, supplementary 19, EXP-001 3, EXP-002 13, EXP-003 20, EXP-004 5; every manuscript page and the first page of each report inspected (the reports and supplementary embed no figures), plus table pages; two table fixes; metadata title set, no e-mail address or local path; each PDF under 1 MB.
- [x] Every registered experiment has a truthful standalone report. Evidence: `research/experiments/EXP-001` to `EXP-004/report.md` and `.pdf`, labelled exploratory or confirmatory as registered.
- [x] Claims audit complete (`claims_audit.md`). Evidence: present since M4; `herd.audit` 88 of 88 trace rows verified, 0 untraced prose numbers (M6).
- [ ] Owner review complete (`author_review.md`)
- [ ] Owner approval for any publication (G-PUBLIC)

## Version and date at the release (owner decision sheet item B8, 2026-11-26)

`CITATION.cff` keeps `version: 0.1.0-rc1` and no `date-released` until the release. At the release, `version` becomes `0.1.0` and `date-released` is set to the release day. `pyproject.toml` stays at `0.0.0` (changing it would change the lockfile and the recorded environments).

## Release notes (draft)

- External build and check tools are used but not redistributed: pandoc (GPL-2.0-or-later) converts Markdown to Typst and LaTeX, Google Chrome runs the accessibility check of the demo, and lightningcss (MPL-2.0) is a build-time CSS tool of Vite that is not shipped in the page bundle (see `dependency_licences.md`).
- The eight run-report PDFs under `results/` predate the M6 PDF builder and carry no title in their metadata; they are kept unchanged as parts of committed result folders (owner decision sheet item R-HERD-1, kept).
