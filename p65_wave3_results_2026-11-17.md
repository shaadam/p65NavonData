# p65 wave 3, Indonesian census: results (2026-11-17)

Last updated: 2026-11-17 11:50 (Eastern). Registration `p65_wave3_registration_FROZEN_2026-11-16.md` (Section 6.5, the
first preprint's analysis; 2.2a; 5.2; 5.3; 13) with amendments 1 to 3 (`wave3/`). Analysis `scripts/p65_wave3_analyze.py
--real`, run ONCE at 11:47 EST after every batch was DONE and no HALT.txt existed; its output is
`wave3/p65_wave3_analysis-run_2026-11-17.txt` verbatim. Manuscript: `docs/manuscript/p65_navon_v1.md` Section 2.6.

## Run

- Census: 6,628 sentences (Indonesian GSD + CSUI, UD r2.18), P01 (500) and M01 to M16 (400 each, M16 128), every sentence
  coded by coder 1 (claude-opus-5-5) and coder 2 (claude-sonnet-5-5), adjudicated by claude-opus-5-5; 5 gold items per batch.
  Spend $79.70 list of the $165 cap (`wave3/main/spend.tsv`). No HALT. Runner commits a136995 to 64021d6 on main.
- S1: P01 P-kappa 0.937, D-kappa 0.215 on 50 both-present (bar 0.40): STOP; one notes revision (amendment 2); second
  pilot P02 (300, amendment 3): P-kappa 0.954, D-kappa 0.846 on 36 both-present (bar 0.60): confirmatory
  (`wave3/main/S1_LABEL.txt`; `p65_wave3_check.py gate P02` re-run direction-blind 2026-11-17 10:4x EST, same numbers).
  P02 sentences are analysed from their M-batch codes only; P01 codes (first notes) stay in the census (registration 2.1).

## Registered estimates, as printed

| quantity | value | registration |
|---|---|---|
| sentences analysed | 6,628 (17 batches) | 2.2a |
| P-kappa (presence), raw presence agreement | 0.930, 0.985 | 5.2 (reported) |
| D-kappa on both-present sentences | 0.603 on 743; gate **pass** (bar 0.60, n ≥ 100) | 5.2 |
| directional sentences | 70: TP 49, PT 21 | 6.5 |
| share time over place, 95% logit interval | **0.700 (0.583 to 0.796)**; logit 0.847, SE 0.261 | 6.5 primary |
| two-sided exact test of share = 0.5 | p = 0.0011 | 6.5 primary |
| flip rate e (both-directional 42, disagreeing 2) | d 0.048, e 0.024, upper 0.089, under 0.15 | 5.3 |
| flip-corrected share | 0.710 (0.588 to 0.811); at the upper e 0.743 | 5.3, D.7 |
| difference from English A3b 0.823, logit | −0.690 (−1.509 to 0.130) | 6.5 secondary, exploratory |
| rule Y on the achieved count | 70 is in 60 to 99: "insufficient-for-own-test" | 3 |
| screen recall TP, PT; precision | 0.694, 0.810; 0.045 (English 0.769, 0.366) | 6.5 descriptive |
| label | CONFIRMATORY (S1_SECOND passed) | 9 S1, amendment 3 |

## Reading

Time over place holds in Indonesian (0.70, interval above one half, p = .001), somewhat below the English estimates
(0.74 registered, 0.82 exploratory); the logit difference from the exploratory English share does not exclude zero.
The yield fell short: 70 directional sentences against 164 expected (113 lower), so by rule Y the per-language test is
reported as insufficient in weight while the registered estimate, interval and test stand. The English date-and-time
screen does not transfer: in Indonesian it recalls place-over-time (0.81) better than time-over-place (0.69), the reverse
of English, at precision 0.045.

## Independent recounts (own code, no analysis-script import)

- `scripts/p65_v1_figure-audit.py` (fig2 ID rows): share 0.7, interval 0.5832 / 0.7955, TP 49, PT 21, 6,628 non-gold rows,
  17 DONE, label confirmatory: all OK; `--perturb` (share + 0.01) MISMATCH fires.
- `scripts/p65_v1_number-trace.py` wave 3 block: see `p65_v1_number-trace.md` rows sourced "wave3/main/codes (own recount)".
