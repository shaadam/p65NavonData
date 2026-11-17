"""Extract every verb sense from the three dictionaries into one TSV (dict, sense_id, headword, definition).
Usage: python3 -I p65_change_verbs_extract.py <dict dir from p65_change_verbs_fetch.sh> <out.tsv>
WordNet 3.1: one row per verb synset (data.verb), definition = gloss before the first quoted example;
  lexfile 30 = verb.change is kept as a column (seed set, not the boundary).
GCIDE 0.53: <def> texts under a verb <pos> (v. i., v. t., v.) in paragraphs sourced "1913 Webster" only
  (WordNet-derived and later additions excluded).
Wiktionary (kaikki verb JSONL): one row per sense; form-of / alt-of senses excluded; glosses joined with " : ".
"""
import sys, os, re, json, html
D, OUT = sys.argv[1], sys.argv[2]
rows = []
def clean(s):
    s = re.sub(r'\s+', ' ', s).strip()
    return s.replace('\t', ' ')
# WordNet
with open(os.path.join(D, 'wn/dict/data.verb'), encoding='utf-8') as f:
    for line in f:
        if line.startswith('  '):
            continue
        head, gloss = line.split(' | ', 1)
        p = head.split()
        off, lex, wcnt = p[0], int(p[1]), int(p[3], 16)
        lemmas = [p[4 + 2 * i].replace('_', ' ') for i in range(wcnt)]
        g = gloss.strip()
        g = re.split(r';\s*"', g)[0].strip().strip(';').strip()
        rows.append(('WN', 'WN:' + off, '|'.join(lemmas), clean(g), 'verb.change' if lex == 30 else str(lex)))
# GCIDE
ent_re = re.compile(r'<p>(.*?)</p>', re.S)
tag_re = re.compile(r'<[^>]+>')
ENT = {'ldquo': '"', 'rdquo': '"', 'lsquo': "'", 'rsquo': "'", 'mdash': '--', 'ndash': '-', 'amp': '&',
       'eacute': 'e', 'ae': 'ae', 'oe': 'oe', 'br': ' ', 'frac12': '1/2', 'deg': ' deg'}
def gtext(s):
    s = re.sub(r'<([a-z0-9]+)/', lambda m: ENT.get(m.group(1), ''), s)
    s = tag_re.sub('', s)
    return clean(html.unescape(s))
n = 0
for L in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    txt = open(os.path.join(D, 'gcide/gcide-0.53/CIDE.' + L), encoding='latin-1').read()
    hw, pos = None, None
    for m in ent_re.finditer(txt):
        b = m.group(1)
        h = re.search(r'<hw>(.*?)</hw>', b)
        if h:
            hw = gtext(h.group(1)).replace('*', '').replace('"', '').replace('`', '')
            pm = re.search(r'<pos>(.*?)</pos>', b)
            pos = gtext(pm.group(1)) if pm else None
        else:
            pm = re.search(r'^\s*<pos>(.*?)</pos>', b)
            if pm:
                pos = gtext(pm.group(1))
        if not hw or not pos or not re.match(r'v\.( |$|,|\s*[it]\.)', pos):
            continue
        if '1913 Webster' not in b:
            continue
        for d in re.findall(r'<def>(.*?)</def>', b, re.S):
            n += 1
            rows.append(('GC', 'GC:%s%06d' % (L, n), hw, gtext(d), pos))
# Wiktionary
with open(os.path.join(D, 'wikt/kaikki-English-verb.jsonl'), encoding='utf-8') as f:
    for i, line in enumerate(f):
        e = json.loads(line)
        if e.get('pos') != 'verb' or e.get('lang_code') != 'en':
            continue
        for j, s in enumerate(e.get('senses', [])):
            if 'form_of' in s or 'alt_of' in s or not s.get('glosses'):
                continue
            tags = s.get('tags', [])
            if 'form-of' in tags or 'alt-of' in tags:
                continue
            rows.append(('WK', 'WK:%d.%d' % (i, j), e['word'], clean(' : '.join(s['glosses'])), ','.join(tags)))
with open(OUT, 'w', encoding='utf-8') as f:
    f.write('dict\tsense_id\theadword\tdefinition\textra\n')
    for r in rows:
        f.write('\t'.join(r) + '\n')
from collections import Counter
print(Counter(r[0] for r in rows), 'WN verb.change', sum(1 for r in rows if r[4] == 'verb.change'))
