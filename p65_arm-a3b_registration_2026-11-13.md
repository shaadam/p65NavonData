# p65 Arm A3b: closing the unsampled-zero gap in F-N and R-N, registration (2026-11-13)

Written and saved before any A3b item is drawn, coded or read. Follows the "Next" line of
`p65_arm-a3_results_2026-11-13.md`. (No git commands in this session; the file's mtime and SHA-256, recorded in
`arm-a3b-model/p65_a3b-run-log.txt`, stand in for a commit until Adam commits it.)

## Why

A3 gave s = 0.738 (95% 0.561 to 0.893), SUPPORTS_DIRECTION. Two cells without a DATE/TIME entity hold most of the
corpus but were barely coded:

| cell | population (eligible) | coded so far | weight | final labels so far |
|---|---|---|---|---|
| F-N | 9,052 | 188 | 48.15 | PT 1, PAR 8, NA 179 |
| R-N | 17,017 | 45 | 378.16 | NA 45 |

The bootstrap cannot see what an unsampled cell might hold: R-N's rule-of-three bound (3/45) allows up to about
1,100 directional sentences, four times all the TP estimated elsewhere; and F-N's one PT stands for 48 of the 101
estimated PT. A3b codes 1,000 more from each cell.

## Draw

- Pools: eligible sentences (protocol v2 sec. 4.4: at most 60 tokens, content list) of F-N and R-N, minus every
  sentence already coded in Arm A (M items) or A3 (N items). Sizes: F-N 8,864, R-N 16,972.
- **1,000 from F-N and 1,000 from R-N**, uniform without replacement, **seed 20261115**. Cells as in A3: Arm A
  group (F or R) x T (spaCy 3.8.18 `en_core_web_sm` 3.8.0 finds no DATE/TIME entity), read from the same entity
  cache as A2/A3 (`spacy_ents.json`, SHA-256 d72cf8e2...6fd9; UD r2.18 files, hashes equal to A2's).
- The 2,000 are shuffled together, given IDs Z0001 to Z2000, and split into 4 batches of 500. Coders see only
  item, previous sentence, sentence; no cell, no source.
- Script: `arm-a3b-model/p65_navon_arm_a3b_sample.py` (A3's sampler with the cells and pools changed; reuses
  `scripts/p65_navon_arm_a_sample.py` for loading and exclusions). It asserts no drawn item was coded before.

## Coding (A3's procedure, unchanged)

- Codebook v2 sec. 2 only (protocol v2), five classes TP / PT / PAR / AMB / NA, with time phrase, place phrase,
  confidence 1-3, note.
- Two blind model coders in fresh contexts: coder 1 Opus, coder 2 Sonnet (Claude subagents, as in Arm A and A3).
  Each codes the 4 batches; each output is checked to hold exactly its batch's items, in order, with valid classes.
- Disagreements go to a blind Opus adjudicator: codebook, previous sentence, sentence, the two codes (unlabelled
  as code_A / code_B); no cell, no coder identity; Arm A's consistency rule for PT ("when a sentence asserts a
  time value and place picks which instance, it is PT").
- Note on blindness: every A3b item lacks a DATE/TIME entity, so the batches are mostly NA. The coders are not
  told this.

## Analysis (registered script `arm-a3b-model/p65_navon_arm_a3b_analyze.py`, smoke-tested on synthetic codes before any real code exists)

1. Final labels for Arm A (500), A3 (1,500) and A3b (2,000), all frozen except A3b's. The same 6 cells; F-N coded
   becomes 1,188 (weight 7.62), R-N 1,045 (weight 16.28); other cells unchanged.
2. s = N_TP / (N_TP + N_PT), expansion over 6 cells; 95% interval by document bootstrap within cells, 10,000
   resamples, seed 20261114 (A3's). Decision label by protocol v2 sec. 5 (unchanged).
3. Agreement on the 2,000 A3b items: raw, Cohen's kappa with bootstrap 95%. Bar 0.60 as before. Because nearly
   all items will be NA, kappa may fall from prevalence alone; raw agreement and the NA-vs-other confusion
   table are reported beside it, but the protocol rule (kappa < 0.60 -> exploratory) is kept as written.
4. **Per-stratum bounds** for F-N and R-N, each direction: count k of n, exact Clopper-Pearson 95% two-sided
   interval on the rate, and for k = 0 the one-sided 95% upper bound (rule of three, 3/n, and the exact
   1 - 0.05^(1/n)). Each bound is multiplied by the cell population to give the most sentences of that
   direction the cell can hold.
5. **Bracket for s from these two cells** (a sensitivity check the bootstrap cannot give): s_low sets F-N and
   R-N TP at their Clopper-Pearson lower bounds and PT at their upper bounds; s_high the reverse; the other four
   cells at their estimates.
6. T-screen recall per direction, as in A3.

## Predictions

With the other four cells as in A3 (N_TP 285, N_PT 53 from them), the point estimate depends on the A3b counts as
follows (F-N totals include the old PT; R-N with 0 directional unless stated):

| F-N TP / PT (of 1,188) | R-N TP / PT (of 1,045) | s |
|---|---|---|
| 0 / 1 | 0 / 0 | 0.82 |
| 2 / 3 | 0 / 0 | 0.80 |
| 3 / 6 | 0 / 0 | 0.76 |
| 0 / 10 | 0 / 0 | 0.69 |
| 0 / 20 | 0 / 0 | 0.58 |
| 0 / 30 | 0 / 0 | 0.50 |
| 0 / 1 | 0 / 3 | 0.72 |
| 0 / 1 | 0 / 14 | 0.50 |
| 10 / 1 | 0 / 0 | 0.86 |

What counts as what:
- **A3 claim holds (interval essentially unchanged or narrower):** s stays in 0.65 to 0.85 and the label stays
  SUPPORTS_DIRECTION. Needs roughly PT - TP below about 10 in F-N and below about 3 in R-N.
- **Moves toward Navon's strong rate:** F-N and R-N add TP but almost no PT (e.g. F-N 10 TP / 1 PT, s about 0.86);
  label could become SUPPORTS_STRONG only if L > 0.80.
- **Moves against:** about 20+ net PT in F-N (s < 0.6) or 8+ net PT in R-N; 30 net PT in F-N or 14 in R-N
  brings s to 0.5 and the label to INCONCLUSIVE.
- **Zero-gap closed:** if a cell has 0 of a direction, its exact upper bound becomes at most about 23 (F-N) and
  49 (R-N) sentences in the population, against N_TP about 285, so no unseen remainder in these cells could
  reverse the direction.

| # | quantity | prediction (range) | basis |
|---|---|---|---|
| B1 | F-N new 1,000: directional | 6 (1 to 15): TP 3 (0 to 9), PT 3 (0 to 8) | A3 F-N 1/188; time words spaCy misses ("then", "when", "now") |
| B2 | F-N new 1,000: PAR | 45 (25 to 70) | 8/188 |
| B3 | R-N new 1,000: directional | 1 (0 to 4); PAR 5 (0 to 20) | 0/45; no predicate with two adjuncts |
| B4 | s | 0.78 (0.68 to 0.86) | F-N's single heavy PT drops from weight 48 to 7.6 |
| B5 | 95% interval width | 0.22 (0.14 to 0.32) | A3 width 0.332 came mainly from the F-N PT |
| B6 | kappa on A3b items | 0.60 (0.35 to 0.80); raw agreement 0.96 (0.93 to 0.99) | mostly NA; NA vs PAR was A3's main disagreement |
| B7 | decision | SUPPORTS_DIRECTION 65%, AGAINST_STRONG_THRESHOLD 15%, SUPPORTS_STRONG 10%, INCONCLUSIVE 10% | |
| B8 | T recall | TP 0.93 (0.85 to 0.98); PT 0.80 (0.55 to 0.95) | removing the weight-48 PT from F-N |

## Limits stated now

Model coders only (the class's human codes are separate). A3b does not change F-T, R-T or C; their sampling
error stays. The cells are still defined by spaCy's entity tagger and the v1 frame; A3b measures what that screen
misses inside EWT+GUM, not in English at large.
