"""Unit 4b extraction (registration addendum B, docs/p65_unit4-spatial-change-verbs_registration_2026-11-19.md).
Unit 4's extractor (p65_unit4_extract.py) with the verb list and plants changed; marking identical.
Usage: python3 -I p65_unit4b_extract.py <ud r2.18 dir> <unit4b dir with p65_unit4b_verblist.tsv and _wn-senses.tsv> <job dir>
Writes: <unit4b dir>/p65_unit4b_key.tsv (every item, plants answered), <job dir>/U4B_items.tsv (id, type, lemma, text).
Sentence text: UD English EWT and GUM r2.18, CC BY-SA 4.0 (EWT) / CC BY(-NC)-SA per GUM README. WordNet 3.1 licence."""
import sys, os, glob, random
d4b = sys.argv[2]
LEMMAS = set(l.split('\t')[0] for l in open(os.path.join(d4b, 'p65_unit4b_verblist.tsv'), encoding='utf-8').read().splitlines()[1:])
assert len(LEMMAS) == 45, len(LEMMAS)
PLANTS = [
    ('narrow', 'SPATIAL', 'Past the last farmhouse the road [[narrows]] to a single lane.'),
    ('rise', 'SPATIAL', 'From the harbour the streets [[rise]] steeply toward the castle.'),
    ('widen', 'TEMPORAL', 'During the drought the cracks in the field [[widened]] week by week.'),
    ('encompass', 'NOT-CHANGE', 'The new report [[encompasses]] all three northern regions.'),
    ('rise', 'OTHER-DIM', 'The boiling point of the mixture [[rises]] with the pressure in the vessel.'),
]
CAP, CAPSEED = 1200, 20261121
ud, job = sys.argv[1], sys.argv[3]

files = sorted(glob.glob(os.path.join(ud, 'UD_English-EWT', '*.conllu'))) + \
        sorted(glob.glob(os.path.join(ud, 'UD_English-GUM', '*.conllu')))
assert len(files) == 6
uses = []
for fp in files:
    sid, text, toks = None, None, []
    def flush():
        if not toks:
            return
        words = [t for t in toks if t[0].isdigit()]
        for t in words:
            if t[3] == 'VERB' and t[2].lower() in LEMMAS:
                if text:
                    # mark by token offset: rebuild from tokens using SpaceAfter to place [[ ]] exactly
                    pass
                parts = []
                for w in toks:
                    if '.' in w[0]:
                        continue
                    if '-' in w[0]:
                        continue
                    form = '[[%s]]' % w[1] if w is t else w[1]
                    sp = '' if 'SpaceAfter=No' in w[9] else ' '
                    parts.append(form + sp)
                uses.append((os.path.basename(fp), sid, t[0], t[2].lower(), t[1], ''.join(parts).strip(), ''))
    for line in open(fp, encoding='utf-8'):
        line = line.rstrip('\n')
        if line.startswith('# sent_id'):
            sid = line.split('=', 1)[1].strip()
        elif line.startswith('# text ='):
            text = line.split('=', 1)[1].strip()
        elif line == '':
            flush(); sid, text, toks = None, None, []
        elif not line.startswith('#'):
            toks.append(line.split('\t'))
    flush()
print('real uses', len(uses))
if len(uses) > CAP:
    uses = random.Random(CAPSEED).sample(uses, CAP)
    print('sampled', CAP)
for lem, ans, s in PLANTS:
    uses.append(('PLANT', 'PLANT', '0', lem, '', s, ans))
senses = [l.split('\t') for l in open(os.path.join(d4b, 'p65_unit4b_wn-senses.tsv'), encoding='utf-8').read().splitlines()[1:]]
items = [('USE',) + u for u in uses] + [('SENSE', 'WN3.1', x[2], x[0], x[1], '', x[1] + ': ' + x[4], '') for x in senses]
rng = random.Random(20261122)
ids = rng.sample(range(10000, 100000), len(items))
items = [('B%d' % i,) + it for i, it in zip(ids, items)]
with open(os.path.join(d4b, 'p65_unit4b_key.tsv'), 'w', encoding='utf-8') as f:
    f.write('id\ttype\tfile\tsent_id_or_synset\ttoken_or_sense\tlemma\tform\ttext\tplant_answer\n')
    for it in sorted(items):
        f.write('\t'.join(x.replace('\t', ' ') for x in it) + '\n')
L = items[:]
random.Random(3).shuffle(L)
with open(os.path.join(job, 'U4B_items.tsv'), 'w', encoding='utf-8') as f:
    f.write('id\ttype\tlemma\ttext\n')
    for it in L:
        f.write('%s\t%s\t%s\t%s\n' % (it[0], it[1], it[5], it[7].replace('\t', ' ')))
print('items', len(items), 'uses incl plants', sum(1 for i in items if i[1] == 'USE'), 'senses', len(senses))
