"""Independent recount of p65 Arm B (verifier, 2026-11-14). Own code; does not import the worker's scripts.
Usage: python3 -I p65v_recount.py <codes dir> <items_key.tsv (with or without definitions)> [--plant-wrong]
--plant-wrong: negative control; flips coder B's OVER on the 5 plants to UNSPECIFIED (falsifier count must drop)
and appends a fake extra TIME-over-POSITION real item (falsifier count must rise)."""
import sys, csv, itertools, random, math
from collections import Counter, defaultdict
cd, keyf = sys.argv[1], sys.argv[2]; plant = '--plant-wrong' in sys.argv
def load(names):
    out = {}
    for n in names:
        with open(f'{cd}/{n}.tsv', encoding='utf-8') as f:
            for r in csv.DictReader(f, delimiter='\t'):
                out[r['item']] = (r['CHANGE'], r['DIM'] or '', r['OVER'] or '')
    return out
A = load(['A1', 'A2', 'A3']); B = load(['B1', 'B2', 'B3']); C = load(['C1'])
key = {}
with open(keyf, encoding='utf-8') as f:
    for r in csv.DictReader(f, delimiter='\t'):
        key[r['item']] = r
assert set(A) == set(B) == set(key), (len(A), len(B), len(key))
if plant:
    for i, r in key.items():
        if 'P' in r['strata']: B[i] = (B[i][0], B[i][1], 'UNSPECIFIED')
    key['IFAKE'] = dict(item='IFAKE', dict='WK', sense_id='WK:FAKE', headword='fake', strata='R', cand='0', tcensus='0')
    A['IFAKE'] = B['IFAKE'] = ('Y', 'TIME', 'POSITION'.replace('POSITION', 'SPACE'))
def kappa(pairs):
    n = len(pairs); po = sum(a == b for a, b in pairs) / n
    ca = Counter(a for a, _ in pairs); cb = Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / n / n
    return round((po - pe) / (1 - pe), 4), n
print('kappa CHANGE', kappa([(A[i][0], B[i][0]) for i in A]))
yy = [i for i in A if A[i][0] == 'Y' and B[i][0] == 'Y']
print('kappa DIM', kappa([(A[i][1], B[i][1]) for i in yy]), 'kappa OVER', kappa([(A[i][2], B[i][2]) for i in yy]))
dis = [i for i in A if A[i] != B[i]]
print('A!=B items', len(dis), 'C coded', len(C), 'missing C', len(set(dis) - set(C)), 'extra C', len(set(C) - set(dis)))
F = {}
for i in A:
    if A[i] == B[i]: F[i] = A[i]; continue
    c = C.get(i)
    if c is None: F[i] = A[i]; continue
    fld = []
    for k in range(3):
        vals = [A[i][k], B[i][k], c[k]]; m = Counter(vals).most_common(1)[0]
        fld.append(m[0] if m[1] >= 2 else c[k])
    if fld[0] == 'N': fld = ['N', '', '']
    F[i] = tuple(fld)
DIMS = ['TIME', 'POSITION', 'SIZE', 'COLOUR', 'INTENSITY', 'QUANTITY', 'OTHER']
ov = lambda o: 'POSITION' if o == 'SPACE' else o
real = [i for i in key if 'P' not in key[i]['strata']]
# de-duplicate by sense id (each sense appears once in the key by construction; check)
assert len({key[i]['sense_id'] for i in real}) == len(real)
def directional(codes, i):
    ch, d, o = codes[i]
    return ch == 'Y' and d in DIMS and ov(o) in DIMS and ov(o) != d
fals_both = [i for i in key if A[i][1] == 'TIME' and ov(A[i][2]) in DIMS[1:] and B[i][1] == 'TIME' and ov(B[i][2]) in DIMS[1:] and A[i][0] == B[i][0] == 'Y']
print('falsifier both coders: real', [ (key[i]['sense_id'], key[i]['headword']) for i in fals_both if 'P' not in key[i]['strata']], 'plants', sum('P' in key[i]['strata'] for i in fals_both))
disp = [i for i in real if i not in fals_both and any(x[0] == 'Y' and x[1] == 'TIME' and ov(x[2]) in DIMS[1:] for x in [A[i], B[i], F[i]] + ([C[i]] if i in C else []))]
print('falsifier disputed', [(key[i]['sense_id'], key[i]['headword'], A[i], B[i], C.get(i), F[i]) for i in disp])
M = Counter(); dirs = []
for i in real:
    if directional(F, i):
        M[(F[i][1], ov(F[i][2]))] += 1; dirs.append((F[i][1], ov(F[i][2])))
print('directional real senses', len(dirs), 'over TIME', sum(1 for d, o in dirs if o == 'TIME'), 'over POSITION', sum(1 for d, o in dirs if o == 'POSITION'), 'col counts', Counter(o for _, o in dirs))
print('dim TIME rows', [(d, o) for d, o in dirs if d == 'TIME'])
for d in DIMS: print('  %-9s' % d, ' '.join('%3s' % ('-' if d == o else M[(d, o)]) for o in DIMS))
uns = Counter(F[i][1] for i in real if F[i][0] == 'Y' and F[i][2] == 'UNSPECIFIED'); print('UNSPECIFIED', sum(uns.values()), dict(uns))
# random-sample stratum: share of change senses with OVER UNSPECIFIED
for dct in ('WN', 'GC', 'WK'):
    R = [i for i in real if key[i]['dict'] == dct and 'R' in key[i]['strata'] and F[i][0] == 'Y']
    miss = [i for i in R if key[i]['cand'] == '0']
    print(dct, 'random change', len(R), 'UNSPEC', sum(F[i][2] == 'UNSPECIFIED' for i in R), 'TIME', sum(F[i][2] == 'TIME' for i in R), 'SPACE', sum(F[i][2] == 'SPACE' for i in R), 'missed by filter', len(miss), 'time-dim', [(key[i]['headword'], key[i]['tcensus']) for i in R if F[i][1] == 'TIME'])
def loss(order, data):
    rk = {d: k for k, d in enumerate(order)}
    return sum(1 for d, o in data if rk[d] < rk[o])  # A over B with A ranked above B
def best(data):
    res = [(loss(p, data), p) for p in itertools.permutations(DIMS)]
    m = min(r[0] for r in res); return m, [p for l, p in res if l == m]
m, bo = best(dirs)
nav = ('TIME', 'POSITION', 'SIZE', 'COLOUR', 'INTENSITY', 'QUANTITY', 'OTHER')
navbest = min(loss(p, dirs) for p in itertools.permutations(DIMS) if p[0] == 'TIME' and p[1] == 'POSITION')
print('F5 min loss', m, 'n best orders', len(bo), 'all TIME first', all(p[0] == 'TIME' for p in bo), 'any POSITION second', any(p[1] == 'POSITION' for p in bo), 'best with TIME,POSITION first', navbest, '=%.3f' % (navbest / len(dirs)))
print('  sample best order', bo[0])
tr = [(o, d) for d, o in dirs]; mt, bt = best(tr); print('transpose: TIME last in all best orders', all(p[-1] == 'TIME' for p in bt))
rng = random.Random(7); ds = [d for d, _ in dirs]; os_ = [o for _, o in dirs]; ge = 0; NP = 300
for _ in range(NP):
    rng.shuffle(os_); sh = [(d, o) for d, o in zip(ds, os_)]
    sh = [(d, o) for d, o in sh if d != o]  # diagonal dropped after shuffle
    ge += best(sh)[0] <= m
print('permutation p (min loss <= observed), %d shuffles' % NP, round(ge / NP, 3))
def dep(a, b):
    if b == 'TIME': return a != 'TIME'
    if a == 'TIME': return False
    if b == 'POSITION': return a in ('SIZE', 'COLOUR')  # POSITION->SPACE self dropped as diagonal
    return False
lic = [(d, o) for d, o in dirs if dep(d, o) and not dep(o, d)]
print('Garner licenses', len(lic), 'of', len(dirs), 'not licensed', Counter((d, o) for d, o in dirs if not (dep(d, o) and not dep(o, d))))
pair = lambda x, y: (M[(y, x)], M[(x, y)])  # votes x dominates y, y dominates x
for x, y in [('TIME', 'POSITION'), ('TIME', 'QUANTITY'), ('POSITION', 'QUANTITY'), ('TIME', 'OTHER'), ('POSITION', 'OTHER')]: print('pair', x, y, pair(x, y))
