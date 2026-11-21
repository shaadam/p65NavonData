"""Unit 3 addendum A, cross-family route: the blind file for ChatGPT (job p65-unit3b-dependence-blind-HIGH-ADAM-CHAT).
Same rule (p65_depadv_coder-brief.md, sha256 125a268e...9c13d44) and the same 243 extracted rows
(p65_depadv_extracted.tsv) as the Claude coders; 6 new plants (p65_depadv_chatgpt_plants.tsv) replace addendum A's,
whose 'all afternoon' plant reads as local time. New seed 20261123, new ids C0001 on, same per-row coin scheme.
Usage: python3 -I p65_depadv_chatgpt_build.py <job dir>"""
import csv, random, os, sys
A = '/Users/as/_Claude/Claude/worktrees/p65-stats-fix/dependence/adversarial/'
ex = list(csv.DictReader(open(A+'p65_depadv_extracted.tsv'), delimiter='\t', quoting=csv.QUOTE_NONE))
pl = list(csv.DictReader(open(A+'p65_depadv_chatgpt_plants.tsv'), delimiter='\t', quoting=csv.QUOTE_NONE))
assert len(ex) == 243 and len(pl) == 6
recs = [(r['item'], r['entity'], r['time_expr'], r['place_expr']) for r in ex] + \
       [(p['pid'], p['entity'], p['time_expr'], p['place_expr']) for p in pl]
rng = random.Random(20261123); rng.shuffle(recs)
with open(os.path.join(sys.argv[1], 'U3B_items.tsv'), 'w') as f, open(A+'p65_depadv_chatgpt_map.tsv', 'w') as m:
    f.write('bid\tentity\texpr_1\texpr_2\n'); m.write('bid\titem\ttime_first\n')
    for i, (item, ent, t, p) in enumerate(recs, 1):
        bid = f'C{i:04d}'; tf = rng.random() < 0.5
        e1, e2 = (t, p) if tf else (p, t)
        f.write(f'{bid}\t{ent}\t{e1}\t{e2}\n'); m.write(f'{bid}\t{item}\t{int(tf)}\n')
        if item.startswith('CP'):
            print('PLANT', bid, item, [x['answer'] for x in pl if x['pid'] == item][0])
print('rows', len(recs))
