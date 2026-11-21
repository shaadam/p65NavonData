"""Second route for the Arm D count after the 2026-11-20 full-text recode; shares no code with p65_armD_recount.py.

Usage: python3 -I scripts/p65_armD_count_route2.py <repo root>
Inputs differ from route 1 on purpose: the per-source list as it stood before the recode (git object a3b79ed,
read with `git show`) with the recode file's new codes laid over it by id, so the apply step is checked too.
Lines are split on tabs by hand (no csv module). Prints N, the primary counts, the counts with second codes,
the number of sources read (code not unknown) and the T>S count.
"""
import os, subprocess, sys

ROOT = sys.argv[1]
BASE = 'a3b79ed'
old = subprocess.run(['git', '-C', ROOT, 'show', BASE + ':error-evidence/p65_armD_per-source_2026-11-17.tsv'],
                     capture_output=True, text=True, check=True).stdout.splitlines()
head = old[0].split('\t')
ix = {h: i for i, h in enumerate(head)}
table = {}
for line in old[1:]:
    if not line.strip():
        continue
    f = line.split('\t')
    table[f[ix['id']]] = [f[ix['direction_code']], f[ix['secondary_code']], f[ix['double_coded']]]

rec = open(os.path.join(ROOT, 'error-evidence', 'p65_armD_fulltext-recode_2026-11-20.tsv'), encoding='utf-8').read().splitlines()
rh = rec[0].split('\t')
ri = {h: i for i, h in enumerate(rh)}
for line in rec[1:]:
    f = line.split('\t')
    i = f[ri['id']]
    if i not in table:
        sys.exit('recode id %s not in the base list' % i)
    table[i] = [f[ri['new_code']], f[ri['new_secondary']], f[ri['new_double']]]

order = ['S>T', 'DISSOC', 'MIXED', 'T>S', 'NONE', 'unknown']
prim = dict.fromkeys(order, 0)
both = dict.fromkeys(order, 0)
doubles = 0
for code, sec, dbl in table.values():
    prim[code] += 1
    both[code] += 1
    if dbl == 'Y':
        both[sec] += 1
        doubles += 1
n = len(table)
print('ROUTE 2 (base %s + recode overlay): N = %d' % (BASE, n))
print('  primary   : ' + ' · '.join('%s %d' % (k, prim[k]) for k in order) + '  (sum %d)' % sum(prim.values()))
print('  with 2nd  : ' + ' · '.join('%s %d' % (k, both[k]) for k in order) + '  (sum %d, %d double-coded)' % (sum(both.values()), doubles))
print('  read (code not unknown): %d' % (n - prim['unknown']))
print('  T>S: %d' % prim['T>S'])
