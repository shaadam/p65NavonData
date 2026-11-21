# P65 Unit 3: logical dependence in the corpus sentences. REGISTRATION (2026-11-19)

Status: REGISTERED. Written and committed before any sentence is coded for dependence. Decided by Adam 2026-11-19
(run before the Monday release; `docs/p65_v2_tests-plan_2026-11-19.md`, "Unit 3"). Before this commit the
registrant had read the definitional test's files, the change study's dependence table, and the first six rows of
the item file (to learn its format). No item was coded for dependence by anyone.

Last updated: 2026-11-19 12:40 (Eastern).

## Claim under test

Manuscript Section 6.2, logical dependence reading: logical dependence "fits the corpus direction too, but no corpus
sentence was coded for dependence, so that fit is not tested." This unit codes the corpus sentences for dependence
and tests the fit, copying the design of the post-hoc definitional test in the same section (branch
`claude/p65-definitional-dependence-2026-11-18`, folder `definitional/`, commits 23f39e2 codebook, bfadfc0 coders,
1bee21e counts, cd20ab8 and 7cd720f model, bafe36b recount).

## Sentences (fixed)

The same 243 directional sentences the definitional test used: every corpus sentence with a final label TP (time over
place: a place is stated and a time restricts when it holds) or PT (place over time: a time value is stated and a
place restricts where it holds). English 173 (146 TP, 27 PT), Indonesian 70 (49 TP, 21 PT); pooled TP share 195 of
243 = 0.802. Source file: `definitional/p65_defdep_items.tsv` on the branch above, sha256
`d9f2dbcda9b66ec19a129f1d1c2f33348000209baa8f7712a3d18b8271234681`, read as tab-separated with quoting off (a
quote-aware reader merges rows and finds 233). It is copied unchanged to `dependence/p65_dep_items.tsv`.

## Coding rule (fixed)

**Source table.** The change study's registered dependence table (`p65_change-verbs-registration_2026-11-14.md`,
"Logical dependence"): DEP(A to B) = Y if anything having a value on A must have a value on B; DEP(X to TIME) = Y for
every X; DEP(TIME to X) = N for X other than time; DEP(POSITION to SPACE) = Y. The verb rule: dependence licenses
"A changes over B" where DEP(A to B) = Y and DEP(B to A) = N.

**Adaptation from verbs to time-place pairings.** A pairing is DEPENDENT when the dimension stated under the other
logically requires it: in a TP sentence, the place stated requires the time; in a PT sentence, the time stated
requires the place. Read at the level of dimensions, the table makes every TP pairing dependent and every PT pairing
not, so dependence would equal direction and the test would be empty. The table is therefore applied at the level of
the thing that carries the stated value: the stated value requires the other dimension when, by the kind of thing
that carries it, it has no fixed value until the other dimension is given. The restriction itself never counts,
because every TP or PT sentence restricts its stated value by definition.

Three codes (coder text, frozen: `dependence/p65_dep_coder-brief.md`, sha256
`7c7bea08274967c6f68ac89f9117c754825aeb5578d283cc46205d376775bcee`):

- **S, strict.** Place stated: the located thing is somewhere only for a time by its kind (person, animal, vehicle,
  movable object, event, stay, weather). Time stated: the time value is local by the nature of time-keeping or the
  sky (clock reading, date, weekday, season, daylight, sun position), or is the time a moving thing passes a stop.
- **B, broad.** Place stated: a normally fixed thing (building, shop, institution, town) shown to have been or to be
  elsewhere at another time. Time stated: a time set by a custom, rule or schedule of the place.
- **N, not dependent.** Place stated: a thing fixed by kind or identity (mountain, lake, city, landmark, ruins).
  Time stated: the time of a single event or state that the place only locates or picks out.

Worked minimal pairs (in the brief): "At noon the ferry is at the pier" S / "At noon the lighthouse is at the end of
the pier" N; "In 1990 the bakery was on Main Street, before it moved" B / "In 1990 the cathedral was on Main
Street" N; "In Jakarta it is already evening" S / "In Jakarta the opening ceremony was on a Monday" N; "At this stop
the last bus leaves at 11:40" S / "In this town the shops close at six" B.

**Primary:** DEPENDENT = S (strict, the "logically requires" reading). **Broader coding (sensitivity, as the
definitional test's broad rule):** DEPENDENT = S or B.

## Coders and planted items (fixed)

Two blind model coders in fresh contexts, one Opus subagent and one Sonnet subagent. Each receives only the coder
brief and a blind file: 249 rows (243 items and 6 plants), shuffled with seed 20261119, ids D0001 to D0249, columns
`did`, `frame` (PLACE-STATED for TP, TIME-STATED for PT), `previous_sentence`, `sentence`. No corpus label, no
hypothesis, no author or study named. The id-to-item map stays with the analyst.

The frame is shown because the code is defined on the stated value. To stop a coder from coding by frame alone, the
plants flip it: a coder who codes every PLACE-STATED row S and every TIME-STATED row N misses four of six. Plant text,
frozen (expected primary code in brackets):

| id | frame | previous sentence | sentence | expected |
|---|---|---|---|---|
| PL1 | PLACE-STATED | We looked everywhere for him. | At nine he was still at his aunt's house. | S |
| PL2 | PLACE-STATED | The road climbs steeply. | Even in midwinter the old fort sits on the ridge above the town. | N |
| PL3 | PLACE-STATED | Kotanya kecil. | Sampai sekarang pun danau itu terletak di sebelah utara kota. | N |
| PL4 | TIME-STATED | The call came from abroad. | In Sydney it was already Saturday morning. | S |
| PL5 | TIME-STATED | Kami menelepon keluarga di rumah. | Di Jayapura waktu itu sudah pukul sembilan malam. | S |
| PL6 | TIME-STATED | The conference had three days of talks. | In the main hall the keynote was on the Tuesday. | N |

Plants are scored first, on the primary binary (S against B or N). A coder missing 2 or more of 6 is UNTRUSTED: its
codes are reported but not used for the final codes, and the final codes then come from the trusted coder with the
analyst's adjudication of that coder's confidence-1 items; if both are untrusted the unit reports NOT TESTABLE with
the coders' raw codes.

Agreement: Cohen's kappa on the primary binary over the 243 real items (plants excluded), also on the broad binary,
and quadratic-weighted kappa on the three-level code (order N < B < S).

## Adjudication (fixed)

Items where the two trusted coders differ on the three-level code are adjudicated by the analyst with the sentence
and previous sentence in view and the brief as the only rule, recording a one-line reason per item. The analyst sees
the frame (as the coders did) but adjudicates before the analysis script is run on final codes. Sensitivity rows,
both reported: union (dependent if either coder says S) and intersection (both say S); and the same two for the
broad rule.

## Predictions (fixed before coding)

Statistic: s0 = TP share among non-dependent pairings, pooled over both languages, raw counts, exact
(Clopper-Pearson) 95% interval [lo, hi]. Overall pooled TP share: 0.802.

- **Logical dependence:** the direction comes from dependence, so among non-dependent pairings nothing pushes it:
  s0 falls toward one half. Also the dependence odds ratio (odds of TP among dependent over odds of TP among
  non-dependent) exceeds 1.
- **Navon's hierarchy:** direction is set by the hierarchy, not by dependence: s0 stays near the overall share, and
  the odds ratio is near 1.

Verdict rule, on the primary codes, pooled:

| outcome | logical dependence | Navon's hierarchy |
|---|---|---|
| [lo, hi] covers 0.5 and excludes 0.802 | SUPPORTED | NOT SUPPORTED |
| lo > 0.5 and [lo, hi] covers 0.802 | NOT SUPPORTED | SUPPORTED |
| lo > 0.5 and hi < 0.802 | PARTLY (falls, stays above half) | PARTLY (stays above half, falls) |
| [lo, hi] covers both 0.5 and 0.802 | UNDECIDED | UNDECIDED |
| hi < 0.5 | NOT SUPPORTED as stated (non-dependent pairings lean place over time); reported | NOT SUPPORTED |
| fewer than 10 non-dependent pairings | NOT TESTABLE (dependence near universal); reported | NOT TESTABLE |

Per-language shares (English, Indonesian) are reported beside the pooled verdict, descriptive only. A known limit,
stated now: because the code is defined on the stated value, its base rate can differ between TP and PT sentences for
reasons of subject matter (people move; clocks are local). That difference is what the logical-dependence account
claims drives direction, so it is not removed; the odds ratio and s0 are read as the fit of that account, not as a
causal estimate.

## Model (fixed; the definitional test's model with dependence in place of definitional status)

`dependence/p65_dep_assoc.py`, adapted from `definitional/p65_defdep_assoc.py` (only the input file and column name
change): count table by direction, dependence and language; Fisher exact per language; exact conditional common odds
ratio across the two language strata with exact 95% interval; Mantel-Haenszel common odds ratio; Firth-penalised
logistic regression TP ~ dependent + language, and with the interaction, profile-penalised 95% intervals; predicted
TP share for non-dependent sentences per language (the counterpart of the definitional test's 87% English and 73%
Indonesian). Run on primary, broad, union and intersection codes. Second route sharing no code: Wolfram, adapted from
`definitional/p65_defdep_assoc.wls`, through `scripts/wolfram-run.sh`, on the primary codes.

Controls: (1) shuffle control, dependence labels permuted within language (2,000 permutations, seed 6518) must
remove the association; (2) synthetic collapse control, the pipeline run once on synthetic codes with every TP item
dependent and no PT item dependent must report s0 undefined or 0 with the odds ratio at the upper limit, and on
codes with every PT item dependent and no TP item must report s0 = 1; (3) plants, above.

## Report either way

Every outcome in the verdict table is reported, including NOT TESTABLE and UNDECIDED, with counts, the odds ratio and
interval, s0 and per-language shares, plants, kappa, and the sensitivity rows. A proposed manuscript paragraph
replaces "but no corpus sentence was coded for dependence, so that fit is not tested" with what was found. The
manuscript is not edited by this unit.

## Files

`dependence/` in worktree `/Users/as/_Claude/Claude/worktrees/p65-stats-fix` (branch
`claude/p65-stats-fix-2026-11-17`): brief, items, blind file, map, coder outputs, adjudication, final codes,
analysis scripts and run logs. Results: `docs/p65_unit3-dependence_results_2026-11-19.md`.

## Addendum A: direction-blind re-test (registered 2026-11-19, before any direction-blind coding)

Status: REGISTERED by the adversarial pass (main-session brief, 2026-11-19). Written after the primary results
(commit 1e4cd77) were known and after the circularity analysis (commit 9112a79), before any item was coded under
this addendum.

**Why.** The rule above asks a different question on each side: on TP rows whether the place needs a time, on PT
rows whether the time needs a place. The coder sees the frame. The label therefore depends on the outcome, and the
statistic s0 is fixed by the two questions' base rates alone (s0 = nTP(1-a)/(nTP(1-a)+nPT(1-b)), a = 171/195,
b = 19/48). In a simulated world where direction is independent of both dependence facts, the registered verdict
table returns "logical dependence SUPPORTED" in 92% of 5,000 runs and "hierarchy SUPPORTED" in none
(`dependence/adversarial/p65_depadv_circularity_run_2026-11-19.txt`). The re-test asks both questions of every item,
with the direction hidden.

**Extraction.** A Sonnet subagent with no hypothesis and no direction labels copies, from each of the 243 sentences,
the time expression, the place expression, and the entity involved as a bare noun phrase with no verb
(`p65_depadv_extracted.tsv`). Departure from the brief's "two expressions only", in one line: dependence by kind
is a property of what is located (a ferry versus a lighthouse at the same pier), so an expression pair without the
entity cannot be coded; the entity is given as a verbless noun phrase so that no syntax survives.

**Blind file.** 249 rows (243 items, 6 plants), shuffled with seed 20261120, ids B0001 to B0249, columns `bid`,
`entity`, `expr_1`, `expr_2`; the time and place expressions are assigned to `expr_1` and `expr_2` by a per-row coin
(same seed). No sentence, no frame, no corpus label. Map kept by the analyst.

**Rule.** Brief `dependence/adversarial/p65_depadv_coder-brief.md`, sha256
`125a268e23ce80ed3787a48c3fec88ff1b3b97e691e441f2dc47e8fac9c13d44`. Two questions per row, each by kind: Q-PLACE,
where the entity is has no fixed value until a time is given; Q-TIME, the time value has no fixed value until a place
is given. Codes P (place requires time only), T (time requires place only), BOTH, NEITHER.

**Plants** (`p65_depadv_plants.tsv`, sha256 `bc796816bb8bc67fb9fb263e1de353656669ac7824ba1dd25cd1314b6d31f4bb`),
none identical to a brief example: stray dog / all afternoon / under the bridge = P; waktu setempat / pukul sembilan
malam / di Jayapura = T; the last bus / at 11:40 / at this stop = BOTH; the old fort / since the eighteenth century /
on the ridge = NEITHER; danau itu / sampai sekarang / di sebelah utara kota = NEITHER; anak-anak / selama dua minggu
/ di rumah nenek = P. Scored first on the four-level code; a coder missing 2 or more is UNTRUSTED.

**Coders.** One Opus and one Sonnet subagent, fresh contexts, brief and blind file only. Cohen's kappa on the
four-level code over the 243 items. Disagreements adjudicated by the analyst from the blind file only (entity and
expressions), and the adjudication file is committed before the map joins direction to codes.

**Statistic and predictions.** TP share, exact Clopper-Pearson 95% interval, in each cell P, T, BOTH, NEITHER.
Logical dependence predicts TP share high in P, low in T, near one half in NEITHER. Navon's hierarchy predicts the
share near the overall 0.802 in every cell, in particular in NEITHER and T.

**Verdict on the unit 3 result** (pooled, adjudicated codes):

| outcome | verdict |
|---|---|
| NEITHER interval covers 0.5 and excludes 0.802, and the TP share in T is below that in P (Fisher two-sided p < 0.05) | CONFIRMED |
| No direction-blind association: TP share in P against T plus NEITHER, Fisher p >= 0.05, and the NEITHER interval covers 0.802 or lies above it | CIRCULAR |
| Any other outcome | PARTLY |

Small cells: if NEITHER has fewer than 10 items, the NEITHER criterion uses NEITHER plus BOTH (no unique licence);
if T has fewer than 5, the contrast is P against T plus NEITHER. Sensitivity: coder 1 alone, coder 2 alone, items
where both agree. Also reported: the share of TP items whose time is local (Q-TIME yes), which the original rule
never asked.
