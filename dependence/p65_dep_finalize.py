"""P65 unit 3: final codes from two coders plus analyst adjudication (p65_dep_adjudication.tsv: did, final, reason).
Writes p65_dep_final.tsv (all rules) and p65_dep_final-numeric.tsv (Wolfram route, primary only)."""
import csv
D = "/Users/as/_Claude/Claude/worktrees/p65-stats-fix/dependence/"
rd = lambda p: list(csv.DictReader(open(p), delimiter="\t", quoting=csv.QUOTE_NONE))
mp = {r["did"]: r["item"] for r in rd(D + "p65_dep_blind_map.tsv")}
items = {r["item"]: r for r in rd(D + "p65_dep_items.tsv")}
c1 = {r["did"]: r["code"].strip() for r in rd(D + "coder1/codes.tsv")}
c2 = {r["did"]: r["code"].strip() for r in rd(D + "coder2/codes.tsv")}
adj = {r["did"]: r["final"].strip() for r in rd(D + "p65_dep_adjudication.tsv")}
out = []
for did, item in sorted(mp.items(), key=lambda x: x[1]):
    if item not in items: continue
    a, b = c1[did], c2[did]
    if a == b: fin = a; assert did not in adj
    else: fin = adj[did]
    assert fin in "SBN"
    it = items[item]
    out.append(dict(item=item, did=did, corpus=it["corpus"], final=it["final"], c1=a, c2=b, code=fin,
                    dependent=int(fin == "S"), broad=int(fin in "SB"),
                    union=int("S" in (a, b)), intersection=int(a == b == "S"),
                    union_broad=int(a in "SB" or b in "SB"), intersection_broad=int(a in "SB" and b in "SB")))
assert len(out) == 243
cols = list(out[0])
with open(D + "p65_dep_final.tsv", "w") as f:
    f.write("\t".join(cols) + "\n")
    for r in out: f.write("\t".join(str(r[c]) for c in cols) + "\n")
with open(D + "p65_dep_final-numeric.tsv", "w") as f:
    f.write("item\tcorpus\tfinal\tdependent\n")
    for r in out: f.write(f"{r['item']}\t{r['corpus']}\t{r['final']}\t{r['dependent']}\n")
from collections import Counter
print("final codes by direction:", dict(Counter((r["corpus"], r["final"], r["code"]) for r in out)))
