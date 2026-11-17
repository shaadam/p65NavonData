# p65 Arm A3: re-stratified corpus estimate, scored against the registration (2026-11-13)

Registration: `p65_arm-a3_registration_2026-11-13.md` (a81a309, before any draw). Items d35b9a8. Codes 28ebda0.
Full output: `arm-a3-model/p65_a3-results_2026-11-13.txt`.

## What was done
1,500 new sentences (F-T 943, R-T 557: sentences with a DATE or TIME entity that Arm A had not coded) coded blind by
two model coders (Opus, coder 1; Sonnet, coder 2), each in three 500-item batches with only the codebook. Each
output file was checked to hold exactly its batch's items in order. 176 disagreements went to a blind Opus
adjudicator (codebook, sentence, two codes; no cell, no coder identity; Arm A's consistency rule for PT).
Registered script `scripts/p65_navon_arm_a3_analyze.py` combined these with Arm A's 500 final labels over six cells.

## Result
- Agreement 0.883 raw, kappa 0.676 (0.632 to 0.719): usable (bar 0.60), lower than Arm A's 0.79. 100 of 176
  disagreements were NA vs PAR (does the sentence pair a literal time with a literal place at all).
- 155 directional sentences in all (105 new: TP 88, PT 17).
- Share s = 0.738, 95% document-bootstrap interval 0.561 to 0.893. **Decision: SUPPORTS_DIRECTION** (lower bound
  above 0.5; strong 0.80 rate neither shown nor excluded). Statements of place restricted by time outnumber the
  reverse by about 2.8 to 1 in this corpus.
- DATE/TIME screen recall: TP 0.97, PT 0.51 (0.21 to 1.00). The PT figure rests on the one F-N place-over-time
  sentence at weight 48.

## Predictions scored
| # | predicted | observed | score |
|---|---|---|---|
| Q1 directional among 1,500 | 55 (25-90) | 105 | MISS (high) |
| Q2 PT among them | 8 (2-18) | 17 | HIT (top of range) |
| Q3 s | 0.80 (0.65-0.92) | 0.738 | HIT |
| Q4 interval width | 0.35 (0.20-0.55) | 0.332 | HIT |
| Q5 kappa | 0.78 (0.68-0.86) | 0.676 | MISS (just below) |
| Q6 T recall | TP 0.75 (0.55-0.90); PT 0.55 (0.20-0.85) | TP 0.97; PT 0.51 | TP MISS (high), PT HIT |
| Q7 decision | SUPPORTS_DIRECTION 35% | SUPPORTS_DIRECTION | second most likely outcome |

## Limits the interval does not carry
1. **Unsampled zeros.** R-N (17,017 sentences, no DATE/TIME entity, no multi-modifier predicate) has 45 coded, all NA,
   weight 378. Its rule-of-three bound allows up to about 6.7% directional, which would swamp everything else; the
   bootstrap cannot see this. The registration assumed R-N is near empty; the 45 support that but cannot bound it
   tightly. F-N (9,052) has one PT and zero TP in 188.
2. **Single heavy sentence.** The F-N place-over-time sentence stands for about 48 of the 101 estimated PT. Without
   it s would be about 0.85; with a second such sentence, about 0.66. The direction holds either way; the strength
   does not.
3. **Model coders only;** the human (class) coding of 300 items is still to come. Kappa fell from 0.79 to 0.68 on
   this harder, mostly-frame sample.

## Next (not registered yet)
- Tighten F-N and R-N: a random draw of about 1,000 from each, coded the same way, bounds the unseen-zero problem.
- Formal-model predictions F2/F3 need other dimension pairs (place-colour, time-colour) coded in text.
