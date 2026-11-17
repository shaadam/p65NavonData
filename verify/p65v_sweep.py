"""Verifier's own recall sweep (not the worker's TIME_RE/OVER_RE): every verb sense whose definition pairs a
timing comparative or timing noun with a co-variation marker. Prints hits outside the worker's T-census.
Usage: python3 -I p65v_sweep.py <all_senses.tsv> <items_key.tsv with defs> [--plant]
--plant appends 3 planted time-over-X definitions to the sense list; all must be hit (negative control)."""
import sys, re, csv
TIMING = r'(sooner|later|earlier|faster|slower|longer|shorter|quicker|more (quickly|slowly|rapidly)|time zone|clock|o\'clock|timing|time of|hour of|date of|season of|onset|duration|tempo|rate)'
COVAR = r'(than|according to|depending on|with (the|each|every|increasing|decreasing|distance|altitude|latitude|longitude|temperature|depth|height|size|age)|the (farther|further|higher|lower|more|less|greater|larger|smaller)|in proportion|proportional|from place to place|in different (places|zones|regions|parts)|between .* zones|as .* (increases|decreases|rises|falls))'
P = re.compile(r'\b' + TIMING + r'\b.*\b' + COVAR + r'|\b' + COVAR + r'\b.*\b' + TIMING + r'\b', re.I)
rows = list(csv.reader(open(sys.argv[1], encoding='utf-8'), delimiter='\t'))[1:]
if '--plant' in sys.argv:
    rows += [['WN', 'PL1', 'x', 'to ripen earlier the farther south the orchard lies', ''],
             ['GC', 'PL2', 'y', 'To strike the hour later in each town westward than in the last.', ''],
             ['WK', 'PL3', 'z', 'To vary in onset depending on altitude.', '']]
cen = {r['sense_id'] for r in csv.DictReader(open(sys.argv[2], encoding='utf-8'), delimiter='\t')}
hits = [r for r in rows if P.search(r[3])]
print('hits', len(hits), 'outside coded items', sum(r[1] not in cen for r in hits))
for r in hits:
    if r[1] not in cen: print('%s\t%s\t%s\t%s' % (r[0], r[1], r[2], r[3][:300]))
