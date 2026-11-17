# p65 Arm A3b: F-N and R-N tightened, scored against the registration (2026-11-13)

Registration: `p65_arm-a3b_registration_2026-11-13.md`, saved to disk (SHA-256 eaebfa2c...5ab6, 18:44) before
the draw. No git commands were run in this session, so nothing is committed yet. Full output:
`arm-a3b-model/p65_a3b-results_2026-11-13.txt`. Run log with hashes: `arm-a3b-model/p65_a3b-run-log.txt`.

## What was done
- Draw: 1,000 from F-N (uncoded eligible pool 8,864) and 1,000 from R-N (pool 16,972), seed 20261115. None of
  them had been coded in Arm A or A3. Shuffled, Z0001 to Z2000, 4 batches of 500.
- Coding as in A3: Opus (coder 1) and Sonnet (coder 2) in fresh contexts, each with codebook v2 sec. 2 only, one
  run per batch. All 8 outputs checked: 500 rows, same order, valid classes. One Sonnet run tried a Bash command;
  it was denied and the file was written with Write.
- 63 disagreements went to a blind Opus adjudicator (sheet with code_A/code_B, no cell, A3's PT consistency
  rule). Result: TP 8, PT 2, PAR 28, AMB 2, NA 23. The adjudicator added rules of its own that the codebook leaves
  open: frequency words ("always", "never") are not literal time, and "when/while" clauses are.
- Registered script `arm-a3b-model/p65_navon_arm_a3b_analyze.py` (smoke-tested on synthetic codes before coding).

## Result
| | A3 | A3b |
|---|---|---|
| F-N coded (TP / PT) | 188 (0 / 1) | 1,188 (13 / 1) |
| R-N coded (TP / PT) | 45 (0 / 0) | 1,045 (3 / 2) |
| expansion TP / PT | 285 / 101 | 433 / 93 |
| **s, 95% interval** | 0.738 (0.561 to 0.893) | **0.823 (0.728 to 0.906)** |
| interval width | 0.332 | 0.179 |
| decision | SUPPORTS_DIRECTION | SUPPORTS_DIRECTION, **EXPLORATORY** (kappa < 0.60) |

- **Agreement:** raw 0.969, but kappa 0.576 (0.479 to 0.665): below the 0.60 bar, so the protocol labels this result
  exploratory. Kappa is low because almost every item is NA. F-N kappa is 0.61. R-N kappa is 0.30, from 15
  non-NA calls. The main confusion is coder 1 PAR versus coder 2 NA (38 items).
- **Per-stratum bounds (Clopper-Pearson 95%, as sentences in the cell):** F-N TP 53 to 169 (point 99). F-N PT 0
  to 42 (8). R-N TP 10 to 142 (49). R-N PT 4 to 117 (33). Before A3b, R-N's 3/45 bound allowed about 1,100. Now
  neither cell's PT bound can come close to the 433 estimated TP. **The unsampled-zero problem is closed.** No
  remainder these cells could plausibly hold reverses the direction.
- **Bracket from these two cells** (TP at the lower bound and PT at the upper, then the reverse): s 0.62 to 0.91.
  Even at the worst case for these cells, s stays above 0.5.
- **What changed:** F-N turned out to hold place-restricted-by-time (TP) sentences the DATE/TIME tagger misses
  ("currently at sea", "now at relatives in Amiriya", "here all the time"). These moved s up. The heavy F-N
  place-over-time sentence now carries weight 7.6, not 48. T-screen recall fell to TP 0.64 and PT 0.56: the
  entity screen misses about a third of time-over-place statements, mostly ones with deictic time ("now",
  "currently").
- **Unregistered robustness check** (`arm-a3b-model/p65_a3b-robustness-agreed-only.txt`): count A3b directional
  codes only when both coders agreed (adjudicated TP/PT set to NA). This gives s 0.854 (0.785 to 0.915), the same
  label. So the result does not rest on the adjudicator's calls. Some single directional codes look loose (Z0445
  "What are the dates of Aberdeen?" as PT; Z1170 as TP). The agreed-only run removes those.

## Predictions scored
| # | predicted | observed | score |
|---|---|---|---|
| B1 | F-N directional 6 (1-15): TP 3 (0-9), PT 3 (0-8) | 13: TP 13, PT 0 | total HIT; TP MISS (high); PT HIT |
| B2 | F-N PAR 45 (25-70) | 56 | HIT |
| B3 | R-N directional 1 (0-4); PAR 5 (0-20) | 5 (TP 3, PT 2); PAR 7 | directional MISS (one over); PAR HIT |
| B4 | s 0.78 (0.68-0.86) | 0.823 | HIT |
| B5 | width 0.22 (0.14-0.32) | 0.179 | HIT |
| B6 | kappa 0.60 (0.35-0.80); raw 0.96 (0.93-0.99) | 0.576; 0.969 | HIT (but below the 0.60 bar) |
| B7 | SUPPORTS_DIRECTION 65% | SUPPORTS_DIRECTION | modal outcome |
| B8 | T recall TP 0.93 (0.85-0.98); PT 0.80 (0.55-0.95) | TP 0.64; PT 0.56 | TP MISS (low); PT HIT (edge) |

## What this means for the claim
In the registration's terms, the A3 claim **holds and moves toward Navon's strong rate**. The direction (time
restricts place more often than the reverse, about 4.7 to 1) is now secure against the unseen strata. The interval
halved and its lower bound rose from 0.56 to 0.73. It still includes values both below and above 0.80, so the strong
rate is neither shown nor excluded. Two caveats keep this a pilot-strength result. First, kappa on these mostly-NA
items is below the registered bar, so the label is exploratory. Second, all coding is by models; the class's human
codes are still to come. Next steps: a codebook v3 note on frequency adverbs and deictic "now/here" (where coders split), and an
entity screen that adds deictic time words, since the DATE/TIME screen misses a third of TP.
