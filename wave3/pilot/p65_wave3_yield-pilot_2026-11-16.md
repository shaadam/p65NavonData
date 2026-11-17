# p65 wave 3: direction-blind yield pilot (unit 2, 2026-11-16)

Last updated: 2026-11-16 (Eastern)

Script `scripts/p65_wave3_yield_pilot.py` (seed 20261130, 500 sentences per language, UD r2.18 from
`scripts/p65_wave3_ud_fetch.py`). Full output: `wave3/pilot/p65_wave3_yield-pilot-run_2026-11-16.txt`. Draws (sentence
IDs and presence flags only, no text): `wave3/pilot/p65_wave3_yield-draw_<language>.tsv`. **Presence only. No
direction was read, guessed or counted for any language.**

## In plain language

A screen built from the treebanks' own annotation finds sentences that hold both a time and a place expression. On
English, where two blind model coders and an adjudicator coded 4,000 sentences in Arm A, A3 and A3b, it catches **70% of the
time-over-place and place-over-time sentences** (95% interval 59% to 80%). The earlier entity screen caught 24%. Run on
each language, it says **six of the eight recommended languages should reach the 100 directional items Appendix D asks
for if the whole treebank is coded; Mandarin (about 65) and Naija (about 74) fall short.** These numbers carry English's
precision over to every other language, so each is an expectation with roughly a factor-of-two band, not a count.

## English validation (the screen against Arm A's codes)

Truth: final protocol v2 class of the 4,000 Arm A + A3 + A3b sentences (agreed code, else adjudicated). "Both present"
= any class but NA; "directional" = TP or PT. Weighted by the A3b cell weights; the weights sum to 30,526, the eligible
population, as they must. Intervals: 2,000 bootstrap resamples within cells.

| screen | flags (share of English) | recall, both present | precision, both present | recall, directional | of which TP / PT | directional share of flagged |
|---|---|---|---|---|---|---|
| time + BROAD place | 0.120 | 0.698 (0.646-0.748) | 0.393 (0.357-0.429) | **0.698 (0.592-0.795)** | 0.769 / 0.366 | 0.100 (0.079-0.123) |
| time + NARROW place | 0.073 | 0.545 | 0.500 | 0.510 (0.414-0.614) | 0.544 / 0.355 | 0.120 |

- **Positive control.** Applied to the English census, the broad screen implies 376 directional items among flagged
  sentences; divided by its recall that is **539**, against the **526** Arm A3b measured.
- **Time is not the bottleneck.** Only 5 of 173 directional coded items lacked a time flag; place carries the misses.
- **The screen recalls time-over-place about twice as well as place-over-time (0.77 against 0.37; the PT interval is
  0.18 to 0.67, from 27 PT items).** A draw restricted to flagged sentences would therefore inflate the time-over-place
  share. This decides the wave 3 design: **code a census, or a flagged draw plus a uniform frame that measures recall
  per direction (the A3b design); never a flagged draw alone.**

## Yield per language against the 100-item requirement

D = N x r x 0.100 (English directional share of flagged). "Total" = D / 0.698, the expected directional items if the
whole treebank is coded. The feasibility note's English-rate expectation (by sentence / by token) is given for
comparison. Draw r carries a Wilson 95% interval.

| language | verdict (feasibility) | sentences | draw: flagged of 500 | census r | expected in flagged sentences | **expected total (census coding)** | feasibility expectation | vs 100 |
|---|---|---|---|---|---|---|---|---|
| Hindi | FEASIBLE | 16,649 | 107 (0.18-0.25) | 0.222 | 371 | **532** | 283 / 362 | clears |
| Persian (reserve) | FEASIBLE | 29,107 | 42 (0.06-0.11) | 0.087 | 254 | **365** | 494 / 516 | clears |
| Arabic | MARGINAL | 7,664 | 150 (0.26-0.34) | 0.322 | 248 | **355** | 130 / 290 | clears, but see caution 2 |
| Korean (reserve) | FEASIBLE | 27,363 | 23 (0.03-0.07) | 0.058 | 160 | **229** | 465 / 360 | clears |
| Finnish | FEASIBLE | 15,136 | 50 (0.08-0.13) | 0.103 | 157 | **225** | 257 / 208 | clears |
| Indonesian | MARGINAL | 6,628 | 86 (0.14-0.21) | 0.171 | 114 | **164** | 113 / 155 | clears |
| Turkish (BOUN) | MARGINAL | 9,761 | 54 (0.08-0.14) | 0.114 | 111 | **160** | 166 / 129 | clears |
| Turkish (Kenet, fallback) | | 18,687 | 20 (0.03-0.06) | 0.050 | 94 | 135 | | adds 135 |
| Japanese | MARGINAL | 8,100 | 54 (0.08-0.14) | 0.109 | 88 | **127** | 138 / 199 | marginal |
| Naija | MARGINAL | 9,241 | 38 (0.06-0.10) | 0.056 | 52 | **74** | 157 / 145 | **short** |
| Mandarin (GSD + HK) | MARGINAL | 6,001 | 34 (0.05-0.09) | 0.075 | 45 | **65** | 102 / 137 | **short** |
| English (check) | | 30,975 | 67 (0.11-0.17) | 0.121 | 376 | 539 | 526 measured | |

Secondary, unvalidated: sentences with both a time expression and a count numeral (time-quantity) run from 1.1%
(Naija) to 19.7% (Mandarin, where 年 / 月 / 日 dates are numerals) of each treebank; see the run file.

## Cautions

1. **Precision is borrowed from English.** No other language has coded sentences, so the 0.100 directional share of
   flagged sentences is assumed to transfer. Each language's screen is a different instrument (its own adpositions,
   cases and lexicon). The cheapest decisive step is unchanged: model-code each language's 500-sentence draw, already
   fixed in the draw files, and replace 0.100 with the measured share.
2. **Arabic flags 32% of sentences**, because في ("in") marks abstract as well as spatial phrases and PADT sentences
   average 37 tokens. Its precision is probably below English's, so 355 is likely high.
3. **Mandarin's place screen is weak**: the narrow screen flags 1.9% (GSD tags few place names PROPN) while time flags
   43%. Its 65 may be low. No other Mandarin treebank with original text adds much (GSDSimp is the same text; PUD is
   translated).
4. **Korean's screen was repaired during this run** (verb lemmas matched time words; the locative particle 에 was
   misfiled). Its numbers rest on one pass of fixes, made before any coded Korean data exist, but they are the least
   tested.
5. **Lexicon dead entries** are listed per language in the run file (for example, simplified-script entries for
   traditional-script Mandarin); none is a common word in its treebank's script.

## Controls run

- Re-run: the 12 draw files are byte-identical (sha256 list compared).
- English weights sum to the eligible population (30,526).
- English implied total 539 against measured 526 (above).
- Bugs found by inspection, fixed before the reported run: Turkish-BOUN r2.18 ships a `finetuning` file repeating the
  7,803 training sentences (excluded: only train/dev/test files are read, so BOUN is 9,761 sentences as in the
  feasibility count); Korean, as in caution 4.

Last updated: 2026-11-16 (Eastern)
