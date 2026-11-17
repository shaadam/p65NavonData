#!/usr/bin/env python3
"""p65_navon_arm_a3_sample.py -- Arm A3 draw (registration: p65_arm-a3_registration_2026-11-13.md).

Cells = Arm A groups (C, F, R) x T (spaCy en_core_web_sm finds a DATE or TIME entity in the sentence text).
Draws 1,500 NEW items uniformly without replacement from the uncoded, eligible (<= 60 tokens, protocol v2 sec 4.4
content list) sentences of F-T and R-T, allocated in proportion to those uncoded eligible sizes (largest remainder).
Writes: blind item file (item, previous_sentence, sentence; shuffled), 3 batch files of 500, the key map, the cell
table (population = eligible; C taken whole) and the Arm A items' cell assignments.

T flags come from the spaCy entity cache written by scripts/p65_navon_arm_a2_entity_screen.py (--cache).
Usage: python3 -I p65_navon_arm_a3_sample.py --ud DIR --ents CACHE.json --armA-map arm-a-model/p65_model-items_map.tsv
       --out arm-a3-model [--n 1500 --seed 20261114 --batch 500]
"""
import argparse, collections, csv, hashlib, importlib.util, json, os, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("samp", os.path.join(HERE, "p65_navon_arm_a_sample.py"))
samp = importlib.util.module_from_spec(spec); spec.loader.exec_module(samp)
CELLS = ("C-T", "C-N", "F-T", "F-N", "R-T", "R-N")
DRAW_CELLS = ("F-T", "R-T")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ud", required=True); ap.add_argument("--ents", required=True)
    ap.add_argument("--armA-map", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=1500); ap.add_argument("--seed", type=int, default=20261114)
    ap.add_argument("--batch", type=int, default=500); ap.add_argument("--maxtok", type=int, default=60)
    a = ap.parse_args()

    rows = samp.load(a.ud, {"train", "dev", "test"})
    ents = json.load(open(a.ents))
    assert len(rows) == 30975 and len(ents) == 30975, (len(rows), len(ents))
    amap = list(csv.DictReader(open(a.armA_map, encoding="utf-8"), delimiter="\t"))
    coded = {m["treebank"] + "|" + m["sent_id"]: m["item"] for m in amap}
    for r in rows:
        r["key"] = r["treebank"] + "|" + r["sent_id"]
        r["T"] = "T" if set(ents[r["key"]]) & {"DATE", "TIME"} else "N"
        r["cell"] = r["stratum"] + "-" + r["T"]
        r["elig"] = bool(r["ntok"] <= a.maxtok and r["text"] and not samp.EXCLUDE.search(r["text"] + " " + r["context"]))
    allc = collections.Counter(r["cell"] for r in rows)
    pop = collections.Counter(r["cell"] for r in rows if r["elig"] or r["stratum"] == "C")  # C taken whole, as in Arm A
    armA = collections.Counter(r["cell"] for r in rows if r["key"] in coded)
    pools = {c: [r for r in rows if r["cell"] == c and r["elig"] and r["key"] not in coded] for c in DRAW_CELLS}
    tot = sum(len(p) for p in pools.values())
    raw = {c: a.n * len(pools[c]) / tot for c in DRAW_CELLS}
    alloc = {c: int(raw[c]) for c in DRAW_CELLS}
    for c in sorted(DRAW_CELLS, key=lambda c: raw[c] - alloc[c], reverse=True)[: a.n - sum(alloc.values())]:
        alloc[c] += 1
    rng = random.Random(a.seed)
    draw = []
    for c in DRAW_CELLS:
        draw += rng.sample(pools[c], alloc[c])
    rng.shuffle(draw)
    for i, r in enumerate(draw, 1):
        r["item"] = "N%04d" % i

    os.makedirs(a.out, exist_ok=True)
    P = lambda f: os.path.join(a.out, f)
    with open(P("p65_a3-cells.tsv"), "w", encoding="utf-8") as f:
        f.write("cell\tall_sentences\tpopulation\tarmA_coded\tuncoded_eligible\tnew_draw\tcoded_after\n")
        for c in CELLS:
            ue = len(pools[c]) if c in pools else 0
            nd = alloc.get(c, 0)
            f.write("%s\t%d\t%d\t%d\t%d\t%d\t%d\n" % (c, allc[c], pop[c], armA[c], ue, nd, armA[c] + nd))
    with open(P("p65_a3-armA-cells.tsv"), "w", encoding="utf-8") as f:
        f.write("item\tcell\n")
        for r in rows:
            if r["key"] in coded:
                f.write("%s\t%s\n" % (coded[r["key"]], r["cell"]))
    with open(P("p65_a3-items_map.tsv"), "w", encoding="utf-8") as f:
        f.write("item\tcell\tstratum\tT\ttreebank\tdoc\tsent_id\n")
        for r in draw:
            f.write("\t".join([r["item"], r["cell"], r["stratum"], r["T"], r["treebank"], r["doc"], r["sent_id"]]) + "\n")

    def blind(path, items):
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, delimiter="\t", lineterminator="\n")
            w.writerow(["item", "previous_sentence", "sentence"])
            for r in items:
                w.writerow([r["item"], r["context"], r["text"]])
    blind(P("p65_a3-items_blind.tsv"), draw)
    for b in range(0, len(draw), a.batch):
        blind(P("p65_a3-items_blind_b%d.tsv" % (b // a.batch + 1)), draw[b:b + a.batch])

    print("cells (all / population / Arm A coded / uncoded eligible / new / coded after):")
    for c in CELLS:
        print("  %s %d / %d / %d / %d / %d / %d" % (c, allc[c], pop[c], armA[c], len(pools.get(c, [])), alloc.get(c, 0), armA[c] + alloc.get(c, 0)))
    assert len({r["key"] for r in draw}) == len(draw) == a.n and not any(r["key"] in coded for r in draw)
    print("drawn %d, all new, all eligible: OK" % len(draw))
    print("sha256 blind:", hashlib.sha256(open(P("p65_a3-items_blind.tsv"), "rb").read()).hexdigest())
    print("sha256 map:  ", hashlib.sha256(open(P("p65_a3-items_map.tsv"), "rb").read()).hexdigest())
    return 0


if __name__ == "__main__":
    sys.exit(main())
