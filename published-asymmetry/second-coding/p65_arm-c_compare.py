"""Arm C second coding: merge blinded part files, then (only after merging) compare
with the first coding and re-run the registered tally on the second codes.
Usage: python3 -I p65_arm-c_compare.py <second-coding dir> <original coded.tsv>

Unit ruling (2026-11-19, G04 ledger row 21): the first coding split Jagorska, Steinecker & Riemer (2025) into two
rows by age group (blinded rows 36 and 37). Under the registered unit rule (the experiment as numbered by the authors;
a between-subjects split is tagged BETWEEN, not split) it is one experiment, coded by its main direction test
(trial-type main effect, t(519) = -0.49, p = .62: SYMMETRIC). The coded table now carries row 36 as the merged
experiment and row 37 as MERGED. The frozen second-coding file is not edited; UNIT_RULINGS below applies the same
ruling to the second coder's codes after merging the parts: row 36 takes the merged experiment's code, row 37 is
dropped from agreement and tallies on both sides.
"""
import csv, sys, math, os, glob
from collections import Counter, defaultdict

CODES = ['SPACE>TIME', 'TIME>SPACE', 'SYMMETRIC', 'NONE']
d, orig = sys.argv[1], sys.argv[2]
blind = {r['row']: r for r in csv.DictReader(open(os.path.join(d, 'p65_arm-c_blinded_2026-11-13.tsv')), delimiter='\t')}
parts = {}
for p in sorted(glob.glob(os.path.join(d, 'parts', 'g*.tsv'))):
    for r in csv.DictReader(open(p), delimiter='\t'):
        parts[r['row'].strip()] = {k: (v or '').strip() for k, v in r.items()}
missing = sorted(set(blind) - set(parts), key=int)
assert not missing, f'missing rows {missing}'
cols = ['row', 'key', 'exp', 'code2', 'code2_2tailed', 'S_on_T_stat', 'T_on_S_stat', 'asym_test', 'source', 'justification']
outp = os.path.join(d, 'p65_arm-c-second-coding_2026-11-13.tsv')
with open(outp, 'w', newline='') as g:
    w = csv.writer(g, delimiter='\t')
    w.writerow(cols + ['doi'])
    for row in sorted(blind, key=int):
        w.writerow([parts[row].get(c, '') for c in cols] + [blind[row]['doi']])
print('wrote', outp)
if len(sys.argv) > 3 and sys.argv[3] == '--merge-only':
    sys.exit()

o = list(csv.DictReader(open(orig), delimiter='\t'))
first = {str(i): r for i, r in enumerate(o, 1)}

# unit ruling applied to the second coder (see docstring); the frozen file on disk is unchanged
UNIT_RULINGS = {'36': ('Jagorska2025_young', 'SYMMETRIC'), '37': ('Jagorska2025_older', None)}
for r, (key, code) in UNIT_RULINGS.items():
    assert blind[r]['key'] == key == first[r]['key'], (r, key, blind[r]['key'], first[r]['key'])
    if code is None:
        assert first[r]['code'] == 'MERGED', first[r]['code']
        del blind[r]
    else:
        print(f"unit ruling: row {r} {key} second-coder code {parts[r]['code2']} (2t {parts[r]['code2_2tailed']}) -> {code}")
        parts[r] = dict(parts[r], code2=code, code2_2tailed=code)
print(f'unit ruling: rows compared {len(blind)} (row 37 merged into row 36)')

def norm(c):
    c = c.upper().replace(' ', '')
    for k in CODES + ['UNREACHED']:
        if c.startswith(k):
            return k
    return c

def kappa(pairs):
    n = len(pairs)
    po = sum(a == b for a, b in pairs) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / n / n
    return po, (po - pe) / (1 - pe) if pe < 1 else float('nan')

def sign_test(a, b):
    n = a + b
    k = min(a, b)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n) if n else float('nan')

def wilson(k, n, z=1.959964):
    p = k / n; dd = 1 + z * z / n
    c = (p + z * z / (2 * n)) / dd; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / dd
    return c - h, c + h

def tally(label, codes_by_row):
    rows = [r for r, c in codes_by_row.items() if c in CODES]
    c = Counter(codes_by_row[r] for r in rows); n = len(rows)
    print(f'\n== {label}: n = {n}')
    for k in CODES:
        lo, hi = wilson(c[k], n)
        print(f'  {k:11s} {c[k]:3d} ({c[k]/n:.2f}; 95% Wilson {lo:.2f}-{hi:.2f})')
    a, b = c['SPACE>TIME'], c['TIME>SPACE']
    print(f'  sign test S>T {a} vs T>S {b}: two-sided exact p = {sign_test(a, b):.4f}')
    by = defaultdict(list)
    for r in rows:
        by[blind[r]['doi'] or blind[r]['key']].append(codes_by_row[r])
    pc = Counter()
    for cs in by.values():
        m = Counter(cs).most_common()
        pc['MIXED' if len(m) > 1 and m[0][1] == m[1][1] else m[0][0]] += 1
    print(f'  paper level ({len(by)} papers): ' + ', '.join(f'{k} {pc[k]}' for k in CODES + ['MIXED'])
          + f'; sign p = {sign_test(pc["SPACE>TIME"], pc["TIME>SPACE"]):.4f}')

for mine, theirs in (('code2', 'code'), ('code2_2tailed', 'code_2tailed')):
    allp = [(norm(parts[r][mine]), norm(first[r][theirs])) for r in sorted(blind, key=int)]
    reached = [(a, b) for a, b in allp if a != 'UNREACHED']
    po, k = kappa(reached)
    po_all = sum(a == b for a, b in allp) / len(allp)
    print(f'\n### {mine} vs first {theirs}: reached n = {len(reached)}, raw agreement {po:.3f}, Cohen kappa {k:.3f};'
          f' all {len(allp)} (UNREACHED = disagree) raw {po_all:.3f}')
    # directional collapse: S>T / T>S / non-directional
    col = lambda c: c if c in ('SPACE>TIME', 'TIME>SPACE') else 'NONDIR'
    po3, k3 = kappa([(col(a), col(b)) for a, b in reached])
    print(f'  3-way (S>T / T>S / nondirectional): raw {po3:.3f}, kappa {k3:.3f}')
    conf = Counter(reached)
    print('  confusion (second, first): ' + '; '.join(f'{a}/{b} {n}' for (a, b), n in sorted(conf.items())))

print('\n### DISAGREEMENTS (primary columns)')
for r in sorted(blind, key=int):
    a, b = norm(parts[r]['code2']), norm(first[r]['code'])
    a2, b2 = norm(parts[r]['code2_2tailed']), norm(first[r]['code_2tailed'])
    if a != b or a2 != b2:
        f = first[r]
        print(f"\nrow {r} {blind[r]['key']} exp {blind[r]['exp']}: SECOND {a} (2t {a2}) [{parts[r]['source']}] vs FIRST {b} (2t {b2}) [{f['verification']}]")
        print(f"  second: S->T {parts[r]['S_on_T_stat']} | T->S {parts[r]['T_on_S_stat']} | asym {parts[r]['asym_test']} | {parts[r]['justification']}")
        print(f"  first : S->T {f['S_on_T_stat']} | T->S {f['T_on_S_stat']} | asym {f['asym_test']} | adj {f['adjudication']}")

for mine, theirs in (('code2', 'code'), ('code2_2tailed', 'code_2tailed')):
    sec = {r: norm(parts[r][mine]) for r in blind}
    tally(f'SECOND CODER {mine} (UNREACHED dropped)', sec)
    filled = {r: (c if c != 'UNREACHED' else norm(first[r][theirs])) for r, c in sec.items()}
    tally(f'SECOND CODER {mine} (UNREACHED filled with first code)', filled)
    tally(f'SECOND CODER {mine}, second-coder FULL TEXT rows only',
          {r: c for r, c in sec.items() if parts[r]['source'].upper().startswith('FULL')})
    tally(f'FIRST CODER {theirs} (check)', {r: norm(first[r][theirs]) for r in blind})
