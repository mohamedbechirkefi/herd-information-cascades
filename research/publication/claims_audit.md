<!-- SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0 -->
# Claims audit (M4, 2026-11-25)

Done by the AI assistant as part of the evidence audit; details in `research/publication/evidence_audit.md`. The owner reviews it before any publication.

For every row of `research/claims_register.csv` (CLM-001 to CLM-015):

- [x] Numerical claim maps to experiment ID, run IDs, metric, result path, generator script, config hash and code revision (columns `result_id`, `config_sha256`, `figure_or_table`, `manuscript_section`, `trace_ids`; trace rows in `research/publication/number_trace.csv`; artifacts in `artifact_manifest.json`)
- [x] Number re-derived from raw outputs; denominators, units, precision and sample counts checked (`python -m herd.audit`: 88 of 88 trace rows verified; findings F-1 to F-8)
- [x] External claim maps to a source actually opened, with URL or DOI and access date; abstract-only and metadata-only sources marked (evidence audit section 3)
- [x] Scope stated; no generalisation from synthetic agents to human behaviour
- [x] Second review pass that challenges the preferred hypothesis recorded (`research/publication/review_pass_2.md`)

Exploratory claims (CLM-009 to CLM-013, CLM-015) are labelled exploratory in the register, the manuscript and the EXP-004 report.
