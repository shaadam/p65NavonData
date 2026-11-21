#!/usr/bin/env python3
"""P65 Section 6.2 (apply pass 2026-11-20, rows G01-48-2, G16-48-2, S-01): weighted recompute of the Section 6.2 'neither' cell.

Independent route: reads the raw TSVs only; imports no project code.
Run: /Users/as/opt/anaconda3/bin/python3 -I dependence/adversarial/p65_depadv_weighted_neither.py
English pairings carry the registered A3 cell weights (population / coded in cell, the estimator of
scripts/p65_navon_arm_a3_analyze.py, re-implemented here). A3b weights (exploratory design) as a sensitivity row.
Indonesian is a census (equal weights), so its weighted share equals its raw share.
Interval: document bootstrap within cells, weights held at the cell weight, 10,000 resamples, seed 20261120.
Controls: (P) the same estimator on all 155 registered-design directional pairings must give 0.738;
(N1) uniform weights must give the raw share, which differs; (N2) swapping TP and PT must give 1 - s.
"""
import csv, random, collections
from scipy.stats import beta, binom_test as _bt
binomtest = lambda k, n: type("R", (), {"pvalue": _bt(k, n)})()

W = '/Users/as/_Claude/Claude/worktrees/p65-stats-fix/'
A = W + 'dependence/adversarial/'
rd = lambda p: list(csv.DictReader(open(p, encoding='utf-8'), delimiter='\t', quoting=csv.QUOTE_NONE))

code = {r['bid']: r['code'] for r in rd(A + 'p65_depadv_final.tsv')}
bmap = {r['bid']: r['item'] for r in rd(A + 'p65_depadv_blind_map.tsv')}
dep = {}
for b, i in bmap.items():
    if not i.startswith('PL'):
        dep[i] = code[b]
items = {r['item']: r for r in rd(W + 'dependence/p65_dep_items.tsv')}
assert set(dep) == set(items), (len(dep), len(items))

cell, doc = {}, {}
for r in rd(W + 'arm-a3-model/p65_a3-armA-cells.tsv'):
    cell[r['item']] = r['cell']
for r in rd(W + 'arm-a-model/p65_model-items_map.tsv'):
    doc[r['item']] = r['doc']
for f in ('arm-a3-model/p65_a3-items_map.tsv', 'arm-a3b-model/p65_a3b-items_map.tsv'):
    for r in rd(W + f):
        cell[r['item']] = r['cell']; doc[r['item']] = r['doc']

# cell weights, population / coded, as printed in the two results files (CELL TABLE)
POP = {'C-T': 151, 'C-N': 49, 'F-T': 2696, 'F-N': 9052, 'R-T': 1561, 'R-N': 17017}
CODED_A3 = {'C-T': 151, 'C-N': 49, 'F-T': 1005, 'F-N': 188, 'R-T': 562, 'R-N': 45}
CODED_A3B = dict(CODED_A3, **{'F-N': 1188, 'R-N': 1045})
w_a3 = {c: POP[c] / CODED_A3[c] for c in POP}
w_a3b = {c: POP[c] / CODED_A3B[c] for c in POP}

def share(its, wt, swap=False):
    tp = sum(wt[cell[i]] for i in its if (items[i]['final'] == 'TP') != swap)
    pt = sum(wt[cell[i]] for i in its if (items[i]['final'] == 'PT') != swap)
    return tp / (tp + pt)

def boot(its, wt, n=10000, seed=20261120):
    rng = random.Random(seed)
    by = collections.defaultdict(lambda: collections.defaultdict(list))
    for i in its:
        by[cell[i]][doc[i]].append(i)
    out = []
    for _ in range(n):
        tp = pt = 0.0
        for c, dd in by.items():
            ks = list(dd)
            for _ in ks:
                for i in dd[ks[rng.randrange(len(ks))]]:
                    if items[i]['final'] == 'TP': tp += wt[c]
                    else: pt += wt[c]
        if tp + pt > 0:
            out.append(tp / (tp + pt))
    out.sort()
    return out[int(.025 * len(out))], out[int(.975 * len(out)) - 1]

def cp(k, n):
    return (beta.ppf(.025, k, n - k + 1) if k else 0.0, beta.ppf(.975, k + 1, n - k) if k < n else 1.0)

en_reg = [i for i in items if items[i]['corpus'] == 'en' and items[i]['sample'] in ('armA', 'a3')]
en_all = [i for i in items if items[i]['corpus'] == 'en']
print('English pairings: registered design (armA + A3) %d, with A3b %d' % (len(en_reg), len(en_all)))

s = share(en_reg, w_a3)
print('CONTROL P (all registered-design directional English, A3 weights): s = %.3f (must be 0.738) -> %s'
      % (s, 'PASS' if abs(s - 0.738) < 0.0005 else 'FAIL'))
s3b = share(en_all, w_a3b)
print('CONTROL P2 (all English incl. A3b, A3b weights): s = %.3f (A3b results file prints 0.823) -> %s'
      % (s3b, 'PASS' if abs(s3b - 0.823) < 0.0005 else 'FAIL'))

for lab in ('NEITHER', 'P', 'BOTH', 'T'):
    for name, its, wt in (('A3 weights, registered design', en_reg, w_a3), ('A3b weights, all English', en_all, w_a3b)):
        sub = [i for i in its if dep[i] == lab]
        k = sum(items[i]['final'] == 'TP' for i in sub)
        cells = collections.Counter((cell[i], items[i]['final']) for i in sub)
        ws = share(sub, wt) if sub else float('nan')
        lo, hi = boot(sub, wt) if lab == 'NEITHER' else (float('nan'),) * 2
        print('%-8s %-30s n %3d raw %d/%d = %.3f  weighted %.3f  boot95 %.3f to %.3f  cells %s'
              % (lab, name, len(sub), k, len(sub), k / len(sub) if sub else float('nan'), ws, lo, hi, dict(cells)))

neU = [i for i in en_reg if dep[i] == 'NEITHER']
uni = {c: 1.0 for c in POP}
print('CONTROL N1 (uniform weights on the registered-design neither cell): %.3f; differs from weighted: %s'
      % (share(neU, uni), abs(share(neU, uni) - share(neU, w_a3)) > 1e-9))
print('CONTROL N2 (TP/PT swapped): %.3f; equals 1 - s: %s'
      % (share(neU, w_a3, swap=True), abs(share(neU, w_a3, swap=True) - (1 - share(neU, w_a3))) < 1e-12))

idn = [i for i in items if items[i]['corpus'] == 'id' and dep[i] == 'NEITHER']
k = sum(items[i]['final'] == 'TP' for i in idn)
lo, hi = cp(k, len(idn))
print('Indonesian neither (census, equal weights): %d/%d = %.3f, exact 95%% %.3f to %.3f, two-sided p = %.3f'
      % (k, len(idn), k / len(idn), lo, hi, binomtest(k, len(idn)).pvalue))
en_n = [i for i in en_all if dep[i] == 'NEITHER']
k = sum(items[i]['final'] == 'TP' for i in en_n)
lo, hi = cp(k, len(en_n))
print('English neither, raw (all samples): %d/%d = %.3f, exact 95%% %.3f to %.3f, two-sided p = %.3f'
      % (k, len(en_n), k / len(en_n), lo, hi, binomtest(k, len(en_n)).pvalue))
