# p65 Arm A protocol v2: Navon (1978) criterion (c) in English, class coding pilot (2026-11-13)

Status: FROZEN at the commit that adds this file, before any sentence is coded. Its SHA-256 goes in
`arm-a-class/FREEZE.txt`. Any later change is a v3 with a dated reason, never an edit in place.
Supersedes `ARM_A_FROZEN_CODEBOOK.json` v1 (W02 return, sha256 db1c5c0e...) for English. Built from the W02
adjudication (`p65_navon-w02-adjudication_2026-11-13.md`, claims C1 to C3 accepted) and Adam's coder decision
(his class, English only).

## 1. Question

Navon (1978, pp. 226-227) proposes that time dominates place: we say where a thing is *at* a given time
("The sun is at zenith at noon") far more naturally than what time it is *at* a given place. His criterion
(c): if one dimension's values are stated conditional on the other's, and not the reverse, the conditioning
dimension dominates. Navon gave the argument with examples and no sample. This pilot asks how often English
text states place conditional on time versus time conditional on place, and whether untrained coders agree
on that judgement well enough to support a full study.

The pilot's primary outputs are therefore (i) coder agreement, (ii) the base rates of the five classes in
each sampling group, and (iii) the recall of the word-list screen in each direction. The directional share
is tested only under the minimum-count rule of section 5.

## 2. Codebook v2: five classes

The unit is one sentence, read with the sentence before it. If a sentence holds more than one time-place
pairing, the coder labels the one that is most clearly directional and notes the others.

| code | class | definition | anchor |
|---|---|---|---|
| TP | time over place | The sentence states where something is (a location, position, or place reached as a state), and a time expression restricts when that holds. | "The sun was overhead at noon." "By six the children were home." |
| PT | place over time | The sentence states a time value (clock time, date, season, timing of an event), and a place expression restricts where that holds. | "In Tokyo it was already midnight." "In Spain dinner is at ten." |
| PAR | parallel | Time and place each locate an event or action; neither restricts the truth of the other. | "We met in the park yesterday." "She flew here last night." |
| AMB | ambiguous | Time and place are both present and literal, but the coder cannot choose between TP, PT and PAR, even with the previous sentence. | "He was here then." |
| NA | not applicable | No literal time expression, or no literal place expression, or one is figurative or institutional. | "She came into office in 2004." (office = position) "Home in on the problem today." |

Decision steps for coders, in order: (1) literal time AND literal place present? If not, NA. (2) Is the
sentence an event or action located in time and space? Then PAR. (3) Is a location state asserted, with time
narrowing it? TP. (4) Is a time value asserted, with place narrowing it? PT. (5) Still torn: AMB.

Minimal pairs (the guide uses these):
- "She was at the office on Monday." (location state at a time: TP) vs "She arrived at the office on Monday." (event: PAR)
- "The train is in Boston at nine." (TP) vs "It is nine o'clock in Boston." (PT)
- "At noon the square is empty." (TP) vs "Noon comes earlier in the eastern towns." (PT)

Mapping from v1: TOVERP -> TP; POVERT -> PT; PARALLEL -> PAR; UNCLEAR -> AMB; OTHER -> NA. v2 changes:
literal-use test moved into NA; the event-versus-state test is stated as step 2; minimal pairs added; unit
fixed to the sentence with context; v1's lexical screen kept unchanged as the candidate definition.

Each coder also copies the time phrase and the place phrase (or leaves them blank for NA) and gives a
confidence of 1 to 3.

## 3. What a UD parse can and cannot do here (claim C1)

A dependency parse tells which word governs which. It does not say which dimension conditions the other.
The parse is used only to build sampling groups. Every class label is a human reading.

## 4. Sampling and the recall audit (claim C2)

Source: UD English EWT and GUM, release r2.18, train + dev + test (29,975 sentences in all; test-split
SHA-256 equal to the W02 manifest). Script: `scripts/p65_navon_arm_a_sample.py`, seed 20261113.

4.1 Groups (disjoint, covering every sentence):
- **C, candidates:** the frozen v1 screen. At least one v1 temporal word and one v1 locative word, each attached as obl, advmod, advcl or nmod (subtypes pooled). 200 sentences.
- **F, frame:** not C, and some predicate carries two or more adjunct dependents (obl, advmod, advcl, nmod, subtypes pooled). This frame uses no word list, so it holds time-place pairings the v1 words miss ("in 1990 in Paris"). 12,067 sentences.
- **R, rest:** neither. 18,708 sentences. Assumed to hold almost no directional time-place statements, and that assumption is tested.

4.2 Draw: 150 from C, 250 from F, 50 from R, uniform without replacement within each group, after the
exclusions in 4.4. 450 sentences, shuffled together so no coder can tell the groups apart.

4.3 Control: the script re-counts the v1 screen on the two test splits and must reproduce W02's 9 (EWT) and
10 (GUM); it does. Negative control: removing "here" from the locative list gives 7 and 7, so the check can
fail.

4.4 Exclusions, applied before sampling: sentences over 60 tokens (readability), and sentences whose text or
previous sentence contains profanity, slurs or sexual-violence terms (word list in the script; classroom
use). Excluded counts: C 3, F 77, R 118 for content, plus length. Both rules are stated here before coding.

4.5 Recall. For each direction d in {TP, PT}, the expected English total is the stratified expansion
N_d = sum over groups h of (population_h / drawn_h) x (final codes d in h). The screen's recall for d is
N_d(C) / N_d. The screen is **equal-recall** only if the 95% interval for recall(TP) / recall(PT) contains 1.
If either direction has zero final codes in F and R together, recall for that direction is UNKNOWN.

## 5. Decisions, written before any label is seen (claim C3)

Final label per sentence: the two coders' label when they agree; otherwise an adjudicator (Adam or a trained
third coder), blind to group, decides from the codebook. Packets whose coder misses two or more of the three
keyed check items are dropped and reported.

Agreement: Cohen's kappa on the five classes for each A/B packet pair, and pooled, with a 95% bootstrap
interval over sentences. Kappa below 0.60 means the codebook is not usable by untrained coders as written;
the pilot then reports agreement and base rates only, and the directional result below is labelled
exploratory.

Directional share: s = N_TP / (N_TP + N_PT), using the expansion counts of 4.5. 95% interval: bootstrap over
source documents within each group (10,000 resamples), because sentences from one document are not
independent.

Minimum count: if fewer than 30 sentences carry a final TP or PT label across all groups, no directional
test is run. The result is **INSUFFICIENT** and the pilot sizes the full study from the observed rates.

Zero counts: if one direction has zero final labels, report the one-sided 95% upper bound for its rate in
each group (3 / n_h, the rule of three) and never read the zero as showing the construction does not exist.

Coverage: if recall is UNKNOWN or not equal-recall (4.5), the raw candidate-only share is not reported as an
estimate. Only the expansion share s is reported, with the recall result beside it.

Labels for s (lower bound L, upper bound U of the 95% interval):

| condition | label | meaning |
|---|---|---|
| L > 0.80 | SUPPORTS_STRONG | time dominates place at Navon's strong rate |
| 0.50 < L <= 0.80 and U > 0.80 | SUPPORTS_DIRECTION | time dominates; strong rate neither shown nor excluded |
| L > 0.50 and U < 0.80 | AGAINST_STRONG_THRESHOLD | time dominates, but below the strong rate |
| L <= 0.50 <= U | INCONCLUSIVE | no evidence either way; this is not evidence against Navon |
| U < 0.50 | AGAINST_DIRECTION | place dominates time in this sample |

The 0.80 strong threshold is carried from v1 and is a convention, not a value Navon states.

## 6. What this pilot cannot show

Two treebanks of web, news and spoken English are not a balanced corpus of English. Student coders make
this a pilot-strength estimate. Navon's claim is about conceptual hierarchy; corpus rates bear on it only
through the linking assumption that speakers state the dominated dimension conditional on the dominant one.
Garner (1976) offers a rival account (logical dependence between dimensions), which a rate alone cannot
separate from Navon's; see `p65_navon1978-references-read_2026-11-13.md`.

## 7. Before the class session (Adam)

- IRB: classroom coding as a teaching exercise needs no review. Using the students' codes as published
  research data may need Hunter IRB review (or an exemption determination) before the session. Check first
  if publication is intended.
- Licences: EWT annotation CC BY-SA 4.0; GUM CC BY-NC-SA 4.0 (non-commercial classroom use fits). The coder
  guide carries the attribution.
- Packets: 15 blocks x 2 = 30 packets of 33 rows (30 sentences + 3 check items), about 25 minutes each. With
- Debrief after all packets are in: explain Navon's claim then, never before (the guide is neutral on purpose so the expected direction cannot steer codes).
  fewer than 30 students, a student may take two packets but never both the A and the B of one block.

## References

Garner, W. R. (1976). Interaction of stimulus dimensions in concept and choice processes. *Cognitive Psychology, 8*, 98-123. https://doi.org/10.1016/0010-0285(76)90006-2

Navon, D. (1978). On a conceptual hierarchy of time, space, and other dimensions. *Cognition, 6*(3), 223-228. https://doi.org/10.1016/0010-0277(78)90014-8

Silveira, N., Dozat, T., de Marneffe, M.-C., Bowman, S., Connor, M., Bauer, J., & Manning, C. D. (2014). A gold standard dependency corpus for English. In *Proceedings of the Ninth International Conference on Language Resources and Evaluation (LREC 2014)*. European Language Resources Association. (UD English EWT; page range not verified)

Zeldes, A. (2017). The GUM corpus: Creating multilayer resources in the classroom. *Language Resources and Evaluation, 51*(3), 581-612. https://doi.org/10.1007/s10579-016-9343-x
