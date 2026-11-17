# p65 wave 3 (Indonesian census): amendment 1, pre-data, 2026-11-17 09:14 EST

Approved: Adam, 2026-11-17 (rwj, launch today; the $165 list-price cap stands). Written before any coded direction or
adjudication was seen.

## What was seen

The run launched at 08:58 EST and halted at 09:00 EST on the pilot batch P01: both coders failed the format check twice
(`wave3/main/logs/run.log`: "FAIL format: row P0001" / "row P0002"), $1.55 list price spent (`wave3/main/spend.tsv`, four
rows, kept). The main session and this agent inspected ONLY the format of the four outputs: field counts per row, the
header, the id order, the `confidence` column being one of 1/2/3, the result JSON's `subtype`, cost, `modelUsage` and
final one-line reply. No label, no phrase, no sentence, no direction and no count by label was read or printed. No
adjudication ran.

## Two mechanical defects, neither in the coders' judgement

1. **The checker refused a row whose trailing empty `note` column was dropped.** `codes/P01_coder1_part1.tsv` had 49 of
   101 rows with 5 tab-separated fields and 52 with 6; `P01_coder2_part1.tsv` 56 of 101 with 5. In every 5-field row the
   fifth field is a valid confidence (1/2/3), so the dropped field is the empty `note` (a tab-separated writer with an
   empty last column often omits the trailing tab). Padding the note gives 0 other defects and ids in order, both files.
2. **One `claude -p` call wrote only part 1 of 5 and stopped.** The runner's single prompt asked for five part files "one
   per response". A headless call gives one response: coder 1 replied "done, 101 rows written" (attempts 1 and 2), coder
   2 on attempt 2 replied that it was waiting for the part 2 message. Parts 2 to 5 were never written.

## What changed (scripts only)

- `scripts/p65_wave3_check.py` `read_codes`: a row of exactly 5 fields is padded with an empty `note`; nothing else is
  loosened (label set, confidence set, header, id order and count unchanged).
- `scripts/p65_wave3_run.py`: one `claude -p` job per part file (the coder brief already describes a task message as
  naming one part, its id range and its path, so the brief is unchanged); a part whose file fails format is re-prompted
  once within the attempt (fresh session, same prompt); the gold rule (2 of 5 missed re-codes the batch once, a second
  failure drops the coder and halts) is unchanged; per-part cap `--max-budget-usd` = 2 x (per-coder cap / 5) = $3.20
  Opus, $1.60 Sonnet (P01 part 1 cost $0.57 and $0.26); the global guard "no job starts unless spent + its cap stays within
  $165" and the fail-closed ledger are unchanged, and the $1.55 already spent counts. Ledger `attempt` column now carries
  the part: `1p3`, and `1p3b` for a re-prompt. A budget stop inside a coder thread is now printed and halts the unit.
  `check_freeze` reads FREEZE.txt hash lines last-wins, so this amendment's block supersedes the two script hashes while
  the original lines stay.
- Selftests 5 to 7 (stub model, no money): a stub writing 5-field rows; a stub writing only the first part named in its
  prompt; a stub whose part 3 is garbage once. Fixtures 5 and 6 FAIL on the frozen 2026-11-16 scripts (reproducing the
  09:00 log lines) and PASS on the amended ones; selftests 1 to 4 still pass.

Not changed: the frozen registration, codebook, both briefs, gold key, batches, queue, maps, analysis script.

## Hashes (sha256)

| file | frozen 2026-11-16 | amended 2026-11-17 |
|---|---|---|
| scripts/p65_wave3_check.py | 0e7684ea15b8510854ca96b3f10e0a87f703878ee618d97ce88279e1a9341758 | b2fe6eb9f23977840a8ea3f230b184c6109824e60c826fa3f676b410e3cec8ba |
| scripts/p65_wave3_run.py | 5c4f6f5db36a3e4ade9bfd743f288817a1095d6f75d225e407a7c02dd5f61bd2 | 3f145e10e8fdeceb94692ab4b1fb7a1703d6b2d93d2ee2a6457c3c25f51488f3 |

The P01 outputs of the halted run are kept unread in `wave3/main/results/_failed-2026-11-17/` (two part files, two
DROPPED markers, eight result and meter JSONs); the relaunch re-codes P01 from scratch.
