"""P65 definitional adversarial: direction-blind file. Two expressions per row, random order; no sentence, no entity,
no frame, no language label. 243 items (unit 3 extraction, sha pinned) + 6 plants, rows shuffled seed 20261121."""
import csv, random, hashlib, os
X = '/Users/as/_Claude/Claude/worktrees/p65-stats-fix/dependence/adversarial/p65_depadv_extracted.tsv'
A = '/Users/as/_Claude/Claude/worktrees/p65-stats-fix/definitional-adversarial/'
assert hashlib.sha256(open(X, 'rb').read()).hexdigest() == 'a45427af88147a36e601bd85633ba9c05eef7845df878bffbadafcd124818a21'
ex = list(csv.DictReader(open(X), delimiter='\t', quoting=csv.QUOTE_NONE)); assert len(ex) == 243
pl = list(csv.DictReader(open(A + 'p65_defadv_plants.tsv'), delimiter='\t', quoting=csv.QUOTE_NONE)); assert len(pl) == 6
recs = [(r['item'], r['time_expr'], r['place_expr']) for r in ex] + [(p['pid'], p['time_expr'], p['place_expr']) for p in pl]
rng = random.Random(20261121); rng.shuffle(recs)
for c in ('coderA', 'coderB'): os.makedirs(A + c, exist_ok=True)
clean = lambda s: s.replace('\t', ' ').replace('\n', ' ').strip()
with open(A + 'p65_defadv_blind.tsv', 'w') as f, open(A + 'p65_defadv_blind_map.tsv', 'w') as m:
    f.write('bid\texpr_1\texpr_2\n'); m.write('bid\titem\ttime_first\n')
    for i, (item, t, p) in enumerate(recs, 1):
        bid = f'E{i:04d}'; tf = rng.random() < 0.5
        e1, e2 = (t, p) if tf else (p, t)
        f.write(f'{bid}\t{clean(e1)}\t{clean(e2)}\n'); m.write(f'{bid}\t{item}\t{int(tf)}\n')
print('blind rows', len(recs))
