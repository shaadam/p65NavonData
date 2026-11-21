# P65 dictionary study: Wiktionary senses that repeat Webster 1913, match rule (registered 2026-11-19)

Written and committed BEFORE the overlap is computed. Plan: `docs/p65_v2_tests-plan_2026-11-19.md`, v1 step 3.
Question: how many English Wiktionary verb senses repeat a Webster 1913 definition, and does the change count
hold with those senses removed? The answer goes into the existing Limitations sentence ("Wiktionary repeats some
Webster 1913 definitions"), no new sentence.

## Data

The same files the dictionary study registered (`p65_change-verbs-registration_2026-11-14.md`): GCIDE 0.53
(Webster 1913 paragraphs only, as `scripts/p65_change_verbs_extract.py` keeps them) and the kaikki.org English verb
extract, sha256 4090549f13cc5bd726fce6b72abbac9fd3770f36736b8f8e29243d34f986507c. If a re-fetched file does not
match that sha256, the run stops: Wiktionary sense IDs (`WK:<line>.<sense>`) depend on the file version, so a
different file cannot be joined to the coded items.

## Normalisation

For each definition string: lowercase; remove text inside parentheses or square brackets; replace every character
that is not a letter, digit or space with a space; collapse runs of spaces; strip.

## Match rule

- **Exact match (primary).** A Wiktionary verb sense matches when its normalised gloss string equals the normalised
  string of at least one Webster 1913 verb definition of the same headword (headwords compared lowercased, spaces
  collapsed). A Wiktionary sense with several glosses (joined with " : " by the extractor) matches if any one gloss
  matches.
- **Near match (secondary, threshold registered here).** Same headword, and `difflib.SequenceMatcher` ratio of the two
  normalised strings at or above **0.90**. Exact matches are counted inside the near-match share.
- Normalised strings shorter than 3 words are not counted as matches (too generic to show copying).

## What is reported

1. Share of all extracted Wiktionary verb senses that match (exact; near).
2. Share of the Wiktionary items in the coded set (`change-verbs/items_key_nodefs.tsv`, dict WK) that match.
3. The study's change counts recomputed with the matched Wiktionary items removed, by the existing analysis rule
   (final codes by the 2-of-3 rule, as `scripts/p65_v1_number-trace.py` re-derives them): directional senses naming
   time, of all directional senses (printed now as 112 of 121); and the unbiased C and R strata (printed now as 23
   of 27).

## Negative control

A shuffled pairing: each Wiktionary sense compared with the Webster definitions of a different, randomly drawn
headword (seed 20261119). Its exact-match share must be near zero; if it is not, the rule is matching generic
strings and the result is not reported.
