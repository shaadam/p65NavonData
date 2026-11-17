# p65 Arm A: model-coded results, scored against the registered predictions (2026-11-13)

Registered plan: `p65_arm-a_predictions_2026-11-13.md` (committed before any label). This file reports the run.

## What was done

1. The stopped coders' partial output (`arm-a-model/_aborted-unread_2026-11-13/`) was moved out of the project unread (auto mode refused deletion; it now sits in a session scratch folder, to be deleted).
2. Two blind coders, Opus (coder 1) and Sonnet (coder 2), each in a fresh context, coded all 500 items in `arm-a-model/p65_model-items_blind.tsv` from codebook v2 section 2 alone (no map, no predictions, no protocol). Outputs: `arm-a-model/p65_model-codes_coder{1,2}.tsv`, both format-checked (500 rows, valid classes).
3. The 56 disagreements were adjudicated by Claude (main session) from the codebook, blind to group: the map was never opened; the sheet showed only sentence, previous sentence and the two codes. `arm-a-model/p65_model-adjudication.tsv` (item, class, reason). One rule was applied consistently: when a sentence asserts a time value and place picks which instance ("the last ballot there was cast at 2:30"), it is PT, as in the codebook anchor "In Spain dinner is at ten", even if the time belongs to an event.
4. `scripts/p65_navon_arm_a_analyze.py` (unchanged since registration) was run with `--adj`. Full output: `arm-a-model/p65_model-results_2026-11-13.txt`.

## Result

- Agreement: raw 0.888, Cohen's kappa 0.789 (95% 0.739 to 0.838). Usable (bar 0.60). By group: C 0.713, F 0.721, R all NA.
- Final labels: candidates C (200): TP 39, PT 7, PAR 102, AMB 4, NA 48. Frame F (250): TP 3, PT 1, PAR 31, NA 215. Rest R (50): all NA.
- Directional sentences: 50 (TP 42, PT 8), above the 30-sentence floor.
- Expansion to the eligible EWT+GUM pool: TP 180, PT 54.
- Share s = 0.769, 95% document-cluster interval 0.364 to 0.984. Candidate-only share 0.848 (39 TP, 7 PT).
- Screen recall: TP 0.22, PT 0.13; ratio interval 0.12 to 12.6, so equal-recall cannot be rejected (the interval is wide).
- **Decision (protocol v2 sec. 5): INCONCLUSIVE.** The point estimate leans towards time holding place (about 3 to 1), but the interval crosses 0.5. Almost all the width comes from the frame group: 4 directional sentences there, each standing for about 47 in the pool, and one PT among them.

## Predictions scored

| # | predicted | observed | score |
|---|---|---|---|
| P1 | candidates: NA 45% (35-55), PAR 38% (28-48), TP 10% (5-16), AMB 5% (2-9), PT 2% (0-5) | NA 24%, PAR 51%, TP 19.5%, AMB 2%, PT 3.5% | MISS (3 of 5 outside range: fewer NA, more PAR and TP than expected; AMB and PT hit) |
| P2 | about 30 directional (TP ~25, PT ~5) | 50 (TP 42, PT 8) | MISS on count (ratio close: 5.3 to 1 predicted, 5.25 to 1 observed) |
| P3 | s mean 0.85, 80% range 0.70 to 0.95 | 0.769 | HIT |
| P4 | TP recall about 0.1; PT recall UNKNOWN with p 0.6 | TP 0.22; PT 0.13 (one PT in the frame, so not unknown) | MISS (TP recall twice the guess; the 0.6 bet on UNKNOWN lost) |
| P5 | kappa 0.55 to 0.75; most disagreements TP vs PAR | 0.789; most disagreements NA vs PAR (28 of 56), TP vs PAR only 7 | MISS on both parts |
| P6 | INSUFFICIENT 45%, SUPPORTS_DIRECTION 25%, INCONCLUSIVE 13% ... | INCONCLUSIVE | outcome given 13%; modal guess wrong |

What the misses say: the codebook is easier for model coders than expected (kappa above range), and the hard line is whether a sentence has a literal time-place pairing at all (NA vs PAR), not the state/event line. The word screen finds more directional sentences than guessed, but the frame still holds most of them in the population (expansion: 141 of 180 TP, 47 of 54 PT).

## Pivot (registered row: "INCONCLUSIVE with 30 or more directional -> report it; size the Gutenberg study from the observed rates")

Observed rates for sizing: directional sentences are 23% of candidates (46/200) but 1.6% of the frame (4/250), and the frame carries 80% of the estimated population. The interval is set by the frame count. To give the frame about 100 directional sentences at 1.6% needs about 6,000 coded frame sentences, which is affordable with model coders but wasteful. The registered pivot's own fix is better: find candidates by named-entity type (DATE/TIME together with GPE/LOC/FAC, spaCy) instead of the word list, so the screen's recall rises and the frame's share of the estimate falls. Next steps, to be registered before any coding:

1. Run the entity screen on EWT+GUM first and measure its recall against the 50 labelled directional sentences here (a free check before scaling).
2. Then Project Gutenberg fiction plus English Wikipedia, 1,000 entity-screened candidates plus a frame sample sized from step 1, same codebook, two model coders, same script.
3. The class's human codes on 300 of these items still measure human-model agreement, and the timed task (P7, P8) still runs.

Kappa is above 0.60, so the result is not labelled exploratory.
