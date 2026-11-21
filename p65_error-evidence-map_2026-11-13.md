# p65: what errors and disorders say about time and space, evidence map and linking (2026-11-13)

Adam (2026-11-13): "look at the types of mistakes people make in written and spoken speech. There's evidence
in that too." The search was run by a subagent (web search standard + extended, OpenAlex, Europe PMC, OSF API;
Semantic Scholar returned 429 on every call). Queries are in `lit-search-log.md`. Test registered and run on
public data: `p65_error-evidence-registration_2026-11-13.md` (commit 0c6fcdd) and
`p65_error-evidence-results_2026-11-13.md`.

Direction codes: **S>T** space primary, time depends on space (metaphor view); **T>S** time primary or scoping
over space (Navon-consistent); **DISSOC** independence, against strict dependence either way; **MIXED**;
**NONE** no bearing. Status: **FULL** text read; **ABS** abstract only; **SEC** only seen cited.

## Counts (33 sources)

S>T 10 (1 of them also DISSOC) · DISSOC 6 · MIXED 7 · **T>S 0** (Feagans 1980 and Lafford & Ryan 1995 lean that way) · NONE 10 ·
unknown 1. Full text read for 28 (the 23 recoded 2026-11-20, and Mätzig 2009, Kranjec et al. 2012, Lam 2018,
Alzamil 2025, Feagans 1980 on 2026-11-21), Gijssels et al. 2013 partly; the other 4 codes (Morton & Patterson 1980,
Kotten 1977, Coker 1978, Onnis et al. 2010) rest on abstracts, secondary sources or a title, and only those are provisional.

Full-text recode 2026-11-20 (`error-evidence/p65_armD_fulltext-recode_2026-11-20.md`, one row per source with page
and quote in `error-evidence/p65_armD_fulltext-recode_2026-11-20.tsv`): the line above replaces "S>T 9 (2 of them
also DISSOC) · DISSOC 7 · MIXED 9 · T>S 0 · NONE 8 · unknown 2". The statuses in the table below predate the recode.

Recount 2026-11-17 (`p65_armD_recount_2026-11-17.md`): the line above replaces the 2026-11-13 line "Counts (42
sources): S>T 12 (2 of them also DISSOC) · DISSOC 7 · MIXED 9 · T>S 0 · NONE 15 · unknown 2", whose entries sum
to 45 (43 net) and whose 42 cannot be reproduced from this file, which names 33 published sources. One row per
source with its code and basis: `error-evidence/p65_armD_per-source_2026-11-17.tsv`; counter with controls:
`scripts/p65_armD_recount.py`.

## Strongest three

1. **Kemmerer (2005)**, *Neuropsychologia, 43*(5), 797-806, https://doi.org/10.1016/j.neuropsychologia.2004.06.025
   (ABS). Four left-perisylvian patients; the spatial and temporal senses of the same prepositions were impaired
   separately in each direction. DISSOC. Contested by **Mätzig (2009)**, UCL thesis,
   https://discovery.ucl.ac.uk/15806/ (FULL): 5 aphasic patients, 48 spatial / 60 temporal items, no reliable
   difference, and a task confound in Kemmerer (pictures only for spatial items).
2. **Saj, Fuhrman, Vuilleumier & Boroditsky (2014)**, *Psychological Science, 25*(1), 207-214,
   https://doi.org/10.1177/0956797612475222 (ABS). Left spatial neglect brings neglect of the past ("left") side
   of time. S>T. Qualified by Anelli et al. (2018, *Cortex, 101*, 192-205; SEC): slowing was for the future.
3. **Rousselle, Dembour & Noël (2013)**, *PLoS ONE, 8*(8), e72621, https://doi.org/10.1371/journal.pone.0072621
   (ABS). Williams syndrome: space and number acuity impaired, time acuity spared. DISSOC (time does not need
   intact space).

## Map by error type

| error type | key sources (status) | what they show | direction |
|---|---|---|---|
| Aphasia, preposition senses | Kemmerer 2005 (ABS); Mätzig 2009 (FULL); Morton & Patterson 1980 (SEC: spatial 81%, temporal 72% in a deep dyslexic); Kotten 1977, *Folia Phoniatrica 29*, 270-278 (title only) | double dissociation, then a null replication | DISSOC / NONE |
| Neglect and the mental time line | Saj et al. 2014; Bonato, Saj & Vuilleumier 2016, *Neural Plasticity*, 2716036 (ABS); Anelli et al. 2018 (SEC) | spatial attention deficits distort time judgements | S>T (MIXED in detail) |
| Neuroimaging, not errors | Kranjec et al. 2012, *J Cogn Neurosci 24*, 1-16 (FULL: time voxels overlap causality 65%, space 15%); Gijssels et al. 2013 (partial: shared parietal cluster, space interferes with time more) | split | DISSOC vs S>T |
| Developmental disorders | Rousselle et al. 2013; Landau & Hoffman 2005 (SEC); Landau & Ferrara 2013 (SEC); Lukács et al. 2007 | time spared in Williams syndrome; no temporal-language data | DISSOC |
| Slips of the tongue/pen | Alderete et al. 2022, *J Cognition 6*, 26 (SEC; closed-class excluded); Harley & MacAndrew 2001 (SEC; more imageable words win); Garrett 1975 (PDF grepped, no time/space preposition slips) | **no published count of time vs space slips** | gap |
| Child L1 | H. Clark 1973 (SEC, theory S>T); E. Clark 1971 (SEC); Feagans 1980, *J Child Lang 7*, 529-537 (FULL, read 2026-11-21: spatial before/after learned in the temporal order); Coker 1978; Weist et al. 1997 (Polish better at time, Finnish at space); Tillman et al. 2017; Bowerman 1978 ("behind" for "after"-type substitutions: NOT verified) | no universal space-first order | MIXED, one lean T>S |
| L2 learners | Lam 2018 (FULL: L2 Spanish, spatial = temporal accuracy, temporal as chunks); Lafford & Ryan 1995 (SEC); Zhang & Murao 2024 (ABS); Alzamil 2025 (FULL: time preps more accurate, confounded word sets); Onnis, Jackson & Spivey 2010 (ABS: temporal in/on prime spatial shapes) | time uses not harder | MIXED / DISSOC |
| L2, our count | p65 E1 (FCE + W&I, 1.22 M tokens) | 10 cross-domain errors; time->space 8, space->time 2; p = 0.20 (0.03-0.56), INCONCLUSIVE; 4 of the 8 are text deixis ("mentioned before" -> "above") | none established |
| Gesture / sign | Casasanto & Jasmin 2012 (ABS: lateral time gestures while speech says front/back); Núñez & Sweetser 2006 (ABS: Aymara future behind); Sinha et al. 2011 (ABS: Amondawa time not spatial). No sign-language slip study found | spatial time beyond words, culturally variable | S>T + DISSOC |
| Diachrony (context) | Traugott 1978; Haspelmath 1997 (both SEC) | spatial -> temporal grammaticalization | S>T |

Not found despite searching: any speech-error count of time vs space words; any SLI/DLD study contrasting
temporal with spatial prepositions; any sign-language slip on the time line; a Kemmerer review titled "Space,
time and prepositions" (his 2010 chapter is on spatial relations only). Held library: none of these sources
held; Navon 1978 and Garner 1970 are.

## Linking: what each account predicts per error type

| error type | Navon (1978) | metaphor view (space -> time) | Garner (1976) | differ? |
|---|---|---|---|---|
| Aphasia: spatial vs temporal sense loss | **No clear prediction.** His hierarchy is about orderliness, change and scope, not processing. A dependence reading (space defined at a time) would predict temporal loss carries spatial loss | strong form: spatial loss brings temporal loss, not the reverse; weak form (stored mappings, Boroditsky 2000): either can dissociate | no prediction | only for the strong metaphor form; Kemmerer's double dissociation counts against it, Mätzig's null makes it unsettled |
| Neglect -> time distortion | none | predicts it | none | the metaphor view alone predicts; observed, with mixed details |
| Slips: spatial word for temporal and reverse | none stated; our extension "dominant terms spread" gives time->space > space->time | space->time slips > reverse (spatial representations active when talking about time; more imageable words win) | none | yes, metaphor vs our Navon extension; **no data published**; SFUSED could test it |
| Child acquisition order | no clear prediction | spatial senses first, temporal derived | none | metaphor alone; data (Weist, Feagans, Coker) do not show a universal space-first order |
| L2 accuracy by sense | none | temporal uses (derived) harder | none | metaphor alone; Lam, Alzamil show no temporal disadvantage |
| L2 cross-domain intrusion direction (E1) | none; our extension gives p < 0.5 | p > 0.5 | none | yes; E1 point estimate p = 0.20 but inconclusive |
| Gesture / signed time line | none | spatial layout of time in gesture | none | metaphor alone |
| Scope in errors (Navon criterion c) | temporal adjuncts outscope locatives, also in learner word order | no prediction | no prediction | not testable on these data (L2 order errors are L1 transfer) |

Bottom line: error and disorder evidence bears almost entirely on the metaphor view. Navon's hierarchy makes
no stated prediction about errors, and Garner none; only our "dominant terms spread" extension of Navon gives
a direction, and it is weak. Where the metaphor view's strong (dependence) form is tested, the evidence splits:
neglect supports it, the aphasia double dissociation and Williams syndrome go against it. Nothing in this
literature supports time over space as such.

## Second test not run: SFUSED speech errors (cheapest route)

SFUSED English (Alderete 2025, *J Cognition 8*, 28, https://doi.org/10.5334/joc.440) is on OSF under CC BY 4.0:
`https://osf.io/download/df7cg/` (sfusedEnglish_dataSpeechErrors2024-11-04.csv, 6.38 MB) with field
documentation `https://osf.io/download/jd93b/`. Both downloads redirect to an Oracle Cloud storage host that
the sandbox network filter denies; per the rules this was not bypassed. Route: Adam runs, in Terminal.app,
`curl -L -o p65_sfused_errors.csv https://osf.io/download/df7cg/` and
`curl -L -o p65_sfused_fields.pdf https://osf.io/download/jd93b/`; then a registration (same
S/T term sets and E1 rule applied to lexical substitutions, intended vs produced word) is written from the
field list and committed before counting. Expected yield is small (SFUSED holds a few thousand errors), so it
will likely be descriptive.
