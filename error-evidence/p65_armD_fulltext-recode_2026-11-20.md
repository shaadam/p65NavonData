# p65 Arm D: full-text recode of the error-and-disorder sources (2026-11-20)

Branch `claude/p65-armD-recode-2026-11-20` (from `claude/p65-stats-fix-2026-11-17` at a3b79ed). Inputs:
`error-evidence/p65_armD_fulltext-status_2026-11-20.tsv` (28 sources, 23 held), current codes in
`error-evidence/p65_armD_per-source_2026-11-17.tsv`. Output rows: `error-evidence/p65_armD_fulltext-recode_2026-11-20.tsv`.

## 1. Decision rule (written 2026-11-20 01:55 Eastern, before any source was coded; not changed after)

Codebook: the map's own codes (`p65_error-evidence-map_2026-11-13.md` lines 9-11), unchanged.

- **S>T** space primary, time depends on space (the metaphor view).
- **T>S** time primary or scoping over space (Navon-consistent).
- **DISSOC** independence: time and space impaired, spared or acquired separately, against strict dependence either way.
- **MIXED** evidence points in more than one direction, or the order varies with language, group, item or task.
- **NONE** no bearing on direction: the source has no time-versus-space contrast that could order the two.
- **unknown** not read.

Rules, applied in order to each held source:

1. **Identity first.** The title page (page 1 of the PDF, read with PyMuPDF) must match the reference in the status
   file. If it does not, the old code stands, flagged `MISMATCH`, and the source is not recoded.
2. **Code what the source itself reports**: its results and its authors' stated conclusion about time and space.
   The map's gloss is not evidence. Every code carries a page number and a verbatim quote from that page.
3. **Direction from a deficit or a derivation.** A spatial deficit that brings a matching temporal deficit, temporal
   meanings derived from or learned after spatial ones, or time represented by spatial layout -> S>T. The same with
   time and space exchanged -> T>S.
4. **Dissociation.** One domain impaired or spared while the other is not, in either direction, or the authors'
   conclusion that the two are represented or learned independently -> DISSOC.
5. **Order varies.** The order differs across languages, groups, items or tasks within the source, or the source's
   own results point both ways -> MIXED.
6. **No contrast.** No temporal data, no spatial data, or a time-versus-space comparison with no difference and no
   claim of dependence -> NONE.
7. **Theory and language-change sources** code the direction the source argues for (a space-to-time derivation ->
   S>T); a source that argues no order holds codes MIXED or DISSOC by rules 4 and 5.
8. **Second code** only when the source itself supports two codes on separate findings (as the 2026-11-17 rows did
   for Gijssels et al. and Núñez & Sweetser); `double_coded = Y` then. A qualification of detail goes in the note.
9. **Doubt.** Between a direction code and MIXED, NONE or DISSOC, take the code that claims less direction. T>S needs
   an explicit result or conclusion in the source that time structures or precedes space.
10. **Partial copies.** A preprint, scan or excerpt is coded if it carries the relevant results; page numbers then
    refer to the held copy and the row says which copy.

Second pass: 6 of the recoded sources drawn at random (seed recorded below) plus 2 planted checks, recoded from the
text without the first-pass codes in view; agreement reported as a count.

## 2. Pass 1 result (commit 6134ddd)

23 held sources coded from full text; every title page matched its reference. Primary code changed for 4:
E. Clark 1971 MIXED -> S>T (p. 273), Tillman et al. 2017 MIXED -> NONE (preprint p. 30), Bowerman 1978 unknown ->
MIXED (p. 979), Zhang & Murao 2024 MIXED -> NONE (p. 100). Second code changed for 2: Núñez & Sweetser 2006 loses
its DISSOC second code (rule 8; p. 441), Lafford & Ryan 1995 gains a non-counted T>S-lean (Figure 13, p. 547). The
five sources not held (Morton & Patterson 1980, Kotten 1977, Feagans 1980, Coker 1978, Onnis et al. 2010) keep their
old codes, marked as coded from the abstract or a secondary source. No source is coded T>S: the headline holds.

## 3. Blind second pass

Sample: `random.Random(20261120).sample` of the 23 held ids, giving ids 12, 15, 18, 22, 25, 29 (Landau & Ferrara
2013, Harley & MacAndrew 2001, E. Clark 1971, Tillman et al. 2017, Lafford & Ryan 1995, Casasanto & Jasmin 2012).
Plants, mixed in unlabelled: Mätzig 2009 (coded NONE from full text on 2026-11-13) and Gijssels et al. 2013 (S>T,
read in part). Coder: a fresh agent given only this file's Section 1 rule and the eight PDFs, barred from the codes,
the map and the manuscript. Its rows: `error-evidence/p65_armD_blind-pass2_2026-11-20.tsv`.

| source | pass 1 | pass 2 | agree |
|---|---|---|---|
| Landau & Ferrara 2013 | NONE | NONE | Y |
| Harley & MacAndrew 2001 | NONE | NONE | Y |
| E. Clark 1971 | S>T | S>T | Y |
| Tillman et al. 2017 | NONE | NONE (S>T-lean, not counted) | Y |
| Lafford & Ryan 1995 | MIXED (T>S-lean) | NONE (T>S-lean) | N |
| Casasanto & Jasmin 2012 | S>T | S>T | Y |
| plant: Gijssels et al. 2013 | S>T | S>T | Y |
| plant: Mätzig 2009 | NONE | MIXED (DISSOC-lean) | N |

Random sample: 5 of 6 primary codes agree; both coders give Lafford & Ryan the same lean toward time first.
Plants: 1 of 2.

Ruling on Lafford & Ryan (by the rule text, before any count was rerun): MIXED stands. Rule 6 (NONE) needs no
time-versus-space contrast, and Figure 13 orders the temporal and spatial uses of *por*. Rule 5 covers an order
that differs across items (*por* time first, *para* both at the same stage). Pass 2's points (the earliest temporal
tokens were cued by the interviewer, p. 531; the authors draw no time-space conclusion) go into the row's note. The
headline and the time-first lean are the same under either code; only MIXED 7 against 6 and NONE 10 against 11
depend on the ruling.

Mätzig 2009 (plant missed): pass 2 finds no group difference but two patients with small advantages in opposite
directions, one reversing across tasks. That fits rule 5 as well as rule 6. Mätzig is outside this recode (it was
already full-text coded), so its code is not changed here; flagged for a ruling. If it became MIXED: MIXED +1,
NONE -1, no effect on T>S.

## 4. Ruling on the Mätzig 2009 plant (main session, 2026-11-20 ~09:45 Eastern)

The blind coder gave MIXED (DISSOC-lean); the planted code was NONE. **NONE stands; the plant counts as missed (1 of 2).**
Mätzig's own conclusion, PDF p. 147 (read with PyMuPDF): "The small differences and the inconsistent performance
patterns suggest that the patients were not influenced by the distinct meanings of spatial and temporal
prepositions" and "to date there is no good evidence for a difference in the availability of spatial and temporal
prepositions." On p. 146 the controls show no difference, and "in most patients there was none or only a small difference".
The two single-case effects the blind coder used (EW spatial, TH temporal, each p ≈ .02-.03 on one task, with TH
reversing in sentence completion) are ones the author sets aside. Rule 2 (code the source's own conclusion) and
rule 6 (no difference, no claim of dependence) give NONE, and rule 9 also points to the code that claims less.
No count changes: N 33, NONE 10, MIXED 7. Consequence: the blind pass agreed on 5 of 6 sampled sources and
caught 1 of 2 plants, which is weak support for the recode's reliability, not a defect in it.
