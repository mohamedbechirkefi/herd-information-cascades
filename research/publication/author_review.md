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

1. **Authorship and affiliation metadata.** `research/paper/manuscript.md`, "Author and affiliation metadata"; `CITATION.cff` (`authors`, `preferred-citation`); `README.md`, citation section. The author line "Mohamed Bechir Kefi" and "No affiliation" were approved on 2026-11-24 (common decision C3); the PDFs carry the same author in their metadata.
2. **Protocol freezes (EXP-001 to EXP-003), with hashes.** `research/freeze.json`; `research/experiment_registry.csv`; `research/decision_log.md`, D-008 and D-009. EXP-002 and EXP-003 are frozen at v1.0; EXP-001 is exploratory by design and EXP-004 is exploratory and not frozen.
3. **Claims and limitations.** `research/paper/manuscript.pdf` (13 pages; sections 5 to 7), `research/claims_register.csv`, `research/limitations.md`, `research/publication/claims_audit.md`, `research/publication/review_pass_2.md`, and the four experiment reports `research/experiments/EXP-00N/report.pdf`. The wording correction D-014 and the M6 reference edits (D-015, item 3) are part of this review.
4. **AI assistance disclosure.** `research/paper/manuscript.md`, section 11; `CITATION.cff`, `message`; the identification section of each experiment report.
5. **Licence and data statements.** `LICENSE`, `NOTICE.md`, `CLA.md` (unchanged by agents); `data/manifest.json`; `research/publication/dependency_licences.md` (no flagged dependency); manuscript section 10.
6. **Publication approval.** `research/publication/release_checklist.md`, `research/publication/reproducibility_report.md`, `articles/medium.md`, `articles/linkedin.md`, `demo/README.md`.

### Open decisions for this repository

- Publication of any kind (push, GitHub repository, release, tag, preprint, articles, demo hosting) is not decided and needs the owner's approval (G-PUBLIC; owner-approvals-2026-11-25e).
- The owner has not yet signed off any box of this checklist, so M6 is not done.
- The owner's full-text review of the manuscript, including the D-014 wording correction and the M6 reference qualifications (D-015), is pending.
- The repository URL and the demo URL are owner-only facts that are not yet known.
- Re-adding `date-released` to `CITATION.cff` belongs to the owner's publication step (owner-approvals-2026-11-25e, coordinator default).
- The release-candidate version `0.1.0-rc1` in `CITATION.cff` was chosen by the AI assistant (D-015) and the owner may set another version at release.
- The committed run-report PDFs under `results/` predate the M6 builder and have no title in their metadata; rebuilding them would change committed result folders, so whether to rebuild them is left to the owner (D-015).
- Funding, competing interests, the author line and the affiliation were already approved by the owner (C3, D-012) and need no further decision unless the owner wishes to change them.

### Remaining owner placeholders (file and line)

| File | Line | Placeholder |
|---|---|---|
| `CITATION.cff` | 4 | Repository URL: to be added after the owner approves publication |
| `CITATION.cff` | 27 | Repository URL to be added after the owner approves publication (in `notes`) |
| `README.md` | 31 | Demo URL |
| `README.md` | 96 | Repository URL (citation) |
| `articles/linkedin.md` | 12 | Repository |
| `articles/linkedin.md` | 13 | Interactive demo |
| `articles/medium.md` | 27 | Demo link |
| `articles/medium.md` | 55 | Repository link |
| `demo/README.md` | 4 | Demo URL |
| `demo/src/App.tsx` | 52 to 53 | Repository and demo URL (page footer) |
| `research/paper/manuscript.md` | 282 | Public URL (section 10) |
