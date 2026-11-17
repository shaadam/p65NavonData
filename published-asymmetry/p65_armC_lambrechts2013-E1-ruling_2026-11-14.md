# p65 Arm C: ruling on Lambrechts et al. (2013) Experiment 1 (row 13) (2026-11-14)

**Ruling: TIME>SPACE** (primary code; the 2-tailed code is the same). It is decided by the coding rule as registered before coding, not by its effect on the tally.

## The source

Lambrechts, A., Walsh, V., & van Wassenhove, V. (2013). Evidence accumulation in the magnitude system. *PLoS ONE*, 8(12), e82122. https://doi.org/10.1371/journal.pone.0082122

- Now held: `sources/Lambrechts2013_evidence-accumulation-magnitude_PLoSONE8-e82122.pdf` (sha256 a92966fd…4d2b41). Open access, from journals.plos.org, fetched 2026-11-13. Quotes were read off PyMuPDF-rendered page images.
- Table S1 is held as `sources/Lambrechts2013_TableS1_pone.0082122.s004.docx` (sha256 bf7855c2…eea946). PLoS publishes it only as a Word file (supplement .s004), not a PDF, so its t and p values were read from the table cells of the authors' own document. No office renderer was available to make an image of it.

## The rule, as registered before coding

The registration is `p65_published-asymmetry-registration_2026-11-13.md`, commit 66d9131 (15:31). The first coding is commit 7e10c7b (16:07).

- Coding table, row 1: "SPACE>TIME | space-on-time effect significant (p < .05) and time-on-space not significant; OR a significant dimension × direction interaction favouring space-on-time | the authors' slope, regression coefficient, interaction F or t". Row 2: "TIME>SPACE | the mirror image".
- Inclusion rule: each experiment must measure "(ii) the effect of irrelevant temporal magnitude on a spatial judgement".
- "Where the authors' own summary and their statistics disagree, the statistics win".

The rule defines significance as **p < .05** on the authors' t. It says nothing about correcting for multiple comparisons, and it does not adopt each paper's own significance threshold.

## What the paper reports (Experiment 1, prospective, N = 12)

- p. 3, Analysis: "Post-hoc Bonferroni-corrected paired t-tests were performed to explore significant main effects or interactions."
- p. 9, legend of Table S1: "Results are Bonferroni-corrected (significance threshold = .005). Values in the table are t values (p values)."
  - The printed p values are uncorrected. The table stars only p ≤ .005, and the surface c1 vs c2 contrast is printed as .006 with no star.
- p. 5, surface estimation: "surfaces were judged to be smaller when duration and number were maximal than when they were minimal (PSE2>PSE1, t12,11 = −3.389, p<0.01)". This contrast changes duration and number together.
- p. 5: "Unexpectedly, neither surface nor numerosity significantly interfered with duration estimation."
- p. 5, the omnibus test across all three tasks: "a marginal interaction of magnitude with condition (F12,8 = 2.905, p = .051".
  - The first coding transcribed this as F(12,4). The page prints F12,8. This does not affect the code.

### Contrasts that isolate one dimension (Table S1A)

Each contrast below changes one dimension and holds number fixed.

| direction | contrast | t | p (uncorrected) | < .05? | < .005 (authors' Bonferroni)? |
|---|---|---|---|---|---|
| time on space (surface task) | c1 (Dmin, Nmin) vs c4 (Dmax, Nmin) | −2.423 | .034 | yes | no |
| time on space (surface task) | c3 (Dmin, Nmax) vs c2 (Dmax, Nmax) | 3.247 | .008 | yes | no |
| space on time (duration task) | c1 (Smin, Nmin) vs c4 (Smax, Nmin) | 0.047 | .964 | no | no |
| space on time (duration task) | c3 (Smin, Nmax) vs c2 (Smax, Nmax) | −1.292 | .223 | no | no |

Both duration-only contrasts point the same way: the surface PSE is higher at Dmax, so longer duration makes the surface look smaller.

## Applying the rule

1. **Which contrasts count.** The inclusion rule asks for "the effect of irrelevant temporal magnitude". Only contrasts that change duration with number held fixed measure that. So the first coder's grounds do not count:
   - PSE2 vs PSE1, p = .006 in Table S1, changes duration and number together;
   - PSE0 vs PSE1 changes them together too.

   The second coder chose the right contrasts.
2. **Significance threshold.** The registered rule says p < .05 on the authors' t. On that rule:
   - time on space is significant: p = .034 and p = .008;
   - space on time is not: p = .964 and p = .223.

   The result holds whether the rule needs one duration-only contrast to be significant or both. Using the authors' .005 threshold would bring in a correction the registration did not set. It covers a family of 10 pairwise contrasts per task, and most of them do not bear on the registered question.
3. **Asymmetry test.** No direct test of time-on-space against space-on-time is reported, so the "both sig" clause does not apply.

**Code: TIME>SPACE.** This matches the first coder's code, but on the duration-only contrasts rather than the confounded ones. The second coder's NONE comes from applying the authors' Bonferroni threshold, which the registered rule does not use.

## Effect on the tally

The second coding's frozen primary codes are 28 SPACE>TIME, 13 TIME>SPACE, 18 SYM, 3 NONE and 2 UNREACHED (recounted from `second-coding/p65_arm-c-second-coding_2026-11-13.tsv`). Recoding row 13 from NONE to TIME>SPACE gives:

- **28 SPACE>TIME / 14 TIME>SPACE** (18 SYM, 2 NONE);
- two-sided exact sign test **p = .044** (exact value .0436, recomputed).

**Correction to the second-coding report.** The report says that coding row 13 TIME>SPACE "goes back to exactly 27/14, p = .060". That is wrong. Changing row 13 alone gives 28/14. The second coding differs from the first coding's 27/14 by two rows:

- row 13, Lambrechts E1, decided here;
- row 76, Riedl & Hallez 2026 Exp 1. The second coder read only the abstract and coded SPACE>TIME. The first coder read the full text and coded SYMMETRIC. The report itself calls the first coding better founded.

With both rows at the first coder's codes, the tally is 27/14, p = .060. So the .05 line now depends on row 76, not on row 13. This ruling does not decide row 76.

**What stays the same.**

- The registered verdict is unchanged: the experiment-level primary sign test of the first, registered coding is still p = .060, and the paper-level and full-text-only tallies still do not reject.
- The registration asks for no sensitivity analysis on multiple-comparison correction. The tally with row 13 coded NONE (28/13, p = .028) is recorded here only as a record of the disagreement. It is not a registered result.

## Draft change

`docs/manuscript/p65_navon-validation_DRAFT.md`, §5: the sentence that gave 28/13 (p = .028) and said the result "turns on" Lambrechts E1 now gives:

- the decided 28/14 (p = .044);
- the row-76 sensitivity: 27/14, p = .060, if the first coder's full-text code is used.
