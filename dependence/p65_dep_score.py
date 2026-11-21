"""P65 unit 3: score plants, kappa, disagreement sheet. Reads coder1/codes.tsv, coder2/codes.tsv."""
import csv, sys
D = "/Users/as/_Claude/Claude/worktrees/p65-stats-fix/dependence/"
rd = lambda p: list(csv.DictReader(open(p), delimiter="\t", quoting=csv.QUOTE_NONE))
mp = {r["did"]: r["item"] for r in rd(D + "p65_dep_blind_map.tsv")}
plants = {r["pid"]: r["expected"] for r in rd(D + "p65_dep_plants.tsv")}
blind = {r["did"]: r for r in rd(D + "p65_dep_blind.tsv")}
items = {r["item"]: r for r in rd(D + "p65_dep_items.tsv")}
codes = {}
out = []; P = out.append
for c in ("coder1", "coder2"):
    rows = rd(D + c + "/codes.tsv")
    ids = [r["did"] for r in rows]
    assert ids == sorted(blind), f"{c}: ids/order mismatch ({len(ids)} rows)"
    assert all(r["code"].strip() in ("S", "B", "N") for r in rows), f"{c}: bad code"
    codes[c] = {r["did"]: r["code"].strip() for r in rows}
    miss = [(d, mp[d], codes[c][d], plants[mp[d]]) for d in blind if mp[d] in plants
            and (codes[c][d] == "S") != (plants[mp[d]] == "S")]
    exact = sum(codes[c][d] == plants[mp[d]] for d in blind if mp[d] in plants)
    real = [d for d in blind if mp[d] not in plants]
    from collections import Counter
    P(f"{c}: plants missed (primary binary) {len(miss)}/6 {miss}; exact three-level {exact}/6; "
      f"{'UNTRUSTED' if len(miss) >= 2 else 'trusted'}; real-item codes {dict(Counter(codes[c][d] for d in real))}")

def kappa(a, b):
    n = len(a); cats = sorted(set(a) | set(b))
    po = sum(x == y for x, y in zip(a, b)) / n
    pe = sum((a.count(k) / n) * (b.count(k) / n) for k in cats)
    return (po - pe) / (1 - pe) if pe < 1 else float("nan"), po

def wkappa(a, b, order=("N", "B", "S")):
    k = len(order); idx = {c: i for i, c in enumerate(order)}; n = len(a)
    w = [[(i - j) ** 2 / (k - 1) ** 2 for j in range(k)] for i in range(k)]
    O = [[0] * k for _ in range(k)]
    for x, y in zip(a, b): O[idx[x]][idx[y]] += 1
    ra = [sum(O[i]) for i in range(k)]; cb = [sum(O[i][j] for i in range(k)) for j in range(k)]
    num = sum(w[i][j] * O[i][j] for i in range(k) for j in range(k))
    den = sum(w[i][j] * ra[i] * cb[j] / n for i in range(k) for j in range(k))
    return 1 - num / den

real = [d for d in sorted(blind) if mp[d] not in plants]
a = [codes["coder1"][d] for d in real]; b = [codes["coder2"][d] for d in real]
kp, po = kappa([x == "S" for x in a], [x == "S" for x in b])
kb, pob = kappa([x != "N" for x in a], [x != "N" for x in b])
P(f"kappa primary (S vs not) {kp:.3f} (agreement {po:.3f}); broad (S/B vs N) {kb:.3f} ({pob:.3f}); "
  f"quadratic-weighted three-level {wkappa(a, b):.3f}; exact three-level agreement {sum(x==y for x,y in zip(a,b))/len(a):.3f}")
# negative control on kappa: shuffle coder2 against coder1 must give kappa near 0
import random
rng = random.Random(7); ks = []
for _ in range(500):
    bb = b[:]; rng.shuffle(bb); ks.append(kappa([x == "S" for x in a], [x == "S" for x in bb])[0])
ks.sort(); P(f"kappa shuffle control (500): median {ks[250]:.3f}, 97.5th pct {ks[487]:.3f} -> "
             f"{'FIRED' if abs(ks[250]) < 0.1 else 'DID NOT FIRE'}")
dis = [d for d in real if codes["coder1"][d] != codes["coder2"][d]]
P(f"disagreements on three-level code: {len(dis)}; on primary binary: "
  f"{sum((codes['coder1'][d]=='S') != (codes['coder2'][d]=='S') for d in real)}")
c1n = {r["did"]: r for r in rd(D + "coder1/codes.tsv")}; c2n = {r["did"]: r for r in rd(D + "coder2/codes.tsv")}
with open(D + "p65_dep_adjudication-sheet.tsv", "w") as f:
    f.write("did\titem\tframe\tc1\tc1_conf\tc1_note\tc2\tc2_conf\tc2_note\tprevious_sentence\tsentence\n")
    for d in dis:
        bl = blind[d]
        f.write("\t".join([d, mp[d], bl["frame"], c1n[d]["code"], c1n[d]["confidence"], c1n[d]["note"],
                           c2n[d]["code"], c2n[d]["confidence"], c2n[d]["note"], bl["previous_sentence"], bl["sentence"]]) + "\n")
txt = "\n".join(out); print(txt); open(D + "p65_dep_score_run_2026-11-19.txt", "w").write(txt + "\n")
