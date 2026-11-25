<!-- SPDX-License-Identifier: LicenseRef-HERD-NC-Research-1.0 -->
# Second review pass: arguing against the preferred hypothesis (M4)

- **Date:** 2026-11-25. **Reviewed:** `research/paper/manuscript.md` draft v0.9 and the experiment reports EXP-001 to EXP-004.
- **Reviewer:** the AI assistant, in an adversarial pass separate from drafting. This is internal quality control, not peer review; the owner reviews the outcome.
- **Preferred hypothesis under attack:** "within this model, social information raises mean decision accuracy against independent decisions, robustly to tie rule and horizon, while producing frequent wrong cascades."
- **Method:** for each challenge, state the strongest version, check it against the committed results (no new computation beyond EXP-004), and decide whether it holds. Where it holds, the manuscript was changed; the changes are listed in the last section.

## 1. Strongest alternative readings

### C-1. The gain is mostly a product of the own-signal tie convention

- **Challenge.** The headline magnitudes (up to +0.1439) come from one arbitrary convention. Under coin-flip ties the gains fall to between 0.18 and 0.81 of their EXP-002 values in the confirmatory grid (EXP-003) and between 0.27 and 0.63 at $q \in \{0.60, 0.80\}$ (EXP-004, exploratory); below half in 16 of 24 and 17 of 24 contrasts. Reporting own-tie magnitudes in the abstract overstates the effect under an equally standard convention.
- **Check.** `results/EXP-003/EXP-003-R001/tables/robustness_vs_EXP-002-R001.csv`, `results/exploratory/EXP-004-R001/tables/robustness_vs_EXP-002-R001.csv`; V1 ranges 0.0036 to 0.0494 (EXP-003) and 0.0083 to 0.0600 (EXP-004).
- **Verdict: holds for magnitudes, not for signs.** No sign reversed in 144 comparisons (72 confirmatory, 72 exploratory). The manuscript draft gave coin-tie magnitudes only in Section 5.3.
- **Change:** the abstract and the conclusion now state the coin-tie range next to the own-tie range, and say that magnitudes are convention-specific.

### C-2. "Social information improves decisions" is false for a large share of groups

- **Challenge.** At $q = 0.55$ the social group ends below the independent baseline in 0.371 to 0.425 of episodes (EXP-004, exploratory). A reader who sees "raises accuracy in all 24 cells" will understand that groups gain; four in ten do not. The working title "How groups can become confidently wrong" points the opposite way from the primary result, which is also a misreading risk.
- **Check.** `results/exploratory/EXP-004-derived/q2_distribution.csv`; with $v = 1$ the share equals the wrong-cascade probability (Table 3).
- **Verdict: holds as a framing problem.** The primary result is about means; the draft said so in Section 6 but not in the title or abstract.
- **Change:** the title is revised (the master prompt asks for a revision after results) to name both findings; the abstract's conclusion says "on average" and gives the share below baseline as exploratory.

### C-3. Some significant effects are practically negligible

- **Challenge.** The protocol (section 5) names 0.01 as "the smallest effect treated as practically meaningful". Two EXP-002 contrasts are below it: imitation +0.0059 and Bayesian +0.0091 at $q = 0.55$, window-2, $v = 0.5$. Under coin ties, 5 of the 48 V1 contrasts (EXP-003 and EXP-004 together) are below 0.01. Holm significance at $n = 10{,}000$ does not make them meaningful.
- **Check.** `results/EXP-002/EXP-002-R001/result.json` (sorted contrast means 0.0059, 0.0091, 0.0131, ...); the two robustness CSVs.
- **Verdict: holds.** The draft did not use the protocol's own threshold.
- **Change:** Section 5.2 and Table 6 now say that 46 of 48 contrasts exceed the protocol's 0.01 threshold and 2 do not; the Discussion qualifies "in every cell" accordingly.

### C-4. The contradicted imitation expectation is a strawman result

- **Challenge.** The naive rule is weak by construction: it is action-equivalent to Bayes under `complete`, and in window networks it counts at most three actions. Its failure to harm says little about naive inference. Claiming a contradiction of the naive-herding literature would overgeneralise.
- **Check.** C4 (0 differing episodes in all `complete` cells); Table 4 (window-2, $v = 1$: identical on every episode; elsewhere differences of at most 0.0178).
- **Verdict: holds against any broader claim; the draft already limited it.** Section 6 of the draft said the result "says nothing about other naive rules or about the richer setting of Eyster and Rabin (2010)".
- **Change:** the abstract now says "this naive rule"; CLM-003 keeps its limit.

### C-5. The window-network results could be a shared implementation error

- **Challenge.** Both social rules in the window networks rest on code verified against the exact oracle only for $N \le 9$, and the analytic anchor covers only `complete`, $v = 1$. A bug that grows with $N$ would move both rules together.
- **Check.** Unit suite (oracle tests), C3 and C6 in every run; window-2, $v = 1$ identity between the rules (Table 4) is a property of the decision tables that a bug would be unlikely to preserve, but it is not a proof.
- **Verdict: cannot be excluded; already disclosed** (Sections 6 and 7). No change beyond keeping it in the abstract-level caveats of the conclusion.

### C-6. Information quantity, not structure, explains network differences

- **Challenge.** The protocol's third competing explanation. Table 5 shows the window gains ordered by expected observed actions.
- **Verdict: partly holds.** Quantity orders the window cells; the complete network does not gain more despite about 8.5 times more observed actions than window-3 at $v = 1$. Quantity and structure are confounded in this grid.
- **Change:** none needed; the draft already said the data cannot separate them. The word "structure" is avoided in the conclusion.

## 2. Overgeneralisation

- **"Wrong-cascade probabilities exceed 0.8" (draft Section 5.2).** True only for 3 of the 16 half-visibility window social arms, all at $q = 0.55$ (range over the 16: 0.248 to 0.868). Rewritten as "reach 0.868". The same loose phrase in the EXP-002 report (section 10) refers to "wrong-cascade probabilities exceed 0.8 while accuracy improves" without saying "in some cells"; it is left as written in that M3 report but the manuscript no longer repeats it.
- **"In every cell" / "all 24 cells".** Correct for the sign; qualified for practical size (C-3).
- **Exploratory extension presented beside confirmatory rows (Table 2).** The label column and caption mark EXP-004 rows as exploratory; Section 5.4 repeats that the confirmatory verdict is unchanged. Kept.
- **Claims about people.** None found. Section 8 keeps the misuse warning.

## 3. Stale figures and tables

- All manuscript tables are generated (`python -m herd.paper check`: match). Report tables in EXP-002 and EXP-003 match a fresh regeneration line by line (`python -m herd.audit`).
- Figures FIG-001 to FIG-003 were regenerated after the caption fix of D-010 from the unchanged `result.json`; `shasum -a 256 -c` of both `SHA256SUMS` files passes, so they are the committed versions.
- The draft's Section 4.2 test count (281) is the count after M3; the M4 count is given in the revision.

## 4. Leakage

- Exploratory values of the primary contrast were seen before the freeze (EXP-001-R001 to R004, disclosed as C4 in `research/freeze.json`). R001 used seeds 0 and 1 at $N = 20$ only, so no confirmatory episode was seen. This is disclosed in Section 4.4.
- EXP-004-R001 used the confirmatory seeds 0 to 9 after the confirmatory runs; it is post hoc and cannot leak into a frozen analysis. Disclosed.
- No test set exists in this design; no tuning on outcomes occurred.

## 5. Missing failed runs

The registry, the journal (J-0001 to J-0010) and the result folders list EXP-001-R001 to R005, EXP-002-R001, EXP-003-R001 and EXP-004-R001. None failed, none was dropped, none was rerun. Nothing is missing.

## 6. Changes made to the manuscript (v0.9 to v1.0)

1. Title revised from the working title to one that states both findings.
2. Abstract: coin-tie magnitude range added; "on average" and "this naive rule" added; the share-below-baseline sentence kept as exploratory.
3. Section 5.2: the protocol's 0.01 practical threshold applied (46 of 48 above it); "exceed 0.8" replaced by "reach 0.868".
4. Table 6: the H1 row notes the 2 contrasts below the practical threshold.
5. Section 6: "in every cell" qualified by practical size; a paragraph on what the result does not show (C-2).
6. Section 9: coin-tie magnitudes stated.
7. Section 4.2: M4 test count added.
8. Units: "accuracy points" is now used only for the percentage-point scale (0.01 = one point); proportion-scale values carry no unit word. The same correction was made in the EXP-002 report and in CLM-002 and CLM-009 (evidence audit finding F-2).
