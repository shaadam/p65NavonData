"""Merge the five coder TSVs into one adjudicated file.

Usage: python3 -I p65_published_asymmetry_merge.py <out.tsv> <coded_A.tsv> ... <coded_D.tsv>
Adjudication (main session, 2026-11-13), applied by rule, logged in column `adjudication`:
  - code normalised to the first token of the coder's code (parenthetical flags kept in notes);
  - Cai & Connell 2012 CogSci rows -> EXCLUDED-DUPLICATE (same samples as Cai & Connell 2015);
  - rows whose code starts with SYMMETRIC (SECONDARY...) -> SECONDARY-NOT-COUNTED;
  - two-tailed sensitivity code in `code_2tailed` for rows whose significance rests on one-tailed tests
    or on a contested asymmetry test (listed in SENS below).
"""
import csv, sys, re

SENS = {  # key|exp -> code if only two-tailed tests / authors' CI are accepted
    'CaiConnell2015_E2|2': ('NONE', 'both directions one-tailed only (S>T p=.094, T>S p=.046 one-tailed)'),
    'CaiConnell2015_E3|3': ('NONE', 'visuohaptic cell rests on one-tailed p'),
    'Kranjec2019_E1|1': ('SYMMETRIC', 'asymmetry test one-tailed on 9 bin means'),
    'Merritt2010_E2b|2b (monkeys, same animals)': ('SYMMETRIC', 'authors call it symmetric; OR CI 0.97-1.63 includes 1'),
    'Jagorska2025_young|1 (younger group)': ('SYMMETRIC', 'own re-analysis of posted data does not reproduce t(36)=2.2'),
    'BratzkeUlrich2025_E1|1 (dimension known in advance? see paradigm)': ('SYMMETRIC', 'asymmetry p=.049/.050 borderline'),
}
CODES = ('SPACE>TIME', 'TIME>SPACE', 'SYMMETRIC', 'NONE')


def main(out, files):
    rows = []
    for f in files:
        for r in csv.DictReader(open(f), delimiter='\t'):
            r['batch'] = f.rsplit('_', 1)[-1].replace('.tsv', '')
            rows.append(r)
    for r in rows:
        raw = r['code'].strip()
        r['code_coder'] = raw
        adj = []
        if 'SECONDARY' in raw.upper() and raw.upper().startswith('SYMMETRIC'):
            code = 'SECONDARY-NOT-COUNTED'; adj.append('secondary evidence only')
        elif r['key'].startswith('CaiConnell2012'):
            code = 'EXCLUDED-DUPLICATE'; adj.append('same samples as Cai & Connell 2015')
        else:
            m = re.match(r'(SPACE>TIME|TIME>SPACE|SYMMETRIC|NONE)', raw)
            code = m.group(1) if m else raw
        r['code'] = code
        k = f"{r['key']}|{r['exp']}"
        hit = [v for kk, v in SENS.items() if kk.split('|')[0] == r['key'] and r['exp'].startswith(kk.split('|')[1][:2].strip())]
        if hit and code in CODES:
            r['code_2tailed'] = hit[0][0]; adj.append('sensitivity: ' + hit[0][1])
        else:
            r['code_2tailed'] = code
        r['adjudication'] = '; '.join(adj)
    cols = ['batch', 'key', 'authors', 'year', 'title', 'journal', 'volume', 'pages', 'doi', 'exp', 'N', 'tags',
            'paradigm', 'space_dim', 'time_dim', 'modality', 'S_on_T_stat', 'T_on_S_stat', 'asym_test',
            'code', 'code_2tailed', 'code_coder', 'adjudication', 'cells', 'effsize_S_on_T', 'effsize_T_on_S',
            'data_public', 'verification', 'notes']
    with open(out, 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter='\t', extrasaction='ignore')
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(len(rows), 'rows written')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2:])
