# Arm C row 76 (Riedl & Hallez 2026, Exp 1): full-text ruling — RULED SYMMETRIC (2026-11-17)

Status: **RULED 2026-11-17, code SYMMETRIC; the primary tally is unchanged (27 / 14 / 21 / 2, two-sided exact sign
test p = .0596).** Ruled from the HAL author manuscript
(`sources/RiedlHallez2026_development-space-time-interactions_JECP269-106533_HAL-author-manuscript.pdf`, 35 pp.,
fetched by the v1 citation pass), pages 15 and 17 rendered with PyMuPDF at 110 dpi and read as images, not text.

Work shown (registered rule, commit 66d9131: primary tally uses the experiment's own main test, or the visual
condition where the authors give none; SYMMETRIC = both directions significant and no asymmetry test reported):
- Exp 1 analyses the two directions in separate ANOVAs per modality and reports no direction or asymmetry test
  (p. 15, "Effect of space on time perception"; p. 17, "Effect of time on space perception"). So the visual condition
  decides the primary code.
- Visual, space on time (bisection points): Spacing main effect F(1, 87) = 23.00, p < .001, η² = .09 (p. 15).
- Visual, time on space (bisection points): Duration main effect F(1, 87) = 4.11, p = .046, η² = .015 (p. 17).
- Both directions significant at the authors' uncorrected p < .05, no asymmetry test: **SYMMETRIC**, definite.
- Auditory cell (secondary tally, unchanged): Spacing F(1, 86) = 0.95, p = .33 (p. 15); Duration F(1, 81) = 5.64,
  p = .02 (p. 17), i.e. TIME>SPACE, as the TSV's `cells` column already records.
- The first coder's transcription in the coded TSV (row 77 of the file, batch C2, exp 1) matches the rendered pages
  value for value. The second coder's abstract-only SPACE>TIME does not stand against the full text.

Consequence for the manuscript: Section 4 keeps 27 against 14 (p = .060) as the registered tally and 28 against 14
(p = .044) as the second-coder sensitivity. The number trace marks row 76 RULED.

## History (2026-11-14, superseded)

Status was BLOCKED: row 76 not ruled, draft unchanged. The text below is the 2026-11-14 record.

## Reference

Riedl, F., & Hallez, Q. (2026). The development of space-time interactions: A paradoxical effect of age modulated by sensory context and task difficulty. *Journal of Experimental Child Psychology*, 269, 106533. https://doi.org/10.1016/j.jecp.2026.106533 (PMID 42160914)

Google Scholar: https://scholar.google.com/scholar?q=%22The+development+of+space-time+interactions%3A+a+paradoxical+effect+of+age+modulated+by+sensory+context+and+task+difficulty%22

Open copy: HAL author manuscript hal-05646716, CC BY (Semantic Scholar lists it as green OA): https://hal.science/hal-05646716 (file: https://hal.science/hal-05646716/file/Manuscript.pdf)

## Why blocked

- Not in `sources/` or the local library (searched for riedl, hal-05646716, 106533).
- HAL (`/document` and `/file/Manuscript.pdf`) returns an Anubis "Making sure you're not a bot!" proof-of-work page (HTTP 200, text/html), not the PDF. Solving that challenge by script would defeat the site's bot control, so it was not done. This is the same block the second coder hit.
- The publisher version (ScienceDirect) is subscription-only; Europe PMC lists "Subscription required" and no PMC copy.
- OSF https://osf.io/5guc6 (the authors' data project) holds data and two .docx stats notes, not the article; it cannot stand in for the full text the rule is applied to.

## What the ruling will need (registered rule, commit 66d9131)

- SYMMETRIC: "both directions significant and no significant asymmetry test (or no asymmetry test reported)".
- SPACE>TIME: space-on-time p < .05 and time-on-space not significant, or a significant direction interaction favouring space-on-time.
- Cells: "the primary tally uses the experiment's own main test (or, where the authors give none, the visual condition)". Exp 1 crossed visual and auditory, so the page images must show whether the authors report one pooled main test for Exp 1 or only per-modality analyses.
- "Where the authors' own summary and their statistics disagree, the statistics win."

The first coder's full-text transcription (not re-verified here): visual time-on-space Duration main effect F(1,87) = 4.11, p = .046; space-on-time Spacing F(1,87) = 23.00, p < .001; no direction test. If page images confirm these as Exp 1's main tests, the code is SYMMETRIC and the tally is 27/14, two-sided exact sign test p = .0596. If they do not, the code follows the verified statistics.

## Next step

Adam saves the HAL Manuscript.pdf (or the JECP PDF) to Downloads and says "process local files"; then row 76 is ruled from PyMuPDF page images and folded into §5. Listed in `FETCH_LIST.md`.
