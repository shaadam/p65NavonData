"""Compare coders A and B (registered): Cohen's kappa for CHANGE, DIM, OVER; write the disagreement batch for coder C.
Usage: python3 -I p65_change_verbs_compare.py <codes dir> <items_key.tsv with definitions> <out C batch tsv>"""
import sys, os, random
from collections import Counter
def load(dirn, pre):
    c = {}
    for b in (1, 2, 3):
        with open(os.path.join(dirn, '%s%d.tsv' % (pre, b)), encoding='utf-8') as f:
            f.readline()
            for line in f:
                p = (line.rstrip('\n').split('\t') + ['', '', ''])[:4]
                c[p[0]] = tuple(x.strip() for x in p[1:4])
    return c
def kappa(pairs):
    n = len(pairs)
    if n == 0:
        return float('nan'), 0
    po = sum(a == b for a, b in pairs) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / n / n
    return (po - pe) / (1 - pe) if pe < 1 else float('nan'), n, po
def main():
    A, B = load(sys.argv[1], 'A'), load(sys.argv[1], 'B')
    assert set(A) == set(B), 'id sets differ'
    ids = sorted(A)
    print('items', len(ids))
    print('kappa CHANGE (k, n, agreement)', kappa([(A[i][0], B[i][0]) for i in ids]))
    yy = [i for i in ids if A[i][0] == 'Y' and B[i][0] == 'Y']
    print('kappa DIM  ', kappa([(A[i][1], B[i][1]) for i in yy]))
    print('kappa OVER ', kappa([(A[i][2], B[i][2]) for i in yy]))
    print('kappa CELL ', kappa([(A[i][1:], B[i][1:]) for i in yy]))
    dis = [i for i in ids if A[i] != B[i] and not (A[i][0] == 'N' and B[i][0] == 'N')]
    print('disagreements', len(dis))
    key = {}
    with open(sys.argv[2], encoding='utf-8') as f:
        f.readline()
        for line in f:
            p = line.rstrip('\n').split('\t')
            key[p[0]] = (p[3], p[7], p[1])
    random.Random(20261115).shuffle(dis)
    with open(sys.argv[3], 'w', encoding='utf-8') as g:
        g.write('item\theadword\tdefinition\n')
        for i in dis:
            hw, df, d = key[i]
            g.write('\t'.join([i, hw.replace('|', ', ') if d == 'WN' else hw.split('|')[0], df]) + '\n')
if __name__ == '__main__':
    main()
