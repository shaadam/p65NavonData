"""Language-stratified check of the direction-blind contrast (P against T+NEITHER), adjudicated codes."""
import csv
from statsmodels.stats.contingency_tables import StratifiedTable
A='/Users/as/_Claude/Claude/worktrees/p65-stats-fix/dependence/adversarial/'; D=A+'../'
rd=lambda p: list(csv.DictReader(open(p),delimiter='\t',quoting=csv.QUOTE_NONE))
c={r['bid']:r['code'] for r in rd(A+'p65_depadv_final.tsv')}; mp={r['bid']:r['item'] for r in rd(A+'p65_depadv_blind_map.tsv')}
it={r['item']:r for r in rd(D+'p65_dep_items.tsv')}
for label, grpP, grpO in [('P vs T+NEITHER',{'P'},{'T','NEITHER'}),('P vs NEITHER',{'P'},{'NEITHER'}),('P+BOTH vs T+NEITHER (place needs time vs not)',{'P','BOTH'},{'T','NEITHER'})]:
    tabs=[]
    for lg in ['en','id']:
        t=[[0,0],[0,0]]
        for b,i in mp.items():
            if i.startswith('PL') or it[i]['corpus']!=lg or c[b] not in grpP|grpO: continue
            t[0 if c[b] in grpP else 1][0 if it[i]['final']=='TP' else 1]+=1
        tabs.append(t)
    st=StratifiedTable(tabs); lo,hi=st.oddsratio_pooled_confint()
    print(f'{label}: tables {tabs}; MH OR {st.oddsratio_pooled:.2f} [{lo:.2f}, {hi:.2f}], CMH p {st.test_null_odds().pvalue:.3g}, homogeneity p {st.test_equal_odds().pvalue:.2f}')
