# P65 definitional test: ADVERSARIAL RE-TEST (2026-11-19)

Last updated: 2026-11-19 (Eastern).

Target: the definitional paragraph in Section 6.2 of `docs/manuscript/p65_navon_v1.md` ("Two blind coders marked a
pairing *definitional* when meaning or convention fixes one expression by the other ... 0.16 (0.05 to 0.46)").
Source test: branch `claude/p65-definitional-dependence-2026-11-18`, folder `definitional/` (codebook
`p65_defdep_codebook_2026-11-18.md`, commit 23f39e2; codes bfadfc0; adjudication 1bee21e; model `p65_defdep_assoc.py`,
cd20ab8; broad recount bafe36b). Read only; nothing on that branch is changed. Files for this re-test:
`definitional-adversarial/`.

## Registration (committed before any direction-blind coding)

**Step 1 result, already run (commit 72bc51f).** The registered label is directional by its rule. Question 1 asks
whether "the restricting expression" is tied to the asserted state, so the coder must first find which expression
restricts which, and that is the outcome. The TZ subtype is defined as "a clock or calendar value ... stated as
holding *at a place*", the place-over-time frame. The codebook's own examples code the same kind of pair both ways
by frame: "The train is in Boston at nine" is 0, "In Tokyo it was already midnight" is 1. No frame label was shown
(the blind file has only the two sentences), but the sentence shows the frame.

**Step 2 design.** Input: the unit 3 adversarial extraction, `dependence/adversarial/p65_depadv_extracted.tsv`
(243 rows, the same 243 items, sha256 a45427af...818a21, commit ad6ac39). Each coder sees only the time and the
place expression, in random order, with no sentence, no entity, no frame and no language label; 6 plants; rows
shuffled (seed 20261121). Brief: `definitional-adversarial/p65_defadv_coder-brief.md`. Codes: TBP (the time is fixed
by the place), PBT (the place is fixed by the time), BOTH, NEITHER. The brief carries the registered codebook's four
ties (TZ, SUN, ARR, POS) with the frame condition removed. Departure from the dispatch, in one line: the brief keeps
the original codebook's tie list so that "fixed by" means what the manuscript's "definitional" means.

**Coders.** Coder A is an Opus subagent, coder B a Sonnet subagent, each in a fresh context with only its folder.

**Plants, scored first.** 6 plants with expected codes (`p65_defadv_plants.tsv`). A coder missing 3 or more is
excluded and the verdict rests on the other coder; if both are excluded the verdict is UNRESOLVED.

**Labels.** Blind-definitional = the code is not NEITHER. Primary: both coders say so (intersection); no
adjudication. Sensitivity: union, and each coder alone. Directional cells (TBP, PBT, BOTH) reported per coder.

**Statistic.** The manuscript's own: Firth logistic regression, direction (time over place = 1) on blind-definitional
plus language, odds ratio with profile-penalised 95% interval, run by a copy of the registered script; exact
conditional common odds ratio across language as a second route. Shares: time-over-place share among
blind-non-definitional sentences, per language, exact 95% intervals. Controls: labels shuffled within language
(must remove the association); a synthetic label equal to place-over-time (must return an odds ratio near 0).

**Verdict, fixed now.**

| outcome on the primary label | verdict |
|---|---|
| Firth interval includes 1 | CIRCULAR: the association does not survive hiding the direction |
| upper bound below 1 and odds ratio at or below 0.25 (inside the manuscript's interval) | CONFIRMED |
| upper bound below 1 and odds ratio above 0.25 | PARTLY |

## Results (after coding; registration above unchanged)

### Verdict: PARTLY

- **Circularity of the registered test: certain.** The rule defines its main subtype by the outcome. The registered
  odds ratio of 0.07 reproduces exactly (copied script, 0.0723 [0.0171, 0.2454]) but measures mostly the rule.
- **Direction-blind re-test: the association survives, at about a third of its strength on the log scale.**
  Primary label, odds ratio of time over place 0.32 [0.12, 0.85], against the registered 0.07.
- **The manuscript's shares stand.** Pairings that are not definitional still put time over place in 86% of
  English and 72% of Indonesian sentences.

### Step 1. The registered label is conditioned on direction (commit 72bc51f)

The coders saw no frame label, but the rule makes them read the frame from the sentence.

- Question 1 asks whether "the restricting expression" is tied to the asserted state. Answering it needs the
  direction first.
- The TZ subtype is "a clock or calendar value ... stated as holding at a place". That phrase is the
  place-over-time frame. The codebook's own Part 2 says so ("TZ is itself a place-over-time construction").
- All 7 TZ rows are place over time. Without them, 3 of the 5 remaining definitional rows put time over place, and
  the association is not significant (exact conditional p = 0.24).
- **Null world.** Each item carries a latent convention tie at rates matched to the registered counts, independent
  of direction. The registered rule is applied as written. In 5,000 runs the registered analysis reported an odds
  ratio below 1 with p < 0.05 in **91%** (median odds ratio 0.11, median 12 definitional rows). The registered test
  is NON-DISCRIMINATING.
- **Control that could fail.** The same latent ties with a frame-blind label gave that result in 2.7% of runs
  (median odds ratio 1.01). The simulation does not manufacture the effect.
- The null world assumes the ties occur equally in both frames. Step 2 measures that assumption and finds it false:
  real ties are more common in place-over-time sentences.

### Step 2. Direction-blind re-test (commit 9afe7d4 registered; this commit codes and results)

- **Plants:** coder A (Opus) 6 of 6; coder B (Sonnet) 6 of 6. Neither coder is excluded.
- **Agreement:** kappa 0.815. Coder A marked 26 items, coder B 22, all as "time fixed by place". No real item drew
  "place fixed by time" or "both".
- **Caveat on coder B:** it reports writing its file from a list of its non-NEITHER rows, with NEITHER as the default.
  The plants still caught nothing wrong, and its counts sit within 4 of coder A's.
- **Overlap with the registered 12:** 8 of them are blind-definitional on both coders. The blind label adds 12 rows
  the registered rule left at 0: the same kind of pair (a date or weekday at a city, a season at a region) inside a
  time-over-place sentence. Examples are "Monday, September 20, 1999" with "in Sao Paulo", and "by Sunday afternoon"
  with "in Houston". This is the codebook's "train in Boston at nine" versus "Tokyo at midnight" split, made visible.

**Time-over-place share (raw counts, exact 95% intervals):**

| label | definitional | not definitional |
|---|---|---|
| primary (both coders) | 12 / 20 = 0.600 [0.361, 0.809] | 183 / 223 = 0.821 [0.764, 0.869] |
| English, primary | 9 / 14 = 0.643 | 137 / 159 = 0.862 [0.798, 0.911] |
| Indonesian, primary | 3 / 6 = 0.500 | 46 / 64 = 0.719 [0.592, 0.824] |

**Odds ratio for time over place, definitional against other pairings, adjusted for language (Firth logistic
regression, as in the manuscript; profile 95% interval):**

| label | odds ratio [95%] | exact conditional, second route |
|---|---|---|
| registered (sentence shown) | 0.072 [0.017, 0.245] | 0.066 [0.011, 0.287] |
| **blind, both coders (primary)** | **0.319 [0.124, 0.851]** | 0.323 [0.110, 0.993] |
| blind, either coder | 0.171 [0.073, 0.396] | 0.170 [0.066, 0.435] |
| blind, coder A | 0.218 [0.092, 0.518] | 0.218 [0.083, 0.575] |
| blind, coder B | 0.236 [0.094, 0.594] | 0.237 [0.084, 0.673] |

- **Controls.** Shuffling the primary label within language removed the association: median odds ratio 0.995, and
  4.1% of 2,000 shuffles had p < 0.05. A synthetic label equal to place over time returned an odds ratio of 0.0001,
  so the pipeline detects a real separation.
- **Verdict rule applied.** The primary upper bound (0.85) is below 1 and the odds ratio (0.32) is above 0.25.
  The verdict is therefore PARTLY. The sensitivity labels fall between 0.17 and 0.24, inside the registered
  interval. The primary label is the most conservative of the four.
- **The exact second route on the primary label** only just excludes 1 (upper bound 0.993, p = 0.033). The
  association is real but weak on this label.

### Verdicts

| claim in Section 6.2 | verdict | evidence |
|---|---|---|
| Registered odds ratio 0.07 [0.02, 0.25] measures definitional status | DISPROVED (non-discriminating: null world 91%) | CHECKED NUMERICALLY |
| Definitional pairings lean toward a time stated at a place | SUPPORTED, weaker: 0.32 [0.12, 0.85] | CHECKED NUMERICALLY |
| "12 of 243", "9 of 12" | frame-dependent; blind count 20 (primary), 8 of 20 place over time | CHECKED NUMERICALLY |
| Broader coding 0.16 (0.05 to 0.46) | its numbers stand, but it uses the same frame-reading rule; not independent support | not re-run |
| 87% English, 73% Indonesian with definitional status in the model | SUPPORTED: 86% and 72% on the blind label | CHECKED NUMERICALLY |
| "definitional pairings do not produce the direction" | SUPPORTED | CHECKED NUMERICALLY |
| Re-test verdict | PARTLY | |

### Consequences

Replace the two sentences from "Two blind coders marked..." through "...leaves those shares unchanged." with this
text (69 words):

> Coders shown only the two expressions marked a pairing definitional when convention or the sky fixes one by the
> other, as a time zone fixes clock time. The 20 such pairings of 243 leaned toward a time stated at a place (odds
> ratio for the reverse 0.32, 95% interval 0.12 to 0.85); other pairings stated a place at a time in 86% of English
> sentences and 72% of Indonesian.

- The closing clause of the paragraph ("so definitional pairings do not produce the direction") still follows.
- The broader-coding sentence goes. It rests on the same frame-reading rule.
- A methods note, if one is wanted: the first coding showed the sentence, so its count depended on the frame. The
  re-test hid the sentence.
- The same rule now holds for units 3 and 6.2: any label coded from the full sentence needs a frame-blind check
  before it is cited.

### Not examined

- **Extraction leakage.** The unit 3 extractor saw the sentence. Its wording may carry the frame, for example
  "Houston time" as the place expression in N1468. The 50 MULTI rows were not audited for this.
- **Human coders.** None were used. Both coders are Claude models, so their errors may be shared.
- **Separate subtype re-test.** No separate sun or arrival re-test was run. The blind coders marked only "time
  fixed by place".
- **Wolfram second route.** None was run for this re-test. The exact conditional route is in Python and shares
  table code with the Firth route.
- **Voice gates.** G35 and G36 were not run on this note.
