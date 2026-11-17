# p65 wave 3 (Indonesian census): amendment 2, the one notes revision under S1, 2026-11-17 09:28 EST

Registered rule: `p65_wave3_registration_FROZEN_2026-11-16.md` Section 9 S1 (and Section 13, "S1 on one language"). The
runner stopped after the pilot P01 (`wave3/main/logs/run.log`, 2026-11-17: P-kappa 0.937, D-kappa 0.215 on 50 both-present
items, bar 0.40; `wave3/main/HALT.txt`; $5.74 list price spent of $165). S1 then allows the per-language notes (Section 4.1)
to be revised **once**, from disagreement content only, never direction counts, after which a second pilot of 300 is drawn
(seed 20261132, string seed `20261132:<language>`, excluding the first pilot) and coded. This file records the one revision.
Approved: Adam's standing approval for this run (2026-11-17) covers the registered next steps.

## What was read

`wave3/main/codes/P01_adjudication-sheet.tsv` (12 split items with both codes) and `P01_adjudication.tsv` (rule citations),
read for the constructions that split the coders. Written up in `wave3/p65_wave3_s1-disagreement-read_2026-11-17.md`. No
count by direction was made or printed; the run log prints kappas as numbers only. The 44 agreed both-present items and
the 445 agreed-NA items were not read.

## What changed (one file)

`wave3/main/p65_codebook-v2-TP-x_id.md`, section "Indonesian notes": one example added to the existing PR3 note and eight
notes appended under a dated heading. Each says how a rule already in the codebook shows in Indonesian grammar:
other time markers (`dari`, `sejak`, `antara ... dan`, `dalam waktu`, bare dates and day names); time clauses and the
conditional `bila / jika / kalau`; other place markers and `di` + institution; a preposition inside a title; locative and
existential predicates as the 1.3 "asserted value" and framing phrases as settings; fronting decides nothing; R2 in
Indonesian (`yang` clauses on a name); the two-sentence treebank unit is one target. None names a direction. Examples
are the three anchors and constructed phrases, none a pilot sentence. The "Last updated" line changed.

Not changed: the registration, bars, seeds, both briefs (the coder brief points at the codebook by path, so coders read
the revised notes), gold key, batches, queue, scripts.

## Hashes (sha256)

| file | frozen 2026-11-16 | amended 2026-11-17 |
|---|---|---|
| wave3/main/p65_codebook-v2-TP-x_id.md | b5612927edc37cb834c98a011390c11ee71e3c29e398ee6102cbcbe41f541642 | c675721c9b3c69997ab171971a7c9225f1cc65e11340203e01fe50a956e10c50 |

## Reading of Section 13

Section 13 lists "the second pilot draw" under "not applicable to this run" and says a second pilot "needs a person".
Section 13 also states that nothing in it changes a stopping rule, and S1 (Section 9) is the stopping rule that provides
the second pilot. The person is Adam (standing approval, 2026-11-17). The draw itself is amendment 3.
