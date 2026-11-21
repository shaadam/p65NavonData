# P65 v2 Unit 4: spatial uses of the dictionary study's change verbs in corpus usage. REGISTRATION (2026-11-19)

Status: REGISTERED before any corpus sentence is read or coded. Written and committed before extraction output is
opened. Done before this file: the 121 directional senses were listed with their headwords
(`change-verbs/unit4/p65_unit4_verblist.py`, output `p65_unit4_directional-senses.tsv`), the six corpus files were
checksummed against `wave3/p65_wave3_ud-checksums_r2.18.tsv` (all six match), and matching verb tokens were COUNTED
per lemma (915 tokens, 38 lemmas). No sentence text was looked at.

Plan: `docs/p65_v2_tests-plan_2026-11-19.md`, Unit 4. Adam decided 2026-11-19 to run it before the Monday release.

## Claim tested

Manuscript 6.4 Limitations: "Spatial-extent uses such as 'the road widens' exist in speech without a dictionary
sense of their own, so change over space is under-counted" in the dictionary change study (112 of 121 directional
senses vary over time; 9 of 121 do not: 6 over space, 1 over colour, 2 over another dimension).

## Verb list (frozen)

Source: the 121 directional senses of the dictionary study (`p65_change-verbs-registration_2026-11-14.md`, final
codes from `change-verbs/codes/`, plants removed, matrix (iii) pooled). Lemmas = every single-word headword, plus
every single-word member of a WordNet synset headword (for example "turn|grow" gives turn and grow). Multi-word
headwords (phrasal verbs and idioms such as "run out", "wear thin", "age like a fine wine") are excluded because a
lemma match cannot find them; their single-word head is included only when it is itself a headword or synset
member. Lowercased. 81 lemmas:

alternate ameliorate amortize anneal temper normalize bioaccumulate break checker chisel co-vary convalesce crash
creep dawn daypart decrease depreciate develop drip-feed evanesce fade fleet pass explode filter fine flit gather
glean graduate grizzle grow interchange iterate knit lull marinate mature mellow migrate mushroom overfish
overprint phase plateau proliferate pulse refract reoxidize rust scaffold scrape scratch shade shawshank shift
shoot sink slug soil stale step superannuate time-change track turn uptalk vanish fly vaporize vary wear wipe
wizen melt

Token counts (counted before registration, sentences unseen): 915 VERB tokens of 38 lemmas; 43 lemmas have none.
Largest: turn 138, grow 137, develop 101, pass 85, break 68, wear 64, fly 50.

## Corpus (frozen)

Universal Dependencies release 2.18, the files the corpus study used (fetched by
`scripts/p65_wave3_ud_fetch.py`; held at `/Users/as/_Claude/p65Spacetime_Claude/data/ud/r2.18/`, not committed):
UD_English-EWT en_ewt-ud-{train,dev,test}.conllu and UD_English-GUM en_gum-ud-{train,dev,test}.conllu. sha256 as in
`wave3/p65_wave3_ud-checksums_r2.18.tsv`.

## Extraction (frozen)

A use = one token with UPOS = VERB whose lowercased LEMMA is in the list. Every use is coded (no sampling). The item
shown to coders is the sentence text (`# text`, or tokens joined if absent) with the target token wrapped in
[[ ]]; two targets in one sentence are two items. Item ids are random (seed 20261119), order shuffled per coder
(seeds 1 and 2). Coders see id, marked sentence and lemma only; not the corpus, genre or sentence id.

## Codebook (frozen; given verbatim to each coder)

You will see English sentences with one verb marked [[like this]]. For each, decide how the marked verb is used.
Code what the sentence says.

- TEMPORAL: the verb describes something becoming different as time passes: an event or process of change
  (grows, fades, develops, breaks, melts, turns into, moves somewhere, decreases). Time need not be named. Motion of
  a thing from one place to another is TEMPORAL (its position changes over time).
- SPATIAL: nothing needs to happen in time; the verb describes a value differing from one place to another along a
  path, surface or extent, as in "the road widens toward the coast", "the trail turns north after the bridge",
  "the hills shade from green to brown further inland". Static layouts described with motion or change words count
  here.
- OTHER-DIM: the verb describes a value changing as a function of some dimension that is neither time nor space,
  as in "the boiling point varies with pressure".
- ACROSS-ITEMS: the verb says values differ across a set of separate things, people or cases, not along one
  dimension, as in "prices vary from shop to shop", "opinions vary".
- NOT-CHANGE: the verb is not used to describe a change or a difference in some value (for example "pass the
  salt", "graduate from college" as an act, "track the package", "shoot a photo", "wear a hat").
- UNCLEAR: the sentence is too short, garbled or ambiguous to decide.

Output one line per item: id <TAB> code. Use exactly one of the six codes.

## Plants (negative and positive controls; text frozen)

Five constructed sentences, inserted with ids indistinguishable from real ones, known answers:
- P1 SPATIAL: "Beyond the old bridge the trail [[turns]] sharply north and follows the ridge to the summit."
- P2 SPATIAL: "The cliff face [[shades]] from deep red at its base to pale yellow near the top."
- P3 TEMPORAL: "Over the summer the puppy [[grew]] to almost twice its size."
- P4 NOT-CHANGE: "Could you [[pass]] me the report when you are done with it?"
- P5 OTHER-DIM: "The boiling point of the mixture [[varies]] with the pressure in the vessel."

Plants are scored first. A coder who misses 2 or more plants is untrusted: their codes are not used, and a
replacement coder of the same model is run once with fresh shuffling. Plants are removed before every analysis.

## Coders and adjudication

Coder A: a Claude Opus subagent; coder B: a Claude Sonnet subagent. Each in a fresh context, given the codebook and
the items only; the hypothesis, the dictionary numbers and the manuscript are not named. Agreement: Cohen's kappa on
the six codes over real items, and on the collapsed primary variable (SPATIAL / TEMPORAL / OTHER-DIM / not
directional). Disagreements are adjudicated by the main analyst (this agent) with the sentence in view, blind to
which coder said what is not possible, so the adjudication rationale is written per item. Final code = agreed code,
else the adjudicated code.

## Prediction and test (frozen)

Directional uses = final code SPATIAL, TEMPORAL or OTHER-DIM (the usage counterpart of a directional sense: a change
that runs over some dimension).

- Prediction: the SPATIAL share of directional uses exceeds the dictionaries' share of directional senses not over
  time, 9 of 121 (0.074).
- Primary test: Fisher's exact test, two-sided, alpha .05, on the 2 x 2 table [usage SPATIAL, usage not SPATIAL]
  versus [dictionary not-over-time 9, dictionary over-time 112]. Secondary: exact binomial test of the usage count
  against p0 = 9/121, two-sided. Shares carry Wilson 95% intervals.
- Verdict: SUPPORTED if the usage share is higher and Fisher p < .05. CONTRADICTED if lower and p < .05. NOT
  SUPPORTED (no detectable difference) otherwise.
- Sensitivity (reported, not verdicts): (a) usage SPATIAL share against dictionary SPACE-only 6/121; (b) usage
  non-temporal share (SPATIAL + OTHER-DIM) against 9/121; (c) codes from each coder alone; (d) SPATIAL share of all
  uses, including non-directional.
- Per-lemma counts of SPATIAL uses are reported, and every SPATIAL use is listed verbatim.

## Stopping and reporting rule

All 915 uses are coded once by each coder; no interim look, no added verbs, no re-run except the untrusted-coder
replacement above. The outcome is reported either way, in
`docs/p65_unit4-spatial-change-verbs_results_2026-11-19.md`, with a paragraph for the manuscript whichever way it
goes. The manuscript is not edited by this unit.

## Limits stated in advance

The list holds few extent verbs: "widen", "narrow", "slope", "rise" are not among the 121 directional senses, so this
tests the verbs the dictionary study counted, not spatial-extent verbs at large. EWT (web text) and GUM (mixed
genres, some spoken) are written-heavy, not speech. Coders are AI models, not human raters. The analyst adjudicates
knowing the hypothesis; each adjudication carries its sentence and reason in the results data so it can be audited.

Scripts: `change-verbs/unit4/p65_unit4_extract.py` (items and key), `p65_unit4_analyze.py` (plants, kappa, shares,
tests). Data: `change-verbs/unit4/` (sentence ids and codes; sentence text from CC BY-SA EWT and GUM is kept in the
coder item files, attributed).

## Addendum B (2026-11-19): spatial-extent change verbs (unit 4b). REGISTERED before any unit 4b use is extracted

Why: unit 4 tested the dictionary study's own verbs and found 3 spatial uses of 499 directional uses. The
Limitations' examples, "widen" and "slope", were not on that list (stated above under "Limits stated in advance").
Unit 4b asks the same question of spatial-extent verbs. Requested by the coordinating session for Adam, 2026-11-19.

**Verb list (frozen, drawn by rule, not by hand).** `change-verbs/unit4/p65_unit4b_verblist.py` on WordNet 3.1
(`wn3.1.dict.tar.gz`, sha256 3f7d8be8...1c22a, the file the dictionary study used). A verb synset qualifies when its
lexicographer file is verb.change, verb.motion or verb.stative and its definition (gloss before any example) contains
a spatial-extent word (wide, broad, narrow, deep, shallow, thick, steep, slope, slant, incline, angle, taper, height,
tall, elevation, upward, downward and their listed inflections). A single-word lemma of a qualifying synset is listed
when that synset is one of the lemma's two most frequent WordNet verb senses. The 76 unit 4 lemmas are removed. Result,
45 lemmas: acuminate angle bottleneck broaden camber climb cock descend dilate distend embrace encompass fall fathom
flare ford foreshorten gape glance globalise globalize incline inspissate jackknife lean narrow rise scend shallow
shoal skew slope snowboard squat steepen supinate tend thicken thin tilt wade weather widen yaw yawn. Of the examples
named in the request, taper and deepen are outside the rule (their extent senses are not among their two most frequent
senses); they are not added by hand.

**Usage side.** Every UPOS VERB token of a listed lemma in the six EWT and GUM r2.18 files, extracted and marked
exactly as unit 4 (`p65_unit4b_extract.py`, unit 4's extractor with the list and plants changed). If more than 1,200
real uses exist, a uniform random sample of 1,200 is coded (seed 20261121), and the sample size is stated.

**Dictionary side.** Every WordNet 3.1 verb sense of the 45 lemmas (160 senses: lemma, gloss, WordNet's examples),
written by the same script. This replaces the dictionary study's 9/121 benchmark for these verbs: the comparison is
the same verbs' senses.

**Codebook.** Unit 4's codebook, verbatim, six codes. Senses are coded with the same codes, applied to what the
definition says. Collapse for the test: directional = SPATIAL, TEMPORAL or OTHER-DIM; SPATIAL vs the other two.

**Coders.** Coder A: ChatGPT (High setting, a regular chat run by Adam), uses and senses in one job, items shuffled
together, 5 plants with known answers among the uses. Coder B: a Claude Opus subagent on the same items afterwards,
blind, fresh context. Agreement and adjudication as unit 4. A coder missing 2 or more plants is untrusted, as unit 4.

**Prediction and test (frozen).** Prediction: among directional items, the SPATIAL share of uses exceeds the SPATIAL
share of the same verbs' WordNet senses. Primary test: Fisher's exact test, two-sided, alpha .05, on [uses SPATIAL,
uses other directional] x [senses SPATIAL, senses other directional]. Verdict words as unit 4 (SUPPORTED, CONTRADICTED,
NOT SUPPORTED). Sensitivity: each coder alone; senses of the qualifying synsets only; per-lemma SPATIAL counts, every
SPATIAL use listed. Reported either way, in a results file for unit 4b; the manuscript is not edited by this unit.
