# p65: registration — published space–time interference as a test of Navon's Garner criterion (2026-11-13)

Written and committed BEFORE any search for this unit. Prior knowledge at registration: the sources named in the source-reading note of 2026-11-13 (working repository) (Casasanto & Boroditsky 2008 read in full; Cai & Connell 2015 abstract) and general memory of the literature. No new reading has been done for this unit.

## Question

Navon (1978, p. 223) reads Garner's speeded-classification logic this way: "if the speed of sorting a set of stimuli by one dimension is affected by variation on the other dimension but not vice versa, the second one dominates in some sense the first one". So the dimension that intrudes is the dominant one. His hierarchy puts time over space. Under this reading, Navon predicts that **irrelevant time (duration, temporal order) intrudes on space judgements (length, distance, location) more than irrelevant space intrudes on time judgements**.

Competing accounts: the metaphor account (Casasanto & Boroditsky 2008) predicts the reverse (space intrudes on time more). A Theory of Magnitude (ATOM; Walsh 2003) predicts symmetry. Navon himself warns (p. 227) that the conceptual hierarchy need not match "dimensional priority in attention and memory", and that "different procedures may reveal different hierarchies" (p. 223). So this is a test of one operational reading of Navon, not of his whole claim.

## Inclusion rule

- An **experiment** is included if, **in the same participants**, it measures both (i) the effect of irrelevant spatial magnitude on a temporal judgement and (ii) the effect of irrelevant temporal magnitude on a spatial judgement.
  - Space = length, distance, size-as-extent, displacement, location. Time = duration, temporal interval, temporal order.
  - Any task (reproduction, bisection, comparison, speeded classification, Stroop-type) and any modality.
- Same participants means within-subject or both directions run in one sample in one experiment. A between-subjects split within one experiment is included but tagged BETWEEN.
- Populations: healthy humans of any age. Children are included and tagged CHILD. Non-human animals are included and tagged ANIMAL. Clinical samples are excluded (listed, not counted).
- Excluded: studies that measure only one direction; studies of number–time or number–space only; association/transfer studies without interference (e.g. infant preference); purely linguistic tasks without a perceptual magnitude judgement (tagged LING and listed, not counted, unless both directions use perceptual judgements); modelling papers with no new data.
- Unit of counting: the experiment as numbered by the authors. If one experiment has conditions that differ in modality (e.g. visual vs tactile), each modality condition is a **cell** and is coded separately in a secondary tally; the primary tally uses the experiment's own main test (or, where the authors give none, the visual condition).
- Published data only: journals, conference proceedings, and preprints with full text. Theses tagged THESIS.

## Coding rule (per experiment)

| code | rule | statistic it rests on |
|---|---|---|
| SPACE>TIME | space-on-time effect significant (p < .05) and time-on-space not significant; OR a significant dimension × direction interaction favouring space-on-time | the authors' slope, regression coefficient, interaction F or t |
| TIME>SPACE | the mirror image | as above |
| SYMMETRIC | both directions significant and no significant asymmetry test (or no asymmetry test reported) | both effect tests |
| NONE | neither direction significant | both effect tests |

- Where both effects are significant AND a significant asymmetry test is reported, code by the asymmetry test (SPACE>TIME or TIME>SPACE), and flag "both sig".
- Where the authors' own summary and their statistics disagree, the statistics win; the disagreement is noted.
- Each row records the statistic, N, paradigm, tags, data availability, and verification status (FULL TEXT / ABSTRACT ONLY / SECONDARY "as cited in").
- A row coded from the abstract only is counted but flagged; a secondary-only row is listed and not counted.

## Counting rule

- Primary tally: all included experiments, by code. Secondary tallies: (1) adult healthy humans, visual domain only; (2) by tag (CHILD, ANIMAL, non-visual); (3) cells.
- Test: among directional experiments (SPACE>TIME + TIME>SPACE), a two-sided exact sign test of SPACE>TIME vs TIME>SPACE. SYMMETRIC and NONE are reported as proportions with 95% Wilson intervals.
- Experiments within one paper are not independent (same lab, same stimuli). A paper-level tally (majority code per paper; ties = MIXED) is reported alongside.
- Effect-size summary only if ≥ 5 experiments report both directional effects on a comparable scale (e.g. slope of the irrelevant dimension on the judged one, both in proportion-of-range units, with SE or CI). Method then: per-experiment asymmetry d_i = (standardised space→time effect) − (standardised time→space effect); DerSimonian–Laird random-effects mean with 95% CI and tau². Negative control: within each experiment, randomly swap the two direction labels (10,000 permutations); the permuted mean asymmetry must be centred on 0 and the observed mean is compared against that distribution. If < 5 qualify, no pooled statistic is computed and the negative control is skipped.

## Prediction (mine, before searching)

- Included experiments: about 25–40 (C&B 2008 alone has 6).
- Primary tally: SPACE>TIME about 55%, SYMMETRIC/NONE about 30%, TIME>SPACE about 15%.
- Adult-human visual: SPACE>TIME a larger share (about 65%), because the metaphor-lab paradigm (growing lines, static lines) dominates that cell.
- TIME>SPACE expected mainly in non-visual cells (touch, Cai & Connell 2015) and possibly in animals.
- Pooled asymmetry, if computed: positive (space→time larger), CI excluding 0.

## What counts for or against Navon (under the Garner reading)

- **For Navon:** TIME>SPACE outnumbers SPACE>TIME with sign-test p < .05, or the pooled asymmetry is negative with CI excluding 0.
- **Against Navon:** SPACE>TIME outnumbers TIME>SPACE with sign-test p < .05, or the pooled asymmetry is positive with CI excluding 0. Interpretation then: interference dominance and Navon's conceptual hierarchy diverge, which Navon's p. 223 and p. 227 caveats allow. The verdict is "against Navon's hierarchy as read through Garner", not "against Navon's hierarchy".
- **Neither:** a SYMMETRIC/NONE majority, or a sign test that does not reject. This is itself reportable: it says the interference literature does not establish a Garner-type dominance in either direction, and that the direction depends on the paradigm (e.g. acuity, Cai & Connell 2015).
- Any of these is reported; there is no outcome that is dropped.
