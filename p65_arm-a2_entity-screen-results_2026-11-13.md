# p65 Arm A2 step 1: entity-screen recall, results (2026-11-13)

Registration: `p65_arm-a2_entity-screen-registration_2026-11-13.md`, commit 4a2de35, pushed before spaCy was
installed or any screen run. Script: `scripts/p65_navon_arm_a2_entity_screen.py`. Full output (every number
below, plus each of the 50 directional sentences with its flags): `arm-a2-model/p65_a2-entity-screen-run_2026-11-13.txt`.

## Decision: REPORT AND STOP

S1 (spaCy DATE/TIME with GPE/LOC/FAC) found 12 of the 50 directional sentences: recall 0.24, 95% interval 0.14
to 0.37. The rule needed 0.60 with a lower bound of 0.45. No Arm A2 coding sample was built. The entity screen
as registered does not fix the frame problem that made Arm A inconclusive.

## Data checks

- UD_English-EWT and UD_English-GUM, tag r2.18 (exists), files from
  `https://raw.githubusercontent.com/UniversalDependencies/UD_English-{EWT,GUM}/r2.18/en_{ewt,gum}-ud-{train,dev,test}.conllu`.
  SHA-256: EWT train d68e0612...2143, dev 39239e0a...90f8, test fa024f43...494a; GUM train 88c410ca...0329, dev 61d02ce2...7910, test cd96a285...0b69. Both test hashes equal the W02 manifest.
- v1 control (protocol v2 sec. 4.3): test splits EWT 9, GUM 10, MATCH.
- **Sentence total is 30,975, not 29,975.** EWT 16,622 + GUM 14,353. The v1 groups reproduce exactly (C 200, F
  12,067, R 18,708), and those sum to 30,975, so the "29,975" in protocol v2 sec. 4 and in the predictions file
  is an arithmetic slip, not a data difference. It changes no Arm A estimate (the analysis used the group pools).
- spaCy 3.8.18, `en_core_web_sm` 3.8.0, in a Python 3.12 venv under $TMPDIR (the default Python 3.8 could not
  build spaCy's dependencies; pip needed `--use-deprecated=legacy-certs` inside the sandbox). Run twice, cache
  cleared: identical output.

## Results

Recall is the share of the labelled directional sentences the screen flags (Wilson 95% interval). "Weighted"
counts each frame sentence as the 47 pool sentences it stands for, as the Arm A expansion did.

| screen | scope | recall all | TP | PT | weighted | flagged share |
|---|---|---|---|---|---|---|
| S1 | all 50 | **0.24 (0.14-0.37)** | 0.24 (10/42; 0.14-0.39) | 0.25 (2/8; 0.07-0.59) | 0.44 | 3.4% of 30,975 (1,057) |
| S1 | GUM 24 | 0.33 (0.18-0.53) | 0.30 | 0.50 (2/4) | 0.47 | 3.6% of GUM |
| S2 (GUM gold time+place) | GUM 24 | 0.75 (0.55-0.88) | 0.75 | 0.75 (3/4) | 0.55 | 6.5% of GUM (936); 3.0% of all |
| S3 (S1 or S2) | GUM 24 | 0.83 (0.64-0.93) | 0.85 | 0.75 | 0.57 | 7.4% of GUM (1,059) |
| control: DATE/TIME alone | all 50 | 0.80 (0.67-0.89) | 0.81 | 0.75 | 0.76 | 14.6% of all (4,525) |

What each number means for the claim:

- **S1 0.24.** spaCy's place labels miss most directional sentences, so a Gutenberg/Wikipedia study screened
  this way would again leave most directional sentences in an unscreened frame, and the share's interval would
  again be set by a handful of frame hits. S1 does not unblock the test of Navon's direction.
- **Where S1 fails is the place half.** Of the 38 sentences S1 misses, 28 have a DATE/TIME entity; the place is
  "here", "there", "home", "in the office", "in there" (deictic or common-noun places, which spaCy does not tag).
  The prediction (0.26, range 0.14-0.40) was right, and for that reason.
- **S2 0.75 and S3 0.83 on GUM.** Gold entity annotation that marks common-noun and deictic places would reach
  the bar on recall (S3's lower bound 0.64 clears 0.45), at a flag rate of about 7%. This says a screen of the
  right kind can work; it does not say an automatic one does, because gold GUM entities exist only for GUM.
  Predictions: S2 0.70 (hit), S3 0.75 (hit, observed slightly above).
- **PT recall** is 0.25 (S1) on 8 sentences; the interval (0.07-0.59) is too wide to say the screen favours
  one direction. Whether S1 is equal-recall across TP and PT cannot be decided at n = 8.
- **Flagged shares** were all below prediction: S1 3.4% (predicted 6%, range 3-10%, low end), S2 6.5% of GUM
  (predicted 12%, out of range), DATE/TIME alone 14.6% (predicted 20%, out of range).

## Controls

- **Random screen at the same flag count** (10,000 draws, seed 20261114): S1's rate gives mean recall 0.034,
  97.5th percentile 0.10. S1's 0.24 is above it, so S1 picks out directional sentences about 7 times better
  than chance; its failure is coverage, not selection. S2 at its rate: random 0.065 (97.5th 0.17) vs 0.75,
  about 11 times chance. So the recall differences between screens are not an artefact of flag rate.
- **DATE/TIME alone** reaches 0.80 at a 14.6% flag rate (random at that rate: 0.146, 97.5th 0.26) and flags
  3 of the 4 frame directional sentences. It is not a screen that fails: it shows the time half carries the
  recall and the place half removes it. It was registered as a control, not a screen, so it does not change the
  decision.
- Bias of the test set: 46 of the 50 were found by the v1 word list, so recall here is measured mostly on
  word-list-type sentences. The weighted column corrects for that only through 4 frame sentences, and is noisy.

## Not done

- No Arm A2 sampling plan or blind item file: the decision rule said stop.
- Any follow-up screen (for example DATE/TIME entity plus a deictic and common-noun place list, or a better
  entity model that tags common-noun places) is a new registration, not part of this one.
