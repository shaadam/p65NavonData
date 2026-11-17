# p65 wave 3 (Indonesian census): amendment 3, the S1 second pilot, 2026-11-17 09:50 EST

Registered rule: `p65_wave3_registration_FROZEN_2026-11-16.md` Section 9 S1. After the S1 stop on P01 and the one notes
revision (amendment 2), "a second pilot of 300 per language is drawn (seed 20261132, string seed `20261132:<language>`,
excluding the first pilot) and coded. At most two pilots. If the second pilot's pooled D-kappa is below 0.60, wave 3
proceeds with every result exploratory. These bars are constants `S1_FIRST = 0.40`, `S1_SECOND = 0.60` with a unit test."
Approved: Adam's standing approval for this run (2026-11-17) covers the registered next steps. Written before any P02 code.

## What this adds (nothing in the registration changes)

- **The draw.** `scripts/p65_wave3_id_build.py` `pilot2_draw`: 300 sentences sampled with `random.Random("20261132:Indonesian")`
  from the census minus P01 (universe sorted by treebank and sentence id, as the P01 draw). The string seed takes the form of
  the registration's other seeds (`20261130:Indonesian`, `20261131:Indonesian`), capital I; the registration's template
  `20261132:<language>` fixes nothing about case, and this is recorded here so the draw is reproducible. Five gold items
  (an 18th wording per kind, constructed, distinct from the 85) shuffled in with the same `Random(20261135)` continued after
  the 17 batches. Batch P02 has 305 items, ids P0506 to P0810 (the P stage continues), files `P02_blind/coder1_input/
  coder2_input.tsv` (git-ignored, hashed in `batches_sha256.tsv`), `P02_map.tsv`, five rows appended to `gold_key.tsv`.
  Verified: the rebuild reproduces all 51 frozen batch files byte for byte, the 86 gold rows and `census_map.tsv` unchanged;
  P02 shares no sentence with P01 (0 of 300).
- **The M batches are untouched.** A P02 sentence stays in its M batch (S3: no draw outside the permutations); it is coded
  twice, and `p65_wave3_analyze.py` reads the census from P01 and M01 to M16 only. P02 serves S1.
- **The runner** (`scripts/p65_wave3_run.py`): unit order P01 (DONE, skipped), P02, M01 to M16. After P02 the checker's
  `gate P02` compares P02's D-kappa with `S1_SECOND = 0.60` (printed as numbers, never by direction) and the runner writes
  `wave3/main/S1_LABEL.txt` ("confirmatory" or "exploratory") and continues; it never stops on P02. Caps, ledger, gold
  rule, model-family check, direction-blind checker unchanged; P02 parts are 61 items, per-part caps unchanged ($3.20 Opus,
  $1.60 Sonnet). The coder brief (frozen, unchanged) says "about 405 to 505 items"; P02 has 305.
- **The checker** (`scripts/p65_wave3_check.py`): `S1_SECOND = 0.60`; `gate(unit, bar)`; `gate P02`.
- **The analysis** (`scripts/p65_wave3_analyze.py`): reads `S1_LABEL.txt`; when exploratory, prints `RESULT LABEL:
  EXPLORATORY` first, tags every result line `[exploratory]` and prefixes the gate field. No label file means confirmatory.
- **Queue** rebuilt: three P02 rows inserted, the 51 rows of P01 and M01 to M16 unchanged (brief hashes unchanged).
- **Selftests, fixtures first.** Build: the draw's size, exclusion, reproducibility and a wrong-seed control; 90 distinct gold
  wordings. Checker: the 0.60 bar with a concordant and a discordant control. Analysis: the label reader on a temporary
  file. Runner 8 and 9: a stub coder 2 discordant on P02 only labels the run exploratory, writes S1_LABEL.txt and the
  run reaches M01 with no HALT; a concordant pair labels it confirmatory. All three fixtures FAILED on the amendment-1
  scripts (NameError) and PASS now; selftests 1 to 7 still pass.
- `wave3/main/HALT.txt` (the S1 stop marker) is removed in this commit so the relaunch proceeds; the stop is recorded in the
  run log, amendment 2 and the disagreement read.

Expected P02 cost: P01's successful attempt (505 items) cost $4.19 list, so about $2.60 for 305 items; cap $165 unchanged.

## Hashes (sha256)

| file | before (last FREEZE line) | amended 2026-11-17 |
|---|---|---|
| scripts/p65_wave3_check.py | b2fe6eb9f23977840a8ea3f230b184c6109824e60c826fa3f676b410e3cec8ba | de9b2a6892d392eb30897b7f804816b6f4a3a625959d8d30c3891dea578edeac |
| scripts/p65_wave3_run.py | 3f145e10e8fdeceb94692ab4b1fb7a1703d6b2d93d2ee2a6457c3c25f51488f3 | 7a5dae3aad0079432fe3f2b1ab03487925e878400c54ebae6f040f59d9a8ba13 |
| scripts/p65_wave3_analyze.py | 55f6cc85ff3dad86ef8bd0417eb8e97c4fc74704f99786ec5fc1fbbe04b23ddd | 64b278bc468a2e5813279a320afdf9c19620274b88de31a78eaa75cf306c010e |
| scripts/p65_wave3_id_build.py | 9dbf7fc8a16afff3e2f976e3a7eb7a106ee9609404c872ae74f5e8d0616ac47b | 9163b8d95f13722c9cb7f9e436f812c7dea9448866b7dff0c76b564b5a74a831 |
| wave3/main/queue.tsv | 83a2802593434cc639557752c02d9860f14b3e5e9431f459a13dc03cda8b0d70 | 7cb10255539382f1eda08344033bc5f3968dd64a109f2bd93243275a18626156 |
| wave3/main/batches/gold_key.tsv | cb1ea3e91e0ee67652b31c7476217018a7bfd423d926cf08f43f8bb88b0a6c18 | e38feae47ccb55d57299fc03fc5fa1bf25ffe87f919b5898b3b5613e44a1fec6 |
| wave3/main/batches/batches_sha256.tsv | 7a02ba28eef682c4359fabdbc35049afbf9d4778c930bf80e70c17f8398b76fa | ba477ee571698a78810e1678266030e9bc502493d51fd0d05ff51684d2e5563b |
