# p65 E1 results: time/space intrusions in learner writing errors (2026-11-13)

Registration: `p65_error-evidence-registration_2026-11-13.md`, commit **0c6fcdd**, pushed before any count.
Script: `scripts/p65_error_intrusion_count.py` (unchanged since registration). Raw output:
`error-evidence/p65_e1-run_2026-11-13.txt` (counts and word pairs only; no corpus text committed).
Data: FCE v2.1 + W&I A/B/C train+dev (BEA-2019 M2, annotator 0), learner; LOCNESS N.dev, native.

## Registered result

| quantity | value | prediction | hit? |
|---|---|---|---|
| learner tokens | 1,223,992 (70,940 sentences, 123,036 edits) | 1.1 M (0.8-1.5 M) | hit |
| N_T (temporal-only terms, corrected text) | 4,356 | 2,800 (1,500-6,000) | hit |
| N_S (spatial-only terms, corrected text) | 2,376 | 3,000 (1,500-6,000) | hit |
| n(S->T), space word where time belongs | 2 | 5 (1-15) | hit |
| n(T->S), time word where space belongs | 8 | 12 (3-35) | hit |
| **p = S->T share** | **0.20 (95% 0.025-0.556), n = 10** | 0.30 (0.10-0.60) | hit |
| opportunity-normalised RR | 0.14 | - | - |
| contains-match sensitivity | 2 vs 8 (same) | - | - |
| per corpus | FCE 0 vs 5; W&I 2 vs 3 | same direction where n >= 5 | both below 0.5 |
| C1 before/after vs during/until/since | 5 vs 4, n = 9 | n 25 (8-80), p near 0.5 | n hit; below n = 10, uninformative |
| C2 vertical vs frontal | 1 vs 0, n = 1 | n 4 (0-15) | uninformative |
| D dedicated-ness | T 0.025, S 0.018 | <= 0.10 | pass |
| native intrusions (23,117 tokens) | 0 | 0 (0-2) | hit |

**Decision (registered rule): INCONCLUSIVE.** n reached the minimum of 10 exactly; the interval contains 0.5
and is too wide (0.03-0.56) to count as "no strong asymmetry". The point estimate runs AGAINST the metaphor
corollary (time words intrude into space slots, not the reverse), in both corpora, but 10 errors cannot carry
that. Both negative controls had too few cases to test anything, so the symmetric null is unchecked.

## What the 10 errors are (read after the registered count; exploratory)

Cross-domain preposition errors are very rare: 10 in 1.22 M learner tokens, about 1 per 120,000 words. That
rarity is itself the main finding: learners almost never swap a temporal-only word for a spatial-only one.
Their time/space trouble sits in the shared prepositions (in/on/at), which E1 excluded by design.

- Of the 8 T->S edits, 4 are "before" -> "above" in "the reasons I mentioned before" and "the aspects described
  before". The slot is position in the text being read, which English writing convention marks spatially
  ("above"); the learners marked it temporally (the reader met it earlier). This is a register correction, not
  a physical-space error. One more ("after all of that" -> "on top of all of that") is an idiom.
- Physical-space errors left: T->S 3 (2 sentences: "... walking through the door with the being after him" -> "behind him"; "Before me
  and after are my friends" -> "in front of ... behind"), S->T 2 ("Near the race, I was very nervous" ->
  "before"; "Along the course I had to ..." -> "during"). On these 5 the split is 2:3, no asymmetry, and the
  two S->T cases are exactly the metaphor view's kind of error (a spatial path or proximity word used for time).

## What it means for the three accounts

- **Metaphor (space-to-time) corollary:** not supported; the net direction runs the other way, but the data
  cannot reject p = 0.5. The text-deixis cases show that "before"/"above" reflect a writing convention, not a
  conceptual direction, so a larger replication must code them separately.
- **Navon:** the result fits our weak extension (time terms spread into space) only through the text-deixis
  items, which are not a test of his hierarchy. No support claimed.
- **Garner:** no prediction; unaffected.

## Cheapest route to a decisive test

At this rate about 30 physical-space cross-domain errors need roughly 7 M learner tokens. Candidates:
Lang-8 Corpus of Learner English (about 1 M sentences, free for research via the BEA-2019 request form, not
open download), NUCLE (1.2 M tokens, licence form), EFCAMDAT (about 83 M words, free registration; partial
error tags). A rerun should (1) register a text-deixis exclusion ("before/after/above/below" referring to the
text), (2) report L1 for EFCAMDAT/Lang-8 so transfer from one-word-for-both L1s (German vor, Russian pered)
can be separated from a conceptual direction.
