# p65 Arm B: Navon's (1978) change-verb criterion on three open dictionaries (results, 2026-11-14)

Registration: `p65_change-verbs-registration_2026-11-14.md`, commit ea3fef9, pushed before any item was drawn
or coded. Codes frozen before comparison: 31ad62d (coders A, B), 596c1fd (third pass C). Analysis run: 775aeb6.

## Plain summary

Navon (1978, p. 226) says that dictionaries define change verbs (grow, fade, move) as changes over time, a few
(shade, slope) as changes over space, and that he found no verb "that could be interpreted to denote changes of
time or space as a function of some other dimensions". I tested this on WordNet 3.1, Webster's 1913 (GCIDE) and
English Wiktionary. Two independent model coders coded 1,725 verb senses blind, and a third coder settled the
141 disagreements.

1. **The asymmetry holds in all three dictionaries. The absolute "no such verb" claim fails once, in
   Wiktionary.** Among the 121 senses that name another dimension a change runs over, 112 name TIME, 6 SPACE,
   1 COLOUR and 2 OTHER; in 2 of them the thing that changes is time itself. Both coders put exactly one real sense in the
   falsifier cell. It is Wiktionary's *time-change* (sense 2, tagged "intransitive, uncommon"): "To undergo a
   difference in clocktime between two or more different time zones." Clock time varying across longitude is
   time changing over space. WordNet has none, and Webster 1913 has none on both coders. Webster 1913 has one
   on 2 of 3 coders: *soil*, "To become soiled; as, light colors soil sooner than dark ones" (when soiling
   happens varies with colour).
2. **Navon's reading rule is overwhelmingly borne out.** In the unbiased random samples, most change senses
   name no dimension at all ("to become X"), which Navon reads as change over time: WordNet 66 of 69 (96%),
   Webster 1913 58 of 59 (98%), Wiktionary 65 of 70 (93%). Explicit TIME: 2, 1 and 2. Explicit SPACE: 1, 0 and 2.
3. **Coder agreement is high.** Cohen's kappa is 0.91 for whether a sense is a change (n = 1,725), 0.95 for
   which dimension changes and 0.89 for what it changes over (n = 931 senses both coders call a change).
4. **Recall is the weak point.** The change-word filter (become, grow, vary, change, turn...) misses most change
   senses: 75% in WordNet (52 of 69; 95% interval 64–84%), 86% in Webster 1913 (51 of 59; 75–93%) and 87% in
   Wiktionary (61 of 70; 77–93%). Most change verbs are defined without those words ("to redden", "to dry").
   The falsifier search therefore did not rely on that filter. It used a full census of every verb sense with
   a time word plus a change or variation word: 580 real senses, of which 59 have time as the changing
   dimension on both coders. Even so, the 600 random senses held only 2 time-dimension senses, and both fell
   outside the census (*bishop* "to make seem younger", *marmorealize* "to make permanent"). The census's
   coverage of time senses cannot be estimated (0 of 2). So "zero falsifiers in WordNet and Webster 1913" shows
   that such senses are rare, not that they are absent.
5. **Negative control.** All 5 fabricated time-over-space senses planted in the WordNet census were flagged by
   both coders. The coders recognise the falsifier when it is there. The plants test the coders, not the filter,
   because they were planted inside the census.
6. **Formal-model predictions** (`p65_navon-formal-model_2026-11-13.md`):
   - **F5, shape: FAIL on the registered rule.** The near-triangular part holds: loss under Navon's order is
     3 of 121 (2.5%). Two registered conditions fail. First, one sense has time changing over another dimension
     on both coders. Second, an order that ranks OTHER above POSITION does strictly better (2 of 121). All 48 best
     orders put TIME first and none puts POSITION second. That margin is one item, *refract*, coded position over
     "density" on 2 of 3 coders.
   - **Permutation control: NON-DISCRIMINATING** (p = 0.95). TIME takes 112 of 121 column votes, so shuffled
     data are just as triangular. The triangle is a margin fact: nearly everything changes over time. It says
     nothing finer about an order among the other dimensions.
   - **Transpose control: fired as required.** Reversing every vote puts TIME last.
   - **F2, transitivity: NOT TESTABLE.** The pair POSITION vs QUANTITY has 0 votes.
   - **F3, additivity: NOT TESTABLE.** Every pair needs votes in both directions, and two pairs have 0 in one
     direction.
7. **Garner's logical-dependence rival is not separated from Navon.** Logical dependence licenses 117 of the 121
   directional senses (A changes over B where A needs B and B does not need A; everything needs time). Of the 4
   it does not license, 3 also contradict Navon: time over space, time over colour, and position over density.
   The fourth, quantity over heat, is neutral to Navon. Criterion (b) in dictionaries cannot tell a conceptual
   hierarchy from logical dependence.

**What the paper can print** (proposed sentences, not edited into any manuscript):
"In three openly licensed dictionaries (WordNet 3.1, Webster's 1913, English Wiktionary), 112 of 121 change
senses that name another dimension they vary over name time, and 93–98% of a random sample of change senses name nothing,
which Navon read as implicit change over time. One sense, Wiktionary's 'time-change' (clock time differing
across time zones), describes time varying over space, so the asymmetry holds but Navon's 'no such verb' does
not survive a modern sense inventory. Because nearly every directional sense runs over time, these data fit
Garner's logical-dependence account (117 of 121) as well as Navon's hierarchy."

## Counts per cell (final codes; change senses only)

| dictionary | stratum | change senses | over TIME | over SPACE | over other dim | ITEMS | UNSPECIFIED |
|---|---|---|---|---|---|---|---|
| WordNet 3.1 | random 200 | 69 | 2 | 1 | 0 | 0 | 66 |
| WordNet 3.1 | change-word sample 150 | 139 | 7 | 1 | 1 | 0 | 130 |
| WordNet 3.1 | time census (33 real) | 18 | 5 | 0 | 2 | 2 | 9 |
| Webster 1913 | random 200 | 59 | 1 | 0 | 0 | 0 | 58 |
| Webster 1913 | change-word sample 150 | 133 | 5 | 4 | 0 | 0 | 124 |
| Webster 1913 | time census (111) | 70 | 10 | 2 | 4 | 0 | 54 |
| Wiktionary | random 200 | 70 | 2 | 2 | 1 | 0 | 65 |
| Wiktionary | change-word sample 150 | 132 | 7 | 1 | 0 | 0 | 124 |
| Wiktionary | time census (436) | 242 | 77 | 1 | 0 | 7 | 157 |

Pooled changes-over matrix, all coded real senses (rows: what changes; columns: what it changes over; diagonal dropped):

| | TIME | POSITION | SIZE | COLOUR | INTENSITY | QUANTITY | OTHER |
|---|---|---|---|---|---|---|---|
| TIME | - | **1** | 0 | **1** | 0 | 0 | 0 |
| POSITION | 10 | - | 0 | 0 | 0 | 0 | 1 |
| SIZE | 7 | 2 | - | 0 | 0 | 0 | 0 |
| COLOUR | 6 | 3 | 0 | - | 0 | 0 | 0 |
| INTENSITY | 11 | 0 | 0 | 0 | - | 0 | 0 |
| QUANTITY | 29 | 0 | 0 | 0 | 0 | - | 1 |
| OTHER | 49 | 0 | 0 | 0 | 0 | 0 | - |

Beside it, per Navon's reading rule: 835 change senses with UNSPECIFIED over-dimension (OTHER 337, POSITION 234,
SIZE 89, TIME 60, INTENSITY 39, COLOUR 38, QUANTITY 38). Time vs position: 10 votes for time dominating, 1
against, share 0.91 (Wilson 95% 0.62–0.98). Time vs quantity: 29 vs 0 (0.88–1.00).

Positive controls (Navon's own verbs): every change sense of grow, mature, fade and move in all three dictionaries
is coded over TIME or UNSPECIFIED (17/17, 12/12, 18/18; move 7/7, 6/6, 7/7). Shade and slope are coded over
SPACE in only 1 of 5, 3 of 7 and 2 of 8 change senses; the rest are UNSPECIFIED (e.g. "to darken"). Dictionaries
name the spatial gradient less often than Navon's examples suggest.

## Falsifier and disputed senses, verbatim

- BOTH CODERS (falsifier): Wiktionary `WK:185048.1` *time-change*: "To undergo a difference in clocktime between
  two or more different time zones." (A, B, final: TIME over SPACE.) Same entry, sense 1: "To undergo a change
  as time passes." Source: kaikki.org English verb extract, line 185,049 of the file checksummed in the
  registration.
- 2 of 3 coders: Webster 1913 `GC:S020548` *Soil*: "To become soiled; as, light colors soil sooner than dark
  ones." (A: OTHER/UNSPECIFIED; B, C: TIME over COLOUR.) The timing difference is in the usage example, and it is
  across kinds of things more than along a colour dimension.
- Secondary claim (position over a non-spatial dimension), 2 of 3 coders: Webster 1913 `GC:R017656` *Refract*:
  "...to cause to deviate from a direct course..., as a dense medium refracts the rays of light as they pass into
  it from a rare medium." (direction over density).
- Near-misses (time over a set of items, not a dimension): Wiktionary *stagger* (2 senses: "starting at
  different, evenly spaced, times or places"; "To schedule in intervals or at different times"), WordNet
  *desynchronize* ("cause to occur at unrelated times").

## Method (as registered; deviations: none)

Sources, checksums and extraction: see registration table (WordNet 3.1 13,789 verb synsets; GCIDE 0.53 1913
Webster verb definitions 25,354; Wiktionary 91,176 verb senses). Strata per dictionary: 150 random change-word
candidates, the full time census, all senses of Navon's six verbs, 200 random verb senses; plus 5 plants. Total
1,725 items, shuffled, shown without dictionary or stratum, in three batches per coder. Coders were six
general-purpose subagents (Opus; three for coder A, three for coder B, no shared context) and one for coder C,
with the frozen codebook verbatim. Scripts: `scripts/p65_change_verbs_{fetch.sh,extract,filter,items,compare,analyze}.py`.
Codes (ids only, no definitions): `change-verbs/codes/`, sha256 in `change-verbs/codes_sha256.txt`; the item key
without definitions is `change-verbs/items_key_nodefs.tsv`. The full key with definitions is not committed for
licensing reasons; it is rebuilt with the fetch, extract, filter and items scripts (seed 20261114). Run outputs:
`change-verbs/p65_analysis-run_2026-11-14.txt`, `..._transpose-control_...txt`.

## Prior art

- Tests of Navon's criterion (b) on any dictionary or corpus: **not located** in two web searches (2026-11-14),
  and not in the citer screen recorded in `p65_navon-formal-model_2026-11-13.md`. That screen covered criterion
  (a) only.
- ADJACENT, from memory, to verify: Hay, Kennedy & Levin (1999) on degree achievements (widen, cool), change
  along a scale in time. Gawron (2005, 2009) on "extent" readings of change verbs ("the road widens near the
  town"), a spatial-change use that dictionaries rarely define. Talmy (1996/2000) on fictive motion. These are
  the linguistic literature on the same asymmetry, and Gawron's extent readings mean that dictionary definitions
  under-count change over space in usage.

## Limits

Dictionary definitions are lexicographers' paraphrases, not usage. Spatial-extent uses ("the road widens") exist
in usage without their own dictionary sense, so SPACE is under-counted. Webster's New Collegiate (1973), Navon's
source, remains unread. The coders are model subagents, not human raters. Wiktionary imports many 1913 Webster
definitions (its *fade* senses are Webster's word for word), so the three dictionaries are not independent. The
census's recall for time-dimension senses is unknown (0 of 2 random time senses fell inside it). The one
falsifier is a rare, "uncommon"-tagged Wiktionary coinage about clock time, a social reading of time rather than
time itself. A reader may reasonably discount it, but under Navon's wording ("any verb that could be interpreted")
it counts.
