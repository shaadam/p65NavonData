"""Make a blinded copy of the Arm C coded TSV for the second coder.
Keeps only bibliographic/design columns plus a row id and a 'counted' flag
(the registered inclusion filter, computed here so the coder never sees the
outcome columns). Prints nothing from outcome columns.
Usage: python3 -I p65_arm-c_blind.py <coded.tsv> <blinded_out.tsv>
"""
import csv, sys
KEEP = ['batch', 'key', 'authors', 'year', 'title', 'journal', 'volume', 'pages',
        'doi', 'exp', 'N', 'paradigm', 'space_dim', 'time_dim', 'modality']
CODES = {'SPACE>TIME', 'TIME>SPACE', 'SYMMETRIC', 'NONE'}
src, out = sys.argv[1], sys.argv[2]
with open(src, newline='') as f:
    rows = list(csv.DictReader(f, delimiter='\t'))
n = 0
with open(out, 'w', newline='') as g:
    w = csv.writer(g, delimiter='\t')
    w.writerow(['row'] + KEEP)
    for i, r in enumerate(rows, 1):
        counted = (r['code'].strip() in CODES and 'CLINICAL' not in r['tags'].upper()
                   and not r['verification'].upper().startswith('SECONDARY'))
        if counted:
            n += 1
            w.writerow([i] + [r[k] for k in KEEP])
print(f'wrote {n} counted rows (of {len(rows)})')
