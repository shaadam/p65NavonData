# P65 Unit 3: logical dependence. ADVERSARIAL RE-TEST (2026-11-19)

Last updated: 2026-11-19 (Eastern).

Target: `docs/p65_unit3-dependence_results_2026-11-19.md` (commit 1e4cd77), and this sentence in its proposed
manuscript text: "On this coding the corpus direction follows dependence, with no lean toward time over place beyond
it." Registration of this re-test: Addendum A in `docs/p65_unit3-dependence_registration_2026-11-19.md`, commit
c3b240e, made before any coding. Files: `dependence/adversarial/`.

## Verdict: PARTLY, and the unit 3 headline does not stand

- **Circularity: certain.** The registered test cannot fail in the direction it reports. Its numbers reproduce
  exactly, but they measure the coding rule, not the corpus.
- **Re-test with the direction hidden.** Dependence still predicts direction, at about a third of the registered
  strength (odds ratio 3.9 after allowing for language, against 12.0).
- **No lean beyond dependence: disproved.** Pairings where neither fact needs the other still put time over place
  68% of the time.

## 1. Circularity (commit 9112a79)

The coder saw the frame, and the frame is the outcome. On a time-over-place (TP) row, the coder asked whether the
**place** needs a time. On a place-over-time (PT) row, the coder asked whether the **time** needs a place. The
"dependent" label therefore answers two different questions, and which question it answers is set by the outcome.

- Labelled dependent: 171 of 195 TP rows (0.877) and 19 of 48 PT rows (0.396).
- The headline share among non-dependent pairings, 24 of 53 (0.453), follows from those two rates and the margins
  alone. In symbols, s0 = nTP(1 − a) / (nTP(1 − a) + nPT(1 − b)), where a and b are the two rates above.
- **Negative control.** I simulated a world where direction is independent of both facts: each item carries a place
  fact (rate 0.877) and a time fact (rate 0.396), TP is drawn at 0.802, and the registered rule is applied. In 5,000
  runs:
  - the registered table returned "logical dependence SUPPORTED" in 92%;
  - it returned "hierarchy SUPPORTED" in none;
  - the median s0 was 0.453 and the median odds ratio 10.5.
  The registered statistic is therefore NON-DISCRIMINATING.
- The registered controls do not detect this. The plants test whether a coder codes by frame alone. The label
  shuffle only removes an association. Neither control can see a label whose question depends on the outcome.

## 2. Direction-blind re-test (commits c3b240e, ad6ac39, 6c7d219, this commit)

**Extraction.** A Sonnet subagent, given no labels and no hypothesis, copied three fields from each sentence: the
time expression, the place expression, and the entity involved as a noun phrase with no verb. 50 rows had competing
expressions and 15 had a missing one; these were flagged and kept.

Departure from the brief, in one line: the entity is shown alongside the two expressions. A ferry and a lighthouse
can stand at the same pier at the same hour, so dependence cannot be judged from the expressions alone.

**Coders.** One Opus and one Sonnet subagent, each in a fresh context. Each saw the entity and the two expressions
in random order. Each answered both questions for every item: whether the place needs the time, and whether the
time needs the place.

- Plants: each coder got 5 of 6. Both missed PL1 the same way, coding "all afternoon" as local time. That miss is a
  flaw in the plant, not in the coders.
- Agreement: kappa 0.822 on the four codes.
- 27 disagreements were adjudicated from the blind file before direction was joined.
- The blind codes match the original label on the question the original rule asked in 217 of 243 items (0.893).
  The extraction therefore kept the information the original coders used.

**TP share by cell, adjudicated codes, with exact 95% intervals:**

| code | TP / n | share [95%] |
|---|---|---|
| place requires time only (P) | 121 / 134 | 0.903 [0.840, 0.947] |
| time requires place only (T) | 5 / 9 | 0.556 [0.212, 0.863] |
| both (BOTH) | 37 / 53 | 0.698 [0.557, 0.817] |
| neither (NEITHER) | 32 / 47 | **0.681 [0.529, 0.809]** |

- **The neither cell.** Its interval lies above one half and covers the overall 0.802. Pairings with no dependence
  either way still lean time over place.
- **Contrast between cells.** P against T plus NEITHER:
  - pooled Fisher odds ratio 4.8, p = 0.0002;
  - allowing for language (Mantel-Haenszel), odds ratio 3.9 [1.75, 8.64], p = 0.0002.
  - English carries the effect: 96 of 103 TP in P against 17 of 28 in T plus NEITHER.
  - Indonesian shows little: 25 of 31 against 20 of 28. The two languages differ, p = 0.04.
- **The T cell** has 9 items and shows no lean toward place over time (5 of 9 TP).
- **What the original rule never asked:** 42 of 195 TP items (0.215) carry a local time, and 29 of 48 PT items
  (0.604) carry an entity whose place needs a time.
- **Each coder alone** gives the same verdict. The neither-cell share is 0.682 for coder A and 0.702 for coder B.
- **Control.** Shuffling direction within language gave p < 0.05 for the pooled contrast in 8.3% of 2,000 shuffles.
  That is above the nominal 5%, because language is confounded with both codes and direction. The language-adjusted
  test is therefore the one to quote.

## 3. Verdicts

| claim | verdict | evidence |
|---|---|---|
| Registered s0 = 0.453 and odds ratio 12.0 test logical dependence | DISPROVED (non-discriminating) | identity plus null simulation; CHECKED NUMERICALLY |
| Dependence, coded blind, predicts direction | SUPPORTED, weaker: language-adjusted odds ratio 3.9 | CHECKED NUMERICALLY |
| No lean toward time over place beyond dependence | DISPROVED: neither cell 0.681 [0.529, 0.809] | CHECKED NUMERICALLY |
| Re-test verdict (Addendum A table) | PARTLY | |

## 4. Consequences

- Do not adopt the proposed replacement text, the 90% / 45% split, or the odds ratio of 12. Section 6.2's claims
  that the corpus favours Navon's hierarchy are not overturned by this unit.
- One replacement that the evidence supports: coded with the direction hidden, pairings whose located thing moves
  lean further toward time over place (90%) than pairings where neither dimension needs the other (68%, 95% interval
  53% to 81%), and those still lean.
  - Plain reading: both accounts contribute.
  - Limits: model coders, a post-hoc test, and an effect concentrated in English.
- The original registration made the same structural choice for the definitional test (frame shown, code defined on
  the stated value). That test (`definitional/`, other branch) should get the same direction-blind check before it
  is cited. Not examined here.

## Not examined

- The definitional test.
- Whether the extractor's choice among competing expressions (50 rows) favoured either direction.
- A human coder.
- The voice scripts (G35, G36) were not run on this note.
