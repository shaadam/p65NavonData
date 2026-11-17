"""Registered analysis for p65 Arm B (p65_change-verbs-registration_2026-11-14.md).
Usage: python3 -I p65_change_verbs_analyze.py <codes dir> <items_key.tsv (with definitions)> [--control-transpose]
Prints: final-code rule, falsifier hits (verbatim), plants, recall, positive controls, matrices,
order fit + permutation control + transpose control, F2, F3, F5, Garner dependence table."""
import sys, os, math, random, itertools
from collections import Counter, defaultdict
DIMS = ['TIME', 'POSITION', 'SIZE', 'COLOUR', 'INTENSITY', 'QUANTITY', 'OTHER']
OVER2DIM = {'TIME': 'TIME', 'SPACE': 'POSITION', 'SIZE': 'SIZE', 'COLOUR': 'COLOUR', 'INTENSITY': 'INTENSITY',
            'QUANTITY': 'QUANTITY', 'OTHER': 'OTHER'}
NAVON_TIME = {'grow', 'mature', 'fade'}
NAVON_SPACE = {'shade', 'slope'}

def load(dirn, pre, nb):
    c = {}
    for b in range(1, nb + 1):
        p = os.path.join(dirn, '%s%d.tsv' % (pre, b))
        with open(p, encoding='utf-8') as f:
            f.readline()
            for line in f:
                q = (line.rstrip('\n').split('\t') + ['', '', ''])[:4]
                c[q[0]] = tuple(x.strip() for x in q[1:4])
    return c

def maj(vals, cval):
    m = Counter(vals).most_common()
    return m[0][0] if m[0][1] >= 2 else cval

def final(a, b, c):
    if a == b:
        return a
    ch = maj([a[0], b[0], c[0]], c[0])
    if ch == 'N':
        return ('N', '', '')
    ys = [x for x in (a, b, c) if x[0] == 'Y']
    cy = c if c[0] == 'Y' else ys[0]
    return ('Y', maj([x[1] for x in ys], cy[1]) if len(ys) > 1 else ys[0][1],
            maj([x[2] for x in ys], cy[2]) if len(ys) > 1 else ys[0][2])

def wilson(k, n, z=1.96):
    if n == 0:
        return (float('nan'), float('nan'))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (c - h, c + h)

def dirn(code):
    """directional (changing dim, over dim) or None"""
    if code[0] != 'Y' or code[2] not in OVER2DIM:
        return None
    a, b = code[1], OVER2DIM[code[2]]
    if a == b or a not in DIMS:
        return None
    return (a, b)

def loss(order, M):
    r = {d: i for i, d in enumerate(order)}
    # "a over b": b should dominate (rank above, smaller index). Violation if a ranked above b.
    return sum(v for (a, b), v in M.items() if r[a] < r[b])

def best_orders(M):
    best, arg = None, []
    for o in itertools.permutations(DIMS):
        l = loss(o, M)
        if best is None or l < best:
            best, arg = l, [o]
        elif l == best:
            arg.append(o)
    return best, arg

def main():
    cd, keyf = sys.argv[1], sys.argv[2]
    transpose = '--control-transpose' in sys.argv
    A, B = load(cd, 'A', 3), load(cd, 'B', 3)
    C = load(cd, 'C', 1)
    key = {}
    with open(keyf, encoding='utf-8') as f:
        f.readline()
        for line in f:
            p = line.rstrip('\n').split('\t')
            key[p[0]] = dict(d=p[1], sid=p[2], hw=p[3], cand=int(p[4]), tc=int(p[5]), st=p[6], df=p[7])
    F = {}
    for i in A:
        if A[i] == B[i]:
            F[i] = A[i]
        else:
            F[i] = final(A[i], B[i], C[i])
    out = []
    pr = lambda *x: print(*x)
    pr('== FINAL CODES: %d items; A=B on %d; adjudicated %d' % (len(F), sum(A[i] == B[i] for i in A), len(C)))
    timeover = lambda x: x[0] == 'Y' and x[1] == 'TIME' and x[2] in OVER2DIM and x[2] != 'TIME'
    posover = lambda x: x[0] == 'Y' and x[1] == 'POSITION' and x[2] in ('SIZE', 'COLOUR', 'INTENSITY', 'QUANTITY', 'OTHER')
    for label, test in (('FALSIFIER time changes over a non-time dimension', timeover),
                        ('SECONDARY position changes over a non-time non-space dimension', posover)):
        both = [i for i in F if test(A[i]) and test(B[i])]
        disp = [i for i in F if (test(A[i]) or test(B[i]) or test(F[i])) and i not in both]
        pr('\n== %s' % label)
        for tag, L in (('BOTH CODERS', both), ('DISPUTED (one coder or final only)', disp)):
            real = [i for i in L if 'P' not in key[i]['st']]
            pl = [i for i in L if 'P' in key[i]['st']]
            pr('-- %s: real senses %d, plants %d' % (tag, len(real), len(pl)))
            for i in sorted(real, key=lambda i: key[i]['sid']):
                k = key[i]
                pr('   %s %s %s [%s] A=%s B=%s F=%s :: "%s"' % (i, k['d'], k['sid'], k['hw'], '/'.join(A[i]),
                                                               '/'.join(B[i]), '/'.join(F[i]), k['df']))
    nm = [i for i in F if F[i][0] == 'Y' and F[i][1] == 'TIME' and F[i][2] == 'ITEMS' and 'P' not in key[i]['st']]
    pr('\n-- near-miss TIME over ITEMS (final): %d' % len(nm))
    for i in nm:
        pr('   %s %s [%s] :: "%s"' % (key[i]['d'], key[i]['sid'], key[i]['hw'], key[i]['df']))
    # plants
    pl = [i for i in F if 'P' in key[i]['st']]
    flagged = [i for i in pl if timeover(A[i]) and timeover(B[i]) and key[i]['tc'] == 1]
    pr('\n== NEGATIVE CONTROL plants: %d of %d flagged (in T-census and both coders time-over-X)' % (len(flagged), len(pl)))
    for i in pl:
        pr('   %s A=%s B=%s' % (key[i]['hw'], '/'.join(A[i]), '/'.join(B[i])))
    real = [i for i in F if 'P' not in key[i]['st']]
    # recall
    pr('\n== RECALL (random 200 verb senses per dictionary, final codes)')
    for d in ('WN', 'GC', 'WK'):
        R = [i for i in real if key[i]['d'] == d and 'R' in key[i]['st']]
        ch = [i for i in R if F[i][0] == 'Y']
        miss = [i for i in ch if key[i]['cand'] == 0]
        lo, hi = wilson(len(miss), len(ch))
        tm = [i for i in ch if F[i][1] == 'TIME']
        tmiss = [i for i in tm if key[i]['tc'] == 0]
        pr('   %s: sample %d, change senses %d (%.1f%%), missed by candidate filter %d = %.2f (95%% %.2f-%.2f); '
           'time-dimension senses %d, outside T-census %d' % (d, len(R), len(ch), 100 * len(ch) / len(R), len(miss),
                                                             len(miss) / max(1, len(ch)), lo, hi, len(tm), len(tmiss)))
        for i in tmiss:
            pr('      time sense outside census: %s [%s] F=%s :: "%s"' % (key[i]['sid'], key[i]['hw'], '/'.join(F[i]), key[i]['df']))
    # positive controls
    pr('\n== POSITIVE CONTROLS (Navon verbs; final codes)')
    for d in ('WN', 'GC', 'WK'):
        for grp, want in ((NAVON_TIME, ('TIME', 'UNSPECIFIED')), (NAVON_SPACE, ('SPACE',)), ({'move'}, ('TIME', 'UNSPECIFIED'))):
            S = [i for i in real if key[i]['d'] == d and 'N' in key[i]['st'] and F[i][0] == 'Y'
                 and set(h.lower() for h in key[i]['hw'].split('|')) & grp]
            ok = [i for i in S if F[i][2] in want]
            pr('   %s %s: change senses %d, OVER in %s: %d; OVER counts %s' % (d, '/'.join(sorted(grp)), len(S), want, len(ok),
                                                                            dict(Counter(F[i][2] for i in S))))
    # cells
    pr('\n== OVER x stratum counts (final, change senses only; real senses)')
    for d in ('WN', 'GC', 'WK'):
        for st in ('C', 'T', 'R'):
            S = [i for i in real if key[i]['d'] == d and st in key[i]['st'] and F[i][0] == 'Y']
            pr('   %s %s n=%d %s' % (d, st, len(S), dict(sorted(Counter(F[i][2] for i in S).items()))))
    # matrices
    def matrix(S):
        M = Counter()
        for i in S:
            x = dirn(F[i])
            if x:
                M[(x[1], x[0]) if transpose else x] += 1
        return M
    def show(M, title):
        pr('\n-- matrix %s (rows: dimension that changes; cols: dimension it changes over); directional n=%d' % (title, sum(M.values())))
        pr('   %-10s' % '' + ''.join('%9s' % c[:8] for c in DIMS))
        for a in DIMS:
            pr('   %-10s' % a + ''.join('%9s' % (M[(a, b)] if a != b else '-') for b in DIMS))
    pr('\n== MATRICES')
    for d in ('WN', 'GC', 'WK', None):
        S = [i for i in real if (d is None or key[i]['d'] == d) and 'C' in key[i]['st']]
        show(matrix(S), '(i) C-sample %s' % (d or 'pooled'))
    show(matrix([i for i in real if 'T' in key[i]['st']]), '(ii) T-census pooled')
    for d in ('WN', 'GC', 'WK'):
        show(matrix([i for i in real if key[i]['d'] == d]), '(iii) all coded, %s' % d)
    M = matrix(real)
    show(M, '(iii) all coded, pooled (VERDICT MATRIX)')
    # UNSPECIFIED beside TIME
    U = Counter(F[i][1] for i in real if F[i][0] == 'Y' and F[i][2] == 'UNSPECIFIED')
    T = Counter(F[i][1] for i in real if F[i][0] == 'Y' and F[i][2] == 'TIME')
    pr('\n-- pooled: over TIME by dim %s; UNSPECIFIED by dim %s (Navon reading rule: UNSPECIFIED counts with TIME)' % (dict(T), dict(U)))
    # order fit
    n = sum(M.values())
    pr('\n== ORDER FIT (exhaustive, 5,040 orders) on pooled matrix (iii), n directional = %d' % n)
    best, arg = best_orders(M)
    pr('   minimum loss %d (%.1f%%); number of minimum orders %d' % (best, 100 * best / max(1, n), len(arg)))
    firsts = Counter(o[0] for o in arg); seconds = Counter(o[1] for o in arg)
    pr('   first place among minimum orders %s; second place %s' % (dict(firsts), dict(seconds)))
    nav = [o for o in itertools.permutations(DIMS) if o[0] == 'TIME' and o[1] == 'POSITION']
    navbest = min(loss(o, M) for o in nav)
    pr('   best Navon-consistent order (TIME, POSITION first) loss %d (%.1f%%)' % (navbest, 100 * navbest / max(1, n)))
    pr('   example minimum order: %s' % ' > '.join(arg[0]))
    # permutation control
    items = [k for k, v in M.items() for _ in range(v)]
    rows = [a for a, b in items]; cols = [b for a, b in items]
    rng = random.Random(20261114)
    worse = 0; mins = []
    NP = 1000
    for _ in range(NP):
        cs = cols[:]
        rng.shuffle(cs)
        Mp = Counter((a, b) for a, b in zip(rows, cs) if a != b)
        lp, _a = best_orders(Mp)
        mins.append(lp / max(1, sum(Mp.values())))
        if lp / max(1, sum(Mp.values())) <= best / max(1, n):
            worse += 1
    mins.sort()
    pr('   permutation control (%d shuffles of the over-dimension, diagonal draws dropped): shuffled minimum loss share median %.3f, '
       '2.5%% %.3f; observed %.3f; p = %.3f' % (NP, mins[NP // 2], mins[int(0.025 * NP)], best / max(1, n), (worse + 1) / (NP + 1)))
    # F5
    fals = sum(1 for i in real if timeover(A[i]) and timeover(B[i]))
    c1 = fals == 0
    c2 = all(o[0] == 'TIME' and o[1] == 'POSITION' for o in arg)
    c3 = navbest <= 0.10 * n
    better_non_navon = best < navbest
    if n < 20:
        f5 = 'NOT TESTABLE'
    elif c1 and c2 and c3:
        f5 = 'PASS'
    elif (not c1) or (not c3) or better_non_navon:
        f5 = 'FAIL'
    else:
        f5 = 'PARTIAL (no strictly better non-Navon order, but some minimum orders are not Navon\'s)'
    pr('\n== F5: %s  [falsifiers both coders %d; all minimum orders TIME>POSITION first: %s; Navon-order loss %d of %d <= 10%%: %s; '
       'strictly better non-Navon order: %s]' % (f5, fals, c2, navbest, n, c3, better_non_navon))
    # F2 / F3
    third = Counter(a for (a, b), v in M.items() for _ in range(v) if a in ('SIZE', 'COLOUR', 'INTENSITY', 'QUANTITY'))
    X = third.most_common(1)[0][0]
    def votes(i, j):  # votes for i dominating j = items "j over i"
        return M[(j, i)], M[(i, j)]
    pairs = [('TIME', 'POSITION'), ('POSITION', X), ('TIME', X)]
    pr('\n== F2/F3 triad TIME, POSITION, %s (X = most frequent changing dimension among SIZE/COLOUR/INTENSITY/QUANTITY: %s)' % (X, dict(third)))
    sh = {}
    testable2 = True; testable3 = True
    for i, j in pairs:
        vi, vj = votes(i, j)
        t = vi + vj
        lo, hi = wilson(vi, t)
        sh[(i, j)] = ((vi + 0.5) / (t + 1), vi, vj)
        pr('   a(%s > %s): %d vs %d, share %s, Wilson 95%% %.3f-%.3f, testable(>=5) %s, clear %s' % (
            i, j, vi, vj, '%.3f' % (vi / t) if t else 'n/a', lo, hi, t >= 5, t >= 5 and (lo > 0.5 or hi < 0.5)))
        testable2 &= t >= 5
        testable3 &= t >= 5 and vi >= 1 and vj >= 1
    dom = {p: (sh[p][1] > sh[p][2]) for p in pairs}
    cyc = (dom[pairs[0]] == dom[pairs[1]]) and (dom[pairs[2]] != dom[pairs[0]])
    f2 = 'NOT TESTABLE' if not testable2 else ('FAIL' if cyc else 'PASS')
    pr('   F2: %s (cycle present: %s)' % (f2, cyc))
    lg = lambda p: math.log(p / (1 - p))
    pred = lg(sh[pairs[0]][0]) + lg(sh[pairs[1]][0])
    pr('   F3 corrected shares: T>P %.3f, P>X %.3f, T>X %.3f; predicted logit(T>X) %.2f vs observed %.2f' % (
        sh[pairs[0]][0], sh[pairs[1]][0], sh[pairs[2]][0], pred, lg(sh[pairs[2]][0])))
    if not testable3:
        f3 = 'NOT TESTABLE (a pair lacks votes in one direction or has < 5)'
    else:
        f3 = 'FAIL' if sh[pairs[2]][0] < max(sh[pairs[0]][0], sh[pairs[1]][0]) else 'PASS'
    pr('   F3: %s' % f3)
    # Garner dependence
    def dep(a, b):
        if b == 'TIME':
            return True
        if a == 'TIME':
            return False
        if b == 'POSITION':
            return a in ('POSITION', 'SIZE', 'COLOUR')
        return False
    pr('\n== GARNER logical dependence on pooled directional items (A over B)')
    lic = Counter(); unl = Counter()
    for (a, b), v in M.items():
        if dep(a, b) and not dep(b, a):
            lic[(a, b)] += v
        else:
            unl[(a, b)] += v
    pr('   licensed by dependence (DEP(A->B)=Y, DEP(B->A)=N): %d; not licensed: %d %s' % (
        sum(lic.values()), sum(unl.values()), dict(unl)))
    for i in real:
        x = dirn(F[i])
        if x and not (dep(*x) and not dep(x[1], x[0])):
            pr('   unlicensed: %s %s [%s] %s over %s :: "%s"' % (key[i]['d'], key[i]['sid'], key[i]['hw'], x[0], x[1], key[i]['df']))

if __name__ == '__main__':
    main()
