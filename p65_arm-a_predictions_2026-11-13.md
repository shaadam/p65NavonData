# p65 Arm A: study plan, predictions and pivots, registered before any coding (2026-11-13, 13:45 ET)

Adam: "Plan the study, make predictions, graph predictions, pivot, then run the study next chat." Written and
committed before any sentence received a label. Two blind model coders were started at about 13:30 and stopped at about 13:38 on Adam's instruction; their partial output was moved to `arm-a-model/_aborted-unread_2026-11-13/` by
filename and NOT read. The next chat deletes that folder unread and starts the coders fresh.

## What is being tested

Navon (1978) argued, with examples and no data, that time dominates place: we say where something is *at* a
time ("The sun is at zenith at noon") far more readily than what time it is *at* a place. His criterion (c):
the dimension whose values condition the other's is the dominant one. Navon ran no study, so there is nothing
to replicate; this is the first test of criterion (c) on public text: UD English EWT + GUM r2.18 (29,975
sentences of web, news, fiction, spoken and academic English).

## Design (protocol v2, with model coders as v3)

- Items: all 200 candidate sentences (the frozen v1 word screen), 250 random frame sentences (a predicate with two or more modifiers, no word list) and 50 random rest sentences. 500 in all, shuffled, group labels hidden (`arm-a-model/p65_model-items_blind.tsv`; key `p65_model-items_map.tsv`).
- Coders: two blind model passes (Opus and Sonnet, fresh contexts, codebook v2 sec. 2). Disagreements adjudicated by a third reading against the codebook, blind to group. The class Google Forms later measure human-model agreement on 300 of these items.
- Analysis: `scripts/p65_navon_arm_a_analyze.py`, committed before any label existed: agreement (Cohen's kappa, usable at 0.60 or more), expansion counts (frame and rest weighted by pool size / sample size), the share s = time-holds-place / (time-holds-place + place-holds-time) with a 95% interval resampling whole documents, screen recall per direction, and the pre-registered decision label (protocol v2 sec. 5; at least 30 directional sentences or the result is INSUFFICIENT).

## Predictions (figure: `arm-a-model/p65_arm-a_predictions_2026-11-13.png`)

| # | prediction | value | why |
|---|---|---|---|
| P1 | labels among the 200 candidates | not applicable 45% (35-55), side by side 38% (28-48), time holds place 10% (5-16), can't decide 5% (2-9), place holds time 2% (0-5) | most hits are "there is", "home" as a goal of motion, or events with a when and a where |
| P2 | directional sentences in all 500 | about 30 (time holds place ~25, place holds time ~5) | candidates give ~24; the frame adds a few |
| P3 | share s | mean 0.85, 80% range 0.70 to 0.95 | place-holds-time needs time zones, seasons or local custom, which these genres rarely discuss |
| P4 | screen recall | low for time-holds-place (about 0.1: "in 1990", "at the time" are not in the word list); place-holds-time recall UNKNOWN (no such sentence among the 300 non-candidates) with probability 0.6 | the v1 list has 14 time words and 13 place words |
| P5 | coder agreement | kappa 0.55 to 0.75; most disagreements on time-holds-place versus side by side (a state versus an event) | the state/event line is the codebook's hardest call |
| P6 | decision | INSUFFICIENT 45%, SUPPORTS_DIRECTION 25%, INCONCLUSIVE 13%, SUPPORTS_STRONG 10%, AGAINST_STRONG_THRESHOLD 5%, AGAINST_DIRECTION 2% | P2 sits on the 30-sentence floor; intervals on ~30 items are wide |

## What each result would and would not show

A large share is what Navon predicts, but it is ALSO what a plain frequency account predicts (people talk
more about where things are than about what time it is somewhere), and Garner's (1976) logical-dependence
account predicts it too. So SUPPORTS is necessary for Navon, not sufficient. AGAINST_DIRECTION would count
against him in this kind of text. INSUFFICIENT says only that these 30,000 sentences are too few.

## Pivots, decided now

| result | next step |
|---|---|
| INSUFFICIENT, or recall UNKNOWN / DIFFERENTIAL | Scale up on public-domain text: Project Gutenberg fiction plus English Wikipedia, parsed with spaCy, candidates found by named-entity type (DATE/TIME with GPE/LOC/FAC) instead of a word list, 1,000 candidates model-coded the same way; target 100 or more directional sentences. Same analysis script. |
| SUPPORTS_DIRECTION or SUPPORTS_STRONG | Run the tests that separate Navon from frequency: (i) acceptability of minimal pairs built from his own examples ("The sun is at zenith at noon" vs "It is noon where the sun is at zenith"), in the class Google Form; (ii) criterion (b) on dictionaries (paced job 29); (iii) a third dimension (place versus manner) to test the hierarchy's order, not only its top. |
| INCONCLUSIVE with 30 or more directional | Report it; size the Gutenberg study from the observed rates. |
| AGAINST_STRONG_THRESHOLD | Report; check genre (news and how-to text may favour place-holds-time); rerun by genre. |
| AGAINST_DIRECTION | Check the coder rule first (time-zone and weather text), then report as evidence against Navon in this register. |
| kappa below 0.60 (any result) | The directional result is exploratory; revise the codebook (v4) on the disagreements, and the class forms become the deciding coders. |

## Addendum before any coding (2026-11-13, ~13:48 ET; Adam: "For human responders there's info if the task performance is asymmetrical. Some judgements are harder than others")

The human task carries evidence the label counts cannot: how HARD each judgement is. If time is the frame people
think in (Navon), judging a sentence where place holds time should be slower and less accurate than judging one
where time holds place, at matched length. A frequency account predicts only a familiarity effect, removed by
matching on how common each construction is; Garner (1976) predicts asymmetric interference between the two
dimensions, which a speeded classification version can measure directly.

| # | prediction | value |
|---|---|---|
| P7 | human response time and accuracy, place-holds-time items versus time-holds-place items (matched on sentence length) | place-holds-time items slower by 10 to 25% (median response time) and agreement with the keyed answer lower by 5 to 15 points |
| P8 | speeded classification (classify by time while place varies, versus the reverse) | irrelevant place slows time judgements less than irrelevant time slows place judgements |

Consequence for collection: Google Forms records no response times, so the human task moves to the timed
held/holding app on a public page with answers and per-item times saved to a Google Sheet (option B), or an
established platform (jsPsych/Pavlovia). Items: minimal pairs built from Navon's own examples plus matched corpus
sentences, so the asymmetry is not a vocabulary effect.

Pivot added: P7 and P8 hit -> asymmetry evidence for Navon over a pure frequency account, report with the share;
P7 miss -> the share alone stands, as frequency-compatible.

## Run steps for the next chat

1. Delete `arm-a-model/_aborted-unread_2026-11-13/` unread.
2. Start the two blind coders on `p65_model-items_blind.tsv` (briefs as in this session: codebook v2, no access to the map, output `arm-a-model/p65_model-codes_coder{1,2}.tsv`).
3. `python3 -I scripts/p65_navon_arm_a_analyze.py --map arm-a-model/p65_model-items_map.tsv --c1 ...coder1.tsv --c2 ...coder2.tsv`; adjudicate the listed disagreements into `arm-a-model/p65_model-adjudication.tsv` (item, class, reason) blind to group; rerun with `--adj`.
4. Score each prediction P1-P6 against the result in a table (hit / miss), take the pivot the table names, and log everything in methods-evidence.md.

## References

Garner, W. R. (1976). Interaction of stimulus dimensions in concept and choice processes. *Cognitive Psychology, 8*, 98-123. https://doi.org/10.1016/0010-0285(76)90006-2

Navon, D. (1978). On a conceptual hierarchy of time, space, and other dimensions. *Cognition, 6*(3), 223-228. https://doi.org/10.1016/0010-0277(78)90014-8
