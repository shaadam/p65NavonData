# P65 v2 Unit 4: spatial uses of the dictionary study's change verbs in corpus usage. RESULTS (2026-11-19)

Registration: `docs/p65_unit4-spatial-change-verbs_registration_2026-11-19.md`, commit 537b60c (before extraction).
Script and data: `change-verbs/unit4/`. Full output: `change-verbs/unit4/p65_unit4_analysis-output_2026-11-19.txt`.
Manuscript not edited; the main session integrates.

## Verdict

**CONTRADICTED.** The prediction was that spatial uses would make up more of these verbs' change uses in the corpus
than the dictionaries' 9 of 121 directional senses not over time. They make up less: 3 of 499 (0.6%). For the verbs
the dictionary study counted, usage does not reveal change over space that the dictionaries missed.

## Data

- Corpus: UD English EWT and GUM, release 2.18, the six files the corpus study used. All six sha256 values match
  `wave3/p65_wave3_ud-checksums_r2.18.tsv`.
- Verbs: single-word headwords and synset members of the 121 directional senses (76 lemmas). 915 VERB tokens of 38
  lemmas. Every token was coded, with no sampling.
- Coders: coder A was a Claude Opus subagent and coder B a Claude Sonnet subagent. Each worked in a fresh context
  with the codebook only and a separate shuffle. 5 planted sentences were mixed in.

## Plants and agreement

- Planted sentences: coder A 5 of 5, coder B 5 of 5. Both coders are trusted.
- Cohen's kappa on 915 real items: 0.78 on the six codes (88.3% raw agreement). 0.77 on the collapsed variable
  (spatial, temporal, other dimension, or not directional).
- 107 disagreements. 100 of them are TEMPORAL versus NOT-CHANGE: coder B treated flying, cultivating ("grow
  basil") and developing as not a change. The codebook's motion and change-of-state rules make those TEMPORAL.
- 7 disagreements had one coder saying SPATIAL. None was adjudicated SPATIAL: a train or bus passing a place is
  motion (codebook rule), "these things shade into one another" is a gradation between concepts, and a phrase
  "broken up across two lines" is an arrangement. Every adjudication with its reason is in
  `p65_unit4_adjudication.tsv`.

## Counts (final codes, 915 real uses)

| code | n | share of all uses |
|---|---|---|
| TEMPORAL | 494 | 54.0% |
| SPATIAL | 3 | 0.3% |
| OTHER-DIM | 2 | 0.2% |
| ACROSS-ITEMS | 18 | 2.0% |
| NOT-CHANGE | 398 | 43.5% |
| UNCLEAR | 0 | 0 |

The three spatial uses, which both coders coded SPATIAL:
- creep (EWT answers-20111108090616AAv6fpU_ans-0015): "there is a corner of a rug creeping in" (the edge of a photo).
- grow (GUM_fiction_time-25): "south-eastward it grew brighter to a glowing scarlet" (sky colour across the horizon).
- pass (EWT weblog dakbangla 20050210141134 -0066): "The route from Kalikhola ... passes through northern Bengal,
  Assam and Meghalaya".

## Test (registered)

| comparison | usage | dictionary | Fisher two-sided p | binomial p |
|---|---|---|---|---|
| **primary**: SPATIAL of directional uses vs not-over-time senses | 3/499 = 0.6% [0.2, 1.8] | 9/121 = 7.4% [4.0, 13.5] | 4.1e-05 (odds ratio 0.08) | 3.4e-13 |
| (a) vs SPACE-only senses | 3/499 = 0.6% | 6/121 = 5.0% [2.3, 10.4] | .0025 | 7.3e-08 |
| (b) SPATIAL + OTHER-DIM vs 9/121 | 5/499 = 1.0% [0.4, 2.3] | 7.4% | .00026 | 3.3e-11 |
| (c1) coder A alone | 3/482 = 0.6% | 7.4% | 5.2e-05 | |
| (c2) coder B alone | 8/426 = 1.9% [1.0, 3.7] | 7.4% | .0046 | |
| (d) SPATIAL of all 915 uses | 3/915 = 0.3% [0.1, 1.0] | | | |

The bracketed figures are Wilson 95% intervals. As a negative control, the hand-written Fisher sum matches scipy to
four figures on every row and returns p = 1.000 on a table with no difference.

Not registered, added because the primary comparison is not like for like:
- Agreed items only (no adjudication): 3 of 400, Fisher p = .0002.
- Usage counts every change event as TEMPORAL, but the dictionary's 121 left out the 835 change senses that name no
  dimension ("become X"). Putting those back gives a dictionary share of 18 of 981 change senses over space (1.8%).
  Against that share, usage (0.6%) is lower but not detectably so (Fisher p = .064). Read either way, usage is not
  more spatial than the dictionaries.

## What it means for 6.4

The Limitations claim says spatial-extent uses exist in speech without a dictionary sense of their own, so change
over space is under-counted. For the verbs the dictionary study counted, the corpus does not support it. Spatial
uses are rarer in usage than in the dictionaries, and coder B, the more generous coder, agrees. The claim can still
hold for extent verbs that never entered the 121 directional senses ("widen", "narrow", "slope", "rise"). This test
did not cover those verbs, as the registration stated in advance.

### Proposed paragraph for the manuscript (replaces the under-count sentence in 6.4)

> We checked this for the verbs the dictionary study counted. In 915 uses of these verbs in two English corpora,
> two independent coders judged 3 of the 499 uses that describe a change to run over space (0.6%, 95% interval
> 0.2% to 1.8%), fewer than the dictionaries' 9 of 121 senses not over time (7.4%; Fisher's exact test, p < .001).
> Spatial-extent verbs such as "widen" and "slope" were not on that list, so an under-count remains possible for
> them but is untested.

## Deviations from the registration

1. The registration text says 81 lemmas; the frozen list it prints has 76. The list was used unchanged, and only
   the count was wrong.
2. Sentence text is not committed. GUM is CC BY-NC-SA, and the repo holds codes and sentence ids only (as in
   `scripts/p65_wave3_ud_fetch.py`). `p65_unit4_extract.py` regenerates `p65_unit4_key.tsv` and the coder item files
   from the held corpus. The committed key is `p65_unit4_key_nosent.tsv`.
3. The analyst adjudicated knowing both the hypothesis and both codes, as the registration disclosed. No
   adjudication moved an item into SPATIAL, and the coder-alone rows show that adjudication does not drive the
   verdict.

## Limits

EWT and GUM are mostly written text (web, news, academic, fiction, some spoken), not speech. The coders are AI
models, not human raters. Several high-frequency lemmas (turn, grow, develop, fly) dominate the count. The
adjudication call that flying is motion adds 42 TEMPORAL uses to the denominator. The agreed-only row (3 of 400)
removes that call without changing the verdict.
