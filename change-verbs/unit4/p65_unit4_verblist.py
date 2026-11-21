"""Unit 4 step 1: list the dictionary study's 121 directional senses (final codes, plants removed) with headwords.
Reuses the frozen final-code rule from scripts/p65_change_verbs_analyze.py.
Usage: python3 -I p65_unit4_verblist.py <repo root>  -> writes change-verbs/unit4/p65_unit4_directional-senses.tsv"""
import sys, os, importlib.util
R = sys.argv[1]
spec = importlib.util.spec_from_file_location('an', os.path.join(R, 'scripts/p65_change_verbs_analyze.py'))
an = importlib.util.module_from_spec(spec); spec.loader.exec_module(an)
cd = os.path.join(R, 'change-verbs/codes')
A, B, C = an.load(cd, 'A', 3), an.load(cd, 'B', 3), an.load(cd, 'C', 1)
key = {}
with open(os.path.join(R, 'change-verbs/items_key_nodefs.tsv'), encoding='utf-8') as f:
    f.readline()
    for line in f:
        p = line.rstrip('\n').split('\t')
        key[p[0]] = dict(d=p[1], sid=p[2], hw=p[3], st=p[6])
F = {}
for i in A:
    c = C.get(i, A[i])
    F[i] = an.final(A[i], B[i], c)
rows = []
for i in sorted(F):
    if 'P' in key[i]['st']:
        continue
    d = an.dirn(F[i])
    if d:
        rows.append((i, key[i]['d'], key[i]['sid'], key[i]['hw'], F[i][1], F[i][2]))
out = os.path.join(R, 'change-verbs/unit4/p65_unit4_directional-senses.tsv')
with open(out, 'w', encoding='utf-8') as f:
    f.write('item\tdict\tsense_id\theadword\tDIM\tOVER\n')
    for r in rows:
        f.write('\t'.join(r) + '\n')
from collections import Counter
print('directional senses:', len(rows), Counter(r[5] for r in rows))
print('distinct headwords (lowercased):', len(set(r[3].lower() for r in rows)))
