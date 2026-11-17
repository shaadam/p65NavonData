#!/usr/bin/env python3
"""p65_navon_arm_a3b_analyze.py -- Arm A3b analysis (registration: p65_arm-a3b_registration_2026-11-13.md).

Reuses scripts/p65_navon_arm_a3_analyze.py (kappa, finals, expand) and its estimator. Combines frozen Arm A and A3
final labels with A3b's (two coders + adjudication) over the six cells, coded counts updated for F-N and R-N.
Adds per-stratum Clopper-Pearson bounds for F-N and R-N and the s_low / s_high bracket.
"""
import argparse, collections, csv, importlib.util, math, os, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("a3", os.path.join(HERE, "..", "scripts", "p65_navon_arm_a3_analyze.py"))
a3 = importlib.util.module_from_spec(spec); spec.loader.exec_module(a3)
read, kappa, finals, expand, CLASSES, CELLS = a3.read, a3.kappa, a3.finals, a3.expand, a3.CLASSES, a3.CELLS


def ibeta(x, a, b):
    """regularized incomplete beta I_x(a, b) (Numerical Recipes betai)."""
    if x <= 0: return 0.0
    if x >= 1: return 1.0
    lb = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1 - x)
    if x < (a + 1) / (a + b + 2):
        return math.exp(lb) * _cf(x, a, b) / a
    return 1 - math.exp(lb) * _cf(1 - x, b, a) / b


def betainc_inv(p, a, b):
    """quantile of Beta(a, b) by bisection."""
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if ibeta(mid, a, b) < p: lo = mid
        else: hi = mid
    return (lo + hi) / 2


def _cf(x, a, b):
    qab, qap, qam = a + b, a + 1, a - 1
    c, d = 1.0, 1 - qab * x / qap
    d = 1 / (d if abs(d) > 1e-300 else 1e-300); h = d
    for m in range(1, 300):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1 + aa * d; d = 1 / (d if abs(d) > 1e-300 else 1e-300)
        c = 1 + aa / c if abs(c) > 1e-300 else 1e300
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1 + aa * d; d = 1 / (d if abs(d) > 1e-300 else 1e-300)
        c = 1 + aa / c if abs(c) > 1e-300 else 1e300
        de = d * c; h *= de
        if abs(de - 1) < 1e-12:
            break
    return h


def cp(k, n, alpha=0.05):
    lo = 0.0 if k == 0 else betainc_inv(alpha / 2, k, n - k + 1)
    hi = 1.0 if k == n else betainc_inv(1 - alpha / 2, k + 1, n - k)
    return lo, hi


def main():
    ap = argparse.ArgumentParser()
    for x in ("armA-map", "armA-c1", "armA-c2", "armA-adj", "armA-cells", "a3-cells", "a3-map", "a3-c1", "a3-c2",
              "a3-adj", "map", "c1", "c2"):
        ap.add_argument("--" + x, required=True)
    ap.add_argument("--adj"); ap.add_argument("--boot", type=int, default=10000); ap.add_argument("--seed", type=int, default=20261114)
    a = ap.parse_args()
    rng = random.Random(a.seed)

    am = read(a.armA_map)
    afin, u = finals(read(a.armA_c1), read(a.armA_c2), read(a.armA_adj), am); assert not u
    acell = {i: r["cell"] for i, r in read(a.armA_cells).items()}
    m3 = read(a.a3_map)
    f3, u = finals(read(a.a3_c1), read(a.a3_c2), read(a.a3_adj), m3); assert not u
    mp, c1, c2 = read(a.map), read(a.c1), read(a.c2)
    assert set(c1) == set(mp) == set(c2), "coders must cover every A3b item exactly"
    assert not [i for i in mp if c1[i]["class"] not in CLASSES or c2[i]["class"] not in CLASSES], "invalid classes"
    assert all(mp[i]["cell"] in ("F-N", "R-N") for i in mp)

    pairs = [(c1[i]["class"], c2[i]["class"]) for i in sorted(mp)]
    k, po = kappa(pairs)
    ks = sorted(kappa([pairs[rng.randrange(len(pairs))] for _ in pairs])[0] for _ in range(2000))
    print("AGREEMENT (A3b items, n %d)  raw %.3f  Cohen kappa %.3f  (95%% bootstrap %.3f to %.3f; usable >= 0.60)" % (len(pairs), po, k, ks[49], ks[1949]))
    for c in ("F-N", "R-N"):
        sp = [(c1[i]["class"], c2[i]["class"]) for i in mp if mp[i]["cell"] == c]
        kc, pc = kappa(sp)
        print("  cell %s: n %d, kappa %.3f, raw %.3f" % (c, len(sp), kc, pc))
    conf = collections.Counter(pairs)
    print("  confusion (coder1, coder2): " + ", ".join("%s/%s %d" % (x, y, n) for (x, y), n in sorted(conf.items(), key=lambda t: -t[1])))
    adj = read(a.adj) if a.adj else {}
    fin, unres = finals(c1, c2, adj, mp)
    dis = sum(c1[i]["class"] != c2[i]["class"] for i in mp)
    print("DISAGREEMENTS %d, adjudicated %d, unresolved %d" % (dis, dis - len(unres), len(unres)))
    if unres:
        print("  unresolved:", " ".join(unres))
        return 2

    labels = dict(afin); labels.update(f3); labels.update(fin)
    cell_of = dict(acell); cell_of.update({i: m3[i]["cell"] for i in m3}); cell_of.update({i: mp[i]["cell"] for i in mp})
    doc_of = {i: am[i]["doc"] for i in am}; doc_of.update({i: m3[i]["doc"] for i in m3}); doc_of.update({i: mp[i]["doc"] for i in mp})
    pop = {c: int(r["population"]) for c, r in read(a.a3_cells, "cell").items()}
    coded = collections.Counter(cell_of[i] for i in labels)
    by = collections.Counter((cell_of[i], cl) for i, cl in labels.items())
    print("CELL TABLE (population, coded, weight; final labels unweighted)")
    for c in CELLS:
        print("  %s pop %6d coded %5d weight %7.2f | %s" % (c, pop[c], coded[c], pop[c] / coded[c],
              ", ".join("%s %d" % (cl, by[(c, cl)]) for cl in CLASSES)))
    newby = collections.Counter((mp[i]["cell"], cl) for i, cl in fin.items())
    print("A3b NEW ITEMS ONLY: " + "; ".join("%s: %s" % (c, ", ".join("%s %d" % (cl, newby[(c, cl)]) for cl in CLASSES)) for c in ("F-N", "R-N")))
    N, Nt = expand(labels, cell_of, pop)
    print("EXPANSION: " + ", ".join("%s %.0f" % (cl, N[cl]) for cl in CLASSES))
    raw_dir = sum(1 for cl in labels.values() if cl in ("TP", "PT"))

    print("PER-STRATUM BOUNDS (rate k/n; Clopper-Pearson 95%; x population = sentences)")
    lohi = {}
    for c in ("F-N", "R-N"):
        for d in ("TP", "PT"):
            kk, n = by[(c, d)], coded[c]
            lo, hi = cp(kk, n)
            lohi[(c, d)] = (lo, hi)
            extra = ""
            if kk == 0:
                extra = "; one-sided 95%% upper: rule of three %.4f (%.0f), exact %.4f (%.0f)" % (3 / n, 3 / n * pop[c], 1 - 0.05 ** (1 / n), (1 - 0.05 ** (1 / n)) * pop[c])
            print("  %s %s: %d/%d = %.4f, CP %.4f to %.4f -> %.0f to %.0f sentences (point %.0f)%s" % (
                c, d, kk, n, kk / n, lo, hi, lo * pop[c], hi * pop[c], kk / n * pop[c], extra))
    # bracket for s from these two cells
    base = {d: sum(pop[c] / coded[c] * by[(c, d)] for c in CELLS if c not in ("F-N", "R-N")) for d in ("TP", "PT")}
    tlo = base["TP"] + sum(lohi[(c, "TP")][0] * pop[c] for c in ("F-N", "R-N"))
    thi = base["TP"] + sum(lohi[(c, "TP")][1] * pop[c] for c in ("F-N", "R-N"))
    plo = base["PT"] + sum(lohi[(c, "PT")][0] * pop[c] for c in ("F-N", "R-N"))
    phi = base["PT"] + sum(lohi[(c, "PT")][1] * pop[c] for c in ("F-N", "R-N"))
    print("BRACKET from F-N/R-N bounds (other cells at estimate): s_low %.3f, s_high %.3f" % (tlo / (tlo + phi), thi / (thi + plo)))

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
        if n["TP"] + n["PT"] > 0: shares.append(n["TP"] / (n["TP"] + n["PT"]))
        if n["TP"] > 0: rTP.append(nt["TP"] / n["TP"])
        if n["PT"] > 0: rPT.append(nt["PT"] / n["PT"])
    q = lambda v: (sorted(v)[int(.025 * len(v))], sorted(v)[int(.975 * len(v)) - 1])
    s = N["TP"] / (N["TP"] + N["PT"])
    L, U = q(shares)
    print("DIRECTIONAL share s = %.3f, 95%% document bootstrap within cells %.3f to %.3f (width %.3f; %d resamples)" % (s, L, U, U - L, len(shares)))
    for d, v in (("TP", rTP), ("PT", rPT)):
        lo, hi = q(v)
        print("T-SCREEN RECALL %s: %.3f (95%% %.3f to %.3f)" % (d, Nt[d] / N[d], lo, hi))
    print("MINIMUM COUNT: %d coded sentences with a final TP or PT label (rule: >= 30)" % raw_dir)
    if raw_dir < 30: label = "INSUFFICIENT"
    elif L > 0.80: label = "SUPPORTS_STRONG"
    elif L > 0.50 and U > 0.80: label = "SUPPORTS_DIRECTION"
    elif L > 0.50 and U < 0.80: label = "AGAINST_STRONG_THRESHOLD"
    elif U < 0.50: label = "AGAINST_DIRECTION"
    else: label = "INCONCLUSIVE"
    print("DECISION (protocol v2 sec. 5): %s" % label)
    if k < 0.60:
        print("  kappa below 0.60: the directional result is EXPLORATORY")
    return 0


if __name__ == "__main__":
    sys.exit(main())
