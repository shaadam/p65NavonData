#!/usr/bin/env python3
"""p65_navon_arm_a3_analyze.py -- Arm A3 analysis (registration: p65_arm-a3_registration_2026-11-13.md).

Committed before any A3 code existed; smoke-tested on synthetic codes only.
Inputs: Arm A map + both coder files + adjudication (-> Arm A final labels), Arm A items' A3 cells
(arm-a3-model/p65_a3-armA-cells.tsv), the A3 cell table (p65_a3-cells.tsv), the A3 map, the two A3 coder files
and the A3 adjudication (item<TAB>class<TAB>reason).
Outputs: kappa on the A3 items (bootstrap 95%), the 6-cell table of final labels, the expansion counts
(weight = cell population / coded in cell), s = N_TP/(N_TP+N_PT) with a document bootstrap within cells
(10,000), recall of the T screen per direction, the minimum count and the protocol v2 sec. 5 decision label.
Usage: p65_navon_arm_a3_analyze.py --armA-map M --armA-c1 A --armA-c2 B --armA-adj J --armA-cells AC
       --cells CT --map M3 --c1 A3 --c2 B3 [--adj J3] [--boot 10000] [--seed 20261114]
"""
import argparse, collections, csv, random, sys

CLASSES = ("TP", "PT", "PAR", "AMB", "NA")
CELLS = ("C-T", "C-N", "F-T", "F-N", "R-T", "R-N")


def read(path, key="item"):
    return {r[key]: r for r in csv.DictReader(open(path, encoding="utf-8"), delimiter="\t")}


def kappa(pairs):
    n = len(pairs)
    po = sum(x == y for x, y in pairs) / n
    ca, cb = collections.Counter(x for x, _ in pairs), collections.Counter(y for _, y in pairs)
    pe = sum(ca[k] * cb[k] for k in CLASSES) / n / n
    return (po - pe) / (1 - pe) if pe < 1 else float("nan"), po


def finals(c1, c2, adj, items):
    out, unres = {}, []
    for i in items:
        if c1[i]["class"] == c2[i]["class"]:
            out[i] = c1[i]["class"]
        elif i in adj:
            out[i] = adj[i]["class"]
        else:
            unres.append(i)
    return out, unres


def expand(labels, cell_of, pop):
    coded = collections.Counter(cell_of[i] for i in labels)
    N, Nt = collections.Counter(), collections.Counter()
    for i, cl in labels.items():
        w = pop[cell_of[i]] / coded[cell_of[i]]
        N[cl] += w
        if cell_of[i].endswith("-T"):
            Nt[cl] += w
    return N, Nt


def main():
    ap = argparse.ArgumentParser()
    for x in ("armA-map", "armA-c1", "armA-c2", "armA-adj", "armA-cells", "cells", "map", "c1", "c2"):
        ap.add_argument("--" + x, required=True)
    ap.add_argument("--adj"); ap.add_argument("--boot", type=int, default=10000); ap.add_argument("--seed", type=int, default=20261114)
    a = ap.parse_args()
    rng = random.Random(a.seed)

    # Arm A final labels (frozen)
    am, a1, a2, aj = read(a.armA_map), read(a.armA_c1), read(a.armA_c2), read(a.armA_adj)
    afin, aun = finals(a1, a2, aj, am)
    assert not aun, "Arm A has unresolved items"
    acell = {i: r["cell"] for i, r in read(a.armA_cells).items()}
    assert set(acell) == set(am)

    # A3 codes
    mp, c1, c2 = read(a.map), read(a.c1), read(a.c2)
    assert set(c1) == set(mp) == set(c2), "coders must cover every A3 item exactly"
    bad = [i for i in mp if c1[i]["class"] not in CLASSES or c2[i]["class"] not in CLASSES]
    assert not bad, "invalid classes: %s" % bad[:5]
    pairs = [(c1[i]["class"], c2[i]["class"]) for i in sorted(mp)]
    k, po = kappa(pairs)
    ks = sorted(kappa([pairs[rng.randrange(len(pairs))] for _ in pairs])[0] for _ in range(2000))
    print("AGREEMENT (A3 items, n %d)  raw %.3f  Cohen kappa %.3f  (95%% bootstrap %.3f to %.3f; usable >= 0.60)" % (len(pairs), po, k, ks[49], ks[1949]))
    for c in ("F-T", "R-T"):
        sp = [(c1[i]["class"], c2[i]["class"]) for i in mp if mp[i]["cell"] == c]
        if sp:
            print("  cell %s: n %d, kappa %.3f, raw %.3f" % ((c, len(sp)) + kappa(sp)))
    adj = read(a.adj) if a.adj else {}
    fin3, unres = finals(c1, c2, adj, mp)
    dis = sum(c1[i]["class"] != c2[i]["class"] for i in mp)
    print("DISAGREEMENTS %d, adjudicated %d, unresolved %d" % (dis, dis - len(unres), len(unres)))
    if unres:
        print("  unresolved (write them to --adj):", " ".join(unres[:50]), "..." if len(unres) > 50 else "")
        return 2

    labels = dict(afin); labels.update(fin3)
    cell_of = dict(acell); cell_of.update({i: mp[i]["cell"] for i in mp})
    doc_of = {i: am[i]["doc"] for i in am}; doc_of.update({i: mp[i]["doc"] for i in mp})
    pop = {c: int(r["population"]) for c, r in read(a.cells, "cell").items()}
    coded = collections.Counter(cell_of[i] for i in labels)

    print("CELL TABLE (population, coded, weight; final labels unweighted)")
    by = collections.Counter((cell_of[i], cl) for i, cl in labels.items())
    for c in CELLS:
        print("  %s pop %6d coded %5d weight %7.2f | %s" % (c, pop[c], coded[c], pop[c] / coded[c] if coded[c] else float("nan"),
              ", ".join("%s %d" % (cl, by[(c, cl)]) for cl in CLASSES)))
    N, Nt = expand(labels, cell_of, pop)
    print("EXPANSION (eligible pool; C whole): " + ", ".join("%s %.0f" % (cl, N[cl]) for cl in CLASSES))
    raw_dir = sum(1 for cl in labels.values() if cl in ("TP", "PT"))
    new_dir = sum(1 for cl in fin3.values() if cl in ("TP", "PT"))
    print("DIRECTIONAL coded: %d in all (A3 new %d: TP %d, PT %d)" % (raw_dir, new_dir,
          sum(v == "TP" for v in fin3.values()), sum(v == "PT" for v in fin3.values())))
    for d in ("TP", "PT"):
        for c in CELLS:
            if by[(c, d)] == 0 and coded[c]:
                print("  zero %s in %s: one-sided 95%% upper bound on its rate = 3/%d = %.4f" % (d, c, coded[c], 3 / coded[c]))

    # document bootstrap within cells
    docs = collections.defaultdict(lambda: collections.defaultdict(list))
    for i in labels:
        docs[cell_of[i]][doc_of[i]].append(i)
    shares, rTP, rPT = [], [], []
    for _ in range(a.boot):
        bl, bc = {}, {}
        for c, dd in docs.items():
            keys = list(dd)
            for j in range(len(keys)):
                for i in dd[keys[rng.randrange(len(keys))]]:
                    bl["%s#%d" % (i, j)] = labels[i]; bc["%s#%d" % (i, j)] = c
        n, nt = expand(bl, bc, pop)
        if n["TP"] + n["PT"] > 0:
            shares.append(n["TP"] / (n["TP"] + n["PT"]))
        if n["TP"] > 0:
            rTP.append(nt["TP"] / n["TP"])
        if n["PT"] > 0:
            rPT.append(nt["PT"] / n["PT"])
    q = lambda v: (sorted(v)[int(.025 * len(v))], sorted(v)[int(.975 * len(v)) - 1]) if v else (float("nan"),) * 2
    tot = N["TP"] + N["PT"]
    s = N["TP"] / tot if tot else float("nan")
    L, U = q(shares)
    print("DIRECTIONAL share s = %.3f, 95%% document bootstrap within cells %.3f to %.3f (width %.3f; %d resamples)" % (s, L, U, U - L, len(shares)))
    for d, v in (("TP", rTP), ("PT", rPT)):
        if N[d] > 0:
            lo, hi = q(v)
            print("T-SCREEN RECALL %s: %.3f (95%% %.3f to %.3f)" % (d, Nt[d] / N[d], lo, hi))
        else:
            print("T-SCREEN RECALL %s: UNKNOWN (no %s codes)" % (d, d))
    print("MINIMUM COUNT: %d coded sentences with a final TP or PT label (rule: >= 30)" % raw_dir)
    if raw_dir < 30:
        label = "INSUFFICIENT"
    elif L > 0.80:
        label = "SUPPORTS_STRONG"
    elif L > 0.50 and U > 0.80:
        label = "SUPPORTS_DIRECTION"
    elif L > 0.50 and U < 0.80:
        label = "AGAINST_STRONG_THRESHOLD"
    elif U < 0.50:
        label = "AGAINST_DIRECTION"
    else:
        label = "INCONCLUSIVE"
    print("DECISION (protocol v2 sec. 5): %s" % label)
    if k < 0.60:
        print("  kappa below 0.60: the directional result is EXPLORATORY")
    return 0


if __name__ == "__main__":
    sys.exit(main())
