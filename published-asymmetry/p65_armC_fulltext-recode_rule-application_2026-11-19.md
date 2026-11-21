# P65 interference study: full-text recode of the ten abstract-coded papers, rule application (2026-11-19)

Written and committed BEFORE any of the ten full texts is read for coding. Plan: `docs/p65_v2_tests-plan_2026-11-19.md`,
v1 step 1. The rule is the registered one (`p65_published-asymmetry-registration_2026-11-13.md`, commit 66d9131;
manuscript Section 4). This file only says how that rule is applied to these rows. It adds no new criterion.

## Rows in scope

Every row of `published-asymmetry/p65_published-asymmetry-coded_2026-11-13.tsv` whose verification starts ABSTRACT for
these ten papers, plus any further experiment the full text reports that the abstract coding missed.

| paper (References name) | TSV keys now | full text in `sources/` |
|---|---|---|
| Cai et al. (2022) | CaiWuLiuWang2022 | 1-s2.0-S0001691822001238-main.pdf |
| Charras et al. (2026) | CharrasPonceLupianezCapizzi2026 | British J of Psychology - 2026 - Charras - ... .pdf |
| Dormal & Pesenti (2013) | DormalPesenti2013 | s00426-012-0414-3.pdf |
| Homma & Ashida (2019) | HommaAshida2018 | msr-article-p25_2.pdf |
| Magnani et al. (2014) | Magnani2014 | s00221-014-4005-y.pdf |
| Pierson & Hallez (2026) | PiersonHallez2026 | s13414-026-03371-z.pdf |
| Reali et al. (2019) | RealiLlerasAlviar2019 | Asymmetrical time and space interference in Tau and Kappa effects.pdf |
| Riemer et al. (2026) | RiemerBratzkeMichael2026 (Exp 1, Exp 2; ledger row E-11) | 1-s2.0-S0010028526000174-main.pdf |
| Riemer et al. (2018) | RiemerShineWolbers2018 (Exp 1, Exp 2) | Hippocampus - 2018 - Riemer - ... .pdf |
| Sarrazin et al. (2004) | Sarrazin2004_E1, _E2, _E3 | 2004-14382-001.pdf |

Out of scope: Sarrazin et al. (2007), RiemerHoelzlKleinboehl2014 and the other abstract-only EXCLUDED or UNCODED rows
(no full text held; none is counted now).

## How the registered rule is applied

1. **Unit.** The experiment as numbered by the authors. A between-subjects factor inside one numbered experiment
   (age group, sensory group) does not split it (G04 merge of Jagorska et al., 2025). Conditions differing in
   modality are cells, coded in the `cells` column only.
2. **Inclusion.** Both directions measured in the same participants within the experiment: an irrelevant spatial
   magnitude varied while time is judged, and an irrelevant temporal magnitude varied while space is judged. Space is
   length, distance, size-as-extent, displacement or location; time is duration, interval or temporal order. Only one
   direction measured: EXCLUDED-ONE-DIRECTION. Number-only pairings: excluded. Clinical samples: listed, not counted.
3. **Primary test.** The experiment's own main test of each direction (the effect of the irrelevant magnitude on the
   judged one, as the authors register or headline it). Where the authors give several, use the one their abstract
   or Results name as the interference measure. Where modalities differ and no overall test exists, use the visual
   condition.
4. **Significance.** p < .05 as the authors report it, uncorrected for multiple comparisons (Lambrechts et al., 2013,
   Experiment 1 ruling, 2026-11-14).
5. **Codes.** SPACE>TIME: space-on-time significant and time-on-space not, or a significant asymmetry test
   (direction x irrelevant-magnitude interaction, or a direct comparison of the two effects) favouring
   space-on-time. TIME>SPACE: the mirror image. SYMMETRIC: both significant and no significant asymmetry test, or none
   reported. NONE: neither significant. Both significant with a significant asymmetry test: code by the asymmetry test
   and flag "both sig".
6. **Sign.** A significant effect counts as significant whatever its sign; a reversed (incongruent) effect is noted
   (Riemer et al., 2022 precedent).
7. **Statistics over prose.** Where the authors' summary and their statistics disagree, the statistics win and the
   disagreement is noted.
8. **Polynomial terms.** Where the model has linear and higher terms, the linear term of the irrelevant magnitude is
   the registered effect (Jagorska et al., 2026 precedent); the higher terms go in the notes.
9. **Evidence recorded.** Each recoded row gets the statistic for each direction and the asymmetry test with the PDF
   page (PyMuPDF page index + 1, as printed in the PDF viewer), N, and `verification` = "FULL TEXT (sources/<file>,
   read with PyMuPDF, 2026-11-19 recode)".

## Procedure

- Pass 1: the main session codes every in-scope experiment from the full text.
- Pass 2: a Sonnet subagent codes the same papers from the same PDFs, given this file and the registration only. It
  sees neither the TSV, the abstract codes, nor pass 1. Papers are given neutral IDs.
- Plant: one already full-text-coded paper, relabelled with a neutral ID among the ten. Known answer fixed here:
  Kirsch (2023), `sources/s13414-023-02678-5.pdf`: Experiment 1 EXCLUDED-ONE-DIRECTION (time judged only),
  Experiment 2 EXCLUDED-ONE-DIRECTION (space judged only, different sample), Experiment 3 SPACE>TIME. Pass 2 must
  reproduce all three; if it does not, its codes are not used without a full re-read of every disagreement.
- Disagreements between passes are adjudicated from the PDF with page and verbatim quote (PyMuPDF text, checked
  against the rendered page where a number decides the code).
- Then the TSV is updated (coded_from = full text in `verification`), and the tally, clustered analyses, Figure 4,
  Appendix E and the number trace are rerun. If the sign-test direction or its significance at .05 changes, the
  manuscript text is not edited until the main session reports it.

## Ruling added after coding: Reali et al. (2019) (2026-11-19)

The two passes split on this row (`p65_armC_fulltext-recode_comparison_2026-11-19.md`). The committed rule does not
decide it. Lighting (flashing vs static circles) was between subjects, and each group measured both directions, but
no test pools the groups. Point 1 keeps a between-subjects factor inside one experiment, and the precedent there
(Jagorska et al., 2025) was coded by a pooled test that this paper lacks. Point 3 picks the authors' main test, and
here each group has its own. The standard-condition precedents (Cai et al., 2022; Starr & Brannon, 2016) were
within-subject conditions. The flashing group (classic display) gives both effects significant; the static group
gives space on time only.

Decision (main session, 2026-11-19, rwj, conservative choice): **SYMMETRIC**, the flashing-group code, because it
does not create a significant asymmetry from a group chosen after the result was seen. SPACE>TIME is reported as a
sensitivity analysis where the adult-visual test is reported (24 vs 11, p = .041, against 23 vs 11, p = .058 as
coded).
