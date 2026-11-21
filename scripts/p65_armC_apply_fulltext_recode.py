"""Apply the 2026-11-19 full-text recode of the ten abstract-coded papers to the interference TSV.

Usage: python3 -I p65_armC_apply_fulltext_recode.py <repo root>
Source of every value: published-asymmetry/p65_armC_fulltext-recode_pass1_2026-11-19.tsv (pass 1), agreed by the blind
pass 2 except Reali et al. (2019), ruled SYMMETRIC (rule-application file, ruling section). Rows are matched by key
and experiment; the script fails if a target row is missing or matched twice.
"""
import csv, os, sys

ROOT = sys.argv[1]
T = os.path.join(ROOT, 'published-asymmetry', 'p65_published-asymmetry-coded_2026-11-13.tsv')
P1 = os.path.join(ROOT, 'published-asymmetry', 'p65_armC_fulltext-recode_pass1_2026-11-19.tsv')
VER = 'FULL TEXT (sources/{f}, read with PyMuPDF; 2026-11-19 recode, two blind passes)'
FILES = {
    'CaiWuLiuWang2022': '1-s2.0-S0001691822001238-main.pdf',
    'CharrasPonceLupianezCapizzi2026': 'British J of Psychology - 2026 - Charras - Space time interference ... .pdf',
    'DormalPesenti2013': 's00426-012-0414-3.pdf',
    'HommaAshida2018': 'msr-article-p25_2.pdf',
    'Magnani2014': 's00221-014-4005-y.pdf',
    'PiersonHallez2026': 's13414-026-03371-z.pdf',
    'RealiLlerasAlviar2019': 'Asymmetrical time and space interference in Tau and Kappa effects.pdf',
    'RiemerBratzkeMichael2026': '1-s2.0-S0010028526000174-main.pdf',
    'RiemerShineWolbers2018': 'Hippocampus - 2018 - Riemer - ... .pdf',
    'Sarrazin2004_E1': '2004-14382-001.pdf', 'Sarrazin2004_E2': '2004-14382-001.pdf',
    'Sarrazin2004_E3': '2004-14382-001.pdf',
}
TAGS = {('DormalPesenti2013', '1'): 'BETWEEN (length and duration tasks in separate groups of 18)',
        ('Sarrazin2004_E3', '3'): 'BETWEEN (spatial and temporal tasks in separate groups of 6)'}
RULING = {('RealiLlerasAlviar2019', '1'): '2026-11-19 recode: coders split (pass 1 SYMMETRIC on the flashing group, '
          'pass 2 SPACE>TIME on the static group); ruled SYMMETRIC, conservative (rule-application file, ruling '
          'section). Sensitivity: SPACE>TIME.'}

p1 = list(csv.DictReader(open(P1, encoding='utf-8'), delimiter='\t'))
raw = open(T, encoding='utf-8', newline='').read().split('\r\n')
assert raw[-1] == '', 'expected CRLF-terminated file'
fn = raw[0].split('\t')
rows = [dict(zip(fn, l.split('\t'))) for l in raw[1:-1]]
assert all(len(l.split('\t')) == len(fn) for l in raw[1:-1]), 'ragged row'


def exp_of(s):
    s = s.strip()
    return 'single' if s.startswith(('single', 'unknown')) else s.split()[0] if s else s


done = 0
for q in p1:
    e = q['exp'].strip().split()[0] if not q['exp'].startswith('single') else 'single'
    hits = []
    for r in rows:
        if r['key'] != q['key']:
            continue
        re_ = exp_of(r['exp'])
        if re_ == e or (e in ('1', 'single') and re_ in ('1', 'single', 'unknown', 'all')) \
                or (q['key'].startswith('Sarrazin2004') and r['key'] == q['key']):
            hits.append(r)
    if len(hits) != 1:
        sys.exit(f'row match failed for {q["key"]} exp {q["exp"]}: {len(hits)} hits')
    r = hits[0]
    k = (q['key'], q['exp'].strip().split()[0] if q['exp'][0].isdigit() else '1')
    code = q['pass1_code'] if k not in RULING else 'SYMMETRIC'
    r['exp'] = q['exp']
    r['N'] = q['N']
    r['S_on_T_stat'] = q['S_on_T (page)'].strip()
    r['T_on_S_stat'] = q['T_on_S (page)'].strip()
    r['asym_test'] = q['asym_test (page)'].strip()
    r['code'] = r['code_2tailed'] = code
    r['code_coder'] = code + ' (full text, two blind passes)'
    if k in TAGS:
        r['tags'] = TAGS[k]
    r['adjudication'] = RULING.get(k, '2026-11-19 full-text recode; passes 1 and 2 agree')
    r['verification'] = VER.format(f=FILES[q['key']])
    r['notes'] = (q['note'].strip() + ' | ' if q['note'].strip() else '') + 'Was: ' + r['notes'][:300]
    done += 1

for r in rows:
    for v in r.values():
        assert '\t' not in v and '\n' not in v and '\r' not in v, 'tab or newline in a value'
out = '\r\n'.join(['\t'.join(fn)] + ['\t'.join(r[c] for c in fn) for r in rows]) + '\r\n'
open(T, 'w', encoding='utf-8', newline='').write(out)
print(f'rows updated: {done} of {len(p1)}')
