<!-- SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0 -->
# Evidence audit (M4, master prompt 11.5)

- **Date:** 2026-11-25. **Performed by:** the AI assistant; internal quality control, not peer review. The owner reviews it.
- **Scope:** `research/paper/manuscript.md` v1.0, `research/paper/supplementary.md`, the experiment reports EXP-001 to EXP-004, `research/claims_register.csv`, `research/literature_review.md`.
- **Tools (all read-only on results):** `python -m herd.audit` (number trace, coverage, report tables, generated tables), `python -m herd.paper check`, `python -m herd.manifest`, `shasum -a 256 -c results/EXP-00N/SHA256SUMS`.

## 1. Result of the automated checks

| Check | Command | Result |
|---|---|---|
| Number trace: every manuscript prose number resolved from its source and compared at printed precision | `python -m herd.audit` | 88 rows, 88 verified, 0 failed |
| Coverage: every decimal in the manuscript prose has a trace row | `python -m herd.audit` | 0 missing |
| Generated manuscript and supplementary tables match the result files | `python -m herd.paper check` | match (9 tables) |
| Report tables of EXP-002 and EXP-003 match a fresh regeneration line by line | `python -m herd.audit` | all rows present verbatim |
| Raw and result files unchanged since M3 | `shasum -a 256 -c results/EXP-002/SHA256SUMS results/EXP-003/SHA256SUMS` | all OK |
| Frozen protocol and config hashes | `pytest tests/test_freeze.py` (in the full suite) | pass |

The trace file is `research/publication/number_trace.csv` (columns: id, doc, token, relation, selector, exp_id, run_ids, metric, hashes, claim). The selector is evaluated against the committed artifact, so each row gives experiment, run, metric definition, result path, config and protocol hash and code revision. `research/publication/artifact_manifest.json` maps every run, table (TAB-001 to TAB-005, TAB-S01 to TAB-S04), figure (FIG-001 to FIG-004), the derived analyses and the trace file to its sources, generator, hashes and revision.

**Limits of the automated checks.** (a) Coverage matches tokens by value within a document, so a design constant such as 0.8 covers every printed 0.8, even when the printed 0.8 is a result statement; this is how F-3 escaped the automated check and was found by reading. (b) Integer counts are verified only where a trace row exists (the main claims: 48, 46, 2, 70, 72, 16, 17, 11, 8, 4, 61, 89); other integers were checked by reading. (c) The prose of the EXP-001 to EXP-003 reports is not covered by the trace; it was written at M3 from the same results, its tables are verified mechanically, and its prose numbers were read against the tables during this audit. A value-only matching approach was tried first and rejected: against an index of all numbers in the result files it matched 87% to 100% of random 2- to 4-decimal values, so it could not discriminate.

## 2. Denominators, units, precision, uncertainty and sample counts

- **Denominators.** Every contrast: 10,000 paired episodes (10 seeds x 1,000), checked in `result.json` (`n` = 10000 for all 192 contrasts of the three confirmatory and exploratory runs). Agent decisions: EXP-002 72 arms x 10,000 x 50 = 36,000,000; EXP-003 and EXP-004-R001 36 arms x 10,000 x (50 + 10 + 200) = 93,600,000. Shares in Table 3 have denominator 10,000 episodes per arm.
- **Units.** Finding F-2 below.
- **Precision.** Contrasts and intervals at 4 decimals, proportions of episodes at 3, longest runs at 2, p-values at 2 significant digits. Values are rounded, not truncated (verified by the trace's half-unit tolerance).
- **Uncertainty.** Intervals are unadjusted normal 95% intervals; the normal and bootstrap bounds differ by at most 0.0006 (lower bounds, 0.00055) and 0.0005 (upper bounds, 0.00049) in EXP-002, consistent with the "at most 0.0006" of the EXP-002 report. EXP-004 intervals are labelled unadjusted and exploratory. No simultaneous interval is claimed anywhere.
- **Sample counts.** Holm families: EXP-002 m = 48; each EXP-003 and EXP-004-R001 variation m = 24; no degenerate contrast anywhere.

## 3. External claims

| Source | Level verified | Used for | Finding |
|---|---|---|---|
| BHW1992 | metadata and abstract (RePEc, 2026-11-24); title checked against the Crossref record (`api.crossref.org/works/10.1086/261849`, 2026-11-25) | definition of an informational cascade; the complete-network setting | The title ends "as Informational Cascades" (Crossref), resolving the M0 doubt. The statement that coin-flip tie-breaking is "the convention of BHW1992" (study protocol section 8, EXP-003 protocol and report) is a model detail beyond the abstract and is **unverified**; the full text was not accessible (publisher HTTP 403). The manuscript does not attribute the convention; the EXP-003 report now flags it. The frozen protocols are not edited. |
| Banerjee1992 | metadata and abstract | herding definition | none |
| ER2010 | metadata and abstract | naive inference idea | Manuscript states the imitation rule is a simplified operationalisation, not a replication, and that the results neither confirm nor contradict ER2010. |
| ADLO2011 | metadata and abstract | network learning context | none |
| CK2004 | bibliographic metadata only; content from a search snippet | single-predecessor setting | Marked "metadata only, content unverified" in the manuscript and now in the EXP-002 report (finding F-4). |
| SS2000 | metadata and abstract; DOI only from a search snippet | confounded learning excluded | The manuscript cites the RePEc URL, not the unverified DOI. |
| GJ2010, AH1997, W2008wp | metadata and abstract | related work, human-subject context | W2008wp cited as a working paper; its published version is unverified and not cited. |

No full text was read for any source. Every reference in the manuscript is labelled accordingly.

## 4. Findings and fixes

| ID | Finding | Where | Fix |
|---|---|---|---|
| F-1 | The automated value-only check proposed first could not discriminate (see section 1); replaced by the selector-based trace. | `src/herd/audit.py` | Rewritten before use; tests in `tests/test_audit.py` show that a token off by one unit in the last digit fails. |
| F-2 | Unit inconsistency: "accuracy points" was used both for proportion-scale differences ("+0.0059 accuracy points") and for the percentage-point scale ("between 0.6 and 14.4 accuracy points", "one accuracy point" = 0.01 in the protocol). | EXP-002 report sections 2 and 9; CLM-002; CLM-009; manuscript draft abstract and Table 1 caption | Proportion-scale values now carry no unit word, and "accuracy point" means 0.01 throughout. EXP-002 report edited (dated note); claims register and manuscript corrected. |
| F-3 | Overgeneralisation: "wrong-cascade probabilities exceed 0.8" under partial visibility holds for 3 of 16 half-visibility window social arms only. | manuscript draft Section 5.2 | Rewritten ("are high ... reach 0.868 at q = 0.55"). The M3 EXP-002 report (section 10) keeps its phrase, which is about the cells where it holds. |
| F-4 | Unsourced or over-stated external claims: "a known theme of the cascade literature" with no verified source; CK2004 content cited from a snippet. | EXP-002 report sections 3 and 9 | Phrase removed with a dated note; CK2004 marked metadata only. |
| F-5 | BHW1992 tie convention unverified (see section 3). | protocols (frozen), EXP-003 report section 3 | Flagged in the EXP-003 report; recorded as a limitation; frozen protocols unchanged. |
| F-6 | Practical size not applied: two Holm-significant contrasts are below the protocol's own 0.01 threshold. | manuscript draft | Stated in Section 5.2, Table 6 and Section 6 (from the second review pass). |
| F-7 | Stale counts: the draft's test count (281) predates M4. | manuscript Section 4.2 | Updated to 289. |
| F-8 | Manifest field: `protocol_sha256` of EXP-001 runs R001 to R004 is the hash of the current (amended, pre-freeze) EXP-001 protocol, not of the draft in force when they ran. | `artifact_manifest.json` | Disclosed here; the pre-amendment text is in git history before `c507f05`. |

No number in the manuscript or the reports was found to differ from its source. No failed, dropped or hidden run was found.

## 5. Confounder inspection (task 1 of the M4 brief)

Competing explanations named in the study protocol (section 9) and the EXP-002 protocol (section 3), against each confirmatory conclusion.

| Conclusion | Competing explanation | Addressed by | Status |
|---|---|---|---|
| EXP-002: social rules raise mean accuracy (CLM-001) | Averaging over agents mixes early and late behaviour | Last-agent accuracy (secondary metric; EXP-004 paired last-agent difference positive in 48 of 48 with intervals excluding zero); horizons N = 10 and 200 (EXP-003, and EXP-004-R001 exploratory) keep every sign | Addressed for the sign; magnitude depends on N |
| same | Tie convention | EXP-003 V1 (confirmatory): no reversal, 2 lost significance; EXP-004-R001 V1 (exploratory): 24 of 24 robust | Addressed for the sign; magnitude strongly convention-dependent |
| same | Implementation error | Analytic anchor C1, zero-information C2, baseline C3, equivalence C4, schema C5, near ties C6 in every run; exact rational oracle (N up to 9) | Addressed within verification coverage; window code at N over 9 not independently verified |
| EXP-002: network and visibility differences in the gain | Information quantity rather than structure | Visibility varies quantity within each network (EXP-002); EXP-004 Q4 tabulates gains against expected observed actions | Partly: quantity orders the window cells, but the complete network does not gain more than window-3 at v = 1; quantity and structure are confounded in this grid and cannot be separated |
| EXP-002: imitation expectation contradicted (CLM-003) | The rule is too weak to show naive harm | C4 (equivalence under complete) and EXP-004 Q3 (small differences, window-2 at v = 1 identical) | Holds as an explanation; the claim is limited to this rule |
| EXP-003: 70 of 72 robust; 2 convention-dependent (CLM-005, CLM-006) | Monte Carlo error near the threshold | Per-seed signs (V1: 13 of 24 contrasts positive in all 10 seeds); intervals | The two lost contrasts have intervals including effects up to about 1.8 points; loss of significance is not evidence of zero |

New computation for this inspection was limited to EXP-004 (exploratory, journaled J-0009 and J-0010, outputs under `results/exploratory/`, one worker). It changes no frozen verdict.

## 6. Strength and scope of evidence per conclusion

| Claim | Strength | Scope |
|---|---|---|
| CLM-001, CLM-002 | Confirmatory, frozen protocol, Holm-controlled, 10,000 paired episodes per contrast | Model only; own-signal ties; N = 50; the grid of EXP-002 |
| CLM-003 | Confirmatory test of a pre-stated expectation | One naive rule |
| CLM-004 | Exact (0 differing episodes) | Complete network, own ties, q over 1/2 |
| CLM-005 to CLM-007 | Confirmatory sensitivity | q in {0.55, 0.70} |
| CLM-008 | Descriptive secondary metric | EXP-002 grid |
| CLM-014 | Confirmatory estimates judged against the protocol's stated practical threshold | EXP-002 grid |
| CLM-009 to CLM-013, CLM-015 | Exploratory, post hoc, unadjusted | As stated in each row |
