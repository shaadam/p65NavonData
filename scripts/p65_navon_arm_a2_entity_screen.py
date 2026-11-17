#!/usr/bin/env python3
"""p65_navon_arm_a2_entity_screen.py -- Arm A2 step 1: recall of entity-based screens on the 50 directional
sentences of the Arm A model-coded run (registration: p65_arm-a2_entity-screen-registration_2026-11-13.md).

Screens:
  S1  spaCy en_core_web_sm on the sentence text: a DATE or TIME entity AND a GPE, LOC or FAC entity (EWT + GUM)
  S2  GUM gold entities (MISC Entity=): a 'time' mention AND a 'place' mention in the sentence (GUM only)
  S3  S1 OR S2 (GUM only)
Controls: DATE/TIME alone (S1 without the place half); random screens with the same flag count (10,000 draws).
Decision (registered): S1 recall on all 50 >= 0.60 and Wilson 95% lower bound >= 0.45 -> PROCEED, else STOP.

Must run in a Python with spaCy (venv). Reads UD via scripts/p65_navon_arm_a_sample.py's loader.
Usage: python -I p65_navon_arm_a2_entity_screen.py --ud DIR --model-dir arm-a-model --cache FILE.json [--seed 20261114]
"""
import argparse, collections, csv, importlib.util, json, math, os, random, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("samp", os.path.join(HERE, "p65_navon_arm_a_sample.py"))
samp = importlib.util.module_from_spec(spec); spec.loader.exec_module(samp)

ENT_OPEN = re.compile(r"\((\d+)-([a-z]+)")
POOL_F, DRAWN_F = 11748, 250


def gum_types(path):
    """sent_id -> set of GUM entity types opened in that sentence."""
    out = {}
    for meta, toks in samp.sentences(path):
        ty = set()
        for c in toks:
            for f in c[9].split("|"):
                if f.startswith("Entity="):
                    ty.update(m.group(2) for m in ENT_OPEN.finditer(f))
        out[meta["sent_id"]] = ty
    return out


def wilson(k, n, z=1.959964):
    if n == 0:
        return float("nan"), float("nan"), float("nan")
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, max(0.0, c - h), min(1.0, c + h)


def final_labels(md):
    r = lambda p: {x["item"]: x for x in csv.DictReader(open(os.path.join(md, p), encoding="utf-8"), delimiter="\t")}
    mp, c1, c2, adj = (r("p65_model-items_map.tsv"), r("p65_model-codes_coder1.tsv"),
                       r("p65_model-codes_coder2.tsv"), r("p65_model-adjudication.tsv"))
    fin = {i: (c1[i]["class"] if c1[i]["class"] == c2[i]["class"] else adj[i]["class"]) for i in mp}
    return mp, fin


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ud", required=True); ap.add_argument("--model-dir", required=True)
    ap.add_argument("--cache", required=True); ap.add_argument("--seed", type=int, default=20261114)
    ap.add_argument("--draws", type=int, default=10000); ap.add_argument("--flags-out")
    a = ap.parse_args()

    rows = samp.load(a.ud, {"train", "dev", "test"})
    print("SENTENCES: %d (EWT %d, GUM %d)" % (len(rows), sum(r["treebank"] == "en_ewt" for r in rows),
                                              sum(r["treebank"] == "en_gum" for r in rows)))
    print("v1 strata:", dict(collections.Counter(r["stratum"] for r in rows)))
    gum = {}
    for sp in ("train", "dev", "test"):
        gum.update(gum_types(os.path.join(a.ud, "en_gum-ud-%s.conllu" % sp)))
    for r in rows:
        r["key"] = r["treebank"] + "|" + r["sent_id"]
        t = gum.get(r["sent_id"], set()) if r["treebank"] == "en_gum" else None
        r["S2"] = (t is not None) and ("time" in t) and ("place" in t)

    # spaCy NER (cached: the run is deterministic, the cache only saves time)
    if os.path.exists(a.cache):
        ents = json.load(open(a.cache))
    else:
        import spacy
        nlp = spacy.load("en_core_web_sm", disable=["parser", "lemmatizer"])
        print("spaCy", spacy.__version__, "model", nlp.meta["name"], nlp.meta["version"])
        ents = {}
        for r, doc in zip(rows, nlp.pipe((r["text"] for r in rows), batch_size=256)):
            ents[r["key"]] = sorted({e.label_ for e in doc.ents})
        json.dump(ents, open(a.cache, "w"))
    for r in rows:
        lab = set(ents[r["key"]])
        r["DT"] = bool(lab & {"DATE", "TIME"})
        r["S1"] = r["DT"] and bool(lab & {"GPE", "LOC", "FAC"})
        r["S3"] = r["S1"] or r["S2"]

    mp, fin = final_labels(a.model_dir)
    byk = {r["key"]: r for r in rows}
    dirs = []
    for it in sorted(mp):
        if fin[it] in ("TP", "PT"):
            k = mp[it]["treebank"] + "|" + mp[it]["sent_id"]
            assert k in byk, k
            dirs.append(dict(item=it, cls=fin[it], st=mp[it]["stratum"], tb=mp[it]["treebank"], r=byk[k]))
    print("DIRECTIONAL: %d (TP %d, PT %d; GUM %d)" % (len(dirs), sum(d["cls"] == "TP" for d in dirs),
          sum(d["cls"] == "PT" for d in dirs), sum(d["tb"] == "en_gum" for d in dirs)))

    N, Ngum = len(rows), sum(r["treebank"] == "en_gum" for r in rows)
    rng = random.Random(a.seed)
    print("\nRECALL (Wilson 95%) and FLAGGED SHARE")
    for scr, scope in (("S1", "all"), ("S1", "gum"), ("S2", "gum"), ("S3", "gum"), ("DT", "all"), ("DT", "gum")):
        pop = rows if scope == "all" else [r for r in rows if r["treebank"] == "en_gum"]
        dd = dirs if scope == "all" else [d for d in dirs if d["tb"] == "en_gum"]
        nflag = sum(r[scr] for r in pop)
        line = "%s on %s: flagged %d / %d = %.4f (of all %d EWT+GUM: %.4f)" % (scr, scope, nflag, len(pop), nflag / len(pop), N, nflag / N)
        print(line)
        for lab, sub in (("all", dd), ("TP", [d for d in dd if d["cls"] == "TP"]), ("PT", [d for d in dd if d["cls"] == "PT"])):
            k = sum(d["r"][scr] for d in sub)
            p, lo, hi = wilson(k, len(sub))
            print("   recall %-3s %2d/%2d = %.3f  (%.3f to %.3f)" % (lab, k, len(sub), p, lo, hi))
        w = [1.0 if d["st"] == "C" else POOL_F / DRAWN_F for d in dd]
        wr = sum(wi for wi, d in zip(w, dd) if d["r"][scr]) / sum(w)
        print("   weighted recall (C 1, F %.1f): %.3f; frame directional flagged %d/%d" % (
            POOL_F / DRAWN_F, wr, sum(d["r"][scr] for d in dd if d["st"] == "F"), sum(d["st"] == "F" for d in dd)))
        # random screen with the same flag count over the same population
        idx = {d["r"]["key"] for d in dd}
        keys = [r["key"] for r in pop]
        sims = sorted(sum(k in idx for k in rng.sample(keys, nflag)) / len(dd) for _ in range(a.draws))
        print("   random screen, same flag count (%d draws): mean recall %.3f, 95%% range %.3f to %.3f, 97.5th pct %.3f" % (
            a.draws, sum(sims) / len(sims), sims[int(0.025 * a.draws)], sims[int(0.975 * a.draws) - 1], sims[int(0.975 * a.draws) - 1]))

    print("\nPER DIRECTIONAL SENTENCE (item class stratum treebank S1 DT S2 spaCy-labels | text)")
    for d in dirs:
        r = d["r"]
        print("%s %s %s %s S1=%d DT=%d S2=%s %s | %s" % (d["item"], d["cls"], d["st"], d["tb"], r["S1"], r["DT"],
              ("%d" % r["S2"]) if d["tb"] == "en_gum" else "-", ",".join(ents[r["key"]]), r["text"]))

    k = sum(d["r"]["S1"] for d in dirs); p, lo, hi = wilson(k, len(dirs))
    dec = "PROCEED (entity screen adequate)" if (p >= 0.60 and lo >= 0.45) else "STOP (report and stop)"
    print("\nDECISION (S1, all %d): recall %.3f, Wilson lower %.3f -> %s" % (len(dirs), p, lo, dec))
    if a.flags_out:
        with open(a.flags_out, "w", encoding="utf-8") as f:
            f.write("treebank\tsent_id\tv1_stratum\tntok\tS1\tDT\tS2\tS3\n")
            for r in rows:
                f.write("%s\t%s\t%s\t%d\t%d\t%d\t%s\t%s\n" % (r["treebank"], r["sent_id"], r["stratum"], r["ntok"], r["S1"], r["DT"],
                        int(r["S2"]) if r["treebank"] == "en_gum" else "", int(r["S3"]) if r["treebank"] == "en_gum" else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
