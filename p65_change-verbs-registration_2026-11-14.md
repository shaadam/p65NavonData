# p65 Arm B: Navon (1978) criterion (b) on three open dictionaries — REGISTRATION (2026-11-14)

Status: REGISTERED before any sense is classified. Written and committed before the coding items are drawn.
What was done before this file: the three dictionaries were downloaded and checksummed, every verb sense was
extracted, and the candidate filter below was run to COUNT pool sizes (numbers in "Pools"). No definition was
classified by anyone, and no sample was drawn.

## What is tested

Navon (1978, p. 226; PyMuPDF text of `sources/1-s2.0-0010027778900148-main.pdf`, scan OCR, checked by eye):
"numerous verbs denote co-variation of some attribute with time (e.g., to grow, to mature, to fade, etc.),
however they are always interpreted as describing variation of that attribute over time. To illustrate, all
the definitions of 'to fade' in Webster's Dictionary imply this interpretation by not even mentioning time
(e.g., 'to lose freshness or brilliance of color'). Fewer verbs stand for changes of some attributes as a
function of space (e.g., to shade, to slope). But I have not found any verb that could be interpreted to
denote changes of time or space as a function of some other dimensions."
Criterion (b), p. 227: "If objects are said to undergo change of one dimension over a second one but not vice
versa, the first is viewed as dominated by the second."

Webster's New Collegiate (1973), Navon's source, is not held. It is replaced by three openly licensed
dictionaries (files are not committed; `scripts/p65_change_verbs_fetch.sh` re-fetches them):

| dictionary | URL | version | fetched (UTC) | sha256 |
|---|---|---|---|---|
| WordNet 3.1 (Princeton licence) | https://wordnetcode.princeton.edu/wn3.1.dict.tar.gz | 3.1 | 2026-11-14 11:09 | 3f7d8be8ef6ecc7167d39b10d66954ec734280b5bdcd57f7d9eafe429d11c22a |
| GCIDE (Webster's Revised Unabridged 1913 + volunteers; GPL v3) | https://ftp.gnu.org/gnu/gcide/gcide-0.53.tar.xz | 0.53 | 2026-11-14 11:09 | d3acbd984de1ce022d5d139903887b36232e436e30eca2cb0fb1c058dd7f319f |
| English Wiktionary, kaikki.org verb extract (CC BY-SA) | https://kaikki.org/dictionary/English/pos-verb/kaikki.org-dictionary-English-by-pos-verb.jsonl | file Last-Modified 2026-10-31 | 2026-11-14 11:09 | 4090549f13cc5bd726fce6b72abbac9fd3770f36736b8f8e29243d34f986507c |

Extraction (`scripts/p65_change_verbs_extract.py`, run with `python3 -I`): WordNet one row per verb synset
(gloss before the first quoted example); GCIDE `<def>` texts under a verb part of speech in paragraphs marked
"1913 Webster" only (WordNet-derived additions excluded); Wiktionary one row per sense, form-of and alt-of
senses excluded. Verb senses: WordNet 13,789 (of which lexicographer file verb.change 2,388), GCIDE-1913 25,354,
Wiktionary 91,176.

## Pools (filter counts only)

`scripts/p65_change_verbs_filter.py` (regexes frozen in that file):
- CHANGE_RE (become, grow, increase, decrease, vary, change, gradual(ly), pass from, turn and inflections) or the
  headword is one of Navon's verbs (grow, mature, fade, shade, slope, move): candidates WN 802, GC 1,409, WK 4,717.
- TIME_RE (time, tempo, duration, date, hour, period, age, era, season, schedule, clock, delay, late(r),
  earlier, early, sooner, moment, day, year, pace, when).
- OVER_RE (place, distance, along, across, position, location, region, latitude, longitude, route, space,
  spatial, different, differ, successive(ly), according to, depending, vary, each, per, zone, stagger, spread,
  distribute(d), over) — frozen in `scripts/p65_change_verbs_items.py`.

## Coding items (drawn by `scripts/p65_change_verbs_items.py`, seed 20261114, after this commit)

Per dictionary:
1. **C-sample**: 150 random candidates (CHANGE_RE pool). Estimates the changes-over matrix of the candidate pool.
2. **T-census**: EVERY verb sense whose definition matches TIME_RE and (CHANGE_RE or OVER_RE). This is where a
   sense describing time changing over another dimension would have to be; it is coded in full, not sampled.
   (WordNet's change-word candidates with a time word number only 8, so the census is widened to OVER_RE.)
3. **Navon controls**: every sense of grow, mature, fade, shade, slope, move.
4. **Recall sample**: 200 random verb senses from ALL verb senses (filter not consulted).
5. **Plants (negative control)**: five fabricated senses describing time changing over space or another
   dimension, inserted into the WordNet T-census with ids indistinguishable from real ones. Text frozen here:
   - zonelag: "to occur at progressively later hours of the day as one moves westward along a route"
   - hourslope: "(of a timetable) to become later by a fixed number of minutes with each kilometre of distance from the terminus"
   - datedrift: "to fall on an earlier calendar date the farther south the place is"
   - thermotime: "to occur sooner as the temperature increases; to vary in time of onset with the degree of heat"
   - duralong: "to last a longer time with increasing distance from the source; to vary in duration from place to place"

All items are pooled, de-duplicated, shuffled (one order per coder), shown with headword and definition only
(no dictionary name, no stratum, no filter flag), split into three batches per coder.

## Codebook (frozen; given verbatim to every coder)

For each sense, read the definition only.
- CHANGE: Y if the sense describes a value of something being different at different points along some
  dimension: a change (become, grow, lose, increase, move from A to B, turn into) or a gradient (slopes, shades
  off, varies from place to place); causatives ("to cause to fade") count as the change they cause. N otherwise
  (actions, communication, possession, judgement, etc. with no dimension changing). If N, leave the rest blank.
- DIM (the dimension that changes): TIME (when something happens, how long it lasts, its timing, tempo, date,
  age), POSITION (place, location, orientation, distance, altitude), SIZE (size, length, extent, volume, shape),
  COLOUR (colour, hue, brightness, tint), INTENSITY (strength, loudness, degree, force, vigour, emotion level),
  QUANTITY (number, amount, proportion), OTHER (any other state or quality: freshness, health, temperature,
  social state, kind).
- OVER (what the change is described as varying over): TIME if the definition explicitly marks time (time words,
  "gradually", "slowly", "progressively", "with age", "in the course of", "over a period"); SPACE if the variation
  is across places, positions, distance or extent ("from place to place", "along its length", "with distance",
  "inclines", gradations across a surface); SIZE / COLOUR / INTENSITY / QUANTITY / OTHER if the definition makes
  the change a function of that dimension ("boils sooner as pressure falls" = TIME over OTHER); ITEMS if the value
  differs across a set of separate things or persons rather than along a dimension ("arrange at different times
  for different groups"); UNSPECIFIED if the definition says a change happens but not over what (most "become X"
  senses). Code what the definition SAYS, not what you know about the world.

## Analysis (frozen; `scripts/p65_change_verbs_analyze.py`)

- Agreement: Cohen's kappa for CHANGE (all items), and for DIM and OVER (items both coders call Y).
- Adjudication: items where coders A and B differ on CHANGE, DIM or OVER go to a third blind coder (codebook
  only, no prior codes). Final value per field = the value at least two of three share; else coder C's.
- **Falsifier (criterion b)**: a sense coded DIM = TIME with OVER in {SPACE, SIZE, COLOUR, INTENSITY, QUANTITY,
  OTHER} by BOTH coders A and B. Every such sense is reported verbatim with its dictionary and id. Senses where
  only one coder or only the final code says so are listed as disputed. DIM = TIME with OVER = ITEMS is listed as a
  near-miss, not a falsifier. Secondary (Navon's own wider sentence): DIM = POSITION with OVER in {SIZE, COLOUR,
  INTENSITY, QUANTITY, OTHER}, same rule.
- Zero falsifiers is a result only if the recall check and the plants pass.
- **Recall**: among recall-sample items with final CHANGE = Y, the share NOT in the candidate pool = filter miss
  rate (Wilson 95% interval), per dictionary. Also: among recall items with final DIM = TIME, the share outside
  the T-census.
- **Negative control (plants)**: all five must be flagged by the falsifier rule. Fewer than five = the falsifier
  check is NON-DISCRIMINATING to that extent, stated in the summary.
- **Positive controls**: share of Navon-verb senses coded CHANGE = Y whose OVER is TIME or UNSPECIFIED (grow,
  mature, fade) or SPACE (shade, slope gradient senses), reported, not gated.
- **Navon reading rule** (p. 226): UNSPECIFIED is reported beside TIME as evidence for change over time, never
  pooled silently.
- **Matrix**: rows DIM, columns OVER, final codes, (i) C-sample per dictionary and pooled; (ii) T-census;
  (iii) all coded items, de-duplicated, plants removed. Directional cells = OVER in the seven dimensions, off
  diagonal (X over X dropped).
- **Logical dependence (Garner 1976, p. 102 rival)**: a pair table frozen here, applied per hit. DEP(A→B) = Y if
  anything having a value on A must have a value on B. DEP(X→TIME) = Y for every X; DEP(TIME→X) = N for every
  X ≠ TIME; DEP(X→SPACE) = Y for POSITION, SIZE, COLOUR, and N for TIME, INTENSITY, QUANTITY, OTHER;
  DEP(SPACE→X) = N for X ≠ TIME; DEP between non-spatial non-temporal dimensions = N. Pure logical dependence
  predicts "A changes over B" only where DEP(A→B) = Y and DEP(B→A) = N. Directional hits with DEP(A→B) = N are
  reported: they are changes that dependence does not license, and they separate Navon from Garner's rival.

## Predictions (formal model, `p65_navon-formal-model_2026-11-13.md`), each PASS / FAIL / NOT TESTABLE

Dominance: "A changes over B" is one vote for B dominating A.
- **F5 (shape)**: on matrix (iii) pooled. Fit every linear order of the seven dimensions (7! = 5,040); loss = mass
  of items "A over B" where A is ranked above B. PASS if (1) the falsifier count is zero, (2) every minimum-loss
  order ranks TIME first and SPACE/POSITION second, and (3) loss under the best order with TIME first and POSITION
  second is at most 10% of directional items. FAIL if (1) or (3) fails, or a strictly better order exists that is
  not Navon's. NOT TESTABLE if fewer than 20 directional items. Controls: (a) permutation: 1,000 shuffles of OVER
  across directional items (row and column totals kept), minimum loss recomputed; p = share of shuffles with
  minimum loss ≤ observed (structure must beat shuffling, p < .05, or the order fit is NON-DISCRIMINATING);
  (b) planted reversal: the transposed matrix must put TIME last.
- **F2 (transitivity)**: triad TIME, POSITION, X, where X = most frequent DIM among SIZE, COLOUR, INTENSITY,
  QUANTITY in matrix (iii). For each pair, share a(i, j) = votes for i dominating j / all directional votes in
  the pair, Wilson 95%. A pair is testable if it has at least 5 votes, and clear if its interval excludes 0.5.
  FAIL if the three pairs form a cycle with all three clear; PASS if all three are testable and no cycle;
  NOT TESTABLE if any pair has fewer than 5 votes.
- **F3 (additivity)**: testable only if all three pairs have at least 5 votes and at least one vote in EACH
  direction (otherwise the logits come from the zero-cell correction, not data). Then with +0.5 cell correction,
  FAIL if a(TIME, X) is lower than max(a(TIME, POSITION), a(POSITION, X)); report predicted logit sum vs observed.
- Per-dictionary F5 is reported as descriptive; the verdicts above are on the pooled matrix.

## Limits stated in advance
Dictionary definitions are lexicographers' paraphrases, not usage; the 1973 Webster's itself remains unread;
model coders (subagents) are not human raters; GCIDE 1913 text is OCR-proofread volunteer data; Wiktionary
senses overlap with GCIDE (Wiktionary imported many 1913 Webster definitions, e.g. "fade").
