"""Apply the 2026-11-20 full-text recode of the Arm D sources to the per-source list.

Usage: python3 -I scripts/p65_armD_apply_fulltext_recode.py <repo root>
Source of every value: error-evidence/p65_armD_fulltext-recode_2026-11-20.tsv (pass 1; blind pass 2 and its
agreement are in error-evidence/p65_armD_fulltext-recode_2026-11-20.md). Rows are matched by id and source_key;
the script fails if a target row is missing, matched twice, or already carries a different old code than the
recode file records (so it cannot be applied on top of a changed list). Rows the recode marks "not held" keep
their old code and get no edit.
"""
import csv, os, sys

ROOT = sys.argv[1]
T = os.path.join(ROOT, 'error-evidence', 'p65_armD_per-source_2026-11-17.tsv')
R = os.path.join(ROOT, 'error-evidence', 'p65_armD_fulltext-recode_2026-11-20.tsv')

rows = list(csv.DictReader(open(T, encoding='utf-8'), delimiter='\t'))
cols = list(rows[0].keys())
rec = list(csv.DictReader(open(R, encoding='utf-8'), delimiter='\t'))
done = 0
for r in rec:
    hit = [x for x in rows if x['id'] == r['id'] and x['source_key'] == r['source_key']]
    if len(hit) != 1:
        sys.exit('row %s %s matched %d times' % (r['id'], r['source_key'], len(hit)))
    x = hit[0]
    if x['code_basis'] == 'fulltext':
        continue  # already applied
    if (x['direction_code'], x['secondary_code'], x['double_coded']) != (r['old_code'], r['old_secondary'], r['old_double']):
        if (x['direction_code'], x['secondary_code'], x['double_coded']) == (r['new_code'], r['new_secondary'], r['new_double']) \
                and x['code_basis'] == 'fulltext':
            continue  # already applied
        sys.exit('row %s %s: list carries %s, recode file says old code %s' % (
            r['id'], r['source_key'], x['direction_code'], r['old_code']))
    if r['title_page_match'] != 'Y':
        if x['note'].startswith('Not held'):
            continue
        x['note'] = 'Not held at the 2026-11-20 recode; code from %s. %s' % (
            {'ABS': 'the abstract', 'SEC': 'a secondary source'}.get(x['status_in_map'], 'the map (status: %s)' % x['status_in_map']),
            x['note'])
        continue
    x['direction_code'], x['secondary_code'], x['double_coded'] = r['new_code'], r['new_secondary'], r['new_double']
    x['status_in_map'] = 'FULL'
    x['code_basis'] = 'fulltext'
    x['note'] = 'Full text 2026-11-20, p. %s: "%s" %s' % (r['page'], r['quote'], r['note'])
    done += 1

with open(T, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols, delimiter='\t', lineterminator='\n')
    w.writeheader(); w.writerows(rows)
print('applied full-text codes to %d rows; %d rows in the list' % (done, len(rows)))
