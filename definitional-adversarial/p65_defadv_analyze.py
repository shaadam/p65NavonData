"""P65 definitional adversarial: score plants, agreement, join direction AFTER codes are fixed, build final table,
run the registered model (copy of the registered association script) on each label."""
import csv, subprocess, sys
from collections import Counter
A = '/Users/as/_Claude/Claude/worktrees/p65-stats-fix/definitional-adversarial/'
DEF = '/Users/as/_Claude/Claude/worktrees/p65-definitional-dependence-2026-11-18/definitional/p65_defdep_final.tsv'
rd = lambda p: list(csv.DictReader(open(p), delimiter='\t', quoting=csv.QUOTE_NONE))
mp = {r['bid']: r['item'] for r in rd(A + 'p65_defadv_blind_map.tsv')}
pl = {r['pid']: r['expected'] for r in rd(A + 'p65_defadv_plants.tsv')}
codes = {}
for c in ('A', 'B'):
    rows = rd(A + f'coder{c}/codes.tsv'); assert len(rows) == 249, (c, len(rows))
    assert [r['bid'] for r in rows] == sorted(mp), c
    codes[c] = {mp[r['bid']]: r['code'].strip().upper() for r in rows}
    assert set(codes[c].values()) <= {'TBP', 'PBT', 'BOTH', 'NEITHER'}, set(codes[c].values())
out = []; P = out.append
P('PLANTS (scored before direction is joined)')
for c in ('A', 'B'):
    miss = [(p, codes[c][p], e) for p, e in pl.items() if codes[c][p] != e]
    P(f'  coder {c}: {6-len(miss)}/6; misses {miss}')
items = [i for i in codes['A'] if i not in pl]; assert len(items) == 243
# kappa on 4 codes and on binary
def kappa(x, y):
    n = len(x); po = sum(a == b for a, b in zip(x, y)) / n
    cx, cy = Counter(x), Counter(y); pe = sum(cx[k] * cy[k] for k in cx) / n / n
    return (po - pe) / (1 - pe)
xa = [codes['A'][i] for i in items]; xb = [codes['B'][i] for i in items]
P(f'AGREEMENT (243 items): 4-code kappa {kappa(xa, xb):.3f}; binary kappa '
  f'{kappa([a != "NEITHER" for a in xa], [b != "NEITHER" for b in xb]):.3f}; '
  f'counts A {dict(Counter(xa))}, B {dict(Counter(xb))}')
# join direction now
fin = {r['item']: r for r in rd(DEF)}
with open(A + 'p65_defadv_final.tsv', 'w') as f:
    f.write('item\tcorpus\tfinal\tcodeA\tcodeB\tdefA\tdefB\tinter\tunion\treg_def\treg_subtype\tsynthPT\n')
    for i in items:
        r = fin[i]; a, b = codes['A'][i], codes['B'][i]
        dA, dB = int(a != 'NEITHER'), int(b != 'NEITHER')
        f.write(f"{i}\t{r['corpus']}\t{r['final']}\t{a}\t{b}\t{dA}\t{dB}\t{dA*dB}\t{max(dA,dB)}\t{r['definitional']}\t"
                f"{r['subtype']}\t{int(r['final']=='PT')}\n")
F = rd(A + 'p65_defadv_final.tsv')
P('\nCELLS by code (TP / n), per coder, direction joined after codes fixed')
for c in ('A', 'B'):
    for k in ('TBP', 'PBT', 'BOTH', 'NEITHER'):
        s = [r for r in F if r['code' + c] == k]
        P(f"  coder {c} {k:8s} TP {sum(r['final']=='TP' for r in s):3d} / {len(s):3d}")
agree = [r for r in F if r['codeA'] == r['codeB']]
for k in ('TBP', 'PBT', 'BOTH', 'NEITHER'):
    s = [r for r in agree if r['codeA'] == k]
    P(f"  both agree {k:8s} TP {sum(r['final']=='TP' for r in s):3d} / {len(s):3d}")
P('\nREGISTERED 12 definitional rows: blind codes')
for r in F:
    if r['reg_def'] == '1': P(f"  {r['item']:6s} {r['final']} reg {r['reg_subtype']:4s} A {r['codeA']:7s} B {r['codeB']}")
P('\nREGISTERED vs BLIND (intersection) 2x2: ' + str(Counter((r['reg_def'], r['inter']) for r in F)))
txt = '\n'.join(out); print(txt); open(A + 'p65_defadv_analysis_run_2026-11-19.txt', 'w').write(txt + '\n')
for col in ('inter', 'union', 'defA', 'defB', 'synthPT'):
    subprocess.run([sys.executable, '-I', A + 'p65_defadv_assoc.py', col, A + 'p65_defadv_final.tsv', col], check=True,
                   stdout=subprocess.DEVNULL)
print('model runs written')
