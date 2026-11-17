# Does time dominate space? Testing Navon's (1978) conceptual hierarchy with public data: data and code

Last updated: 2026-11-17 (Eastern)

Adam Y. Shavit, Hunter College and the Graduate Center, City University of New York. Preprint version 1 (2026).
Built on 2026-11-17 from the working repository shaadam/p65Spacetime. Code under the MIT licence (LICENSE).
MANIFEST.txt lists a sha256 for every file.

## What this bundle holds

The paper tests Navon's three dominance criteria on public data in four arms, and reports a registered census of
Indonesian. This bundle holds what the paper cannot: the registrations written before any item was coded, the
codebooks, the item keys (treebank, document and sentence identifiers for every sampled sentence; dictionary and
sense identifiers for every sampled verb sense), the blind model coders' codes and the adjudications, the coded
table of published interference experiments, the per-source error-evidence list, the analysis and verification
scripts behind every reported number, the recorded outputs of those scripts, and the number trace that records
where every printed value sits in the manuscript and recomputes it from these tables.

A file is here only if a number, table or figure value the paper reports depends on it, or if the paper cites it
as the registered protocol. The paper itself, its figures, and the working records behind the project are not
here.

| folder or file | contents |
|---|---|
| `scripts/` | sampling, analysis, verification and fetch scripts for the four arms, the Indonesian census and the mathematical appendix |
| `arm-a-model/`, `arm-a3-model/`, `arm-a3b-model/` | corpus arm: item keys, model codes, adjudications, cell tables, recorded results, the exploratory extension's codebook and scripts |
| `change-verbs/` | dictionary arm: item key (sense identifiers, no definitions), the three coders' codes with their checksums, the recorded analysis run, its transpose control and the coder agreement |
| `published-asymmetry/` | interference arm: the coded table of experiments, tallies, random-effects summary, the two rulings, the second coder's codes and the comparison |
| `error-evidence/` | error-evidence arm: the per-source list, the recount run, the learner-corpus intrusion count |
| `wave1-math/` | mathematical appendix: attack checks, power table, independent verify runs, Wolfram run |
| `verify/` | independent recounts of the dictionary arm written without reading the analysis code, and the second recall sweep |
| `wave3/` | the Indonesian census: frozen registration hash and treebank checksums, the three pre-data amendments, the one revision of the language notes, the codebook, the census map and batch maps (identifiers and screen flags), the two coders' codes and the adjudications for the pilot and the sixteen main batches, the gold key (constructed sentences), the yield pilot, the spend ledger and the recorded analysis run |
| `p65_*.md` | registrations, the prediction file, codebooks and results notes, the frozen Indonesian registration |
| `p65_v1_number-trace.md` | the number trace |
| `run-all.sh` | the cold run below |

## What is not here, and why

- The manuscript, its appendix and its figures: they are the paper. Every plotted value is a value of a recorded
  results file here, and the registered analyses below regenerate those files.
- Third-party text. The Universal Dependencies treebanks (English EWT and GUM, Indonesian GSD and CSUI), the three
  dictionaries (WordNet 3.1, GCIDE 0.53, the kaikki.org Wiktionary extract) and the learner corpora (FCE and
  Write & Improve, as released for the 2019 Building Educational Applications shared task) are not redistributed.
  The blind item sheets the coders read, which quote treebank sentences, are therefore left out, as are the
  Indonesian coders' part files and adjudication sheets, which copy sentences. The item keys give every sentence's
  treebank, document and sentence identifier; `scripts/p65_wave3_ud_fetch.py` and `scripts/p65_change_verbs_fetch.sh`
  fetch the sources against the checksums recorded in `wave3/p65_wave3_ud-checksums_r2.18.tsv` and
  `p65_change-verbs-registration_2026-11-14.md`. The learner corpora are obtained from the shared-task organisers.
  The coders' code files keep the short phrases a coder named as the time or place expression; no sentence is
  reproduced.
- Working records of the project (the methods log, ledgers, agent reports, run logs, the wave 2 registration of
  an extension that has no result in this paper, the scripts that drive the model coders and build the PDF) and
  the PDFs of the cited papers. They live in the working repository.

## Cold run

Unzip into an empty folder and run `sh run-all.sh` (Python 3.8 or later; numpy, scipy 1.6 or later, sympy and
mpmath for the appendix steps; `PYTHON=/path/to/python3 sh run-all.sh` picks an interpreter). The run:

1. regenerates the number trace (`scripts/p65_v1_number-trace.py`): every number in the abstract and discussion
   is recomputed from the tables here by arithmetic that shares nothing with the analysis scripts and compared
   with the printed value recorded in `p65_v1_number-trace.md` (each printed string was located in the manuscript
   when that table was written in the repository); then runs its negative control, which nudges three values
   and must fail;
2. re-runs the registered analysis of each arm from the codes and keys and compares the output byte for byte with
   the recorded copy (for the dictionary arm, after dropping the quoted definitions, which are not redistributed);
3. re-runs the independent recounts with their planted-error controls;
4. re-runs the appendix's numerical checks, the power table and the independent verify pass (seeds fixed);
5. re-runs the registered analysis of the Indonesian census (`scripts/p65_wave3_analyze.py --real`) from the
   codes and adjudications and compares its output with the recorded run, after its self-test on synthetic codes
   (floats compared to 10 significant digits: scipy versions print the exact binomial p to a different last digit).

cold-run: 4 min (Mac mini, Apple silicon; Python 3.11 with numpy 2.4 and scipy 1.17; measured 2026-11-17 in a
fresh temporary folder; under Python 3.8.8 with numpy 1.20.1 and scipy 1.6.2 every step gives the same output
except the verify pass, whose superseded box-optimiser detector counts depend on the scipy optimiser version).
The run prints each step's exit code and whether its output equals the recorded copy, and ends with one line
saying whether every step passed.

Not re-run cold, because they read the third-party sources: the sampling scripts (`p65_navon_arm_a_sample.py`,
`p65_navon_arm_a3_sample.py`, `arm-a3b-model/p65_navon_arm_a3b_sample.py`, `p65_change_verbs_extract.py` and
its filter and item builders, `p65_wave3_id_build.py`, `p65_wave3_yield_pilot.py`), the entity screen
(`p65_navon_arm_a2_entity_screen.py`) and the learner-corpus count (`p65_error_intrusion_count.py`). Their
recorded outputs are here (`error-evidence/p65_e1-run_2026-11-13.txt`, `wave3/pilot/`, the results notes), each
with the command it was run with and the source checksums in its registration or results note. The Wolfram
checks (`scripts/p65_wave1_wolfram_checks.wls`, `scripts/p65_wave1_verify_wolfram.wls`) need Mathematica; each
check of an appendix result is paired with a control that must come out false, and their recorded run is
`wave1-math/p65_wave1_wolfram-run_2026-11-16.txt`.

## Model coders

The codes in `*codes_coder*.tsv`, `wave3/main/codes/` and `change-verbs/codes/` were produced by blind model
coders (Claude models, named in each registration) working from the codebook and the blind item sheets;
disagreements went to a model adjudicator (`*adjudication.tsv`). The registrations record the models, the briefs
and the sha256 of every file frozen before coding.

Last updated: 2026-11-17 (Eastern)
