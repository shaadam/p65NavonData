"""Build the direction-blind file: entity plus time and place expressions in random order; no sentence, no frame."""
import csv, random, os
A = '/Users/as/_Claude/Claude/worktrees/p65-stats-fix/dependence/adversarial/'
ex = list(csv.DictReader(open(A+'p65_depadv_extracted.tsv'), delimiter='\t', quoting=csv.QUOTE_NONE))
pl = list(csv.DictReader(open(A+'p65_depadv_plants.tsv'), delimiter='\t', quoting=csv.QUOTE_NONE))
assert len(ex) == 243, len(ex)
recs = [(r['item'], r['entity'], r['time_expr'], r['place_expr']) for r in ex] + \
       [(p['pid'], p['entity'], p['time_expr'], p['place_expr']) for p in pl]
rng = random.Random(20261120); rng.shuffle(recs)
os.makedirs(A+'coderA', exist_ok=True); os.makedirs(A+'coderB', exist_ok=True)
with open(A+'p65_depadv_blind.tsv','w') as f, open(A+'p65_depadv_blind_map.tsv','w') as m:
    f.write('bid\tentity\texpr_1\texpr_2\n'); m.write('bid\titem\ttime_first\n')
    for i,(item,ent,t,p) in enumerate(recs,1):
        bid=f'B{i:04d}'; tf = rng.random() < 0.5
        e1,e2 = (t,p) if tf else (p,t)
        f.write(f'{bid}\t{ent}\t{e1}\t{e2}\n'); m.write(f'{bid}\t{item}\t{int(tf)}\n')
print('blind rows', len(recs))
