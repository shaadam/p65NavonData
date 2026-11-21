# P65 interference study: full-text recode, pass 1 versus blind pass 2 (2026-11-19)

Rule application: `p65_armC_fulltext-recode_rule-application_2026-11-19.md` (commit e00cc5b, before coding).
Pass 1 (main session, Opus): `p65_armC_fulltext-recode_pass1_2026-11-19.tsv` (commit f308916, before pass 2 was opened).
Pass 2 (Sonnet subagent, blind to the TSV, the abstract codes and pass 1; neutral IDs P01 to P11):
`p65_armC_fulltext-recode_pass2-blind_2026-11-19.tsv`. ID map: `p65_armC_fulltext-recode_blind-id-map_2026-11-19.tsv`.

## Plant

P07 was Kirsch (2023), already full-text coded. Fixed answer: Exp 1 and Exp 2 EXCLUDED-ONE-DIRECTION, Exp 3
SPACE>TIME. Pass 2 returned exactly that. **Plant reproduced, 3 of 3.**

## Agreement on the ten papers

16 experiment rows. The passes agree on 15. The one disagreement is Reali et al. (2019).

| paper | exp | abstract code | pass 1 | pass 2 | status |
|---|---|---|---|---|---|
| Cai et al. (2022) | 1 | SPACE>TIME | SPACE>TIME | SPACE>TIME | agreed, unchanged |
| Charras et al. (2026) | 1 | SYMMETRIC | SYMMETRIC | SYMMETRIC | agreed, unchanged |
| Dormal & Pesenti (2013) | 1 | SPACE>TIME | SPACE>TIME | SPACE>TIME | agreed, unchanged; tag BETWEEN added |
| Homma & Ashida (2019) | 1 | TIME>SPACE | TIME>SPACE | TIME>SPACE | agreed, unchanged |
| Magnani et al. (2014) | 1 | SPACE>TIME | SPACE>TIME | SPACE>TIME | agreed, unchanged |
| Pierson & Hallez (2026) | 1 | SYMMETRIC | SYMMETRIC | SYMMETRIC | agreed, unchanged |
| Reali et al. (2019) | 1 | SPACE>TIME | SYMMETRIC | SPACE>TIME | **DISAGREE, open** |
| Riemer et al. (2026) | 1 | SPACE>TIME | SPACE>TIME | SPACE>TIME | agreed, unchanged |
| Riemer et al. (2026) | 2 | UNCODABLE-FROM-ABSTRACT | SYMMETRIC | SYMMETRIC | agreed, **new counted row** |
| Riemer et al. (2018) | 1 | SYMMETRIC | SYMMETRIC | SYMMETRIC | agreed, unchanged |
| Riemer et al. (2018) | 2 | SPACE>TIME | SPACE>TIME | SPACE>TIME | agreed, unchanged |
| Sarrazin et al. (2004) | 1 | EXCLUDED-ONE-DIRECTION | same | same | agreed, unchanged |
| Sarrazin et al. (2004) | 2 | EXCLUDED-ONE-DIRECTION | same | same | agreed, unchanged |
| Sarrazin et al. (2004) | 3 | SYMMETRIC | NONE | NONE | agreed, **changed**; tag BETWEEN |

## The open row: Reali et al. (2019)

Lighting (flashing vs static circles) was between subjects, 28 per group; both directions were measured within each
group. No test pools the groups.

- Flashing group (the classic tau-kappa display): kappa 72.3% vs chance, t(27) = 6.5, p < .0001 (PDF p. 8); tau
  58.4%, t(27) = 3.53, p = .001 (p. 9). Both significant: SYMMETRIC.
- Static group: kappa t(27) = 4.88, p < .0001 (p. 8); tau t(27) = 0.22, p = .82 (p. 9). SPACE>TIME.
- Authors' Results summary: "Kappa effect was observed both when circles were flashing and static, but Tau effect
  was only observed when dots were flashing as in typical paradigms" (p. 10).

Pass 1 took the standard display (precedent: standard-condition cells in Cai et al., 2022 and Starr & Brannon,
2016). Pass 2 took the authors' headline condition. Neither precedent fits cleanly: those were within-subject
conditions, and the closest between-subjects precedent (Jagorska et al., 2025) had a pooled test, which this paper
lacks. The committed rule does not decide it, so it is not adjudicated here.

Consequence (tally script on a scratch copy with all agreed recodes applied):

| Reali code | counted | primary sign test | adult visual | paper level |
|---|---|---|---|---|
| SPACE>TIME | 64 | 26 vs 14, p = .0807 | 24 vs 11, p = .0410 | 14 vs 8, p = .2863 |
| SYMMETRIC | 64 | 25 vs 14, p = .1081 | 23 vs 11, p = .0576 | 13 vs 8, p = .3833 |

The primary result keeps its direction and stays non-significant either way. The registered adult-visual
secondary test is significant at .05 under one code and not under the other. The manuscript was therefore not
edited (stop rule in the brief).

## Disagreements adjudicated

None besides Reali. Pass 2 flagged as unsure Sarrazin Exp 3 (BETWEEN, no direct interference statistic), Cai 2022
(negative-correlation block), Pierson & Hallez (crossover), Riemer 2026 Exp 2 (crossover) and Charras (drift-rate
per-direction tests). Pass 1 reached the same codes on each, by the same rule clauses.
