"""Unit 4 registered analysis (docs/p65_unit4-spatial-change-verbs_registration_2026-11-19.md).
Usage: python3 -I p65_unit4_analyze.py <unit4 dir>
Reads p65_unit4_key.tsv, p65_unit4_codes_A.tsv, p65_unit4_codes_B.tsv, p65_unit4_adjudication.tsv (id, code, reason).
Prints plants, kappa, final counts, shares (Wilson 95%), Fisher and binomial tests (scipy, cross-checked by a
hand-written exact sum), sensitivity analyses, and every SPATIAL use verbatim."""
import sys, os, math
from collections import Counter
from scipy.stats import fisher_exact, binom_test

CODES = ['TEMPORAL', 'SPATIAL', 'OTHER-DIM', 'ACROSS-ITEMS', 'NOT-CHANGE', 'UNCLEAR']
DIRECTIONAL = {'TEMPORAL', 'SPATIAL', 'OTHER-DIM'}
D = sys.argv[1]


def tsv(name, ncol):
    rows = {}
    with open(os.path.join(D, name), encoding='utf-8') as f:
        for line in f:
            p = line.rstrip('\n').split('\t')
            if p[0] == 'id' or not p[0]:
                continue
            rows[p[0]] = p[1:ncol] if ncol > 2 else p[1].strip()
    return rows


key = {}
with open(os.path.join(D, 'p65_unit4_key.tsv'), encoding='utf-8') as f:
    f.readline()
    for line in f:
        p = line.rstrip('\n').split('\t')
        key[p[0]] = dict(file=p[1], sid=p[2], tok=p[3], lemma=p[4], sent=p[6], plant=p[7])
A, B = tsv('p65_unit4_codes_A.tsv', 2), tsv('p65_unit4_codes_B.tsv', 2)
assert set(A) == set(key) == set(B), (len(A), len(B), len(key))
for c in list(A.values()) + list(B.values()):
    assert c in CODES, c


def wilson(k, n, z=1.959964):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


def kappa(x, y, cats):
    n = len(x)
    po = sum(a == b for a, b in zip(x, y)) / n
    cx, cy = Counter(x), Counter(y)
    pe = sum(cx[c] * cy[c] for c in cats) / n / n
    return (po - pe) / (1 - pe), po


def coll(c):
    return c if c in DIRECTIONAL else 'NONDIR'


def fisher_hand(a, b, c, d):
    """two-sided Fisher by summing hypergeometric probabilities <= observed (no scipy)"""
    r1, c1, n = a + b, a + c, a + b + c + d
    def lp(x):
        return (math.lgamma(r1 + 1) - math.lgamma(x + 1) - math.lgamma(r1 - x + 1) + math.lgamma(n - r1 + 1)
                - math.lgamma(c1 - x + 1) - math.lgamma(n - r1 - c1 + x + 1) - math.lgamma(n + 1)
                + math.lgamma(c1 + 1) + math.lgamma(n - c1 + 1))
    lo, hi = max(0, c1 - (n - r1)), min(r1, c1)
    p0 = lp(a)
    return sum(math.exp(lp(x)) for x in range(lo, hi + 1) if lp(x) <= p0 + 1e-9)


def pr(*s):
    print(*s)


pr('== PLANTS (scored first; 2+ misses = untrusted coder)')
plants = [i for i in key if key[i]['plant']]
for tag, C in (('A (Opus)', A), ('B (Sonnet)', B)):
    miss = [i for i in plants if C[i] != key[i]['plant']]
    pr('  coder %s: %d of %d plants correct%s' % (tag, len(plants) - len(miss), len(plants),
       ''.join('; MISS %s expected %s got %s' % (key[i]['lemma'], key[i]['plant'], C[i]) for i in miss)))
    pr('    -> %s' % ('UNTRUSTED' if len(miss) >= 2 else 'trusted'))
real = sorted(i for i in key if not key[i]['plant'])
pr('\nreal items: %d' % len(real))

pr('\n== AGREEMENT (real items)')
k6, po6 = kappa([A[i] for i in real], [B[i] for i in real], CODES)
k4, po4 = kappa([coll(A[i]) for i in real], [coll(B[i]) for i in real], list(DIRECTIONAL) + ['NONDIR'])
pr('  six codes: agreement %.3f, Cohen kappa %.3f' % (po6, k6))
pr('  collapsed (SPATIAL / TEMPORAL / OTHER-DIM / not directional): agreement %.3f, kappa %.3f' % (po4, k4))
pr('  coder A counts:', dict(Counter(A[i] for i in real)))
pr('  coder B counts:', dict(Counter(B[i] for i in real)))
pr('  confusion (A row, B col):')
pr('    %-13s' % '' + ''.join('%13s' % c for c in CODES))
for a in CODES:
    pr('    %-13s' % a + ''.join('%13d' % sum(1 for i in real if A[i] == a and B[i] == b) for b in CODES))

dis = [i for i in real if A[i] != B[i]]
adj = tsv('p65_unit4_adjudication.tsv', 3) if os.path.exists(os.path.join(D, 'p65_unit4_adjudication.tsv')) else {}
missing = [i for i in dis if i not in adj]
pr('\ndisagreements: %d; adjudicated: %d; missing adjudication: %d' % (len(dis), len([i for i in dis if i in adj]), len(missing)))
if missing:
    sys.exit('adjudication incomplete')
F = {i: (A[i] if A[i] == B[i] else adj[i][0]) for i in real}
for i in F:
    assert F[i] in CODES, (i, F[i])

DICT_NOT_TIME, DICT_N = 9, 121
DICT_SPACE = 6


def report(label, codes, num_set, dict_k):
    cnt = Counter(codes.values())
    n = sum(cnt[c] for c in DIRECTIONAL)
    k = sum(cnt[c] for c in num_set)
    lo, hi = wilson(k, n)
    dlo, dhi = wilson(dict_k, DICT_N)
    odds, pf = fisher_exact([[k, n - k], [dict_k, DICT_N - dict_k]], alternative='two-sided')
    ph = fisher_hand(k, n - k, dict_k, DICT_N - dict_k)
    pb = binom_test(k, n, dict_k / DICT_N, alternative='two-sided')
    pr('  %s: usage %d/%d = %.3f [%.3f, %.3f] vs dictionary %d/%d = %.3f [%.3f, %.3f]' %
       (label, k, n, k / n, lo, hi, dict_k, DICT_N, dict_k / DICT_N, dlo, dhi))
    pr('     Fisher two-sided p = %.4g (hand sum %.4g), odds ratio %.2f; binomial vs p0 two-sided p = %.4g' %
       (pf, ph, odds, pb))
    return k, n, pf


pr('\n== FINAL COUNTS (real items)')
fc = Counter(F.values())
for c in CODES:
    pr('  %-13s %4d  (%.3f of all uses)' % (c, fc[c], fc[c] / len(real)))
pr('\n== PRIMARY: SPATIAL share of directional uses vs dictionary not-over-time 9/121')
k, n, pf = report('primary', F, {'SPATIAL'}, DICT_NOT_TIME)
if k / n > DICT_NOT_TIME / DICT_N and pf < .05:
    v = 'SUPPORTED'
elif k / n < DICT_NOT_TIME / DICT_N and pf < .05:
    v = 'CONTRADICTED'
else:
    v = 'NOT SUPPORTED (no detectable difference)'
pr('  VERDICT: %s' % v)
pr('\n== SENSITIVITY (reported, not verdicts)')
report('(a) SPATIAL vs dictionary SPACE-only 6/121', F, {'SPATIAL'}, DICT_SPACE)
report('(b) SPATIAL+OTHER-DIM vs 9/121', F, {'SPATIAL', 'OTHER-DIM'}, DICT_NOT_TIME)
report('(c1) coder A alone', {i: A[i] for i in real}, {'SPATIAL'}, DICT_NOT_TIME)
report('(c2) coder B alone', {i: B[i] for i in real}, {'SPATIAL'}, DICT_NOT_TIME)
s = fc['SPATIAL']
lo, hi = wilson(s, len(real))
pr('  (d) SPATIAL of all uses: %d/%d = %.3f [%.3f, %.3f]' % (s, len(real), s / len(real), lo, hi))
pr('\n== CONTROL: hand Fisher on a table with no difference (10/100 vs 10/100) should give p = 1: %.4f'
   % fisher_hand(10, 90, 10, 90))

pr('\n== PER LEMMA (final): directional n, SPATIAL n')
lem = sorted(set(key[i]['lemma'] for i in real))
for L in lem:
    ii = [i for i in real if key[i]['lemma'] == L]
    pr('  %-12s uses %4d  directional %4d  spatial %3d  temporal %4d' % (
        L, len(ii), sum(F[i] in DIRECTIONAL for i in ii), sum(F[i] == 'SPATIAL' for i in ii),
        sum(F[i] == 'TEMPORAL' for i in ii)))
pr('\n== EVERY SPATIAL USE (final), verbatim; A/B codes shown')
for i in real:
    if F[i] == 'SPATIAL':
        pr('  %s %s %s [%s] A=%s B=%s :: %s' % (i, key[i]['file'], key[i]['sid'], key[i]['lemma'], A[i], B[i], key[i]['sent']))
pr('\n== USES WHERE ONE CODER SAID SPATIAL (adjudicated)')
for i in real:
    if (A[i] == 'SPATIAL') != (B[i] == 'SPATIAL'):
        pr('  %s [%s] A=%s B=%s final=%s :: %s' % (i, key[i]['lemma'], A[i], B[i], F[i], key[i]['sent']))
