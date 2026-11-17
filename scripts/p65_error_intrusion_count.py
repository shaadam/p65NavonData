#!/usr/bin/env python3
"""p65 E1: direction of time/space preposition intrusions in learner error corpora (M2 format).

Registered in p65_error-evidence-registration_2026-11-13.md BEFORE any counting.

Counting rule (annotator 0 only; noop edits skipped):
  an edit is an INTRUSION from domain X into domain Y when the learner's original span,
  lowercased and whitespace-normalised, equals a term of X and the correction equals a term of Y.
  E1:  S->T  (spatial term written where a temporal term is required)  vs  T->S.
  C1 (negative control): T1 {before, after} <-> T2 {during, until, till, since}.
  C2 (negative control): V (vertical spatial) <-> F (frontal spatial).
Primary statistic: p = n(X->Y) / (n(X->Y) + n(Y->X)), Clopper-Pearson 95% interval; null 0.5
(source-frequency x target-frequency model, which is symmetric).
Secondary: opportunity-normalised rate ratio; per-corpus replication; contains-match sensitivity;
dedicated-ness check of the sets; native (LOCNESS N.dev) counts.

Usage: python3 -I p65_error_intrusion_count.py --learner F1.m2 F2.m2 ... --native N.dev.m2 [--examples OUT.tsv]
Corpus label of each file = its basename up to the first '.'.
"""
import argparse
import math
import os
import sys
from collections import Counter

T = ["before", "after", "during", "until", "till", "'til", "since", "prior to"]
S = ["in front of", "behind", "above", "below", "beneath", "under", "underneath", "beside",
     "next to", "inside", "outside", "opposite", "across", "along", "alongside", "into", "onto",
     "near", "on top of"]
T1 = ["before", "after"]
T2 = ["during", "until", "till", "'til", "since"]
V = ["above", "below", "beneath", "under", "underneath", "on top of"]
F = ["in front of", "behind", "opposite"]

TIME_NOUNS = set("""monday tuesday wednesday thursday friday saturday sunday january february march april may
june july august september october november december morning afternoon evening night weekend summer winter
spring autumn christmas easter o'clock noon midnight hour hours minute minutes moment century week weeks month
months year years day days lunch dinner breakfast class lesson lessons exam exams holiday holidays war
meal party concert show film match trip journey""".split())
PLACE_NOUNS = set("""house home school city town street room park hotel restaurant country village london
centre center shop shops station airport beach office building kitchen garden floor corner cinema theatre
theater club bus train car table door window wall tree trees river sea mountain mountains hill bridge road
church museum bed desk stage building sky ground water box bag""".split())

PAIRS = {
    "E1": ("S", S, "T", T),
    "C1": ("T1", T1, "T2", T2),
    "C2": ("V", V, "F", F),
}


def norm(s):
    return " ".join(s.lower().split())


def read_m2(path):
    """Yield (orig_tokens, edits) per sentence; edits = list of (start, end, type, corr) for annotator 0."""
    with open(path, encoding="utf-8") as fh:
        block = []
        for line in fh:
            line = line.rstrip("\n")
            if not line.strip():
                if block:
                    yield parse_block(block)
                    block = []
            else:
                block.append(line)
        if block:
            yield parse_block(block)


def parse_block(block):
    toks = block[0][2:].split(" ") if block[0].startswith("S ") else []
    edits = []
    for ln in block[1:]:
        if not ln.startswith("A "):
            continue
        parts = ln[2:].split("|||")
        span = parts[0].split()
        s, e = int(span[0]), int(span[1])
        etype, corr, ann = parts[1], parts[2], parts[-1].strip()
        if ann != "0" or etype == "noop" or s < 0:
            continue
        corr = "" if corr == "-NONE-" else corr
        edits.append((s, e, etype, corr))
    return toks, edits


def corrected(toks, edits):
    out = list(toks)
    for s, e, _t, c in sorted(edits, key=lambda x: (-x[0], -x[1])):
        out[s:e] = c.split() if c else []
    return out


def count_terms(tokens, terms):
    low = [t.lower() for t in tokens]
    n = 0
    hits = []
    for term in terms:
        tt = term.split()
        k = len(tt)
        for i in range(len(low) - k + 1):
            if low[i:i + k] == tt:
                n += 1
                hits.append((i, i + k))
    return n, hits


def contains(span, terms):
    low = norm(span).split()
    for term in terms:
        tt = term.split()
        for i in range(len(low) - len(tt) + 1):
            if low[i:i + len(tt)] == tt:
                return True
    return False


def binom_cdf(k, n, p):
    return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(0, k + 1))


def clopper_pearson(k, n, alpha=0.05):
    if n == 0:
        return (float("nan"), float("nan"))

    def solve(f, target):
        lo, hi = 0.0, 1.0
        for _ in range(200):
            mid = (lo + hi) / 2
            if f(mid) > target:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2
    lower = 0.0 if k == 0 else solve_lower(k, n, alpha)
    upper = 1.0 if k == n else solve(lambda p: binom_cdf(k, n, p), alpha / 2)
    return lower, upper


def solve_lower(k, n, alpha):
    # lower bound: P(X >= k | p) = alpha/2, increasing in p
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if 1 - binom_cdf(k - 1, n, mid) < alpha / 2:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def analyse(files, examples=None):
    res = {"pairs": Counter(), "contains": Counter(), "opp_corr": Counter(), "opp_orig": Counter(),
           "percorpus": Counter(), "dedic": Counter(), "sent": 0, "tok": 0, "edits": 0,
           "pairwords": Counter()}
    for path in files:
        corpus = os.path.basename(path).split(".")[0]
        for toks, edits in read_m2(path):
            res["sent"] += 1
            res["tok"] += len(toks)
            res["edits"] += len(edits)
            cor = corrected(toks, edits)
            for name, terms in (("T", T), ("S", S), ("T1", T1), ("T2", T2), ("V", V), ("F", F)):
                res["opp_corr"][name] += count_terms(cor, terms)[0]
                res["opp_orig"][name] += count_terms(toks, terms)[0]
            # dedicated-ness: next 1-3 tokens after a T term contain a place noun; after an S term a time noun
            low = [t.lower() for t in cor]
            for dom, terms, nouns in (("T", T, PLACE_NOUNS), ("S", S, TIME_NOUNS)):
                _, hits = count_terms(cor, terms)
                for _s, e in hits:
                    res["dedic"][dom + "_n"] += 1
                    if any(w in nouns for w in low[e:e + 3]):
                        res["dedic"][dom + "_cross"] += 1
            for s, e, etype, c in edits:
                o = norm(" ".join(toks[s:e]))
                cc = norm(c)
                for pname, (xa, xs, ya, ys) in PAIRS.items():
                    for src_n, src, dst_n, dst in ((xa, xs, ya, ys), (ya, ys, xa, xs)):
                        key = (pname, src_n + "->" + dst_n)
                        if o in src and cc in dst:
                            res["pairs"][key] += 1
                            res["percorpus"][(corpus,) + key] += 1
                            res["pairwords"][(pname, o + " -> " + cc)] += 1
                            if examples is not None:
                                examples.append((corpus, pname, o, cc, etype, " ".join(toks)))
                        if (contains(o, src) and contains(cc, dst) and not contains(o, dst)
                                and not contains(cc, src)):
                            res["contains"][key] += 1
    return res


def report(res, label):
    out = [f"## {label}", f"sentences {res['sent']:,}; tokens {res['tok']:,}; annotator-0 edits {res['edits']:,}"]
    out.append("opportunities (term tokens) corrected text: " + ", ".join(
        f"{k} {v:,}" for k, v in sorted(res["opp_corr"].items())))
    out.append("opportunities original text: " + ", ".join(f"{k} {v:,}" for k, v in sorted(res["opp_orig"].items())))
    d = res["dedic"]
    for dom in ("T", "S"):
        n = d[dom + "_n"]
        out.append(f"dedicated-ness check {dom}: {d[dom + '_cross']}/{n} = "
                   f"{(d[dom + '_cross'] / n if n else float('nan')):.3f} followed (<=3 tokens) by other-domain noun")
    for pname, (xa, _xs, ya, _ys) in PAIRS.items():
        a = res["pairs"][(pname, xa + "->" + ya)]
        b = res["pairs"][(pname, ya + "->" + xa)]
        n = a + b
        lo, hi = clopper_pearson(a, n)
        p = a / n if n else float("nan")
        line = f"{pname}: n({xa}->{ya}) = {a}, n({ya}->{xa}) = {b}, p = {p:.3f} (95% {lo:.3f}-{hi:.3f}), n = {n}"
        ox, oy = res["opp_corr"][ya], res["opp_corr"][xa]
        if a and b and ox and oy:
            rr = (a / ox) / (b / oy)
            line += f"; opportunity-normalised RR = {rr:.3f}"
        ca = res["contains"][(pname, xa + "->" + ya)]
        cb = res["contains"][(pname, ya + "->" + xa)]
        line += f"; contains-match {ca} vs {cb}"
        out.append(line)
        for k, v in sorted(res["percorpus"].items()):
            if k[1] == pname:
                out.append(f"    {k[0]} {k[2]}: {v}")
    out.append("word pairs (orig -> corr): ")
    for (pname, w), v in sorted(res["pairwords"].items(), key=lambda x: (x[0][0], -x[1])):
        out.append(f"    {pname} {w}: {v}")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--learner", nargs="+", required=True)
    ap.add_argument("--native", nargs="*", default=[])
    ap.add_argument("--examples")
    a = ap.parse_args()
    ex = [] if a.examples else None
    print(report(analyse(a.learner, ex), "LEARNER (pooled)"))
    if a.native:
        print()
        print(report(analyse(a.native, ex), "NATIVE (LOCNESS)"))
    if a.examples:
        with open(a.examples, "w", encoding="utf-8") as fh:
            for row in ex:
                fh.write("\t".join(row) + "\n")


if __name__ == "__main__":
    sys.exit(main())
