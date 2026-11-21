"""Unit 4 extraction (registration docs/p65_unit4-spatial-change-verbs_registration_2026-11-19.md).
Usage: python3 -I p65_unit4_extract.py <ud r2.18 dir> <out dir>
Writes: p65_unit4_key.tsv (id, source file, sent_id, token id, lemma, form, plant answer),
        p65_unit4_items_coderA.tsv / _coderB.tsv (id, lemma, marked sentence; shuffled seeds 1 and 2).
Sentence text: UD English EWT and GUM r2.18, CC BY-SA 4.0 (EWT) / CC BY(-NC)-SA per GUM README."""
import sys, os, glob, random
LEMMAS = set("""alternate ameliorate amortize anneal temper normalize bioaccumulate break checker chisel co-vary
convalesce crash creep dawn daypart decrease depreciate develop drip-feed evanesce fade fleet pass explode filter
fine flit gather glean graduate grizzle grow interchange iterate knit lull marinate mature mellow migrate mushroom
overfish overprint phase plateau proliferate pulse refract reoxidize rust scaffold scrape scratch shade shawshank
shift shoot sink slug soil stale step superannuate time-change track turn uptalk vanish fly vaporize vary wear wipe
wizen melt""".split())
assert len(LEMMAS) == 76, len(LEMMAS)  # registration text says 81: miscount; list identical, see results deviations
PLANTS = [
    ('turn', 'SPATIAL', 'Beyond the old bridge the trail [[turns]] sharply north and follows the ridge to the summit.'),
    ('shade', 'SPATIAL', 'The cliff face [[shades]] from deep red at its base to pale yellow near the top.'),
    ('grow', 'TEMPORAL', 'Over the summer the puppy [[grew]] to almost twice its size.'),
    ('pass', 'NOT-CHANGE', 'Could you [[pass]] me the report when you are done with it?'),
    ('vary', 'OTHER-DIM', 'The boiling point of the mixture [[varies]] with the pressure in the vessel.'),
]
ud, out = sys.argv[1], sys.argv[2]
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
for lem, ans, s in PLANTS:
    uses.append(('PLANT', 'PLANT', '0', lem, '', s, ans))
rng = random.Random(20261119)
ids = rng.sample(range(1000, 10000), len(uses))
items = [('U%d' % i,) + u for i, u in zip(ids, uses)]
with open(os.path.join(out, 'p65_unit4_key.tsv'), 'w', encoding='utf-8') as f:
    f.write('id\tfile\tsent_id\ttoken\tlemma\tform\tsentence\tplant_answer\n')
    for it in sorted(items):
        f.write('\t'.join(it) + '\n')
for tag, seed in (('A', 1), ('B', 2)):
    L = items[:]
    random.Random(seed).shuffle(L)
    with open(os.path.join(out, 'p65_unit4_items_coder%s.tsv' % tag), 'w', encoding='utf-8') as f:
        f.write('id\tlemma\tsentence\n')
        for it in L:
            f.write('%s\t%s\t%s\n' % (it[0], it[4], it[6].replace('\t', ' ')))
print('items per coder', len(items))
