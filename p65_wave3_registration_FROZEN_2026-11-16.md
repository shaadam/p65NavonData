# p65 wave 3: does time over place hold across languages? REGISTRATION (FROZEN 2026-11-16, one-language run)

Last updated: 2026-11-16 (Eastern); scope narrowed to one language (Indonesian census) after independent verification, branch claude/p65-wave3-verify-2026-11-16

**Status: FROZEN 2026-11-16 for the one-language (Indonesian census) run, before any Indonesian sentence is coded; no direction has been seen in any language other
than English. Section 13 is the freeze addendum. Sections for the extension languages remain drafts.** Adam or the next session freezes it, after deciding the items in Section 11. Everything marked
"rwj default" is a call made under the trial rule, which Adam may override before the freeze.

**Scope (Adam, 2026-11-16, via the coordinator): the first preprint adds ONE language to English. The other languages
are a listed future extension, run as a revision or a second article under the same design.** The one language is
**Indonesian** (ranking and reasons: `p65_wave3_design-verify_2026-11-16.md` Section 3), coded as a **census of its
6,628 sentences, double-coded** (Design A, scheme D1): a census needs no sampling weights, no stopping rule and no
coder-2 gating, so the parts of this draft that describe Design C and hybrid coding D3 (Sections 2.2, 2.3, 5.1) apply
to the extension languages only and are kept for them. Where a section below speaks of "ten languages" or "per
language", read it as the extension; the first preprint's own analysis is Section 6.5. The verification of the design
behind this draft is in `p65_wave3_design-verify_2026-11-16.md` (estimator, stopping rule, hybrid coding, cost; every
numeric claim recomputed by independent code with a control that fires).

Inputs: sampling design `wave3/design/p65_wave3_sampling-design_2026-11-16.md` (70d5b43, a3b7480); feasibility `p65_wave3-feasibility_2026-11-16.md` (c517884); treebanks `scripts/p65_wave3_ud_fetch.py` and
`wave3/p65_wave3_ud-checksums_r2.18.tsv` (48e0d4b); yield pilot `wave3/pilot/p65_wave3_yield-pilot_2026-11-16.md`
(fba9396); power `docs/manuscript/p65_appendix-D_math_2026-11-16.md` D.5 and D.6; codebook v3.1
`wave2/p65_codebook-v3.1_sec1.md`; wave 2 registration and Addenda 1 to 6 `p65_wave2_registration_2026-11-16.md`.

## 0. What this registration does, and the four facts that shape it

Navon (1978) proposed that people conceive of time as dominating place: a time setting restricts what holds at a
place more often than the reverse. In English text, Arms A, A3 and A3b found time over place in about three of every
four directional sentences (A3b share 0.823, 95% document interval 0.728 to 0.906; exploratory, kappa 0.576). One
language cannot carry a claim about human conception. Wave 3 asks whether the same direction holds in other
languages, and how much languages differ.

1. **The question is one pair, time and place.** Wave 3 codes only that pair. Wave 2 showed that asking coders to
   inventory six dimensions breaks agreement on presence: time-place kappa fell to 0.376 in pilot 2 (n 58), against
   0.789 (Arm A, n 500) and 0.676 (A3, n 1,500) when time-place was coded alone under protocol v2. Most pilot 1
   disagreements (76 of 84) were about whether a dimension was present, not about direction (Addendum 3).
2. **Languages matter more than items.** Appendix D.6: past about 100 independent time-place directional items per
   language, more items barely move power; more languages do. Eight languages suffice if languages differ by a logit
   standard deviation of 0.5; at 1.0, twelve give 0.90 and eight plateau at 0.72.
3. **The screen recalls time-over-place better than place-over-time.** On English, the presence screen catches 0.77
   of time-over-place sentences and 0.37 of place-over-time ones (the PT interval runs 0.18 to 0.67). A draw of
   flagged sentences alone would inflate the time-over-place share. **No wave 3 estimate may rest on flagged
   sentences without a sample of the unflagged sentences drawn at a known rate** (Section 2).
4. **Expected yield is short in two languages.** Coding every sentence, the expected directional items are Hindi 532,
   Arabic 355, Finnish 225, Indonesian 164, Turkish 160, Japanese 127, Naija 74 and Mandarin 65, with Persian 365 and
   Korean 229 as reserves. These carry English's precision over to each language, so each has about a factor-of-two
   band.

## 1. Languages and treebanks

All from Universal Dependencies release **r2.18** (the release Arm A's English codes were made on; r2.19 exists and is
not used, so every language shares one release). Fetched by tag; checksums of every file committed (48e0d4b). Text is
not redistributed: the repository holds sentence IDs and codes only.

| # | language | family; region | treebank(s) | sentences | licence | expected directional (census) | role |
|---|---|---|---|---|---|---|---|
| 1 | **Indonesian** | Austronesian; Southeast Asia | GSD + CSUI | 6,628 | CC BY-SA 4.0 | 164 (feasibility's alternative expectations 113 and 155) | **first preprint: census, double-coded** |
| 2 | Arabic | Afro-Asiatic, Semitic; Middle East | PADT | 7,664 | CC BY-NC-SA 3.0 | 355 (likely high: 32% of sentences flagged, precision unmeasured) | extension, first in line |
| 3 | Finnish | Uralic; Northern Europe | TDT | 15,136 | CC BY-SA 4.0 | 225 | extension |
| 4 | Hindi | Indo-European, Indo-Aryan; South Asia | HDTB | 16,649 | CC BY-NC-SA 4.0 | 532 | extension |
| 5 | Japanese | Japonic; East Asia | GSD | 8,100 | CC BY-SA 4.0 | 127 | extension |
| 6 | Turkish | Turkic; West Asia | BOUN (Kenet only by rule T, below) | 9,761 | CC BY-SA 4.0 | 160 | extension |
| 7 | Mandarin | Sino-Tibetan; East Asia | GSD + HK | 6,001 | CC BY-SA 4.0 | 65 | extension, expected short |
| 8 | Naija (Nigerian Pidgin) | English-lexified creole; West Africa | NSC | 9,241 | CC BY-SA 4.0 | 74 | extension, expected short; weak independence from English |
| 9 | Korean | Koreanic; East Asia | Kaist | 27,363 | CC BY-SA 4.0 | 229 | extension (rwj default) |
| 10 | Persian | Indo-European, Iranian; West Asia | PerDT | 29,107 | CC BY-SA 4.0 | 365 | extension (rwj default) |

**Why Indonesian first** (criteria in Adam's order, `p65_wave3_design-verify_2026-11-16.md` Section 3): it is
non-Indo-European; it marks place (`di`) and time (`pada`) with distinct words, where Arabic `في`, Finnish inessive and
adessive, Turkish `-DA`, Korean `-에` and Japanese `に` each cover both, so the screen's two dimensions stay apart; a
census of its 6,628 sentences is the cheapest robust option in the set (about $110 double-coded, Latin script, so no
non-Latin token factor), and a census codes every directional sentence the treebank holds, so the yield borrowed from
English (164, with a factor-of-two band) stops being a risk: the feasibility note's lower expectation, 113, still clears
100; its genre (news, blog) overlaps the English Web Treebank; its licence is CC BY-SA 4.0. Against it: it is SVO and
analytic, so typologically nearer English than Arabic or Finnish; a census yields fewer items than Hindi's or Arabic's.
Arabic is the natural second language (census about $190, 355 expected items; NC licence and newswire-only genre to be
stated). Indonesian GSD and CSUI carry no document IDs, so the clustering unit is the sentence (Section 6.1).

**Extension (ten languages, rwj default ten not eight).** Mandarin and Naija are expected below 100. Adding the two
reserves keeps eight languages expected above 100, and moves the count toward the twelve that Appendix D needs if
languages differ widely. Cost: Section 2.3. Persian and Hindi share a family (Indo-European), which the model in
Section 6 treats as two languages, not two families; a family-level sensitivity is listed in Section 6.4.

**Rule T (Turkish).** Kenet (18,687 dictionary example sentences) is added to Turkish only if the Turkish pilot
(Section 3) measures a directional yield that projects below 100 for BOUN. Kenet's genre (constructed dictionary
examples) is stated wherever it is used.

**Coverage gap, stated in every report of wave 3.** The set has **no language of the Americas** and **no sub-Saharan
language other than an English-lexified creole**. Yoruba (317 sentences) and Wolof (2,107) have UD treebanks too small
to yield 100 items; Hausa (4,342, pooled) is short; K'iche' and Puno Quechua are far smaller; Aymara, the language
with the best-known "past ahead" contrast, has no treebank. The universality claim, if supported, is a claim about
these ten languages, eight families plus an English-lexified creole, and four macro-areas (Asia, Europe, North Africa and the Middle East, West Africa
through Naija), not about human languages in general.

## 2. Draws and seeds

### 2.1 The pilot draws (already fixed, direction-blind)

The 500-sentence draws of the yield pilot (seed 20261130, per-language string seed `20261130:<language>`,
`wave3/pilot/p65_wave3_yield-draw_<language>.tsv`, fba9396) are the wave 3 pilot. They were drawn uniformly from the
train, dev and test files of each treebank, before any wave 3 code. Each language's 500 are coded by both coders
(Section 4). Pilot sentences stay in the main run; their codes are reused, so pilot and main run are one census or
one frame (Section 2.2), not two samples.

### 2.2a The first preprint's main run: Indonesian census (Design A), double-coded

Every sentence of Indonesian GSD and CSUI (train, dev, test; 6,628, the pilot's 500 among them) is coded by both coders
and adjudicated (Section 5.1, scheme D1). Order of coding: one uniform random permutation of the sentences not in the
pilot (seed 20261131, string seed `20261131:Indonesian`), in batches of 400; the screen flag is recorded but plays no
part in the draw, the estimate or the stopping, which is exhaustion of the treebank. No weights: the share is the plain
share of time-over-place among final TP and PT labels, with a 95% logit-scale interval, sentence as the unit (no
document IDs). If the budget cap (Section 2.3) stops the run early, the coded sentences are a uniform sample of the
treebank and the analysis runs on them with the achieved count stated (rule Y applies to the count).

### 2.2 The extension's main run: Design C, two-phase stratified, sequential (rwj default, replaces Design B)

**In plain language.** The screen splits each treebank into flagged and unflagged sentences. Both groups are sampled at
known rates, the flagged group somewhat more densely, and each coded sentence counts in proportion to how many
sentences it stands for. Coding goes in batches and stops, language by language, when the coded sentences carry the
precision of 100 independent directional items. The stopping rule never looks at direction.

- **Strata.** Per language, the broad screen of the yield pilot (`scripts/p65_wave3_yield_pilot.py`, fba9396) splits the
  treebank into F (flagged) and U (unflagged). Both are fixed now; the counts are in the pilot run file.
- **Order of coding.** Within each stratum, a uniform random permutation of the sentences not in the pilot (seed
  20261131, string seed `20261131:<language>:<F or U>`). Each batch of 400 takes the next sentences of each
  permutation in the ratio n_F : n_U of the planning allocation (design note, Part 2 at planning share 0.74; for
  example Hindi 969 : 1,931, Korean 1,587 : 7,476). The pilot's 500 uniform sentences join their strata; within a
  stratum, the pilot plus the permutation's first k sentences are a simple random sample, so inclusion probabilities
  stay n_h / N_h.
- **Estimator.** The share is the weighted ratio Σ w d y / Σ w d, w = N_h / n_h, with the linearised variance
  (design note, DERIVE), document-clustered by a bootstrap within stratum where the treebank has document IDs.
- **Stopping rule (per language, direction-blind).** After each batch the checker computes, over coded items with a
  final label TP or PT pooled (never split), the Kish count K = (Σ w d)² / Σ w² d, and the count of directional items
  coded in U. The language stops when K ≥ K\* and at least 20 directional items have been coded in U, or when both
  strata are exhausted (census). K\* is fixed at the freeze from the pilot's counts (English value 128.8, equivalent to
  100 effective items). Mandarin and Naija start as a census (their expected total, 65 and 74, is below 100 at any
  size). Proposition in the design note: a rule using only the sampling and the directional-or-not status keeps the
  fixed-design error rates (CONDITIONAL on directions being independent given stratum and status; simulated type I
  0.051 against 0.294 for a rule that peeks at direction).
- **Compared and not chosen.** Census (Design A): $2,910, meets the target in the same eight languages, 2.4 times the
  cost. Draft Design B (all flagged plus 1,500 unflagged): $757 with the pilot, but 26 to 182 effective items, under 60
  in seven of ten languages, because it samples the flagged group 6.9 times as densely as the unflagged one when the
  optimum is 1.8. Flagged only: biased by +0.12 in the share; not allowed.

**What sampling cannot do.** Mandarin and Naija are short of directional sentences, not of money. A census of their
treebanks reaches about 65 and 74 effective items and no design exceeds the census. They stay in, coded in full,
because the cross-language tests gain more from a language than from items; their own direction tests follow rule Y.

### 2.3 Cost and precision, as estimates

**First preprint (Indonesian census, double-coded).** 6,628 sentences at $0.0165 per sentence (wave 2's measured
per-item prices: Opus coder $0.0068, Sonnet coder $0.0035, adjudication $0.0177 per row at 0.25 rows per sentence, plus
the measured per-job harness overhead at batches of 400; Latin script, so no non-Latin factor): **central $110, cap
$165** (×1.5, fail closed as wave 2 Section 7). Expected effective items 164 (every directional sentence; 113 at the
feasibility note's lower expectation), half-width about 0.067 at 164 items and 0.081 at 113, planning share 0.74.
Money is Adam's decision.

**Extension (ten languages).** At the draft's anchor of $0.0215 per sentence (wave 2's measured-based $0.0143, times an
assumed 1.5 for non-Latin scripts), ten languages, pilot included. Effective items are per language at planning share
0.74; the half-width is the 95% half-width of a language's share. The independent verification
(`p65_wave3_design-verify_2026-11-16.md` row 4a) puts the same designs at $1,304 (D1) and $893 to $969 (D3) from the
per-item prices with harness overhead; the caps below hold only while the ×1.5 token factor holds, which the pilot
measures.

| design | sentences | cost | effective items per language | half-width |
|---|---|---|---|---|
| A census, double-coded | 135,650 | $2,910 | 65 to 535 | 0.037 to 0.106 |
| B draft (flagged + 1,500 unflagged) | 35,280 | $757 | 26 to 182 | 0.064 to 0.167 |
| **C, double-coded (D1)** | **55,628** | **$1,193** | **100; Mandarin 65, Naija 74** | **0.086; 0.106, 0.100** |
| **C, hybrid coding (D3, Section 5.1)** | **about 65,600** | **$793** | as C | as C |

Caps (fail closed, as wave 2 Section 7): central times 1.5, so **$1,790 for C with D1 and $1,190 for C with D3**. The
sequential rule moves spend toward languages whose yield turns out below English's (a language at half English's
yield needs about twice the sentences); a language reaching its census stops there. If unflagged sentences cost 1/1.3
as much as flagged ones (assumed, not measured), C with D1 costs $967. Money is Adam's decision.

## 3. Pilot and what it decides

The pilot (2.1) is coded by both coders and adjudicated. Before any direction count is opened, it yields, per
language: presence agreement, the agreement statistics of Section 5, and the **count** of sentences with a final
label in {TP, PT} — a count, never split by direction. That count replaces the English-borrowed precision in the
yield estimate, and decides:
- **Rule T** (Turkish Kenet), above.
- **Rule Y (yield).** A language whose projected directional total (pilot rate times treebank size, Wilson lower
  bound) is below 60 is coded anyway but enters only the exploratory analyses (Section 7). Projected 60 to 99: it
  enters the hierarchical model (partial pooling handles small n) but its own per-language test is reported as
  INSUFFICIENT unless the main run reaches 100.
- **K\* and the coding scheme per language** (Section 5.1): from the pilot's directional count and coder-1 miss
  count, both pooled over direction.

Direction counts in the pilot stay closed until the main run is frozen, exactly as wave 2 Section 3.4.

## 4. Codebook: protocol v2 time-place, with the v3.1 presence rules, adapted per language

**Codebook name: v2-TP-x (cross-linguistic).** Built from parts already frozen, plus per-language presence notes.
- **Labels:** protocol v2's five classes for the one pair: **TP** (time over place), **PT** (place over time), **PAR**,
  **AMB**, **NA** (time and place not both literally present).
- **Directional rule:** v3.1 Section 1.3 for the time-place pair, word for word, with R1 (one asserted value, two
  restrictors) and R3 (instance picking). R2 applies to time and place modifiers inside referring noun phrases.
- **Presence rules:** the v3.1 rules that concern time and place, word for word: PR1 (target sentence only), PR2
  (whole sentence, across clauses), PR3 (time and place must locate something), PR4 (motion, residence; persons as
  goals do not count), PR5 (events as settings), PR6 (ages and travel times), PR12 (when in doubt, not present). PR7
  to PR11 (quantity, manner, size, colour) are not used.
- **Anchors:** the six time-place anchors of v3.1 Section 1.4, in English, plus a translation of each into the
  coded language (Section 4.2). Coders are told the English anchor is authoritative.

### 4.1 Per-language presence notes (translation of the rules, not new rules)

Each note says how a rule shows in the language's grammar. None mentions direction. Every note was written from the
grammar and the treebank's annotation, before any wave 3 code.
- **All languages: one marker, two readings.** Where one adposition or case marks both time and place, the head
  decides: a phrase is time when its head names a time (date, year, period, part of day, time unit, event with a
  temporal word under PR5) and place when its head names a location. Applies to: Mandarin 在 / 於; Japanese に and で;
  Turkish locative -DA (also on dates, "2010'da"); Finnish inessive and adessive (also "tammikuussa", "illalla");
  Arabic في; Hindi में and पर; Persian در; Indonesian di / pada (pada mostly time or abstract); Korean -에; Naija for
  and inside.
- **Finnish:** the essive of a time noun ("maanantaina", "vuonna 2010") is time. The adessive with a person
  ("minulla on") is possession, not place.
- **Japanese and Korean:** a topic-marked time or place noun (は / 은·는) counts if it locates something (PR3), not if
  it is what the sentence is about.
- **Mandarin:** a localiser (中, 上, 裡, 內, 外, 下) after a noun marks place only when the noun is a location or a
  physical thing ("桌子上"); after an abstract noun ("歷史上", "會議中") it is not place (PR12 if unclear).
- **Arabic and Persian:** the construct state or ezafe linking a place name to a noun ("مدينة القاهرة", "شهر تهران")
  is one expression, not two.
- **Naija:** "for" before a location is the general locative ("for house"); "for" before a person or purpose is not
  place.
- **Turkish:** a dative or ablative case on a location is place (goal or source, PR4); on a person it is not.
- **Hindi:** postpositions बाद, पहले, दौरान and तक after a time noun are time; पास, अंदर, बाहर after a location are
  place.

### 4.2 Translation of anchors and notes

Anchor translations are made by a model, back-translated by a second model in a fresh context, and fixed where the
back-translation changes which dimension restricts which. If a native speaker is available (Section 4.3) they read
the translated anchors before coding. Translations are committed before the pilot.

### 4.3 What coders see

The target sentence and the one before it, in the treebank's own text, and nothing else: no parse, no screen flag, no
transliteration, no English translation. Indonesian and Naija treebanks carry English translations; they are withheld,
because a directional reading taken from a translation measures the translator's English (the same caution as the
sign-language arm). **Optional native-speaker check (needs Adam to recruit; does not gate anything):** a native
speaker codes 50 pilot sentences per language blind; agreement with the final label is reported per language.

## 5. Coders, agreement and the bars

### 5.1 Coders

Coder 1 Opus, coder 2 Sonnet, adjudicator Opus, each in a fresh context, told nothing about Navon, the expected
direction, the screen or the design (as wave 2 Section 5.1).

**Coding scheme. First preprint (Indonesian): D1, every sentence double-coded and adjudicated.** The hybrid scheme
below is for the extension only. Reason (verification row 3b): under D3 coder 2's batches are about 47% truly present
against 12% under D1, so coder 2 no longer sees a design independent of coder 1; the D-kappa item set is unchanged by
construction, but the context shift is a behavioural question the simulations cannot price, and on one language the
saving (about $30) does not buy it. **Extension (rwj default D3, with fallback D1).** The pilot is double-coded in full (D1). In the main run, coder 1
codes every drawn sentence; coder 2 and the adjudicator see every sentence coder 1 labels other than NA, plus a random
15% of coder 1's NA sentences (seed 20261134, string seed `20261134:<language>`), mixed in the same batches so coder 2
cannot tell them apart. Audited NA sentences carry weight 1 / 0.15 on top of their design weight; unaudited coder-1 NA
sentences are NA. D-kappa is unchanged (every both-present item is double-coded); P-kappa is estimated with the audit
weights. **Fallback rule:** a language whose pilot shows coder 1 labelling NA on more than 0.10 of final directional
items (upper 95% Clopper-Pearson bound, a count pooled over direction) is double-coded in full (D1). Evidence: on
English, coder 1 (Opus) missed 0.031 of directional items and coder 2 (Sonnet) 0.366, with Sonnet's misses
direction-differential (PT 0.63, TP 0.31); D3 simulated on English has bias -0.0001 and coverage 0.969, and fails only
when coder-1 misses are large and direction-differential (design note). **Lesson from Addendum 6:** pilot 2 silently ran two
Opus coders. Here the model identifiers are written into the queue file before the pilot, and the checker refuses a
code file whose recorded model differs from the queue.

### 5.2 Agreement statistics and bars, and why they are set where they are

Two statistics, because wave 2 showed they fail for different reasons and do different damage:
- **Direction agreement, D-kappa (primary, gates).** Cohen's kappa on {TP, PT, PAR, AMB} over items **both** coders
  labelled as both-present. This is the agreement the direction estimate rests on: a flip or a TP/PAR confusion moves
  the share directly. **Bar 0.60**, kept from protocol v2. Evidence it is reachable: pilot 1's equivalent statistic
  was 0.839 (n 155), with 0 of 24 directional items flipped; Arm A's whole kappa was 0.789.
- **Presence agreement, P-kappa (reported; gates only the pilot stop).** Cohen's kappa on present-or-not (NA versus
  any other class) over all coded sentences, with raw agreement and positive specific agreement beside it, because
  kappa collapses when almost every sentence is NA (A3b: 0.576 at raw 0.969). Presence errors change which sentences
  enter, which changes yield; they bias the share only if they correlate with direction. That correlation is checked,
  not assumed: the share on items both coders found present is compared with the share on items only the adjudicator
  admitted (Section 7, exploratory).

**Why not wave 2's pooled five-way kappa with a 0.60 point bar.** Wave 2's S1 statistic mixed presence and direction,
was decided on a point estimate with a 95% interval of 0.295 to 0.672 (n 149), and was run by a script that tested the
wrong bar (0.40 instead of 0.60, Addendum 6). Here: the two components are gated separately; a bar applies only where
n gives an interval half-width near 0.1 (at least 100 both-present items for a per-language gate, else the gate is
"undecided" and the language is exploratory); and every bar is a named constant in the analysis script, with a unit
test asserting each constant against this text before any real code is read.

**Per language (main run).** A language with D-kappa below 0.60, or undecided, is exploratory for its own direction
test and is left out of the confirmatory fit of Section 6 (it enters the exploratory fit).

**For the wave.** The confirmatory test of Section 6 needs **at least six** languages that pass rule Y and the D-kappa
bar. With fewer, every wave 3 result is exploratory.

### 5.3 Flip rate

As wave 2 Section 5.3, per language and pooled: e = (1 − √(1 − 2d)) / 2 from the share d of both-directional items
whose directions disagree; Clopper-Pearson bound. A language with e above 0.15 is exploratory. The share estimate is
corrected for e (Appendix D, Proposition D.7), with the upper bound as sensitivity.

## 6. The hierarchical model: language variance as the measure of universality

### 6.1 Model (Appendix D.5, one pair)

For language ℓ and directional item k (TP or PT; PAR and AMB carry no direction),

  y(k, ℓ) ~ Bernoulli( logit⁻¹( δ + v(ℓ) ) ),  v(ℓ) ~ Normal(0, s²),

where y = 1 means time over place, δ = θ(time) − θ(place) is the shared gap on the dominance scale, and s is the
standard deviation of the gap across languages (s = τ√2 in D.5's notation). Under Design C, each item carries its
design weight, and per-language logit shares with design-based variances are combined by a random-effects
meta-analysis (REML) instead of the item-level fit; the two coincide under a census. Clustering by document is carried
by a document bootstrap within language where the treebank has document IDs, and by the sentence otherwise (stated per
language).

### 6.2 What measures universality

1. **s, the between-language standard deviation of the time-place gap (primary).** s = 0 means one order for all
   languages.
2. **P(new language keeps time over place) = Φ(δ / s)**, with an interval from the posterior or the bootstrap. At
   English's gap (logit 0.823 = 1.54, or 1.04 at Arm A's 0.738), s = 0.5 gives 0.999 or 0.98; s = 1.0 gives 0.94
   or 0.85.
3. The count of languages whose own interval excludes 0.5 on each side (descriptive).

### 6.3 Confirmatory tests (if Section 5.2 allows)

- **H1, mean direction:** δ > 0, one-sided, α = .05, t-test on the per-language logit shares (the test Appendix D.6
  powered: 8 languages × 50 items gives 0.99 at s = 0.5). Estimation by the model in 6.1.
- **H2, heterogeneity:** chi-square on L − 1 degrees of freedom across languages (D.6: 8 × 100 gives 0.92 at
  s = 0.5). The likelihood-ratio test of s = 0 against the mixture of chi-square on 0 and 1 degrees of freedom is
  a sensitivity, marked as resting on Self and Liang (1987), recalled and not read.
- **What this wave cannot promise.** Heterogeneity as small as s = 0.25 is detected with power about 0.54 under
  Design C and 0.86 even under a full census (design note, Part 6). A non-rejection of H2 is reported with the interval
  of s, never as evidence that s = 0.
- **Power at the expected yields.** Eight languages above 100 items: H1 about 0.99 at s = 0.5 and about 0.72 at
  s = 1.0 (D.6); H2 about 0.92 at s = 0.5. Ten languages lift the s = 1.0 case toward 0.90 (D.6 gives 0.90 at
  twelve). These are Appendix D's numbers, not recomputed here.

### 6.5 The first preprint's analysis (English plus Indonesian)

With one added language, s and H1/H2 are not estimable and wait for the extension. The first preprint registers:
- **Primary (confirmatory if Section 5.2 allows for Indonesian):** the Indonesian time-over-place share among final TP
  and PT items, with a 95% logit-scale interval (sentence as the unit; flip-rate correction of Section 5.3), and the
  two-sided test of share = 0.5 at α = .05. Power (normal approximation): at a true share of 0.74, 1.00 at 164 or 113
  items; the test keeps power 0.80 down to a true share of 0.63 at 113 items and 0.60 at 164 (verification run,
  `scripts/p65_wave3_design_verify.py` companion arithmetic, 2026-11-16).
- **Secondary (exploratory, because the English design differs):** the difference between the Indonesian share and
  English's A3b share (0.823, document interval 0.728 to 0.906), with its interval; and Φ(δ/s) is NOT reported, since
  s needs more languages.
- **Descriptive:** the screen's recall and precision in Indonesian (every sentence is coded, so both are measured
  exactly, by direction), reported against English's 0.769 / 0.366, as the first measurement of whether the English
  screen transfers.

### 6.4 Sensitivities (all reported, extension)

English added as an eleventh language (A3b share; a different design, so not in the primary fit); Naija left out
(English-lexified); Hindi and Persian merged as one Indo-European family; Turkish with Kenet; flip-rate upper bound;
per-language presence notes withdrawn (coders given the base rules only), if a re-code is affordable.

## 7. Exploratory analyses (labelled as such)

Every language below rule Y's 60 or the D-kappa bar; per-language direction tests for languages with 60 to 99 items;
the presence-direction correlation check (5.2); share by genre within a treebank (news, wiki, spoken); typological
contrasts (case-marking versus adpositional languages; languages where one marker carries both time and place), which
are hypotheses for later, never tests here.

## 8. What each outcome means for Navon's claim

| outcome | reading |
|---|---|
| H1 holds; H2 does not reject; Φ(δ/s) interval above 0.9 | time over place is shared across ten languages from eight families and a creole: the English result generalises within this coverage. Navon's claim survives its first cross-linguistic test, with the coverage gap of Section 1 stated |
| H1 holds; H2 rejects; most languages above 0.5 | a shared tendency with real variation: the order is a default of conception that languages modulate. Navon's claim holds as a tendency, not a universal |
| H1 holds only because of a few languages; several languages reverse | the order is language-specific. Navon's claim, read as a claim about conception, is not supported by text; English is one setting of a variable |
| H1 fails; δ near 0 | no shared direction: the English asymmetry is a property of English text (or of its genres), not of conception |
| too few languages pass the bars (Section 5.2) | wave 3 is exploratory: report each language's share with its interval and say the cross-linguistic question is open |

A text-based result speaks to how languages express time and place together. It bears on conception only through the
assumption that frequent restriction in text reflects dominance in conception; that bridge belongs to the paper's
argument, not to this wave.

## 9. Stopping rules

- **S1, pilot agreement.** Computed on the ten pilots pooled. If pooled D-kappa is below 0.40, or pooled P-kappa
  below 0.40, coding stops; the per-language notes (4.1) may be revised once, using disagreement content only, never
  direction counts; a second pilot of 300 per language is drawn (seed 20261132, string seed `20261132:<language>`,
  excluding the first pilot) and coded. At most two pilots. If the second pilot's pooled D-kappa is below 0.60, wave 3
  proceeds with every result exploratory. These bars are constants `S1_FIRST = 0.40`, `S1_SECOND = 0.60` with a unit
  test.
- **S2, gold items.** Five constructed gold items per batch of 500, in the batch's language (translated anchors, keyed
  before coding). A batch is re-coded at most once; a second failure drops that coder's batch.
- **S3, sampling.** One main run, Design C. Batches follow the fixed permutations of Section 2.2; the only decision
  between batches is the direction-blind stopping rule. No checker or script prints a direction before the freeze
  of all codes (the wave 2 checker's no-`>` assertion). No draw outside the permutations, ever.
- **S4, adjudication.** One blind pass.
- **S5, analysis.** The analysis script is committed and smoke-tested on synthetic codes (including a planted
  heterogeneous set that H2 must reject and a homogeneous set it must not) before any real code; it runs once on the
  frozen labels. A fix afterwards is an addendum with both results.
- **S6, budget.** Batches are scheduled round-robin across languages that have not stopped. If the cap (Section
  2.3) is reached, the analysis runs on every language as of its last complete batch: under Design C each batch
  boundary is a valid stratified sample with known inclusion probabilities, so a budget stop leaves languages short of
  K\*, not biased. Each language's achieved effective count is reported, and a language below 100 is handled by rule Y.

## 10. Confirmatory versus exploratory

Confirmatory, if Section 5.2 allows: H1 and H2 on the languages passing rule Y and the bars, s and Φ(δ/s) as the
reported measures. Exploratory: everything in Section 7, every sensitivity in 6.4, and every language that fails a
bar.

## 11. Left open for the freeze (decisions)

1. **First preprint: Indonesian census, double-coded, central $110, cap $165.** Alternatives: Arabic census ($190,
   355 expected items, NC licence, newswire only); Indonesian under Design C to 100 items ($60, keeps the weights and
   stopping machinery for a saving of $50). Needs Adam: money, and confirmation of Indonesian over Arabic (ranking in
   `p65_wave3_design-verify_2026-11-16.md` Section 3; the verifier recommends Indonesian).
   **DECIDED (Adam, 2026-11-16, "rwj", option A): Indonesian census, double-coded, central $110, cap $165.** The
   English main run (stage A, $57) is not approved and is not part of this registration's money. Items 2 and 3 stay open.
2. **Extension design and money (later).** rwj default: Design C with hybrid coding D3 (central $793, cap $1,190, pilot
   included; the independent recount gives $893 to $969 central). Alternatives: C fully double-coded (central $1,193,
   recount $1,304, cap $1,790; no reliance on coder 1's miss rate and no coder-2 context shift); census A ($2,910).
   Draft Design B ($757) is withdrawn: it misses the 100-item target in eight of ten languages.
3. **Extension: ten languages or eight.** rwj default ten (adds Korean and Persian). Override to eight saves about $220
   under C with D3, $330 double-coded (Korean and Persian need the most unflagged sentences).

Not open: the codebook, seeds, bars, model and stopping rules above, unless the freeze session changes them before
any wave 3 code.

## 13. Freeze addendum for the one-language run (2026-11-16)

Fixes details the draft left open for the Indonesian census. Nothing here changes a bar, seed, rule or the codebook.
- **Decision.** Section 11 item 1 is decided (Adam rwj, option A). The English main run (stage A, $57) is not approved and
  is not part of this registration; items 2 and 3 stay open for the extension.
- **Batches.** The pilot is batch P01 (500 sentences, ids P0001 on). The other 6,128 sentences follow Section 2.2a's
  permutation in M01 to M16 (400 each, M16 holds 128, ids M0001 on). Five gold items per batch (S2), 85 in all, in
  Indonesian, five kinds (TP, PT, PAR, two NA), distinct wordings, keyed in `wave3/main/batches/gold_key.tsv`, inserted
  with Random(20261135). Blind ids run through a stage including the gold slots. The sentence before the target is the
  previous sentence in the treebank file; English translations are never shown.
- **Labels and codebook.** `wave3/main/p65_codebook-v2-TP-x_id.md`: TP, PT, PAR, AMB, NA, with the Indonesian notes of
  Section 4.1 expanded there. Anchors and gold were back-translated by a fresh model (`wave3/p65_wave3_id_anchors_2026-11-16.md`).
  No native-speaker check; it gates nothing (4.3).
- **S1 on one language.** S1 is read on the Indonesian pilot P01 alone: if its P-kappa or its D-kappa is below 0.40 the
  runner stops after P01 and writes HALT.txt; a second pilot needs a person. Both kappas are printed as numbers, never by direction.
- **Coders.** Coder 1 claude-opus-5-5, coder 2 claude-sonnet-5-5, adjudicator claude-opus-5-5, in fresh headless sessions,
  Read and Write only. The runner refuses a result whose model family differs from the queue. A coder missing 2 or more of 5
  gold items re-codes the batch once; a second failure drops that coder's batch and halts the run for a person.
- **Money.** Cap $165, central $110; spend ledger `wave3/main/spend.tsv` fails closed; no job launches unless spend plus its
  cap stays within $165. If the cap ends the run, the analysis uses complete batches only (2.2a), the achieved count stated.
- **Analysis.** `scripts/p65_wave3_analyze.py`, run once on frozen labels. The extension's H1 and H2 functions exist in it and
  are smoke-tested (S5) but are not run on one language.
- **Not applicable to this run:** Design C, hybrid coding D3, rule T, the second pilot draw, K\*.

## 12. References

- Navon, D. (1978). On a conceptual hierarchy of time, space, and other dimensions. *Cognition, 6*(3), 223-228.
  https://doi.org/10.1016/0010-0277(78)90014-8 [as recorded in the project's source read,
  `p65_navon1978-source-read_2026-11-13.md`]
- de Marneffe, M.-C., Manning, C. D., Nivre, J., & Zeman, D. (2021). Universal Dependencies. *Computational
  Linguistics, 47*(2), 255-308. https://doi.org/10.1162/coli_a_00402
- Self, S. G., & Liang, K.-Y. (1987). Asymptotic properties of maximum likelihood estimators and likelihood ratio tests
  under nonstandard conditions. *Journal of the American Statistical Association, 82*(398), 605-610.
  https://doi.org/10.1080/01621459.1987.10478472 [recalled, not read; unverified]
- Sampling theory behind Design C (recalled, not read, unverified; to the fetch list before manuscript use): Neyman, J.
  (1934), On the two different aspects of the representative method, *Journal of the Royal Statistical Society, 97*(4),
  558-625; Neyman, J. (1938), Contribution to the theory of sampling human populations, *Journal of the American
  Statistical Association, 33*(201), 101-116; Horvitz, D. G., & Thompson, D. J. (1952), A generalization of sampling
  without replacement from a finite universe, *Journal of the American Statistical Association, 47*(260), 663-685;
  Cochran, W. G. (1977), *Sampling Techniques* (3rd ed.), Wiley; Särndal, C.-E., Swensson, B., & Wretman, J. (1992),
  *Model Assisted Survey Sampling*, Springer.
- Treebank references: `p65_wave3-feasibility_2026-11-16.md` Section 5, with their verification status.

Last updated: 2026-11-16 (Eastern); scope narrowed to one language after independent verification
