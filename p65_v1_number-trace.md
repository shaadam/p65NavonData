# p65 v1: number-to-source trace (rebuilt 2026-11-17 at integration)

Every number in `docs/manuscript/p65_navon_v1.md` that carries a claim, with the file it was read from. Paths are
repository-relative. The abstract and discussion block below is written by `scripts/p65_v1_number-trace.py`, which
locates each printed value in the manuscript (string count in Python), recomputes it from the results files by its
own arithmetic (cell-table expansion, coder files, codes files, the coded Arm C table, the Arm D per-source list,
the census map, exact binomial power), and compares. Its negative control `--perturb` nudges three recomputed
values and must report mismatches. The body tables that follow are kept by hand from the fold trace (F1) and
updated at integration for the Arm C row 76 ruling and the Arm D recount. A number marked DERIVED was computed at
the fold from the source values shown.

<!-- trace:generated:begin -->
## Abstract and Discussion, recomputed by `scripts/p65_v1_number-trace.py` (2026-11-17)

Status: OK = printed value matches the recomputation; READ = taken from the results line (bootstrap or simulation not rerun); LOCATED = text-only claim found; MISMATCH / NOT IN TEXT fail the run.

| region | printed | meaning | source | recomputed | method | status |
|---|---|---|---|---|---|---|
| abstract | almost fifty years | 2026 minus 1978 | Navon 1978 (title page) | 48 | subtraction; 48 is 'almost fifty' | OK |
| abstract | four arms | arms A, B, C, D | Sections 2 to 5 | 4 | count of arm sections | OK |
| abstract | two blind model coders | coders per sample | arm-a*/codes_coder1, coder2 | 2 | files per sample | OK |
| abstract | about three times as often | 0.738 / (1 − 0.738) = 2.8 | arm-a3-model/p65_a3-results_2026-11-13.txt | 2.815 | odds from the recomputed share; 2.8 reads 'about three' | OK |
| abstract | 0.74 of directional sentences | registered share, time over place | arm-a3-model/p65_a3-results_2026-11-13.txt CELL TABLE | 0.7379 | Σ TP·pop/coded ÷ Σ (TP+PT)·pop/coded over the six cells | OK |
| abstract | (95% interval 0.56 to 0.89) | document bootstrap within cells, 10,000 resamples | same file, 'DIRECTIONAL share' line: 0.561 to 0.893 | 0.561, 0.893 | READ: the bootstrap is not rerun here | READ (source line) |
| abstract | three openly licensed dictionaries | WordNet, GCIDE, Wiktionary | change-verbs/items_key_nodefs.tsv 'dict' column | 3 | distinct dict values | OK |
| abstract | 23 of 27 unbiased cases | directional change senses in the C and R strata naming time | change-verbs/codes/*.tsv + items_key (final codes re-derived by the 2-of-3 rule) | 23, 27 | final OVER not UNSPECIFIED/ITEMS, strata C or R, plants out; OVER == TIME | OK |
| abstract | 64 published experiments | counted experiments | published-asymmetry/p65_published-asymmetry-coded_2026-11-13.tsv | 64 | tally rule re-applied: code in the four codes, not CLINICAL, not SECONDARY | OK |
| abstract | (27 against 14, with 21 symmetric) | primary tally | same TSV | 27, 14, 21 | Counter over counted rows (row 76 Riedl & Hallez Exp 1 = SYMMETRIC, ruled 2026-11-17) | OK |
| abstract | (p = .060) | two-sided exact sign test 27 vs 14 | same TSV | 0.05958 | binomial tail sum, doubled | OK |
| abstract | of 33 sources | Arm D map, one row per source | error-evidence/p65_armD_per-source_2026-11-17.tsv | 33 | rows counted; source_key distinct | OK |
| abstract | none shows time structuring space | T>S count | same TSV, direction_code | 0 | rows with direction_code T>S | OK |
| discussion | about three of four directional English sentences | 0.738 ≈ 3/4 | arm-a3-model results, CELL TABLE | 0.7379 | recomputed share; 0.74 reads 'three of four' | OK |
| discussion | lower bound 0.56 above one half | A3 interval lower bound | arm-a3-model results 'DIRECTIONAL share' line: 0.561 | 0.561 | READ | READ (source line) |
| discussion | 117 of the 121 directional senses | Garner licence on pooled directional senses | change-verbs/codes (final codes) with the appendix's dependence rule | 117, 121 | licensed = X over TIME (X ≠ TIME) plus size/colour/intensity/quantity over POSITION; total directional | OK |
| discussion | ten errors cannot decide | E1 count | error-evidence/p65_e1-run_2026-11-13.txt | 10 | n(S->T) + n(T->S) | OK |
| discussion | kappa 0.79 and 0.68 | first sample and A3 agreement | arm-a-model and arm-a3-model coder files | 0.7895, 0.6758 | Cohen's kappa recomputed on the 'class' columns (n 500, 1500) | OK |
| discussion | 0.58 on the | A3b agreement | arm-a3b-model coder files | 0.5759 | Cohen's kappa recomputed (n 2000) | OK |
| discussion | 300 of the same sentences is planned | planned human coding | docs/manuscript/p65_navon-validation_DRAFT.md (plan, no results file) |  | plan statement, not a result | LOCATED |
| discussion | 155 directional sentences | A3 combined directional count | arm-a3-model results CELL TABLE | 155 | Σ (TP + PT) over the six cells | OK |
| discussion | design effect of about 6 | stratified-draw design effect | p65_wave1_verify_2026-11-16.md L20: 5.0 to 6.9 | 5.95 | READ: midpoint of the verify pass's range | READ (source line) |
| discussion | about 22 to 31 independent items | 155 ÷ design effect | same, L20 | 22, 31 | 155 ÷ 6.9 and 155 ÷ 5.0, rounded | OK |
| discussion | ten of its 39 papers | abstract-only papers among counted | published-asymmetry coded TSV, 'verification' column | 10, 39 | papers whose counted rows all start ABSTRACT; distinct doi-or-key | OK |
| discussion | re-codes the 4,000 | wave 2 items | item maps (as above) | 4000 | rows counted | OK |
| discussion | all 30 ordered pairs | 6 dimensions, ordered pairs | p65_wave2_registration_2026-11-16.md Section 1.4 | 30 | 6 × 5 | OK |
| discussion | about 37 directional items per pair for direction at a share of 0.74 | exact binomial power 0.80 | Appendix D.6 table (exact binomial) | 37 | smallest n with exact two-sided power ≥ 0.80 at p = 0.74, α = .05 | OK |
| discussion | about 110 per pair | additivity power, simulation | docs/manuscript/p65_appendix-D_math_2026-11-16.md D.6 table | 110 | READ: simulation not rerun | READ (source line) |
| discussion | at least 20 per pair per criterion | rank-one power, simulation | same, D.6 table | 20 | READ: simulation not rerun | READ (source line) |
| discussion | time-place kappa 0.38 on 58 pilot | wave 2 pilot 2 | p65_wave3_registration_FROZEN_2026-11-16.md Section 0 ('0.376 in pilot 2 (n 58)') | 0.376, 58 | READ: pilot codes not re-scored here | READ (source line) |
| discussion | SHA-256 1c3e0fee | wave 3 freeze hash | wave3/FREEZE.txt |  | prefix compared with FREEZE.txt line 4 | LOCATED |
| discussion | (6,628 sentences, two treebanks | Indonesian census size | wave3/main/census_map.tsv | 6628 | rows counted | OK |
| discussion | about 164 directional items (113 | expected yield | p65_wave3_registration_FROZEN_2026-11-16.md Section 2.3 | 164, 113 | READ: yield pilot not rerun | READ (source line) |
| discussion | has power 1.00 at either count | exact binomial power at 0.74, n = 164 and 113 | recomputed | 0.9995 | exact two-sided binomial test of 0.5; power at p = 0.74 (the smaller of the two counts) | OK |
| discussion | keeps power 0.80 down to a true share of about 0.62 at 164 items | smallest share with exact power ≥ 0.80 at n = 164 | recomputed; the frozen registration's normal approximation said 0.60 (exact power there is 0.68) | 0.615 | exact binomial power scanned in steps of 0.001 | OK |
| discussion | eight languages suffice | mean-direction power, SD 0.5 | Appendix D.6 table ('8 languages × 50 items (0.99)') | 8 | READ: simulation not rerun | READ (source line) |
| discussion | twelve give power 0.90 | mean-direction power, SD 1.0 | Appendix D.6 table ('12 languages × 100 items (0.90)') | 12 | READ: simulation not rerun | READ (source line) |
| abstract | two Indonesian treebanks (6,628 sentences) | census size | wave3/main/codes (own recount) | 6628 | non-gold rows over P01 and M01 to M16 code files | OK |
| abstract | the share was 0.70 (0.58 to 0.80; 70 directional sentences) | share; interval; directional count | wave3/main/codes (own recount) | 0.7, 0.5832, 0.7955, 70 | TP / (TP + PT); logit(k/n) ± 1.96·sqrt(1/k + 1/(n−k)), own arithmetic; TP + PT, final labels re-derived | OK |
| discussion | 0.70 of its directional sentences | share | wave3/main/codes (own recount) | 0.7 | as above | OK |
| discussion | pair-label agreement was 0.60 | D-kappa over both-present sentences | wave3/main/codes (own recount) | 0.6034 | Cohen's kappa recomputed on the two coders' labels where neither is NA (n 743) | OK |
| discussion | the census returned 70, under the 100 | directional count; rule Y bar | wave3/main/codes (own recount) | 70, 100 | TP + PT; registration Section 3 | OK |
| discussion | Indonesian sentences about twice as often | 0.70 / 0.30 = 2.3 | wave3/main/codes (own recount) | 2.333 | odds from the recomputed share; 2.3 reads 'about twice' | OK |

43 numbers: 32 recomputed OK, 9 read from source lines, 2 located as text, 0 failures.
<!-- trace:generated:end -->

## Arm A (Sections 2.2 to 2.5)

| number in text | meaning | source | location |
|---|---|---|---|
| 30,975 sentences | corpus size (EWT 16,622 + GUM 14,353) | p65_arm-a2_entity-screen-results_2026-11-13.md | Data checks, "Sentence total is 30,975" |
| 29,975 | the slip in the frozen protocol | same | same paragraph |
| 200 / 250 / 50 | first-sample draw by group | p65_arm-a_model-results_2026-11-13.md | Result, "Final labels" |
| 88.8%, kappa 0.79 (0.74 to 0.84) | first-sample agreement | p65_arm-a_model-results_2026-11-13.md | Result: raw 0.888, kappa 0.789 (0.739 to 0.838) |
| 28 of 56 | disagreements that were NA vs PAR | same | Predictions scored, P5 |
| 50 directional, 42 TP, 8 PT | first sample | same | Result |
| 0.77 (0.36 to 0.98) | first-sample share, inconclusive | same | Result: s 0.769, 0.364 to 0.984 |
| recall 0.22 / 0.13 | word-list recall by direction | same | Result: "Screen recall: TP 0.22, PT 0.13" |
| 0.85 (39 of 46) | candidate-only share | same | Result: 0.848 (39 TP, 7 PT) |
| 1 hit, 4 miss, 13% | prediction scoring | same | Predictions scored |
| 4 frame directional, ~47 each | why the interval is wide | same | Decision paragraph |
| 12 of 50, 0.24 (0.14 to 0.37) | entity-screen recall | p65_arm-a2_entity-screen-results_2026-11-13.md | Results table, S1 |
| 10 of 42; 2 of 8 | recall by direction | same | S1 row |
| 3.4%, 0.03, "seven times" | flag rate and random control | same | Controls: mean recall 0.034 |
| 28 of 38 | misses with a date but a deictic place | same | "Where S1 fails" |
| 18 of 24, 0.75 (0.55 to 0.88) | GUM gold screen | same | S2 row |
| 40 of 50, 0.80, 14.6% | date-or-time alone | same | control row |
| 0.60 / 0.45 bar, commit 4a2de35 | registered bar | same | Decision |
| 1,500; commit a81a309 | registered extension draw | p65_arm-a3_results_2026-11-13.md | header and "What was done" |
| kappa 0.68 (0.63 to 0.72) | extension agreement | same | Result: 0.676 (0.632 to 0.719) |
| 155 directional | combined | same | Result |
| 0.74 (0.56 to 0.89), "about three to one" | registered share | same | Result: 0.738 (0.561 to 0.893), "about 2.8 to 1" |
| 4 of 7 hit, second most likely | prediction scoring | same | Predictions scored |
| one PT sentence, ~half of PT; 17,017 and 45 | limits | same | Limits 1 and 2 (weight 48 of 101 PT; R-N 17,017, 45 coded) |
| 1,000 + 1,000; commit 63f3a67 | exploratory draw | p65_arm-a3b_results_2026-11-13.md; commit 63f3a67 message | What was done |
| 0.82 (0.73 to 0.91) | exploratory share | same | Result table: 0.823 (0.728 to 0.906) |
| width "almost half" | 0.332 to 0.179 | same | Result table (DERIVED: 0.179/0.332 = 0.54) |
| 0.62 to 0.91 | worst-case bracket | same | "Bracket from these two cells" |
| kappa 0.58, raw 0.97 | agreement | same | Agreement: 0.576, 0.969 |
| 0.85 (0.79 to 0.92) | agreed-only share | same | Unregistered robustness: 0.854 (0.785 to 0.915) |
| "about a third" missed, "now"/"currently" | screen recall TP 0.64 | same | "What changed" |
| 0.80 strong-form rate | the plan's threshold, not Navon's | p65_arm-a_protocol-v2_2026-11-13.md Section 5 | decision labels (citation pass M09: Navon states no rate) |
| design effect about 6, 22 to 31 | Limitations, D.6 | p65_wave1_verify_2026-11-16.md | L20 row: 5.0 to 6.9; effective n 22-31 |

## Arm B (Section 3)

| number in text | meaning | source | location |
|---|---|---|---|
| 13,789 / 25,354 / 91,176 | verb senses per dictionary | p65_change-verbs-registration_2026-11-14.md | Extraction paragraph |
| 130,319 | total verb senses swept | p65_change-verbs-verification_2026-11-14.md (DERIVED sum matches) | step 3 |
| commit ea3fef9 | registration | p65_change-verbs-dictionaries_2026-11-14.md | header |
| 580 real senses | time census | same | Plain summary 4 |
| 1,725 items; 141 disagreements | coding | same | Plain summary, intro |
| kappa 0.91 / 0.95 / 0.89; n 931 | agreement | same | Plain summary 3 (verified 0.9105/0.9471/0.8854) |
| 5 of 5 plants | negative control | same | Plain summary 5 |
| 96% (66/69), 98% (58/59), 93% (65/70) | unspecified over-dimension | same | Plain summary 2 |
| 23 of 27 (0.68 to 0.94) | unbiased directional senses naming time | p65_change-verbs-verification_2026-11-14.md | claim 5 (Wilson 0.68-0.94); recomputed from the codes files in the block above |
| 112 of 121 | with the census | p65_change-verbs-dictionaries_2026-11-14.md | Plain summary 1 |
| time-change sense, "uncommon", no attested example | falsifier | dictionaries file, Falsifier section; verification claim 12 | |
| soil, 2 of 3 coders | disputed | dictionaries file | Falsifier and disputed |
| 3 of 121 (2.5%) | loss under Navon's order | same | Plain summary 6, F5 |
| refract, 2 of 3; "other" above position by one item | F5 failure | same; verification claim 11 | |
| permutation p = 0.95 | control | same | Plain summary 6 |
| 117 of 121 | Garner licence | same | Plain summary 7; recomputed in the block above |
| 10 vs 1 time-position (0.91, 0.62 to 0.98); 29 vs 0 | pair votes (not printed in v1 body; in Figure 3's data) | same | below pooled matrix |

## Arm C (Section 4)

| number in text | meaning | source | location |
|---|---|---|---|
| commit 66d9131 | registration | p65_published-asymmetry-results_2026-11-13.md | header |
| 64 experiments, 39 papers, 29 full, 10 abstract | inclusion | same | Section 1; recomputed in the block above |
| 27 / 14 / 21 / 2, p = .060 | primary tally | same | Section 2 table, row "all counted"; recomputed in the block above |
| 25 vs 11, p = .029 | adult visual | same | row "adult human, visual" |
| 15 vs 8, p = .21 | paper level | same | row "paper level" |
| 9 experiments; +0.018 (−0.002 to +0.037); Q = 27.8 | effect-size summary | same | Section 3: +0.0177, −0.0019 to +0.0373 |
| shuffle control +0.00004 | negative control | same | Section 3 |
| kappa 0.95 on 62 rows | second coding | published-asymmetry/second-coding/p65_arm-c-second-coding-report_2026-11-13.md | Agreement table: .952 |
| Lambrechts E1 ruling: TIME>SPACE, p < .05 vs Bonferroni .005 | ruling | published-asymmetry/p65_armC_lambrechts2013-E1-ruling_2026-11-14.md | Ruling and table |
| row 76 (Riedl & Hallez 2026 Exp 1): SYMMETRIC, full-text code stands | RULED 2026-11-17 from rendered pages 15 and 17 of the HAL manuscript (visual Spacing F(1, 87) = 23.00, p < .001; Duration F(1, 87) = 4.11, p = .046; no direction test); primary tally unchanged | published-asymmetry/p65_armC_row76-ruling_2026-11-14.md | Status |
| 28 vs 14, p = .044 | second-coder tally | second-coding report; p65_tally_2tailed.txt | DERIVED: 27 + row 76 as S>T under the second coder's abstract code |
| 42% / 36% / 22% vs predicted 55 / 30 / 15 | Arm C prediction | p65_published-asymmetry-results_2026-11-13.md | Bottom line, last bullet |
| paradigm list (moving/growing stimuli vs touch, accumulation, harder tasks, repeated intervals) | Section 4 | same | Section 4 bullets |

## Arm D (Section 5)

| number in text | meaning | source | location |
|---|---|---|---|
| 33 sources; 5 read in full | map, recounted 2026-11-17 | error-evidence/p65_armD_per-source_2026-11-17.tsv; p65_armD_recount_2026-11-17.md | 33 rows (33 distinct source keys); status FULL 4 + "PDF grepped" 1 |
| 9 S>T (2 also DISSOC), 7 DISSOC, 9 MIXED, 0 T>S, 8 NONE, 2 unknown | direction codes | same TSV; error-evidence/p65_armD_recount-run_2026-11-17.txt | sum 35 = 33 + 2 double-coded. The map's 2026-11-13 line (42 sources; 12/7/9/0/15/2) is not reproducible from a source list and is retired. |
| Kemmerer 2005; Mätzig 2009 (five patients, no reliable difference); Saj 2014; Rousselle 2013 | strongest three | p65_error-evidence-map_2026-11-13.md; citation ledger M13-M15 | Strongest three |
| commit 0c6fcdd | registration | p65_error-evidence-results_2026-11-13.md | header |
| 1.22 million words | learner tokens 1,223,992 | error-evidence/p65_e1-run_2026-11-13.txt | LEARNER tokens; recomputed in the block above |
| 10 errors: 8 T->S, 2 S->T; 0.20 (0.03 to 0.56) | share | same | E1 line (0.025-0.556) |
| 23,117 native tokens, 0 | native control | same | NATIVE block |
| 4 of 8 "before" -> "above" | text deixis | same | word pairs: "E1 before -> above: 4" |

## Introduction

| number in text | meaning | source | location |
|---|---|---|---|
| 24 to 26 citers, criterion (a) only | citer screen | p65_navon-validation_DRAFT.md line 42; p65_navon-formal-model_2026-11-13.md line 15 | |
| two searches, no test of (b) | prior art | p65_change-verbs-dictionaries_2026-11-14.md | Prior art |
| Mondor 1998 screened by title only | S3 verification F03/A65 | p65_s3-triage-verdicts_2026-11-17.tsv | rows F03, A65 |
| p. 223, 226, 227 quotations and page cites | Navon 1978 | sources/ PDF; p65_v1_citation-ledger_2026-11-17.tsv rows M02-M05, M17, A05 (p. 225 corrected to p. 226 at integration) | |
| Garner pp. 102, 105 | logical dependence left open | p65_v1_citation-ledger_2026-11-17.tsv M16 | |
| one-sided p .030 / .022 | D.4 | docs/manuscript/p65_appendix-D_math_2026-11-16.md | D.4 "Where the data stand" |

## Appendix B, C, D

- Appendix B describes the registered estimators in words. Sources: p65_arm-a_protocol-v2_2026-11-13.md Sections
  4 and 5 (expansion, document bootstrap, decision labels, kappa bar), p65_arm-a3b_results_2026-11-13.md
  (Clopper-Pearson bracket), p65_change-verbs-registration_2026-11-14.md (Wilson, F5 fit, permutation),
  p65_published-asymmetry-results_2026-11-13.md Section 3 (DerSimonian-Laird, permutation control),
  p65_error-evidence-registration_2026-11-13.md (minimum of ten). The decision-label thresholds (0.5, 0.8) are
  as printed in protocol v2 Section 5; F4 should confirm the "supports strong" bound against that file.
- Appendix C tables are copied verbatim from p65_arm-a_model-results_2026-11-13.md, p65_arm-a3_results_2026-11-13.md
  and p65_arm-a3b_results_2026-11-13.md ("Predictions scored").
- Appendix D is docs/manuscript/p65_appendix-D_math_2026-11-16.md with these edits only: figure numbers kept as
  D1, D2 (the fold's "Figures 6, 7" reverted at integration, figure files p65_figD1/D2); "waves 2 and 3" phrasing
  kept; the design-effect sentence reworded per verify L20 ("about 6 (5 to 7 by approximation)"); the pointer to
  `p65_navon-formal-model_2026-11-13.md` in D.4 dropped; a one-sentence note under F5 in D.7 that Arm B's falsifier
  makes the time row non-empty; the opening paragraph gained a sentence naming the verdict vocabulary and the
  Wolfram and verify checks; citation edits A05 (p. 226, no "never" quotation), A08 (logical-dependence reading of
  Garner p. 102), M09 (F6 is the registered strong form, not Navon's) and years added at first mention of
  Thurstone, Luce and Rao-Kupper. Its reference list is merged into the main References.

## Figures

Every plotted value is in `docs/manuscript/figures/p65_v1_figure-data.json`, recomputed by
`scripts/p65_v1_figure-audit.py` (run of 2026-11-17 after the Arm D rebuild: 69 checks, 0 mismatches; `--perturb`
control fires 8). Figure 5 was rebuilt at integration with N = 33 and codes 9/7/9/0/8/2.
