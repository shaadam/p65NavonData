# P65 Unit 3: logical dependence in the corpus sentences. RESULTS (2026-11-19)

Last updated: 2026-11-19 (Eastern).

Registration: `docs/p65_unit3-dependence_registration_2026-11-19.md`, commit 3408706, made before any coding.
Data, scripts and logs: `dependence/` (this worktree, branch `claude/p65-stats-fix-2026-11-17`). The definitional
test's folder sits on its own branch, `claude/p65-definitional-dependence-2026-11-18`. Its item file was copied here
unchanged, with the sha256 checked by the build script.

## Headline

On the 243 directional corpus sentences, whether a pairing is dependent predicts its direction strongly. Dependent
pairings state a place at a time in 90% of cases. Among non-dependent pairings, the time-over-place share is 45%,
whose interval covers one half and excludes the overall 80%. By the registered verdict table, the logical
dependence prediction is SUPPORTED and the Navon's-hierarchy prediction is NOT SUPPORTED. Five of the six coding
rules give the same verdict.

## Coding

- Coders: coder 1 was an Opus subagent and coder 2 a Sonnet subagent. Each worked in a fresh context and saw only
  the brief and the blind file (249 rows, shuffled with seed 20261119).
- Plants: coder 1 got 6 of 6, both on the primary binary and exactly on the three-level code. Coder 2 also got 6 of
  6 on both. Both coders are trusted. Coding by frame alone would have missed 4 of the 6.
- Agreement on the 243 real items:
  - primary binary (S against B or N): Cohen's kappa 0.883, raw agreement 95.9%
  - broad binary (S or B against N): kappa 0.613, agreement 92.6%
  - three-level code, quadratic-weighted: kappa 0.812, exact agreement 90.9%
  - shuffle control: kappa near 0 (median -0.010), so the control fired.
- Disagreements: 22 on the three-level code, 10 of them on the primary binary. The analyst adjudicated all 22 with
  the sentence in view, giving a one-line reason for each (`dependence/p65_dep_adjudication.tsv`).
- Final codes: English TP S 139 / B 4 / N 3, English PT S 16 / B 4 / N 7. Indonesian TP S 32 / B 10 / N 7,
  Indonesian PT S 3 / B 8 / N 10.

## Primary result (dependent = S)

| | dependent: TP / n | share [exact 95%] | non-dependent: TP / n | share [exact 95%] |
|---|---|---|---|---|
| English | 139 / 155 | 0.897 [0.838, 0.940] | 7 / 18 | 0.389 [0.173, 0.643] |
| Indonesian | 32 / 35 | 0.914 [0.769, 0.982] | 17 / 35 | 0.486 [0.314, 0.660] |
| pooled | 171 / 190 | 0.900 [0.848, 0.939] | 24 / 53 | **0.453 [0.316, 0.596]** |

Here TP means time over place: a place is stated and a time restricts when it holds. The overall pooled TP share
is 195 / 243 = 0.802.

Odds ratio, defined as the odds of TP among dependent pairings over the odds among non-dependent ones:

- Firth logistic regression TP ~ dependent + language: **12.0, 95% profile interval 5.4 to 28.7**, likelihood-ratio
  p < 1e-6.
  - Language term: 1.32 [0.58, 3.24].
  - Dependence by language interaction: 0.76 [0.15, 4.34], p = 0.74. The effect does not differ between the
    languages.
- Exact conditional common odds ratio across the two languages: 12.3 [5.0, 32.7].
- Mantel-Haenszel common odds ratio: 12.4 [5.2, 29.7].
- Fisher exact test: English p = 2.8e-6, Indonesian p = 0.00017.
- Predicted TP share for non-dependent pairings (Firth model, the counterpart of the definitional test's 87% and
  73%): English 41%, Indonesian 48%. For dependent pairings: English 89%, Indonesian 92%.

## Verdicts (registered table, pooled, primary codes)

- Logical dependence: **SUPPORTED**. The interval for the non-dependent share, [0.316, 0.596], covers 0.5 and
  excludes 0.802. The odds ratio is above 1.
- Navon's hierarchy: **NOT SUPPORTED**. Among non-dependent pairings the share does not stay near the overall
  share, and the odds ratio is far from 1.

## Sensitivity (broader coding and coder rules)

| rule | non-dependent TP / n | share [95%] | Firth OR [95%] | verdict (dependence / hierarchy) |
|---|---|---|---|---|
| primary (adjudicated S) | 24 / 53 | 0.453 [0.316, 0.596] | 12.0 [5.4, 28.7] | SUPPORTED / NOT SUPPORTED |
| broad (adjudicated S or B) | 10 / 27 | 0.370 [0.194, 0.576] | 8.4 [3.5, 20.9] | SUPPORTED / NOT SUPPORTED |
| union (either coder S) | 22 / 50 | 0.440 [0.300, 0.587] | 11.7 [5.2, 27.9] | SUPPORTED / NOT SUPPORTED |
| intersection (both S) | 29 / 60 | 0.483 [0.352, 0.616] | 10.9 [5.0, 24.9] | SUPPORTED / NOT SUPPORTED |
| union, broad | 4 / 17 | 0.235 [0.068, 0.499] | 14.2 [4.9, 49.5] | NOT SUPPORTED as stated (leans place over time) / NOT SUPPORTED |
| intersection, broad | 15 / 35 | 0.429 [0.263, 0.606] | 7.3 [3.3, 16.4] | SUPPORTED / NOT SUPPORTED |

The broad-union rule leaves only 17 non-dependent pairings, and they lean place over time. That goes further than
dependence predicts, but it points the same way and is still against the hierarchy. No rule leaves the
non-dependent share near the overall 0.80.

## Controls

- Plants: 6 of 6 for both coders.
- Kappa shuffle control fired.
- Dependence labels shuffled within language (2,000 permutations): median odds ratio 0.95, and 4.2% of shuffles
  gave p < 0.05. The control fired under every rule.
- Synthetic collapse control: with every TP item dependent, s0 = 0 of 48 and the odds ratio is unbounded. With
  every PT item dependent, s0 = 195 of 195. Both behave as registered. The script first failed with a division by
  zero under complete separation; it was guarded and rerun before any real codes existed.
- Second route (Wolfram, no shared code, `dependence/p65_dep_assoc.wls`) recomputes on the primary codes:
  - the counts, Fisher exact p-values, Firth odds ratio 12.003 [5.354, 28.745], the predicted shares and the
    Clopper-Pearson intervals all match Python to 3 or more digits;
  - the shuffle control fired (median S 155, null expectation 155.3).
  - One check failed: the Wolfram exact conditional interval did not converge. Its root-finder starting values
    were set for the definitional test's odds ratio below 1, and it returned bounds of 0.018 and 1.8e8. The
    conditional maximum-likelihood estimate (12.317) matches, but the 12.3 [5.0, 32.7] interval rests on the
    Python route alone. The Firth interval, which the manuscript quotes, is confirmed by both routes.
- No stray WolframKernel process was left after the run.

## Limits

- **Adaptation.** At the level of dimensions, the change study's table makes every TP pairing dependent and every
  PT pairing not. The registration therefore coded the kind of thing that carries the stated value: a person's
  place needs a time, and a clock reading needs a place. The test is only as strong as that adaptation.
- **Reading of the odds ratio.** People and vehicles fill TP sentences, and local clock times fill PT sentences.
  The large odds ratio partly restates that subject matter. That is the logical-dependence account's own claim,
  so the result is a fit of that account, not a causal estimate (as registered).
- **Interpretation.** The informative number is s0, the share among non-dependent pairings, not the odds ratio.
- **Coders.** The coders are models, not people. The analyst adjudicated knowing the hypothesis, but the union and
  intersection rows bracket the adjudication and give the same verdict.
- **Scope.** The test is post hoc on the existing corpus. It has 53 non-dependent pairings, or 27 under the broad
  rule.

## Consequence for the manuscript (for the main session; the manuscript was not edited)

This result goes further than replacing one clause. Section 6.2 says "Both language criteria agree with" Navon's
hierarchy, and that the corpus "adds a new result in which time takes scope over place." On this coding, the corpus
direction is accounted for by dependence. Non-dependent pairings show no time-over-place lean. The corpus therefore
no longer separates the hierarchy from logical dependence in the hierarchy's favour. The sentence "The two accounts
come apart only on pairs where..." and "None of the four studies tests those" also need checking against this test.
Those paragraphs, the abstract, and any claim-spine row that counts the corpus as support for the hierarchy should
be reviewed at integration.

## Proposed replacement text

The text below replaces "but no corpus sentence was coded for dependence, so that fit is not tested." The sentence
opening "It fits the corpus direction too" stays and is followed by a full stop.

> We tested that fit after the registered analyses, with the coding rule committed first. Two blind coders marked
> a pairing *dependent* when the stated value has no fixed value without the other dimension, as a person's place
> needs a time and a clock reading needs a place (Cohen's kappa 0.88). Dependent pairings, 190 of 243, stated a
> place at a time in 90% of sentences; among the other 53 the share was 45% (95% interval 32% to 60%), against 80%
> overall (odds ratio 12, 95% interval 5.4 to 29). On this coding the corpus direction follows dependence, with no
> lean toward time over place beyond it, and a broader coding gives the same pattern (37% of 27 sentences).
