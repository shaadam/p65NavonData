#!/usr/bin/env python3
"""p65_navon_arm_a3b_sample.py -- Arm A3b draw (registration: p65_arm-a3b_registration_2026-11-13.md).

Draws 1,000 NEW items from each of F-N and R-N (uniform without replacement, seed 20261115) from eligible sentences
not coded in Arm A or A3. Shuffles the 2,000 together, IDs Z0001.., 4 blind batches of 500, key map.
Usage: python3 -I p65_navon_arm_a3b_sample.py --ud DIR --ents CACHE.json --armA-map M --a3-map M3 --out DIR
"""
import argparse, collections, csv, hashlib, importlib.util, json, os, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("samp", os.path.join(HERE, "..", "scripts", "p65_navon_arm_a_sample.py"))
samp = importlib.util.module_from_spec(spec); spec.loader.exec_module(samp)
DRAW = (("F-N", 1000), ("R-N", 1000))


def main():
    ap = argparse.ArgumentParser()
    for x in ("ud", "ents", "armA-map", "a3-map", "out"):
        ap.add_argument("--" + x, required=True)
    ap.add_argument("--seed", type=int, default=20261115); ap.add_argument("--batch", type=int, default=500)
    a = ap.parse_args()
    rows = samp.load(a.ud, {"train", "dev", "test"})
    ents = json.load(open(a.ents))
    assert len(rows) == 30975 and len(ents) == 30975
    coded = set()
    for p in (a.armA_map, a.a3_map):
        coded |= {m["treebank"] + "|" + m["sent_id"] for m in csv.DictReader(open(p, encoding="utf-8"), delimiter="\t")}
    assert len(coded) == 2000, len(coded)
    for r in rows:
        r["key"] = r["treebank"] + "|" + r["sent_id"]
        r["cell"] = r["stratum"] + "-" + ("T" if set(ents[r["key"]]) & {"DATE", "TIME"} else "N")
        r["elig"] = bool(r["ntok"] <= 60 and r["text"] and not samp.EXCLUDE.search(r["text"] + " " + r["context"]))
    rng = random.Random(a.seed)
    draw = []
    for c, n in DRAW:
        pool = [r for r in rows if r["cell"] == c and r["elig"] and r["key"] not in coded]
        print("%s eligible uncoded pool %d, draw %d" % (c, len(pool), n))
        draw += rng.sample(pool, n)
    rng.shuffle(draw)
    for i, r in enumerate(draw, 1):
        r["item"] = "Z%04d" % i
    assert len({r["key"] for r in draw}) == 2000 and not any(r["key"] in coded for r in draw)
    os.makedirs(a.out, exist_ok=True)
    P = lambda f: os.path.join(a.out, f)
    with open(P("p65_a3b-items_map.tsv"), "w", encoding="utf-8") as f:
        f.write("item\tcell\tstratum\tT\ttreebank\tdoc\tsent_id\n")
        for r in draw:
            f.write("\t".join([r["item"], r["cell"], r["stratum"], "N", r["treebank"], r["doc"], r["sent_id"]]) + "\n")

    def blind(path, items):
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, delimiter="\t", lineterminator="\n")
            w.writerow(["item", "previous_sentence", "sentence"])
            for r in items:
                w.writerow([r["item"], r["context"], r["text"]])
    blind(P("p65_a3b-items_blind.tsv"), draw)
    for b in range(0, len(draw), a.batch):
        blind(P("p65_a3b-items_blind_b%d.tsv" % (b // a.batch + 1)), draw[b:b + a.batch])
    print("drawn %d, all new, all eligible: OK; by cell %s" % (len(draw), dict(collections.Counter(r["cell"] for r in draw))))
    for f in ("p65_a3b-items_blind.tsv", "p65_a3b-items_map.tsv"):
        print("sha256 %s %s" % (f, hashlib.sha256(open(P(f), "rb").read()).hexdigest()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
