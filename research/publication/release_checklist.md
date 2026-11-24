<!-- SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0 -->
# Release checklist (M6). Nothing is checked at M0.

- [ ] Clean clone into a separate directory
- [ ] `uv sync --frozen` succeeds from `uv.lock`
- [ ] Test suite run; actual counts and output recorded in `progress.md`
- [ ] Smoke reproduction (EXP-001) matches recorded results within tolerance
- [ ] Demo builds and works offline after initial load
- [ ] `data/manifest.json` and every result manifest verified
- [ ] All links and cross-references checked
- [ ] Secret, personal-identifier and licence scan clean
- [ ] Manuscript and report PDFs compiled and visually inspected
- [ ] Every registered experiment has a truthful standalone report
- [ ] Claims audit complete (`claims_audit.md`)
- [ ] Owner review complete (`author_review.md`)
- [ ] Owner approval for any publication (G-PUBLIC)
