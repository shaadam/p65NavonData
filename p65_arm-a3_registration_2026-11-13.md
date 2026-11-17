# p65 Arm A3: re-stratified estimate with the DATE/TIME-entity screen, registration (2026-11-13)

Adam chose option A after Arm A2 step 1 (`p65_arm-a2_entity-screen-results_2026-11-13.md`). This file is
committed and pushed before any new item is drawn. No A3 item has been drawn, coded or read.

## Why

Arm A was INCONCLUSIVE (s = 0.769, 95% 0.364 to 0.984) because the frame F held most directional sentences
but only 4 were coded there, each standing for about 47. The DATE/TIME-entity flag (T) found 40 of the 50
directional sentences (0.80) while flagging 14.6% of the corpus, and 3 of the 4 frame ones. Stratifying on T
puts most of the coding effort where directional sentences are.

**Caveat, stated plainly:** T's recall of 0.80 was measured on the same 50 sentences, as a control registered
in A2 (commit 4a2de35), not designed from them. It was not tuned on them, but it was chosen after seeing that
it did well on them, so 0.80 is an optimistic estimate of T's recall. A3 estimates T's recall again from the
new design (below); that estimate is the one to cite.

## Corpus

UD English EWT + GUM r2.18, train+dev+test: **30,975 sentences** (EWT 16,622, GUM 14,353). The "29,975" in
protocol v2 sec. 4 was an arithmetic slip; the groups C 200, F 12,067, R 18,708 are unchanged.
T = spaCy 3.8.18 `en_core_web_sm` 3.8.0 finds at least one DATE or TIME entity in the sentence text
(same run as A2, `scripts/p65_navon_arm_a2_entity_screen.py`).

## Design: 6 cells = Arm A groups x T

Population = eligible sentences (protocol v2 sec. 4.4: at most 60 tokens, content list), as in Arm A; C is
taken whole (200, all coded in Arm A, weight 1, as before).

| cell | all sentences | eligible (population) | coded in Arm A | uncoded eligible | new draw | coded after A3 |
|---|---|---|---|---|---|---|
| C-T | 151 | (whole, 151) | 151 | 0 | 0 | 151 |
| C-N | 49 | (whole, 49) | 49 | 0 | 0 | 49 |
| F-T | 2,801 | 2,696 | 62 | 2,634 | **943** | 1,005 |
| F-N | 9,266 | 9,052 | 188 | 8,864 | 0 | 188 |
| R-T | 1,573 | 1,561 | 5 | 1,556 | **557** | 562 |
| R-N | 17,135 | 17,017 | 45 | 16,972 | 0 | 45 |

New draw: 1,500 sentences, uniform without replacement within F-T and R-T from the uncoded eligible sentences,
allocated in proportion to those cells' uncoded eligible sizes (2,634 : 1,556 -> 943 : 557). Seed 20261114.
Arm A's items keep their final labels and sit in the cell their T flag puts them in; because Arm A drew F and
R uniformly, its items in each sub-cell are a uniform sample of that sub-cell.

## Coding

Same as Arm A: codebook v2 sec. 2 only, two blind model coders (Opus, Sonnet) in fresh contexts, 3 batches of
500, item file shuffled with no cell shown; disagreements adjudicated blind to cell from the codebook.

## Estimator and decision

- Expansion: N_d = sum over the 6 cells of (cell population / coded in cell) x (final codes d in cell).
- s = N_TP / (N_TP + N_PT). 95% interval: document bootstrap within cells, 10,000 resamples, seed 20261114.
- Agreement: Cohen's kappa on the 1,500 A3 items, bootstrap 95% interval. Below 0.60 -> exploratory.
- Minimum count, zero-count rule and decision labels exactly as protocol v2 sec. 5 (count over all 2,000 coded
  items; SUPPORTS_STRONG / SUPPORTS_DIRECTION / AGAINST_STRONG_THRESHOLD / INCONCLUSIVE / AGAINST_DIRECTION by
  L and U against 0.50 and 0.80).
- T recall per direction: N_d(T cells) / N_d, with its bootstrap interval.
- Script: `scripts/p65_navon_arm_a3_analyze.py`, committed before any A3 code exists, smoke-tested on
  synthetic codes only.

Known weak point: F-N keeps 188 coded items at weight 48 and holds Arm A's one frame PT (Arm A item M478,
no DATE/TIME entity). That single item contributes about 48 to N_PT, so the interval will stay wide on the PT
side unless F-T adds many PT. This design does not fix that; it is stated now so it is not a surprise later.

## Predictions

| # | quantity | prediction (range) | basis |
|---|---|---|---|
| Q1 | directional (TP+PT) among the 1,500 new items | 55 (25 to 90); F-T about 49 (5%), R-T about 6 (1%) | Arm A frame rate 1.6%, 3 of 4 frame hits had T, F-T is 23% of F |
| Q2 | PT among those | 8 (2 to 18) | Arm A ratio about 1 PT to 5 TP |
| Q3 | s | 0.80 (0.65 to 0.92) | Arm A 0.77; frame TP gets better measured |
| Q4 | 95% interval width of s | 0.35 (0.20 to 0.55) | F-N's single PT at weight 48 keeps it wide |
| Q5 | kappa on A3 items | 0.78 (0.68 to 0.86) | Arm A 0.79 overall, frame 0.72; A3 items are mostly NA vs PAR calls |
| Q6 | T recall (re-estimated) | TP 0.75 (0.55 to 0.90), PT 0.55 (0.20 to 0.85) | F-N's PT weighs against T on PT |
| Q7 | decision | INCONCLUSIVE 45%, SUPPORTS_DIRECTION 35%, SUPPORTS_STRONG 8%, AGAINST_STRONG_THRESHOLD 7%, AGAINST_DIRECTION 2%, INSUFFICIENT 3% | |
