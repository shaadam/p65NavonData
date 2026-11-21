"""P65 unit 3 adversarial, step 1: is the registered dependence-direction association built in?
Reads the final codes; counts S by direction; then runs a null simulation in which direction is drawn
independently of both dependence facts, and the registered coding rule (code the place fact on TP rows,
the time fact on PT rows) is applied. If the null reproduces the registered verdict, the test is
non-discriminating."""
import csv, math, random, sys
from collections import Counter
D = '/Users/as/_Claude/Claude/worktrees/p65-stats-fix/dependence/'
rows = list(csv.DictReader(open(D + 'p65_dep_final.tsv'), delimiter='\t', quoting=csv.QUOTE_NONE))
print('rows', len(rows))
ct = Counter((r['final'], r['dependent']) for r in rows)
print('crosstab final x dependent(S):', dict(ct))
tp1, tp0, pt1, pt0 = ct[('TP','1')], ct[('TP','0')], ct[('PT','1')], ct[('PT','0')]
a = tp1/(tp1+tp0); b = pt1/(pt1+pt0)
print(f'P(S | TP row; question = does the PLACE need a time) = {tp1}/{tp1+tp0} = {a:.3f}')
print(f'P(S | PT row; question = does the TIME need a place) = {pt1}/{pt1+pt0} = {b:.3f}')
print(f'crude OR = {tp1*pt0/(tp0*pt1):.2f}; s0 = {tp0}/{tp0+pt0} = {tp0/(tp0+pt0):.3f}')
# predictability of label from direction alone
acc = (tp1+pt0)/len(rows); base = max(tp1+pt1, tp0+pt0)/len(rows)
print(f'label predicted from direction alone (TP->S, PT->not S): accuracy {acc:.3f} vs majority {base:.3f}')
def H(ps): return -sum(p*math.log2(p) for p in ps if p>0)
n=len(rows); pS=(tp1+pt1)/n; pT=(tp1+tp0)/n
mi = H([pS,1-pS]) - (pT*H([a,1-a]) + (1-pT)*H([b,1-b]))
print(f'mutual information label;direction = {mi:.3f} bits of H(label) = {H([pS,1-pS]):.3f}')
# identity: s0 is a function of a, b and the margin only
nT, nP = tp1+tp0, pt1+pt0
print(f'identity check s0 = nT(1-a)/(nT(1-a)+nP(1-b)) = {nT*(1-a)/(nT*(1-a)+nP*(1-b)):.3f}')
# null simulation: each item carries BOTH facts independently of direction
def ci_cp(k, m, al=0.05):
    from scipy.stats import beta
    lo = 0.0 if k==0 else beta.ppf(al/2, k, m-k+1); hi = 1.0 if k==m else beta.ppf(1-al/2, k+1, m-k)
    return lo, hi
def verdict(k, m):
    if m < 10: return 'NOT TESTABLE'
    lo, hi = ci_cp(k, m)
    if hi < 0.5: return 'NOT SUPPORTED as stated (leans PT)'
    c5, c8 = lo <= 0.5 <= hi, lo <= 0.802 <= hi
    if c5 and not c8: return 'DEP SUPPORTED'
    if lo > 0.5 and c8: return 'HIER SUPPORTED'
    if lo > 0.5 and hi < 0.802: return 'PARTLY'
    if c5 and c8: return 'UNDECIDED'
    return 'other'
rng = random.Random(20261119); R = 5000; V = Counter(); s0s=[]; ors=[]
for _ in range(R):
    k0=m0=d1=d0=e1=e0=0
    for i in range(n):
        tp = rng.random() < pT          # direction: independent of everything (hierarchy-only world)
        place_needs_time = rng.random() < a
        time_needs_place = rng.random() < b
        dep = place_needs_time if tp else time_needs_place   # the registered rule
        if tp: (d1:=d1+1) if dep else (d0:=d0+1)
        else: (e1:=e1+1) if dep else (e0:=e0+1)
    s0 = d0/(d0+e0); s0s.append(s0); ors.append((d1*e0+.5)/((d0+.5)*(e1+.5)) if True else 0)
    V[verdict(d0, d0+e0)] += 1
s0s.sort(); ors.sort()
print(f'NULL (direction independent of both dependence facts), {R} sims:')
print(f'  median s0 {s0s[R//2]:.3f} [2.5%,97.5%] [{s0s[int(.025*R)]:.3f}, {s0s[int(.975*R)]:.3f}]; median OR {ors[R//2]:.1f}')
print('  registered verdict frequencies:', {k: round(v/R,3) for k,v in V.items()})
# positive control: a world where direction DOES follow dependence, with no hierarchy
rng = random.Random(6518); V2 = Counter()
for _ in range(2000):
    d0=e0=0
    for i in range(n):
        p = rng.random() < 0.80; t = rng.random() < 0.15
        if p and not t: tp = rng.random() < 0.95
        elif t and not p: tp = rng.random() < 0.05
        else: tp = rng.random() < 0.5
        dep = p if tp else t
        if not dep: (d0:=d0+1) if tp else (e0:=e0+1)
    V2[verdict(d0, d0+e0)] += 1
print('DEPENDENCE-ONLY world (direction follows dependence, none-or-both at 0.5): verdicts', {k: round(v/2000,3) for k,v in V2.items()})
