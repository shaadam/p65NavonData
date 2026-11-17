#!/usr/bin/env python3
"""p65_navon_arm_a_sample.py -- Arm A (Navon 1978 criterion (c)) English sampling for the class coding session.

Reads UD English EWT + GUM r2.18 (train/dev/test CoNLL-U), applies the FROZEN v1 lexical screen
(ARM_A_FROZEN_CODEBOOK.json, W02 return) to build the CANDIDATE set, and builds a word-list-free RECALL
FRAME so the screen's misses can be counted. Then draws seeded samples, shuffles them blind, and writes
coding packets in which every sentence appears in exactly two packets (two independent student codes).

Strata (codebook v2 sec. 4):
  C  candidate: >=1 v1 temporal cue and >=1 v1 locative cue, each as an obl/advmod/advcl/nmod dependent
  F  frame: not C, and some predicate carries >=2 adjunct dependents (obl*, advmod, advcl, nmod*, obl:tmod ...)
  R  rest: neither C nor F (tests the assumption that R holds no time-place predications)

Control: --control re-counts the v1 screen on the two test splits and must reproduce W02's 9 (EWT) and 10 (GUM).
Usage: p65_navon_arm_a_sample.py --ud DIR --out DIR [--seed 20261113] [--nc 150 --nf 250 --nr 50 --packet 30]
"""
import argparse, collections, csv, glob, hashlib, os, random, re, sys

TEMPORAL = {"today", "yesterday", "tomorrow", "now", "noon", "midnight", "morning", "evening", "night",
            "day", "week", "month", "year", "hour"}
LOCATIVE = {"here", "there", "home", "house", "city", "street", "room", "school", "office", "park",
            "corner", "village", "square"}
SCREEN_REL = ("obl", "advmod", "advcl", "nmod")
ADJUNCT_REL = ("obl", "advmod", "advcl", "nmod")
# Classroom exclusion (codebook v2 sec. 4.4), applied to the pool BEFORE sampling and counted per stratum:
# profanity, slurs and sexual-violence content. News-register words (killed, suicide) stay in.
EXCLUDE = re.compile(r"\b(fuck\w*|shit\w*|bitch\w*|cunt\w*|nigg\w*|fag\w*|retard\w*|whore\w*|slut\w*|rap(e|ed|es|ing|ist)|porn\w*|pussy|cock\w*|asshole\w*)\b", re.I)

# Gold items: constructed sentences with a keyed class, three per packet (attention and training check).
GOLD = [
    ("G1", "The sun was directly overhead at noon.", "TP"),
    ("G2", "In Tokyo it was already midnight, while in London it was still afternoon.", "PT"),
    ("G3", "We met in the park yesterday.", "PAR"),
    ("G4", "She works from home.", "NA"),
    ("G5", "By evening the boat was back at the dock.", "TP"),
    ("G6", "Here it is summer now; down south it is winter.", "PT"),
]


def sentences(path):
    meta, toks = {}, []
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line:
            if toks:
                yield meta, toks
            meta, toks = {}, []
        elif line.startswith("#"):
            if "=" in line:
                k, v = line[1:].split("=", 1)
                meta[k.strip()] = v.strip()
        else:
            c = line.split("\t")
            if c[0].isdigit():
                toks.append(c)
    if toks:
        yield meta, toks


def rel_ok(rel, base):
    return rel.split(":")[0] in base


def classify(toks):
    t = l = False
    heads = collections.Counter()
    for c in toks:
        form, lemma, rel, head = c[1].lower(), c[2].lower(), c[7], c[6]
        if rel_ok(rel, SCREEN_REL):
            if lemma in TEMPORAL or form in TEMPORAL:
                t = True
            if lemma in LOCATIVE or form in LOCATIVE:
                l = True
        if rel_ok(rel, ADJUNCT_REL):
            heads[head] += 1
    if t and l:
        return "C"
    if heads and max(heads.values()) >= 2:
        return "F"
    return "R"


def load(ud, splits):
    rows = []
    for path in sorted(glob.glob(os.path.join(ud, "en_*-ud-*.conllu"))):
        tb, sp = os.path.basename(path).split("-ud-")
        sp = sp.split(".")[0]
        if sp not in splits:
            continue
        prev, doc = "", ""
        for meta, toks in sentences(path):
            sid = meta.get("sent_id", "")
            if "newdoc id" in meta:
                d = meta["newdoc id"]
            elif doc and sid.startswith(doc):
                d = doc
            else:
                d = sid.rsplit("-", 1)[0]
            if d != doc:
                doc, prev = d, ""                      # context never crosses a document boundary
            text = meta.get("text", " ".join(c[1] for c in toks))
            rows.append(dict(treebank=tb, split=sp, doc=doc, sent_id=sid, text=text, context=prev,
                             stratum=classify(toks), ntok=len(toks)))
            prev = text
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ud", required=True)
    ap.add_argument("--out")
    ap.add_argument("--seed", type=int, default=20261113)
    ap.add_argument("--nc", type=int, default=150)
    ap.add_argument("--nf", type=int, default=250)
    ap.add_argument("--nr", type=int, default=50)
    ap.add_argument("--packet", type=int, default=30)
    ap.add_argument("--maxtok", type=int, default=60, help="drop sentences longer than this (readability)")
    ap.add_argument("--control", action="store_true")
    a = ap.parse_args()

    if a.control:
        got = collections.Counter(r["treebank"] for r in load(a.ud, {"test"}) if r["stratum"] == "C")
        want = {"en_ewt": 9, "en_gum": 10}
        ok = dict(got) == want
        print("v1 screen on test splits:", dict(got), "W02 printed:", want, "->", "MATCH" if ok else "MISMATCH")
        return 0 if ok else 1

    rows = load(a.ud, {"train", "dev", "test"})
    os.makedirs(a.out, exist_ok=True)
    pop = collections.Counter((r["treebank"], r["stratum"]) for r in rows)
    elig = [r for r in rows if r["ntok"] <= a.maxtok and r["text"] and not EXCLUDE.search(r["text"] + " " + r["context"])]
    excl = collections.Counter(r["stratum"] for r in rows if EXCLUDE.search(r["text"] + " " + r["context"]))
    print("classroom exclusion (sentence or its context):", dict(excl))
    rng = random.Random(a.seed)
    draw = []
    for st, n in (("C", a.nc), ("F", a.nf), ("R", a.nr)):
        pool = [r for r in elig if r["stratum"] == st]
        k = min(n, len(pool))
        draw += rng.sample(pool, k)
        print("stratum %s: population %d (eligible <=%d tokens: %d), drawn %d" % (
            st, sum(v for (tb, s), v in pop.items() if s == st), a.maxtok, len(pool), k))
    rng.shuffle(draw)
    for i, r in enumerate(draw, 1):
        r["item"] = "S%03d" % i

    # Each sentence in two packets: the shuffled list splits into blocks of `packet`; block b goes to packets
    # "<b>A" and "<b>B", coded by two different students, so agreement is a per-pair kappa on identical items.
    blocks = [draw[i:i + a.packet] for i in range(0, len(draw), a.packet)]
    packets = collections.defaultdict(list)
    for b, blk in enumerate(blocks, 1):
        packets["%02dA" % b] += blk
        packets["%02dB" % b] += blk
    gold_rng = random.Random(a.seed + 1)

    key_path = os.path.join(a.out, "p65_arm-a_sample-key.tsv")
    with open(key_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["item", "stratum", "treebank", "split", "doc", "sent_id", "ntok", "text"])
        for r in draw:
            w.writerow([r["item"], r["stratum"], r["treebank"], r["split"], r["doc"], r["sent_id"], r["ntok"], r["text"]])
    with open(os.path.join(a.out, "p65_arm-a_population.tsv"), "w", encoding="utf-8") as f:
        f.write("treebank\tstratum\tsentences\n")
        for (tb, st), v in sorted(pop.items()):
            f.write("%s\t%s\t%d\n" % (tb, st, v))

    sheet = os.path.join(a.out, "p65_arm-a_coding-sheet_all-packets.csv")
    with open(sheet, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["packet", "row", "item", "previous_sentence", "sentence", "class (TP/PT/PAR/AMB/NA)",
                    "time phrase (copy words)", "place phrase (copy words)", "confidence (1-3)", "note"])
        for p in sorted(packets):
            items = [(r["item"], r["context"], r["text"]) for r in packets[p]]
            items += [(g[0], "", g[1]) for g in gold_rng.sample(GOLD, 3)]
            gold_rng.shuffle(items)
            for j, (it, ctx, tx) in enumerate(items, 1):
                w.writerow(["P" + p, j, it, ctx, tx, "", "", "", "", ""])
    copies = collections.Counter(r["item"] for p in packets.values() for r in p)
    assert set(copies.values()) == {2}, "every sentence must appear in exactly two packets"
    for p in packets:
        ids = [r["item"] for r in packets[p]]
        assert len(ids) == len(set(ids)), "a packet repeats a sentence"
    with open(os.path.join(a.out, "p65_arm-a_gold-key.tsv"), "w", encoding="utf-8") as f:
        f.write("item\tsentence\tkeyed_class\n")
        for g in GOLD:
            f.write("%s\t%s\t%s\n" % g)
    print("packets: %d of %d sentences + 3 gold each; every sentence in exactly 2 packets: OK" % (len(packets), a.packet))
    print("sha256 sample key:", hashlib.sha256(open(key_path, "rb").read()).hexdigest())
    return 0


if __name__ == "__main__":
    sys.exit(main())
