"""Draw the registered coding items (p65_change-verbs-registration_2026-11-14.md).
Usage: python3 -I p65_change_verbs_items.py <flagged.tsv> <outdir>
Writes <outdir>/items_key.tsv (item id -> dict, sense id, strata; NOT shown to coders),
<outdir>/coder{A,B}_batch{1,2,3}.tsv (item, headword, definition; shuffled per coder)."""
import sys, re, random, os, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from p65_change_verbs_filter import CHANGE_RE, TIME_RE
OVER_RE = re.compile(r'\b(place|places|distance|along|across|position|positions|location|locations|region|regions|'
                     r'latitude|longitude|route|space|spatial|different|differ|differs|differing|successive|'
                     r'successively|according to|depending|varies|vary|varying|each|per|zone|zones|stagger|'
                     r'staggered|spread|distribute|distributed|over)\b', re.I)
PLANTS = [('zonelag', 'to occur at progressively later hours of the day as one moves westward along a route'),
          ('hourslope', '(of a timetable) to become later by a fixed number of minutes with each kilometre of distance from the terminus'),
          ('datedrift', 'to fall on an earlier calendar date the farther south the place is'),
          ('thermotime', 'to occur sooner as the temperature increases; to vary in time of onset with the degree of heat'),
          ('duralong', 'to last a longer time with increasing distance from the source; to vary in duration from place to place')]
SEED = 20261114
def main():
    src, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    rows = []
    with open(src, encoding='utf-8') as f:
        f.readline()
        for line in f:
            d, sid, hw, df, ex, c, t, nav = line.rstrip('\n').split('\t')
            rows.append(dict(d=d, sid=sid, hw=hw, df=df, cand=int(c), nav=int(nav),
                             tc=1 if (TIME_RE.search(df) and (CHANGE_RE.search(df) or OVER_RE.search(df))) else 0))
    rng = random.Random(SEED)
    strata = {}
    for d in ('WN', 'GC', 'WK'):
        R = [r for r in rows if r['d'] == d]
        for r in rng.sample([r for r in R if r['cand']], 150):
            strata.setdefault(r['sid'], set()).add('C')
        for r in R:
            if r['tc']:
                strata.setdefault(r['sid'], set()).add('T')
            if r['nav']:
                strata.setdefault(r['sid'], set()).add('N')
        for r in rng.sample(R, 200):
            strata.setdefault(r['sid'], set()).add('R')
    by = {r['sid']: r for r in rows}
    items = [by[s] for s in strata]
    for k, (hw, df) in enumerate(PLANTS):
        sid = 'WN:PLANT%d' % (k + 1)
        by[sid] = dict(d='WN', sid=sid, hw=hw, df=df, cand=1 if CHANGE_RE.search(df) else 0, nav=0,
                       tc=1 if (TIME_RE.search(df) and (CHANGE_RE.search(df) or OVER_RE.search(df))) else 0)
        strata[sid] = {'T', 'P'}
        items.append(by[sid])
    rng.shuffle(items)
    ids = {}
    with open(os.path.join(out, 'items_key.tsv'), 'w', encoding='utf-8') as g:
        g.write('item\tdict\tsense_id\theadword\tcand\ttcensus\tstrata\tdefinition\n')
        for i, r in enumerate(items):
            iid = 'I%04d' % (i + 1)
            ids[r['sid']] = iid
            g.write('\t'.join([iid, r['d'], r['sid'], r['hw'], str(r['cand']), str(r['tc']),
                               ''.join(sorted(strata[r['sid']])), r['df']]) + '\n')
    for coder, cs in (('A', 1), ('B', 2)):
        order = items[:]
        random.Random(SEED + cs).shuffle(order)
        n = len(order)
        for b in range(3):
            part = order[b * n // 3:(b + 1) * n // 3]
            with open(os.path.join(out, 'coder%s_batch%d.tsv' % (coder, b + 1)), 'w', encoding='utf-8') as g:
                g.write('item\theadword\tdefinition\n')
                for r in part:
                    g.write('\t'.join([ids[r['sid']], r['hw'].split('|')[0] if r['d'] != 'WN' else r['hw'].replace('|', ', '), r['df']]) + '\n')
    from collections import Counter
    cnt = Counter()
    for s, st in strata.items():
        for x in st:
            cnt[(by[s]['d'], x)] += 1
    print('items', len(items), sorted(cnt.items()))
    print('plants cand/tcensus', [(by['WN:PLANT%d' % (k + 1)]['cand'], by['WN:PLANT%d' % (k + 1)]['tc']) for k in range(5)])
if __name__ == '__main__':
    main()
