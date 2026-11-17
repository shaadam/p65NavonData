#!/usr/bin/env python3
"""p65_navon_arm_a_analyze.py -- Arm A analysis, protocol v2 sections 4.5 and 5, applied to model codes (v3).

Committed before any label existed. Inputs: the blind item map, two coders' code files, and (for disagreements)
an adjudication file `item<TAB>class<TAB>reason`. Prints agreement, the expansion counts, the directional share
with a document-cluster bootstrap interval, recall per direction, and the pre-registered decision label.

Weights: C is coded in full (weight 1). F and R were drawn uniformly from the eligible pools (<= 60 tokens, not
excluded for classroom content): F 11,748 -> 250, R 18,578 -> 50. Ineligible sentences (long or excluded) are
outside the estimate and are reported as such.
Usage: p65_navon_arm_a_analyze.py --map M --c1 A --c2 B [--adj J] [--boot 10000] [--seed 20261114]
"""
import argparse, collections, csv, random, sys

POOL = {"C": None, "F": 11748, "R": 18578}
CLASSES = ("TP", "PT", "PAR", "AMB", "NA")


def read(path, key="item"):
    return {r[key]: r for r in csv.DictReader(open(path, encoding="utf-8"), delimiter="\t")}


def kappa(pairs):
    n = len(pairs)
    po = sum(a == b for a, b in pairs) / n
    ca, cb = collections.Counter(a for a, _ in pairs), collections.Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb[k] for k in CLASSES) / n / n
    return (po - pe) / (1 - pe) if pe < 1 else float("nan"), po


def expand(final, mp, drawn):
    N = collections.Counter()
    by = collections.Counter()
    for it, cl in final.items():
        st = mp[it]["stratum"]
        w = 1.0 if st == "C" else POOL[st] / drawn[st]
        N[cl] += w
        by[(st, cl)] += 1
    return N, by


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--map", required=True); ap.add_argument("--c1", required=True); ap.add_argument("--c2", required=True)
    ap.add_argument("--adj"); ap.add_argument("--boot", type=int, default=10000); ap.add_argument("--seed", type=int, default=20261114)
    a = ap.parse_args()
    mp, c1, c2 = read(a.map), read(a.c1), read(a.c2)
    assert set(c1) == set(mp) == set(c2), "coders must cover every item exactly"
    bad = [i for i in mp if c1[i]["class"] not in CLASSES or c2[i]["class"] not in CLASSES]
    assert not bad, "invalid classes: %s" % bad[:5]
    pairs = [(c1[i]["class"], c2[i]["class"]) for i in sorted(mp)]
    k, po = kappa(pairs)
    rng = random.Random(a.seed)
    ks = sorted(kappa([pairs[rng.randrange(len(pairs))] for _ in pairs])[0] for _ in range(2000))
    print("AGREEMENT  raw %.3f  Cohen kappa %.3f  (95%% bootstrap %.3f to %.3f; usable >= 0.60)" % (po, k, ks[49], ks[1949]))
    for st in "CFR":
        sp = [(c1[i]["class"], c2[i]["class"]) for i in mp if mp[i]["stratum"] == st]
        print("  stratum %s: n %d, kappa %.3f, raw %.3f" % ((st, len(sp)) + kappa(sp)))
    dis = [i for i in sorted(mp) if c1[i]["class"] != c2[i]["class"]]
    adj = read(a.adj) if a.adj else {}
    unres = [i for i in dis if i not in adj]
    print("DISAGREEMENTS %d, adjudicated %d, unresolved %d" % (len(dis), len(dis) - len(unres), len(unres)))
    if unres:
        print("  unresolved (write them to --adj):", " ".join(unres))
        return 2
    final = {i: (c1[i]["class"] if i not in dis else adj[i]["class"]) for i in mp}
    drawn = collections.Counter(mp[i]["stratum"] for i in mp)
    N, by = expand(final, mp, drawn)
    print("FINAL LABELS by stratum (unweighted):")
    for st in "CFR":
        print("  %s: %s" % (st, ", ".join("%s %d" % (c, by[(st, c)]) for c in CLASSES)))
    raw_dir = sum(by[(st, c)] for st in "CFR" for c in ("TP", "PT"))
    print("EXPANSION (estimated sentences in the eligible EWT+GUM pool): " + ", ".join("%s %.0f" % (c, N[c]) for c in CLASSES))

    # zero-count rule
    for d in ("TP", "PT"):
        for st in "CFR":
            if by[(st, d)] == 0:
                print("  zero %s in %s: one-sided 95%% upper bound on its rate there = 3/%d = %.3f" % (d, st, drawn[st], 3 / drawn[st]))

    # document-cluster bootstrap within strata
    docs = collections.defaultdict(lambda: collections.defaultdict(list))
    for i in mp:
        docs[mp[i]["stratum"]][mp[i]["doc"]].append(i)
    shares, rTP, rPT, ratio = [], [], [], []
    for _ in range(a.boot):
        samp = {}
        for st, dd in docs.items():
            keys = list(dd)
            for j in range(len(keys)):
                for i in dd[keys[rng.randrange(len(keys))]]:
                    samp["%s#%d" % (i, j)] = final[i]
        dr = collections.Counter(mp[s.split("#")[0]]["stratum"] for s in samp)
        n = collections.Counter(); nc = collections.Counter()
        for s, cl in samp.items():
            st = mp[s.split("#")[0]]["stratum"]
            w = (drawn["C"] / dr["C"]) if st == "C" else POOL[st] / dr[st]
            n[cl] += w
            if st == "C":
                nc[cl] += w
        if n["TP"] + n["PT"] > 0:
            shares.append(n["TP"] / (n["TP"] + n["PT"]))
        if n["TP"] > 0 and n["PT"] > 0:
            a1, a2 = nc["TP"] / n["TP"], nc["PT"] / n["PT"]
            rTP.append(a1); rPT.append(a2)
            if a2 > 0:
                ratio.append(a1 / a2)
    q = lambda v: (sorted(v)[int(.025 * len(v))], sorted(v)[int(.975 * len(v)) - 1]) if v else (float("nan"),) * 2
    tot = N["TP"] + N["PT"]
    s = N["TP"] / tot if tot else float("nan")
    L, U = q(shares)
    Nc = collections.Counter({c: by[("C", c)] for c in CLASSES})
    print("DIRECTIONAL share s = N_TP/(N_TP+N_PT) = %.3f, 95%% document-cluster interval %.3f to %.3f (%d resamples)" % (s, L, U, len(shares)))
    if Nc["TP"] + Nc["PT"]:
        print("  candidate-only share (not an estimate unless equal-recall): %.3f (%d TP, %d PT)" % (Nc["TP"] / (Nc["TP"] + Nc["PT"]), Nc["TP"], Nc["PT"]))
    fr = by[("F", "TP")] + by[("R", "TP")], by[("F", "PT")] + by[("R", "PT")]
    if 0 in fr:
        print("RECALL: UNKNOWN for %s (zero final codes outside the candidates)" % " and ".join(d for d, z in zip(("TP", "PT"), fr) if z == 0))
        equal = None
    else:
        rl, ru = q(ratio)
        print("RECALL of the word-list screen: TP %.2f, PT %.2f; ratio TP/PT 95%% %.2f to %.2f -> %s" % (
            Nc["TP"] / N["TP"], Nc["PT"] / N["PT"], rl, ru, "equal-recall" if rl <= 1 <= ru else "DIFFERENTIAL"))
    print("MINIMUM COUNT: %d sentences with a final TP or PT label (rule: >= 30)" % raw_dir)
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
        print("  kappa below 0.60: the directional result is EXPLORATORY (protocol v2 sec. 5)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
