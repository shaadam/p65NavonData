# p65 Arm A2: entity-based screen, registration before any screen is computed (2026-11-13)

Registered pivot step 1 of `p65_arm-a_model-results_2026-11-13.md`: the v1 word list found the directional
sentences poorly (recall TP 0.22, PT 0.13), so the share's interval was set by the frame. Question: does a
named-entity screen find the directional sentences the word list missed? This file is committed and pushed
before spaCy is installed and before any screen is run on any sentence.

What was known when this was written: the 50 final directional sentences (TP 42, PT 8) split as candidates C 46
(EWT TP 21 PT 3, GUM TP 18 PT 4) and frame F 4 (GUM TP 2, EWT TP 1, EWT PT 1). So 24 are in GUM (TP 20, PT 4)
and 26 in EWT. The sentences themselves were not re-read for this registration.

## Screens

- **S1 (spaCy, both treebanks):** `en_core_web_sm` run on the sentence text (the UD `# text` line, one sentence
  at a time). Flag if the sentence has at least one DATE or TIME entity AND at least one GPE, LOC or FAC entity.
- **S2 (GUM only, gold):** GUM's own entity annotation (the `Entity=` field in MISC of the r2.18 CoNLL-U).
  Flag if the sentence contains a mention of entity type `time` AND a mention of type `place`.
- **S3 (GUM only):** S1 OR S2.

S1 is the screen that can transfer to unannotated text (Gutenberg, Wikipedia), so **the decision rule below
is applied to S1 on all 50**. S2 and S3 are measured on the 24 GUM directional sentences and say how much a
better entity detector would gain; they do not decide.

## Measures

- Recall = flagged directional / all directional, on the 50 (S1) and on the 24 GUM (S1, S2, S3), also TP and PT
  separately. Wilson 95% intervals.
- Secondary (reported, not deciding): recall weighted as in the expansion (C weight 1, F weight 11,748/250 =
  47.0), because the 46 candidate sentences were found by the word list and are not a random draw of all
  directional sentences; the 4 frame sentences stand for about 188.
- Flagged share: flagged sentences / 29,975 (S1), and flagged / GUM sentences (S2, S3).
- Controls: (a) DATE/TIME entity alone (S1 without the place half), with its recall and flag rate; (b) a
  random screen with S1's flag rate, 10,000 draws, seed 20261114: mean recall and 95% range. S1 is better than
  chance only if its recall is above the random screen's 97.5th percentile. Same random check for S2 at S2's
  rate on GUM.

## Predictions

| screen | recall on directional (range) | TP | PT | flagged share |
|---|---|---|---|---|
| S1, all 50 | 0.26 (0.14 to 0.40) | 0.24 | 0.38 (0.10 to 0.70; n = 8) | 6% of 29,975 (3 to 10%) |
| S1, GUM 24 | 0.25 (0.10 to 0.45) | | | |
| S2, GUM 24 | 0.70 (0.45 to 0.90) | | | 12% of GUM sentences (6 to 20%) |
| S3, GUM 24 | 0.75 (0.50 to 0.92) | | | 15% of GUM sentences (8 to 24%) |
| control DATE/TIME alone, all 50 | 0.55 (0.35 to 0.75) | | | 20% (12 to 30%) |
| random at S1's rate | equals S1's rate, about 0.06 | | | |

Why S1 is expected to fail: 46 of the 50 were found by the word list, whose place words (here, there, home,
room, office, park ...) are common nouns and deictic adverbs, which spaCy's small model does not tag as
GPE/LOC/FAC. Directional sentences tend to use deictic place ("by six the children were home"), not proper
names. GUM's gold entities cover common nouns and (we expect) some deictic adverbs, hence the higher guess for
S2. Probability S1 meets the rule: 0.10.

## Decision rule (S1, all 50)

- Recall >= 0.60 AND Wilson 95% lower bound >= 0.45: **entity screen adequate, proceed to an Arm A2 coding
  sample** (sampling plan and blind item file only; no coding in this step).
- Otherwise: **report and stop**. The results file then says which part failed (TP, PT, or both) and whether
  S2/S3 show that gold-quality entities would have passed, which bears on whether a better detector is worth
  trying. Any such follow-up is a new registration.

## Data and code

UD_English-EWT and UD_English-GUM at tag r2.18 from GitHub (URL, tag and sha256 of each file recorded in the
results). Must reproduce 29,975 sentences and the v1 control counts (test splits EWT 9, GUM 10). Script:
`scripts/p65_navon_arm_a2_entity_screen.py`. spaCy in a venv under $TMPDIR; if it cannot be installed, S2 only,
said plainly.
