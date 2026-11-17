# p65: published space–time interference as a test of Navon's Garner criterion — results (2026-11-13)

Registration (committed and pushed before any search): `p65_published-asymmetry-registration_2026-11-13.md`, commit 66d9131.
Coded data: `published-asymmetry/p65_published-asymmetry-coded_2026-11-13.tsv` (108 rows, SHA-256 00fb760a…bb31f68).
Scripts: `scripts/p65_published_asymmetry_merge.py`, `scripts/p65_published_asymmetry_tally.py`, `scripts/p65_published_asymmetry_meta.py`. Outputs: `published-asymmetry/p65_tally_primary.txt`, `p65_tally_2tailed.txt`, `p65_meta_random-effects.txt`.

## Bottom line

- **No tally supports Navon under the Garner reading.** TIME>SPACE never outnumbers SPACE>TIME, in any subset.
- **The primary registered test does not reject.** Over 64 experiments in 39 papers, the split is SPACE>TIME 27, TIME>SPACE 14, SYMMETRIC 21, NONE 2. The sign test of 27 against 14 gives p = .060.
- **The adult-human visual subset leans against Navon at p < .05.** Of 55 experiments, 25 are SPACE>TIME and 11 TIME>SPACE (p = .029).
- **The lean does not survive stricter cuts.**
  - Counting papers instead of experiments: 15 against 8, p = .21.
  - Full-text rows only: 21 against 13, p = .23.
- **The effect-size summary is small and not significant.** Across 9 experiments with slopes in a common unit, the random-effects mean asymmetry is +0.018 of the stimulus range (95% CI −0.002 to +0.037, p = .077). Heterogeneity is large (Q = 27.8 on 8 df).
- **Verdict, by the registered rules: "Neither", leaning against Navon.**
  - The literature does not show time intruding on space more than the reverse.
  - It shows a modest, paradigm-dependent excess of space intruding on time, concentrated in the metaphor-lab paradigms (Casasanto & Boroditsky 2008, 6 experiments).
  - The reverse appears often too (14 experiments), and a third of experiments are symmetric.
- **My registered prediction was roughly right.** I predicted about 55% SPACE>TIME, 30% symmetric or none, and 15% TIME>SPACE. The observed shares are 42%, 36% and 22%. TIME>SPACE was more common than I expected, and not only in non-visual cells.

## 1. What was searched and included

- **Sources.**
  - The OpenAlex citers of Casasanto & Boroditsky (2008): 1,220 works, filtered by title and abstract.
  - The citers of Cai & Connell (2015), Merritt et al. (2010) and Riemer & Cai (2024).
  - Standard web searches, and the reference lists of the papers read (including the Table 1 of the Riemer & Cai 2024 review).
  - The held library: `pdf-index.md`, `all-pdfs-index.tsv` and every PDF in the local library. No relevant paper was held.
- **No meta-analysis exists.** The nearest thing is a narrative review (Riemer & Cai 2024), which argues that the asymmetry "we get out" comes from paradigms biased toward space.
- **Coding.** Five coder batches (subagents, the registered brief) produced 108 rows covering 62 papers. I adjudicated them by rule, as logged in the `adjudication` column. Main changes:
  - The Cai & Connell 2012 CogSci rows were dropped as duplicates; they use the same samples as Cai & Connell (2015).
  - De Corte et al. (2017, pigeons) is not counted: the only evidence for both directions is a press report.
  - Three 1970s–80s Perception & Psychophysics papers (Thomas & Cantor 1975; Collyer 1977; Huang & Jones 1982) are listed but not coded, because the Springer full texts were bot-walled and only secondary descriptions were found.
- **Counted:** 64 experiments from 39 papers.
  - 29 papers read in full (PDF, Europe PMC XML, or a publisher page extracted with WebFetch).
  - 10 papers coded from the abstract only.
  - Across all 62 papers screened: 41 full text, 21 abstract only, 4 records secondary only.

## 2. Tallies (registered coding; `p65_tally_primary.txt`)

| subset | n | SPACE>TIME | TIME>SPACE | SYMMETRIC | NONE | sign test S>T vs T>S |
|---|---|---|---|---|---|---|
| all counted (primary) | 64 | 27 (.42) | 14 (.22) | 21 (.33) | 2 (.03) | p = .060 |
| adult human, visual | 55 | 25 (.45) | 11 (.20) | 17 (.31) | 2 (.04) | p = .029 |
| full text only | 53 | 21 | 13 | 17 | 2 | p = .23 |
| paper level (majority; 4 MIXED) | 39 | 15 | 8 | 11 | 1 | p = .21 |
| children (CHILD) | 5 | 2 | 0 | 3 | 0 | — |
| animals (ANIMAL; Merritt et al. 2010 monkeys) | 2 | 0 | 1 | 1 | 0 | — |
| primary modality non-visual | 2 | 0 | 2 | 0 | 0 | — |

**Two-tailed sensitivity (`p65_tally_2tailed.txt`).**
- Six codes rest on one-tailed tests, a borderline asymmetry p, or a disputed test. Recoding them as if only two-tailed tests counted gives SPACE>TIME 25, TIME>SPACE 10, SYMMETRIC 25, NONE 4 (sign test p = .017).
- In this version the adult-visual subset gives p = .020 and the paper level p = .078.
- The stricter reading strengthens the lean against Navon, mostly because three of Cai & Connell's and Kranjec's TIME>SPACE codes rest on one-tailed p.

## 3. Effect-size summary (registered: at least 5 comparable experiments; `p65_meta_random-effects.txt`)

- **Experiments included (9).** These report both directions as slopes of the judged magnitude on the irrelevant one, in a common unit (proportion of the stimulus range, or both predictors rescaled to one range), with an SE:
  - Cai et al. 2018, Exps 1–4
  - Starr & Brannon 2016
  - Bratzke & Ulrich 2025, Exps 1–3
  - Riemer, Wolbers & van Rijn 2024
- **Method.**
  - Per-experiment asymmetry a = b(space→time) − b(time→space).
  - SE = √(SE₁² + SE₂²). The within-subject covariance is unknown and was set to 0.
  - The pooled estimate is a DerSimonian–Laird random-effects mean.
- **Result.**
  - Mean asymmetry +0.0177 (95% CI −0.0019 to +0.0373), z = 1.77, p = .077.
  - τ² = 0.00058.
  - Leave-one-out estimates range from +0.013 to +0.024. Only dropping Bratzke & Ulrich Exp 3 gives a CI that excludes 0.
- **Negative control.** Direction labels were swapped at random within each experiment (10,000 permutations). The mean permuted pooled asymmetry was +0.00004, so the procedure gives no asymmetry when there is none. The permutation p for the observed value is .099.
- **Caveats.**
  - Most SEs are derived (from p or t), and the Bratzke & Ulrich Exp 1 space→time SE is an upper bound.
  - Riemer 2024 uses a different rescaling (comparison values mapped to −1..+1).
  - The Casasanto & Boroditsky (2008) slopes are in raw ms/px vs px/ms and could not be put on a common scale, so the strongest SPACE>TIME paper is absent from this summary.

## 4. What it means for Navon (1978)

- **Under Navon's own Garner reading (p. 223), this literature does not confirm his hierarchy.** That reading says the dimension that intrudes is the dominant one. Time does not intrude on space more than space on time.
  - Where an asymmetry appears, it more often runs the other way, with space intruding on time. That would put space over time, the reverse of his order.
  - That lean is not robust to counting papers instead of experiments, or to dropping abstract-only rows. The registered primary test misses .05 (p = .060).
- **The direction depends on the paradigm, which is the strongest regularity in the data.**
  - Growing lines and moving dots (Casasanto & Boroditsky 2008; Merritt 2010; Starr & Brannon 2016) give SPACE>TIME.
  - Several manipulations give TIME>SPACE:
    - touch (Cai & Connell 2015);
    - evidence accumulated over time (Lambrechts et al. 2013; Martin et al. 2017);
    - a harder spatial task (Vidaud-Laperrière et al. 2022 Exp 2; Homma & Ashida 2018/2019);
    - repeated intervals (Pierson & Hallez 2026);
    - post-cued static lines (Bratzke & Ulrich 2025 Exps 2–3).
  - Illusory size, registered replications and VR navigation mostly give SYMMETRIC (Bratzke 2024; Whitaker et al. 2024; Riemer et al. 2022).
  - This matches Cai & Connell's acuity account and Riemer & Cai's (2024) "asymmetry we put in". It also matches Navon's own p. 223 caveat that "different procedures may reveal different hierarchies".
- **This is not a test of the conceptual hierarchy itself.**
  - Navon (p. 227) says the hierarchy's relation to "dimensional priority in attention and memory is yet to be determined".
  - The interference studies measure processing, mostly memory interference. Cai et al. 2018 show it arises when both magnitudes sit in working memory.
  - So the fair statement is narrower: the interference operationalisation of dominance does not deliver Navon's order. If his criteria (b) and (c) (Arm A corpus) or (a) (the orderliness design) do deliver it, the divergence between procedures is itself the finding.

## 5. Included experiments (code; statistic; N; verification; data)

Full rows, with every statistic, are in the TSV. Short form:

| paper | exp | code | key statistic | N | read | public data |
|---|---|---|---|---|---|---|
| Casasanto & Boroditsky 2008 | 1–6 | SPACE>TIME ×6 | space→time significant, time→space not, in each; difference-of-correlations z significant | 9–19 | full (author PDF) | none |
| Casasanto, Fotakopoulou & Boroditsky 2010 | 1 | SPACE>TIME (CHILD) | direction F(1,95) = 139.2 | 99 | full | none |
| Merritt, Casasanto & Brannon 2010 | humans | SPACE>TIME | asymmetry χ²(1) = 19.66, p < .001 | 13 | full (PMC) | none |
| Merritt et al. 2010 | monkeys 2a, 2b | SYMMETRIC; TIME>SPACE (2b χ² = 4.39, p = .04; the authors call it symmetric) | — | 2 | full | none |
| Bottini & Casasanto 2013 | 1 | SPACE>TIME (CHILD) | — | 56 | full | none |
| Homma & Ashida 2015 | 1 | SPACE>TIME (400–800 ms cell) | χ²(1) = 4.54 | 24 | full | none |
| Homma & Ashida 2018/2019 | — | TIME>SPACE | abstract | ? | abstract | ? |
| Starr & Brannon 2016 | 1 | SPACE>TIME | direction F(1,19) = 119.95 (raw units) | 20 | full | none |
| Cai & Connell 2015 | 1–3 | TIME>SPACE ×3 (E1 haptic; E2/E3 one-tailed) | partial r .41 vs .13 (E1) | 26–32 | full (author PDF) | none |
| Cai, Wang, Shen & Speekenbrink 2018 | 1–4 | SPACE>TIME, NONE, NONE, SYMMETRIC | proportion-of-range slopes | 20–50 | full | osf.io/zrg7d |
| Cai & Wang 2021 | 1–3 | SPACE>TIME, SPACE>TIME, SYMMETRIC | E2 asymmetry t(30) = 3.62 | 24–31 | full (PsyArXiv preprint) | osf.io/8pvsr |
| Cai, Wu, Liu & Wang 2022 | 1 | SPACE>TIME (positive-correlation cell) | abstract | ? | abstract | osf.io/spmzj |
| Lambrechts, Walsh & van Wassenhove 2013 | 1–2 | TIME>SPACE ×2 (surface) | — | 12 | full | none |
| Martin, Wiener & van Wassenhove 2017 | 1 | TIME>SPACE (surface) | — | 17 | full (bioRxiv) | none |
| Kranjec et al. 2019 | 1 | TIME>SPACE (auditory; one-tailed) | partial r .81 vs .64 | 20 | full | none |
| Gijssels et al. 2013 | 1 | SPACE>TIME | Wald χ²(1) = 8.00 | 17 | full | none |
| Moon et al. 2015 | 1 | SPACE>TIME | task × congruity F(1,29) = 7.48 | 30 | full (PMC) | none |
| Magnani, Oliveri & Frassinetti 2014 | 1 | SPACE>TIME | abstract | ? | abstract | none |
| Dormal & Pesenti 2013 | length–duration | SPACE>TIME | abstract | ? | abstract | none |
| Reali, Lleras & Alviar 2019 | — | SPACE>TIME (tau eliminated, kappa intact) | abstract | ? | abstract | ? |
| Riemer, Shine & Wolbers 2018 | 1, 2 | SYMMETRIC; SPACE>TIME | abstract | ? | abstract | ? |
| Riemer, Achtzehn, Kuehn & Wolbers 2022 | 1 | SYMMETRIC | d_av .53 vs .36 (reversed sign) | 24 | full | GitHub jAchtzehn/timePath |
| Riemer, Wolbers & van Rijn 2024 | 1 | SPACE>TIME | asymmetry t(84) = −2.0, p = .049 | 13 | full | osf.io/f2xra |
| Riemer, Bratzke & Michael 2026 | 1 | SPACE>TIME (growing lines) | abstract | ? | abstract | osf.io/mxv48 |
| Vidaud-Laperrière et al. 2022 | 1, 2 | SPACE>TIME; TIME>SPACE | F(1,15) = 6.32; F(1,31) = 9.56 | 16, 32 | full (thesis manuscript) | none |
| Whitaker et al. 2024 (registered replication of C&B 2008) | lab, online | SYMMETRIC ×2 | both p < .001; R² values overlap | 35, 35 | full (WebFetch) | osf.io/t2a67 |
| Kirsch 2023 | 3 | SPACE>TIME | kappa F(8,120) = 17.15; tau F(8,128) = 0.89 | 17 | full | osf.io/ykasw |
| Bratzke 2024 | 1–3 | SYMMETRIC ×3 (illusory size; pooled ANOVA) | F(1,146) = 24.25 vs 128.41 | 44–57 | full | none |
| Bratzke, Peris & Ulrich 2024 | 1–2 | SYMMETRIC ×2 | — | 75, 82 | full | none |
| Bratzke & Ulrich 2025 | 1–3 | SPACE>TIME (asymmetry p = .049); TIME>SPACE; TIME>SPACE | E3 asymmetry t(24) = 2.28 | 23–25 | full | osf.io/wcv6f |
| Jagorska, Steinecker & Riemer 2025 | young; older | SPACE>TIME (t(36) = 2.2; fragile); SYMMETRIC (OLDER) | — | 37, 41 | full | GitHub cindyjag |
| Jagorska, Michel & Riemer 2026 | perceptual | TIME>SPACE | time→space p = .006; space→time p = .12 | 40 | full | GitHub cindyjag |
| Bogon, Jagorska, Heinz & Riemer 2025 | 1 | TIME>SPACE | t(113) = −2.1, p = .038 | 40 | full | osf.io/v9wxn |
| Schroeger et al. 2022 | 2 | SYMMETRIC (tau reversed) | Bayesian CrIs exclude 0 | 53 | full | OSF 675J4 |
| Sarrazin et al. 2004 | 3 | SYMMETRIC | abstract | ? | abstract | none |
| Hallez & Balcı 2024 | 1 | SYMMETRIC (CHILD) | partial η² .13 vs .13 | 82 | full (preprint) | osf.io/neyt6 |
| Hallez, Öztel & Balcı 2025 | 1 | SYMMETRIC | partial η² .08 vs .31 | 43 | full (HAL) | osf.io/kavzq |
| Riedl & Hallez 2026 | 1–2 | SYMMETRIC ×2 (CHILD; auditory cell TIME>SPACE) | — | 90, 112 | full (HAL) | osf.io/5guc6 |
| Pierson & Hallez 2026 | 1 | SYMMETRIC (reverses with sequence length) | partial η² .17 vs .49 | 30 | abstract + OSF supplement | OSF m57zn |
| Charras, Ponce, Lupiáñez & Capizzi 2026 | 1 | SYMMETRIC | abstract | ? | abstract | osf.io/z27k5 |

**Excluded (one direction, review, reanalysis, no interference test or duplicate).** Listed with reasons in the TSV:
- Bottini & Casasanto 2010: each direction in a different sample.
- Cai & Connell 2012 (duplicate data), 2016; Cai, Connell & Holler 2013.
- Eikmeier et al. 2013; Kirsch 2023 Exps 1–2; Martin 2017 Exp 2; Kranjec 2019 Exp 2; Vidaud-Laperrière 2022 Exp 3.
- Yates et al. 2012; Xuan et al. 2007; Ono & Kawahara 2007; Bausenhart & Quinn 2018.
- Sarrazin et al. 2004 Exps 1–2 and 2007; Schroeger 2022 Exp 1.
- Long et al. 2026; Nourouzi Mehlabani et al. 2020; Chen et al. 2021; Jagorska & Riemer 2024.
- Robinson & Wiener 2021; Riemer et al. 2014.
- Loeffler et al. 2018; Marcos & Genovesio 2017; Choy & Cheung 2017; Hamamouche & Cordes 2019; Riemer & Cai 2024.
- Hallez, Riedl & Balcı 2026 (reanalysis).
- Gladhill et al. 2024 (uncodable from the abstract).

**Listed, not counted (secondary only):**
- De Corte, Navarro & Wasserman 2017 (pigeons).
- Coull et al. 2015, J Cogn Neurosci 27(11), 2281–2298, doi 10.1162/jocn_a_00854. As cited in Riemer & Cai 2024, Table 1: space→time +, time→space −.
- Thomas & Cantor 1975; Collyer 1977; Huang & Jones 1982.

## 6. Limits

1. **A third of included papers rest on abstracts.** Ten of the 39 are abstract-only, and the TSV says which. The full-text-only tally is reported above and does not reject.
2. **Experiments within a paper are not independent.** Casasanto & Boroditsky contribute 6 rows; Bratzke 2024 gives one pooled ANOVA coded three times. The paper-level tally is the conservative check.
3. **Coding was done by model subagents.** I adjudicated six borderline codes, and the two-tailed sensitivity covers them. A second, independent human coder has not checked the rows.
4. **The registration did not fix one-tailed against two-tailed tests.** Both versions are reported. Neither favours Navon.
5. **Some full texts were unobtainable from the sandbox:**
   - Elsevier: Cai et al. 2022, Riemer 2026, De Corte 2017.
   - Wiley: Charras 2026.
   - Brill: Homma & Ashida 2018.
   - Springer archives (1970s–80s P&P papers).
   - Fetching these via a Google Scholar title search would let the 10 abstract-only rows be recoded: `https://scholar.google.com/scholar?q=%22Using+speed+to+think+about+space+and+time%22`; `…%22Temporal+cognition+can+affect+spatial+cognition+more+than+vice+versa%22`; `…%22Asymmetrical+time+and+space+interference+in+Tau+and+Kappa+effects%22`; `…%22On+the+duality+of+simultaneous+time+and+size+perception%22`.

## References (full; verification as coded)

Full references for every row (authors, year, title, journal, volume, pages, DOI, verification route, data URL) are in `published-asymmetry/p65_published-asymmetry-coded_2026-11-13.tsv`, columns `authors`–`doi`, `verification`, `data_public`. The core set:

- Bogon, J., Jagorska, C., Heinz, A., & Riemer, M. (2025). Presentation time shapes perceived room size in visual and auditory modalities. *Cognitive Research: Principles and Implications*, 10, 31. https://doi.org/10.1186/s41235-025-00644-3
- Bottini, R., & Casasanto, D. (2010). Implicit spatial length modulates time estimates, but not vice versa. In *Spatial Cognition VII* (LNCS 6222, pp. 152–162). https://doi.org/10.1007/978-3-642-14749-4_15
- Bottini, R., & Casasanto, D. (2013). Space and time in the child's mind: Metaphoric or ATOMic? *Frontiers in Psychology*, 4, 803. https://doi.org/10.3389/fpsyg.2013.00803
- Bratzke, D. (2024). Ebbinghaus, Müller-Lyer, and Ponzo: Three examples of bidirectional space-time interference. *Psychonomic Bulletin & Review*, 31(5), 2285–2292. https://doi.org/10.3758/s13423-024-02491-7
- Bratzke, D., Peris, L., & Ulrich, R. (2024). Time and visual-spatial illusions: Evidence for cross-dimensional interference between duration and illusory size. *Attention, Perception, & Psychophysics*, 86(2), 567–578. https://doi.org/10.3758/s13414-023-02737-x
- Bratzke, D., & Ulrich, R. (2025). Space–time interference between the length and duration of static lines. *Attention, Perception, & Psychophysics*, 87(5), 1665–1677. https://doi.org/10.3758/s13414-025-03093-8
- Cai, Z. G., & Connell, L. (2015). Space–time interdependence: Evidence against asymmetric mapping between time and space. *Cognition*, 136, 268–281. https://doi.org/10.1016/j.cognition.2014.11.039
- Cai, Z. G., & Wang, R. (2021/2022). Cross-dimensional magnitude interaction is modulated by representational noise: Evidence from space–time interaction. *Psychological Research*, 86(1), 196–208. https://doi.org/10.1007/s00426-020-01472-4
- Cai, Z. G., Wang, R., Shen, M., & Speekenbrink, M. (2018). Cross-dimensional magnitude interactions arise from memory interference. *Cognitive Psychology*, 106, 21–42. https://doi.org/10.1016/j.cogpsych.2018.08.001
- Cai, Z. G., Wu, L., Liu, H., & Wang, R. (2022). Cross-dimensional magnitude interactions reflect statistical correlations among physical dimensions. *Acta Psychologica*, 227, 103608. https://doi.org/10.1016/j.actpsy.2022.103608
- Casasanto, D., & Boroditsky, L. (2008). Time in the mind: Using space to think about time. *Cognition*, 106(2), 579–593. https://doi.org/10.1016/j.cognition.2007.03.004
- Casasanto, D., Fotakopoulou, O., & Boroditsky, L. (2010). Space and time in the child's mind: Evidence for a cross-dimensional asymmetry. *Cognitive Science*, 34(3), 387–405. https://doi.org/10.1111/j.1551-6709.2010.01094.x
- Charras, P., Ponce, R., Lupiáñez, J., & Capizzi, M. (2026). Space–time interference in magnitude judgements revealed by drift-diffusion modelling. *British Journal of Psychology*. https://doi.org/10.1111/bjop.70113
- Dormal, V., & Pesenti, M. (2013). Processing numerosity, length and duration in a three-dimensional Stroop-like task. *Psychological Research*, 77(2), 116–127. https://doi.org/10.1007/s00426-012-0414-3
- Gijssels, T., Bottini, R., Rueschemeyer, S.-A., & Casasanto, D. (2013). Space and time in the parietal cortex: fMRI evidence for a neural asymmetry. *Proceedings of the 35th Annual Conference of the Cognitive Science Society*, 495–500. https://escholarship.org/uc/item/41g9w85r
- Hallez, Q., & Balcı, F. (2024). Memory capacity as the core mechanism of the development of space–time interferences in children. *Scientific Reports*, 14. https://doi.org/10.1038/s41598-024-61018-1
- Hallez, Q., Öztel, T., & Balcı, F. (2025). Bidirectional interference between spatial and temporal processing. *Cognitive Science*, 49(12), e70156. https://doi.org/10.1111/cogs.70156
- Homma, C. T., & Ashida, H. (2015). What makes space-time interactions in human vision asymmetrical? *Frontiers in Psychology*, 6, 756. https://doi.org/10.3389/fpsyg.2015.00756
- Homma, C. T., & Ashida, H. (2019; online 2018). Temporal cognition can affect spatial cognition more than vice versa. *Multisensory Research*, 32(1), 25–44. https://doi.org/10.1163/22134808-20181287
- Jagorska, C., Michel, M., & Riemer, M. (2026). Space–time interference in action. *Cognitive Research: Principles and Implications*, 11, 41. https://doi.org/10.1186/s41235-026-00745-7
- Jagorska, C., Steinecker, I., & Riemer, M. (2025). Interferences between time and space in advanced age. *Memory & Cognition*. https://doi.org/10.3758/s13421-025-01775-0
- Kirsch, W. (2023). On the interplay between time and space perception in discontinuous stimulus displays. *Attention, Perception, & Psychophysics*, 85(7), 2406–2421. https://doi.org/10.3758/s13414-023-02678-5
- Kranjec, A., Lehet, M., Woods, A. J., & Chatterjee, A. (2019). Time is not more abstract than space in sound. *Frontiers in Psychology*, 10, 48. https://doi.org/10.3389/fpsyg.2019.00048
- Lambrechts, A., Walsh, V., & van Wassenhove, V. (2013). Evidence accumulation in the magnitude system. *PLoS ONE*, 8(12), e82122. https://doi.org/10.1371/journal.pone.0082122
- Magnani, B., Oliveri, M., & Frassinetti, F. (2014). Exploring the reciprocal modulation of time and space in dancers and non-dancers. *Experimental Brain Research*, 232(10), 3191–3199. https://doi.org/10.1007/s00221-014-4005-y
- Martin, B., Wiener, M., & van Wassenhove, V. (2017). A Bayesian perspective on accumulation in the magnitude system. *Scientific Reports*, 7, 630. https://doi.org/10.1038/s41598-017-00680-0
- Merritt, D. J., Casasanto, D., & Brannon, E. M. (2010). Do monkeys think in metaphors? Representations of space and time in monkeys and humans. *Cognition*, 117(2), 191–202. https://doi.org/10.1016/j.cognition.2010.08.011
- Moon, J. A., Fincham, J. M., Betts, S., & Anderson, J. R. (2015). End effects and cross-dimensional interference in identification of time and length. *Cognitive, Affective, & Behavioral Neuroscience*, 15, 680–695. https://doi.org/10.3758/s13415-015-0348-5
- Navon, D. (1978). On a conceptual hierarchy of time, space, and other dimensions. *Cognition*, 6(3), 223–228. https://doi.org/10.1016/0010-0277(78)90014-8
- Pierson, A., & Hallez, Q. (2026). From kappa to tau: Sequential repetition of an interval reverses the asymmetry of space–time interference. *Attention, Perception, & Psychophysics*. https://doi.org/10.3758/s13414-026-03371-z
- Reali, F., Lleras, M., & Alviar, C. (2019). Asymmetrical time and space interference in Tau and Kappa effects. *Cogent Psychology*, 6, 1568069. https://doi.org/10.1080/23311908.2019.1568069
- Riedl, F., & Hallez, Q. (2026). The development of space-time interactions. *Journal of Experimental Child Psychology*, 269, 106533. https://doi.org/10.1016/j.jecp.2026.106533
- Riemer, M., Achtzehn, J., Kuehn, E., & Wolbers, T. (2022). Cross-dimensional interference between time and distance during spatial navigation. *NeuroImage*, 257, 119336. https://doi.org/10.1016/j.neuroimage.2022.119336
- Riemer, M., Bratzke, D., & Michael, L. (2026). Using speed to think about space and time. *Cognitive Psychology*, 101797. https://doi.org/10.1016/j.cogpsych.2026.101797 (third author's initial not verified)
- Riemer, M., & Cai, Z. G. (2024). Space-time interference: The asymmetry we get out is the asymmetry we put in. *Neuroscience & Biobehavioral Reviews*, 167, 105941. https://doi.org/10.1016/j.neubiorev.2024.105941
- Riemer, M., Shine, J. P., & Wolbers, T. (2018). On the (a)symmetry between the perception of time and space in large-scale environments. *Hippocampus*, 28(8), 539–548. https://doi.org/10.1002/hipo.22954
- Riemer, M., Wolbers, T., & van Rijn, H. (2024). Memory traces of duration and location in the right intraparietal sulcus. *NeuroImage*, 297, 120706. https://doi.org/10.1016/j.neuroimage.2024.120706
- Sarrazin, J.-C., Giraudo, M.-D., Pailhous, J., & Bootsma, R. J. (2004). Dynamics of balancing space and time in memory: Tau and kappa effects revisited. *JEP: HPP*, 30(3), 411–430. https://doi.org/10.1037/0096-1523.30.3.411
- Schroeger, A., Grießbach, E., Raab, M., & Cañal-Bruland, R. (2022). Spatial distances affect temporal prediction and interception. *Scientific Reports*, 12, 15786. https://doi.org/10.1038/s41598-022-18789-2
- Starr, A., & Brannon, E. M. (2016). Visuospatial working memory influences the interaction between space and time. *Psychonomic Bulletin & Review*, 23(6), 1839–1845. https://doi.org/10.3758/s13423-016-1043-4
- Vidaud-Laperrière, K., Brunel, L., Syssau-Vaccarella, A., & Charras, P. (2022). Exploring spatiotemporal interactions: On the superiority of time over space. *Attention, Perception, & Psychophysics*. https://doi.org/10.3758/s13414-022-02546-8
- Walsh, V. (2003). A theory of magnitude: Common cortical metrics of time, space and quantity. *Trends in Cognitive Sciences*, 7(11), 483–488. https://doi.org/10.1016/j.tics.2003.09.002 (theory reference; not coded)
- Whitaker, M. M., Hansen, G. A., Creem-Regehr, S. H., & Stefanucci, J. K. (2024). The relationship between space and time perception: A registered replication of Casasanto and Boroditsky (2008). *Attention, Perception, & Psychophysics*. https://doi.org/10.3758/s13414-024-02942-2
