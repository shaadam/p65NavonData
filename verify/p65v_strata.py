"""Verifier: directional senses by sampling route. The T-census is selected on time words, so it can inflate
'over TIME'; this splits the 121 into senses reached by an unbiased draw (C-sample or random R) vs census/Navon only.
Usage: python3 -I p65v_strata.py <codes dir> <items_key_nodefs.tsv>"""
import sys, csv
from collections import Counter
cd, kf = sys.argv[1:3]
def load(ns):
    o = {}
    for n in ns:
        for r in csv.DictReader(open(f'{cd}/{n}.tsv', encoding='utf-8'), delimiter='\t'): o[r['item']] = (r['CHANGE'], r['DIM'], r['OVER'])
    return o
A = load(['A1', 'A2', 'A3']); B = load(['B1', 'B2', 'B3']); C = load(['C1'])
key = {r['item']: r for r in csv.DictReader(open(kf, encoding='utf-8'), delimiter='\t')}
D = ['TIME', 'POSITION', 'SIZE', 'COLOUR', 'INTENSITY', 'QUANTITY', 'OTHER']
ov = lambda o: 'POSITION' if o == 'SPACE' else o
def fin(i):
    if A[i] == B[i]: return A[i]
    f = []
    for k in range(3):
        v = [A[i][k], B[i][k], C[i][k]]; m = Counter(v).most_common(1)[0]; f.append(m[0] if m[1] >= 2 else C[i][k])
    return tuple(f)
for label, test in [('unbiased (C or R)', lambda s: 'C' in s or 'R' in s), ('random R only', lambda s: 'R' in s), ('census/Navon only', lambda s: not ('C' in s or 'R' in s))]:
    cnt = Counter(); n = 0
    for i, r in key.items():
        if 'P' in r['strata'] or not test(r['strata']): continue
        ch, d, o = fin(i)
        if ch == 'Y' and d in D and ov(o) in D and ov(o) != d: cnt[ov(o)] += 1; n += 1
    print(label, 'directional', n, 'over-dimension counts', dict(cnt))
