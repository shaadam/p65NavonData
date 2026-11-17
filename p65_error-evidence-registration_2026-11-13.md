# p65 E1: direction of time/space intrusions in learner writing errors, registration (2026-11-13)

Adam (2026-11-13): "look at the types of mistakes people make in written and spoken speech. There's evidence
in that too." This file is committed and pushed before any count is made. State at commit time: the two
archives are downloaded and hashed and their licence and readme files read; no M2 sentence or edit has been
read or counted. The script `scripts/p65_error_intrusion_count.py` is committed with this file and was
smoke-tested on a three-sentence SYNTHETIC M2 file only.

## Why this test (and why only one)

Of the error types in the evidence map (aphasia, slips of the tongue, child errors, L2 errors, sign/gesture),
only learner-corpus preposition errors are (i) public, licensed and downloadable without a request form and
(ii) large enough to count in a few hours. Speech-error corpora (Fromkin, Stemberger, SFUSED) are either not
downloadable or hold too few time/space substitutions (as far as known at registration; the evidence-map search
running in parallel may change this, and any later speech-error test would be registered separately);
aphasia data are case tables, not countable corpora.

The test turns on one question that the accounts answer differently: **when a learner picks the wrong
preposition across the time/space boundary, which way does the error run?**

- **Metaphor (space-to-time) view** (Casasanto & Boroditsky, 2008; Boroditsky, 2000): people think about time
  through space, not the reverse. When a writer expresses a time relation, spatial representations are
  active; when expressing a spatial relation, temporal ones need not be. Corollary: spatial terms intrude into
  temporal slots ("in front of the exam", "under the summer") more often than temporal terms intrude into
  spatial slots ("before the cinema"). Predicts p > 0.5. This is our corollary of the view, not a claim
  any of its authors made about errors.
- **Navon (1978)**: no stated prediction about errors. His criteria concern orderliness, change verbs and
  marker scope. A possible extension ("terms of the dominant dimension spread to the dominated one") would
  predict p < 0.5; that extension is ours, weak, and is labelled as such wherever it is used.
- **Garner (1976)**: logical dependence between stimulus dimensions; it makes no prediction about which way
  lexical substitutions run. Predicts nothing (p is uninformative for Garner).

So E1 can count against the metaphor corollary (p < 0.5 or p near 0.5 with a tight interval) or for it
(p > 0.5). It cannot confirm Navon; at most it is consistent with the extension.

## Data (public, licensed, not committed)

Cambridge BEA-2019 shared-task releases, downloaded 2026-11-13 from
`https://www.cl.cam.ac.uk/research/nl/bea2019st/data/`:

| archive | SHA-256 | licence |
|---|---|---|
| fce_v2.1.bea19.tar.gz | c574c1cd...c07ec67e | CLC FCE licence: non-commercial research; cite Yannakoudakis, Briscoe & Medlock (2011); excerpts under 100 words |
| wi+locness_v2.1.bea19.tar.gz | d5cbf68c...c76c666 | W&I: same Cambridge terms; LOCNESS: non-commercial, credit CECL, no redistribution |

Files counted (annotator 0, all present in these releases):
- Learner (pooled): `fce.train/dev/test.gold.bea19.m2` (SHA-256 fa2d2c56..., 3c651088..., 085ac316...);
  `A/B/C.train.gold.bea19.m2` (79cf56f7..., 22465fae..., 66aea2af...) and `A/B/C.dev.gold.bea19.m2`
  (ddd7d1e9..., 9b8ea2c7..., d7cdfa7d...). `ABC.train` and `ABCN.dev` are concatenations and are NOT added
  (no double counting).
- Native: `N.dev.gold.bea19.m2` (02140717...), LOCNESS essays by native writers, descriptive only.

No data, sentence or excerpt is committed; the committed output holds counts and orig->correction word pairs.

## Counting rule

- Term sets (lowercased, whole-token match, multiword allowed):
  - T (temporal-only): before, after, during, until, till, 'til, since, prior to.
  - S (spatial-only): in front of, behind, above, below, beneath, under, underneath, beside, next to, inside,
    outside, opposite, across, along, alongside, into, onto, near, on top of.
  - Shared prepositions (in, on, at, by, over, through, within, between, around, towards, from, to, for) are
    excluded from both sets on purpose: their errors cannot be assigned a direction.
- An edit (annotator 0; noop skipped) is an intrusion **S->T** when the learner's original span equals an S term
  and the correction equals a T term; **T->S** the reverse. Exact span match is primary; a "contains" match
  (span contains a term of one set and none of the other) is a registered sensitivity count.
- Primary statistic: **p = n(S->T) / (n(S->T) + n(T->S))**, Clopper-Pearson 95% interval.
  Null p = 0.5: if the chance of writing X where Y belongs is proportional to freq(X) x freq(Y), the two
  directions have equal expected counts.
- Secondary: opportunity-normalised rate ratio RR = [n(S->T)/N_T] / [n(T->S)/N_S], N = term tokens in the
  corrected text; per-corpus (FCE vs W&I A/B/C) direction; word-pair table.

## Controls (each can fail)

- **C1, C2 (negative controls).** The same rule on two pairs that no account orders:
  C1 = T1 {before, after} vs T2 {during, until, till, 'til, since}; C2 = vertical {above, below, beneath,
  under, underneath, on top of} vs frontal {in front of, behind, opposite}. Each with n >= 10 must have a 95%
  interval containing 0.5. If one excludes 0.5, the symmetric null is not credible in these data and E1's p is
  reported as "not interpretable against 0.5": E1's departure is then judged only if it is larger than the
  control's departure (|p - 0.5|) and the intervals do not overlap.
- **D (dedicated-ness check).** In the corrected learner text, the share of T tokens followed within 3 tokens by
  a listed place noun, and of S tokens followed by a listed time noun, must each be <= 0.10. Above 0.10 the
  sets are not domain-pure and the result is labelled WEAK.
- **N (native).** LOCNESS natives should make almost no cross-domain intrusions: predicted 0 (0 to 2).

## Decision

- n = n(S->T) + n(T->S) < 10: **INSUFFICIENT** (report counts; say what larger corpus would settle it).
- Lower 95% bound > 0.5: **SUPPORTS metaphor corollary** (space intrudes into time).
- Upper 95% bound < 0.5: **AGAINST metaphor corollary**; consistent with (not evidence for) the Navon
  extension.
- Otherwise **INCONCLUSIVE**; if the interval lies within 0.30-0.70 it is reported as "no strong asymmetry
  in either direction", which counts against a strong metaphor corollary.
- Per-corpus replication: the direction (p above or below 0.5) should agree in FCE and in W&I where each has
  n >= 5; disagreement is reported and weakens any label.

## Predictions (made before counting)

| # | quantity | prediction (range) | basis |
|---|---|---|---|
| P1 | learner tokens (pooled) | 1.1 M (0.8 to 1.5 M) | FCE ~0.5 M, W&I train+dev ~0.6 M |
| P2 | N_T in corrected learner text | 2,800 (1,500 to 6,000) | ~1,500-2,500 per M in English, narrative tasks |
| P3 | N_S in corrected learner text | 3,000 (1,500 to 6,000) | "into" dominates |
| P4 | n(S->T) | 5 (1 to 15) | "under" for "during" (Scandinavian L1), "in front of" for "before" |
| P5 | n(T->S) | 12 (3 to 35) | "before" for "in front of" (L1s with one word for both: German vor, Polish przed, Russian pered) |
| P6 | p (E1) | 0.30 (0.10 to 0.60); P(n < 10) about 35% | T->S expected to dominate |
| P7 | E1 decision | INSUFFICIENT 35%, INCONCLUSIVE 35%, AGAINST 22%, SUPPORTS 8% | |
| P8 | C1 n; p | 25 (8 to 80); p inside 0.30-0.70, interval contains 0.5 (80%) | |
| P9 | C2 n; p | 4 (0 to 15); usually below n = 10 | |
| P10 | D shares | T 0.03 (0.00 to 0.08); S 0.02 (0.00 to 0.08) | |
| P11 | native intrusions | 0 (0 to 2) | |

## Threats stated now

- L1 transfer drives most learner preposition errors, and it runs both ways (one L1 word for "before" and
  "in front of" makes both S->T and T->S errors possible). E1 measures the net direction; it cannot tell
  conceptual from lexical transfer, and BEA M2 files carry no L1 field.
- ERRANT edit boundaries can merge a preposition with neighbouring words; the contains-match count bounds
  this.
- Written, edited exam essays are not speech; spoken slips may differ. The result speaks only to written L2
  errors.
