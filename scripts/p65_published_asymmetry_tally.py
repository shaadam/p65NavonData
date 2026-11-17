"""Tally coded space-time interference experiments by direction (registered rule:
p65_published-asymmetry-registration_2026-11-13.md).

Usage: python3 -I p65_published_asymmetry_tally.py <coded.tsv> [code|code_2tailed]
Counted rows: code in {SPACE>TIME, TIME>SPACE, SYMMETRIC, NONE}, tag not CLINICAL,
verification not SECONDARY. Prints primary tally, adult-human-visual tally,
paper-level tally, exact two-sided sign test, Wilson 95% intervals.
"""
import csv, sys, math
from collections import Counter, defaultdict

CODES = ['SPACE>TIME', 'TIME>SPACE', 'SYMMETRIC', 'NONE']


def wilson(k, n, z=1.959964):
    if n == 0:
        return (float('nan'), float('nan'))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (c - h, c + h)


def sign_test(a, b):
    n = a + b
    if n == 0:
        return float('nan')
    k = min(a, b)
    p = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
    return min(1.0, 2 * p)


def report(label, rows):
    c = Counter(r['code'] for r in rows)
    n = len(rows)
    print(f'\n== {label}: n = {n} experiments')
    for k in CODES:
        lo, hi = wilson(c[k], n)
        print(f'  {k:11s} {c[k]:3d}  ({c[k]/n if n else 0:.2f}; 95% Wilson {lo:.2f}-{hi:.2f})')
    a, b = c['SPACE>TIME'], c['TIME>SPACE']
    print(f'  sign test SPACE>TIME {a} vs TIME>SPACE {b}: two-sided exact p = {sign_test(a, b):.4f}')
    return c


def main(path, col='code'):
    rows = list(csv.DictReader(open(path), delimiter='\t'))
    for r in rows:
        r['code'] = r[col]
    print(f'coding column: {col}')
    counted = [r for r in rows if r['code'].strip() in CODES
               and 'CLINICAL' not in r['tags'].upper()
               and not r['verification'].upper().startswith('SECONDARY')]
    for r in counted:
        r['code'] = r['code'].strip()
    print(f'rows in file {len(rows)}; counted {len(counted)}')
    report('PRIMARY (all counted)', counted)
    tags = lambda r: r['tags'].upper()
    nonvis = lambda r: 'NONVISUAL' in tags(r) and 'CELL' not in tags(r)
    adult_vis = [r for r in counted if not nonvis(r) and not any(t in tags(r) for t in ('CHILD', 'ANIMAL', 'LING'))]
    report('ADULT HUMAN, VISUAL', adult_vis)
    report('CHILD', [r for r in counted if 'CHILD' in tags(r)])
    report('ANIMAL', [r for r in counted if 'ANIMAL' in tags(r)])
    report('NONVISUAL (primary modality)', [r for r in counted if nonvis(r)])
    report('FULL TEXT only (abstract-only rows dropped)',
           [r for r in counted if not r['verification'].upper().startswith('ABSTRACT')])
    # paper level: majority code; ties -> MIXED
    by = defaultdict(list)
    for r in counted:
        by[r['doi'] or r['key']].append(r['code'])
    pc = Counter()
    for d, cs in by.items():
        m = Counter(cs).most_common()
        pc['MIXED' if len(m) > 1 and m[0][1] == m[1][1] else m[0][0]] += 1
    print(f'\n== PAPER LEVEL: {len(by)} papers: ' + ', '.join(f'{k} {pc[k]}' for k in CODES + ['MIXED']))
    print(f'  sign test (papers) SPACE>TIME {pc["SPACE>TIME"]} vs TIME>SPACE {pc["TIME>SPACE"]}: p = {sign_test(pc["SPACE>TIME"], pc["TIME>SPACE"]):.4f}')


if __name__ == '__main__':
    main(sys.argv[1], *(sys.argv[2:3]))
