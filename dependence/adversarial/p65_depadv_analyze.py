"""Direction-blind re-test analysis (addendum A). Usage: p65_depadv_analyze.py CODES_TSV(bid,code) LABEL"""
import csv, sys, random
from collections import Counter
from scipy.stats import beta, fisher_exact
A='/Users/as/_Claude/Claude/worktrees/p65-stats-fix/dependence/adversarial/'
D='/Users/as/_Claude/Claude/worktrees/p65-stats-fix/dependence/'
rd=lambda p: list(csv.DictReader(open(p),delimiter='\t',quoting=csv.QUOTE_NONE))
codes={r['bid']:r['code'].strip().upper() for r in rd(sys.argv[1])}; label=sys.argv[2]
mp={r['bid']:r['item'] for r in rd(A+'p65_depadv_blind_map.tsv')}
items={r['item']:r for r in rd(D+'p65_dep_items.tsv')}
orig={r['item']:r for r in rd(D+'p65_dep_final.tsv')}
def cp(k,n):
    if n==0: return (float('nan'),)*2
    return (0.0 if k==0 else beta.ppf(.025,k,n-k+1), 1.0 if k==n else beta.ppf(.975,k+1,n-k))
rows=[]
for bid,it in mp.items():
    if it.startswith('PL'): continue
    rows.append((it, items[it]['final'], items[it]['corpus'], codes[bid]))
assert len(rows)==243
print(f'== {label}: {len(rows)} items; code counts', dict(Counter(r[3] for r in rows)))
def cell(rs,c): 
    s=[r for r in rs if r[3]==c]; k=sum(r[1]=='TP' for r in s); return k,len(s)
out={}
for c in ['P','T','BOTH','NEITHER']:
    k,n=cell(rows,c); lo,hi=cp(k,n); out[c]=(k,n)
    print(f'  {c:8s} TP {k:3d}/{n:3d} = {k/n if n else float("nan"):.3f} [{lo:.3f}, {hi:.3f}]')
    for lg in ['en','id']:
        k2,n2=cell([r for r in rows if r[2]==lg],c)
        print(f'      {lg}: {k2}/{n2}')
def fis(a,b):
    t=[[a[0],a[1]-a[0]],[b[0],b[1]-b[0]]]; return fisher_exact(t)
kP,nP=out['P']; kT,nT=out['T']; kN,nN=out['NEITHER']; kB,nB=out['BOTH']
if nT>=1: print('  Fisher P vs T: OR %.2f p %.3g'%fis(out['P'],out['T']))
pTN=(kT+kN,nT+nN); orr,pp=fis(out['P'],pTN); print(f'  Fisher P vs T+NEITHER: OR {orr:.2f} p {pp:.3g}')
NN=(kN,nN) if nN>=10 else (kN+kB,nN+nB); lo,hi=cp(*NN)
print(f'  NEITHER criterion cell ({"NEITHER" if nN>=10 else "NEITHER+BOTH"}): {NN[0]}/{NN[1]} [{lo:.3f}, {hi:.3f}]')
cT = fis(out['P'],out['T'])[1] if nT>=5 else pp
Tlow = (kT/nT < kP/nP) if nT>=5 else ((kT+kN)/(nT+nN) < kP/nP)
if lo<=.5<=hi and not (lo<=.802<=hi) and Tlow and cT<.05: v='CONFIRMED'
elif pp>=.05 and (lo<=.802<=hi or lo>.802): v='CIRCULAR'
else: v='PARTLY'
print('  VERDICT', v)
# what the original rule never asked: is the time local on TP rows?
tp=[r for r in rows if r[1]=='TP']; loc=sum(r[3] in ('T','BOTH') for r in tp)
print(f'  TP items whose time is local (T or BOTH): {loc}/{len(tp)} = {loc/len(tp):.3f}')
pt=[r for r in rows if r[1]=='PT']; mov=sum(r[3] in ('P','BOTH') for r in pt)
print(f'  PT items whose place needs a time (P or BOTH): {mov}/{len(pt)} = {mov/len(pt):.3f}')
# positive control: blind codes reproduce the original answer to the question the original rule asked
agree=0
for it,d,lg,c in rows:
    o=orig[it]['dependent']=='1'
    blind = c in ('P','BOTH') if d=='TP' else c in ('T','BOTH')
    agree += (o==blind)
print(f'  agreement with original S label on the question it asked: {agree}/243 = {agree/243:.3f}')
# negative control: direction shuffled within language
rng=random.Random(6518); hits=0; R=2000
for _ in range(R):
    sh=[]
    for lg in ['en','id']:
        sub=[r for r in rows if r[2]==lg]; ds=[r[1] for r in sub]; rng.shuffle(ds)
        sh += [(r[0],d,lg,r[3]) for r,d in zip(sub,ds)]
    a=cell(sh,'P'); b=(cell(sh,'T')[0]+cell(sh,'NEITHER')[0], cell(sh,'T')[1]+cell(sh,'NEITHER')[1])
    hits += fis(a,b)[1]<.05
print(f'  shuffle control: P vs T+NEITHER p<.05 in {hits/R:.3f} of {R} shuffles (should be near .05)')
