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
## Abstract and Discussion, recomputed by `scripts/p65_v1_number-trace.py` (2026-11-19, after the full-text recode)

Status: OK = printed value matches the recomputation; READ = taken from the results line (bootstrap or simulation not rerun); LOCATED = text-only claim found; MISMATCH / NOT IN TEXT fail the run.

| region | printed | meaning | source | recomputed | method | status |
|---|---|---|---|---|---|---|
| abstract | in four studies | arms A, B, C, D | Sections 2 to 5 | 4 | count of arm sections | OK |
| abstract | Two AI coders of one model family | coders per sample | arm-a*/codes_coder1, coder2 | 2 | files per sample | OK |
| abstract | about three times as often | 0.738 / (1 − 0.738) = 2.8 | arm-a3-model/p65_a3-results_2026-11-13.txt | 2.815 | odds from the recomputed share; 2.8 reads 'about three' | OK |
| abstract | 0.74 of sentences in which one dimension restricts the other | registered share, time over place | arm-a3-model/p65_a3-results_2026-11-13.txt CELL TABLE | 0.7379 | Σ TP·pop/coded ÷ Σ (TP+PT)·pop/coded over the six cells | OK |
| abstract | (95% interval 0.56 to 0.89) | document bootstrap within cells, 10,000 resamples | same file, 'DIRECTIONAL share' line: 0.561 to 0.893 | 0.561, 0.893 | READ: the bootstrap is not rerun here | READ (source line) |
| abstract | that say what the change happens over, 23 say time | directional change senses in the C and R strata naming time | change-verbs/codes/*.tsv + items_key (final codes re-derived by the 2-of-3 rule) | 23, 27 | final OVER not UNSPECIFIED/ITEMS, strata C or R, plants out; OVER == TIME | OK |
| abstract | 64 experiments from 39 papers | counted experiments | published-asymmetry/p65_published-asymmetry-coded_2026-11-13.tsv | 64 | tally rule re-applied: code in the four codes, not CLINICAL, not SECONDARY | OK |
| abstract | only the effect of space (extent or distance) on time reached significance in 25, and only that of time on space in 14 (both in 22, neither in 3) | primary tally | same TSV | 25, 14, 22, 3 | Counter over counted rows (row 76 Riedl & Hallez Exp 1 = SYMMETRIC, ruled 2026-11-17; Jagorska et al. 2025 one experiment = SYMMETRIC/MERGED, G04 merge 2026-11-19; full-text recode 2026-11-19, Reali et al. 2019 = SYMMETRIC by ruling) | OK |
| abstract | none shows time dominating space, and two partly | T>S count (the sentence opens 'Of 32 sources') | same TSV, direction_code | 0 | rows with direction_code T>S | OK |
| abstract | Of 32 sources on errors | Arm D sources read (direction code not unknown) | same TSV | 32 | rows minus direction_code unknown (apply pass 2026-11-19) | OK |
| discussion | about three of four directional English sentences | 0.738 ≈ 3/4 | arm-a3-model results, CELL TABLE | 0.7379 | recomputed share; 0.74 reads 'three of four' | OK |
| discussion | lower bound 0.56 above one half | A3 interval lower bound | arm-a3-model results 'DIRECTIONAL share' line: 0.561 | 0.561 | READ | READ (source line) |
| discussion | 117 of the 121 directional senses | Garner licence on pooled directional senses | change-verbs/codes (final codes) with the appendix's dependence rule | 117, 121 | licensed = X over TIME (X ≠ TIME) plus size/colour/intensity/quantity over POSITION; total directional | OK |
| discussion | kappa 0.79 and 0.68 | first sample and A3 agreement | arm-a-model and arm-a3-model coder files | 0.7895, 0.6758 | Cohen's kappa recomputed on the 'class' columns (n 500, 1500) | OK |
| discussion | 0.58 on the | A3b agreement | arm-a3b-model coder files | 0.5759 | Cohen's kappa recomputed (n 2000) | OK |
| discussion | 300 of the same sentences is planned | planned human coding | docs/manuscript/p65_navon-validation_DRAFT.md (plan, no results file) |  | plan statement, not a result | LOCATED |
| discussion | 155 directional sentences | A3 combined directional count | arm-a3-model results CELL TABLE | 155 | Σ (TP + PT) over the six cells | OK |
| discussion | design effect of about 6 | stratified-draw design effect | p65_wave1_verify_2026-11-16.md L20: 5.0 to 6.9 | 5.95 | READ: midpoint of the verify pass's range | READ (source line) |
| discussion | about 22 to 31 independent items | 155 ÷ design effect | same, L20 | 22, 31 | 155 ÷ 6.9 and 155 ÷ 5.0, rounded | OK |
| discussion | Its 64 experiments come from 39 papers | counted experiments and papers (none coded from an abstract: 0) | published-asymmetry coded TSV | 64, 39 | tally rule re-applied; papers = distinct doi-or-key | OK |
| discussion | Four of the 33 error-map sources were read only as abstracts or as cited | error-map sources not read in full or in part | error-evidence/p65_armD_per-source_2026-11-17.tsv column status_in_map | 4, 33 | rows with status other than FULL or partial (ABS, SEC, title only, not stated); all rows | OK |
| discussion | word for word in 4% of its verb senses | Wiktionary verb senses repeating a Webster 1913 definition exactly (3814 of 91176) | change-verbs/p65_wiktionary-webster-overlap_run_2026-11-19.txt | 4.183 | parsed from the registered run (dictionaries not in the tree); percent | OK |
| discussion | 111 of 120 directional senses vary over time | change count with exact-matched Wiktionary items removed | same run file | 111, 120 | parsed from the EXACT-MATCHED WK REMOVED line | OK |
| discussion | in 121 of 134 where the place needs the time (0.90) | direction-blind dependence: place needs time, TP | dependence/adversarial final codes + blind map + item directions | 121, 134, 0.903 | join and count, plants dropped | OK |
| discussion | 32 of 47 where neither needs the other (0.68 | direction-blind dependence: neither, TP | same | 32, 47, 0.6809 | join and count | OK |
| discussion | (0.68, 95% interval 0.53 to 0.81) | exact interval, neither cell | p65_depadv_analysis_run_2026-11-19.txt NEITHER line | 0.529, 0.809 | READ | READ (source line) |
| discussion | too few to read (5 of 9) | direction-blind dependence: time needs place, TP | same join | 5, 9 | join and count | OK |
| discussion | the pooled odds ratio of 3.9 | Mantel-Haenszel OR, P vs T+NEITHER by language | same join | 3.892 | MH point estimate recomputed here (apply pass 2026-11-19; interval 1.75 to 8.64 no longer printed) | OK |
| discussion | in English (odds ratio 8.9, | English OR, P vs T+NEITHER | same join | 8.874 | ad/bc from the joined 2x2 | OK |
| discussion | in Indonesian (1.7, *p* = .54) | Indonesian OR and Fisher p | same join; p from scipy fisher_exact on the same table (methods-evidence 2026-11-19 apply pass) | 1.667, 0.5424 | ad/bc; p READ | OK |
| discussion | The two languages differ (*p* = .04) | MH homogeneity p | p65_depadv_stratified_run_2026-11-19.txt 'homogeneity p 0.04' | 0.04 | READ | READ (source line) |
| discussion | in 37 of 53 where each needs the other (0.70) | direction-blind dependence: both, TP | same join | 37, 53, 0.6981 | join and count | OK |
| discussion | less often than the others (12 of 20; | TP among definitional pairings | p65_defadv_final.tsv column inter | 12, 20 | count | OK |
| discussion | The 20 such pairings of 243 | blind definitional, both coders | definitional-adversarial/p65_defadv_final.tsv column inter | 20, 243 | rows counted | OK |
| discussion | 0.32, 95% interval 0.12 to 0.85 | Firth OR, blind definitional, language-adjusted | p65_defadv_assoc_run_inter_2026-11-19.txt 'dependent' Firth line | 0.3186, 0.1237, 0.851 | READ | READ (source line) |
| discussion | 86% of the coded English pairings and 72% of the Indonesian | TP share among non-definitional pairings, per language | p65_defadv_final.tsv | 86.16, 71.88 | count; percent | OK |
| discussion | 3 of the 499 changes to run over space (0.6%) | unit 4 spatial share of directional uses | change-verbs/unit4 codes + adjudication, plants dropped | 3, 499, 0.6012 | final code = adjudicated else agreed; directional = TEMPORAL + SPATIAL + OTHER-DIM | OK |
| discussion | 9 of 121 senses not over time (7.4% | dictionary directional senses not over time | change-verbs/unit4/p65_unit4_directional-senses.tsv | 9, 121, 7.438 | rows counted; percent | OK |
| discussion | their 6 of 121 over space (5.0%, p = .002) | dictionary directional senses over space; Fisher vs usage 3/499 | p65_unit4_directional-senses.tsv; p from p65_unit4_analysis-output_2026-11-19.txt sensitivity (a) 'p = 0.002484' | 6, 121, 4.959, 0.002484 | rows counted; percent; p READ | OK |
| discussion | In 915 corpus uses | unit 4 real uses coded | same | 915 | rows counted, plants dropped | OK |
| discussion | re-codes the 4,000 | wave 2 items | item maps (as above) | 4000 | rows counted | OK |
| discussion | all 30 ordered pairs | 6 dimensions, ordered pairs | p65_wave2_registration_2026-11-16.md Section 1.4 | 30 | 6 × 5 | OK |
| discussion | about 37 directional items per pair for direction at a share of 0.74 | exact binomial power 0.80 | Appendix D.6 table (exact binomial) | 37 | smallest n with exact two-sided power ≥ 0.80 at p = 0.74, α = .05 | OK |
| discussion | about 110 per pair | additivity power, simulation | docs/manuscript/p65_appendix-D_math_2026-11-16.md D.6 table | 110 | READ: simulation not rerun | READ (source line) |
| discussion | at least 20 per pair per criterion | rank-one power, simulation | same, D.6 table | 20 | READ: simulation not rerun | READ (source line) |
| discussion | time-place kappa 0.38 on 58 pilot | wave 2 pilot 2 | p65_wave3_registration_FROZEN_2026-11-16.md Section 0 ('0.376 in pilot 2 (n 58)') | 0.376, 58 | READ: pilot codes not re-scored here | READ (source line) |
| discussion | SHA-256 1c3e0fee | wave 3 freeze hash | wave3/FREEZE.txt |  | prefix compared with FREEZE.txt line 4 | LOCATED |
| discussion | (6,628 sentences, two treebanks | Indonesian census size | wave3/main/census_map.tsv | 6628 | rows counted | OK |
| discussion | about 164 directional items (113 | expected yield | p65_wave3_registration_FROZEN_2026-11-16.md Section 2.3 | 164, 113 | READ: yield pilot not rerun | READ (source line) |
| discussion | has power 1.00 at 164 or 113 items | exact binomial power at 0.74, n = 164 and 113 | recomputed | 0.9995 | exact two-sided binomial test of 0.5; power at p = 0.74 (the smaller of the two counts) | OK |
| discussion | keeps power 0.80 down to a true share of about 0.62 at 164 items | smallest share with exact power ≥ 0.80 at n = 164 | recomputed; the frozen registration's normal approximation said 0.60 (exact power there is 0.68) | 0.615 | exact binomial power scanned in steps of 0.001 | OK |
| discussion | eight languages of 50 directional items each suffice | mean-direction power, SD 0.5 | Appendix D.6 table ('8 languages × 50 items (0.99)') | 8 | READ: simulation not rerun | READ (source line) |
| discussion | twelve of 100 give power 0.90 | mean-direction power, SD 1.0 | Appendix D.6 table ('12 languages × 100 items (0.90)') | 12 | READ: simulation not rerun | READ (source line) |
| abstract | 70 such sentences among 6,628 | census size | wave3/main/codes (own recount) | 6628 | non-gold rows over P01 and M01 to M16 code files | OK |
| abstract | gave 0.70 (0.58 to 0.80; 70 such sentences | share; interval; directional count | wave3/main/codes (own recount) | 0.7, 0.5832, 0.7955, 70 | TP / (TP + PT); logit(k/n) ± 1.96·sqrt(1/k + 1/(n−k)), own arithmetic; TP + PT, final labels re-derived | OK |
| discussion | 0.70 of its directional sentences | share | wave3/main/codes (own recount) | 0.7 | as above | OK |
| discussion | pair-label agreement was 0.60 | D-kappa over both-present sentences | wave3/main/codes (own recount) | 0.6034 | Cohen's kappa recomputed on the two coders' labels where neither is NA (n 743) | OK |
| discussion | the census returned 70, under the 100 | directional count; rule Y bar | wave3/main/codes (own recount) | 70, 100 | TP + PT; registration Section 3 | OK |
| discussion | Indonesian sentences about twice as often | 0.70 / 0.30 = 2.3 | wave3/main/codes (own recount) | 2.333 | odds from the recomputed share; 2.3 reads 'about twice' | OK |

59 numbers: 45 recomputed OK, 12 read from source lines, 2 located as text, 0 failures.
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
| 4% (3,814 of 91,176); 111 of 120 | Wiktionary senses repeating Webster 1913 word for word; change count without them (6.4) | change-verbs/p65_wiktionary-webster-overlap_run_2026-11-19.txt (registration commit 806e8d6) | ALL senses exact 0.0418; EXACT-MATCHED WK REMOVED 111 of 120; recomputed in the block above |
| 10 vs 1 time-position (0.91, 0.62 to 0.98); 29 vs 0 | pair votes (not printed in v1 body; in Figure 3's data) | same | below pooled matrix |

## Arm C (Section 4)

| number in text | meaning | source | location |
|---|---|---|---|
| commit 66d9131 | registration | p65_published-asymmetry-results_2026-11-13.md | header |
| 64 experiments, 39 papers, all read in full | inclusion | published-asymmetry/p65_tally_primary.txt (full-text recode 2026-11-19, commit 8d36e59: Riemer et al. 2026 Exp 2 added; was 63 after the G04 merge, 29 full / 10 abstract) | header; recomputed in the block above |
| 25 / 14 / 22 / 3, p = .108; share .64 [.47, .79] Clopper-Pearson | primary tally | published-asymmetry/p65_tally_primary.txt; verify/p65_v1_sign-tests-R_2026-11-17.R | "PRIMARY" block (p = 0.1081); R binom.test 25/39: 0.641, CP 0.472 to 0.788; recomputed in the block above |
| 23 vs 11, p = .058; .68 [.49, .83]; sensitivity 24 vs 11, p = .041 | adult visual; sensitivity codes Reali et al. 2019 SPACE>TIME | published-asymmetry/p65_tally_primary.txt; R binom.test; published-asymmetry/p65_armC_fulltext-recode_comparison_2026-11-19.md | "ADULT HUMAN, VISUAL" block (p = 0.0576); R 23/34: 0.676, CP 0.4947 to 0.826; sensitivity 24/35 p = 0.0410 |
| 13 vs 8, p = .38; .62 [.38, .82] | paper level | same; R binom.test | row "paper level" (p = 0.3833); R 13/21: 0.619, CP 0.384 to 0.819 |
| 9 experiments; +0.018 (−0.002 to +0.037); Q = 27.8 | effect-size summary | same | Section 3: +0.0177, −0.0019 to +0.0373 |
| shuffle control +0.00004 | negative control | same | Section 3 |
| kappa 0.93 on 61 rows; three substantive disagreements | second coding | published-asymmetry/second-coding/p65_arm-c_compare-output_2026-11-19.txt (rerun after the recode) | "code2 vs first code": reached n = 61, kappa 0.927 (was 0.951 before the recode; Reali et al. 2019 now differs) |
| Lambrechts E1 ruling: TIME>SPACE, p < .05 vs Bonferroni .005 | ruling | published-asymmetry/p65_armC_lambrechts2013-E1-ruling_2026-11-14.md | Ruling and table |
| row 76 (Riedl & Hallez 2026 Exp 1): SYMMETRIC, full-text code stands | RULED 2026-11-17 from rendered pages 15 and 17 of the HAL manuscript (visual Spacing F(1, 87) = 23.00, p < .001; Duration F(1, 87) = 4.11, p = .046; no direction test); primary tally unchanged | published-asymmetry/p65_armC_row76-ruling_2026-11-14.md | Status |
| 27 vs 13, p = .038 | second-coder tally | published-asymmetry/second-coding/p65_arm-c_compare-output_2026-11-19.txt | "SECOND CODER code2 (UNREACHED dropped)": p = 0.0385 |
| 61 experiments, 38 papers; 0.53 logits, SE 0.41, p = .19; sign-flip p = .26 | exploratory clustered analyses | published-asymmetry/p65_clmm_by-paper-run_2026-11-17.txt (rerun after the recode) | threshold midpoint -0.5343, SE 0.4051, Wald p 0.1872; sign-flip p 0.2616 |
| 39% / 39% / 22% vs predicted 55 / 30 / 15 | Arm C prediction | published-asymmetry/p65_tally_primary.txt | 25, 22 + 3, 14 of 64 (DERIVED: 39.1, 39.1, 21.9) |
| 14 of 39; p = .108; one-sided .054 | Appendix D.4 and Figure D1 | published-asymmetry/p65_tally_primary.txt; R binom.test one-sided 0.0541 | Figure D1 annotation read from the tally file by scripts/p65_wave1_figs.py |
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
