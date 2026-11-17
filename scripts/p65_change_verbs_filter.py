"""Registered candidate filter (p65_change-verbs-dictionaries_2026-11-14.md, section 'Method').
Usage: python3 -I p65_change_verbs_filter.py <all_senses.tsv> <out_candidates.tsv>
Adds columns cand (1 if the definition matches CHANGE_RE or the sense is a Navon example verb)
and tstrat (1 if a candidate definition also matches TIME_RE: the census stratum for the falsifier)."""
import sys, re
CHANGE_RE = re.compile(r'\b(become|becomes|becoming|became|grow|grows|growing|grew|increase[sd]?|increasing|'
                       r'decrease[sd]?|decreasing|vary|varies|varied|varying|change[sd]?|changing|gradual|gradually|'
                       r'pass(es|ed|ing)? from|turn|turns|turned|turning)\b', re.I)
TIME_RE = re.compile(r'\b(time|times|timing|tempo|duration|date|dates|dated|hour|hours|period|periods|age|ages|aging|'
                     r'ageing|era|season|seasons|schedule|scheduled|clock|clocks|delay|delayed|late|later|earlier|early|'
                     r'sooner|moment|day|days|year|years|pace|when)\b', re.I)
NAVON = {'grow', 'mature', 'fade', 'shade', 'slope', 'move'}
def main():
    src, out = sys.argv[1], sys.argv[2]
    with open(src, encoding='utf-8') as f, open(out, 'w', encoding='utf-8') as g:
        hdr = f.readline().rstrip('\n')
        g.write(hdr + '\tcand\ttstrat\tnavon\n')
        for line in f:
            d, sid, hw, df, ex = line.rstrip('\n').split('\t')
            heads = {h.lower() for h in hw.split('|')}
            nav = 1 if heads & NAVON else 0
            c = 1 if (CHANGE_RE.search(df) or nav) else 0
            t = 1 if (c and TIME_RE.search(df)) else 0
            g.write('\t'.join([d, sid, hw, df, ex, str(c), str(t), str(nav)]) + '\n')
if __name__ == '__main__':
    main()
