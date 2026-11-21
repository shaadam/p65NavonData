"""Wiktionary verb senses that repeat a Webster 1913 definition (registered rule:
change-verbs/p65_wiktionary-webster-overlap_registration_2026-11-19.md).

Usage: python3 -I p65_wiktionary_webster_overlap.py <senses_all.tsv from p65_change_verbs_extract.py> <repo root>
Prints: exact and near (difflib ratio >= 0.90) match shares over all Wiktionary verb senses and over the coded
Wiktionary items; the change counts (directional senses naming time; unbiased C/R strata) with matched Wiktionary
items removed; and a shuffled-headword negative control (seed 20261119).
"""
import sys, os, re, csv, random, difflib
from collections import defaultdict

SENSES, ROOT = sys.argv[1], sys.argv[2]
NEAR = 0.90
MINW = 3


def norm(s):
    s = s.lower()
    s = re.sub(r'\([^)]*\)|\[[^\]]*\]', ' ', s)
    s = re.sub(r'[^0-9a-z ]', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


def hw(s):
    return re.sub(r'\s+', ' ', s.lower()).strip()


web = defaultdict(set)
wk = {}
with open(SENSES, encoding='utf-8') as f:
    next(f)
    for line in f:
        p = line.rstrip('\n').split('\t')
        d, sid, head, defn = p[0], p[1], p[2], p[3]
        if d == 'GC':
            n = norm(defn)
            if len(n.split()) >= MINW:
                web[hw(head)].add(n)
        elif d == 'WK':
            gl = [norm(g) for g in defn.split(' : ')]
            wk[sid] = (hw(head), [g for g in gl if len(g.split()) >= MINW])


def match(head, glosses, pool):
    cands = pool.get(head, ())
    if not cands or not glosses:
        return False, False
    exact = any(g in cands for g in glosses)
    if exact:
        return True, True
    for g in glosses:
        for c in cands:
            sm = difflib.SequenceMatcher(None, g, c, autojunk=False)
            if sm.real_quick_ratio() >= NEAR and sm.quick_ratio() >= NEAR and sm.ratio() >= NEAR:
                return False, True
    return False, False


res = {sid: match(h, g, web) for sid, (h, g) in wk.items()}
n_all = len(res)
ex_all = sum(1 for v in res.values() if v[0])
nr_all = sum(1 for v in res.values() if v[1])
print(f'Wiktionary verb senses: {n_all}; Webster 1913 headwords with a definition: {len(web)}')
print(f'ALL senses: exact {ex_all} ({ex_all / n_all:.4f}); near (incl. exact) {nr_all} ({nr_all / n_all:.4f})')

# negative control: each sense against a different random headword's Webster definitions
rng = random.Random(20261119)
heads = sorted(web)
ctrl_ex = 0
for sid, (h, g) in wk.items():
    other = rng.choice(heads)
    while other == h:
        other = rng.choice(heads)
    if g and any(x in web[other] for x in g):
        ctrl_ex += 1
print(f'CONTROL (shuffled headword): exact {ctrl_ex} ({ctrl_ex / n_all:.4f})')

# coded items and change counts, final codes by the 2-of-3 rule (as scripts/p65_v1_number-trace.py)
cv = os.path.join(ROOT, 'change-verbs')


def tsv(*p):
    return list(csv.DictReader(open(os.path.join(*p), encoding='utf-8'), delimiter='\t'))


def load(f):
    return {r['item']: (r['CHANGE'], r['DIM'], r['OVER']) for r in tsv(cv, 'codes', f)}


A, B = {}, {}
for i in '123':
    A.update(load(f'A{i}.tsv')); B.update(load(f'B{i}.tsv'))
C = load('C1.tsv')
key = {r['item']: r for r in tsv(cv, 'items_key_nodefs.tsv')}


def maj(vals, tie):
    for v in set(vals):
        if vals.count(v) >= 2:
            return v
    return tie


final = {}
for k in A:
    a, b = A[k], B[k]
    if a == b:
        final[k] = a; continue
    c = C[k]
    if maj([a[0], b[0], c[0]], c[0]) == 'N':
        final[k] = ('N', '', ''); continue
    ys = [x for x in (a, b, c) if x[0] == 'Y']
    cy = c if c[0] == 'Y' else ys[0]
    final[k] = ('Y', maj([x[1] for x in ys], cy[1]) if len(ys) > 1 else ys[0][1],
                maj([x[2] for x in ys], cy[2]) if len(ys) > 1 else ys[0][2])
real = [k for k in final if 'PLANT' not in key[k]['sense_id']]
over = {k: ('POSITION' if final[k][2] == 'SPACE' else final[k][2]) for k in final}

wk_items = [k for k in real if key[k]['dict'] == 'WK']
missing = [k for k in wk_items if key[k]['sense_id'] not in res]
ex_items = [k for k in wk_items if key[k]['sense_id'] in res and res[key[k]['sense_id']][0]]
nr_items = [k for k in wk_items if key[k]['sense_id'] in res and res[key[k]['sense_id']][1]]
print(f'CODED Wiktionary items: {len(wk_items)} (sense id not found in file: {len(missing)}); '
      f'exact {len(ex_items)} ({len(ex_items) / len(wk_items):.4f}); near {len(nr_items)} ({len(nr_items) / len(wk_items):.4f})')


def counts(drop):
    d = [k for k in real if k not in drop and final[k][0] == 'Y' and over[k] not in ('UNSPECIFIED', 'ITEMS', '')
         and over[k] != final[k][1]]
    t = [k for k in d if over[k] == 'TIME']
    u = [k for k in d if 'C' in key[k]['strata'] or 'R' in key[k]['strata']]
    ut = [k for k in u if over[k] == 'TIME']
    dwk = [k for k in d if key[k]['dict'] == 'WK']
    return len(t), len(d), len(ut), len(u), len(dwk)


for label, drop in (('ALL ITEMS', set()), ('EXACT-MATCHED WK REMOVED', set(ex_items)),
                    ('NEAR-MATCHED WK REMOVED', set(nr_items)),
                    ('ALL WK REMOVED (bound)', set(wk_items))):
    t, d, ut, u, dwk = counts(drop)
    print(f'{label}: directional naming time {t} of {d} ({t / d:.3f}); unbiased C/R {ut} of {u}; '
          f'Wiktionary directional left {dwk}')
